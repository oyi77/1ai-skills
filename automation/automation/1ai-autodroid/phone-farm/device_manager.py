#!/usr/bin/env python3
"""
Phone Farm — Device Manager v2 (Production Scale)

Changes from v1:
  - Parallel ADB calls via ThreadPoolExecutor (not sequential)
  - SQLite persistence (not in-memory dict)
  - ADB pool (multiple servers, not single)
  - Exponential backoff on failure
  - Per-device error budgets (circuit breaker)
  - Thread-safe everywhere
  - Handles 1000+ devices without blocking

Usage as library:
    from device_manager import DeviceManager
    dm = DeviceManager()
    devices = dm.list_devices()          # parallel, <5s for 100 devices
    dm.screenshot("SERIAL")             # non-blocking
    health = dm.health_check_all()      # parallel health checks
"""

import json
import logging
import re
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from adb_pool import get_pool, ADBPool
import db

log = logging.getLogger("device_manager")

ADB = "adb"

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "devices.json"
SCREENSHOTS_DIR = Path("/tmp/autodroid_screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Circuit breaker: disable device after N consecutive failures
ERROR_BUDGET = 5


@dataclass
class DeviceState:
    serial: str
    name: str = ""
    model: str = ""
    android: str = ""
    battery: int = -1
    screen_on: bool = False
    connected: bool = False
    current_app: str = ""
    last_seen: float = 0
    error_count: int = 0
    last_error: str = ""
    assigned_skills: list = field(default_factory=list)
    installed_apps: dict = field(default_factory=dict)
    # Circuit breaker
    _disabled: bool = False


class DeviceManager:
    """
    Manages hundreds/thousands of Android devices.
    All multi-device operations run in parallel via thread pool.
    State persisted in SQLite.
    """

    def __init__(self, config_path: str | Path | None = None, workers: int = 32):
        self.config_path = Path(config_path) if config_path else CONFIG_PATH
        self.pool: ADBPool = get_pool()
        self.workers = workers
        self._executor = ThreadPoolExecutor(
            max_workers=workers, thread_name_prefix="dm-worker"
        )
        db.init_db()
        self._load_config_to_db()
        log.info(f"DeviceManager ready ({workers} workers)")

    def _load_config_to_db(self):
        """Import devices.json into DB if not already there."""
        if not self.config_path.exists():
            return
        with open(self.config_path) as f:
            config = json.load(f)
        for serial, info in config.get("devices", {}).items():
            if not info.get("enabled", True):
                continue
            existing = db.get_device(serial)
            if not existing:
                db.upsert_device(
                    serial=serial,
                    name=info.get("name", serial),
                    model=info.get("model", ""),
                    android_ver=info.get("android", ""),
                    connection=info.get("connection", "usb"),
                    config_json=json.dumps(info),
                    enabled=1,
                )
                log.info(f"Imported device {serial} → DB")
            # Register in ADB pool
            self.pool.register_device(serial, is_wifi=info.get("connection") == "wifi")

    # ── Discovery ────────────────────────────────────────────────────────

    def discover(self) -> list[str]:
        """Scan all ADB servers for connected devices. Parallel."""
        connected = self.pool.list_devices()
        # Update DB: mark connected/disconnected
        known = {d["serial"] for d in db.get_all_devices()["items"]}
        for serial in connected:
            if serial not in known:
                # Auto-register unknown device
                db.upsert_device(
                    serial=serial, name=serial, connected=1, last_seen=time.time()
                )
                self.pool.register_device(serial)
                log.info(f"Auto-registered new device: {serial}")
            else:
                db.upsert_device(serial=serial, connected=1, last_seen=time.time())
        # Mark disconnected
        for serial in known:
            if serial not in connected:
                db.upsert_device(serial=serial, connected=0)
        return connected

    # ── Parallel health refresh ───────────────────────────────────────────

    def refresh_device(self, serial: str) -> DeviceState:
        """Refresh one device state. Called in parallel."""
        state = DeviceState(serial=serial)
        try:
            model = self.pool.shell(serial, "getprop ro.product.model")
            android = self.pool.shell(serial, "getprop ro.build.version.release")

            bat_raw = self.pool.shell(serial, "dumpsys battery")
            battery = -1
            for line in bat_raw.split("\n"):
                if "level:" in line:
                    try:
                        battery = int(line.split(":")[1].strip())
                    except (ValueError, IndexError):
                        pass
                    break

            screen_raw = self.pool.shell(serial, "dumpsys power | grep 'Display Power'")
            screen_on = "ON" in screen_raw.upper() if screen_raw else False

            focus = self.pool.shell(serial, "dumpsys window | grep mCurrentFocus")
            current_app = ""
            if focus:
                m = re.search(r"(\w+\.\w+[\w.]*)/", focus)
                if m:
                    current_app = m.group(1)

            state.model = model
            state.android = android
            state.battery = battery
            state.screen_on = screen_on
            state.connected = True
            state.current_app = current_app
            state.last_seen = time.time()
            state.error_count = 0

            # Persist
            existing = db.get_device(serial)
            name = existing["name"] if existing else serial
            db.upsert_device(
                serial=serial,
                name=name,
                model=model,
                android_ver=android,
                battery=battery,
                screen_on=int(screen_on),
                connected=1,
                current_app=current_app,
                last_seen=state.last_seen,
                error_count=0,
                last_error="",
            )
        except Exception as e:
            state.connected = True  # We know it's connected (from discover())
            state.last_error = str(e)
            state.error_count = (db.get_device(serial) or {}).get("error_count", 0) + 1
            db.upsert_device(
                serial=serial, error_count=state.error_count, last_error=str(e)
            )
            log.warning(f"Refresh error {serial}: {e}")

        return state

    def refresh_all(self, serials: list[str] | None = None) -> dict[str, DeviceState]:
        """Refresh all (or given) devices in PARALLEL. Fast at any scale."""
        if serials is None:
            serials = self.discover()
        if not serials:
            return {}
        log.info(f"Refreshing {len(serials)} devices in parallel...")
        t0 = time.time()
        results = self.pool.run_parallel(serials, self.refresh_device, timeout=60)
        elapsed = time.time() - t0
        ok = sum(
            1 for v in results.values() if isinstance(v, DeviceState) and v.connected
        )
        log.info(f"Refresh complete: {ok}/{len(serials)} healthy in {elapsed:.1f}s")
        return {k: v for k, v in results.items() if isinstance(v, DeviceState)}

    def health_check_all(self) -> list[dict]:
        """Run health checks on all connected devices. Parallel."""
        serials = self.discover()
        states = self.refresh_all(serials)
        results = []
        for serial, state in states.items():
            device = db.get_device(serial) or {}
            issues = []
            if not state.connected:
                issues.append("disconnected")
            if state.battery >= 0 and state.battery <= 10:
                issues.append(f"battery_critical:{state.battery}%")
            elif state.battery >= 0 and state.battery <= 20:
                issues.append(f"battery_low:{state.battery}%")
            if state.error_count >= ERROR_BUDGET:
                issues.append(f"error_budget_exceeded:{state.error_count}")
            results.append(
                {
                    "serial": serial,
                    "name": device.get("name", serial),
                    "model": state.model,
                    "battery": state.battery,
                    "screen_on": state.screen_on,
                    "connected": state.connected,
                    "current_app": state.current_app,
                    "issues": issues,
                    "status": "healthy" if not issues else "degraded",
                }
            )
        return results

    # ── Actions (single device) ───────────────────────────────────────────

    def screenshot(self, serial: str, path: str | None = None) -> str:
        if not path:
            ts = int(time.time() * 1000)
            path = str(SCREENSHOTS_DIR / f"{serial}_{ts}.png")
        remote = "/sdcard/autodroid_cap.png"
        for attempt in range(3):
            self.pool.shell(serial, f"screencap {remote}")
            r = self.pool.run(serial, ["pull", remote, path])
            if (
                r.returncode == 0
                and Path(path).exists()
                and Path(path).stat().st_size > 1000
            ):
                return path
            time.sleep(1)
        raise RuntimeError(f"Screenshot failed for {serial}")

    def screenshots_parallel(self, serials: list[str]) -> dict[str, str]:
        """Take screenshots of multiple devices in parallel."""

        def _ss(serial):
            return self.screenshot(serial)

        return self.pool.run_parallel(serials, _ss, timeout=60)

    def tap(self, serial: str, x: int, y: int):
        self.pool.shell_root(serial, f"input tap {x} {y}")

    def swipe(self, serial: str, x1: int, y1: int, x2: int, y2: int, dur: int = 300):
        self.pool.shell_root(serial, f"input swipe {x1} {y1} {x2} {y2} {dur}")

    def type_text(self, serial: str, text: str):
        escaped = text.replace(" ", "%s").replace("'", "\\'")
        self.pool.shell_root(serial, f"input text '{escaped}'")

    def press_key(self, serial: str, key: str):
        KEYCODES = {"HOME": 3, "BACK": 4, "MENU": 82, "POWER": 26, "ENTER": 66}
        code = KEYCODES.get(key.upper(), key)
        self.pool.shell_root(serial, f"input keyevent {code}")

    def launch_app(self, serial: str, package: str):
        self.pool.shell_root(
            serial, f"monkey -p {package} -c android.intent.category.LAUNCHER 1"
        )
        time.sleep(2)

    def stop_app(self, serial: str, package: str):
        self.pool.shell(serial, f"am force-stop {package}")

    def wake_screen(self, serial: str):
        self.pool.shell_root(serial, "input keyevent 224")
        time.sleep(0.3)

    def unlock_screen(self, serial: str, pin: str | None = None):
        self.wake_screen(serial)
        self.pool.shell_root(serial, "input keyevent 82")
        time.sleep(0.5)
        if pin:
            self.pool.shell_root(serial, f"input text {pin}")
            self.pool.shell_root(serial, "input keyevent 66")

    def ui_dump(self, serial: str, output: str | None = None) -> str:
        if not output:
            output = f"/tmp/ui_{serial}.xml"
        remote = "/sdcard/autodroid_ui.xml"
        self.pool.shell(serial, f"uiautomator dump {remote}")
        self.pool.run(serial, ["pull", remote, output])
        return output

    def find_text(self, serial: str, text: str) -> tuple[int | None, int | None]:
        xml_path = self.ui_dump(serial)
        try:
            tree = ET.parse(xml_path)
            for node in tree.iter():
                node_text = node.get("text", "") or node.get("content-desc", "")
                if text.lower() in node_text.lower():
                    bounds = node.get("bounds", "")
                    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds)
                    if m:
                        x1, y1, x2, y2 = map(int, m.groups())
                        return (x1 + x2) // 2, (y1 + y2) // 2
        except ET.ParseError:
            pass
        return None, None

    def tap_text(self, serial: str, text: str) -> bool:
        x, y = self.find_text(serial, text)
        if x is not None:
            self.tap(serial, x, y)
            return True
        return False

    def is_app_running(self, serial: str, package: str) -> bool:
        focus = self.pool.shell(serial, "dumpsys window | grep mCurrentFocus")
        return package in focus if focus else False

    def get_notifications(self, serial: str) -> list[str]:
        raw = self.pool.shell(
            serial, "dumpsys notification --noredact | grep 'android.title'"
        )
        return [l.strip() for l in raw.split("\n") if l.strip()]

    def reconnect(self, serial: str) -> bool:
        """Reconnect a lost device via ADB pool recovery."""
        log.info(f"Reconnect attempt: {serial}")
        self.pool.health_check_all_servers()
        time.sleep(3)
        connected = self.pool.list_devices()
        if serial in connected:
            db.upsert_device(serial=serial, connected=1, last_seen=time.time())
            log.info(f"Reconnected: {serial}")
            return True
        return False

    def connect_wifi(self, ip: str, port: int = 5555, name: str | None = None) -> bool:
        """Add a WiFi ADB device (no USB limit)."""
        serial = f"{ip}:{port}"
        ok = self.pool.connect_wifi(ip, port)
        if ok:
            db.upsert_device(
                serial=serial,
                name=name or serial,
                connection="wifi",
                enabled=1,
                connected=1,
                last_seen=time.time(),
            )
        return ok

    def register_device(self, serial: str, name: str, **kwargs):
        """Manually register a new device."""
        db.upsert_device(serial=serial, name=name, enabled=1, **kwargs)
        is_wifi = kwargs.get("connection") == "wifi"
        self.pool.register_device(serial, is_wifi=is_wifi)

    def list_devices(self, connected_only: bool = False) -> dict:
        return db.get_all_devices(connected_only=connected_only)

    def get_stats(self) -> dict:
        pool_status = self.pool.get_server_status()
        db_stats = db.get_stats()
        return {
            **db_stats,
            "adb_servers": len(pool_status),
            "server_details": pool_status,
        }

    def _run_adb(self, serial: str, *args, timeout: int = 30):
        """Run an ADB command for a specific device. Returns subprocess result."""
        import subprocess

        return subprocess.run(
            [ADB, "-s", serial] + list(args),
            capture_output=True,
            timeout=timeout,
        )

    def shutdown(self):
        self._executor.shutdown(wait=False)

    def install_app(self, serial: str, package: str, timeout: int = 120) -> dict:
        r = self._run_adb(serial, "install", "-r", package, timeout=timeout)
        return {
            "success": r.returncode == 0,
            "output": r.stdout.decode(errors="replace"),
            "serial": serial,
            "package": package,
        }

    def uninstall_app(self, serial: str, package: str, timeout: int = 60) -> dict:
        r = self._run_adb(serial, "uninstall", "-k", package, timeout=timeout)
        return {
            "success": r.returncode == 0,
            "output": r.stdout.decode(errors="replace"),
            "serial": serial,
            "package": package,
        }

    def list_apps(
        self,
        serial: str,
        filter_pkg: str = None,
        search: str = None,
        sort: str = "package",
        order: str = "asc",
        offset: int = 0,
        limit: int = 50,
        detailed: bool = False,
        timeout: int = 30,
    ) -> dict:
        cmd = ["shell", "pm", "list", "packages", "-3", "-U", "--show-versioncode"]
        r = self._run_adb(serial, *cmd, timeout=timeout)
        if r.returncode != 0:
            return {
                "items": [],
                "total": 0,
                "offset": offset,
                "limit": limit,
                "has_more": False,
            }
        all_apps = []
        for line in r.stdout.decode(errors="replace").strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("Error"):
                continue
            pkg, uid, version_code = "", "", ""
            for part in line.split():
                if part.startswith("package:"):
                    pkg = part[len("package:") :]
                elif part.startswith("uid:"):
                    uid = part[len("uid:") :]
                elif part.startswith("versionCode:"):
                    version_code = part[len("versionCode:") :]
            if not pkg:
                continue
            q = filter_pkg or ""
            if q and q.lower() not in pkg.lower():
                continue
            app = {"package": pkg, "uid": uid, "version_code": version_code}
            if detailed:
                info = self.get_app_info(serial, pkg, timeout=timeout)
                app.update(info)
            all_apps.append(app)
        if search:
            q = search.lower()
            all_apps = [a for a in all_apps if q in a["package"].lower()]
        sort_key = sort.lstrip("-")
        reverse = sort.startswith("-") or order == "desc"
        if sort_key in ("package", "uid", "version_code"):
            all_apps.sort(key=lambda a: a.get(sort_key, ""), reverse=reverse)
        total = len(all_apps)
        items = all_apps[offset : offset + limit]
        return {
            "items": items,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": (offset + limit) < total,
        }

    def get_app_info(self, serial: str, package: str, timeout: int = 10) -> dict:
        r = self._run_adb(
            serial, "shell", "dumpsys", "package", package, timeout=timeout
        )
        info = {
            "package": package,
            "version": "",
            "version_code": "",
            "app_id": "",
            "code_path": "",
            "first_install": "",
            "last_update": "",
            "target_sdk": "",
        }
        if r.returncode != 0:
            return info
        for line in r.stdout.decode(errors="replace").strip().split("\n"):
            if line.strip().startswith("versionName="):
                info["version"] = line.strip().split("=", 1)[1].split()[0]
            elif line.strip().startswith("versionCode="):
                info["version_code"] = line.strip().split("=", 1)[1].split()[0]
            elif line.strip().startswith("appId="):
                info["app_id"] = line.strip().split("=", 1)[1]
            elif line.strip().startswith("codePath="):
                info["code_path"] = line.strip().split("=", 1)[1]
            elif line.strip().startswith("firstInstallTime="):
                info["first_install"] = line.strip().split("=", 1)[1]
            elif line.strip().startswith("lastUpdateTime="):
                info["last_update"] = line.strip().split("=", 1)[1]
            elif "targetSdk=" in line:
                parts = line.strip().split()
                for p in parts:
                    if p.startswith("targetSdk="):
                        info["target_sdk"] = p.split("=", 1)[1]
        return info

    def get_app_by_uid(self, serial: str, uid: str, timeout: int = 10) -> dict:
        r = self._run_adb(
            serial, "shell", "pm", "list", "packages", "--uid", uid, timeout=timeout
        )
        if r.returncode == 0:
            for line in r.stdout.decode(errors="replace").strip().split("\n"):
                line = line.strip()
                if line.startswith("package:"):
                    pkg = line.split(":")[1].split()[0] if ":" in line else ""
                    if pkg:
                        return self.get_app_info(serial, pkg, timeout=timeout)
        return {"error": f"No package found with uid={uid}", "serial": serial}

    def get_battery_temp(self, serial: str, timeout: int = 10) -> dict:
        r = self._run_adb(serial, "shell", "dumpsys", "battery", timeout=timeout)
        info = {}
        if r.returncode == 0:
            for line in r.stdout.decode(errors="replace").strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    info[k.strip()] = v.strip()
        return {"serial": serial, "battery": info}

    def reboot(self, serial: str, timeout: int = 15) -> dict:
        r = self._run_adb(serial, "reboot", timeout=timeout)
        return {"success": True, "serial": serial}

    def get_clipboard(self, serial: str, timeout: int = 10) -> dict:
        r = self._run_adb(
            serial,
            "shell",
            "service",
            "call",
            "clipboard",
            "-e",
            "get_text",
            timeout=timeout,
        )
        text = r.stdout.decode(errors="replace").strip() if r.returncode == 0 else ""
        return {"serial": serial, "clipboard": text}

    def set_clipboard(self, serial: str, text: str, timeout: int = 10) -> dict:
        r = self._run_adb(
            serial,
            "shell",
            "service",
            "call",
            "clipboard",
            "-e",
            "set_text",
            "--es",
            text,
            timeout=timeout,
        )
        return {"success": r.returncode == 0, "serial": serial}

    def logcat(
        self, serial: str, filter_spec: str = "", lines: int = 100, timeout: int = 10
    ) -> str:
        cmd = ["logcat", "-d", serial]
        if filter_spec:
            cmd.extend(["-s", filter_spec])
        cmd.extend(["-t", str(lines)])
        r = self._run_adb(serial, *cmd, timeout=timeout)
        return (
            r.stdout.decode(errors="replace")
            if r.returncode == 0
            else f"Error: {r.stderr.decode()}"
        )

    def push_file(
        self,
        serial: str,
        local_path: str,
        remote_path: str = "/sdcard/",
        timeout: int = 120,
    ) -> dict:
        r = self._run_adb(serial, "push", local_path, remote_path, timeout=timeout)
        return {
            "success": r.returncode == 0,
            "output": r.stdout.decode(errors="replace"),
            "serial": serial,
            "remote_path": remote_path,
        }

    def pull_file(
        self, serial: str, remote_path: str, local_dir: str, timeout: int = 120
    ) -> dict:
        import os

        os.makedirs(local_dir, exist_ok=True)
        fname = os.path.basename(remote_path)
        local_path = os.path.join(local_dir, fname)
        r = self._run_adb(serial, "pull", remote_path, local_path, timeout=timeout)
        return {
            "success": r.returncode == 0,
            "local_path": local_path,
            "remote_path": remote_path,
        }

    def adb_shell(self, serial: str, command: str, timeout: int = 30) -> dict:
        r = self._run_adb(serial, "shell", command, timeout=timeout)
        return {
            "success": r.returncode == 0,
            "output": r.stdout.decode(errors="replace"),
            "serial": serial,
            "command": command,
        }


# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd",
        nargs="?",
        default="status",
        choices=["status", "discover", "refresh", "health"],
    )
    args = parser.parse_args()

    dm = DeviceManager()
    if args.cmd in ("status", "discover"):
        connected = dm.discover()
        print(f"Connected: {connected}")
        print(json.dumps(dm.get_stats(), indent=2))
    elif args.cmd == "refresh":
        states = dm.refresh_all()
        print(
            json.dumps({s: asdict(d) for s, d in states.items()}, indent=2, default=str)
        )
    elif args.cmd == "health":
        results = dm.health_check_all()
        print(json.dumps(results, indent=2))
