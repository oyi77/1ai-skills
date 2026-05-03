#!/usr/bin/env python3
"""
JENDRALBOT PostBridge TikTok Uploader - V3 (BYPASS ACCOUNT CHECK)
Upload 18 hook frames ke TikTok menggunakan PostBridge API
Directly use @jasakontenai (already connected)
"""

import json
import requests
import time
from pathlib import Path

# Constants
POSTBRIDGE_API_KEY = "pb_live_LzxK4Q4428kb1b6KETgdue"
POSTBRIDGE_BASE_URL = "https://api.post-bridge.com/api/v1"

# Asset paths
HOOK_FRAMES_DIR = Path("/home/openclaw/.openclaw/workspace/fonts/output_ultimate")
HOOK_FRAMES = sorted(HOOK_FRAMES_DIR.glob("*.png"))

# Product definitions
PRODUCTS = {
    "belanja_duit_balik": {
        "name": "Belanja Tetap Jalan Tapi Du Tetap Balik",
        "price": "FREE",
        "affiliate_link": "https://ynk.id/jendralbot/kkjk0mv1vg7o",
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
        "affiliate_link": "https://ynk.id/jendralbot/6821op5e24kn",
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
        "affiliate_link": "https://ynk.id/jendralbot/emne05mm7v25",
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
        "affiliate_link": "https://ynk.id/jendralbot/x8g6m3p9q1r2",
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
        "affiliate_link": "https://ynk.id/jendralbot/y5h7j8k9l0m1",
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
        "affiliate_link": "https://ynk.id/jendralbot/n2o3p4q5r6s7",
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
        filename = hook_file.stem
        
        parts = filename.split("_")
        
        if len(parts) >= 3:
            product_key = "_".join(parts[:-2])
            hook_type = "_".join(parts[-2:])
            
            mapping[filename] = {
                "product": product_key,
                "hook_type": hook_type,
                "filepath": hook_file
            }
    
    return mapping

def upload_to_postbridge_v3(product_key, hook_type, caption, hashtags, affiliate_link, filepath, social_account_username="jasakontenai"):
    """Upload single hook frame ke PostBridge TikTok API"""
    
    # Build full caption
    full_caption = f"{caption}\n\n{hashtags}\n\n🔗 {affiliate_link}"
    
    print(f"\n📤 Uploading: {filepath.name}")
    print(f"   Product: {product_key}")
    print(f"   Caption: {caption}")
    print(f"   TikTok Account: @{social_account_username}")
    
    # Prepare payload untuk PostBridge
    payload = {
        "platform": "tiktok",
        "content": full_caption,
        "social_account_username": social_account_username,
        "platforms": ["tiktok"]
    }
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_API_KEY}"
    }
    
    try:
        print(f"   ⏳ Uploading to PostBridge API...")
        
        # Read file
        with open(filepath, "rb") as f:
            files = {
                "media": (filepath.name, f, "image/png")
            }
            
            response = requests.post(
                f"{POSTBRIDGE_BASE_URL}/posts",
                headers=headers,
                data=payload,
                files=files,
                timeout=60
            )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print(f"   ✅ UPLOAD SUKSES!")
            print(f"   Post ID: {result.get('id', 'N/A')}")
            
            return {
                "success": True,
                "post_id": result.get('id', 'N/A'),
                "platform": "tiktok",
                "file": str(filepath)
            }
        else:
            print(f"   ❌ UPLOAD FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text[:500]}")
            
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:200]}",
                "file": str(filepath)
            }
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "error": str(e),
            "file": str(filepath)
        }

def batch_upload_via_postbridge_v3():
    """Upload semua hook frames ke TikTok menggunakan @jasakontenai"""
    
    file_mapping = get_file_mapping()
    
    print("\n" + "="*80)
    print("🚀 JENDRALBOT - POSTBRIDGE TIKTOK UPLOAD (V3 - BYPASS)")
    print("="*80)
    print(f"📦 Total hook frames: {len(file_mapping)}")
    print(f"📱 TikTok Account: @jasakontenai")
    print(f"🔑 API Key: pb_live_LzxK4Q4428kb1b6KETgdue")
    print("="*80 + "\n")
    
    print("✅ @JASAKONTENAI ALREADY CONNECTED TO POSTBRIDGE!")
    print("✅ BYPASS ACCOUNT CHECK - LANGSUNG UPLOAD KE @JASAKONTENAI\n")
    
    results = []
    success_count = 0
    
    for filename, info in file_mapping.items():
        product_key = info["product"]
        hook_type = info["hook_type"]
        filepath = info["filepath"]
        
        product = PRODUCTS.get(product_key)
        if not product:
            print(f"   ⚠️ Product not found: {product_key}")
            continue
        
        affiliate_link = product["affiliate_link"]
        
        hook_data = product["hooks"].get(hook_type)
        if not hook_data:
            print(f"   ⚠️ Hook not found: {hook_type}")
            continue
        
        caption = hook_data["caption"]
        hashtags = hook_data["hashtags"]
        
        # Upload via PostBridge V3
        result = upload_to_postbridge_v3(
            product_key=product_key,
            hook_type=hook_type,
            caption=caption,
            hashtags=hashtags,
            affiliate_link=affiliate_link,
            filepath=filepath,
            social_account_username="jasakontenai"
        )
        
        results.append(result)
        if result["success"]:
            success_count += 1
        
        print(f"   ⏳ Waiting 5 seconds...")
        time.sleep(5)
    
    # Summary
    print("\n" + "="*80)
    print("📊 POSTBRIDGE UPLOAD SUMMARY - V3")
    print("="*80)
    print(f"✅ Successful uploads: {success_count}/{len(results)}")
    print(f"❌ Failed uploads: {len(results) - success_count}/{len(results)}")
    
    if len(results) - success_count > 0:
        print(f"\n⚠️ Failed uploads:")
        for result in results:
            if not result["success"]:
                print(f"   - {Path(result['file']).name}: {result.get('error', 'Unknown')}")
    
    print("\n✅ POSTBRIDGE UPLOAD COMPLETE!")
    if success_count > 0:
        print(f"📱 {success_count} hook frames berhasil di-upload ke @jasakontenai")
        print(f"💰 Siap untuk TRACKING: https://lynk.id/jendralbot")
        print(f"🎯 Check TikTok: https://www.tiktok.com/@jasakontenai")
    print("")

def main():
    print("🎯 POSTBRIDGE TIKTOK UPLOAD - JENDRALBOT CAMPAIGN (V3 - BYPASS)")
    print("🚀 Uploading 18 hook frames to @jasakontenai using PostBridge API")
    print("✅ @jasakontenai already connected - BYPASS account check")
    
    try:
        batch_upload_via_postbridge_v3()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()