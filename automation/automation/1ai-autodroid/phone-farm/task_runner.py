#!/usr/bin/env python3
"""
Phone Farm — Task Runner v2 (Production Scale)

Changes from v1:
  - Priority queue instead of sequential loop
  - Per-device task scheduling (not global loop)
  - Non-blocking task submission
  - SQLite results (not JSONL file per day)
  - Retry with exponential backoff per task
  - Dead device auto-skip
  - Parallel multi-device tasks

Task priorities:
  0 = CRITICAL (reconnect, alerts)
  1 = HIGH     (health check, screenshot)
  2 = NORMAL   (inbox check, order check)
  3 = LOW      (background tasks)
"""

import json
import logging
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from queue import PriorityQueue, Empty
from threading import Thread
from typing import Callable, Optional

sys.path.insert(0, str(Path(__file__).parent))
from device_manager import DeviceManager
import db

log = logging.getLogger("task_runner")

PRIORITY_CRITICAL = 0
PRIORITY_HIGH = 1
PRIORITY_NORMAL = 2
PRIORITY_LOW = 3

MAX_RETRIES = 3
RETRY_BACKOFF = [5, 30, 120]  # seconds between retries


@dataclass
class Task:
    priority: int
    serial: str
    task_type: str
    params: dict
    attempt: int = 0
    created_at: float = 0

    def __lt__(self, other):
        return (self.priority, self.created_at) < (other.priority, other.created_at)

    def __le__(self, other):
        return (self.priority, self.created_at) <= (other.priority, other.created_at)


class TaskRunner:
    """
    Priority-queued task runner for phone farm.
    Supports N worker threads consuming from shared queue.
    """

    def __init__(self, dm: DeviceManager | None = None, workers: int = 16):
        self.dm = dm or DeviceManager()
        self._queue: PriorityQueue = PriorityQueue()
        self._workers: list[Thread] = []
        self._running = False
        self._workers_count = workers
        self._handlers: dict[str, Callable] = self._build_handlers()

    def _build_handlers(self) -> dict:
        return {
            "health_check": self._task_health_check,
            "screenshot": self._task_screenshot,
            "app_check": self._task_app_check,
            "check_notifications": self._task_check_notifications,
            "tiktok_inbox": self._task_tiktok_inbox,
            "shopee_orders": self._task_shopee_orders,
            "whatsapp_unread": self._task_whatsapp_unread,
            "instagram_dms": self._task_instagram_dms,
            "go_home": self._task_go_home,
            "battery_report": self._task_battery_report,
            "wake_screen": self._task_wake,
            "unlock": self._task_unlock,
            "launch_app": self._task_launch_app,
        }

    def start(self):
        """Start worker threads."""
        self._running = True
        for i in range(self._workers_count):
            t = Thread(target=self._worker, name=f"task-worker-{i}", daemon=True)
            t.start()
            self._workers.append(t)
        log.info(f"TaskRunner started with {self._workers_count} workers")

    def stop(self):
        self._running = False
        # Poison pills
        for _ in self._workers:
            self._queue.put(None)

    def submit(
        self,
        serial: str,
        task_type: str,
        priority: int = PRIORITY_NORMAL,
        params: dict | None = None,
    ) -> None:
        """Non-blocking task submission."""
        task = Task(
            priority=priority,
            serial=serial,
            task_type=task_type,
            params=params or {},
            created_at=time.time(),
        )
        self._queue.put(task)

    def submit_all(
        self,
        serials: list[str],
        task_type: str,
        priority: int = PRIORITY_NORMAL,
        params: dict | None = None,
    ):
        """Submit same task for all devices."""
        for serial in serials:
            self.submit(serial, task_type, priority, params)

    def run_now(self, serial: str, task_type: str, params: dict | None = None) -> dict:
        """Synchronous task run (bypasses queue). Returns result dict."""
        return self._execute(serial, task_type, params or {})

    def _worker(self):
        while self._running:
            try:
                task = self._queue.get(timeout=5)
                if task is None:
                    break
                # Check if device is alive (skip dead devices)
                device = db.get_device(task.serial)
                if (
                    device
                    and not device.get("connected", 0)
                    and device.get("error_count", 0) > 5
                ):
                    log.debug(
                        f"Skipping task {task.task_type} — device {task.serial} dead"
                    )
                    self._queue.task_done()
                    continue
                try:
                    self._execute_task(task)
                except Exception as e:
                    log.error(f"Worker error on {task.serial}: {e}")
                finally:
                    self._queue.task_done()
            except Empty:
                continue

    def _execute_task(self, task: Task):
        try:
            result = self._execute(task.serial, task.task_type, task.params)
            log.debug(f"Task {task.task_type} on {task.serial}: OK")
        except Exception as e:
            log.warning(
                f"Task {task.task_type} on {task.serial} failed (attempt {task.attempt + 1}): {e}"
            )
            if task.attempt < MAX_RETRIES - 1:
                delay = RETRY_BACKOFF[min(task.attempt, len(RETRY_BACKOFF) - 1)]
                task.attempt += 1
                task.created_at = time.time() + delay  # Schedule future execution
                self._queue.put(task)

    def _execute(self, serial: str, task_type: str, params: dict) -> dict:
        handler = self._handlers.get(task_type)
        if not handler:
            raise ValueError(f"Unknown task: {task_type}")
        t0 = time.time()
        device = db.get_device(serial) or {}
        name = device.get("name", serial)
        success = False
        data = {}
        error = ""
        screenshot = ""
        try:
            data = handler(serial, params)
            success = True
        except Exception as e:
            error = str(e)
            raise
        finally:
            duration_ms = int((time.time() - t0) * 1000)
            db.insert_task(
                serial=serial,
                device_name=name,
                task_type=task_type,
                success=success,
                data=data,
                error=error,
                duration_ms=duration_ms,
                screenshot=screenshot,
            )
        return data

    # ── Task Implementations ─────────────────────────────────────────────

    def _task_health_check(self, serial: str, params: dict) -> dict:
        states = self.dm.refresh_all([serial])
        state = states.get(serial)
        if not state:
            return {"status": "no_state"}
        device = db.get_device(serial) or {}
        issues = []
        if state.battery >= 0 and state.battery <= 10:
            issues.append(f"battery_critical:{state.battery}%")
            if not db.is_alert_recent(serial, "battery_critical"):
                db.insert_alert(
                    serial,
                    "battery_critical",
                    f"🔴 {device.get('name', serial)} battery: {state.battery}%",
                )
        elif state.battery >= 0 and state.battery <= 20:
            issues.append(f"battery_low:{state.battery}%")
            if not db.is_alert_recent(serial, "battery_low", 3600):
                db.insert_alert(
                    serial,
                    "battery_low",
                    f"🟡 {device.get('name', serial)} battery: {state.battery}%",
                )
        log.info(
            f"Health [{device.get('name', serial)}]: battery={state.battery}% "
            f"screen={state.screen_on} app={state.current_app} issues={issues}"
        )
        return {
            "status": "healthy" if not issues else "degraded",
            "battery": state.battery,
            "screen_on": state.screen_on,
            "current_app": state.current_app,
            "issues": issues,
        }

    def _task_screenshot(self, serial: str, params: dict) -> dict:
        path = params.get("path")
        screenshot_path = self.dm.screenshot(serial, path)
        size_kb = Path(screenshot_path).stat().st_size // 1024
        return {"screenshot": screenshot_path, "size_kb": size_kb}

    def _task_app_check(self, serial: str, params: dict) -> dict:
        device = db.get_device(serial) or {}
        config = json.loads(device.get("config_json", "{}"))
        apps = config.get("installed_apps", {})
        app_status = {}
        for skill, pkg in apps.items():
            app_status[skill] = {
                "package": pkg,
                "running": self.dm.is_app_running(serial, pkg),
            }
        return {"apps": app_status}

    def _task_check_notifications(self, serial: str, params: dict) -> dict:
        notifs = self.dm.get_notifications(serial)
        return {"count": len(notifs), "notifications": notifs[:20]}

    def _task_tiktok_inbox(self, serial: str, params: dict) -> dict:
        pkg = "com.ss.android.ugc.trill"
        installed = self.dm.pool.shell(serial, f"pm list packages | grep {pkg}")
        if not installed:
            return {"status": "not_installed"}
        self.dm.wake_screen(serial)
        self.dm.launch_app(serial, pkg)
        time.sleep(3)
        ss = self.dm.screenshot(serial)
        found = self.dm.tap_text(serial, "Inbox")
        time.sleep(2)
        ss2 = self.dm.screenshot(serial)
        return {
            "status": "checked",
            "screenshot": ss,
            "screenshot_inbox": ss2,
            "inbox_tapped": found,
        }

    def _task_shopee_orders(self, serial: str, params: dict) -> dict:
        pkg = "com.shopee.id"
        installed = self.dm.pool.shell(serial, f"pm list packages | grep {pkg}")
        if not installed:
            return {"status": "not_installed"}
        self.dm.wake_screen(serial)
        self.dm.launch_app(serial, pkg)
        time.sleep(4)
        ss = self.dm.screenshot(serial)
        if not self.dm.tap_text(serial, "Me"):
            self.dm.tap_text(serial, "Saya")
        time.sleep(2)
        ss2 = self.dm.screenshot(serial)
        return {"status": "checked", "screenshot": ss, "screenshot_me": ss2}

    def _task_whatsapp_unread(self, serial: str, params: dict) -> dict:
        self.dm.wake_screen(serial)
        self.dm.launch_app(serial, "com.whatsapp")
        time.sleep(3)
        ss = self.dm.screenshot(serial)
        return {"status": "checked", "screenshot": ss}

    def _task_instagram_dms(self, serial: str, params: dict) -> dict:
        self.dm.wake_screen(serial)
        self.dm.launch_app(serial, "com.instagram.android")
        time.sleep(3)
        ss = self.dm.screenshot(serial)
        found = self.dm.tap_text(serial, "Direct")
        time.sleep(2)
        ss2 = self.dm.screenshot(serial)
        return {
            "status": "checked",
            "screenshot": ss,
            "screenshot_dm": ss2,
            "dm_tapped": found,
        }

    def _task_go_home(self, serial: str, params: dict) -> dict:
        self.dm.press_key(serial, "HOME")
        time.sleep(1)
        ss = self.dm.screenshot(serial)
        return {"status": "home", "screenshot": ss}

    def _task_battery_report(self, serial: str, params: dict) -> dict:
        raw = self.dm.pool.shell(serial, "dumpsys battery")
        data = {}
        for line in raw.split("\n"):
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
        return data

    def _task_wake(self, serial: str, params: dict) -> dict:
        self.dm.wake_screen(serial)
        return {"status": "woken"}

    def _task_unlock(self, serial: str, params: dict) -> dict:
        pin = params.get("pin")
        self.dm.unlock_screen(serial, pin)
        return {"status": "unlocked"}

    def _task_launch_app(self, serial: str, params: dict) -> dict:
        package = params.get("package")
        if not package:
            raise ValueError("package param required")
        self.dm.launch_app(serial, package)
        return {"status": "launched", "package": package}

    def queue_depth(self) -> int:
        return self._queue.qsize()

    def get_recent_results(self, serial: str = None, limit: int = 20) -> dict:
        return db.get_recent_tasks(serial=serial, limit=limit)
