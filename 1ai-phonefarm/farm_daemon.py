#!/usr/bin/env python3
"""
Phone Farm Daemon v3 — All-in-one: Dashboard + Live Monitor + Remote Control

Single server on port 8889:
  /                    → Dashboard (overview, live monitor, alerts, tasks)
  /control/{serial}    → Remote control (web scrcpy)
  /ws/{serial}         → WebSocket screen stream + input
  /device/...          → REST API (health, screenshot, task, etc.)
  /stats, /tasks, /alerts, /devices → API endpoints
"""

import asyncio
import io
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Auth imports
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


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
STATIC_DIR = Path(__file__).parent / "static"
ADB = "adb"

HEALTH_INTERVAL = 300
SCREENSHOT_INTERVAL = 120
ACTIVE_INTERVAL = 600
WATCHDOG_INTERVAL = 60
PRUNE_INTERVAL = 3600
STATE_SAVE_INTERVAL = 30
DISCONNECT_ALERT_SEC = 300


# ── Screen Streamer ──────────────────────────────────────────────────────

class DeviceStreamer:
    """Streams screen frames via WebSocket + handles input."""

    def __init__(self, serial: str, fps: int = 8, quality: int = 35, scale: float = 0.4):
        self.serial = serial
        self.fps = fps
        self.quality = quality
        self.scale = scale
        self.running = True
        self.clients: set = set()
        self.width = 720
        self.height = 1640
        self._detect_resolution()

    def _detect_resolution(self):
        try:
            r = subprocess.run([ADB, "-s", self.serial, "shell", "wm", "size"],
                               capture_output=True, text=True, timeout=5)
            if "Physical size:" in r.stdout:
                w, h = r.stdout.strip().split(":")[-1].strip().split("x")
                self.width, self.height = int(w), int(h)
        except Exception:
            pass

    def capture_frame(self) -> bytes:
        try:
            r = subprocess.run(
                [ADB, "-s", self.serial, "exec-out", "screencap", "-p"],
                capture_output=True, timeout=5)
            if r.returncode != 0 or len(r.stdout) < 100:
                return b""
            try:
                from PIL import Image
                img = Image.open(io.BytesIO(r.stdout))
                if self.scale != 1.0:
                    img = img.resize(
                        (int(img.width * self.scale), int(img.height * self.scale)),
                        Image.LANCZOS)
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=self.quality, optimize=True)
                return buf.getvalue()
            except ImportError:
                return r.stdout
        except Exception:
            return b""

    async def stream_loop(self):
        while self.running:
            if not self.clients:
                await asyncio.sleep(0.5)
                continue
            frame = await asyncio.get_event_loop().run_in_executor(None, self.capture_frame)
            if frame:
                dead = set()
                for ws in list(self.clients):
                    try:
                        await ws.send_bytes(frame)
                    except Exception:
                        dead.add(ws)
                self.clients -= dead
            await asyncio.sleep(1.0 / self.fps)

    def tap(self, x, y):
        rx, ry = int(x / self.scale), int(y / self.scale)
        subprocess.Popen([ADB, "-s", self.serial, "shell", "input", "tap", str(rx), str(ry)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def swipe(self, x1, y1, x2, y2, dur=300):
        s = self.scale
        subprocess.Popen([ADB, "-s", self.serial, "shell", "input", "swipe",
                          str(int(x1/s)), str(int(y1/s)), str(int(x2/s)), str(int(y2/s)), str(dur)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def type_text(self, text):
        escaped = text.replace(" ", "%s").replace("'", "\\'")
        subprocess.Popen([ADB, "-s", self.serial, "shell", "input", "text", f"'{escaped}'"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def key(self, keycode):
        codes = {"home":"3","back":"4","menu":"82","power":"26","enter":"66",
                 "delete":"67","tab":"61","up":"19","down":"20","left":"21",
                 "right":"22","volume_up":"24","volume_down":"25",
                 "recent":"187","notification":"83"}
        code = codes.get(keycode.lower(), keycode)
        subprocess.Popen([ADB, "-s", self.serial, "shell", "input", "keyevent", str(code)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def long_press(self, x, y, dur=1000):
        s = self.scale
        rx, ry = int(x/s), int(y/s)
        subprocess.Popen([ADB, "-s", self.serial, "shell", "input", "swipe",
                          str(rx), str(ry), str(rx), str(ry), str(dur)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ── Farm Daemon ──────────────────────────────────────────────────────────

class FarmDaemon:

    def __init__(self, mode="monitor", workers=16, port=8889):
        self.mode = mode
        self.workers = workers
        self.port = port
        self.dm = DeviceManager(workers=workers)
        self.runner = TaskRunner(self.dm, workers=workers)
        self.running = False
        self.start_time = time.time()
        self._lock = threading.Lock()
        self._stats = {"start_time": datetime.now().isoformat(), "mode": mode,
                       "reconnects": 0, "alerts_sent": 0, "prune_runs": 0}
        self.streamers: dict[str, DeviceStreamer] = {}

    def start(self):
        self.running = True
        PID_FILE.write_text(str(os.getpid()))
        log.info(f"Farm daemon v3 — mode={self.mode}, workers={self.workers}, port={self.port}")
        signal.signal(signal.SIGTERM, lambda *_: self.stop())
        signal.signal(signal.SIGINT, lambda *_: self.stop())
        db.init_db()

        connected = self.dm.discover()
        log.info(f"Discovery: {len(connected)} devices")

        self.runner.start()

        for fn, name in [
            (self._scheduler_loop, "scheduler"),
            (self._watchdog_loop, "watchdog"),
            (self._state_save_loop, "state-saver"),
            (self._prune_loop, "pruner"),
        ]:
            threading.Thread(target=fn, name=name, daemon=True).start()

        if self.mode in ("monitor", "active"):
            threading.Thread(target=self._screenshot_loop, name="screenshotter", daemon=True).start()
        if self.mode == "active":
            threading.Thread(target=self._active_task_loop, name="active", daemon=True).start()

        self._run_server()

    def get_streamer(self, serial: str) -> DeviceStreamer:
        if serial not in self.streamers:
            self.streamers[serial] = DeviceStreamer(serial)
            asyncio.ensure_future(self.streamers[serial].stream_loop())
        return self.streamers[serial]

    # ── Background threads ───────────────────────────────────────────────

    def _scheduler_loop(self):
        last = 0
        while self.running:
            if time.time() - last >= HEALTH_INTERVAL:
                serials = [d["serial"] for d in db.get_all_devices(connected_only=True)]
                if serials:
                    self.runner.submit_all(serials, "health_check", priority=PRIORITY_HIGH)
                last = time.time()
            time.sleep(10)

    def _screenshot_loop(self):
        last = 0
        while self.running:
            if time.time() - last >= SCREENSHOT_INTERVAL:
                serials = [d["serial"] for d in db.get_all_devices(connected_only=True)]
                if serials:
                    self.runner.submit_all(serials, "screenshot", priority=PRIORITY_LOW)
                last = time.time()
            time.sleep(15)

    def _active_task_loop(self):
        last = 0
        while self.running:
            if time.time() - last >= ACTIVE_INTERVAL:
                for dev in db.get_all_devices(connected_only=True):
                    config = json.loads(dev.get("config_json", "{}"))
                    task_map = {"tiktok": "tiktok_inbox", "shopee": "shopee_orders",
                                "whatsapp": "whatsapp_unread", "instagram": "instagram_dms"}
                    for skill in config.get("assigned_skills", []):
                        t = task_map.get(skill)
                        if t:
                            self.runner.submit(dev["serial"], t, priority=PRIORITY_NORMAL)
                    self.runner.submit(dev["serial"], "go_home", priority=PRIORITY_LOW)
                last = time.time()
            time.sleep(30)

    def _watchdog_loop(self):
        while self.running:
            try:
                self.dm.pool.health_check_all_servers()
                actual = set(self.dm.pool.list_devices())
                for dev in db.get_all_devices():
                    serial = dev["serial"]
                    was = bool(dev.get("connected"))
                    now = serial in actual
                    if was and not now:
                        db.upsert_device(serial=serial, connected=0)
                    elif not was and now:
                        db.upsert_device(serial=serial, connected=1, last_seen=time.time())
                        with self._lock: self._stats["reconnects"] += 1
                        if not db.is_alert_recent(serial, "reconnected"):
                            db.insert_alert(serial, "reconnected", f"✅ {dev.get('name',serial)} reconnected")
                    if not now and dev.get("last_seen") and time.time() - dev["last_seen"] > DISCONNECT_ALERT_SEC:
                        if not db.is_alert_recent(serial, "disconnect", 3600):
                            db.insert_alert(serial, "disconnect",
                                            f"❌ {dev.get('name',serial)} offline {int((time.time()-dev['last_seen'])/60)}min")
            except Exception as e:
                log.error(f"Watchdog: {e}")
            time.sleep(WATCHDOG_INTERVAL)

    def _state_save_loop(self):
        while self.running:
            self._save_state()
            time.sleep(STATE_SAVE_INTERVAL)

    def _save_state(self):
        state = {
            "pid": os.getpid(), "mode": self.mode,
            "uptime_seconds": int(time.time() - self.start_time),
            "last_updated": datetime.now().isoformat(),
            "stats": {**self._stats, **db.get_stats()},
            "queue_depth": self.runner.queue_depth(),
            "devices_total": db.get_stats()["devices_total"],
            "devices_connected": db.get_stats()["devices_connected"],
            "adb_servers": self.dm.pool.get_server_status(),
            "active_streams": {s: len(st.clients) for s, st in self.streamers.items()},
        }
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def _prune_loop(self):
        while self.running:
            time.sleep(PRUNE_INTERVAL)
            deleted = db.prune_old_tasks(days=7)
            if deleted: log.info(f"Pruned {deleted} old tasks")
            with self._lock: self._stats["prune_runs"] += 1

    # ── Combined Server (FastAPI + WebSocket) ────────────────────────────

    def _run_server(self):
        try:
            from fastapi import FastAPI, WebSocket, WebSocketDisconnect
            from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
            from fastapi.staticfiles import StaticFiles
            import uvicorn
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "websockets"], check=True)
            from fastapi import FastAPI, WebSocket, WebSocketDisconnect
            from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
            from fastapi.staticfiles import StaticFiles
            import uvicorn

        app = FastAPI(title="Phone Farm v3")

        # ── WebSocket: Screen stream + input ──

        @app.websocket("/ws/{serial}")
        async def ws_stream(websocket: WebSocket, serial: str):
            await websocket.accept()
            streamer = self.get_streamer(serial)
            streamer.clients.add(websocket)
            log.info(f"WS client connected to {serial} ({len(streamer.clients)} total)")
            try:
                while True:
                    data = await websocket.receive_text()
                    try:
                        msg = json.loads(data)
                        cmd = msg.get("cmd")
                        if cmd == "tap": streamer.tap(msg["x"], msg["y"])
                        elif cmd == "swipe": streamer.swipe(msg["x1"], msg["y1"], msg["x2"], msg["y2"], msg.get("duration", 300))
                        elif cmd == "type": streamer.type_text(msg["text"])
                        elif cmd == "key": streamer.key(msg["key"])
                        elif cmd == "longpress": streamer.long_press(msg["x"], msg["y"], msg.get("duration", 1000))
                        elif cmd == "fps": streamer.fps = max(1, min(20, int(msg.get("value", 8))))
                        elif cmd == "quality": streamer.quality = max(10, min(90, int(msg.get("value", 35))))
                        elif cmd == "scale": streamer.scale = max(0.25, min(1.0, float(msg.get("value", 0.4))))
                    except Exception as e:
                        await websocket.send_text(json.dumps({"error": str(e)}))
            except WebSocketDisconnect:
                pass
            finally:
                streamer.clients.discard(websocket)
                log.info(f"WS client disconnected from {serial}")

        # ── Auth Setup ──
        # Simple in‑memory user (for demo). In production replace with DB.
        USERS = {"admin": {"username": "admin", "hashed_pw": CryptContext(schemes=["bcrypt"], deprecated="auto").hash("admin")}}
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
        SECRET_KEY = os.getenv("JWT_SECRET", "change_me_secret")
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 30

        def create_access_token(data: dict, expires_delta: Optional[int] = None):
            to_encode = data.copy()
            expire = int(time.time()) + (expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES * 60)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return encoded_jwt

        async def get_current_user(token: str = Depends(oauth2_scheme)):
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise credentials_exception
            except JWTError:
                raise credentials_exception
            user = USERS.get(username)
            if user is None:
                raise credentials_exception
            return user

        class AuthMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Request, call_next):
                if request.url.path.startswith("/dashboard"):
                    token = request.headers.get("Authorization")
                    if not token or not token.startswith("Bearer "):
                        return JSONResponse({"detail": "Not authenticated"}, status_code=401)
                    try:
                        jwt.decode(token.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
                    except JWTError:
                        return JSONResponse({"detail": "Invalid token"}, status_code=401)
                response = await call_next(request)
                return response

        app.add_middleware(AuthMiddleware)

        # ── Pages ──

        @app.get("/")
        async def root():
            return RedirectResponse("/auth.html")

        @app.get("/control/{serial}")
        async def control_page(serial: str):
            html_path = STATIC_DIR / "control.html"
            if not html_path.exists():
                return HTMLResponse("control.html not found", status_code=404)
            text = html_path.read_text()
            text = text.replace("{{SERIAL}}", serial)
            text = text.replace("{{WS_URL}}", f"AUTO_DETECT")
            return HTMLResponse(text)

        # ── REST API ──

        @app.get("/api")
        async def api_root():
            return FarmDaemon.get_status()

        # ── Auth Endpoints ──
        @app.post("/api/login")
        async def login(form: OAuth2PasswordRequestForm = Depends()):
            user = USERS.get(form.username)
            if not user or not pwd_context.verify(form.password, user["hashed_pw"]):
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            access_token = create_access_token(data={"sub": user["username"]})
            return {"access_token": access_token, "token_type": "bearer"}

        @app.get("/stats")
        async def stats():
            self._save_state()
            return FarmDaemon.get_status()

        @app.get("/devices")
        async def devices(connected: bool = False):
            return db.get_all_devices(connected_only=connected)

        @app.get("/health")
        async def health():
            serials = [d["serial"] for d in db.get_all_devices(connected_only=True)]
            states = self.dm.refresh_all(serials)
            return [{"serial": s, "battery": st.battery, "screen_on": st.screen_on,
                     "current_app": st.current_app, "connected": st.connected}
                    for s, st in states.items()]

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
            return {"status": "launched"}

        @app.post("/device/{serial}/wake")
        async def wake(serial: str):
            """Wake screen + swipe to dismiss lockscreen."""
            import subprocess as sp
            adb = lambda *args: sp.run([ADB, "-s", serial, "shell"] + list(args),
                                       capture_output=True, timeout=5)
            # Check if awake
            r = adb("dumpsys", "power")
            awake = "mWakefulness=Awake" in r.stdout.decode()
            if not awake:
                adb("input", "keyevent", "26")  # power on
                await asyncio.sleep(1)
            # Dismiss lockscreen
            adb("input", "keyevent", "82")       # menu unlock
            await asyncio.sleep(0.3)
            adb("input", "swipe", "360", "900", "360", "300", "400")  # swipe up
            await asyncio.sleep(0.3)
            return {"status": "woken"}

        @app.post("/device/{serial}/tap/{x}/{y}")
        async def tap(serial: str, x: int, y: int):
            self.dm.tap(serial, x, y)
            return {"status": "tapped"}

        @app.post("/device/{serial}/swipe/{x1}/{y1}/{x2}/{y2}")
        async def swipe(serial: str, x1: int, y1: int, x2: int, y2: int, dur: int = 300):
            self.dm.swipe(serial, x1, y1, x2, y2, dur)
            return {"status": "swiped"}

        @app.post("/device/{serial}/key/{key}")
        async def press(serial: str, key: str):
            self.dm.press_key(serial, key)
            return {"status": "pressed"}

        @app.post("/device/add")
        async def add_device(serial: str, name: str, connection: str = "usb"):
            self.dm.register_device(serial, name, connection=connection)
            return {"status": "registered"}

        @app.post("/wifi/connect")
        async def wifi_connect(ip: str, port: int = 5555, name: str = None):
            ok = self.dm.connect_wifi(ip, port, name)
            return {"status": "connected" if ok else "failed"}

        @app.post("/api/pay")
        async def pay(payload: dict):
            """NowPayments crypto invoice creation."""
            import httpx, os, time
            api_key = os.environ.get("NOWPAYMENTS_API_KEY", "")
            plan = payload.get("plan", "starter")
            price = payload.get("price", 9)
            currency = payload.get("currency", "usdttrc20")
            billing = payload.get("billing", "monthly")
            descriptions = {
                "starter": "PhoneFarm Starter — 1 Real Android Phone",
                "growth":  "PhoneFarm Growth — 5 Real Android Phones",
                "scale":   "PhoneFarm Scale — 20 Real Android Phones",
            }
            if not api_key:
                return JSONResponse({"error": "payment_not_configured",
                                     "message": "Payment not yet configured. Contact support@aitradepulse.com to purchase."}, status_code=503)
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    r = await client.post(
                        "https://api.nowpayments.io/v1/invoice",
                        headers={"x-api-key": api_key, "Content-Type": "application/json"},
                        json={
                            "price_amount": float(price),
                            "price_currency": "usd",
                            "pay_currency": currency.lower(),
                            "order_id": f"{plan}_{billing}_{int(time.time())}",
                            "order_description": descriptions.get(plan, f"PhoneFarm {plan.title()} Plan"),
                            "ipn_callback_url": "https://phonefarm.aitradepulse.com/api/webhook/nowpayments",
                            "success_url": "https://phonefarm.aitradepulse.com/dashboard/",
                            "cancel_url": "https://phonefarm.aitradepulse.com/dashboard/pricing.html",
                        })
                    data = r.json()
                    if r.status_code == 200 and data.get("invoice_url"):
                        return {"invoice_url": data["invoice_url"], "invoice_id": data.get("id")}
                    return JSONResponse({"error": "nowpayments_error", "detail": data}, status_code=r.status_code)
            except Exception as e:
                return JSONResponse({"error": "request_failed", "message": str(e)}, status_code=500)

        @app.post("/api/webhook/nowpayments")
        async def nowpayments_webhook(payload: dict):
            """NowPayments IPN callback — mark order as paid."""
            log.info(f"NowPayments webhook: {payload}")
            # TODO: verify IPN signature, provision device access
            return {"status": "received"}

        # ── Static files (dashboard) ──
        if STATIC_DIR.exists():
            app.mount("/dashboard", StaticFiles(directory=str(STATIC_DIR), html=True), name="dashboard")

        log.info(f"Server on http://0.0.0.0:{self.port}")
        uvicorn.run(app, host="0.0.0.0", port=self.port, log_level="warning")

    def stop(self):
        log.info("Stopping...")
        self.running = False
        for st in self.streamers.values():
            st.running = False
        self.runner.stop()
        self._save_state()
        self.dm.shutdown()
        PID_FILE.unlink(missing_ok=True)
        sys.exit(0)

    @staticmethod
    def get_status() -> dict:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        return {"status": "not_running"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["monitor", "active", "dashboard"], default="monitor")
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--port", type=int, default=8889)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--stop", action="store_true")
    args = parser.parse_args()
    if args.status:
        print(json.dumps(FarmDaemon.get_status(), indent=2)); sys.exit(0)
    if args.stop:
        if PID_FILE.exists():
            os.kill(int(PID_FILE.read_text().strip()), signal.SIGTERM)
        sys.exit(0)
    FarmDaemon(mode=args.mode, workers=args.workers, port=args.port).start()
# PATCH applied separately — see below
