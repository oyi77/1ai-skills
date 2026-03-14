#!/usr/bin/env python3
"""
Phase 2 Planner - Transition to Paid Products (Day 16 onwards)
After 15 days foundation, introduce entry-level paid product
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

# Products for Phase 2
# Main product: Starter AI Content (Rp 49.000)
# Supporting: GRATIS products (warm up leads)

PRODUCTS = {
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "priority": "warmup",
        "role": "lead magnet & education",
        "price": "GRATIS",
        "url": "https://lnkd.in/gurupintarai",
        "hashtags": "#free #AItraining #belajarAI #education #AIindonesia",
        "cta": "100% FREE - Training lengkap"
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "priority": "support",
        "role": "utility & engagement",
        "price": "GRATIS",
        "url": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "hashtags": "#cashback #belanja #hemat #smartshopping",
        "cta": "GRATIS tips & strategy"
    },
    "starter_ai_content": {
        "name": "AI Content Pro (Entry Level)",
        "priority": "main",
        "role": "primary selling",
        "price": "Rp 89.000",
        "url": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #productivity #business #efficiency",
        "cta": "Full automation - Rp 89.000"
    }
}

# Entry level product (focus day 16-30) - rename for clarity
ENTRY_PRODUCT = {
    "name": "Starter AI Content (Entry Level)",
    "original": "ai_content_pro",
    "price": "Rp 49.000",
    "url": "https://lynk.id/jendralbot/d70eo2x45em5",
    "hashtags": "#AIcontent #AIautomation #contentcreation #AIbeginner"
}

# Product cycle for 6-hour blocks (rotating)
SALES_CYCLE = [
    "starter_ai_content",  # Entry level (main focus Day 16-30)
    "studio_marketplace_pro",
    "mesin_cetak_kuliner"  # Add these ke cycle for later
]

def generate_day_schedule(day):
    """Generate daily schedule for Phase 2"""
    
    date = datetime.now() + timedelta(days=day)
    date_str = date.strftime("%Y-%m-%d")
    
    schedule = {
        "date": date_str,
        "phase": "Transition - Entry Level Sales",
        "day": day + 16,  # Day 16 relative to start
        "strategy": "70% Sales + 30% Education (transition from free to paid)",
        "products": ["starter_ai_content"],  # Main focus now
        "posts": []
    }
    
    # 15 posts per day (every ~2.4 hours = ~6 times per day)
    # For simplicity, let's use 12 posts per still like before, but now with MAIN product focus
    hours = list(range(0, 24, 2))  # 00:00 to 22:00 (12 posts)
    
    # Rotate: Entry level + FREE products mix
    for hour in hours:
        # 70% sales, 30% education phase 2 transition
        is_sales = (hour % 10 < 7)  # 7 sales, 3 education per 10 posts
        
        if is_sales:
            # Main product: Starter AI Content (Entry Level)
            # But keep some soft variety
            content_type = "hook" if hour % 3 == 0 else "benefit" if hour % 3 == 1 else "social_proof"
            post_type = "sales"
            product_key = "starter_ai_content"
        else:
            # Education: Mix FREE products
            post_type = "education"
            # Alternate between guru_pintar_ai and belanja_duit_balik
            product_key = "guru_pintar_ai" if hour % 4 == 2 else "belanja_duit_balik"
        
        # Generate caption
        if is_sales:
            post = generate_sales_post(product_key, content_type, hour, day)
        else:
            post = generate_education_post_phase2(product_key, hour, day+15)
        
        post["time"] = f"{hour:02d}:00"
        post["product"] = product_key
        schedule["posts"].append(post)
    
    return schedule

def generate_sales_post(product_key, content_type, hour, day):
    """Generate sales post for Phase 2 (entry level)"""
    product = PRODUCTS.get(product_key, PRODUCTS["starter_ai_content"])
    
    sales_hooks = {
        "hook": {
            "caption": f"🔥 STOP! Konten manual makan waktu 4 jam/post!\n\nMasalahnya:\n• Ide kosong → nunggu 2 jam\n• Writing → 1 jam\n• Editing → 45 menit\n• Publishing → 15 menit\n\nTotal: 4 jam = 1 post! 😱\n\nSolusinya: {product['name']} ({product['price']})\n\n✨ Ide: 5 detik via AI\n⚡ Caption: 1 menit\n🎨 Image: 1 menit\n⏰ Share: 1 menit\n\nTOTAL: 8 menit untuk kualitas premium!\n\n💰 Investasi: {product['price']} → Save 3.5 jam/post\n\nKembal ROI: 50x lipat dalam 1 bulan!\n\n👉 {product['url']}\n\n{product['hashtags']}\n\n#AIcontent #AIautomation #productivity #contentcreation #AIbeginner"
        },
        "benefit": {
            "content": f"⭐ Kunci {product['name']}:\n\n⭐ Fitur 1: AI Content Generator (infinite ideas)\n\"Bisa generate ide konten dalam SATU JAM!\n⭐ Fitur 2: AI Caption Writer (caption natural & engaging)\n\"Bikin caption TikTok-ready dalam hitungan detik!\n⭐ Fitur 3: Hashtag Research (trending + niche)\n\"Bisa 50+ hashtags relevan dalam 1 klik!\n⭐ Fitur 4: Image Suggestions (match brand style)\n\"Gak perlu skill desain lagi!\n⭐ Fitur 5: PostBridge Integration (auto posting ke 5 platform)\n\"Tinggal set schedule, jadi auto!\n\n\n📊 Sebelum {product['name']}:\n- 1 post every 4 days\n- Manual: 4 posts/bulan\n- Growth: 0-5 followers/month\n\n📊 Sesudah {product['name']}:\n- 90 posts/month (daily auto)\n- Growth: 200-500 followers/month\n\nGrowth: 40x lebih cepat! 🚀\n\n💰 {product['price']} = 1 jam kerja (jika bayar freelance atau investasi skill)\n\n👉 Coba sekarang: {product['url']}\n\n{product['hashtags']}"
        },
        "social_proof": {
            "caption": f"\"Alhamdulillah! Order naik 300% dalam 1 bulan!\" 🎉\n\nTestimoni pelanggan {product_name}:\n\nSaya sebelumnya:\n❌ Hanya bisa bikin 2-3 konten/bulan (manual)\n❌ Growth stagnan di 10 followers\n❌ Capek & burnout editing\n\nSekarang pakai:\n✅ Bis postinganan 2-3 post/hari (auto)\n✅ Growth jadi rame 10-20 followers/bulan\n✅ Engagement naik 300%\n✅ Saya kangen bisa focus di revenue instead!\n\n💰 {product['price']} = Invest kecil untuk 400-500% growth!\n\n\"Kesimpulan: Buat kamu bisa focus di bisnis, bukan di editing!\" 💪\n\n👉 {product['url']}\n\n{product['hashtags']}"
        },
        "comparison": {
            "content": f"📊 Comparison: Manual vs {product['name']} - Harga & ROI\n\n📉 MANUAL CONTENT CREATION:\nFreelance editor: Rp 500k/bulan\n4 jam/post × 10 post = 40 jam\nBiasa: 2-3 post/bulan hasilnya\n\nTotal biaya: Rp 500.000/bulan\nHasil: 6-10 post/bulan\nCost: Rp 50k-83k/post\n\n🤖 {product['name']}:\n💰 Harga: {product['price']}\nGenerasi: UNLIMITED\nHasil: 30-90 post/bulan\nCost per post: Rp 1.000-3.000\n\n💰 Total biaya: Rp 89.000 (one-time)\n→ Break even hanya di bulan 3-4!\n\n📊 OUTPUT PER BULAN:\nManual: 6-10 posts → Revenue Rp 300k-500k (asumsi Rp 50k/post)\n{product_name}: 30-90 posts → Revenue: (30-90 × Rp 50k) - Rp 89.000 = Rp 1.4M - Rp 4.2M\n\nROI: 15-50x dalam bulan pertama!\nROI ke-60 tahun! 🚀\n\n\"Efisiensi = ((1.400.000-4.200.000) - 89.000) / 89.000 → 15-47x ROI!\n\n👉 Coba: {product['url']}\n\n{product['hashtags']}"
        },
        "urgent": {
            "content": f"🎯 LIMITED TIME: SPECIAL FOUNDATION PRICE!\n\n📦 {product['name']}\n\nHarga normal: Rp 150.000 (bundled)\n\n🎁 FOUNDATION PRICE: Rp 89.000 (50% OFF!)\n\nBukan diskon sementara, ini FOUNDATION PRICE selam-lamanya!\n\nBatas Waktu: 30 post tanggal dari sekarang!\n\n⏰ Aman? Investasi cuma {product['price']} bisa kembali full dalambulan jika gak cocok (refunds available for 7 days)\n\n👉 Ambil sekarang sebelum habis! {product['url']}\n\n{product['hashtags']}\n\n#limitedoffer #special #foundprice #discount #AItools #productivity #lastchance"
        }
    }
    
    hook = sales_hooks[content_type]
    
    return {
        "type": "sales",
        "variant": content_type,
        "caption": hook["caption"],
        "product": product_key
    }

def generate_education_post_phase2(product_key, hour, day):
    """Generate education post for Phase 2 (now supporting paid products)"""
    product = PRODUCTS[product_key]
    
    # 5-day education series for products
    series_cycles = {
        "guru_pintar_ai": {
            1: "AI Content 101 - Foundation (Review)",
            2: "Tools AI wajib untuk pemula",
            3: "Skill AI bisa digenerate: Writing, Image, Video, Audio",
            4: "Cara pakai: Step-by-Step praktis {PRODUCTS['starter_ai_content']['name']}",
            5: "Roadmap: Dari Beginner ke Pro dalam 6 bulan"
        },
        "belanja_duit_balik": {
            1: "Cashback Foundation (Review)",
            2: "Strategy: Stacking Cashback - Triple Trick",
            3: "Kalkulator: Hemat berapa per hari/bulan?",
            4: "Hidden Gems: Cashback di platform kecil",
            5: "Advanced: Traveloka + Trip.com strategy"
        }
    }
    
    # For education, we still promote Guru Pintar AI even in Phase 2
    edukasi_data = {
        "guru_pintar_ai": {
            1: "Review: Apa yang sudah dipelajari di Day 1-15?",
            2: "Tools AI yang sudah kalian belajar sekarang",
            3: "Mistakes yang sering dilakukan pemula ketika belajar AI",
            4: "Tips: Konsistensi belajar (hari ini 20 menit, besok 30 menit)",
            5: "Next Level: Kapan naik ke Starter AI Content?"
        }
    }
    
    # Select series day (cycle of 5)
    day_key = f"day_{(day-1) % 5 + 1}"  # Day cycle through 1-5
    
    # Get education theme
    if product_key in edukasi_data:
        theme = edukasi_data[product_key][day_key]
        
        if product_key == "guru_pintar_ai":
            caption = f"""📖 REVIEW DAY {day} - {theme}

---

HARI 1-15: SUDAH LEARNING APA?

Quick review apa yang sudah dipelajari di series 15 hari ini!

---

✅ Foundation:
→ Apa itu AI? Definisi & konsep dasar AI
→ AI vs Manual - Sama atau beda?
→ Tools AI wajib dipelajari (TOP 5)
→ Skill AI yang bisa digenerate AI

✅ Practice:
→ Sudah mulai belajar? Apa tools AI yang sudah dipakai?
→ Hasilnya seperti apa?

---

🤔 SUDAH BISA PRAKTIK?

✨ Generate ide konten → Coba ChatGPT (GRATIS)
✨ Caption writing → Coba {PRODUCTS['starter_ai_content']['name']} (trial 14 hari)
✨ Image creation → Canva (GRATIS) / DALL-E (limited free credits)

---

💡 KEUNTUKAN YANG SUDAH BELAJAR:

1. Understanding AI limits (gak bisa apa aja)
2. Quality control (AI need human review)
3. Consistency (post reguler, bukan random)

---

📚 MULAI LEVEL UP!

Kalau sudah mulai praktik dan MAU:
→ {PRODUCTS['starter_ai_content']['name']} → Otomatisasi full workflow
→ Belajar 1 bulan = jadi 10x-20x produktifitas

💬 Komen: "Sudah coba AI tools sebelum? Share pengalaman kamu!"

---

📖 Besok: Tools AI yang Wajib Dipelajari (Top 5) - ULTIMATE GUIDE!

{PRODUCTS['guru_pintar_ai']['hashtags']}
#AIeducation #review #AI #productivity #growth #belajarAI
"""
    
    elif product_key == "belanja_duit_balik":
        # Use Guru Pintar AI for education in Phase 2
        caption = f"""📖 {theme} - Day {day}/Advanced

---

PENGALAMAN CASHBACK - LEVEL ADVANCED!

---

Di Hari 1-15: kita sudah cover BASIC cashback:
✅ Shopee double cashback timing
✅ Stacked cashback strategy (triple trick)
✅ Kartu bank dengan bonus cashback

Hari 16-30: LEVEL UP dengan ADVANCED!

---

🎯 Hari ini: {theme}

---

ADVANCED TOPICS:
→ Stack 4+ aplikasi sekaligus (ROI 15-30%!)
→ Taktik kalender promo (best shoper double cashback)
→ Credit card bonus cycle optimization
→ Platform comparison: Shopee vs Tokopedia vs Tokopedia Promo
→ Traveloka + Trip.com stacking

---

💬 SHARE TESTIMONI:

User A (Pemula):
• Belanja: 500k/bulan\n• Dapat: 50k cashback/month\n• Setelah kalkulator: Hemat 600k/tahun!\n• Alhamdulillah, gampang banget!

User B (Intermediate):
• Belanja: 2jt/bulan\n• Dapat: 200k cashback/month\n• Setelah kalkulator plus advanced tricks: Hemat 2.400k/tahun!
• "Saya bisa liburan 3x tahun dari cashback!"

User C (Expert):
• Belanja: 5jt/bulan
• Dapat: 500k cashback/month\n• Semua stacking tips dipraktikin
• "Revenue + cashback = 3x lipat! 15jt revenue jadi 45jt!"

---

💡 Cek kalkulator harian ini:
https://lynk.id/jendralbot/kzryk28dxmpx

---

💬 Punya pengalaman advanced? Share di komentar!

👉 {PRODUCTS['belanja_duit_balik']['url']}
GRATIS informasi lengkap! 💰

{PRODUCTS['belanja_duit_balik']['hashtags']}
#cashback #advanced #stacking #tips #GRATIS #hemat #belanja #smartshopping
"""
    
    else:
        caption = f"Education about {product['name']}"

Series info = series_cycles.get("guru_pintar_ai", {})
    day_info = series_info.get(f"day_{(day-1) % 5 + 1}", "Advanced AI topic")
    
    caption = f"""📚 Series Part {day}/{5} - {day_info}

Learn: {day_info}

Complete tutorial at: {product['url']}

{product['hashtags']}
"""
    
    return caption

def generate_day_schedule_all_phase2():
    """Generate complete Phase 2 schedule (15 days: Day 16-30)"""
    all_days = []
    
    for day in range(15):  # Day 16-30
        day_schedule = generate_day_schedule(day)
        all_days.append({
            "day_number": day + 16,
            "date": day_schedule["date"],
            "schedule": day_schedule
        })
    
    return all_days

def main():
    print("=" * 80)
    print("📅 PHASE 2 PLANNER - ENTRY LEVEL SALES")
    print("=" * 80)
    print()
    print("Phase: Transition (Hari 16-30)")
    print("Main Product: Starter AI Content Entry Version (Rp 49.000)")
    print("Supporting: Guru Pintar AI + Belanja Duit Balik (warm up)")
    print("Strategy: 70% Sales + 30% Education (building on trust)")
    print()
    
    # Generate Phase 2 schedules
    all_days = generate_day_schedule_all_phase2()
    
    # Save all
    workspace = Path.home() / ".openclaw" / "workspace"
    phase2_file = workspace / "phase2_entry_level_schedule.json"
    with open(phase2_file, "w") as f:
        json.dump(all_days, f, indent=2)
    
    # Show Day 16 (first day of Phase 2)
    day16 = all_days[0]
    
    print("=" * 80)
    print("📋 SAMPLE: DAY 16 (Transition Day!)")
    print("=" * 80)
    print(f"Date: {day16['date']}")
    print()
    
    for post in day16["schedule"]["posts"][:10]:  # Show first 10 posts
        icon = "💰" if post['type'] == 'sales' else '📚'
        product_name = post['product'].replace('ai_content_pro', '')  # Clean up the name
        product_display = product_name.strip() or post['product'].title()
        
        print(f"{icon} {post['time']} - {post['type'].upper():7s} - {product_display}")
        
        if post['type'] == 'sales':
            print(f"   Variant: {post['variant']}")
        
        print(f"   Caption preview: {post['caption'][:80]}...")
        print()
    
    print("=" * 80)
    print("📊 PHASE 2 SUMMARY")
    print("=" * 80)
    
    total_posts = sum(len(d["schedule"]["posts"]) for d in all_days)
    total_sales = sum(1 for d in all_days for p in d["schedule"]["posts"] if p["type"]=="sales")
    total_edu = total_posts - total_sales
    
    print(f"Duration: Day 16 to Day {15+15} (15 days)")
    print(f"Total Posts: {total_posts}")
    print(f"Sales Posts: {total_sales} (~70%)")
    print(f"Education Posts: {total_edu} (~30%)")
    print()
    
    print("💡 PHASE 2 GOALS:")
    print("1. Introduce entry level product (Starter AI Content)")
    print("2. Capture early adopters (risk-taker buyers)")
    print("3. Generate revenue dari produk benerharga"))
    print("4. Build proof of concept (social proof for Phase 3)")
    print("5. Prepare scaling ke Phase 3 (mid tier products)")
    print()
    
    print("💼 EXPECTED OUTCOMES Phase 2 (Weeks 3-6):")
    print("- Followers: +1000-2000 (continuing growth)")
    print("- Paid customers: 20-50 new customers")
    "- Revenue: Rp 1-3 juta (cumulative dari produk Rp 49k × 20-50)")
    print("- Engagement: Medium (education still engages, sales converts)")
    print("- Leads: 50-100 (Guru Pintar AI signups for Phase 2)")
    print()
    
    print("=" * 80)
    print("✅ Phase 2 plan saved to: phase2_entry_level_schedule.json")
    print()
    print("📋 NEXT:")
    print("1. Review Phase 2 schedule")
    print("2. Create captivating visual content for entry level product")
    "3. Post via PostBridge (12 posts/day)")
    print("4. Track sales & customer feedback")
    print("5. Adjust strategy based on results")
    print("=" * 80)

    print("=" * 80)
    print("⚠️ TRANSITION TIPS:")
    print("=" * 80)
    print("✅ Mention trust built in Phase 1 (education consistency)")
    print("✅ Highlight value proposition (Rp 49k = full month subscription)")
    print("✅ Use testimonials from Phase 1 soft sales")
    print("❌ Don't hard sell - soft & helpful approach still")
    print("✅ Keep education 5-15 day series going")
    print("✅ Continue soft sells for FREE products (keep warm leads coming)")
    print("=" * 80)

if __name__ == "__main__":
    main()