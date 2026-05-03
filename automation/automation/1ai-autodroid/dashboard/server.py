#!/usr/bin/env python3
"""
Autodroid Dashboard Server — FastAPI multi-device manager for Android farm.

Endpoints:
  GET  /devices                              → List connected devices
  GET  /device/{serial}/screenshot           → PNG binary screenshot
  POST /device/{serial}/skill/{skill_name}   → Run skill command
  WS   /ws/devices                           → Real-time device list (5s interval)
  GET  /skills                               → List available autodroid skills

Usage:
  python3 dashboard/server.py [--port 8888]
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("[dashboard] Installing FastAPI + uvicorn...", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"],
        check=True,
    )
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.responses import FileResponse
    from pydantic import BaseModel
    import uvicorn

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR.parent
AUTODROID_SCRIPT = BASE_DIR / "scripts" / "autodroid.py"
SCREENSHOTS_DIR = Path("/tmp/autodroid_screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

ADB = os.path.expanduser("~/.local/bin/adb")
if not Path(ADB).exists():
    ADB = "adb"


class SkillRequest(BaseModel):
    command: str
    params: Optional[dict] = None


class DeviceInfo(BaseModel):
    serial: str
    model: str
    battery: int
    status: str


class SkillResponse(BaseModel):
    result: dict
    screenshot: str


def adb_cmd(args: list[str], device: str | None = None) -> subprocess.CompletedProcess:
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += args
    return subprocess.run(cmd, capture_output=True, text=True)


def get_connected_devices() -> list[str]:
    r = adb_cmd(["devices"])
    if r.returncode != 0:
        return []
    devices = []
    for line in r.stdout.strip().split("\n")[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def get_device_info(serial: str) -> dict:
    r = adb_cmd(["shell", "getprop", "ro.product.model"], device=serial)
    model = r.stdout.strip() if r.returncode == 0 else "Unknown"

    r = adb_cmd(["shell", "dumpsys", "battery"], device=serial)
    battery = 0
    if r.returncode == 0:
        for line in r.stdout.split("\n"):
            if "level:" in line:
                try:
                    battery = int(line.split(":")[1].strip())
                except ValueError:
                    pass
                break

    status = "ok"

    return {
        "serial": serial,
        "model": model,
        "battery": battery,
        "status": status,
    }


def take_screenshot(serial: str) -> str:
    ts = int(time.time() * 1000)
    local_path = str(SCREENSHOTS_DIR / f"{serial}_{ts}.png")
    remote_path = "/sdcard/autodroid_screenshot.png"

    adb_cmd(["shell", "screencap", remote_path], device=serial)
    r = adb_cmd(["pull", remote_path, local_path], device=serial)
    if r.returncode != 0:
        raise RuntimeError(f"Screenshot failed: {r.stderr}")

    return local_path


def discover_skills() -> list[dict]:
    skills = []

    for agent_dir in SKILLS_DIR.glob("autodroid-*-agent"):
        scripts_dir = agent_dir / "scripts"
        if not scripts_dir.exists():
            continue

        for script in scripts_dir.glob("*_agent.py"):
            skill_name = script.stem.replace("_agent", "")
            skills.append(
                {
                    "name": skill_name,
                    "path": str(script),
                    "agent_dir": str(agent_dir),
                }
            )

    return skills


def run_skill(skill_name: str, command: str, params: dict | None, device: str) -> dict:
    skills = discover_skills()
    skill = next((s for s in skills if s["name"] == skill_name), None)
    if not skill:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found. Available: {[s['name'] for s in skills]}",
        )

    script_path = skill["path"]

    cmd_args = ["python3", script_path, command]
    if params:
        for key, value in params.items():
            cmd_args.extend([f"--{key}", str(value)])
    cmd_args.extend(["--device", device])

    env = os.environ.copy()
    env["ANDROID_SERIAL"] = device
    r = subprocess.run(cmd_args, capture_output=True, text=True, env=env)

    result = {}
    if r.stdout:
        try:
            result = json.loads(r.stdout.strip())
        except json.JSONDecodeError:
            for line in r.stdout.split("\n"):
                line = line.strip()
                if line.startswith("{"):
                    try:
                        result = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        pass
            if not result:
                result = {"output": r.stdout}

    if r.returncode != 0 and not result:
        result = {"error": r.stderr or "Command failed"}

    screenshot_path = ""
    try:
        screenshot_path = take_screenshot(device)
    except Exception:
        pass

    return {
        "result": result,
        "screenshot": screenshot_path,
    }


app = FastAPI(
    title="Autodroid Dashboard",
    description="Multi-device Android farm manager",
    version="1.0.0",
)


@app.get("/devices", response_model=list[DeviceInfo])
async def list_devices():
    """List all connected Android devices with model, battery, and status."""
    serials = get_connected_devices()
    devices = []
    for serial in serials:
        info = get_device_info(serial)
        devices.append(DeviceInfo(**info))
    return devices


@app.get("/device/{serial}/screenshot")
async def device_screenshot(serial: str):
    """Take and return a PNG screenshot from the specified device."""
    serials = get_connected_devices()
    if serial not in serials:
        raise HTTPException(
            status_code=404,
            detail=f"Device {serial} not connected. Available: {serials}",
        )

    try:
        path = take_screenshot(serial)
        return FileResponse(path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/device/{serial}/skill/{skill_name}")
async def run_device_skill(serial: str, skill_name: str, req: SkillRequest):
    """
    Run a skill command on a device.

    Example:
      POST /device/SGZTONV.../skill/gemini
      Body: {"command": "chat", "params": {"prompt": "hello"}}
    """
    serials = get_connected_devices()
    if serial not in serials:
        raise HTTPException(
            status_code=404,
            detail=f"Device {serial} not connected. Available: {serials}",
        )

    result = run_skill(skill_name, req.command, req.params, serial)
    return SkillResponse(**result)


@app.get("/skills")
async def list_skills():
    """List all available autodroid-*-agent skills."""
    return discover_skills()


@app.websocket("/ws/devices")
async def websocket_devices(websocket: WebSocket):
    """
    Real-time device list via WebSocket.
    Streams device updates every 5 seconds.
    """
    await websocket.accept()
    try:
        while True:
            serials = get_connected_devices()
            devices = []
            for serial in serials:
                info = get_device_info(serial)
                devices.append(info)

            await websocket.send_json({"devices": devices, "timestamp": time.time()})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Autodroid Dashboard Server")
    parser.add_argument("--port", type=int, default=8888, help="Server port")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    args = parser.parse_args()

    print(f"[dashboard] Starting on http://{args.host}:{args.port}", file=sys.stderr)
    print(f"[dashboard] Skills dir: {SKILLS_DIR}", file=sys.stderr)
    print(
        f"[dashboard] Discovered skills: {[s['name'] for s in discover_skills()]}",
        file=sys.stderr,
    )

    uvicorn.run(app, host=args.host, port=args.port)
