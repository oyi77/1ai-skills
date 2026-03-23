#!/usr/bin/env python3
"""
PostBridge Mass Scheduler - Schedule ALL posts to ALL accounts
Uses existing posting_schedule.json
"""

import json
import requests
import time
from datetime import datetime, timedelta, timezone
import os

# PostBridge API
API_BASE = "https://api.post-bridge.com/v1"
API_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Rate limiting - 5 requests/second
DELAY = 0.25

def load_accounts():
    """Load PostBridge accounts"""
    path = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/postbridge_accounts.json")
    with open(path) as f:
        return json.load(f)

def load_schedule():
    """Load posting schedule"""
    path = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/posting_schedule.json")
    with open(path) as f:
        return json.load(f)

def schedule_post(account_id, caption, scheduled_at):
    """Schedule a post to PostBridge"""
    payload = {
        "caption": caption,
        "scheduled_at": scheduled_at,
        "social_accounts": [account_id]
    }
    
    try:
        resp = requests.post(f"{API_BASE}/posts", headers=HEADERS, json=payload, timeout=30)
        if resp.status_code in [200, 201]:
            return True, None
        else:
            return False, resp.text[:100]
    except Exception as e:
        return False, str(e)[:100]

def main():
    print("=" * 70)
    print("🚀 PostBridge Mass Scheduler - Shopee Affiliate")
    print("=" * 70)
    
    # Load data
    accounts = load_accounts()
    posts = load_schedule()
    
    print(f"\n📱 Accounts: {len(accounts)}")
    print(f"📝 Posts to schedule: {len(posts)}")
    
    # Create account ID set for validation
    valid_account_ids = {a['id'] for a in accounts}
    
    # Filter to text-only platforms
    text_platforms = ['facebook', 'threads', 'tiktok', 'twitter', 'linkedin', 'youtube']
    
    # Filter valid posts
    valid_posts = []
    for post in posts:
        if post.get('account_id') in valid_account_ids:
            if post.get('platform') in text_platforms:
                valid_posts.append(post)
    
    print(f"✅ Valid posts (matching accounts): {len(valid_posts)}")
    
    # Recalculate schedule times - start 30 min from now
    start_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    # Group by account
    posts_by_account = {}
    for post in valid_posts:
        acc_id = post['account_id']
        if acc_id not in posts_by_account:
            posts_by_account[acc_id] = []
        posts_by_account[acc_id].append(post)
    
    print(f"📊 Distribution: {len(posts_by_account)} accounts")
    
    # Schedule posts
    successful = 0
    failed = 0
    skipped = 0
    
    for acc_id, acc_posts in posts_by_account.items():
        # 3 posts per day, 8 hour intervals
        for i, post in enumerate(acc_posts):
            # Calculate time slot
            day = i // 3
            slot = i % 3
            post_time = start_time + timedelta(days=day, hours=slot * 8)
            
            # Format for API
            scheduled_at = post_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            
            success, error = schedule_post(acc_id, post['caption'], scheduled_at)
            
            if success:
                successful += 1
                if successful % 100 == 0:
                    print(f"✅ Progress: {successful} scheduled")
            else:
                failed += 1
                if failed <= 10:
                    print(f"❌ [{post.get('username', '?')[:15]}] {error}")
            
            time.sleep(DELAY)
    
    print("\n" + "=" * 70)
    print(f"📊 FINAL RESULTS")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⏭️ Skipped: {skipped}")
    print("=" * 70)
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "successful": successful,
        "failed": failed,
        "accounts_used": len(posts_by_account)
    }
    
    results_path = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/schedule_results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved")

if __name__ == "__main__":
    main()
