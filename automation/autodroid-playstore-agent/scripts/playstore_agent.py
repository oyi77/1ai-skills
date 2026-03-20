#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../1ai-skills
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


def run(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)


def adb_shell(cmd: str) -> subprocess.CompletedProcess:
    return run(f"adb shell {cmd}")


def status(package: str) -> int:
    r = adb_shell(f"pm list packages | grep -i {package}")
    if r.returncode == 0 and package in r.stdout:
        print(f"INSTALLED: {package}")
        return 0
    print(f"NOT INSTALLED: {package}")
    return 1


def open_store() -> int:
    if not AUTODROID.exists():
        print(
            "autodroid.py not found; ensure 1ai-autodroid is installed",
            file=sys.stderr,
        )
        return 1
    r = run(f"python3 '{AUTODROID}' launch {PLAY_STORE_PACKAGE}")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


def search(query: str) -> int:
    if open_store() != 0:
        return 1
    run("sleep 2")
    run(f"python3 '{AUTODROID}' tap-text 'Search for apps & games'")
    run("sleep 1")
    r = run(f"python3 '{AUTODROID}' type '{query}'")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return 0


def install_by_name(name: str) -> int:
    if search(name) != 0:
        return 1
    run("sleep 3")
    r = run(f"python3 '{AUTODROID}' tap-text 'Install'")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode


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
