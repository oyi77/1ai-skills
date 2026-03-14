#!/usr/bin/env python3
"""
Content Variator Generator - 12 Posts Per Day (FIXED)
Mix of Sales & Education (50-50) - Exact 2-hour intervals
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
        "price": "Rp 75.000",
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

# 12 Posts Per Day (Every 2 hours from 00:00 to 22:00)
HOURS = [
    0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22
]

def get_product_for_hour(hour):
    """Rotate products every 2 hours"""
    products_list = list(PRODUCTS.keys())
    return products_list[hour % len(products_list)]

def generate_sales_post(product_key, hour):
    """Generate sales post"""
    product = PRODUCTS[product_key]
    
    sales_hooks = [
        {
            "type": "problem_solution",
            "caption": f"🔥 STOP! Masalah {product['tone']} bikin kamu capek?\n\nSolusinya: {product['name']} ({product['price']})\n\n✅ {get_benefit(product)}\n✅ {get_benefit(product)}\n✅ {get_benefit(product)}\n\n💡 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "social_proof",
            "caption": f"\"Alhamdulillah! Order naik 300%!\" 🔥\n\nTestimoni pelanggan {product['target']} tentang {product['name']}.\n\n📊 {product['price']}'s investment untuk ROI tinggi.\n\n👉 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "feature_highlight",
            "caption": f"⭐ Fitur {product['name']} yang Wajib Kamu Tahu:\n\n\n✨ [Fitur 1]\n⚡ [Fitur 2]\n💎 [Fitur 3]\n\n💰 {product['price']} - Investasi bijak!\n\n👉 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "comparison",
            "caption": f"📊 BEFORE vs AFTER - {product['name']}\n\n📉 BEFORE:\n{get_before_state(product)}\n\n📈 AFTER:\n{get_after_state(product)}\n\nTransformasi nyata! 💪\n\n👉 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "urgency",
            "caption": f"🎯 LIMITED TIME OFFER! ⏰\n\n{product['name']} - {product['price']}\n\nSpecial hari ini saja!\n\n💊 Diskon khusus followers!\n\n⏰ Berakhir sampai midnight!\n\n👉 {product['link']}\n\n{product['hashtags']}"
        },
        {
            "type": "success_story",
            caption": f"💎 Kisah Sukses: Budi dengan {product['name']}!\n\n👤 Dulu: {get_before_state(product)}\n✨ Sekarang: {get_after_state(product)}\n\n📈 ROI: 10x lipat!\n\n💰 Hanya {product['price']}\n\n{product['link']}\n\n{product['hashtags']}"
        }
    ]
    
    hook = sales_hooks[hour % len(sales_hooks)]
    return {
        "time": f"{hour:02d}:00",
        "type": "sales",
        "variant": hook["type"],
        "caption": hook["caption"],
        "product": product_key
    }

def generate_education_post(product_key, hour, day):
    """Generate education post"""
    product = PRODUCTS[product_key]
    
    # Edu types cycle: image → series → tips → image → series → tips
    edu_types = ["image", "series", "tips"]
    edu_type = edu_types[(hour // 2) % 3]
    
    if edu_type == "image":
        caption = generate_education_image(product_key)
    elif edu_type == "series":
        series_part = ((day - 1) % 5) + 1
        caption = generate_education_series(product_key, series_part)
    else:  # tips
        caption = generate_education_tips(product_key)
    
    return {
        "time": f"{hour:02d}:00",
        "type": "education",
        "variant": edu_type,
        "caption": caption,
        "product": product_key
    }

def generate_education_image(product_key):
    """Education image: explain WHY need this product"""
    product = PRODUCTS[product_key]
    
    return f"""📚 INFO: Kenapa Butuh {product['name']}?

---

🤔 Pemikiran: {product['target']} sering...

❌ Masalah:
{get_problem_state(product)}

✅ {product['name']} Solusi:
{get_solution_state(product)}

💡 Kenapa penting?

→ Reason 1: Solusi masalah utama
→ Reason 2: Hemat waktu & effort
→ Reason 3: Hasil lebih baik berkali-kali lipat

❓ Masih ragu? DM "INFO" for details!

👉 {product['link']}

{product['hashtags']}
#edukasi #infoproduk #{product['name'].replace(' ', '').lower()}"""

def generate_education_series(product_key, part):
    """Education series: multi-part learning"""
    series_data = {
        "starter_ai_content": {
            1: "AI Content 101 - Dasar-Dasar",
            2: "Masalah Manual Content Creation",
            3: "Solusi dengan {produk}",
            4: "Tutorial: Cara Pakai",
            5: "Tips: Memaksimalkan Hasil"
        },
        "studio_marketplace_pro": {
            1: "Fotografi Produk vs Studio Pro",
            2: "Cara Edit Foto Tercepat",
            3: "Before/After Transformation",
            4: "Strategi Foto Viral",
            5: "Testimoni Seller Sukses"
        },
        "mesin_cetak_kuliner": {
            1: "Food Photography 101",
            2: "Makanan Enak = Order Naik",
            3: "GoFood/GrabFood Optimization",
            4: "Transformasi Menu Nyata",
            5: "Tips Menarik Order"
        },
        "ai_content_pro": {
            1: "Produtivitas Revolution",
            2: "Time Audit: Berapa Hemat?",
            3: "AI Workflow Efektif",
            4: "Kebiasaan Sukses Creator",
            5: "Future of Content Creation"
        },
        "guru_pintar_ai": {
            1: "AI untuk Pemula",
            2: "Tools Wajib Dipelajari",
            3: "Skill AI yang Bisa Digenerate",
            4: "Case Study: Kerja 10x Cepat",
            5: "Roadmap Belajar AI 6 Bulan"
        },
        "belanja_duit_balik": {
            1: "Cashback 101",
            2: "Aplikasi Cashback Terbesar",
            3: "Strategi Belanja Tepat",
            4: "Testimoni 1 Bulan Hemat",
            5: "Advanced: Stacking Cashback"
        }
    }
    
    series = series_data[product_key]
    topic = series[part]
    product_name = PRODUCTS[product_key]["name"]
    link = PRODUCTS[product_key]["link"]
    hashtags = PRODUCTS[product_key]["hashtags"]
    
    return f"""📖 SERIES: {topic}
{product_name} Edukasi - Part {part}/5
---

📘 Hari ini kita bahas:
{get_series_content(product_key, part)}

---
📅 Besok: Part {part + 1 if part < 5 else 1}
(Next topic: {series[part + 1 if part < 5 else 1]})

💬 Tanya di komen jika ada pertanyaan!

👉 Jelajah lebih: {link}

{hashtags}
#series #edukasi #belajarAI #{product_name.replace(' ', '')}
"""

def generate_education_tips(product_key):
    """Education tips: quick actionable advice"""
    product = PRODUCTS[product_key]
    
    tips = [
        "5 Tips Memaksimalkan Hasil",
        "5 Kesalahan Umum yang Musti Diedit",
        "Cara Pemakaian yang Benar",
        "Tips Pemula untuk {product['target']}",
        "Advanced Strategy untuk Pro"
    ]
    
    tip = tips[datetime.now().hour % len(tips)]
    tips_list = get_tips_list(product_key)
    
    return f"""💡 {tip} - {product['name']}

---

{tips_list}

---

💰 {product['price']}

Info lengkap: {product['link']}

{product['hashtags']}
#tips #tutorial #{product['name'].replace(' ', '')}"""

# Helper functions
def get_benefit(product):
    benefits = {
        "starter_ai_content": ["Dapat inspirasi konten dengan mudah", "Hemat waktu 80%", "Upgrade-ready"),
        "studio_marketplace_pro": ["Foto profesional 1 menit", "Boost konversi 300%", "Hemat biaya fotografer"],
        "mesin_cetak_kuliner": ["Food aesthetic menarik", "Order naik berlipat", "Profesional tanpa fotografer"],
        "ai_content_pro": ["Otomatisasi konten", "Kualitas premium", "Save time 80%"],
        "guru_pintar_ai": ["Training lengkap", "Step-by-step", "Support penuh"],
        "belanja_duit_balik": ["Cashback otomatis", "Duit balik terus", "Belanja tapi dapat duit"]
    }
    return benefits.get(product["product_key"], ["Benefit 1", "Benefit 2", "Benefit 3"])[0]

def get_before_state(product_key):
    states = {
        "starter_ai_content": "Ide konten kosong, butuh waktu berhari-hari, editing manual capek",
        "studio_marketplace_pro": "Foto produk buram, jualan sepi, customer ragu order",
        "mesin_cetak_kuliner": "Foto makanan biasa saja, order sedikit, branding kurang profesional",
        "ai_content_pro": "Bikin konten manual makan waktu, bakar budget desainer, competitor lebih cepat",
        "guru_pintar_ai": "Bingung cara pakai AI, tidak tahu tools mana yang penting",
        "belanja_duit_balik": "Belanja habis saja, tidak dapat keuntungan apa-apa"
    }
    return states.get(product_key, "Masalah sebelumnya")

    def get_after_state(product_key):
        states = {
            "starter_ai_content": "Ide konten mengalir, selesai dalam hitungan menit, kualitas konten meningkat",
            "studio_marketplace_pro": "Foto produk profesional & menarik, customers percaya, order naik berkali-kali",
            "mesin_cetak_kuliner": "Food aesthetic & premium, order meledak, branding profesional",
            "ai_content_pro": "Otomatisasi konten bekerja, save 80% waktu, kompetitor tertinggal",
            "guru_pintar_ai": "Paham cara pakai AI tools, skill meningkat, produktivitas naik",
            "belanja_duit_balik": "Belanja tapi dapat duit, cashback rutinites, budget lebih hemat"
        }
        return states.get(product_key, "Solusi sesudahnya")

def get_problem_state(product):
    states = {
        "starter_ai_content": "Struggle untuk menemukan ide tulisan\nEditor manual makan berjam-jam\nBingung mulai",
        "studio_marketplace_pro": "Editing foto produk manual butuh skill\nBiaya fotografer mahal\nPerlu waktu berhari-hari",
        "mesin_cetak_kuliner": "Foto makanan kurang menarik\nRestaurant pesaing sepi dengan kompetitor\nFood aesthetic berpengaruh ke order",
        "ai_content_pro": "Bakar budget desainer dan copywriter\nCompetitor lebih cepat rilis konten\nScale jadi hambatan",
        "guru_pintar_ai": "Bingung tools AI mana yang relevan\nLearning curve terjal\nTidak tahu mulai dari mana",
        "belanja_duit_balik": "Belanja habis dompet kering\nTidak pernah dapat cashback atau diskon\nBoros pengeluaran"
    }
    return states.get(product["product_key"], "Problem umum")

def get_solution_state(product):
    states = {
        "starter_ai_content": "AI generate ide & tulisan dalam hitungan detik\nHemat waktu drastis\nQuality konsisten setiap posts",
        "studio_marketplace_pro": "Generate foto profesional 1 menit saja\nTanpa keterampilan editing\nHemat biaya fotografer",
        "mesin_cetak_kuliner": "Enhance photo menjadi food aesthetic\nBoost brand restaurant\nOrder naik signifikan",
        "ai_content_pro": "Otomatisasikan workflow konten\nHemat 80% waktu produksi\nScale tanpa nambah team",
        "guru_pintar_ai": "Pelajari tools yang relevan & proven\nStep-by-step roadmap\nSupport komunitas",
        "belanja_duit_balik": "Dapatkan cashback otomatis setiap belanja\nHemat budget bulanan\nStrategi cashback maksimal"
    }
    return states.get(product["product_key"], "Solusi yang ditawarkan")

def get_series_content(product_key, part):
    content = {
        "starter_ai_content": {
            1: "Apa itu AI Content? Kenapa penting untuk {PRODUCTS[product_key]['target']}?\n\nAI Content bukan cuma buzz - ini real technology yang mengubah cara kita bikin konten.",
            2: "Masalah besar: TIME! ⏰\n- Ide: 10 menit\n- Writing: 30 menit\n- Editing: 20 menit\n- Posting: 10 menit\nTotal: 70 menit per post!\n\nAI Content: 3-5 menit.",
            3: "Ini fitur utamanya:\n✅ AI Prompt Generator\n✅ Caption Writer\n✅ Hashtag Generator\n✅ Content Calendar\n\nSemua dalam 1 tool!",
            4: "Cara pakai:\n1. Tentukan topik\n2. AI generate konten\n3. Review & edit\n4. Publish!\n\nPraktis & cepat.",
            5: "Tips hasil:\n- Post 3x lebih banyak (bukan capek)\n- Quality lebih konsisten\n- Ada waktu untuk interaksi\n- Fokus di engagement, bukan editing!",
            2: "Masalah: TIME! ⏰\n- Edit foto: 1-4 jam per produk\n- Need skilled designer → mahal\n- Quality inconsistency\n\nStudio Pro: 1 menit, hasil profesional!",
            3: "Sebelum: Foto rumahan\nSesudah: Foto premium\n- Customer lebih percaya\n- Order meledak\n- Brand authority naik",
            4: "Strategi viral:\n- Story format (before/after)\n- Behind-the-scenes\n- Product in real settings\n- Customer showcases\n- Review & tutorial",
            5: "Testimoni:\n\"Setelah pakai Studio Pro, order naik 300%!\"\n\"Customer jadi lebih serius\"",
            2: "Masalah: Visual\n- Makanan enak tapi foto kurang menarik\n- Customer judge bukan dari rasa\n- Order kecewaan dari foto buram",
            3: "Solusi:\n- Food aesthetic = Premium product\n- People makan dengan mata (trust!)\n- Higher willingness to pay",
            4: "Transformasi:\nFrom: Foto biasa\nTo: Food aesthetic premium\n- Customer testimonials\n- ROI: 200-300% lebih",
            5: "Tips:\n- Lighting penting! 📸\n- Props & background\n- Angle terbaik (45 derajat)\n- Testimonial foto real",
            2: "Masalah: PRODUCTIVITY\n- Bakar budget desainer/copywriter\n- Competitor rilis lebih cepat\n- Scale jadi hambatan",
            3: "Solusi:\n- AI automatis 80% workflow\n- Save time = scale = revenue\n- Professional quality tanpa agency",
            4: "Kebiasaan:\n- Planning batch content\n- Repurpose konten\n- Review & optimize weekly\n- Measure & adjust strategy",
            5: "Future:\n- AI akan mengubah industri\n- Early adopters menang\n- Build now or get left behind",
            2: "Proliferasi tools AI\n- Bingung mana yang penting?\n- Overwhelmed dengan pilihan",
            3: "Solusi:\n- Tool yang WAJIB dipelajari:\n✨ ChatGPT (writing)\n✨ Midjourney (visuals)\n✨ AI Content Pro (automation)",
            4: "Case Study:\n- Before: 5 konten/hari (manual)\n- After: 20 konten/hari (AI assisted)\n- Revenue: 4x lipat!",
            5: "6-bulan roadmap:\nMonth 1-2: dasar-dasar\nMonth 3-4: intermediate\nMonth 5-6: advanced & master\n- Commit & ikuti!",
            2: "Pemberat cashback sering\nTapi user lupa/gak tahu cara maksimalkan\nBanyak duit hilang sia-sia",
            3: "Aplikasi terbesar:\n✨ Shopee (Double Cashback promo)\n✨ GoFood/GrabFood (regular cashback)\n✨ OVO (often)\n✨ Traveloka (regular)",
            4: "Testimoni pertama:\n「Belanja 1 juta, cashback 100k!」\n「Hemat 10% bulanan tanpa banyak effort」",
            5: "Advanced tips:\n- Stack aplikasi (triple cashback)\n- Kalender promosi\n- Credit card cashback\n- Budgeting strategy"
        }
    }
    return content.get(product_key, {}).get(part, "")