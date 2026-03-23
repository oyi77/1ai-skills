#!/usr/bin/env python3
"""
Phone Farm Task Runner — Executes scheduled tasks on Android devices.

Task types:
  - health_check: Monitor battery, connectivity, screen state
  - screenshot: Periodic screenshots for monitoring
  - app_check: Verify apps are running/responsive
  - custom: Run arbitrary ADB commands or skill scripts
  - tiktok_inbox: Check TikTok inbox for messages
  - shopee_orders: Check Shopee for new orders
  - whatsapp_unread: Check WhatsApp unread messages
  - instagram_dms: Check Instagram DMs

Each task produces a TaskResult saved to logs.
"""

import json
import logging
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from device_manager import DeviceManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("task_runner")

LOGS_DIR = Path(__file__).parent.parent.parent / "logs" / "phone-farm"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class TaskResult:
    task_type: str
    device_serial: str
    device_name: str
    timestamp: str
    success: bool
    data: dict
    error: str = ""
    duration_ms: int = 0
    screenshot_path: str = ""


class TaskRunner:
    """Runs tasks on devices via DeviceManager."""

    def __init__(self, dm: DeviceManager | None = None):
        self.dm = dm or DeviceManager()
        self.results: list[TaskResult] = []

    def run_task(self, serial: str, task_type: str, params: dict | None = None) -> TaskResult:
        start = time.time()
        state = self.dm.devices.get(serial)
        name = state.name if state else serial

        try:
            handler = getattr(self, f"_task_{task_type}", None)
            if not handler:
                raise ValueError(f"Unknown task type: {task_type}")
            data = handler(serial, params or {})
            result = TaskResult(
                task_type=task_type,
                device_serial=serial,
                device_name=name,
                timestamp=datetime.now().isoformat(),
                success=True,
                data=data,
                duration_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            log.error(f"Task {task_type} failed on {serial}: {e}")
            result = TaskResult(
                task_type=task_type,
                device_serial=serial,
                device_name=name,
                timestamp=datetime.now().isoformat(),
                success=False,
                data={},
                error=str(e),
                duration_ms=int((time.time() - start) * 1000),
            )

        self.results.append(result)
        self._log_result(result)
        return result

    def _log_result(self, result: TaskResult):
        log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(asdict(result)) + "\n")

    # ── Built-in Tasks ───────────────────────────────────────────────────

    def _task_health_check(self, serial: str, params: dict) -> dict:
        health = self.dm.health_check(serial)
        log.info(
            f"Health [{health['name']}]: battery={health['battery']}% "
            f"connected={health['connected']} screen={health['screen_on']} "
            f"app={health['current_app']} issues={health['issues']}"
        )
        return health

    def _task_screenshot(self, serial: str, params: dict) -> dict:
        path = params.get("path")
        screenshot_path = self.dm.screenshot(serial, path)
        return {"screenshot": screenshot_path, "size_kb": Path(screenshot_path).stat().st_size // 1024}

    def _task_app_check(self, serial: str, params: dict) -> dict:
        """Check if specified apps are installed and get their status."""
        state = self.dm.devices.get(serial)
        if not state:
            return {"error": "device not registered"}
        app_status = {}
        for skill_name, package in state.installed_apps.items():
            running = self.dm.is_app_running(serial, package)
            app_status[skill_name] = {
                "package": package,
                "running": running,
            }
        return {"apps": app_status, "current_focus": state.current_app}

    def _task_check_notifications(self, serial: str, params: dict) -> dict:
        """Get device notifications."""
        notifs = self.dm.get_notifications(serial)
        return {"count": len(notifs), "notifications": notifs[:20]}

    def _task_tiktok_inbox(self, serial: str, params: dict) -> dict:
        """Open TikTok and check inbox for new messages."""
        state = self.dm.devices.get(serial)
        pkg = (state.installed_apps.get("tiktok", "com.ss.android.ugc.trill")
               if state else "com.ss.android.ugc.trill")

        # Check if TikTok is installed
        installed = self.dm._shell(serial, f"pm list packages | grep {pkg}")
        if not installed:
            return {"status": "not_installed", "package": pkg}

        self.dm.wake_screen(serial)
        time.sleep(0.5)
        self.dm.launch_app(serial, pkg)
        time.sleep(3)

        # Take screenshot to see current state
        ss = self.dm.screenshot(serial)

        # Try to navigate to inbox
        found = self.dm.tap_text(serial, "Inbox")
        time.sleep(2)

        ss_inbox = self.dm.screenshot(serial)
        return {
            "status": "checked",
            "screenshot_main": ss,
            "screenshot_inbox": ss_inbox,
            "inbox_tapped": found,
        }

    def _task_shopee_orders(self, serial: str, params: dict) -> dict:
        """Open Shopee and check for new orders."""
        state = self.dm.devices.get(serial)
        pkg = (state.installed_apps.get("shopee", "com.shopee.id")
               if state else "com.shopee.id")

        installed = self.dm._shell(serial, f"pm list packages | grep {pkg}")
        if not installed:
            return {"status": "not_installed", "package": pkg}

        self.dm.wake_screen(serial)
        time.sleep(0.5)
        self.dm.launch_app(serial, pkg)
        time.sleep(4)

        ss = self.dm.screenshot(serial)

        # Try to find order/notification indicators
        found_me = self.dm.tap_text(serial, "Me")
        if not found_me:
            self.dm.tap_text(serial, "Saya")
        time.sleep(2)

        ss_me = self.dm.screenshot(serial)
        return {
            "status": "checked",
            "screenshot_main": ss,
            "screenshot_me": ss_me,
        }

    def _task_whatsapp_unread(self, serial: str, params: dict) -> dict:
        """Open WhatsApp and capture unread messages screenshot."""
        self.dm.wake_screen(serial)
        time.sleep(0.5)
        self.dm.launch_app(serial, "com.whatsapp")
        time.sleep(3)

        ss = self.dm.screenshot(serial)
        return {
            "status": "checked",
            "screenshot": ss,
        }

    def _task_instagram_dms(self, serial: str, params: dict) -> dict:
        """Open Instagram and check DMs."""
        self.dm.wake_screen(serial)
        time.sleep(0.5)
        self.dm.launch_app(serial, "com.instagram.android")
        time.sleep(3)

        ss = self.dm.screenshot(serial)

        # Try to find DM icon (paper plane)
        found = self.dm.tap_text(serial, "Direct")
        time.sleep(2)

        ss_dm = self.dm.screenshot(serial)
        return {
            "status": "checked",
            "screenshot_main": ss,
            "screenshot_dm": ss_dm,
            "dm_tapped": found,
        }

    def _task_go_home(self, serial: str, params: dict) -> dict:
        """Press HOME to go back to launcher."""
        self.dm.press_key(serial, "HOME")
        time.sleep(1)
        ss = self.dm.screenshot(serial)
        return {"status": "home", "screenshot": ss}

    def _task_battery_report(self, serial: str, params: dict) -> dict:
        """Detailed battery report."""
        raw = self.dm._shell(serial, "dumpsys battery")
        data = {}
        for line in raw.split("\n"):
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
        return data

    # ── Batch Operations ─────────────────────────────────────────────────

    def run_all_health_checks(self) -> list[TaskResult]:
        self.dm.refresh_all()
        results = []
        for serial, state in self.dm.devices.items():
            if state.connected:
                results.append(self.run_task(serial, "health_check"))
        return results

    def run_all_screenshots(self) -> list[TaskResult]:
        self.dm.refresh_all()
        results = []
        for serial, state in self.dm.devices.items():
            if state.connected:
                results.append(self.run_task(serial, "screenshot"))
        return results


# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phone Farm Task Runner")
    parser.add_argument("task", nargs="?", default="health_check",
                        choices=["health_check", "screenshot", "app_check",
                                 "check_notifications", "tiktok_inbox",
                                 "shopee_orders", "whatsapp_unread",
                                 "instagram_dms", "go_home", "battery_report"],
                        help="Task to run")
    parser.add_argument("--device", "-d", help="Device serial (default: all)")
    parser.add_argument("--all", "-a", action="store_true", help="Run on all devices")
    args = parser.parse_args()

    runner = TaskRunner()
    runner.dm.refresh_all()

    if args.device:
        result = runner.run_task(args.device, args.task)
        print(json.dumps(asdict(result), indent=2))
    else:
        # Run on all connected
        for serial, state in runner.dm.devices.items():
            if state.connected:
                result = runner.run_task(serial, args.task)
                print(json.dumps(asdict(result), indent=2))
