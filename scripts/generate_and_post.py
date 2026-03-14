#!/usr/bin/env python3
"""
Generate Jendralbot Content & Post to PostBridge Platforms
Batch generation for all 6 products
"""

import asyncio
import aiohttp
import json
import os
from pathlib import Path
from datetime import datetime

# PostBridge API Configuration
POSTBRIDGE_API_KEY = os.getenv('POST_BRIDGE_API_KEY')
BASE_URL = "https://api.postbridge.io"

# Products data
PRODUCTS = {
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "hashtags": "#free #AItraining #belajarAI #AIindonesia #AIeducation #tutorial #automation",
        "cta": "GRATIS training lengkap!",
        "hook": "🔥 STOP! Konten manual makan waktu 4 jam/post!"
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "hashtags": "#cashback #belanja #hemat #smartshopping #tips #GRATIS #duitbalik #voucher",
        "cta": "Rahasia cashback di sini!",
        "hook": "💡 5 Tips Hemat Belanja Hari Ini!"
    },
    "starter_ai_content": {
        "name": "Starter AI Content",
        "price": "Rp 49.000",
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #contentcreation #productivity #business #automation #contentmarketing",
        "cta": "Full automation - Rp 49.000!",
        "hook": "🚀 Scale kontenmu dari 5 ke 50 per BULAN!"
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "hashtags": "#ecommerce #productphoto #jualanonline #marketplace #AIbusiness #productphotography #tokopedia #shopee",
        "cta": "Foto produk PRO - Rp 75.000!",
        "hook": "📸 Jualan tanpa foto PRO? GAK MUNGKIN!"
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": "Rp 75.000",
        "link": "https://lnkd.in/mesin_cetak",
        "hashtags": "#kuliner #foodphotography #restaurant #GoFood #GrabFood #foodbusiness #restoran #bisniskuliner",
        "cta": "Dapatkan foto premium - Rp 75.000!",
        "hook": "🍽️ Restoran mau EXIST butuh foto MENARIK!"
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #business #productivity #contentmarketing #creator #automation #AItool",
        "cta": "Full automation untuk pros - Rp 89.000!",
        "hook": "🤖 AI ini bisa generate 360 konten/bulan OLEH DIRI!"
    }
}

def generate_caption(product_key):
    """Generate TikTok caption for product."""
    product = PRODUCTS[product_key]
    
    caption = f"""{product['hook']}

Dulu saya {product['name']} manual prosesnya lama.

💸 Problem:
❌ Ide konten kosong
❌ Writing caption butuh 1 jam
❌ Edit gambar makan waktu
❌ Posting manual slow

✨ {product['name']} - {product['price']}:
AI Content Pro: 5 menit untuk COMPLETE workflow!

📊 Sebelum: 2-3 konten/bulan
📊 Sesudah: 30-90 konten/bulan

✅ Growth: 10-30x lebih cepat!

💰 Investasi: {product['price']}
⏰ ROI: 90 jam/hari dihemat = 360 konten/bulan

{product['cta']}

👉 {product['link']}

{product['hashtags']}
"""
    return caption

async def create_post_request(product_key, platform="tiktok"):
    """Create PostBridge API post request."""
    product = PRODUCTS[product_key]
    
    # Generate caption
    caption = generate_caption(product_key)
    
    # Prepare request
    url = f"{BASE_URL}/v1/posts"
    
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "platform": platform,
        "type": "text" if platform in ["twitter", "linkedin"] else "image",
        "content": {
            "text": caption
        }
    }
    
    # Add image if available for TikTok/IG
    if platform in ["tiktok", "instagram"]:
        image_path = Path.home() / ".openclaw" / "workspace" / "content" / "samples" / "nvidia_hook_final.png"
        if image_path.exists():
            # Read image as base64
            with open(image_path, "rb") as f:
                import base64
                image_data = base64.b64encode(f.read()).decode()
                payload["content"]["image"] = image_data
                payload["content"]["filename"] = "hook_image.png"
    
    return {
        "url": url,
        "headers": headers,
        "payload": payload
    }

async def post_to_platform(product_key, platform):
    """Post content to specific platform via PostBridge."""
    
    post_request = await create_post_request(product_key, platform)
    
    print(f"\n📤 Posting `{PRODUCTS[product_key]['name']}` to {platform.upper()}...")
    print(f"   API URL: {post_request['url']}")
    print(f"   API Key: {POSTBRIDGE_API_KEY[:8]}...{POSTBRIDGE_API_KEY[-8:]}")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            post_request["url"],
            json=post_request["payload"],
            headers=post_request["headers"]
        ) as resp:
            print(f"   Response: HTTP {resp.status}")
            
            if resp.status == 200:
                data = await resp.json()
                print(f"   ✅ SUCCESS!")
                print(f"   Response: {data}")
                return {"success": True, "data": data}
            else:
                error_text = await resp.text()
                print(f"   ❌ FAILED: {error_text}")
                return {"success": False, "error": error_text}

async def generate_and_post_all():
    """Generate and post all content to all platforms."""
    
    print("="*80)
    print("🚀 JENDRALBOT CONTENT GENERATION & POSTING")
    print("="*80)
    print()
    print(f"Products: {len(PRODUCTS)}")
    print("Platforms: TikTok, Instagram, X (Twitter), LinkedIn, Facebook")
    print()
    print("="*80)
    
    # Platforms to post
    platforms = ["tiktok", "instagram", "twitter", "linkedin", "facebook"]
    
    results = []
    
    # Generate and post each product to each platform
    for product_key in PRODUCTS:
        product = PRODUCTS[product_key]
        
        print(f"\n{'='*80}")
        print(f"📦 Product: {product['name']}")
        print(f"{'='*80}")
        
        # Post to each platform
        for platform in platforms:
            result = await post_to_platform(product_key, platform)
            results.append({
                "product": product_key,
                "platform": platform,
                "success": result.get("success", False),
                "data": result.get("data", {}),
                "error": result.get("error", "")
            })
    
    # Summary
    print("\n" + "="*80)
    print("📊 POSTING SUMMARY")
    print("="*80)
    
    successful = sum(1 for r in results if r.get("success"))
    failed = len(results) - successful
    
    print(f"Total Posts: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print()
    
    print("="*80)
    print("✅ COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    try:
        asyncio.run(generate_and_post_all())
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()