"""
Warmup Manager — Gradually increase activity for accounts.
Prevents platform bans by mimicking organic growth patterns.

Warmup Schedule:
  Day 1-3:  5 actions/day  (brand new accounts)
  Day 4-7: 15 actions/day  (warming up)
  Day 8+:  30 actions/day  (fully active)
"""
import json
from datetime import date, timedelta
from pathlib import Path
from account_manager import (
    KNOWN_ACCOUNTS,
    get_account_warmup_level,
    get_actions_today,
    can_act,
    _load_state,
    _save_state
)


def get_warmup_phase(account_id: int) -> str:
    """Return the warmup phase label for an account."""
    level = get_account_warmup_level(account_id)
    if level == 5:
        return "COLD (Day 1-3)"
    elif level == 15:
        return "WARMING (Day 4-7)"
    else:
        return "ACTIVE (Day 8+)"


def days_active(account_id: int) -> int:
    """How many days since account was first seen."""
    state = _load_state()
    key = str(account_id)
    if key not in state:
        return 0
    first_seen = date.fromisoformat(state[key].get("first_seen", date.today().isoformat()))
    return (date.today() - first_seen).days + 1


def get_all_account_warmup_status() -> list:
    """Full warmup status for all known accounts."""
    results = []
    for platform, ids in KNOWN_ACCOUNTS.items():
        for acc_id in ids:
            d = days_active(acc_id)
            limit = get_account_warmup_level(acc_id)
            used = get_actions_today(acc_id)
            results.append({
                "platform": platform,
                "id": acc_id,
                "days_active": d,
                "phase": get_warmup_phase(acc_id),
                "daily_limit": limit,
                "used_today": used,
                "remaining": max(0, limit - used),
                "can_act": can_act(acc_id)
            })
    return results


def register_new_account(account_id: int, platform: str = "unknown"):
    """Manually register a brand new account (starts warmup clock)."""
    state = _load_state()
    key = str(account_id)
    if key not in state:
        state[key] = {
            "first_seen": date.today().isoformat(),
            "platform": platform,
            "total_actions": 0,
            "daily": {}
        }
        _save_state(state)
        print(f"[warmup] Registered new account {account_id} ({platform}) - Day 1, limit: 5/day")
    else:
        print(f"[warmup] Account {account_id} already registered (Day {days_active(account_id)})")


def get_safe_accounts(min_remaining: int = 1) -> list:
    """Return accounts that still have daily capacity."""
    return [a for a in get_all_account_warmup_status() if a["remaining"] >= min_remaining]


def simulate_warmup_schedule(account_id: int, days: int = 14):
    """Show projected action limits for the next N days."""
    state = _load_state()
    key = str(account_id)
    if key not in state:
        first_day = 1
    else:
        first_seen = date.fromisoformat(state[key].get("first_seen", date.today().isoformat()))
        first_day = (date.today() - first_seen).days + 1

    print(f"\n=== Warmup Schedule for Account {account_id} ===")
    print(f"Currently Day {first_day}")
    for delta in range(days):
        day = first_day + delta
        if day <= 3:
            limit = 5
            phase = "COLD"
        elif day <= 7:
            limit = 15
            phase = "WARMING"
        else:
            limit = 30
            phase = "ACTIVE"
        marker = " ← TODAY" if delta == 0 else ""
        print(f"  Day {day:2d}: {limit:2d} actions/day [{phase}]{marker}")


def print_warmup_report():
    statuses = get_all_account_warmup_status()
    print("\n=== Warmup Status Report ===")
    for s in statuses:
        icon = "✅" if s["can_act"] else "🔴"
        print(f"  {icon} [{s['platform']}] ID:{s['id']} | Day {s['days_active']} | {s['phase']} | "
              f"limit:{s['daily_limit']} used:{s['used_today']} remaining:{s['remaining']}")
    
    safe = get_safe_accounts()
    print(f"\n  Active accounts with remaining capacity: {len(safe)}/{len(statuses)}")


if __name__ == "__main__":
    # Register all known accounts if not already registered
    for platform, ids in KNOWN_ACCOUNTS.items():
        for acc_id in ids:
            register_new_account(acc_id, platform)

    print_warmup_report()

    # Show schedule for first TikTok account
    simulate_warmup_schedule(48374, days=10)
