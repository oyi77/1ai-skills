#!/usr/bin/env python3
"""
JENDRALBOT Post Bridge Auto Upload - Rate Limit Prevention
Intelligent upload system with rate limiting, retry logic, and staggered scheduling
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import time
import random

workspace = os.path.expanduser("~/.openclaw/workspace")

# Account IDs
ACCOUNT_IDS = {
    'instagram': '47681',
    'facebook': '47664'
}

# Configuration
QUEUE_FILE = os.path.join(workspace, "postbridge_queue_jendralbot.json")
LOG_FILE = os.path.join(workspace, "logs/rate_limit_aware_upload.log")
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

# Rate Limiting Settings
MIN_DELAY_SECONDS = 60      # Minimum 1 minute between uploads
MAX_DELAY_SECONDS = 300     # Maximum 5 minutes between uploads
RETRY_DELAY_BASE = 600      # 10 minutes base retry delay
MAX_RETRIES = 3             # Maximum retries per post

class RateLimitAwareUploader:
    """Smart uploader with rate limit prevention"""
    
    def __init__(self):
        print(f"\n🚀 Initializing Rate Limit Aware Uploader")
        self.log_file = open(LOG_FILE, 'a')
    
    def log(self, message):
        """Log to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        self.log_file.write(json.dumps(log_entry) + '\n')
        self.log_file.flush()
    
    def calculate_upload_delay(self, post_index, platform):
        """
        Calculate adaptive delay between uploads to prevent rate limiting
        
        Strategy:
        - Exponential backoff based on post number
        - Random jitter to avoid patterns
        - Longer delays for Facebook (more strict)
        """
        
        base_delay = MIN_DELAY_SECONDS
        
        # Add exponential component based on position
        post_delay_multiplier = min(post_index * 0.1, 5)  # Max 5x multiplier
        
        # Different delays per platform
        platform_multiplier = 2.0 if platform == 'facebook' else 1.0
        
        # Add random jitter (±20%)
        jitter = random.uniform(0.8, 1.2)
        
        delay = base_delay * post_delay_multiplier * platform_multiplier * jitter
        
        # Cap at max delay
        delay = min(delay, MAX_DELAY_SECONDS)
        
        return int(delay)
    
    def load_uploads_pending(self):
        """Load posts that still need uploading"""
        file_path = Path(LOG_FILE)
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                logs = [json.loads(line) for line in f.readlines()]
            
            # Extract successful post IDs
            successful_post_ids = set()
            for log in logs:
                if 'post_id' in log.get('message_obj', {}):
                    successful_post_ids.add(log['message_obj']['post_id'])
            
            print(f"✅ Loaded {len(logs)} previous logs")
            print(f"   Successful uploads: {len(successful_post_ids)}")
            
            return successful_post_ids
        
        return set()
    
    def rate_limit_check(self):
        """Check if we should pause for rate limit"""
        file_path = Path(LOG_FILE)
        
        if file_path.exists():
            with open(file_path, 'r') as f:
                logs = [json.loads(line) for line in f.readlines()]
            
            # Count recent failures (last 10 uploads)
            recent_logs = logs[-10:] if len(logs) >= 10 else logs
            recent_failures = sum(1 for log in recent_logs 
                                if 'error' in log.get('message_obj', {})
                                and 'HTTP 500' in log.get('message_obj', {}).get('error', ''))
            
            # If 3+ recent failures, pause
            if recent_failures >= 3:
                pause_time = 900  # 15 minutes
                print(f"\n⚠️  {recent_failures} recent failures detected")
                print(f"⏸️  Pausing for {pause_time} seconds ({pause_time/60:.1f} minutes)")
                print(f"   This prevents rate limit")
                time.sleep(pause_time)
    
    def upload_with_retry(self, item, successful_post_ids):
        """Upload with retry logic and rate limit detection"""
        platform = item['platform']
        account_id = ACCOUNT_IDS.get(platform)
        headline = item['metadata']['headline']
        
        # Check rate limit before uploading
        self.rate_limit_check()
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # Calculate delay
                delay = self.calculate_upload_delay(len(successful_post_ids), platform)
                
                print(f"\n[Attempt {attempt}/{MAX_RETRIES}]")
                print(f"📤 Uploading to {platform.upper()}...")
                print(f"   Headline: {headline[:50]}...")
                print(f"   Delay: {delay}s")
                print(f"   Waiting...", end='', flush=True)
                
                # Wait before upload
                time.sleep(delay)
                print(f" ✅")
                
                # Build caption
                caption = item['content']['caption']
                hashtags = item['content'].get('hashtag', [])
                full_caption = f"{caption}\n\n{' '.join(hashtags)}"
                
                # Upload
                payload = {
                    'caption': full_caption,
                    'social_accounts': [account_id],
                    'scheduled_at': item['schedule']['publish_at'],
                    'time_zone': item['schedule']['time_zone'],
                    'media': []
                }
                
                response = requests.post(
                    f"{BASE_URL}/posts",
                    headers={
                        'Authorization': f'Bearer {API_KEY}',
                        'Content-Type': 'application/json'
                    },
                    json=payload,
                    timeout=60  # Longer timeout
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    post_id = result.get('id', 'N/A')
                    print(f"   ✅ Success! Post ID: {post_id}")
                    
                    self.log({
                        "platform": platform,
                        "post_id": post_id,
                        "headline": headline[:50],
                        "attempt": attempt,
                        "status": "SUCCESS",
                        "scheduled": item['schedule']['publish_at']
                    })
                    
                    return {
                        'success': True,
                        'post_id': post_id,
                        'attempt': attempt
                    }
                
                elif response.status_code == 500:
                    # Rate limit / server error
                    print(f"   ⚠️  HTTP 500 - Rate limit likely")
                    print(f"   Will retry in {RETRY_DELAY_BASE * attempt}s")
                    
                    self.log({
                        "platform": platform,
                        "headline": headline[:50],
                        "attempt": attempt,
                        "status": "RATE_LIMIT",
                        "error": f"HTTP 500"
                    })
                    
                    if attempt < MAX_RETRIES:
                        # Exponential backoff for retry
                        retry_delay = RETRY_DELAY_BASE * attempt
                        print(f"   ⏳  Retrying in {retry_delay}s ({retry_delay/60:.1f} min)")
                        time.sleep(retry_delay)
                        continue
                    else:
                        return {
                            'success': False,
                            'error': f"Max retries ({MAX_RETRIES}) reached"
                        }
                
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    print(f"   Response: {response.text}")
                    
                    return {
                        'success': False,
                        'error': f"HTTP {response.status_code}"
                    }
            
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                
                self.log({
                    "platform": platform,
                    "headline": headline[:50],
                    "attempt": attempt,
                    "status": "ERROR",
                    "error": str(e)
                })
                
                if attempt < MAX_RETRIES:
                    retry_delay = RETRY_DELAY_BASE * attempt
                    print(f"   ⏳  Retrying in {retry_delay}s")
                    time.sleep(retry_delay)
                    continue
                else:
                    return {
                        'success': False,
                        'error': str(e)
                    }

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Rate Limit Aware Poster')
    parser.add_argument('--platform', type=str, choices=['instagram', 'facebook'], 
                        help='Platform to upload', required=True)
    parser.add_argument('--batch', type=int, default=10, 
                        help='Posts per batch (default: 10)')
    
    args = parser.parse_args()
    
    print("="*70)
    print("JENDRALBOT - Rate Limit Aware Upload")
    print("Prevents HTTP 500 rate limit errors")
    print("="*70)
    
    # Initialize uploader
    uploader = RateLimitAwareUploader()
    
    # Load queue
    path = Path(QUEUE_FILE)
    with open(path) as f:
        queue_data = json.load(f)
    
    # Filter by platform
    platform_queue = [item for item in queue_data['posts'] if item['platform'] == args.platform]
    
    print(f"\nPlatform: {args.platform.upper()}")
    print(f"Total posts in queue: {len(platform_queue)}")
    print(f"Batch size: {args.batch}")
    print()
    
    # Load successful uploads
    successful_post_ids = uploader.load_uploads_pending()
    
    # Filter out already successful uploads
    pending = [item for item in platform_queue 
                if item.get('post_id') not in successful_post_ids]
    
    print(f"Pending uploads: {len(pending)}")
    
    if not pending:
        print(f"\n✅ All posts already uploaded!")
        return
    
    # Process batch
    batch = pending[:args.batch]
    successful = 0
    failed = 0
    
    print(f"\nProcessing {len(batch)} posts...")
    print("-"*70)
    
    for i, item in enumerate(batch, 1):
        result = uploader.upload_with_retry(item, successful_post_ids)
        
        if result['success']:
            successful += 1
            successful_post_ids.add(result['post_id'])
        else:
            failed += 1
        
        print(f"[{i}/{len(batch)}]{'✅' if result['success'] else '❌'}")
        
        # Progress update every 5 posts
        if i % 5 == 0:
            print(f"\nProgress: {i}/{len(batch)} posts processed")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            print()

if __name__ == "__main__":
    main()