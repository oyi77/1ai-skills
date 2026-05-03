#!/usr/bin/env python3
"""
Phone Farm CLI — Unified command-line interface for the phone farm.

Usage:
  farm_cli.py status                     # Show all devices + daemon status
  farm_cli.py devices                    # List connected devices
  farm_cli.py health                     # Run health checks on all devices
  farm_cli.py screenshot [SERIAL]        # Take screenshot (all or specific)
  farm_cli.py task TASK [--device SER]   # Run a task
  farm_cli.py launch SERIAL PACKAGE      # Launch app on device
  farm_cli.py tap SERIAL X Y             # Tap coordinates
  farm_cli.py type SERIAL "text"         # Type text
  farm_cli.py key SERIAL KEY             # Press key (HOME/BACK/etc)
  farm_cli.py shell SERIAL "command"     # Raw ADB shell
  farm_cli.py daemon start [--mode M]    # Start daemon (bg)
  farm_cli.py daemon stop                # Stop daemon
  farm_cli.py daemon status              # Daemon status
  farm_cli.py add SERIAL NAME            # Register new device
  farm_cli.py logs [--lines N]           # Show recent logs
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from device_manager import DeviceManager
from task_runner import TaskRunner
from farm_daemon import FarmDaemon, STATE_FILE, PID_FILE

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "devices.json"
LOGS_DIR = Path(__file__).parent.parent.parent / "logs" / "phone-farm"


def cmd_status(args):
    dm = DeviceManager()
    dm.refresh_all()
    
    print("=" * 60)
    print("📱 PHONE FARM STATUS")
    print("=" * 60)
    
    # Daemon status
    daemon_state = FarmDaemon.get_status()
    if daemon_state.get("pid"):
        uptime = daemon_state.get("uptime_seconds", 0)
        h, m = divmod(uptime, 3600)
        m, s = divmod(m, 60)
        print(f"\n🤖 Daemon: ✅ RUNNING (PID {daemon_state['pid']}, mode={daemon_state.get('mode','?')}, uptime={int(h)}h{int(m)}m)")
        stats = daemon_state.get("stats", {})
        print(f"   Tasks: {stats.get('tasks_run',0)} run, {stats.get('tasks_failed',0)} failed")
        print(f"   Screenshots: {stats.get('screenshots_taken',0)}")
        print(f"   Reconnects: {stats.get('reconnects',0)}")
        print(f"   Alerts: {stats.get('alerts_sent',0)}")
    else:
        print(f"\n🤖 Daemon: ❌ NOT RUNNING")

    # Devices
    print(f"\n📱 Devices ({len(dm.devices)} registered):")
    print("-" * 60)
    for serial, state in dm.devices.items():
        icon = "✅" if state.connected else "❌"
        bat = f"{state.battery}%" if state.battery >= 0 else "?"
        screen = "🟢" if state.screen_on else "⚫"
        app = state.current_app or "-"
        print(f"  {icon} {state.name} ({state.model})")
        print(f"     Serial: {serial}")
        print(f"     Battery: {bat} | Screen: {screen} | App: {app}")
        print(f"     Skills: {', '.join(state.assigned_skills) or 'none'}")
        if state.last_error:
            print(f"     ⚠️ Error: {state.last_error}")
        print()

    # Recent alerts
    if daemon_state.get("recent_alerts"):
        print("🚨 Recent Alerts:")
        for alert in daemon_state["recent_alerts"][-5:]:
            print(f"  [{alert.get('time_str','')}] {alert.get('message','')}")


def cmd_devices(args):
    dm = DeviceManager()
    dm.refresh_all()
    print(json.dumps(dm.to_dict(), indent=2))


def cmd_health(args):
    runner = TaskRunner()
    results = runner.run_all_health_checks()
    for r in results:
        print(json.dumps(asdict(r), indent=2))


def cmd_screenshot(args):
    dm = DeviceManager()
    dm.refresh_all()
    serial = args.serial
    if serial:
        path = dm.screenshot(serial)
        print(f"Screenshot saved: {path}")
    else:
        for s, state in dm.devices.items():
            if state.connected:
                try:
                    path = dm.screenshot(s)
                    print(f"{state.name}: {path}")
                except Exception as e:
                    print(f"{state.name}: FAILED - {e}")


def cmd_task(args):
    runner = TaskRunner()
    runner.dm.refresh_all()
    if args.device:
        result = runner.run_task(args.device, args.task)
        print(json.dumps(asdict(result), indent=2))
    else:
        for serial, state in runner.dm.devices.items():
            if state.connected:
                result = runner.run_task(serial, args.task)
                print(json.dumps(asdict(result), indent=2))


def cmd_launch(args):
    dm = DeviceManager()
    dm.launch_app(args.serial, args.package)
    print(f"Launched {args.package} on {args.serial}")


def cmd_tap(args):
    dm = DeviceManager()
    dm.tap(args.serial, int(args.x), int(args.y))
    print(f"Tapped ({args.x}, {args.y}) on {args.serial}")


def cmd_type(args):
    dm = DeviceManager()
    dm.type_text(args.serial, args.text)
    print(f"Typed on {args.serial}")


def cmd_key(args):
    dm = DeviceManager()
    dm.press_key(args.serial, args.key)
    print(f"Pressed {args.key} on {args.serial}")


def cmd_shell(args):
    dm = DeviceManager()
    result = dm._shell(args.serial, args.command)
    print(result)


def cmd_daemon(args):
    if args.daemon_cmd == "start":
        # Check if already running
        if PID_FILE.exists():
            pid = PID_FILE.read_text().strip()
            try:
                os.kill(int(pid), 0)
                print(f"Daemon already running (PID {pid})")
                return
            except ProcessLookupError:
                PID_FILE.unlink()

        mode = args.mode or "monitor"
        script = Path(__file__).parent / "farm_daemon.py"
        log_path = LOGS_DIR / "daemon.log"
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Start as background process
        cmd = [sys.executable, str(script), "--mode", mode]
        with open(log_path, "a") as log_f:
            proc = subprocess.Popen(
                cmd,
                stdout=log_f,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        print(f"✅ Daemon started (PID {proc.pid}, mode={mode})")
        print(f"   Logs: {log_path}")

    elif args.daemon_cmd == "stop":
        if PID_FILE.exists():
            pid = int(PID_FILE.read_text().strip())
            try:
                os.kill(pid, 15)  # SIGTERM
                print(f"✅ Sent SIGTERM to PID {pid}")
                time.sleep(1)
                try:
                    os.kill(pid, 0)
                    os.kill(pid, 9)  # Force kill
                    print(f"   Force killed PID {pid}")
                except ProcessLookupError:
                    pass
            except ProcessLookupError:
                print(f"PID {pid} not running")
            PID_FILE.unlink(missing_ok=True)
        else:
            print("Daemon not running")

    elif args.daemon_cmd == "status":
        state = FarmDaemon.get_status()
        print(json.dumps(state, indent=2))

    elif args.daemon_cmd == "restart":
        # Stop then start
        args.daemon_cmd = "stop"
        cmd_daemon(args)
        time.sleep(2)
        args.daemon_cmd = "start"
        cmd_daemon(args)


def cmd_add(args):
    config = {}
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
    
    if "devices" not in config:
        config["devices"] = {}
    
    config["devices"][args.serial] = {
        "name": args.name,
        "model": "",
        "android": "",
        "connection": "usb",
        "assigned_skills": [],
        "installed_apps": {},
        "auto_tasks": {
            "screenshot_interval_sec": 60,
            "health_check_interval_sec": 300,
            "task_loop_interval_sec": 120,
        },
        "enabled": True,
    }
    
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Added device {args.serial} as '{args.name}'")
    
    # Auto-detect model
    dm = DeviceManager()
    dm.refresh_all()
    state = dm.devices.get(args.serial)
    if state and state.connected:
        config["devices"][args.serial]["model"] = state.model
        config["devices"][args.serial]["android"] = state.android
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        print(f"   Model: {state.model}, Android: {state.android}")


def cmd_logs(args):
    lines = args.lines or 50
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"{today}.jsonl"
    daemon_log = LOGS_DIR / "daemon.log"
    
    if log_file.exists():
        print(f"=== Task logs ({today}) ===")
        all_lines = log_file.read_text().strip().split("\n")
        for line in all_lines[-lines:]:
            try:
                entry = json.loads(line)
                status = "✅" if entry.get("success") else "❌"
                print(f"  {status} [{entry.get('timestamp','')}] "
                      f"{entry.get('task_type','')} on {entry.get('device_name','')} "
                      f"({entry.get('duration_ms',0)}ms)")
            except json.JSONDecodeError:
                print(f"  {line}")
    
    if daemon_log.exists():
        print(f"\n=== Daemon log (last {lines} lines) ===")
        all_lines = daemon_log.read_text().strip().split("\n")
        for line in all_lines[-lines:]:
            print(f"  {line}")


def main():
    parser = argparse.ArgumentParser(description="📱 Phone Farm CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Farm status overview")
    sub.add_parser("devices", help="List devices (JSON)")
    sub.add_parser("health", help="Health check all devices")

    p_ss = sub.add_parser("screenshot", help="Take screenshot")
    p_ss.add_argument("serial", nargs="?", help="Device serial")

    p_task = sub.add_parser("task", help="Run task on device(s)")
    p_task.add_argument("task", help="Task type")
    p_task.add_argument("--device", "-d", help="Device serial")

    p_launch = sub.add_parser("launch", help="Launch app")
    p_launch.add_argument("serial")
    p_launch.add_argument("package")

    p_tap = sub.add_parser("tap", help="Tap coordinates")
    p_tap.add_argument("serial")
    p_tap.add_argument("x")
    p_tap.add_argument("y")

    p_type = sub.add_parser("type", help="Type text")
    p_type.add_argument("serial")
    p_type.add_argument("text")

    p_key = sub.add_parser("key", help="Press key")
    p_key.add_argument("serial")
    p_key.add_argument("key")

    p_shell = sub.add_parser("shell", help="ADB shell command")
    p_shell.add_argument("serial")
    p_shell.add_argument("command")

    p_daemon = sub.add_parser("daemon", help="Manage daemon")
    p_daemon.add_argument("daemon_cmd", choices=["start", "stop", "status", "restart"])
    p_daemon.add_argument("--mode", choices=["monitor", "active", "dashboard"])

    p_add = sub.add_parser("add", help="Register new device")
    p_add.add_argument("serial")
    p_add.add_argument("name")

    p_logs = sub.add_parser("logs", help="Show recent logs")
    p_logs.add_argument("--lines", "-n", type=int, default=50)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmd_map = {
        "status": cmd_status,
        "devices": cmd_devices,
        "health": cmd_health,
        "screenshot": cmd_screenshot,
        "task": cmd_task,
        "launch": cmd_launch,
        "tap": cmd_tap,
        "type": cmd_type,
        "key": cmd_key,
        "shell": cmd_shell,
        "daemon": cmd_daemon,
        "add": cmd_add,
        "logs": cmd_logs,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
