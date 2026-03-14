#!/usr/bin/env python3
"""
PostBridge Queue & Retry System

When POST /posts returns 500 or network errors, queue the posts locally.
This script runs via cron every 5 minutes to retry queued posts.

Usage:
  python3 postbridge_queue_retry.py --retry
  python3 postbridge_queue_retry.py --status
  
Cron: */5 * * * * cd /home/openclaw/.openclaw/workspace && python3 content_suite/postbridge_queue_retry.py --retry >> content_suite/logs/queue_retry.log 2>&1
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path

import requests

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
QUEUE_FILE = WORKSPACE / "content_suite/queue/pending_posts.json"
RETRY_LOG = WORKSPACE / "content_suite/logs/queue_retry.log"

POSTBRIDGE_API = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = os.getenv("POSTBRIDGE_API_KEY", "pb_live_AT9Xm4PKaYBzAvFZYGgexi")
PB_HDR = {"Authorization": f"Bearer {POSTBRIDGE_KEY}", "Content-Type": "application/json"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(RETRY_LOG),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def load_queue() -> list:
    """Load pending posts from queue file."""
    if not QUEUE_FILE.exists():
        return []
    return json.loads(QUEUE_FILE.read_text())


def save_queue(items: list):
    """Save pending posts to queue file."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False))


def enqueue_post(caption: str, accounts: list, media_ids: list,
                 scheduled_at: str, persona_id: str = None):
    """Add a post to the retry queue."""
    queue = load_queue()
    queue.append({
        "caption": caption,
        "social_accounts": accounts,
        "media": media_ids if media_ids else None,
        "scheduled_at": scheduled_at,
        "persona_id": persona_id,
        "queued_at": datetime.now().isoformat(),
        "retry_count": 0,
    })
    save_queue(queue)
    log.info(f"  📦 Queued: {persona_id or 'unknown'} → {len(queue)} total pending")


def retry_queue():
    """Attempt to publish all queued posts."""
    queue = load_queue()
    if not queue:
        log.info("No queued posts")
        return

    log.info(f"Retrying {len(queue)} queued posts...")
    succeeded, failed, dropped = 0, 0, 0
    new_queue = []

    for item in queue:
        item["retry_count"] = item.get("retry_count", 0) + 1
        max_retries = 100  # retry for up to 500 minutes (5 days)

        if item["retry_count"] > max_retries:
            log.warning(f"  ⏭️  Dropping after {max_retries} retries: {item.get('persona_id')}")
            dropped += 1
            continue

        try:
            r = requests.post(f"{POSTBRIDGE_API}/posts", headers=PB_HDR,
                              json={
                                  "caption": item["caption"],
                                  "social_accounts": item["social_accounts"],
                                  "media": item["media"],
                                  "scheduled_at": item["scheduled_at"],
                              }, timeout=15)
            if r.status_code in (200, 201):
                post_id = r.json().get("id")
                log.info(f"  ✅ {item['persona_id']} (retry #{item['retry_count']}) → {post_id}")
                succeeded += 1
                continue
            else:
                log.warning(f"  ⚠️  {item['persona_id']}: {r.status_code} (retry #{item['retry_count']})")
        except Exception as e:
            log.warning(f"  ⚠️  {item['persona_id']}: {e} (retry #{item['retry_count']})")

        # Keep in queue if failed
        new_queue.append(item)
        failed += 1
        time.sleep(0.3)

    save_queue(new_queue)
    log.info(f"📊 Result: {succeeded} OK, {failed} retry, {dropped} dropped. Queue: {len(new_queue)} pending")


def show_status():
    """Show queue status."""
    queue = load_queue()
    if not queue:
        print("✅ Queue empty — no pending posts")
        return
    print(f"\n📦 Pending Posts Queue — {len(queue)} items\n")
    for i, item in enumerate(queue, 1):
        print(f"{i}. {item.get('persona_id', 'unknown'):30} | retry: {item.get('retry_count', 0)} | scheduled: {item.get('scheduled_at', 'N/A')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--retry", action="store_true", help="Retry queued posts")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    args = parser.parse_args()

    if args.retry:
        retry_queue()
    elif args.status:
        show_status()
    else:
        parser.print_help()
