#!/usr/bin/env python3
"""
PixVerse Android Automation Agent
==================================
Production-ready ADB automation for PixVerse - AI Video Generator
Package: com.pixverse.app
Port: 8775
Device: Redmi 2409BRN2CY, Android 14, 720x1640

Commands: status, open, login, text2video, image2video, screenshot, scroll, server
"""

import argparse
import base64
import json
import os
import random
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

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

# ─── Constants ────────────────────────────────────────────────────────────────
PACKAGE = "com.pixverse.app"
ACTIVITY = "com.pixverse.app/.MainActivity"
DEFAULT_DEVICE = "SGZTONV4OBL74TJZ"
DOWNLOADS = Path.home() / ".openclaw/workspace/downloads"
SCREENSHOTS_DIR = Path.home() / ".openclaw/workspace/downloads/screenshots"
SERVER_PORT = 8775
MAX_RETRIES = 3
GENERATION_TIMEOUT = 180  # seconds

# Possible PixVerse video save paths (in priority order)
VIDEO_SAVE_PATHS = [
    "/sdcard/Pictures/PixVerse",
    "/sdcard/DCIM/PixVerse",
    "/sdcard/Movies/PixVerse",
    "/sdcard/Movies",
    "/sdcard/DCIM",
    "/sdcard/Pictures",
]

# UI state detection keywords
STATE_KEYWORDS = {
    "HOME": ["For You", "Following", "Explore", "feed", "Discover"],
    "CREATE": ["Create video", "Text to Video", "Image to Video", "Describe your video",
               "Enter prompt", "Write a prompt", "Generate"],
    "GENERATING": ["Generating", "Processing", "Creating", "Loading", "Please wait",
                   "In Queue", "%" ],
    "RESULT": ["Download", "Share", "Save", "Publish", "Re-generate"],
    "LOGIN": ["Sign in", "Log in", "Continue with Google", "Continue with Apple",
              "Email", "Login", "Sign up", "Create account"],
}


# ─── ADB Helpers ──────────────────────────────────────────────────────────────

def adb(*args, device=None, timeout=30):
    """Run adb command, return stdout string."""
    cmd = ["adb"]
    if device:
        cmd += ["-s", device]
    cmd += list(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except FileNotFoundError:
        return "__ADB_NOT_FOUND__"


def adb_check(device=None):
    """Check if adb is available and device is connected."""
    result = adb("devices", device=None)
    if result == "__ADB_NOT_FOUND__":
        return False, "adb not found in PATH"
    if device:
        lines = result.splitlines()
        for line in lines:
            if device in line and "device" in line and "offline" not in line:
                return True, "connected"
        return False, f"device {device} not found or offline"
    return True, "adb available"


def wake(device=None):
    """Wake device, unlock screen."""
    adb("shell", "input", "keyevent", "26", device=device)
    time.sleep(0.5)
    adb("shell", "input", "keyevent", "82", device=device)
    time.sleep(0.5)
    # Swipe up to unlock
    adb("shell", "input", "swipe", "360", "1500", "360", "800", device=device)
    time.sleep(0.8)


def dump_ui(device=None):
    """Dump UI hierarchy and return list of node dicts."""
    adb("shell", "uiautomator", "dump", "/sdcard/pv.xml", device=device)
    time.sleep(0.3)
    adb("pull", "/sdcard/pv.xml", "/tmp/pv_ui.xml", device=device)
    try:
        root = ET.parse("/tmp/pv_ui.xml").getroot()
        nodes = []
        for n in root.iter():
            nodes.append({
                "class": n.get("class", ""),
                "text": n.get("text", ""),
                "content-desc": n.get("content-desc", ""),
                "resource-id": n.get("resource-id", ""),
                "bounds": n.get("bounds", ""),
                "clickable": n.get("clickable", "false"),
                "enabled": n.get("enabled", "true"),
                "focused": n.get("focused", "false"),
            })
        return nodes
    except Exception:
        return []


def find_node(nodes, label=None, res_id=None, partial=False, cls=None):
    """Find a node by text/content-desc, resource-id, or class."""
    for n in nodes:
        t = (n["text"] + " " + n["content-desc"]).strip()
        if label:
            if partial and label.lower() in t.lower():
                if cls is None or cls.lower() in n["class"].lower():
                    return n
            elif not partial and t.lower() == label.lower():
                if cls is None or cls.lower() in n["class"].lower():
                    return n
        if res_id and res_id in n["resource-id"]:
            if cls is None or cls.lower() in n["class"].lower():
                return n
    return None


def find_all_nodes(nodes, label=None, res_id=None, partial=False, cls=None):
    """Find all matching nodes."""
    results = []
    for n in nodes:
        t = (n["text"] + " " + n["content-desc"]).strip()
        match = False
        if label:
            if partial and label.lower() in t.lower():
                match = True
            elif not partial and t.lower() == label.lower():
                match = True
        if res_id and res_id in n["resource-id"]:
            match = True
        if match:
            if cls is None or cls.lower() in n["class"].lower():
                results.append(n)
    return results


def bounds_to_center(bounds_str):
    """Parse '[x1,y1][x2,y2]' bounds string to center (x, y)."""
    nums = list(map(int, re.findall(r"\d+", bounds_str)))
    if len(nums) == 4:
        return (nums[0] + nums[2]) // 2, (nums[1] + nums[3]) // 2
    return None


def tap(x, y, device=None):
    """Tap at coordinates with natural delay."""
    adb("shell", "input", "tap", str(x), str(y), device=device)
    time.sleep(random.uniform(0.3, 0.6))


def tap_node(node, device=None):
    """Tap the center of a UI node."""
    c = bounds_to_center(node["bounds"])
    if c:
        tap(c[0], c[1], device=device)
        return True
    return False


def swipe(x1, y1, x2, y2, duration=300, device=None):
    """Perform a swipe gesture."""
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration), device=device)
    time.sleep(random.uniform(0.4, 0.7))


def scroll_down(device=None, count=1):
    """Scroll down on screen."""
    for _ in range(count):
        swipe(360, 1000, 360, 400, duration=300, device=device)
        time.sleep(0.3)


def scroll_up(device=None, count=1):
    """Scroll up on screen."""
    for _ in range(count):
        swipe(360, 400, 360, 1000, duration=300, device=device)
        time.sleep(0.3)


def type_text(text, device=None):
    """Type text using ADB input (URL-encoded for special chars)."""
    # Escape special characters for shell
    escaped = text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
    escaped = escaped.replace(" ", "%s").replace("&", "\\&")
    adb("shell", "input", "text", escaped, device=device)
    time.sleep(0.3)


def type_prompt(prompt, device=None):
    """Type prompt word by word via Xiaomi keyboard."""
    # Switch to Xiaomi keyboard (no autocorrect)
    adb("shell", "settings", "put", "secure", "default_input_method",
        "com.preff.kb.xm/com.preff.kb.LatinIME", device=device)
    time.sleep(0.3)
    words = prompt.split()
    for i, word in enumerate(words):
        # Escape special chars
        escaped = word.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
        escaped = escaped.replace("&", "\\&").replace(";", "\\;")
        adb("shell", "input", "text", escaped, device=device)
        time.sleep(random.uniform(0.15, 0.25))
        if i < len(words) - 1:
            adb("shell", "input", "keyevent", "62", device=device)  # Space
            time.sleep(random.uniform(0.1, 0.2))


def clear_text_field(device=None):
    """Select all and delete text in focused field."""
    adb("shell", "input", "keyevent", "KEYCODE_CTRL_A", device=device)
    time.sleep(0.2)
    adb("shell", "input", "keyevent", "KEYCODE_DEL", device=device)
    time.sleep(0.2)


def take_screenshot(device=None, filename=None):
    """Take screenshot and save locally."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    if not filename:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pixverse_screenshot_{ts}.png"
    remote_path = f"/sdcard/{filename}"
    local_path = SCREENSHOTS_DIR / filename
    adb("shell", "screencap", "-p", remote_path, device=device)
    time.sleep(0.5)
    adb("pull", remote_path, str(local_path), device=device)
    adb("shell", "rm", remote_path, device=device)
    return str(local_path) if local_path.exists() else None


def get_current_app(device=None):
    """Get the foreground package name."""
    out = adb("shell", "dumpsys", "window", "windows", device=device)
    for line in out.splitlines():
        if "mCurrentFocus" in line or "mFocusedApp" in line:
            m = re.search(r"([a-z][a-z0-9_]*\.[a-z][a-z0-9_.]+)/", line)
            if m:
                return m.group(1)
    return ""


def is_app_installed(package, device=None):
    """Check if package is installed on device."""
    out = adb("shell", "pm", "list", "packages", package, device=device)
    return package in out


# ─── State Detection ──────────────────────────────────────────────────────────

def detect_state(nodes):
    """Detect current PixVerse app state from UI nodes."""
    all_text = " ".join(
        (n["text"] + " " + n["content-desc"]).strip()
        for n in nodes
    ).lower()

    # Check for daily limit
    limit_phrases = ["daily limit", "limit reached", "no more credits",
                     "out of credits", "quota", "ran out"]
    for phrase in limit_phrases:
        if phrase in all_text:
            return "DAILY_LIMIT"

    # Check each state
    for state, keywords in STATE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in all_text:
                return state

    return "UNKNOWN"


def wait_for_state(target_states, device=None, timeout=30, interval=2):
    """Poll UI until one of target_states is detected."""
    if isinstance(target_states, str):
        target_states = [target_states]
    deadline = time.time() + timeout
    while time.time() < deadline:
        nodes = dump_ui(device=device)
        state = detect_state(nodes)
        if state in target_states:
            return state, nodes
        time.sleep(interval)
    return None, []


# ─── Video File Detection ──────────────────────────────────────────────────────

def get_current_timestamp(device=None):
    """Get current Unix timestamp from device."""
    out = adb("shell", "date", "+%s", device=device)
    try:
        return int(out.strip())
    except Exception:
        return int(time.time())


def wait_for_video_file(ts_before, device=None, timeout=60):
    """Poll MediaStore for new video files added after ts_before."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        # Query MediaStore for recent videos
        out = adb(
            "shell", "content", "query",
            "--uri", "content://media/external_primary/video/media",
            "--projection", "_data,date_added",
            "--sort", "date_added DESC",
            device=device,
            timeout=15
        )
        for line in out.splitlines():
            if "_data=" in line and "date_added=" in line:
                try:
                    ts_str = line.split("date_added=")[1].split(",")[0].strip()
                    path_str = line.split("_data=")[1].split(",")[0].strip()
                    ts = int(ts_str)
                    if ts > ts_before:
                        return path_str
                except (IndexError, ValueError):
                    continue
        time.sleep(2)
    return None


def pull_video(remote_path, device=None):
    """Pull video from device to local downloads directory."""
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_filename = f"pixverse_video_{ts}.mp4"
    local_path = DOWNLOADS / local_filename
    result = adb("pull", remote_path, str(local_path), device=device, timeout=60)
    if local_path.exists() and local_path.stat().st_size > 0:
        return str(local_path)
    return None


# ─── Retry Decorator ──────────────────────────────────────────────────────────

def with_retry(func, *args, retries=MAX_RETRIES, base_delay=1.0, **kwargs):
    """Execute func with exponential backoff retry."""
    last_err = None
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                time.sleep(delay)
    raise last_err


# ─── Core Commands ────────────────────────────────────────────────────────────

def cmd_status(device=None):
    """Check ADB device + app installation status."""
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    installed = is_app_installed(PACKAGE, device=device)
    current_app = get_current_app(device=device)

    result = {
        "ok": True,
        "device": device or "default",
        "app_installed": installed,
        "app_running": PACKAGE in current_app,
        "current_app": current_app,
    }

    if not installed:
        result["install_cmd"] = (
            f"adb shell am start -a android.intent.action.VIEW "
            f"-d 'market://details?id={PACKAGE}'"
        )

    return result


def cmd_open(device=None):
    """Wake device and launch PixVerse app."""
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    if not is_app_installed(PACKAGE, device=device):
        return {
            "ok": False,
            "error": "app_not_installed",
            "install": (
                f"adb shell am start -a android.intent.action.VIEW "
                f"-d 'market://details?id={PACKAGE}'"
            ),
        }

    wake(device=device)
    time.sleep(0.5)

    # Launch app
    adb("shell", "am", "start", "-n", ACTIVITY, device=device)
    time.sleep(3)

    # Wait for app to load
    state, nodes = wait_for_state(
        ["HOME", "CREATE", "LOGIN"], device=device, timeout=15, interval=2
    )

    if state is None:
        # Try force-stop and re-launch
        adb("shell", "am", "force-stop", PACKAGE, device=device)
        time.sleep(1)
        adb("shell", "am", "start", "-n", ACTIVITY, device=device)
        time.sleep(4)
        state, nodes = wait_for_state(
            ["HOME", "CREATE", "LOGIN"], device=device, timeout=15, interval=2
        )

    return {
        "ok": state is not None,
        "state": state or "UNKNOWN",
        "detail": "App launched successfully" if state else "App did not reach expected state",
    }


def cmd_login(method="google", device=None):
    """Perform login via Google or email."""
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    # Open app first
    open_result = cmd_open(device=device)
    if not open_result["ok"]:
        return open_result

    # Check if already logged in
    if open_result.get("state") in ["HOME", "CREATE"]:
        return {"ok": True, "detail": "Already logged in", "state": open_result["state"]}

    # Wait for login screen
    state, nodes = wait_for_state(["LOGIN", "HOME"], device=device, timeout=10)

    if state == "HOME":
        return {"ok": True, "detail": "Already logged in"}

    if state != "LOGIN":
        nodes = dump_ui(device=device)

    # Find login button
    if method == "google":
        btn = find_node(nodes, label="Continue with Google", partial=True)
        if not btn:
            btn = find_node(nodes, label="Google", partial=True)
        if not btn:
            btn = find_node(nodes, label="Sign in with Google", partial=True)
    else:
        btn = find_node(nodes, label="Continue with Email", partial=True)
        if not btn:
            btn = find_node(nodes, label="Email", partial=True)
        if not btn:
            btn = find_node(nodes, label="Sign in with Email", partial=True)

    if btn:
        tap_node(btn, device=device)
        time.sleep(3)
        # Wait for home after login
        state, _ = wait_for_state(["HOME", "CREATE"], device=device, timeout=30)
        if state:
            return {"ok": True, "detail": f"Logged in via {method}", "state": state}
        else:
            screenshot = take_screenshot(device=device)
            return {
                "ok": False,
                "error": "login_incomplete",
                "detail": "Login flow started but home not reached (may need manual interaction)",
                "screenshot_path": screenshot,
            }
    else:
        screenshot = take_screenshot(device=device)
        return {
            "ok": False,
            "error": "login_button_not_found",
            "method": method,
            "screenshot_path": screenshot,
        }


def _navigate_to_create(device=None):
    """Navigate to the Create/text2video input screen."""
    nodes = dump_ui(device=device)
    state = detect_state(nodes)

    # If already on CREATE, return current nodes
    if state == "CREATE":
        return True, nodes

    # Look for create/plus button
    create_labels = ["+", "Create", "New", "Make", "Generate"]
    for label in create_labels:
        btn = find_node(nodes, label=label, partial=(label not in ["+", "Create"]))
        if btn and btn["clickable"] == "true":
            tap_node(btn, device=device)
            time.sleep(1.5)
            nodes = dump_ui(device=device)
            if detect_state(nodes) == "CREATE":
                return True, nodes
            break

    # Try tapping bottom center (common location for create button)
    tap(360, 1530, device=device)
    time.sleep(1.5)
    nodes = dump_ui(device=device)

    if detect_state(nodes) == "CREATE":
        return True, nodes

    # Try looking for text input area
    text_input = find_node(nodes, label="Describe your video", partial=True)
    if not text_input:
        text_input = find_node(nodes, label="Enter prompt", partial=True)
    if not text_input:
        text_input = find_node(nodes, label="Write a prompt", partial=True)
    if not text_input:
        text_input = find_node(nodes, cls="EditText")

    if text_input:
        return True, nodes

    return False, nodes


def cmd_text2video(prompt, timeout=GENERATION_TIMEOUT, device=None):
    """Generate video from text prompt."""
    # AI Interceptor: enhance prompt if available (fail-safe)
    if AI_INTERCEPT_ENABLED and _interceptor:
        try:
            prompt = _interceptor.intercept(skill_type="pixverse_gen")(lambda p: p)(prompt)
        except Exception:
            pass
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    if not is_app_installed(PACKAGE, device=device):
        return {
            "ok": False,
            "error": "app_not_installed",
            "install": (
                f"adb shell am start -a android.intent.action.VIEW "
                f"-d 'market://details?id={PACKAGE}'"
            ),
        }

    # Open app
    open_result = cmd_open(device=device)
    if not open_result["ok"]:
        return open_result

    # Check login
    if open_result.get("state") == "LOGIN":
        return {
            "ok": False,
            "error": "login_required",
            "detail": "Please login first using the login command",
        }

    # Check daily limit
    nodes = dump_ui(device=device)
    if detect_state(nodes) == "DAILY_LIMIT":
        return {"ok": False, "error": "daily_limit_reached", "resets_in": "24h"}

    # Navigate to create screen
    navigated, nodes = _navigate_to_create(device=device)
    if not navigated:
        screenshot = take_screenshot(device=device)
        return {
            "ok": False,
            "error": "navigation_failed",
            "detail": "Could not navigate to create screen",
            "screenshot_path": screenshot,
        }

    time.sleep(0.5)

    # Find text input
    text_input = find_node(nodes, label="Describe your video", partial=True)
    if not text_input:
        text_input = find_node(nodes, label="Enter prompt", partial=True)
    if not text_input:
        text_input = find_node(nodes, label="Write a prompt", partial=True)
    if not text_input:
        text_input = find_node(nodes, label="Type something", partial=True)
    if not text_input:
        text_input = find_node(nodes, cls="EditText")

    if text_input:
        tap_node(text_input, device=device)
        time.sleep(0.8)
        clear_text_field(device=device)
    else:
        # Try tapping center of screen where prompt box likely is
        tap(360, 800, device=device)
        time.sleep(0.8)

    # Type the prompt
    type_prompt(prompt, device=device)
    time.sleep(0.5)

    # Dismiss keyboard
    adb("shell", "input", "keyevent", "111", device=device)  # KEYCODE_ESCAPE
    time.sleep(0.5)

    # Look for generate/create button
    nodes = dump_ui(device=device)
    generate_btn = None
    for label in ["Generate", "Create", "Create video", "Make video", "Submit"]:
        generate_btn = find_node(nodes, label=label, partial=True)
        if generate_btn and generate_btn["clickable"] == "true":
            break

    # Record timestamp before generation for video file detection
    ts_before = get_current_timestamp(device=device)

    if generate_btn:
        tap_node(generate_btn, device=device)
    else:
        # Try tapping common generate button location (bottom of screen)
        tap(360, 1580, device=device)

    time.sleep(2)

    # Check for daily limit after attempting to generate
    nodes = dump_ui(device=device)
    if detect_state(nodes) == "DAILY_LIMIT":
        return {"ok": False, "error": "daily_limit_reached", "resets_in": "24h"}

    # Wait for generation to complete
    generation_start = time.time()
    generation_done = False
    poll_interval = 5

    while time.time() - generation_start < timeout:
        nodes = dump_ui(device=device)
        state = detect_state(nodes)

        if state == "DAILY_LIMIT":
            return {"ok": False, "error": "daily_limit_reached", "resets_in": "24h"}

        if state == "RESULT":
            generation_done = True
            break

        # Check for progress/generating indicators
        if state == "GENERATING":
            # Still generating, continue waiting
            time.sleep(poll_interval)
            continue

        # Check for error/failure indicators
        error_phrases = ["failed", "error", "try again", "something went wrong"]
        all_text = " ".join(n["text"] + " " + n["content-desc"] for n in nodes).lower()
        for phrase in error_phrases:
            if phrase in all_text:
                screenshot = take_screenshot(device=device)
                return {
                    "ok": False,
                    "error": "generation_failed",
                    "detail": f"Error detected: {phrase}",
                    "screenshot_path": screenshot,
                }

        time.sleep(poll_interval)

    if not generation_done:
        screenshot = take_screenshot(device=device)
        # Check one more time
        nodes = dump_ui(device=device)
        if detect_state(nodes) != "RESULT":
            return {
                "ok": False,
                "error": "generation_timeout",
                "detail": f"Generation did not complete within {timeout}s",
                "screenshot_path": screenshot,
            }

    # Find and tap download button
    nodes = dump_ui(device=device)
    download_btn = find_node(nodes, label="Download", partial=True)
    if not download_btn:
        download_btn = find_node(nodes, label="Save", partial=True)
    if not download_btn:
        download_btn = find_node(nodes, res_id="download")

    if download_btn:
        tap_node(download_btn, device=device)
        time.sleep(2)
    else:
        screenshot = take_screenshot(device=device)
        return {
            "ok": False,
            "error": "download_button_not_found",
            "screenshot_path": screenshot,
        }

    # Wait for video file to appear
    video_path = wait_for_video_file(ts_before, device=device, timeout=60)

    if not video_path:
        screenshot = take_screenshot(device=device)
        return {
            "ok": False,
            "error": "video_file_not_found",
            "detail": "Video was generated but could not find downloaded file",
            "screenshot_path": screenshot,
        }

    # Pull video to local machine
    local_path = pull_video(video_path, device=device)

    if not local_path:
        return {
            "ok": False,
            "error": "video_pull_failed",
            "remote_path": video_path,
            "detail": "Could not pull video from device",
        }

    return {
        "ok": True,
        "video_path": local_path,
        "remote_path": video_path,
        "prompt": prompt,
        "generation_time_s": round(time.time() - generation_start, 1),
    }


def _push_image_to_device(image_path, device=None):
    """Push local image to device temp folder."""
    image_path = Path(image_path)
    if not image_path.exists():
        return None, f"Image not found: {image_path}"
    remote_path = f"/sdcard/DCIM/{image_path.name}"
    result = adb("push", str(image_path), remote_path, device=device, timeout=30)
    if "error" in result.lower():
        return None, result
    # Trigger media scan
    adb("shell", "am", "broadcast",
        "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
        "-d", f"file://{remote_path}", device=device)
    time.sleep(1)
    return remote_path, None


def cmd_image2video(image_path, prompt="", timeout=GENERATION_TIMEOUT, device=None):
    """Generate video from image + optional prompt."""
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    if not is_app_installed(PACKAGE, device=device):
        return {
            "ok": False,
            "error": "app_not_installed",
            "install": (
                f"adb shell am start -a android.intent.action.VIEW "
                f"-d 'market://details?id={PACKAGE}'"
            ),
        }

    # Push image to device if local path
    remote_image = None
    if image_path and not image_path.startswith("/sdcard"):
        remote_image, err = _push_image_to_device(image_path, device=device)
        if err:
            return {"ok": False, "error": "image_push_failed", "detail": err}
    else:
        remote_image = image_path

    # Open app
    open_result = cmd_open(device=device)
    if not open_result["ok"]:
        return open_result

    if open_result.get("state") == "LOGIN":
        return {"ok": False, "error": "login_required"}

    # Navigate to create screen
    navigated, nodes = _navigate_to_create(device=device)

    # Look for Image to Video tab/button
    i2v_labels = ["Image to Video", "Image", "I2V", "Photo to Video"]
    for label in i2v_labels:
        btn = find_node(nodes, label=label, partial=True)
        if btn:
            tap_node(btn, device=device)
            time.sleep(1)
            nodes = dump_ui(device=device)
            break

    # Look for image upload button
    upload_labels = ["Upload", "Add image", "Choose image", "Select image", "Gallery", "+"]
    upload_btn = None
    for label in upload_labels:
        upload_btn = find_node(nodes, label=label, partial=True)
        if upload_btn:
            break

    ts_before = get_current_timestamp(device=device)

    if upload_btn:
        tap_node(upload_btn, device=device)
        time.sleep(2)

        # Handle file picker — try to navigate to the pushed image
        picker_nodes = dump_ui(device=device)
        # Look for gallery/recent
        gallery_btn = find_node(picker_nodes, label="Gallery", partial=True)
        if not gallery_btn:
            gallery_btn = find_node(picker_nodes, label="Recent", partial=True)
        if not gallery_btn:
            gallery_btn = find_node(picker_nodes, label="Photos", partial=True)

        if gallery_btn:
            tap_node(gallery_btn, device=device)
            time.sleep(1.5)

        # Tap on first image (most recent)
        picker_nodes = dump_ui(device=device)
        # Look for image items
        img_item = find_node(picker_nodes, cls="ImageView")
        if img_item:
            tap_node(img_item, device=device)
            time.sleep(1.5)
    else:
        screenshot = take_screenshot(device=device)
        return {
            "ok": False,
            "error": "upload_button_not_found",
            "screenshot_path": screenshot,
        }

    # Add prompt if provided
    if prompt:
        nodes = dump_ui(device=device)
        text_input = find_node(nodes, label="Describe motion", partial=True)
        if not text_input:
            text_input = find_node(nodes, label="Add caption", partial=True)
        if not text_input:
            text_input = find_node(nodes, label="Enter prompt", partial=True)
        if not text_input:
            text_input = find_node(nodes, cls="EditText")

        if text_input:
            tap_node(text_input, device=device)
            time.sleep(0.5)
            type_prompt(prompt, device=device)
            time.sleep(0.3)
            adb("shell", "input", "keyevent", "111", device=device)
            time.sleep(0.3)

    # Find generate button
    nodes = dump_ui(device=device)
    generate_btn = None
    for label in ["Generate", "Create", "Animate", "Submit"]:
        generate_btn = find_node(nodes, label=label, partial=True)
        if generate_btn and generate_btn["clickable"] == "true":
            break

    if generate_btn:
        tap_node(generate_btn, device=device)
    else:
        tap(360, 1580, device=device)

    time.sleep(2)

    # Check daily limit
    nodes = dump_ui(device=device)
    if detect_state(nodes) == "DAILY_LIMIT":
        return {"ok": False, "error": "daily_limit_reached", "resets_in": "24h"}

    # Wait for generation
    generation_start = time.time()
    generation_done = False

    while time.time() - generation_start < timeout:
        nodes = dump_ui(device=device)
        state = detect_state(nodes)

        if state == "DAILY_LIMIT":
            return {"ok": False, "error": "daily_limit_reached", "resets_in": "24h"}

        if state == "RESULT":
            generation_done = True
            break

        all_text = " ".join(n["text"] + " " + n["content-desc"] for n in nodes).lower()
        for phrase in ["failed", "error occurred", "try again"]:
            if phrase in all_text:
                screenshot = take_screenshot(device=device)
                return {"ok": False, "error": "generation_failed", "screenshot_path": screenshot}

        time.sleep(5)

    if not generation_done:
        nodes = dump_ui(device=device)
        if detect_state(nodes) != "RESULT":
            screenshot = take_screenshot(device=device)
            return {
                "ok": False,
                "error": "generation_timeout",
                "screenshot_path": screenshot,
            }

    # Download the video
    nodes = dump_ui(device=device)
    download_btn = find_node(nodes, label="Download", partial=True)
    if not download_btn:
        download_btn = find_node(nodes, label="Save", partial=True)

    if download_btn:
        tap_node(download_btn, device=device)
        time.sleep(2)
    else:
        screenshot = take_screenshot(device=device)
        return {"ok": False, "error": "download_button_not_found", "screenshot_path": screenshot}

    # Wait for and pull the video
    video_path = wait_for_video_file(ts_before, device=device, timeout=60)
    if not video_path:
        screenshot = take_screenshot(device=device)
        return {"ok": False, "error": "video_file_not_found", "screenshot_path": screenshot}

    local_path = pull_video(video_path, device=device)
    if not local_path:
        return {"ok": False, "error": "video_pull_failed", "remote_path": video_path}

    return {
        "ok": True,
        "video_path": local_path,
        "remote_path": video_path,
        "image_path": image_path,
        "prompt": prompt,
        "generation_time_s": round(time.time() - generation_start, 1),
    }


def cmd_screenshot(device=None):
    """Capture current screen."""
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    path = take_screenshot(device=device)
    if path:
        return {"ok": True, "screenshot_path": path}
    return {"ok": False, "error": "screenshot_failed"}


def cmd_scroll(direction="down", count=3, device=None):
    """Scroll the video feed."""
    ok, msg = adb_check(device=device)
    if not ok:
        return {"ok": False, "error": "device_not_found", "detail": msg}

    if direction == "down":
        scroll_down(device=device, count=count)
    elif direction == "up":
        scroll_up(device=device, count=count)
    else:
        return {"ok": False, "error": "invalid_direction", "valid": ["up", "down"]}

    return {"ok": True, "direction": direction, "count": count}


# ─── FastAPI Server ────────────────────────────────────────────────────────────

def cmd_server(port=SERVER_PORT, device=None):
    """Start FastAPI HTTP server."""
    try:
        from fastapi import FastAPI, Query
        from fastapi.responses import JSONResponse, FileResponse
        import uvicorn
        from pydantic import BaseModel
    except ImportError:
        print(json.dumps({
            "ok": False,
            "error": "missing_dependencies",
            "install": "pip install fastapi uvicorn pydantic",
        }))
        sys.exit(1)

    app = FastAPI(title="PixVerse Agent", version="1.0.0")

    class LoginRequest(BaseModel):
        method: str = "google"

    class Text2VideoRequest(BaseModel):
        prompt: str
        timeout: int = GENERATION_TIMEOUT

    class Image2VideoRequest(BaseModel):
        image_path: str
        prompt: str = ""
        timeout: int = GENERATION_TIMEOUT

    @app.get("/health")
    def health():
        return {"ok": True, "service": "pixverse-agent", "port": port}

    @app.get("/status")
    def status():
        return cmd_status(device=device)

    @app.post("/open")
    def open_app():
        return cmd_open(device=device)

    @app.post("/login")
    def login(req: LoginRequest):
        return cmd_login(method=req.method, device=device)

    @app.post("/text2video")
    def text2video(req: Text2VideoRequest):
        result = cmd_text2video(
            prompt=req.prompt,
            timeout=req.timeout,
            device=device,
        )
        return result

    @app.post("/image2video")
    def image2video(req: Image2VideoRequest):
        result = cmd_image2video(
            image_path=req.image_path,
            prompt=req.prompt,
            timeout=req.timeout,
            device=device,
        )
        return result

    @app.get("/screenshot")
    def screenshot():
        result = cmd_screenshot(device=device)
        if result["ok"]:
            path = result["screenshot_path"]
            if Path(path).exists():
                return FileResponse(path, media_type="image/png")
        return JSONResponse(result)

    @app.get("/scroll")
    def scroll(direction: str = Query("down"), count: int = Query(3)):
        return cmd_scroll(direction=direction, count=count, device=device)

    print(json.dumps({"ok": True, "server": "starting", "port": port, "device": device}))
    uvicorn.run(app, host="0.0.0.0", port=port)


# ─── CLI Entry Point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="PixVerse Android Automation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  status                  Check device and app status
  open                    Wake device and launch PixVerse
  login                   Sign in to PixVerse
  text2video              Generate video from text prompt
  image2video             Animate an image with optional prompt
  screenshot              Capture current screen
  scroll                  Scroll video feed
  server                  Start FastAPI server

Examples:
  python pixverse_agent.py status --device SGZTONV4OBL74TJZ
  python pixverse_agent.py text2video --prompt "A cat dancing in neon lights"
  python pixverse_agent.py image2video --image /path/to/image.jpg --prompt "Zoom out slowly"
  python pixverse_agent.py server --port 8775
        """,
    )
    parser.add_argument("command", help="Command to run")
    parser.add_argument("--device", default=DEFAULT_DEVICE, help="ADB device serial")
    parser.add_argument("--prompt", help="Text prompt for video generation")
    parser.add_argument("--image", help="Image path for image2video")
    parser.add_argument("--method", default="google", choices=["google", "email"],
                        help="Login method")
    parser.add_argument("--direction", default="down", choices=["up", "down"],
                        help="Scroll direction")
    parser.add_argument("--count", type=int, default=3, help="Number of scrolls")
    parser.add_argument("--timeout", type=int, default=GENERATION_TIMEOUT,
                        help="Generation timeout in seconds")
    parser.add_argument("--port", type=int, default=SERVER_PORT,
                        help="Server port")
    parser.add_argument("--json", action="store_true", help="Force JSON output")

    args = parser.parse_args()
    device = args.device if args.device != "auto" else None

    # Ensure downloads dir exists
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    cmd = args.command.lower()

    if cmd == "status":
        result = cmd_status(device=device)
    elif cmd == "open":
        result = cmd_open(device=device)
    elif cmd == "login":
        result = cmd_login(method=args.method, device=device)
    elif cmd == "text2video":
        if not args.prompt:
            result = {"ok": False, "error": "missing_argument", "detail": "--prompt is required"}
        else:
            result = cmd_text2video(
                prompt=args.prompt,
                timeout=args.timeout,
                device=device,
            )
    elif cmd == "image2video":
        if not args.image:
            result = {"ok": False, "error": "missing_argument", "detail": "--image is required"}
        else:
            result = cmd_image2video(
                image_path=args.image,
                prompt=args.prompt or "",
                timeout=args.timeout,
                device=device,
            )
    elif cmd == "screenshot":
        result = cmd_screenshot(device=device)
    elif cmd == "scroll":
        result = cmd_scroll(direction=args.direction, count=args.count, device=device)
    elif cmd == "server":
        cmd_server(port=args.port, device=device)
        return  # Server runs until killed
    else:
        result = {"ok": False, "error": "unknown_command", "command": cmd,
                  "valid": ["status", "open", "login", "text2video", "image2video",
                            "screenshot", "scroll", "server"]}

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
