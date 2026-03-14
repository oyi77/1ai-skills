#!/usr/bin/env python3
"""
Auto Posting to PostBridge for JENDRALBOT
Full automation: read queue → post to platforms → track results
"""

import json
import requests
from datetime import datetime
from pathlib import Path

# PostBridge API
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"  # Provided by user
BASE_URL = "https://api.post-bridge.com/api/v1"

QUEUE_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/postbridge_queue_jendralbot.json"
LOG_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/post_execution_log_jendralbot.json"

# Platform to PostBridge ID mapping
PLATFORM_IDS = {
    'tiktok': 'tiktok',
    'instagram': 'instagram',
    'facebook': 'facebook',
    'twitter': 'twitter',
    'youtube': 'youtube'
}

# Account IDs from MOVA campaign (connected and working)
ACCOUNT_IDS = {
    'tiktok': '45648',      # jasakontenai
    'instagram': '47681',   # berkahkaryadigitalmarketing
    'facebook': '47664',    # Berkah Karya Digital Marketing Agency
    'twitter': '47682',     # AgencyKarya
    'youtube': '47691'      # grahaelektroniktws
}

def get_content_type(platform):
    """Determine content type for platform"""
    if platform == 'instagram':
        return 'reel'
    elif platform == 'youtube':
        return 'shorts'
    elif platform == 'tiktok':
        return 'video'
    else:
        return 'post'

def get_social_accounts():
    """Get connected social accounts"""
    print("📱 Fetching connected accounts...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/social-accounts?limit=50&offset=0",
            headers={'Authorization': f'Bearer {API_KEY}'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            accounts = data.get('data', [])
            print(f"✅ Found {len(accounts)} connected accounts")
            return accounts
        else:
            print(f"❌ Error fetching accounts: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"❌ Exception: {e}")
        return []

def load_queue():
    """Load JENDRALBOT queue"""
    try:
        with open(QUEUE_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading queue: {e}")
        return []

def create_post_payload(queue_item, social_accounts):
    """Create PostBridge API payload"""
    platform = queue_item['platform']
    content = queue_item['content']
    scheduled_at = queue_item['schedule']['publish_at']
    
    # Find account ID for this platform
    account_id = ACCOUNT_IDS.get(platform)
    
    if not account_id:
        # Try to find from connected accounts
        for account in social_accounts:
            if account.get('platform') == platform:
                account_id = account.get('id')
                break
    
    if not account_id:
        return None, f"No account found for platform: {platform}"
    
    # Build payload
    payload = {
        'caption': content['caption'],
        'social_accounts': [account_id],
        'media': [],
        'scheduled_at': scheduled_at,
        'type': get_content_type(platform)
    }
    
    return payload, None

def submit_to_postbridge(queue_item, social_accounts):
    """Submit post to PostBridge"""
    platform = queue_item['platform'].upper()
    product = queue_item['metadata']['product']
    
    payload, error = create_post_payload(queue_item, social_accounts)
    
    if error:
        return {
            'success': False,
            'platform': platform,
            'error': error,
            'product': product
        }
    
    try:
        print(f"\n📤 Posting to {platform}...")
        print(f"   Product: {product}")
        print(f"   Account ID: {payload['social_accounts'][0]}")
        print(f"   Type: {payload['type']}")
        print(f"   Scheduled: {queue_item['schedule']['publish_at']}")
        print(f"   Caption: {content['caption'][:60]}...")
        
        response = requests.post(
            f"{BASE_URL}/posts",
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success! Post ID: {result.get('id', 'N/A')}")
            
            return {
                'success': True,
                'platform': platform,
                'post_id': result.get('id'),
                'response': result,
                'product': product,
                'account_id': payload['social_accounts'][0]
            }
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
            return {
                'success': False,
                'platform': platform,
                'error': f"HTTP {response.status_code}: {response.text}",
                'product': product
            }
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        
        return {
            'success': False,
            'platform': platform,
            'error': str(e),
            'product': product
        }

def run_auto_posting():
    """Run full auto posting"""
    print("="*70)
    print("🚀 JENDRALBOT AUTO POSTING - POSTBRIDGE")
    print("="*70)
    print()
    
    # Load queue
    queue = load_queue()
    if not queue:
        print("❌ No queue data found")
        return
    
    print(f"✅ Loaded {len(queue)} posts from queue")
    print()
    
    # Get connected accounts
    social_accounts = get_social_accounts()
    if not social_accounts:
        print("❌ No connected accounts. Cannot proceed.")
        return
    
    print()
    
    # Track results
    results = []
    success_count = 0
    failed_count = 0
    
    # Post each item
    for i, queue_item in enumerate(queue, 1):
        print(f"[{i}/{len(queue)}]", end=" ")
        
        result = submit_to_postbridge(queue_item, social_accounts)
        results.append(result)
        
        if result['success']:
            success_count += 1
        else:
            failed_count += 1
        
        # Rate limiting
        if i < len(queue):
            import time
            time.sleep(0.5)
    
    # Save log
    log = {
        'timestamp': datetime.now().isoformat(),
        'total_posts': len(queue),
        'successful': success_count,
        'failed': failed_count,
        'results': results
    }
    
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)
    
    # Summary
    print("\n" + "="*70)
    print("📊 AUTO POSTING SUMMARY")
    print("="*70)
    print(f"\n✅ Successful: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Success Rate: {(success_count/len(queue)*100):.1f}%")
    
    if success_count > 0:
        print(f"\n📅 Scheduled posts:")
        for r in results:
            if r['success']:
                emoji = {'tiktok': '📱', 'instagram': '📸', 'facebook': '📘',
                         'twitter': '🐦', 'youtube': '▶️'}.get(r['platform'].lower(), '📝')
                print(f"   {emoji} {r['platform']}: Post ID {r['post_id']}")
    
    print(f"\n📝 Log saved to: {LOG_FILE}")
    print("="*70)
    
    return log

if __name__ == "__main__":
    run_auto_posting()