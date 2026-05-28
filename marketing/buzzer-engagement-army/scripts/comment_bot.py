"""
Comment Bot — post natural-sounding comments from multiple accounts.

Uses comment_library.py for contextual Indonesian comments.
Staggers comments to avoid platform detection.
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
HEADERS = {"Authorization": f"Bearer {POSTBRIDGE_KEY}", "Content-Type": "application/json"}

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "comment_bot.log"
USED_COMMENTS_FILE = LOG_DIR / "used_comments.json"


def _log(msg: str):
    LOG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def _load_used_comments() -> dict:
    """Load previously used comments per post to avoid duplicates."""
    if USED_COMMENTS_FILE.exists():
        try:
            return json.loads(USED_COMMENTS_FILE.read_text())
        except Exception:
            pass
    return {}


def _save_used_comments(data: dict):
    LOG_DIR.mkdir(exist_ok=True)
    USED_COMMENTS_FILE.write_text(json.dumps(data, indent=2))


def post_comment_via_api(
    account_id: int,
    post_id: str,
    platform: str,
    comment_text: str,
    dry_run: bool = False
) -> bool:
    """
    Post a comment via platform API.
    
    Note: PostBridge is a scheduling tool, not a commenting API.
    Real commenting requires platform-specific APIs:
      - TikTok: Research API / unofficial methods
      - Instagram: Graph API (comment on media)
      - Facebook: Graph API (comment on post)
    
    This function logs the intent and simulates the action.
    For production: integrate platform-specific commenting API here.
    """
    _log(f"COMMENT | account:{account_id} | platform:{platform} | post:{post_id} | text:'{comment_text[:50]}...'")
    
    if dry_run:
        _log(f"  [DRY RUN] Would comment: '{comment_text}'")
        return True

    # === Instagram Graph API (if credentials available) ===
    # ig_token = os.environ.get(f"IG_TOKEN_{account_id}")
    # if platform == "instagram" and ig_token:
    #     resp = requests.post(
    #         f"https://graph.facebook.com/v18.0/{post_id}/comments",
    #         params={"message": comment_text, "access_token": ig_token}
    #     )
    #     return resp.status_code == 200

    # === Simulation mode ===
    time.sleep(random.uniform(1, 3))  # Simulate API call
    _log(f"  ✅ Comment logged for account {account_id}")
    return True


def run_comment_campaign(
    account_ids: list,
    post_id: str,
    post_caption: str = "",
    platform: str = "tiktok",
    delay_range: tuple = (120, 300),
    comments_per_account: int = 1,
    dry_run: bool = False
) -> dict:
    """
    Run a comment campaign across multiple accounts.
    
    Each account posts a different, niche-appropriate comment.
    Comments are staggered with 2-5 minute gaps.
    """
    from account_manager import can_act, record_action
    from comment_library import get_comments_for_post

    _log(f"=== Comment Campaign START | post:{post_id} | accounts:{len(account_ids)} | dry_run:{dry_run} ===")

    # Load used comments to avoid duplication on same post
    used_data = _load_used_comments()
    post_key = f"{platform}_{post_id}"
    already_used = used_data.get(post_key, [])

    results = {"success": 0, "failed": 0, "skipped": 0, "comments": []}

    # Shuffle accounts for natural ordering
    shuffled = account_ids.copy()
    random.shuffle(shuffled)

    for i, acc_id in enumerate(shuffled):
        # Check warmup limit
        if not can_act(acc_id):
            _log(f"  SKIP account {acc_id} — daily limit reached")
            results["skipped"] += 1
            continue

        # Get unique comment(s) for this account
        comments = get_comments_for_post(post_caption, count=comments_per_account, exclude=already_used)

        for comment_text in comments:
            success = post_comment_via_api(
                account_id=acc_id,
                post_id=post_id,
                platform=platform,
                comment_text=comment_text,
                dry_run=dry_run
            )

            if success:
                if not dry_run:
                    record_action(acc_id)
                    already_used.append(comment_text)
                results["success"] += 1
                results["comments"].append({
                    "account_id": acc_id,
                    "comment": comment_text,
                    "status": "success"
                })
            else:
                results["failed"] += 1

        # Stagger between accounts
        if i < len(shuffled) - 1:
            delay = random.uniform(*delay_range)
            _log(f"  Waiting {delay:.0f}s before next account...")
            if not dry_run:
                time.sleep(delay)

    # Save updated used comments
    used_data[post_key] = already_used
    _save_used_comments(used_data)

    _log(f"=== Comment Campaign DONE | success:{results['success']} failed:{results['failed']} skipped:{results['skipped']} ===")
    return results


def get_recent_post_ids(limit: int = 5, platform: str = None) -> list:
    """Fetch recent post IDs from PostBridge for commenting."""
    try:
        params = {"limit": limit}
        resp = requests.get(f"{POSTBRIDGE_BASE}/post-results", headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        results = data if isinstance(data, list) else data.get("data", [])
        
        posts = []
        for r in results:
            if platform and r.get("platform", "").lower() != platform.lower():
                continue
            posts.append({
                "post_id": r.get("platform_post_id", r.get("id", "")),
                "platform": r.get("platform", ""),
                "url": r.get("url", ""),
                "caption": r.get("caption", "")
            })
        return posts
    except Exception as e:
        _log(f"ERROR get_recent_post_ids: {e}")
        return []


if __name__ == "__main__":
    print("=== Comment Bot Test ===")
    
    # Test comment library
    from comment_library import get_comments_for_post, detect_niche
    
    test_caption = "Tips kesehatan harian supaya badan tetap fit dan bugar"
    niche = detect_niche(test_caption)
    print(f"\nTest caption: '{test_caption}'")
    print(f"Detected niche: {niche}")
    
    # Get 7 unique comments (one per TikTok account)
    comments = get_comments_for_post(test_caption, count=7)
    print(f"\nGenerated {len(comments)} unique comments:")
    for i, c in enumerate(comments, 1):
        print(f"  {i}. {c}")

    # Test comment campaign (dry run)
    test_accounts = [48374, 48373, 48372]
    print(f"\nRunning comment campaign (DRY RUN) on {len(test_accounts)} accounts...")
    
    results = run_comment_campaign(
        account_ids=test_accounts,
        post_id="test_post_001",
        post_caption=test_caption,
        platform="tiktok",
        delay_range=(3, 8),  # Short delays for testing
        dry_run=True
    )
    
    print(f"\nResults: {results['success']} success, {results['failed']} failed, {results['skipped']} skipped")
    print("\nComments posted:")
    for c in results["comments"]:
        print(f"  Account {c['account_id']}: {c['comment']}")
