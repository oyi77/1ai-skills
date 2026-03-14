#!/usr/bin/env python3
"""
JENDRALBOT Post Bridge Auto Upload - Facebook Phase
Upload queue to Facebook via Post Bridge
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
import time

workspace = os.path.expanduser("~/.openclaw/workspace")

# Facebook account ID
FACEBOOK_ACCOUNT_ID = "47664"  # From auto_postbridge_v2.py

# Configuration
QUEUE_FILE = os.path.join(workspace, "postbridge_queue_jendralbot.json")
LOG_FILE = os.path.join(workspace, "logs/postbridge_facebook_log.txt")
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

def load_facebook_queue():
    """Load Facebook-only posts from queue"""
    path = Path(QUEUE_FILE)
    
    if not path.exists():
        print(f"❌ Queue file not found: {QUEUE_FILE}")
        return []
    
    with open(path) as f:
        queue_data = json.load(f)
    
    # Filter only Facebook posts
    facebook_posts = [item for item in queue_data['posts'] if item['platform'] == 'facebook']
    
    print(f"✅ Loaded Facebook queue")
    print(f"   Total Facebook posts: {len(facebook_posts)}")
    
    return facebook_posts

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

def upload_facebook_post(item):
    """Upload single Facebook post via Post Bridge API"""
    platform = item['platform']
    
    # Build caption
    caption = item['content']['caption']
    hashtags = item['content'].get('hashtag', [])
    
    # Combine caption and hashtags
    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
    
    # PostBridge payload for Facebook
    payload = {
        'caption': full_caption,
        'social_accounts': [FACEBOOK_ACCOUNT_ID],
        'scheduled_at': item['schedule']['publish_at'],
        'time_zone': item['schedule']['time_zone'],
        'media': []
    }
    
    try:
        print(f"\n📤 Uploading to FACEBOOK...")
        print(f"   Account ID: {FACEBOOK_ACCOUNT_ID}")
        print(f"   Product: {item['metadata']['product']}")
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
                'account_id': FACEBOOK_ACCOUNT_ID,
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

def run_facebook_upload(queue, batch_size=20):
    """Run Facebook upload batch"""
    print(f"\n{'='*70}")
    print("JENDRALBOT - Facebook Post Bridge Auto Upload")
    print(f"{'='*70}")
    print(f"\nBatch size: {batch_size}")
    print(f"Facebook posts ready: {len(queue)}")
    print()
    
    successful = 0
    failed = 0
    
    # Process batch
    batch = queue[:batch_size]
    
    print(f"Processing first {len(batch)} Facebook posts...\n")
    
    for i, item in enumerate(batch, 1):
        # Wait 2 seconds between Facebook posts
        if i > 1:
            time.sleep(2)
        
        result = upload_facebook_post(item)
        log_upload(item, result)
        
        if result['success']:
            successful += 1
        else:
            failed += 1
        
        print(f"[{i}/{len(batch)}] {'✅' if result['success'] else '❌'} Facebook - {item['metadata']['product']}")
    
    print(f"\n{'='*70}")
    print("UPLOAD SUMMARY")
    print(f"{'='*70}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {len(batch)}")
    print(f"\n📊 Log file: {LOG_FILE}")
    print(f"\n🎉 Facebook upload batch complete!")
    print(f"📤 Remaining Facebook posts: {len(queue) - batch_size}")

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JENDRALBOT Facebook Auto Upload')
    parser.add_argument('--batch', type=int, default=20, help='Posts per batch (default: 20)')
    
    args = parser.parse_args()
    
    # Load Facebook queue
    queue = load_facebook_queue()
    
    if not queue:
        print("No Facebook posts in queue")
        return
    
    # Run upload
    run_facebook_upload(queue, batch_size=args.batch)

if __name__ == "__main__":
    main()