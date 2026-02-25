#!/usr/bin/env python3
"""
viral_amplifier.py — Detect viral posts and amplify your presence.

Features:
  - Detect viral posts by engagement velocity (likes/comments per minute)
  - Queue niche-relevant comments with smart spacing
  - Auto-repost trending content with attribution
  - Velocity scoring to prioritize highest-momentum posts

Usage:
    python3 viral_amplifier.py --niche "productivity" --platform twitter
    python3 viral_amplifier.py --niche "dropshipping" --platform instagram --watch
    python3 viral_amplifier.py --queue-status
"""

import json
import os
import sys
import time
import random
import argparse
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import deque

import requests

# ─── Configuration ────────────────────────────────────────────────────────────

BYTEPLUS_API_URL = "https://ark.ap-southeast.bytepluses.com/api/v3/chat/completions"
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea")
BYTEPLUS_MODEL   = "seed-1-6-250915"

DATA_DIR   = Path(__file__).parent.parent / "data"
QUEUE_FILE = DATA_DIR / "viral_queue.json"
LOG_FILE   = DATA_DIR / "viral_amplifier.log"

# Viral detection thresholds
VIRAL_VELOCITY_THRESHOLD = 5.0   # engagements per minute to be considered viral
MIN_TOTAL_ENGAGEMENT     = 50    # minimum total engagements
COMMENT_QUEUE_SPACING    = 8 * 60  # 8 minutes between queued comments (seconds)

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("viral_amplifier")


# ─── Viral Detection ──────────────────────────────────────────────────────────

class ViralDetector:
    """
    Detects viral posts by measuring engagement velocity.
    Velocity = (likes + comments*2 + shares*3) / minutes_since_posted
    """

    @staticmethod
    def compute_velocity(post: dict) -> float:
        """Compute engagement velocity score for a post."""
        likes    = post.get("likes", 0)
        comments = post.get("comments", 0)
        shares   = post.get("shares", post.get("retweets", 0))

        total_engagement = likes + (comments * 2) + (shares * 3)

        # Time since posted in minutes
        created_at = post.get("created_at")
        if created_at:
            try:
                if isinstance(created_at, str):
                    posted_time = datetime.fromisoformat(created_at)
                else:
                    posted_time = datetime.fromtimestamp(created_at)
                age_minutes = max(1.0, (datetime.now() - posted_time).total_seconds() / 60)
            except Exception:
                age_minutes = 60.0  # Default to 1 hour if parse fails
        else:
            age_minutes = 60.0

        velocity = total_engagement / age_minutes
        return round(velocity, 2)

    @staticmethod
    def is_viral(post: dict, velocity_threshold: float = VIRAL_VELOCITY_THRESHOLD,
                 min_engagement: int = MIN_TOTAL_ENGAGEMENT) -> bool:
        """Return True if post meets viral criteria."""
        total = post.get("likes", 0) + post.get("comments", 0)
        if total < min_engagement:
            return False
        velocity = ViralDetector.compute_velocity(post)
        return velocity >= velocity_threshold

    @staticmethod
    def rank_posts(posts: list[dict]) -> list[dict]:
        """Sort posts by viral velocity score, highest first."""
        scored = []
        for post in posts:
            velocity = ViralDetector.compute_velocity(post)
            scored.append({**post, "_velocity": velocity})
        return sorted(scored, key=lambda p: p["_velocity"], reverse=True)


# ─── Comment Queue ────────────────────────────────────────────────────────────

class CommentQueue:
    """
    Manages a persistent queue of comments to post on viral content.
    Comments are spaced at least COMMENT_QUEUE_SPACING seconds apart.
    """

    def __init__(self, path: Path = QUEUE_FILE):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {
            "queue": [],        # [{"post_id": ..., "comment": ..., "scheduled_at": ..., "posted": bool}]
            "last_posted_at": None,
        }

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def add(self, post_id: str, post_url: str, comment: str, priority: int = 5):
        """Add a comment to the queue."""
        # Avoid duplicates
        existing_ids = {item["post_id"] for item in self.data["queue"]}
        if post_id in existing_ids:
            log.info(f"  ⏭️  Post {post_id} already in queue, skipping")
            return

        scheduled_at = self._next_available_slot()
        entry = {
            "post_id": post_id,
            "post_url": post_url,
            "comment": comment,
            "scheduled_at": scheduled_at.isoformat(),
            "priority": priority,
            "posted": False,
            "added_at": datetime.now().isoformat(),
        }
        self.data["queue"].append(entry)
        self.data["queue"].sort(key=lambda x: (x["posted"], -x["priority"], x["scheduled_at"]))
        self._save()
        log.info(f"📥 Queued comment for post {post_id} at {scheduled_at.strftime('%H:%M:%S')}")

    def _next_available_slot(self) -> datetime:
        """Calculate when next comment can be posted."""
        pending = [
            datetime.fromisoformat(item["scheduled_at"])
            for item in self.data["queue"]
            if not item["posted"]
        ]
        if not pending:
            last = self.data.get("last_posted_at")
            if last:
                last_dt = datetime.fromisoformat(last)
                earliest = last_dt + timedelta(seconds=COMMENT_QUEUE_SPACING)
                return max(earliest, datetime.now())
            return datetime.now()
        last_scheduled = max(pending)
        return last_scheduled + timedelta(seconds=COMMENT_QUEUE_SPACING)

    def get_due(self) -> list[dict]:
        """Return comments that are due to be posted now."""
        now = datetime.now()
        return [
            item for item in self.data["queue"]
            if not item["posted"] and datetime.fromisoformat(item["scheduled_at"]) <= now
        ]

    def mark_posted(self, post_id: str):
        """Mark a queued comment as posted."""
        for item in self.data["queue"]:
            if item["post_id"] == post_id:
                item["posted"] = True
                item["posted_at"] = datetime.now().isoformat()
        self.data["last_posted_at"] = datetime.now().isoformat()
        self._save()

    def status(self) -> dict:
        """Return queue status summary."""
        total   = len(self.data["queue"])
        pending = sum(1 for i in self.data["queue"] if not i["posted"])
        done    = total - pending
        return {
            "total": total,
            "pending": pending,
            "posted": done,
            "next_slot": self._next_available_slot().isoformat(),
        }

    def clear_old(self, days: int = 7):
        """Remove items older than N days."""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        before = len(self.data["queue"])
        self.data["queue"] = [
            i for i in self.data["queue"]
            if i["added_at"] > cutoff or not i["posted"]
        ]
        removed = before - len(self.data["queue"])
        if removed:
            self._save()
            log.info(f"🗑️  Cleared {removed} old queue entries")


# ─── AI Commenter ─────────────────────────────────────────────────────────────

def generate_viral_comment(
    post_content: str,
    niche: str,
    platform: str,
    comment_style: str = "insightful",
) -> Optional[str]:
    """Generate a comment optimized for viral posts using BytePlus AI."""

    style_prompts = {
        "insightful": "Add a genuinely insightful observation that enriches the conversation.",
        "question": "Ask a thoughtful follow-up question that gets others to engage.",
        "agreement": "Agree in a specific, non-generic way and add a related data point or experience.",
        "story": "Share a 1-sentence relevant micro-story or example.",
    }

    system_prompt = f"""You are a social media expert specializing in the {niche} niche.
Write comments for viral {platform} posts that:
- {style_prompts.get(comment_style, style_prompts['insightful'])}
- Sound natural and human, not bot-like
- Are specific to the post content
- Don't mention brands or plug products
- Are conversational and encourage reply
- 1-3 sentences max (unless LinkedIn)
Return ONLY the comment text, no quotes or explanation."""

    payload = {
        "model": BYTEPLUS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Write a comment for this viral {platform} post:\n\n{post_content}",
            },
        ],
        "temperature": 0.9,
        "max_tokens": 120,
    }

    try:
        resp = requests.post(
            BYTEPLUS_API_URL,
            headers={
                "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"AI comment generation failed: {e}")
        return None


# ─── Repost Logic ─────────────────────────────────────────────────────────────

def generate_repost_caption(
    original_content: str,
    original_author: str,
    niche: str,
    platform: str,
) -> Optional[str]:
    """Generate a caption for reposting/quoting a trending post."""

    system_prompt = f"""You write captions for sharing trending content in the {niche} niche.
Your repost caption should:
- Add your own angle or commentary (not just "sharing this!")
- Credit the original author
- Add 1-2 relevant hashtags
- Be engaging and make your followers want to see the original
- Platform: {platform}
Return ONLY the caption text."""

    payload = {
        "model": BYTEPLUS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Original post by @{original_author}:\n\n{original_content}\n\nWrite a repost caption.",
            },
        ],
        "temperature": 0.8,
        "max_tokens": 200,
    }

    try:
        resp = requests.post(
            BYTEPLUS_API_URL,
            headers={
                "Authorization": f"Bearer {BYTEPLUS_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"Repost caption generation failed: {e}")
        return None


# ─── Mock Platform Client ─────────────────────────────────────────────────────

class MockPlatformClient:
    def __init__(self, platform: str):
        self.platform = platform

    def search_trending(self, niche: str, limit: int = 30) -> list[dict]:
        log.info(f"[MOCK] Fetching trending {self.platform} posts in '{niche}'")
        styles = [
            f"Just realized {niche} is going to change everything in 2025. Thread 🧵",
            f"Controversial take on {niche}: most people are doing it completely wrong.",
            f"I went from $0 to $10k/mo in {niche} in 6 months. Here's the exact playbook:",
            f"Nobody is talking about this {niche} hack that saves me 3 hours/week.",
        ]
        posts = []
        for i in range(limit):
            age_minutes = random.uniform(1, 120)
            created_at = (datetime.now() - timedelta(minutes=age_minutes)).isoformat()
            likes    = random.randint(10, 10000)
            comments = random.randint(5, 1000)
            shares   = random.randint(0, 500)
            posts.append({
                "id": hashlib.md5(f"{niche}-trend-{i}".encode()).hexdigest()[:12],
                "author_id": f"influencer_{i}",
                "author_handle": f"@trend_account_{i}",
                "content": random.choice(styles),
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "created_at": created_at,
                "url": f"https://{self.platform}.com/post/{i}",
            })
        return posts

    def comment_post(self, post_id: str, text: str) -> bool:
        log.info(f"[MOCK] 💬 Commenting on {post_id}: '{text[:60]}...'")
        return True

    def repost(self, post_id: str, caption: str = "") -> bool:
        log.info(f"[MOCK] 🔁 Reposting {post_id} with caption: '{caption[:60]}...'")
        return True


# ─── Viral Amplifier Engine ───────────────────────────────────────────────────

class ViralAmplifier:
    """Main viral amplification engine."""

    def __init__(
        self,
        niche: str,
        platform: str = "twitter",
        dry_run: bool = False,
        auto_repost: bool = False,
        velocity_threshold: float = VIRAL_VELOCITY_THRESHOLD,
    ):
        self.niche              = niche
        self.platform           = platform
        self.dry_run            = dry_run
        self.auto_repost        = auto_repost
        self.velocity_threshold = velocity_threshold

        self.detector = ViralDetector()
        self.queue    = CommentQueue()
        self.client   = MockPlatformClient(platform)

        # Cycle through comment styles
        self.comment_styles = deque(["insightful", "question", "agreement", "story"])

        log.info(f"🚀 Viral Amplifier | niche={niche} | platform={platform} | threshold={velocity_threshold}")

    def _next_comment_style(self) -> str:
        style = self.comment_styles[0]
        self.comment_styles.rotate(-1)
        return style

    def scan_and_queue(self, limit: int = 30):
        """Scan trending posts, detect viral ones, queue comments."""
        log.info(f"\n🔍 Scanning {self.platform} for viral {self.niche} posts...")
        posts = self.client.search_trending(self.niche, limit=limit)

        ranked = self.detector.rank_posts(posts)
        viral  = [p for p in ranked if self.detector.is_viral(p, self.velocity_threshold)]

        log.info(f"📊 Found {len(posts)} posts → {len(viral)} viral (velocity ≥ {self.velocity_threshold}/min)")

        for post in viral:
            velocity = post["_velocity"]
            log.info(f"  🔥 Viral: {post['id']} by {post['author_handle']} | velocity={velocity:.1f}/min | likes={post['likes']}")

            # Generate and queue comment
            comment = generate_viral_comment(
                post_content=post["content"],
                niche=self.niche,
                platform=self.platform,
                comment_style=self._next_comment_style(),
            )
            if comment:
                priority = min(10, int(velocity))
                self.queue.add(
                    post_id=post["id"],
                    post_url=post.get("url", ""),
                    comment=comment,
                    priority=priority,
                )

            # Auto-repost if enabled and post is very viral
            if self.auto_repost and velocity > self.velocity_threshold * 2:
                caption = generate_repost_caption(
                    original_content=post["content"],
                    original_author=post["author_handle"].lstrip("@"),
                    niche=self.niche,
                    platform=self.platform,
                )
                if caption:
                    if not self.dry_run:
                        self.client.repost(post["id"], caption)
                    else:
                        log.info(f"  [DRY RUN] Would repost {post['id']}: '{caption[:60]}...'")

        status = self.queue.status()
        log.info(f"📥 Queue: {status['pending']} pending | {status['posted']} posted | next slot: {status['next_slot']}")

    def process_queue(self):
        """Post any comments that are due."""
        due = self.queue.get_due()
        if not due:
            log.info("⏰ No comments due yet")
            return

        log.info(f"📤 Processing {len(due)} due comments...")
        for item in due:
            log.info(f"  💬 Posting comment on {item['post_id']}: '{item['comment'][:60]}...'")
            if not self.dry_run:
                success = self.client.comment_post(item["post_id"], item["comment"])
                if success:
                    self.queue.mark_posted(item["post_id"])
            else:
                log.info("  [DRY RUN] Skipping actual post")
                self.queue.mark_posted(item["post_id"])

    def run(self, watch: bool = False, scan_interval_min: float = 30.0):
        """Run one scan+queue cycle, or continuously watch."""
        if watch:
            log.info(f"👁️  Watching mode: scanning every {scan_interval_min}m")
            while True:
                self.scan_and_queue()
                self.process_queue()
                self.queue.clear_old()
                log.info(f"😴 Sleeping {scan_interval_min}m...")
                time.sleep(scan_interval_min * 60)
        else:
            self.scan_and_queue()
            self.process_queue()


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Viral Amplifier — detect and ride viral waves")
    parser.add_argument("--niche", "-n", required=True, help="Your content niche")
    parser.add_argument(
        "--platform", "-p",
        default="twitter",
        choices=["twitter", "instagram", "tiktok", "linkedin"],
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--watch", action="store_true", help="Continuously monitor for viral posts")
    parser.add_argument("--auto-repost", action="store_true", help="Auto-repost extremely viral content")
    parser.add_argument("--interval", type=float, default=30.0, help="Scan interval in minutes (watch mode)")
    parser.add_argument("--threshold", type=float, default=VIRAL_VELOCITY_THRESHOLD, help="Viral velocity threshold")
    parser.add_argument("--queue-status", action="store_true", help="Show queue status and exit")
    args = parser.parse_args()

    if args.queue_status:
        q = CommentQueue()
        print(json.dumps(q.status(), indent=2))
        return

    amp = ViralAmplifier(
        niche=args.niche,
        platform=args.platform,
        dry_run=args.dry_run,
        auto_repost=args.auto_repost,
        velocity_threshold=args.threshold,
    )
    amp.run(watch=args.watch, scan_interval_min=args.interval)


if __name__ == "__main__":
    main()
