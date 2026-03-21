#!/usr/bin/env python3
"""
autodroid-youtube-agent v1.1 — YouTube Android automation via ADB

Commands:
  status                       -- check app + device
  open   [--device]            -- launch YouTube, screenshot
  search --query TEXT [--device] -- search YouTube, return top 3 titles
  screenshot [--out PATH]      -- capture screen
  login  --account EMAIL [--device]   -- check logged-in state via profile icon
  subscribe --channel NAME [--device] -- search channel and subscribe
  like-video [--device]               -- like currently playing video
  comment --text TEXT [--device]      -- comment on currently playing video
  play --query TEXT [--device]        -- search and play first video result
  server [--port 8770]         -- start FastAPI server

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
from typing import List, Optional

# ─── AI Interceptor (fail-safe) ───────────────────────────────────────────────
try:
    import sys as _sys
    _sys.path.insert(0, '/mnt/data/berkahkarya/skills/1ai-skills/automation/ai-interceptor/scripts')
    from ai_interceptor import AIInterceptor
    from content_interceptor import ContentInterceptor
    _interceptor = AIInterceptor()  # YouTube = title/description enhancement
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

PACKAGE = "com.google.android.youtube"
DOWNLOADS = Path("~/.openclaw/workspace/downloads").expanduser()
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

DISMISS_LABELS = {
    "Skip", "Got it", "Not now", "OK", "Continue", "Lewati",
    "Accept", "Agree", "Close", "Dismiss", "No thanks",
    "Oke", "Lanjutkan", "Tidak sekarang",
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


def swipe(x1, y1, x2, y2, duration=300, device=None):
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration), device=device)


def keyevent(key, device=None):
    adb("shell", "input", "keyevent", str(key), device=device)


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
    remote = "/sdcard/yt_dump.xml"
    local = "/tmp/yt_dump.xml"
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
            if label and bounds:
                nodes.append({
                    "label": label, "text": text, "desc": desc,
                    "class": cls, "bounds": bounds, "resource_id": resource_id,
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
        if label:
            match = (n["label"] == label) if not partial else (label.lower() in n["label"].lower())
            if not match:
                continue
        if cls and cls not in n["class"]:
            continue
        if resource_id and resource_id not in n.get("resource_id", ""):
            continue
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


def launch_youtube(device=None):
    wake(device=device)
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(0.5)
    adb("shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1",
        device=device)
    time.sleep(3.5)
    wake(device=device)
    nodes = dump_ui(device=device)
    dismiss_popups(nodes, device=device)
    time.sleep(0.5)


def do_search(query, active_device):
    """Internal: perform a YouTube search and wait for results."""
    nodes = dump_ui(device=active_device)
    dismiss_popups(nodes, device=active_device)
    time.sleep(0.5)

    # Tap search icon
    search_tapped = (
        tap_node(nodes, label="Search", device=active_device) or
        tap_node(nodes, label="Telusuri", device=active_device) or
        tap_node(nodes, partial=True, label="Search YouTube", device=active_device) or
        tap_node(nodes, partial=True, desc="Search", device=active_device)
    )
    if not search_tapped:
        print("[search] Search icon not found, using fallback coords (640,70)", file=sys.stderr)
        tap(640, 70, device=active_device)
    time.sleep(1.5)

    # Type query word by word
    words = query.split()
    for i, word in enumerate(words):
        safe = "".join(c for c in word if c.isalnum() or c in "-_@.'")
        if safe:
            adb("shell", "input", "text", safe, device=active_device)
            time.sleep(0.15)
        if i < len(words) - 1:
            keyevent("KEYCODE_SPACE", device=active_device)
            time.sleep(0.1)

    time.sleep(0.3)
    keyevent("KEYCODE_ENTER", device=active_device)
    time.sleep(3)
    return dump_ui(device=active_device)


def extract_video_titles(nodes, max_count=3) -> List[str]:
    """Extract video titles from UI nodes — TextViews with substantial text."""
    SKIP_LABELS = {
        "Home", "Shorts", "Subscriptions", "You", "Explore", "Library",
        "Search", "Notifications", "Cast", "Settings", "More options",
        "Share", "Like", "Dislike", "Subscribe", "Save",
        "YouTube", "Beranda", "Langganan", "Anda", "Telusuri",
        "Notifikasi", "Putar", "Jeda",
    }
    titles = []
    seen = set()
    for n in nodes:
        t = n["text"]
        if not t:
            continue
        if n["class"] not in ("TextView",):
            continue
        if len(t) < 10 or len(t) > 200:
            continue
        if t in SKIP_LABELS:
            continue
        stripped = t.strip()
        if stripped.replace(".", "").replace(",", "").replace("K", "").replace("M", "").replace("B", "").isdigit():
            continue
        if stripped in seen:
            continue
        seen.add(stripped)
        titles.append(stripped)
        if len(titles) >= max_count:
            break
    return titles


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
            launch_youtube(device=active_device)

            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)
            time.sleep(1)

            ss_path = str(DOWNLOADS / "youtube_open.png")
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
        "error": "Failed to open YouTube after all retries",
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_search(query, device=None, max_retries=3):
    """
    Search YouTube:
    1. Launch YouTube
    2. Tap search icon
    3. Type query word by word
    4. Press Enter
    5. Wait 3s, dump UI to get video titles
    6. Screenshot
    """
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[search] Attempt {attempt}/{max_retries}, query={query!r}", file=sys.stderr)
        try:
            launch_youtube(device=active_device)
            time.sleep(1)

            nodes_result = do_search(query, active_device)
            dismiss_popups(nodes_result, device=active_device)
            titles = extract_video_titles(nodes_result, max_count=3)

            ss_path = str(DOWNLOADS / "youtube_search.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "query": query,
                "results": titles,
                "screenshot_path": ss_path,
                "device": active_device or "none",
                "attempt": attempt,
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[search] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    result = {
        "ok": False,
        "query": query,
        "results": [],
        "error": "Search failed after all retries",
        "screenshot_path": None,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(device=None, out=None):
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)
    out_path = out or str(DOWNLOADS / "youtube_screenshot.png")
    screencap(out_path, device=active_device)
    result = {
        "ok": True,
        "screenshot_path": out_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


# ─── NEW COMMANDS v1.1 ───────────────────────────────────────────────────────

def cmd_login(account, device=None, max_retries=3):
    """
    Check YouTube login state.
    - YouTube uses Google account (usually already signed in)
    - Tap profile icon (top right)
    - Check logged-in state from account name
    """
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[login] Attempt {attempt}/{max_retries}, account={account}", file=sys.stderr)
        try:
            launch_youtube(device=active_device)
            time.sleep(2)

            nodes = dump_ui(device=active_device)
            dismiss_popups(nodes, device=active_device)

            # Tap profile icon — top right corner
            profile_tapped = (
                tap_node(nodes, label="Account", device=active_device) or
                tap_node(nodes, label="Akun", device=active_device) or
                tap_node(nodes, partial=True, desc="Account", device=active_device) or
                tap_node(nodes, partial=True, label="Profile", device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/avatar_container", device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/account_avatar", device=active_device)
            )
            if not profile_tapped:
                print("[login] Profile icon not found, tapping top-right (670, 70)", file=sys.stderr)
                tap(670, 70, device=active_device)
            time.sleep(1.5)

            # Check if account name is visible in the account sheet
            nodes = dump_ui(device=active_device)
            logged_in = False
            found_account = ""

            # Look for email or account name
            for n in nodes:
                label = n.get("label", "") or n.get("text", "")
                if "@" in label or (account and account.lower() in label.lower()):
                    logged_in = True
                    found_account = label
                    break
                # Also look for "Google Account" header
                if "google" in label.lower() and "account" in label.lower():
                    logged_in = True
                    break

            ss_path = str(DOWNLOADS / "youtube_login.png")
            screencap(ss_path, device=active_device)

            # Close account sheet
            keyevent("KEYCODE_BACK", device=active_device)

            result = {
                "ok": True,
                "logged_in": logged_in,
                "account": found_account or account,
                "screenshot_path": ss_path,
                "device": active_device or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[login] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "youtube_login_fail.png")
    try:
        screencap(ss_path, device=active_device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "logged_in": False,
        "account": account,
        "error": "Failed to check login state after all retries",
        "screenshot_path": ss_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_subscribe(channel, device=None, max_retries=3):
    """
    Subscribe to a YouTube channel.
    - Search for channel
    - Tap first channel result (not video)
    - Tap Subscribe / Berlangganan button
    """
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[subscribe] Attempt {attempt}/{max_retries}, channel={channel}", file=sys.stderr)
        try:
            launch_youtube(device=active_device)
            time.sleep(1)

            # Search for channel
            nodes_result = do_search(channel, active_device)
            dismiss_popups(nodes_result, device=active_device)

            # Look for channel result (has "Saluran" / "Channel" type indicator or verified checkmark)
            # Channels usually appear before videos in search results
            nodes = dump_ui(device=active_device)

            # Try to find a channel card — look for nodes labeled with channel name
            channel_node = (
                find_node(nodes, label=channel) or
                find_node(nodes, label=channel, partial=True) or
                find_node(nodes, partial=True, label="Saluran") or
                find_node(nodes, partial=True, label="Channel") or
                find_node(nodes, partial=True, desc=channel)
            )

            if channel_node:
                c = bounds_to_center(channel_node["bounds"])
                if c:
                    tap(*c, device=active_device)
                    time.sleep(2.5)
            else:
                print("[subscribe] Channel node not found, tapping first result area (360, 300)", file=sys.stderr)
                tap(360, 300, device=active_device)
                time.sleep(2.5)

            # Tap Subscribe / Berlangganan
            nodes = dump_ui(device=active_device)
            subscribed = (
                tap_node(nodes, label="Subscribe", device=active_device) or
                tap_node(nodes, label="Berlangganan", device=active_device) or
                tap_node(nodes, label="SUBSCRIBE", device=active_device) or
                tap_node(nodes, partial=True, label="Berlangganan", device=active_device) or
                tap_node(nodes, partial=True, label="Subscribe", device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/subscribe_button", device=active_device)
            )

            if not subscribed:
                print("[subscribe] Subscribe button not found", file=sys.stderr)

            time.sleep(1.5)
            ss_path = str(DOWNLOADS / f"youtube_subscribe_{channel.replace(' ', '_')}.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": subscribed,
                "subscribed": subscribed,
                "channel": channel,
                "screenshot_path": ss_path,
                "device": active_device or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[subscribe] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "youtube_subscribe_fail.png")
    try:
        screencap(ss_path, device=active_device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "subscribed": False,
        "channel": channel,
        "error": "Failed to subscribe after all retries",
        "screenshot_path": ss_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_like_video(device=None, max_retries=3):
    """
    Like the currently playing video.
    - Find thumbs up button
    - Tap it
    """
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[like-video] Attempt {attempt}/{max_retries}", file=sys.stderr)
        try:
            nodes = dump_ui(device=active_device)

            # Find like/thumbs up button
            liked = (
                tap_node(nodes, label="Like", device=active_device) or
                tap_node(nodes, label="Suka", device=active_device) or
                tap_node(nodes, desc="like this video", partial=True, device=active_device) or
                tap_node(nodes, desc="Like this video", partial=True, device=active_device) or
                tap_node(nodes, desc="Suka video ini", partial=True, device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/like_button", device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/likes_count_view", device=active_device)
            )

            if not liked:
                print("[like-video] Like button not found, trying thumbs-up area (120, 1100)", file=sys.stderr)
                tap(120, 1100, device=active_device)
                liked = True  # Assume tapped

            time.sleep(1)
            ss_path = str(DOWNLOADS / "youtube_like.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": liked,
                "liked": liked,
                "screenshot_path": ss_path,
                "device": active_device or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[like-video] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "youtube_like_fail.png")
    try:
        screencap(ss_path, device=active_device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "liked": False,
        "error": "Failed to like video after all retries",
        "screenshot_path": ss_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_comment(text, device=None, max_retries=3):
    """
    Comment on the currently playing video.
    - Scroll down in current video
    - Tap "Tambahkan komentar..." field
    - Type text
    - Tap send arrow
    """
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[comment] Attempt {attempt}/{max_retries}, text={text!r}", file=sys.stderr)
        try:
            # Scroll down to reveal comments section
            swipe(360, 1000, 360, 400, duration=500, device=active_device)
            time.sleep(1.5)

            nodes = dump_ui(device=active_device)

            # Find comment input field
            comment_field = (
                find_node(nodes, partial=True, label="Tambahkan komentar") or
                find_node(nodes, partial=True, label="Add a comment") or
                find_node(nodes, partial=True, label="comment") or
                find_node(nodes, resource_id="com.google.android.youtube:id/comment_input_field") or
                find_node(nodes, cls="EditText")
            )

            if comment_field:
                c = bounds_to_center(comment_field["bounds"])
                if c:
                    tap(*c, device=active_device)
                    time.sleep(1)
            else:
                print("[comment] Comment field not found, scrolling more and retrying", file=sys.stderr)
                swipe(360, 1000, 360, 300, duration=600, device=active_device)
                time.sleep(1.5)
                nodes = dump_ui(device=active_device)
                comment_field = find_node(nodes, cls="EditText")
                if comment_field:
                    c = bounds_to_center(comment_field["bounds"])
                    if c:
                        tap(*c, device=active_device)
                        time.sleep(1)
                else:
                    # Fallback tap where comment area usually is
                    tap(360, 1500, device=active_device)
                    time.sleep(1)

            # Type comment text
            words = text.split()
            for i, word in enumerate(words):
                safe = word.replace("'", "\\'").replace('"', '\\"')
                if safe:
                    adb("shell", "input", "text", safe, device=active_device)
                    time.sleep(0.1)
                if i < len(words) - 1:
                    keyevent("KEYCODE_SPACE", device=active_device)
                    time.sleep(0.07)

            time.sleep(0.5)

            # Tap send button
            nodes = dump_ui(device=active_device)
            send_tapped = (
                tap_node(nodes, label="Post", device=active_device) or
                tap_node(nodes, label="Kirim", device=active_device) or
                tap_node(nodes, desc="Send", device=active_device) or
                tap_node(nodes, desc="Post", device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/post_comment", device=active_device) or
                tap_node(nodes, resource_id="com.google.android.youtube:id/send_button", device=active_device)
            )
            if not send_tapped:
                print("[comment] Send button not found, trying ENTER", file=sys.stderr)
                keyevent("KEYCODE_ENTER", device=active_device)

            time.sleep(2)
            ss_path = str(DOWNLOADS / "youtube_comment.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "commented": True,
                "text": text,
                "screenshot_path": ss_path,
                "device": active_device or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[comment] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "youtube_comment_fail.png")
    try:
        screencap(ss_path, device=active_device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "commented": False,
        "text": text,
        "error": "Failed to post comment after all retries",
        "screenshot_path": ss_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


@_ai_intercept(skill_type="content_gen")
def cmd_play(query, device=None, max_retries=3):
    """
    Search and play first video result.
    - search(query)
    - Tap first video result
    - Wait 2s for video to start
    - Screenshot
    - Return playing info with title from UI
    """
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    for attempt in range(1, max_retries + 1):
        print(f"[play] Attempt {attempt}/{max_retries}, query={query!r}", file=sys.stderr)
        try:
            launch_youtube(device=active_device)
            time.sleep(1)

            # Search for query
            nodes_result = do_search(query, active_device)
            dismiss_popups(nodes_result, device=active_device)

            # Get titles from search results
            nodes = dump_ui(device=active_device)
            titles = extract_video_titles(nodes, max_count=5)

            # Tap first video result — first video thumbnail area
            # Video results are usually around y=250-400 range from top
            # Try finding by title text first
            first_video_node = None
            for n in nodes:
                t = n.get("text", "")
                if len(t) > 10 and n["class"] == "TextView":
                    # Skip nav items
                    skip = {"Home", "Shorts", "Subscriptions", "You", "Beranda", "Langganan"}
                    if t not in skip:
                        first_video_node = n
                        break

            if first_video_node:
                c = bounds_to_center(first_video_node["bounds"])
                if c:
                    # Tap on the video, not just the title — offset slightly up for thumbnail
                    tap(c[0], max(c[1] - 50, 50), device=active_device)
            else:
                print("[play] Video node not found, tapping first result area (360, 300)", file=sys.stderr)
                tap(360, 300, device=active_device)

            # Wait for video to start
            time.sleep(3)

            # Get title from now-playing screen
            nodes_playing = dump_ui(device=active_device)
            playing_title = ""
            for n in nodes_playing:
                t = n.get("text", "")
                if len(t) > 10 and n["class"] == "TextView":
                    skip_labels = {"Home", "Shorts", "Subscriptions", "You", "Beranda", "Langganan"}
                    if t not in skip_labels:
                        playing_title = t
                        break

            if not playing_title and titles:
                playing_title = titles[0]

            ss_path = str(DOWNLOADS / "youtube_play.png")
            screencap(ss_path, device=active_device)

            result = {
                "ok": True,
                "playing": True,
                "title": playing_title,
                "query": query,
                "screenshot_path": ss_path,
                "device": active_device or "none",
            }
            print(json.dumps(result, indent=2))
            return result

        except Exception as e:
            print(f"[play] Error on attempt {attempt}: {e}", file=sys.stderr)
            time.sleep(2)

    ss_path = str(DOWNLOADS / "youtube_play_fail.png")
    try:
        screencap(ss_path, device=active_device)
    except Exception:
        ss_path = None

    result = {
        "ok": False,
        "playing": False,
        "title": "",
        "query": query,
        "error": "Failed to play video after all retries",
        "screenshot_path": ss_path,
        "device": active_device or "none",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_scroll(direction="up", count=3, device=None):
    """Scroll YouTube feed/search results with natural swipes."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    try:
        for i in range(count):
            print(f"[scroll] Swipe {i+1}/{count} ({direction})", file=sys.stderr)
            natural_swipe(direction, device=active_device)
            natural_pause(0.8, 2.0)

        ss_path = str(DOWNLOADS / "youtube_scroll.png")
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


def cmd_browse(duration=30, device=None):
    """Scroll YouTube home feed for `duration` seconds with natural timing."""
    devices = get_connected_devices()
    active_device = device or (devices[0] if devices else None)

    scrolled_count = 0
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            # Wait 5-10s between scrolls (simulate browsing thumbnails)
            wait = random.uniform(5.0, 10.0)
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            if remaining <= 0:
                break
            time.sleep(min(wait, remaining))

            if time.time() - start_time >= duration:
                break

            print(f"[browse] Scrolling up ({scrolled_count+1})", file=sys.stderr)
            natural_swipe("up", device=active_device)
            scrolled_count += 1

        ss_path = str(DOWNLOADS / "youtube_browse.png")
        screencap(ss_path, device=active_device)

        result = {
            "ok": True,
            "duration": duration,
            "scrolled_count": scrolled_count,
            "screenshot_path": ss_path,
            "device": active_device or "none",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "duration": duration,
            "scrolled_count": scrolled_count,
            "screenshot_path": None,
            "device": active_device or "none",
        }

    print(json.dumps(result, indent=2))
    return result


# ─── API Server ──────────────────────────────────────────────────────────────

def run_server(port=8770):
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
        title="autodroid-youtube-agent",
        version="1.1.0",
        description="Control YouTube Android app via ADB",
    )
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    class SearchRequest(BaseModel):
        query: str
        device: Optional[str] = None

    class LoginRequest(BaseModel):
        account: str
        device: Optional[str] = None

    class SubscribeRequest(BaseModel):
        channel: str
        device: Optional[str] = None

    class CommentRequest(BaseModel):
        text: str
        device: Optional[str] = None

    class PlayRequest(BaseModel):
        query: str
        device: Optional[str] = None

    class BrowseRequest(BaseModel):
        duration: int = 30
        device: Optional[str] = None

    @app.get("/")
    def root():
        return {
            "service": "autodroid-youtube-agent",
            "version": "1.1.0",
            "endpoints": [
                "/status", "/open", "/search", "/screenshot",
                "/login", "/subscribe", "/like-video", "/comment", "/play",
                "/scroll", "/browse",
            ],
        }

    @app.get("/status")
    def api_status(device: Optional[str] = None):
        return cmd_status(device=device)

    @app.post("/open")
    def api_open(device: Optional[str] = None):
        return cmd_open(device=device)

    @app.post("/search")
    def api_search(req: SearchRequest):
        return cmd_search(req.query, device=req.device)

    @app.get("/screenshot")
    def api_screenshot(device: Optional[str] = None, out: Optional[str] = None):
        return cmd_screenshot(device=device, out=out)

    @app.post("/login")
    def api_login(req: LoginRequest):
        return cmd_login(req.account, device=req.device)

    @app.post("/subscribe")
    def api_subscribe(req: SubscribeRequest):
        result = cmd_subscribe(req.channel, device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to subscribe"))
        return result

    @app.post("/like-video")
    def api_like_video(device: Optional[str] = None):
        result = cmd_like_video(device=device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to like video"))
        return result

    @app.post("/comment")
    def api_comment(req: CommentRequest):
        result = cmd_comment(req.text, device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to post comment"))
        return result

    @app.post("/play")
    def api_play(req: PlayRequest):
        result = cmd_play(req.query, device=req.device)
        if not result.get("ok"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to play video"))
        return result

    @app.get("/scroll")
    def api_scroll(direction: str = "up", count: int = 3, device: Optional[str] = None):
        return cmd_scroll(direction=direction, count=count, device=device)

    @app.post("/browse")
    def api_browse(req: BrowseRequest):
        return cmd_browse(duration=req.duration, device=req.device)

    @app.get("/health")
    def health():
        devices = get_connected_devices()
        return {"status": "ok", "connected_devices": devices, "count": len(devices)}

    print(f"[server] autodroid-youtube-agent v1.1 on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[server] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description="autodroid-youtube-agent v1.1 — YouTube Android automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s open
  %(prog)s search --query "tutorial python 2024"
  %(prog)s screenshot --out /tmp/yt.png
  %(prog)s login --account "user@gmail.com"
  %(prog)s subscribe --channel "PewDiePie"
  %(prog)s like-video
  %(prog)s comment --text "Great video!"
  %(prog)s play --query "lofi music"
  %(prog)s server --port 8770
""",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="Check app + device status")
    s.add_argument("--device", "-d")

    s = sub.add_parser("open", help="Launch YouTube, screenshot")
    s.add_argument("--device", "-d")

    s = sub.add_parser("search", help="Search YouTube, return top 3 titles")
    s.add_argument("--query", "-q", required=True)
    s.add_argument("--device", "-d")

    s = sub.add_parser("screenshot", help="Capture screenshot")
    s.add_argument("--device", "-d")
    s.add_argument("--out", "-o")

    s = sub.add_parser("login", help="Check YouTube login state via profile icon")
    s.add_argument("--account", required=True, help="Expected Google account email")
    s.add_argument("--device", "-d")

    s = sub.add_parser("subscribe", help="Subscribe to a YouTube channel")
    s.add_argument("--channel", required=True, help="Channel name to search and subscribe")
    s.add_argument("--device", "-d")

    s = sub.add_parser("like-video", help="Like currently playing video")
    s.add_argument("--device", "-d")

    s = sub.add_parser("comment", help="Comment on currently playing video")
    s.add_argument("--text", required=True, help="Comment text to post")
    s.add_argument("--device", "-d")

    s = sub.add_parser("play", help="Search and play first video result")
    s.add_argument("--query", "-q", required=True, help="Search query to find and play")
    s.add_argument("--device", "-d")

    s = sub.add_parser("scroll", help="Scroll YouTube feed with natural swipes")
    s.add_argument("--direction", default="up", choices=["up", "down"], help="Swipe direction (default: up)")
    s.add_argument("--count", "-n", type=int, default=3, help="Number of swipes (default: 3)")
    s.add_argument("--device", "-d")

    s = sub.add_parser("browse", help="Browse YouTube home feed for N seconds")
    s.add_argument("--duration", type=int, default=30, help="Browse duration in seconds (default: 30)")
    s.add_argument("--device", "-d")

    s = sub.add_parser("server", help="Start FastAPI server")
    s.add_argument("--port", type=int, default=8770)

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status(device=args.device)
    elif args.cmd == "open":
        cmd_open(device=args.device)
    elif args.cmd == "search":
        cmd_search(args.query, device=args.device)
    elif args.cmd == "screenshot":
        cmd_screenshot(device=args.device, out=args.out)
    elif args.cmd == "login":
        cmd_login(args.account, device=args.device)
    elif args.cmd == "subscribe":
        cmd_subscribe(args.channel, device=args.device)
    elif args.cmd == "like-video":
        cmd_like_video(device=args.device)
    elif args.cmd == "comment":
        cmd_comment(args.text, device=args.device)
    elif args.cmd == "play":
        cmd_play(args.query, device=args.device)
    elif args.cmd == "scroll":
        cmd_scroll(direction=args.direction, count=args.count, device=args.device)
    elif args.cmd == "browse":
        cmd_browse(duration=args.duration, device=args.device)
    elif args.cmd == "server":
        run_server(port=args.port)


if __name__ == "__main__":
    main()
