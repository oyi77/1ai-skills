#!/usr/bin/env python3
"""
PostBridge Bulk Scheduler
Schedules all posts from posting_schedule.json to PostBridge API
"""

import json
import requests
import time
from datetime import datetime, timedelta
import os

# PostBridge API config
API_BASE = "https://api.post-bridge.com/v1"
API_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Rate limiting
REQUESTS_PER_SECOND = 5
DELAY = 1.0 / REQUESTS_PER_SECOND

def load_schedule():
    """Load posting schedule from JSON file"""
    schedule_path = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/posting_schedule.json")
    with open(schedule_path, 'r') as f:
        return json.load(f)

def get_social_accounts():
    """Get all connected social accounts from PostBridge"""
    resp = requests.get(f"{API_BASE}/social-accounts", headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"Error getting accounts: {resp.status_code}")
        return []

def schedule_post(account_id, caption, scheduled_at, platform):
    """Schedule a single post to PostBridge"""
    # Convert datetime string to ISO format
    if isinstance(scheduled_at, str):
        dt = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
    else:
        dt = scheduled_at
    
    payload = {
        "caption": caption,
        "scheduled_at": dt.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "social_accounts": [account_id],
        "media": []  # Text-only post
    }
    
    try:
        resp = requests.post(f"{API_BASE}/posts", headers=HEADERS, json=payload)
        if resp.status_code in [200, 201]:
            return True, resp.json()
        else:
            return False, resp.text
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("PostBridge Bulk Scheduler")
    print("=" * 60)
    
    # Load schedule
    print("\n📂 Loading posting schedule...")
    posts = load_schedule()
    print(f"   Found {len(posts)} posts to schedule")
    
    # Get accounts
    print("\n📱 Getting connected accounts...")
    accounts = get_social_accounts()
    print(f"   Found {len(accounts)} connected accounts")
    
    # Create account ID lookup
    account_ids = set()
    for acc in accounts:
        account_ids.add(acc.get('id'))
    
    # Filter posts to valid accounts
    valid_posts = [p for p in posts if p.get('account_id') in account_ids]
    print(f"   {len(valid_posts)} posts have valid account IDs")
    
    # Schedule posts with staggered times
    # Start from now + 1 hour, spread across 12 days
    start_time = datetime.utcnow() + timedelta(hours=1)
    posts_per_account_per_day = 3
    post_interval_hours = 8  # 3 posts per day = 8 hour intervals
    
    # Group posts by account
    posts_by_account = {}
    for post in valid_posts:
        acc_id = post['account_id']
        if acc_id not in posts_by_account:
            posts_by_account[acc_id] = []
        posts_by_account[acc_id].append(post)
    
    print(f"\n📊 Posts distributed across {len(posts_by_account)} accounts")
    
    # Calculate schedule for each account
    scheduled = 0
    failed = 0
    
    for acc_id, acc_posts in posts_by_account.items():
        acc_time = start_time
        for i, post in enumerate(acc_posts[:10]):  # Limit to first 10 per account for testing
            # Stagger times
            post_time = acc_time + timedelta(hours=i * post_interval_hours)
            
            success, result = schedule_post(
                account_id=acc_id,
                caption=post['caption'],
                scheduled_at=post_time,
                platform=post['platform']
            )
            
            if success:
                scheduled += 1
                print(f"✅ [{scheduled}] Scheduled to {post.get('username', acc_id)[:20]}")
            else:
                failed += 1
                print(f"❌ Failed: {result[:100]}")
            
            time.sleep(DELAY)
            
            # Progress every 50 posts
            if (scheduled + failed) % 50 == 0:
                print(f"\n   Progress: {scheduled} scheduled, {failed} failed")
    
    print("\n" + "=" * 60)
    print(f"COMPLETE: {scheduled} scheduled, {failed} failed")
    print("=" * 60)

if __name__ == "__main__":
    main()
