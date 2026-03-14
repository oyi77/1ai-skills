#!/usr/bin/env python3
"""
EMERGENCY POST UPLOAD - IDR 0 BALANCE CRISIS
Upload all 305 hooks to all connected PostBridge accounts
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

# Connected accounts from status check
ACCOUNTS = {
    'tiktok': ['45648'],  # 6 TikTok accounts - using primary
    'instagram': ['47681'],  # 1 Instagram
    'facebook': ['47664']  # 3 Facebook - using primary
}

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MASTER_FILE = WORKSPACE / "output" / "all_viral_hooks_master.json"
LOG_FILE = WORKSPACE / "logs" / "emergency_upload.log"

def create_caption(hook, product_name, lynk_url):
    """Create caption from hook"""
    headline = hook.get('headline', '')
    body = hook.get('body', '')
    cta = hook.get('cta', '')

    # Replace [LYNK] placeholder with actual URL
    cta = cta.replace('[LYNK]', lynk_url) if '[LYNK]' in cta else cta
    body = body.replace('[LYNK]', lynk_url) if '[LYNK]' in body else body

    caption = f"{headline}\n\n{body}\n\n{cta}\n\n{lynk_url}"
    return caption

def upload_post(platform, account_id, caption):
    """Upload single post via PostBridge API"""
    payload = {
        'caption': caption,
        'social_accounts': [account_id],
        'media': [],  # No media - text posts for speed
        'scheduled_at': None  # Post immediately
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
            return {
                'success': True,
                'post_id': result.get('id'),
                'platform': platform
            }
        else:
            return {
                'success': False,
                'platform': platform,
                'error': f"HTTP {response.status_code}: {response.text[:200]}"
            }

    except Exception as e:
        return {
            'success': False,
            'platform': platform,
            'error': str(e)
        }

def main():
    print("="*60)
    print("🆘 EMERGENCY POST UPLOAD - IDR 0 BALANCE CRISIS")
    print("="*60)

    # Load master hooks
    print("\n📂 Loading hooks...")
    try:
        with open(MASTER_FILE, 'r') as f:
            data = json.load(f)

        products = data.get('products', [])
        total_hooks = sum(len(p.get('hooks', [])) for p in products)
        print(f"✓ Loaded {len(products)} products with {total_hooks} hooks")

    except FileNotFoundError:
        print(f"✗ Master file not found: {MASTER_FILE}")
        return
    except Exception as e:
        print(f"✗ Error loading hooks: {e}")
        return

    # Setup logging
    LOG_FILE.parent.mkdir(exist_ok=True)

    # Upload all hooks to all platforms
    results = {
        'tiktok': {'success': 0, 'failed': 0},
        'instagram': {'success': 0, 'failed': 0},
        'facebook': {'success': 0, 'failed': 0},
        'youtube': {'success': 0, 'failed': 0}
    }

    total_posts = 0
    upload_log = []

    print("\n🚀 STARTING EMERGENCY UPLOAD...")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for platform in ['tiktok', 'instagram', 'facebook']:
        accounts = ACCOUNTS.get(platform, [])
        if not accounts:
            print(f"\n⚠️ No accounts for {platform}, skipping...")
            continue

        account_id = accounts[0]
        print(f"\n📱 {platform.upper()} (Account: {account_id})")
        print("-" * 40)

        for product in products:
            product_name = product['product']
            lynk_url = product['LYNK']
            hooks = product['hooks']

            print(f"   📦 {product_name} ({len(hooks)} hooks)")

            for i, hook in enumerate(hooks):
                caption = create_caption(hook, product_name, lynk_url)

                print(f"      [{i+1}/{len(hooks)}] Uploading... ", end='', flush=True)

                result = upload_post(platform, account_id, caption)

                if result['success']:
                    print(f"✅ Post ID: {result['post_id']}")
                    results[platform]['success'] += 1
                    total_posts += 1
                    upload_log.append({
                        'timestamp': datetime.now().isoformat(),
                        'platform': platform,
                        'product': product_name,
                        'post_id': result['post_id'],
                        'status': 'success'
                    })
                else:
                    print(f"❌ {result['error'][:80]}")
                    results[platform]['failed'] += 1
                    upload_log.append({
                        'timestamp': datetime.now().isoformat(),
                        'platform': platform,
                        'product': product_name,
                        'status': 'failed',
                        'error': result['error']
                    })

    # Save upload log
    with open(LOG_FILE, 'w') as f:
        json.dump(upload_log, f, indent=2)

    # Summary
    print("\n" + "="*60)
    print("📊 UPLOAD SUMMARY")
    print("="*60)

    total_success = sum(r['success'] for r in results.values())
    total_failed = sum(r['failed'] for r in results.values())

    for platform, counts in results.items():
        if counts['success'] > 0 or counts['failed'] > 0:
            print(f"\n{platform.upper()}:")
            print(f"  ✅ Success: {counts['success']}")
            print(f"  ❌ Failed: {counts['failed']}")

    print(f"\n{'='*60}")
    print(f"TOTAL POSTS UPLOADED: {total_success}/{total_posts}")
    print(f"SUCCESS RATE: {(total_success/total_posts*100):.1f}%")
    print(f"LOG FILE: {LOG_FILE}")
    print(f"COMPLETED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    if total_success > 0:
        print("\n🎉 SUCCESS! Posts are now live on platforms.")
        print("   Monitor LYNK dashboard: https://lynk.id/jendralbot")
        print("   First revenue expected in 24-48 hours.")
        print("   CRISIS MODE: Check every 2 hours!")

if __name__ == "__main__":
    main()