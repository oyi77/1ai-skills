#!/usr/bin/env python3
"""
1ai-autodroid — Universal Android automation CLI.

Usage:
  autodroid.py screenshot [--path /tmp/screen.png]
  autodroid.py tap X Y
  autodroid.py swipe x1 y1 x2 y2 [duration_ms]
  autodroid.py type "text to type"
  autodroid.py key HOME|BACK|POWER|ENTER|<keycode>
  autodroid.py launch <package>
  autodroid.py status
  autodroid.py unlock [PIN]
  autodroid.py pull-screen   # just pull without analysis

Key codes: HOME=3, BACK=4, MENU=82, POWER=26, ENTER=66
"""

import subprocess
import sys
import os
import time
from pathlib import Path

ADB = os.path.expanduser("~/.local/bin/adb")
if not Path(ADB).exists():
    ADB = "adb"  # fallback to system PATH

KEYCODES = {
    "HOME": 3, "BACK": 4, "MENU": 82, "POWER": 26,
    "ENTER": 66, "TAB": 61, "DEL": 67, "CAMERA": 27,
    "VOLUME_UP": 24, "VOLUME_DOWN": 25,
}


def run(cmd: str, capture=True):
    result = subprocess.run(
        f"{ADB} {cmd}", shell=True,
        capture_output=capture, text=True
    )
    return result.stdout.strip() if capture else None


def screenshot(path="/tmp/autodroid_screen.png"):
    remote = "/sdcard/autodroid_cap.png"
    run(f"shell screencap {remote}")
    run(f"pull {remote} {path}")
    size = Path(path).stat().st_size if Path(path).exists() else 0
    print(f"Screenshot saved: {path} ({size//1024}KB)")
    return path


def tap(x, y):
    run(f"shell input tap {x} {y}")
    print(f"Tapped: ({x}, {y})")


def swipe(x1, y1, x2, y2, duration=300):
    run(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    print(f"Swiped: ({x1},{y1}) → ({x2},{y2})")


def type_text(text):
    # Escape special chars for shell
    escaped = text.replace(" ", "%s").replace("&", "\\&")
    run(f"shell input text '{escaped}'")
    print(f"Typed: {text}")


def press_key(key):
    code = KEYCODES.get(key.upper(), key)
    run(f"shell input keyevent {code}")
    print(f"Key: {key} ({code})")


def launch_app(package):
    run(f"shell monkey -p {package} -c android.intent.category.LAUNCHER 1")
    time.sleep(2)
    print(f"Launched: {package}")


def status():
    devices = run("devices -l")
    print("=== ADB Devices ===")
    print(devices)
    # Get phone info if connected
    model = run("shell getprop ro.product.model")
    android = run("shell getprop ro.build.version.release")
    resolution = run("shell wm size")
    battery = run("shell dumpsys battery | grep level")
    print(f"\nModel: {model}")
    print(f"Android: {android}")
    print(f"Resolution: {resolution}")
    print(f"Battery: {battery.strip()}")


def unlock(pin=None):
    run("shell input keyevent 26")  # wake
    time.sleep(0.5)
    run("shell input keyevent 82")  # unlock
    time.sleep(0.5)
    if pin:
        run(f"shell input text {pin}")
        run("shell input keyevent 66")  # ENTER
    print("Screen unlocked")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == "screenshot":
        path = args[0] if args else "/tmp/autodroid_screen.png"
        screenshot(path)

    elif cmd == "pull-screen":
        screenshot()

    elif cmd == "tap":
        if len(args) < 2:
            print("Usage: autodroid.py tap X Y")
            sys.exit(1)
        tap(int(args[0]), int(args[1]))

    elif cmd == "swipe":
        if len(args) < 4:
            print("Usage: autodroid.py swipe x1 y1 x2 y2 [duration_ms]")
            sys.exit(1)
        dur = int(args[4]) if len(args) > 4 else 300
        swipe(int(args[0]), int(args[1]), int(args[2]), int(args[3]), dur)

    elif cmd == "type":
        if not args:
            print("Usage: autodroid.py type 'text'")
            sys.exit(1)
        type_text(args[0])

    elif cmd == "key":
        if not args:
            print(f"Usage: autodroid.py key KEY\nKeys: {list(KEYCODES.keys())}")
            sys.exit(1)
        press_key(args[0])

    elif cmd == "launch":
        if not args:
            print("Usage: autodroid.py launch com.package.name")
            sys.exit(1)
        launch_app(args[0])

    elif cmd == "status":
        status()

    elif cmd == "unlock":
        pin = args[0] if args else None
        unlock(pin)

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
