#!/usr/bin/env python3
"""
autodroid-dashboard — Master orchestrator for all Android ADB agents.

Agents:
  gemini   → port 8765  (chat + image generation)
  tiktok   → port 8766  (TikTok navigation)
  shopee   → port 8767  (Shopee browse/orders)
  whatsapp → port 8768  (chat list + send message)
  instagram→ port 8769  (feed + DM inbox)
  youtube  → port 8770  (search + play)
  playstore→ port 8771  (install apps)

Usage:
  python3 autodroid_dashboard.py status           # all agents health check
  python3 autodroid_dashboard.py start [agent]    # start one or all servers
  python3 autodroid_dashboard.py stop [agent]     # stop one or all
  python3 autodroid_dashboard.py restart [agent]  # restart
  python3 autodroid_dashboard.py devices          # list connected ADB devices
  python3 autodroid_dashboard.py test [agent]     # run smoke test
  python3 autodroid_dashboard.py server           # start dashboard API (port 8800)
"""

import sys
import json
import subprocess
import time
import signal
import os
import requests
from pathlib import Path
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

BASE = Path("/mnt/data/berkahkarya/skills/1ai-skills/automation")
WORKSPACE = Path.home() / ".openclaw/workspace"
DOWNLOADS = WORKSPACE / "downloads"

AGENTS = {
    "gemini": {
        "script": BASE / "autodroid-gemini-agent/scripts/gemini_agent.py",
        "port": 8765,
        "package": "com.google.android.apps.bard",
        "smoke_cmd": "status",
    },
    "tiktok": {
        "script": BASE / "autodroid-tiktok-agent/scripts/tiktok_agent.py",
        "port": 8766,
        "package": "com.ss.android.ugc.trill",
        "smoke_cmd": "status",
    },
    "shopee": {
        "script": BASE / "autodroid-shopee-agent/scripts/shopee_agent.py",
        "port": 8767,
        "package": "com.shopee.id",
        "smoke_cmd": "status",
    },
    "whatsapp": {
        "script": BASE / "autodroid-whatsapp-agent/scripts/whatsapp_agent.py",
        "port": 8768,
        "package": "com.whatsapp",
        "smoke_cmd": "status",
    },
    "instagram": {
        "script": BASE / "autodroid-instagram-agent/scripts/instagram_agent.py",
        "port": 8769,
        "package": "com.instagram.android",
        "smoke_cmd": "status",
    },
    "youtube": {
        "script": BASE / "autodroid-youtube-agent/scripts/youtube_agent.py",
        "port": 8770,
        "package": "com.google.android.youtube",
        "smoke_cmd": "status",
    },
    "playstore": {
        "script": BASE / "autodroid-playstore-agent/scripts/playstore_agent.py",
        "port": 8771,
        "package": "com.android.vending",
        "smoke_cmd": "devices",
    },
    "device": {
        "script": BASE / "autodroid-device-agent/scripts/device_agent.py",
        "port": 8772,
        "package": "system",
        "smoke_cmd": "battery",
    },
}

PID_DIR = WORKSPACE / "run"
PID_DIR.mkdir(exist_ok=True)


# ─── ADB helpers ──────────────────────────────────────────────────────────────

def adb(cmd, device=None, timeout=10):
    prefix = ["adb"] + (["-s", device] if device else []) + ["shell"]
    try:
        r = subprocess.run(prefix + cmd.split(), capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def list_devices():
    r = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devices = []
    for line in r.stdout.strip().splitlines()[1:]:
        if "\tdevice" in line:
            serial = line.split("\t")[0].strip()
            model = adb("getprop ro.product.model", device=serial)
            android = adb("getprop ro.build.version.release", device=serial)
            devices.append({"serial": serial, "model": model, "android": android})
    return devices


# ─── Process management ───────────────────────────────────────────────────────

def pid_file(name):
    return PID_DIR / f"autodroid_{name}.pid"


def save_pid(name, pid):
    pid_file(name).write_text(str(pid))


def load_pid(name):
    pf = pid_file(name)
    if pf.exists():
        try:
            return int(pf.read_text().strip())
        except Exception:
            pass
    return None


def is_running(name):
    pid = load_pid(name)
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        pid_file(name).unlink(missing_ok=True)
        return False


def is_port_alive(port):
    try:
        r = requests.get(f"http://localhost:{port}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        try:
            r = requests.get(f"http://localhost:{port}/status", timeout=2)
            return r.status_code == 200
        except Exception:
            return False


def start_agent(name, device=None):
    if name not in AGENTS:
        return {"ok": False, "error": f"Unknown agent: {name}"}
    cfg = AGENTS[name]
    script = cfg["script"]
    if not script.exists():
        return {"ok": False, "error": f"Script not found: {script}"}
    if is_running(name):
        return {"ok": True, "message": f"{name} already running (pid={load_pid(name)})"}

    cmd = [sys.executable, str(script), "server", "--port", str(cfg["port"])]
    if device:
        cmd += ["--device", device]

    log_path = WORKSPACE / "logs" / f"autodroid_{name}.log"
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "a") as lf:
        proc = subprocess.Popen(cmd, stdout=lf, stderr=lf)
    save_pid(name, proc.pid)
    time.sleep(2)
    alive = is_port_alive(cfg["port"])
    return {"ok": alive, "name": name, "pid": proc.pid, "port": cfg["port"], "alive": alive}


def stop_agent(name):
    pid = load_pid(name)
    if not pid:
        return {"ok": True, "message": f"{name} not running"}
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)
        pid_file(name).unlink(missing_ok=True)
        return {"ok": True, "name": name, "stopped_pid": pid}
    except ProcessLookupError:
        pid_file(name).unlink(missing_ok=True)
        return {"ok": True, "name": name, "message": "process already dead"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def agent_status_all():
    results = {}
    for name, cfg in AGENTS.items():
        running = is_running(name)
        port_ok = is_port_alive(cfg["port"]) if running else False
        # Check install via quick adb pm
        installed_raw = adb(f"pm list packages {cfg['package']}")
        installed = cfg["package"] in installed_raw
        results[name] = {
            "running": running,
            "pid": load_pid(name),
            "port": cfg["port"],
            "port_alive": port_ok,
            "installed": installed,
            "script_exists": cfg["script"].exists(),
        }
    return results


def smoke_test(name, device=None):
    if name not in AGENTS:
        return {"ok": False, "error": f"Unknown agent: {name}"}
    cfg = AGENTS[name]
    script = cfg["script"]
    if not script.exists():
        return {"ok": False, "error": f"Missing script: {script}"}
    cmd = [sys.executable, str(script), cfg["smoke_cmd"]]
    if device:
        cmd += ["--device", device]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            data = json.loads(r.stdout)
            data["smoke_test"] = "passed"
            return data
        else:
            return {"ok": False, "error": r.stderr.strip() or r.stdout.strip()}
    except json.JSONDecodeError:
        return {"ok": False, "error": "non-JSON output", "raw": r.stdout[:200]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─── CLI ──────────────────────────────────────────────────────────────────────

def cmd_devices():
    devs = list_devices()
    print(json.dumps({"ok": True, "devices": devs, "count": len(devs)}, indent=2))


def cmd_status():
    statuses = agent_status_all()
    devices = list_devices()
    summary = {
        "timestamp": datetime.now().isoformat(),
        "devices": devices,
        "device_count": len(devices),
        "agents": statuses,
        "running_count": sum(1 for v in statuses.values() if v["running"]),
        "installed_count": sum(1 for v in statuses.values() if v["installed"]),
    }
    print(json.dumps(summary, indent=2))


def cmd_start(agent=None, device=None):
    targets = [agent] if agent and agent in AGENTS else list(AGENTS.keys())
    results = {}
    for name in targets:
        print(f"[start] Starting {name}...", file=sys.stderr)
        results[name] = start_agent(name, device=device)
    print(json.dumps({"ok": True, "results": results}, indent=2))


def cmd_stop(agent=None):
    targets = [agent] if agent and agent in AGENTS else list(AGENTS.keys())
    results = {}
    for name in targets:
        results[name] = stop_agent(name)
    print(json.dumps({"ok": True, "results": results}, indent=2))


def cmd_restart(agent=None, device=None):
    targets = [agent] if agent and agent in AGENTS else list(AGENTS.keys())
    results = {}
    for name in targets:
        stop_agent(name)
        time.sleep(1)
        results[name] = start_agent(name, device=device)
    print(json.dumps({"ok": True, "results": results}, indent=2))


def cmd_test(agent=None, device=None):
    targets = [agent] if agent and agent in AGENTS else list(AGENTS.keys())
    results = {}
    for name in targets:
        print(f"[test] Testing {name}...", file=sys.stderr)
        results[name] = smoke_test(name, device=device)
    passed = sum(1 for v in results.values() if v.get("ok"))
    print(json.dumps({"ok": passed == len(targets), "passed": passed, "total": len(targets), "results": results}, indent=2))


def cmd_server(port=8800):
    """Start dashboard FastAPI server."""
    try:
        from fastapi import FastAPI
        import uvicorn
    except ImportError:
        print("pip install fastapi uvicorn", file=sys.stderr)
        sys.exit(1)

    app = FastAPI(title="autodroid-dashboard", version="1.0")

    @app.get("/status")
    def get_status():
        statuses = agent_status_all()
        devices = list_devices()
        return {"ok": True, "devices": devices, "agents": statuses,
                "running_count": sum(1 for v in statuses.values() if v["running"])}

    @app.get("/devices")
    def get_devices():
        return {"ok": True, "devices": list_devices()}

    @app.post("/start/{agent}")
    def post_start(agent: str, device: str = None):
        if agent == "all":
            results = {n: start_agent(n, device=device) for n in AGENTS}
            return {"ok": True, "results": results}
        return start_agent(agent, device=device)

    @app.post("/stop/{agent}")
    def post_stop(agent: str):
        if agent == "all":
            results = {n: stop_agent(n) for n in AGENTS}
            return {"ok": True, "results": results}
        return stop_agent(agent)

    @app.post("/restart/{agent}")
    def post_restart(agent: str, device: str = None):
        targets = list(AGENTS.keys()) if agent == "all" else [agent]
        results = {}
        for n in targets:
            stop_agent(n)
            time.sleep(0.5)
            results[n] = start_agent(n, device=device)
        return {"ok": True, "results": results}

    @app.get("/test/{agent}")
    def get_test(agent: str, device: str = None):
        targets = list(AGENTS.keys()) if agent == "all" else [agent]
        results = {n: smoke_test(n, device=device) for n in targets}
        passed = sum(1 for v in results.values() if v.get("ok"))
        return {"ok": passed == len(targets), "passed": passed, "total": len(targets), "results": results}

    @app.get("/health")
    def health():
        return {"status": "ok", "agents": list(AGENTS.keys())}

    @app.get("/ports")
    def get_ports():
        return {"ok": True, "ports": {n: c["port"] for n, c in AGENTS.items()}}

    print(f"[dashboard] Starting on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[dashboard] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    agent = args[1] if len(args) > 1 and not args[1].startswith("--") else None
    device = None
    port = 8800

    for i, a in enumerate(args):
        if a == "--device" and i + 1 < len(args):
            device = args[i + 1]
        if a == "--port" and i + 1 < len(args):
            port = int(args[i + 1])

    if cmd == "devices":
        cmd_devices()
    elif cmd == "status":
        cmd_status()
    elif cmd == "start":
        cmd_start(agent, device=device)
    elif cmd == "stop":
        cmd_stop(agent)
    elif cmd == "restart":
        cmd_restart(agent, device=device)
    elif cmd == "test":
        cmd_test(agent, device=device)
    elif cmd == "server":
        cmd_server(port=port)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
