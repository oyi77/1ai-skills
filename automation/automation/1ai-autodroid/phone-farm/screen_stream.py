#!/usr/bin/env python3
"""
Phone Farm — Screen Stream Server (Web scrcpy)

Real-time phone screen streaming + touch/swipe/keyboard control via WebSocket.

Architecture:
  Browser ←WebSocket→ This server ←ADB→ Android device

Streaming: Continuous screencap → JPEG → WebSocket (10-15 FPS)
Control:   WebSocket messages → ADB input commands

Endpoints:
  GET  /stream/{serial}         → HTML control page
  WS   /ws/{serial}             → WebSocket (screen frames + input)
  GET  /api/screen/{serial}     → Single JPEG screenshot
  POST /api/input/{serial}      → REST input (tap/swipe/type/key)
"""

import asyncio
import io
import json
import logging
import os
import struct
import subprocess
import sys
import time
import threading
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("screen_stream")

ADB = "adb"


class DeviceStreamer:
    """Manages screen capture and input for one device."""

    def __init__(self, serial: str, fps: int = 10, quality: int = 40, scale: float = 0.5):
        self.serial = serial
        self.fps = fps
        self.quality = quality
        self.scale = scale
        self.running = False
        self.clients: set = set()
        self.latest_frame: bytes = b""
        self.lock = threading.Lock()
        self._capture_task: Optional[asyncio.Task] = None
        # Device screen dimensions (detected)
        self.width = 720
        self.height = 1640
        self._detect_resolution()

    def _detect_resolution(self):
        try:
            r = subprocess.run(
                [ADB, "-s", self.serial, "shell", "wm", "size"],
                capture_output=True, text=True, timeout=5
            )
            if "Physical size:" in r.stdout:
                parts = r.stdout.strip().split(":")[-1].strip().split("x")
                self.width = int(parts[0])
                self.height = int(parts[1])
                log.info(f"Device {self.serial}: {self.width}x{self.height}")
        except Exception as e:
            log.warning(f"Resolution detect failed: {e}")

    def _capture_frame(self) -> bytes:
        """Capture screen as PNG via ADB, convert to JPEG for compression."""
        try:
            # Capture raw PNG from device
            r = subprocess.run(
                [ADB, "-s", self.serial, "exec-out", "screencap", "-p"],
                capture_output=True, timeout=5
            )
            if r.returncode != 0 or len(r.stdout) < 100:
                return b""

            png_data = r.stdout

            # Convert PNG to smaller JPEG using Python PIL if available
            try:
                from PIL import Image
                img = Image.open(io.BytesIO(png_data))
                if self.scale != 1.0:
                    new_w = int(img.width * self.scale)
                    new_h = int(img.height * self.scale)
                    img = img.resize((new_w, new_h), Image.LANCZOS)
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=self.quality, optimize=True)
                return buf.getvalue()
            except ImportError:
                # No PIL — send raw PNG (larger but works)
                return png_data

        except subprocess.TimeoutExpired:
            return b""
        except Exception as e:
            log.debug(f"Capture error: {e}")
            return b""

    async def start_streaming(self):
        """Start capture loop."""
        self.running = True
        interval = 1.0 / self.fps
        log.info(f"Streaming {self.serial} at {self.fps}fps, quality={self.quality}, scale={self.scale}")
        while self.running:
            if not self.clients:
                await asyncio.sleep(0.5)
                continue
            frame = await asyncio.get_event_loop().run_in_executor(None, self._capture_frame)
            if frame:
                with self.lock:
                    self.latest_frame = frame
                # Broadcast to all connected clients
                dead = set()
                for ws in list(self.clients):
                    try:
                        await ws.send_bytes(frame)
                    except Exception:
                        dead.add(ws)
                self.clients -= dead
            await asyncio.sleep(interval)

    def stop(self):
        self.running = False

    # ── Input commands ──

    def tap(self, x: int, y: int):
        # Scale coordinates back to device resolution
        real_x = int(x / self.scale) if self.scale != 1.0 else x
        real_y = int(y / self.scale) if self.scale != 1.0 else y
        subprocess.Popen(
            [ADB, "-s", self.serial, "shell", "input", "tap", str(real_x), str(real_y)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300):
        s = self.scale or 1.0
        rx1, ry1 = int(x1/s), int(y1/s)
        rx2, ry2 = int(x2/s), int(y2/s)
        subprocess.Popen(
            [ADB, "-s", self.serial, "shell", "input", "swipe",
             str(rx1), str(ry1), str(rx2), str(ry2), str(duration)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def type_text(self, text: str):
        escaped = text.replace(" ", "%s").replace("'", "\\'").replace('"', '\\"')
        subprocess.Popen(
            [ADB, "-s", self.serial, "shell", "input", "text", f"'{escaped}'"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def key(self, keycode: str):
        KEYCODES = {
            "home": "3", "back": "4", "menu": "82", "power": "26",
            "enter": "66", "delete": "67", "tab": "61",
            "up": "19", "down": "20", "left": "21", "right": "22",
            "volume_up": "24", "volume_down": "25",
            "recent": "187", "notification": "83",
        }
        code = KEYCODES.get(keycode.lower(), keycode)
        subprocess.Popen(
            [ADB, "-s", self.serial, "shell", "input", "keyevent", str(code)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def long_press(self, x: int, y: int, duration: int = 1000):
        s = self.scale or 1.0
        rx, ry = int(x/s), int(y/s)
        subprocess.Popen(
            [ADB, "-s", self.serial, "shell", "input", "swipe",
             str(rx), str(ry), str(rx), str(ry), str(duration)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


# ── Web Server ──

async def create_app():
    from aiohttp import web

    app = web.Application()
    streamers: dict[str, DeviceStreamer] = {}

    def get_streamer(serial: str) -> DeviceStreamer:
        if serial not in streamers:
            streamers[serial] = DeviceStreamer(serial)
            asyncio.ensure_future(streamers[serial].start_streaming())
        return streamers[serial]

    async def ws_handler(request):
        serial = request.match_info["serial"]
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        streamer = get_streamer(serial)
        streamer.clients.add(ws)
        log.info(f"Client connected to {serial} ({len(streamer.clients)} total)")

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        cmd = data.get("cmd")
                        if cmd == "tap":
                            streamer.tap(data["x"], data["y"])
                        elif cmd == "swipe":
                            streamer.swipe(data["x1"], data["y1"], data["x2"], data["y2"],
                                           data.get("duration", 300))
                        elif cmd == "type":
                            streamer.type_text(data["text"])
                        elif cmd == "key":
                            streamer.key(data["key"])
                        elif cmd == "longpress":
                            streamer.long_press(data["x"], data["y"], data.get("duration", 1000))
                        elif cmd == "fps":
                            streamer.fps = max(1, min(30, int(data.get("value", 10))))
                        elif cmd == "quality":
                            streamer.quality = max(10, min(95, int(data.get("value", 40))))
                        elif cmd == "scale":
                            streamer.scale = max(0.25, min(1.0, float(data.get("value", 0.5))))
                    except Exception as e:
                        await ws.send_str(json.dumps({"error": str(e)}))
                elif msg.type == web.WSMsgType.ERROR:
                    break
        finally:
            streamer.clients.discard(ws)
            log.info(f"Client disconnected from {serial} ({len(streamer.clients)} left)")
            if not streamer.clients:
                # Auto-stop streaming if no clients
                pass

        return ws

    async def control_page(request):
        serial = request.match_info["serial"]
        html_path = Path(__file__).parent / "static" / "control.html"
        if html_path.exists():
            text = html_path.read_text()
            text = text.replace("{{SERIAL}}", serial)
            host = request.host
            ws_proto = "wss" if request.secure else "ws"
            text = text.replace("{{WS_URL}}", f"{ws_proto}://{host}/ws/{serial}")
            return web.Response(text=text, content_type="text/html")
        return web.Response(text="control.html not found", status=404)

    async def list_devices(request):
        r = subprocess.run([ADB, "devices", "-l"], capture_output=True, text=True, timeout=5)
        devices = []
        for line in r.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                serial = parts[0]
                model = ""
                for p in parts[2:]:
                    if p.startswith("model:"):
                        model = p.split(":")[1]
                devices.append({"serial": serial, "model": model,
                                "streaming": serial in streamers and bool(streamers[serial].clients)})
        return web.json_response(devices)

    async def input_handler(request):
        serial = request.match_info["serial"]
        data = await request.json()
        streamer = get_streamer(serial)
        cmd = data.get("cmd")
        if cmd == "tap":
            streamer.tap(data["x"], data["y"])
        elif cmd == "swipe":
            streamer.swipe(data["x1"], data["y1"], data["x2"], data["y2"], data.get("duration", 300))
        elif cmd == "type":
            streamer.type_text(data["text"])
        elif cmd == "key":
            streamer.key(data["key"])
        return web.json_response({"ok": True})

    app.router.add_get("/ws/{serial}", ws_handler)
    app.router.add_get("/control/{serial}", control_page)
    app.router.add_get("/api/devices", list_devices)
    app.router.add_post("/api/input/{serial}", input_handler)
    app.router.add_static("/static", Path(__file__).parent / "static")

    # Index page
    async def index(request):
        devices = []
        r = subprocess.run([ADB, "devices", "-l"], capture_output=True, text=True, timeout=5)
        for line in r.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                serial = parts[0]
                model = ""
                for p in parts[2:]:
                    if p.startswith("model:"):
                        model = p.split(":")[1]
                devices.append({"serial": serial, "model": model})
        links = "".join(f'<li><a href="/control/{d["serial"]}">{d["model"] or d["serial"]}</a></li>' for d in devices)
        return web.Response(
            text=f'<html><body style="background:#0f1117;color:#dfe6e9;font-family:sans-serif;padding:40px">'
                 f'<h1>📱 Phone Farm — Remote Control</h1>'
                 f'<ul style="font-size:18px;line-height:2">{links}</ul></body></html>',
            content_type="text/html")

    app.router.add_get("/", index)
    return app


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8890)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    from aiohttp import web
    app = asyncio.get_event_loop().run_until_complete(create_app())
    log.info(f"Screen stream server on http://{args.host}:{args.port}")
    web.run_app(app, host=args.host, port=args.port, print=None)


if __name__ == "__main__":
    main()
