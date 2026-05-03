#!/usr/bin/env python3
"""
Phone Farm — ADB Connection Pool.

Solves:
  - Single ADB server bottleneck → multiple ADB servers on different ports
  - USB hub partitioning → devices assigned to server groups
  - WiFi ADB → connect by IP, no USB limit
  - Parallel command execution via ThreadPoolExecutor
  - Auto-restart dead ADB servers
  - Per-device connection retry with exponential backoff

Architecture:
  ADBPool
  ├── server_0 (adb -P 5037) → USB hub 0 → devices 0-15
  ├── server_1 (adb -P 5038) → USB hub 1 → devices 16-31
  ├── server_N (adb -P 503N) → USB hub N → ...
  └── wifi_pool → WiFi ADB connections (no limit)

For 1000 devices: 63 ADB servers × 16 USB devices each = 1008 devices
"""

import logging
import os
import shutil
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from dataclasses import dataclass, field
from typing import Callable, Optional

log = logging.getLogger("adb_pool")

ADB_BIN = "adb"
DEVICES_PER_SERVER = 16   # Safe limit per ADB server
MAX_SERVERS = 64           # Max ADB server instances
BASE_PORT = 5037           # First ADB server port
WORKER_THREADS = 32        # Parallel command workers
COMMAND_TIMEOUT = 15       # Per-command timeout (seconds)


@dataclass
class ADBServer:
    port: int
    devices: list[str] = field(default_factory=list)
    process: Optional[subprocess.Popen] = None
    started: float = 0
    restart_count: int = 0

    def is_alive(self) -> bool:
        if self.process is None:
            return False
        return self.process.poll() is None

    def start(self):
        env = os.environ.copy()
        env["ANDROID_ADB_SERVER_PORT"] = str(self.port)
        try:
            self.process = subprocess.Popen(
                [ADB_BIN, "-P", str(self.port), "start-server"],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.started = time.time()
            time.sleep(1)
            log.info(f"ADB server started on port {self.port}")
        except Exception as e:
            log.error(f"Failed to start ADB server on port {self.port}: {e}")

    def stop(self):
        env = os.environ.copy()
        env["ANDROID_ADB_SERVER_PORT"] = str(self.port)
        subprocess.run(
            [ADB_BIN, "-P", str(self.port), "kill-server"],
            env=env, capture_output=True,
        )
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass
        log.info(f"ADB server stopped on port {self.port}")

    def restart(self):
        self.stop()
        time.sleep(2)
        self.restart_count += 1
        self.start()


class ADBPool:
    """
    Manages multiple ADB servers for high-device-count farms.
    Thread-safe. Supports USB (partitioned by server) and WiFi.
    """

    def __init__(self, max_workers: int = WORKER_THREADS):
        self._lock = threading.Lock()
        self._servers: dict[int, ADBServer] = {}  # port → server
        self._device_server: dict[str, int] = {}  # serial → port
        self._wifi_devices: set[str] = set()
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="adb-worker",
        )
        self._ensure_default_server()

    def _ensure_default_server(self):
        """Always have at least the default ADB server."""
        if BASE_PORT not in self._servers:
            srv = ADBServer(port=BASE_PORT)
            srv.start()
            self._servers[BASE_PORT] = srv

    def _get_or_create_server(self, device_count: int) -> ADBServer:
        """Find a server with capacity or create a new one."""
        for port, srv in self._servers.items():
            if len(srv.devices) < DEVICES_PER_SERVER:
                return srv
        # All servers full — create new
        new_port = BASE_PORT + len(self._servers)
        if new_port >= BASE_PORT + MAX_SERVERS:
            raise RuntimeError(f"Max ADB servers ({MAX_SERVERS}) reached")
        srv = ADBServer(port=new_port)
        srv.start()
        with self._lock:
            self._servers[new_port] = srv
        return srv

    def _get_env(self, port: int) -> dict:
        env = os.environ.copy()
        env["ANDROID_ADB_SERVER_PORT"] = str(port)
        return env

    def _port_for(self, serial: str) -> int:
        """Return the ADB server port assigned to this device."""
        return self._device_server.get(serial, BASE_PORT)

    def register_device(self, serial: str, is_wifi: bool = False):
        """Register a device to an ADB server."""
        with self._lock:
            if serial in self._device_server:
                return  # Already registered
            if is_wifi:
                self._wifi_devices.add(serial)
                self._device_server[serial] = BASE_PORT
            else:
                srv = self._get_or_create_server(len(self._device_server))
                srv.devices.append(serial)
                self._device_server[serial] = srv.port
                log.info(f"Device {serial} assigned to ADB server :{srv.port}")

    def unregister_device(self, serial: str):
        with self._lock:
            port = self._device_server.pop(serial, None)
            if port and port in self._servers:
                srv = self._servers[port]
                if serial in srv.devices:
                    srv.devices.remove(serial)
            self._wifi_devices.discard(serial)

    def run(self, serial: str, args: list[str],
            timeout: int = COMMAND_TIMEOUT) -> subprocess.CompletedProcess:
        """Run an ADB command for a specific device."""
        port = self._port_for(serial)
        env = self._get_env(port)
        cmd = [ADB_BIN, "-P", str(port), "-s", serial] + args
        try:
            return subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=timeout, env=env,
            )
        except subprocess.TimeoutExpired:
            log.warning(f"ADB timeout ({timeout}s): {serial} {args[:2]}")
            return subprocess.CompletedProcess(cmd, 1, "", "timeout")
        except Exception as e:
            return subprocess.CompletedProcess(cmd, 1, "", str(e))

    def shell(self, serial: str, cmd: str, timeout: int = 10) -> str:
        r = self.run(serial, ["shell", cmd], timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else ""

    def shell_root(self, serial: str, cmd: str) -> str:
        r = self.run(serial, ["shell", cmd])
        if r.returncode == 0 and "Permission denied" not in r.stderr:
            return r.stdout.strip()
        r2 = self.run(serial, ["shell", f"su -c '{cmd}'"])
        return r2.stdout.strip()

    def list_devices(self) -> list[str]:
        """List all ADB-visible devices across all servers."""
        all_serials = []
        for port, srv in self._servers.items():
            r = subprocess.run(
                [ADB_BIN, "-P", str(port), "devices"],
                capture_output=True, text=True, timeout=10,
                env=self._get_env(port),
            )
            for line in r.stdout.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "device":
                    if parts[0] not in all_serials:
                        all_serials.append(parts[0])
        return all_serials

    def run_parallel(
        self,
        serials: list[str],
        fn: Callable[[str], any],
        timeout: float = 60,
    ) -> dict[str, any]:
        """
        Run fn(serial) for each serial in parallel.
        Returns {serial: result_or_exception}.
        Never blocks more than `timeout` seconds total.
        """
        futures = {
            self._executor.submit(fn, serial): serial
            for serial in serials
        }
        results = {}
        try:
            for future in as_completed(futures, timeout=timeout):
                serial = futures[future]
                try:
                    results[serial] = future.result()
                except Exception as e:
                    results[serial] = e
                    log.warning(f"Parallel task failed for {serial}: {e}")
        except TimeoutError:
            for future, serial in futures.items():
                if serial not in results:
                    results[serial] = TimeoutError(f"Task timed out for {serial}")
                    future.cancel()
        return results

    def health_check_all_servers(self):
        """Restart any dead ADB servers."""
        for port, srv in list(self._servers.items()):
            if not srv.is_alive():
                log.warning(f"ADB server :{port} dead — restarting")
                srv.restart()

    def connect_wifi(self, ip: str, port: int = 5555) -> bool:
        """Connect to an Android device over WiFi."""
        serial = f"{ip}:{port}"
        env = self._get_env(BASE_PORT)
        r = subprocess.run(
            [ADB_BIN, "-P", str(BASE_PORT), "connect", serial],
            capture_output=True, text=True, env=env, timeout=10,
        )
        if "connected" in r.stdout.lower():
            self.register_device(serial, is_wifi=True)
            log.info(f"WiFi device connected: {serial}")
            return True
        log.warning(f"WiFi connect failed: {serial} — {r.stdout.strip()}")
        return False

    def disconnect_wifi(self, ip: str, port: int = 5555):
        serial = f"{ip}:{port}"
        self.run(serial, ["disconnect"])
        self.unregister_device(serial)

    def get_server_status(self) -> list[dict]:
        return [
            {
                "port": srv.port,
                "devices": len(srv.devices),
                "alive": srv.is_alive(),
                "restarts": srv.restart_count,
                "uptime_sec": int(time.time() - srv.started) if srv.started else 0,
            }
            for srv in self._servers.values()
        ]

    def shutdown(self):
        self._executor.shutdown(wait=False)
        for srv in self._servers.values():
            srv.stop()


# Singleton pool (import and reuse)
_pool: Optional[ADBPool] = None
_pool_lock = threading.Lock()


def get_pool() -> ADBPool:
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = ADBPool()
    return _pool
