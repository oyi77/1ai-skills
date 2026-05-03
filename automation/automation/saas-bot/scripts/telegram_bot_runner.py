#!/usr/bin/env python3
"""
Telegram Bot Runner — one-shot or watch mode for OpenClaw Video Studio.
"""

import subprocess
import sys
import os
import time
import signal

PROJECT_DIR = "/home/openclaw/.openclaw/workspace/projects/openclaw-saas-bot"


def run(watch: bool = False) -> None:
    cmd = ["pnpm", "dev" if watch else "start"]
    env = os.environ.copy()

    if watch:
        print("Starting in watch mode (tsx watch)...")
        proc = subprocess.Popen(cmd, cwd=PROJECT_DIR, env=env)
        try:
            proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
            proc.wait()
    else:
        print("Starting in production mode...")
        os.execvp("pnpm", cmd)


if __name__ == "__main__":
    watch = "--watch" in sys.argv or "-w" in sys.argv
    run(watch=watch)
