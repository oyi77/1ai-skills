#!/usr/bin/env python3
"""
Kling AI Android Automation Agent — Production Rewrite v2.0
============================================================
Based on live testing sessions on Redmi Note 12, Android 14, 720x1640px.

App:     Kling AI: AI Image&Video (Kling 3.0)
Package: kling.ai.video.chat
Activity: kling.ai.video.chat/.MainActivityPagerActivity
Device:  Redmi Note 12, Android 14, 720x1640
Serial:  SGZTONV4OBL74TJZ
Login:   favstore649@gmail.com (Google OAuth)

CLI Usage:
    python kling_agent.py t2v --prompt "text" [--duration 5] [--device SERIAL]
    python kling_agent.py i2v --image /path/img.jpg [--motion "Chinese trend"] [--prompt "text"]
    python kling_agent.py credits
    python kling_agent.py status
    python kling_agent.py download
    python kling_agent.py screenshot [--out /path/file.png]

Output JSON:
    {"status": "success", "type": "t2v", "output": "/path/video.mp4", "credits_used": 144, "duration_seconds": 47}
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("kling_agent")

# ─── AI Interceptor Integration (fail-safe) ───────────────────────────────────

try:
    import sys as _sys
    _sys.path.insert(0, '/mnt/data/berkahkarya/skills/1ai-skills/automation/ai-interceptor/scripts')
    from adb_interceptor import ADBInterceptor
    from prompt_interceptor import PromptInterceptor
    _adb_interceptor = ADBInterceptor(
        device_serial="SGZTONV4OBL74TJZ",
        target_package="kling.ai.video.chat",
        target_activity="kling.ai.video.chat/com.yxcorp.gifshow.kling.KLingHomeActivity"
    )
    _prompt_interceptor = PromptInterceptor()
    AI_INTERCEPT_ENABLED = True
    logging.getLogger("kling_agent").info("AI Interceptor enabled")
except Exception as _ai_exc:
    AI_INTERCEPT_ENABLED = False
    _adb_interceptor = None
    _prompt_interceptor = None

# ─── Video Enhancer Integration (fail-safe) ───────────────────────────────────

try:
    from video_enhancer import VideoEnhancer
    _video_enhancer = VideoEnhancer()
    VIDEO_ENHANCE_ENABLED = True
    logging.getLogger("kling_agent").info("Video Enhancer enabled")
except Exception as _ve_exc:
    VIDEO_ENHANCE_ENABLED = False
    _video_enhancer = None

# ─── Constants ────────────────────────────────────────────────────────────────

PACKAGE         = "kling.ai.video.chat"
ACTIVITY        = "kling.ai.video.chat/com.yxcorp.gifshow.kling.KLingHomeActivity"  # Confirmed via adb
ACTIVITY_ALT    = "kling.ai.video.chat/.MainActivityPagerActivity"  # Also works via monkey

DEFAULT_DEVICE  = "SGZTONV4OBL74TJZ"
DEFAULT_PORT    = 8775

SCREEN_W        = 720
SCREEN_H        = 1640

# Output directory
DOWNLOADS = Path.home() / ".openclaw/workspace/downloads"
DOWNLOADS.mkdir(parents=True, exist_ok=True)

ADB = "adb"

# ─── EXACT Navigation Coordinates (Confirmed from live testing) ──────────────
# Device nav bar starts at ~y=1540 — DO NOT tap below this!

NAV_HOME        = (72,  1413)   # Home tab
NAV_EXPLORE     = (216, 1413)   # Explore tab
NAV_CREATE      = (263, 1413)   # Create (+) button — MAIN
NAV_CREATE_ALT  = (263, 1052)   # Create (+) alternate position (floating)
NAV_ASSETS      = (368, 1413)   # Assets tab
NAV_MY_SPACE    = (476, 1413)   # My Space tab

# ─── I2V Motion Control Interface Coordinates ────────────────────────────────
# Accessed via Create (+) button

I2V_ADD_IMAGE_Y     = 355       # "Add Character Image" upload box (y-coord)
I2V_MOTION_Y_MIN    = 615       # Motion templates row start
I2V_MOTION_Y_MAX    = 665       # Motion templates row end
I2V_PROMPT_Y        = 800       # Prompt text field
I2V_GENERATE_X      = 573       # Generate button center X (parent is clickable)
I2V_GENERATE_Y      = 843       # Generate button center Y
I2V_RESET_X         = 134       # Reset button X
I2V_RESET_Y         = 746       # Reset button Y

# ─── Omni Mode (T2V green send arrow) ────────────────────────────────────────
OMNI_SEND_X     = 644           # Green ImageView X
OMNI_SEND_Y     = 1362          # Green ImageView Y
OMNI_SEND_BOUNDS = (616, 1334, 672, 1390)  # [x1,y1][x2,y2]

# ─── Gallery Upload Coordinates ──────────────────────────────────────────────
GALLERY_PERMISSION_X    = 360   # "Izinkan semua" X
GALLERY_PERMISSION_Y    = 1304  # "Izinkan semua" Y
GALLERY_DONE_X          = 589   # "Done(1)" X
GALLERY_DONE_Y          = 1303  # "Done(1)" Y

# Gallery grid: 4 cols x 180px wide
GALLERY_COL_X           = [90, 270, 450, 630]   # Col centers
GALLERY_ROW1_Y          = 167   # Row 1 (CAMERA — AVOID!)
GALLERY_ROW2_Y          = 300   # Row 2 (most recent photo)
GALLERY_ROW3_Y          = 420   # Row 3
GALLERY_ROW4_Y          = 540   # Row 4

# ─── Screen State Text Markers (from live UI dumps) ──────────────────────────
HOME_MARKERS        = ["Omni", "AI Image", "AI Video", "For You", "Trending"]
CREATOR_MARKERS     = ["Generate", "Add Character Image", "Describe your video", "Motion"]
GALLERY_MARKERS     = ["Camera roll", "Done", "Izinkan semua", "Allow all"]
PROCESSING_MARKERS  = ["Generating", "Processing", "Please wait", "0%", "25%", "50%", "75%"]
VIDEO_RESULT_MARKERS = ["Download", "Save to", "Share", "Video ready"]

# ─── Motion Template Names (I2V) ─────────────────────────────────────────────
MOTION_TEMPLATES = [
    "Chinese trend",
    "Slight movement",
    "Zoom in",
    "Zoom out",
    "Pan left",
    "Pan right",
    "Rotate",
    "Wave",
]

# ─── Core ADB Helpers ─────────────────────────────────────────────────────────

def adb(*args, device: str = None, timeout: int = 30) -> str:
    """Run ADB command, return stdout as string. Empty string on failure."""
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += list(str(a) for a in args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        log.warning(f"ADB timeout: {' '.join(cmd)}")
        return ""
    except Exception as e:
        log.debug(f"ADB error: {e}")
        return ""


def adb_rc(*args, device: str = None, timeout: int = 30) -> Tuple[str, int]:
    """Run ADB command, return (stdout, returncode)."""
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += list(str(a) for a in args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", 1
    except Exception:
        return "", 1


def screencap(out_path: str, device: str = None) -> str:
    """Capture screenshot via exec-out (no temp file on device)."""
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += ["exec-out", "screencap", "-p"]
    try:
        raw = subprocess.run(cmd, capture_output=True, timeout=15)
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(raw.stdout)
        return out_path
    except Exception as e:
        log.warning(f"screencap failed: {e}")
        return out_path


def is_screen_black(path: str) -> bool:
    """Heuristic: file < 2KB = likely FLAG_SECURE black screen."""
    try:
        return Path(path).stat().st_size < 2000
    except Exception:
        return False


def wake(device: str = None):
    """Wake device screen and unlock."""
    # Check if screen is already on
    power = adb("shell", "dumpsys", "power", device=device)
    screen_on = "mWakefulness=Awake" in power or "mHoldingWakeLockSuspendBlocker=true" in power
    
    if not screen_on:
        # Power key to wake
        adb("shell", "input", "keyevent", "26", device=device)
        time.sleep(1.0)
    
    # Dismiss lockscreen with upward swipe
    adb("shell", "input", "swipe", "360", "1400", "360", "700", "400", device=device)
    time.sleep(0.8)
    
    # Extra swipe in case lockscreen didn't dismiss
    adb("shell", "input", "swipe", "360", "1200", "360", "600", "300", device=device)
    time.sleep(0.5)


def tap(x: int, y: int, device: str = None, delay: float = 0.4):
    """Tap screen at (x, y). Safety: refuses to tap below y=1540."""
    if y > 1530:
        log.warning(f"BLOCKED tap at ({x},{y}) — below device nav bar threshold 1530")
        return
    # AI Interceptor hook (non-blocking fail-safe)
    if AI_INTERCEPT_ENABLED and _adb_interceptor is not None:
        try:
            _adb_interceptor.log_tap(x=x, y=y, device=device, skill_type="adb_tap")
        except Exception:
            pass
    adb("shell", "input", "tap", str(x), str(y), device=device)
    time.sleep(delay)


def long_press(x: int, y: int, duration_ms: int = 1000, device: str = None):
    """Long press at (x, y) for duration_ms milliseconds."""
    adb("shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms), device=device)
    time.sleep(0.5)


def swipe(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500, device: str = None):
    """Swipe from (x1,y1) to (x2,y2)."""
    adb("shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms), device=device)
    time.sleep(0.4)


def press_back(device: str = None):
    """Press Android back button."""
    adb("shell", "input", "keyevent", "4", device=device)
    time.sleep(0.4)


def press_home(device: str = None):
    """Press Android home button."""
    adb("shell", "input", "keyevent", "3", device=device)
    time.sleep(0.4)


def dismiss_keyboard(device: str = None):
    """Dismiss soft keyboard."""
    adb("shell", "input", "keyevent", "111", device=device)  # KEYCODE_ESCAPE
    time.sleep(0.3)
    # Fallback: hide keyboard event
    adb("shell", "input", "keyevent", "4", device=device)
    time.sleep(0.2)


# ─── Text Input (CRITICAL: + for spaces workaround) ──────────────────────────

def type_prompt_safe(prompt: str, device: str = None):
    """
    Type text into focused input field.
    
    CRITICAL WORKAROUND (confirmed from live testing):
    - adb input text does NOT handle spaces properly
    - Use + as space separator (Kling UI accepts this)
    - Also supports word-by-word fallback with SPACE keyevent
    
    Args:
        prompt: Text to type
        device: ADB device serial
    """
    if not prompt:
        return
    
    # Method 1: Use + for spaces (fastest, confirmed working)
    words = prompt.strip().split()
    plus_text = "+".join(words)
    
    # Escape shell special characters
    safe = _escape_adb_text(plus_text)
    
    out = adb("shell", "input", "text", safe, device=device)
    time.sleep(0.5)
    
    # Verify by checking if text appeared (dump UI)
    nodes = dump_ui(device=device)
    typed_texts = " ".join(n.get("text", "") for n in nodes)
    first_word = words[0].lower() if words else ""
    
    if first_word and first_word not in typed_texts.lower():
        log.warning("type_prompt_safe method 1 may have failed, trying word-by-word")
        # Method 2: Word-by-word with SPACE keyevent
        clear_input(device=device)
        for i, word in enumerate(words):
            safe_word = _escape_adb_text(word)
            adb("shell", "input", "text", safe_word, device=device)
            time.sleep(0.15)
            if i < len(words) - 1:
                adb("shell", "input", "keyevent", "62", device=device)  # SPACE
                time.sleep(0.1)
        time.sleep(0.3)


def _escape_adb_text(text: str) -> str:
    """Escape text for adb shell input text command."""
    # Characters that need escaping in shell
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "\\'")
    text = text.replace('"', '\\"')
    text = text.replace("&", "\\&")
    text = text.replace(";", "\\;")
    text = text.replace("|", "\\|")
    text = text.replace("<", "\\<")
    text = text.replace(">", "\\>")
    text = text.replace("(", "\\(")
    text = text.replace(")", "\\)")
    text = text.replace("`", "\\`")
    text = text.replace("$", "\\$")
    return text


def clear_input(device: str = None):
    """Clear current input field content."""
    # Select all + delete
    adb("shell", "input", "keyevent", "KEYCODE_CTRL_A", device=device)
    time.sleep(0.2)
    adb("shell", "input", "keyevent", "KEYCODE_DEL", device=device)
    time.sleep(0.2)
    
    # Also try long press to select all, then delete
    adb("shell", "input", "keyevent", "KEYCODE_MOVE_HOME", device=device)
    time.sleep(0.1)
    # Hold shift+end to select all
    adb("shell", "input", "keyevent", "--longpress", "KEYCODE_DEL", device=device)
    time.sleep(0.3)


# ─── UI Dump & XML Parsing ────────────────────────────────────────────────────

def dump_ui(device: str = None, timeout: int = 15) -> List[Dict]:
    """
    Dump UI hierarchy via uiautomator.
    Returns list of node dicts with: class, text, content-desc, resource-id, bounds, clickable.
    NOTE: On React Native apps (Kling), uiautomator dump can take 10-15s. timeout controls this.
    """
    # Dump to device with shell timeout to avoid infinite hang
    import subprocess as _sp
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += ["shell", f"timeout {timeout} uiautomator dump /sdcard/kling_ui.xml 2>/dev/null"]
    try:
        _sp.run(cmd, capture_output=True, text=True, timeout=timeout + 3)
    except Exception:
        pass
    time.sleep(0.3)
    
    # Pull to local temp file
    local_xml = f"/tmp/kling_ui_{int(time.time())}.xml"
    out, rc = adb_rc("pull", "/sdcard/kling_ui.xml", local_xml, device=device)
    
    if rc != 0 or not Path(local_xml).exists():
        log.debug("UI dump pull failed")
        return []
    
    try:
        tree = ET.parse(local_xml)
        root = tree.getroot()
        nodes = []
        for elem in root.iter():
            nodes.append({
                "class": elem.get("class", ""),
                "text": elem.get("text", ""),
                "content-desc": elem.get("content-desc", ""),
                "resource-id": elem.get("resource-id", ""),
                "bounds": elem.get("bounds", ""),
                "clickable": elem.get("clickable", "false"),
                "enabled": elem.get("enabled", "true"),
                "focused": elem.get("focused", "false"),
                "package": elem.get("package", ""),
            })
        # Cleanup
        try:
            os.unlink(local_xml)
        except Exception:
            pass
        return nodes
    except Exception as e:
        log.debug(f"UI dump parse error: {e}")
        return []


def dump_ui_raw(device: str = None) -> str:
    """Return raw XML text from UI dump (for debugging)."""
    adb("shell", "uiautomator", "dump", "/sdcard/kling_ui.xml", device=device)
    time.sleep(0.3)
    local_xml = f"/tmp/kling_ui_raw_{int(time.time())}.xml"
    adb("pull", "/sdcard/kling_ui.xml", local_xml, device=device)
    try:
        return Path(local_xml).read_text()
    except Exception:
        return ""


def bounds_to_center(bounds_str: str) -> Optional[Tuple[int, int]]:
    """Parse '[x1,y1][x2,y2]' → center (x, y)."""
    nums = list(map(int, re.findall(r"\d+", bounds_str)))
    if len(nums) == 4:
        return (nums[0] + nums[2]) // 2, (nums[1] + nums[3]) // 2
    return None


def find_element_by_text(text: str, device: str = None, partial: bool = True) -> Dict:
    """
    Find UI element by text or content-desc.
    
    Returns:
        dict with node info + 'center': (x, y) or empty dict if not found
    """
    nodes = dump_ui(device=device)
    for n in nodes:
        combined = (n.get("text", "") + " " + n.get("content-desc", "")).strip()
        match = (text.lower() in combined.lower()) if partial else (combined == text)
        if match:
            center = bounds_to_center(n.get("bounds", ""))
            if center:
                n["center"] = center
            return n
    return {}


def tap_element_by_text(text: str, device: str = None, partial: bool = True) -> bool:
    """
    Find and tap UI element by text.
    
    Returns:
        True if found and tapped, False otherwise
    """
    elem = find_element_by_text(text, device=device, partial=partial)
    if not elem:
        return False
    
    center = elem.get("center") or bounds_to_center(elem.get("bounds", ""))
    if not center:
        return False
    
    # Check if this element or parent is clickable
    # If text element not clickable, try clicking parent by checking bounds overlap
    if elem.get("clickable") == "true":
        tap(center[0], center[1], device=device)
        return True
    else:
        # Try tapping anyway (parent might be clickable)
        tap(center[0], center[1], device=device)
        return True


def find_node(nodes: List[Dict], label: str = None, res_id: str = None,
              partial: bool = False, cls: str = None) -> Optional[Dict]:
    """Find first matching UI node."""
    for n in nodes:
        t = (n.get("text", "") + " " + n.get("content-desc", "")).strip()
        if label:
            matched = (label.lower() in t.lower()) if partial else (t == label)
            if matched:
                if cls is None or cls in n.get("class", ""):
                    return n
        if res_id and res_id in n.get("resource-id", ""):
            if cls is None or cls in n.get("class", ""):
                return n
    return None


def find_nodes(nodes: List[Dict], label: str = None, res_id: str = None,
               partial: bool = False) -> List[Dict]:
    """Find all matching UI nodes."""
    results = []
    for n in nodes:
        t = (n.get("text", "") + " " + n.get("content-desc", "")).strip()
        matched = False
        if label:
            matched = (label.lower() in t.lower()) if partial else (t == label)
        if res_id and res_id in n.get("resource-id", ""):
            matched = True
        if matched:
            results.append(n)
    return results


def tap_node(node: Dict, device: str = None) -> bool:
    """Tap center of a UI node's bounds."""
    if not node or not node.get("bounds"):
        return False
    center = bounds_to_center(node["bounds"])
    if center:
        tap(center[0], center[1], device=device)
        return True
    return False


# ─── Screen State Detection ───────────────────────────────────────────────────

def get_screen_state(device: str = None) -> str:
    """
    Detect current Kling AI screen state.
    
    Returns:
        'home'       — Main home feed (shows "Omni", "AI Image", "AI Video")
        'creator'    — Video creation screen (shows "Generate", "Add Character Image")
        'gallery'    — Image picker / gallery (shows "Camera roll", "Done")
        'processing' — Generation in progress (shows "Generating", %)
        'video'      — Video result/player
        'myspace'    — My Space / video history
        'unknown'    — Cannot determine
    """
    nodes = dump_ui(device=device)
    return _classify_screen(nodes)


def _classify_screen(nodes: List[Dict]) -> str:
    """Classify screen from nodes list."""
    if not nodes:
        return "unknown"
    
    # Collect all text
    all_text = " ".join(
        (n.get("text", "") + " " + n.get("content-desc", "")).strip()
        for n in nodes
    )
    
    # Processing/generating (check first — highest priority)
    if any(m.lower() in all_text.lower() for m in PROCESSING_MARKERS):
        return "processing"
    
    # Gallery picker
    if any(m.lower() in all_text.lower() for m in GALLERY_MARKERS):
        return "gallery"
    
    # Creator screen
    if any(m.lower() in all_text.lower() for m in CREATOR_MARKERS):
        return "creator"
    
    # Video result  
    if any(m.lower() in all_text.lower() for m in VIDEO_RESULT_MARKERS):
        return "video"
    
    # My Space
    if "my space" in all_text.lower() or "my creation" in all_text.lower():
        return "myspace"
    
    # Home
    if any(m.lower() in all_text.lower() for m in HOME_MARKERS):
        return "home"
    
    # Check if Kling package visible at all
    if any(PACKAGE in n.get("package", "") for n in nodes):
        return "home"  # In app but unrecognized state — assume home
    
    return "unknown"


def wait_for_screen_state(state: str = "home", timeout: int = 30, device: str = None) -> bool:
    """
    Wait until screen reaches desired state.
    
    Args:
        state: Target state ('home', 'creator', 'gallery', 'processing', 'video', 'myspace')
        timeout: Max seconds to wait
        device: ADB device serial
    
    Returns:
        True if state reached, False if timeout
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = get_screen_state(device=device)
        log.debug(f"wait_for_screen_state: current={current}, target={state}")
        if current == state:
            return True
        time.sleep(1.5)
    return False


# ─── App Lifecycle ────────────────────────────────────────────────────────────

def is_app_installed(device: str = None) -> bool:
    """Check if Kling AI is installed."""
    out = adb("shell", "pm", "list", "packages", PACKAGE, device=device)
    return PACKAGE in out


def get_foreground_package(device: str = None) -> str:
    """Get currently foreground/resumed package name."""
    # Fast method: grep only mCurrentFocus line (avoids huge dumpsys output hang)
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += ["shell", "dumpsys activity activities 2>/dev/null | grep -m1 mCurrentFocus"]
    try:
        import subprocess as _sp
        r = _sp.run(cmd, capture_output=True, text=True, timeout=5)
        out = r.stdout.strip()
    except Exception:
        out = ""
    match = re.search(r"mCurrentFocus=Window\{[^}]+\s+([a-zA-Z][a-zA-Z0-9.]+)/", out)
    if match:
        return match.group(1)
    # Fallback: window manager (also fast with grep)
    out2 = adb("shell", "dumpsys window windows 2>/dev/null | grep -m1 mCurrentFocus", device=device)
    match2 = re.search(r"mCurrentFocus.*?([a-zA-Z][a-zA-Z0-9.]+)/", out2)
    if match2:
        return match2.group(1)
    return ""


def launch_kling(device: str = None):
    """
    Launch Kling AI app via confirmed working activity.
    Uses primary activity first, falls back to monkey launcher.
    """
    log.info("Launching Kling AI...")
    
    # Method 1: Direct activity start (confirmed working)
    out = adb("shell", "am", "start", ACTIVITY, device=device)
    time.sleep(2.5)
    
    if get_foreground_package(device=device) == PACKAGE:
        log.info("Kling launched via am start")
        return
    
    # Method 2: Monkey launcher (also confirmed working)
    log.info("Fallback: launching via monkey")
    adb("shell", "monkey", "-p", PACKAGE, "-c", "android.intent.category.LAUNCHER", "1", device=device)
    time.sleep(2.5)
    
    if get_foreground_package(device=device) == PACKAGE:
        log.info("Kling launched via monkey")
        return
    
    # Method 3: Try alternate activity
    adb("shell", "am", "start", ACTIVITY_ALT, device=device)
    time.sleep(2.5)
    log.info(f"Foreground after launch attempts: {get_foreground_package(device=device)}")


def ensure_kling_foreground(device: str = None) -> bool:
    """
    Ensure Kling AI is in foreground. Launch/bring to front if needed.
    
    Returns:
        True if Kling is now in foreground, False if failed
    """
    pkg = get_foreground_package(device=device)
    if pkg == PACKAGE:
        return True
    
    log.info(f"Kling not foreground (current: {pkg}), launching...")
    launch_kling(device=device)
    time.sleep(1.5)
    
    pkg = get_foreground_package(device=device)
    if pkg == PACKAGE:
        return True
    
    log.warning("Failed to bring Kling to foreground after launch")
    return False


def force_stop_kling(device: str = None):
    """Force stop Kling AI."""
    adb("shell", "am", "force-stop", PACKAGE, device=device)
    time.sleep(1.0)
    log.info("Kling force stopped")


def navigate_home_tab(device: str = None):
    """Navigate to Home tab via bottom nav."""
    tap(NAV_HOME[0], NAV_HOME[1], device=device)
    time.sleep(0.8)


def navigate_myspace_tab(device: str = None):
    """Navigate to My Space tab via bottom nav."""
    tap(NAV_MY_SPACE[0], NAV_MY_SPACE[1], device=device)
    time.sleep(0.8)


def navigate_create(device: str = None):
    """Navigate to Create screen via (+) button."""
    tap(NAV_CREATE[0], NAV_CREATE[1], device=device)
    time.sleep(1.0)


# ─── Credits ──────────────────────────────────────────────────────────────────

def get_credits(device: str = None) -> int:
    """
    Get remaining generation credits.
    
    Looks for TextView with pattern: "🔥 NNN Generate" or "NNN Generate"
    Returns credit count, or -1 if cannot determine.
    
    Credit costs (confirmed):
        I2V (5s): ~144 credits
        T2V (5s): varies
    """
    nodes = dump_ui(device=device)
    return _parse_credits_from_nodes(nodes)


def _parse_credits_from_nodes(nodes: List[Dict]) -> int:
    """Parse credit count from UI nodes."""
    for n in nodes:
        text = n.get("text", "")
        # Pattern: "🔥 192 Generate" or "192 Generate" or "48 Generate"
        match = re.search(r"(\d+)\s+Generate", text)
        if match:
            return int(match.group(1))
        # Also check content-desc
        desc = n.get("content-desc", "")
        match2 = re.search(r"(\d+)\s+Generate", desc)
        if match2:
            return int(match2.group(1))
    
    # Try broader pattern: find any TextView with just a number near "Generate" nodes
    for i, n in enumerate(nodes):
        text = n.get("text", "").strip()
        if text.isdigit():
            # Check surrounding nodes for "Generate"
            ctx_start = max(0, i - 3)
            ctx_end = min(len(nodes), i + 3)
            ctx = " ".join(nodes[j].get("text", "") for j in range(ctx_start, ctx_end))
            if "Generate" in ctx or "generate" in ctx:
                return int(text)
    
    return -1


# ─── Gallery / Image Upload ───────────────────────────────────────────────────

def upload_image(local_path: str, device: str = None) -> bool:
    """
    Push image to device and make it available in gallery.
    
    Steps:
        1. adb push image to /sdcard/Pictures/
        2. Trigger MediaScanner to make it visible in gallery
    
    Returns:
        True on success, False on failure
    """
    local_path = Path(local_path)
    if not local_path.exists():
        log.error(f"Image not found: {local_path}")
        return False
    
    filename = local_path.name
    device_path = f"/sdcard/Pictures/{filename}"
    
    log.info(f"Pushing image to device: {device_path}")
    out, rc = adb_rc("push", str(local_path), device_path, device=device)
    if rc != 0:
        log.error(f"adb push failed (rc={rc}): {out}")
        return False
    
    time.sleep(0.5)
    
    # Trigger media scanner so image appears in gallery
    log.info("Triggering MediaScanner...")
    adb(
        "shell", "am", "broadcast",
        "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
        "-d", f"file://{device_path}",
        device=device
    )
    time.sleep(1.5)
    
    log.info(f"Image ready on device: {device_path}")
    return True


def _select_image_in_gallery(device: str = None) -> bool:
    """
    Navigate gallery picker and select the most recently added image.
    Handles Android permissions dialog.
    
    CRITICAL NOTES (from live testing):
    - Camera is FIRST cell (Row1 Col1) at x=90, y=167 — AVOID!
    - Start from Row2 (y~300) to get photos
    - Permission dialog "Izinkan semua" at (360, 1304)
    - "Done(1)" confirmation at (589, 1303)
    
    Returns:
        True if image selected, False on failure
    """
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    
    if screen != "gallery":
        log.warning(f"Expected gallery screen, got: {screen}")
        # Try to open gallery via tap
        # Maybe we need to tap the upload area first
        return False
    
    # Handle permission dialog if present
    all_text = " ".join(n.get("text", "") + " " + n.get("content-desc", "") for n in nodes)
    if "izinkan semua" in all_text.lower() or "allow all" in all_text.lower():
        log.info("Granting gallery permission...")
        tap(GALLERY_PERMISSION_X, GALLERY_PERMISSION_Y, device=device)
        time.sleep(1.0)
        nodes = dump_ui(device=device)
    
    # Tap first photo (Row2, Col1) — Row1 Col1 is camera!
    # Most recently added photo is typically at Row2 Col1 (x=270, y=300)
    # or Row1 Col2 (x=270, y=167) 
    log.info("Selecting most recent photo from gallery...")
    
    # Best bet: Row1 Col2 (second cell, first row — skips camera at Col1)
    tap(GALLERY_COL_X[1], GALLERY_ROW1_Y, device=device)
    time.sleep(0.8)
    
    # Check if image was selected (Done button should appear)
    nodes = dump_ui(device=device)
    all_text = " ".join(n.get("text", "") + " " + n.get("content-desc", "") for n in nodes)
    
    if "done" in all_text.lower() or "Done" in all_text:
        # Click Done
        log.info("Confirming image selection...")
        tap(GALLERY_DONE_X, GALLERY_DONE_Y, device=device)
        time.sleep(1.5)
        return True
    
    # Fallback: try Row2 Col1
    tap(GALLERY_COL_X[0], GALLERY_ROW2_Y, device=device)
    time.sleep(0.8)
    
    nodes = dump_ui(device=device)
    all_text = " ".join(n.get("text", "") + " " + n.get("content-desc", "") for n in nodes)
    if "done" in all_text.lower():
        tap(GALLERY_DONE_X, GALLERY_DONE_Y, device=device)
        time.sleep(1.5)
        return True
    
    log.warning("Could not confirm gallery selection")
    return False


# ─── Generate Button ──────────────────────────────────────────────────────────

def tap_generate_button(device: str = None) -> bool:
    """
    Tap the Generate button.
    
    CRITICAL (from live testing):
    - "Generate" text node at (603, 843) is NOT clickable
    - Parent node at (573, 843) bounds [475,811][672,875] IS clickable
    - Must tap parent, not text
    
    Returns:
        True if tapped, False if not found
    """
    nodes = dump_ui(device=device)
    
    # Strategy 1: Find clickable parent of Generate text
    # Look for node with bounds containing [475,811][672,875]
    for n in nodes:
        bounds = n.get("bounds", "")
        if not bounds:
            continue
        nums = list(map(int, re.findall(r"\d+", bounds)))
        if len(nums) != 4:
            continue
        x1, y1, x2, y2 = nums
        # Parent generate button area
        if 400 <= x1 <= 500 and 790 <= y1 <= 830 and 640 <= x2 <= 720 and 860 <= y2 <= 910:
            if n.get("clickable") == "true":
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                log.info(f"Tapping Generate parent at {center}")
                tap(center[0], center[1], device=device)
                return True
    
    # Strategy 2: Tap at exact confirmed coords (573, 843) — parent center
    log.info("Using hardcoded Generate button coords (573, 843)")
    tap(I2V_GENERATE_X, I2V_GENERATE_Y, device=device)
    time.sleep(0.5)
    
    # Check if something happened
    nodes2 = dump_ui(device=device)
    screen2 = _classify_screen(nodes2)
    if screen2 in ("processing", "home"):
        return True
    
    # Strategy 3: Search by text label (fallback)
    for label in ["Generate", "Create", "Make Video"]:
        node = find_node(nodes, label=label, partial=True)
        if node and node.get("clickable") == "true":
            log.info(f"Tapping Generate via text label '{label}'")
            return tap_node(node, device=device)
    
    # Strategy 4: Try clicking the generate text anyway (may trigger parent)
    generate_node = find_node(nodes, label="Generate", partial=False)
    if generate_node:
        center = bounds_to_center(generate_node.get("bounds", ""))
        if center:
            tap(center[0], center[1], device=device)
            return True
    
    log.warning("Could not find Generate button")
    return False


# ─── Wait for Generation ──────────────────────────────────────────────────────

def wait_for_generation(timeout: int = 300, device: str = None) -> Dict:
    """
    Wait for video generation to complete.
    
    Polls UI every 5s. Detects:
    - Progress percentages (0%, 25%, 50%, 75%, 100%)
    - "Generating" state
    - Completion (video result screen)
    - Error messages
    - Credit exhaustion
    
    Args:
        timeout: Max seconds to wait (default 300s = 5 min)
        device: ADB device serial
    
    Returns:
        dict with 'status': 'success'|'failed'|'timeout'|'error'
        and optional 'progress', 'error_message'
    """
    deadline = time.time() + timeout
    start_time = time.time()
    last_progress = -1
    check_interval = 5
    credits_before = -1
    
    log.info(f"Waiting for generation (timeout={timeout}s)...")
    
    while time.time() < deadline:
        nodes = dump_ui(device=device)
        screen = _classify_screen(nodes)
        all_text = " ".join(
            n.get("text", "") + " " + n.get("content-desc", "")
            for n in nodes
        ).lower()
        
        # Check for errors first
        if "failed" in all_text or "error" in all_text:
            if "credit" in all_text or "quota" in all_text or "limit" in all_text:
                log.error("Credits exhausted or limit reached")
                return {"status": "error", "error": "credits_exhausted"}
            if "network" in all_text or "connection" in all_text:
                log.error("Network error during generation")
                return {"status": "error", "error": "network_error"}
            log.error("Generation failed")
            return {"status": "failed", "error": "generation_failed"}
        
        # Check for success
        if screen == "video":
            elapsed = int(time.time() - start_time)
            log.info(f"Generation complete! Elapsed: {elapsed}s")
            
            # Try to get credits after
            credits_after = get_credits(device=device)
            credits_used = -1
            if credits_before > 0 and credits_after >= 0:
                credits_used = credits_before - credits_after
            
            return {
                "status": "success",
                "elapsed_seconds": elapsed,
                "credits_used": credits_used,
            }
        
        # Check for "My Space" — generation pushed there
        if screen == "myspace":
            elapsed = int(time.time() - start_time)
            log.info(f"Video sent to My Space. Elapsed: {elapsed}s")
            return {"status": "success", "elapsed_seconds": elapsed, "location": "myspace"}
        
        # Log progress
        progress_match = re.search(r"(\d+)%", all_text)
        if progress_match:
            progress = int(progress_match.group(1))
            if progress != last_progress:
                log.info(f"Generation progress: {progress}%")
                last_progress = progress
        elif screen == "processing":
            log.debug("Still processing...")
        
        # If back to home (generation may have queued)
        if screen == "home":
            elapsed = time.time() - start_time
            if elapsed > 15:  # Give it at least 15s before assuming it went to queue
                log.info("Generation queued/completed, checking My Space...")
                navigate_myspace_tab(device=device)
                time.sleep(2)
                return {"status": "success", "elapsed_seconds": int(elapsed), "location": "myspace_queued"}
        
        time.sleep(check_interval)
    
    log.warning(f"Generation timeout after {timeout}s")
    return {"status": "timeout", "elapsed_seconds": timeout}


# ─── Download Latest Output ───────────────────────────────────────────────────

def download_latest_output(device: str = None) -> str:
    """
    Download the most recently generated video from device.
    
    Strategy:
        1. Query MediaStore for newest MP4
        2. Pull it to local downloads directory
    
    Returns:
        Local path to downloaded video, or empty string on failure
    """
    log.info("Looking for latest generated video...")
    
    # Query MediaStore for recent videos
    for uri in [
        "content://media/external_primary/video/media",
        "content://media/external/video/media",
    ]:
        out = adb(
            "shell", "content", "query",
            "--uri", uri,
            "--projection", "_data,date_added,display_name",
            "--sort", "date_added%20DESC",
            device=device,
        )
        
        if not out:
            continue
        
        for line in out.splitlines():
            try:
                if "_data=" not in line:
                    continue
                device_path = line.split("_data=")[1].split(",")[0].strip()
                if not device_path.endswith((".mp4", ".mov", ".webm")):
                    continue
                
                # Pull it
                local_path = _pull_to_downloads(device_path, device=device)
                if local_path:
                    log.info(f"Downloaded: {local_path}")
                    return local_path
                break
            except Exception as e:
                log.debug(f"Parse error: {e}")
                continue
    
    log.warning("No video found in MediaStore")
    return ""


def _pull_to_downloads(device_path: str, device: str = None, prefix: str = "kling_video") -> str:
    """Pull device file to local downloads dir. Returns local path."""
    ts = int(time.time())
    ext = Path(device_path).suffix or ".mp4"
    local_path = str(DOWNLOADS / f"{prefix}_{ts}{ext}")
    
    out, rc = adb_rc("pull", device_path, local_path, device=device)
    if rc == 0 and Path(local_path).exists() and Path(local_path).stat().st_size > 0:
        return local_path
    
    log.warning(f"Pull failed for {device_path}: {out}")
    return ""


def _get_latest_video_timestamp(device: str = None) -> int:
    """Get timestamp of most recent video in MediaStore. Returns 0 if none."""
    for uri in [
        "content://media/external_primary/video/media",
        "content://media/external/video/media",
    ]:
        out = adb(
            "shell", "content", "query",
            "--uri", uri,
            "--projection", "date_added",
            "--sort", "date_added%20DESC",
            device=device,
        )
        for line in out.splitlines():
            match = re.search(r"date_added=(\d+)", line)
            if match:
                return int(match.group(1))
    return 0


def wait_for_new_video(ts_before: int, timeout: int = 60, device: str = None) -> str:
    """
    Wait for a new video to appear in MediaStore after ts_before.
    Returns device path of new video, or empty string on timeout.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        for uri in [
            "content://media/external_primary/video/media",
            "content://media/external/video/media",
        ]:
            out = adb(
                "shell", "content", "query",
                "--uri", uri,
                "--projection", "_data,date_added",
                "--sort", "date_added%20DESC",
                device=device,
            )
            for line in out.splitlines():
                try:
                    if "_data=" not in line or "date_added=" not in line:
                        continue
                    ts = int(line.split("date_added=")[1].split(",")[0].strip())
                    path = line.split("_data=")[1].split(",")[0].strip()
                    if ts > ts_before and path.endswith((".mp4", ".mov", ".webm")):
                        return path
                except Exception:
                    continue
        time.sleep(2)
    return ""


# ─── Retry Decorator ──────────────────────────────────────────────────────────

def retry(fn, retries: int = 3, base_delay: float = 1.0, label: str = "operation"):
    """Retry fn up to `retries` times with exponential backoff."""
    last_exc = None
    for attempt in range(retries):
        try:
            result = fn()
            return result
        except Exception as e:
            last_exc = e
            if attempt < retries - 1:
                delay = base_delay * (2 ** attempt)
                log.warning(f"{label} attempt {attempt+1} failed: {e}. Retry in {delay:.1f}s")
                time.sleep(delay)
    log.error(f"{label} failed after {retries} attempts: {last_exc}")
    raise last_exc


# ─── T2V: Text-to-Video ───────────────────────────────────────────────────────

def generate_t2v(
    prompt: str,
    duration: str = "5s",
    model: str = "3.0 Omni",
    device: str = None,
) -> Dict:
    """Alias for t2v_generate with AI Interceptor hook. Used by interceptor wrapper."""
    return t2v_generate(prompt=prompt, duration=duration, model=model, device=device)


def t2v_generate(
    prompt: str,
    duration: str = "5s",
    model: str = "3.0 Omni",
    device: str = None,
) -> Dict:
    """
    Generate video from text prompt using Kling 3.0 Omni mode.
    
    Flow:
        1. Ensure Kling is foreground
        2. Navigate to Home (Omni mode input field)
        3. Type prompt in Omni input
        4. Tap green send arrow (confirmed: x=644, y=1362)
        5. Wait for generation
        6. Download result
    
    Args:
        prompt: Video description text
        duration: "5s" or "10s"
        model: "3.0 Omni" (default), "2.0", etc.
        device: ADB serial
    
    Returns:
        JSON-compatible dict with status, output path, credits_used, etc.
    """
    log.info(f"T2V generate: prompt='{prompt[:50]}...', duration={duration}")

    # AI Interceptor pre-hook
    if AI_INTERCEPT_ENABLED and _prompt_interceptor is not None:
        try:
            _prompt_interceptor.validate(prompt=prompt, skill_type="kling_t2v")
        except Exception:
            pass
    
    ts_before = int(time.time())
    start_time = time.time()
    
    # Pre-check
    if not is_app_installed(device=device):
        return {"status": "error", "error": "app_not_installed"}
    
    if not prompt or not prompt.strip():
        return {"status": "error", "error": "empty_prompt"}
    
    # Step 1: Ensure Kling is foreground
    wake(device=device)
    if not ensure_kling_foreground(device=device):
        return {"status": "error", "error": "launch_failed"}
    
    time.sleep(1.5)
    
    # Step 2: Navigate to Home tab
    navigate_home_tab(device=device)
    time.sleep(1.0)
    
    # Get credits before
    credits_before = get_credits(device=device)
    log.info(f"Credits before: {credits_before}")
    
    # Step 3: Enter prompt in Omni mode
    # Look for the text input field at bottom
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    log.info(f"Current screen: {screen}")
    
    # Tap the Omni input field (usually at bottom area)
    # In Omni mode, there's a text input with placeholder
    omni_field = find_node(nodes, label="Omni", partial=True)
    if omni_field:
        tap_node(omni_field, device=device)
        time.sleep(0.8)
    else:
        # Tap at center-bottom area where Omni input typically is
        tap(SCREEN_W // 2, int(SCREEN_H * 0.85), device=device)
        time.sleep(0.8)
    
    # Clear any existing text
    clear_input(device=device)
    time.sleep(0.3)
    
    # Type the prompt
    log.info("Typing prompt...")
    type_prompt_safe(prompt, device=device)
    time.sleep(0.5)
    
    # Step 4: Tap green send arrow
    log.info(f"Tapping green send arrow at ({OMNI_SEND_X}, {OMNI_SEND_Y})")
    tap(OMNI_SEND_X, OMNI_SEND_Y, device=device)
    time.sleep(1.5)
    
    # Check if generation started
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    log.info(f"Screen after send: {screen}")
    
    if screen == "home":
        # Might still be on home — check if any processing started
        all_text = " ".join(n.get("text", "") for n in nodes).lower()
        if "generating" not in all_text:
            # Try clicking generate via text if on creator
            log.info("Trying creator flow via Create button...")
            navigate_create(device=device)
            time.sleep(1.5)
            
            nodes2 = dump_ui(device=device)
            screen2 = _classify_screen(nodes2)
            if screen2 == "creator":
                # Type prompt in creator
                tap(SCREEN_W // 2, I2V_PROMPT_Y, device=device)
                time.sleep(0.5)
                clear_input(device=device)
                type_prompt_safe(prompt, device=device)
                time.sleep(0.5)
                dismiss_keyboard(device=device)
                time.sleep(0.3)
                tap_generate_button(device=device)
                time.sleep(2.0)
    
    # Step 5: Wait for generation
    gen_result = wait_for_generation(timeout=300, device=device)
    
    elapsed = int(time.time() - start_time)
    
    if gen_result["status"] not in ("success",):
        ss_path = str(DOWNLOADS / f"kling_t2v_fail_{int(time.time())}.png")
        screencap(ss_path, device=device)
        return {
            "status": "failed",
            "type": "t2v",
            "error": gen_result.get("error", gen_result["status"]),
            "screenshot": ss_path,
            "duration_seconds": elapsed,
        }
    
    # Step 6: Download
    log.info("Downloading generated video...")
    
    # Try to tap download button first
    _try_tap_download(device=device)
    time.sleep(2.0)
    
    # Wait for file in MediaStore
    device_path = wait_for_new_video(ts_before, timeout=60, device=device)
    if not device_path:
        # Navigate to My Space and try download there
        log.info("Trying download from My Space...")
        navigate_myspace_tab(device=device)
        time.sleep(2.0)
        _try_tap_download(device=device)
        time.sleep(2.0)
        device_path = wait_for_new_video(ts_before, timeout=30, device=device)
    
    # Get credits after
    credits_after = get_credits(device=device)
    credits_used = -1
    if credits_before > 0 and credits_after >= 0:
        credits_used = credits_before - credits_after
    
    if device_path:
        local_path = _pull_to_downloads(device_path, device=device, prefix="kling_t2v")
        # Video Enhancement post-processing (optional, non-blocking)
        if VIDEO_ENHANCE_ENABLED and _video_enhancer is not None and local_path:
            try:
                enhanced = _video_enhancer.remove_watermark(local_path)
                if enhanced:
                    local_path = enhanced
                    log.info(f"Video enhanced (watermark removed): {local_path}")
            except Exception as _enh_exc:
                log.debug(f"Video enhancement skipped: {_enh_exc}")
        return {
            "status": "success",
            "type": "t2v",
            "output": local_path,
            "device_path": device_path,
            "prompt": prompt,
            "duration": duration,
            "credits_used": credits_used,
            "credits_remaining": credits_after,
            "duration_seconds": elapsed,
        }
    else:
        return {
            "status": "success",
            "type": "t2v",
            "output": None,
            "note": "Video generated but download failed — check My Space manually",
            "prompt": prompt,
            "credits_used": credits_used,
            "credits_remaining": credits_after,
            "duration_seconds": elapsed,
        }


def _try_tap_download(device: str = None) -> bool:
    """Try to tap the download button on current screen."""
    nodes = dump_ui(device=device)
    for label in ["Download", "Save to Gallery", "Save", "⬇"]:
        node = find_node(nodes, label=label, partial=True)
        if node:
            log.info(f"Tapping download: '{label}'")
            tap_node(node, device=device)
            time.sleep(1.5)
            return True
    return False


# ─── I2V: Image-to-Video (Motion Control) ────────────────────────────────────

def generate_i2v(
    image_path: str,
    motion_template: str = None,
    prompt: str = "",
    device: str = None,
) -> Dict:
    """Alias for i2v_motion_control with AI Interceptor hook. Used by interceptor wrapper."""
    return i2v_motion_control(image_path=image_path, motion_template=motion_template, prompt=prompt, device=device)


def i2v_motion_control(
    image_path: str,
    motion_template: str = None,
    prompt: str = "",
    device: str = None,
) -> Dict:
    """
    Generate video from image using Kling's Motion Control (I2V).
    
    CONFIRMED FLOW (from live testing):
    1. Tap Create (+) at (263, 1413)
    2. "Add Character Image" upload box at y~355
    3. Upload image via gallery
    4. Select motion template at y~615-665 (optional)
    5. Enter prompt at y~800
    6. Tap Generate button at (573, 843) — parent is clickable, not text
    7. Wait for generation
    8. Download
    
    Credit cost: ~144 credits per 5s I2V generation
    
    Args:
        image_path: Local path to source image
        motion_template: Optional motion template name (e.g., "Chinese trend")
        prompt: Optional text description for motion guidance
        device: ADB serial
    
    Returns:
        JSON-compatible dict with status, output, credits_used, etc.
    """
    log.info(f"I2V motion control: image={image_path}, motion={motion_template}")

    # AI Interceptor pre-hook
    if AI_INTERCEPT_ENABLED and _prompt_interceptor is not None:
        try:
            _prompt_interceptor.validate(prompt=prompt or "", skill_type="kling_i2v")
        except Exception:
            pass
    
    ts_before = int(time.time())
    start_time = time.time()
    
    # Validate inputs
    if not is_app_installed(device=device):
        return {"status": "error", "error": "app_not_installed"}
    
    if not Path(image_path).exists():
        return {"status": "error", "error": f"image_not_found: {image_path}"}
    
    # Step 1: Push image to device gallery
    log.info("Uploading image to device...")
    if not upload_image(image_path, device=device):
        return {"status": "error", "error": "image_upload_failed"}
    
    # Step 2: Ensure Kling foreground
    wake(device=device)
    if not ensure_kling_foreground(device=device):
        return {"status": "error", "error": "launch_failed"}
    
    time.sleep(1.5)
    
    # Get credits before
    credits_before = get_credits(device=device)
    log.info(f"Credits before: {credits_before}")
    
    # Step 3: Navigate to Home first
    navigate_home_tab(device=device)
    time.sleep(1.0)
    
    # Step 4: Tap Create (+) button
    log.info(f"Tapping Create (+) at {NAV_CREATE}")
    tap(NAV_CREATE[0], NAV_CREATE[1], device=device)
    time.sleep(1.5)
    
    # Verify we're on creator screen
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    log.info(f"Screen after Create tap: {screen}")
    
    if screen != "creator":
        # Try alternate create position
        log.info("Trying alternate Create position...")
        tap(NAV_CREATE_ALT[0], NAV_CREATE_ALT[1], device=device)
        time.sleep(1.5)
        nodes = dump_ui(device=device)
        screen = _classify_screen(nodes)
    
    if screen != "creator":
        ss_path = str(DOWNLOADS / f"kling_i2v_no_creator_{int(time.time())}.png")
        screencap(ss_path, device=device)
        return {
            "status": "error",
            "error": "creator_screen_not_reached",
            "screenshot": ss_path,
        }
    
    # Step 5: Tap "Add Character Image" upload box
    log.info(f"Tapping Add Character Image area (y={I2V_ADD_IMAGE_Y})")
    
    # Look for the upload box by text first
    add_image_node = find_node(nodes, label="Add Character Image", partial=True)
    if add_image_node:
        tap_node(add_image_node, device=device)
    else:
        # Use exact y-coordinate (x centered)
        tap(SCREEN_W // 2, I2V_ADD_IMAGE_Y, device=device)
    time.sleep(1.5)
    
    # Step 6: Gallery should open — select our uploaded image
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    log.info(f"Screen after upload tap: {screen}")
    
    if screen == "gallery":
        selected = _select_image_in_gallery(device=device)
        if not selected:
            log.warning("Gallery selection uncertain, continuing...")
        time.sleep(1.5)
    else:
        log.warning(f"Expected gallery, got {screen} — continuing anyway")
    
    # Step 7: Back on creator — select motion template (optional)
    nodes = dump_ui(device=device)
    
    if motion_template:
        log.info(f"Selecting motion template: {motion_template}")
        template_node = find_node(nodes, label=motion_template, partial=True)
        if template_node:
            tap_node(template_node, device=device)
            time.sleep(0.8)
        else:
            # Try tapping in motion template area
            log.info(f"Template '{motion_template}' not found, tapping motion area...")
            # Scroll through templates area to find it
            swipe(SCREEN_W // 2, I2V_MOTION_Y_MAX, SCREEN_W // 4, I2V_MOTION_Y_MAX, 300, device=device)
            time.sleep(0.5)
            nodes = dump_ui(device=device)
            template_node = find_node(nodes, label=motion_template, partial=True)
            if template_node:
                tap_node(template_node, device=device)
                time.sleep(0.8)
            else:
                log.warning(f"Motion template '{motion_template}' not found, skipping")
    
    # Step 8: Enter prompt (optional)
    if prompt:
        log.info(f"Entering prompt: '{prompt[:50]}'")
        # Tap prompt field
        tap(SCREEN_W // 2, I2V_PROMPT_Y, device=device)
        time.sleep(0.5)
        
        # Clear existing
        clear_input(device=device)
        time.sleep(0.2)
        
        # Type prompt
        type_prompt_safe(prompt, device=device)
        time.sleep(0.5)
        
        # Dismiss keyboard
        dismiss_keyboard(device=device)
        time.sleep(0.5)
    
    # Step 9: Tap Generate button
    log.info("Tapping Generate button...")
    if not tap_generate_button(device=device):
        ss_path = str(DOWNLOADS / f"kling_i2v_no_gen_{int(time.time())}.png")
        screencap(ss_path, device=device)
        return {
            "status": "error",
            "error": "generate_button_not_found",
            "screenshot": ss_path,
        }
    
    time.sleep(2.0)
    
    # Check immediate errors
    nodes = dump_ui(device=device)
    all_text = " ".join(n.get("text", "") + " " + n.get("content-desc", "") for n in nodes).lower()
    if "credit" in all_text and ("insufficient" in all_text or "not enough" in all_text):
        return {"status": "error", "error": "insufficient_credits"}
    
    # Step 10: Wait for generation
    gen_result = wait_for_generation(timeout=300, device=device)
    elapsed = int(time.time() - start_time)
    
    if gen_result["status"] not in ("success",):
        ss_path = str(DOWNLOADS / f"kling_i2v_fail_{int(time.time())}.png")
        screencap(ss_path, device=device)
        return {
            "status": "failed",
            "type": "i2v",
            "error": gen_result.get("error", gen_result["status"]),
            "screenshot": ss_path,
            "duration_seconds": elapsed,
        }
    
    # Step 11: Download
    log.info("Downloading I2V result...")
    _try_tap_download(device=device)
    time.sleep(2.0)
    
    device_path = wait_for_new_video(ts_before, timeout=60, device=device)
    if not device_path:
        navigate_myspace_tab(device=device)
        time.sleep(2.0)
        _try_tap_download(device=device)
        time.sleep(2.0)
        device_path = wait_for_new_video(ts_before, timeout=30, device=device)
    
    # Credits after
    credits_after = get_credits(device=device)
    credits_used = -1
    if credits_before > 0 and credits_after >= 0:
        credits_used = credits_before - credits_after
    
    log.info(f"Credits used: {credits_used} ({credits_before} → {credits_after})")
    
    if device_path:
        local_path = _pull_to_downloads(device_path, device=device, prefix="kling_i2v")
        # Video Enhancement post-processing (optional, non-blocking)
        if VIDEO_ENHANCE_ENABLED and _video_enhancer is not None and local_path:
            try:
                enhanced = _video_enhancer.remove_watermark(local_path)
                if enhanced:
                    local_path = enhanced
                    log.info(f"I2V enhanced (watermark removed): {local_path}")
            except Exception as _enh_exc:
                log.debug(f"I2V enhancement skipped: {_enh_exc}")
        return {
            "status": "success",
            "type": "i2v",
            "output": local_path,
            "device_path": device_path,
            "image_path": image_path,
            "motion_template": motion_template,
            "prompt": prompt,
            "credits_used": credits_used,
            "credits_remaining": credits_after,
            "duration_seconds": elapsed,
        }
    else:
        return {
            "status": "success",
            "type": "i2v",
            "output": None,
            "note": "Video generated but download failed — check My Space",
            "image_path": image_path,
            "motion_template": motion_template,
            "credits_used": credits_used,
            "credits_remaining": credits_after,
            "duration_seconds": elapsed,
        }


# ─── Command: status ──────────────────────────────────────────────────────────

def cmd_status(device: str = None) -> Dict:
    """
    Check device connection, app installation, and screen state.
    Returns comprehensive status dict.
    """
    # Check connected devices
    devices_out = adb("devices")
    connected = [
        line.split("\t")[0]
        for line in devices_out.splitlines()
        if "\tdevice" in line
    ]
    
    target = device or DEFAULT_DEVICE
    device_ok = bool(connected) and any(target in d for d in connected)
    
    if not device_ok and not connected:
        return {
            "status": "error",
            "error": "no_devices_connected",
            "connected_devices": connected,
        }
    
    # Use first connected device if target not found
    effective_device = device or (connected[0] if connected else DEFAULT_DEVICE)
    
    installed = is_app_installed(device=effective_device)
    if not installed:
        return {
            "status": "error",
            "error": "app_not_installed",
            "package": PACKAGE,
            "device": effective_device,
        }
    
    # Get device info
    model = adb("shell", "getprop", "ro.product.model", device=effective_device)
    android = adb("shell", "getprop", "ro.build.version.release", device=effective_device)
    
    # App version (use pm dump + grep for speed — avoid full dumpsys package hang)
    pkg_info = adb("shell", f"dumpsys package {PACKAGE} 2>/dev/null | grep -m1 versionName", device=effective_device)
    version_match = re.search(r"versionName=([^\s]+)", pkg_info)
    app_version = version_match.group(1) if version_match else "unknown"
    
    # Foreground
    foreground_pkg = get_foreground_package(device=effective_device)
    is_foreground = foreground_pkg == PACKAGE
    
    # Screen state (if app is open) — skip UI dump for fast status
    screen = "not_open"
    credits = -1
    if is_foreground:
        # Quick check via uiautomator (skip for speed — use --verbose for full check)
        screen = "open"  # App is foreground = at minimum "open"
    
    return {
        "status": "ok",
        "device": effective_device,
        "model": model,
        "android_version": android,
        "app_installed": True,
        "app_version": app_version,
        "app_foreground": is_foreground,
        "screen_state": screen,
        "credits": credits,
        "connected_devices": connected,
        "package": PACKAGE,
    }


# ─── Command: credits ─────────────────────────────────────────────────────────

def cmd_credits(device: str = None) -> Dict:
    """Get current credit balance."""
    if not ensure_kling_foreground(device=device):
        return {"status": "error", "error": "launch_failed"}
    
    time.sleep(1.0)
    credits = get_credits(device=device)
    
    return {
        "status": "ok",
        "credits": credits,
        "note": "Credits unknown — could not parse from UI" if credits == -1 else None,
        "cost_i2v_5s": 144,
        "cost_t2v_5s": "varies",
    }


# ─── Command: download ────────────────────────────────────────────────────────

def cmd_download(device: str = None) -> Dict:
    """Download the most recent video from My Space."""
    if not ensure_kling_foreground(device=device):
        return {"status": "error", "error": "launch_failed"}
    
    # Navigate to My Space
    navigate_myspace_tab(device=device)
    time.sleep(2.0)
    
    ts_before = _get_latest_video_timestamp(device=device)
    
    # Try to tap the first video and download
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    
    if screen == "myspace":
        # Tap the first video thumbnail (center area)
        tap(SCREEN_W // 2, int(SCREEN_H * 0.3), device=device)
        time.sleep(1.5)
        
        # Try to tap download
        _try_tap_download(device=device)
        time.sleep(2.0)
    
    # Download latest
    local_path = download_latest_output(device=device)
    
    if local_path:
        return {
            "status": "success",
            "output": local_path,
            "size_bytes": Path(local_path).stat().st_size if Path(local_path).exists() else 0,
        }
    else:
        # Just pull most recent without download button
        device_path = wait_for_new_video(ts_before, timeout=15, device=device)
        if device_path:
            local = _pull_to_downloads(device_path, device=device)
            return {"status": "success", "output": local}
        
        # Last resort: download whatever is newest
        local_path = download_latest_output(device=device)
        if local_path:
            return {"status": "success", "output": local_path}
        
        return {"status": "error", "error": "no_video_found"}


# ─── Command: screenshot ──────────────────────────────────────────────────────

def cmd_screenshot(out: str = None, device: str = None) -> Dict:
    """Capture device screenshot."""
    if not out:
        out = str(DOWNLOADS / f"kling_ss_{int(time.time())}.png")
    
    screencap(out, device=device)
    
    flag_secure = is_screen_black(out)
    size = Path(out).stat().st_size if Path(out).exists() else 0
    
    return {
        "status": "ok",
        "screenshot": out,
        "size_bytes": size,
        "flag_secure": flag_secure,
        "note": "FLAG_SECURE: screen is protected (black capture)" if flag_secure else None,
    }


# ─── Command: open ────────────────────────────────────────────────────────────

def cmd_open(device: str = None) -> Dict:
    """Wake device and launch Kling AI."""
    wake(device=device)
    time.sleep(0.5)
    launch_kling(device=device)
    time.sleep(2.0)
    
    screen = get_screen_state(device=device)
    return {
        "status": "ok",
        "screen_state": screen,
        "app_foreground": get_foreground_package(device=device) == PACKAGE,
    }


# ─── CLI Wrappers with Retry ──────────────────────────────────────────────────

def run_t2v(args) -> Dict:
    """CLI handler for 't2v' command with retry."""
    device = args.device or DEFAULT_DEVICE
    
    def _do():
        return t2v_generate(
            prompt=args.prompt,
            duration=args.duration if hasattr(args, "duration") else "5s",
            model=args.model if hasattr(args, "model") else "3.0 Omni",
            device=device,
        )
    
    try:
        result = retry(_do, retries=3, base_delay=2.0, label="t2v_generate")
    except Exception as e:
        result = {"status": "error", "error": str(e), "type": "t2v"}
    
    return result


def run_i2v(args) -> Dict:
    """CLI handler for 'i2v' command with retry."""
    device = args.device or DEFAULT_DEVICE
    
    def _do():
        return i2v_motion_control(
            image_path=args.image,
            motion_template=args.motion if hasattr(args, "motion") and args.motion else None,
            prompt=args.prompt if hasattr(args, "prompt") and args.prompt else "",
            device=device,
        )
    
    try:
        result = retry(_do, retries=3, base_delay=2.0, label="i2v_motion_control")
    except Exception as e:
        result = {"status": "error", "error": str(e), "type": "i2v"}
    
    return result


# ─── Debug / Utility Commands ─────────────────────────────────────────────────

def cmd_debug_ui(device: str = None) -> Dict:
    """Dump current UI to file for debugging."""
    raw = dump_ui_raw(device=device)
    debug_path = str(DOWNLOADS / f"kling_ui_dump_{int(time.time())}.xml")
    Path(debug_path).write_text(raw)
    
    nodes = dump_ui(device=device)
    screen = _classify_screen(nodes)
    credits = _parse_credits_from_nodes(nodes)
    
    # Extract key info
    texts = [(n.get("text", ""), n.get("bounds", ""), n.get("clickable", "")) for n in nodes if n.get("text")]
    
    return {
        "status": "ok",
        "screen_state": screen,
        "credits": credits,
        "node_count": len(nodes),
        "ui_dump_path": debug_path,
        "key_texts": texts[:30],  # First 30 text nodes
    }


def cmd_tap(x: int, y: int, device: str = None) -> Dict:
    """Raw tap at coordinates (for debugging)."""
    tap(x, y, device=device)
    return {"status": "ok", "tapped": (x, y)}


# ─── FastAPI Server (optional) ────────────────────────────────────────────────

def cmd_server(port: int = DEFAULT_PORT):
    """Start FastAPI HTTP server for remote control."""
    try:
        from fastapi import FastAPI, Query
        from fastapi.responses import JSONResponse
        import uvicorn
        from pydantic import BaseModel
    except ImportError:
        print(json.dumps({
            "status": "error",
            "error": "fastapi_not_installed",
            "fix": "pip install fastapi uvicorn",
        }))
        sys.exit(1)
    
    app = FastAPI(title="Kling AI Agent", version="2.0.0", description="Kling Android Automation")
    
    class T2VRequest(BaseModel):
        prompt: str
        duration: str = "5s"
        model: str = "3.0 Omni"
        device: Optional[str] = None
    
    class I2VRequest(BaseModel):
        image_path: str
        motion_template: Optional[str] = None
        prompt: str = ""
        device: Optional[str] = None
    
    @app.get("/health")
    def health():
        return {"status": "ok", "service": "kling-agent", "version": "2.0.0", "port": port}
    
    @app.get("/status")
    def status(device: Optional[str] = Query(None)):
        return cmd_status(device=device or DEFAULT_DEVICE)
    
    @app.get("/credits")
    def credits(device: Optional[str] = Query(None)):
        return cmd_credits(device=device or DEFAULT_DEVICE)
    
    @app.post("/open")
    def open_app(device: Optional[str] = Query(None)):
        return cmd_open(device=device or DEFAULT_DEVICE)
    
    @app.post("/t2v")
    def t2v(req: T2VRequest):
        return t2v_generate(
            prompt=req.prompt,
            duration=req.duration,
            model=req.model,
            device=req.device or DEFAULT_DEVICE,
        )
    
    @app.post("/i2v")
    def i2v(req: I2VRequest):
        return i2v_motion_control(
            image_path=req.image_path,
            motion_template=req.motion_template,
            prompt=req.prompt,
            device=req.device or DEFAULT_DEVICE,
        )
    
    @app.get("/download")
    def download(device: Optional[str] = Query(None)):
        return cmd_download(device=device or DEFAULT_DEVICE)
    
    @app.get("/screenshot")
    def screenshot(out: Optional[str] = Query(None), device: Optional[str] = Query(None)):
        return cmd_screenshot(out=out, device=device or DEFAULT_DEVICE)
    
    @app.get("/debug/ui")
    def debug_ui(device: Optional[str] = Query(None)):
        return cmd_debug_ui(device=device or DEFAULT_DEVICE)
    
    @app.post("/debug/tap")
    def debug_tap(x: int, y: int, device: Optional[str] = Query(None)):
        return cmd_tap(x, y, device=device or DEFAULT_DEVICE)
    
    log.info(f"Starting Kling Agent server on port {port}")
    print(json.dumps({"status": "ok", "message": f"Server starting on port {port}"}))
    uvicorn.run(app, host="0.0.0.0", port=port)


# ─── CLI Argument Parser ──────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Kling AI Android Automation Agent v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video from text
  python kling_agent.py t2v --prompt "A serene mountain lake at sunset"

  # Generate video from image with motion
  python kling_agent.py i2v --image /path/photo.jpg --motion "Chinese trend"

  # Generate video from image with prompt
  python kling_agent.py i2v --image /path/photo.jpg --prompt "gentle breeze"

  # Check credits
  python kling_agent.py credits

  # Check device/app status
  python kling_agent.py status

  # Download latest video
  python kling_agent.py download

  # Take screenshot
  python kling_agent.py screenshot --out /tmp/screen.png

  # Debug UI dump
  python kling_agent.py debug

  # Use specific device
  python kling_agent.py --device SGZTONV4OBL74TJZ t2v --prompt "..."
        """
    )
    
    parser.add_argument(
        "--device", "-d",
        default=None,
        help=f"ADB device serial (default: {DEFAULT_DEVICE})"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=True,
        help="Output JSON (always on)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose/debug logging",
    )
    
    sub = parser.add_subparsers(dest="command", help="Command to run")
    
    # ── t2v ──────────────────────────────────────────────────────────────────
    p_t2v = sub.add_parser("t2v", help="Generate video from text prompt")
    p_t2v.add_argument("--prompt", "-p", required=True, help="Video description")
    p_t2v.add_argument("--duration", default="5s", choices=["5s", "10s"],
                       help="Video duration (default: 5s)")
    p_t2v.add_argument("--model", default="3.0 Omni",
                       help="Model to use (default: 3.0 Omni)")
    
    # ── i2v ──────────────────────────────────────────────────────────────────
    p_i2v = sub.add_parser("i2v", help="Animate image to video (Motion Control)")
    p_i2v.add_argument("--image", "-i", required=True,
                       help="Path to source image")
    p_i2v.add_argument("--motion", "-m", default=None,
                       help=f"Motion template name. Options: {', '.join(MOTION_TEMPLATES)}")
    p_i2v.add_argument("--prompt", "-p", default="",
                       help="Optional text prompt for motion guidance")
    
    # ── credits ───────────────────────────────────────────────────────────────
    sub.add_parser("credits", help="Check remaining generation credits")
    
    # ── status ────────────────────────────────────────────────────────────────
    sub.add_parser("status", help="Check device, app, and screen status")
    
    # ── download ──────────────────────────────────────────────────────────────
    sub.add_parser("download", help="Download latest video from My Space")
    
    # ── open ──────────────────────────────────────────────────────────────────
    sub.add_parser("open", help="Wake device and launch Kling AI")
    
    # ── screenshot ────────────────────────────────────────────────────────────
    p_ss = sub.add_parser("screenshot", help="Take device screenshot")
    p_ss.add_argument("--out", "-o", default=None, help="Output PNG path")
    
    # ── debug ─────────────────────────────────────────────────────────────────
    sub.add_parser("debug", help="Dump current UI hierarchy for debugging")
    
    # ── server ────────────────────────────────────────────────────────────────
    p_srv = sub.add_parser("server", help="Start FastAPI HTTP server")
    p_srv.add_argument("--port", type=int, default=DEFAULT_PORT)
    
    # ── tap (debug) ───────────────────────────────────────────────────────────
    p_tap = sub.add_parser("tap", help="Raw tap at coordinates (debug)")
    p_tap.add_argument("x", type=int)
    p_tap.add_argument("y", type=int)
    
    return parser


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args = parser.parse_args()
    
    # Configure logging
    if hasattr(args, "verbose") and args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    device = args.device or DEFAULT_DEVICE
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    result = None
    
    try:
        if args.command == "t2v":
            result = run_t2v(args)
        
        elif args.command == "i2v":
            result = run_i2v(args)
        
        elif args.command == "credits":
            result = cmd_credits(device=device)
        
        elif args.command == "status":
            result = cmd_status(device=device)
        
        elif args.command == "download":
            result = cmd_download(device=device)
        
        elif args.command == "open":
            result = cmd_open(device=device)
        
        elif args.command == "screenshot":
            out = args.out if hasattr(args, "out") else None
            result = cmd_screenshot(out=out, device=device)
        
        elif args.command == "debug":
            result = cmd_debug_ui(device=device)
        
        elif args.command == "server":
            cmd_server(port=args.port)
            return
        
        elif args.command == "tap":
            result = cmd_tap(args.x, args.y, device=device)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        result = {"status": "interrupted"}
    except Exception as e:
        log.exception(f"Unhandled error in command '{args.command}'")
        result = {"status": "error", "error": str(e), "command": args.command}
    
    if result is not None:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        
        # Exit with non-zero if error
        if result.get("status") == "error":
            sys.exit(1)


if __name__ == "__main__":
    main()
