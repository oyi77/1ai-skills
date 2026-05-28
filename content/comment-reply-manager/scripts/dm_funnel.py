"""
dm_funnel.py — Auto-DM interested commenters with LYNK affiliate offer
Funnel: Detect interested comment → Public reply "DM aku" → Auto-DM with link
"""

import json
import os
import time
from datetime import datetime
from typing import Optional

from comment_templates import get_dm_message, find_product_by_keywords, PRODUCTS

# ─── CONFIG ────────────────────────────────────────────────────────────────────
DM_LOG_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/logs/dm_sent.jsonl"
)
DM_QUEUE_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/logs/dm_queue.jsonl"
)
DM_COOLDOWN_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/cache/dm_cooldowns.json"
)

# Don't DM same user twice within this many hours
DM_COOLDOWN_HOURS = 24
# Max DMs per hour (avoid spam limits)
MAX_DM_PER_HOUR = 20


# ─── DM CONTENT BUILDER ────────────────────────────────────────────────────────

def build_dm_content(username: str, comment_text: str, post_caption: str = "") -> dict:
    """Build DM content for a specific user based on their comment."""
    combined = f"{comment_text} {post_caption}"
    product = find_product_by_keywords(combined)
    message = get_dm_message(product)

    return {
        "username": username,
        "product": product["name"],
        "product_url": product["url"],
        "message": message,
        "product_obj": product,
    }


# ─── COOLDOWN MANAGEMENT ───────────────────────────────────────────────────────

def load_dm_cooldowns() -> dict:
    """Load dict of {username: last_dm_timestamp}."""
    if not os.path.exists(DM_COOLDOWN_FILE):
        return {}
    with open(DM_COOLDOWN_FILE) as f:
        return json.load(f)


def save_dm_cooldowns(cooldowns: dict):
    os.makedirs(os.path.dirname(DM_COOLDOWN_FILE), exist_ok=True)
    with open(DM_COOLDOWN_FILE, "w") as f:
        json.dump(cooldowns, f)


def is_on_cooldown(username: str, cooldowns: dict) -> bool:
    """Return True if user was DM'd recently."""
    if username not in cooldowns:
        return False
    last_dm = datetime.fromisoformat(cooldowns[username])
    hours_since = (datetime.now() - last_dm).total_seconds() / 3600
    return hours_since < DM_COOLDOWN_HOURS


def mark_dm_sent(username: str, cooldowns: dict) -> dict:
    cooldowns[username] = datetime.now().isoformat()
    return cooldowns


# ─── DM LOGGING ────────────────────────────────────────────────────────────────

def log_dm_sent(username: str, platform: str, message: str, product: str, status: str):
    os.makedirs(os.path.dirname(DM_LOG_FILE), exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "username": username,
        "product": product,
        "message_preview": message[:100],
        "status": status,  # sent | queued | failed | cooldown
    }
    with open(DM_LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def queue_dm(username: str, platform: str, message: str, product_url: str, post_url: str = ""):
    """Queue a DM for manual/future sending."""
    os.makedirs(os.path.dirname(DM_QUEUE_FILE), exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "username": username,
        "message": message,
        "product_url": product_url,
        "post_url": post_url,
        "status": "pending",
    }
    with open(DM_QUEUE_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[DM Funnel] Queued DM for @{username} on {platform}")


# ─── PLATFORM DM DISPATCHERS ───────────────────────────────────────────────────

def send_tiktok_dm(username: str, message: str) -> bool:
    """
    Send DM via TikTok.
    TikTok official API doesn't support DMs via API directly.
    Falls back to manual queue.
    """
    print(f"[TikTok DM] @{username}: {message[:60]}...")
    # TikTok DM via API requires special Business API access
    # For now: queue for manual sending or browser automation
    return False


def send_instagram_dm(username: str, message: str) -> bool:
    """
    Send Instagram DM via Graph API.
    Requires: Instagram Business account + approved IG API token.
    """
    import os
    ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    ig_account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID")

    if not ig_token or not ig_account_id:
        print(f"[Instagram DM] No token configured — queuing for manual send")
        return False

    import requests
    try:
        # Find recipient's IG user ID first
        url = f"https://graph.instagram.com/v18.0/{ig_account_id}/messages"
        payload = {
            "recipient": {"username": username},
            "message": {"text": message},
            "access_token": ig_token,
        }
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code == 200:
            print(f"[Instagram DM] ✅ Sent to @{username}")
            return True
        else:
            print(f"[Instagram DM] ❌ Failed: {resp.status_code} {resp.text[:100]}")
            return False
    except Exception as e:
        print(f"[Instagram DM] Error: {e}")
        return False


def send_dm(username: str, platform: str, message: str) -> bool:
    """Dispatch DM to appropriate platform."""
    platform_lower = platform.lower()
    if platform_lower == "tiktok":
        return send_tiktok_dm(username, message)
    elif platform_lower in ("instagram", "ig"):
        return send_instagram_dm(username, message)
    else:
        print(f"[DM Funnel] Unknown platform: {platform}")
        return False


# ─── MAIN FUNNEL PROCESSOR ─────────────────────────────────────────────────────

def process_dm_funnel(dm_candidates: list, dry_run: bool = True) -> dict:
    """
    Process list of DM candidates.
    Each candidate: {username, platform, comment_text, post_caption, post_url}
    Returns stats dict.
    """
    cooldowns = load_dm_cooldowns()
    stats = {
        "total_candidates": len(dm_candidates),
        "skipped_cooldown": 0,
        "dm_sent": 0,
        "dm_queued": 0,
        "dm_failed": 0,
    }

    for candidate in dm_candidates:
        username = candidate.get("username", "")
        platform = candidate.get("platform", "")
        comment_text = candidate.get("comment_text", "")
        post_caption = candidate.get("post_caption", "")
        post_url = candidate.get("post_url", "")

        # Cooldown check
        if is_on_cooldown(username, cooldowns):
            print(f"[DM Funnel] Skipping @{username} — on cooldown")
            stats["skipped_cooldown"] += 1
            log_dm_sent(username, platform, "", "", "cooldown")
            continue

        # Build DM content
        dm_data = build_dm_content(username, comment_text, post_caption)
        message = dm_data["message"]
        product = dm_data["product"]

        print(f"\n[DM Funnel] @{username} ({platform})")
        print(f"           Product: {product}")
        print(f"           Message: {message[:80]}...")

        if not dry_run:
            success = send_dm(username, platform, message)
            if success:
                cooldowns = mark_dm_sent(username, cooldowns)
                stats["dm_sent"] += 1
                log_dm_sent(username, platform, message, product, "sent")
            else:
                # Queue for manual/browser sending
                queue_dm(username, platform, message, dm_data["product_url"], post_url)
                stats["dm_queued"] += 1
                log_dm_sent(username, platform, message, product, "queued")
                # Still mark cooldown to avoid repeat queuing
                cooldowns = mark_dm_sent(username, cooldowns)
        else:
            # Dry run
            queue_dm(username, platform, message, dm_data["product_url"], post_url)
            stats["dm_queued"] += 1
            cooldowns = mark_dm_sent(username, cooldowns)

        time.sleep(1.0)  # Rate limit protection

    save_dm_cooldowns(cooldowns)
    return stats


def get_pending_dms() -> list:
    """Read pending DMs from queue for manual execution."""
    if not os.path.exists(DM_QUEUE_FILE):
        return []
    pending = []
    with open(DM_QUEUE_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("status") == "pending":
                pending.append(entry)
    return pending


def print_pending_dms():
    """Print pending DMs in human-readable format for manual execution."""
    pending = get_pending_dms()
    if not pending:
        print("✅ No pending DMs!")
        return

    print(f"\n📬 PENDING DMs ({len(pending)} total)\n{'='*60}")
    for i, dm in enumerate(pending, 1):
        print(f"\n[{i}] {dm['platform'].upper()} @{dm['username']}")
        print(f"     {dm['message'][:120]}...")
        if dm.get("post_url"):
            print(f"     Post: {dm['post_url']}")
        print(f"     Queued: {dm['timestamp']}")
    print(f"\n{'='*60}")
    print("Execute these manually or via browser automation.")


if __name__ == "__main__":
    # Test DM funnel
    test_candidates = [
        {
            "username": "potential_buyer_1",
            "platform": "tiktok",
            "comment_text": "Kak harganya berapa? Mau beli nih",
            "post_caption": "JobMagnet AI untuk cari kerja",
            "post_url": "https://tiktok.com/@jendralbot/video/123",
        },
        {
            "username": "interested_user",
            "platform": "instagram",
            "comment_text": "Mau dong! Gimana cara belinya?",
            "post_caption": "AI Creative Tools",
            "post_url": "",
        },
        {
            "username": "potential_buyer_1",  # Duplicate — should be cooldown
            "platform": "tiktok",
            "comment_text": "Lagi nanya nih",
            "post_caption": "",
            "post_url": "",
        },
    ]

    print("=== DM Funnel Test (DRY RUN) ===\n")
    stats = process_dm_funnel(test_candidates, dry_run=True)
    print(f"\n=== STATS ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\n=== PENDING DM QUEUE ===")
    print_pending_dms()
