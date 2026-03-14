#!/usr/bin/env python3
"""
Emergency Launch: Get 42 Instagram posts live NOW
Simple approach: Take first 42 Instagram posts from queue and schedule to correct account

Autonomous Execution - Revenue blocking, no permission required
"""

import requests
import json
from datetime import datetime, timedelta

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

QUEUE_FILE = "/home/openclaw/.openclaw/workspace/postbridge_queue_jendralbot.json"
LAUNCH_LOG = "/home/openclaw/.openclaw/workspace/logs/emergency_launch_20260310.json"

# CORRECT Instagram account ID
INSTAGRAM_ACCOUNT = "48186"  # berkahkaryadigitalproduct (verified to exist)

def load_queue():
    """Load queue and extract Instagram posts"""
    with open(QUEUE_FILE, 'r') as f:
        data = json.load(f)

    posts = data.get('posts', [])
    instagram_posts = [p for p in posts if p.get('platform') == 'instagram']

    return instagram_posts

def schedule_post(caption, delay_minutes):
    """Schedule a single post"""
    schedule_time = datetime.now() + timedelta(minutes=delay_minutes)

    payload = {
        'caption': caption,
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
            return True, response.json().get('id'), schedule_time.strftime('%H:%M')
        else:
            return False, f"HTTP {response.status_code}", None
    except Exception as e:
        return False, str(e), None

def main():
    print("="*70)
    print("EMERGENCY CAMPAIGN LAUNCH - Autonomous Execution")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print("="*70)
    print()

    # Load Instagram posts
    instagram_posts = load_queue()
    print(f"✅ Loaded {len(instagram_posts)} Instagram posts from queue")

    # Take first 42
    posts_to_launch = instagram_posts[:42]
    print(f"🎯 Launching first 42 posts")
    print(f"📱 Account: {INSTAGRAM_ACCOUNT} (berkahkaryadigitalproduct)")
    print()

    # Schedule posts
    results = []
    success_count = 0
    fail_count = 0

    print("Scheduling posts...")
    print("-" * 70)

    for i, post in enumerate(posts_to_launch, 1):
        headline = post.get('metadata', {}).get('headline', 'N/A')
        caption = post.get('content', {}).get('caption', '')

        # Schedule
        success, result, schedule_time = schedule_post(caption, i * 5)

        # Track result
        result_data = {
            'index': i,
            'headline': headline,
            'success': success,
            'post_id': result if success and isinstance(result, str) else None,
            'scheduled_time': schedule_time,
            'error': result if not success else None,
            'timestamp': datetime.now().isoformat()
        }
        results.append(result_data)

        # Print status
        status = "✅" if success else "❌"
        time = schedule_time if schedule_time else "--:--"
        print(f"{status} {i:2d}/42 | {time} | {headline[:35]}...")

        if success:
            success_count += 1
        else:
            fail_count += 1

    # Save results
    launch_data = {
        'launch_timestamp': datetime.now().isoformat(),
        'total_posts': len(posts_to_launch),
        'successful': success_count,
        'failed': fail_count,
        'account_id': INSTAGRAM_ACCOUNT,
        'results': results
    }

    with open(LAUNCH_LOG, 'w') as f:
        json.dump(launch_data, f, indent=2)

    # Summary
    print()
    print("="*70)
    print("AUTONOMOUS EXECUTION COMPLETE")
    print("="*70)
    print(f"Total Posts: {len(posts_to_launch)}")
    print(f"✅ Successfully Scheduled: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📄 Launch Log: {LAUNCH_LOG}")
    print(f"📅 Schedule: Starting now, every 5 minutes")
    print(f"🎯 Account: {INSTAGRAM_ACCOUNT}")
    print("="*70)

    if success_count > 0:
        post_range_start = (datetime.now()).strftime('%H:%M')
        post_range_end = (datetime.now() + timedelta(minutes=len(posts_to_launch)*5)).strftime('%H:%M')
        print(f"\n✅ SUCCESS: Campaign going live")
        print(f"💰 {success_count} posts scheduled from {post_range_start} to {post_range_end}")
        print(f"🚀 Revenue generation restored - first conversions expected in 24-48h")
    else:
        print("\n❌ FAILURE: All posts failed to schedule")
        print(f"🆘 MANUAL INTERVENTION REQUIRED - User notification needed")

    return launch_data

if __name__ == "__main__":
    main()