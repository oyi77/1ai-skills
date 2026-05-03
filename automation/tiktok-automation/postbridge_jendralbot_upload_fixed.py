#!/usr/bin/env python3
"""
JENDRALBOT PostBridge Uploader (FIXED VERSION)
Upload 18 hook frames ke social media (YouTube, Instagram, Twitter, Facebook) menggunakan PostBridge API
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime

# Constants
POSTBRIDGE_API_KEY = "pb_live_BBLz9mjZkkL8q41tb2pwxq"
POSTBRIDGE_BASE_URL = "https://api.post-bridge.com"

# Social Accounts (from API response)
SOCIAL_ACCOUNTS = [
    47691,  # YouTube - grahaelektroniktws
    47690,  # YouTube - Diskon Hunter
    47689,  # YouTube - Mak E Nok
    47682,  # Twitter - AgencyKarya
    47681,  # Instagram - berkahkaryadigitalmarketing
    47664,  # Facebook - Berkah Karya Digital Marketing Agency
    45676,  # Facebook - Belanja
    45675,  # Facebook - Stevi Shop
    45674,  # Facebook - Dewi Shop
    45673,  # Facebook - Clara Store
]

# Asset paths
HOOK_FRAMES_DIR = Path("/home/openclaw/.openclaw/workspace/skills/1ai-skills/tiktok-automation/assets")
HOOK_FRAMES = sorted(HOOK_FRAMES_DIR.glob("*.png"))

print(f"📦 Found {len(HOOK_FRAMES)} hook frames")

# Product definitions with captions & hashtags
PRODUCTS = {
    "belanja_duit_balik": {
        "name": "Belanja Tetap Jalan Tapi Du Tetap Balik",
        "price": "FREE",
        "affiliate_link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "hooks": {
            "hook1_shock": {
                "caption": "GILA! BELANJA DU TETAP BALIK!",
                "hashtags": "#cashback #belanja #duitbalik #gratis #affiliate #viral #tiktok #fyp"
            },
            "hook2_problem": {
                "caption": "BELANJA PASTI HABIS DU?",
                "hashtags": "#cashbackbelanja #duit #cashback #solusi #affiliate"
            },
            "hook3_solution": {
                "caption": "Sistem Cashback Otomatis!",
                "hashtags": "#cashback #affiliate #gratis #viral"
            }
        }
    },
    "guru_pintar_ai": {
        "name": "Guru Pintar Ai",
        "price": "IDR 75K",
        "affiliate_link": "https://lynk.id/jendralbot/6821op5e24kn",
        "hooks": {
            "hook1_shock": {
                "caption": "RAHASIA AI UNTUK GURU MODERN! 🤫",
                "hashtags": "#guru #pendidikan #ai #edukasi #guruai #panduan #teacher #viral"
            },
            "hook2_problem": {
                "caption": "GURU PINTER TAPI NGGAK KENA AI?",
                "hashtags": "#guru #gurupintar #education #gurukai"
            },
            "hook3_solution": {
                "caption": "GURU PINTAR AI - 50+ template, auto-grading!",
                "hashtags": "#guru #gurupintar #education #ai #edukasi"
            }
        }
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "IDR 75K",
        "affiliate_link": "https://lynk.id/jendralbot/emne05mm7v25",
        "hooks": {
            "hook1_shock": {
                "caption": "BIKIN PRODUK AI SEHARI JADI! 🚀",
                "hashtags": "#marketplace #produkai #jualan #jualan #bisnisonline #affiliate #dropship"
            },
            "hook2_problem": {
                "caption": "PENGEN JUAL PRODUK AI TAPI?",
                "hashtags": "#marketplace #jualan #bisnisonline"
            },
            "hook3_solution": {
                "caption": "STUDIO MARKETPLACE PRO - 100+ Template!",
                "hashtags": "#marketplace #jualan"
            }
        }
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Bisnis Kulinermu",
        "price": "IDR 75K",
        "affiliate_link": "https://lynk.id/jendralbot/x8g6m3p9q1r2",
        "hooks": {
            "hook1_shock": {
                "caption": "BISNIS KULINER TANPA MODAL BESAR! 🔥",
                "hashtags": "#kuliner #bisniskuliner #bisnis #jualan #makanan #kulinermu"
            },
            "hook2_problem": {
                "caption": "MAU BISNIS KULINER TAPI?",
                "hashtags": "#kuliner #kuliner #bisnis #jualan #makanan"
            },
            "hook3_solution": {
                "caption": "MESIN CETAK BISNIS KULINER!",
                "hashtags": "#kuliner #bisniskuliner"
            }
        }
    },
    "ai_content_pro_seller": {
        "name": "AI Content Pro Seller 4K",
        "price": "IDR 89K",
        "affiliate_link": "https://lynk.id/jendralbot/y5h7j8k9l0m1",
        "hooks": {
            "hook1_shock": {
                "caption": "BLOK WRITING? 4000+ KONTEN SIAP PAKAI! 📱",
                "hashtags": "#contentcreator #viral #tiktok #instagram #youtube #ai #affiliatemarketing"
            },
            "hook2_problem": {
                "caption": "CONTENT CREATOR SUSAH BUAT KONTEN?",
                "hashtags": "#contentcreator #viral #tiktok #instagram"
            },
            "hook3_solution": {
                "caption": "AI CONTENT PRO SELLER 4K - 4000+ Template Viral!",
                "hashtags": "#contentcreator #viral #tiktok #instagram"
            }
        }
    },
    "starter_content_4k": {
        "name": "Starter AI Content 4K",
        "price": "IDR 49K",
        "affiliate_link": "https://lynk.id/jendralbot/n2o3p4q5r6s7",
        "hooks": {
            "hook1_shock": {
                "caption": "MAU KONTEN PAKE? MODAL 49K! 💰",
                "hashtags": "#contentcreator #pemula #viral #tiktok #affiliatemarketing #beginner"
            },
            "hook2_problem": {
                "caption": "PENGEN KONTEN TAPI BUDGET MEPEK?",
                "hashtags": "#contentcreator #pemula #viral #tiktok"
            },
            "hook3_solution": {
                "caption": "STARTER AI CONTENT 4K - 4000+ Templates!",
                "hashtags": "#contentcreator #pemula #viral #tiktok"
            }
        }
    }
}

def get_file_mapping():
    """Map hook frames ke products"""
    mapping = {}
    
    for hook_file in HOOK_FRAMES:
        filename = hook_file.stem  # e.g., "belanja_duit_balik_hook1_shock"
        
        # Parse filename
        parts = filename.split("_")
        
        if len(parts) >= 3:
            product_key = "_".join(parts[:-2])  # Everything except last 2 parts
            hook_type = "_".join(parts[-2:])  # Last 2 parts (e.g., "hook1_shock")
            
            mapping[filename] = {
                "product": product_key,
                "hook_type": hook_type,
                "filepath": hook_file
            }
    
    return mapping

def upload_media_to_postbridge(filepath):
    """Upload media ke PostBridge API (2-step process)"""
    
    print(f"   ⏳ Step 1: Creating upload URL...")
    
    # Get file info
    file_size = filepath.stat().st_size
    filename = filepath.name
    
    # Step 1: Create upload URL
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "mime_type": "image/png",
        "size_bytes": file_size,
        "name": filename
    }
    
    response = requests.post(
        f"{POSTBRIDGE_BASE_URL}/v1/media/create-upload-url",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code not in [200, 201]:
        print(f"   ❌ CREATE UPLOAD URL FAILED (Status: {response.status_code})")
        print(f"   Response: {response.text[:200]}")
        return None
    
    upload_data = response.json()
    upload_url = upload_data.get("upload_url")
    media_id = upload_data.get("media_id")
    
    print(f"   ✅ Upload URL created: {media_id}")
    print(f"   ⏳ Step 2: Uploading binary data...")
    
    # Step 2: Upload binary data
    with open(filepath, "rb") as f:
        binary_data = f.read()
    
    upload_response = requests.put(
        upload_url,
        headers={"Content-Type": "image/png"},
        data=binary_data,
        timeout=60
    )
    
    if upload_response.status_code not in [200, 201]:
        print(f"   ❌ BINARY UPLOAD FAILED (Status: {upload_response.status_code})")
        return None
    
    print(f"   ✅ Media uploaded successfully: {media_id}")
    return media_id

def post_to_social_accounts(media_id, caption, hashtag_str):
    """Post media ke semua social accounts"""
    
    print(f"   ⏳ Step 3: Publishing to social accounts...")
    
    # Combine caption + hashtags
    full_caption = f"{caption}\n\n{hashtag_str}"
    
    # Request payload (FIXED: using "caption" not "content" + adding "social_accounts")
    payload = {
        "caption": full_caption,
        "social_accounts": SOCIAL_ACCOUNTS,
        "media": [media_id]
    }
    
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{POSTBRIDGE_BASE_URL}/v1/posts",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"   ✅ POST CREATED SUCCESSFULLY!")
        print(f"   Post ID: {result.get('id', 'N/A')}")
        return result.get('id', 'N/A')
    else:
        print(f"   ❌ POST FAILED (Status: {response.status_code})")
        print(f"   Response: {response.text[:200]}")
        return None

def upload_hook_frame(product_key, hook_type, caption, hashtag_str, affiliate_link, filepath):
    """Complete flow: upload media + post to social accounts"""
    
    print(f"\n📤 Processing: {filepath.name}")
    print(f"   Product: {product_key} ({hook_type})")
    print(f"   Caption: {caption}")
    
    try:
        # Step 1 & 2: Upload media
        media_id = upload_media_to_postbridge(filepath)
        if not media_id:
            return {
                "success": False,
                "error": "Media upload failed",
                "file": str(filepath)
            }
        
        # Full caption with affiliate link
        full_caption = f"{caption}\n\n🔗 {affiliate_link}"
        
        # Step 3: Post to social accounts
        post_id = post_to_social_accounts(media_id, full_caption, hashtag_str)
        if not post_id:
            return {
                "success": False,
                "error": "Post creation failed",
                "file": str(filepath)
            }
        
        return {
            "success": True,
            "post_id": post_id,
            "media_id": media_id,
            "file": str(filepath)
        }
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "file": str(filepath)
        }

def batch_upload():
    """Upload semua hook frames ke social media"""
    
    file_mapping = get_file_mapping()
    
    print("\n" + "="*80)
    print("🚀 JENDRALBOT - POSTBRIDGE UPLOAD (FIXED VERSION)")
    print("="*80)
    print(f"📦 Total hook frames: {len(file_mapping)}")
    print(f"🔑 API Key: pb_live_BBLz9mjZkkL8q41tb2pwxq")
    print(f"📱 Social Accounts: {len(SOCIAL_ACCOUNTS)} (YouTube, Instagram, Twitter, Facebook)")
    print("="*80 + "\n")
    
    results = []
    success_count = 0
    
    for filename, info in file_mapping.items():
        product_key = info["product"]
        hook_type = info["hook_type"]
        filepath = info["filepath"]
        
        # Get product data
        product = PRODUCTS.get(product_key)
        if not product:
            print(f"   ⚠️ Product not found: {product_key}")
            continue
        
        affiliate_link = product["affiliate_link"]
        
        # Get hook data
        hook_data = product["hooks"].get(hook_type)
        if not hook_data:
            print(f"   ⚠️ Hook not found: {hook_type}")
            continue
        
        caption = hook_data["caption"]
        hashtag_str = hook_data["hashtags"]
        
        # Upload via PostBridge
        result = upload_hook_frame(
            product_key=product_key,
            hook_type=hook_type,
            caption=caption,
            hashtag_str=hashtag_str,
            affiliate_link=affiliate_link,
            filepath=filepath
        )
        
        results.append(result)
        if result["success"]:
            success_count += 1
        
        # Delay sebelum next upload
        print(f"   ⏳ Waiting 3 seconds...")
        time.sleep(3)
    
    # Summary
    print("\n" + "="*80)
    print("📊 POSTBRIDGE UPLOAD SUMMARY")
    print("="*80)
    print(f"✅ Successful uploads: {success_count}/{len(results)}")
    print(f"❌ Failed uploads: {len(results) - success_count}/{len(results)}")
    
    if len(results) - success_count > 0:
        print(f"\n⚠️ Failed uploads:")
        for result in results:
            if not result["success"]:
                print(f"   - {Path(result['file']).name}: {result.get('error', 'Unknown')}")
    
    print("\n✅ POSTBRIDGE UPLOAD COMPLETE!")
    print(f"📱 {success_count} hook frames berhasil di-upload ke social media")
    print(f"💰 Siap untuk TRACKING: https://lynk.id/jendralbot\n")

def main():
    print("🎯 POSTBRIDGE UPLOAD - JENDRALBOT CAMPAIGN (FIXED VERSION)")
    print("🚀 Uploading 18 hook frames ke social media (YouTube, Instagram, Twitter, Facebook)")
    
    try:
        batch_upload()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()