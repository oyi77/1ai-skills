#!/usr/bin/env python3
"""
kling_account_generator_cli.py — Thin CLI wrapper for KlingAccountGenerator.

Usage:
    python3 kling_account_generator_cli.py --count 5 --proxy-list proxies.txt
    python3 kling_account_generator_cli.py --count 1 --proxy http://user:pass@host:port
    python3 kling_account_generator_cli.py --list
    python3 kling_account_generator_cli.py --export-cookies

Accounts saved to: ~/.openclaw/workspace/config/kling_accounts.json
Logs:             ~/.openclaw/workspace/logs/kling_generator.log
"""

import sys
import json
import argparse
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).parent))
from kling_account_generator import KlingAccountGenerator, DEFAULT_ACCOUNTS_PATH


def main():
    parser = argparse.ArgumentParser(
        prog="kling_account_generator_cli",
        description="Kling AI Account Generator — temp email + proxy rotation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 1 account (no proxy)
  python3 kling_account_generator_cli.py --count 1

  # Generate 5 accounts with proxy rotation
  python3 kling_account_generator_cli.py --count 5 --proxy-list proxies.txt

  # Single proxy
  python3 kling_account_generator_cli.py --count 3 --proxy http://user:pass@1.2.3.4:8080

  # List saved accounts
  python3 kling_account_generator_cli.py --list

  # Export only successful accounts with cookies
  python3 kling_account_generator_cli.py --export-cookies

  # Custom output path
  python3 kling_account_generator_cli.py --count 2 --output /tmp/kling.json
        """,
    )

    parser.add_argument("--count", "-n", type=int, default=1,
                        help="Number of accounts to generate (default: 1)")
    parser.add_argument("--proxy", "-p", type=str, default=None,
                        help="Single proxy: http://user:pass@host:port")
    parser.add_argument("--proxy-list", "-P", type=str, default=None,
                        help="File with one proxy per line (rotated)")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help=f"JSON output file (default: {DEFAULT_ACCOUNTS_PATH})")
    parser.add_argument("--otp-timeout", type=int, default=90,
                        help="Seconds to wait for OTP email (default: 90)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all saved accounts and exit")
    parser.add_argument("--export-cookies", "-e", action="store_true",
                        help="Export successful accounts as cookies list")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output results as JSON (for piping)")
    args = parser.parse_args()

    # Init generator
    output_path = Path(args.output) if args.output else None
    gen = KlingAccountGenerator(accounts_path=output_path, otp_timeout=args.otp_timeout)

    # ── List mode ──────────────────────────────────────────────────────────────
    if args.list:
        accounts = gen.list_accounts()
        if args.json:
            print(json.dumps(accounts, indent=2))
        else:
            print(f"\n{'='*70}")
            print(f"  Saved Accounts ({len(accounts)} total) — {gen.accounts_path}")
            print(f"{'='*70}")
            ok = sum(1 for a in accounts if a.get("success"))
            print(f"  ✅ Successful: {ok} | ❌ Failed: {len(accounts) - ok}")
            print(f"{'='*70}")
            for i, acc in enumerate(accounts, 1):
                status = "✅" if acc.get("success") else "❌"
                cookie_preview = acc.get("cookie", "")[:40] + "..." if acc.get("cookie") else "—"
                print(
                    f"  {i:3}. {status} "
                    f"{acc.get('email', 'unknown'):<40} "
                    f"credits={acc.get('credits', 0):<8} "
                    f"ts={acc.get('timestamp', '')[:19]}"
                )
        return

    # ── Export cookies ─────────────────────────────────────────────────────────
    if args.export_cookies:
        cookies = gen.export_cookies()
        if args.json:
            print(json.dumps(cookies, indent=2))
        else:
            print(f"\n{'='*70}")
            print(f"  Successful Accounts with Cookies ({len(cookies)} total)")
            print(f"{'='*70}")
            for acc in cookies:
                print(f"  Email:  {acc.get('email')}")
                print(f"  Cookie: {acc.get('cookie', '')[:80]}...")
                print(f"  Credits: {acc.get('credits', 0)}")
                print()
        return

    # ── Load proxies ───────────────────────────────────────────────────────────
    proxy_list = None
    if args.proxy_list:
        pfile = Path(args.proxy_list)
        if not pfile.exists():
            print(f"❌ Proxy file not found: {pfile}")
            sys.exit(1)
        with open(pfile) as f:
            proxy_list = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"  Loaded {len(proxy_list)} proxies from {pfile}")
    elif args.proxy:
        proxy_list = [args.proxy]

    # ── Generate ───────────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print(f"  Kling Account Generator")
    print(f"  Count: {args.count} | Proxies: {len(proxy_list) if proxy_list else 0} | OTP timeout: {args.otp_timeout}s")
    print(f"  Output: {gen.accounts_path}")
    print(f"{'='*70}\n")

    if args.count == 1:
        proxy = proxy_list[0] if proxy_list else None
        result = gen.generate_account(proxy=proxy)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            _print_result(result)
        sys.exit(0 if result["success"] else 1)
    else:
        results = gen.batch_generate(count=args.count, proxy_list=proxy_list)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            _print_batch_summary(results, gen.accounts_path)
        ok = sum(1 for r in results if r.get("success"))
        sys.exit(0 if ok > 0 else 1)


def _print_result(result: dict):
    status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
    print(f"\n  Result: {status}")
    print(f"  Email:    {result.get('email', '—')}")
    print(f"  Password: {result.get('password', '—')}")
    if result.get("cookie"):
        print(f"  Cookie:   {result['cookie'][:60]}...")
    print(f"  Credits:  {result.get('credits', 0)}")
    if result.get("error"):
        print(f"  Error:    {result['error']}")


def _print_batch_summary(results: list, output_path: Path):
    ok = sum(1 for r in results if r.get("success"))
    print(f"\n{'='*70}")
    print(f"  Batch complete: {ok}/{len(results)} succeeded")
    print(f"{'='*70}")
    for i, r in enumerate(results, 1):
        status = "✅" if r.get("success") else "❌"
        err = r.get("error") or "OK"
        print(f"  {i:3}. {status} {r.get('email', '?'):<40} — {err}")
    print(f"\n  Accounts saved to: {output_path}")


if __name__ == "__main__":
    main()
