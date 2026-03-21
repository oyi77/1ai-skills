#!/usr/bin/env python3
"""
Flow Agent — Google Flow (labs.google/flow) Android Automation
Automates video generation via Chrome browser on Android using ADB UIAutomation.

Usage:
  python flow_agent.py status [--device SERIAL]
  python flow_agent.py open [--device SERIAL]
  python flow_agent.py login [--device SERIAL]
  python flow_agent.py text2video --prompt "TEXT" [--timeout 120] [--device SERIAL]
  python flow_agent.py screenshot [--device SERIAL] [--out PATH]
  python flow_agent.py server [--port 8774] [--device SERIAL]
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import time
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime
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

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
FLOW_URL = "https://labs.google/flow"
CHROME_PKG = "com.android.chrome"
DEFAULT_DEVICE = "SGZTONV4OBL74TJZ"
DEFAULT_PORT = 8774
DOWNLOADS_DIR = os.path.expanduser("~/.openclaw/workspace/downloads")
SDCARD_DOWNLOAD = "/sdcard/Download"
XIAOMI_IME = "com.preff.kb.xm/com.preff.kb.LatinIME"
GBOARD_IME = "com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME"

# Ensure downloads dir exists
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
def log(msg: str):
    """Log progress to stderr."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def out(data: dict):
    """Output JSON result to stdout."""
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────
# ADB Core
# ─────────────────────────────────────────────
def adb(*args, device: Optional[str] = None, timeout: int = 30) -> str:
    """Run ADB command, return stdout string."""
    cmd = ["adb"]
    if device:
        cmd += ["-s", device]
    cmd += list(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        log(f"ADB timeout: {' '.join(cmd)}")
        return ""
    except FileNotFoundError:
        log("ERROR: adb not found in PATH")
        return ""


def adb_shell(cmd_str: str, device: Optional[str] = None, timeout: int = 30) -> str:
    """Run adb shell command string."""
    return adb("shell", cmd_str, device=device, timeout=timeout)


def screencap(out_path: str, device: Optional[str] = None) -> str:
    """Capture screenshot via ADB exec-out."""
    cmd = ["adb"]
    if device:
        cmd += ["-s", device]
    cmd += ["exec-out", "screencap", "-p"]
    try:
        raw = subprocess.run(cmd, capture_output=True, timeout=15)
        with open(out_path, "wb") as f:
            f.write(raw.stdout)
        return out_path
    except subprocess.TimeoutExpired:
        log("Screenshot timeout")
        return ""
    except Exception as e:
        log(f"Screenshot error: {e}")
        return ""


def get_devices() -> list:
    """List connected ADB devices."""
    result = adb("devices")
    lines = result.splitlines()
    devices = []
    for line in lines[1:]:
        if "\tdevice" in line:
            devices.append(line.split("\t")[0])
    return devices


# ─────────────────────────────────────────────
# Retry decorator
# ─────────────────────────────────────────────
def retry(func, attempts=3, delay=1.0, backoff=2.0):
    """Retry function with exponential backoff."""
    last_exc = None
    for i in range(attempts):
        try:
            result = func()
            if result is not None:
                return result
        except Exception as e:
            last_exc = e
            log(f"Attempt {i+1}/{attempts} failed: {e}")
        if i < attempts - 1:
            sleep_time = delay * (backoff ** i)
            log(f"Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)
    if last_exc:
        raise last_exc
    return None


# ─────────────────────────────────────────────
# UI Hierarchy Parsing
# ─────────────────────────────────────────────
def dump_ui(device: Optional[str] = None) -> Optional[ET.Element]:
    """Dump UI hierarchy and parse XML."""
    tmp_xml = "/tmp/flow_ui.xml"
    adb("shell", "uiautomator", "dump", "/sdcard/ui.xml", device=device, timeout=15)
    time.sleep(0.5)
    adb("pull", "/sdcard/ui.xml", tmp_xml, device=device, timeout=15)
    try:
        tree = ET.parse(tmp_xml)
        return tree.getroot()
    except Exception as e:
        log(f"XML parse error: {e}")
        return None


def find_element(root: ET.Element, **attrs) -> Optional[ET.Element]:
    """Find first element matching attribute criteria."""
    if root is None:
        return None
    for elem in root.iter("node"):
        match = True
        for key, val in attrs.items():
            elem_val = elem.get(key, "")
            if isinstance(val, str):
                if val.lower() not in elem_val.lower():
                    match = False
                    break
            elif callable(val):
                if not val(elem_val):
                    match = False
                    break
        if match:
            return elem
    return None


def find_elements(root: ET.Element, **attrs) -> list:
    """Find all elements matching attribute criteria."""
    results = []
    if root is None:
        return results
    for elem in root.iter("node"):
        match = True
        for key, val in attrs.items():
            elem_val = elem.get(key, "")
            if isinstance(val, str):
                if val.lower() not in elem_val.lower():
                    match = False
                    break
            elif callable(val):
                if not val(elem_val):
                    match = False
                    break
        if match:
            results.append(elem)
    return results


def get_bounds(elem: ET.Element) -> Optional[tuple]:
    """Parse bounds attribute '[x1,y1][x2,y2]' → (cx, cy)."""
    bounds = elem.get("bounds", "")
    if not bounds:
        return None
    try:
        parts = bounds.replace("][", ",").replace("[", "").replace("]", "")
        x1, y1, x2, y2 = map(int, parts.split(","))
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        return (cx, cy)
    except Exception:
        return None


def tap(x: int, y: int, device: Optional[str] = None):
    """Tap at coordinates."""
    adb("shell", "input", "tap", str(x), str(y), device=device)
    time.sleep(0.4)


def tap_element(elem: ET.Element, device: Optional[str] = None) -> bool:
    """Tap the center of a UI element."""
    coords = get_bounds(elem)
    if coords:
        tap(coords[0], coords[1], device=device)
        return True
    return False


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300,
          device: Optional[str] = None):
    """Swipe from (x1,y1) to (x2,y2)."""
    adb("shell", "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration_ms),
        device=device)
    time.sleep(0.3)


def press_back(device: Optional[str] = None):
    adb("shell", "input", "keyevent", "4", device=device)
    time.sleep(0.3)


def press_home(device: Optional[str] = None):
    adb("shell", "input", "keyevent", "3", device=device)
    time.sleep(0.3)


# ─────────────────────────────────────────────
# Keyboard Input
# ─────────────────────────────────────────────
def set_xiaomi_keyboard(device: Optional[str] = None):
    """Switch to Xiaomi keyboard to avoid autocorrect issues."""
    adb("shell", "settings", "put", "secure", "default_input_method",
        XIAOMI_IME, device=device)
    time.sleep(0.3)


def set_gboard(device: Optional[str] = None):
    """Switch back to Gboard."""
    adb("shell", "settings", "put", "secure", "default_input_method",
        GBOARD_IME, device=device)
    time.sleep(0.3)


def type_text_safe(text: str, device: Optional[str] = None):
    """
    Type text word by word using Xiaomi keyboard to avoid autocorrect.
    Handles special characters via escape.
    """
    set_xiaomi_keyboard(device=device)
    time.sleep(0.5)

    words = text.split()
    for i, word in enumerate(words):
        # Escape shell-special characters
        escaped = word.replace("'", "\\'").replace('"', '\\"').replace(
            "&", "\\&").replace("|", "\\|").replace(";", "\\;").replace(
            "(", "\\(").replace(")", "\\)").replace("<", "\\<").replace(
            ">", "\\>").replace("`", "\\`").replace("$", "\\$").replace(
            " ", "%s")

        adb("shell", "input", "text", escaped, device=device)
        time.sleep(0.2)

        # Add space between words (not after last word)
        if i < len(words) - 1:
            adb("shell", "input", "keyevent", "62", device=device)  # SPACE
            time.sleep(0.15)

    log(f"Typed: {text[:60]}{'...' if len(text) > 60 else ''}")


def clear_field(device: Optional[str] = None):
    """Clear current text field (select all + delete)."""
    adb("shell", "input", "keyevent", "KEYCODE_CTRL_A", device=device)
    time.sleep(0.2)
    adb("shell", "input", "keyevent", "KEYCODE_DEL", device=device)
    time.sleep(0.2)


# ─────────────────────────────────────────────
# Chrome Navigation
# ─────────────────────────────────────────────
def open_url_in_chrome(url: str, device: Optional[str] = None):
    """Open URL in Chrome browser."""
    log(f"Opening: {url}")
    adb("shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", url,
        CHROME_PKG,
        device=device)
    time.sleep(2.5)


def is_chrome_running(device: Optional[str] = None) -> bool:
    """Check if Chrome is running."""
    result = adb("shell", "pidof", CHROME_PKG, device=device)
    return bool(result.strip())


def get_current_url(device: Optional[str] = None) -> str:
    """Try to get current URL from Chrome address bar via UI dump."""
    root = dump_ui(device=device)
    if root is None:
        return ""
    # Look for address bar
    for elem in root.iter("node"):
        res_id = elem.get("resource-id", "")
        if "url_bar" in res_id or "location_bar" in res_id or "omnibox" in res_id:
            return elem.get("text", "")
    return ""


def chrome_navigate_addressbar(url: str, device: Optional[str] = None):
    """Navigate Chrome to URL via address bar."""
    root = dump_ui(device=device)
    if root is None:
        log("Cannot dump UI for address bar navigation")
        return

    # Find address bar
    addr_bar = find_element(root, **{"resource-id": "com.android.chrome:id/url_bar"})
    if addr_bar is None:
        addr_bar = find_element(root, **{"resource-id": "com.android.chrome:id/location_bar_edit_text"})

    if addr_bar:
        tap_element(addr_bar, device=device)
        time.sleep(0.5)
        clear_field(device=device)
        type_text_safe(url, device=device)
        adb("shell", "input", "keyevent", "66", device=device)  # ENTER
        time.sleep(3.0)
    else:
        # Fallback: use intent
        open_url_in_chrome(url, device=device)


def wait_for_page_load(keyword: str, device: Optional[str] = None,
                       timeout: int = 20) -> bool:
    """Wait until UI contains a keyword (page loaded)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        root = dump_ui(device=device)
        if root is None:
            time.sleep(1)
            continue
        xml_str = ET.tostring(root, encoding="unicode")
        if keyword.lower() in xml_str.lower():
            return True
        time.sleep(1.5)
    return False


# ─────────────────────────────────────────────
# Flow-Specific UI Detection
# ─────────────────────────────────────────────
def detect_flow_state(device: Optional[str] = None) -> dict:
    """
    Detect current state of Flow page.
    Returns dict with keys: loaded, login_required, credits_exhausted,
    has_input, has_generate_btn, generating, done, error_msg
    """
    state = {
        "loaded": False,
        "login_required": False,
        "credits_exhausted": False,
        "has_input": False,
        "has_generate_btn": False,
        "generating": False,
        "done": False,
        "error_msg": "",
    }

    root = dump_ui(device=device)
    if root is None:
        return state

    xml_str = ET.tostring(root, encoding="unicode").lower()

    # Check if Flow page is loaded
    if "flow" in xml_str and ("labs.google" in xml_str or "generate" in xml_str or
                               "text to video" in xml_str or "video" in xml_str):
        state["loaded"] = True

    # Check login required
    if ("sign in" in xml_str or "google account" in xml_str or
            "log in" in xml_str or "accounts.google.com" in xml_str):
        state["login_required"] = True

    # Check credits exhausted
    if ("credit" in xml_str and ("0" in xml_str or "out" in xml_str or
                                   "exhausted" in xml_str or "daily limit" in xml_str)):
        state["credits_exhausted"] = True

    # Check for text input area
    for elem in root.iter("node"):
        cls = elem.get("class", "").lower()
        hint = elem.get("hint", "").lower()
        text = elem.get("text", "").lower()
        if cls in ("android.widget.edittext", "android.widget.multiautocompletetextview"):
            state["has_input"] = True
        if "describe" in hint or "prompt" in hint or "text to video" in hint:
            state["has_input"] = True
        if "describe" in text or "enter" in text:
            state["has_input"] = True

    # Check for Generate button
    for elem in root.iter("node"):
        text = elem.get("text", "").lower()
        content_desc = elem.get("content-desc", "").lower()
        if "generate" in text or "generate" in content_desc:
            state["has_generate_btn"] = True

    # Check if generating (progress indicators)
    if ("progress" in xml_str or "loading" in xml_str or "generating" in xml_str or
            "processing" in xml_str or "wait" in xml_str):
        state["generating"] = True

    # Check if video ready (download button present)
    for elem in root.iter("node"):
        text = elem.get("text", "").lower()
        cd = elem.get("content-desc", "").lower()
        if "download" in text or "download" in cd or "save" in text:
            state["done"] = True

    return state


def find_text_input(root: ET.Element) -> Optional[ET.Element]:
    """Find the text input field on Flow page."""
    if root is None:
        return None

    # Priority: EditText with prompt-related hints
    for elem in root.iter("node"):
        cls = elem.get("class", "")
        hint = elem.get("hint", "").lower()
        if "EditText" in cls:
            if any(k in hint for k in ["describe", "prompt", "text", "video", "enter"]):
                return elem

    # Second: any EditText
    for elem in root.iter("node"):
        cls = elem.get("class", "")
        if "EditText" in cls:
            return elem

    # Third: clickable content area with placeholder text
    for elem in root.iter("node"):
        text = elem.get("text", "").lower()
        clickable = elem.get("clickable", "")
        if clickable == "true" and any(k in text for k in ["describe", "type", "enter", "prompt"]):
            return elem

    return None


def find_generate_button(root: ET.Element) -> Optional[ET.Element]:
    """Find the Generate button."""
    if root is None:
        return None

    for elem in root.iter("node"):
        text = elem.get("text", "").lower()
        cd = elem.get("content-desc", "").lower()
        clickable = elem.get("clickable", "")
        if clickable == "true" and ("generate" in text or "generate" in cd):
            return elem

    return None


def find_download_button(root: ET.Element) -> Optional[ET.Element]:
    """Find the Download button."""
    if root is None:
        return None

    for elem in root.iter("node"):
        text = elem.get("text", "").lower()
        cd = elem.get("content-desc", "").lower()
        clickable = elem.get("clickable", "")
        if clickable == "true" and ("download" in text or "download" in cd):
            return elem

    return None


# ─────────────────────────────────────────────
# File Download Helpers
# ─────────────────────────────────────────────
def list_mp4_on_device(device: Optional[str] = None) -> list:
    """List all MP4 files in /sdcard/Download on device."""
    result = adb("shell", f"find {SDCARD_DOWNLOAD} -name '*.mp4' 2>/dev/null",
                 device=device)
    files = [f.strip() for f in result.splitlines() if f.strip()]
    return files


def wait_for_new_mp4(existing_files: list, device: Optional[str] = None,
                     timeout: int = 60) -> Optional[str]:
    """Wait for a new MP4 file to appear in /sdcard/Download."""
    existing_set = set(existing_files)
    deadline = time.time() + timeout
    log(f"Waiting for MP4 download (timeout={timeout}s)...")

    while time.time() < deadline:
        current = list_mp4_on_device(device=device)
        new_files = [f for f in current if f not in existing_set]
        if new_files:
            # Return the newest one
            log(f"New MP4 detected: {new_files[0]}")
            return new_files[0]
        time.sleep(2)

    return None


def pull_video_from_device(device_path: str, device: Optional[str] = None) -> str:
    """Pull video file from device to local downloads directory."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_path = os.path.join(DOWNLOADS_DIR, f"flow_video_{ts}.mp4")
    log(f"Pulling {device_path} → {local_path}")
    adb("pull", device_path, local_path, device=device, timeout=60)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return local_path
    return ""


# ─────────────────────────────────────────────
# Command: status
# ─────────────────────────────────────────────
def cmd_status(device: Optional[str] = None) -> dict:
    """Check device connection and Chrome status."""
    log("Checking status...")

    devices = get_devices()
    if not devices:
        return {"ok": False, "error": "no_device", "message": "No ADB devices connected"}

    target_device = device or DEFAULT_DEVICE
    if target_device not in devices and len(devices) == 1:
        target_device = devices[0]

    if target_device not in devices:
        return {
            "ok": False,
            "error": "device_not_found",
            "device": target_device,
            "available_devices": devices
        }

    # Get device info
    model = adb("shell", "getprop", "ro.product.model", device=target_device)
    android_ver = adb("shell", "getprop", "ro.build.version.release", device=target_device)
    chrome_running = is_chrome_running(device=target_device)

    # Check Chrome version
    chrome_ver = adb("shell", "dumpsys", "package", CHROME_PKG, device=target_device)
    ver_line = ""
    for line in chrome_ver.splitlines():
        if "versionName" in line:
            ver_line = line.strip()
            break

    return {
        "ok": True,
        "device": target_device,
        "model": model,
        "android_version": android_ver,
        "chrome_running": chrome_running,
        "chrome_version": ver_line,
        "adb_devices": devices,
    }


# ─────────────────────────────────────────────
# Command: open
# ─────────────────────────────────────────────
def cmd_open(url: str = FLOW_URL, device: Optional[str] = None,
             timeout: int = 30) -> dict:
    """Open Chrome and navigate to Flow."""
    log(f"Opening {url} in Chrome...")
    target_device = device or DEFAULT_DEVICE

    def _open():
        open_url_in_chrome(url, device=target_device)
        time.sleep(2)
        return True

    try:
        retry(_open, attempts=3, delay=1.0)
    except Exception as e:
        return {"ok": False, "error": "open_failed", "message": str(e)}

    # Wait for page to load
    log("Waiting for page to load...")
    loaded = wait_for_page_load("flow", device=target_device, timeout=timeout)

    state = detect_flow_state(device=target_device)

    return {
        "ok": True,
        "url": url,
        "page_loaded": loaded,
        "state": state,
    }


# ─────────────────────────────────────────────
# Command: login
# ─────────────────────────────────────────────
def cmd_login(device: Optional[str] = None, timeout: int = 60) -> dict:
    """
    Handle Google login flow.
    NOTE: Actual credential entry must be done manually by user.
    This command checks login state and guides the process.
    """
    target_device = device or DEFAULT_DEVICE
    log("Checking login state...")

    state = detect_flow_state(device=target_device)

    if not state["login_required"]:
        return {
            "ok": True,
            "message": "Already logged in or login not required",
            "state": state,
        }

    # Take screenshot to show current state
    ss_path = os.path.join(tempfile.gettempdir(), f"flow_login_{int(time.time())}.png")
    screencap(ss_path, device=target_device)

    log("Login required. Opening login page...")
    # Navigate to Google sign-in
    open_url_in_chrome("https://accounts.google.com", device=target_device)
    time.sleep(3)

    return {
        "ok": False,
        "error": "login_required",
        "login_url": "https://accounts.google.com",
        "message": "Please complete Google login manually. Screenshot saved.",
        "screenshot_path": ss_path,
        "instructions": [
            "1. Complete Google sign-in on the device",
            "2. Return to labs.google/flow",
            "3. Run 'open' command again",
        ]
    }


# ─────────────────────────────────────────────
# Command: screenshot
# ─────────────────────────────────────────────
def cmd_screenshot(out: Optional[str] = None, device: Optional[str] = None) -> dict:
    """Capture screenshot of current screen."""
    target_device = device or DEFAULT_DEVICE

    if out is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = os.path.join(DOWNLOADS_DIR, f"flow_screenshot_{ts}.png")

    log(f"Capturing screenshot → {out}")
    result = screencap(out, device=target_device)

    if not result or not os.path.exists(out):
        return {"ok": False, "error": "screenshot_failed", "path": out}

    size = os.path.getsize(out)
    return {
        "ok": True,
        "screenshot_path": out,
        "size_bytes": size,
    }


# ─────────────────────────────────────────────
# Command: text2video (main)
# ─────────────────────────────────────────────
def cmd_text2video(prompt: str, device: Optional[str] = None,
                   timeout: int = 120) -> dict:
    """
    Main command: Generate video from text prompt using Google Flow.
    Steps:
    1. Open Flow in Chrome
    2. Find text input → type prompt
    3. Click Generate
    4. Wait for generation (up to timeout)
    5. Click Download
    6. Pull MP4 to local downloads
    """
    # AI Interceptor: enhance prompt if available (fail-safe)
    if AI_INTERCEPT_ENABLED and _interceptor:
        try:
            prompt = _interceptor.intercept(skill_type="flow_gen")(lambda p: p)(prompt)
        except Exception:
            pass
    if not prompt or not prompt.strip():
        return {"ok": False, "error": "empty_prompt", "message": "Prompt cannot be empty"}

    target_device = device or DEFAULT_DEVICE
    prompt = prompt.strip()
    log(f"Starting text2video: '{prompt[:60]}...' (timeout={timeout}s)")

    # Step 1: Open Flow
    log("Step 1: Opening Google Flow...")
    open_result = cmd_open(FLOW_URL, device=target_device, timeout=30)
    if not open_result["ok"]:
        return open_result

    state = open_result.get("state", {})

    # Check login required
    if state.get("login_required"):
        ss_path = _take_screenshot(target_device, "login_required")
        return {
            "ok": False,
            "error": "login_required",
            "login_url": "https://accounts.google.com",
            "screenshot_path": ss_path,
        }

    # Check credits exhausted
    if state.get("credits_exhausted"):
        ss_path = _take_screenshot(target_device, "no_credits")
        return {
            "ok": False,
            "error": "credits_exhausted",
            "credits_remaining": 0,
            "screenshot_path": ss_path,
        }

    # Step 2: Wait for page to fully load
    log("Step 2: Waiting for Flow UI to be ready...")
    ui_ready = _wait_for_flow_ui(target_device, timeout=20)
    if not ui_ready:
        log("Flow UI not detected, attempting to scroll/refresh...")
        # Try scrolling down in case content is below fold
        swipe(360, 800, 360, 400, device=target_device)
        time.sleep(1.5)
        ui_ready = _wait_for_flow_ui(target_device, timeout=10)

    # Step 3: Find and tap text input
    log("Step 3: Finding text input field...")
    root = dump_ui(device=target_device)
    input_elem = find_text_input(root)

    if input_elem is None:
        log("Text input not found, trying to scroll and find...")
        swipe(360, 900, 360, 300, device=target_device)
        time.sleep(1.5)
        root = dump_ui(device=target_device)
        input_elem = find_text_input(root)

    if input_elem is None:
        ss_path = _take_screenshot(target_device, "no_input")
        log("ERROR: Text input not found on page")
        return {
            "ok": False,
            "error": "ui_not_found",
            "message": "Could not find text input on Flow page",
            "screenshot_path": ss_path,
        }

    # Tap input field
    log("Tapping text input field...")
    tap_element(input_elem, device=target_device)
    time.sleep(0.8)

    # Step 4: Type the prompt
    log("Step 4: Typing prompt...")
    clear_field(device=target_device)
    time.sleep(0.3)
    type_text_safe(prompt, device=target_device)
    time.sleep(0.5)

    # Verify text was entered by checking UI
    root = dump_ui(device=target_device)
    ss_after_type = _take_screenshot(target_device, "after_type")

    # Step 5: Find and click Generate button
    log("Step 5: Looking for Generate button...")
    root = dump_ui(device=target_device)
    gen_btn = find_generate_button(root)

    if gen_btn is None:
        # Scroll down to find button
        log("Generate button not visible, scrolling...")
        swipe(360, 1200, 360, 600, device=target_device)
        time.sleep(1.0)
        root = dump_ui(device=target_device)
        gen_btn = find_generate_button(root)

    if gen_btn is None:
        # Try coordinate-based tap at bottom area where Generate usually is
        log("Generate button not found via UI, trying bottom area tap...")
        ss_path = _take_screenshot(target_device, "no_generate_btn")
        # Try common positions for Generate button
        for y_pos in [1400, 1300, 1500, 1200]:
            tap(360, y_pos, device=target_device)
            time.sleep(0.5)
            root = dump_ui(device=target_device)
            state = detect_flow_state(device=target_device)
            if state.get("generating"):
                log("Generation started (via coordinate tap)")
                break
        else:
            return {
                "ok": False,
                "error": "generate_btn_not_found",
                "message": "Could not find Generate button",
                "screenshot_path": ss_path,
            }
    else:
        log("Clicking Generate button...")
        tap_element(gen_btn, device=target_device)
        time.sleep(1.0)

    # Record existing MP4 files before download
    existing_mp4s = list_mp4_on_device(device=target_device)
    log(f"Existing MP4s on device: {len(existing_mp4s)}")

    # Step 6: Wait for generation to complete
    log(f"Step 6: Waiting for generation (timeout={timeout}s)...")
    gen_result = _wait_for_generation(target_device, timeout=timeout)

    if gen_result == "credits_exhausted":
        ss_path = _take_screenshot(target_device, "credits_exhausted")
        return {
            "ok": False,
            "error": "credits_exhausted",
            "credits_remaining": 0,
            "screenshot_path": ss_path,
        }

    if gen_result == "timeout":
        ss_path = _take_screenshot(target_device, "timeout")
        return {
            "ok": False,
            "error": "timeout",
            "message": f"Video generation timed out after {timeout}s",
            "screenshot_path": ss_path,
        }

    if gen_result == "error":
        ss_path = _take_screenshot(target_device, "gen_error")
        return {
            "ok": False,
            "error": "generation_failed",
            "message": "Generation failed or errored",
            "screenshot_path": ss_path,
        }

    log("Generation complete! Looking for Download button...")

    # Step 7: Find and click Download
    time.sleep(1.0)
    root = dump_ui(device=target_device)
    dl_btn = find_download_button(root)

    if dl_btn is None:
        # Scroll to find it
        swipe(360, 800, 360, 400, device=target_device)
        time.sleep(1.0)
        root = dump_ui(device=target_device)
        dl_btn = find_download_button(root)

    if dl_btn is None:
        ss_path = _take_screenshot(target_device, "no_download_btn")
        log("Download button not found, video may be on screen")
        return {
            "ok": True,
            "video_path": None,
            "screenshot_path": ss_path,
            "note": "video_on_screen",
            "message": "Video generated but download button not found. Check screenshot.",
        }

    log("Clicking Download button...")
    tap_element(dl_btn, device=target_device)
    time.sleep(2.0)

    # Handle download confirmation dialog if any
    root = dump_ui(device=target_device)
    for elem in root.iter("node"):
        text = elem.get("text", "").lower()
        if text in ("ok", "download", "save", "confirm", "yes"):
            clickable = elem.get("clickable", "")
            if clickable == "true":
                tap_element(elem, device=target_device)
                time.sleep(1.0)
                break

    # Step 8: Wait for MP4 to appear in /sdcard/Download
    log("Step 8: Waiting for MP4 to download to device...")
    new_mp4 = wait_for_new_mp4(existing_mp4s, device=target_device, timeout=60)

    if new_mp4 is None:
        ss_path = _take_screenshot(target_device, "download_wait_timeout")
        return {
            "ok": True,
            "video_path": None,
            "screenshot_path": ss_path,
            "note": "video_on_screen",
            "message": "Download not detected in 60s. Video may still be downloading.",
        }

    # Step 9: Pull file to local machine
    log("Step 9: Pulling video to local machine...")
    local_path = pull_video_from_device(new_mp4, device=target_device)

    if not local_path:
        return {
            "ok": False,
            "error": "pull_failed",
            "device_path": new_mp4,
            "message": "File exists on device but pull failed",
        }

    log(f"✓ Video saved: {local_path}")

    return {
        "ok": True,
        "video_path": local_path,
        "device_path": new_mp4,
        "prompt": prompt,
        "timestamp": datetime.now().isoformat(),
    }


# ─────────────────────────────────────────────
# Helper functions for text2video
# ─────────────────────────────────────────────
def _take_screenshot(device: Optional[str], label: str = "") -> str:
    """Take screenshot and return path."""
    ts = int(time.time())
    path = os.path.join(DOWNLOADS_DIR, f"flow_{label}_{ts}.png")
    screencap(path, device=device)
    return path


def _wait_for_flow_ui(device: Optional[str], timeout: int = 20) -> bool:
    """Wait until Flow UI is ready (input or generate button visible)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        state = detect_flow_state(device=device)
        if state.get("has_input") or state.get("has_generate_btn"):
            return True
        if state.get("login_required"):
            return False
        time.sleep(2)
    return False


def _wait_for_generation(device: Optional[str], timeout: int = 120) -> str:
    """
    Wait for video generation to complete.
    Returns: 'done', 'timeout', 'error', 'credits_exhausted'
    """
    deadline = time.time() + timeout
    poll_interval = 3.0
    last_log = time.time()

    while time.time() < deadline:
        state = detect_flow_state(device=device)

        elapsed = time.time() - (deadline - timeout)
        if time.time() - last_log > 15:
            log(f"  Generating... ({elapsed:.0f}s elapsed, state: {state})")
            last_log = time.time()

        if state.get("credits_exhausted"):
            return "credits_exhausted"

        if state.get("done"):
            return "done"

        # Check for error states
        root = dump_ui(device=device)
        if root is not None:
            xml_str = ET.tostring(root, encoding="unicode").lower()
            if "error" in xml_str and "retry" in xml_str:
                return "error"
            if "failed" in xml_str and "generate" in xml_str:
                return "error"

        time.sleep(poll_interval)

    return "timeout"


# ─────────────────────────────────────────────
# FastAPI Server
# ─────────────────────────────────────────────
def cmd_server(port: int = DEFAULT_PORT, device: Optional[str] = None):
    """Start FastAPI server."""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import FileResponse, JSONResponse
        import uvicorn
        from pydantic import BaseModel
    except ImportError:
        log("ERROR: fastapi and uvicorn required. Install: pip install fastapi uvicorn")
        sys.exit(1)

    app = FastAPI(
        title="Flow Agent API",
        description="Google Flow video generation via Android ADB",
        version="1.0.0"
    )

    target_device = device or DEFAULT_DEVICE

    class Text2VideoRequest(BaseModel):
        prompt: str
        timeout: int = 120
        device: Optional[str] = None

    class OpenRequest(BaseModel):
        url: str = FLOW_URL

    @app.get("/health")
    def health():
        return {"ok": True, "service": "flow-agent", "version": "1.0.0"}

    @app.get("/status")
    def status():
        d = device or DEFAULT_DEVICE
        result = cmd_status(device=d)
        return result

    @app.post("/open")
    def open_flow(req: OpenRequest):
        d = device or DEFAULT_DEVICE
        result = cmd_open(url=req.url, device=d)
        return result

    @app.post("/text2video")
    def text2video(req: Text2VideoRequest):
        d = req.device or device or DEFAULT_DEVICE
        result = cmd_text2video(
            prompt=req.prompt,
            device=d,
            timeout=req.timeout
        )
        return result

    @app.get("/screenshot")
    def screenshot():
        d = device or DEFAULT_DEVICE
        result = cmd_screenshot(device=d)
        if result["ok"] and os.path.exists(result["screenshot_path"]):
            return FileResponse(
                result["screenshot_path"],
                media_type="image/png",
                filename="screenshot.png"
            )
        return JSONResponse(result, status_code=500)

    log(f"Starting Flow Agent server on port {port}...")
    log(f"Device: {target_device}")
    log(f"Endpoints: GET /health, GET /status, POST /text2video, GET /screenshot, POST /open")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Flow Agent — Google Flow video generation via Android ADB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--device", "-d", default=DEFAULT_DEVICE,
                        help=f"ADB device serial (default: {DEFAULT_DEVICE})")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # status
    subparsers.add_parser("status", help="Check device and Chrome status")

    # open
    p_open = subparsers.add_parser("open", help="Open Chrome → labs.google/flow")
    p_open.add_argument("--url", default=FLOW_URL, help="URL to open")
    p_open.add_argument("--timeout", type=int, default=30, help="Page load timeout")

    # login
    p_login = subparsers.add_parser("login", help="Handle Google login")
    p_login.add_argument("--timeout", type=int, default=60)

    # text2video
    p_t2v = subparsers.add_parser("text2video", help="Generate video from text prompt")
    p_t2v.add_argument("--prompt", "-p", required=True, help="Text prompt for video")
    p_t2v.add_argument("--timeout", type=int, default=120,
                        help="Generation timeout in seconds (default: 120)")

    # screenshot
    p_ss = subparsers.add_parser("screenshot", help="Capture current screen")
    p_ss.add_argument("--out", "-o", default=None, help="Output path for PNG")

    # server
    p_srv = subparsers.add_parser("server", help="Start FastAPI server")
    p_srv.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"Port (default: {DEFAULT_PORT})")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    device = args.device

    if args.command == "status":
        result = cmd_status(device=device)
        out(result)

    elif args.command == "open":
        result = cmd_open(url=args.url, device=device, timeout=args.timeout)
        out(result)

    elif args.command == "login":
        result = cmd_login(device=device, timeout=args.timeout)
        out(result)

    elif args.command == "text2video":
        result = cmd_text2video(
            prompt=args.prompt,
            device=device,
            timeout=args.timeout
        )
        out(result)

    elif args.command == "screenshot":
        result = cmd_screenshot(out=args.out, device=device)
        out(result)

    elif args.command == "server":
        cmd_server(port=args.port, device=device)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
