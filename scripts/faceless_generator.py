#!/usr/bin/env python3
"""
Faceless Short Video Generator - Faceless Education → Product CTA
For: TikTok, Instagram Reels, YouTube Shorts, Facebook Reels
"""

import json
from pathlib import Path

# Products with faceless-friendly formats
PRODUCTS = {
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/6821op5e24kn",
        "hashtags": "#free #AItraining #belajarAI #AIindonesia #AIeducation",
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "hashtags": "#cashback #belanja #hemat #smartshopping #tips",
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "url": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #contentcreation",
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "url": "https://lynk.id/jendralbot/emne05mm7v25",
        "hashtags": "#ecommerce #productphoto #jualanonline #marketplace",
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": "Rp 75.000",
        "url": "https://lnkd.in/mesin_cetak",
        "hashtags": "#kuliner #foodphotography #GoFood #GrabFood",
    }
}

def generate_faceless_script(product_key, content_type):
    """Generate faceless video script"""
    product = PRODUCTS.get(product_key)
    
    if product_key == "guru_pintar_ai" and content_type == "info_benefit":
        return """=== FACELESS VIDEO SCRIPT ===
Product: Guru Pintar AI
Duration: 15s
Type: Info Benefit

---

HOOK (0-3s):
"🔥 STOP! Konten manual makan waktu 4 jam/post!"

BODY (3-12s):
"Dulu saya ide konten kosong nungguin 2 jam.
Writing caption 1 jam + edit gambar 45 menit + posting 15 menit
Total: 4 jam per post!

Masalah: Hanya 2-3 konten per minggu.
GAK SCALE!

Solusi: Guru Pintar AI - Start belajar GRATIS
AI Content Pro: Ide 5 menit + caption 1 menit + edit 1 menit
Total: 8 menit per post.

ROI: 90 jam/bulan = 360 konten/bulan!

CTA (3s):
Mulai dari belajar GRATIS di Guru Pintar AI
Level-up ke AI Content Pro: https://lnkd.in/ai-content-pro

VISUAL:
→ Text overlay: 'AI = 24x lebih cepat!' (bold, centered putih)
→ B-ROLL: Workspace b-roll (person struggling vs productive)
→ End: Product screen centered showing speed
→ Fade: To black

AUDIO:
→ Voice: Energetic, friendly
→ Music: Upbeat instrumental
→ Tempo: 120-140 BPM (medium-fast)
→ Volume: 30-40% dari voice max

"""
    
    elif product_key == "belanja_duit_balik" and content_type == "quick_tips":
        return """=== FACELESS VIDEO SCRIPT ===
Product: Belanja Duit Balik
Duration: 15s
Type: Quick Tips

---

HOOK (0-3s):
"💡 5 Tips Hemat Belanja Hari Ini!"

BODY (3-12s):
1. Check promo hari ini sebelum belanja (kalau di jam 9-11 AM shopee double cashback!)
2. Gunakan kartu BCA/Mandiri/NISS yang ada bonus cashback di merchant tertentu
3. Stack aplikasi saat promo (Shopee + OVO + TikTok Shop = TRIPLE CASHBACK!)
4. Fokus kebutuhan, jangan belanja karena keta-ketan!
5. Cek kalender promo sebelum belanja

CTA (3s):
Kalkulator: https://lynk.id/jendralbot/kzryk28dxmpx
GRATIS info lengkap di sana!

VISUAL:
→ Numbered tips (1, 2, 3, 4, 5) overlay
→ Shopee app screenshots showing promo calendar
→ Cashback kalkulator screen capture
→ Lifestyle b-roll: people shopping happily

AUDIO:
→ Voice: Energetic dan helpful
→ Music: Playful upbeat
→ Tempo: Fast (mengikur 140 BPM)
→ Volume: Medium-high

"""
    
    else:
        # Default
        return generate_faceless_script("guru_pintar_ai", "info_benefit")
    
    return script

def main():
    print("=" * 80)
    print("🎬 FACELESS SHORT VIDEO GENERATOR")
    print("=" * 80)
    print()
    print("Platforms: TikTok / Instagram Reels / YouTube Shorts / Facebook Reels")
    print("Style: Faceless (Voice Over Only + B-Roll)")
    print("Duration: 15-20 seconds")
    print("Format: 9:16 vertical")
    print()
    
    # Show sample for each major product
    print("✅ GURU PINTAR AI - INFO_BENEFIT:")
    print("-" * 80)
    print(generate_faceless_script("guru_pintar_ai", "info_benefit"))
    print()
    print()
    print("✅ BELANJA DUIT BALIK - QUICK_TIPS:")
    print("-" * 80)
    print(generate_faceless_script("belanja_duit_balik", "quick_tips"))
    print()
    
    print("=" * 80)
    print("📊 STRATEGY")
    print("=" * 80)
    print()
    print("💡 VARIASI KONTEN FACELESS:")
    print()
    print("1. Info Benefit (Educational)")
    "   → Product problem → AI solution with stats")
    "   → Hook: STOP/SHOCKING number")
    "   → Tone: Informative + authority")
    "   → CTA: Soft natural")
    print()
    print("2. Quick Tips (Value-first)")
    "   → 5 actionable tips in 15 seconds")
    "   → Numbered format: 1, 2, 3, 4, 5")
    "   → Tone: Fast, helpful, practical")
    print()
    print("3. Storytelling (Motivational)")
    "   → Before/After transformation journey")
    "   → Relatable struggle → success story")
    "   → Tone: Emotional, inspiring")
    "   → CTA: Natural progress suggestion")
    print()
    print("4. Data Dock (Shock value)")
    "   → Start dengan mengejutkan data")
    "   → 3 data points震惊受众")
    "   - "Stop wasting [X] jam/bulan!"
    "   → Solution: {product}"
    "   → Tone: Authoritative + urgent")
    print()
    print("💰 CTA OPTIONS:")
    print("   • Edukasi: Link sebagai sumber info (soft sell)")
    print("   • Jualan: "Coba sekarang: {link} (medium sell)")
    "   • Engagement: "DM: 'INFO' untuk detail (soft sell)")
    print("   • Community: "Komen di bawah untuk diskusi (community)")
    print()
    print("=" * 80)
    print("📹 FACELESS FACE-SHOT PRODUCTION:")
    print("=" * 80)
    print()
    print("🤖 VOICE OVER:")
    "   • Tools: ElevenLabs (GRATIS) / Google TTS (free tier)")
    "   • Style: Friendly but conversational (not robotic)")
    "   • Speed: Medium-fast (120-140 BPM)")
    print()
    print("🎵 MUSIC:")
    "   • Upbeat instrumental (Spotify free tier works well)")
    "   - Energetic yet not overpowering voice")
    "   - Volume: 30-40% of voice max volume")
    "🌙 Platform-Specific:")
    "   • TikTok: Trending sound, upbeat")
    "   • Instagram: Chill lofi, calm")
    "   - YouTube: Inspirational, motivational")
    "   - Facebook: Fun, upbeat")
    print()
    print("🎨 B-ROLL VISUAL:")
    "   • Screen recording (product interface - AI Content Pro)")
    "   • Stock footage (workspaces, office setups, people working)")
    "   • Product photographs (Studio Marketplace Pro, Mesin Cetak Kuliner)")
    "   • Lifestyle overlays (shopping, food, travel)")
    print()
    print("📏 TEXT OVERLAYS:")
    "   → Hook: Bold, centered, white text on first 15% of video")
    "   → Body: 2-3 key points (numbered, left or center aligned)")
    "   → CTA: Product link atau DM 'INFO' centered on last 20%")
    ")
    print("   Font: White, bold sans-serif (Arial, Helvetica, Roboto)")
    print()
    print("📹 EXPORT:")
    "   - Format: MP4 (H.264)")
    "   - Resolution: 1080x1920 (9:16 vertical)")
    "   - Duration: 15-20 seconds")
    "   - File size: <8-10 MB (TikTok limit)")
    "   - Bitrate: 4-6 Mbps")
    print()
    print("=" * 80)
    print("💡 FACELESS SUCCESS TIPS:")
    print("=" * 80)
    print("✅ Hook matters most - First 3 seconds critical!")
    print("✅ 5-second hook is ideal (STOP, SHOCKING numbers)")
    print("✅ Keep text short & punchy (banyak emoji)")
    print("✅ Use trending sound (TikTok has popular audio library)")
    print("✅ Text overlay timing: Hook=visible 3s, Body=5-12s, CTA=last 2s)")
    print("✅ CTA di akhir JAMAN hard sell (DM "INFO" lebih soft)")
    print()
    print("=" * 80)
    print("📋 READY TO GENERATE:")
    print("1. Choose product & content type")
    "2. Get script + visual breakdown from this generator")
    "3. Generate voice over (ElevenLabs/Google TTS)")
    "4. Collect/create b-roll footage")
    "5. Edit in video editor (CapCut, Premiere Pro, or simpler tools)")
    "6. Export: 9:16 vertical, upload ke PostBridge")
    print("=" * 80)

if __name__ == "__main__":
    main()

# Sample generated scripts for each product
# These are ready to use: faceless_generator.py creates similar structured scripts