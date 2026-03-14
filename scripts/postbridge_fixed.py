#!/usr/bin/env python3
"""
PostBridge Poster - Fixed Version
Correct API payload format
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

# Test content
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
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Sample URL - replace with real
        "social_account_id": 45648  # jasakontenai first
    }
]

def post_to_tikTok_fixed(account_id, video_url, caption):
    """Post to TikTok via PostBridge with correct payload"""

    url = f"{BASE_URL}/posts"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Correct payload format for PostBridge
    payload = {
        "social_account_id": account_id,  # Singular, not array
        "content": caption,
        "media": {
            "url": video_url,
            "type": "video"
        }
    }

    try:
        print(f"   → Posting...")
        print(f"   Payload: account_id={account_id}, media_url={video_url[:50]}...")
        print(f"   Caption length: {len(caption)} chars")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {json.dumps(result, indent=2)}")
            return True, result
        else:
            error = response.json()
            print(f"   ❌ FAILED ({response.status_code})")
            print(f"   Error Response: {json.dumps(error, indent=2)}")
            return False, error

    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False, {"error": str(e)}

def test_single_account():
    """Test posting to ONE account first"""

    print("=" * 80)
    print("🧪 TEST POSTING TO SINGLE ACCOUNT")
    print("=" * 80)
    print()

    test_post = TEST_POSTS[0]
    print(f"Product: {test_post['product']}")
    print(f"Account: @jasakontenai (ID: {test_post['social_account_id']})")
    print(f"Video URL: {test_post['url']}")
    print(f"Caption Preview: {test_post['caption'][:100]}...")
    print()
    print("-" * 80)

    success, result = post_to_tikTok(
        test_post["social_account_id"],
        test_post["url"],
        test_post["caption"]
    )

    print("-" * 80)
    print()

    if success:
        print("✅ TEST SUCCESSFUL!")
        print("→ You can now post to all 5 accounts")
    else:
        print("❌ TEST FAILED")
        print("→ Check the error message above")
        print("→ Possible issues:")
        print("  1. Video URL is invalid/accessible")
        print("  2. Caption is too long/has issues")
        print("  3. Account ID is incorrect")
        print("  4. API Key issue")

    return success

def post_to_all_accounts():
    """Post to all 5 TikTok accounts"""

    print("=" * 80)
    print("🚀 POSTING TO ALL TIKTOK ACCOUNTS")
    print("=" * 80)
    print()

    test_post = TEST_POSTS[0]
    results = []

    for acc in TIKTOK_ACCOUNTS:
        print(f"📱 Posting to: @{acc['username']} (ID: {acc['id']})")
        print("-" * 80)

        success, result = post_to_tikTok(
            acc["id"],
            test_post["url"],
            test_post["caption"]
        )

        results.append({
            "username": acc["username"],
            "account_id": acc["id"],
            "status": "success" if success else "failed",
            "result": result
        })

        print()
        
        # Delay between posts
        import time
        time.sleep(5)  # 5 second delay

    return results

def main():
    print("🚀 POSTBRIDGE POSTER - FIXED VERSION")
    print("=" * 80)
    print()

    print("Choose Mode:")
    print("1. Test single account (@jasakontenai)")
    print("2. Post to all 5 accounts")
    print()

    choice = input("Enter choice (1 or 2): ").strip()

    print()
    print("=" * 80)

    if choice == "1":
        success = test_single_account()
    elif choice == "2":
        results = post_to_all_accounts()
        
        # Summary
        print("=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        
        success_count = sum(1 for r in results if r["status"] == "success")
        failed_count = len(results) - success_count
        
        print(f"Total: {len(results)}")
        print(f"✅ Success: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print()
        
        for r in results:
            status_icon = "✅" if r["status"] == "success" else "❌"
            print(f"{status_icon} @{r['username']} (ID: {r['account_id']}) - {r['status']}")
        
        print()
        print("=" * 80)

        # Save results
        output_file = "/home/openclaw/.openclaw/workspace/postbridge_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to: {output_file}")
        print("=" * 80)

    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()