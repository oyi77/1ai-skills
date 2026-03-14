#!/usr/bin/env python3
"""
PostBridge Failed Posts Retry - Autonomous
Reschedules all failed posts based on error logs and original queue
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

LOG_FILE = "/home/openclaw/.openclaw/workspace/logs/postbridge_upload_log.txt"
QUEUE_FILE = "/home/openclaw/.openclaw/workspace/postbridge_queue_jendralbot.json"
RETRY_LOG = "/home/openclaw/.openclaw/workspace/logs/postbridge_retry_log.json"

# Instagram account ID
INSTAGRAM_ACCOUNT = "47681"

def load_original_queue():
    """Load original post queue with full captions"""
    with open(QUEUE_FILE, 'r') as f:
        data = json.load(f)
        return data.get('posts', [])

def get_failed_posts_from_logs():
    """Extract failed posts from upload log"""
    failed_posts = []

    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'error' in data.get('result', {}) and '500' in data['result']['error']:
                    failed_posts.append(data)
            except:
                continue

    return failed_posts

def match_failed_to_original(failed_posts, queue):
    """Match failed posts to original queue entries to get captions"""
    matched = []

    for failed in failed_posts:
        # Find matching post in queue by product, headline
        for queue_item in queue:
            q_prod = queue_item.get('metadata', {}).get('product')
            q_head = queue_item.get('metadata', {}).get('headline')
            q_plat = queue_item.get('platform')

            f_prod = failed.get('product')
            f_head = failed.get('headline')
            f_plat = failed.get('platform')

            if (q_plat == f_plat and q_prod == f_prod and q_head == f_head):
                matched.append({
                    'timestamp': failed['timestamp'],
                    'platform': failed['platform'],
                    'product': failed['product'],
                    'headline': failed['headline'],
                    'original_scheduled': failed['scheduled'],
                    'caption': queue_item.get('content', {}).get('caption', '')
                })
                break

    return matched

def reschedule_failed_posts(posts_to_retry):
    """Retry all failed posts with new schedule times"""
    results = []

    # Start scheduling tomorrow at 8 AM
    start_time = datetime.now() + timedelta(days=1)
    start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)

    # Space posts every 5 minutes
    interval_minutes = 5

    print(f"🔁 Retrying {len(posts_to_retry)} failed posts...")
    print(f"📅 Starting: {start_time.strftime('%Y-%m-%d %H:%M UTC+7')}")
    print(f"⏱️  Interval: {interval_minutes} minutes")
    print("-" * 70)

    for i, post in enumerate(posts_to_retry, 1):
        # Calculate new schedule time
        schedule_time = start_time + timedelta(minutes=i * interval_minutes)

        payload = {
            'caption': post['caption'],
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
                print(f"✅ {i:2d}/{len(posts_to_retry)} | {post['headline'][:40]:40s} | {schedule_time.strftime('%H:%M')}")
                results.append({
                    'original_error_time': post['timestamp'],
                    'original_headline': post['headline'],
                    'rescheduled_time': schedule_time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'post_id': result.get('id'),
                    'status': 'success'
                })
            else:
                print(f"❌ {i:2d}/{len(posts_to_retry)} | HTTP {response.status_code}")
                results.append({
                    'original_error_time': post['timestamp'],
                    'original_headline': post['headline'],
                    'error': f"HTTP {response.status_code}: {response.text[:100]}",
                    'status': 'failed'
                })

        except Exception as e:
            print(f"❌ {i:2d}/{len(posts_to_retry)} | Exception: {str(e)[:50]}")
            results.append({
                'original_error_time': post['timestamp'],
                'original_headline': post['headline'],
                'error': str(e),
                'status': 'exception'
            })

    return results

def main():
    print("="*70)
    print("PostBridge Failed Posts Retry - Autonomous Execution")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()

    # Load original queue
    try:
        queue = load_original_queue()
        print(f"✅ Loaded original queue: {len(queue)} posts")
        print()
    except Exception as e:
        print(f"❌ Error loading queue: {e}")
        return

    # Extract failed posts
    failed_posts = get_failed_posts_from_logs()
    print(f"📊 Found {len(failed_posts)} failed posts in log")

    if not failed_posts:
        print("✅ No failed posts found.")
        return

    # Match failed posts to original queue
    posts_to_retry = match_failed_to_original(failed_posts, queue)
    print(f"🔄 Matched {len(posts_to_retry)} posts with captions")

    if len(posts_to_retry) == 0:
        print("⚠️  No matches found in original queue")
        return

    print()

    # Retry all failed posts
    results = reschedule_failed_posts(posts_to_retry)

    # Save results
    retry_data = {
        'retry_timestamp': datetime.now().isoformat(),
        'total_failed': len(failed_posts),
        'total_matched': len(posts_to_retry),
        'successful_retries': sum(1 for r in results if r['status'] == 'success'),
        'failed_retries': sum(1 for r in results if r['status'] != 'success'),
        'results': results
    }

    with open(RETRY_LOG, 'w') as f:
        json.dump(retry_data, f, indent=2)

    # Summary
    print()
    print("="*70)
    print("AUTONOMOUS EXECUTION COMPLETE")
    print("="*70)
    print(f"Total Posts Found: {len(failed_posts)}")
    print(f"Posts Matched: {len(posts_to_retry)}")
    print(f"✅ Successfully Rescheduled: {retry_data['successful_retries']}")
    print(f"❌ Still Failed: {retry_data['failed_retries']}")
    print(f"📄 Retry Log: {RETRY_LOG}")
    print(f"📅 New Schedule: Starting March 9, 8:00 AM UTC+7")
    print("="*70)

    return retry_data

if __name__ == "__main__":
    main()