#!/usr/bin/env python3
"""
Phone Farm Daemon — Autonomous orchestrator for Android device farm.

Runs as a persistent daemon that:
  1. Monitors device health (every 5 min)
  2. Auto-reconnects disconnected devices
  3. Runs scheduled tasks per device
  4. Sends alerts on critical issues (battery low, disconnect)
  5. Takes periodic screenshots for audit
  6. Exposes HTTP API for real-time status

Daemon modes:
  --mode monitor   : Health checks + screenshots only (safe, default)
  --mode active    : Full task automation (opens apps, checks inboxes)
  --mode dashboard : HTTP API only (no autonomous tasks)

Usage:
  python3 farm_daemon.py                    # default monitor mode
  python3 farm_daemon.py --mode active      # full automation
  python3 farm_daemon.py --mode dashboard   # API only (port 8889)
  python3 farm_daemon.py --status           # print current state and exit
"""

import asyncio
import json
import logging
import os
import signal
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from device_manager import DeviceManager
from task_runner import TaskRunner

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            Path(__file__).parent.parent.parent / "logs" / "phone-farm" / "daemon.log",
            mode="a",
        ),
    ],
)
log = logging.getLogger("farm_daemon")

STATE_FILE = Path(__file__).parent.parent.parent / "logs" / "phone-farm" / "daemon_state.json"
PID_FILE = Path("/tmp/phone-farm-daemon.pid")

# ── Alert thresholds ─────────────────────────────────────────────────────
BATTERY_WARN = 20
BATTERY_CRIT = 10
DISCONNECT_ALERT_AFTER_SEC = 300  # 5 min disconnected = alert
HEALTH_INTERVAL = 300             # 5 min
SCREENSHOT_INTERVAL = 120        # 2 min
ACTIVE_TASK_INTERVAL = 600       # 10 min (for active mode tasks)
RECONNECT_INTERVAL = 60          # 1 min between reconnect attempts


class FarmDaemon:
    """Autonomous phone farm orchestrator."""

    def __init__(self, mode: str = "monitor"):
        self.mode = mode
        self.dm = DeviceManager()
        self.runner = TaskRunner(self.dm)
        self.running = False
        self.start_time = time.time()
        self.last_health = 0
        self.last_screenshot = 0
        self.last_active_task = 0
        self.last_reconnect = 0
        self.alerts: list[dict] = []
        self.stats = {
            "tasks_run": 0,
            "tasks_failed": 0,
            "reconnects": 0,
            "alerts_sent": 0,
            "screenshots_taken": 0,
        }

    def start(self):
        """Start the daemon main loop."""
        self.running = True
        self._write_pid()
        log.info(f"Farm daemon started in {self.mode} mode (PID {os.getpid()})")
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        # Initial refresh
        self.dm.refresh_all()
        connected = [s for s, d in self.dm.devices.items() if d.connected]
        log.info(f"Devices: {len(self.dm.devices)} registered, {len(connected)} connected")

        if self.mode == "dashboard":
            self._run_dashboard()
        else:
            self._run_loop()

    def _run_loop(self):
        """Main daemon loop."""
        while self.running:
            try:
                now = time.time()

                # Health check every HEALTH_INTERVAL
                if now - self.last_health >= HEALTH_INTERVAL:
                    self._do_health_checks()
                    self.last_health = now

                # Screenshots every SCREENSHOT_INTERVAL
                if now - self.last_screenshot >= SCREENSHOT_INTERVAL:
                    self._do_screenshots()
                    self.last_screenshot = now

                # Active mode tasks every ACTIVE_TASK_INTERVAL
                if self.mode == "active" and now - self.last_active_task >= ACTIVE_TASK_INTERVAL:
                    self._do_active_tasks()
                    self.last_active_task = now

                # Reconnect check
                if now - self.last_reconnect >= RECONNECT_INTERVAL:
                    self._check_reconnect()
                    self.last_reconnect = now

                # Save state
                self._save_state()

                # Sleep 10s between cycles
                time.sleep(10)

            except KeyboardInterrupt:
                self.stop()
            except Exception as e:
                log.error(f"Daemon loop error: {e}", exc_info=True)
                time.sleep(30)

    def _do_health_checks(self):
        log.info("Running health checks...")
        self.dm.refresh_all()
        for serial, state in self.dm.devices.items():
            if not state.connected:
                self._alert("disconnect", serial, f"Device {state.name} ({serial}) disconnected")
                continue

            health = self.dm.health_check(serial)
            self.stats["tasks_run"] += 1

            # Battery alerts
            if health["battery"] >= 0:
                if health["battery"] <= BATTERY_CRIT:
                    self._alert("battery_critical", serial,
                                f"🔴 {state.name} battery CRITICAL: {health['battery']}%")
                elif health["battery"] <= BATTERY_WARN:
                    self._alert("battery_low", serial,
                                f"🟡 {state.name} battery low: {health['battery']}%")

            if health["issues"]:
                log.warning(f"Device {state.name} issues: {health['issues']}")

    def _do_screenshots(self):
        for serial, state in self.dm.devices.items():
            if state.connected:
                try:
                    self.dm.screenshot(serial)
                    self.stats["screenshots_taken"] += 1
                except Exception as e:
                    log.warning(f"Screenshot failed {state.name}: {e}")

    def _do_active_tasks(self):
        """Run active automation tasks on devices (active mode only)."""
        log.info("Running active tasks...")
        for serial, state in self.dm.devices.items():
            if not state.connected:
                continue
            for skill in state.assigned_skills:
                task_map = {
                    "tiktok": "tiktok_inbox",
                    "shopee": "shopee_orders",
                    "whatsapp": "whatsapp_unread",
                    "instagram": "instagram_dms",
                }
                task = task_map.get(skill)
                if task:
                    try:
                        result = self.runner.run_task(serial, task)
                        self.stats["tasks_run"] += 1
                        if not result.success:
                            self.stats["tasks_failed"] += 1
                    except Exception as e:
                        log.error(f"Active task {task} failed: {e}")
                        self.stats["tasks_failed"] += 1
                    # Go home between tasks
                    self.dm.press_key(serial, "HOME")
                    time.sleep(2)

    def _check_reconnect(self):
        """Auto-reconnect disconnected devices."""
        for serial, state in self.dm.devices.items():
            if not state.connected and state.last_seen > 0:
                elapsed = time.time() - state.last_seen
                if elapsed > DISCONNECT_ALERT_AFTER_SEC:
                    log.info(f"Attempting reconnect for {state.name} (disconnected {int(elapsed)}s)")
                    if self.dm.reconnect(serial):
                        self.stats["reconnects"] += 1
                        self._alert("reconnected", serial, f"✅ {state.name} reconnected")

    def _alert(self, alert_type: str, serial: str, message: str):
        """Record an alert (deduplication: same type+serial within 30min)."""
        now = time.time()
        # Dedup: skip if same alert within 30 minutes
        for existing in self.alerts[-50:]:
            if (existing["type"] == alert_type
                    and existing["serial"] == serial
                    and now - existing["timestamp"] < 1800):
                return

        alert = {
            "type": alert_type,
            "serial": serial,
            "message": message,
            "timestamp": now,
            "time_str": datetime.now().isoformat(),
        }
        self.alerts.append(alert)
        self.stats["alerts_sent"] += 1
        log.warning(f"ALERT [{alert_type}]: {message}")

    def _save_state(self):
        state = {
            "mode": self.mode,
            "pid": os.getpid(),
            "uptime_seconds": int(time.time() - self.start_time),
            "last_updated": datetime.now().isoformat(),
            "stats": self.stats,
            "devices": self.dm.to_dict(),
            "recent_alerts": [
                {k: v for k, v in a.items() if k != "timestamp"}
                for a in self.alerts[-20:]
            ],
        }
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def _run_dashboard(self):
        """Run HTTP API server for dashboard mode."""
        try:
            from fastapi import FastAPI
            from fastapi.responses import JSONResponse, FileResponse
            import uvicorn
        except ImportError:
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"], check=True)
            from fastapi import FastAPI
            from fastapi.responses import JSONResponse, FileResponse
            import uvicorn

        app = FastAPI(title="Phone Farm Dashboard", version="2.0.0")

        @app.get("/")
        async def root():
            return {"status": "running", "mode": self.mode, "uptime": int(time.time() - self.start_time)}

        @app.get("/devices")
        async def devices():
            self.dm.refresh_all()
            return self.dm.to_dict()

        @app.get("/health")
        async def health():
            self.dm.refresh_all()
            results = {}
            for serial, state in self.dm.devices.items():
                if state.connected:
                    results[serial] = self.dm.health_check(serial)
            return results

        @app.get("/device/{serial}/screenshot")
        async def screenshot(serial: str):
            try:
                path = self.dm.screenshot(serial)
                return FileResponse(path, media_type="image/png")
            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

        @app.post("/device/{serial}/task/{task_type}")
        async def run_task(serial: str, task_type: str):
            result = self.runner.run_task(serial, task_type)
            from dataclasses import asdict
            return asdict(result)

        @app.get("/stats")
        async def stats():
            return {
                "mode": self.mode,
                "uptime": int(time.time() - self.start_time),
                "stats": self.stats,
                "alerts": [
                    {k: v for k, v in a.items() if k != "timestamp"}
                    for a in self.alerts[-20:]
                ],
            }

        @app.post("/device/{serial}/launch/{package}")
        async def launch(serial: str, package: str):
            self.dm.launch_app(serial, package)
            return {"status": "launched", "package": package}

        @app.post("/device/{serial}/tap/{x}/{y}")
        async def tap(serial: str, x: int, y: int):
            self.dm.tap(serial, x, y)
            return {"status": "tapped", "x": x, "y": y}

        @app.post("/device/{serial}/key/{key}")
        async def press(serial: str, key: str):
            self.dm.press_key(serial, key)
            return {"status": "pressed", "key": key}

        port = 8889
        log.info(f"Dashboard API on http://0.0.0.0:{port}")
        uvicorn.run(app, host="0.0.0.0", port=port)

    def _write_pid(self):
        PID_FILE.write_text(str(os.getpid()))

    def _handle_signal(self, signum, frame):
        log.info(f"Received signal {signum}, shutting down...")
        self.stop()

    def stop(self):
        self.running = False
        self._save_state()
        if PID_FILE.exists():
            PID_FILE.unlink()
        log.info("Farm daemon stopped")
        sys.exit(0)

    @staticmethod
    def get_status() -> dict:
        """Read daemon state from file (no daemon needed)."""
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        if PID_FILE.exists():
            pid = PID_FILE.read_text().strip()
            return {"status": "pid_exists", "pid": pid, "state_file": "missing"}
        return {"status": "not_running"}


# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phone Farm Daemon")
    parser.add_argument("--mode", choices=["monitor", "active", "dashboard"],
                        default="monitor", help="Daemon mode")
    parser.add_argument("--status", action="store_true", help="Print status and exit")
    parser.add_argument("--stop", action="store_true", help="Stop running daemon")
    args = parser.parse_args()

    if args.status:
        print(json.dumps(FarmDaemon.get_status(), indent=2))
        sys.exit(0)

    if args.stop:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"Sent SIGTERM to PID {pid}")
            except ProcessLookupError:
                print(f"PID {pid} not running, cleaning up")
                PID_FILE.unlink()
        else:
            print("Daemon not running (no PID file)")
        sys.exit(0)

    daemon = FarmDaemon(mode=args.mode)
    daemon.start()
