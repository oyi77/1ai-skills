"""
multi_account_example.py — Kling Multi-Account Credit Manager Demo

Demonstrates:
  - Adding multiple Kling accounts to the pool
  - Claiming daily login bonuses across all accounts
  - Selecting the best account for a task
  - Rotating accounts when credits are low
  - Viewing aggregate credit totals

Usage:
    python multi_account_example.py

Set KLING_ACCOUNTS_FILE env var to override default accounts.json location.
"""

import json
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("multi_account_example")


def demo_account_setup():
    """Show how to add accounts and check the pool."""
    from kling_account_manager import KlingAccountManager

    accounts_file = os.getenv(
        "KLING_ACCOUNTS_FILE",
        os.path.expanduser("~/.openclaw/workspace/config/kling_accounts.json"),
    )

    print("=" * 60)
    print("  KLING ACCOUNT MANAGER DEMO")
    print("=" * 60)

    mgr = KlingAccountManager(accounts_file=accounts_file)
    print(f"\n📁 Accounts file: {accounts_file}")
    print(f"📊 Loaded accounts: {len(mgr._accounts)}")

    # Show current summary
    summary = mgr.account_summary()
    if summary:
        print("\n📋 Account Summary:")
        for acc in summary:
            status = "✅" if acc["active"] else "❌"
            credits = f"{acc['credits']:.0f}"
            last = acc.get("last_bonus_claimed", "never") or "never"
            print(f"  {status} {acc['email_masked']:25s} | credits={credits:>8} | last_bonus={last}")
        print(f"\n💰 Total Credits: {mgr.get_total_credits():.0f}")
    else:
        print("\n⚠️  No accounts loaded. Add accounts with:")
        print("   mgr.add_account('email@example.com', 'password')")

    return mgr


def demo_best_account_selection(mgr):
    """Show account selection logic."""
    print("\n" + "=" * 60)
    print("  ACCOUNT SELECTION")
    print("=" * 60)

    min_credits = 60  # text2video costs 60 credits
    best = mgr.get_best_account(min_credits=min_credits)

    if best:
        print(f"\n✅ Best account for text2video (min={min_credits} credits):")
        print(f"   Email:   {best.get('email', 'unknown')}")
        print(f"   Credits: {best.get('credits', 0):.0f}")
    else:
        print(f"\n❌ No account has >= {min_credits} credits.")
        print("   Add accounts or claim daily bonuses first.")

    # Rotation demo
    print("\n🔄 Rotation test (simulating low credits = 30):")
    new_account = mgr.rotate_if_low(current_credits=30.0, threshold=60.0)
    if new_account:
        print(f"   → Rotated to: {new_account.get('email', 'unknown')} ({new_account.get('credits', 0):.0f} credits)")
    else:
        print("   → No rotation needed (or no other accounts available).")

    return best


def demo_daily_bonus(mgr):
    """Show daily bonus claiming."""
    print("\n" + "=" * 60)
    print("  DAILY BONUS CLAIMING")
    print("=" * 60)

    if not mgr._accounts:
        print("\n⚠️  No accounts to claim bonus for.")
        return

    print("\n🎁 Claiming daily login bonuses for all accounts...")
    result = mgr.claim_all_daily_bonuses()

    print(f"\n  Claimed: {len(result['claimed'])} accounts")
    for email in result["claimed"]:
        print(f"    ✅ {email}")

    if result["failed"]:
        print(f"  Failed:  {len(result['failed'])} accounts")
        for email in result["failed"]:
            print(f"    ❌ {email}")

    print(f"\n💰 Total Credits After Bonus: {mgr.get_total_credits():.0f}")


def demo_add_account_instructions():
    """Show how to add accounts programmatically."""
    print("\n" + "=" * 60)
    print("  HOW TO ADD ACCOUNTS")
    print("=" * 60)
    print("""
To add a Kling account to the pool:

    from kling_account_manager import KlingAccountManager
    mgr = KlingAccountManager()
    
    # Add a single account
    success = mgr.add_account("myemail@gmail.com", "mypassword123")
    print(f"Account added: {success}")
    
    # Add multiple accounts
    accounts = [
        ("account1@gmail.com", "pass1"),
        ("account2@gmail.com", "pass2"),
        ("account3@gmail.com", "pass3"),
    ]
    for email, password in accounts:
        mgr.add_account(email, password)
    
    # View total credits
    print(f"Total credits: {mgr.get_total_credits():.0f}")
    
    # Claim all daily bonuses
    result = mgr.claim_all_daily_bonuses()
    print(f"Bonuses claimed: {len(result['claimed'])}")

JSON file format (~/.openclaw/workspace/config/kling_accounts.json):
""")
    example = [
        {
            "email": "account1@example.com",
            "password": "password1",
            "cookie": "",
            "credits": 1200.0,
            "active": True,
        }
    ]
    print("    " + json.dumps(example, indent=4).replace("\n", "\n    "))


if __name__ == "__main__":
    mgr = demo_account_setup()
    demo_best_account_selection(mgr)
    demo_daily_bonus(mgr)
    demo_add_account_instructions()
