"""
run_manager.py — Main entry point for comment-reply-manager
Usage: python3 run_manager.py [--dry-run] [--mode monitor|process|dms|report]
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from comment_monitor import get_posts_with_engagement, get_platform_post_ids
from auto_replier import process_comments
from dm_funnel import process_dm_funnel, print_pending_dms


def run_full_cycle(dry_run: bool = True):
    """Full cycle: monitor → analyze → reply → DM → report."""
    print(f"\n{'🔥'*20}")
    print(f"COMMENT-REPLY-MANAGER — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"{'🔥'*20}\n")

    # 1. Get posts with engagement from PostBridge
    print("[1/4] Fetching posts with comments from PostBridge...")
    engaged_posts = get_posts_with_engagement(min_comments=1)

    if not engaged_posts:
        print("  ℹ️  No posts with comments found via PostBridge.")
        print("  → Check if posts are published and analytics are synced")
        print(
            "  → Try running: curl -H 'Authorization: Bearer REDACTED_ROTATED_CREDENTIAL'"
        )
        print("       'https://api.post-bridge.com/v1/analytics/sync' -X POST")
    else:
        print(f"  Found {len(engaged_posts)} posts with comments")
        for p in engaged_posts[:5]:
            print(
                f"    {p['platform']} @{p['username']}: {p['comments_count']} comments — {p['url']}"
            )

    # 2. Process comments (requires platform-specific comment fetching)
    # PostBridge doesn't return individual comments, only counts.
    # We need platform APIs or browser scraping for actual comment text.
    print("\n[2/4] Comment text retrieval...")
    print("  ℹ️  PostBridge provides comment COUNTS only, not comment text.")
    print("  → For TikTok: Use TikTok Research API or browser automation")
    print("  → For Instagram: Use Instagram Graph API with comments permission")
    print("  → Posts with comments detected above — manual review needed")

    # Show platform map for manual action
    pmap = get_platform_post_ids()
    print(f"\n  Platform distribution:")
    for platform, items in pmap.items():
        print(f"    {platform}: {len(items)} posts")
        for item in items[:2]:
            if item.get("url"):
                print(f"      → {item['url']}")

    # 3. Run sample simulated comments for demo
    print("\n[3/4] Processing queued/simulated comments...")

    # Load from any existing comment queue file
    comment_queue_file = os.path.expanduser(
        "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/cache/comment_queue.jsonl"
    )

    comments = []
    if os.path.exists(comment_queue_file):
        with open(comment_queue_file) as f:
            for line in f:
                line = line.strip()
                if line:
                    comments.append(json.loads(line))
        print(f"  Loaded {len(comments)} comments from queue")
    else:
        print(f"  No comment queue found at {comment_queue_file}")
        print(f"  → Add comments manually to that file or via platform scraping")

    if comments:
        stats = process_comments(comments, dry_run=dry_run)
        print(f"\n  Reply stats: {json.dumps(stats, indent=4)}")

    # 4. DM Funnel
    print("\n[4/4] Pending DMs:")
    print_pending_dms()

    print(f"\n{'='*60}")
    print("NEXT ACTIONS:")
    print("  1. Visit TikTok/IG posts listed above")
    print("  2. Copy comments to comment_queue.jsonl")
    print("  3. Run with --mode process to generate replies")
    print("  4. Execute pending DMs from dm_queue.jsonl")
    print(f"{'='*60}\n")


def mode_report():
    """Show current status report."""
    print("\n📊 COMMENT-REPLY-MANAGER STATUS REPORT\n")

    log_file = os.path.expanduser(
        "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/logs/replies.jsonl"
    )
    dm_file = os.path.expanduser(
        "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/logs/dm_sent.jsonl"
    )

    # Reply stats
    if os.path.exists(log_file):
        with open(log_file) as f:
            lines = [json.loads(l) for l in f if l.strip()]
        categories = {}
        for entry in lines:
            cat = entry.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        print(f"Replies logged: {len(lines)}")
        print(f"By category: {json.dumps(categories, indent=2)}")
    else:
        print("No reply log found yet")

    # DM stats
    if os.path.exists(dm_file):
        with open(dm_file) as f:
            dms = [json.loads(l) for l in f if l.strip()]
        statuses = {}
        for dm in dms:
            s = dm.get("status", "unknown")
            statuses[s] = statuses.get(s, 0) + 1
        print(f"\nDMs logged: {len(dms)}")
        print(f"By status: {json.dumps(statuses, indent=2)}")
    else:
        print("\nNo DM log found yet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comment Reply Manager")
    parser.add_argument(
        "--dry-run", action="store_true", default=True, help="Dry run (default)"
    )
    parser.add_argument(
        "--live", action="store_true", help="Live mode (actually send replies)"
    )
    parser.add_argument(
        "--mode",
        choices=["monitor", "process", "dms", "report", "full"],
        default="full",
        help="Operation mode",
    )
    args = parser.parse_args()

    dry_run = not args.live

    if args.mode == "report":
        mode_report()
    elif args.mode == "dms":
        print_pending_dms()
    else:
        run_full_cycle(dry_run=dry_run)
