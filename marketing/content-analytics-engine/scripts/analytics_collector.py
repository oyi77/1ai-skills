"""
analytics_collector.py — Collect all data from PostBridge API
Fetches: analytics, posts, post-results, social-accounts
Saves raw JSON cache for offline analysis
"""

import os
import json
import time
import requests
from datetime import datetime
from pathlib import Path

POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = "REDACTED_ROTATED_CREDENTIAL"
CACHE_DIR = Path("/home/openclaw/.openclaw/workspace/reports/cache")

HEADERS = {
    "Authorization": f"Bearer {POSTBRIDGE_KEY}",
    "Content-Type": "application/json"
}


def _get_all_pages(endpoint: str, params: dict = None) -> list:
    """Paginate through all results for an endpoint."""
    params = params or {}
    params["limit"] = 100
    params["offset"] = 0
    all_data = []

    while True:
        url = f"{POSTBRIDGE_BASE}{endpoint}"
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        data = body.get("data", [])
        all_data.extend(data)
        meta = body.get("meta", {})
        total = meta.get("total", 0)
        offset = meta.get("offset", 0)
        limit = meta.get("limit", 100)
        if offset + limit >= total:
            break
        params["offset"] += limit
        time.sleep(0.1)  # rate limit respect

    return all_data


def fetch_analytics() -> list:
    """Fetch all analytics records."""
    return _get_all_pages("/analytics")


def fetch_posts() -> list:
    """Fetch all posts."""
    return _get_all_pages("/posts")


def fetch_post_results() -> list:
    """Fetch all post-results (success/failure per account)."""
    return _get_all_pages("/post-results")


def fetch_social_accounts() -> list:
    """Fetch all connected social accounts."""
    return _get_all_pages("/social-accounts")


def sync_analytics(platforms: list = None) -> dict:
    """Trigger analytics refresh for given platforms."""
    platforms = platforms or ["tiktok", "youtube", "instagram"]
    results = {}
    for platform in platforms:
        try:
            resp = requests.post(
                f"{POSTBRIDGE_BASE}/analytics/sync",
                headers=HEADERS,
                params={"platform": platform},
                timeout=30
            )
            results[platform] = resp.status_code == 200
        except Exception as e:
            results[platform] = str(e)
    return results


def collect_all(use_cache: bool = False, force_sync: bool = False) -> dict:
    """
    Master collection function. Returns full dataset dict.
    
    Args:
        use_cache: Load from disk cache if available
        force_sync: Trigger PostBridge sync before collecting
    
    Returns:
        {
          "analytics": [...],
          "posts": [...],
          "post_results": [...],
          "social_accounts": [...],
          "collected_at": "ISO timestamp"
        }
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    cache_file = CACHE_DIR / f"{today}-raw.json"

    if use_cache and cache_file.exists():
        print(f"[CACHE] Loading from {cache_file}")
        with open(cache_file) as f:
            return json.load(f)

    if force_sync:
        print("[SYNC] Triggering PostBridge analytics refresh...")
        sync_results = sync_analytics()
        print(f"[SYNC] Results: {sync_results}")
        time.sleep(5)  # wait for sync

    print("[COLLECT] Fetching analytics...")
    analytics = fetch_analytics()
    print(f"[COLLECT] Got {len(analytics)} analytics records")

    print("[COLLECT] Fetching posts...")
    posts = fetch_posts()
    print(f"[COLLECT] Got {len(posts)} posts")

    print("[COLLECT] Fetching post results...")
    post_results = fetch_post_results()
    print(f"[COLLECT] Got {len(post_results)} post results")

    print("[COLLECT] Fetching social accounts...")
    social_accounts = fetch_social_accounts()
    print(f"[COLLECT] Got {len(social_accounts)} social accounts")

    dataset = {
        "analytics": analytics,
        "posts": posts,
        "post_results": post_results,
        "social_accounts": social_accounts,
        "collected_at": datetime.now().isoformat()
    }

    # Save cache
    with open(cache_file, "w") as f:
        json.dump(dataset, f, indent=2, default=str)
    print(f"[CACHE] Saved to {cache_file}")

    return dataset


def build_lookup_maps(dataset: dict) -> dict:
    """
    Build lookup maps for cross-referencing data.
    Returns maps: post_by_id, account_by_id, results_by_post_id,
                  analytics_by_post_result_id
    """
    post_by_id = {p["id"]: p for p in dataset["posts"]}
    account_by_id = {a["id"]: a for a in dataset["social_accounts"]}

    results_by_post_id = {}
    for r in dataset["post_results"]:
        pid = r["post_id"]
        results_by_post_id.setdefault(pid, []).append(r)

    analytics_by_result_id = {}
    for a in dataset["analytics"]:
        rid = a.get("post_result_id")
        if rid:
            analytics_by_result_id[rid] = a

    return {
        "post_by_id": post_by_id,
        "account_by_id": account_by_id,
        "results_by_post_id": results_by_post_id,
        "analytics_by_result_id": analytics_by_result_id
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Collect PostBridge analytics data")
    parser.add_argument("--sync", action="store_true", help="Force analytics sync first")
    parser.add_argument("--cache", action="store_true", help="Use cached data if available")
    args = parser.parse_args()

    data = collect_all(use_cache=args.cache, force_sync=args.sync)
    print(f"\n✅ Collected:")
    print(f"  Analytics records: {len(data['analytics'])}")
    print(f"  Posts: {len(data['posts'])}")
    print(f"  Post results: {len(data['post_results'])}")
    print(f"  Social accounts: {len(data['social_accounts'])}")
