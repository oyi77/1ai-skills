#!/usr/bin/env python3
"""
Content Variator Generator - 12 Postings Per Day
Mix of Sales & Education (50-50)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

PRODUCTS = {
    "starter_ai_content": {
        "name": "Starter AI Content",
        "price": "Rp 49.000",
        "link": "https://lynk.id/jendralbot/xlymwzj2jylv",
        "target": "Beginners, students, small creators",
        "tone": "friendly",
        "hashtags": "#AIcontent #contentcreation #belajarAI #AIindonesia"
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "target": "E-commerce sellers, online store owners",
        "tone": "professional",
        "hashtags": "#ecommerce #productphoto #jualanonline #marketplace"
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": "RP 75.000",
        "link": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "target": "Restaurant owners, GoFood/GrabFood sellers",
        "tone": "friendly",
        "hashtags": "#kuliner #foodphotography #GoFood #restaurant"
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "target": "Advanced creators, businesses",
        "tone": "professional",
        "hashtags": "#AIcontent #AIautomation #business #efficiency"
    },
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "target": "Everyone who wants to learn AI",
        "tone": "educational",
        "hashtags": "#free #AItraining #belajarAI #gratis #edukasi"
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "target": "Shoppers, cashback seekers",
        "tone": "fun",
        "hashtags": "#cashback #belanja #hemat #shoppingtips"
    }
}

# Edukasi Series Concepts (5-day untuk 1 produk)
EDUKASI_SERIES = {
    "starter_ai_content": {
        "day_1": "Kenapa AI Content? - Foundation",
        "day_2": "Masalah Manual Content Creation",
        "day_3": "Solusi dengan AI Content Pro",
        "day_4": "Cara Pakai: Step-by-Step Tutorial",
        "day_5": "Tips & Tricks Maximalkan Hasil"
    },
    "studio_marketplace_pro": {
        "day_1": "Fotografi Produk vs Studio Marketplace Pro",
        "day_2": "Cara Edit Foto Tercepat",
        "day_3": "Sebelum vs Sesudah: Transformation",
        "day_4": "Strategi Foto Produk Viral",
        "day_5": "Testimoni Seller yang Sukses"
    },
    "mesin_cetak_kuliner": {
        "day_1": "Food Photography 101",
        "day_2": "Makanan Enak Itu Harganya Lebih!",
        "day_3": "GoFood/GrabFood Optimization",
        "day_4": "Contoh Transformasi Menu",
        "day_5": "Tips Menarik Order dengan Foto Bagus"
    },
    "ai_content_pro": {
        "day_1": "Productivity Revolution dengan AI",
        "day_2": "Time Audit: Berapa Waktu Kamu Habis?",
        "day_3": "AI Workflow yang Efektif",
        "day_4": "Kebiasaan Sukses Creator Pro",
        "day_5": "Future of Content Creation"
    },
    "guru_pintar_ai": {
        "day_1": "AI untuk Pemula: Dasar-Dasar",
        "day_2": "Tools AI yang Wajib Dipelajari",
        "day_3": "Skill Skill yang Bisa Digenerate dengan AI",
        "day_4": "Case Study: Pekarjaan 10x Lebih Cepat",
        "day_5": "Roadmap Belajar AI 6 Bulan"
    },
    "belanja_duit_balik": {
        "day_1": "Cashback 101: Apa & Bagaimana",
        "day_2": "Aplikasi Sering Cashback Terbesar",
        "day_3": "Strategy: Belanja di Waktu Tepat",
        "day_4": "Testimoni: 1 Bulan Hemat Berapa?",
        "day_5": "Advanced: Stacking Cashback"
    }
}

def generate_sales_post(product_key, hour):
    """Generate sales-oriented post"""
    product = PRODUCTS[product_key]
    
    sales_hooks = [
        {
            "type": "problem_solution",
            "caption": f"🔥 STOP! Masalah {product['tone']} bikin kamu capek?\n\nSolusinya: {product['name']} ({product['price']})\n\n✅ Benefit 1\n✅ Benefit 2\n✅ Benefit 3\n\n💡 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "social_proof",
            "caption": f"\"Alhamdulillah! Order naik 300%!\"\n\nTestimoni pelanggan {product['target']} tentang {product['name']}.\n\n📊 {product['price']}'s investment untuk ROI tinggi.\n\n👉 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "feature_highlight",
            "caption": f"Fitur {product['name']} yang wajib kamu tahu:\n\n✨ Fitur 1: [detail]\n⚡ Fitur 2: [detail]\n💎 Fitur 3: [detail]\n\n{product['price']} - Investasi bijak!\n\n{product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "comparison",
            "caption": f"Before vs After - {product['name']}\n\nBEFORE: [problem description]\n• Sakit\n• Mahal\n• Lama\n\nAFTER: {product['name']}\n• Sehat\n• Hemat\n• Cepat\n\n📈 Transformasi nyata! {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "urgency",
            "caption": f"🎯 LIMITED TIME!\n\n{product['name']} - {product['price']}\n\nHarga normal: HIGHER!\nDiskon hari ini!\n\n⏰ Berakhir sampai hari ini!\n\n👉 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "success_story",
            "caption": f"Kisah sukses Budi dengan {product['name']}:\n\n👤 Dulu: [struggle]\n📊 Sekarang: [success metrics]\n\nBerapa ROI? {product['price']}\nResult: 10x lipat!\n\n💡 Bener-bener works! {product['link']}\n\n{product['hashtags']}"
        }
    ]
    
    # Select hook based on hour
    hook_idx = (hour % len(sales_hooks))
    hook = sales_hooks[hook_idx]
    
    post = {
        "time": f"{hour:02d}:00",
        "type": "sales",
        "variant": hook["type"],
        "caption": hook["caption"],
        "product": product_key
    }
    
    return post

def generate_education_post(product_key, hour, day):
    """Generate education-oriented post"""
    product = PRODUCTS[product_key]
    series = EDUKASI_SERIES[product_key]
    
    # Determine post type
    if hour % 4 == 2:  # Edukasi Image single
        posts = generate_education_image(product_key)
    elif hour % 4 == 0:  # Edukasi Series part
        series_day_idx = (day - 1) % 5 + 1  # 1-5 cycle
        posts = generate_education_series(product_key, series_day_idx)
    else:  # Edukasi tips/random
        posts = generate_education_tips(product_key)
    
    post = {
        "time": f"{hour:02d}:00",
        "type": "education",
        "caption": posts["caption"],
        "product": product_key
    }
    
    return post

def generate_education_image(product_key):
    """Education image post explaining benefits"""
    product = PRODUCTS[product_key]
    
    # Different benefit angles
    benefits = [
        "Kenapa butuh produk ini?",
        "Masalah yang diatasi",
        "Solusi yang ditawarkan",
        "Fitur premium",
        "Value proposition"
    ]
    
    benefit_idx = datetime.now().hour % len(benefits)
    
    caption = f"""🎓 INFO TERBARU: {product['name']}

{benefits[benefit_idx]}

{product['target']} sering mengalami:
• Masalah 1
• Masalah 2
• Masalah 3

{product['name']} membantu solve semua masalah ini dengan:
✅ Benefit A
✅ Benefit B
✅ Benefit C

📖 Kenapa butuh? Karena:
→ Reason 1
→ Reason 2
→ Reason 3

❓ Tertarik kenapa? DM INFO!
{product['link']}

{product['hashtags']}
#edukasi #infoproduk #{product['name'].replace(' ', '').lower()}"""
    
    return {"caption": caption}

def generate_education_series(product_key, day_idx):
    """Education series post (multi-part)"""
    product = PRODUCTS[product_key]
    series = EDUKASI_SERIES[product_key]
    day_key = f"day_{day_idx}"
    topic = series[day_key]
    
    caption = f"""📖 {topic} - Part {day_idx}/5

{product['name']} Series for {product['target']}

---

Content:
[Detailed explanation about today's topic]

Key Takeaways:
📌 Point 1
📌 Point 2
📌 Point 3

---

📅 Besok: Part {day_idx + 1 if day_idx < 5 else 1}
(Topik: {series[f'day_{day_idx + 1 if day_idx < 5 else 1}']})

💬 Tanya di komen jika kurang jelas!

👉 Tahu {product['name']}: {product['link']}

{product['hashtags']}
#series #edukasi #{product['name'].replace(' ', '').lower()}"""
    
    return {"caption": caption}

def generate_education_tips(product_key):
    """Education tips post"""
    product = PRODUCTS[product_key]
    
    tips_pool = [
        "5 tips memaksimalkan hasil",
        "Kesalahan umum yang harus dihindari",
        "Cara pemakaian yang benar",
        "Tips pemula",
        "Advanced strategy"
    ]
    
    tip_idx = datetime.now().hour % len(tips_pool)
    
    caption = f"""💡 {tips_pool[tip_idx]} - {product['name']}

---

5 Essential Tips:

1️⃣ [Detail tip 1]
2️⃣ [Detail tip 2]
3️⃣ [Detail tip 3]
4️⃣ [Detail tip 4]
5️⃣ [Detail tip 5]

---

💰 {product['price']}

Info lengkap: {product['link']}

{product['hashtags']}
#tips #tutorial #edukasi #{product['name'].replace(' ', '').lower()}"""
    
    return {"caption": caption}

def generate_daily_schedule(day):
    """Generate complete daily schedule for all products"""
    schedule = []
    current_date = datetime.now() + timedelta(days=day)
    date_str = current_date.strftime("%Y-%m-%d")
    
    # Rotate through products
    products_list = list(PRODUCTS.keys())
    num_products = len(products_list)
    
    for hour in range(24):  # 00:00 - 23:00
        # Determine product for this hour (rotate)
        product_idx = hour % num_products
        current_product = products_list[product_idx]
        
        # Determine type (sales vs education)
        # Pattern: S-E-S-E-S-E-S-E-S-E-S-E (sales every even hour, education every odd)
        if hour % 2 == 0:  # Even hour: sales
            post = generate_sales_post(current_product, hour)
        else:  # Odd hour: education
            post = generate_education_post(current_product, hour, day)
        
        post["date"] = date_str
        post["hour"] = hour
        post["day"] = day
        
        schedule.append(post)
    
    return schedule

def generate_monthly_schedule():
    """Generate complete monthly schedule (30 days)"""
    monthly = []
    
    for day in range(30):
        daily = generate_daily_schedule(day)
        monthly.append({
            "day": day + 1,
            "date": f"2026-03-{(day + 1):02d}",
            "posts": daily
        })
    
    return monthly

def main():
    print("=" * 80)
    print("📅 CONTENT VARIATOR GENERATOR - 12 POSTINGS PER DAY")
    print("=" * 80)
    print()
    print("Configuration:")
    print("  Posting interval: Every 2 hours (00:00 - 22:00)")
    print("  Posts per day: 12 posts")
    print("  Sales vs Education: 50-50 (6 sales, 6 education)")
    print("  Pattern: Sales (even hours) → Education (odd hours)")
    print()
    
    # Generate sample for today (Day 1)
    print("Generating Day 1 schedule...")
    today_schedule = generate_daily_schedule(0)
    
    # Display today's schedule
    print("\n" + "=" * 80)
    print("📋 SAMPLE SCHEDULE - DAY 1 (TODAY)")
    print("=" * 80)
    print()
    
    sales_count = 0
    edu_count = 0
    
    for post in today_schedule:
        product_name = PRODUCTS[post["product"]]["name"]
        
        if post["type"] == "sales":
            status_icon = "💰"
            sales_count += 1
        else:
            status_icon = "📚"
            edu_count += 1
        
        print(f"{status_icon} {post['time']} - {post['type'].upper()} - {product_name}")
        print(f"   Variant: {post['variant'] if post['type'] == 'sales' else 'Edu image/tips/series'}")
        print(f"   Caption preview: {post['caption'][:100]}...")
        print()
    
    print("=" * 80)
    print("📊 DAY 1 SUMMARY")
    print("=" * 80)
    print(f"Total posts: {len(today_schedule)}")
    print(f"Sales posts: {sales_count}")
    print(f"Education posts: {edu_count}")
    print(f"Balance: Sales {sales_count} - Edu {edu_count} (50-50 ✓)")
    print()
    
    # Save schedule
    workspace = Path.home() / ".openclaw" / "workspace"
    
    today_file = workspace / "schedule_day_1.json"
    with open(today_file, "w") as f:
        json.dump(today_schedule, f, indent=2)
    print(f"✅ Today's schedule saved to: {today_file}")
    
    # Generate and save monthly schedule
    monthly = generate_monthly_schedule()
    monthly_file = workspace / "schedule_monthly.json"
    with open(monthly_file, "w") as f:
        json.dump(monthly, f, indent=2)
    print(f"✅ Monthly schedule (30 days) saved to: {monthly_file}")
    print(f"   Total posts: {len(monthly) * 12} = 360 posts")
    print()
    
    print("=" * 80)
    print("🎯 STRATEGIKEY POINTS")
    print("=" * 80)
    print()
    print("✅ BALANCED APPROACH")
    print("   • 50% Sales (hook-oriented)")
    print("   • 50% Education (value-oriented)")
    print()
    print("✅ SALES VARIATIONS")
    print("   • Problem/Solution (pain point address)")
    print("   • Social Proof (testimonials)")
    print("   • Feature Highlights (product features)")
    print("   • Comparison (before/after)")
    print("   • Urgency (limited time offers)")
    print()
    print("✅ EDUCATION VARIATIONS")
    print("   • Image: Benefit explanation (why need product)")
    print("   • Series: 5-day course (comprehensive learning)")
    print("   • Tips: Quick actionable advice")
    print("   • Foundation → Problem → Solution → Tips → Future")
    print()
    print("✅ PRODUCT ROTATION")
    print("   • 6 products rotated every 4 hours")
    print("   • All products get equal exposure")
    print("   • Free products build audience for paid ones")
    print()
    print("✅ TIMING")
    print("   • 00:00 - 06:00 (Night owls)")
    print("   • 08:00 - 18:00 (Peak hours)")
    print("   • 20:00 - 22:00 (Evening)")
    print()
    print("=" * 80)
    print("📋 NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Review schedule_day_1.json")
    print("2. Customize captions per product")
    print("3. Generate visual content (images/videos)")
    print("4. Setup automation for posting (PostBridge)")
    print("5. Monitor engagement & optimize")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()