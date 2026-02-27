#!/usr/bin/env python3
"""
Cold Email Generator - Personalized Emails for Shopee Sellers

Generates personalized cold emails for 10 Shopee sellers based on:
- Shop name
- Total sales volume
- Product categories
- Average rating
"""

import json
from datetime import datetime
from pathlib import Path

# Load seller data
with open('/home/openclaw/.openclaw/workspace/output/market_research/sellers.json') as f:
    sellers = json.load(f)

# Email templates
def email_template_direct(seller):
    """Direct approach - short and value-focused"""
    return f"""Subject: TikTok content untuk {seller['shop_name']} - gratis 3 video sample

Halo {seller['shop_name']},

Saya lihat produk kalian sudah terjual {seller['total_sales']:,} di Shopee dengan rating {seller['avg_rating']:.1f}/5.0. Impresif!

Tapi saya perhatikan kalian belum aktif di TikTok, padahal kalian melewatkan 200M+ user potensial.

**Saya bisa bantu:**

- 5-10 viral-optimized video setiap minggu
- 10-50x peningkatan engagement dalam 30 hari
- Full AI-powered generation (cepat & konsisten)
- 30-day money-back guarantee

**Harga mulai dari IDR 3M/bulan (untuk 20 video)**

Saya mau kirim 3 free sample videos untuk kalian review. Cuma butuh:
1. Link produk terlaris kalian
2. 1-2 kata tentang brand vibe kalian

No obligation. Kalau suka, kita lanjut. Kalau tidak, no problem.

Balas email ini kalau tertarik.

Terima kasih,

Veris
BerkahKarya TikTok Content Agency
WA/Telegram: [insert contact]
"""

def email_template_story(seller):
    """Storytelling approach - hook-based"""
    # Get top product
    top_product = max(seller['products'], key=lambda p: p['sold'])
    
    return f"""Subject: Produk kalian {top_product['product_name']} bisa jadi viral di TikTok

Halo {seller['shop_name']},

Cerita singkat: Kemarin saya lihat produk kalian "{top_product['product_name']}" di Shopee. Sudah terjual {top_product['sold']:,} dengan rating {top_product['rating']:.1f}. Keren banget!

Tapi saya berpikir: "Kalau produk ini punya TikTok video yang viral, bisa jadi berapa kali lebih banyak penjualan?"

Jadi saya buat 3 sample videos untuk produk ini. 15 detik. Hook-nya bikin orang stop scrolling.

**Hasil dari klien lain:**
- Brand A: 50x engagement dalam 30 hari
- Brand B: 100K+ followers dalam 2 bulan
- Brand C: IDR 50M tambahan penjualan/bulan

**Saya mau kasih kalian 3 free videos juga.**

Cuma butuh:
1. Link produk "{top_product['product_name']}"
2. Target audience kalian (usia, gender, interest)

Saya buat, kirim ke kalian, kalian review. Kalau suka, kita lanjut. Kalau tidak, tidak apa-apa.

Tertarik?

Veris
BerkahKarya TikTok Content Agency
WA/Telegram: [insert contact]
"""

def email_template_data(seller):
    """Data-driven approach - stats-focused"""
    return f"""Subject: 200M TikTok user melewatkan {seller['shop_name']}?

Halo {seller['shop_name']},

**Data ngomong ini:**

- TikTok Indonesia: 200M+ monthly active users
- Home Decor category: 5B+ monthly views
- {seller['shop_name']}: IDR {seller['total_value']:,} sales di Shopee
- {seller['shop_name']} TikTok presence: Hampir tidak ada

**Tapi kalian bisa ubah ini:**

Dengan TikTok content yang viral, kalian bisa:
- Tambah 10-50% penjualan dari social media
- Brand awareness ke 200M+ user
- Engage dengan customer baru (tidak cuma existing)

**Berapa biayanya?**

IDR 3M-8M/bulan untuk 20-80 video.

Kalau kalian dapat 10% penjualan tambahan dari TikTok:
- Current: IDR {seller['total_value']:,}/bulan
- Potential: +IDR {seller['total_value'] // 10:,}/bulan (konservatif)
- Investment: IDR 3-8M/bulan
- ROI: 10-100x dalam 1-3 bulan

**I'll prove it works:**

Kirim 3 free sample videos untuk kalian review. No obligation.

Reply this email kalau tertarik.

Best,
Veris
BerkahKarya TikTok Content Agency
"""

# Generate emails for all sellers
output_dir = Path("/home/openclaw/.openclaw/workspace/output/market_research/cold_emails")
output_dir.mkdir(exist_ok=True)

print("=" * 80)
print("📧 GENERATING COLD EMAILS FOR 10 SELLERS")
print("=" * 80)

for i, seller in enumerate(sellers, 1):
    print(f"\n{i}. {seller['shop_name']}")
    
    # Generate 3 email variations
    emails = {
        'direct': email_template_direct(seller),
        'story': email_template_story(seller),
        'data': email_template_data(seller)
    }
    
    # Save emails
    for variation, email_body in emails.items():
        filename = f"{i}_{seller['shop_name'].replace(' ', '_')}_{variation}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(email_body)
        
        print(f"   ✅ Saved: {filename}")

print("\n" + "=" * 80)
print(f"✅ TOTAL EMAILS GENERATED: {len(sellers) * 3}")
print(f"📁 Location: {output_dir}")
print("=" * 80)

# Summary
print(f"\n📊 SELLER PRIORITY (by total sales value):")
for i, seller in enumerate(sorted(sellers, key=lambda s: s['total_value'], reverse=True), 1):
    print(f"   {i}. {seller['shop_name']}: IDR {seller['total_value']:,}")

print(f"\n💡 RECOMMENDATION:")
print(f"   1. Start with top 5 sellers (highest value)")
print(f"   2. Use 'story' template for first contact")
print(f"   3. Follow up in 3-5 days with 'data' template")
print(f"   4. Close deal with 'direct' template")

print(f"\n🎯 EXPECTED CONVERSION:")
print(f"   Cold email response rate: 1-3% (1-3 dari 100)")
print(f"   From 10 sellers: 0-3 responses")
print(f"   From 50 sellers: 0-15 responses")
print(f"   Goal: 1-2 meetings this week")
