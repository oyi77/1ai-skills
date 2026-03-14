#!/usr/bin/env python3
"""
PostBridge Auto Posting - Simplified Approach
Direct posting to connected accounts
"""

import json
import requests
from datetime import datetime
from pathlib import Path

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

QUEUE_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/postbridge_queue_jendralbot.json"
LOG_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/post_execution_log_jendralbot.txt"

# Account IDs from MOVA campaign (these should still be connected)
ACCOUNT_IDS = {
    'tiktok': '45648',
    'instagram': '47681',
    'facebook': '47664',
    'twitter': '47682',
    'youtube': '47691'
}

def create_post(queue_item):
    """Create single post via PostBridge API"""
    platform = queue_item['platform']
    product = queue_item['metadata']['product']
    caption = queue_item['content']['caption']
    scheduled_at = queue_item['schedule']['publish_at']
    account_id = ACCOUNT_IDS.get(platform)

    if not account_id:
        return {
            'success': False,
            'platform': platform,
            'product': product,
            'error': f"No account ID for platform: {platform}"
        }

    payload = {
        'caption': caption,
        'social_accounts': [account_id],
        'media': [],  # Media URLs would go here
        'scheduled_at': scheduled_at
    }

    try:
        print(f"\n📤 Posting to {platform.upper()}...")
        print(f"   Product: {product}")
        print(f"   Account ID: {account_id}")
        print(f"   Caption: {caption[:80]}...")
        print(f"   Scheduled: {scheduled_at}")

        response = requests.post(
            f"{BASE_URL}/posts",
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"   ✅ Success! Post ID: {result.get('id', 'N/A')}")

            return {
                'success': True,
                'platform': platform,
                'post_id': result.get('id'),
                'product': product,
                'account_id': account_id
            }
        else:
            print(f"   ❌ HTTP {response.status_code}")
            print(f"   Response: {response.text}")

            return {
                'success': False,
                'platform': platform,
                'product': product,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        print(f"   ❌ Exception: {e}")

        return {
            'success': False,
            'platform': platform,
            'product': product,
            'error': str(e)
        }

def run_auto_posting():
    """Run full auto posting"""
    print("="*70)
    print("🚀 JENDRALBOT AUTO POSTING - POSTBRIDGE API v2")
    print("="*70)
    print()

    # Load queue
    try:
        with open(QUEUE_FILE) as f:
            queue = json.load(f)
    except Exception as e:
        print(f"❌ Error loading queue: {e}")
        return

    print(f"✅ Loaded {len(queue)} posts from queue")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    print()

    # Track results
    results = []
    success_count = 0
    failed_count = 0

    # Post each item
    for i, queue_item in enumerate(queue, 1):
        print(f"[{i}/{len(queue)}]", end=" ")

        result = create_post(queue_item)
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
    log_line = f"\n=== {datetime.now().isoformat()} ===\n"
    log_line += f"Total: {len(queue)} | Success: {success_count} | Failed: {failed_count}\n"
    log_line += f"Success Rate: {(success_count/len(queue)*100):.1f}%\n"

    with open(LOG_FILE, 'a') as f:
        f.write(log_line)
        for r in results:
            status = "✅" if r['success'] else "❌"
            f.write(f"{status} {r['platform']}: {r['product']}\n")

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
                         'twitter': '🐦', 'youtube': '▶️'}.get(r['platform'], '📝')
                print(f"   {emoji} {r['platform']}: Post ID {r['post_id']}")

    print(f"\n📝 Log saved to: {LOG_FILE}")
    print("="*70)

    return {
        'total': len(queue),
        'success': success_count,
        'failed': failed_count,
        'results': results
    }

if __name__ == "__main__":
    run_auto_posting()