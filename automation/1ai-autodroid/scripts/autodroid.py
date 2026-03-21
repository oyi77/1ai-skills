#!/usr/bin/env python3
"""
1ai-autodroid — Universal Android automation CLI.

Usage:
  autodroid.py status
  autodroid.py screenshot [path]
  autodroid.py tap X Y
  autodroid.py swipe x1 y1 x2 y2 [duration_ms]
  autodroid.py type "text"
  autodroid.py key HOME|BACK|POWER|ENTER|MENU|<keycode>
  autodroid.py launch <package>
  autodroid.py unlock [PIN]
  autodroid.py ui-dump [output.xml]          # uiautomator dump
  autodroid.py find-text "text" [xml_file]  # find bounds for text
  autodroid.py tap-text "text"              # dump + find + tap (smart)
  autodroid.py install <apk_path>
  autodroid.py wifi-connect <ip> [port]     # ADB over WiFi
  autodroid.py shell <command>              # raw adb shell

Key codes: HOME=3, BACK=4, MENU=82, POWER=26, ENTER=66
"""

import subprocess
import sys
import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

# ─── ADB path resolution ────────────────────────────────────────────────────
ADB = os.path.expanduser("~/.local/bin/adb")
if not Path(ADB).exists():
    ADB = "adb"

KEYCODES = {
    "HOME": 3, "BACK": 4, "MENU": 82, "POWER": 26,
    "ENTER": 66, "TAB": 61, "DEL": 67, "CAMERA": 27,
    "VOLUME_UP": 24, "VOLUME_DOWN": 25, "SEARCH": 84,
    "DPAD_UP": 19, "DPAD_DOWN": 20, "DPAD_LEFT": 21, "DPAD_RIGHT": 22,
}


# ─── Core helpers ────────────────────────────────────────────────────────────
def run(cmd: str, capture=True, check=False):
    r = subprocess.run(f"{ADB} {cmd}", shell=True, capture_output=capture, text=True)
    if check and r.returncode != 0:
        print(f"ERROR: {r.stderr.strip()}", file=sys.stderr)
    return r.stdout.strip() if capture else None


def run_with_root_fallback(cmd: str):
    """Try non-root, fallback to su if fails."""
    r = subprocess.run(f"{ADB} shell {cmd}", shell=True, capture_output=True, text=True)
    if r.returncode == 0 and "Permission denied" not in r.stderr:
        return r.stdout.strip()
    # root fallback
    r2 = subprocess.run(f"{ADB} shell su -c '{cmd}'", shell=True, capture_output=True, text=True)
    return r2.stdout.strip()


# ─── Commands ────────────────────────────────────────────────────────────────
def screenshot(path="/tmp/autodroid_screen.png"):
    import time
    run_with_root_fallback("input keyevent 224")
    time.sleep(0.5)
    run_with_root_fallback("input swipe 360 1400 360 700")
    time.sleep(0.5)
    remote = "/sdcard/autodroid_cap.png"
    run(f"shell screencap {remote}")
    run(f"pull {remote} {path}")
    size = Path(path).stat().st_size if Path(path).exists() else 0
    print(f"Screenshot: {path} ({size//1024}KB)")
    return path


def tap(x, y):
    run_with_root_fallback(f"input tap {x} {y}")
    print(f"Tapped: ({x}, {y})")


def swipe(x1, y1, x2, y2, duration=300):
    run_with_root_fallback(f"input swipe {x1} {y1} {x2} {y2} {duration}")
    print(f"Swiped: ({x1},{y1})→({x2},{y2}) {duration}ms")


def type_text(text):
    # Escape special chars
    escaped = text.replace("\\", "\\\\").replace(" ", "%s").replace("'", "\\'")
    run_with_root_fallback(f"input text '{escaped}'")
    print(f"Typed: {text}")


def press_key(key):
    code = KEYCODES.get(key.upper(), key)
    run_with_root_fallback(f"input keyevent {code}")
    print(f"Key: {key} ({code})")


def launch_app(package):
    run_with_root_fallback(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
    time.sleep(2)
    print(f"Launched: {package}")


def status():
    devices = run("devices -l")
    print("=== ADB Devices ===")
    print(devices)
    model = run("shell getprop ro.product.model")
    android = run("shell getprop ro.build.version.release")
    resolution = run("shell wm size")
    density = run("shell wm density")
    battery = run("shell dumpsys battery | grep level")
    focus = run("shell dumpsys window | grep mCurrentFocus")
    print(f"\nModel:      {model}")
    print(f"Android:    {android}")
    print(f"Resolution: {resolution}")
    print(f"Density:    {density}")
    print(f"Battery:    {battery.strip()}")
    print(f"Focus:      {focus.strip()}")


def unlock(pin=None):
    run_with_root_fallback("input keyevent 26")  # wake
    time.sleep(0.5)
    run_with_root_fallback("input keyevent 82")  # unlock
    time.sleep(0.5)
    if pin:
        run_with_root_fallback(f"input text {pin}")
        run_with_root_fallback("input keyevent 66")  # ENTER
    print("Screen unlocked")


def ui_dump(output="/tmp/autodroid_ui.xml"):
    remote = "/sdcard/autodroid_ui.xml"
    result = run_with_root_fallback(f"uiautomator dump {remote}")
    run(f"pull {remote} {output}")
    size = Path(output).stat().st_size if Path(output).exists() else 0
    print(f"UI dump: {output} ({size//1024}KB)")
    return output


def find_text_bounds(text, xml_path="/tmp/autodroid_ui.xml"):
    """Find element bounds by text in uiautomator XML dump."""
    if not Path(xml_path).exists():
        ui_dump(xml_path)
    try:
        tree = ET.parse(xml_path)
        for node in tree.iter():
            node_text = node.get("text", "") or node.get("content-desc", "")
            if text.lower() in node_text.lower():
                bounds = node.get("bounds", "")
                match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds)
                if match:
                    x1, y1, x2, y2 = map(int, match.groups())
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    print(f"Found '{node_text}' at bounds {bounds} → center ({cx},{cy})")
                    return cx, cy
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
    print(f"Not found: '{text}'")
    return None, None


def tap_text(text):
    """Smart: dump UI → find text → tap."""
    xml_path = "/tmp/autodroid_ui.xml"
    ui_dump(xml_path)
    x, y = find_text_bounds(text, xml_path)
    if x is not None:
        tap(x, y)
    else:
        print(f"Could not tap '{text}' — element not found in UI tree")


def install_apk(apk_path):
    print(f"Installing: {apk_path}")
    result = run(f"install -r {apk_path}")
    print(result)


def wifi_connect(ip, port="5555"):
    run(f"shell setprop service.adb.tcp.port {port}", capture=False)
    run(f"tcpip {port}", capture=False)
    time.sleep(1)
    result = run(f"connect {ip}:{port}")
    print(result)


def shell_cmd(cmd):
    result = run_with_root_fallback(cmd)
    print(result)


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    dispatch = {
        "status": lambda: status(),
        "screenshot": lambda: screenshot(args[0] if args else "/tmp/autodroid_screen.png"),
        "pull-screen": lambda: screenshot(),
        "unlock": lambda: unlock(args[0] if args else None),
        "ui-dump": lambda: ui_dump(args[0] if args else "/tmp/autodroid_ui.xml"),
    }

    if cmd in dispatch:
        dispatch[cmd]()
    elif cmd == "tap":
        if len(args) < 2:
            sys.exit("Usage: autodroid.py tap X Y")
        tap(int(args[0]), int(args[1]))
    elif cmd == "swipe":
        if len(args) < 4:
            sys.exit("Usage: autodroid.py swipe x1 y1 x2 y2 [duration_ms]")
        swipe(int(args[0]), int(args[1]), int(args[2]), int(args[3]),
              int(args[4]) if len(args) > 4 else 300)
    elif cmd == "type":
        if not args:
            sys.exit("Usage: autodroid.py type 'text'")
        type_text(args[0])
    elif cmd == "key":
        if not args:
            sys.exit(f"Usage: autodroid.py key KEY\nKeys: {list(KEYCODES.keys())}")
        press_key(args[0])
    elif cmd == "launch":
        if not args:
            sys.exit("Usage: autodroid.py launch com.package.name")
        launch_app(args[0])
    elif cmd == "find-text":
        if not args:
            sys.exit("Usage: autodroid.py find-text 'text' [xml_file]")
        find_text_bounds(args[0], args[1] if len(args) > 1 else "/tmp/autodroid_ui.xml")
    elif cmd == "tap-text":
        if not args:
            sys.exit("Usage: autodroid.py tap-text 'text'")
        tap_text(args[0])
    elif cmd == "install":
        if not args:
            sys.exit("Usage: autodroid.py install path/to.apk")
        install_apk(args[0])
    elif cmd == "wifi-connect":
        if not args:
            sys.exit("Usage: autodroid.py wifi-connect <ip> [port]")
        wifi_connect(args[0], args[1] if len(args) > 1 else "5555")
    elif cmd == "shell":
        if not args:
            sys.exit("Usage: autodroid.py shell 'command'")
        shell_cmd(" ".join(args))
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
