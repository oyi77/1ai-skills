#!/usr/bin/env python3
"""
TikTok Video Generator for Jendralbot Products
Custom version for product-specific marketing
"""

import asyncio
import sys
import os
from pathlib import Path

# Add content-generator skills to path
skill_path = Path(__file__).parent.parent / "skills" / "content-generator"
sys.path.insert(0, str(skill_path))

from scripts.generator import ContentGenerator

PRODUCT_CONFIGS = {
    "starter_ai_content": {
        "niche": "productivity",
        "script_hook": "🔥 STOP: Susah bikin konten?",
        "script_body": "Problem: Tidak ide tulisan. Solusinya: Starter AI Content - Rp 49.000. Support penuh, upgrade-ready. Dulu ribet, sekarang satu klik!",
        "hashtag": "#AIcontent #belajarAI #contentcreation"
    },
    "studio_marketplace_pro": {
        "niche": "success",
        "script_hook": "🔥 STOP: Foto produk jelek?",
        "script_body": "Problem: Editing lama. Solusinya: Studio Marketplace Pro - Rp 75.000. Foto profesional, cepat & praktis. Dulu 4 jam, sekarang 1 menit!",
        "hashtag": "#ecommerce #productphoto #online store"
    },
    "mesin_cetak_kuliner": {
        "niche": "success",
        "script_hook": "🔥 Makananmu layak foto lebih bagus!",
        "script_body": "Problem: Foto makanan biasa saja. Solusinya: Mesin Cetak Kuliner - Rp 75.000. Food aesthetic, profesional tanpa fotografer!",
        "hashtag": "#kuliner #foodphotography #GoFood"
    },
    "ai_content_pro": {
        "niche": "productivity",
        "script_hook": "🔥 STOP: Bikin konten manual lama?",
        "script_body": "Problem: Save 80% waktu? Use AI Content Pro - Rp 89.000. Otomatiskan konten, kualitas premium!",
        "hashtag": "#AIcontent #business #AIautomation"
    },
    "guru_pintar_ai": {
        "niche": "motivation",
        "script_hook": "🔥 GRATIS! Belajar AI hari ini!",
        "script_body": "Problem: Belum paham AI? Solusinya: Guru Pintar AI - GRATIS! Training lengkap, step-by-step!",
        "hashtag": "#free #AItraining #belajarAI"
    },
    "belanja_duit_balik": {
        "niche": "money",
        "script_hook": "🔥 Belanja tapi KEMBALI DUIT!",
        "script_body": "Problem: Belanja habis saja. Solusinya: Belanja Duit Balik - GRATIS! Cashback otomatis!",
        "hashtag": "#cashback #belanja #hemat"
    }
}

async def generate_tiktok_video(product_key, ratio="9:16"):
    """Generate TikTok video for a product"""
    if product_key not in PRODUCT_CONFIGS:
        print(f"❌ Unknown product: {product_key}")
        print(f"Available: {', '.join(PRODUCT_CONFIGS.keys())}")
        return None

    config = PRODUCT_CONFIGS[product_key]
    print(f"🎬 Generating TikTok video for: {product_key}")
    print(f"   Niche: {config['niche']}")
    print(f"   Hook: {config['script_hook']}")
    print()

    # Initialize generator
    gen = ContentGenerator()

    # Generate content
    try:
        result = await gen.generate(
            concept=config['niche'],
            platform="tiktok",
            ratio=ratio,
            target_duration=60
        )

        print("✅ Video generated successfully!")
        print(f"   Video: {result.get('video', 'N/A')}")
        print(f"   Hook: {result.get('hook', config['script_hook'])}")
        print(f"   Caption: {result.get('caption', 'Use custom caption')}")

        return result

    except Exception as e:
        print(f"❌ Error generating video: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check NVIDIA_API_KEY: echo $NVIDIA_API_KEY")
        print("   2. Check BYTEPLUS_API_KEY: echo $BYTEPLUS_API_KEY")
        print("   3. Test providers: cd skills/content-generator && python3 scripts/test_providers.py")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_jendralbot_tiktok.py <product_key>")
        print()
        print("Available products:")
        for key in PRODUCT_CONFIGS:
            print(f"   - {key}")
        return

    product_key = sys.argv[1].lower()
    ratio = sys.argv[2] if len(sys.argv) > 2 else "9:16"

    asyncio.run(generate_tiktok_video(product_key, ratio))

if __name__ == "__main__":
    main()