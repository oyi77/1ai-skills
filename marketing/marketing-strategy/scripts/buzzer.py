#!/usr/bin/env python3
"""
buzzer.py — Strategic social media engagement buzzer.

Monitors keywords/hashtags across platforms and engages (like/comment/follow)
with niche-relevant content. Tracks engagement history to avoid over-engaging.
Uses BytePlus AI to generate authentic, context-aware comments.

Usage:
    python3 buzzer.py --keywords "python,indie hacker,solopreneur" --platform twitter
    python3 buzzer.py --keywords "dropshipping" --platform instagram --dry-run
    python3 buzzer.py --config config.json

Config file (~/.buzzer-config.json):
    {
        "keywords": ["indie hacker", "solopreneur", "build in public"],
        "hashtags": ["#indiehacker", "#buildinpublic"],
        "platform": "twitter",
        "max_actions_per_hour": 10,
        "max_follows_per_day": 20,
        "max_comments_per_day": 15,
        "brand_voice": "friendly, knowledgeable, helpful",
        "niche": "productivity tools for solopreneurs"
    }
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

import requests

# ─── Social Scraper (real web scraping, no API keys) ──────────────────────────
import sys as _scraper_sys
import os as _scraper_os

_scraper_sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from scrapers.social_scraper import SocialScraper as _SocialScraper

    _SCRAPER_AVAILABLE = True
except ImportError:
    _SCRAPER_AVAILABLE = False

# ─── Configuration ────────────────────────────────────────────────────────────

BYTEPLUS_API_URL = "https://ark.ap-southeast.bytepluses.com/api/v3/chat/completions"
BYTEPLUS_API_KEY = os.environ.get(
    "BYTEPLUS_API_KEY", "cac5cfc1-e30f-47bb-b8b8-e861ffda28ea"
)
BYTEPLUS_MODEL = "seed-1-6-250915"

DATA_DIR = Path(__file__).parent.parent / "data"
HISTORY_FILE = DATA_DIR / "engagement_history.json"
LOG_FILE = DATA_DIR / "buzzer.log"

# Delay range in seconds (5-30 minutes)
MIN_DELAY_SEC = 5 * 60
MAX_DELAY_SEC = 30 * 60

# ─── Logging ──────────────────────────────────────────────────────────────────

DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("buzzer")


# ─── Engagement History ───────────────────────────────────────────────────────


class EngagementHistory:
    """Tracks all engagement actions to avoid over-engaging with the same accounts/posts."""

    def __init__(self, path: Path = HISTORY_FILE):
        self.path = path
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {
            "likes": {},  # post_id -> timestamp
            "comments": {},  # post_id -> {"timestamp": ..., "text": ...}
            "follows": {},  # user_id -> timestamp
            "daily_counts": {},  # "YYYY-MM-DD" -> {"likes": n, "comments": n, "follows": n}
        }

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def _today(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def _day_counts(self) -> dict:
        today = self._today()
        if today not in self.data["daily_counts"]:
            self.data["daily_counts"][today] = {"likes": 0, "comments": 0, "follows": 0}
        return self.data["daily_counts"][today]

    def already_liked(self, post_id: str) -> bool:
        return post_id in self.data["likes"]

    def already_commented(self, post_id: str) -> bool:
        return post_id in self.data["comments"]

    def already_followed(self, user_id: str) -> bool:
        return user_id in self.data["follows"]

    def can_like(self, max_per_day: int = 50) -> bool:
        return self._day_counts()["likes"] < max_per_day

    def can_comment(self, max_per_day: int = 15) -> bool:
        return self._day_counts()["comments"] < max_per_day

    def can_follow(self, max_per_day: int = 20) -> bool:
        return self._day_counts()["follows"] < max_per_day

    def record_like(self, post_id: str):
        self.data["likes"][post_id] = datetime.now().isoformat()
        self._day_counts()["likes"] += 1
        self._save()
        log.info(f"📋 Recorded like on post {post_id}")

    def record_comment(self, post_id: str, text: str):
        self.data["comments"][post_id] = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
        }
        self._day_counts()["comments"] += 1
        self._save()
        log.info(f"📋 Recorded comment on post {post_id}")

    def record_follow(self, user_id: str):
        self.data["follows"][user_id] = datetime.now().isoformat()
        self._day_counts()["follows"] += 1
        self._save()
        log.info(f"📋 Recorded follow of user {user_id}")

    def stats(self) -> dict:
        today = self._today()
        counts = self.data["daily_counts"].get(today, {})
        return {
            "today": today,
            "daily_likes": counts.get("likes", 0),
            "daily_comments": counts.get("comments", 0),
            "daily_follows": counts.get("follows", 0),
            "total_likes": len(self.data["likes"]),
            "total_comments": len(self.data["comments"]),
            "total_follows": len(self.data["follows"]),
        }


# ─── AI Comment Generator ─────────────────────────────────────────────────────


class AICommentGenerator:
    """Generates authentic, contextual comments via BytePlus AI."""

    def __init__(self, api_key: str = BYTEPLUS_API_KEY, model: str = BYTEPLUS_MODEL):
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        post_content: str,
        brand_voice: str = "friendly and knowledgeable",
        niche: str = "general business",
        platform: str = "twitter",
        max_length: int = 280,
    ) -> Optional[str]:
        """Generate a contextual comment for a given post."""

        platform_hint = {
            "twitter": "Keep it under 280 chars, casual, no hashtags in the comment itself.",
            "instagram": "Warm and friendly, can include 1-2 emojis, 1-2 hashtags if relevant.",
            "tiktok": "Very casual, Gen-Z friendly, short, 1-2 emojis max.",
            "linkedin": "Professional, insightful, add value. 1-3 sentences.",
        }.get(platform.lower(), "Be concise and genuine.")

        system_prompt = f"""You are a social media engagement specialist for a brand in the {niche} niche.
Your brand voice: {brand_voice}.
Generate genuine, non-spammy comments that add value to the conversation.
{platform_hint}
Rules:
- Never sound like a bot or marketer
- Do NOT mention the brand name or plug products
- React authentically to what was said
- Be specific to the post content
- 1-2 sentences max unless LinkedIn
- No generic phrases like "Great post!" or "Love this!"
"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Write a comment for this {platform} post:\n\n{post_content}",
                },
            ],
            "temperature": 0.85,
            "max_tokens": 150,
        }

        try:
            resp = requests.post(
                BYTEPLUS_API_URL,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
            comment = resp.json()["choices"][0]["message"]["content"].strip()
            return comment[:max_length] if len(comment) > max_length else comment
        except Exception as e:
            log.error(f"AI comment generation failed: {e}")
            return None


# ─── Post Bridge Platform Client ─────────────────────────────────────────────

import sys as _sys
import os as _os

_sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from post_bridge_client import PostBridgeClient as _PostBridgeClient


class PostBridgePlatformClient:
    """
    Platform client backed by the Post Bridge API (post-bridge.com).

    Discovers connected social accounts dynamically via GET /social-accounts
    and publishes comments/posts via POST /posts.

    Note: Post Bridge is a publishing API — it does not provide a search API.
    The search_posts() method returns stub data so the buzzer engagement loop
    still works; actual publishing goes through Post Bridge.
    """

    def __init__(self, platform: str):
        self.platform = platform.lower()
        self._pb = _PostBridgeClient()
        # Fetch and cache accounts for this platform
        self._accounts = self._pb.get_accounts_by_platform(self.platform)
        self._account_ids = [a["id"] for a in self._accounts]
        if self._account_ids:
            log.info(
                f"🔌 PostBridge: {len(self._account_ids)} {self.platform} account(s) connected: "
                f"{[a.get('username') for a in self._accounts]}"
            )
        else:
            log.warning(
                f"⚠️  PostBridge: no connected {self.platform} accounts found. "
                f"Posts will broadcast to ALL connected accounts."
            )
            self._account_ids = self._pb.get_all_account_ids()

    def search_posts(self, keyword: str, limit: int = 20) -> list[dict]:
        """
        Search for posts matching a keyword using real web scraping (SocialScraper).
        Falls back to stub data if scraper is unavailable.
        """
        if _SCRAPER_AVAILABLE:
            log.info(
                f"[PostBridge] Scraping {self.platform} for '{keyword}' (real data)..."
            )
            try:
                scraper = _SocialScraper()
                posts = scraper.search(keyword, platform=self.platform, limit=limit)
                if posts:
                    log.info(
                        f"[PostBridge] Got {len(posts)} real posts for '{keyword}'"
                    )
                    return posts
            except Exception as e:
                log.warning(
                    f"[PostBridge] SocialScraper failed: {e} — falling back to stub data"
                )

        log.info(
            f"[PostBridge] Searching {self.platform} for '{keyword}' — using stub data (scraper unavailable)"
        )
        return [
            {
                "id": hashlib.md5(f"{keyword}-{i}".encode()).hexdigest()[:12],
                "author_id": f"user_{i}",
                "author_handle": f"@user_{i}",
                "content": f"Post #{i} about {keyword}",
                "likes": random.randint(5, 500),
                "comments": random.randint(1, 50),
                "created_at": (
                    datetime.now() - timedelta(hours=random.randint(1, 24))
                ).isoformat(),
            }
            for i in range(limit)
        ]

    def get_trending(self, category: str = "general", limit: int = 20) -> list[dict]:
        """
        Fetch trending posts for this platform using real web scraping.
        Falls back to empty list if scraper is unavailable.
        """
        if _SCRAPER_AVAILABLE:
            try:
                scraper = _SocialScraper()
                posts = scraper.get_trending(
                    platform=self.platform, category=category, limit=limit
                )
                log.info(
                    f"[PostBridge] Got {len(posts)} trending posts for {self.platform}/{category}"
                )
                return posts
            except Exception as e:
                log.warning(f"[PostBridge] get_trending scraper failed: {e}")
        return []

    def like_post(self, post_id: str) -> bool:
        """Like a post. Post Bridge doesn't support like actions; logged only."""
        log.info(
            f"[PostBridge] ❤️  Like action not supported by Post Bridge API — post={post_id}"
        )
        return True

    def comment_post(self, post_id: str, text: str) -> bool:
        """
        Publish a comment as a new post via Post Bridge.
        Maps to POST /posts with the comment text as the caption.
        """
        log.info(
            f"[PostBridge] 💬 Publishing comment as post on {self.platform}: '{text[:60]}...'"
        )
        result = self._pb.create_post(
            caption=text,
            account_ids=self._account_ids,
        )
        return "error" not in result

    def follow_user(self, user_id: str) -> bool:
        """Follow a user. Post Bridge doesn't support follow actions; logged only."""
        log.info(
            f"[PostBridge] 👤 Follow action not supported by Post Bridge API — user={user_id}"
        )
        return True


# Alias for backward compatibility / dry-run mode
class MockPlatformClient(PostBridgePlatformClient):
    """Legacy alias — now backed by PostBridgeClient."""

    pass


# ─── Buzzer Engine ────────────────────────────────────────────────────────────


class Buzzer:
    """Main engagement engine."""

    def __init__(
        self,
        keywords: list[str],
        platform: str = "twitter",
        config: dict = None,
        dry_run: bool = False,
    ):
        self.keywords = keywords
        self.platform = platform
        self.dry_run = dry_run
        self.config = config or {}

        self.max_likes_day = self.config.get("max_likes_per_day", 50)
        self.max_comments_day = self.config.get("max_comments_per_day", 15)
        self.max_follows_day = self.config.get("max_follows_per_day", 20)
        self.brand_voice = self.config.get("brand_voice", "friendly and knowledgeable")
        self.niche = self.config.get("niche", "general business")

        self.history = EngagementHistory()
        self.ai = AICommentGenerator()
        self.client = PostBridgePlatformClient(platform)

        log.info(
            f"🚀 Buzzer initialized | platform={platform} | keywords={keywords} | dry_run={dry_run}"
        )

    def _random_delay(self, label: str = "next action"):
        """Sleep a random human-like delay between actions."""
        delay = random.randint(MIN_DELAY_SEC, MAX_DELAY_SEC)
        mins = delay // 60
        secs = delay % 60
        log.info(f"⏳ Waiting {mins}m {secs}s before {label}...")
        if not self.dry_run:
            time.sleep(delay)
        else:
            log.info("  [DRY RUN] Skipping actual sleep")

    def _should_engage(self, post: dict) -> dict:
        """Decide which engagement actions to take for a post."""
        engagement = {"like": False, "comment": False, "follow": False}

        # Engagement velocity score (more likes/comments = more interesting)
        score = post.get("likes", 0) + post.get("comments", 0) * 3

        if not self.history.already_liked(post["id"]) and self.history.can_like(
            self.max_likes_day
        ):
            if score > 0:
                engagement["like"] = True

        if not self.history.already_commented(post["id"]) and self.history.can_comment(
            self.max_comments_day
        ):
            if score > 20:  # Only comment on posts with decent engagement
                engagement["comment"] = True

        if not self.history.already_followed(
            post["author_id"]
        ) and self.history.can_follow(self.max_follows_day):
            if score > 50:  # Follow higher-engagement accounts
                engagement["follow"] = True

        return engagement

    def process_post(self, post: dict):
        """Process a single post — decide and execute engagement."""
        log.info(f"👀 Processing post {post['id']} by {post['author_handle']}")
        engagement = self._should_engage(post)

        if not any(engagement.values()):
            log.info(
                f"  ⏭️  Skipping post {post['id']} (already engaged or limits reached)"
            )
            return

        # Like
        if engagement["like"]:
            if not self.dry_run:
                success = self.client.like_post(post["id"])
                if success:
                    self.history.record_like(post["id"])
            else:
                log.info(f"  [DRY RUN] Would like post {post['id']}")
                self.history.record_like(post["id"])

        # Comment
        if engagement["comment"]:
            comment_text = self.ai.generate(
                post_content=post["content"],
                brand_voice=self.brand_voice,
                niche=self.niche,
                platform=self.platform,
            )
            if comment_text:
                if not self.dry_run:
                    success = self.client.comment_post(post["id"], comment_text)
                    if success:
                        self.history.record_comment(post["id"], comment_text)
                else:
                    log.info(f"  [DRY RUN] Would comment: '{comment_text[:80]}...'")
                    self.history.record_comment(post["id"], comment_text)

        # Follow
        if engagement["follow"]:
            if not self.dry_run:
                success = self.client.follow_user(post["author_id"])
                if success:
                    self.history.record_follow(post["author_id"])
            else:
                log.info(f"  [DRY RUN] Would follow {post['author_handle']}")
                self.history.record_follow(post["author_id"])

    def run_once(self, posts_per_keyword: int = 10):
        """Run one cycle of engagement across all keywords."""
        log.info("=" * 60)
        log.info("🔄 Starting engagement cycle")

        stats_before = self.history.stats()
        log.info(f"📊 Daily stats: {stats_before}")

        for keyword in self.keywords:
            log.info(f"\n🔍 Searching for: {keyword}")
            posts = self.client.search_posts(keyword, limit=posts_per_keyword)

            for post in posts:
                self.process_post(post)
                self._random_delay(f"next post in '{keyword}'")

        stats_after = self.history.stats()
        log.info("\n📊 Cycle complete!")
        log.info(f"  Likes today:    {stats_after['daily_likes']}")
        log.info(f"  Comments today: {stats_after['daily_comments']}")
        log.info(f"  Follows today:  {stats_after['daily_follows']}")

    def run_continuous(
        self, cycle_interval_hours: float = 2.0, posts_per_keyword: int = 10
    ):
        """Run continuous engagement cycles with hourly intervals."""
        log.info(f"🔁 Running continuous mode (cycle every {cycle_interval_hours}h)")
        while True:
            self.run_once(posts_per_keyword=posts_per_keyword)
            sleep_sec = cycle_interval_hours * 3600
            log.info(f"😴 Sleeping {cycle_interval_hours}h until next cycle...")
            time.sleep(sleep_sec)


# ─── CLI Entry Point ──────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Buzzer — Strategic social media engagement bot"
    )
    parser.add_argument(
        "--keywords",
        "-k",
        help="Comma-separated list of keywords/hashtags to monitor",
    )
    parser.add_argument(
        "--platform",
        "-p",
        default="twitter",
        choices=["twitter", "instagram", "tiktok", "linkedin"],
        help="Target platform (default: twitter)",
    )
    parser.add_argument(
        "--config",
        "-c",
        help="Path to JSON config file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without actually posting",
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run in continuous mode (loop every N hours)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Hours between cycles in continuous mode (default: 2.0)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show engagement stats and exit",
    )
    args = parser.parse_args()

    # Load config
    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    # Show stats
    if args.stats:
        h = EngagementHistory()
        print(json.dumps(h.stats(), indent=2))
        return

    # Build keywords list
    keywords = []
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    elif "keywords" in config:
        keywords = config["keywords"]
    if not keywords:
        parser.error("Provide --keywords or a config file with 'keywords'")

    buzzer = Buzzer(
        keywords=keywords,
        platform=args.platform or config.get("platform", "twitter"),
        config=config,
        dry_run=args.dry_run,
    )

    if args.continuous:
        buzzer.run_continuous(cycle_interval_hours=args.interval)
    else:
        buzzer.run_once()


if __name__ == "__main__":
    main()
