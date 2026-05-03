#!/usr/bin/env python3
"""
autodroid-tiktok-agent v2.0 — Robust TikTok Android automation

ADB-based agent to control TikTok app on Android.
Retries on failure. Returns JSON with ok:true/false always.

Commands:
  status    [--device]           -- check app + device info
  open      [--device]           -- launch TikTok, dismiss popups
  inbox     [--device]           -- open inbox/KotakMasuk tab
  profile   [--device]           -- open profile tab
  screenshot [--device] [--out]  -- capture screen
  login     --username U --password P [--device]
  register  --username U --email E --password P [--phone PHONE] [--device]
  upload    --video PATH [--caption TEXT] [--hashtags LIST] [--device]
  like      [--count N] [--device]
  comment   --text TEXT [--device]
  follow    [--device]
  search    --query TEXT [--device]
  server    [--port 8766]        -- start FastAPI server

Tested: Redmi 2409BRN2CY, Android 14, 720x1640, TikTok (com.ss.android.ugc.trill)
"""

import argparse
import json
import os
import random
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

# ─── AI Interceptor (fail-safe) ───────────────────────────────────────────────
try:
    import sys as _sys
    _sys.path.insert(0, '/mnt/data/berkahkarya/skills/1ai-skills/automation/ai-interceptor/scripts')
    from ai_interceptor import AIInterceptor
    from content_interceptor import ContentInterceptor
    _interceptor = ContentInterceptor()  # TikTok = content posting
    AI_INTERCEPT_ENABLED = True
except Exception:
    AI_INTERCEPT_ENABLED = False
    _interceptor = None

def _ai_intercept(skill_type):
    """Safe decorator: wraps with AI interceptor if available, else passthrough."""
    def decorator(fn):
        if AI_INTERCEPT_ENABLED and _interceptor is not None:
            try:
                return _interceptor.intercept(skill_type=skill_type)(fn)
            except Exception:
                pass
        return fn
    return decorator
# ─────────────────────────────────────────────────────────────────────────────

PACKAGE = "com.ss.android.ugc.trill"
DOWNLOADS = Path("~/.openclaw/workspace/downloads").expanduser()
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

# Verified 720x1640 Redmi 2409BRN2CY bottom nav coordinates
NAV_BERANDA      = (72,  1505)
NAV_TOKO         = (216, 1505)
NAV_POST         = (360, 1505)
NAV_KOTAK_MASUK  = (504, 1505)
NAV_PROFIL       = (648, 1505)

# Popup dismiss labels (Indonesian + English)
DISMISS_LABELS = {
    "Lewati", "Skip", "Tidak", "Nanti", "Lanjutkan",
    "Close", "Tutup", "Allow", "OK", "Oke",
    "Izinkan", "Tidak sekarang", "Lain kali",
    "Got it", "Not now", "No thanks", "Continue",
    "Accept", "Dismiss", "Agree",
}


# ─── Natural Scroll Helpers ──────────────────────────────────────────────────

def natural_swipe(direction="up", device=None, speed=None, distance=None):
    """
    Human-like swipe. Randomizes speed, distance, and start position slightly.
    direction: "up" (scroll forward/next), "down" (scroll back), "left", "right"
    speed: ms duration (default random 300-700)
    distance: px (default random 600-900 for up/down)
    """
    speed = speed or random.randint(300, 700)
    cx = random.randint(330, 390)  # slight x variation (human imprecision)

    if direction == "up":
        dist = distance or random.randint(600, 950)
        y1 = random.randint(900, 1100)
        y2 = y1 - dist
        adb("shell", "input", "swipe", str(cx), str(y1), str(cx), str(y2), str(speed), device=device)
    elif direction == "down":
        dist = distance or random.randint(600, 950)
        y1 = random.randint(300, 500)
        y2 = y1 + dist
        adb("shell", "input", "swipe", str(cx), str(y1), str(cx), str(y2), str(speed), device=device)
    elif direction == "left":
        dist = distance or random.randint(400, 700)
        y = random.randint(700, 900)
        adb("shell", "input", "swipe", "600", str(y), str(600 - dist), str(y), str(speed), device=device)
    elif direction == "right":
        dist = distance or random.randint(400, 700)
        y = random.randint(700, 900)
        adb("shell", "input", "swipe", "120", str(y), str(120 + dist), str(y), str(speed), device=device)

    time.sleep(random.uniform(0.1, 0.3))  # settle pause


def natural_pause(min_s=0.5, max_s=2.5):
    """Random human-like pause."""
    time.sleep(random.uniform(min_s, max_s))


# ─── Low-level ADB ──────────────────────────────────────────────────────────

def adb(*args, device=None, binary=False, check=False):
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += list(args)
    if binary:
        r = subprocess.run(cmd, capture_output=True)
        return r.stdout
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"adb {args[0]} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def tap(x, y, device=None):
    adb("shell", "input", "tap", str(x), str(y), device=device)


def double_tap(x, y, device=None):
    """Double-tap at coordinates (for like gesture)."""
    adb("shell", "input", "tap", str(x), str(y), device=device)
    time.sleep(0.1)
    adb("shell", "input", "tap", str(x), str(y), device=device)


def swipe(x1, y1, x2, y2, duration=300, device=None):
    adb("shell", "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration), device=device)


def keyevent(key, device=None):
    adb("shell", "input", "keyevent", str(key), device=device)


def type_text(text, device=None):
    """Type text via ADB. Handles spaces by replacing with %s."""
    # Escape special characters for shell
    safe = text.replace(" ", "%s").replace("'", "\\'").replace('"', '\\"')
    adb("shell", "input", "text", safe, device=device)


def wake(device=None):
    keyevent(224, device=device)
    time.sleep(0.5)
    swipe(360, 1400, 360, 700, duration=200, device=device)
    time.sleep(0.6)


def screencap(path, device=None):
    wake(device=device)
    data = adb("exec-out", "screencap", "-p", device=device, binary=True)
    Path(path).write_bytes(data)
    return str(path)


# ─── UI Parsing ─────────────────────────────────────────────────────────────

def dump_ui(device=None):
    remote = "/sdcard/tiktok_dump.xml"
    local = "/tmp/tiktok_dump.xml"
    adb("shell", "uiautomator", "dump", remote, device=device)
    adb("pull", remote, local, device=device)
    try:
        root = ET.parse(local).getroot()
        nodes = []
        for n in root.iter():
            text = (n.get("text") or "").strip()
            desc = (n.get("content-desc") or "").strip()
            cls = n.get("class", "").split(".")[-1]
            bounds = n.get("bounds", "")
            hint = (n.get("hint") or "").strip()
            label = text or desc
            if bounds:
                nodes.append({
                    "label": label, "text": text, "desc": desc,
                    "class": cls, "bounds": bounds, "hint": hint,
                })
        return nodes
    except ET.ParseError:
        return []


def bounds_to_center(b):
    try:
        vals = b.replace("][", ",").replace("[", "").replace("]", "").split(",")
        l, t, r, bo = map(int, vals)
        return (l + r) // 2, (t + bo) // 2
    except Exception:
        return None


def find_node(nodes, label=None, cls=None, partial=False, hint=None):
    for n in nodes:
        if label:
            match = (n["label"] == label) if not partial else (label.lower() in n["label"].lower())
            if not match:
                continue
        if cls and cls not in n["class"]:
            continue
        if hint and hint.lower() not in (n.get("hint") or "").lower():
            continue
        return n
    return None


def find_nodes_by_class(nodes, cls):
    return [n for n in nodes if cls in n["class"]]


def tap_node(nodes, label=None, cls=None, partial=False, device=None, hint=None):
    n = find_node(nodes, label=label, cls=cls, partial=partial, hint=hint)
    if n:
        c = bounds_to_center(n["bounds"])
        if c:
            tap(*c, device=device)
            return True
    return False


# ─── Device Helpers ──────────────────────────────────────────────────────────

def get_connected_devices():
    out = adb("devices")
    return [l.split()[0] for l in out.splitlines()[1:] if "\tdevice" in l]


def resolve_device(device=None):
    """Return (serial, error_str). If device is None, auto-pick first connected."""
    devices = get_connected_devices()
    if not devices:
        return None, "No ADB devices connected"
    if device:
        if device in devices:
            return device, None
        return None, f"Device {device!r} not found. Connected: {devices}"
    return devices[0], None


# ─── TikTok Actions ──────────────────────────────────────────────────────────

def dismiss_popups(device=None):
    """Scan UI for known dismiss buttons and tap them."""
    nodes = dump_ui(device=device)
    dismissed = 0
    for n in nodes:
        if n["label"] in DISMISS_LABELS:
            c = bounds_to_center(n["bounds"])
            if c:
                tap(*c, device=device)
                time.sleep(0.5)
                dismissed += 1
    return dismissed


def launch_tiktok(device=None):
    """Force-stop then launch TikTok via monkey."""
    wake(device=device)
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(0.8)
    adb("shell", "monkey", "-p", PACKAGE,
        "-c", "android.intent.category.LAUNCHER", "1", device=device)
    time.sleep(4.0)
    wake(device=device)


def open_tiktok_with_dismiss(device=None):
    """Launch TikTok and dismiss any popups. Return True if app seems ready."""
    launch_tiktok(device=device)
    # Dismiss popups in multiple passes
    for _ in range(3):
        dismissed = dismiss_popups(device=device)
        if dismissed == 0:
            break
        time.sleep(0.5)
    return True


def is_logged_in(device=None):
    """Check if user is logged in by looking at profile tab UI."""
    tap(*NAV_PROFIL, device=device)
    time.sleep(2.0)
    nodes = dump_ui(device=device)
    # If logged in, there should be a username (no "Daftar" / "Masuk" buttons visible)
    # Look for register/login buttons which indicate NOT logged in
    login_indicators = ["Masuk", "Daftar", "Log in", "Sign up", "Register"]
    for n in nodes:
        for ind in login_indicators:
            if ind.lower() in n["label"].lower():
                return False
    # Check for username text (non-empty TextView that looks like @username)
    for n in nodes:
        if n["label"].startswith("@") and "TextView" in n["class"]:
            return True
    return False


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_status(device=None):
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    installed_out = adb("shell", "pm", "list", "packages", PACKAGE, device=serial)
    installed = PACKAGE in installed_out

    model = adb("shell", "getprop", "ro.product.model", device=serial)
    android_version = adb("shell", "getprop", "ro.build.version.release", device=serial)
    devices = get_connected_devices()

    result = {
        "ok": True,
        "installed": installed,
        "package": PACKAGE,
        "device": serial,
        "model": model,
        "android_version": android_version,
        "connected_devices": devices,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_open(device=None, max_retries=3):
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    last_error = None
    for attempt in range(1, max_retries + 1):
        print(f"[open] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            open_tiktok_with_dismiss(device=serial)

            ss_path = str(DOWNLOADS / "tiktok_open.png")
            screencap(ss_path, device=serial)

            result = {
                "ok": True,
                "device": serial,
                "screenshot_path": ss_path,
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            last_error = str(e)
            print(f"[open] Error attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "error": last_error or "Failed to open TikTok",
        "device": serial,
        "screenshot_path": None,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_inbox(device=None, max_retries=3):
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    last_error = None
    for attempt in range(1, max_retries + 1):
        print(f"[inbox] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Open TikTok and dismiss popups
            open_tiktok_with_dismiss(device=serial)

            # Tap KotakMasuk nav button
            print("[inbox] Tapping KotakMasuk...", file=sys.stderr)
            tap(*NAV_KOTAK_MASUK, device=serial)
            time.sleep(2.0)

            # Screenshot
            ss_path = str(DOWNLOADS / "tiktok_inbox.png")
            screencap(ss_path, device=serial)

            result = {
                "ok": True,
                "screenshot_path": ss_path,
                "device": serial,
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            last_error = str(e)
            print(f"[inbox] Error attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "error": last_error or "Failed to open inbox",
        "device": serial,
        "screenshot_path": None,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_profile(device=None, max_retries=3):
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    last_error = None
    for attempt in range(1, max_retries + 1):
        print(f"[profile] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Open TikTok and dismiss popups
            open_tiktok_with_dismiss(device=serial)

            # Tap Profil nav button
            print("[profile] Tapping Profil...", file=sys.stderr)
            tap(*NAV_PROFIL, device=serial)
            time.sleep(2.0)

            # Screenshot
            ss_path = str(DOWNLOADS / "tiktok_profile.png")
            screencap(ss_path, device=serial)

            result = {
                "ok": True,
                "screenshot_path": ss_path,
                "device": serial,
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            last_error = str(e)
            print(f"[profile] Error attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "error": last_error or "Failed to open profile",
        "device": serial,
        "screenshot_path": None,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(device=None, out=None):
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    out_path = out or str(DOWNLOADS / "tiktok_screenshot.png")
    try:
        screencap(out_path, device=serial)
        result = {
            "ok": True,
            "screenshot_path": out_path,
            "device": serial,
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "device": serial,
            "screenshot_path": None,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_login(username, password, device=None):
    """
    Login to TikTok using username and password.
    Steps:
      1. Launch TikTok
      2. Tap Profil (648, 1505)
      3. If not logged in: tap "Sudah punya akun? Masuk" or "Masuk"
      4. Select "Gunakan email atau nama pengguna"
      5. Tap "Nama pengguna"
      6. Type username
      7. Tap "Berikutnya"
      8. Type password
      9. Tap "Masuk"
      10. Wait 5s, dismiss popups
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print("[login] Launching TikTok...", file=sys.stderr)
        open_tiktok_with_dismiss(device=serial)

        # Tap Profil tab
        print("[login] Tapping Profil tab...", file=sys.stderr)
        tap(*NAV_PROFIL, device=serial)
        time.sleep(2.5)

        nodes = dump_ui(device=serial)

        # Check if already logged in
        already_logged = True
        login_prompts = ["Masuk", "Daftar", "Log in", "Sign up", "Register",
                         "Sudah punya akun", "Gunakan nomor", "Gunakan email"]
        for n in nodes:
            for prompt in login_prompts:
                if prompt.lower() in n["label"].lower():
                    already_logged = False
                    break
            if not already_logged:
                break

        if already_logged:
            # Check for username
            uname = None
            for n in nodes:
                if n["label"].startswith("@"):
                    uname = n["label"]
                    break
            ss_path = str(DOWNLOADS / "tiktok_login.png")
            screencap(ss_path, device=serial)
            result = {
                "ok": True,
                "logged_in": True,
                "username": uname or username,
                "screenshot_path": ss_path,
                "device": serial,
                "note": "Already logged in",
            }
            print(json.dumps(result, indent=2))
            return result

        # Tap "Sudah punya akun? Masuk" or just "Masuk"
        print("[login] Looking for login button...", file=sys.stderr)
        if not tap_node(nodes, label="Sudah punya akun? Masuk", device=serial):
            if not tap_node(nodes, label="Masuk", device=serial):
                tap_node(nodes, label="Log in", device=serial)
        time.sleep(2.0)

        # Select "Gunakan email atau nama pengguna"
        nodes = dump_ui(device=serial)
        print("[login] Selecting 'Gunakan email atau nama pengguna'...", file=sys.stderr)
        if not tap_node(nodes, label="Gunakan email atau nama pengguna", device=serial):
            tap_node(nodes, label="Use email / username", device=serial)
        time.sleep(1.5)

        # Tap "Nama pengguna" option (choose username login vs email)
        nodes = dump_ui(device=serial)
        print("[login] Tapping 'Nama pengguna'...", file=sys.stderr)
        if not tap_node(nodes, label="Nama pengguna", device=serial):
            tap_node(nodes, label="Username", device=serial)
        time.sleep(1.0)

        # Type username in the first EditText
        nodes = dump_ui(device=serial)
        edit_nodes = find_nodes_by_class(nodes, "EditText")
        if edit_nodes:
            c = bounds_to_center(edit_nodes[0]["bounds"])
            if c:
                tap(*c, device=serial)
                time.sleep(0.5)
        type_text(username, device=serial)
        time.sleep(0.8)

        # Tap "Berikutnya" / "Next"
        nodes = dump_ui(device=serial)
        print("[login] Tapping 'Berikutnya'...", file=sys.stderr)
        if not tap_node(nodes, label="Berikutnya", device=serial):
            tap_node(nodes, label="Next", device=serial)
        time.sleep(2.0)

        # Type password in password field
        nodes = dump_ui(device=serial)
        print("[login] Typing password...", file=sys.stderr)
        # Find password EditText by hint "Kata sandi"
        pw_node = find_node(nodes, cls="EditText", hint="Kata sandi")
        if not pw_node:
            # Fallback: find any EditText that appears to be a password field
            edit_nodes = find_nodes_by_class(nodes, "EditText")
            pw_node = edit_nodes[0] if edit_nodes else None
        if pw_node:
            c = bounds_to_center(pw_node["bounds"])
            if c:
                tap(*c, device=serial)
                time.sleep(0.5)
        type_text(password, device=serial)
        time.sleep(0.8)

        # Tap "Masuk" / "Login" button
        nodes = dump_ui(device=serial)
        print("[login] Tapping 'Masuk' button...", file=sys.stderr)
        if not tap_node(nodes, label="Masuk", device=serial):
            tap_node(nodes, label="Log in", device=serial)
        time.sleep(5.0)

        # Dismiss any popups after login
        for _ in range(3):
            dismissed = dismiss_popups(device=serial)
            if dismissed == 0:
                break
            time.sleep(1.0)

        # Screenshot and verify
        ss_path = str(DOWNLOADS / "tiktok_login.png")
        screencap(ss_path, device=serial)

        # Check login success
        nodes = dump_ui(device=serial)
        logged_in = True
        for n in nodes:
            if "Masuk" in n["label"] or "Daftar" in n["label"]:
                logged_in = False
                break

        result = {
            "ok": logged_in,
            "logged_in": logged_in,
            "username": username,
            "screenshot_path": ss_path,
            "device": serial,
        }
        if not logged_in:
            result["error"] = "Login may have failed — login buttons still visible"

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "logged_in": False,
            "username": username,
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_register(username, email, password, phone=None, device=None):
    """
    Register a new TikTok account.
    Steps:
      1. Launch TikTok → Profil tab
      2. Tap "Daftar" / register option
      3. Select phone or email registration
      4. Fill fields step by step
      5. Handle OTP prompt
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print("[register] Launching TikTok...", file=sys.stderr)
        open_tiktok_with_dismiss(device=serial)

        # Tap Profil tab
        print("[register] Tapping Profil tab...", file=sys.stderr)
        tap(*NAV_PROFIL, device=serial)
        time.sleep(2.5)

        nodes = dump_ui(device=serial)

        # Tap "Daftar" / Sign up
        print("[register] Tapping 'Daftar'...", file=sys.stderr)
        if not tap_node(nodes, label="Daftar", device=serial):
            tap_node(nodes, label="Sign up", device=serial)
        time.sleep(2.0)

        nodes = dump_ui(device=serial)

        # Choose registration method: phone or email
        if phone:
            print("[register] Selecting phone registration...", file=sys.stderr)
            if not tap_node(nodes, label="Gunakan nomor ponsel atau email", device=serial):
                tap_node(nodes, label="Use phone / email", device=serial)
            time.sleep(1.5)
            nodes = dump_ui(device=serial)
            # Select phone option
            tap_node(nodes, label="Nomor telepon", device=serial) or \
                tap_node(nodes, label="Phone", device=serial)
            time.sleep(1.0)
            # Type phone number
            nodes = dump_ui(device=serial)
            edit_nodes = find_nodes_by_class(nodes, "EditText")
            if edit_nodes:
                c = bounds_to_center(edit_nodes[0]["bounds"])
                if c:
                    tap(*c, device=serial)
                    time.sleep(0.5)
            type_text(phone, device=serial)
            time.sleep(0.8)
        else:
            print("[register] Selecting email registration...", file=sys.stderr)
            if not tap_node(nodes, label="Gunakan nomor ponsel atau email", device=serial):
                tap_node(nodes, label="Use phone / email", device=serial)
            time.sleep(1.5)
            nodes = dump_ui(device=serial)
            # Select email option
            tap_node(nodes, label="Email", device=serial) or \
                tap_node(nodes, label="Alamat email", partial=True, device=serial)
            time.sleep(1.0)
            # Type email
            nodes = dump_ui(device=serial)
            email_node = find_node(nodes, cls="EditText", hint="Alamat email")
            if not email_node:
                edit_nodes = find_nodes_by_class(nodes, "EditText")
                email_node = edit_nodes[0] if edit_nodes else None
            if email_node:
                c = bounds_to_center(email_node["bounds"])
                if c:
                    tap(*c, device=serial)
                    time.sleep(0.5)
            type_text(email, device=serial)
            time.sleep(0.8)

        # Tap "Berikutnya" / "Next"
        nodes = dump_ui(device=serial)
        print("[register] Tapping 'Berikutnya'...", file=sys.stderr)
        if not tap_node(nodes, label="Berikutnya", device=serial):
            tap_node(nodes, label="Next", device=serial)
        time.sleep(2.0)

        # Check for OTP / verification code prompt
        nodes = dump_ui(device=serial)
        otp_indicators = ["Kode verifikasi", "Verification code", "OTP", "kode", "Masukkan kode"]
        needs_otp = any(
            any(ind.lower() in n["label"].lower() for ind in otp_indicators)
            for n in nodes
        )

        if needs_otp:
            ss_path = str(DOWNLOADS / "tiktok_register_otp.png")
            screencap(ss_path, device=serial)
            result = {
                "ok": False,
                "needs_otp": True,
                "registered": False,
                "username": username,
                "email": email,
                "screenshot_path": ss_path,
                "device": serial,
                "note": "OTP verification required. Please handle manually.",
            }
            print(json.dumps(result, indent=2))
            return result

        # Type password if prompted
        pw_node = find_node(nodes, cls="EditText", hint="Kata sandi")
        if not pw_node:
            edit_nodes = find_nodes_by_class(nodes, "EditText")
            pw_node = edit_nodes[0] if edit_nodes else None
        if pw_node:
            c = bounds_to_center(pw_node["bounds"])
            if c:
                tap(*c, device=serial)
                time.sleep(0.5)
            type_text(password, device=serial)
            time.sleep(0.8)
            nodes = dump_ui(device=serial)
            # Tap next/register
            if not tap_node(nodes, label="Berikutnya", device=serial):
                tap_node(nodes, label="Daftar", device=serial) or \
                    tap_node(nodes, label="Sign up", device=serial)
            time.sleep(3.0)

        # Handle username step if present
        nodes = dump_ui(device=serial)
        uname_node = find_node(nodes, cls="EditText", hint="Nama pengguna") or \
                     find_node(nodes, label="Nama pengguna", partial=True, cls="EditText")
        if uname_node:
            c = bounds_to_center(uname_node["bounds"])
            if c:
                tap(*c, device=serial)
                time.sleep(0.5)
            # Clear existing and type new username
            keyevent(123, device=serial)  # Move to end
            for _ in range(30):
                keyevent(67, device=serial)  # Delete
            type_text(username, device=serial)
            time.sleep(0.8)
            nodes = dump_ui(device=serial)
            if not tap_node(nodes, label="Berikutnya", device=serial):
                tap_node(nodes, label="Daftar", device=serial)
            time.sleep(3.0)

        # Dismiss post-registration popups
        for _ in range(3):
            dismissed = dismiss_popups(device=serial)
            if dismissed == 0:
                break
            time.sleep(1.0)

        ss_path = str(DOWNLOADS / "tiktok_register.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "registered": True,
            "username": username,
            "email": email,
            "screenshot_path": ss_path,
            "device": serial,
        }

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "registered": False,
            "username": username,
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


@_ai_intercept(skill_type="postbridge_post")
def cmd_upload(video_path, caption=None, hashtags=None, device=None):
    """
    Upload a video to TikTok.
    Steps:
      1. Tap + (360, 1505)
      2. Tap "Unggah" or "Upload" tab
      3. Select first video from gallery
      4. Tap "Berikutnya"
      5. Fill caption + hashtags
      6. Tap "Posting" / "Post"
      7. Wait for upload
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print("[upload] Launching TikTok...", file=sys.stderr)
        open_tiktok_with_dismiss(device=serial)
        time.sleep(1.0)

        # Tap + (Post) button
        print("[upload] Tapping + (Post) button...", file=sys.stderr)
        tap(*NAV_POST, device=serial)
        time.sleep(2.5)

        # Tap "Unggah" / "Upload" tab (not record)
        nodes = dump_ui(device=serial)
        print("[upload] Looking for Upload tab...", file=sys.stderr)
        if not tap_node(nodes, label="Unggah", device=serial):
            if not tap_node(nodes, label="Upload", device=serial):
                tap_node(nodes, label="Galeri", device=serial)
        time.sleep(2.0)

        # Select first video from gallery
        nodes = dump_ui(device=serial)
        print("[upload] Selecting first video from gallery...", file=sys.stderr)
        # Try to find video thumbnail — usually first item in a RecyclerView
        video_nodes = [n for n in nodes if n["class"] in ("ImageView", "FrameLayout", "LinearLayout")
                       and n["bounds"]]
        if video_nodes:
            # Pick first that seems like a media item (has reasonable bounds)
            for vn in video_nodes:
                c = bounds_to_center(vn["bounds"])
                if c and c[1] > 200:  # Skip top navigation area
                    tap(*c, device=serial)
                    break
        time.sleep(1.5)

        # Tap "Berikutnya" / "Next"
        nodes = dump_ui(device=serial)
        print("[upload] Tapping 'Berikutnya'...", file=sys.stderr)
        if not tap_node(nodes, label="Berikutnya", device=serial):
            tap_node(nodes, label="Next", device=serial)
        time.sleep(2.5)

        # May have another "Berikutnya" step (trim/edit screen)
        nodes = dump_ui(device=serial)
        if tap_node(nodes, label="Berikutnya", device=serial):
            time.sleep(2.5)
            nodes = dump_ui(device=serial)

        # Fill caption
        if caption or hashtags:
            # Build full caption text
            full_caption = caption or ""
            if hashtags:
                if isinstance(hashtags, str):
                    # Could be comma-separated or space-separated
                    tags = [t.strip().lstrip("#") for t in hashtags.replace(",", " ").split()]
                    full_caption += " " + " ".join(f"#{t}" for t in tags if t)
                elif isinstance(hashtags, list):
                    full_caption += " " + " ".join(f"#{t.lstrip('#')}" for t in hashtags)

            print(f"[upload] Filling caption: {full_caption[:50]}...", file=sys.stderr)
            # Find caption input
            caption_node = find_node(nodes, cls="EditText")
            if caption_node:
                c = bounds_to_center(caption_node["bounds"])
                if c:
                    tap(*c, device=serial)
                    time.sleep(0.5)
                type_text(full_caption, device=serial)
                time.sleep(0.8)
            else:
                # Try tapping the caption area (usually around y=300-500)
                tap(360, 400, device=serial)
                time.sleep(0.5)
                type_text(full_caption, device=serial)
                time.sleep(0.8)

        # Tap "Posting" / "Post"
        nodes = dump_ui(device=serial)
        print("[upload] Tapping 'Posting'...", file=sys.stderr)
        if not tap_node(nodes, label="Posting", device=serial):
            if not tap_node(nodes, label="Post", device=serial):
                tap_node(nodes, label="Unggah", device=serial)
        time.sleep(3.0)

        # Wait for upload progress (up to 30s)
        print("[upload] Waiting for upload to complete...", file=sys.stderr)
        upload_done = False
        for i in range(10):
            time.sleep(3.0)
            nodes = dump_ui(device=serial)
            # Check if we're back to the main feed (upload complete)
            for n in nodes:
                if any(x in n["label"] for x in ["Untuk Anda", "Mengikuti", "For You", "Following"]):
                    upload_done = True
                    break
            if upload_done:
                break
            print(f"[upload] Still uploading... ({(i+1)*3}s)", file=sys.stderr)

        ss_path = str(DOWNLOADS / "tiktok_upload.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "posted": upload_done,
            "caption": caption or "",
            "hashtags": hashtags or [],
            "screenshot_path": ss_path,
            "device": serial,
        }

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "posted": False,
            "caption": caption or "",
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_like(count=1, device=None):
    """
    Like videos on For You feed by double-tapping.
    Double-tap center (360, 820) then swipe up for next video.
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print(f"[like] Liking {count} video(s)...", file=sys.stderr)
        open_tiktok_with_dismiss(device=serial)
        time.sleep(1.0)

        # Make sure we're on For You feed (Beranda)
        tap(*NAV_BERANDA, device=serial)
        time.sleep(2.0)

        liked_count = 0
        for i in range(count):
            print(f"[like] Double-tapping video {i+1}/{count}...", file=sys.stderr)
            # Double-tap center of video
            double_tap(360, 820, device=serial)
            time.sleep(0.5)
            liked_count += 1

            if i < count - 1:
                # Swipe up to next video
                swipe(360, 1200, 360, 400, duration=300, device=serial)
                time.sleep(1.5)

        ss_path = str(DOWNLOADS / "tiktok_like.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "liked_count": liked_count,
            "device": serial,
            "screenshot_path": ss_path,
        }

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "liked_count": 0,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_comment(text, device=None):
    """
    Post a comment on the current video.
    Taps comment icon (~620, 1000), types text, sends.
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print("[comment] Tapping comment icon...", file=sys.stderr)
        # Tap comment icon on right side
        tap(620, 1000, device=serial)
        time.sleep(2.0)

        # Tap comment input field
        nodes = dump_ui(device=serial)
        comment_input = find_node(nodes, cls="EditText")
        if not comment_input:
            # Try tapping the bottom comment input area
            tap(360, 1580, device=serial)
            time.sleep(1.0)
            nodes = dump_ui(device=serial)
            comment_input = find_node(nodes, cls="EditText")

        if comment_input:
            c = bounds_to_center(comment_input["bounds"])
            if c:
                tap(*c, device=serial)
                time.sleep(0.5)

        print(f"[comment] Typing comment: {text[:30]}...", file=sys.stderr)
        type_text(text, device=serial)
        time.sleep(0.8)

        # Tap send button (arrow/send icon)
        nodes = dump_ui(device=serial)
        if not tap_node(nodes, label="Kirim", device=serial):
            if not tap_node(nodes, label="Send", device=serial):
                # Try pressing Enter
                keyevent(66, device=serial)
        time.sleep(1.5)

        ss_path = str(DOWNLOADS / "tiktok_comment.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "commented": True,
            "text": text,
            "screenshot_path": ss_path,
            "device": serial,
        }

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "commented": False,
            "text": text,
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_follow(device=None):
    """
    Follow the creator of the current video.
    Taps follow button on right side (~620, 700 with + icon).
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print("[follow] Tapping follow button...", file=sys.stderr)
        # Follow button is the + icon on the right side around y=700
        tap(620, 700, device=serial)
        time.sleep(1.5)

        ss_path = str(DOWNLOADS / "tiktok_follow.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "followed": True,
            "device": serial,
            "screenshot_path": ss_path,
        }

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "followed": False,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_search(query, device=None):
    """
    Search TikTok for a query.
    Taps magnifying glass icon at top, types query, returns top 5 results.
    """
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        print(f"[search] Searching for: {query}...", file=sys.stderr)
        open_tiktok_with_dismiss(device=serial)
        time.sleep(1.0)

        # Tap search icon (magnifying glass at top)
        # Usually at top right area of the screen
        nodes = dump_ui(device=serial)
        search_tapped = False

        # Try to find search icon by content-desc or label
        for search_label in ["Cari", "Search", "Telusuri"]:
            if tap_node(nodes, label=search_label, device=serial):
                search_tapped = True
                break

        if not search_tapped:
            # Fallback: tap top area where search icon typically is
            tap(690, 60, device=serial)
        time.sleep(2.0)

        # Type query
        nodes = dump_ui(device=serial)
        search_input = find_node(nodes, cls="EditText")
        if search_input:
            c = bounds_to_center(search_input["bounds"])
            if c:
                tap(*c, device=serial)
                time.sleep(0.5)
        type_text(query, device=serial)
        time.sleep(0.8)

        # Press Enter / Search
        keyevent(66, device=serial)
        time.sleep(3.0)

        # Collect results from TextViews
        nodes = dump_ui(device=serial)
        results = []
        for n in nodes:
            if n["label"] and n["label"] != query and len(n["label"]) > 2:
                if n["class"] in ("TextView", "AppCompatTextView"):
                    results.append(n["label"])
                    if len(results) >= 5:
                        break

        ss_path = str(DOWNLOADS / "tiktok_search.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "query": query,
            "results": results[:5],
            "screenshot_path": ss_path,
            "device": serial,
        }

    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "query": query,
            "results": [],
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_scroll(direction="up", count=3, device=None):
    """Scroll TikTok For You feed by swiping up/down N times with natural timing."""
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    try:
        for i in range(count):
            print(f"[scroll] Swipe {i+1}/{count} ({direction})", file=sys.stderr)
            natural_swipe(direction, device=serial)
            natural_pause(1.5, 4.0)  # simulate watch time

        ss_path = str(DOWNLOADS / "tiktok_scroll.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "scrolled_count": count,
            "direction": direction,
            "screenshot_path": ss_path,
            "device": serial,
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "scrolled_count": 0,
            "direction": direction,
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_browse(duration=30, like_chance=0.3, comment_chance=0.05, device=None):
    """Browse TikTok For You feed for `duration` seconds with human-like behaviour."""
    serial, err = resolve_device(device)
    if err:
        result = {"ok": False, "error": err, "device": device or "none"}
        print(json.dumps(result, indent=2))
        return result

    COMMENTS = ["🔥", "❤️", "bagus banget!", "keren!", "😍"]
    videos_watched = 0
    liked_count = 0
    commented_count = 0
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            # Watch current video
            natural_pause(2.0, 6.0)
            videos_watched += 1

            # Maybe like
            if random.random() < like_chance:
                print("[browse] Double-tap to like", file=sys.stderr)
                double_tap(360, 820, device=serial)
                liked_count += 1
                time.sleep(0.5)

            # Maybe comment
            if random.random() < comment_chance:
                print("[browse] Posting comment", file=sys.stderr)
                try:
                    tap(620, 1000, device=serial)
                    time.sleep(2.0)
                    nodes = dump_ui(device=serial)
                    comment_input = find_node(nodes, cls="EditText")
                    if not comment_input:
                        tap(360, 1580, device=serial)
                        time.sleep(1.0)
                        nodes = dump_ui(device=serial)
                        comment_input = find_node(nodes, cls="EditText")
                    if comment_input:
                        c = bounds_to_center(comment_input["bounds"])
                        if c:
                            tap(*c, device=serial)
                            time.sleep(0.3)
                    text = random.choice(COMMENTS)
                    type_text(text, device=serial)
                    time.sleep(0.5)
                    nodes = dump_ui(device=serial)
                    if not tap_node(nodes, label="Kirim", device=serial):
                        keyevent(66, device=serial)
                    time.sleep(1.5)
                    # Close comment sheet
                    keyevent(4, device=serial)
                    time.sleep(0.5)
                    commented_count += 1
                except Exception as ce:
                    print(f"[browse] Comment error (ignored): {ce}", file=sys.stderr)

            # Check if we have time left before swiping
            if time.time() - start_time >= duration:
                break

            # Swipe to next video
            natural_swipe("up", device=serial)

        ss_path = str(DOWNLOADS / "tiktok_browse.png")
        screencap(ss_path, device=serial)

        result = {
            "ok": True,
            "duration": duration,
            "videos_watched": videos_watched,
            "liked_count": liked_count,
            "commented_count": commented_count,
            "screenshot_path": ss_path,
            "device": serial,
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "duration": duration,
            "videos_watched": videos_watched,
            "liked_count": liked_count,
            "commented_count": commented_count,
            "screenshot_path": None,
            "device": serial,
        }

    print(json.dumps(result, indent=2))
    return result


# ─── API Server ──────────────────────────────────────────────────────────────

def run_server(port=8766):
    try:
        import fastapi
        import uvicorn
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "-q"],
            check=True
        )
        import fastapi
        import uvicorn

    from fastapi import FastAPI, Query
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Optional as Opt

    app = FastAPI(
        title="TikTok Android Agent",
        version="2.0.0",
        description="ADB-based TikTok automation agent. All endpoints return JSON with ok:true/false.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class LoginRequest(BaseModel):
        username: str
        password: str
        device: Opt[str] = None

    class RegisterRequest(BaseModel):
        username: str
        email: str
        password: str
        phone: Opt[str] = None
        device: Opt[str] = None

    class UploadRequest(BaseModel):
        video: str
        caption: Opt[str] = None
        hashtags: Opt[List[str]] = None
        device: Opt[str] = None

    class CommentRequest(BaseModel):
        text: str
        device: Opt[str] = None

    class BrowseRequest(BaseModel):
        duration: int = 30
        like_chance: float = 0.3
        comment_chance: float = 0.05
        device: Opt[str] = None

    @app.get("/")
    def root():
        return {
            "service": "autodroid-tiktok-agent",
            "version": "2.0.0",
            "package": PACKAGE,
            "endpoints": [
                "/status", "/open", "/inbox", "/profile", "/screenshot",
                "/login", "/register", "/upload", "/like", "/comment", "/follow", "/search",
                "/scroll", "/browse",
            ],
        }

    @app.get("/status")
    def api_status(device: Opt[str] = None):
        return cmd_status(device=device)

    @app.post("/open")
    def api_open(device: Opt[str] = None):
        return cmd_open(device=device)

    @app.get("/inbox")
    def api_inbox(device: Opt[str] = None):
        return cmd_inbox(device=device)

    @app.get("/profile")
    def api_profile(device: Opt[str] = None):
        return cmd_profile(device=device)

    @app.get("/screenshot")
    def api_screenshot(device: Opt[str] = None, out: Opt[str] = None):
        return cmd_screenshot(device=device, out=out)

    @app.post("/login")
    def api_login(req: LoginRequest):
        return cmd_login(req.username, req.password, device=req.device)

    @app.post("/register")
    def api_register(req: RegisterRequest):
        return cmd_register(req.username, req.email, req.password,
                            phone=req.phone, device=req.device)

    @app.post("/upload")
    def api_upload(req: UploadRequest):
        return cmd_upload(req.video, caption=req.caption,
                          hashtags=req.hashtags, device=req.device)

    @app.post("/like")
    def api_like(count: int = 1, device: Opt[str] = None):
        return cmd_like(count=count, device=device)

    @app.post("/comment")
    def api_comment(req: CommentRequest):
        return cmd_comment(req.text, device=req.device)

    @app.post("/follow")
    def api_follow(device: Opt[str] = None):
        return cmd_follow(device=device)

    @app.get("/search")
    def api_search(query: str = Query(..., description="Search query"), device: Opt[str] = None):
        return cmd_search(query, device=device)

    @app.get("/scroll")
    def api_scroll(direction: str = "up", count: int = 3, device: Opt[str] = None):
        return cmd_scroll(direction=direction, count=count, device=device)

    @app.post("/browse")
    def api_browse(req: BrowseRequest):
        return cmd_browse(duration=req.duration, like_chance=req.like_chance,
                          comment_chance=req.comment_chance, device=req.device)

    @app.get("/health")
    def health():
        devices = get_connected_devices()
        return {"status": "ok", "connected_devices": devices, "count": len(devices)}

    print(f"[server] autodroid-tiktok-agent v2.0 on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[server] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="autodroid-tiktok-agent v2.0 — TikTok Android ADB Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s open
  %(prog)s inbox
  %(prog)s profile
  %(prog)s screenshot --out /tmp/tiktok.png
  %(prog)s login --username myuser --password mypass
  %(prog)s register --username newuser --email new@email.com --password mypass
  %(prog)s upload --video /sdcard/video.mp4 --caption "Hello!" --hashtags fyp viral
  %(prog)s like --count 5
  %(prog)s comment --text "Great video!"
  %(prog)s follow
  %(prog)s search --query "cooking tutorial"
  %(prog)s server --port 8766

API (after starting server):
  curl http://localhost:8766/status
  curl -X POST http://localhost:8766/open
  curl http://localhost:8766/inbox
  curl http://localhost:8766/profile
  curl http://localhost:8766/screenshot
  curl -X POST http://localhost:8766/login -H 'Content-Type: application/json' -d '{"username":"u","password":"p"}'
  curl -X POST http://localhost:8766/register -H 'Content-Type: application/json' -d '{"username":"u","email":"e@e.com","password":"p"}'
  curl -X POST http://localhost:8766/upload -H 'Content-Type: application/json' -d '{"video":"/path/to/video.mp4"}'
  curl -X POST 'http://localhost:8766/like?count=3'
  curl -X POST http://localhost:8766/comment -H 'Content-Type: application/json' -d '{"text":"Nice!"}'
  curl -X POST http://localhost:8766/follow
  curl 'http://localhost:8766/search?query=cooking'
"""
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Check TikTok install + device info")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("open", help="Launch TikTok and dismiss popups")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("inbox", help="Open TikTok inbox (KotakMasuk)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("profile", help="Open TikTok profile tab")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("screenshot", help="Take a screenshot")
    s.add_argument("--device", "-d", help="ADB device serial")
    s.add_argument("--out", "-o", help="Output path for screenshot")

    s = sub.add_parser("login", help="Login to TikTok with username/password")
    s.add_argument("--username", "-u", required=True, help="TikTok username")
    s.add_argument("--password", "-p", required=True, help="TikTok password")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("register", help="Register a new TikTok account")
    s.add_argument("--username", "-u", required=True, help="Desired username")
    s.add_argument("--email", "-e", required=True, help="Email address")
    s.add_argument("--password", "-p", required=True, help="Password")
    s.add_argument("--phone", help="Phone number (optional)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("upload", help="Upload a video to TikTok")
    s.add_argument("--video", required=True, help="Path to video file")
    s.add_argument("--caption", help="Video caption")
    s.add_argument("--hashtags", nargs="+", help="Hashtags (without #)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("like", help="Like videos on For You feed")
    s.add_argument("--count", "-n", type=int, default=1, help="Number of videos to like (default: 1)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("comment", help="Post a comment on current video")
    s.add_argument("--text", "-t", required=True, help="Comment text")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("follow", help="Follow creator of current video")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("search", help="Search TikTok for a query")
    s.add_argument("--query", "-q", required=True, help="Search query")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("scroll", help="Scroll TikTok feed (natural swipe)")
    s.add_argument("--direction", default="up", choices=["up", "down"], help="Swipe direction (default: up)")
    s.add_argument("--count", "-n", type=int, default=3, help="Number of swipes (default: 3)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("browse", help="Browse TikTok For You feed for N seconds")
    s.add_argument("--duration", type=int, default=30, help="Browse duration in seconds (default: 30)")
    s.add_argument("--like-chance", type=float, default=0.3, help="Probability to like each video (default: 0.3)")
    s.add_argument("--comment-chance", type=float, default=0.05, help="Probability to comment (default: 0.05)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("server", help="Start FastAPI server")
    s.add_argument("--port", type=int, default=8766)

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status(device=args.device)
    elif args.cmd == "open":
        cmd_open(device=args.device)
    elif args.cmd == "inbox":
        cmd_inbox(device=args.device)
    elif args.cmd == "profile":
        cmd_profile(device=args.device)
    elif args.cmd == "screenshot":
        cmd_screenshot(device=args.device, out=args.out)
    elif args.cmd == "login":
        cmd_login(args.username, args.password, device=args.device)
    elif args.cmd == "register":
        cmd_register(args.username, args.email, args.password,
                     phone=getattr(args, "phone", None), device=args.device)
    elif args.cmd == "upload":
        cmd_upload(args.video, caption=args.caption,
                   hashtags=args.hashtags, device=args.device)
    elif args.cmd == "like":
        cmd_like(count=args.count, device=args.device)
    elif args.cmd == "comment":
        cmd_comment(args.text, device=args.device)
    elif args.cmd == "follow":
        cmd_follow(device=args.device)
    elif args.cmd == "search":
        cmd_search(args.query, device=args.device)
    elif args.cmd == "scroll":
        cmd_scroll(direction=args.direction, count=args.count, device=args.device)
    elif args.cmd == "browse":
        cmd_browse(duration=args.duration, like_chance=args.like_chance,
                   comment_chance=args.comment_chance, device=args.device)
    elif args.cmd == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
