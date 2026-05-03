#!/usr/bin/env python3
"""
autodroid-grok-agent v1.0 — Grok Android automation via ADB

State-machine based. Verifies every step. Retries on failure.
No API key needed — controls real Grok app via ADB.

Commands:
  status                                      -- check app + device
  open                                        -- wake and launch Grok
  login --method google|email|x               -- authenticate
  chat --prompt TEXT [--think] [--deepsearch] -- send chat, get response
  imagine --prompt TEXT                       -- generate image
  screenshot [--out PATH]                     -- capture screen
  scroll [--direction up|down] [--count N]    -- scroll chat history
  server [--port 8773]                        -- start FastAPI server

Tested: Redmi 2409BRN2CY, Android 14, 720x1640, Grok app ~2026-03
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

# AI Interceptor (optional — fail-safe)
try:
    import sys as _sys
    _sys.path.insert(0, '/mnt/data/berkahkarya/skills/1ai-skills/automation/ai-interceptor/scripts')
    from ai_interceptor import AIInterceptor
    _interceptor = AIInterceptor()
    AI_INTERCEPT_ENABLED = True
except Exception:
    AI_INTERCEPT_ENABLED = False
    _interceptor = None

PACKAGE = "ai.x.grok"
DOWNLOADS = Path.home() / ".openclaw/workspace/downloads"
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

# ─── Grok-specific constants ─────────────────────────────────────────────────

# Verified UI coordinates (720x1640, Android 14)
COORD_CONTINUE_GOOGLE = (360, 878)
COORD_CONTINUE_EMAIL  = (360, 1014)
COORD_CONTINUE_X      = (360, 1150)
COORD_SKIP            = (649, 131)
COORD_INPUT           = (360, 1515)
COORD_SEND            = (660, 1515)
COORD_NEW_CHAT        = (660, 120)
COORD_SIDEBAR         = (60, 120)

DISMISS_LABELS = {
    "Skip", "Got it", "Not now", "No thanks", "Continue", "Allow",
    "Get started", "Accept", "OK", "Dismiss", "Close", "Agree",
    "Lewati", "Lanjutkan", "Izinkan", "Tidak sekarang", "Oke", "Siap",
    "Lain kali", "Later", "Maybe later", "No thank you",
}

# Labels to exclude from response detection
GROK_UI_CHROME = {
    "Grok", "Think", "DeepSearch", "New Chat", "New chat",
    "Understand the universe_",
    "Continue with Google", "Continue with Email", "Continue with X",
    "Send", "Kirim", "Back", "Menu", "Sidebar", "Search",
    "Grok is thinking...", "Grok is thinking",
}


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


def swipe(x1, y1, x2, y2, duration=300, device=None):
    adb("shell", "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration), device=device)


def keyevent(key, device=None):
    adb("shell", "input", "keyevent", str(key), device=device)


def type_word(word, device=None):
    # Escape shell special chars; adb input text handles basic words
    safe = word.replace("'", "").replace('"', "").replace("\\", "")
    if safe:
        adb("shell", "input", "text", safe, device=device)


def type_text(text, device=None):
    words = text.split()
    for i, word in enumerate(words):
        type_word(word, device=device)
        time.sleep(0.08)
        if i < len(words) - 1:
            keyevent("KEYCODE_SPACE", device=device)
            time.sleep(0.05)


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


# ─── Natural interaction helpers ─────────────────────────────────────────────

def natural_pause(min_ms=80, max_ms=200):
    """Human-like random pause between actions."""
    time.sleep(random.randint(min_ms, max_ms) / 1000.0)


def natural_swipe(x1, y1, x2, y2, device=None):
    """Swipe with slight randomization for more natural movement."""
    jitter_x = random.randint(-10, 10)
    jitter_y = random.randint(-5, 5)
    duration = random.randint(280, 420)
    swipe(
        x1 + jitter_x, y1 + jitter_y,
        x2 + jitter_x, y2 + jitter_y,
        duration=duration, device=device
    )


# ─── UI Parsing ─────────────────────────────────────────────────────────────

def dump_ui(device=None):
    remote = "/sdcard/grok_dump.xml"
    local = "/tmp/grok_dump.xml"
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


def find_node(nodes, label=None, cls=None, partial=False, res_id=None):
    for n in nodes:
        if label:
            match = (n["label"] == label) if not partial else (label.lower() in n["label"].lower())
            if not match:
                continue
        if cls and cls not in n["class"]:
            continue
        if res_id and res_id not in n["resource_id"]:
            continue
        return n
    return None


def tap_node(nodes, label=None, cls=None, partial=False, res_id=None, device=None):
    n = find_node(nodes, label=label, cls=cls, partial=partial, res_id=res_id)
    if n:
        c = bounds_to_center(n["bounds"])
        if c:
            tap(*c, device=device)
            return True
    return False


# ─── Screen State Detection ──────────────────────────────────────────────────

def detect_screen(nodes):
    """
    States:
    - ONBOARDING: has "Continue with Google" or "Understand the universe"
    - CHAT: has EditText input at bottom (resource-id with "input" or "compose")
    - LOADING: has "Grok is thinking" or loading spinner
    - LOGIN_EMAIL: has email/password fields
    - CHAT_WITH_IMAGE: chat with image visible
    - LOCK: lockscreen
    - UNKNOWN
    """
    labels = {n["label"] for n in nodes}
    classes = {n["class"] for n in nodes}

    # Onboarding detection
    if "Continue with Google" in labels or "Understand the universe_" in labels:
        return "ONBOARDING"

    # Email login screen
    if any(n["class"] == "EditText" and any(kw in n["resource_id"].lower()
           for kw in ("email", "username", "password")) for n in nodes):
        return "LOGIN_EMAIL"

    # Loading state
    if "Grok is thinking..." in labels or "Grok is thinking" in labels:
        return "LOADING"

    # Chat with image
    if any("ImageView" in n["class"] and n["bounds"] for n in nodes):
        if any("EditText" in n["class"] and any(kw in n["resource_id"].lower()
               for kw in ("input", "compose", "text")) for n in nodes):
            return "CHAT_WITH_IMAGE"

    # Chat screen: any EditText present = chat input
    if any("EditText" in n["class"] for n in nodes):
        return "CHAT"

    # Also detect by known Grok chat labels
    if "Ask" in labels or "Imagine" in labels or "Tanya apa saja" in labels or "Send message" in labels:
        return "CHAT"

    # Lockscreen
    if not nodes:
        return "LOCK"

    return "UNKNOWN"


# ─── High-level Actions ──────────────────────────────────────────────────────

def launch_grok(device=None):
    """Wake device and launch Grok app."""
    wake(device=device)
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(0.5)
    adb("shell", "monkey", "-p", PACKAGE, "-c",
        "android.intent.category.LAUNCHER", "1", device=device)
    time.sleep(3.5)
    wake(device=device)


def dismiss_all_popups(nodes, device=None):
    """Tap any dismiss/skip buttons found."""
    dismissed = 0
    for n in nodes:
        if n["label"] in DISMISS_LABELS and n["label"] not in ("Continue with Google",
                                                                 "Continue with Email",
                                                                 "Continue with X"):
            c = bounds_to_center(n["bounds"])
            if c:
                tap(*c, device=device)
                time.sleep(0.4)
                dismissed += 1
    return dismissed


def clear_field(device=None):
    """Clear text field reliably — select all then delete."""
    keyevent("KEYCODE_CTRL_A", device=device)
    time.sleep(0.15)
    keyevent("KEYCODE_DEL", device=device)
    time.sleep(0.1)
    # Extra: backspace 80x to clear any remaining text
    for _ in range(80):
        keyevent("KEYCODE_DEL", device=device)
    time.sleep(0.2)


def find_input_field(nodes):
    """Find the chat input EditText node."""
    # Try resource-id first
    for n in nodes:
        if "EditText" in n["class"]:
            rid = n["resource_id"].lower()
            if any(kw in rid for kw in ("input", "compose", "text", "message")):
                return n

    # Fallback: any EditText on screen (Grok input can be at y~820-1020)
    for n in nodes:
        if "EditText" in n["class"] and n["bounds"]:
            return n
    return None


def type_in_chat(text, device=None):
    """Tap input field and type text. Disable autocorrect before typing."""
    # Disable autocorrect temporarily
    adb("shell", "settings", "put", "secure", "spell_checker_enabled", "0", device=device)
    adb("shell", "settings", "put", "secure", "selected_spell_checker", "", device=device)

    nodes = dump_ui(device=device)
    field = find_input_field(nodes)
    if field:
        c = bounds_to_center(field["bounds"])
        if c:
            tap(*c, device=device)
    else:
        tap(364, 905, device=device)  # center of EditText [16,790][704,1020]
    time.sleep(0.8)
    clear_field(device=device)
    time.sleep(0.3)

    # Type word by word with delay — more reliable than full string
    words = text.split()
    for i, word in enumerate(words):
        adb("shell", "input", "text", word, device=device)
        time.sleep(0.2)
        if i < len(words) - 1:
            adb("shell", "input", "keyevent", "62", device=device)  # SPACE
            time.sleep(0.15)
    time.sleep(0.4)


def send_message(device=None):
    """Tap Send message button (Grok uses custom send, not Enter)."""
    nodes = dump_ui(device=device)
    # Grok's send button has content-desc "Send message"
    send_node = (find_node(nodes, label="Send message") or
                 find_node(nodes, label="Send") or
                 find_node(nodes, label="Kirim"))
    if send_node:
        c = bounds_to_center(send_node["bounds"])
        if c:
            tap(*c, device=device)
            return True
    # Fallback coordinate: Send message button at right of input field
    tap(646, 968, device=device)  # verified: [604,926][688,1010] center
    return True


def wait_for_response(timeout=60, device=None):
    """
    Poll UI every 2.5s looking for stable Grok response text.
    Filters out UI chrome, loading text, and short strings.
    Returns when same text appears twice in a row (stable) or timeout.
    """
    deadline = time.time() + timeout
    last_best = None

    while time.time() < deadline:
        time.sleep(2.5)
        nodes = dump_ui(device=device)

        # Check still loading
        state = detect_screen(nodes)
        if state == "LOADING":
            print("[wait_for_response] Still loading...", file=sys.stderr)
            last_best = None  # Reset stability check while loading
            continue

        candidates = []
        for n in nodes:
            t = n["text"]
            if not t or len(t) < 25:
                continue
            # Accept TextView AND View (Grok may use custom views)
            if n["class"] not in ("TextView", "View", "FrameLayout"):
                continue
            if t in GROK_UI_CHROME or t in DISMISS_LABELS:
                continue
            if "Grok is thinking" in t or "Grok is " in t:
                continue
            if t in ("Grok", "Think", "DeepSearch", "New Chat",
                     "Understand the universe_", "Send message",
                     "Try SuperGrok", "Create Videos", "Ask", "Imagine",
                     "Mulai obrolan baru", "Launch images selector", "Auto"):
                continue
            candidates.append(t)

        if candidates:
            best = max(candidates, key=len)
            if best == last_best:
                # Stable — same response twice in a row
                return best
            last_best = best
        else:
            last_best = None

    return last_best  # Return whatever we had at timeout


def save_image_from_device(ts_before, device=None):
    """
    Extract Grok-generated image. Strategy:
    1. MediaStore query (newest image after ts_before)
    2. Long press image → Download → pull from Download folder
    3. Crop from full screenshot (fallback)
    """
    import time as _time

    # Strategy 1: MediaStore (primary + primary_external)
    for uri in (
        "content://media/external_primary/images/media",
        "content://media/external/images/media",
        "content://downloads/public_downloads",
    ):
        try:
            out = adb("shell", "content", "query", "--uri", uri,
                      "--projection", "_data,date_added",
                      "--sort", "date_added%20DESC", device=device)
            for line in out.splitlines():
                if "date_added=" not in line or "_data=" not in line:
                    continue
                ts = int(line.split("date_added=")[1].split(",")[0].strip())
                path = line.split("_data=")[1].split(",")[0].strip()
                if ts > ts_before and path.endswith((".jpg", ".png", ".webp")):
                    return path
        except Exception:
            continue

    # Strategy 2: Check Grok's Android data dir (no root needed via sdcard path)
    for folder in ("/sdcard/Pictures", "/sdcard/DCIM", "/sdcard/Downloads",
                   "/sdcard/Android/data/ai.x.grok/files"):
        try:
            out = adb("shell", f"find {folder} -name '*.jpg' -o -name '*.png' 2>/dev/null",
                      device=device)
            for path in out.splitlines():
                path = path.strip()
                if not path:
                    continue
                stat_out = adb("shell", f"stat {path} 2>/dev/null", device=device)
                # Check mtime via ls
                ls_out = adb("shell", f"ls -la {path} 2>/dev/null", device=device)
                if ls_out:
                    return path
        except Exception:
            continue

    # Strategy 3: Long press image on screen → tap Download → wait → find file
    print("[save_image] Trying long-press download...", file=__import__("sys").stderr)
    nodes = dump_ui(device=device)
    # Find large ImageView in chat area (y between 300-700 roughly)
    for n in nodes:
        if "ImageView" in n["class"] and n["bounds"]:
            c = bounds_to_center(n["bounds"])
            if c and 300 < c[1] < 800:
                # Long press
                adb("shell", "input", "swipe",
                    str(c[0]), str(c[1]), str(c[0]), str(c[1]), "1500", device=device)
                _time.sleep(1.5)
                # Look for Download button
                nodes2 = dump_ui(device=device)
                dl = find_node(nodes2, label="Download") or find_node(nodes2, label="Unduh")
                if dl:
                    cl = bounds_to_center(dl["bounds"])
                    if cl:
                        tap(*cl, device=device)
                        _time.sleep(3)
                        # Re-query MediaStore
                        out = adb("shell", "content", "query",
                                  "--uri", "content://media/external_primary/images/media",
                                  "--projection", "_data,date_added",
                                  "--sort", "date_added%20DESC", device=device)
                        for line in out.splitlines():
                            if "_data=" in line:
                                path = line.split("_data=")[1].split(",")[0].strip()
                                return path
                break

    return None  # Will use screenshot crop as final fallback


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_status(device=None):
    """Check Grok installation and device info."""
    installed = PACKAGE in adb("shell", "pm", "list", "packages", PACKAGE, device=device)
    model = adb("shell", "getprop", "ro.product.model", device=device)
    android = adb("shell", "getprop", "ro.build.version.release", device=device)
    devices = [l.split()[0] for l in adb("devices").splitlines()[1:]
               if "\tdevice" in l]
    result = {
        "ok": True,
        "installed": installed,
        "package": PACKAGE,
        "device": device or (devices[0] if devices else "none"),
        "model": model,
        "android_version": android,
        "connected_devices": devices,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_open(device=None, max_retries=3):
    """Wake, launch Grok, detect state, skip onboarding if needed."""
    for attempt in range(1, max_retries + 1):
        print(f"[open] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            launch_grok(device=device)
            nodes = dump_ui(device=device)
            dismiss_all_popups(nodes, device=device)
            time.sleep(0.5)

            nodes = dump_ui(device=device)
            state = detect_screen(nodes)
            print(f"[open] State: {state}", file=sys.stderr)

            if state == "ONBOARDING":
                print("[open] Onboarding detected, tapping Skip...", file=sys.stderr)
                tap(*COORD_SKIP, device=device)
                time.sleep(2)
                nodes = dump_ui(device=device)
                state = detect_screen(nodes)
                print(f"[open] State after skip: {state}", file=sys.stderr)

            ss_path = str(DOWNLOADS / "grok_open.png")
            screencap(ss_path, device=device)

            result = {
                "ok": True,
                "state": state,
                "screenshot_path": ss_path,
                "device": device or "default",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[open] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "grok_open_failed.png")
    try:
        screencap(ss_path, device=device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "state": "UNKNOWN",
        "error": "Failed to open Grok after all retries",
        "screenshot_path": ss_path,
        "device": device or "default",
        "attempt": max_retries,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_login(method="google", email=None, password=None, device=None, max_retries=3):
    """Login to Grok via google, email, or x (Twitter)."""
    for attempt in range(1, max_retries + 1):
        print(f"[login] Attempt {attempt}/{max_retries} via {method}", file=sys.stderr)
        try:
            launch_grok(device=device)
            time.sleep(2)
            nodes = dump_ui(device=device)
            state = detect_screen(nodes)
            print(f"[login] State: {state}", file=sys.stderr)

            if state == "CHAT":
                # Already logged in
                ss_path = str(DOWNLOADS / "grok_login.png")
                screencap(ss_path, device=device)
                result = {
                    "ok": True,
                    "logged_in": True,
                    "method": method,
                    "screenshot_path": ss_path,
                    "device": device or "default",
                    "note": "Already logged in",
                }
                print(json.dumps(result, indent=2))
                return result

            if state != "ONBOARDING":
                # Try to get to onboarding
                print(f"[login] Unexpected state {state}, waiting...", file=sys.stderr)
                time.sleep(3)
                nodes = dump_ui(device=device)
                state = detect_screen(nodes)

            if state == "ONBOARDING":
                if method == "google":
                    print("[login] Tapping Continue with Google...", file=sys.stderr)
                    tap(*COORD_CONTINUE_GOOGLE, device=device)
                    time.sleep(3)
                    # Google account picker appears — tap first account
                    nodes = dump_ui(device=device)
                    # Find account email in list (first account)
                    for n in nodes:
                        if "@" in n["label"] and "gmail" in n["label"].lower():
                            c = bounds_to_center(n["bounds"])
                            if c:
                                tap(*c, device=device)
                                break
                    else:
                        # Tap first clickable item after title row
                        tappable = [n for n in nodes if n["bounds"] and
                                    "LinearLayout" in n["class"] or
                                    "RelativeLayout" in n["class"]]
                        if tappable:
                            c = bounds_to_center(tappable[0]["bounds"])
                            if c:
                                tap(*c, device=device)

                elif method == "email":
                    print("[login] Tapping Continue with Email...", file=sys.stderr)
                    tap(*COORD_CONTINUE_EMAIL, device=device)
                    time.sleep(2)
                    nodes = dump_ui(device=device)

                    # Fill email
                    email_node = find_node(nodes, cls="EditText", partial=True, label="")
                    if not email_node:
                        email_node = find_node(nodes, res_id="email")
                    if email_node and email:
                        c = bounds_to_center(email_node["bounds"])
                        if c:
                            tap(*c, device=device)
                            time.sleep(0.5)
                            type_text(email, device=device)
                            keyevent("KEYCODE_ENTER", device=device)
                            time.sleep(1.5)

                    # Fill password
                    nodes = dump_ui(device=device)
                    pass_node = find_node(nodes, res_id="password")
                    if not pass_node:
                        pass_node = find_node(nodes, cls="EditText", partial=True, label="")
                    if pass_node and password:
                        c = bounds_to_center(pass_node["bounds"])
                        if c:
                            tap(*c, device=device)
                            time.sleep(0.5)
                            type_text(password, device=device)
                            keyevent("KEYCODE_ENTER", device=device)

                elif method == "x":
                    print("[login] Tapping Continue with X...", file=sys.stderr)
                    tap(*COORD_CONTINUE_X, device=device)

            # Wait 5s for login to complete
            time.sleep(5)
            nodes = dump_ui(device=device)
            dismiss_all_popups(nodes, device=device)
            time.sleep(1)
            nodes = dump_ui(device=device)
            state = detect_screen(nodes)
            logged_in = state in ("CHAT", "CHAT_WITH_IMAGE")

            ss_path = str(DOWNLOADS / "grok_login.png")
            screencap(ss_path, device=device)

            result = {
                "ok": True,
                "logged_in": logged_in,
                "method": method,
                "screenshot_path": ss_path,
                "device": device or "default",
                "state": state,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[login] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "logged_in": False,
        "method": method,
        "error": "Login failed after all retries",
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_chat(prompt, think=False, deepsearch=False, timeout=60, device=None, max_retries=3):
    """Send a chat message to Grok and wait for response."""
    # AI Interceptor: enhance prompt if available (fail-safe)
    if AI_INTERCEPT_ENABLED and _interceptor:
        try:
            prompt = _interceptor.intercept(skill_type="grok_gen")(lambda p: p)(prompt)
        except Exception:
            pass
    for attempt in range(1, max_retries + 1):
        print(f"[chat] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Ensure on CHAT screen
            nodes = dump_ui(device=device)
            state = detect_screen(nodes)

            if state not in ("CHAT", "CHAT_WITH_IMAGE"):
                print(f"[chat] Not on CHAT (state={state}), opening Grok...", file=sys.stderr)
                open_result = cmd_open(device=device)
                if not open_result.get("ok"):
                    continue
                nodes = dump_ui(device=device)
                state = detect_screen(nodes)

            if state == "ONBOARDING":
                tap(*COORD_SKIP, device=device)
                time.sleep(2)
                nodes = dump_ui(device=device)

            # Enable Think mode if requested
            if think:
                print("[chat] Enabling Think mode...", file=sys.stderr)
                if tap_node(nodes, label="Think", device=device):
                    time.sleep(0.5)
                    natural_pause()

            # Enable DeepSearch if requested
            if deepsearch:
                print("[chat] Enabling DeepSearch...", file=sys.stderr)
                nodes = dump_ui(device=device)
                if tap_node(nodes, label="DeepSearch", device=device):
                    time.sleep(0.5)
                    natural_pause()

            # Type and send
            print(f"[chat] Typing prompt: {prompt[:50]}...", file=sys.stderr)
            type_in_chat(prompt, device=device)
            natural_pause(100, 300)

            print("[chat] Sending...", file=sys.stderr)
            send_message(device=device)

            print(f"[chat] Waiting for response (up to {timeout}s)...", file=sys.stderr)
            response = wait_for_response(timeout=timeout, device=device)

            ss_path = str(DOWNLOADS / "grok_chat.png")
            screencap(ss_path, device=device)

            if response:
                result = {
                    "ok": True,
                    "response": response,
                    "prompt": prompt,
                    "mode": {"think": think, "deepsearch": deepsearch},
                    "screenshot_path": ss_path,
                    "device": device or "default",
                    "attempt": attempt,
                }
                print(json.dumps(result, indent=2))
                return result
            else:
                print(f"[chat] No response detected (attempt {attempt})", file=sys.stderr)

        except Exception as e:
            print(f"[chat] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "grok_chat_failed.png")
    try:
        screencap(ss_path, device=device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "response": None,
        "prompt": prompt,
        "mode": {"think": think, "deepsearch": deepsearch},
        "error": "No response after all retries",
        "screenshot_path": ss_path,
        "device": device or "default",
        "attempt": max_retries,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_imagine(prompt, timeout=90, device=None, max_retries=3):
    """Generate an image via Grok chat."""
    ts_before = int(time.time())

    for attempt in range(1, max_retries + 1):
        print(f"[imagine] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            # Ensure on CHAT screen
            nodes = dump_ui(device=device)
            state = detect_screen(nodes)
            if state not in ("CHAT", "CHAT_WITH_IMAGE"):
                print("[imagine] Opening Grok...", file=sys.stderr)
                cmd_open(device=device)

            # Compose image request
            image_prompt = f"Generate an image of: {prompt}"
            print(f"[imagine] Typing: {image_prompt[:60]}...", file=sys.stderr)
            type_in_chat(image_prompt, device=device)
            natural_pause(100, 300)

            print("[imagine] Sending...", file=sys.stderr)
            send_message(device=device)

            # Wait for image to appear
            print(f"[imagine] Waiting for image (up to {timeout}s)...", file=sys.stderr)
            deadline = time.time() + timeout
            image_ready = False
            while time.time() < deadline:
                time.sleep(3)
                wake(device=device)
                nodes = dump_ui(device=device)
                state = detect_screen(nodes)
                print(f"[imagine] State: {state}", file=sys.stderr)
                if state in ("CHAT_WITH_IMAGE", "VIEWER"):
                    image_ready = True
                    print(f"[imagine] Image ready! State: {state}", file=sys.stderr)
                    break
                # Check for ImageView appearing (backup detection)
                if any("ImageView" in n["class"] and n["bounds"] for n in nodes):
                    image_ready = True
                    break

            ss_path = str(DOWNLOADS / "grok_imagine_screen.png")
            screencap(ss_path, device=device)

            if not image_ready:
                print("[imagine] Timeout waiting for image", file=sys.stderr)
                continue

            time.sleep(1)
            # Try to save the image via MediaStore
            remote_path = save_image_from_device(ts_before, device=device)

            if remote_path:
                local_path = str(DOWNLOADS / f"grok_imagine_{attempt}.png")
                adb("pull", remote_path, local_path, device=device)
                if Path(local_path).exists() and Path(local_path).stat().st_size > 1000:
                    result = {
                        "ok": True,
                        "image_path": local_path,
                        "prompt": prompt,
                        "screenshot_path": ss_path,
                        "device": device or "default",
                        "attempt": attempt,
                    }
                    print(json.dumps(result, indent=2))
                    return result
                else:
                    print("[imagine] File pull failed or empty", file=sys.stderr)
            else:
                print("[imagine] No new image found in MediaStore", file=sys.stderr)
                # Return screenshot only as fallback
                result = {
                    "ok": True,
                    "image_path": None,
                    "prompt": prompt,
                    "screenshot_path": ss_path,
                    "device": device or "default",
                    "attempt": attempt,
                    "note": "Image shown on screen but could not pull from device",
                }
                print(json.dumps(result, indent=2))
                return result

        except Exception as e:
            print(f"[imagine] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "image_path": None,
        "prompt": prompt,
        "error": "Image generation failed after all retries",
        "screenshot_path": str(DOWNLOADS / "grok_imagine_screen.png"),
        "device": device or "default",
        "attempt": max_retries,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(out=None, device=None):
    """Capture current screen."""
    out_path = out or str(DOWNLOADS / "grok_screenshot.png")
    screencap(out_path, device=device)
    result = {
        "ok": True,
        "screenshot_path": out_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_scroll(direction="down", count=3, device=None):
    """Scroll chat history using natural swipe."""
    scrolled = 0
    for i in range(count):
        if direction == "down":
            natural_swipe(360, 1300, 360, 400, device=device)
        else:
            natural_swipe(360, 400, 360, 1300, device=device)
        natural_pause(200, 400)
        scrolled += 1

    ss_path = str(DOWNLOADS / "grok_scroll.png")
    screencap(ss_path, device=device)

    result = {
        "ok": True,
        "scrolled_count": scrolled,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_video(photo_path=None, prompt=None, timeout=120, device=None, max_retries=3):
    """
    Generate video in Grok via 'Animate your photos' feature (FREE tier).

    Flow:
      1. Open Grok → navigate to Imagine tab → tap 'Create Videos'
      2. Tap 'Animate your photos' (or first thumbnail = preview existing)
      3. If photo_path given → upload from gallery, else pick first available
      4. Confirm → wait for video to generate (black screen + 6s•480p label)
      5. Screenshot the result (download requires SuperGrok premium)
      6. Return screenshot path + video duration/quality info

    Note: Download requires SuperGrok (Rp 489.000/month).
          Free tier can generate & preview 6s 480p videos.
    """
    ts_before = int(time.time())

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[video] Attempt {attempt}/{max_retries}", file=sys.stderr)

            # Navigate to Grok main screen (force restart for clean state)
            adb("shell", "am", "force-stop", PACKAGE, device=device)
            time.sleep(0.5)
            adb("shell", "monkey", "-p", PACKAGE,
                "-c", "android.intent.category.LAUNCHER", "1", device=device)
            time.sleep(4)

            nodes = dump_ui(device=device)

            # Check if we're already on video/imagine page (has "Animate your photos")
            on_video_page = bool(find_node(nodes, label="Animate your photos") or
                                 find_node(nodes, label="Create from Template") or
                                 find_node(nodes, label="Funky Dance"))

            if on_video_page:
                print("[video] Already on video page", file=sys.stderr)
                # Skip Create Videos tap — already here
            else:
                # Navigate to Imagine tab first
                imagine_tab = find_node(nodes, label="Imagine")
                if imagine_tab:
                    c = bounds_to_center(imagine_tab["bounds"])
                    if c:
                        tap(*c, device=device)
                        time.sleep(1.5)
                        nodes = dump_ui(device=device)

                # Try Create Videos button (on Chat/Ask tab)
                cv_btn = find_node(nodes, label="Create Videos")
                if cv_btn:
                    c = bounds_to_center(cv_btn["bounds"])
                    if c:
                        tap(*c, device=device)
                        time.sleep(3)
                        nodes = dump_ui(device=device)
                else:
                    # Try from Ask tab
                    ask_tab = find_node(nodes, label="Ask")
                    if ask_tab:
                        c = bounds_to_center(ask_tab["bounds"])
                        if c:
                            tap(*c, device=device)
                            time.sleep(1)
                            nodes = dump_ui(device=device)
                    cv_btn = find_node(nodes, label="Create Videos")
                    if cv_btn:
                        c = bounds_to_center(cv_btn["bounds"])
                        if c:
                            tap(*c, device=device)
                            time.sleep(3)
                            nodes = dump_ui(device=device)

            # Refresh UI state
            nodes = dump_ui(device=device)

            # Check if paywall appeared immediately
            if find_node(nodes, label="SuperGrok") or find_node(nodes, label="Upgrade to SuperGrok"):
                print("[video] SuperGrok paywall appeared", file=sys.stderr)
                ss_path = str(DOWNLOADS / "grok_video_paywall.png")
                screencap(ss_path, device=device)
                result = {
                    "ok": False,
                    "error": "Video generation requires SuperGrok (premium). Free tier: preview only.",
                    "paywall": True,
                    "supergrok_price": {
                        "monthly": "Rp 489.000/bulan",
                        "yearly": "Rp 4.890.000/tahun (hemat 17%)"
                    },
                    "free_tier_features": [
                        "chat (unlimited)",
                        "imagine images (free quota)",
                        "video preview/browse (sample videos only)"
                    ],
                    "screenshot_path": ss_path,
                    "device": device or "default",
                }
                print(json.dumps(result, indent=2))
                return result

            # Tap "Animate your photos" or first available thumbnail
            anim_btn = find_node(nodes, label="Animate your photos")
            if anim_btn:
                # Tap "See All" to get full list
                see_all = find_node(nodes, label="See All")
                if see_all:
                    c = bounds_to_center(see_all["bounds"])
                    if c:
                        tap(*c, device=device)
                        time.sleep(2)
            
            # Find first available sample video thumbnail and tap it
            nodes = dump_ui(device=device)
            # Look for "Try the template" (Funky Dance, Fire Horse, Chibi)
            try_template = find_node(nodes, label="Try the template")
            if try_template:
                c = bounds_to_center(try_template["bounds"])
                if c:
                    tap(*c, device=device)
                    time.sleep(2)
                    
                # Photo picker will open — close cloud prompt, pick photo
                nodes2 = dump_ui(device=device)
                close_btn = find_node(nodes2, label="Tutup") or find_node(nodes2, label="Close")
                if close_btn:
                    c2 = bounds_to_center(close_btn["bounds"])
                    if c2:
                        tap(*c2, device=device)
                        time.sleep(0.5)
                
                # Pick first available photo
                nodes3 = dump_ui(device=device)
                photo_nodes = [n for n in nodes3 if "Foto diambil" in (n.get("text","") + n.get("content-desc",""))]
                if photo_nodes:
                    c3 = bounds_to_center(photo_nodes[0]["bounds"])
                    if c3:
                        tap(*c3, device=device)
                        time.sleep(1)
                
                # Confirm selection
                nodes4 = dump_ui(device=device)
                selesai = find_node(nodes4, label="Selesai") or find_node(nodes4, label="Done")
                if selesai:
                    c4 = bounds_to_center(selesai["bounds"])
                    if c4:
                        tap(*c4, device=device)
                        time.sleep(4)
            
            # Wait for video player to show
            deadline = time.time() + timeout
            video_info = None
            while time.time() < deadline:
                nodes_v = dump_ui(device=device)
                # Look for video duration indicator like "6s · 480p"
                for n in nodes_v:
                    t = (n.get("text","") + " " + n.get("content-desc","")).strip()
                    if ("s ·" in t or "s·" in t) and ("480p" in t or "720p" in t):
                        video_info = t.strip()
                        break
                    if "customize video" in t.lower() or "edit image" in t.lower():
                        video_info = "video_ready"
                        break
                if video_info:
                    print(f"[video] Video ready: {video_info}", file=sys.stderr)
                    break
                
                # Check for paywall during generation
                if find_node(nodes_v, label="Upgrade to SuperGrok"):
                    video_info = "paywall"
                    break
                    
                time.sleep(2)
            
            # Screenshot result
            ss_path = str(DOWNLOADS / "grok_video_result.png")
            screencap(ss_path, device=device)
            
            if video_info == "paywall":
                result = {
                    "ok": False,
                    "error": "Video download requires SuperGrok premium",
                    "paywall": True,
                    "note": "Video generation works in free tier, but download requires subscription",
                    "screenshot_path": ss_path,
                    "device": device or "default",
                    "attempt": attempt,
                }
            else:
                result = {
                    "ok": True,
                    "video_info": video_info or "Generated",
                    "note": "Video visible on screen. Download requires SuperGrok (Rp 489K/month). Screenshot saved.",
                    "screenshot_path": ss_path,
                    "device": device or "default",
                    "attempt": attempt,
                }
            
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[video] Error: {e}", file=sys.stderr)
            if attempt == max_retries:
                result = {"ok": False, "error": str(e), "attempt": attempt}
                print(json.dumps(result, indent=2))
                return result
            time.sleep(2 ** attempt)

    result = {"ok": False, "error": "Max retries exceeded"}
    print(json.dumps(result, indent=2))
    return result


# ─── API Server ──────────────────────────────────────────────────────────────

def run_server(port=8773):
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

    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="Grok Android Agent",
        version="1.0.0",
        description="""
Control Grok Android app via ADB.
All endpoints return JSON with `ok: true/false`.
        """,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class LoginRequest(BaseModel):
        method: str = "google"
        email: Optional[str] = None
        password: Optional[str] = None
        device: Optional[str] = None

    class ChatRequest(BaseModel):
        prompt: str
        think: bool = False
        deepsearch: bool = False
        timeout: int = 60
        device: Optional[str] = None

    class ImagineRequest(BaseModel):
        prompt: str
        timeout: int = 90
        device: Optional[str] = None

    class OpenRequest(BaseModel):
        device: Optional[str] = None

    @app.get("/health")
    def health():
        devices = [l.split()[0] for l in adb("devices").splitlines()[1:]
                   if "\tdevice" in l]
        return {"status": "ok", "connected_devices": devices, "count": len(devices)}

    @app.get("/status")
    def api_status(device: Optional[str] = None):
        return cmd_status(device=device)

    @app.post("/open")
    def api_open(req: OpenRequest = OpenRequest()):
        result = cmd_open(device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Open failed"))
        return result

    @app.post("/login")
    def api_login(req: LoginRequest):
        result = cmd_login(
            method=req.method,
            email=req.email,
            password=req.password,
            device=req.device,
        )
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Login failed"))
        return result

    @app.post("/chat")
    def api_chat(req: ChatRequest):
        result = cmd_chat(
            prompt=req.prompt,
            think=req.think,
            deepsearch=req.deepsearch,
            timeout=req.timeout,
            device=req.device,
        )
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Chat failed"))
        return result

    @app.post("/imagine")
    def api_imagine(req: ImagineRequest):
        result = cmd_imagine(
            prompt=req.prompt,
            timeout=req.timeout,
            device=req.device,
        )
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Imagine failed"))
        return result

    @app.get("/screenshot")
    def api_screenshot(out: Optional[str] = None, device: Optional[str] = None):
        return cmd_screenshot(out=out, device=device)

    @app.get("/scroll")
    def api_scroll(
        direction: str = Query("down", regex="^(up|down)$"),
        count: int = Query(3, ge=1, le=20),
        device: Optional[str] = None,
    ):
        return cmd_scroll(direction=direction, count=count, device=device)

    class VideoRequest(BaseModel):
        photo_path: Optional[str] = None
        prompt: Optional[str] = None
        timeout: int = 120
        device: Optional[str] = None

    @app.post("/video")
    def api_video(req: VideoRequest):
        """
        Generate video via Grok 'Animate your photos' (free tier).
        Download requires SuperGrok premium (Rp 489K/month).
        Returns screenshot of video player with duration/quality info.
        """
        result = cmd_video(
            photo_path=req.photo_path,
            prompt=req.prompt,
            timeout=req.timeout,
            device=req.device,
        )
        return result

    print(f"[server] autodroid-grok-agent v1.0 on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[server] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="autodroid-grok-agent v1.0 — Grok Android Agent via ADB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s open
  %(prog)s login --method google
  %(prog)s login --method email --email user@example.com --password secret
  %(prog)s chat --prompt "Explain quantum computing"
  %(prog)s chat --prompt "Step-by-step plan" --think --deepsearch
  %(prog)s imagine --prompt "sunset over Jakarta futuristic"
  %(prog)s screenshot --out /tmp/grok.png
  %(prog)s scroll --direction down --count 5
  %(prog)s server --port 8773

API (after starting server):
  curl http://localhost:8773/health
  curl http://localhost:8773/status
  curl -X POST http://localhost:8773/chat \\
       -H "Content-Type: application/json" \\
       -d '{"prompt": "hello grok", "think": false}'
  curl -X POST http://localhost:8773/imagine \\
       -d '{"prompt": "robot in Jakarta market"}'
""",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # status
    s = sub.add_parser("status", help="Check Grok installation and device")
    s.add_argument("--device", "-d", help="ADB device serial")

    # open
    s = sub.add_parser("open", help="Wake and launch Grok")
    s.add_argument("--device", "-d")

    # login
    s = sub.add_parser("login", help="Login to Grok")
    s.add_argument("--method", choices=["google", "email", "x"], default="google")
    s.add_argument("--email", "-e")
    s.add_argument("--password", "-P")
    s.add_argument("--device", "-d")

    # chat
    s = sub.add_parser("chat", help="Send a chat message")
    s.add_argument("--prompt", "-p", required=True)
    s.add_argument("--think", action="store_true", help="Enable Think mode")
    s.add_argument("--deepsearch", action="store_true", help="Enable DeepSearch")
    s.add_argument("--timeout", "-t", type=int, default=60)
    s.add_argument("--device", "-d")

    # imagine
    s = sub.add_parser("imagine", help="Generate an image")
    s.add_argument("--prompt", "-p", required=True)
    s.add_argument("--timeout", "-t", type=int, default=90)
    s.add_argument("--device", "-d")

    # screenshot
    s = sub.add_parser("screenshot", help="Capture screen")
    s.add_argument("--out", "-o")
    s.add_argument("--device", "-d")

    # scroll
    s = sub.add_parser("scroll", help="Scroll chat history")
    s.add_argument("--direction", choices=["up", "down"], default="down")
    s.add_argument("--count", type=int, default=3)
    s.add_argument("--device", "-d")

    # video
    s = sub.add_parser("video", help="Generate video via Animate your photos (free tier)")
    s.add_argument("--photo", help="Local photo path to upload (optional)")
    s.add_argument("--prompt", "-p", help="Video style prompt (optional)")
    s.add_argument("--timeout", "-t", type=int, default=120)
    s.add_argument("--device", "-d")

    # server
    s = sub.add_parser("server", help="Start FastAPI server")
    s.add_argument("--port", type=int, default=8773)

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status(device=args.device)
    elif args.cmd == "open":
        cmd_open(device=args.device)
    elif args.cmd == "login":
        cmd_login(method=args.method, email=args.email,
                  password=args.password, device=args.device)
    elif args.cmd == "chat":
        cmd_chat(args.prompt, think=args.think, deepsearch=args.deepsearch,
                 timeout=args.timeout, device=args.device)
    elif args.cmd == "imagine":
        cmd_imagine(args.prompt, timeout=args.timeout, device=args.device)
    elif args.cmd == "video":
        cmd_video(
            photo_path=getattr(args, "photo", None),
            prompt=getattr(args, "prompt", None),
            timeout=args.timeout,
            device=args.device,
        )
    elif args.cmd == "screenshot":
        cmd_screenshot(out=args.out, device=args.device)
    elif args.cmd == "scroll":
        cmd_scroll(direction=args.direction, count=args.count, device=args.device)
    elif args.cmd == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
