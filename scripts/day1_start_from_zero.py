#!/usr/bin/env python3
"""
Day 1 Planner - Start from Zero Strategy
Build audience trust with FREE products first
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

# Phase 1: Foundation (Hari 1-15)
# Product focus: Guru Pintar AI + Belanja Duit Balik
# Type: 80% Edukasi + 20% Soft Promotion

# Sample educational content themes for FREE products
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
        "day_10": "Tools AI vs Biaya Freelance",
        "day_11": "Productifitas Hacks dengan AI",
        "day_12": "Time Management dengan AI Automation",
        "day_10": "Quality vs Quantity - Mindset AI Content",
        "day_11": "Tips: Hindari AI Dependency Burnout",
        "day_12": "Budget Management with Cashback Mindset",
        "day_13": "Success Story: Pelajar yang Hemat 500k Tahun Lalu",
        "day_14": "Tips: Kalau Tanpa Belanja Lebih",
        "day_15": "Review & Next Level Strategy"
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
        "day_10": "Hidden Gems: Aplikasi Cashback Yang Jarang Diketahui",
        "day_11": "FOMO: Kalau Nggak Ambil Sekarang Kehilangan",
        "day_12: "Budget Management with Cashback Mindset",
        "day_13": "Success Story: Pelajar yang Hemat 500k Tahun Lalu",
        "day_14": "Tips: Kalengkah Tanpa Belanja Lebih",
        "day_15": "Review & Next Level Strategy"
    }
}

def generate_day_1_schedule():
    """Generate Day 1 complete schedule - Start from zero"""
    
    # Day 1 posts (12 posts, 2-hour interval)
    schedule = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "phase": "Foundation - Day 1",
        "strategy": "Trust Building with FREE Products",
        "products_in_focus": ["guru_pintar_ai", "belanja_duit_balik"],
        "posts": []
    }
    
    for hour in range(0, 24, 2):
        # Product alternation (every 4 hours)
        if hour % 4 == 0:
            product_key = "guru_pintar_ai"
        else:
            product_key = "belanja_duit_balik"
        
        # Type alternation (every 2 hours)
        post_type = "sales" if hour % 2 == 0 else "education"
        
        # Generate post
        if post_type == "education":
            post = generate_education_post(product_key, hour, 1)
        else:
            post = generate_soft_sales_post(product_key, hour)
        
        post["time"] = f"{hour:02d}:00"
        schedule["posts"].append(post)
    
    return schedule

def generate_education_post(product_key, hour, day):
    """Generate education post for Day 1 (foundational)"""
    themes = EDUKASI_THEMES[product_key]
    
    day_key = f"day_{day}"
    theme = themes.get(day_key, f"Edukasi tentang produk")
    
    # Format education post (value-first, no selling)
    if product_key == "guru_pintar_ai":
        caption = f"""📚 {theme} - Day {day}/Foundation

---

🤔 APA SIH AI (Artificial Intelligence)?

---

Banyak ORANG salah paham tentang AI!

Mari kita bedahin:

❌ AI bukan robot pengganti manusia
❌ AI bukan magic instant
❌ AI bukan bikin kita semua jadi "jobless"

✅ AI adalah TOOL yang AMPLIFIK skill manusia
✅ AI bantu kita jadi LEBIH produktif
✅ AI menghemat WAKTU & BIAYA

---

Analogi mudah:

AI itu kayak:
📱 Calculator untuk matematika
🚗 Mobil untuk transportasi

Orang jadi "jobless" kalkulator? GAK.
Orang jadi "jobless" mobil? GAK.

Mereka punya tool, jadi LEBIH cepat & lebih produktif!

---

Contoh nyata:

Content Creator:
❌ Manual: 4 jam/post (ide+edit+publish)
✅ AI-assisted: 10 menit/post → 24x lebih cepat!

Pebisnis Online:
❌ Manual: 1 jam/edit produk
✅ AI-assisted: 1 menit/edit → 60x lebih cepat!
{PRODUCTS['ai_content_pro']['name']}: Full automation

---

KESIMPULAN:

AI itu ENHANCER, bukan replacement.
Belajar AI = LEVEL UP skill productivity!

Jangan takut AI. Kelola AI dengan bijak.

---

📖 Besok lanjut: Tools AI yang Wajib Dipelajari!

---

#AI #AI101 #education #belajarAI #pemula #AIindonesia
"""
    
    elif product_key == "belanja_duit_balik":
        caption = f"""💰 {theme} - Day {day}/Foundation

---

APAK ITU CASHBACK?

---

Banyak orang KURANG PAHAM, padah "cashback sering"!

Mari jelaskan dengan SEDERHANA:

---

💰 DEFINISI:

Cashback = uang balik dari total belanja
• Contoh: Belanja 100.000 → Dapat 5.000 kembali
• BUKAN hadiah! Itu potongan harga

💡 PRINSIP:

Platform (Shopee/GoFood/OVO/Tokopedia)
  ↓
Makin sering belanja
  ↓
Platform promos (cashback)
  ↓
Diskon khusus user loyal

---

📊 CONTOH NYATA:

Shopee Double Cashback:
 Belanja 500.000 → Cashback 50.000 (10%)
Net: 550.000 value!

GoFood OVO Points:
Belanja 30.000 → Points 100+ (≈ 1.000-2.000)
Net: Belanja 30.000 + makanan!

Tokopedia Cashback:
Belanja 200.000 → OVO Points 100+
Net: Belanja 200.000 + benefit

---

🎯 RELEVANSI KE KAMU:

Kalau belanja rutin (mingguan):
→ Setiap 500k dapat 50k
→ Bulanan: 200k cashback (4×500k)
→ Tahun: 2.4 juta cashback!

Ini BUKAN bonus keuntungan ekstra! Hemat bener!

---

⚠️ WARNING:

Cashback untuk KONSUMSI, bukan investasi!
Belanja sesuai KEBUTUHAN, bukan cuma kejar cashback.

🚫 Jangan overspending!"

---

💪 START KECIL:

Mulai dari kecil:
→ Cek aplikasi kamu (Shopee/GoFood/OVO/Tokopedia)
→ Cek promo hari ini
• Belanja sekedarn (5-50k saja)
• Tidak ada tekanan untuk belanja

→ Lihat hasil cashback setelah 1 minggu

---

📚 Besok: Strategi Belanja di Waktu Kritis!

---

💰 #cashback #belanja #hemat #smartshopping #tips #GRATIS
"""

def generate_soft_sales_post(product_key, hour):
    """Generate soft sales post for Day 1 (very soft!)"""
    # Only 20% of posts should be sales on Day 1
    
    # Very soft sell - focus on value, not pushing product
    if product_key == "guru_pintar_ai":
        caption = f"""📚 MULAI BELAJAR GRATIS!

---

Penasaran belajar AI tapi bingung biayanya?

Saya paham. Tools AI mahal banget!

Tapi ada solusi GRATIS untuk PEMULA! 🎁

📖 Guru Pintar AI
Training lengkap:
✅ AI 101 untuk pemula
✅ Step-by-step tutorial
✅ Tools AI yang Wajib dipelajari
✅ Roadmap belajar 6 bulan
✅ Support komunitas

✨ DAPATKAN BANYAK INFO TANPA BIAYA!

Ini bukan produk trial, ini TRAINING KOMPLIT!

Untuk yang serius belajar AI tapi budget terbatas:

{PRODUCTS['ai_content_pro']['name']} → Full automation
👉 {PRODUCTS['ai_content_pro']['link']} (Rp 89k)

Mulai dari {PRODUCTS['guru_pintar_ai']['url']}, level up ke {PRODUCTS['ai_content_pro']['url']}

Gak ada kewajiban beli upgrade!

---

#AItraining #GRATIS #belajar #free #AI #education #{PRODUCTS['guru_pintar_ai']['name'].replace(' ', '').lower()}
"""
    
    elif product_key == "belanja_duit_balik":
        caption = f"""💰 CASHBACK GRATIS! LHO!

---

Dukungan informasi cashback untuk semua!

Platform:
✨ Shopee (sering double cashback)
✨ GoFood (regular)
✨ OVO (often)
✨ Tokopedia (cashback events)
✨ Traveloka (regular)

---

Aplikasi apa yang PALING BAGUS untukmu?

Tergantung kebutuhan:
→ Kuliner → GoFood/GrabFood
→ Shopping umum → Shopee/Tokopedia
→ Travel → Traveloka/Traveloka
→ Payment → OVO (cashback on specific merchants)
→ All platform combination (stacking)

---

💡 Tips awal:

1. Cek promo hari ini sebelum belanja
2. Gunakan kartu bank dengan bonus cashback (BCA/Mandiri/BNI have cashback!)
3. Stack aplikasi (triple cashback saat promo)
4. Timing belanja (pagi/siang/sore/malam - tergantung platform)

---

⚠️ REMINDER:

Cashback itu KEBAHAN bukan PENGHASILAN!

Don't overspending!
Belanja SECARA kebutuhan, enjoy cashback sebagai bonus.

---

📖 Besok: Panduan Stacked Cashback untuk ROI 10x!

---

💰 #cashback #hemat #GRATIS #tipsbelanja #smartshopping #{PRODUCTS['belanja_duit_balik']['name'].replace(' ', '')}
"""

    return {
        "time": f"{hour:02d}:00",
        "type": "sales",
        "variant": "soft_promo",
        "caption": caption,
        "product": product_key
    }

def generate_phase2_introduction():
    """Generate transition post when introducing paid products (Day 16)"""
    caption = """🎉 LEVEL UP TIME!

---

Hari 1-15: Edukasi & GRATIS (fokus trust building)
Hari 16-30: Entry Level (mulai jualan produk benerharga)

---

Yang sudah belajar:

✅ AI itu apa & bukan apa
✅ Tools AI yang perlu dipelajari
✅ Cara memulai skill AI
✅ Productivity mindset dengan AI
✅ Cashback strategy

---

Yang sudah dipraktik:

✅ Menghabiskan 240+ jam (12 posts × 2 jam × 15 hari)
✅ Share edukasi FREE ke 4.000+ followers
✅ Build authority di niche AI & smart shopping
✅ Trust terbentuk

---

Sekarang LEVEL UP!

💰 Starter AI Content (Rp 49.000)
→ Untuk pemula yang mau mulai praktik AI

💰 Studio Marketplace Pro (Rp 75.000)
→ Untuk sellerkuliner yang mau foto premium

💰 Mesin Cetak Kuliner (Rp 75.000)
→ Untuk restaurant owner yang mau food aesthetic

💰 AI Content Pro (Rp 89.000)
→ Untuk yang mau full automation

---

Kenapa mulai dari produk kecil? 🤔

1. ✅ Risk kecil (investasi kecil)
2. ✅ Prove value dulu (trial product)
3. � Upsell otomatis setelah trust built
4. ✅ Customer journey natural flow (GRATIS → Cheap → Expensive)

---

Mulai dari:
→ GRATIS → Entry Level → Mid Tier → Premium
→ Foundation → Traction → Scale

---

🚀 READY TO LEVEL UP?

Starter AI Content: https://lnkd.in/starter_ai_content
Studio Marketplace Pro: https://lnkd.in/studio_marketplace_pro

---

#growth #levelup #foundation #trustfirst #strategy #AIcontent
"""
    
    return {"type": "phase_transition", "caption": caption}

def main():
    print("=" * 80)
    print("📅 DAY 1 PLANNER - START FROM ZERO STRATEGY")
    print("=" * 80)
    print()
    print("Phase: Foundation (Hari 1-15)")
    print("Focus: Trust Building with FREE Products")
    print("Ratio: 80% Edukasi + 20% Soft Sales")
    print("Products: Guru Pintar AI + Belanja Duit Balik")
    print()
    
    # Generate Day 1 schedule
    schedule = generate_day_1_schedule()
    
    # Save
    workspace = Path.home() / ".openclaw" / "workspace"
    day1_file = workspace / "day1_start_from_zero_schedule.json"
    with open(day1_file, "w") as f:
        json.dump(schedule, f, indent=2)
    
    print("=" * 80)
    print("📋 DAY 1 SCHEDULE (START FROM ZERO)")
    print("=" * 80)
    print()
    print(f"📅 {schedule['date']}")
    print(f"Phase: {schedule['phase']}")
    print(f"Strategy: {schedule['strategy']}")
    print()
    
    for post in schedule["posts"]:
        icon = "💰" if post["type"] == "sales" else "📚"
        product_name = "Guru Pintar AI" if "guru" in post["product"] else "Belanja Duit Balik"
        
        print(f"{icon} {post['time']} - {post['type'].upper()} - {product_name}")
        print(f"   {post.get('variant', '')}")
        print(f"   Caption preview: {post['caption'][:80]}...")
        print()
    
    print("=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    print(f"Total Posts: {len(schedule['posts'])}")
    print()
    
    sales_count = sum(1 for p in schedule["posts"] if p["type"] == "sales")
    edu_count = sum(1 for p in schedule["posts"] if p["type"] == "education")
    
    print(f"Sales posts: {sales_count} (soft promotion only - 20%)")
    print(f"Education posts: {edu_count} (value-first - 80%)")
    print(f"Balance: {sales_count}_sales - {edu_count}_edu ({sales_count/len(schedule['posts'])*100:.0f}% sales)")
    print()
    print("💡 DAY 1 GOALS:")
    print("1. Build audience trust (edukasi value)")
    print("2. Establish authority (consistent posting)")
    print("3. Generate leads (capture FREE product users)")
    print("4. Warm up untuk introduce paid products di Day 16")
    print("5. Create engagement (reply to comments, build community)")
    print()
    print("💰 EXPECTED OUTCOMES WEEK 1:")
    print("- Followers: 200-500 (from current level)")
    print("- Engagement: Medium-Low (education builds credibility)")
   ("- Sales: 0-2 (soft sells only, not focus)")
    print("- DM leads: 10-20 (Guru Pintar AI signups)")
    print("- Cashback signups: 5-10 (Belanja Duit Balik registrants)")
    print()
    print("=" * 80)
    print("✅ Day 1 schedule saved to: day1_start_from_zero_schedule.json")
    print()
    print("📋 NEXT STEPS:")
    print("1. Review schedule in file")
    print("2. Generate visuals for 12 posts (6 GRATIS products images)")
    "3. Post manually today via PostBridge or manual")
    "4. Track engagement & leads")
    print("5. Tomorrow: Repeat with fresh content (series continuation)")
    print("=" * 80)

if __name__ == "__main__":
    main()