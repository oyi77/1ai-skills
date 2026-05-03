#!/usr/bin/env python3
"""
Shopee Android Agent — Control Shopee Indonesia app via ADB + autodroid.

Usage:
  shopee_agent.py status [--device SERIAL]
  shopee_agent.py open [--device SERIAL]
  shopee_agent.py orders [--device SERIAL]
  shopee_agent.py search --query TEXT [--device SERIAL]
  shopee_agent.py screenshot [--device SERIAL] [--out PATH]
  shopee_agent.py server [--port 8767]
  shopee_agent.py login --username U --password P [--device SERIAL]
  shopee_agent.py register --phone PHONE --password P [--device SERIAL]
  shopee_agent.py product --query TEXT [--device SERIAL]
  shopee_agent.py cart [--device SERIAL]
  shopee_agent.py like [--device SERIAL]
  shopee_agent.py review --text TEXT [--rating 1-5] [--device SERIAL]
"""

import argparse
import json
import random
import subprocess
import sys
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

AUTODROID = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-autodroid/scripts/autodroid.py"
)
SHOPEE_PACKAGE = "com.shopee.id"
WORKSPACE_DOWNLOADS = os.path.expanduser("~/.openclaw/workspace/downloads")
DEFAULT_SCREENSHOT = os.path.join(WORKSPACE_DOWNLOADS, "shopee_screenshot.png")
PROOF_SCREENSHOT = os.path.join(WORKSPACE_DOWNLOADS, "shopee_agent_proof.png")

Path(WORKSPACE_DOWNLOADS).mkdir(parents=True, exist_ok=True)

# Shopee onboarding dismiss buttons (Indonesian + English)
ONBOARDING_BUTTONS = [
    "Lewati",
    "Skip",
    "Tutup",
    "Close",
    "Tidak",
    "Nanti",
    "OK",
]

# Bottom nav coordinates for 720x1640 resolution (legacy)
BOTTOM_NAV = {
    "Home": (72, 1490),
    "Kategori": (216, 1490),
    "Keranjang": (360, 1490),
    "Chat": (504, 1490),
    "Saya": (648, 1490),
}

# VERIFIED bottom nav coordinates from live screenshots (Redmi 2409BRN2CY, 720x1640, Android 14)
BOTTOM_NAV_VERIFIED = {
    "Beranda": (72, 1575),
    "LiveVideo": (216, 1575),
    "Notifikasi": (504, 1575),
    "Saya": (648, 1575),
}

# VERIFIED top bar coordinates
TOP_SEARCH_X = 360
TOP_SEARCH_Y = 130
CART_ICON_X = 660
CART_ICON_Y = 130

# VERIFIED login field coordinates
LOGIN_USERNAME_Y = 700
LOGIN_PASSWORD_Y = 820
LOGIN_BUTTON_Y = 940

ADB = os.path.expanduser("~/.local/bin/adb")
if not Path(ADB).exists():
    ADB = "adb"


def adb_cmd(args: list[str], device: str | None = None, capture: bool = True) -> str:
    cmd = [ADB]
    if device:
        cmd += ["-s", device]
    cmd += args
    r = subprocess.run(cmd, capture_output=capture, text=True)
    if r.returncode != 0 and r.stderr:
        print(f"[adb err] {r.stderr.strip()}", file=sys.stderr)
    return r.stdout.strip() if capture else ""


# ─── Natural Scroll Helpers ──────────────────────────────────────────────────

def natural_swipe(direction: str = "up", device: str | None = None,
                  speed: int | None = None, distance: int | None = None):
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
        adb_cmd(["shell", "input", "swipe", str(cx), str(y1), str(cx), str(y2), str(speed)], device=device)
    elif direction == "down":
        dist = distance or random.randint(600, 950)
        y1 = random.randint(300, 500)
        y2 = y1 + dist
        adb_cmd(["shell", "input", "swipe", str(cx), str(y1), str(cx), str(y2), str(speed)], device=device)
    elif direction == "left":
        dist = distance or random.randint(400, 700)
        y = random.randint(700, 900)
        adb_cmd(["shell", "input", "swipe", "600", str(y), str(600 - dist), str(y), str(speed)], device=device)
    elif direction == "right":
        dist = distance or random.randint(400, 700)
        y = random.randint(700, 900)
        adb_cmd(["shell", "input", "swipe", "120", str(y), str(120 + dist), str(y), str(speed)], device=device)

    time.sleep(random.uniform(0.1, 0.3))  # settle pause


def natural_pause(min_s: float = 0.5, max_s: float = 2.5):
    """Random human-like pause."""
    time.sleep(random.uniform(min_s, max_s))


def autodroid_cmd(
    args: list[str], device: str | None = None, capture: bool = True
) -> str:
    env = os.environ.copy()
    if device:
        env["ANDROID_SERIAL"] = device
    cmd = ["python3", AUTODROID] + args
    r = subprocess.run(cmd, capture_output=capture, text=True, env=env)
    if r.returncode != 0 and r.stderr:
        print(f"[autodroid err] {r.stderr.strip()}", file=sys.stderr)
    return r.stdout.strip() if capture else ""


def tap(x: int, y: int, device: str | None = None):
    autodroid_cmd(["tap", str(x), str(y)], device=device)


def tap_text(text: str, device: str | None = None) -> bool:
    out = autodroid_cmd(["tap-text", text], device=device)
    return "Could not tap" not in out and "Not found" not in out


def type_text(text: str, device: str | None = None):
    autodroid_cmd(["type", text], device=device)


def press_key(key: str, device: str | None = None):
    autodroid_cmd(["key", key], device=device)


def launch_app(package: str, device: str | None = None):
    autodroid_cmd(["launch", package], device=device)


def screenshot(path: str, device: str | None = None) -> str:
    autodroid_cmd(["screenshot", path], device=device)
    return path


def screencap(path: str, device: str | None = None) -> str:
    """Direct ADB screencap fallback — bypasses autodroid for reliability."""
    tmp_path = "/sdcard/shopee_cap.png"
    adb_cmd(["shell", "screencap", "-p", tmp_path], device=device)
    adb_cmd(["pull", tmp_path, path], device=device)
    adb_cmd(["shell", "rm", tmp_path], device=device)
    return path


def safe_screenshot(path: str, device: str | None = None) -> str:
    """Try autodroid screenshot, fallback to adb screencap."""
    try:
        screenshot(path, device=device)
        if Path(path).exists() and Path(path).stat().st_size > 1000:
            return path
    except Exception:
        pass
    return screencap(path, device=device)


def ui_dump(path: str = "/tmp/shopee_ui.xml", device: str | None = None) -> str:
    autodroid_cmd(["ui-dump", path], device=device)
    return path


def dump_ui_texts(device: str | None = None) -> list[str]:
    """Dump UI and return all text strings. Shopee has heavy animations — may return empty."""
    xml_path = "/tmp/shopee_ui_dump.xml"
    try:
        ui_dump(xml_path, device=device)
        return extract_textview_text(xml_path)
    except Exception:
        return []


def extract_textview_text(xml_path: str) -> list[str]:
    texts: list[str] = []
    if not Path(xml_path).exists():
        return texts
    try:
        tree = ET.parse(xml_path)
        for node in tree.iter():
            node_class = node.get("class", "")
            node_text = node.get("text", "") or ""
            if "TextView" in node_class and node_text.strip():
                texts.append(node_text.strip())
    except ET.ParseError:
        pass
    return texts


def texts_contain_any(texts: list[str], keywords: list[str]) -> bool:
    texts_lower = [t.lower() for t in texts]
    for kw in keywords:
        if any(kw.lower() in t for t in texts_lower):
            return True
    return False


def check_shopee_installed(device: str | None = None) -> bool:
    out = adb_cmd(["shell", "pm", "list", "packages", SHOPEE_PACKAGE], device=device)
    return SHOPEE_PACKAGE in out


def dismiss_onboarding(device: str | None = None) -> int:
    """Dismiss onboarding popups. Returns number of buttons tapped."""
    count = 0
    for btn_text in ONBOARDING_BUTTONS:
        found = tap_text(btn_text, device=device)
        if found:
            count += 1
            time.sleep(0.5)
    return count


def wait_for_app_ready(timeout: int = 5, device: str | None = None) -> bool:
    """Wait for Shopee to be in foreground."""
    start = time.time()
    while time.time() - start < timeout:
        focus = adb_cmd(
            ["shell", "dumpsys", "window", "|", "grep", "mCurrentFocus"],
            device=device,
        )
        if SHOPEE_PACKAGE in focus:
            return True
        time.sleep(0.5)
    return False


def launch_and_dismiss(device: str | None = None):
    """Launch Shopee, wait, dismiss popups."""
    print(f"[shopee] Launching {SHOPEE_PACKAGE}...", file=sys.stderr)
    launch_app(SHOPEE_PACKAGE, device=device)
    time.sleep(3)
    wait_for_app_ready(timeout=5, device=device)
    for _ in range(3):
        dismissed = dismiss_onboarding(device=device)
        if dismissed == 0:
            break
        time.sleep(0.5)


def cmd_status(device: str | None = None) -> dict:
    installed = check_shopee_installed(device)
    model = adb_cmd(["shell", "getprop", "ro.product.model"], device=device)
    android = adb_cmd(["shell", "getprop", "ro.build.version.release"], device=device)

    result = {
        "shopee_installed": installed,
        "package": SHOPEE_PACKAGE,
        "device": device or "default",
        "model": model,
        "android_version": android,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_open(device: str | None = None) -> dict:
    """Launch Shopee and dismiss onboarding popups."""
    print(f"[shopee] Launching {SHOPEE_PACKAGE}...", file=sys.stderr)
    launch_app(SHOPEE_PACKAGE, device=device)
    time.sleep(3)

    print("[shopee] Waiting for app ready...", file=sys.stderr)
    wait_for_app_ready(timeout=5, device=device)

    print("[shopee] Dismissing onboarding popups...", file=sys.stderr)
    # Multiple passes to handle stacked popups
    total_dismissed = 0
    for _ in range(3):
        dismissed = dismiss_onboarding(device=device)
        total_dismissed += dismissed
        if dismissed == 0:
            break
        time.sleep(0.5)

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_open.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "status": "opened",
        "dismissed_popups": total_dismissed,
        "device": device or "default",
        "screenshot_path": ss_path,
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_orders(device: str | None = None) -> dict:
    """
    Open Shopee → navigate to Orders → screenshot.

    Flow:
    1. Launch Shopee
    2. Dismiss onboarding
    3. Tap Profile/Me (Saya) tab — verified coord (648, 1575)
    4. Tap "Pesanan Saya" / "My Orders"
    5. Screenshot
    6. Return JSON
    """
    launch_and_dismiss(device=device)

    print("[shopee] Tapping Saya tab (648, 1575)...", file=sys.stderr)
    tap(648, 1575, device=device)
    time.sleep(2)

    print("[shopee] Tapping 'Pesanan Saya'...", file=sys.stderr)
    order_labels = ["Pesanan Saya", "My Orders", "Pesanan", "Orders"]
    tapped = False
    for label in order_labels:
        if tap_text(label, device=device):
            tapped = True
            print(f"[shopee] Found and tapped: {label}", file=sys.stderr)
            break

    if not tapped:
        print(
            "[shopee] Could not find orders button, trying coordinates...",
            file=sys.stderr,
        )
        tap(360, 500, device=device)

    time.sleep(2)

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_orders.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_search(query: str, device: str | None = None) -> dict:
    """
    Search for a product on Shopee.

    Flow:
    1. Launch Shopee + dismiss popups
    2. Tap search bar at top (360, 130) — verified coord
    3. Type query word by word
    4. Press ENTER
    5. Wait 3s for results
    6. Dump UI for product names/prices
    7. Screenshot
    8. Return JSON with results
    """
    launch_and_dismiss(device=device)

    print("[shopee] Tapping search bar (360, 130)...", file=sys.stderr)
    tap(TOP_SEARCH_X, TOP_SEARCH_Y, device=device)
    time.sleep(1)

    print(f"[shopee] Typing query word by word: {query}...", file=sys.stderr)
    # Type word by word to avoid ADB input issues with spaces
    words = query.split()
    for i, word in enumerate(words):
        adb_cmd(["shell", "input", "text", word], device=device)
        if i < len(words) - 1:
            adb_cmd(["shell", "input", "text", "%s"], device=device)  # space
        time.sleep(0.2)

    time.sleep(0.5)
    print("[shopee] Pressing ENTER...", file=sys.stderr)
    press_key("ENTER", device=device)
    time.sleep(3)

    # Try UI dump for results (may be empty due to animations)
    texts = dump_ui_texts(device=device)
    results = []
    # Parse title/price pairs from UI text (heuristic: Rp prefix = price)
    current_title = None
    for text in texts:
        if text.startswith("Rp") or text.startswith("IDR"):
            if current_title:
                results.append({"title": current_title, "price": text})
                current_title = None
        elif len(text) > 5 and not text.isdigit():
            current_title = text

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_search.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "query": query,
        "results": results[:10],  # top 10
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_screenshot(device: str | None = None, out: str | None = None) -> dict:
    out_path = out or DEFAULT_SCREENSHOT
    safe_screenshot(out_path, device=device)

    result = {
        "screenshot_path": out_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# NEW COMMANDS
# ─────────────────────────────────────────────────────────────────────────────

def cmd_login(username: str, password: str, device: str | None = None) -> dict:
    """
    Login to Shopee.

    Flow:
    1. Launch Shopee + dismiss popups
    2. Tap "Saya" tab — verified coord (648, 1575)
    3. Check UI for login state
    4. If not logged in: tap "Masuk", fill fields, submit
    5. Wait 4s, dismiss popups
    6. Return {ok, logged_in, username, screenshot_path, device}
    """
    launch_and_dismiss(device=device)

    print("[shopee] Tapping Saya tab (648, 1575)...", file=sys.stderr)
    tap(648, 1575, device=device)
    time.sleep(2)

    # Check if already logged in via UI dump
    texts = dump_ui_texts(device=device)
    logged_in_keywords = ["Profil Saya", "My Profile", "Pesanan Saya", "Pengaturan", "Voucher"]
    not_logged_in_keywords = ["Masuk", "Login", "Daftar", "Register"]

    already_logged_in = texts_contain_any(texts, logged_in_keywords)
    has_login_button = texts_contain_any(texts, not_logged_in_keywords)

    detected_username = None
    if already_logged_in and not has_login_button:
        print("[shopee] Already logged in!", file=sys.stderr)
        ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_login.png")
        safe_screenshot(ss_path, device=device)
        result = {
            "ok": True,
            "logged_in": True,
            "username": username,
            "screenshot_path": ss_path,
            "device": device or "default",
        }
        print(json.dumps(result, indent=2))
        return result

    # Not logged in — tap "Masuk" button
    print("[shopee] Not logged in. Tapping Masuk...", file=sys.stderr)
    masuk_tapped = tap_text("Masuk", device=device)
    if not masuk_tapped:
        # Fallback: try coordinate-based tap on Masuk button area
        tap(360, 800, device=device)
    time.sleep(2)

    # Fill username/email/phone — verified y=700, x=360
    print("[shopee] Filling username...", file=sys.stderr)
    tap(360, LOGIN_USERNAME_Y, device=device)
    time.sleep(0.5)
    adb_cmd(["shell", "input", "text", username.replace(" ", "%s")], device=device)
    time.sleep(0.5)

    # Fill password — verified y=820, x=360
    print("[shopee] Filling password...", file=sys.stderr)
    tap(360, LOGIN_PASSWORD_Y, device=device)
    time.sleep(0.5)
    adb_cmd(["shell", "input", "text", password.replace(" ", "%s")], device=device)
    time.sleep(0.5)

    # Tap Login button — verified y=940, x=360
    print("[shopee] Tapping Masuk button (360, 940)...", file=sys.stderr)
    tap(360, LOGIN_BUTTON_Y, device=device)
    time.sleep(4)

    # Dismiss post-login popups
    for _ in range(3):
        dismissed = dismiss_onboarding(device=device)
        if dismissed == 0:
            break
        time.sleep(1)

    # Re-check login state
    texts_after = dump_ui_texts(device=device)
    is_logged_in = texts_contain_any(texts_after, logged_in_keywords) or \
                   not texts_contain_any(texts_after, not_logged_in_keywords)

    # Try to detect username from UI
    for t in texts_after:
        if "@" in t or (len(t) > 3 and t not in logged_in_keywords + not_logged_in_keywords):
            detected_username = t
            break

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_login.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "logged_in": is_logged_in,
        "username": detected_username or username,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_register(phone: str, password: str, device: str | None = None) -> dict:
    """
    Register a new Shopee account.

    Flow:
    1. Launch Shopee + dismiss popups
    2. Tap "Saya" (648, 1575) → tap "Daftar"
    3. Enter phone number
    4. Tap next
    5. Handle OTP: return {ok: false, needs_otp: true}
    6. Return {ok, registered/needs_otp, phone, device}
    """
    launch_and_dismiss(device=device)

    print("[shopee] Tapping Saya tab (648, 1575)...", file=sys.stderr)
    tap(648, 1575, device=device)
    time.sleep(2)

    print("[shopee] Tapping Daftar (Register)...", file=sys.stderr)
    daftar_tapped = tap_text("Daftar", device=device)
    if not daftar_tapped:
        daftar_tapped = tap_text("Register", device=device)
    if not daftar_tapped:
        # Fallback coordinate — typically below Masuk button
        tap(360, 1000, device=device)
    time.sleep(2)

    # Enter phone number
    print(f"[shopee] Entering phone number: {phone}...", file=sys.stderr)
    tap(360, 700, device=device)
    time.sleep(0.5)
    adb_cmd(["shell", "input", "text", phone], device=device)
    time.sleep(0.5)

    # Enter password if field exists
    texts = dump_ui_texts(device=device)
    if texts_contain_any(texts, ["Kata Sandi", "Password", "sandi"]):
        print("[shopee] Entering password...", file=sys.stderr)
        tap(360, 820, device=device)
        time.sleep(0.5)
        adb_cmd(["shell", "input", "text", password.replace(" ", "%s")], device=device)
        time.sleep(0.5)

    # Tap next/register button
    print("[shopee] Tapping Next/Daftar...", file=sys.stderr)
    next_tapped = tap_text("Berikutnya", device=device) or \
                  tap_text("Next", device=device) or \
                  tap_text("Daftar", device=device)
    if not next_tapped:
        tap(360, 940, device=device)
    time.sleep(3)

    # Check if OTP screen appeared
    texts_after = dump_ui_texts(device=device)
    needs_otp = texts_contain_any(texts_after, ["OTP", "Kode", "Verifikasi", "Verification", "kode"])

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_register.png")
    safe_screenshot(ss_path, device=device)

    if needs_otp:
        result = {
            "ok": False,
            "needs_otp": True,
            "phone": phone,
            "screenshot_path": ss_path,
            "device": device or "default",
        }
    else:
        result = {
            "ok": True,
            "registered": True,
            "needs_otp": False,
            "phone": phone,
            "screenshot_path": ss_path,
            "device": device or "default",
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_product(query: str, device: str | None = None) -> dict:
    """
    Search and open first product detail.

    Flow:
    1. search(query)
    2. Tap first product (approx y=400, x=180 for first grid item)
    3. Wait 3s
    4. Dump UI for title, price, rating
    5. Screenshot
    6. Return {ok, title, price, rating, screenshot_path, device}
    """
    print(f"[shopee] Searching for: {query}...", file=sys.stderr)
    cmd_search(query, device=device)

    # Tap first product — first grid item at approx (180, 400)
    print("[shopee] Tapping first product (180, 400)...", file=sys.stderr)
    tap(180, 400, device=device)
    time.sleep(3)

    # Dismiss popups
    for _ in range(2):
        dismissed = dismiss_onboarding(device=device)
        if dismissed == 0:
            break
        time.sleep(0.5)

    # Dump UI for product details
    texts = dump_ui_texts(device=device)

    # Heuristic extraction
    title = None
    price = None
    rating = None
    for text in texts:
        if title is None and len(text) > 10 and not text.startswith("Rp"):
            title = text
        if price is None and (text.startswith("Rp") or text.startswith("IDR")):
            price = text
        if rating is None and ("." in text and len(text) <= 4):
            try:
                v = float(text)
                if 1.0 <= v <= 5.0:
                    rating = text
            except ValueError:
                pass

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_product.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "title": title,
        "price": price,
        "rating": rating,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_cart(device: str | None = None) -> dict:
    """
    View shopping cart.

    Flow:
    1. Tap cart icon top right (~660, 130) — verified coord
    2. Screenshot
    3. Dump UI for cart items
    4. Return {ok, items, screenshot_path, device}
    """
    launch_and_dismiss(device=device)

    print("[shopee] Tapping cart icon (660, 130)...", file=sys.stderr)
    tap(CART_ICON_X, CART_ICON_Y, device=device)
    time.sleep(2)

    # Dismiss popups
    for _ in range(2):
        dismissed = dismiss_onboarding(device=device)
        if dismissed == 0:
            break
        time.sleep(0.5)

    # Dump UI for cart items
    texts = dump_ui_texts(device=device)
    items = []
    current_item = {}
    for text in texts:
        if text.startswith("Rp") or text.startswith("IDR"):
            if current_item.get("title"):
                current_item["price"] = text
                items.append(current_item)
                current_item = {}
        elif len(text) > 5 and not text.isdigit() and text not in ["Keranjang", "Cart", "Belanja Sekarang"]:
            current_item = {"title": text}

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_cart.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "items": items,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_like(device: str | None = None) -> dict:
    """
    Wishlist/favorite the current product.

    Flow:
    1. On product detail page
    2. Tap heart/wishlist icon (usually top right ~660, 200)
    3. Return {ok, liked, screenshot_path, device}
    """
    print("[shopee] Tapping wishlist/heart icon...", file=sys.stderr)

    # Try text-based tap first
    liked_via_text = tap_text("Favorit", device=device) or \
                     tap_text("Wishlist", device=device) or \
                     tap_text("Suka", device=device)

    if not liked_via_text:
        # Fallback: tap typical heart icon position top-right of product page
        print("[shopee] Tapping heart icon at (660, 200)...", file=sys.stderr)
        tap(660, 200, device=device)
    time.sleep(1)

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_like.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "liked": True,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_review(text: str, rating: int = 5, device: str | None = None) -> dict:
    """
    Review a delivered order.

    Flow:
    1. Navigate to orders (Saya → Pesanan Saya)
    2. Find delivered order — tap "Nilai" / "Review" button
    3. Select star rating
    4. Type review text
    5. Submit
    6. Return {ok, reviewed, text, rating, screenshot_path, device}
    """
    # Go to orders first
    launch_and_dismiss(device=device)

    print("[shopee] Navigating to orders...", file=sys.stderr)
    tap(648, 1575, device=device)
    time.sleep(2)

    order_labels = ["Pesanan Saya", "My Orders", "Pesanan", "Orders"]
    for label in order_labels:
        if tap_text(label, device=device):
            break
    time.sleep(2)

    # Look for "Selesai" tab (delivered orders) or "Nilai" button
    print("[shopee] Looking for delivered order to review...", file=sys.stderr)
    tap_text("Selesai", device=device)
    time.sleep(1)

    # Find and tap "Nilai" or "Review" button
    nilai_tapped = tap_text("Nilai", device=device) or \
                   tap_text("Ulas", device=device) or \
                   tap_text("Review", device=device)

    if not nilai_tapped:
        print("[shopee] No 'Nilai' button found — no delivered orders?", file=sys.stderr)
        ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_review.png")
        safe_screenshot(ss_path, device=device)
        result = {
            "ok": False,
            "reviewed": False,
            "text": text,
            "rating": rating,
            "error": "No reviewable order found",
            "screenshot_path": ss_path,
            "device": device or "default",
        }
        print(json.dumps(result, indent=2))
        return result

    time.sleep(2)

    # Select star rating — stars are typically in a row, tap Nth star
    # Star positions: 5 stars across ~360px width, starting ~x=100
    print(f"[shopee] Selecting {rating} stars...", file=sys.stderr)
    star_x_positions = [100, 180, 260, 340, 420]
    star_y = 500  # approximate star row y position
    if 1 <= rating <= 5:
        tap(star_x_positions[rating - 1], star_y, device=device)
    time.sleep(0.5)

    # Type review text
    print("[shopee] Typing review text...", file=sys.stderr)
    tap(360, 650, device=device)
    time.sleep(0.5)
    words = text.split()
    for i, word in enumerate(words):
        adb_cmd(["shell", "input", "text", word], device=device)
        if i < len(words) - 1:
            adb_cmd(["shell", "input", "text", "%s"], device=device)
        time.sleep(0.1)
    time.sleep(0.5)

    # Submit review
    print("[shopee] Submitting review...", file=sys.stderr)
    submitted = tap_text("Kirim", device=device) or \
                tap_text("Submit", device=device) or \
                tap_text("Simpan", device=device)
    if not submitted:
        tap(360, 940, device=device)
    time.sleep(3)

    ss_path = os.path.join(WORKSPACE_DOWNLOADS, "shopee_review.png")
    safe_screenshot(ss_path, device=device)

    result = {
        "ok": True,
        "reviewed": True,
        "text": text,
        "rating": rating,
        "screenshot_path": ss_path,
        "device": device or "default",
    }
    print(json.dumps(result, indent=2))
    return result


def cmd_scroll(direction: str = "up", count: int = 3, device: str | None = None) -> dict:
    """Scroll current Shopee page with natural swipes."""
    try:
        for i in range(count):
            print(f"[scroll] Swipe {i+1}/{count} ({direction})", file=sys.stderr)
            natural_swipe(direction, device=device)
            natural_pause(0.5, 1.5)

        ss_path = PROOF_SCREENSHOT
        safe_screenshot(ss_path, device=device)

        result = {
            "ok": True,
            "scrolled_count": count,
            "direction": direction,
            "screenshot_path": ss_path,
            "device": device or "default",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "scrolled_count": 0,
            "direction": direction,
            "screenshot_path": None,
            "device": device or "default",
        }

    print(json.dumps(result, indent=2))
    return result


def cmd_browse_shopee(duration: int = 30, device: str | None = None) -> dict:
    """Scroll Shopee home feed for `duration` seconds with human-like behaviour."""
    scrolled_count = 0
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            # Simulate reading a product (pause between 1.5-4s)
            wait = random.uniform(1.5, 4.0)
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            if remaining <= 0:
                break
            time.sleep(min(wait, remaining))

            if time.time() - start_time >= duration:
                break

            print(f"[browse] Scrolling up ({scrolled_count+1})", file=sys.stderr)
            natural_swipe("up", device=device)
            scrolled_count += 1

        ss_path = PROOF_SCREENSHOT
        safe_screenshot(ss_path, device=device)

        result = {
            "ok": True,
            "duration": duration,
            "scrolled_count": scrolled_count,
            "screenshot_path": ss_path,
            "device": device or "default",
        }
    except Exception as e:
        result = {
            "ok": False,
            "error": str(e),
            "duration": duration,
            "scrolled_count": scrolled_count,
            "screenshot_path": None,
            "device": device or "default",
        }

    print(json.dumps(result, indent=2))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# SERVER
# ─────────────────────────────────────────────────────────────────────────────

def run_server(port: int = 8767):
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("[shopee] Installing FastAPI + uvicorn...", file=sys.stderr)
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"],
            check=True,
        )

    from fastapi import FastAPI
    from pydantic import BaseModel
    from typing import Optional

    app = FastAPI(title="Shopee Android Agent", version="2.0.0")

    class DeviceRequest(BaseModel):
        device: Optional[str] = None

    class OrdersRequest(BaseModel):
        device: Optional[str] = None

    class SearchRequest(BaseModel):
        query: str
        device: Optional[str] = None

    class ProductRequest(BaseModel):
        query: str
        device: Optional[str] = None

    class LoginRequest(BaseModel):
        username: str
        password: str
        device: Optional[str] = None

    class RegisterRequest(BaseModel):
        phone: str
        password: str
        device: Optional[str] = None

    class ReviewRequest(BaseModel):
        text: str
        rating: int = 5
        device: Optional[str] = None

    class ScrollRequest(BaseModel):
        direction: str = "up"
        count: int = 3
        device: Optional[str] = None

    class BrowseRequest(BaseModel):
        duration: int = 30
        device: Optional[str] = None

    @app.get("/status")
    def api_status(device: Optional[str] = None):
        return cmd_status(device=device)

    @app.post("/login")
    def api_login(req: LoginRequest):
        return cmd_login(req.username, req.password, device=req.device)

    @app.post("/register")
    def api_register(req: RegisterRequest):
        return cmd_register(req.phone, req.password, device=req.device)

    @app.post("/search")
    def api_search(req: SearchRequest):
        return cmd_search(req.query, device=req.device)

    @app.post("/product")
    def api_product(req: ProductRequest):
        return cmd_product(req.query, device=req.device)

    @app.post("/cart")
    def api_cart(req: DeviceRequest):
        return cmd_cart(device=req.device)

    @app.post("/orders")
    def api_orders(req: OrdersRequest):
        return cmd_orders(device=req.device)

    @app.post("/like")
    def api_like(req: DeviceRequest):
        return cmd_like(device=req.device)

    @app.post("/review")
    def api_review(req: ReviewRequest):
        return cmd_review(req.text, req.rating, device=req.device)

    @app.get("/scroll")
    def api_scroll(direction: str = "up", count: int = 3, device: Optional[str] = None):
        return cmd_scroll(direction=direction, count=count, device=device)

    @app.post("/browse")
    def api_browse(req: BrowseRequest):
        return cmd_browse_shopee(duration=req.duration, device=req.device)

    print(f"[shopee] Starting server on port {port}...", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Control Shopee Indonesia Android app via ADB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s status
  %(prog)s open --device SGZTONV4OBL74TJZ
  %(prog)s login --username user@email.com --password P@ss123
  %(prog)s register --phone 081234567890 --password P@ss123
  %(prog)s orders
  %(prog)s search --query "iPhone 15"
  %(prog)s product --query "iPhone 15"
  %(prog)s cart
  %(prog)s like
  %(prog)s review --text "Produk bagus!" --rating 5
  %(prog)s screenshot --out /tmp/shopee.png
  %(prog)s server --port 8767
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status", help="Check if Shopee app is installed")
    p_status.add_argument("--device", "-d", help="ADB device serial")

    p_open = sub.add_parser("open", help="Launch Shopee and dismiss popups")
    p_open.add_argument("--device", "-d", help="ADB device serial")

    p_login = sub.add_parser("login", help="Login to Shopee account")
    p_login.add_argument("--username", "-u", required=True, help="Username/email/phone")
    p_login.add_argument("--password", "-p", required=True, help="Password")
    p_login.add_argument("--device", "-d", help="ADB device serial")

    p_register = sub.add_parser("register", help="Register a new Shopee account")
    p_register.add_argument("--phone", required=True, help="Phone number")
    p_register.add_argument("--password", "-p", required=True, help="Password")
    p_register.add_argument("--device", "-d", help="ADB device serial")

    p_orders = sub.add_parser("orders", help="Open orders page and screenshot")
    p_orders.add_argument("--device", "-d", help="ADB device serial")

    p_search = sub.add_parser("search", help="Search for a product")
    p_search.add_argument("--query", "-q", required=True, help="Search query")
    p_search.add_argument("--device", "-d", help="ADB device serial")

    p_product = sub.add_parser("product", help="Search and open first product detail")
    p_product.add_argument("--query", "-q", required=True, help="Search query")
    p_product.add_argument("--device", "-d", help="ADB device serial")

    p_cart = sub.add_parser("cart", help="View shopping cart")
    p_cart.add_argument("--device", "-d", help="ADB device serial")

    p_like = sub.add_parser("like", help="Wishlist/favorite the current product")
    p_like.add_argument("--device", "-d", help="ADB device serial")

    p_review = sub.add_parser("review", help="Review a delivered order")
    p_review.add_argument("--text", "-t", required=True, help="Review text")
    p_review.add_argument(
        "--rating", "-r", type=int, default=5, choices=[1, 2, 3, 4, 5], help="Star rating (1-5)"
    )
    p_review.add_argument("--device", "-d", help="ADB device serial")

    p_scroll = sub.add_parser("scroll", help="Scroll current Shopee page with natural swipes")
    p_scroll.add_argument("--direction", default="up", choices=["up", "down"], help="Swipe direction (default: up)")
    p_scroll.add_argument("--count", "-n", type=int, default=3, help="Number of swipes (default: 3)")
    p_scroll.add_argument("--device", "-d", help="ADB device serial")

    p_browse = sub.add_parser("browse", help="Scroll Shopee home feed for N seconds")
    p_browse.add_argument("--duration", type=int, default=30, help="Browse duration in seconds (default: 30)")
    p_browse.add_argument("--device", "-d", help="ADB device serial")

    p_server = sub.add_parser("server", help="Run FastAPI server")
    p_server.add_argument(
        "--port", "-p", type=int, default=8767, help="Server port (default: 8767)"
    )

    p_ss = sub.add_parser("screenshot", help="Take a screenshot")
    p_ss.add_argument("--device", "-d", help="ADB device serial")
    p_ss.add_argument("--out", "-o", help="Output PNG path")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(device=args.device)
    elif args.command == "open":
        cmd_open(device=args.device)
    elif args.command == "login":
        cmd_login(args.username, args.password, device=args.device)
    elif args.command == "register":
        cmd_register(args.phone, args.password, device=args.device)
    elif args.command == "orders":
        cmd_orders(device=args.device)
    elif args.command == "search":
        cmd_search(args.query, device=args.device)
    elif args.command == "product":
        cmd_product(args.query, device=args.device)
    elif args.command == "cart":
        cmd_cart(device=args.device)
    elif args.command == "like":
        cmd_like(device=args.device)
    elif args.command == "review":
        cmd_review(args.text, args.rating, device=args.device)
    elif args.command == "scroll":
        cmd_scroll(direction=args.direction, count=args.count, device=args.device)
    elif args.command == "browse":
        cmd_browse_shopee(duration=args.duration, device=args.device)
    elif args.command == "server":
        run_server(port=args.port)
    elif args.command == "screenshot":
        cmd_screenshot(device=args.device, out=args.out)


if __name__ == "__main__":
    main()
