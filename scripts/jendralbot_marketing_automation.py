#!/usr/bin/env python3
"""
JENDRALBOT MARKETING AUTOMATION
─────────────────────────────────────────────────────────────
Full automation for promoting Jendralbot products
Author: OpenClaw AI
Date: 2026-03-07
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Product Configuration
PRODUCTS = {
    "starter_ai_content": {
        "name": "Starter AI Content",
        "price": 49000,
        "link": "https://lynk.id/jendralbot/xlymwzj2jylv",
        "category": "Entry Level",
        "target": "Beginners, students, small creators",
        "platforms": ["tiktok", "instagram", "linkedin"],
        "hashtags": ["#AIcontent", "#contentcreation", "#starter", "#AIindonesia", "#belajarAI"],
        "key_messages": [
            "Mulai perjalanan AI kamu dengan Rp 49k",
            "Perfect untuk pemula",
            "Upgrade-ready ketika butuh lebih"
        ]
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": 75000,
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "category": "Mid Tier",
        "target": "E-commerce sellers, online store owners",
        "platforms": ["tiktok", "instagram", "linkedin", "x"],
        "hashtags": ["#ecommerce", "#onlinestore", "#productphoto", "#marketplace", "#AIbusiness"],
        "key_messages": [
            "Foto produk profesional dalam detik",
            "Boost konversi toko online",
            "Hemat waktu, jual lebih banyak"
        ]
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": 75000,
        "link": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "category": "Mid Tier",
        "target": "Restaurants, GoFood/GrabFood sellers, foodies",
        "platforms": ["tiktok", "instagram", "linkedin", "x"],
        "hashtags": ["#kuliner", "#foodphotography", "#GoFood", "#GrabFood", "#restaurant"],
        "key_messages": [
            "Makananmu layak foto lebih bagus",
            "Tingkatkan nilai order dengan visual lebih baik",
            "Fotografi kuliner profesional tanpa fotografer"
        ]
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": 89000,
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "category": "Premium",
        "target": "Advanced creators, businesses, professionals",
        "platforms": ["tiktok", "instagram", "linkedin", "x", "youtube"],
        "hashtags": ["#AIcontent", "#professional", "#business", "#AIautomation", "#efficiency"],
        "key_messages": [
            "Berhenti bikin konten manual",
            "AI bikin dalam 1 menit",
            "Kualitas profesional tanpa desainer"
        ]
    },
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": 0,
        "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "category": "FREE",
        "target": "Everyone who wants to learn AI",
        "platforms": ["tiktok", "instagram", "linkedin", "x"],
        "hashtags": ["#free", "#AItraining", "#belajarAI", "#gratis", "#AIindonesia"],
        "key_messages": [
            "Mulai belajar AI sekarang - GRATIS",
            "Training lengkap tanpa biaya",
            "Lihat nilainya sebelum beli"
        ]
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": 0,
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "category": "FREE",
        "target": "Shoppers, cashback seekers",
        "platforms": ["tiktok", "instagram", "x"],
        "hashtags": ["#cashback", "#belanja", "#hemat", "#duitbalik", "#shoppingtips"],
        "key_messages": [
            "Belanja tapi dapat duit balik",
            "Tips hemat belanja online",
            "Cashback otomatis setiap belanja"
        ]
    }
}

# Content Templates
CONTENT_TEMPLATES = {
    "tiktok_demo": {
        "hook": "🔥 {product_name} IN ACTION",
        "body": "Ini yang bisa {product_name} lakukan dalam 60 detik:\n\n{key_reason}\n\n💡 {actionable_tip}",
        "cta": "Link di bio / Comment 'MAU'",
        "hashtags": "{hashtags}"
    },
    "instagram_carousel": {
        "hook": "🚀 {product_name} - {category}",
        "slides": [
            "Problem: {problem}",
            "Solution: {product_name}",
            "Keunggulan: {benefit1}, {benefit2}, {benefit3}",
            "Testimoni: {testimonial}",
            "CTA: {cta}"
        ],
        "cta": "Tap link di bio",
        "hashtags": "{hashtags}"
    },
    "linkedin_post": {
        "hook": "🎯 Transformasi {category} dengan {product_name}",
        "body": "Saya melihat banyak {target_audience} mengalami:\n\n{pain_points}\n\nSolusinya?\n\n{product_name} - {price}\n{link}\n\n📊 {metrics}",
        "cta": "Komen 'INFO' untuk detail",
        "hashtags": "{hashtags}"
    },
    "x_thread": {
        "hook": "1/ {product_name} - {price}\n\n{hook_text}",
        "body": "2/ Problem: {problem}\n\n3/ Solution: {solution}\n\n4/ Result: {result}\n\n5/ Link: {link}",
        "cta": "RT jika bermanfaat!",
        "hashtags": "{hashtags}"
    },
    "youtube_shorts": {
        "hook": "🔥 {product_name} - {category}",
        "body": "Ini bedanya sebelum vs setelah pakai {product_name}!\n\n{key_message}\n\n💡 {actionable_tip}",
        "cta": "Klik link di deskripsi",
        "hashtags": "{hashtags}"
    }
}

# Platform-Specific Scheduling
SCHEDULE = {
    "tiktok": {
        "best_times": ["07:00", "12:00", "18:00", "21:00"],
        "post_frequency": 2,  # posts per day
        "format": "video",
        "duration": 60
    },
    "instagram": {
        "best_times": ["07:00", "12:00", "19:00"],
        "post_frequency": 2,
        "format": "carousel/reel",
        "min_slides": 5,
        "max_slides": 10
    },
    "linkedin": {
        "best_times": ["07:00", "12:00", "17:00"],
        "post_frequency": 1,
        "format": "text/image/carousel",
        "max_chars": 3000
    },
    "x": {
        "best_times": ["09:00", "12:00", "15:00", "18:00"],
        "post_frequency": 3,
        "format": "thread/tweet",
        "max_chars": 280
    },
    "youtube": {
        "best_times": ["10:00", "14:00", "17:00"],
        "post_frequency": 1,
        "format": "shorts/video",
        "duration": 60
    }
}

def generate_content_plan(product_key, days=7):
    """Generate 1-week content plan for a product"""
    product = PRODUCTS[product_key]
    plan = []

    for day in range(days):
        date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")

        # Select platforms based on product config
        for platform in product["platforms"]:
            schedule = SCHEDULE[platform]

            # Calculate number of posts for this day
            posts_per_day = schedule["post_frequency"]

            for post_num in range(posts_per_day):
                # Select template
                if platform == "youtube":
                    template_key = "youtube_shorts"
                elif platform == "x":
                    template_key = "x_thread"
                elif post_num == 0:
                    template_key = f"{platform}_demo"
                else:
                    template_key = f"{platform}_carousel"

                if template_key not in CONTENT_TEMPLATES:
                    template_key = list(CONTENT_TEMPLATES.keys())[0]

                template = CONTENT_TEMPLATES[template_key]

                # Generate content
                content = generate_post_content(product, template)

                plan.append({
                    "date": date,
                    "platform": platform,
                    "time": schedule["best_times"][post_num % len(schedule["best_times"])],
                    "content": content,
                    "product": product_key,
                    "template": template_key
                })

    return plan

def generate_post_content(product, template):
    """Generate post content from template"""
    content = template.copy()

    # Select random key message
    key_message = random.choice(product["key_messages"])

    # Fill placeholders
    replacements = {
        "{product_name}": product["name"],
        "{price}": f"Rp {product['price']:,}",
        "{link}": product["link"],
        "{category}": product["category"],
        "{target}": product["target"],
        "{hashtags}": " ".join(product["hashtags"]),
        "{key_reason}": key_message,
        "{key_message}": key_message
    }

    # Replace in content
    cleaned_content = {}
    for key, value in content.items():
        if isinstance(value, str):
            text = value
            for placeholder, replacement in replacements.items():
                text = text.replace(placeholder, replacement)
            cleaned_content[key] = text
        elif isinstance(value, list):
            cleaned_content[key] = [format_slide(slide, replacements) for slide in value]
        else:
            cleaned_content[key] = value

    return cleaned_content

def format_slide(slide, replacements):
    """Format carousel slide"""
    text = slide
    for placeholder, replacement in replacements.items():
        text = text.replace(placeholder, replacement)
    return text

def export_content_plan(plan, output_file="content_plan.json"):
    """Export content plan to JSON"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    return output_file

def print_content_plan(plan):
    """Print content plan in readable format"""
    print("=" * 80)
    print("JENDRALBOT CONTENT PLAN")
    print("=" * 80)
    print()

    current_date = None
    for item in plan:
        if item["date"] != current_date:
            current_date = item["date"]
            print(f"\n{'='*80}")
            print(f"📅 {current_date}")
            print("=" * 80)

        print(f"\n┌─ {item['platform'].upper()} ({item['time']})")
        print(f"│  Product: {item['product'].replace('_', ' ').title()}")
        print(f"│  Template: {item['template']}")
        print(f"├─ Content:")
        print(f"│  {item['content']['hook']}")
        print(f"└─ CTA: {item['content']['cta']}")

def main():
    """Main execution"""
    print("🚀 JENDRALBOT MARKETING AUTOMATION")
    print("=" * 80)

    # Generate content plan for all products
    full_plan = []
    for product_key in PRODUCTS:
        print(f"\n📦 Generating content plan for: {product_key}")
        plan = generate_content_plan(product_key, days=7)
        full_plan.extend(plan)

    # Export to JSON
    output_file = export_content_plan(full_plan)
    print(f"\n✅ Content plan exported to: {output_file}")

    # Print plan
    print_content_plan(full_plan)

    # Statistics
    print("\n" + "=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    print(f"Total Posts: {len(full_plan)}")

    platform_counts = {}
    for item in full_plan:
        platform = item["platform"]
        platform_counts[platform] = platform_counts.get(platform, 0) + 1

    print("\nBy Platform:")
    for platform, count in sorted(platform_counts.items()):
        print(f"  {platform.upper()}: {count} posts")

    print("\nBy Product:")
    for product_key in PRODUCTS:
        count = sum(1 for item in full_plan if item["product"] == product_key)
        print(f"  {product_key.replace('_', ' ').title()}: {count} posts")

    print("\n" + "=" * 80)
    print("✅ DONE! Next steps:")
    print("=" * 80)
    print("1. Review content_plan.json")
    print("2. Generate visual content (images/videos)")
    print("3. Schedule posts using automation tools")
    print("4. Track performance and iterate")
    print("=" * 80)

if __name__ == "__main__":
    main()