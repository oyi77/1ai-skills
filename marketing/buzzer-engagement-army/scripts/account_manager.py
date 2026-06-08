"""
Account Manager — manages all PostBridge connected accounts.
Fetches account details, tracks warmup state, and provides account metadata.
"""

import os
import json
import time
import requests
from datetime import datetime, date
from pathlib import Path

# PostBridge API config
POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = os.environ.get("POSTBRIDGE_KEY", "REDACTED_ROTATED_CREDENTIAL")

HEADERS = {
    "Authorization": f"Bearer {POSTBRIDGE_KEY}",
    "Content-Type": "application/json",
}

# Known account IDs
KNOWN_ACCOUNTS = {
    "tiktok": [48374, 48373, 48372, 48338, 48337, 48336, 48335],
    "instagram": [48186],
    "facebook": [48178, 48177, 48176, 48175],
}

# State file for warmup tracking
STATE_DIR = Path(__file__).parent.parent / "state"
STATE_FILE = STATE_DIR / "account_state.json"


def _load_state() -> dict:
    STATE_DIR.mkdir(exist_ok=True)
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {}


def _save_state(state: dict):
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def fetch_social_accounts() -> list:
    """Fetch all connected social accounts from PostBridge."""
    try:
        resp = requests.get(
            f"{POSTBRIDGE_BASE}/social-accounts", headers=HEADERS, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        # Handle both list and dict with 'data' key
        if isinstance(data, list):
            return data
        return data.get("data", data.get("accounts", []))
    except Exception as e:
        print(f"[account_manager] Failed to fetch accounts: {e}")
        return []


def get_accounts_by_platform(platform: str = None) -> list:
    """
    Get accounts, optionally filtered by platform.
    Falls back to known IDs if API fails.
    """
    accounts = fetch_social_accounts()
    if not accounts:
        # Build fallback list from known IDs
        accounts = []
        for plat, ids in KNOWN_ACCOUNTS.items():
            for acc_id in ids:
                accounts.append(
                    {
                        "id": acc_id,
                        "platform": plat,
                        "name": f"{plat}_{acc_id}",
                        "status": "unknown",
                    }
                )

    if platform:
        platform = platform.lower()
        accounts = [
            a for a in accounts if str(a.get("platform", "")).lower() == platform
        ]

    return accounts


def get_account_warmup_level(account_id: int) -> int:
    """
    Returns daily action limit based on warmup level.
    Day 1-3: 5 actions/day
    Day 4-7: 15 actions/day
    Day 8+:  30 actions/day
    """
    state = _load_state()
    key = str(account_id)
    if key not in state:
        # First time seeing this account → register as day 1
        state[key] = {"first_seen": date.today().isoformat(), "total_actions": 0}
        _save_state(state)

    first_seen = date.fromisoformat(
        state[key].get("first_seen", date.today().isoformat())
    )
    days_active = (date.today() - first_seen).days + 1

    if days_active <= 3:
        return 5
    elif days_active <= 7:
        return 15
    else:
        return 30


def get_actions_today(account_id: int) -> int:
    """How many actions has this account taken today?"""
    state = _load_state()
    key = str(account_id)
    today = date.today().isoformat()
    daily = state.get(key, {}).get("daily", {})
    return daily.get(today, 0)


def record_action(account_id: int):
    """Record that an account performed one action."""
    state = _load_state()
    key = str(account_id)
    today = date.today().isoformat()
    if key not in state:
        state[key] = {"first_seen": today, "total_actions": 0}
    state[key].setdefault("daily", {})
    state[key]["daily"][today] = state[key]["daily"].get(today, 0) + 1
    state[key]["total_actions"] = state[key].get("total_actions", 0) + 1
    _save_state(state)


def can_act(account_id: int) -> bool:
    """Returns True if account is under daily limit."""
    limit = get_account_warmup_level(account_id)
    used = get_actions_today(account_id)
    return used < limit


def get_account_status_report() -> dict:
    """Full status report for all accounts."""
    report = {}
    for platform, ids in KNOWN_ACCOUNTS.items():
        report[platform] = []
        for acc_id in ids:
            limit = get_account_warmup_level(acc_id)
            used = get_actions_today(acc_id)
            state = _load_state()
            key = str(acc_id)
            first_seen = state.get(key, {}).get("first_seen", "new")
            report[platform].append(
                {
                    "id": acc_id,
                    "daily_limit": limit,
                    "used_today": used,
                    "remaining": max(0, limit - used),
                    "can_act": can_act(acc_id),
                    "first_seen": first_seen,
                }
            )
    return report


def print_status():
    report = get_account_status_report()
    print("\n=== Account Status Report ===")
    for platform, accounts in report.items():
        print(f"\n[{platform.upper()}]")
        for acc in accounts:
            status = "✅" if acc["can_act"] else "🔴"
            print(
                f"  {status} ID {acc['id']} | limit:{acc['daily_limit']} used:{acc['used_today']} remaining:{acc['remaining']} | first_seen:{acc['first_seen']}"
            )


if __name__ == "__main__":
    print("Fetching PostBridge accounts...")
    accounts = fetch_social_accounts()
    if accounts:
        print(f"Found {len(accounts)} accounts:")
        for a in accounts:
            print(f"  - {a}")
    else:
        print("Using known account IDs (API unavailable)")
    print_status()
