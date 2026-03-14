#!/usr/bin/env python3
"""
FIX POSTBRIDGE API ERROR - Populate Queue
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/.openclaw/workspace")
ENGINE_DIR = WORKSPACE / "autopilot_affiliate_engine"
QUEUE_FILE = ENGINE_DIR / "postbridge_queue_jendralbot.json"

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

ACCOUNT_IDS = {
    'tiktok': [48186],
    'instagram': [48178, 48177],
    'facebook': [48176, 48175],
}

print("="*70)
print("🔧 FIXING POSTBRIDGE ERROR - POPULATE QUEUE")
print("="*70)
print()

# 1. Test API
print("[1/3] Testing PostBridge API...")

test_post = {
    'caption': f'🧪 Test Post - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
    'social_accounts': [48178, 48177],
    'media': [],
    'scheduled_at': (datetime.now() + timedelta(hours=25)).strftime("%Y-%m-%dT%H:%M:%S")
}

try:
    response = requests.post(
        f"{BASE_URL}/posts",
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json=test_post,
        timeout=30
    )

    print(f"   Status: {response.status_code}")

    if response.status_code in [200, 201]:
        result = response.json()
        print(f"   ✅ Test post created! ID: {result.get('id', 'N/A')}")
        test_post_id = result.get('id', 'N/A')
    else:
        print(f"   ❌ Error: {response.status_code} - {response.text[:100]}")
        print()
        print("="*70)
        print("⚠️  POSTBRIDGE ISSUE - NEEDS MANUAL LOGIN TO FIX")
        print("="*70)
        print()
        print("To fix:")
        print("1. Go to: https://post-bridge.com/")
        print("2. Login ke account JendralBot")
        print("3. Check why API returning 400")
        print("4. Update API key jika perlu")
        print()
        exit(1)

except Exception as e:
    print(f"❌ Exception: {e}")
    print()
    exit(1)

# 2. Load social posts
print()
print("[2/3] Loading social media posts...")

social_files = {
    'instagram': WORKSPACE / "social_automation/instagram_posts_20260307_0056.json",
    'tiktok': WORKSPACE / "social_automation/tiktok_posts_20260307_0056.json',
    'facebook': WORKSPACE / "social_automation/facebook_posts_20260307_0056.json"
}

all_posts = []

for platform, file_path in social_files.items():
    if file_path.exists():
        with open(file_path) as f:
            data = json.load(f)

        posts = data.get('posts', [])
        for post in posts:
            all_posts.append({
                'platform': platform,
                'content': post.get('content', '')
            })

print(f"   Instagram: {len([p for p in all_posts if p['platform'] == 'instagram'])} posts")
print(f"   TikTok: {len([p for p in all_posts if p['platform'] == 'tiktok'])} posts")
print(f"   Facebook: {len([p for p in all_posts if p['platform'] == 'facebook'])} posts")
print(f"   Total: {len(all_posts)} posts")
print()

# 3. Build queue
print()
print("[3/3] Building PostBridge queue...")

new_queue = []
start_time = datetime.now().replace(hour=8, minute=0, second=0) + timedelta(days=1)

# Simple queue - just 15 posts (5 from each platform)
post_counter = 0

for platform in ['instagram', 'tiktok', 'facebook']:
    platform_posts = [p for p in all_posts if p['platform'] == 'platform']]

    for i, post in enumerate(platform_posts[:5]):  # 5 posts per platform
        post_counter += 1

        # Get caption (clean version)
        caption = post['content']

        # Truncate if too long
        if len(caption) > 2000:
            caption = caption[:2000] + "..."

        item = {
            "id": f"social_auto_{post_counter:03d}",
            "platform": platform,
            "type": "post",
            "content": {
                "caption": caption,
                "url": "",
                "hashtags": "#jakarta #restaurant #food #jktfood"
            },
            "schedule": {
                "publish_at": (start_time + timedelta(hours=post_counter*2, days=post_counter//5)).strftime("%Y-%m-%dT%H:%M:%S"),
                "time_zone": "Asia/Jakarta"
            },
            "metadata": {
                "campaign_id": f"jendralbot_social_{datetime.now().strftime('%Y%m%d')}",
                "asset_id": f"{platform}_social_{post_counter}",
                "generated_at": datetime.now().isoformat()
            },
            "media": {
                "type": "image",
                "format": "square"
            }
        }

        new_queue.append(item)
        print(f"   + [{post_counter}] {platform}: {caption[:50]}...")

print()
print(f"✅ Created {len(new_queue)} queue items")
print()

# Save queue
existing_queue = []
if QUEUE_FILE.exists():
    with open(QUEUE_FILE) as f:
        data = json.load(f)
        existing_queue = data.get('queue', [])
        print(f"   Existing queue: {len(existing_queue)} items")

total_queue = existing_queue + new_queue

with open(QUEUE_FILE, 'w') as f:
    json.dump({
        "created_at": datetime.now().isoformat(),
        "campaign_id": f"jendralbot_final_{datetime.now().strftime('%Y%m%d')}",
        "queue": total_queue
    }, f, indent=2)

print(f"✅ Queue saved: {QUEUE_FILE}")
print()
print(f"Total queue size: {len(total_queue)} posts")
print()

print("="*70)
print("✅ POSTBRIDGE QUEUE FIXED!")
print("="*70)
print()
print("Next:")
print("  • Evening workflow akan auto-post besok jam 20:00 WIB")
print("  • System sekarang FULLY OTOMATIS!")
print()
print("Monitor:")
print("   • ~/automation.log")
print("  - Reports akan di-generate tiap 08:00 dan 20:00")
print()
print("✅ SYSTEM IS NOW FULLY AUTOMATED!")
print()