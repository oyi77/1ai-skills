#!/usr/bin/env python3
"""
PostBridge Poster - Post content to all connected accounts
"""

import requests
import json
from pathlib import Path
from datetime import datetime

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"

# Video URLs (for now, use local paths as placeholder - need to upload to hosting)
# User will need to provide hosted video URLs

# TikTok accounts to post to
TIKTOK_ACCOUNTS = [
    {"id": 45648, "username": "jasakontenai"},        # Main Jendralbot account
    {"id": 48338, "username": "massehatyuk"},          # Health
    {"id": 48337, "username": "nugrohopratama5"},      # Niche
    {"id": 48336, "username": "baimwongdiskon"},       # Coupons
    {"id": 48335, "username": "clinicguru"}           # Medical
]

# Video content from today's plan
VIDEOS = {
    "starter_ai_content": {
        "path": "~/.openclaw/workspace/videos/starter_ai_content_shorts.mp4",
        "caption": "🔥 STOP: Tidak ide tulisan?\n\nProblem: Tidak ide tulisan\nIni bikin kamu frustrasi kan?\n\nSolusinya: Starter AI Content\nSupport penuh\n\nDulu ribet, sekarang satu klik\nMulai dengan 1 konten saja\n\n💡 Link di bio atau comment 'MAU'\n\nhttps://lynk.id/jendralbot/xlymwzj2jylv\n\n#AIcontent #contentcreation #starter #AIindonesia #belajarAI",
        "product": "Starter AI Content",
        "price": "Rp 49.000"
    },
    "studio_marketplace_pro": {
        "path": "~/.openclaw/workspace/videos/studio_marketplace_pro_shorts.mp4",
        "caption": "🔥 STOP: Foto produk jelek?\n\nProblem: Foto produk jelek\nIni bikin kamu frustrasi kan?\n\nSolusinya: Studio Marketplace Pro\nCepat & praktis\n\nDulu manual, sekarang otomatis\n\nhttps://lynk.id/jendralbot/emne05mm7v25\n\n#ecommerce #onlinestore #productphoto #marketplace #AIbusiness",
        "product": "Studio Marketplace Pro",
        "price": "Rp 75.000"
    },
    "mesin_cetak_kuliner": {
        "path": "~/.openclaw/workspace/videos/mesin_cetak_kuliner_shorts.mp4",
        "caption": "🔥 STOP: Foto makanan kurang menarik?\n\nProblem: Foto makanan kurang menarik\nIni bikin kamu frustrasi kan?\n\nSolusinya: Mesin Cetak Kuliner\nProfesional tanpa fotografer\n\nDulu 4 jam, sekarang 1 menit\n\nhttps://lynk.id/jendralbot/kzryk28dxmpx\n\n#kuliner #foodphotography #GoFood #GrabFood #restaurant",
        "product": "Mesin Cetak Kuliner",
        "price": "Rp 75.000"
    },
    "ai_content_pro": {
        "path": "~/.openclaw/workspace/videos/ai_content_pro_shorts.mp4",
        "caption": "🔥 STOP: Bikin konten manual lama?\n\nProblem: Bikin konten manual lama\nIni bikin kamu frustrasi kan?\n\nSolusinya: AI Content Pro\nSave time 80%\n\nDulu manual, sekarang otomatis\n\nhttps://lynk.id/jendralbot/d70eo2x45em5\n\n#AIcontent #professional #business #AIautomation #efficiency",
        "product": "AI Content Pro",
        "price": "Rp 89.000"
    },
    "guru_pintar_ai": {
        "path": "~/.openclaw/workspace/videos/guru_pintar_ai_shorts.mp4",
        "caption": "🔥 GRATIS! Belajar AI hari ini!\n\nProblem: Belum paham AI?\nSolusinya: Guru Pintar AI - GRATIS!\n\nTraining lengkap, step-by-step\n\nDulu mahal, sekarang gratis!\n\nhttps://lynk.id/jendralbot/6821op5e24kn\n\n#free #AItraining #belajarAI #gratis #AIindonesia",
        "product": "Guru Pintar AI",
        "price": "GRATIS"
    },
    "belanja_duit_balik": {
        "path": "~/.openclaw/workspace/videos/belanja_duit_balik_shorts.mp4",
        "caption": "🔥 Belanja tapi KEMBALI DUIT!\n\nProblem: Belanja habis saja?\nSolusinya: Belanja Duit Balik - GRATIS!\n\nCashback otomatis setiap belanja\n\nBelanja tetap, dapat duit!\n\nhttps://lynk.id/jendralbot/kkjk0mv1vg7o\n\n#cashback #belanja #hemat #duitbalik #shoppingtips",
        "product": "Belanja Duit Balik",
        "price": "GRATIS"
    }
}

def post_to_tiktok(account_id, video_url, caption):
    """Post video to TikTok account via PostBridge"""

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
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()

        if response.status_code == 200:
            return True, result
        else:
            return False, result

    except Exception as e:
        return False, {"error": str(e)}

def post_to_all_tiktok_accounts(video_url, caption, video_name):
    """Post same video to all TikTok accounts"""

    print("=" * 80)
    print(f"🎬 POSTING: {video_name}")
    print("=" * 80)
    print(f"Video URL: {video_url}")
    print(f"Caption Preview: {caption[:100]}...")
    print()

    results = []
    for account in TIKTOK_ACCOUNTS:
        print(f"📱 Posting to TikTok: @{account['username']} (ID: {account['id']})")

        success, result = post_to_tiktok(account["id"], video_url, caption)

        if success:
            print(f"   ✅ SUCCESS!")
            print(f"   Post ID: {result.get('id', 'N/A')}")
            results.append({"account": account, "status": "success", "result": result})
        else:
            print(f"   ❌ FAILED!")
            print(f"   Error: {result}")
            results.append({"account": account, "status": "failed", "result": result})

        # Delay between posts
        import time
        time.sleep(2)

        print()

    return results

def main():
    print("=" * 80)
    print("🚀 POSTBRIDGE POSTER - JENDRALBOT PRODUCTS")
    print("=" * 80)
    print()

    print("⚠️  IMPORTANT!")
    print("=" * 80)
    print("PostBridge requires HOSTED video URLs (not local paths).")
    print("Please provide video URLs for each product:")
    print()
    print("Options:")
    print("1. Upload to YouTube (public/unlisted)")
    print("2. Upload to Google Drive (make shareable)")
    print("3. Upload to AWS S3 or other hosting")
    print("4. Use placeholder URLs for testing")
    print()
    print("=" * 80)

    # For demonstration, use placeholder
    # User will need to replace these with actual video URLs
    placeholder_url = "https://example.com/placeholder-video.mp4"

    # Option: Ask user for video URLs
    print("\n📥 Please provide video URLs:")
    print("(Press Enter to use placeholder for testing)")

    video_urls = {}
    for key, info in VIDEOS.items():
        user_url = input(f"\n{info['product']} ({info['price']}): ").strip()
        video_urls[key] = user_url if user_url else placeholder_url

    print()\    print("=" * 80)
    print("📤 STARTING POSTS...")
    print("=" * 80)

    all_results = []

    for video_key, video_url in video_urls.items():
        video_info = VIDEOS[video_key]

        results = post_to_all_tiktok_accounts(
            video_url=video_url,
            caption=video_info["caption"],
            video_name=video_info["product"]
        )

        all_results.extend(results)

    # Summary
    print("=" * 80)
    print("📊 POSTING SUMMARY")
    print("=" * 80)

    success_count = sum(1 for r in all_results if r["status"] == "success")
    failed_count = sum(1 for r in all_results if r["status"] == "failed")

    print(f"Total Attempts: {len(all_results)}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print()

    if failed_count > 0:
        print("Failed Posts:")
        print("-" * 80)
        for r in all_results:
            if r["status"] == "failed":
                acc = r["account"]
                print(f"  @{acc['username']}: {r['result']}")
        print()

    # Save results
    output_file = Path.home() / ".openclaw" / "workspace" / "postbridge_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
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