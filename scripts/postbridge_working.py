#!/usr/bin/env python3
"""
PostBridge Poster - WORKING VERSION
Correct API payload format - tested and verified
"""

import requests
import json
import time

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

# TikTok accounts
TIKTOK_ACCOUNTS = [
    {"id": 45648, "username": "jasakontenai"},
    {"id": 48338, "username": "massehatyuk"},
    {"id": 48337, "username": "nugrohopratama5"},
    {"id": 48336, "username": "baimwongdiskon"},
    {"id": 48335, "username": "clinicguru"}
]

# Test content (GRATIS products dulu)
POSTS = [
    {
        "product": "Guru Pintar AI (GRATIS)",
        "caption": """🔥 GRATIS! Belajar AI hari ini!

Problem: Belum paham AI?
Solusinya: Guru Pintar AI - GRATIS!

Training lengkap, step-by-step
Dulu mahal, sekarang gratis!

https://lynk.id/jendralbot/6821op5e24kn

#free #AItraining #belajarAI #gratis #AIindonesia""",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"  # Test video - ganti nanti
    },
    {
        "product": "Belanja Duit Balik (GRATIS)",
        "caption": """🔥 Belanja tapi KEMBALI DUIT!

Problem: Belanja habis saja?
Solusinya: Belanja Duit Balik - GRATIS!

Cashback otomatis setiap belanja
Belanja tetap, dapat duit!

https://lynk.id/jendralbot/kkjk0mv1vg7o

#cashback #belanja #hemat #duitbalik #shoppingtips""",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4"  # Test video - ganti nanti
    }
]

def post_to_tiktok(account_id, caption, media_url):
    """Post to TikTok via PostBridge - CORRECT FORMAT"""

    url = f"{BASE_URL}/posts"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # CORRECT PAYLOAD FORMAT
    payload = {
        "social_accounts": [account_id],      # Array of account IDs
        "caption": caption,                     # Caption text
        "media_url": media_url,                # Direct video URL
        "platform": "tiktok"                   # Platform
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return True, result
        else:
            error = response.json()
            return False, error

    except Exception as e:
        return False, {"error": str(e)}

def main():
    print("=" * 80)
    print("🚀 POSTBRIDGE POSTER - WORKING VERSION")
    print("=" * 80)
    print()

    # Post each product to all accounts
    all_results = []

    for post_idx, post in enumerate(POSTS, 1):
        print(f"{'='*80}")
        print(f"📤 POST {post_idx}: {post['product']}")
        print(f"{'='*80}")
        print(f"Caption: {post['caption'][:80]}...")
        print(f"Video URL: {post['video_url']}")
        print()

        post_results = []

        for acc in TIKTOK_ACCOUNTS:
            print(f"📱 TikTok: @{acc['username']} (ID: {acc['id']})")

            success, result = post_to_tiktok(
                acc["id"],
                post["caption"],
                post["video_url"]
            )

            post_results.append({
                "username": acc["username"],
                "account_id": acc["id"],
                "status": "success" if success else "failed",
                "result": result
            })

            if success:
                print(f"   ✅ SUCCESS! Post ID: {result.get('id', 'N/A')}")
                print(f"   Status: {result.get('status', 'N/A')}")
            else:
                print(f"   ❌ FAILED!")
                print(f"   Error: {result}")

            print()

            # Delay between posts (5 seconds)
            time.sleep(5)

        all_results.append({
            "post_number": post_idx,
            "product": post["product"],
            "results": post_results
        })

    # Summary
    print("=" * 80)
    print("📊 POSTING SUMMARY")
    print("=" * 80)

    total = len(all_results) * len(TIKTOK_ACCOUNTS)
    success = sum(1 for p in all_results for r in p["results"] if r["status"] == "success")
    failed = total - success

    print(f"Total Posts: {total}")
    print(f"✅ Success: {success}")
    print(f"❌ Failed: {failed}")
    print()

    if failed > 0:
        print("Failed Posts:")
        print("-" * 80)
        for p in all_results:
            for r in p["results"]:
                if r["status"] == "failed":
                    print(f"  {p['product']} → @{r['username']}: {r['result']}")
        print()

    # Save results
    output_file = "/home/openclaw/.openclaw/workspace/postbridge_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
    print("=" * 80)
    print()
    print("📋 NEXT STEPS:")
    print("1. Check postbridge_results.json for Post IDs")
    print("2. Visit PostBridge dashboard: https://post-bridge.com")
    print("3. Monitor post status (processing → completed/failed)")
    print("4. Check TikTok accounts to verify posts")
    print("5. Replace test video URL with real hosted URLs")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()