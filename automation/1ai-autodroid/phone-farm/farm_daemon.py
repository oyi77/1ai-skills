#!/usr/bin/env python3
"""
Phone Farm Daemon v2 — Production-grade autonomous orchestrator.

Architecture:
  - Scheduler thread: dispatches tasks at configured intervals
  - N worker threads (TaskRunner): execute tasks from priority queue
  - Watchdog thread: monitors ADB servers, reconnects dead devices
  - Alert thread: reads DB alerts and sends Telegram notifications
  - HTTP API thread: FastAPI dashboard (non-blocking)
  - Pruner thread: keeps DB clean (old task logs)

Design principles:
  - NO sequential device loops in hot path
  - All device work goes through TaskRunner priority queue
  - State in SQLite (survives restarts)
  - Graceful shutdown with SIGTERM
  - Configurable intervals per device
"""

import asyncio
import json
import logging
import os
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from device_manager import DeviceManager
from task_runner import TaskRunner, PRIORITY_HIGH, PRIORITY_NORMAL, PRIORITY_LOW
import db

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

PID_FILE = Path("/tmp/phone-farm-daemon.pid")
STATE_FILE = Path(__file__).parent.parent.parent / "logs" / "phone-farm" / "daemon_state.json"

# Intervals
HEALTH_INTERVAL      = 300   # 5 min
SCREENSHOT_INTERVAL  = 120   # 2 min
ACTIVE_INTERVAL      = 600   # 10 min (active mode)
WATCHDOG_INTERVAL    = 60    # 1 min
ALERT_INTERVAL       = 30    # 30s
PRUNE_INTERVAL       = 3600  # 1 hour
STATE_SAVE_INTERVAL  = 30    # 30s
DISCONNECT_ALERT_SEC = 300   # 5 min before alerting


class FarmDaemon:

    def __init__(self, mode: str = "monitor", workers: int = 16,
                 dashboard_port: int = 8889):
        self.mode = mode
        self.workers = workers
        self.dashboard_port = dashboard_port
        self.dm = DeviceManager(workers=workers)
        self.runner = TaskRunner(self.dm, workers=workers)
        self.running = False
        self.start_time = time.time()
        self._threads: list[threading.Thread] = []
        self._lock = threading.Lock()
        self._stats = {
            "start_time": datetime.now().isoformat(),
            "mode": mode,
            "reconnects": 0,
            "alerts_sent": 0,
            "prune_runs": 0,
        }

    def start(self):
        self.running = True
        self._write_pid()
        log.info(f"Farm daemon v2 starting — mode={self.mode}, workers={self.workers}")
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)

        # Init DB
        db.init_db()

        # Initial discovery
        connected = self.dm.discover()
        log.info(f"Initial discovery: {len(connected)} devices connected")

        # Start TaskRunner workers
        self.runner.start()

        # Start background threads
        self._spawn(self._scheduler_loop, "scheduler")
        self._spawn(self._watchdog_loop, "watchdog")
        self._spawn(self._alert_loop, "alerter")
        self._spawn(self._state_save_loop, "state-saver")
        self._spawn(self._prune_loop, "pruner")

        if self.mode in ("monitor", "active"):
            self._spawn(self._screenshot_loop, "screenshotter")

        if self.mode == "active":
            self._spawn(self._active_task_loop, "active-tasks")

        if self.mode != "dashboard":
            # Block main thread on HTTP API
            self._run_api()
        else:
            self._run_api()

    def _spawn(self, target, name: str) -> threading.Thread:
        t = threading.Thread(target=target, name=name, daemon=True)
        t.start()
        self._threads.append(t)
        return t

    # ── Scheduler: dispatches health checks ─────────────────────────────

    def _scheduler_loop(self):
        last_health = 0
        while self.running:
            now = time.time()
            if now - last_health >= HEALTH_INTERVAL:
                connected = [d["serial"] for d in db.get_all_devices(connected_only=True)]
                if connected:
                    log.info(f"Scheduling health checks for {len(connected)} devices")
                    self.runner.submit_all(connected, "health_check", priority=PRIORITY_HIGH)
                last_health = now
            time.sleep(10)

    # ── Screenshot loop ──────────────────────────────────────────────────

    def _screenshot_loop(self):
        last_ss = 0
        while self.running:
            now = time.time()
            if now - last_ss >= SCREENSHOT_INTERVAL:
                connected = [d["serial"] for d in db.get_all_devices(connected_only=True)]
                if connected:
                    log.debug(f"Scheduling screenshots for {len(connected)} devices")
                    self.runner.submit_all(connected, "screenshot", priority=PRIORITY_LOW)
                last_ss = now
            time.sleep(15)

    # ── Active task loop (active mode) ───────────────────────────────────

    def _active_task_loop(self):
        last_active = 0
        while self.running:
            now = time.time()
            if now - last_active >= ACTIVE_INTERVAL:
                devices = db.get_all_devices(connected_only=True)
                for device in devices:
                    serial = device["serial"]
                    config = json.loads(device.get("config_json", "{}"))
                    skills = config.get("assigned_skills", [])
                    task_map = {
                        "tiktok": "tiktok_inbox",
                        "shopee": "shopee_orders",
                        "whatsapp": "whatsapp_unread",
                        "instagram": "instagram_dms",
                    }
                    for skill in skills:
                        task = task_map.get(skill)
                        if task:
                            self.runner.submit(serial, task, priority=PRIORITY_NORMAL)
                    # Return to home after tasks
                    self.runner.submit(serial, "go_home", priority=PRIORITY_LOW)
                last_active = now
            time.sleep(30)

    # ── Watchdog: detect disconnects, auto-reconnect ─────────────────────

    def _watchdog_loop(self):
        while self.running:
            try:
                # Check ADB servers first
                self.dm.pool.health_check_all_servers()
                # Discover connected devices
                actual_connected = set(self.dm.pool.list_devices())
                all_devices = db.get_all_devices()
                for device in all_devices:
                    serial = device["serial"]
                    was_connected = bool(device.get("connected", 0))
                    is_now = serial in actual_connected
                    if was_connected and not is_now:
                        # Device just disconnected
                        db.upsert_device(serial=serial, connected=0)
                        log.warning(f"Device disconnected: {device.get('name', serial)}")
                    elif not was_connected and is_now:
                        # Device reconnected!
                        db.upsert_device(serial=serial, connected=1, last_seen=time.time())
                        log.info(f"Device reconnected: {device.get('name', serial)}")
                        with self._lock:
                            self._stats["reconnects"] += 1
                        if not db.is_alert_recent(serial, "reconnected"):
                            db.insert_alert(serial, "reconnected",
                                            f"✅ {device.get('name', serial)} reconnected")

                # Check long-disconnected devices
                for device in all_devices:
                    serial = device["serial"]
                    if not device.get("connected"):
                        last_seen = device.get("last_seen", 0)
                        if last_seen and (time.time() - last_seen) > DISCONNECT_ALERT_SEC:
                            if not db.is_alert_recent(serial, "disconnect", 3600):
                                db.insert_alert(
                                    serial, "disconnect",
                                    f"❌ {device.get('name', serial)} offline "
                                    f"{int((time.time()-last_seen)/60)}min"
                                )

            except Exception as e:
                log.error(f"Watchdog error: {e}")
            time.sleep(WATCHDOG_INTERVAL)

    # ── Alert loop: send Telegram notifications ───────────────────────────

    def _alert_loop(self):
        last_check = 0
        while self.running:
            now = time.time()
            if now - last_check >= ALERT_INTERVAL:
                try:
                    alerts = db.get_recent_alerts(limit=10, acked=False)
                    for alert in alerts:
                        if now - alert.get("ts", 0) < ALERT_INTERVAL * 2:
                            self._send_telegram(alert["message"])
                            # Mark acked
                            conn = db.get_conn()
                            conn.execute("UPDATE alerts SET acked=1 WHERE id=?", (alert["id"],))
                            conn.commit()
                            with self._lock:
                                self._stats["alerts_sent"] += 1
                except Exception as e:
                    log.error(f"Alert loop error: {e}")
                last_check = now
            time.sleep(5)

    def _send_telegram(self, message: str):
        """Send alert via Telegram (OpenClaw message routing)."""
        try:
            # Use openclaw's message tool via subprocess
            import subprocess
            msg = f"📱 Phone Farm\n{message}"
            log.info(f"Alert: {message}")
            # Direct Telegram API call using bot token if available
            import os
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID", "228956686")
            if bot_token:
                import urllib.request, urllib.parse
                data = urllib.parse.urlencode({
                    "chat_id": chat_id,
                    "text": msg,
                    "parse_mode": "HTML",
                }).encode()
                req = urllib.request.Request(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage", data=data
                )
                urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            log.warning(f"Telegram send failed: {e} — alert logged to DB only")

    # ── State save loop ──────────────────────────────────────────────────

    def _state_save_loop(self):
        while self.running:
            try:
                self._save_state()
            except Exception as e:
                log.error(f"State save error: {e}")
            time.sleep(STATE_SAVE_INTERVAL)

    def _save_state(self):
        devices = db.get_all_devices()
        db_stats = db.get_stats()
        state = {
            "pid": os.getpid(),
            "mode": self.mode,
            "uptime_seconds": int(time.time() - self.start_time),
            "last_updated": datetime.now().isoformat(),
            "stats": {**self._stats, **db_stats},
            "queue_depth": self.runner.queue_depth(),
            "devices_total": len(devices),
            "devices_connected": sum(1 for d in devices if d.get("connected")),
            "adb_servers": self.dm.pool.get_server_status(),
        }
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    # ── Prune loop ───────────────────────────────────────────────────────

    def _prune_loop(self):
        while self.running:
            time.sleep(PRUNE_INTERVAL)
            try:
                deleted = db.prune_old_tasks(days=7)
                if deleted:
                    log.info(f"Pruned {deleted} old task records")
                with self._lock:
                    self._stats["prune_runs"] += 1
            except Exception as e:
                log.error(f"Prune error: {e}")

    # ── HTTP API ─────────────────────────────────────────────────────────

    def _run_api(self):
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

        app = FastAPI(title="Phone Farm Dashboard v2", version="2.0.0")

        @app.get("/api")
        async def api_root():
            state = FarmDaemon.get_status()
            return state

        @app.get("/devices")
        async def devices(connected: bool = False):
            return db.get_all_devices(connected_only=connected)

        @app.get("/health")
        async def health():
            connected = [d["serial"] for d in db.get_all_devices(connected_only=True)]
            states = self.dm.refresh_all(connected)
            return [
                {"serial": s, "battery": st.battery, "screen_on": st.screen_on,
                 "current_app": st.current_app, "connected": st.connected}
                for s, st in states.items()
            ]

        @app.get("/stats")
        async def stats():
            self._save_state()
            return FarmDaemon.get_status()

        @app.get("/tasks")
        async def tasks(serial: str = None, limit: int = 50):
            return db.get_recent_tasks(serial=serial, limit=limit)

        @app.get("/alerts")
        async def alerts():
            return db.get_recent_alerts(limit=50)

        @app.get("/device/{serial}/screenshot")
        async def screenshot(serial: str):
            try:
                path = self.dm.screenshot(serial)
                return FileResponse(path, media_type="image/png")
            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

        @app.post("/device/{serial}/task/{task_type}")
        async def run_task(serial: str, task_type: str):
            result = self.runner.run_now(serial, task_type)
            return result

        @app.post("/device/{serial}/launch/{package}")
        async def launch(serial: str, package: str):
            self.dm.launch_app(serial, package)
            return {"status": "launched", "package": package}

        @app.post("/device/{serial}/tap/{x}/{y}")
        async def tap(serial: str, x: int, y: int):
            self.dm.tap(serial, x, y)
            return {"status": "tapped"}

        @app.post("/device/{serial}/key/{key}")
        async def key(serial: str, key: str):
            self.dm.press_key(serial, key)
            return {"status": "pressed"}

        @app.post("/device/{serial}/screenshot")
        async def take_screenshot(serial: str):
            path = self.dm.screenshot(serial)
            return {"path": path}

        @app.post("/device/add")
        async def add_device(serial: str, name: str, connection: str = "usb"):
            self.dm.register_device(serial, name, connection=connection)
            return {"status": "registered", "serial": serial}

        @app.post("/wifi/connect")
        async def wifi_connect(ip: str, port: int = 5555, name: str = None):
            ok = self.dm.connect_wifi(ip, port, name)
            return {"status": "connected" if ok else "failed"}

        # Serve static dashboard
        from fastapi.staticfiles import StaticFiles
        static_dir = Path(__file__).parent / "static"
        if static_dir.exists():
            app.mount("/dashboard", StaticFiles(directory=str(static_dir), html=True), name="dashboard")

            @app.get("/")
            async def index():
                from fastapi.responses import RedirectResponse
                return RedirectResponse("/dashboard/")

        log.info(f"Farm API on http://0.0.0.0:{self.dashboard_port}")
        uvicorn.run(app, host="0.0.0.0", port=self.dashboard_port, log_level="warning")

    # ── Lifecycle ────────────────────────────────────────────────────────

    def _write_pid(self):
        PID_FILE.write_text(str(os.getpid()))

    def _handle_signal(self, signum, frame):
        log.info(f"Signal {signum} — shutting down")
        self.stop()

    def stop(self):
        log.info("Farm daemon stopping...")
        self.running = False
        self.runner.stop()
        self._save_state()
        self.dm.shutdown()
        PID_FILE.unlink(missing_ok=True)
        log.info("Farm daemon stopped")
        sys.exit(0)

    @staticmethod
    def get_status() -> dict:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        return {"status": "not_running"}


# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phone Farm Daemon v2")
    parser.add_argument("--mode", choices=["monitor", "active", "dashboard"], default="monitor")
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--port", type=int, default=8889)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    args = parser.parse_args()

    if args.status:
        print(json.dumps(FarmDaemon.get_status(), indent=2))
        sys.exit(0)

    if args.stop:
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            print(f"Sent SIGTERM to PID {pid}")
        sys.exit(0)

    daemon = FarmDaemon(mode=args.mode, workers=args.workers, dashboard_port=args.port)
    daemon.start()
