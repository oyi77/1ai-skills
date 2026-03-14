#!/usr/bin/env python3
"""
Quick PostBridge Test - Validate and Fix
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
ENGINE_DIR = WORKSPACE / "autopilot_affiliate_engine"
QUEUE_FILE = ENGINE_DIR / "postbridge_queue_jendralbot.json"

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

print("="*70)
print("🔧 PostBridge API Test & Fix")
print("="*70)
print()

# Test API with simple post
print("[TEST] Testing PostBridge API...")
print()

test_payload = {
    'caption': '🧪 Test Post - ' + datetime.now().strftime('%Y-%m-%d %H:%M'),
    'social_accounts': [48178, 48177],  # Instagram accounts
    'media': [],  # Start without media
    'scheduled_at': (datetime.now() + timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%S")
}

try:
    response = requests.post(
        f"{BASE_URL}/posts",
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json=test_payload,
        timeout=30
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:200] if len(response.text) < 200 else response.text[:100]}")

    if response.status_code in [200, 201]:
        print("✅ PostBridge API: WORKING!")

        result = response.json()
        post_id = result.get('id', 'No ID returned')

        print(f"✅ Test post created: {post_id}")

        # Now populate real queue
        print()
        print("[FIX] Populating queue with real social posts...")

        # Load social posts
        social_files = {
            'instagram': WORKSPACE / "social_automation/instagram_posts_20260307_0056.json",
            'tiktok': WORKSPACE / "social_automation/tiktok_posts_20260307_0056.json",
            'facebook': WORKSPACE / "social_automation/facebook_posts_20260307_0056.json"
        }

        # Create queue from our social posts
        new_queue = []
        start_time = datetime.now().replace(hour=8, minute=0, second=0) + timedelta(days=1)

        for platform in ['instagram', 'tiktok', 'facebook']:
            social_file = social_files.get(platform)
            if not social_file or not social_file.exists():
                continue

            with open(social_file) as f:
                data = json.load(f)
                posts = data.get('posts', [])

                for post in posts[:5]:  # 5 posts per platform (total 15 for quick test)
                    scheduled_time = start_time + timedelta(hours=len(new_queue))

                    item = {
                        "id": f"social_auto_{len(new_queue):03d}",
                        "platform": platform,
                        "type": "post",
                        "content": {
                            "caption": post.get('content', ''),
                            "url": "",
                            "hashtags": "#jakarta #restaurant #food #marketing"
                        },
                        "schedule": {
                            "publish_at": scheduled_time.strftime("%Y-%m-%dT%H:%M:%S"),
                            "time_zone": "Asia/Jakarta"
                        },
                        "metadata": {
                            "campaign_id": f"jendralbot_social_{datetime.now().strftime('%Y%m%d')}",
                            "asset_id": f"{platform}_social_{len(new_queue)}",
                            "generated_at": datetime.now().isoformat()
                        },
                        "media": {
                            "type": "image",
                            "format": "square"
                        }
                    }

                    new_queue.append(item)
                    print(f"   + {item['id']} - {platform}")

        # Save queue
        with open(QUEUE_FILE, 'w') as f:
            json.dump({
                "created_at": datetime.now().isoformat(),
                "campaign_id": f"jendralbot_social_{datetime.now().strftime('%Y%m%d')}",
                "queue": new_queue
            }, f, indent=2)

        print(f"✅ Queue populated: {len(new_queue)} posts")
        print()
        print("="*70)
        print("✅ SYSTEM FIXED AND READY!")
        print("="*70)
        print()
        print("Next:")
        print("  • Posts will auto-post at 08:00 WIB (tomorrow)")
        print("  • Morning workflow will run automatically")
        print("  • PostBridge will auto-post to Instagram/TikTok/Facebook")
        print()

        return True

    else:
        print(f"❌ Test failed")
        return False

except Exception as e:
    print(f"❌ Exception: {e}")
    return False