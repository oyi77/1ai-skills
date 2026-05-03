#!/usr/bin/env python3
"""
SaaS Bot Manager — start, stop, restart, status for OpenClaw Video Studio.
"""

import subprocess
import sys
import os
import time
import signal

PROJECT_DIR = "/home/openclaw/.openclaw/workspace/projects/openclaw-saas-bot"
PID_FILE = "/tmp/saas-bot.pid"
ENV_FILE = os.path.join(PROJECT_DIR, ".env")


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def start(background: bool = True) -> None:
    if is_running():
        print("SaaS bot already running")
        return

    if not os.path.exists(PROJECT_DIR):
        print(f"Project not found: {PROJECT_DIR}")
        sys.exit(1)

    if not os.path.exists(ENV_FILE):
        print(f".env not found: {ENV_FILE}")
        sys.exit(1)

    cmd = ["pnpm", "start"]
    if background:
        proc = subprocess.Popen(
            cmd,
            cwd=PROJECT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
        with open(PID_FILE, "w") as f:
            f.write(str(proc.pid))
        print(f"Started (PID {proc.pid})")
    else:
        os.execvp("pnpm", cmd)


def stop() -> None:
    if not is_running():
        print("SaaS bot not running")
        if os.path.exists(PID_FILE):
            os.unlink(PID_FILE)
        return

    with open(PID_FILE) as f:
        pid = int(f.read().strip())

    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        time.sleep(2)
        if os.path.exists(PID_FILE):
            os.unlink(PID_FILE)
        print("Stopped")
    except ProcessLookupError:
        print("Process already dead")
        if os.path.exists(PID_FILE):
            os.unlink(PID_FILE)


def restart() -> None:
    stop()
    time.sleep(1)
    start()


def status() -> None:
    if is_running():
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        print(f"Running (PID {pid})")
    else:
        print("Stopped")


def is_running() -> bool:
    if not os.path.exists(PID_FILE):
        return False
    with open(PID_FILE) as f:
        pid = int(f.read().strip())
    return pid_alive(pid)


def logs(lines: int = 50) -> None:
    log_path = os.path.join(PROJECT_DIR, "logs/bot.log")
    if os.path.exists(log_path):
        subprocess.run(["tail", f"-n{lines}", log_path])
    else:
        print("No log file found")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: saas_bot_manager.py {start|stop|restart|status|logs}")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "start":
        start(background=True)
    elif cmd == "start:fg":
        start(background=False)
    elif cmd == "stop":
        stop()
    elif cmd == "restart":
        restart()
    elif cmd == "status":
        status()
    elif cmd == "logs":
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        logs(lines)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
