#!/usr/bin/env python3
"""
autodroid-instagram-agent v2.0 — Instagram Android automation via ADB

Commands:
  status                    -- check app + device
  open   [--device]         -- launch Instagram, dismiss popups, screenshot
  feed   [--device]         -- open Instagram, screenshot feed
  inbox  [--device]         -- open Instagram, tap DM icon, screenshot
  screenshot [--out PATH]   -- capture screen
  register --username U --email E --password P --fullname N [--phone PHONE] [--device]
  login --username U --password P [--device]
  post --media PATH [--caption TEXT] [--device]
  like [--count N] [--device]
  comment --text TEXT [--device]
  follow --username U [--device]
  dm --username U --message MSG [--device]
  server [--port 8769]      -- start FastAPI server

All commands: retry 3x, ok:true/false, include device.
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
    _interceptor = ContentInterceptor()  # Instagram = content posting
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

PACKAGE = "com.instagram.android"
DOWNLOADS = Path("~/.openclaw/workspace/downloads").expanduser()
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

DISMISS_LABELS = {
    "OK", "Allow", "Continue", "Skip", "Not Now", "Nanti", "Tutup",
    "Accept", "Agree", "Close", "Dismiss", "Get Started",
    "Oke", "Izinkan", "Lanjutkan", "Tidak sekarang", "Lewati",
}

# Verified coords for Redmi 2409BRN2CY (720x1640)
COORDS = {
    "mulai": (360, 1290),           # Register new / onboarding
    "punya_akun": (360, 1402),      # Login / "Saya sudah punya akun"
    "language": (360, 278),
    "home": (72, 1540),
    "search": (216, 1540),
    "post_btn": (360, 1540),
    "reels": (504, 1540),
    "profile": (648, 1540),
    "dm_icon": (660, 120),
    "feed_center": (360, 820),
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
    adb("shell", "input", "tap", str(x), str(y), device=device)
    time.sleep(0.1)
    adb("shell", "input", "tap", str(x), str(y), device=device)


def swipe(x1, y1, x2, y2, duration=300, device=None):
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration), device=device)


def keyevent(key, device=None):
    adb("shell", "input", "keyevent", str(key), device=device)


def type_text(text, device=None):
    """Type text via ADB, escaping special characters."""
    escaped = text.replace(" ", "%s").replace("'", "\\'").replace('"', '\\"')
    adb("shell", "input", "text", escaped, device=device)


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
    remote = "/sdcard/ig_dump.xml"
    local = "/tmp/ig_dump.xml"
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
            res_id = n.get("resource-id", "")
            label = text or desc
            nodes.append({
                "label": label, "text": text, "desc": desc,
                "class": cls, "bounds": bounds, "resource_id": res_id,
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


def find_node(nodes, label=None, cls=None, partial=False, resource_id=None):
    for n in nodes:
        if resource_id and resource_id in n.get("resource_id", ""):
            return n
        if label:
            match = (n["label"] == label) if not partial else (label.lower() in n["label"].lower())
            if not match:
                continue
        if cls and cls not in n["class"]:
            continue
        if label or resource_id:
            return n
    return None


def tap_node(nodes, label=None, cls=None, partial=False, resource_id=None, device=None):
    n = find_node(nodes, label=label, cls=cls, partial=partial, resource_id=resource_id)
    if n:
        c = bounds_to_center(n["bounds"])
        if c:
            tap(*c, device=device)
            return True
    return False


def tap_node_and_type(nodes, text_to_type, label=None, resource_id=None, cls=None,
                      partial=False, device=None):
    """Tap a field and type text into it."""
    n = find_node(nodes, label=label, cls=cls, partial=partial, resource_id=resource_id)
    if n:
        c = bounds_to_center(n["bounds"])
        if c:
            tap(*c, device=device)
            time.sleep(0.5)
            # Clear field first
            adb("shell", "input", "keyevent", "KEYCODE_CTRL_A", device=device)
            time.sleep(0.2)
            type_text(text_to_type, device=device)
            return True
    return False


# ─── High-level Actions ──────────────────────────────────────────────────────

def get_connected_devices():
    out = adb("devices")
    return [l.split()[0] for l in out.splitlines()[1:] if "\tdevice" in l]


def dismiss_popups(nodes, device=None):
    dismissed = 0
    for n in nodes:
        if n["label"] in DISMISS_LABELS:
            c = bounds_to_center(n["bounds"])
            if c:
                tap(*c, device=device)
                time.sleep(0.4)
                dismissed += 1
    return dismissed


def dismiss_popups_aggressive(device=None):
    """Multi-round popup dismissal."""
    for _ in range(3):
        nodes = dump_ui(device=device)
        dismissed = dismiss_popups(nodes, device=device)
        if dismissed == 0:
            break
        time.sleep(0.5)


def launch_instagram(device=None):
    wake(device=device)
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(0.5)
    adb("shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1",
        device=device)
    time.sleep(3.5)
    wake(device=device)
    # Dismiss any immediate popups
    nodes = dump_ui(device=device)
    dismiss_popups(nodes, device=device)
    time.sleep(0.5)


def detect_screen_state(nodes):
    """Detect current Instagram screen state from UI nodes."""
    labels = [n["label"].lower() for n in nodes if n["label"]]
    res_ids = [n.get("resource_id", "") for n in nodes]

    # Feed / home state
    if any("com.instagram.android:id/tab_bar" in r for r in res_ids):
        return "FEED"

    # Login page
    if any("login_username" in r or "password" in r for r in res_ids):
        return "LOGIN"
    if any("masuk" in l or "log in" in l or "login" in l for l in labels):
        return "LOGIN"

    # Onboarding
    if any("mulai" in l or "get started" in l for l in labels):
        return "ONBOARDING"
    if any("saya sudah punya akun" in l or "i already have an account" in l for l in labels):
        return "ONBOARDING"

    # Registration steps
    if any("nomor ponsel" in l or "phone number" in l or "alamat email" in l for l in labels):
        return "REGISTER_PHONE_EMAIL"
    if any("nama lengkap" in l or "full name" in l for l in labels):
        return "REGISTER_NAME"
    if any("nama pengguna" in l or "username" in l for l in labels):
        return "REGISTER_USERNAME"
    if any("kata sandi" in l or "password" in l for l in labels):
        return "REGISTER_PASSWORD"
    if any("tanggal lahir" in l or "birthday" in l or "date of birth" in l for l in labels):
        return "REGISTER_BIRTHDAY"
    if any("tambahkan foto" in l or "add photo" in l or "profile photo" in l for l in labels):
        return "REGISTER_PHOTO"

    return "UNKNOWN"


def tap_next(nodes, device=None):
    """Tap Berikutnya / Next / Continue button."""
    return (
        tap_node(nodes, label="Berikutnya", device=device) or
        tap_node(nodes, label="Next", device=device) or
        tap_node(nodes, label="Lanjutkan", device=device) or
        tap_node(nodes, label="Continue", device=device) or
        tap_node(nodes, partial=True, label="Berikut", device=device)
    )


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_status(device=None):
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)
    installed = False
    model = "unknown"
    if active_device:
        installed = PACKAGE in adb("shell", "pm", "list", "packages", PACKAGE, device=active_device)
        model = adb("shell", "getprop", "ro.product.model", device=active_device)
    result = {
        "ok": True,
        "installed": installed,
        "package": PACKAGE,
        "device": active_device or "none",
        "model": model,
        "connected_devices": devices,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_open(device=None, max_retries=3):
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[open] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_instagram(device=active_device)

            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)
            time.sleep(1)

            ss_path = str(DOWNLOADS / "instagram_open.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[open] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "screenshot_path": None,
        "error": "Failed to open Instagram after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_feed(device=None, max_retries=3):
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[feed] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_instagram(device=active_device)
            time.sleep(2)

            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)
            time.sleep(0.5)

            tapped = (
                tap_node(nodes, label="Home", device=active_device) or
                tap_node(nodes, label="Beranda", device=active_device) or
                tap_node(nodes, desc="Home", device=active_device) or
                tap_node(nodes, desc="Beranda", device=active_device)
            )
            if tapped:
                time.sleep(1.5)

            ss_path = str(DOWNLOADS / "instagram_feed.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[feed] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "screenshot_path": None,
        "error": "Failed to get feed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_inbox(device=None, max_retries=3):
    """Open Instagram then tap DM icon (paper plane ~top right ~x=660,y=120)."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[inbox] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_instagram(device=active_device)
            time.sleep(2)

            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)
            time.sleep(0.5)

            dm_tapped = (
                tap_node(nodes, label="Direct", device=active_device) or
                tap_node(nodes, label="Messenger", device=active_device) or
                tap_node(nodes, label="DM", device=active_device) or
                tap_node(nodes, desc="Direct", device=active_device) or
                tap_node(nodes, desc="Messenger", device=active_device) or
                tap_node(nodes, partial=True, label="Direct message", device=active_device) or
                tap_node(nodes, partial=True, desc="Direct message", device=active_device)
            )

            if not dm_tapped:
                print("[inbox] DM icon not found by label, using fallback coordinates (660,120)", file=sys.stderr)
                tap(*COORDS["dm_icon"], device=active_device)

            time.sleep(2)
            nodes2 = dump_ui(device=active_device)
            dismiss_popups(nodes2, device=active_device)
            time.sleep(0.5)

            ss_path = str(DOWNLOADS / "instagram_inbox.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[inbox] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "screenshot_path": None,
        "error": "Failed to open inbox after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(device=None, out=None):
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)
    out_path = out or str(DOWNLOADS / "instagram_screenshot.png")
    screencap(out_path, device=active_device)
    result = {
        "ok": True,
        "screenshot_path": out_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: Register ───────────────────────────────────────────────────────────

def cmd_register(username, email, password, fullname, phone=None, device=None, max_retries=3):
    """Register a new Instagram account."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[register] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_instagram(device=active_device)
            time.sleep(2)

            nodes = dump_ui(device=active_device)
            state = detect_screen_state(nodes)
            print(f"[register] Screen state: {state}", file=sys.stderr)

            # Navigate to registration
            if state == "LOGIN":
                # Tap "Buat akun baru" / "Create new account"
                tapped = (
                    tap_node(nodes, label="Buat akun baru", device=active_device) or
                    tap_node(nodes, label="Create new account", device=active_device) or
                    tap_node(nodes, partial=True, label="akun baru", device=active_device)
                )
                if not tapped:
                    # Fallback: button is around y~1050
                    tap(360, 1050, device=active_device)
                time.sleep(2)
                nodes = dump_ui(device=active_device)

            elif state == "ONBOARDING":
                # Tap "Mulai" to start registration
                tapped = (
                    tap_node(nodes, label="Mulai", device=active_device) or
                    tap_node(nodes, label="Get started", device=active_device) or
                    tap_node(nodes, label="Create new account", device=active_device)
                )
                if not tapped:
                    tap(*COORDS["mulai"], device=active_device)
                time.sleep(2)
                nodes = dump_ui(device=active_device)

            # Step: Enter phone or email
            print("[register] Filling phone/email field", file=sys.stderr)
            contact = phone if phone else email
            filled = (
                tap_node_and_type(nodes, contact, partial=True, label="Nomor ponsel", device=active_device) or
                tap_node_and_type(nodes, contact, partial=True, label="Phone", device=active_device) or
                tap_node_and_type(nodes, contact, partial=True, label="Email", device=active_device) or
                tap_node_and_type(nodes, contact, partial=True, label="Alamat email", device=active_device) or
                tap_node_and_type(nodes, contact, cls="EditText", device=active_device)
            )
            time.sleep(0.5)

            # If using email, tap "Daftar dengan alamat email" link first if present
            nodes = dump_ui(device=active_device)
            tap_node(nodes, partial=True, label="Daftar dengan alamat email", device=active_device)
            tap_node(nodes, partial=True, label="Sign up with email", device=active_device)
            time.sleep(0.5)

            # Tap Next
            nodes = dump_ui(device=active_device)
            if not tap_next(nodes, device=active_device):
                tap(360, 1200, device=active_device)  # fallback
            time.sleep(2)

            # Step: Fill fullname
            print("[register] Filling fullname", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled_name = (
                tap_node_and_type(nodes, fullname, partial=True, label="Nama lengkap", device=active_device) or
                tap_node_and_type(nodes, fullname, partial=True, label="Full name", device=active_device) or
                tap_node_and_type(nodes, fullname, cls="EditText", device=active_device)
            )
            time.sleep(0.5)
            nodes = dump_ui(device=active_device)
            if not tap_next(nodes, device=active_device):
                tap(360, 1200, device=active_device)
            time.sleep(2)

            # Step: Fill username
            print("[register] Filling username", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled_user = (
                tap_node_and_type(nodes, username, partial=True, label="Nama pengguna", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="Username", device=active_device) or
                tap_node_and_type(nodes, username, cls="EditText", device=active_device)
            )
            time.sleep(0.5)
            nodes = dump_ui(device=active_device)
            if not tap_next(nodes, device=active_device):
                tap(360, 1200, device=active_device)
            time.sleep(2)

            # Step: Fill password
            print("[register] Filling password", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled_pass = (
                tap_node_and_type(nodes, password, partial=True, label="Kata sandi", device=active_device) or
                tap_node_and_type(nodes, password, partial=True, label="Password", device=active_device) or
                tap_node_and_type(nodes, password, resource_id="com.instagram.android:id/password", device=active_device) or
                tap_node_and_type(nodes, password, cls="EditText", device=active_device)
            )
            time.sleep(0.5)
            nodes = dump_ui(device=active_device)
            if not tap_next(nodes, device=active_device):
                tap(360, 1200, device=active_device)
            time.sleep(2)

            # Handle birthday page
            print("[register] Handling birthday page", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            state2 = detect_screen_state(nodes)
            if "BIRTHDAY" in state2 or tap_node(nodes, partial=True, label="Tanggal lahir", device=active_device):
                if not tap_next(nodes, device=active_device):
                    tap(360, 1200, device=active_device)
                time.sleep(2)

            # Multiple next presses for intermediate pages
            for _ in range(3):
                nodes = dump_ui(device=active_device)
                dismiss_popups(nodes, device=active_device)
                tap_next(nodes, device=active_device)
                time.sleep(1.5)

            # Dismiss "Tambahkan foto profil" / Add photo
            nodes = dump_ui(device=active_device)
            skipped_photo = (
                tap_node(nodes, label="Lewati", device=active_device) or
                tap_node(nodes, label="Skip", device=active_device) or
                tap_node(nodes, label="Nanti", device=active_device) or
                tap_node(nodes, partial=True, label="Lewat", device=active_device)
            )
            time.sleep(1.5)

            # Dismiss notification prompts
            nodes = dump_ui(device=active_device)
            dismissed = (
                tap_node(nodes, label="Nanti", device=active_device) or
                tap_node(nodes, label="Skip", device=active_device) or
                tap_node(nodes, label="Not Now", device=active_device) or
                tap_node(nodes, label="Tidak sekarang", device=active_device)
            )
            time.sleep(1.5)

            dismiss_popups_aggressive(device=active_device)
            time.sleep(1)

            ss_path = str(DOWNLOADS / f"instagram_register_{username}.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "registered": True,
                "username": username,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[register] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(3)

    result = {
        "ok": False,
        "registered": False,
        "username": username,
        "screenshot_path": None,
        "error": "Registration failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: Login ──────────────────────────────────────────────────────────────

def cmd_login(username, password, device=None, max_retries=3):
    """Login to an existing Instagram account."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[login] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_instagram(device=active_device)
            time.sleep(2)

            nodes = dump_ui(device=active_device)
            state = detect_screen_state(nodes)
            print(f"[login] Screen state: {state}", file=sys.stderr)

            # If on onboarding, tap "Saya sudah punya akun"
            if state == "ONBOARDING":
                tapped = (
                    tap_node(nodes, label="Saya sudah punya akun", device=active_device) or
                    tap_node(nodes, partial=True, label="sudah punya akun", device=active_device) or
                    tap_node(nodes, partial=True, label="already have an account", device=active_device) or
                    tap_node(nodes, label="Log In", device=active_device) or
                    tap_node(nodes, label="Login", device=active_device)
                )
                if not tapped:
                    tap(*COORDS["punya_akun"], device=active_device)
                time.sleep(2)
                nodes = dump_ui(device=active_device)

            # Fill username
            print("[login] Filling username", file=sys.stderr)
            filled_user = (
                tap_node_and_type(nodes, username,
                    resource_id="com.instagram.android:id/login_username", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="Nomor ponsel", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="Email", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="Username", device=active_device)
            )
            if not filled_user:
                # Fallback: EditText index 0 (y~600)
                tap(360, 600, device=active_device)
                time.sleep(0.3)
                type_text(username, device=active_device)
            time.sleep(0.5)

            # Fill password
            print("[login] Filling password", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled_pass = (
                tap_node_and_type(nodes, password,
                    resource_id="com.instagram.android:id/password", device=active_device) or
                tap_node_and_type(nodes, password, partial=True, label="Kata sandi", device=active_device) or
                tap_node_and_type(nodes, password, partial=True, label="Password", device=active_device)
            )
            if not filled_pass:
                # Fallback: EditText index 1 (y~720)
                tap(360, 720, device=active_device)
                time.sleep(0.3)
                type_text(password, device=active_device)
            time.sleep(0.5)

            # Tap Login button
            print("[login] Tapping login button", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            tapped_login = (
                tap_node(nodes, label="Masuk", device=active_device) or
                tap_node(nodes, label="Login", device=active_device) or
                tap_node(nodes, label="Log In", device=active_device) or
                tap_node(nodes, label="Sign In", device=active_device) or
                tap_node(nodes, partial=True, label="Masuk", device=active_device)
            )
            if not tapped_login:
                tap(360, 900, device=active_device)

            # Wait for feed to load
            print("[login] Waiting for feed...", file=sys.stderr)
            time.sleep(5)

            # Dismiss post-login popups
            for _ in range(4):
                nodes = dump_ui(device=active_device)
                state2 = detect_screen_state(nodes)
                dismissed = (
                    tap_node(nodes, label="Nanti", device=active_device) or
                    tap_node(nodes, label="Tidak sekarang", device=active_device) or
                    tap_node(nodes, label="Lewati", device=active_device) or
                    tap_node(nodes, label="Skip", device=active_device) or
                    tap_node(nodes, label="Allow", device=active_device) or
                    tap_node(nodes, label="Izinkan", device=active_device) or
                    tap_node(nodes, label="Not Now", device=active_device)
                )
                if state2 == "FEED":
                    break
                time.sleep(1)

            nodes = dump_ui(device=active_device)
            state_final = detect_screen_state(nodes)
            logged_in = state_final == "FEED"

            ss_path = str(DOWNLOADS / f"instagram_login_{username}.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": logged_in,
                "logged_in": logged_in,
                "username": username,
                "screen_state": state_final,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            if logged_in:
                return result

        except Exception as e:
            print(f"[login] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(3)

    result = {
        "ok": False,
        "logged_in": False,
        "username": username,
        "screenshot_path": None,
        "error": "Login failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: Post ───────────────────────────────────────────────────────────────

@_ai_intercept(skill_type="postbridge_post")
def cmd_post(media_path, caption=None, device=None, max_retries=3):
    """Post an image/video to Instagram."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    # Push media to device first
    remote_media = f"/sdcard/DCIM/{Path(media_path).name}"
    print(f"[post] Pushing media to device: {remote_media}", file=sys.stderr)
    adb("push", media_path, remote_media, device=active_device)
    # Scan media so gallery finds it
    adb("shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
        "-d", f"file://{remote_media}", device=active_device)
    time.sleep(1)

    for attempt in range(1, max_retries + 1):
        print(f"[post] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Ensure on feed
            wake(device=active_device)
            time.sleep(1)
            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)

            # Tap + (post) button
            print("[post] Tapping post (+) button", file=sys.stderr)
            tapped_post = (
                tap_node(nodes, partial=True, label="New post", device=active_device) or
                tap_node(nodes, partial=True, label="Post baru", device=active_device) or
                tap_node(nodes, partial=True, desc="New post", device=active_device) or
                tap_node(nodes, partial=True, desc="Post baru", device=active_device)
            )
            if not tapped_post:
                tap(*COORDS["post_btn"], device=active_device)
            time.sleep(2)

            # Select first gallery item
            print("[post] Selecting first gallery item", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)
            # Gallery items usually at top area of selection screen
            tap(90, 300, device=active_device)  # First gallery item (top-left)
            time.sleep(1.5)

            # Tap Berikutnya (Next) to proceed past gallery
            nodes = dump_ui(device=active_device)
            if not tap_next(nodes, device=active_device):
                tap(650, 80, device=active_device)  # Top right Next button fallback
            time.sleep(1.5)

            # Tap Berikutnya again to skip filters
            nodes = dump_ui(device=active_device)
            if not tap_next(nodes, device=active_device):
                tap(650, 80, device=active_device)
            time.sleep(1.5)

            # Fill caption if provided
            if caption:
                print("[post] Filling caption", file=sys.stderr)
                nodes = dump_ui(device=active_device)
                filled_caption = (
                    tap_node_and_type(nodes, caption, partial=True, label="Tulis caption", device=active_device) or
                    tap_node_and_type(nodes, caption, partial=True, label="Write a caption", device=active_device) or
                    tap_node_and_type(nodes, caption, cls="EditText", device=active_device)
                )
                if not filled_caption:
                    tap(360, 300, device=active_device)
                    time.sleep(0.4)
                    type_text(caption, device=active_device)
                time.sleep(0.5)

            # Tap Bagikan / Share
            print("[post] Tapping share button", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            shared = (
                tap_node(nodes, label="Bagikan", device=active_device) or
                tap_node(nodes, label="Share", device=active_device) or
                tap_node(nodes, partial=True, label="Bagik", device=active_device)
            )
            if not shared:
                tap(650, 80, device=active_device)

            # Wait for upload
            print("[post] Waiting for upload...", file=sys.stderr)
            time.sleep(8)

            dismiss_popups_aggressive(device=active_device)

            ss_path = str(DOWNLOADS / "instagram_post.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "posted": True,
                "caption": caption or "",
                "media_path": media_path,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[post] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(3)

    result = {
        "ok": False,
        "posted": False,
        "caption": caption or "",
        "screenshot_path": None,
        "error": "Post failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: Like ───────────────────────────────────────────────────────────────

def cmd_like(count=1, device=None, max_retries=3):
    """Like posts by double-tapping on feed."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[like] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            liked_count = 0
            wake(device=active_device)

            # Ensure on feed
            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)
            tap(*COORDS["home"], device=active_device)
            time.sleep(2)

            for i in range(count):
                print(f"[like] Liking post {i+1}/{count}", file=sys.stderr)
                # Double-tap center of screen
                double_tap(*COORDS["feed_center"], device=active_device)
                liked_count += 1
                time.sleep(1.5)

                if i < count - 1:
                    # Swipe up for next post
                    swipe(360, 900, 360, 400, duration=400, device=active_device)
                    time.sleep(2)

                    # Dismiss any popups
                    nodes = dump_ui(device=active_device)
                    dismiss_popups(nodes, device=active_device)

            ss_path = str(DOWNLOADS / "instagram_like.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "liked_count": liked_count,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[like] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "liked_count": 0,
        "screenshot_path": None,
        "error": "Like failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: Comment ─────────────────────────────────────────────────────────────

def cmd_comment(text, device=None, max_retries=3):
    """Comment on current post."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[comment] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            wake(device=active_device)
            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)

            # Find and tap comment icon
            print("[comment] Tapping comment icon", file=sys.stderr)
            tapped_comment = (
                tap_node(nodes, partial=True, label="Comment", device=active_device) or
                tap_node(nodes, partial=True, label="Komentar", device=active_device) or
                tap_node(nodes, partial=True, desc="Comment", device=active_device) or
                tap_node(nodes, partial=True, desc="comment", device=active_device)
            )
            if not tapped_comment:
                # Fallback: comment icon usually below post, to right of like
                tap(120, 1200, device=active_device)
            time.sleep(1.5)

            # Find comment input field
            print("[comment] Finding comment input", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled = (
                tap_node_and_type(nodes, text, partial=True, label="Tambahkan komentar", device=active_device) or
                tap_node_and_type(nodes, text, partial=True, label="Add a comment", device=active_device) or
                tap_node_and_type(nodes, text, partial=True, label="Tulis komentar", device=active_device) or
                tap_node_and_type(nodes, text, cls="EditText", device=active_device)
            )
            if not filled:
                # Fallback: bottom of screen
                tap(360, 1580, device=active_device)
                time.sleep(0.4)
                type_text(text, device=active_device)
            time.sleep(0.5)

            # Tap Kirim / Post / Send
            nodes = dump_ui(device=active_device)
            sent = (
                tap_node(nodes, label="Kirim", device=active_device) or
                tap_node(nodes, label="Post", device=active_device) or
                tap_node(nodes, label="Send", device=active_device) or
                tap_node(nodes, label="Posting", device=active_device)
            )
            if not sent:
                keyevent("KEYCODE_ENTER", device=active_device)
            time.sleep(1.5)

            ss_path = str(DOWNLOADS / "instagram_comment.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "commented": True,
                "text": text,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[comment] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "commented": False,
        "text": text,
        "screenshot_path": None,
        "error": "Comment failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: Follow ──────────────────────────────────────────────────────────────

def cmd_follow(username, device=None, max_retries=3):
    """Follow a user by searching their profile."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[follow] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            wake(device=active_device)
            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)

            # Tap search icon
            print("[follow] Tapping search", file=sys.stderr)
            tapped_search = (
                tap_node(nodes, label="Search", device=active_device) or
                tap_node(nodes, label="Cari", device=active_device) or
                tap_node(nodes, desc="Search", device=active_device)
            )
            if not tapped_search:
                tap(*COORDS["search"], device=active_device)
            time.sleep(1.5)

            # Tap search bar and type username
            print(f"[follow] Searching for {username}", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled = (
                tap_node_and_type(nodes, username, partial=True, label="Cari", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="Search", device=active_device) or
                tap_node_and_type(nodes, username, cls="EditText", device=active_device)
            )
            if not filled:
                tap(360, 150, device=active_device)  # Search bar fallback
                time.sleep(0.4)
                type_text(username, device=active_device)
            time.sleep(2)

            # Tap first result
            print("[follow] Tapping first result", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            tapped_result = tap_node(nodes, label=username, device=active_device)
            if not tapped_result:
                # Tap first result item
                tap(360, 350, device=active_device)
            time.sleep(2)

            # Tap Ikuti / Follow
            print("[follow] Tapping follow button", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            followed = (
                tap_node(nodes, label="Ikuti", device=active_device) or
                tap_node(nodes, label="Follow", device=active_device) or
                tap_node(nodes, partial=True, label="Ikuti", device=active_device)
            )

            time.sleep(1.5)
            ss_path = str(DOWNLOADS / f"instagram_follow_{username}.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "followed": followed,
                "username": username,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[follow] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "followed": False,
        "username": username,
        "screenshot_path": None,
        "error": "Follow failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW: DM ─────────────────────────────────────────────────────────────────

def cmd_dm(username, message, device=None, max_retries=3):
    """Send a direct message to a user."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[dm] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            wake(device=active_device)
            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)

            # Tap DM icon (paper plane top right)
            print("[dm] Tapping DM icon", file=sys.stderr)
            tapped_dm = (
                tap_node(nodes, partial=True, label="Direct", device=active_device) or
                tap_node(nodes, partial=True, desc="Direct message", device=active_device) or
                tap_node(nodes, partial=True, label="Pesan", device=active_device)
            )
            if not tapped_dm:
                tap(*COORDS["dm_icon"], device=active_device)
            time.sleep(2)

            # Tap compose / pencil icon
            print("[dm] Tapping compose icon", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            tapped_compose = (
                tap_node(nodes, partial=True, label="Compose", device=active_device) or
                tap_node(nodes, partial=True, label="New message", device=active_device) or
                tap_node(nodes, partial=True, label="Pesan baru", device=active_device) or
                tap_node(nodes, partial=True, desc="Compose", device=active_device) or
                tap_node(nodes, partial=True, desc="New message", device=active_device)
            )
            if not tapped_compose:
                tap(650, 120, device=active_device)  # Pencil/compose icon top right
            time.sleep(1.5)

            # Type username in To: field
            print(f"[dm] Typing recipient: {username}", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled_to = (
                tap_node_and_type(nodes, username, partial=True, label="Cari", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="Search", device=active_device) or
                tap_node_and_type(nodes, username, partial=True, label="To:", device=active_device) or
                tap_node_and_type(nodes, username, cls="EditText", device=active_device)
            )
            if not filled_to:
                tap(360, 200, device=active_device)
                time.sleep(0.4)
                type_text(username, device=active_device)
            time.sleep(2)

            # Tap username in dropdown
            print("[dm] Selecting user from dropdown", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            tapped_user = tap_node(nodes, label=username, device=active_device)
            if not tapped_user:
                tap(360, 350, device=active_device)
            time.sleep(1.5)

            # Tap Chat / Next
            nodes = dump_ui(device=active_device)
            tapped_chat = (
                tap_node(nodes, label="Chat", device=active_device) or
                tap_node(nodes, label="Next", device=active_device) or
                tap_node(nodes, label="Berikutnya", device=active_device) or
                tap_node(nodes, label="Mulai chat", device=active_device)
            )
            if not tapped_chat:
                tap(650, 80, device=active_device)
            time.sleep(1.5)

            # Type message
            print(f"[dm] Typing message", file=sys.stderr)
            nodes = dump_ui(device=active_device)
            filled_msg = (
                tap_node_and_type(nodes, message, partial=True, label="Kirim pesan", device=active_device) or
                tap_node_and_type(nodes, message, partial=True, label="Message", device=active_device) or
                tap_node_and_type(nodes, message, partial=True, label="Pesan", device=active_device) or
                tap_node_and_type(nodes, message, cls="EditText", device=active_device)
            )
            if not filled_msg:
                tap(300, 1580, device=active_device)
                time.sleep(0.4)
                type_text(message, device=active_device)
            time.sleep(0.5)

            # Tap Send
            nodes = dump_ui(device=active_device)
            sent = (
                tap_node(nodes, label="Kirim", device=active_device) or
                tap_node(nodes, label="Send", device=active_device) or
                tap_node(nodes, partial=True, desc="Send", device=active_device)
            )
            if not sent:
                keyevent("KEYCODE_ENTER", device=active_device)
            time.sleep(1.5)

            ss_path = str(DOWNLOADS / f"instagram_dm_{username}.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "sent": True,
                "username": username,
                "message": message,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[dm] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "sent": False,
        "username": username,
        "message": message,
        "screenshot_path": None,
        "error": "DM failed after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_scroll(direction="up", count=3, device=None):
    """Scroll Instagram feed with natural swipes."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    try:
        for i in range(count):
            print(f"[scroll] Swipe {i+1}/{count} ({direction})", file=sys.stderr)
            natural_swipe(direction, device=active_device)
            natural_pause(1.0, 3.0)

        ss_path = str(DOWNLOADS / "instagram_scroll.png")
        screencap(ss_path, device=active_device)

        result = {
            "ok": True,
            "scrolled_count": count,
            "direction": direction,
            "screenshot_path": ss_path,
            "device": active_device or "none",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "scrolled_count": 0,
            "direction": direction,
            "screenshot_path": None,
            "device": active_device or "none",
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_scroll_reels(count=5, device=None):
    """Navigate to Reels tab and swipe through N reels with realistic watch pauses."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    try:
        # Navigate to Reels tab (504, 1540)
        print("[scroll-reels] Tapping Reels tab (504, 1540)", file=sys.stderr)
        adb("shell", "input", "tap", "504", "1540", device=active_device)
        time.sleep(2.0)

        for i in range(count):
            print(f"[scroll-reels] Reel {i+1}/{count} — watching...", file=sys.stderr)
            natural_pause(3.0, 8.0)  # simulate watching reel
            natural_swipe("up", device=active_device)

        ss_path = str(DOWNLOADS / "instagram_scroll_reels.png")
        screencap(ss_path, device=active_device)

        result = {
            "ok": True,
            "scrolled_count": count,
            "screenshot_path": ss_path,
            "device": active_device or "none",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "scrolled_count": 0,
            "screenshot_path": None,
            "device": active_device or "none",
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_browse(duration=30, like_chance=0.4, device=None):
    """Browse Instagram feed for `duration` seconds with human-like behaviour."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    posts_seen = 0
    liked_count = 0
    start_time = time.time()

    try:
        # Go to home feed
        tap(*COORDS["home"], device=active_device)
        time.sleep(2.0)

        while time.time() - start_time < duration:
            # Simulate reading/watching
            natural_pause(3.0, 8.0)
            posts_seen += 1

            # Maybe like
            if random.random() < like_chance:
                print("[browse] Double-tap to like post", file=sys.stderr)
                double_tap(360, 820, device=active_device)
                liked_count += 1
                time.sleep(0.5)

            # Check time before swiping
            if time.time() - start_time >= duration:
                break

            natural_swipe("up", device=active_device)

        ss_path = str(DOWNLOADS / "instagram_browse.png")
        screencap(ss_path, device=active_device)

        result = {
            "ok": True,
            "duration": duration,
            "posts_seen": posts_seen,
            "liked_count": liked_count,
            "screenshot_path": ss_path,
            "device": active_device or "none",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "duration": duration,
            "posts_seen": posts_seen,
            "liked_count": liked_count,
            "screenshot_path": None,
            "device": active_device or "none",
        }

    print(json.dumps(result, indent=2))
    return result


# ─── API Server ──────────────────────────────────────────────────────────────

def run_server(port=8769):
    try:
        import fastapi
        import uvicorn
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "-q"], check=True)
        import fastapi
        import uvicorn

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="autodroid-instagram-agent",
        version="2.0.0",
        description="Control Instagram Android app via ADB",
    )
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    # ── Request bodies ──
    class RegisterBody(BaseModel):
        username: str
        email: str
        password: str
        fullname: str
        phone: Optional[str] = None
        device: Optional[str] = None

    class LoginBody(BaseModel):
        username: str
        password: str
        device: Optional[str] = None

    class PostBody(BaseModel):
        media_path: str
        caption: Optional[str] = None
        device: Optional[str] = None

    class LikeBody(BaseModel):
        count: int = 1
        device: Optional[str] = None

    class CommentBody(BaseModel):
        text: str
        device: Optional[str] = None

    class FollowBody(BaseModel):
        username: str
        device: Optional[str] = None

    class DMBody(BaseModel):
        username: str
        message: str
        device: Optional[str] = None

    class BrowseBody(BaseModel):
        duration: int = 30
        like_chance: float = 0.4
        device: Optional[str] = None

    @app.get("/")
    def root():
        return {
            "service": "autodroid-instagram-agent",
            "version": "2.0.0",
            "endpoints": [
                "/status", "/open", "/feed", "/inbox", "/screenshot",
                "/register", "/login", "/post", "/like", "/comment", "/follow", "/dm",
                "/scroll", "/scroll-reels", "/browse",
            ],
        }

    @app.get("/status")
    def api_status(device: Optional[str] = None):
        return cmd_status(device=device)

    @app.post("/open")
    def api_open(device: Optional[str] = None):
        return cmd_open(device=device)

    @app.get("/feed")
    def api_feed(device: Optional[str] = None):
        return cmd_feed(device=device)

    @app.get("/inbox")
    def api_inbox(device: Optional[str] = None):
        return cmd_inbox(device=device)

    @app.get("/screenshot")
    def api_screenshot(device: Optional[str] = None, out: Optional[str] = None):
        return cmd_screenshot(device=device, out=out)

    @app.post("/register")
    def api_register(body: RegisterBody):
        return cmd_register(
            username=body.username, email=body.email, password=body.password,
            fullname=body.fullname, phone=body.phone, device=body.device,
        )

    @app.post("/login")
    def api_login(body: LoginBody):
        return cmd_login(username=body.username, password=body.password, device=body.device)

    @app.post("/post")
    def api_post(body: PostBody):
        return cmd_post(media_path=body.media_path, caption=body.caption, device=body.device)

    @app.post("/like")
    def api_like(body: LikeBody):
        return cmd_like(count=body.count, device=body.device)

    @app.post("/comment")
    def api_comment(body: CommentBody):
        return cmd_comment(text=body.text, device=body.device)

    @app.post("/follow")
    def api_follow(body: FollowBody):
        return cmd_follow(username=body.username, device=body.device)

    @app.post("/dm")
    def api_dm(body: DMBody):
        return cmd_dm(username=body.username, message=body.message, device=body.device)

    @app.get("/scroll")
    def api_scroll(direction: str = "up", count: int = 3, device: Optional[str] = None):
        return cmd_scroll(direction=direction, count=count, device=device)

    @app.get("/scroll-reels")
    def api_scroll_reels(count: int = 5, device: Optional[str] = None):
        return cmd_scroll_reels(count=count, device=device)

    @app.post("/browse")
    def api_browse(body: BrowseBody):
        return cmd_browse(duration=body.duration, like_chance=body.like_chance, device=body.device)

    print(f"[server] autodroid-instagram-agent v2.0 on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[server] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="autodroid-instagram-agent v2.0 — Instagram Android automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s open
  %(prog)s feed
  %(prog)s inbox
  %(prog)s screenshot --out /tmp/ig.png
  %(prog)s register --username myuser --email me@example.com --password P@ss123 --fullname "My Name"
  %(prog)s register --username myuser --email me@example.com --password P@ss123 --fullname "My Name" --phone +6281234567890
  %(prog)s login --username myuser --password P@ss123
  %(prog)s post --media /path/to/image.jpg --caption "Hello world"
  %(prog)s like --count 5
  %(prog)s comment --text "Nice photo!"
  %(prog)s follow --username targetuser
  %(prog)s dm --username targetuser --message "Hello!"
  %(prog)s server --port 8769
""",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Check app + device status")
    s.add_argument("--device", "-d")

    s = sub.add_parser("open", help="Launch Instagram, dismiss popups, screenshot")
    s.add_argument("--device", "-d")

    s = sub.add_parser("feed", help="Open Instagram feed, screenshot")
    s.add_argument("--device", "-d")

    s = sub.add_parser("inbox", help="Open Instagram DM inbox, screenshot")
    s.add_argument("--device", "-d")

    s = sub.add_parser("screenshot", help="Capture screenshot")
    s.add_argument("--device", "-d")
    s.add_argument("--out", "-o")

    s = sub.add_parser("register", help="Register a new Instagram account")
    s.add_argument("--username", "-u", required=True)
    s.add_argument("--email", "-e", required=True)
    s.add_argument("--password", "-p", required=True)
    s.add_argument("--fullname", "-n", required=True)
    s.add_argument("--phone")
    s.add_argument("--device", "-d")

    s = sub.add_parser("login", help="Login to Instagram")
    s.add_argument("--username", "-u", required=True)
    s.add_argument("--password", "-p", required=True)
    s.add_argument("--device", "-d")

    s = sub.add_parser("post", help="Post media to Instagram")
    s.add_argument("--media", "-m", required=True)
    s.add_argument("--caption", "-c")
    s.add_argument("--device", "-d")

    s = sub.add_parser("like", help="Like posts on feed")
    s.add_argument("--count", "-n", type=int, default=1)
    s.add_argument("--device", "-d")

    s = sub.add_parser("comment", help="Comment on current post")
    s.add_argument("--text", "-t", required=True)
    s.add_argument("--device", "-d")

    s = sub.add_parser("follow", help="Follow a user")
    s.add_argument("--username", "-u", required=True)
    s.add_argument("--device", "-d")

    s = sub.add_parser("dm", help="Send a direct message")
    s.add_argument("--username", "-u", required=True)
    s.add_argument("--message", "-m", required=True)
    s.add_argument("--device", "-d")

    s = sub.add_parser("scroll", help="Scroll Instagram feed with natural swipes")
    s.add_argument("--direction", default="up", choices=["up", "down"], help="Swipe direction (default: up)")
    s.add_argument("--count", "-n", type=int, default=3, help="Number of swipes (default: 3)")
    s.add_argument("--device", "-d")

    s = sub.add_parser("scroll-reels", help="Open Reels tab and scroll through reels")
    s.add_argument("--count", "-n", type=int, default=5, help="Number of reels to scroll (default: 5)")
    s.add_argument("--device", "-d")

    s = sub.add_parser("browse", help="Browse Instagram feed for N seconds")
    s.add_argument("--duration", type=int, default=30, help="Browse duration in seconds (default: 30)")
    s.add_argument("--like-chance", type=float, default=0.4, help="Probability to like each post (default: 0.4)")
    s.add_argument("--device", "-d")

    s = sub.add_parser("server", help="Start FastAPI server")
    s.add_argument("--port", type=int, default=8769)

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status(device=args.device)
    elif args.cmd == "open":
        cmd_open(device=args.device)
    elif args.cmd == "feed":
        cmd_feed(device=args.device)
    elif args.cmd == "inbox":
        cmd_inbox(device=args.device)
    elif args.cmd == "screenshot":
        cmd_screenshot(device=args.device, out=args.out)
    elif args.cmd == "register":
        cmd_register(
            username=args.username, email=args.email, password=args.password,
            fullname=args.fullname, phone=args.phone, device=args.device,
        )
    elif args.cmd == "login":
        cmd_login(username=args.username, password=args.password, device=args.device)
    elif args.cmd == "post":
        cmd_post(media_path=args.media, caption=args.caption, device=args.device)
    elif args.cmd == "like":
        cmd_like(count=args.count, device=args.device)
    elif args.cmd == "comment":
        cmd_comment(text=args.text, device=args.device)
    elif args.cmd == "follow":
        cmd_follow(username=args.username, device=args.device)
    elif args.cmd == "dm":
        cmd_dm(username=args.username, message=args.message, device=args.device)
    elif args.cmd == "scroll":
        cmd_scroll(direction=args.direction, count=args.count, device=args.device)
    elif args.cmd == "scroll-reels":
        cmd_scroll_reels(count=args.count, device=args.device)
    elif args.cmd == "browse":
        cmd_browse(duration=args.duration, like_chance=args.like_chance, device=args.device)
    elif args.cmd == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
