#!/usr/bin/env python3
"""
autodroid-playstore-agent v2.0 — Robust Play Store automation via ADB.

Commands:
  status --package <pkg>            Check if package is installed
  devices                           List connected ADB devices
  open-store                        Launch Play Store
  search --query <term>             Search app by name, return results
  install --package <pkg>           Install by package ID (most reliable)
  install --name <name>             Install by app name (fallback search)
  uninstall --package <pkg>         Uninstall app
  screenshot [--out path]           Take screenshot
  server [--port 8771]              Start FastAPI server

Strategy for install (tried in order):
  1. Direct market:// URI → find Instal button via UI dump
  2. Play Store search → tap first result → find Instal button
  3. adb install fallback (requires APK path)
"""

import argparse
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────

PACKAGE = "com.android.vending"
DOWNLOADS = Path.home() / ".openclaw/workspace/downloads"
DOWNLOADS.mkdir(parents=True, exist_ok=True)

INSTALL_LABELS   = {"Instal", "Install", "Pasang"}
DISMISS_LABELS   = {
    "Skip", "Lewati", "Not now", "Nanti", "No thanks",
    "Close", "Tutup", "Got it", "Dismiss", "Cancel",
    "Batal", "OK", "Allow", "Izinkan", "Continue", "Lanjutkan",
}
UNINSTALL_LABELS = {"Uninstall", "Uninstal", "Hapus instalan"}
OPEN_LABELS      = {"Open", "Buka"}


# ─── ADB helpers ──────────────────────────────────────────────────────────────

def adb(cmd, device=None, timeout=10):
    prefix = ["adb"] + (["-s", device] if device else []) + ["shell"]
    try:
        r = subprocess.run(prefix + cmd.split(), capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""


def adb_run(cmd, device=None, timeout=15):
    """Run adb (non-shell) command."""
    prefix = ["adb"] + (["-s", device] if device else [])
    try:
        r = subprocess.run(prefix + cmd.split(), capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def wake(device=None):
    adb("input keyevent 224", device=device)  # KEYCODE_WAKEUP
    time.sleep(0.3)
    adb("input swipe 360 900 360 300", device=device)  # unlock swipe
    time.sleep(0.3)


def screencap(path, device=None):
    path = str(path)
    prefix = ["adb"] + (["-s", device] if device else [])
    cmd = prefix + ["exec-out", "screencap", "-p"]
    try:
        with open(path, "wb") as f:
            subprocess.run(cmd, stdout=f, timeout=10, check=True)
        return path
    except Exception:
        return None


def dump_ui(device=None):
    """Dump UI hierarchy, return list of node dicts."""
    adb("uiautomator dump /sdcard/_ui.xml", device=device, timeout=15)
    rc, _, _ = adb_run(f"pull /sdcard/_ui.xml /tmp/_ps_ui.xml", device=device)
    nodes = []
    try:
        root = ET.parse("/tmp/_ps_ui.xml").getroot()
        for n in root.iter():
            nodes.append({
                "text": n.get("text", ""),
                "desc": n.get("content-desc", ""),
                "class": n.get("class", ""),
                "bounds": n.get("bounds", ""),
                "clickable": n.get("clickable", "false") == "true",
                "resource_id": n.get("resource-id", ""),
            })
    except Exception:
        pass
    return nodes


def bounds_center(bounds_str):
    """'[x1,y1][x2,y2]' → (cx, cy)"""
    nums = list(map(int, re.findall(r"\d+", bounds_str)))
    if len(nums) == 4:
        return (nums[0] + nums[2]) // 2, (nums[1] + nums[3]) // 2
    return None


def find_node(nodes, label=None, labels=None, partial=False, cls=None):
    """Find first node matching label(s), optionally filtered by class."""
    check = labels or ({label} if label else set())
    for n in nodes:
        t = n["text"].strip()
        d = n["desc"].strip()
        match = any(
            (c in t or c in d) if partial else (t == c or d == c)
            for c in check
        )
        if match:
            if cls and cls not in n["class"]:
                continue
            return n
    return None


def tap(x, y, device=None):
    adb(f"input tap {x} {y}", device=device)
    time.sleep(0.4)


def tap_node(nodes, label=None, labels=None, partial=False, device=None):
    n = find_node(nodes, label=label, labels=labels, partial=partial)
    if n and n["bounds"]:
        c = bounds_center(n["bounds"])
        if c:
            tap(c[0], c[1], device=device)
            return True
    return False


def list_devices():
    r = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    out = []
    for line in r.stdout.strip().splitlines()[1:]:
        if "\tdevice" in line:
            serial = line.split("\t")[0].strip()
            model   = adb("getprop ro.product.model", device=serial)
            android = adb("getprop ro.build.version.release", device=serial)
            out.append({"serial": serial, "model": model, "android": android})
    return out


def is_installed(package, device=None):
    out = adb(f"pm list packages {package}", device=device)
    return package in out


# ─── Play Store navigation ────────────────────────────────────────────────────

def launch_playstore(device=None):
    wake(device=device)
    adb(f"am force-stop {PACKAGE}", device=device)
    time.sleep(0.3)
    adb(f"am start -a android.intent.action.MAIN -n {PACKAGE}/com.google.android.finsky.activities.MainActivity", device=device)
    time.sleep(3)


def dismiss_popups(nodes, device=None):
    dismissed = False
    for label in DISMISS_LABELS:
        if tap_node(nodes, label=label, device=device):
            dismissed = True
            time.sleep(0.3)
    return dismissed


def open_app_detail_by_package(package, device=None):
    """Open Play Store detail page for a package via market:// URI."""
    wake(device=device)
    adb(f"am start -a android.intent.action.VIEW -d market://details?id={package} {PACKAGE}", device=device)
    time.sleep(4)
    nodes = dump_ui(device=device)
    dismiss_popups(nodes, device=device)
    return dump_ui(device=device)


def find_install_button(nodes):
    """Find Instal/Install button, return (x, y) or None."""
    for n in nodes:
        t = n["text"].strip()
        d = n["desc"].strip()
        if t in INSTALL_LABELS or d in INSTALL_LABELS:
            c = bounds_center(n["bounds"])
            if c:
                return c
    return None


def find_open_button(nodes):
    for n in nodes:
        t = n["text"].strip()
        if t in OPEN_LABELS:
            c = bounds_center(n["bounds"])
            if c:
                return c
    return None


def wait_for_install(package, timeout=120, device=None):
    """Poll until package appears in pm list or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if is_installed(package, device=device):
            return True
        time.sleep(5)
    return False


# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_status(package, device=None):
    devs = list_devices()
    installed = is_installed(package, device=device)
    result = {
        "ok": True,
        "installed": installed,
        "package": package,
        "device": device or (devs[0]["serial"] if devs else "none"),
        "model": devs[0]["model"] if devs else "unknown",
        "connected_devices": [d["serial"] for d in devs],
    }
    print(json.dumps(result, indent=2))
    return 0


def cmd_devices():
    devs = list_devices()
    print(json.dumps({"ok": True, "devices": devs, "count": len(devs)}, indent=2))
    return 0


def cmd_open_store(device=None):
    launch_playstore(device=device)
    shot = screencap(DOWNLOADS / "playstore_open.png", device=device)
    nodes = dump_ui(device=device)
    dismiss_popups(nodes, device=device)
    print(json.dumps({"ok": True, "screenshot_path": shot, "device": device or "default"}, indent=2))
    return 0


def cmd_search(query, device=None):
    """Search Play Store, return first 5 app names."""
    launch_playstore(device=device)
    nodes = dump_ui(device=device)
    dismiss_popups(nodes, device=device)

    # Tap search tab (bottom nav "Telusuri")
    if not tap_node(nodes, label="Telusuri", device=device):
        tap(449, 1518, device=device)  # fallback coordinate
    time.sleep(1.5)

    nodes = dump_ui(device=device)
    # Tap search input
    if not tap_node(nodes, label="Telusuri aplikasi & game", device=device):
        tap(360, 124, device=device)
    time.sleep(0.8)

    # Type query
    adb(f"input text {query.replace(' ', '%s')}", device=device)
    time.sleep(0.5)
    adb("input keyevent 66", device=device)  # Enter
    time.sleep(3)

    nodes = dump_ui(device=device)
    shot = screencap(DOWNLOADS / "playstore_search.png", device=device)

    # Collect app names (TextViews in results)
    results = []
    for n in nodes:
        t = n["text"].strip()
        if t and len(t) > 2 and n["class"].endswith("TextView"):
            if t not in {"Telusuri", "Google Play", "Instal", "Buka", query}:
                results.append(t)
        if len(results) >= 10:
            break

    print(json.dumps({
        "ok": True, "query": query, "results": results[:5],
        "screenshot_path": shot, "device": device or "default"
    }, indent=2))
    return 0


def cmd_install(package=None, name=None, device=None, wait=True):
    """
    Install an app. Strategy:
    1. market:// URI → find Instal button via UI dump
    2. Fallback: search by name → tap first result → find Instal button
    Returns JSON {ok, installed, package, strategy, device}
    """
    devs = list_devices()
    dev_serial = device or (devs[0]["serial"] if devs else None)

    # Already installed?
    if package and is_installed(package, device=device):
        print(json.dumps({
            "ok": True, "already_installed": True,
            "package": package, "device": dev_serial or "default"
        }, indent=2))
        return 0

    screenshot_path = str(DOWNLOADS / "playstore_install.png")
    strategies_tried = []

    # ── Strategy 1: market:// URI ──────────────────────────────────────────
    if package:
        strategies_tried.append("market_uri")
        print(f"[install] Strategy 1: market://{package}", file=sys.stderr)
        nodes = open_app_detail_by_package(package, device=device)
        screencap(screenshot_path, device=device)

        btn = find_install_button(nodes)
        if btn:
            print(f"[install] Found Instal at {btn}", file=sys.stderr)
            tap(btn[0], btn[1], device=device)
            time.sleep(2)
            screencap(screenshot_path, device=device)

            if wait:
                print(f"[install] Waiting for install (max 120s)...", file=sys.stderr)
                success = wait_for_install(package, timeout=120, device=device)
                if success:
                    print(json.dumps({
                        "ok": True, "installed": True, "package": package,
                        "strategy": "market_uri", "screenshot_path": screenshot_path,
                        "device": dev_serial or "default"
                    }, indent=2))
                    return 0
        else:
            # Check if already installed (button shows "Buka" instead)
            open_btn = find_open_button(nodes)
            if open_btn:
                print(json.dumps({
                    "ok": True, "already_installed": True,
                    "package": package, "device": dev_serial or "default"
                }, indent=2))
                return 0
            print(f"[install] Instal button not found via market:// — trying strategy 2", file=sys.stderr)

    # ── Strategy 2: Search by name ─────────────────────────────────────────
    search_term = name or package
    if search_term:
        strategies_tried.append("search_by_name")
        print(f"[install] Strategy 2: search '{search_term}'", file=sys.stderr)

        launch_playstore(device=device)
        nodes = dump_ui(device=device)
        dismiss_popups(nodes, device=device)

        # Tap search tab
        if not tap_node(nodes, label="Telusuri", device=device):
            tap(449, 1518, device=device)
        time.sleep(1.5)
        nodes = dump_ui(device=device)

        # Tap search bar
        if not tap_node(nodes, label="Telusuri aplikasi & game", device=device):
            tap(360, 124, device=device)
        time.sleep(0.8)

        # Type app name
        adb(f"input text {search_term.replace(' ', '%s')}", device=device)
        time.sleep(0.5)
        adb("input keyevent 66", device=device)
        time.sleep(3)

        # Tap first result
        nodes = dump_ui(device=device)
        tap(360, 220, device=device)  # first result row
        time.sleep(3)

        # Now on detail page — look for Instal button
        nodes = dump_ui(device=device)
        screencap(screenshot_path, device=device)
        btn = find_install_button(nodes)

        if btn:
            print(f"[install] Found Instal at {btn}", file=sys.stderr)
            tap(btn[0], btn[1], device=device)
            time.sleep(2)
            screencap(screenshot_path, device=device)

            if package and wait:
                print(f"[install] Waiting for install...", file=sys.stderr)
                success = wait_for_install(package, timeout=120, device=device)
                if success:
                    print(json.dumps({
                        "ok": True, "installed": True,
                        "package": package or search_term,
                        "strategy": "search_by_name", "screenshot_path": screenshot_path,
                        "device": dev_serial or "default"
                    }, indent=2))
                    return 0
            else:
                # No package to verify — assume success if button was tapped
                print(json.dumps({
                    "ok": True, "installed": None,
                    "note": "Install tapped but cannot verify (no --package given)",
                    "screenshot_path": screenshot_path,
                    "device": dev_serial or "default"
                }, indent=2))
                return 0
        else:
            open_btn = find_open_button(nodes)
            if open_btn:
                print(json.dumps({
                    "ok": True, "already_installed": True,
                    "package": package or search_term, "device": dev_serial or "default"
                }, indent=2))
                return 0

    # ── All strategies failed ──────────────────────────────────────────────
    screencap(screenshot_path, device=device)
    print(json.dumps({
        "ok": False,
        "error": "Install button not found after all strategies",
        "strategies_tried": strategies_tried,
        "package": package, "name": name,
        "screenshot_path": screenshot_path,
        "device": dev_serial or "default",
        "hint": "Check screenshot_path for current screen state"
    }, indent=2))
    return 1


def cmd_uninstall(package, device=None):
    devs = list_devices()
    if not is_installed(package, device=device):
        print(json.dumps({"ok": True, "note": "not installed", "package": package}, indent=2))
        return 0
    out = adb(f"pm uninstall -k --user 0 {package}", device=device)
    success = "Success" in out
    print(json.dumps({
        "ok": success, "package": package,
        "uninstalled": success, "adb_output": out,
        "device": device or (devs[0]["serial"] if devs else "default")
    }, indent=2))
    return 0 if success else 1


def cmd_screenshot(out=None, device=None):
    path = out or str(DOWNLOADS / "playstore_screenshot.png")
    wake(device=device)
    shot = screencap(path, device=device)
    print(json.dumps({"ok": bool(shot), "screenshot_path": shot, "device": device or "default"}, indent=2))
    return 0


def cmd_server(port=8771):
    try:
        from fastapi import FastAPI, Query
        from pydantic import BaseModel
        import uvicorn
    except ImportError:
        print("pip install fastapi uvicorn", file=sys.stderr)
        sys.exit(1)

    app = FastAPI(title="autodroid-playstore-agent", version="2.0")

    class InstallRequest(BaseModel):
        package: str = None
        name: str = None
        device: str = None
        wait: bool = True

    class UninstallRequest(BaseModel):
        package: str
        device: str = None

    @app.get("/health")
    def health():
        return {"status": "ok", "package": PACKAGE}

    @app.get("/status")
    def get_status(package: str, device: str = None):
        devs = list_devices()
        return {
            "ok": True, "installed": is_installed(package, device=device),
            "package": package, "device": device or (devs[0]["serial"] if devs else "none"),
            "connected_devices": [d["serial"] for d in devs]
        }

    @app.get("/devices")
    def get_devices():
        return {"ok": True, "devices": list_devices()}

    @app.post("/open-store")
    def post_open(device: str = None):
        launch_playstore(device=device)
        shot = screencap(DOWNLOADS / "playstore_open.png", device=device)
        return {"ok": True, "screenshot_path": shot, "device": device or "default"}

    @app.get("/search")
    def get_search(query: str, device: str = None):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cmd_search(query, device=device)
        try:
            return json.loads(buf.getvalue())
        except Exception:
            return {"ok": False, "error": buf.getvalue()}

    @app.post("/install")
    def post_install(req: InstallRequest):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cmd_install(package=req.package, name=req.name, device=req.device, wait=req.wait)
        try:
            return json.loads(buf.getvalue())
        except Exception:
            return {"ok": False, "error": buf.getvalue()}

    @app.post("/uninstall")
    def post_uninstall(req: UninstallRequest):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cmd_uninstall(req.package, device=req.device)
        try:
            return json.loads(buf.getvalue())
        except Exception:
            return {"ok": False, "error": buf.getvalue()}

    @app.get("/screenshot")
    def get_screenshot(device: str = None):
        wake(device=device)
        shot = screencap(DOWNLOADS / "playstore_screenshot.png", device=device)
        return {"ok": bool(shot), "screenshot_path": shot, "device": device or "default"}

    print(f"[playstore-agent] Running on http://0.0.0.0:{port}", file=sys.stderr)
    print(f"[playstore-agent] Docs: http://localhost:{port}/docs", file=sys.stderr)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="autodroid-playstore-agent v2.0")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("devices", help="list connected devices")

    sp = sub.add_parser("status", help="check if package is installed")
    sp.add_argument("--package", required=True)
    sp.add_argument("--device")

    sub.add_parser("open-store", help="launch Play Store").add_argument("--device", default=None)

    sp = sub.add_parser("search", help="search app by name")
    sp.add_argument("--query", required=True)
    sp.add_argument("--device")

    sp = sub.add_parser("install", help="install app by package or name")
    sp.add_argument("--package", default=None, help="package ID e.g. com.instagram.android")
    sp.add_argument("--name",    default=None, help="app name e.g. Instagram")
    sp.add_argument("--device")
    sp.add_argument("--no-wait", action="store_true")

    sp = sub.add_parser("uninstall", help="uninstall app")
    sp.add_argument("--package", required=True)
    sp.add_argument("--device")

    sp = sub.add_parser("screenshot")
    sp.add_argument("--out", default=None)
    sp.add_argument("--device")

    sp = sub.add_parser("server", help="start FastAPI server")
    sp.add_argument("--port", type=int, default=8771)

    args = p.parse_args()

    if args.cmd == "devices":
        sys.exit(cmd_devices())
    elif args.cmd == "status":
        sys.exit(cmd_status(args.package, device=getattr(args, "device", None)))
    elif args.cmd == "open-store":
        sys.exit(cmd_open_store(device=getattr(args, "device", None)))
    elif args.cmd == "search":
        sys.exit(cmd_search(args.query, device=getattr(args, "device", None)))
    elif args.cmd == "install":
        if not args.package and not args.name:
            print(json.dumps({"ok": False, "error": "Provide --package or --name"}), indent=2)
            sys.exit(1)
        sys.exit(cmd_install(
            package=args.package, name=args.name,
            device=getattr(args, "device", None),
            wait=not getattr(args, "no_wait", False)
        ))
    elif args.cmd == "uninstall":
        sys.exit(cmd_uninstall(args.package, device=getattr(args, "device", None)))
    elif args.cmd == "screenshot":
        sys.exit(cmd_screenshot(out=getattr(args, "out", None), device=getattr(args, "device", None)))
    elif args.cmd == "server":
        cmd_server(port=args.port)


if __name__ == "__main__":
    main()
