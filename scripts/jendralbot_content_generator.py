#!/usr/bin/env python3
"""
JENDRALBOT MARKETING AUTOMATION - V2
─────────────────────────────────────────────────────────────
Full content generation with complete placeholder replacement
"""

import json
from datetime import datetime, timedelta
import random

PRODUCTS = {
    "starter_ai_content": {
        "name": "Starter AI Content",
        "price": 49000,
        "link": "https://lynk.id/jendralbot/xlymwzj2jylv",
        "category": "Entry Level",
        "keywords": ["pemula", "AI content", "belajar AI", "content creation", "beginner"],
        "pain_points": ["Susah bikin konten", "Makan waktu", "Tidak ide tulisan", "Bingung mulai dari mana"],
        "benefits": ["Mudah dipakai", "Harga terjangkau", "Upgrade-ready", "Support penuh"],
        "hashtags": ["#AIcontent", "#contentcreation", "#starter", "#AIindonesia", "#belajarAI"]
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": 75000,
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "category": "Mid Tier",
        "keywords": ["ecommerce", "product photo", "marketplace", "online store", "TOKOPEDIA"],
        "pain_points": ["Foto produk jelek", "Jualan sepi", "Biaya fotografer mahal", "Editing lama"],
        "benefits": ["Foto profesional", "Cepat & praktis", "Boost konversi", "Jaminan kualitas"],
        "hashtags": ["#ecommerce", "#onlinestore", "#productphoto", "#marketplace", "#AIbusiness"]
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": 75000,
        "link": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "category": "Mid Tier",
        "keywords": ["kuliner", "food photography", "restaurant", "GoFood", "GrabFood"],
        "pain_points": ["Foto makanan kurang menarik", "Order sepi", "Value order rendah", "Competitor terlihat lebih premium"],
        "benefits": ["Food aesthetic", "Tingkatkan value", "Profesional tanpa fotografer", "Instant results"],
        "hashtags": ["#kuliner", "#foodphotography", "#GoFood", "#GrabFood", "#restaurant"]
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": 89000,
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "category": "Premium",
        "keywords": ["AI content pro", "professional", "business", "automation", "scale"],
        "pain_points": ["Bikin konten manual lama", "Bakar budget desainer", "Competitor lebih cepat", "Gak scale"],
        "benefits": ["Otomatisasikan konten", "Kualitas premium", "Save time 80%", "ROI tinggi"],
        "hashtags": ["#AIcontent", "#professional", "#business", "#AIautomation", "#efficiency"]
    },
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": 0,
        "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "category": "FREE Training",
        "keywords": ["belajar AI", "training gratis", "AI course", "pintar AI", "learn AI"],
        "pain_points": ["Bingung cara pakai AI", "Takut ketinggalan", "Mau upgrade skill", "Belum ada arahan"],
        "benefits": ["Gratis tanpa biaya", "Training lengkap", "Step-by-step", "Support komunitas"],
        "hashtags": ["#free", "#AItraining", "#belajarAI", "#gratis", "#AIindonesia"]
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": 0,
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "category": "FREE Cashback",
        "keywords": ["cashback", "belanja", "hemat", "duit balik", "shopping"],
        "pain_points": ["Belanja habis aja", "Gak dapat apa-apa", "Dompet kering", "Gak ada tips hemat"],
        "benefits": ["Cashback otomatis", "Belanja tetap, dapat duit", "Tips hemat", "Rahasia shopper cerdas"],
        "hashtags": ["#cashback", "#belanja", "#hemat", "#duitbalik", "#shoppingtips"]
    }
}

ACTIONS = [
    "Mulai dengan 1 konten saja",
    "Coba 1 fitur, suka lanjut",
    "Testimonial pelanggan kami",
    "Transformasi sebelum vs sesudah",
    "Tips rahasia dari pro"
]

TIMELINES = [
    "Dulu 4 jam, sekarang 1 menit",
    "Dulu ribet, sekarang satu klik",
    "Dulu mahal, sekarang terjangkau",
    "Dulu manual, sekarang otomatis"
]

TESTIMONIALS = [
    "\"Dulu susah bikin konten, sekarang 5 menit selesai!\" - Andi, Creator",
    "\"Foto produk saya jadi super premium, konversi naik 300%!\" - Rina, Seller",
    "\"Makanan saya sekarang terlihat lebih jualan! Order naik.\" - Chef Budi",
    "\"Saya hemat 80% waktu bikin konten. Sangat recommended!\" - Dian, Entrepreneur",
    "\"Training gratis tapi lengkap banget! Baru paham AI.\" - Tono, Student"
]

def generate_tiktok_content(product):
    """Generate TikTok video script"""
    pain = random.choice(product["pain_points"])
    action = random.choice(ACTIONS)
    benefit = random.choice(product["benefits"])
    timeline = random.choice(TIMELINES)

    content = {
        "hook": f"🔥 STOP: {pain}?",
        "problem": f"Problem: {pain}\n\nIni bikin kamu frustrasi kan?",
        "solution": f"Solusinya: {product['name']}\n\n{benefit}",
        "result": f"{timeline}\n\n{action}",
        "cta": f"💡 Link di bio atau comment 'MAU'\n\n{product['link']}",
        "hashtags": " ".join(product["hashtags"])
    }
    return content

def generate_instagram_carousel(product):
    """Generate Instagram carousel structure"""
    pain = random.choice(product["pain_points"])
    benefit1 = product["benefits"][0] if len(product["benefits"]) > 0 else "Mudah dipakai"
    benefit2 = product["benefits"][1] if len(product["benefits"]) > 1 else "Cepat hasil"
    benefit3 = product["benefits"][2] if len(product["benefits"]) > 2 else "Kualitas terjamin"
    testimonial = random.choice(TESTIMONIALS)
    timeline = random.choice(TIMELINES)

    slides = [
        f"Slide 1: 🚨 Problem? {pain}\n\nKamu alamin ini?",
        f"Slide 2: 💡 Solusi: {product['name']}\n\n{benefit1}, {benefit2}, {benefit3}",
        f"Slide 3: 🔥 Hasil: {timeline}\n\n{product['link']}",
        f"Slide 4: ⭐ Testimoni:\n\n{testimonial}",
        f"Slide 5: 🎯 CTA: Tap link di bio!\n\n{product['name']} - Rp {product['price']:,}"
    ]

    content = {
        "slides": slides,
        "caption": f"{product['name']} - {product['category']}\n\n{slides[0]}\n\n{slides[1]}\n\n{slides[2]}\n\n{slides[3]}\n\n{slides[4]}\n\n{' '.join(product['hashtags'])}",
        "hashtags": " ".join(product["hashtags"])
    }
    return content

def generate_linkedin_post(product):
    """Generate LinkedIn post"""
    pain = random.choice(product["pain_points"])
    benefit = random.choice(product["benefits"])
    testimonial = random.choice(TESTIMONIALS)
    keyword = random.choice(product["keywords"])

    content = {
        "hook": f"🎯 Transformasi {product['category']} dengan {product['name']}",
        "body": f"""Saya melihat banyak para {keyword} mengalami:

❌ {pain}
❌ Kejar deadline
❌ Hasil gak maksimal

Ini bikin mereka burnout dan gak produktif.

Solusinya?

📦 {product['name']}
💰 Rp {product['price']:,}
🔗 {product['link']}

Keunggulan:
✅ {benefit}

📊 {testimonial}

Yang Anda dapatkan:
• {product['benefits'][0] if len(product['benefits']) > 0 else 'Mudah dipakai'}
• {product['benefits'][1] if len(product['benefits']) > 1 else 'Cepat hasil'}
• Support penuh kalau butuh bantuan""",
        "cta": f"📲 Comment 'INFO' kalau mau detail lengkap\n\n{product['link']}",
        "hashtags": " ".join(product["hashtags"])
    }
    return content

def generate_x_thread(product):
    """Generate X/Twitter thread"""
    pain = random.choice(product["pain_points"])
    benefit = random.choice(product["benefits"])
    testimonial = random.choice(TESTIMONIALS)
    timeline = random.choice(TIMELINES)

    tweets = [
        f"1/ 🧵 {product['name']} - {product['category']}\n\n🔥 {product['price']:,} rupiah\n\nKetahui bedanya... ↓",
        f"2/ 💀 Problem: {pain}\n\nBanyak orang alamin ini & stuck gak maju-maju.",
        f"3/ ✅ Solution: {product['name']}\n\n{benefit}\n\n{timeline}",
        f"4/ ⭐ Testimoni:\n\n{testimonial}",
        f"5/ 🔗 Coba sekarang:\n{product['link']}\n\nRT kalau bermanfaat! 🔄"
    ]

    content = {
        "tweets": tweets,
        "ct": f"1/ 🧵 {product['name']} - {product['category']}\n\n🔥 {product['price']:,} rupiah\n\nKetahui bedanya... ↓",
        "hashtags": " ".join(product["hashtags"])
    }
    return content

def generate_youtube_shorts_script(product):
    """Generate YouTube Shorts script"""
    pain = random.choice(product["pain_points"])
    action = random.choice(ACTIONS)
    benefit = random.choice(product["benefits"])
    timeline = random.choice(TIMELINES)

    content = {
        "hook": f"🔥 KALAU {pain.upper()}, TONTON INI!",
        "body": f"Dulu: {pain}\n\nSekarang: {product['name']}\n\n{benefit}\n\n{timeline}\n\n{action}",
        "cta": f"Link di deskripsi atau bio 👇\n{product['link']}",
        "hashtags": " ".join(product["hashtags"])
    }
    return content

def generate_content_plan(days=7):
    """Generate complete content plan"""
    plan = []

    for day in range(days):
        date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")

        # Each product gets different content type per platform
        for product_key, product in PRODUCTS.items():
            for platform in product.get("platforms", ["tiktok", "instagram"]):
                # Generate content based on platform
                if platform == "tiktok":
                    content = generate_tiktok_content(product)
                elif platform == "instagram":
                    content = generate_instagram_carousel(product)
                elif platform == "linkedin":
                    content = generate_linkedin_post(product)
                elif platform == "x":
                    content = generate_x_thread(product)
                elif platform == "youtube":
                    content = generate_youtube_shorts_script(product)
                else:
                    content = generate_tiktok_content(product)

                plan.append({
                    "date": date,
                    "platform": platform,
                    "product": product_key,
                    "content": content
                })

    return plan

def print_plan_summary(plan):
    """Print plan summary in readable format"""
    print("=" * 80)
    print("📊 JENDRALBOT CONTENT PLAN SUMMARY")
    print("=" * 80)
    print(f"Total Content: {len(plan)} items\n")

    # By product
    print("By Product:")
    for product_key, product in PRODUCTS.items():
        count = sum(1 for item in plan if item["product"] == product_key)
        print(f"  • {product['name']:25s} - {count:3d} content")

    # By platform
    print("\nBy Platform:")
    platforms = {}
    for item in plan:
        platform = item["platform"]
        platforms[platform] = platforms.get(platform, 0) + 1

    for platform, count in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {platform.upper():15s} - {count:3d} content")

    print("=" * 80)

def export_plan(plan, output_file="jendralbot_content_plan.json"):
    """Export plan to JSON"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    return output_file

def main():
    print("🚀 JENDRALBOT CONTENT GENERATOR V2")
    print("=" * 80)

    # Generate plan
    plan = generate_content_plan(days=7)

    # Export
    output_file = export_plan(plan)
    print(f"✅ Plan exported to: {output_file}\n")

    # Print summary
    print_plan_summary(plan)

    # Show sample
    print("\n" + "=" * 80)
    print("📋 SAMPLE CONTENT (First 3 items)")
    print("=" * 80)
    for i, item in enumerate(plan[:3]):
        print(f"\n{i+1}. {item['date']} - {item['platform'].upper()} - {PRODUCTS[item['product']]['name']}")
        print("─" * 80)
        for key, value in item['content'].items():
            if isinstance(value, list):
                print(f"{key.upper()}:")
                for j, slide in enumerate(value):
                    print(f"  [{j+1}] {slide}")
            else:
                print(f"{key.upper()}: {value}")
        print()

    print("=" * 80)
    print("✅ DONE! Check jendralbot_content_plan.json")
    print("=" * 80)

if __name__ == "__main__":
    main()