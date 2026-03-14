#!/usr/bin/env python3
"""
Day 1 Planner - Start from Zero Strategy
Build audience trust with FREE products first
"""

import json
from pathlib import Path

FREE_PRODUCTS = {
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/6821op5e24kn",
        "hashtags": "#free #AItraining #belajarAI #gratis #AIindonesia"
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "hashtags": "#cashback #belanja #hemat #smartshopping #GRATIS"
    }
}

EDUKASI_THEMES = {
    "guru_pintar_ai": {
        "day_1": "Apa itu AI? Definisi untuk Pemula",
        "day_2": "AI vs Manual - Sama atau Beda?",
        "day_3": "Tools AI yang Wajib Dipelajari (Top 5)",
        "day_4": "Skill Skills yang Bisa Digenerate AI",
        "day_5": "Cara Dipakai AI untuk Pemula (Step-by-Step)",
        "day_6": "Cost Analysis: Manual vs AI Tools",
        "day_7": "Mitos tentang AI yang Salah",
        "day_8": "Case Study: Pekerjaan 10x Cepat dengan AI",
        "day_9": "Roadmap Belajar AI dalam 6 Bulan",
        "day_10": "Quality vs Quantity - Mindset AI Content",
        "day_11": "Tips: Hindari AI Dependency Burnout",
        "day_12": "Budget Management dengan AI Tools",
        "day_13": "Success Story: Pekerjaan Hemat 500k dengan AI",
        "day_14": "Tips: Quality Content vs Quantity",
        "day_15": "Review: Apa yang Sudah Dipelajari"
    },
    "belanja_duit_balik": {
        "day_1": "Cashback 101 - Apa Itu?",
        "day_2": "Aplikasi Cashback Terbesar di Indonesia",
        "day_3": "Strategi: Belanja di Waktu Kritis",
        "day_4": "Tips: Stacking Cashback (Triple Cashback Trick)",
        "day_5": "Kisah Orang Hemat 1 Bulan: Testimoni",
        "day_6": "Kalkulator: Berapa Bisa Hemat Per Bulan?",
        "day_7": "Mitos: Cashback Hanya Buat Boros?",
        "day_8": "Advanced: Credit Card Cashback Strategy",
        "day_9": "Platform Comparison: Shopee vs Tokopedia",
        "day_10": "Hidden Gems: Aplikasi Cashback Jarang Diketahui",
        "day_11": "FOMO: Kalau Nggak Ambil Sekarang Kehilangan",
        "day_12": "Budget Management Mindset",
        "day_13": "Success Story: Hemat 500k Setahun",
        "day_14": "Tips: Hemat Tanpa Belanja Tambah",
        "day_15": "Review & Next Level Strategy"
    }
}

def generate_day_1_schedule():
    """Generate Day 1 schedule (12 posts)"""
    schedule = {
        "date": "2026-03-07",
        "phase": "Foundation - Day 1",
        "strategy": "Trust Building (80% Edukasi, 20% Soft Sales)",
        "products": ["guru_pintar_ai", "belanja_duit_balik"],
        "posts": []
    }
    
    # 12 posts (every 2 hours: 00:00 to 22:00)
    hours = list(range(0, 24, 2))  # 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22
    
    for hour in hours:
        # Alternate products every 4 hours
        if hour % 4 == 0:
            product_key = "guru_pintar_ai"
        else:
            product_key = "belanja_duit_balik"
        
        # Alternate type: Sales (even hours), Education (odd hours)
        post_type = "sales" if hour % 2 == 0 else "education"
        series_part = ((hour // 2) % 15) + 1  # day 1-15 cycle
        
        if post_type == "education":
            post = generate_education_post(product_key, series_part)
        else:
            post = generate_soft_sales_post(product_key, hour)
        
        post["time"] = f"{hour:02d}:00"
        post["product"] = product_key
        schedule["posts"].append(post)
    
    return schedule

def generate_education_post(product_key, day):
    """Generate education post"""
    product = FREE_PRODUCTS[product_key]
    theme = EDUKASI_THEMES[product_key][f"day_{day}"]
    
    if product_key == "guru_pintar_ai":
        caption = f"""📚 {theme} - Day {day}/Foundation

APA ITU AI?

---

Banyak ORANG salah paham! Mari bedahin:

❌ BUKAN robot pengganti manusia
❌ BUKAN magic instant
✅ TOOL yang AMPLIFIK skill manusia

Analogi:
📱 Calculator tidak gantikan matematikawan
🚗 Mobil tidak gantikan driver
🎓 AI tidak gantikan creator

AI = LEVEL UP productivity!

CONTOH NYATA:
Content Creator:
- Manual: 4 jam/post
- AI: 10 menit/post → 24x lebih cepat!

Pebisnis Online:
- Manual: 1 jam/edit
- AI: 1 menit/edit → 60x lebih cepat!

KESIMPULAN:
AI itu enhancer, bukan replacement.

---
📖 Besok: Tools AI yang Wajib Dipelajari!

{product['hashtags']}
#AI101 #education #belajarAI #pemula #{product['name'].replace(' ', '')}"""
    
    else:  # belanja_duit_balik
        caption = f"""💰 {theme} - Day {day}/Foundation

APAK ITU CASHBACK?

---

DEFINISI:
Cashback = uang balik dari total belanja
Contoh: Belanja 100k → Balik 5k
⚠️ BUKAN hadiah! Itu potongan harga

CONTOH NYATA:
• Shopee Double Cashback: 500k → Dapat 50k (10%)
• GoFood OVO Points: 30k → 100 points (~1k)
• Tokopedia Cashback Events: 200k → 100+ points

RELEVANSI:
Kalau belanja rutin 200k/bulan
→ Cashback: 20k/bulan
→ Tahunan: 240k!

HEMAT BENER-BENER!

⚠️ WARNING:
Cashback untuk KONSUMSI, bukan investasi!
Jangan overspending!

---
📖 Besok: Strategi Belanja di Waktu Kritis!

{product['hashtags']}
#cashback #belanja #hemat #smartshopping #GRATIS
"""
    
    return caption

def generate_soft_sales_post(product_key, hour):
    """Generate soft sales (20% only on Day 1)"""
    product = FREE_PRODUCTS[product_key]
    
    if product_key == "guru_pintar_ai":
        caption = f"""📚 MULAI BELAJAR GRATIS!

Penasaran tapi bingung biayanya? Saya paham.

Solusi: Guru Pintar AI ✨

Training Lengkap:
✅ AI 101 untuk pemula
✅ Step-by-step tutorial
✅ Tools AI yang wajib dipelajari
✅ Roadmap 6 bulan
✅ Support komunitas

100% GRATIS! Tanpa kewajiban upgrade!

Untuk yang sudah paham dasar & mau level up:
AI Content Pro (Rp 89k) → Full automation
👉 https://lynk.id/jendralbot/d70eo2x45em5

Mulai dari GRATIS, level up ke PRO! 💪

{product['hashtags']}
#GRATIS #AItraining #belajar #education #AI
"""
    
    else:  # belanja_duit_balik
        caption = f"""💰 CASHBACK GRATIS! LHO!

Support informasi cashback untuk semua!

Platforms:
✨ Shopee (double cashback)
✨ GoFood (regular)
✨ OVO (often)
✨ Tokopedia (events)

Aplikasi paling bagus?
→ Kuliner: GoFood/GrabFood
→ Shopping: Shopee/Tokopedia
→ Travel: Traveloka
→ Payment: OVO (specific merchants)

💡 Tips Awal:
1. Cek promo hari ini
2. Gunakan kartu dengan bonus cashback
3. Stack aplikasi (triple during promo)

⚠️ Jangan overspending! Belanja SECARA kebutuhan!

📖 Besok: Stacked Cashback Trick (ROI 3x!)

{product['url']}
{product['hashtags']}
#cashback #hemat #GRATIS #tipsbelanja #discount
"""
    
    return caption

def main():
    schedule = generate_day_1_schedule()
    
    # Save
    workspace = Path.home() / ".openclaw" / "workspace"
    with open(workspace / "day1_start_from_zero.json", "w") as f:
        json.dump(schedule, f, indent=2)
    
    print("=" * 80)
    print("📅 DAY 1 - START FROM ZERO SCHEDULE")
    print("=" * 80)
    print(f"📅 {schedule['date']}")
    print(f"Phase: {schedule['phase']}")
    print(f"Strategy: {schedule['strategy']}")
    print(f"Products: {schedule['products'][0]} + " & " + schedule['products'][1]}")
    print()
    
    for post in schedule["posts"]:
        icon = "💰" if post["type"] == "sales" else "📚"
        product_name = "Guru Pintar AI" if "guru" in post["product"] else "Belanja Duit Balik"
        
        print(f"{icon} {post['time']} - {post['type'].upper():7s} - {product_name}")
        if post["type"] == "sales":
            print(f"   Soft sell - 20% only")
        print(f"   Caption preview: {post['caption'][:70]}...")
        print()
    
    print("=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    
    total = len(schedule["posts"])
    sales = sum(1 for p in schedule["posts"] if p["type"] == "sales")
    edu = sum(1 for p in schedule["posts"] if p["type"] == "education")
    
    print(f"Total Posts: {total}")
    print(f"Sales Posts: {sales} (soft promotion - 20%)")
    print(f"Education Posts: {edu} (value - 80%)")
    print(f"Balance: {sales * 100 // total}% Sales - {edu * 100 // total}% Edu")
    print()
    print("🎯 DAY 1 GOALS:")
    print("1. Build trust with education")
    print("2. Generate leads (Guru Pintar AI signups)")
    print("3. Capture email/leads from users")
    print("4. Establish authority in AI & smart shopping")
    print("5. Warm up audience (15 hari foundation)")
    print()
    print("💼 EXPECTED OUTCOMES WEEK 1:")
    print("- Followers: +200-500 (organic)")
    print("- Leads: 20-30 (Guru Pintar AI registrants)")
    print("- Engagement: Medium (education engages)")
    print("- Sales: 0-2 (soft sells only)")
    print()
    print("=" * 80)
    print("✅ Saved to: day1_start_from_zero.json")
    print()
    print("📋 NEXT STEPS:")
    print("1. Review schedule (12 posts)")
    print("2. Generate visuals for 12 posts")
    print("3. Setup PostBridge automation")
    print("4. Day 1 execution (manual or auto)")
    print("5. Track leads & engagement")
    print("=" * 80)

if __name__ == "__main__":
    main()