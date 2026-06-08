"""
Engagement Scheduler — staggers engagement timing to look natural.

Rules:
- 2-5 min gap between each account's engagement on same post
- Mix action order: like → wait → comment → wait
- Never all accounts engage at exact same second
- Different accounts pick random delay slots
"""

import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Callable, Optional


def random_delay(min_sec: int = 120, max_sec: int = 300) -> float:
    """Return a random delay in seconds (default 2-5 minutes)."""
    return random.uniform(min_sec, max_sec)


def jitter(base_sec: float, spread_pct: float = 0.3) -> float:
    """Add ±spread% jitter to a base delay."""
    spread = base_sec * spread_pct
    return base_sec + random.uniform(-spread, spread)


def generate_engagement_schedule(
    account_ids: List[int],
    actions: List[str] = None,
    start_time: datetime = None,
    min_gap_sec: int = 120,
    max_gap_sec: int = 300,
) -> List[Dict]:
    """
    Generate a staggered engagement schedule for multiple accounts.

    Returns list of scheduled actions:
    [
      {"account_id": 48374, "action": "like", "scheduled_at": datetime, "delay_sec": 143},
      ...
    ]
    """
    if actions is None:
        actions = ["like", "comment"]
    if start_time is None:
        start_time = datetime.now()

    schedule = []
    current_time = start_time

    # Shuffle accounts to randomize order
    shuffled_accounts = account_ids.copy()
    random.shuffle(shuffled_accounts)

    for i, acc_id in enumerate(shuffled_accounts):
        # Each account gets its own set of actions with internal gaps
        account_start = current_time

        for j, action in enumerate(actions):
            if j > 0:
                # Small intra-account gap between like → comment
                intra_gap = random.uniform(30, 90)  # 30-90 seconds between actions
                account_start += timedelta(seconds=intra_gap)

            schedule.append(
                {
                    "account_id": acc_id,
                    "action": action,
                    "scheduled_at": account_start,
                    "delay_from_start_sec": (
                        account_start - start_time
                    ).total_seconds(),
                }
            )

        # Inter-account gap: 2-5 minutes
        inter_gap = jitter(random.uniform(min_gap_sec, max_gap_sec))
        current_time += timedelta(seconds=inter_gap)

    return schedule


def execute_schedule(
    schedule: List[Dict],
    action_fn: Callable[[int, str], bool],
    dry_run: bool = False,
    verbose: bool = True,
) -> List[Dict]:
    """
    Execute a schedule by sleeping between actions and calling action_fn.

    action_fn(account_id, action) → True if success, False if failed.
    Returns list of results.
    """
    results = []
    now = datetime.now()

    for i, item in enumerate(schedule):
        wait_sec = max(0, (item["scheduled_at"] - datetime.now()).total_seconds())

        if verbose:
            print(
                f"[{i+1}/{len(schedule)}] Account {item['account_id']} → {item['action']} "
                f"at {item['scheduled_at'].strftime('%H:%M:%S')} (wait {wait_sec:.0f}s)"
            )

        if not dry_run:
            if wait_sec > 0:
                time.sleep(wait_sec)

            try:
                success = action_fn(item["account_id"], item["action"])
            except Exception as e:
                success = False
                print(f"  ❌ Error: {e}")

            result = {
                **item,
                "success": success,
                "executed_at": datetime.now().isoformat(),
            }
            results.append(result)

            if verbose:
                icon = "✅" if success else "❌"
                print(f"  {icon} Done")
        else:
            results.append({**item, "dry_run": True})

    return results


def print_schedule(schedule: List[Dict]):
    print("\n=== Engagement Schedule ===")
    for item in schedule:
        t = item["scheduled_at"].strftime("%H:%M:%S")
        d = item["delay_from_start_sec"]
        print(f"  T+{d:6.0f}s [{t}] Account {item['account_id']:5d} → {item['action']}")

    if schedule:
        total_duration = (
            schedule[-1]["scheduled_at"] - schedule[0]["scheduled_at"]
        ).total_seconds()
        print(
            f"\n  Total duration: {total_duration/60:.1f} minutes for {len(schedule)} actions"
        )


if __name__ == "__main__":
    # Demo with TikTok accounts
    tiktok_ids = [48374, 48373, 48372, 48338, 48337, 48336, 48335]

    print("=== Engagement Scheduler Demo ===")
    schedule = generate_engagement_schedule(
        account_ids=tiktok_ids, actions=["like", "comment"], start_time=datetime.now()
    )

    print_schedule(schedule)

    # Show first 5 actions
    print("\n=== First 5 scheduled actions ===")
    for item in schedule[:5]:
        print(
            f"  Account {item['account_id']} → {item['action']} at T+{item['delay_from_start_sec']:.0f}s"
        )
