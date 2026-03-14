#!/usr/bin/env python3
"""
PostBridge Untouched Posts Upload - Autonomous
Uploads posts that were never attempted (not in log file)
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

LOG_FILE = "/home/openclaw/.openclaw/workspace/logs/postbridge_upload_log.txt"
QUEUE_FILE = "/home/openclaw/.openclaw/workspace/postbridge_queue_jendralbot.json"
UPLOAD_LOG = "/home/openclaw/.openclaw/workspace/logs/postbridge_untouched_upload_log.json"

# Instagram account ID
INSTAGRAM_ACCOUNT = "47681"

def load_original_queue():
    """Load original post queue"""
    with open(QUEUE_FILE, 'r') as f:
        data = json.load(f)
        return data.get('posts', [])

def get_attempted_posts():
    """Get list of posts that were attempted (success or failed)"""
    attempted = []

    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    # Add to attempted if it has result (success or error)
                    if 'result' in data:
                        headline = data.get('headline')
                        platform = data.get('platform')
                        product = data.get('product')
                        attempted.append({
                            'headline': headline,
                            'platform': platform,
                            'product': product
                        })
                except:
                    continue
    except:
        pass

    return attempted

def find_untouched_posts(queue, attempted):
    """Find posts that were never attempted"""
    untouched = []

    for post in queue:
        post_headline = post.get('metadata', {}).get('headline')
        post_platform = post.get('platform')
        post_product = post.get('metadata', {}).get('product')

        # Check if this post was attempted
        is_attempted = False
        for att in attempted:
            if (att['headline'] == post_headline and 
                att['platform'] == post_platform and 
                att['product'] == post_product):
                is_attempted = True
                break

        if not is_attempted:
            untouched.append(post)

    return untouched

def upload_untouched_posts(posts, max_count=100):
    """Upload untouched posts to PostBridge"""
    results = []
    
    # Limit to max_count posts (to avoid overwhelming)
    posts = posts[:max_count]

    # Start scheduling this evening at 6 PM
    start_time = datetime.now() + timedelta(hours=1)
    start_time = start_time.replace(hour=18, minute=0, second=0, microsecond=0)

    # If it's already past 6 PM, start at next 5-minute interval
    if datetime.now().hour >= 18:
        start_time = datetime.now() + timedelta(minutes=5)
        start_time = start_time.replace(second=0, microsecond=0)

    # Space posts every 5 minutes
    interval_minutes = 5

    print(f"🚀 Uploading {len(posts)} untouched posts...")
    print(f"📅 Starting: {start_time.strftime('%Y-%m-%d %H:%M UTC+7')}")
    print(f"⏱️  Interval: {interval_minutes} minutes")
    print("-" * 70)

    for i, post in enumerate(posts, 1):
        # Calculate schedule time
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
    print("PostBridge Untouched Posts Upload - Autonomous Execution")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()

    # Load queue
    try:
        queue = load_original_queue()
        print(f"✅ Loaded queue: {len(queue)} posts")
    except Exception as e:
        print(f"❌ Error loading queue: {e}")
        return

    # Get attempted posts
    attempted = get_attempted_posts()
    print(f"📊 Posts attempted: {len(attempted)}")

    # Find untouched posts
    untouched = find_untouched_posts(queue, attempted)
    print(f"🆕 Posts untouched: {len(untouched)}")
    print()

    if len(untouched) == 0:
        print("✅ All posts have been attempted.")
        return

    # Upload untouched posts
    results = upload_untouched_posts(untouched, max_count=100)

    # Save results
    upload_data = {
        'upload_timestamp': datetime.now().isoformat(),
        'total_untouched': len(untouched),
        'posts_uploaded': len(results),
        'successful_uploads': sum(1 for r in results if r['status'] == 'success'),
        'failed_uploads': sum(1 for r in results if r['status'] != 'success'),
        'results': results
    }

    with open(UPLOAD_LOG, 'w') as f:
        json.dump(upload_data, f, indent=2)

    # Summary
    print()
    print("="*70)
    print("AUTONOMOUS EXECUTION COMPLETE")
    print("="*70)
    print(f"Total Untouched Found: {len(untouched)}")
    print(f"Posts Uploaded: {len(results)}")
    print(f"✅ Successfully Scheduled: {upload_data['successful_uploads']}")
    print(f"❌ Failed: {upload_data['failed_uploads']}")
    print(f"📄 Upload Log: {UPLOAD_LOG}")
    print(f"📅 New Schedule: Starting TODAY 18:00 UTC+7")
    print("="*70)

    return upload_data

if __name__ == "__main__":
    main()