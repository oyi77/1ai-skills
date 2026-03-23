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
        known = {d["serial"] for d in db.get_all_devices()}
        for serial in connected:
            if serial not in known:
                # Auto-register unknown device
                db.upsert_device(serial=serial, name=serial, connected=1,
                                 last_seen=time.time())
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
                serial=serial, name=name, model=model,
                android_ver=android, battery=battery,
                screen_on=int(screen_on), connected=1,
                current_app=current_app, last_seen=state.last_seen,
                error_count=0, last_error="",
            )
        except Exception as e:
            state.connected = True  # We know it's connected (from discover())
            state.last_error = str(e)
            state.error_count = (db.get_device(serial) or {}).get("error_count", 0) + 1
            db.upsert_device(serial=serial, error_count=state.error_count,
                             last_error=str(e))
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
        results = self.pool.run_parallel(
            serials, self.refresh_device, timeout=60
        )
        elapsed = time.time() - t0
        ok = sum(1 for v in results.values() if isinstance(v, DeviceState) and v.connected)
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
            results.append({
                "serial": serial,
                "name": device.get("name", serial),
                "model": state.model,
                "battery": state.battery,
                "screen_on": state.screen_on,
                "connected": state.connected,
                "current_app": state.current_app,
                "issues": issues,
                "status": "healthy" if not issues else "degraded",
            })
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
            if r.returncode == 0 and Path(path).exists() and Path(path).stat().st_size > 1000:
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
        self.pool.shell_root(serial, f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
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
                    m = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
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
        raw = self.pool.shell(serial, "dumpsys notification --noredact | grep 'android.title'")
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
            db.upsert_device(serial=serial, name=name or serial,
                             connection="wifi", enabled=1, connected=1,
                             last_seen=time.time())
        return ok

    def register_device(self, serial: str, name: str, **kwargs):
        """Manually register a new device."""
        db.upsert_device(serial=serial, name=name, enabled=1, **kwargs)
        is_wifi = kwargs.get("connection") == "wifi"
        self.pool.register_device(serial, is_wifi=is_wifi)

    def list_devices(self, connected_only: bool = False) -> list[dict]:
        return db.get_all_devices(connected_only=connected_only)

    def get_stats(self) -> dict:
        pool_status = self.pool.get_server_status()
        db_stats = db.get_stats()
        return {
            **db_stats,
            "adb_servers": len(pool_status),
            "server_details": pool_status,
        }

    def shutdown(self):
        self._executor.shutdown(wait=False)
        self.pool.shutdown()


# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", nargs="?", default="status",
                        choices=["status", "discover", "refresh", "health"])
    args = parser.parse_args()

    dm = DeviceManager()
    if args.cmd in ("status", "discover"):
        connected = dm.discover()
        print(f"Connected: {connected}")
        print(json.dumps(dm.get_stats(), indent=2))
    elif args.cmd == "refresh":
        states = dm.refresh_all()
        print(json.dumps({s: asdict(d) for s, d in states.items()}, indent=2, default=str))
    elif args.cmd == "health":
        results = dm.health_check_all()
        print(json.dumps(results, indent=2))
