#!/usr/bin/env python3
"""
PostBridge Upload Remaining Untouched Posts - Autonomous
Uploads remaining untouched posts (skip first 100 already uploaded today)
"""

import json
import requests
from datetime import datetime, timedelta

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

LOG_FILE = "/home/openclaw/.openclaw/workspace/logs/postbridge_upload_log.txt"
QUEUE_FILE = "/home/openclaw/.openclaw/workspace/postbridge_queue_jendralbot.json"
UNTCHED_LOG = "/home/openclaw/.openclaw/workspace/logs/postbridge_untouched_upload_log.json"
REMAINING_LOG = "/home/openclaw/.openclaw/workspace/logs/postbridge_remaining_upload_log.json"

INSTAGRAM_ACCOUNT = "47681"

def load_queue():
    with open(QUEUE_FILE, 'r') as f:
        data = json.load(f)
        return data.get('posts', [])

def get_attempted_headlines():
    attempted = set()
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                entry = json.loads(line)
                headline = entry.get('headline')
                if headline:
                    attempted.add(headline)
    except:
        pass
    return attempted

def get_todays_uploaded():
    uploaded = set()
    try:
        with open(UNTCHED_LOG, 'r') as f:
            data = json.load(f)
            for r in data.get('results', []):
                if r.get('status') == 'success':
                    headline = r.get('headline')
                    if headline:
                        uploaded.add(headline)
    except:
        pass
    return uploaded

def find_remaining_posts(queue, attempted, todays_uploaded):
    remaining = []
    for post in queue:
        headline = post.get('metadata', {}).get('headline')

        # Skip if already attempted OR uploaded today
        if headline in attempted or headline in todays_uploaded:
            continue

        remaining.append(post)

    return remaining

def upload_posts(posts, max_count=100):
    results = []
    
    # Start scheduling tomorrow at 11:30 (after retry batch)
    start_time = datetime.now() + timedelta(days=1)
    start_time = start_time.replace(hour=11, minute=30, second=0, microsecond=0)

    interval_minutes = 5

    print(f"🚀 Uploading {len(posts)} remaining posts...")
    print(f"📅 Starting: {start_time.strftime('%Y-%m-%d %H:%M UTC+7')}")
    print(f"⏱️  Interval: {interval_minutes} minutes")
    print("-" * 70)

    for i, post in enumerate(posts, 1):
        schedule_time = start_time + timedelta(minutes=i * interval_minutes)

        payload = {
            'caption': post.get('content', {}).get('caption', ''),
            'social_accounts': [INSTAGRAM_ACCOUNT],
            'media': [],
            'scheduled_at': schedule_time.strftime('%Y-%m-%dT%H:%M:%S')
        }

        try:
            response = requests.post(
                f"{BASE_URL}/posts",
                headers={
                    'Authorization': f'Bearer {API_KEY}',
                    'Content-Type': 'application/json'
                },
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 201]:
                result = response.json()
                headline = post.get('metadata', {}).get('headline', '')
                print(f"✅ {i:3d}/{len(posts)} | {headline[:40]:40s} | {schedule_time.strftime('%H:%M')}")
                results.append({
                    'product': post.get('metadata', {}).get('product'),
                    'headline': headline,
                    'scheduled_time': schedule_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'post_id': result.get('id'),
                    'status': 'success'
                })
            else:
                print(f"❌ {i:3d}/{len(posts)} | HTTP {response.status_code}")
                results.append({
                    'product': post.get('metadata', {}).get('product'),
                    'headline': post.get('metadata', {}).get('headline'),
                    'error': f"HTTP {response.status_code}",
                    'status': 'failed'
                })

        except Exception as e:
            print(f"❌ {i:3d}/{len(posts)} | {str(e)[:30]}")
            results.append({
                'product': post.get('metadata', {}).get('product'),
                'headline': post.get('metadata', {}).get('headline'),
                'error': str(e),
                'status': 'exception'
            })

    return results

def main():
    print("="*70)
    print("PostBridge Remaining Posts Upload - Autonomous")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()

    # Load data
    queue = load_queue()
    attempted = get_attempted_headlines()
    todays_uploaded = get_todays_uploaded()

    print(f"✅ Queue posts: {len(queue)}")
    print(f"📊 Attempted (log): {len(attempted)}")
    print(f"✅ Uploaded today: {len(todays_uploaded)}")
    print()

    # Find remaining
    remaining = find_remaining_posts(queue, attempted, todays_uploaded)
    print(f"🆕 Remaining untouched: {len(remaining)}")
    print()

    if len(remaining) == 0:
        print("✅ All posts processed.")
        return

    # Upload limited batch
    results = upload_posts(remaining, max_count=100)

    # Save
    upload_data = {
        'upload_timestamp': datetime.now().isoformat(),
        'total_remaining': len(remaining),
        'posts_uploaded': len(results),
        'successful': sum(1 for r in results if r['status'] == 'success'),
        'failed': sum(1 for r in results if r['status'] != 'success'),
        'results': results
    }

    with open(REMAINING_LOG, 'w') as f:
        json.dump(upload_data, f, indent=2)

    # Summary
    print()
    print("="*70)
    print("AUTONOMOUS EXECUTION COMPLETE")
    print("="*70)
    print(f"Total Remaining: {len(remaining)}")
    print(f"Uploaded This Batch: {len(results)}")
    print(f"✅ Successful: {upload_data['successful']}")
    print(f"❌ Failed: {upload_data['failed']}")
    print(f"📄 Log: {REMAINING_LOG}")
    print(f"📅 Schedule: Starting March 9, 11:35 UTC+7")
    print("="*70)

    return upload_data

if __name__ == "__main__":
    main()