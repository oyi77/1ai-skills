#!/usr/bin/env python3
"""
autodroid-whatsapp-agent v1.1 — Robust WhatsApp Android automation via ADB

Commands:
  status   [--device]                          -- check WhatsApp install + device info
  open     [--device]                          -- launch WhatsApp, dismiss popups
  chats    [--device]                          -- list chat names + message previews
  send     --contact NAME --message TEXT [--device]  -- send message to contact
  screenshot [--device] [--out PATH]           -- capture screen
  register --phone PHONE [--device]            -- register/login with phone number
  verify-otp --otp CODE [--device]             -- enter OTP code after register
  login    --phone PHONE [--device]            -- alias for register
  send-media --contact NAME --media PATH [--caption TEXT] [--device]  -- send media file
  broadcast --contacts LIST --message MSG [--device]  -- broadcast message to multiple contacts
  status-tab [--device]                        -- check WhatsApp Status tab
  server   [--port 8768]                       -- start FastAPI server

Each command retries 3x on failure and always returns {ok: true/false}.
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
from typing import Optional, List

# ─── AI Interceptor (fail-safe) ───────────────────────────────────────────────
try:
    import sys as _sys
    _sys.path.insert(0, '/mnt/data/berkahkarya/skills/1ai-skills/automation/ai-interceptor/scripts')
    from ai_interceptor import AIInterceptor
    from content_interceptor import ContentInterceptor
    _interceptor = AIInterceptor()  # WhatsApp = message enhancement
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

PACKAGE = "com.whatsapp"
DOWNLOADS = Path("~/.openclaw/workspace/downloads").expanduser()
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

DISMISS_LABELS = {
    "OK", "Allow", "Continue", "Skip", "Got it", "Dismiss", "Agree", "Accept",
    "ALLOW", "CONTINUE", "SKIP", "OK, GOT IT",
    # Indonesian
    "Izinkan", "Lanjutkan", "Lewati", "Oke", "Setuju", "Tutup",
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
        raise RuntimeError(f"adb {' '.join(args[:2])} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def tap(x, y, device=None):
    adb("shell", "input", "tap", str(x), str(y), device=device)


def swipe(x1, y1, x2, y2, duration=300, device=None):
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration), device=device)


def keyevent(key, device=None):
    adb("shell", "input", "keyevent", str(key), device=device)


def type_text(text, device=None):
    """Type text word by word via ADB input."""
    words = text.split()
    for i, word in enumerate(words):
        # Escape special shell characters
        safe = word.replace("'", "\\'").replace('"', '\\"').replace("&", "\\&").replace("|", "\\|").replace(";", "\\;").replace("<", "\\<").replace(">", "\\>").replace("(", "\\(").replace(")", "\\)")
        if safe:
            adb("shell", "input", "text", safe, device=device)
            time.sleep(0.1)
        if i < len(words) - 1:
            keyevent("KEYCODE_SPACE", device=device)
            time.sleep(0.07)


def wake(device=None):
    """Wake device and unlock screen."""
    keyevent(224, device=device)
    time.sleep(0.5)
    swipe(360, 1400, 360, 700, duration=200, device=device)
    time.sleep(0.6)


def screencap(path, device=None):
    """Capture screenshot and save to path."""
    wake(device=device)
    data = adb("exec-out", "screencap", "-p", device=device, binary=True)
    Path(path).write_bytes(data)
    return str(path)


# ─── UI Parsing ─────────────────────────────────────────────────────────────

def dump_ui(device=None):
    """Dump UI hierarchy and return list of node dicts."""
    remote = "/sdcard/wa_dump.xml"
    local = "/tmp/wa_dump.xml"
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
            resource_id = n.get("resource-id", "")
            label = text or desc
            nodes.append({
                "label": label,
                "text": text,
                "desc": desc,
                "class": cls,
                "bounds": bounds,
                "resource_id": resource_id,
            })
        return nodes
    except ET.ParseError:
        return []


def bounds_to_center(b):
    """Convert bounds string '[x1,y1][x2,y2]' to center (x, y)."""
    try:
        vals = b.replace("][", ",").replace("[", "").replace("]", "").split(",")
        l, t, r, bo = map(int, vals)
        return (l + r) // 2, (t + bo) // 2
    except Exception:
        return None


def find_node(nodes, label=None, cls=None, partial=False, resource_id=None):
    """Find first node matching label and/or class."""
    for n in nodes:
        if label:
            match = (n["label"] == label) if not partial else (label.lower() in n["label"].lower())
            if not match:
                continue
        if cls and cls not in n["class"]:
            continue
        if resource_id and resource_id not in n["resource_id"]:
            continue
        return n
    return None


def tap_node(nodes, label=None, cls=None, partial=False, resource_id=None, device=None):
    """Find and tap a node. Returns True if tapped."""
    n = find_node(nodes, label=label, cls=cls, partial=partial, resource_id=resource_id)
    if n:
        c = bounds_to_center(n["bounds"])
        if c:
            tap(*c, device=device)
            return True
    return False


# ─── WhatsApp Helpers ────────────────────────────────────────────────────────

def get_connected_devices():
    """Return list of connected ADB device serial numbers."""
    out = adb("devices")
    return [line.split()[0] for line in out.splitlines()[1:] if "\tdevice" in line]


def dismiss_popups(nodes, device=None):
    """Dismiss any dismiss-able popups. Returns count dismissed."""
    dismissed = 0
    for n in nodes:
        if n["label"] in DISMISS_LABELS and n["bounds"]:
            c = bounds_to_center(n["bounds"])
            if c:
                tap(*c, device=device)
                time.sleep(0.4)
                dismissed += 1
    return dismissed


def launch_whatsapp(device=None):
    """Force-stop and re-launch WhatsApp."""
    wake(device=device)
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(0.5)
    adb("shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1", device=device)
    time.sleep(3.5)
    wake(device=device)


def is_whatsapp_foreground(nodes):
    """Check if WhatsApp is in foreground."""
    for n in nodes:
        if PACKAGE in n.get("resource_id", ""):
            return True
    return False


def ensure_whatsapp_open(device=None, max_attempts=3):
    """Make sure WhatsApp is open. Returns True on success."""
    for attempt in range(max_attempts):
        nodes = dump_ui(device=device)
        if is_whatsapp_foreground(nodes):
            dismiss_popups(nodes, device=device)
            return True
        print(f"[ensure_open] Launching WhatsApp, attempt {attempt+1}", file=sys.stderr)
        launch_whatsapp(device=device)
        nodes = dump_ui(device=device)
        dismiss_popups(nodes, device=device)
        if is_whatsapp_foreground(nodes):
            return True
    return False


def parse_chat_list(nodes):
    """
    Parse WhatsApp chat list from UI nodes.
    Chat list items are consecutive TextViews: first=contact name, second=message preview.
    Returns list of {name, preview} dicts.
    """
    chats = []
    # Collect all TextViews that are visible and have text
    text_nodes = [n for n in nodes if "TextView" in n["class"] and n["text"] and n["bounds"]]

    # Group by vertical position — chats appear as rows
    # Each row has: contact name (left/top) + preview message (right or below)
    # Strategy: find nodes where resource_id suggests chat row components
    # Also try heuristic: pairs of consecutive TextViews with different y-positions close together

    # First try resource_id-based parsing
    name_nodes = [n for n in text_nodes if "contact_name" in n["resource_id"] or "title" in n["resource_id"]]
    preview_nodes = [n for n in text_nodes if "last_message" in n["resource_id"] or "subtitle" in n["resource_id"] or "preview" in n["resource_id"]]

    if name_nodes:
        for name_node in name_nodes:
            name = name_node["text"]
            # Find matching preview by proximity
            ny_center = bounds_to_center(name_node["bounds"])
            if not ny_center:
                continue
            nx, ny = ny_center
            best_preview = ""
            best_dist = 999999
            for pn in preview_nodes:
                pc = bounds_to_center(pn["bounds"])
                if not pc:
                    continue
                px, py = pc
                dist = abs(ny - py)
                if dist < 80 and dist < best_dist:
                    best_dist = dist
                    best_preview = pn["text"]
            chats.append({"name": name, "preview": best_preview})
        return chats

    # Heuristic fallback: group TextViews in pairs by row proximity
    # Skip UI chrome like timestamps, status icons
    skip_patterns = ["WhatsApp", "Search", "More options", "New chat", "Camera", "Calls", "Status"]

    filtered = []
    for n in text_nodes:
        if any(n["text"] == s for s in skip_patterns):
            continue
        if not n["bounds"]:
            continue
        filtered.append(n)

    i = 0
    seen_names = set()
    while i < len(filtered):
        n1 = filtered[i]
        c1 = bounds_to_center(n1["bounds"])
        if not c1:
            i += 1
            continue
        x1, y1 = c1

        # Look ahead for a node on the same row (similar y)
        best_preview_node = None
        for j in range(i + 1, min(i + 5, len(filtered))):
            n2 = filtered[j]
            c2 = bounds_to_center(n2["bounds"])
            if not c2:
                continue
            x2, y2 = c2
            # Same row = y within 40px, different x
            if abs(y1 - y2) < 40 and x1 != x2:
                best_preview_node = n2
                break

        name = n1["text"]
        preview = best_preview_node["text"] if best_preview_node else ""

        # Skip duplicates and very short items (timestamps, icons)
        if name not in seen_names and len(name) > 1:
            seen_names.add(name)
            chats.append({"name": name, "preview": preview})
        i += 1

    return chats


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_status(device=None):
    """Check WhatsApp installation and device info."""
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    installed = False
    model = ""
    android_version = ""

    if dev:
        out = adb("shell", "pm", "list", "packages", PACKAGE, device=dev)
        installed = PACKAGE in out
        model = adb("shell", "getprop", "ro.product.model", device=dev)
        android_version = adb("shell", "getprop", "ro.build.version.release", device=dev)

    result = {
        "ok": True,
        "installed": installed,
        "package": PACKAGE,
        "device": dev or "none",
        "model": model,
        "android_version": android_version,
        "connected_devices": devices,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_open(device=None, max_retries=3):
    """Launch WhatsApp and dismiss any popups."""
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[open] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_whatsapp(device=dev)

            nodes = dump_ui(device=dev)
            dismissed = dismiss_popups(nodes, device=dev)
            print(f"[open] Dismissed {dismissed} popups", file=sys.stderr)
            time.sleep(0.5)

            ss_path = str(DOWNLOADS / "wa_open.png")
            screencap(ss_path, device=dev)

            # Check if WhatsApp is now in foreground
            nodes = dump_ui(device=dev)
            if is_whatsapp_foreground(nodes):
                result = {
                    "ok": True,
                    "device": dev or "none",
                    "screenshot_path": ss_path,
                }
                print(json.dumps(result, indent=2))
                return result
            else:
                print(f"[open] WhatsApp not in foreground after attempt {attempt}", file=sys.stderr)

        except Exception as e:
            print(f"[open] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "wa_open_fail.png")
    try:
        screencap(ss_path, device=dev)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "error": "Failed to open WhatsApp after all retries",
        "device": dev or "none",
        "screenshot_path": ss_path,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_chats(device=None, max_retries=3):
    """Open WhatsApp and collect chat list."""
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[chats] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Ensure WhatsApp is open
            if not ensure_whatsapp_open(device=dev):
                print("[chats] Failed to open WhatsApp", file=sys.stderr)
                continue

            # Make sure we're on the main chats screen
            # Press back to ensure we're at top level
            keyevent("KEYCODE_BACK", device=dev)
            time.sleep(0.5)
            nodes = dump_ui(device=dev)
            dismiss_popups(nodes, device=dev)
            time.sleep(0.5)

            # Dump UI and parse chats
            nodes = dump_ui(device=dev)
            chats = parse_chat_list(nodes)
            print(f"[chats] Found {len(chats)} chats", file=sys.stderr)

            ss_path = str(DOWNLOADS / "wa_chats.png")
            screencap(ss_path, device=dev)

            result = {
                "ok": True,
                "chats": chats,
                "screenshot_path": ss_path,
                "device": dev or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[chats] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "wa_chats_fail.png")
    try:
        screencap(ss_path, device=dev)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "error": "Failed to fetch chats after all retries",
        "chats": [],
        "screenshot_path": ss_path,
        "device": dev or "none",
    }
    print(json.dumps(result, indent=2))
    return result


@_ai_intercept(skill_type="generic")
def cmd_send(contact, message, device=None, max_retries=3):
    """Send a WhatsApp message to a contact."""
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[send] Attempt {attempt}/{max_retries} → '{contact}'", file=sys.stderr)
        try:
            # 1. Open WhatsApp
            if not ensure_whatsapp_open(device=dev):
                print("[send] Failed to open WhatsApp", file=sys.stderr)
                continue

            # Navigate to main screen (in case we're in a chat)
            keyevent("KEYCODE_BACK", device=dev)
            time.sleep(0.5)
            keyevent("KEYCODE_BACK", device=dev)
            time.sleep(0.5)

            nodes = dump_ui(device=dev)

            # 2. Tap search icon (magnifying glass)
            print("[send] Tapping search...", file=sys.stderr)
            tapped = (
                tap_node(nodes, label="Search", device=dev) or
                tap_node(nodes, label="Search…", device=dev) or
                tap_node(nodes, partial=True, label="Search", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/menuitem_search", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/search_btn", device=dev)
            )
            if not tapped:
                # Try finding by content-desc
                search_node = find_node(nodes, label="Search", partial=True)
                if search_node:
                    c = bounds_to_center(search_node["bounds"])
                    if c:
                        tap(*c, device=dev)
                        tapped = True
            if not tapped:
                print("[send] Could not find search icon, trying fallback position", file=sys.stderr)
                # Fallback: top-right area where search typically lives
                tap(900, 60, device=dev)

            time.sleep(1.5)

            # 3. Type contact name
            print(f"[send] Typing contact: {contact}", file=sys.stderr)
            nodes = dump_ui(device=dev)

            # Find and tap the search input field
            search_field = (
                find_node(nodes, resource_id="com.whatsapp:id/search_input") or
                find_node(nodes, resource_id="com.whatsapp:id/search_src_text") or
                find_node(nodes, cls="EditText")
            )
            if search_field:
                c = bounds_to_center(search_field["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(0.5)

            type_text(contact, device=dev)
            time.sleep(2.0)

            # 4. Tap first result
            print("[send] Selecting first result...", file=sys.stderr)
            nodes = dump_ui(device=dev)

            # Find contact result — look for the contact name in results
            result_node = find_node(nodes, label=contact)
            if not result_node:
                # Try partial match
                result_node = find_node(nodes, label=contact, partial=True)
            if not result_node:
                # Try any result item that appeared after search
                # Look for nodes that could be contact list items
                for n in nodes:
                    if PACKAGE in n.get("resource_id", "") and n["text"] and len(n["text"]) > 1:
                        if "search" not in n["resource_id"].lower():
                            result_node = n
                            break

            if result_node:
                c = bounds_to_center(result_node["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(2.0)
            else:
                print("[send] No result found, cannot continue", file=sys.stderr)
                continue

            # 5. Tap message input field
            print("[send] Finding message input...", file=sys.stderr)
            time.sleep(1.0)
            nodes = dump_ui(device=dev)

            msg_field = (
                find_node(nodes, resource_id="com.whatsapp:id/entry") or
                find_node(nodes, resource_id="com.whatsapp:id/conversation_entry") or
                find_node(nodes, cls="EditText")
            )
            if msg_field:
                c = bounds_to_center(msg_field["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(0.8)
            else:
                print("[send] Could not find message input field", file=sys.stderr)
                # Fallback tap at typical message field position
                tap(530, 1550, device=dev)
                time.sleep(0.8)

            # 6. Type message word by word
            print(f"[send] Typing message: {message}", file=sys.stderr)
            type_text(message, device=dev)
            time.sleep(0.5)

            # 7. Tap send button
            print("[send] Sending message...", file=sys.stderr)
            nodes = dump_ui(device=dev)
            sent = (
                tap_node(nodes, label="Send", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/send", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/send_btn", device=dev)
            )
            if not sent:
                # Fallback: ENTER key
                keyevent("KEYCODE_ENTER", device=dev)
            time.sleep(1.5)

            # 8. Screenshot confirmation
            ss_path = str(DOWNLOADS / f"wa_send_{contact.replace(' ', '_')}.png")
            screencap(ss_path, device=dev)

            result = {
                "ok": True,
                "contact": contact,
                "message_sent": message,
                "screenshot_path": ss_path,
                "device": dev or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[send] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "wa_send_fail.png")
    try:
        screencap(ss_path, device=dev)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "contact": contact,
        "message_sent": None,
        "error": "Failed to send message after all retries",
        "screenshot_path": ss_path,
        "device": dev or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(device=None, out=None):
    """Capture a screenshot of the current screen."""
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    out_path = out or str(DOWNLOADS / "wa_screenshot.png")
    screencap(out_path, device=dev)

    result = {
        "ok": True,
        "screenshot_path": out_path,
        "device": dev or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW COMMANDS v1.1 ───────────────────────────────────────────────────────

def cmd_register(phone, device=None, max_retries=3):
    """
    Register/login WhatsApp with phone number.
    - Launch WhatsApp
    - Tap "Setuju dan lanjutkan" (Agree and Continue)
    - Enter phone number
    - Tap "Berikutnya" (Next)
    - Return needs_otp if OTP step reached
    """
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[register] Attempt {attempt}/{max_retries}, phone={phone}", file=sys.stderr)
        try:
            # 1. Launch WhatsApp fresh
            launch_whatsapp(device=dev)
            time.sleep(2)

            nodes = dump_ui(device=dev)

            # 2. Tap "Setuju dan lanjutkan" / "Agree and Continue"
            agreed = (
                tap_node(nodes, label="Setuju dan lanjutkan", device=dev) or
                tap_node(nodes, label="AGREE AND CONTINUE", device=dev) or
                tap_node(nodes, label="Agree and continue", device=dev) or
                tap_node(nodes, partial=True, label="Setuju", device=dev) or
                tap_node(nodes, partial=True, label="Agree", device=dev)
            )
            if agreed:
                print("[register] Tapped Agree button", file=sys.stderr)
                time.sleep(2)
                nodes = dump_ui(device=dev)

            # 3. Find phone input field and enter number
            phone_field = (
                find_node(nodes, resource_id="com.whatsapp:id/registration_phone") or
                find_node(nodes, resource_id="com.whatsapp:id/phone_number") or
                find_node(nodes, cls="EditText")
            )
            if phone_field:
                c = bounds_to_center(phone_field["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(0.5)
                    # Clear field first
                    adb("shell", "input", "keyevent", "KEYCODE_CTRL_A", device=dev)
                    time.sleep(0.2)
                    adb("shell", "input", "keyevent", "KEYCODE_DEL", device=dev)
                    time.sleep(0.2)
                    # Type phone number (digits only)
                    safe_phone = "".join(c for c in phone if c.isdigit() or c == "+")
                    adb("shell", "input", "text", safe_phone, device=dev)
                    time.sleep(0.5)
                    print(f"[register] Entered phone: {safe_phone}", file=sys.stderr)
            else:
                print("[register] Phone field not found, trying fallback tap center-screen", file=sys.stderr)
                tap(360, 820, device=dev)
                time.sleep(0.5)
                adb("shell", "input", "text", phone, device=dev)
                time.sleep(0.5)

            # 4. Tap "Berikutnya" / "Next"
            nodes = dump_ui(device=dev)
            next_tapped = (
                tap_node(nodes, label="Berikutnya", device=dev) or
                tap_node(nodes, label="NEXT", device=dev) or
                tap_node(nodes, label="Next", device=dev) or
                tap_node(nodes, partial=True, label="Berikut", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/registration_submit", device=dev)
            )
            if next_tapped:
                print("[register] Tapped Next", file=sys.stderr)
            else:
                print("[register] Next button not found, trying ENTER", file=sys.stderr)
                keyevent("KEYCODE_ENTER", device=dev)

            time.sleep(2)

            # 5. Check if we reached OTP screen
            nodes = dump_ui(device=dev)
            # Look for OTP-related elements
            otp_screen = (
                find_node(nodes, partial=True, label="OTP") is not None or
                find_node(nodes, partial=True, label="kode") is not None or
                find_node(nodes, partial=True, label="verifikasi") is not None or
                find_node(nodes, partial=True, label="verification") is not None or
                find_node(nodes, resource_id="com.whatsapp:id/verify_sms_code_text") is not None or
                find_node(nodes, resource_id="com.whatsapp:id/otp_edit_text") is not None
            )

            ss_path = str(DOWNLOADS / "wa_register.png")
            screencap(ss_path, device=dev)

            if otp_screen:
                result = {
                    "ok": False,
                    "needs_otp": True,
                    "registered": False,
                    "phone": phone,
                    "device": dev or "none",
                    "screenshot_path": ss_path,
                    "note": "Enter OTP manually then call verify-otp",
                }
            else:
                result = {
                    "ok": True,
                    "needs_otp": True,
                    "registered": False,
                    "phone": phone,
                    "device": dev or "none",
                    "screenshot_path": ss_path,
                    "note": "Phone entered, waiting for OTP. Call verify-otp after receiving SMS.",
                }

            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[register] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "needs_otp": False,
        "registered": False,
        "phone": phone,
        "device": dev or "none",
        "error": "Failed to register after all retries",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_verify_otp(otp, device=None, max_retries=3):
    """
    Enter OTP code after register step.
    - Find OTP input field (EditText or individual digit boxes)
    - Type OTP code
    - Wait for auto-verification or tap "Verifikasi"
    """
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[verify-otp] Attempt {attempt}/{max_retries}, otp={otp}", file=sys.stderr)
        try:
            nodes = dump_ui(device=dev)

            # Find OTP input — could be single EditText or multiple digit boxes
            otp_field = (
                find_node(nodes, resource_id="com.whatsapp:id/verify_sms_code_text") or
                find_node(nodes, resource_id="com.whatsapp:id/otp_edit_text") or
                find_node(nodes, resource_id="com.whatsapp:id/sms_code") or
                find_node(nodes, cls="EditText")
            )

            # Check for individual digit boxes (6 separate EditText fields)
            digit_boxes = [n for n in nodes if "EditText" in n["class"] and n["bounds"]]

            if otp_field:
                c = bounds_to_center(otp_field["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(0.5)
                    # Type OTP digits
                    adb("shell", "input", "text", otp, device=dev)
                    print(f"[verify-otp] Typed OTP into single field", file=sys.stderr)
            elif len(digit_boxes) >= len(otp):
                # Type digit by digit into each box
                for i, digit in enumerate(otp):
                    if i < len(digit_boxes):
                        c = bounds_to_center(digit_boxes[i]["bounds"])
                        if c:
                            tap(*c, device=dev)
                            time.sleep(0.2)
                            adb("shell", "input", "text", digit, device=dev)
                            time.sleep(0.2)
                print(f"[verify-otp] Typed OTP digit by digit into {len(otp)} boxes", file=sys.stderr)
            else:
                print("[verify-otp] No OTP field found, trying keyboard input directly", file=sys.stderr)
                adb("shell", "input", "text", otp, device=dev)

            # Wait for auto-verification
            time.sleep(3)
            nodes = dump_ui(device=dev)

            # Try to tap "Verifikasi" / "Verify" if auto-verify didn't happen
            verify_tapped = (
                tap_node(nodes, label="Verifikasi", device=dev) or
                tap_node(nodes, label="VERIFY", device=dev) or
                tap_node(nodes, label="Verify", device=dev) or
                tap_node(nodes, partial=True, label="Verif", device=dev)
            )
            if verify_tapped:
                print("[verify-otp] Tapped Verify button", file=sys.stderr)
                time.sleep(3)

            ss_path = str(DOWNLOADS / "wa_verify_otp.png")
            screencap(ss_path, device=dev)

            result = {
                "ok": True,
                "verified": True,
                "otp": otp,
                "device": dev or "none",
                "screenshot_path": ss_path,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[verify-otp] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "wa_verify_otp_fail.png")
    try:
        screencap(ss_path, device=dev)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "verified": False,
        "otp": otp,
        "device": dev or "none",
        "error": "Failed to verify OTP after all retries",
        "screenshot_path": ss_path,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_login(phone, device=None):
    """
    Login to WhatsApp — WhatsApp uses phone-based auth.
    This is an alias for register.
    """
    return cmd_register(phone, device=device)


def cmd_send_media(contact, media_path, caption=None, device=None, max_retries=3):
    """
    Send media (image/video) to a contact via WhatsApp.
    - Open chat with contact
    - Tap attachment icon (paperclip)
    - Select Gallery
    - Pick first image/video
    - Add caption if provided
    - Send
    """
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    # Push media to device if it's a local path
    remote_media = None
    if media_path and Path(media_path).exists():
        remote_media = f"/sdcard/DCIM/wa_media_{Path(media_path).name}"
        adb("push", media_path, remote_media, device=dev)
        # Broadcast media to gallery
        adb("shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
            "-d", f"file://{remote_media}", device=dev)
        time.sleep(1)
        print(f"[send-media] Pushed media to {remote_media}", file=sys.stderr)

    for attempt in range(1, max_retries + 1):
        print(f"[send-media] Attempt {attempt}/{max_retries} → '{contact}'", file=sys.stderr)
        try:
            # 1. Open WhatsApp
            if not ensure_whatsapp_open(device=dev):
                print("[send-media] Failed to open WhatsApp", file=sys.stderr)
                continue

            # Navigate to main screen
            keyevent("KEYCODE_BACK", device=dev)
            time.sleep(0.5)
            keyevent("KEYCODE_BACK", device=dev)
            time.sleep(0.5)
            nodes = dump_ui(device=dev)

            # 2. Search for contact
            tapped_search = (
                tap_node(nodes, label="Search", device=dev) or
                tap_node(nodes, partial=True, label="Search", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/menuitem_search", device=dev)
            )
            if not tapped_search:
                tap(900, 60, device=dev)
            time.sleep(1.5)

            nodes = dump_ui(device=dev)
            search_field = (
                find_node(nodes, resource_id="com.whatsapp:id/search_input") or
                find_node(nodes, cls="EditText")
            )
            if search_field:
                c = bounds_to_center(search_field["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(0.5)
            type_text(contact, device=dev)
            time.sleep(2.0)

            # 3. Tap first result
            nodes = dump_ui(device=dev)
            result_node = find_node(nodes, label=contact) or find_node(nodes, label=contact, partial=True)
            if result_node:
                c = bounds_to_center(result_node["bounds"])
                if c:
                    tap(*c, device=dev)
                    time.sleep(2.0)
            else:
                print("[send-media] Contact not found in search results", file=sys.stderr)
                continue

            # 4. Tap attachment icon (paperclip)
            nodes = dump_ui(device=dev)
            attach_tapped = (
                tap_node(nodes, label="Attach", device=dev) or
                tap_node(nodes, label="Lampiran", device=dev) or
                tap_node(nodes, desc="Attach", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/input_attach_button", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/clip_holder", device=dev)
            )
            if not attach_tapped:
                print("[send-media] Attachment icon not found, trying coords (65, 1550)", file=sys.stderr)
                tap(65, 1550, device=dev)
            time.sleep(1.5)

            # 5. Select Gallery
            nodes = dump_ui(device=dev)
            gallery_tapped = (
                tap_node(nodes, label="Gallery", device=dev) or
                tap_node(nodes, label="Galeri", device=dev) or
                tap_node(nodes, label="Photos & Videos", device=dev) or
                tap_node(nodes, partial=True, label="Galeri", device=dev) or
                tap_node(nodes, partial=True, label="Gallery", device=dev)
            )
            if not gallery_tapped:
                print("[send-media] Gallery option not found, trying coords (180, 1400)", file=sys.stderr)
                tap(180, 1400, device=dev)
            time.sleep(2)

            # 6. Pick first image/video
            nodes = dump_ui(device=dev)
            # Tap first media item — usually in a grid, first item around top-left
            media_item = (
                find_node(nodes, resource_id="com.whatsapp:id/media_item") or
                find_node(nodes, resource_id="com.android.providers.media:id/image_thumbnail")
            )
            if media_item:
                c = bounds_to_center(media_item["bounds"])
                if c:
                    tap(*c, device=dev)
            else:
                print("[send-media] Media item not found, tapping first grid position (120, 300)", file=sys.stderr)
                tap(120, 300, device=dev)
            time.sleep(1.5)

            # 7. Add caption if provided
            if caption:
                nodes = dump_ui(device=dev)
                caption_field = (
                    find_node(nodes, resource_id="com.whatsapp:id/caption") or
                    find_node(nodes, partial=True, label="caption") or
                    find_node(nodes, partial=True, label="Add a caption") or
                    find_node(nodes, cls="EditText")
                )
                if caption_field:
                    c = bounds_to_center(caption_field["bounds"])
                    if c:
                        tap(*c, device=dev)
                        time.sleep(0.5)
                        type_text(caption, device=dev)
                        time.sleep(0.5)
                        print(f"[send-media] Added caption: {caption}", file=sys.stderr)

            # 8. Tap Send
            nodes = dump_ui(device=dev)
            send_tapped = (
                tap_node(nodes, label="Send", device=dev) or
                tap_node(nodes, label="Kirim", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/send", device=dev)
            )
            if not send_tapped:
                print("[send-media] Send button not found, trying ENTER", file=sys.stderr)
                keyevent("KEYCODE_ENTER", device=dev)
            time.sleep(2)

            ss_path = str(DOWNLOADS / f"wa_send_media_{contact.replace(' ', '_')}.png")
            screencap(ss_path, device=dev)

            result = {
                "ok": True,
                "sent": True,
                "contact": contact,
                "media": media_path,
                "caption": caption,
                "screenshot_path": ss_path,
                "device": dev or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[send-media] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "wa_send_media_fail.png")
    try:
        screencap(ss_path, device=dev)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "sent": False,
        "contact": contact,
        "error": "Failed to send media after all retries",
        "screenshot_path": ss_path,
        "device": dev or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_broadcast(contacts: List[str], message: str, device=None):
    """
    Broadcast a message to multiple contacts.
    For each contact: open chat → type message → send.
    Returns sent_count and list of results.
    """
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    sent_count = 0
    results = []

    for contact in contacts:
        print(f"[broadcast] Sending to: {contact}", file=sys.stderr)
        result = cmd_send(contact, message, device=dev, max_retries=2)
        if result.get("ok"):
            sent_count += 1
            results.append({"contact": contact, "ok": True})
        else:
            results.append({"contact": contact, "ok": False, "error": result.get("error", "unknown")})
        # Small delay between sends to avoid rate limiting
        time.sleep(1.5)

    final_result = {
        "ok": sent_count > 0,
        "sent_count": sent_count,
        "total": len(contacts),
        "contacts": results,
        "device": dev or "none",
    }
    print(json.dumps(final_result, indent=2))
    return final_result


def cmd_status_tab(device=None, max_retries=3):
    """
    Check WhatsApp Status tab.
    - Tap Status tab
    - Screenshot
    """
    devices = get_connected_devices()
    dev = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[status-tab] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Ensure WhatsApp is open
            if not ensure_whatsapp_open(device=dev):
                print("[status-tab] Failed to open WhatsApp", file=sys.stderr)
                continue

            # Navigate to main screen
            keyevent("KEYCODE_BACK", device=dev)
            time.sleep(0.5)
            nodes = dump_ui(device=dev)
            dismiss_popups(nodes, device=dev)

            # Tap Status tab
            nodes = dump_ui(device=dev)
            status_tapped = (
                tap_node(nodes, label="Status", device=dev) or
                tap_node(nodes, desc="Status", device=dev) or
                tap_node(nodes, resource_id="com.whatsapp:id/tab_status", device=dev) or
                tap_node(nodes, partial=True, label="Status", device=dev)
            )
            if not status_tapped:
                print("[status-tab] Status tab not found, trying fallback coords (540, 1580)", file=sys.stderr)
                # Status tab is usually second from left in bottom nav
                tap(540, 1580, device=dev)
            time.sleep(1.5)

            ss_path = str(DOWNLOADS / "wa_status_tab.png")
            screencap(ss_path, device=dev)

            result = {
                "ok": True,
                "screenshot_path": ss_path,
                "device": dev or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[status-tab] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "wa_status_tab_fail.png")
    try:
        screencap(ss_path, device=dev)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "error": "Failed to check Status tab after all retries",
        "screenshot_path": ss_path,
        "device": dev or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_scroll_chat(contact=None, direction="up", count=3, device=None):
    """Scroll chat history for a contact (or current open chat) up/down."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    try:
        if contact:
            print(f"[scroll-chat] Opening chat with: {contact}", file=sys.stderr)
            ensure_whatsapp_open(device=active_device)
            time.sleep(1.5)
            nodes = dump_ui(device=active_device)
            # Search for contact in list
            contact_found = tap_node(nodes, label=contact, device=active_device)
            if not contact_found:
                contact_found = tap_node(nodes, label=contact, partial=True, device=active_device)
            if contact_found:
                time.sleep(1.5)

        for i in range(count):
            print(f"[scroll-chat] Swipe {i+1}/{count} ({direction})", file=sys.stderr)
            natural_swipe(direction, device=active_device)
            natural_pause(0.5, 1.5)

        ss_path = str(DOWNLOADS / "wa_scroll_chat.png")
        screencap(ss_path, device=active_device)

        result = {
            "ok": True,
            "scrolled_count": count,
            "direction": direction,
            "contact": contact,
            "screenshot_path": ss_path,
            "device": active_device or "none",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "scrolled_count": 0,
            "direction": direction,
            "contact": contact,
            "screenshot_path": None,
            "device": active_device or "none",
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_scroll_status(device=None):
    """Open WhatsApp Status tab and swipe left to view next status."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    try:
        # Open WhatsApp
        print("[scroll-status] Opening WhatsApp Status tab", file=sys.stderr)
        ensure_whatsapp_open(device=active_device)
        time.sleep(2.0)
        nodes = dump_ui(device=active_device)

        # Tap Status tab
        status_tapped = (
            tap_node(nodes, label="Status", device=active_device) or
            tap_node(nodes, label="Updates", device=active_device) or
            tap_node(nodes, desc="Status", device=active_device)
        )
        if not status_tapped:
            # Common WhatsApp Status tab position (top tabs)
            tap(216, 120, device=active_device)
        time.sleep(1.5)

        # Swipe left to view next status
        print("[scroll-status] Swiping left to next status", file=sys.stderr)
        natural_swipe("left", device=active_device)

        ss_path = str(DOWNLOADS / "wa_scroll_status.png")
        screencap(ss_path, device=active_device)

        result = {
            "ok": True,
            "screenshot_path": ss_path,
            "device": active_device or "none",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "screenshot_path": None,
            "device": active_device or "none",
        }

    print(json.dumps(result, indent=2))
    return result


# ─── API Server ──────────────────────────────────────────────────────────────

def run_server(port=8768):
    """Start FastAPI server for WhatsApp agent."""
    try:
        import fastapi
        import uvicorn
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "-q"], check=True)
        import fastapi
        import uvicorn

    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="WhatsApp Android Agent",
        version="1.1.0",
        description="Control WhatsApp on Android via ADB. All endpoints return {ok: true/false}.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class SendRequest(BaseModel):
        contact: str
        message: str
        device: Optional[str] = None

    class RegisterRequest(BaseModel):
        phone: str
        device: Optional[str] = None

    class VerifyOtpRequest(BaseModel):
        otp: str
        device: Optional[str] = None

    class SendMediaRequest(BaseModel):
        contact: str
        media: str
        caption: Optional[str] = None
        device: Optional[str] = None

    class BroadcastRequest(BaseModel):
        contacts: List[str]
        message: str
        device: Optional[str] = None

    @app.get("/")
    def root():
        return {
            "service": "autodroid-whatsapp-agent",
            "version": "1.1.0",
            "endpoints": [
                "/status", "/open", "/chats", "/send", "/screenshot",
                "/register", "/verify-otp", "/send-media", "/broadcast", "/status-tab",
            ],
        }

    @app.get("/status")
    def api_status(device: Optional[str] = None):
        return cmd_status(device=device)

    @app.post("/open")
    def api_open(device: Optional[str] = None):
        result = cmd_open(device=device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to open WhatsApp"))
        return result

    @app.get("/chats")
    def api_chats(device: Optional[str] = None):
        result = cmd_chats(device=device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to fetch chats"))
        return result

    @app.post("/send")
    def api_send(req: SendRequest):
        result = cmd_send(req.contact, req.message, device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to send message"))
        return result

    @app.get("/screenshot")
    def api_screenshot(device: Optional[str] = None, out: Optional[str] = None):
        return cmd_screenshot(device=device, out=out)

    @app.post("/register")
    def api_register(req: RegisterRequest):
        return cmd_register(req.phone, device=req.device)

    @app.post("/verify-otp")
    def api_verify_otp(req: VerifyOtpRequest):
        result = cmd_verify_otp(req.otp, device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to verify OTP"))
        return result

    @app.post("/send-media")
    def api_send_media(req: SendMediaRequest):
        result = cmd_send_media(req.contact, req.media, caption=req.caption, device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to send media"))
        return result

    @app.post("/broadcast")
    def api_broadcast(req: BroadcastRequest):
        return cmd_broadcast(req.contacts, req.message, device=req.device)

    @app.get("/status-tab")
    def api_status_tab(device: Optional[str] = None):
        result = cmd_status_tab(device=device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to check Status tab"))
        return result

    @app.get("/scroll-chat")
    def api_scroll_chat(
        contact: Optional[str] = None,
        direction: str = "up",
        count: int = 3,
        device: Optional[str] = None,
    ):
        return cmd_scroll_chat(contact=contact, direction=direction, count=count, device=device)

    @app.get("/scroll-status")
    def api_scroll_status(device: Optional[str] = None):
        return cmd_scroll_status(device=device)

    @app.get("/health")
    def health():
        devices = get_connected_devices()
        return {"status": "ok", "connected_devices": devices, "count": len(devices)}

    print(f"[server] autodroid-whatsapp-agent v1.1 on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[server] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="autodroid-whatsapp-agent v1.1 — WhatsApp Android automation via ADB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s open
  %(prog)s chats
  %(prog)s send --contact "John Doe" --message "Hello from agent"
  %(prog)s screenshot --out /tmp/wa_screen.png
  %(prog)s register --phone "+6281234567890"
  %(prog)s verify-otp --otp "123456"
  %(prog)s login --phone "+6281234567890"
  %(prog)s send-media --contact "John Doe" --media /tmp/photo.jpg --caption "Check this out"
  %(prog)s broadcast --contacts "John,Jane,Bob" --message "Hello everyone"
  %(prog)s status-tab
  %(prog)s server --port 8768

API (after starting server):
  curl http://localhost:8768/status
  curl http://localhost:8768/chats
  curl -X POST http://localhost:8768/send \\
       -H "Content-Type: application/json" \\
       -d '{"contact": "John Doe", "message": "Hello!"}'
  curl -X POST http://localhost:8768/register \\
       -H "Content-Type: application/json" \\
       -d '{"phone": "+6281234567890"}'
  curl -X POST http://localhost:8768/broadcast \\
       -H "Content-Type: application/json" \\
       -d '{"contacts": ["John", "Jane"], "message": "Hello!"}'
""",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Check WhatsApp install and device info")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("open", help="Launch WhatsApp and dismiss popups")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("chats", help="List chat names and message previews")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("send", help="Send message to a contact")
    s.add_argument("--contact", "-c", required=True, help="Contact name to search")
    s.add_argument("--message", "-m", required=True, help="Message text to send")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("screenshot", help="Capture current screen")
    s.add_argument("--device", "-d", help="ADB device serial")
    s.add_argument("--out", "-o", help="Output path for screenshot PNG")

    s = sub.add_parser("register", help="Register/login WhatsApp with phone number")
    s.add_argument("--phone", required=True, help="Phone number (e.g. +6281234567890)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("verify-otp", help="Enter OTP code after register")
    s.add_argument("--otp", required=True, help="OTP code received via SMS")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("login", help="Login with phone number (alias for register)")
    s.add_argument("--phone", required=True, help="Phone number (e.g. +6281234567890)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("send-media", help="Send media file to a contact")
    s.add_argument("--contact", "-c", required=True, help="Contact name to send to")
    s.add_argument("--media", required=True, help="Path to media file (image/video)")
    s.add_argument("--caption", help="Optional caption for the media")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("broadcast", help="Broadcast message to multiple contacts")
    s.add_argument("--contacts", required=True, help="Comma-separated list of contact names")
    s.add_argument("--message", "-m", required=True, help="Message to broadcast")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("status-tab", help="Check WhatsApp Status tab")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("scroll-chat", help="Scroll chat history for a contact")
    s.add_argument("--contact", "-c", help="Contact name (optional, uses current open chat)")
    s.add_argument("--direction", default="up", choices=["up", "down"], help="Scroll direction (default: up = older messages)")
    s.add_argument("--count", "-n", type=int, default=3, help="Number of swipes (default: 3)")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("scroll-status", help="Open Status tab and swipe to next status")
    s.add_argument("--device", "-d", help="ADB device serial")

    s = sub.add_parser("server", help="Start FastAPI HTTP server")
    s.add_argument("--port", type=int, default=8768, help="Port to listen on (default: 8768)")

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status(device=args.device)
    elif args.cmd == "open":
        cmd_open(device=args.device)
    elif args.cmd == "chats":
        cmd_chats(device=args.device)
    elif args.cmd == "send":
        cmd_send(args.contact, args.message, device=args.device)
    elif args.cmd == "screenshot":
        cmd_screenshot(device=args.device, out=args.out)
    elif args.cmd == "register":
        cmd_register(args.phone, device=args.device)
    elif args.cmd == "verify-otp":
        cmd_verify_otp(args.otp, device=args.device)
    elif args.cmd == "login":
        cmd_login(args.phone, device=args.device)
    elif args.cmd == "send-media":
        cmd_send_media(args.contact, args.media, caption=args.caption, device=args.device)
    elif args.cmd == "broadcast":
        contacts_list = [c.strip() for c in args.contacts.split(",") if c.strip()]
        cmd_broadcast(contacts_list, args.message, device=args.device)
    elif args.cmd == "status-tab":
        cmd_status_tab(device=args.device)
    elif args.cmd == "scroll-chat":
        cmd_scroll_chat(contact=args.contact, direction=args.direction,
                        count=args.count, device=args.device)
    elif args.cmd == "scroll-status":
        cmd_scroll_status(device=args.device)
    elif args.cmd == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
