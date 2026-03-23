#!/usr/bin/env python3
"""
Phone Farm Device Manager — Core device abstraction layer.

Handles:
  - ADB connection management (USB + WiFi)
  - Device health monitoring (battery, connectivity, screen state)
  - Screenshot capture with retry logic
  - App launch/control primitives
  - Auto-reconnect on disconnect
  - UI element interaction (tap, swipe, type, find-text)

Usage as library:
    from device_manager import DeviceManager
    dm = DeviceManager()
    devices = dm.list_devices()
    dm.screenshot("SERIAL", "/tmp/screen.png")
    dm.tap("SERIAL", 360, 820)
    dm.launch_app("SERIAL", "com.shopee.id")
"""

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("device_manager")

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "devices.json"
SCREENSHOTS_DIR = Path("/tmp/autodroid_screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


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


class DeviceManager:
    """Manages ADB devices with health monitoring and auto-recovery."""

    def __init__(self, config_path: str | Path | None = None):
        self.config_path = Path(config_path) if config_path else CONFIG_PATH
        self.config = self._load_config()
        self.adb = self.config.get("farm_settings", {}).get("adb_path", "adb")
        self.max_retries = self.config.get("farm_settings", {}).get("max_retries", 3)
        self.retry_delay = self.config.get("farm_settings", {}).get("retry_delay_sec", 10)
        self.devices: dict[str, DeviceState] = {}
        self._init_devices()

    def _load_config(self) -> dict:
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        log.warning(f"Config not found: {self.config_path}, using defaults")
        return {"devices": {}, "farm_settings": {}}

    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def _init_devices(self):
        for serial, info in self.config.get("devices", {}).items():
            if not info.get("enabled", True):
                continue
            self.devices[serial] = DeviceState(
                serial=serial,
                name=info.get("name", serial),
                model=info.get("model", ""),
                android=info.get("android", ""),
                assigned_skills=info.get("assigned_skills", []),
                installed_apps=info.get("installed_apps", {}),
            )

    # ── ADB helpers ──────────────────────────────────────────────────────

    def _adb(self, args: list[str], serial: str | None = None,
             timeout: int = 15) -> subprocess.CompletedProcess:
        cmd = [self.adb]
        if serial:
            cmd += ["-s", serial]
        cmd += args
        try:
            return subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            log.warning(f"ADB timeout: {' '.join(cmd)}")
            return subprocess.CompletedProcess(cmd, 1, "", "timeout")
        except Exception as e:
            log.error(f"ADB error: {e}")
            return subprocess.CompletedProcess(cmd, 1, "", str(e))

    def _shell(self, serial: str, cmd: str, timeout: int = 10) -> str:
        r = self._adb(["shell", cmd], serial=serial, timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else ""

    def _shell_root(self, serial: str, cmd: str) -> str:
        """Try normal shell, fallback to su."""
        r = self._adb(["shell", cmd], serial=serial)
        if r.returncode == 0 and "Permission denied" not in r.stderr:
            return r.stdout.strip()
        r2 = self._adb(["shell", f"su -c '{cmd}'"], serial=serial)
        return r2.stdout.strip()

    # ── Device Discovery ─────────────────────────────────────────────────

    def list_connected(self) -> list[str]:
        r = self._adb(["devices"])
        if r.returncode != 0:
            return []
        serials = []
        for line in r.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                serials.append(parts[0])
        return serials

    def refresh_all(self) -> dict[str, DeviceState]:
        connected = self.list_connected()
        for serial, state in self.devices.items():
            if serial in connected:
                state.connected = True
                state.last_seen = time.time()
                self._refresh_device(state)
            else:
                state.connected = False
        # Auto-register unknown devices
        for serial in connected:
            if serial not in self.devices:
                log.info(f"New device detected: {serial}")
                state = DeviceState(serial=serial, connected=True, last_seen=time.time())
                self._refresh_device(state)
                self.devices[serial] = state
        return self.devices

    def _refresh_device(self, state: DeviceState):
        try:
            if not state.model:
                state.model = self._shell(state.serial, "getprop ro.product.model")
            if not state.android:
                state.android = self._shell(state.serial, "getprop ro.build.version.release")
            # Battery
            bat = self._shell(state.serial, "dumpsys battery")
            for line in bat.split("\n"):
                if "level:" in line:
                    try:
                        state.battery = int(line.split(":")[1].strip())
                    except (ValueError, IndexError):
                        pass
                    break
            # Screen state
            screen = self._shell(state.serial, "dumpsys power | grep 'Display Power'")
            state.screen_on = "ON" in screen.upper() if screen else False
            # Current app
            focus = self._shell(state.serial, "dumpsys window | grep mCurrentFocus")
            if focus:
                m = re.search(r"(\w+\.\w+[\w.]*)/", focus)
                if m:
                    state.current_app = m.group(1)
            state.error_count = 0
            state.last_error = ""
        except Exception as e:
            state.error_count += 1
            state.last_error = str(e)
            log.error(f"Refresh failed for {state.serial}: {e}")

    # ── Actions ──────────────────────────────────────────────────────────

    def screenshot(self, serial: str, path: str | None = None) -> str:
        if not path:
            ts = int(time.time() * 1000)
            path = str(SCREENSHOTS_DIR / f"{serial}_{ts}.png")
        remote = "/sdcard/autodroid_cap.png"
        for attempt in range(self.max_retries):
            self._shell(serial, f"screencap {remote}")
            r = self._adb(["pull", remote, path], serial=serial)
            if r.returncode == 0 and Path(path).exists() and Path(path).stat().st_size > 1000:
                log.debug(f"Screenshot: {path} ({Path(path).stat().st_size // 1024}KB)")
                return path
            log.warning(f"Screenshot attempt {attempt + 1} failed for {serial}")
            time.sleep(1)
        raise RuntimeError(f"Screenshot failed for {serial} after {self.max_retries} attempts")

    def tap(self, serial: str, x: int, y: int):
        self._shell_root(serial, f"input tap {x} {y}")

    def swipe(self, serial: str, x1: int, y1: int, x2: int, y2: int, duration: int = 300):
        self._shell_root(serial, f"input swipe {x1} {y1} {x2} {y2} {duration}")

    def type_text(self, serial: str, text: str):
        escaped = text.replace(" ", "%s").replace("'", "\\'")
        self._shell_root(serial, f"input text '{escaped}'")

    def press_key(self, serial: str, key: str):
        KEYCODES = {
            "HOME": 3, "BACK": 4, "MENU": 82, "POWER": 26,
            "ENTER": 66, "TAB": 61, "DEL": 67,
        }
        code = KEYCODES.get(key.upper(), key)
        self._shell_root(serial, f"input keyevent {code}")

    def launch_app(self, serial: str, package: str):
        self._shell_root(serial, f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
        time.sleep(2)
        log.info(f"Launched {package} on {serial}")

    def stop_app(self, serial: str, package: str):
        self._shell(serial, f"am force-stop {package}")
        log.info(f"Stopped {package} on {serial}")

    def wake_screen(self, serial: str):
        self._shell_root(serial, "input keyevent 224")  # WAKEUP
        time.sleep(0.3)

    def unlock_screen(self, serial: str, pin: str | None = None):
        self.wake_screen(serial)
        self._shell_root(serial, "input keyevent 82")  # MENU = unlock
        time.sleep(0.5)
        if pin:
            self._shell_root(serial, f"input text {pin}")
            self._shell_root(serial, "input keyevent 66")  # ENTER

    def ui_dump(self, serial: str, output: str = "/tmp/autodroid_ui.xml") -> str:
        remote = "/sdcard/autodroid_ui.xml"
        self._shell(serial, f"uiautomator dump {remote}")
        self._adb(["pull", remote, output], serial=serial)
        return output

    def find_text(self, serial: str, text: str) -> tuple[int | None, int | None]:
        xml_path = f"/tmp/ui_{serial}.xml"
        self.ui_dump(serial, xml_path)
        try:
            tree = ET.parse(xml_path)
            for node in tree.iter():
                node_text = node.get("text", "") or node.get("content-desc", "")
                if text.lower() in node_text.lower():
                    bounds = node.get("bounds", "")
                    match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                    if match:
                        x1, y1, x2, y2 = map(int, match.groups())
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
        focus = self._shell(serial, "dumpsys window | grep mCurrentFocus")
        return package in focus if focus else False

    def get_notifications(self, serial: str) -> list[str]:
        raw = self._shell(serial, "dumpsys notification --noredact | grep 'android.title'")
        return [line.strip() for line in raw.split("\n") if line.strip()]

    # ── Health ───────────────────────────────────────────────────────────

    def health_check(self, serial: str) -> dict:
        state = self.devices.get(serial)
        if not state:
            return {"status": "unknown", "serial": serial}
        self.refresh_all()
        state = self.devices[serial]
        issues = []
        if not state.connected:
            issues.append("disconnected")
        if state.battery >= 0 and state.battery < 15:
            issues.append(f"low_battery:{state.battery}%")
        if state.error_count > 3:
            issues.append(f"errors:{state.error_count}")
        return {
            "status": "healthy" if not issues else "degraded",
            "serial": serial,
            "name": state.name,
            "model": state.model,
            "battery": state.battery,
            "screen_on": state.screen_on,
            "connected": state.connected,
            "current_app": state.current_app,
            "issues": issues,
            "last_seen": datetime.fromtimestamp(state.last_seen).isoformat() if state.last_seen else None,
        }

    def reconnect(self, serial: str) -> bool:
        """Attempt to reconnect a lost device."""
        log.info(f"Attempting reconnect for {serial}")
        # Kill and restart ADB server
        self._adb(["kill-server"])
        time.sleep(2)
        self._adb(["start-server"])
        time.sleep(3)
        connected = self.list_connected()
        if serial in connected:
            log.info(f"Reconnected: {serial}")
            if serial in self.devices:
                self.devices[serial].connected = True
                self.devices[serial].last_seen = time.time()
            return True
        log.warning(f"Reconnect failed for {serial}")
        return False

    def to_dict(self) -> dict:
        return {
            serial: {
                "serial": s.serial,
                "name": s.name,
                "model": s.model,
                "android": s.android,
                "battery": s.battery,
                "screen_on": s.screen_on,
                "connected": s.connected,
                "current_app": s.current_app,
                "error_count": s.error_count,
                "last_error": s.last_error,
                "assigned_skills": s.assigned_skills,
                "last_seen": datetime.fromtimestamp(s.last_seen).isoformat() if s.last_seen else None,
            }
            for serial, s in self.devices.items()
        }


# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    dm = DeviceManager()
    dm.refresh_all()
    print(json.dumps(dm.to_dict(), indent=2))
