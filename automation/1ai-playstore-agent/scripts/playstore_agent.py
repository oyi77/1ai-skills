#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] # .../1ai-skills
AUTODROID = Path.home() / ".openclaw" / "workspace" / "skills" / "1ai-autodroid" / "scripts" / "autodroid.py"

PLAY_STORE_PACKAGE = "com.android.vending"


def run(cmd: str) -> subprocess.CompletedProcess:
 return subprocess.run(cmd, shell=True, text=True, capture_output=True)


def adb_shell(cmd: str) -> subprocess.CompletedProcess:
 return run(f"adb shell {cmd}")


def status(package: str) -> int:
 r = adb_shell(f"pm list packages | grep -i {package}")
 if r.returncode ==0 and package in r.stdout:
 print(f"INSTALLED: {package}")
 return0
 print(f"NOT INSTALLED: {package}")
 return1


def open_store() -> int:
 # use autodroid launch for consistency
 if not AUTODROID.exists():
 print("autodroid.py not found; ensure1ai-autodroid is installed", file=sys.stderr)
 return1
 r = run(f"python3 '{AUTODROID}' launch {PLAY_STORE_PACKAGE}")
 sys.stdout.write(r.stdout)
 sys.stderr.write(r.stderr)
 return r.returncode


def search(query: str) -> int:
 # simple flow: open store, tap search box, type query
 if open_store() !=0:
 return1
 # small delay to let UI settle
 run("sleep2")
 # tap search field by text; may need tuning per-device
 run(f"python3 '{AUTODROID}' tap-text 'Search for apps & games'")
 run("sleep1")
 r = run(f"python3 '{AUTODROID}' type-text '{query}'")
 sys.stdout.write(r.stdout)
 sys.stderr.write(r.stderr)
 return0


def install_by_name(name: str) -> int:
 # best-effort: search then try tap "Install"
 if search(name) !=0:
 return1
 run("sleep3")
 # try tap Install button
 r = run(f"python3 '{AUTODROID}' tap-text 'Install'")
 sys.stdout.write(r.stdout)
 sys.stderr.write(r.stderr)
 return r.returncode


def main():
 p = argparse.ArgumentParser(description="Play Store helper on top of1ai-autodroid")
 sub = p.add_subparsers(dest="cmd", required=True)

 sp_status = sub.add_parser("status", help="check if package is installed")
 sp_status.add_argument("--package", required=True)

 sub.add_parser("open-store", help="open Play Store app")

 sp_search = sub.add_parser("search", help="search app by name in Play Store")
 sp_search.add_argument("--query", required=True)

 sp_install = sub.add_parser("install", help="attempt install by app name")
 sp_install.add_argument("--name", required=True)

 args = p.parse_args()

 if args.cmd == "status":
 sys.exit(status(args.package))
 elif args.cmd == "open-store":
 sys.exit(open_store())
 elif args.cmd == "search":
 sys.exit(search(args.query))
 elif args.cmd == "install":
 sys.exit(install_by_name(args.name))


if __name__ == "__main__":
 main()
