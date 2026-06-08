"""
comment_monitor.py — Monitor comments on posts via PostBridge API
Fetches post IDs and analytics to identify posts with engagement
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Optional

# ─── CONFIG ────────────────────────────────────────────────────────────────────
POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = os.environ.get("POSTBRIDGE_KEY", "REDACTED_ROTATED_CREDENTIAL")

HEADERS = {
    "Authorization": f"Bearer {POSTBRIDGE_KEY}",
    "Content-Type": "application/json",
}

CACHE_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/1ai-skills/content/comment-reply-manager/cache/posts_cache.json"
)


def _get(endpoint: str, params: dict = None) -> dict:
    """Make authenticated GET request to PostBridge API."""
    url = f"{POSTBRIDGE_BASE}{endpoint}"
    try:
        resp = requests.get(url, headers=HEADERS, params=params or {}, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        print(
            f"[PostBridge] HTTP Error {e.response.status_code}: {e.response.text[:200]}"
        )
        return {}
    except Exception as e:
        print(f"[PostBridge] Error: {e}")
        return {}


def fetch_posts(platform: str = None, limit: int = 50) -> list:
    """Fetch list of published posts from PostBridge."""
    params = {"limit": limit, "status": "posted"}
    if platform:
        params["platform"] = platform
    data = _get("/posts", params)
    posts = data.get("data", data.get("posts", []))
    print(f"[Monitor] Fetched {len(posts)} posts from PostBridge")
    return posts


def fetch_post_results(limit: int = 50) -> list:
    """Fetch post results with platform-specific post IDs."""
    data = _get("/post-results", {"limit": limit})
    results = data.get("data", data.get("results", []))
    print(f"[Monitor] Fetched {len(results)} post results")
    return results


def fetch_analytics(post_id: str = None) -> dict:
    """Fetch analytics for posts — returns engagement data."""
    params = {}
    if post_id:
        params["post_id"] = post_id
    data = _get("/analytics", params)
    return data


def get_posts_with_engagement(min_comments: int = 1) -> list:
    """
    Return posts that have comments (based on analytics).
    These are the posts we need to reply to.
    """
    results = fetch_post_results(limit=100)
    engaged_posts = []

    for result in results:
        # PostBridge post-results format may vary
        comments = result.get("comments_count", result.get("comment_count", 0)) or 0
        if comments >= min_comments:
            engaged_posts.append(
                {
                    "postbridge_id": result.get("id") or result.get("post_id"),
                    "platform": result.get("platform", "unknown"),
                    "platform_post_id": result.get("platform_post_id")
                    or result.get("external_id"),
                    "account_id": result.get("social_account_id")
                    or result.get("account_id"),
                    "username": result.get("username")
                    or result.get("account_username", ""),
                    "url": result.get("url") or result.get("post_url", ""),
                    "comments_count": comments,
                    "likes_count": result.get("likes_count", 0) or 0,
                    "caption": result.get("caption", "")[:100],
                    "published_at": result.get("published_at")
                    or result.get("created_at", ""),
                }
            )

    print(f"[Monitor] {len(engaged_posts)} posts with >={min_comments} comments")
    return engaged_posts


def get_platform_post_ids() -> dict:
    """
    Return dict mapping platform → list of (username, platform_post_id).
    Used by TikTok/IG scrapers to target specific posts.
    """
    results = fetch_post_results(limit=100)
    platform_map = {}

    for result in results:
        platform = result.get("platform", "unknown").lower()
        post_id = result.get("platform_post_id") or result.get("external_id")
        username = result.get("username") or result.get("account_username", "")
        url = result.get("url") or result.get("post_url", "")

        if platform not in platform_map:
            platform_map[platform] = []

        if post_id or url:
            platform_map[platform].append(
                {
                    "username": username,
                    "post_id": post_id,
                    "url": url,
                }
            )

    return platform_map


def cache_posts(posts: list):
    """Save posts to local cache."""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(
            {
                "cached_at": datetime.now().isoformat(),
                "posts": posts,
            },
            f,
            indent=2,
        )
    print(f"[Monitor] Cached {len(posts)} posts to {CACHE_FILE}")


def load_cached_posts(max_age_minutes: int = 30) -> Optional[list]:
    """Load posts from cache if fresh."""
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE) as f:
        data = json.load(f)
    cached_at = datetime.fromisoformat(data["cached_at"])
    if datetime.now() - cached_at > timedelta(minutes=max_age_minutes):
        return None
    return data["posts"]


def monitor_loop(interval_seconds: int = 300, callback=None):
    """
    Continuous monitoring loop. Calls callback(post) for each post with comments.
    callback signature: callback(post: dict)
    """
    print(f"[Monitor] Starting loop — checking every {interval_seconds}s")
    seen_ids = set()

    while True:
        try:
            posts = get_posts_with_engagement(min_comments=1)
            for post in posts:
                post_key = f"{post['platform']}:{post['platform_post_id']}"
                if post_key not in seen_ids:
                    seen_ids.add(post_key)
                    if callback:
                        callback(post)
                    else:
                        print(
                            f"[Monitor] New engaged post: {post['platform']} @{post['username']} "
                            f"({post['comments_count']} comments) — {post['url']}"
                        )
        except Exception as e:
            print(f"[Monitor] Loop error: {e}")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    print("=== PostBridge Comment Monitor ===\n")

    print("[1] Fetching posts...")
    posts = fetch_posts(limit=10)
    if posts:
        print(f"    Sample post: {json.dumps(posts[0], indent=2)[:300]}")

    print("\n[2] Fetching post results (with platform IDs)...")
    results = fetch_post_results(limit=5)
    if results:
        print(f"    Sample result: {json.dumps(results[0], indent=2)[:300]}")

    print("\n[3] Platform post ID map:")
    pmap = get_platform_post_ids()
    for platform, items in pmap.items():
        print(f"    {platform}: {len(items)} posts")
        if items:
            print(f"      Sample: {items[0]}")

    print("\n[4] Posts with engagement:")
    engaged = get_posts_with_engagement(min_comments=0)
    for p in engaged[:5]:
        print(
            f"    {p['platform']} @{p['username']} — {p['comments_count']} comments — {p['url']}"
        )
