#!/usr/bin/env python3
"""
PostBridge Poster - Quick Test Version
Test posting with sample URLs or use your own
"""

import requests
import json

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

# Sample content (FREE products first - test with these)
TEST_POSTS = [
    {
        "product": "Guru Pintar AI (GRATIS)",
        "caption": """🔥 GRATIS! Belajar AI hari ini!

Problem: Belum paham AI?
Solusinya: Guru Pintar AI - GRATIS!

Training lengkap, step-by-step
Dulu mahal, sekarang gratis!

https://lynk.id/jendralbot/6821op5e24kn

#free #AItraining #belajarAI #gratis #AIindonesia""",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Sample URL - please replace
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
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Sample URL - please replace
    }
]

def post_to_tiktok(account_id, video_url, caption):
    """Post to TikTok via PostBridge"""

    url = f"{BASE_URL}/posts"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "social_account_ids": [account_id],
        "content": caption,
        "media_url": video_url,
        "platform": "tiktok"
    }

    try:
        print(f"   → Posting...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS!")
            print(f"   Post ID: {result.get('id', 'N/A')}")
            return True, result
        else:
            error = response.json()
            print(f"   ❌ FAILED ({response.status_code})")
            print(f"   Error: {error.get('message', 'Unknown')}")
            return False, error

    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False, {"error": str(e)}

def main():
    print("=" * 80)
    print("🚀 POSTBRIDGE POSTER - QUICK TEST")
    print("=" * 80)
    print()

    print("TikTok Accounts:")
    for acc in TIKTOK_ACCOUNTS:
        print(f"  • @{acc['username']} (ID: {acc['id']})")
    print()

    print("Test Posts:")
    print("  1. Guru Pintar AI (GRATIS)")
    print("  2. Belanja Duit Balik (GRATIS)")
    print()

    # Post each test content
    all_results = []

    for i, test_post in enumerate(TEST_POSTS, 1):
        print("=" * 80)
        print(f"📤 POST {i}: {test_post['product']}")
        print("=" * 80)
        print(f"Video URL: {test_post['url']}")
        print(f"Caption Preview: {test_post['caption'][:80]}...")
        print()

        post_results = []

        for acc in TIKTOK_ACCOUNTS:
            print(f"📱 TikTok: @{acc['username']} (ID: {acc['id']})")

            success, result = post_to_tiktok(
                acc["id"],
                test_post["url"],
                test_post["caption"]
            )

            post_results.append({
                "account": acc["username"],
                "account_id": acc["id"],
                "status": "success" if success else "failed",
                "result": result
            })

            # Delay between posts
            import time
            time.sleep(3)
            print()

        all_results.append({
            "post_number": i,
            "product": test_post["product"],
            "results": post_results
        })

    # Summary
    print("=" * 80)
    print("📊 POSTING SUMMARY")
    print("=" * 80)

    total = len(all_results) * len(TIKTOK_ACCOUNTS)
    success = sum(1 for p in all_results for r in p["results"] if r["status"] == "success")
    failed = total - success

    print(f"Total Posts Attempted: {total}")
    print(f"✅ Success: {success}")
    print(f"❌ Failed: {failed}")
    print()

    if failed > 0:
        print("Failed Posts Details:")
        print("-" * 80)
        for p in all_results:
            for r in p["results"]:
                if r["status"] == "failed":
                    print(f"  {p['product']} → @{r['account']}: {r['result']}")
        print()

    # Save results
    output_file = "/home/openclaw/.openclaw/workspace/postbridge_test_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
    print("=" * 80)
    print()
    print("📋 NEXT STEPS:")
    print("1. Check if posts were successful")
    print("2. Visit TikTok accounts to verify")
    print("3. If successful, post remaining 4 products!")
    print("4. Upload videos to YouTube for real URLs")
    print("5. Run full postbridge_poster.py")
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