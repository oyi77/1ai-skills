#!/usr/bin/env python3
"""
Play Store Agent — Android automation built on top of 1ai-autodroid.

Subcommands:
  status --package <pkg>    Check if package is installed
  open-store                Launch Play Store and dismiss promos
  search --query <term>     Search for an app
  install --name <app>      Install app by name
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

# ─── Paths ──────────────────────────────────────────────────────────────────
AUTODROID = (
    Path.home()
    / ".openclaw"
    / "workspace"
    / "skills"
    / "1ai-autodroid"
    / "scripts"
    / "autodroid.py"
)
PLAY_STORE_PACKAGE = "com.android.vending"

# Promo-dismiss button labels Play Store may show
DISMISS_LABELS = [
    "Skip",
    "Not now",
    "No thanks",
    "Close",
    "Got it",
    "Dismiss",
    "Cancel",
]


# ─── Helpers ────────────────────────────────────────────────────────────────
def run(cmd: str) -> subprocess.CompletedProcess:
    """Run a shell command, capture output."""
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)


def adb_shell(cmd: str) -> subprocess.CompletedProcess:
    """Shortcut: adb shell <cmd>."""
    return run(f"adb shell {cmd}")


def autodroid(args: str) -> subprocess.CompletedProcess:
    """Call autodroid.py with the given argument string."""
    return run(f"python3 '{AUTODROID}' {args}")


# ─── Dismiss promos ─────────────────────────────────────────────────────────
def dismiss_promos() -> None:
    """Try tapping common promo/dismiss buttons. Silently ignore misses."""
    for label in DISMISS_LABELS:
        # autodroid tap-text prints an error when text not found but never raises
        r = autodroid(f"tap-text '{label}'")
        # Small pause so the UI settles between attempts
        time.sleep(0.5)


# ─── Subcommands ─────────────────────────────────────────────────────────────
def status(package: str) -> int:
    """Return 0 if <package> is installed, 1 otherwise."""
    r = adb_shell(f"pm list packages | grep -i {package}")
    if r.returncode == 0 and package in r.stdout:
        print(f"INSTALLED: {package}")
        return 0
    print(f"NOT INSTALLED: {package}")
    return 1


def open_store() -> int:
    """Launch Play Store, wait 2 s, then dismiss promos."""
    if not AUTODROID.exists():
        print(
            "autodroid.py not found; ensure 1ai-autodroid is installed", file=sys.stderr
        )
        return 1
    r = autodroid(f"launch {PLAY_STORE_PACKAGE}")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        return r.returncode
    time.sleep(2)
    dismiss_promos()
    return 0


def search(query: str) -> int:
    """Open Play Store, tap Search tab, type query, submit."""
    if open_store() != 0:
        return 1
    time.sleep(1)
    # Tap "Telusuri" (Search) tab in bottom nav — reliable coordinate on 720x1640 screen
    run("adb shell input tap 450 1462")
    time.sleep(1)
    # Tap the search input field at top of search page
    run("adb shell input tap 360 80")
    time.sleep(0.5)
    r = autodroid(f"type '{query}'")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    # Submit search
    run("adb shell input keyevent 66")
    time.sleep(3)
    return 0


def install_by_name(name: str) -> int:
    """Search for <name> in Play Store, then tap Install."""
    if search(name) != 0:
        return 1
    time.sleep(2)
    # Parse UI dump to find the correct Install/Instal button for target app
    import xml.etree.ElementTree as ET, re
    try:
        tree = ET.parse("/tmp/autodroid_ui.xml")
        # Find all nodes that look like Install buttons (content-desc or text = Instal/Install)
        buttons = []
        for el in tree.iter():
            txt = el.get("text", "")
            desc = el.get("content-desc", "")
            bounds = el.get("bounds", "")
            if txt in ["Install", "Instal", "Pasang"] or desc in ["Install", "Instal"]:
                m = re.findall(r"\d+", bounds)
                if m and len(m) == 4:
                    cx = (int(m[0]) + int(m[2])) // 2
                    cy = (int(m[1]) + int(m[3])) // 2
                    buttons.append((cy, cx))  # sort by Y position
        if not buttons:
            print("Install button not found in UI dump", file=sys.stderr)
            return 1
        # Tap the LAST install button (usually the target app, not sponsored top result)
        buttons.sort()
        cy, cx = buttons[-1]
        print(f"Tapping Install at ({cx},{cy})")
        run(f"adb shell input tap {cx} {cy}")
        time.sleep(2)
        print("Install tapped successfully")
        return 0
    except Exception as e:
        print(f"UI parse error: {e}", file=sys.stderr)
        return 1


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Play Store helper built on top of 1ai-autodroid"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp_status = sub.add_parser("status", help="check if package is installed")
    sp_status.add_argument("--package", required=True)

    sub.add_parser("open-store", help="open Play Store app")

    sp_search = sub.add_parser("search", help="search app by name")
    sp_search.add_argument("--query", required=True)

    sp_install = sub.add_parser("install", help="attempt install by app name")
    sp_install.add_argument("--name", required=True)

    args = parser.parse_args()

    if args.cmd == "status":
        sys.exit(status(args.package))
    if args.cmd == "open-store":
        sys.exit(open_store())
    if args.cmd == "search":
        sys.exit(search(args.query))
    if args.cmd == "install":
        sys.exit(install_by_name(args.name))


if __name__ == "__main__":
    main()
