#!/usr/bin/env python3
"""
autodroid-device-agent v1.0 — Full Android device control via ADB.

Commands:
  # Device info
  info [--device]                    Full device info JSON
  battery [--device]                 Battery level + status
  apps [--installed|--system] [--device]  List packages

  # Screen
  screenshot [--out PATH] [--device]
  screenrecord [--duration 10] [--out PATH] [--device]
  brightness [--level 0-255] [--auto] [--device]
  rotation [--mode 0|1|2|3|auto] [--device]

  # Power
  lock [--device]                    Lock screen (power key)
  unlock [--pin PIN] [--device]      Wake + swipe/PIN unlock
  reboot [--device]                  Reboot (requires root)
  wake [--device]                    Wake screen

  # Connectivity
  wifi [--on|--off] [--device]       Toggle WiFi
  wifi-connect --ssid S --password P [--device]
  mobile-data [--on|--off] [--device]
  airplane [--on|--off] [--device]
  bluetooth [--on|--off] [--device]
  proxy [--host H --port P] [--clear] [--device]

  # Audio/Camera/Flash
  volume [--level 0-15] [--stream ringtone|music|alarm] [--device]
  flashlight [--on|--off] [--device]
  photo [--out PATH] [--device]      Take photo via camera intent
  video [--duration 5] [--out PATH] [--device]  Record video

  # Communication
  call --number PHONE [--device]     Make a phone call
  sms --to PHONE --text MSG [--device]  Send SMS
  sms-read [--count 10] [--device]   Read SMS inbox
  contacts [--query NAME] [--device] List/search contacts

  # Files
  push --src PATH --dst PATH [--device]    Push file to device
  pull --src PATH --dst PATH [--device]    Pull file from device
  ls [--path /sdcard/] [--device]          List files
  rm --path PATH [--device]               Delete file
  mkdir --path PATH [--device]            Create directory

  # Apps
  install --apk PATH [--device]      Install APK
  uninstall --package PKG [--device]
  launch --package PKG [--device]    Launch app
  stop --package PKG [--device]      Force stop app
  clear-data --package PKG [--device] Clear app data
  permissions --package PKG [--device] List app permissions

  # Input
  tap --x X --y Y [--device]
  swipe --x1 X --y1 Y --x2 X2 --y2 Y2 [--duration 300] [--device]
  key --code CODE [--device]         Send keyevent
  text --value TEXT [--device]       Type text
  clipboard --text TEXT [--device]   Set clipboard

  # Notifications
  notifications [--device]           Read notification panel

  # System
  gps [--on|--off] [--device]        Toggle location
  font-scale [--scale 1.0] [--device]
  timezone [--tz Asia/Jakarta] [--device]
  date-time [--dt "2026-01-01 12:00:00"] [--device]

  # Server
  server [--port 8772]               FastAPI server
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

DOWNLOADS = Path.home() / ".openclaw/workspace/downloads"
DOWNLOADS.mkdir(parents=True, exist_ok=True)


# ─── Core ADB ──────────────────────────────────────────────────────────────────

def adb(cmd, device=None, timeout=15, shell=True):
    prefix = ["adb"] + (["-s", device] if device else [])
    if shell:
        args = prefix + ["shell"] + (cmd if isinstance(cmd, list) else cmd.split())
    else:
        args = prefix + (cmd if isinstance(cmd, list) else cmd.split())
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return 1, "", "timeout"
    except Exception as e:
        return 1, "", str(e)


def sh(cmd, device=None, timeout=15):
    """Run adb shell command, return stdout."""
    _, out, _ = adb(cmd, device=device, timeout=timeout)
    return out


def list_devices():
    r = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    devs = []
    for line in r.stdout.strip().splitlines()[1:]:
        if "\tdevice" in line:
            serial = line.split("\t")[0].strip()
            model   = sh("getprop ro.product.model", device=serial)
            android = sh("getprop ro.build.version.release", device=serial)
            devs.append({"serial": serial, "model": model, "android": android})
    return devs


def get_device(device=None):
    devs = list_devices()
    if device:
        for d in devs:
            if d["serial"] == device:
                return d
        return {"serial": device, "model": "unknown", "android": "unknown"}
    return devs[0] if devs else {"serial": "none", "model": "none", "android": "none"}


def screencap(path=None, device=None):
    path = path or str(DOWNLOADS / "device_screenshot.png")
    prefix = ["adb"] + (["-s", device] if device else [])
    cmd = prefix + ["exec-out", "screencap", "-p"]
    try:
        with open(path, "wb") as f:
            subprocess.run(cmd, stdout=f, timeout=10, check=True)
        return path
    except Exception:
        return None


def ok(data: dict):
    print(json.dumps({"ok": True, **data}, indent=2, ensure_ascii=False))


def err(msg, **data):
    print(json.dumps({"ok": False, "error": msg, **data}, indent=2, ensure_ascii=False))


# ─── Device Info ──────────────────────────────────────────────────────────────

def cmd_info(device=None):
    props = {
        "model":        sh("getprop ro.product.model", device=device),
        "brand":        sh("getprop ro.product.brand", device=device),
        "manufacturer": sh("getprop ro.product.manufacturer", device=device),
        "android":      sh("getprop ro.build.version.release", device=device),
        "sdk":          sh("getprop ro.build.version.sdk", device=device),
        "serial":       sh("getprop ro.serialno", device=device),
        "imei":         sh("service call iphonesubinfo 1 | awk -F\"'\" 'NR>1{print $2}' | tr -d '\\n. '", device=device),
        "resolution":   sh("wm size", device=device).replace("Physical size: ", ""),
        "density":      sh("wm density", device=device).replace("Physical density: ", ""),
        "cpu":          sh("getprop ro.product.cpu.abi", device=device),
        "ram_mb":       sh("cat /proc/meminfo | grep MemTotal | awk '{print $2}'", device=device),
        "storage":      sh("df /data | tail -1", device=device),
        "ip_wlan":      sh("ip addr show wlan0 | grep 'inet ' | awk '{print $2}'", device=device),
        "ip_mobile":    sh("ip addr show rmnet0 | grep 'inet ' | awk '{print $2}'", device=device),
        "timezone":     sh("getprop persist.sys.timezone", device=device),
        "locale":       sh("getprop persist.sys.locale", device=device),
        "uptime":       sh("uptime", device=device),
    }
    dev = get_device(device)
    ok({"device": dev["serial"], "props": props})


def cmd_battery(device=None):
    raw = sh("dumpsys battery", device=device)
    result = {}
    for line in raw.splitlines():
        line = line.strip()
        if ": " in line:
            k, v = line.split(": ", 1)
            result[k.strip()] = v.strip()
    dev = get_device(device)
    ok({"device": dev["serial"], "battery": result})


def cmd_apps(installed=True, system=False, device=None):
    flag = "-3" if installed and not system else ("-s" if system else "")
    raw = sh(f"pm list packages {flag}", device=device)
    packages = [l.replace("package:", "").strip() for l in raw.splitlines() if l.startswith("package:")]
    dev = get_device(device)
    ok({"device": dev["serial"], "packages": packages, "count": len(packages)})


# ─── Screen ───────────────────────────────────────────────────────────────────

def cmd_screenshot(out=None, device=None):
    path = screencap(out, device=device)
    dev = get_device(device)
    ok({"device": dev["serial"], "screenshot_path": path})


def cmd_screenrecord(duration=10, out=None, device=None):
    remote = "/sdcard/_record.mp4"
    local  = out or str(DOWNLOADS / "device_screenrecord.mp4")
    sh(f"screenrecord --time-limit {duration} {remote}", device=device, timeout=duration+10)
    rc, _, _ = adb(f"pull {remote} {local}", device=device, shell=False)
    sh(f"rm {remote}", device=device)
    dev = get_device(device)
    ok({"device": dev["serial"], "video_path": local, "duration": duration, "success": rc == 0})


def cmd_brightness(level=None, auto=False, device=None):
    dev = get_device(device)
    if auto:
        sh("settings put system screen_brightness_mode 1", device=device)
        ok({"device": dev["serial"], "brightness": "auto"})
    elif level is not None:
        level = max(0, min(255, int(level)))
        sh("settings put system screen_brightness_mode 0", device=device)
        sh(f"settings put system screen_brightness {level}", device=device)
        ok({"device": dev["serial"], "brightness": level})
    else:
        val = sh("settings get system screen_brightness", device=device)
        mode = sh("settings get system screen_brightness_mode", device=device)
        ok({"device": dev["serial"], "brightness": val, "auto": mode == "1"})


def cmd_rotation(mode=None, device=None):
    dev = get_device(device)
    if mode == "auto":
        sh("settings put system accelerometer_rotation 1", device=device)
        ok({"device": dev["serial"], "rotation": "auto"})
    elif mode is not None:
        sh("settings put system accelerometer_rotation 0", device=device)
        sh(f"settings put system user_rotation {mode}", device=device)
        ok({"device": dev["serial"], "rotation": mode})
    else:
        val = sh("settings get system user_rotation", device=device)
        auto = sh("settings get system accelerometer_rotation", device=device)
        ok({"device": dev["serial"], "rotation": val, "auto": auto == "1"})


# ─── Power ────────────────────────────────────────────────────────────────────

def cmd_lock(device=None):
    sh("input keyevent 26", device=device)  # KEYCODE_POWER
    dev = get_device(device)
    ok({"device": dev["serial"], "locked": True})


def cmd_wake(device=None):
    sh("input keyevent 224", device=device)  # KEYCODE_WAKEUP
    time.sleep(0.3)
    sh("input swipe 360 900 360 300", device=device)
    dev = get_device(device)
    ok({"device": dev["serial"], "awake": True})


def cmd_unlock(pin=None, device=None):
    # Wake
    sh("input keyevent 224", device=device)
    time.sleep(0.5)
    # Swipe to unlock
    sh("input swipe 360 900 360 300", device=device)
    time.sleep(0.5)
    dev = get_device(device)
    if pin:
        sh(f"input text {pin}", device=device)
        sh("input keyevent 66", device=device)
        time.sleep(0.5)
    shot = screencap(device=device)
    ok({"device": dev["serial"], "unlocked": True, "pin_used": bool(pin), "screenshot_path": shot})


def cmd_reboot(device=None):
    dev = get_device(device)
    sh("reboot", device=device)
    ok({"device": dev["serial"], "rebooting": True})


# ─── Connectivity ─────────────────────────────────────────────────────────────

def cmd_wifi(on=None, device=None):
    dev = get_device(device)
    if on is True:
        sh("svc wifi enable", device=device)
        time.sleep(2)
        ok({"device": dev["serial"], "wifi": "enabled"})
    elif on is False:
        sh("svc wifi disable", device=device)
        ok({"device": dev["serial"], "wifi": "disabled"})
    else:
        state = sh("dumpsys wifi | grep 'Wi-Fi is'", device=device)
        ok({"device": dev["serial"], "wifi_state": state})


def cmd_wifi_connect(ssid, password=None, device=None):
    dev = get_device(device)
    # Android 10+ cmd wifi
    cmd = f"cmd wifi connect-network \"{ssid}\" wpa2 \"{password}\"" if password else f"cmd wifi connect-network \"{ssid}\" open"
    out = sh(cmd, device=device)
    time.sleep(3)
    ip = sh("ip addr show wlan0 | grep 'inet ' | awk '{print $2}'", device=device)
    ok({"device": dev["serial"], "ssid": ssid, "connected": bool(ip), "ip": ip, "adb_out": out})


def cmd_mobile_data(on=None, device=None):
    dev = get_device(device)
    if on is True:
        sh("svc data enable", device=device)
        ok({"device": dev["serial"], "mobile_data": "enabled"})
    elif on is False:
        sh("svc data disable", device=device)
        ok({"device": dev["serial"], "mobile_data": "disabled"})
    else:
        state = sh("settings get global mobile_data", device=device)
        ok({"device": dev["serial"], "mobile_data": "enabled" if state == "1" else "disabled"})


def cmd_airplane(on=None, device=None):
    dev = get_device(device)
    if on is True:
        sh("settings put global airplane_mode_on 1", device=device)
        sh("am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true", device=device)
        ok({"device": dev["serial"], "airplane_mode": "on"})
    elif on is False:
        sh("settings put global airplane_mode_on 0", device=device)
        sh("am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false", device=device)
        ok({"device": dev["serial"], "airplane_mode": "off"})
    else:
        state = sh("settings get global airplane_mode_on", device=device)
        ok({"device": dev["serial"], "airplane_mode": "on" if state == "1" else "off"})


def cmd_bluetooth(on=None, device=None):
    dev = get_device(device)
    if on is True:
        sh("svc bluetooth enable", device=device)
        ok({"device": dev["serial"], "bluetooth": "enabled"})
    elif on is False:
        sh("svc bluetooth disable", device=device)
        ok({"device": dev["serial"], "bluetooth": "disabled"})
    else:
        state = sh("settings get global bluetooth_on", device=device)
        ok({"device": dev["serial"], "bluetooth": "enabled" if state == "1" else "disabled"})


def cmd_proxy(host=None, port=None, clear=False, device=None):
    dev = get_device(device)
    if clear:
        sh("settings put global http_proxy :0", device=device)
        ok({"device": dev["serial"], "proxy": "cleared"})
    elif host and port:
        sh(f"settings put global http_proxy {host}:{port}", device=device)
        ok({"device": dev["serial"], "proxy": f"{host}:{port}", "set": True})
    else:
        val = sh("settings get global http_proxy", device=device)
        ok({"device": dev["serial"], "proxy": val})


# ─── Audio / Camera / Flash ───────────────────────────────────────────────────

VOLUME_KEYCODES = {
    "up":   "24",   # KEYCODE_VOLUME_UP
    "down": "25",   # KEYCODE_VOLUME_DOWN
    "mute": "164",  # KEYCODE_VOLUME_MUTE
}

STREAM_IDS = {"ringtone": 2, "music": 3, "alarm": 4, "notification": 5}

def cmd_volume(level=None, stream="music", direction=None, device=None):
    dev = get_device(device)
    if direction in ("up", "down", "mute"):
        sh(f"input keyevent {VOLUME_KEYCODES[direction]}", device=device)
        ok({"device": dev["serial"], "volume_action": direction})
    elif level is not None:
        stream_id = STREAM_IDS.get(stream, 3)
        sh(f"media volume --stream {stream_id} --set {level}", device=device)
        ok({"device": dev["serial"], "stream": stream, "level": level})
    else:
        raw = sh("media volume --get --stream 3", device=device)
        ok({"device": dev["serial"], "volume_info": raw})


def cmd_flashlight(on=True, device=None):
    dev = get_device(device)
    # Android 13+ settings flashlight
    val = "1" if on else "0"
    out = sh(f"cmd flashlight {val}", device=device)
    if not out or "Error" in out:
        # Fallback: camera2 torch intent
        action = "TURN_ON" if on else "TURN_OFF"
        sh(f"am start -n com.android.settings/.MainSettings", device=device)
    ok({"device": dev["serial"], "flashlight": "on" if on else "off", "note": out or "sent"})


def cmd_photo(out=None, device=None):
    remote = "/sdcard/DCIM/_autodroid_photo.jpg"
    local  = out or str(DOWNLOADS / "device_photo.jpg")
    sh(f"am start -a android.media.action.IMAGE_CAPTURE --es output file://{remote}", device=device)
    time.sleep(3)
    # Try pull
    rc, _, _ = adb(f"pull {remote} {local}", device=device, shell=False)
    dev = get_device(device)
    if rc == 0:
        ok({"device": dev["serial"], "photo_path": local})
    else:
        shot = screencap(device=device)
        ok({"device": dev["serial"], "photo_path": None, "note": "camera opened, manual capture needed", "screenshot_path": shot})


def cmd_video(duration=5, out=None, device=None):
    remote = "/sdcard/DCIM/_autodroid_video.mp4"
    local  = out or str(DOWNLOADS / "device_video.mp4")
    sh(f"am start -a android.media.action.VIDEO_CAPTURE", device=device)
    time.sleep(duration + 3)
    rc, _, _ = adb(f"pull {remote} {local}", device=device, shell=False)
    dev = get_device(device)
    ok({"device": dev["serial"], "video_path": local if rc == 0 else None, "duration": duration})


# ─── Communication ────────────────────────────────────────────────────────────

def cmd_call(number, device=None):
    dev = get_device(device)
    sh(f"am start -a android.intent.action.CALL -d tel:{number}", device=device)
    time.sleep(2)
    shot = screencap(device=device)
    ok({"device": dev["serial"], "calling": number, "screenshot_path": shot})


def cmd_sms_send(to, text, device=None):
    dev = get_device(device)
    # URI-encode text
    encoded = text.replace(" ", "%20").replace("&", "%26")
    sh(f"am start -a android.intent.action.SENDTO -d sms:{to} --es sms_body \"{text}\" --ez exit_on_sent true", device=device)
    time.sleep(2)
    shot = screencap(device=device)
    ok({"device": dev["serial"], "sms_to": to, "text": text, "screenshot_path": shot,
        "note": "SMS app opened. Tap Send if not auto-sent."})


def cmd_sms_read(count=10, device=None):
    dev = get_device(device)
    raw = sh(f"content query --uri content://sms/inbox --projection address,body,date --sort 'date DESC' --result-count {count}", device=device)
    messages = []
    current = {}
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("Row:"):
            if current:
                messages.append(current)
            current = {}
        for field in ("address", "body", "date"):
            if f"{field}=" in line:
                val = line.split(f"{field}=", 1)[1].split(",")[0].strip()
                current[field] = val
    if current:
        messages.append(current)
    ok({"device": dev["serial"], "messages": messages, "count": len(messages)})


def cmd_contacts(query=None, device=None):
    dev = get_device(device)
    proj = "display_name,has_phone_number"
    uri  = "content://contacts/people"
    raw  = sh(f"content query --uri {uri} --projection {proj}" + (f" --where \"display_name LIKE '%{query}%'\"" if query else ""), device=device)
    contacts = []
    for line in raw.splitlines():
        if "display_name=" in line:
            name = line.split("display_name=")[1].split(",")[0].strip()
            contacts.append(name)
    ok({"device": dev["serial"], "contacts": contacts, "count": len(contacts), "query": query})


# ─── Files ────────────────────────────────────────────────────────────────────

def cmd_push(src, dst, device=None):
    dev = get_device(device)
    rc, out, err_msg = adb(f"push {src} {dst}", device=device, shell=False)
    ok({"device": dev["serial"], "src": src, "dst": dst, "success": rc == 0, "output": out})


def cmd_pull(src, dst, device=None):
    dev = get_device(device)
    rc, out, err_msg = adb(f"pull {src} {dst}", device=device, shell=False)
    ok({"device": dev["serial"], "src": src, "dst": dst, "success": rc == 0, "local_path": dst if rc == 0 else None})


def cmd_ls(path="/sdcard/", device=None):
    dev = get_device(device)
    raw = sh(f"ls -la {path}", device=device)
    files = [l.strip() for l in raw.splitlines() if l.strip()]
    ok({"device": dev["serial"], "path": path, "files": files, "count": len(files)})


def cmd_rm(path, device=None):
    dev = get_device(device)
    rc, out, _ = adb(f"rm -rf {path}", device=device)
    ok({"device": dev["serial"], "path": path, "deleted": rc == 0})


def cmd_mkdir(path, device=None):
    dev = get_device(device)
    rc, _, _ = adb(f"mkdir -p {path}", device=device)
    ok({"device": dev["serial"], "path": path, "created": rc == 0})


# ─── Apps ─────────────────────────────────────────────────────────────────────

def cmd_install(apk, device=None):
    dev = get_device(device)
    rc, out, err_msg = adb(f"install -r {apk}", device=device, shell=False, timeout=120)
    ok({"device": dev["serial"], "apk": apk, "installed": "Success" in out, "output": out or err_msg})


def cmd_uninstall(package, device=None):
    dev = get_device(device)
    rc, out, _ = adb(f"uninstall {package}", device=device, shell=False)
    ok({"device": dev["serial"], "package": package, "uninstalled": "Success" in out, "output": out})


def cmd_launch(package, device=None):
    dev = get_device(device)
    sh(f"monkey -p {package} -c android.intent.category.LAUNCHER 1", device=device)
    time.sleep(1.5)
    shot = screencap(device=device)
    ok({"device": dev["serial"], "package": package, "launched": True, "screenshot_path": shot})


def cmd_stop(package, device=None):
    dev = get_device(device)
    sh(f"am force-stop {package}", device=device)
    ok({"device": dev["serial"], "package": package, "stopped": True})


def cmd_clear_data(package, device=None):
    dev = get_device(device)
    out = sh(f"pm clear {package}", device=device)
    ok({"device": dev["serial"], "package": package, "cleared": "Success" in out, "output": out})


def cmd_permissions(package, device=None):
    dev = get_device(device)
    raw = sh(f"dumpsys package {package} | grep 'permission'", device=device)
    perms = [l.strip() for l in raw.splitlines() if "android.permission" in l]
    ok({"device": dev["serial"], "package": package, "permissions": perms})


# ─── Input ────────────────────────────────────────────────────────────────────

def cmd_tap(x, y, device=None):
    dev = get_device(device)
    sh(f"input tap {x} {y}", device=device)
    ok({"device": dev["serial"], "tapped": [x, y]})


def cmd_swipe(x1, y1, x2, y2, duration=300, device=None):
    dev = get_device(device)
    sh(f"input swipe {x1} {y1} {x2} {y2} {duration}", device=device)
    ok({"device": dev["serial"], "swiped": {"from": [x1, y1], "to": [x2, y2], "duration_ms": duration}})


def cmd_key(code, device=None):
    dev = get_device(device)
    sh(f"input keyevent {code}", device=device)
    ok({"device": dev["serial"], "keyevent": code})


def cmd_text(value, device=None):
    dev = get_device(device)
    escaped = value.replace(" ", "%s").replace("'", "\\'")
    sh(f"input text {escaped}", device=device)
    ok({"device": dev["serial"], "typed": value})


def cmd_clipboard(text, device=None):
    dev = get_device(device)
    # Android 10+ restricts clipboard; use content provider trick
    sh(f"am broadcast -a clipper.set -e text \"{text}\"", device=device)
    ok({"device": dev["serial"], "clipboard": text, "note": "requires Clipper app or ADB root"})


# ─── Notifications ────────────────────────────────────────────────────────────

def cmd_notifications(device=None):
    dev = get_device(device)
    raw = sh("dumpsys notification | grep -A3 'NotificationRecord'", device=device)
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    ok({"device": dev["serial"], "notifications_raw": lines[:50]})


# ─── System ───────────────────────────────────────────────────────────────────

def cmd_gps(on=None, device=None):
    dev = get_device(device)
    if on is True:
        sh("settings put secure location_mode 3", device=device)  # HIGH_ACCURACY
        ok({"device": dev["serial"], "gps": "on"})
    elif on is False:
        sh("settings put secure location_mode 0", device=device)
        ok({"device": dev["serial"], "gps": "off"})
    else:
        state = sh("settings get secure location_mode", device=device)
        ok({"device": dev["serial"], "gps": "on" if state != "0" else "off", "mode": state})


def cmd_font_scale(scale=1.0, device=None):
    dev = get_device(device)
    sh(f"settings put system font_scale {scale}", device=device)
    ok({"device": dev["serial"], "font_scale": scale})


def cmd_timezone(tz, device=None):
    dev = get_device(device)
    sh(f"setprop persist.sys.timezone {tz}", device=device)
    ok({"device": dev["serial"], "timezone": tz})


def cmd_datetime(dt, device=None):
    """dt format: 'MMDDHHMMYYYY.SS'"""
    dev = get_device(device)
    sh(f"date {dt}", device=device)
    ok({"device": dev["serial"], "datetime_set": dt})


# ─── FastAPI Server ────────────────────────────────────────────────────────────

def cmd_server(port=8772):
    try:
        from fastapi import FastAPI, Query
        from pydantic import BaseModel
        import uvicorn
    except ImportError:
        print("pip install fastapi uvicorn", file=sys.stderr)
        sys.exit(1)

    app = FastAPI(title="autodroid-device-agent", version="1.0",
                  description="Full Android device control via ADB")

    class ProxyReq(BaseModel):
        host: str = None
        port: int = None
        clear: bool = False
        device: str = None

    class SmsReq(BaseModel):
        to: str
        text: str
        device: str = None

    class PushReq(BaseModel):
        src: str
        dst: str
        device: str = None

    class PullReq(BaseModel):
        src: str
        dst: str
        device: str = None

    class WifiConnectReq(BaseModel):
        ssid: str
        password: str = None
        device: str = None

    class TextReq(BaseModel):
        value: str
        device: str = None

    def cap(fn, *a, **kw):
        """Capture JSON output from cmd_* function."""
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            fn(*a, **kw)
        try:
            return json.loads(buf.getvalue())
        except Exception:
            return {"ok": False, "raw": buf.getvalue()}

    @app.get("/health")
    def health(): return {"status": "ok"}

    @app.get("/devices")
    def devices(): return {"ok": True, "devices": list_devices()}

    @app.get("/info")
    def info(device: str = None): return cap(cmd_info, device=device)

    @app.get("/battery")
    def battery(device: str = None): return cap(cmd_battery, device=device)

    @app.get("/apps")
    def apps(device: str = None, system: bool = False): return cap(cmd_apps, system=system, device=device)

    @app.get("/screenshot")
    def screenshot(device: str = None): return cap(cmd_screenshot, device=device)

    @app.get("/screenrecord")
    def screenrecord(duration: int = 10, device: str = None): return cap(cmd_screenrecord, duration=duration, device=device)

    @app.post("/brightness")
    def brightness(level: int = None, auto: bool = False, device: str = None): return cap(cmd_brightness, level=level, auto=auto, device=device)

    @app.post("/lock")
    def lock(device: str = None): return cap(cmd_lock, device=device)

    @app.post("/wake")
    def wake(device: str = None): return cap(cmd_wake, device=device)

    @app.post("/unlock")
    def unlock(pin: str = None, device: str = None): return cap(cmd_unlock, pin=pin, device=device)

    @app.post("/wifi")
    def wifi(on: bool = None, device: str = None): return cap(cmd_wifi, on=on, device=device)

    @app.post("/wifi-connect")
    def wifi_connect(req: WifiConnectReq): return cap(cmd_wifi_connect, req.ssid, req.password, device=req.device)

    @app.post("/mobile-data")
    def mobile_data(on: bool = None, device: str = None): return cap(cmd_mobile_data, on=on, device=device)

    @app.post("/airplane")
    def airplane(on: bool = None, device: str = None): return cap(cmd_airplane, on=on, device=device)

    @app.post("/bluetooth")
    def bluetooth(on: bool = None, device: str = None): return cap(cmd_bluetooth, on=on, device=device)

    @app.post("/proxy")
    def proxy(req: ProxyReq): return cap(cmd_proxy, req.host, req.port, req.clear, device=req.device)

    @app.post("/volume")
    def volume(level: int = None, stream: str = "music", direction: str = None, device: str = None):
        return cap(cmd_volume, level=level, stream=stream, direction=direction, device=device)

    @app.post("/flashlight")
    def flashlight(on: bool = True, device: str = None): return cap(cmd_flashlight, on=on, device=device)

    @app.post("/photo")
    def photo(device: str = None): return cap(cmd_photo, device=device)

    @app.post("/call")
    def call(number: str, device: str = None): return cap(cmd_call, number, device=device)

    @app.post("/sms")
    def sms(req: SmsReq): return cap(cmd_sms_send, req.to, req.text, device=req.device)

    @app.get("/sms-read")
    def sms_read(count: int = 10, device: str = None): return cap(cmd_sms_read, count=count, device=device)

    @app.get("/contacts")
    def contacts(query: str = None, device: str = None): return cap(cmd_contacts, query=query, device=device)

    @app.post("/push")
    def push(req: PushReq): return cap(cmd_push, req.src, req.dst, device=req.device)

    @app.post("/pull")
    def pull(req: PullReq): return cap(cmd_pull, req.src, req.dst, device=req.device)

    @app.get("/ls")
    def ls(path: str = "/sdcard/", device: str = None): return cap(cmd_ls, path=path, device=device)

    @app.post("/launch")
    def launch(package: str, device: str = None): return cap(cmd_launch, package, device=device)

    @app.post("/stop")
    def stop(package: str, device: str = None): return cap(cmd_stop, package, device=device)

    @app.post("/tap")
    def tap(x: int, y: int, device: str = None): return cap(cmd_tap, x, y, device=device)

    @app.post("/swipe")
    def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300, device: str = None):
        return cap(cmd_swipe, x1, y1, x2, y2, duration=duration, device=device)

    @app.post("/key")
    def key(code: str, device: str = None): return cap(cmd_key, code, device=device)

    @app.post("/text")
    def text(req: TextReq): return cap(cmd_text, req.value, device=req.device)

    @app.post("/gps")
    def gps(on: bool = None, device: str = None): return cap(cmd_gps, on=on, device=device)

    @app.get("/notifications")
    def notifications(device: str = None): return cap(cmd_notifications, device=device)

    print(f"[device-agent] Running on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[device-agent] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="autodroid-device-agent v1.0 — Full Android device control")
    p.add_argument("--device", default=None, help="ADB device serial")
    sub = p.add_subparsers(dest="cmd", required=True)

    # Info
    sub.add_parser("info")
    sub.add_parser("battery")
    sp = sub.add_parser("apps")
    sp.add_argument("--system", action="store_true")

    # Screen
    sp = sub.add_parser("screenshot"); sp.add_argument("--out")
    sp = sub.add_parser("screenrecord"); sp.add_argument("--duration", type=int, default=10); sp.add_argument("--out")
    sp = sub.add_parser("brightness"); sp.add_argument("--level", type=int); sp.add_argument("--auto", action="store_true")
    sp = sub.add_parser("rotation"); sp.add_argument("--mode")

    # Power
    sub.add_parser("lock")
    sub.add_parser("wake")
    sp = sub.add_parser("unlock"); sp.add_argument("--pin")
    sub.add_parser("reboot")

    # Connectivity
    sp = sub.add_parser("wifi"); g = sp.add_mutually_exclusive_group(); g.add_argument("--on", dest="on", action="store_true"); g.add_argument("--off", dest="on", action="store_false"); sp.set_defaults(on=None)
    sp = sub.add_parser("wifi-connect"); sp.add_argument("--ssid", required=True); sp.add_argument("--password")
    sp = sub.add_parser("mobile-data"); g = sp.add_mutually_exclusive_group(); g.add_argument("--on", dest="on", action="store_true"); g.add_argument("--off", dest="on", action="store_false"); sp.set_defaults(on=None)
    sp = sub.add_parser("airplane"); g = sp.add_mutually_exclusive_group(); g.add_argument("--on", dest="on", action="store_true"); g.add_argument("--off", dest="on", action="store_false"); sp.set_defaults(on=None)
    sp = sub.add_parser("bluetooth"); g = sp.add_mutually_exclusive_group(); g.add_argument("--on", dest="on", action="store_true"); g.add_argument("--off", dest="on", action="store_false"); sp.set_defaults(on=None)
    sp = sub.add_parser("proxy"); sp.add_argument("--host"); sp.add_argument("--port", type=int); sp.add_argument("--clear", action="store_true")

    # Audio/Camera
    sp = sub.add_parser("volume"); sp.add_argument("--level", type=int); sp.add_argument("--stream", default="music"); sp.add_argument("--direction", choices=["up","down","mute"])
    sp = sub.add_parser("flashlight"); g = sp.add_mutually_exclusive_group(); g.add_argument("--on", dest="on", action="store_true", default=True); g.add_argument("--off", dest="on", action="store_false")
    sp = sub.add_parser("photo"); sp.add_argument("--out")
    sp = sub.add_parser("video"); sp.add_argument("--duration", type=int, default=5); sp.add_argument("--out")

    # Communication
    sp = sub.add_parser("call"); sp.add_argument("--number", required=True)
    sp = sub.add_parser("sms"); sp.add_argument("--to", required=True); sp.add_argument("--text", required=True)
    sp = sub.add_parser("sms-read"); sp.add_argument("--count", type=int, default=10)
    sp = sub.add_parser("contacts"); sp.add_argument("--query")

    # Files
    sp = sub.add_parser("push"); sp.add_argument("--src", required=True); sp.add_argument("--dst", required=True)
    sp = sub.add_parser("pull"); sp.add_argument("--src", required=True); sp.add_argument("--dst", required=True)
    sp = sub.add_parser("ls"); sp.add_argument("--path", default="/sdcard/")
    sp = sub.add_parser("rm"); sp.add_argument("--path", required=True)
    sp = sub.add_parser("mkdir"); sp.add_argument("--path", required=True)

    # Apps
    sp = sub.add_parser("install"); sp.add_argument("--apk", required=True)
    sp = sub.add_parser("uninstall"); sp.add_argument("--package", required=True)
    sp = sub.add_parser("launch"); sp.add_argument("--package", required=True)
    sp = sub.add_parser("stop"); sp.add_argument("--package", required=True)
    sp = sub.add_parser("clear-data"); sp.add_argument("--package", required=True)
    sp = sub.add_parser("permissions"); sp.add_argument("--package", required=True)

    # Input
    sp = sub.add_parser("tap"); sp.add_argument("--x", type=int, required=True); sp.add_argument("--y", type=int, required=True)
    sp = sub.add_parser("swipe"); sp.add_argument("--x1",type=int,required=True); sp.add_argument("--y1",type=int,required=True); sp.add_argument("--x2",type=int,required=True); sp.add_argument("--y2",type=int,required=True); sp.add_argument("--duration",type=int,default=300)
    sp = sub.add_parser("key"); sp.add_argument("--code", required=True)
    sp = sub.add_parser("text"); sp.add_argument("--value", required=True)
    sp = sub.add_parser("clipboard"); sp.add_argument("--text", required=True)

    # System
    sub.add_parser("notifications")
    sp = sub.add_parser("gps"); g = sp.add_mutually_exclusive_group(); g.add_argument("--on", dest="on", action="store_true"); g.add_argument("--off", dest="on", action="store_false"); sp.set_defaults(on=None)
    sp = sub.add_parser("font-scale"); sp.add_argument("--scale", type=float, default=1.0)
    sp = sub.add_parser("timezone"); sp.add_argument("--tz", required=True)

    sp = sub.add_parser("server"); sp.add_argument("--port", type=int, default=8772)

    args = p.parse_args()
    d = getattr(args, "device", None)

    dispatch = {
        "info":        lambda: cmd_info(device=d),
        "battery":     lambda: cmd_battery(device=d),
        "apps":        lambda: cmd_apps(system=args.system, device=d),
        "screenshot":  lambda: cmd_screenshot(out=getattr(args,"out",None), device=d),
        "screenrecord":lambda: cmd_screenrecord(duration=args.duration, out=getattr(args,"out",None), device=d),
        "brightness":  lambda: cmd_brightness(level=getattr(args,"level",None), auto=getattr(args,"auto",False), device=d),
        "rotation":    lambda: cmd_rotation(mode=getattr(args,"mode",None), device=d),
        "lock":        lambda: cmd_lock(device=d),
        "wake":        lambda: cmd_wake(device=d),
        "unlock":      lambda: cmd_unlock(pin=getattr(args,"pin",None), device=d),
        "reboot":      lambda: cmd_reboot(device=d),
        "wifi":        lambda: cmd_wifi(on=getattr(args,"on",None), device=d),
        "wifi-connect":lambda: cmd_wifi_connect(args.ssid, getattr(args,"password",None), device=d),
        "mobile-data": lambda: cmd_mobile_data(on=getattr(args,"on",None), device=d),
        "airplane":    lambda: cmd_airplane(on=getattr(args,"on",None), device=d),
        "bluetooth":   lambda: cmd_bluetooth(on=getattr(args,"on",None), device=d),
        "proxy":       lambda: cmd_proxy(getattr(args,"host",None), getattr(args,"port",None), getattr(args,"clear",False), device=d),
        "volume":      lambda: cmd_volume(level=getattr(args,"level",None), stream=args.stream, direction=getattr(args,"direction",None), device=d),
        "flashlight":  lambda: cmd_flashlight(on=args.on, device=d),
        "photo":       lambda: cmd_photo(out=getattr(args,"out",None), device=d),
        "video":       lambda: cmd_video(duration=args.duration, out=getattr(args,"out",None), device=d),
        "call":        lambda: cmd_call(args.number, device=d),
        "sms":         lambda: cmd_sms_send(args.to, args.text, device=d),
        "sms-read":    lambda: cmd_sms_read(count=args.count, device=d),
        "contacts":    lambda: cmd_contacts(query=getattr(args,"query",None), device=d),
        "push":        lambda: cmd_push(args.src, args.dst, device=d),
        "pull":        lambda: cmd_pull(args.src, args.dst, device=d),
        "ls":          lambda: cmd_ls(path=args.path, device=d),
        "rm":          lambda: cmd_rm(args.path, device=d),
        "mkdir":       lambda: cmd_mkdir(args.path, device=d),
        "install":     lambda: cmd_install(args.apk, device=d),
        "uninstall":   lambda: cmd_uninstall(args.package, device=d),
        "launch":      lambda: cmd_launch(args.package, device=d),
        "stop":        lambda: cmd_stop(args.package, device=d),
        "clear-data":  lambda: cmd_clear_data(args.package, device=d),
        "permissions": lambda: cmd_permissions(args.package, device=d),
        "tap":         lambda: cmd_tap(args.x, args.y, device=d),
        "swipe":       lambda: cmd_swipe(args.x1, args.y1, args.x2, args.y2, duration=args.duration, device=d),
        "key":         lambda: cmd_key(args.code, device=d),
        "text":        lambda: cmd_text(args.value, device=d),
        "clipboard":   lambda: cmd_clipboard(args.text, device=d),
        "notifications":lambda: cmd_notifications(device=d),
        "gps":         lambda: cmd_gps(on=getattr(args,"on",None), device=d),
        "font-scale":  lambda: cmd_font_scale(scale=args.scale, device=d),
        "timezone":    lambda: cmd_timezone(args.tz, device=d),
        "server":      lambda: cmd_server(port=args.port),
    }

    fn = dispatch.get(args.cmd)
    if fn:
        fn()
    else:
        err(f"Unknown command: {args.cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
