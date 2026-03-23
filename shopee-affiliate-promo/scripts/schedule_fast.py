#!/usr/bin/env python3
"""PostBridge Fast Scheduler with retry logic"""

import json
import requests
import time
from datetime import datetime, timedelta, timezone
import os

API_BASE = "https://api.post-bridge.com/v1"
API_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def load_data():
    base = os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/")
    with open(base + "postbridge_accounts.json") as f:
        accounts = json.load(f)
    with open(base + "posting_schedule.json") as f:
        posts = json.load(f)
    return accounts, posts

def schedule_post(acc_id, caption, scheduled_at, retries=3):
    payload = {
        "caption": caption,
        "scheduled_at": scheduled_at,
        "social_accounts": [acc_id]
    }
    
    for attempt in range(retries):
        try:
            resp = requests.post(f"{API_BASE}/posts", headers=HEADERS, json=payload, timeout=30)
            if resp.status_code in [200, 201]:
                return True, None
            elif resp.status_code == 500 and attempt < retries - 1:
                time.sleep(1)  # Wait before retry
                continue
            else:
                return False, f"{resp.status_code}: {resp.text[:50]}"
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return False, str(e)[:50]
    return False, "Max retries"

def main():
    print("🚀 PostBridge Fast Scheduler")
    print("=" * 50)
    
    accounts, posts = load_data()
    valid_ids = {a['id'] for a in accounts}
    text_platforms = ['facebook', 'threads', 'tiktok', 'twitter', 'linkedin', 'youtube']
    
    # Filter valid posts
    valid_posts = [p for p in posts if p.get('account_id') in valid_ids and p.get('platform') in text_platforms]
    print(f"📝 {len(valid_posts)} posts to schedule")
    
    # Group by account
    by_account = {}
    for p in valid_posts:
        aid = p['account_id']
        if aid not in by_account:
            by_account[aid] = []
        by_account[aid].append(p)
    
    print(f"📱 {len(by_account)} accounts")
    
    # Schedule
    start = datetime.now(timezone.utc) + timedelta(minutes=30)
    ok = 0
    fail = 0
    
    for acc_id, acc_posts in by_account.items():
        for i, post in enumerate(acc_posts):
            day = i // 3
            slot = i % 3
            post_time = start + timedelta(days=day, hours=slot * 8)
            scheduled_at = post_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            
            success, err = schedule_post(acc_id, post['caption'], scheduled_at)
            
            if success:
                ok += 1
                if ok % 50 == 0:
                    print(f"✅ {ok} scheduled...")
            else:
                fail += 1
                if fail <= 5:
                    print(f"❌ {err}")
            
            time.sleep(0.2)  # Rate limit
    
    print(f"\n{'=' * 50}")
    print(f"✅ Scheduled: {ok}")
    print(f"❌ Failed: {fail}")
    
    # Save result
    with open(os.path.expanduser("~/.openclaw/workspace/skills/shopee-affiliate-promo/data/schedule_results.json"), 'w') as f:
        json.dump({"ok": ok, "fail": fail, "time": datetime.now().isoformat()}, f)

if __name__ == "__main__":
    main()
