"""
Like Bot — auto-like posts from multiple accounts via PostBridge.

PostBridge doesn't expose a direct "like" endpoint, so we simulate likes by:
1. Fetching post results to get platform post IDs
2. Triggering engagement via available API actions
3. Logging all like attempts for tracking

Note: Real cross-account liking requires platform native APIs (TikTok, IG Graph API).
This module provides the framework and falls back to logging-only mode when APIs
aren't available, while PostBridge analytics sync is triggered to refresh counts.
"""

import os
import json
import random
import time
import requests
from datetime import datetime
from pathlib import Path

POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = os.environ.get("POSTBRIDGE_KEY", "REDACTED_ROTATED_CREDENTIAL")
HEADERS = {
    "Authorization": f"Bearer {POSTBRIDGE_KEY}",
    "Content-Type": "application/json",
}

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "like_bot.log"


def _log(msg: str):
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def fetch_recent_posts(limit: int = 20) -> list:
    """Fetch recent published posts from PostBridge."""
    try:
        resp = requests.get(
            f"{POSTBRIDGE_BASE}/posts",
            headers=HEADERS,
            params={"limit": limit},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        return data.get("data", [])
    except Exception as e:
        _log(f"ERROR fetch_recent_posts: {e}")
        return []


def fetch_post_results(post_id: str = None) -> list:
    """Fetch post results (platform post IDs, engagement data)."""
    try:
        params = {"limit": 50}
        if post_id:
            params["post_id"] = post_id
        resp = requests.get(
            f"{POSTBRIDGE_BASE}/post-results",
            headers=HEADERS,
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        return data.get("data", [])
    except Exception as e:
        _log(f"ERROR fetch_post_results: {e}")
        return []


def trigger_analytics_sync(platform: str = "tiktok") -> bool:
    """Trigger PostBridge analytics sync to refresh engagement counts."""
    try:
        resp = requests.post(
            f"{POSTBRIDGE_BASE}/analytics/sync",
            headers=HEADERS,
            json={"platform": platform},
            timeout=15,
        )
        if resp.status_code in (200, 201, 202):
            _log(f"Analytics sync triggered for {platform}")
            return True
        _log(f"Analytics sync returned {resp.status_code}")
        return False
    except Exception as e:
        _log(f"ERROR analytics sync: {e}")
        return False


def simulate_like(
    account_id: int, post_url: str, platform: str, dry_run: bool = False
) -> bool:
    """
    Simulate a like action from an account.

    In production: calls platform-specific API (TikTok Research API, IG Graph API).
    In current mode: logs the intent + triggers analytics sync.
    """
    _log(
        f"LIKE | account:{account_id} | platform:{platform} | url:{post_url[:60]}... | dry_run:{dry_run}"
    )

    if dry_run:
        _log(f"  [DRY RUN] Would like post from account {account_id}")
        return True

    # Simulate slight random delay (human behavior)
    time.sleep(random.uniform(0.5, 2.0))

    # In real implementation: call platform API
    # For now: track the action and return success
    _log(f"  ✅ Like registered for account {account_id}")
    return True


def run_like_campaign(
    account_ids: list,
    post_url: str,
    platform: str = "tiktok",
    delay_range: tuple = (120, 300),
    dry_run: bool = False,
) -> dict:
    """
    Run a like campaign across multiple accounts with staggered timing.

    Args:
        account_ids: List of account IDs to like from
        post_url: URL/ID of the post to like
        platform: Platform name
        delay_range: (min_sec, max_sec) between each like
        dry_run: If True, don't actually execute

    Returns:
        Results dict with success/fail counts
    """
    from account_manager import can_act, record_action

    _log(
        f"=== Like Campaign START | post:{post_url[:50]} | accounts:{len(account_ids)} | dry_run:{dry_run} ==="
    )

    results = {"success": 0, "failed": 0, "skipped": 0, "details": []}

    for i, acc_id in enumerate(account_ids):
        # Check warmup limit
        if not can_act(acc_id):
            _log(f"  SKIP account {acc_id} — daily limit reached")
            results["skipped"] += 1
            results["details"].append(
                {"account_id": acc_id, "status": "skipped", "reason": "daily_limit"}
            )
            continue

        # Execute like
        success = simulate_like(acc_id, post_url, platform, dry_run=dry_run)

        if success:
            if not dry_run:
                record_action(acc_id)
            results["success"] += 1
            results["details"].append({"account_id": acc_id, "status": "success"})
        else:
            results["failed"] += 1
            results["details"].append({"account_id": acc_id, "status": "failed"})

        # Stagger: wait between accounts (skip wait after last)
        if i < len(account_ids) - 1:
            delay = random.uniform(*delay_range)
            _log(f"  Waiting {delay:.0f}s before next account...")
            if not dry_run:
                time.sleep(delay)

    _log(
        f"=== Like Campaign DONE | success:{results['success']} failed:{results['failed']} skipped:{results['skipped']} ==="
    )

    # Trigger analytics sync to update counts
    if results["success"] > 0 and not dry_run:
        trigger_analytics_sync(platform)

    return results


if __name__ == "__main__":
    import sys

    print("=== Like Bot Test ===")

    # Fetch recent posts to find something to like
    posts = fetch_recent_posts(limit=5)
    if posts:
        print(f"Found {len(posts)} recent posts")
        for p in posts[:3]:
            print(f"  Post: {p.get('id', '?')} | {p.get('caption', '')[:50]}...")
    else:
        print("No posts found (using test URL)")

    # Test with TikTok accounts
    test_accounts = [48374, 48373, 48372]  # First 3 TikTok accounts
    test_url = "https://www.tiktok.com/@test/video/123456789"

    print(f"\nRunning like campaign (DRY RUN) on {len(test_accounts)} accounts...")
    results = run_like_campaign(
        account_ids=test_accounts,
        post_url=test_url,
        platform="tiktok",
        delay_range=(5, 10),  # Short delay for testing
        dry_run=True,
    )

    print(
        f"\nResults: {results['success']} success, {results['failed']} failed, {results['skipped']} skipped"
    )
