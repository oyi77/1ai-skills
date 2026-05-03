#!/usr/bin/env python3
"""Phone Farm Daemon - CLI wrapper for FastAPI server."""

import argparse
import os
import signal
import sys
import time
from pathlib import Path

PID_FILE = Path(__file__).parent / "farm_daemon.pid"


def start_daemon(host: str, port: int, debug: bool = False):
    """Start the Phone Farm FastAPI server."""
    import uvicorn
    from src.api.server import create_app

    app = create_app()

    print(f"Starting Phone Farm server on {host}:{port}...")
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info",
    )


def stop_daemon():
    """Stop the running daemon."""
    if not PID_FILE.exists():
        print("Daemon is not running (no PID file found).")
        return

    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink()
        print(f"Daemon stopped (PID {pid}).")
    except ProcessLookupError:
        print(f"Process {pid} not found. Cleaning up PID file.")
        PID_FILE.unlink()
    except Exception as e:
        print(f"Error stopping daemon: {e}")


def status_daemon():
    """Check daemon status."""
    if not PID_FILE.exists():
        print("Daemon is not running.")
        return

    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)
        print(f"Daemon is running (PID {pid}).")
    except ProcessLookupError:
        print(f"Daemon is not running (stale PID file).")
        PID_FILE.unlink()


def main():
    parser = argparse.ArgumentParser(description="Phone Farm Daemon")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    start_parser = subparsers.add_parser("start", help="Start the server")
    start_parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    start_parser.add_argument("--port", type=int, default=8889, help="Port number")
    start_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    subparsers.add_parser("stop", help="Stop the server")
    subparsers.add_parser("status", help="Check server status")

    args = parser.parse_args()

    if args.command == "start":
        start_daemon(args.host, args.port, args.debug)
    elif args.command == "stop":
        stop_daemon()
    elif args.command == "status":
        status_daemon()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
