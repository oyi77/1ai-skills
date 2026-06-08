"""
Engagement Coordinator — orchestrates all engagement actions across accounts.

This is the MAIN entry point. It:
1. Fetches recent posts from PostBridge
2. Determines which posts need engagement boost
3. Coordinates likes + comments with proper staggering
4. Respects account warmup limits
5. Logs everything for audit trail

Usage:
  python engagement_coordinator.py --boost-latest
  python engagement_coordinator.py --post-id 12345 --platform tiktok
  python engagement_coordinator.py --dry-run
  python engagement_coordinator.py --status
"""

import os
import sys
import json
import time
import random
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path

POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = os.environ.get("POSTBRIDGE_KEY", "REDACTED_ROTATED_CREDENTIAL")
HEADERS = {
    "Authorization": f"Bearer {POSTBRIDGE_KEY}",
    "Content-Type": "application/json",
}

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "coordinator.log"

# Account IDs by platform
ACCOUNTS = {
    "tiktok": [48374, 48373, 48372, 48338, 48337, 48336, 48335],
    "instagram": [48186],
    "facebook": [48178, 48177, 48176, 48175],
}


def _log(msg: str, level: str = "INFO"):
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def fetch_posts(limit: int = 20, status: str = None) -> list:
    """Fetch posts from PostBridge."""
    try:
        params = {"limit": limit}
        if status:
            params["status"] = status
        resp = requests.get(
            f"{POSTBRIDGE_BASE}/posts", headers=HEADERS, params=params, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("data", [])
    except Exception as e:
        _log(f"Failed to fetch posts: {e}", "ERROR")
        return []


def fetch_post_results(limit: int = 50) -> list:
    """Fetch post results with platform post IDs."""
    try:
        resp = requests.get(
            f"{POSTBRIDGE_BASE}/post-results",
            headers=HEADERS,
            params={"limit": limit},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("data", [])
    except Exception as e:
        _log(f"Failed to fetch post results: {e}", "ERROR")
        return []


def select_posts_for_boost(max_posts: int = 5, hours_old_max: int = 24) -> list:
    """
    Select recent posts that need an engagement boost.

    Priority:
    1. Posts published < 2 hours ago (critical window)
    2. Posts published < 24 hours ago (still relevant)
    3. Posts with lowest engagement
    """
    posts = fetch_posts(limit=50)
    results = fetch_post_results(limit=100)

    # Index results by post_id
    result_by_post = {}
    for r in results:
        pid = str(r.get("post_id", ""))
        if pid not in result_by_post:
            result_by_post[pid] = []
        result_by_post[pid].append(r)

    # Filter and score posts
    scored = []
    now = datetime.now()

    for post in posts:
        post_id = str(post.get("id", ""))
        published_at_str = (
            post.get("published_at")
            or post.get("scheduled_at")
            or post.get("created_at")
        )

        # Parse published time
        published_at = None
        if published_at_str:
            try:
                published_at = datetime.fromisoformat(
                    published_at_str.replace("Z", "+00:00")
                )
                # Convert to naive if needed
                if published_at.tzinfo:
                    from datetime import timezone

                    published_at = published_at.replace(tzinfo=None)
            except Exception:
                pass

        if published_at:
            age_hours = (now - published_at).total_seconds() / 3600
        else:
            age_hours = hours_old_max  # assume older

        # Skip if too old
        if age_hours > hours_old_max:
            continue

        # Score: newer = higher priority
        priority_score = max(0, hours_old_max - age_hours)

        scored.append(
            {
                "post_id": post_id,
                "caption": post.get("caption", "")[:100],
                "platform_results": result_by_post.get(post_id, []),
                "age_hours": round(age_hours, 1),
                "priority_score": priority_score,
                "platforms": list(
                    set(r.get("platform", "") for r in result_by_post.get(post_id, []))
                ),
            }
        )

    # Sort by priority (newest first)
    scored.sort(key=lambda x: x["priority_score"], reverse=True)

    _log(f"Found {len(scored)} recent posts eligible for boost")
    return scored[:max_posts]


def run_engagement_wave(
    post: dict,
    platform: str,
    actions: list = None,
    dry_run: bool = False,
    delay_range: tuple = (120, 300),
) -> dict:
    """
    Run a full engagement wave on a post from all available accounts.

    Wave = like + comment from multiple accounts, staggered.
    """
    if actions is None:
        actions = ["like", "comment"]

    account_ids = ACCOUNTS.get(platform, [])
    if not account_ids:
        _log(f"No accounts for platform: {platform}", "WARN")
        return {"status": "no_accounts"}

    _log(
        f"=== Engagement Wave | platform:{platform} | post:{post['post_id']} | accounts:{len(account_ids)} | actions:{actions} ==="
    )

    wave_results = {"platform": platform, "post_id": post["post_id"], "actions": {}}

    # Get platform post IDs from results
    platform_post_ids = []
    for r in post.get("platform_results", []):
        if r.get("platform", "").lower() == platform.lower():
            pid = r.get("platform_post_id") or r.get("url") or post["post_id"]
            platform_post_ids.append(str(pid))

    target_id = platform_post_ids[0] if platform_post_ids else post["post_id"]
    caption = post.get("caption", "")

    # Execute each action type
    for action in actions:
        if action == "like":
            from like_bot import run_like_campaign

            result = run_like_campaign(
                account_ids=account_ids,
                post_url=target_id,
                platform=platform,
                delay_range=delay_range,
                dry_run=dry_run,
            )
            wave_results["actions"]["like"] = result

            # Wait between like and comment waves
            if "comment" in actions and not dry_run:
                inter_action_delay = random.uniform(60, 180)
                _log(
                    f"Waiting {inter_action_delay:.0f}s between like and comment waves..."
                )
                time.sleep(inter_action_delay)

        elif action == "comment":
            from comment_bot import run_comment_campaign

            result = run_comment_campaign(
                account_ids=account_ids,
                post_id=target_id,
                post_caption=caption,
                platform=platform,
                delay_range=delay_range,
                dry_run=dry_run,
            )
            wave_results["actions"]["comment"] = result

    return wave_results


def boost_latest_posts(
    max_posts: int = 3,
    platforms: list = None,
    dry_run: bool = False,
    quick_mode: bool = False,
) -> dict:
    """
    Main function: boost engagement on the latest posts.

    Args:
        max_posts: How many posts to boost
        platforms: Which platforms to engage on (default: all)
        dry_run: Simulate without executing
        quick_mode: Use shorter delays (for testing)
    """
    if platforms is None:
        platforms = list(ACCOUNTS.keys())

    delay_range = (5, 15) if quick_mode else (120, 300)

    _log(
        f"🚀 Boost Campaign START | posts:{max_posts} | platforms:{platforms} | dry_run:{dry_run}"
    )

    posts = select_posts_for_boost(max_posts=max_posts)

    if not posts:
        _log("No recent posts found for boosting", "WARN")
        return {"status": "no_posts"}

    all_results = []

    for i, post in enumerate(posts):
        _log(
            f"\n--- Post {i+1}/{len(posts)}: ID={post['post_id']} | age={post['age_hours']}h ---"
        )
        _log(f"  Caption: {post['caption'][:60]}...")
        _log(f"  Available platforms: {post['platforms']}")

        post_results = {"post": post, "platform_results": {}}

        for platform in platforms:
            # Only boost platforms where this post was published
            if post["platforms"] and platform not in post["platforms"]:
                _log(f"  Skipping {platform} (post not on this platform)")
                continue

            wave_result = run_engagement_wave(
                post=post,
                platform=platform,
                actions=["like", "comment"],
                dry_run=dry_run,
                delay_range=delay_range,
            )
            post_results["platform_results"][platform] = wave_result

        all_results.append(post_results)

        # Gap between posts
        if i < len(posts) - 1 and not dry_run:
            inter_post_delay = random.uniform(300, 600)  # 5-10 min between posts
            _log(f"\nWaiting {inter_post_delay/60:.1f} min before next post...")
            time.sleep(inter_post_delay)

    _log(f"\n✅ Boost Campaign COMPLETE | {len(posts)} posts boosted")
    return {"status": "complete", "posts_boosted": len(posts), "results": all_results}


def print_status():
    """Print current system status."""
    from account_manager import print_status as acc_status
    from warmup_manager import print_warmup_report

    print("\n" + "=" * 60)
    print("  BUZZER ENGAGEMENT ARMY — STATUS REPORT")
    print("=" * 60)
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # PostBridge connection test
    try:
        resp = requests.get(
            f"{POSTBRIDGE_BASE}/social-accounts", headers=HEADERS, timeout=10
        )
        if resp.status_code == 200:
            print(f"  PostBridge API: ✅ Connected")
        else:
            print(f"  PostBridge API: ❌ Error {resp.status_code}")
    except Exception as e:
        print(f"  PostBridge API: ❌ {e}")

    # Recent posts
    posts = fetch_posts(limit=5)
    print(f"  Recent posts: {len(posts)} found")

    acc_status()
    print_warmup_report()


def main():
    parser = argparse.ArgumentParser(description="Buzzer Engagement Army Coordinator")
    parser.add_argument(
        "--boost-latest", action="store_true", help="Boost latest posts"
    )
    parser.add_argument("--post-id", type=str, help="Boost specific post ID")
    parser.add_argument(
        "--platform",
        type=str,
        default=None,
        help="Specific platform (tiktok/instagram/facebook)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate without executing"
    )
    parser.add_argument(
        "--quick", action="store_true", help="Use short delays (testing)"
    )
    parser.add_argument("--status", action="store_true", help="Show status report")
    parser.add_argument("--max-posts", type=int, default=3, help="Max posts to boost")
    args = parser.parse_args()

    if args.status:
        print_status()
        return

    platforms = [args.platform] if args.platform else None

    if args.post_id:
        post = {
            "post_id": args.post_id,
            "caption": "",
            "platform_results": [],
            "platforms": [args.platform] if args.platform else list(ACCOUNTS.keys()),
        }
        result = run_engagement_wave(
            post=post,
            platform=args.platform or "tiktok",
            dry_run=args.dry_run,
            delay_range=(5, 10) if args.quick else (120, 300),
        )
        print(f"\nResult: {json.dumps(result, indent=2, default=str)}")

    elif args.boost_latest or True:  # Default action
        result = boost_latest_posts(
            max_posts=args.max_posts,
            platforms=platforms,
            dry_run=args.dry_run,
            quick_mode=args.quick,
        )
        _log(f"Final result: {result['status']}")


if __name__ == "__main__":
    main()
