#!/usr/bin/env python3
"""
JENDRALBOT Post Bridge Auto Upload
Upload queue to Instagram & Facebook via Post Bridge
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
import time

workspace = os.path.expanduser("~/.openclaw/workspace")

# Configuration
QUEUE_FILE = os.path.join(workspace, "postbridge_queue_jendralbot.json")
LOG_FILE = os.path.join(workspace, "logs/postbridge_upload_log.txt")
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

ACCOUNT_IDS = {
    'instagram': '47681',  # berkahkaryadigitalproduct
    'facebook': '47664'
}

def load_queue():
    """Load Post Bridge queue"""
    path = Path(QUEUE_FILE)
    
    if not path.exists():
        print(f"❌ Queue file not found: {QUEUE_FILE}")
        return []
    
    with open(path) as f:
        queue_data = json.load(f)
    
    print(f"✅ Loaded queue: {queue_data['campaign_name']}")
    print(f"   Total posts: {queue_data['total_posts']}")
    print(f"   Platforms: {', '.join(queue_data['platforms'])}")
    
    return queue_data['posts']

def log_upload(item, result):
    """Log upload result"""
    with open(LOG_FILE, 'a') as f:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": item['platform'],
            "product": item['metadata']['product'],
            "headline": item['metadata']['headline'][:50],
            "scheduled": item['schedule']['publish_at'],
            "result": result
        }
        f.write(json.dumps(log_entry) + '\n')

def upload_post(item):
    """Upload single post via Post Bridge API"""
    platform = item['platform']
    account_id = ACCOUNT_IDS.get(platform)
    
    if not account_id:
        return {
            'success': False,
            'error': f"No account ID for {platform}"
        }
    
    # Build caption
    caption = item['content']['caption']
    hashtags = item['content'].get('hashtag', [])
    
    # Combine caption and hashtags
    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
    
    # PostBridge payload
    payload = {
        'caption': full_caption,
        'social_accounts': [account_id],
        'scheduled_at': item['schedule']['publish_at'],
        'time_zone': item['schedule']['time_zone'],
        'media': []
    }
    
    try:
        print(f"\n📤 Uploading to {platform.upper()}...")
        print(f"   Product: {item['metadata']['product']}")
        print(f"   Account ID: {account_id}")
        print(f"   Headline: {item['metadata']['headline'][:50]}...")
        print(f"   Scheduled: {item['schedule']['publish_at']}")
        
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
            post_id = result.get('id', 'N/A')
            print(f"   ✅ Success! Post ID: {post_id}")
            
            log_result = {
                'success': True,
                'platform': platform,
                'post_id': post_id,
                'account_id': account_id,
                'scheduled': item['schedule']['publish_at'],
                'response': result
            }
        else:
            print(f"   ❌ HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
            log_result = {
                'success': False,
                'platform': platform,
                'error': f"HTTP {response.status_code}: {response.text[:200]}"
            }
        
        return log_result
    
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        
        return {
            'success': False,
            'platform': platform,
            'error': str(e)
        }

def run_upload(queue, batch_size=10):
    """Run upload batch"""
    print(f"\n{'='*70}")
    print("JENDRALBOT - Post Bridge Auto Upload")
    print(f"{'='*70}")
    print(f"\nBatch size: {batch_size}")
    print(f"Queue length: {len(queue)}")
    print()
    
    successful = 0
    failed = 0
    
    # Process first batch
    batch = queue[:batch_size]
    
    print(f"Processing first {len(batch)} posts...\n")
    
    for i, item in enumerate(batch, 1):
        # Wait 1 second between posts
        if i > 1:
            time.sleep(1)
        
        result = upload_post(item)
        log_upload(item, result)
        
        if result['success']:
            successful += 1
        else:
            failed += 1
        
        print(f"[{i}/{len(batch)}] {'✅' if result['success'] else '❌'} {item['platform']} - {item['metadata']['product']}")
    
    print(f"\n{'='*70}")
    print("UPLOAD SUMMARY")
    print(f"{'='*70}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(batch)}")
    print(f"\n📊 Log file: {LOG_FILE}")
    print(f"\n🔗 Monitor LYNK dashboard: https://lynk.id/jendralbot")
    print("\n🎉 Upload batch complete!")
    print(f"📤 Remaining posts: {len(queue) - batch_size}")

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JENDRALBOT Post Bridge Auto Upload')
    parser.add_argument('--batch', type=int, default=10, help='Posts per batch (default: 10)')
    parser.add_argument('--platform', type=str, choices=['instagram', 'facebook'], help='Filter by platform')
    
    args = parser.parse_args()
    
    # Load queue
    queue = load_queue()
    
    if not queue:
        return
    
    # Filter by platform if specified
    if args.platform:
        queue = [item for item in queue if item['platform'] == args.platform]
        print(f"Filtered to {len(queue)} {args.platform} posts")
    
    # Run upload
    run_upload(queue, batch_size=args.batch)

if __name__ == "__main__":
    main()