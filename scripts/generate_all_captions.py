#!/usr/bin/env python3
"""
Generate All Jendralbot Content Captions
Create complete captions for 6 products - ready for manual posting
"""

# Products data
PRODUCTS = [
    {
        "index": 1,
        "name": "Guru Pintar AI",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "hashtags": "#free #AItraining #belajarAI #AIindonesia #AIeducation #tutorial #automation",
        "cta": "GRATIS training lengkap!",
        "hook": "🔥 STOP! Konten manual makan waktu 4 jam/post!"
    },
    {
        "index": 2,
        "name": "Belanja Duit Balik",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "hashtags": "#cashback #belanja #hemat #smartshopping #tips #GRATIS #duitbalik #voucher",
        "cta": "Rahasia cashback di sini!",
        "hook": "💡 5 Tips Hemat Belanja Hari Ini!"
    },
    {
        "index": 3,
        "name": "Starter AI Content",
        "price": "Rp 49.000",
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #contentcreation #productivity #business #automation #contentmarketing",
        "cta": "Full automation - Rp 49.000!",
        "hook": "🚀 Scale kontenmu dari 5 ke 50 per BULAN!"
    },
    {
        "index": 4,
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "hashtags": "#ecommerce #productphoto #jualanonline #marketplace #AIbusiness #productphotography #tokopedia #shopee",
        "cta": "Foto produk PRO - Rp 75.000!",
        "hook": "📸 Jualan tanpa foto PRO? GAK MUNGKIN!"
    },
    {
        "index": 5,
        "name": "Mesin Cetak Kuliner",
        "price": "Rp 75.000",
        "link": "https://lnkd.in/mesin_cetak",
        "hashtags": "#kuliner #foodphotography #restaurant #GoFood #GrabFood #foodbusiness #restoran #bisniskuliner",
        "cta": "Dapatkan foto premium - Rp 75.000!",
        "hook": "🍽️ Restoran mau EXIST butuh foto MENARIK!"
    },
    {
        "index": 6,
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "link": "https://lynk.id/jendralbot/d70eo2x45em5",
        "hashtags": "#AIcontent #AIautomation #business #productivity #contentmarketing #creator #automation #AItool",
        "cta": "Full automation untuk pros - Rp 89.000!",
        "hook": "🤖 AI ini bisa generate 360 konten/bulan OLEH DIRI!"
    }
]

def generate_tiktok_caption(product):
    """Generate TikTok caption for product."""
    caption = f"""{product['hook']}

💸 PROBLEM:
❌ {product['name']} manual jalan SLOW
❌ Konten hanya 2-3 per minggu
❌ Revenue stagnan
❌ Capek & burnout

✨ {product['name']} - {product['price']}:
🚀 Ide: 5 detik
⚡ Caption: 1 menit
🎨 Edit: 1 menit
⏰ Posting: auto

📊 ROI:
🔥 Sebelum: 2-3 konten/bulan
🔥 Sesudah: 30-90 konten/bulan
🔥 Growth: 15-30x lebih cepat!

💰 {product['cta']}
👉 {product['link']}

{product['hashtags']}
"""
    return caption

def generate_instagram_caption(product):
    """Generate Instagram caption for product."""
    caption = f"""{product['hook']}

— — —

❌ Manual Content Creation:
• Ide konten kosong nungguin hours
• Writing caption 1 jam/post
• Edit gambar 45 menit/post
• Posting manual 15 menit/post
• Total: 4 jam/post!

✨ {product['name']} - {product['price']}

🤖 Content Production:
• Ide: 5 detik via AI
• Caption: 1 menit
• Edit: 1 menit
• Posting: otomatis
• Total: 8 menit/post!

📊 Impact:
• 8 menit/post x 90 post/bulan = 720 menit = 12 jam kerja!
• 2-3 konten/bulan → 30-90 konten/bulan

🔄 {product['cta']}
🔗 {product['link']}

{product['hashtags']}
"""
    return caption

def generate_facebook_caption(product):
    """Generate Facebook caption for product."""
    caption = f"""{product['hook']}

Banyak content creator struggle dengan production time. 4 jam per post terbukti TIDAK SCALE!

💡 Solusi: {product['name']} - {product['price']}

Apa yang bisa dilakukan AI Content Generator:
✅ Generate ide konten unlimited (5 detik)
✅ AI Caption Writer natural & engaging (1 menit)
✅ Image Generation untuk visual (1 menit)
✅ Auto posting ke TIKTOK/IG/YT/FB (auto)

📊 Hasil:
• Sebelum: 2-3 konten per minggu
• Sesudah: 30-90 konten per bulan
• Growth: 15-30x faster!

🤔 Mau scale up kontenmu?
Mulai dari {product['cta']}
👉 {product['link']}

Koment di bawah: Bagaimana konten production kamu sekarang?

#AI #contentcreation #productivity #automation #business #{product['hashtags'].replace('#', '')}
"""
    return caption

def generate_x_caption(product):
    """Generate X/Twitter caption for product."""
    caption = f"""{product['hook']}

Manual: 4 jam/post = 2-3 konten/minggu ❌
{product['name']}: 8 menit/post = 30-90 konten/bulan ✅

ROI: 90 jam/bulan dihemat @ 720 menit/hari

{product['cta']}
👉 {product['link']}

{product['hashtags']}
"""
    return caption

def generate_linkedin_caption(product):
    """Generate LinkedIn caption for product."""
    caption = f"""{product['hook']}

Content creators struggle with production:
• Ide konten kosong berjam-jam
• Writing caption takes 1 hour/post
• Editing images 45 min/post
• Manual posting 15 min/post
• Total: 4 hours per post

Solution: {product['name']} - {product['price']}

Automation Benefits:
• AI Content Generator: 5 seconds for unlimited ideas
• AI Caption Writer: 1 minute for natural, engaging captions
• Image Generation: 1 minute for professional visuals
• Auto Posting: Automated scheduling across platforms

Impact:

Before: 2-3 pieces of content per month
After: 30-90 pieces of content per month

Growth: 15-30x faster

Investment: {product['cta']}
Website: {product['link']}

{product['hashtags']}
"""
    return caption

def generate_all_content():
    """Generate all content for all products."""
    
    print("="*80)
    print("🎯 JENDRALBOT CONTENT GENERATION - ALL PRODUCTS")
    print("="*80)
    print()
    print(f"Total Products: {len(PRODUCTS)}")
    print("Platforms: TikTok, Instagram Reels, Facebook, X, LinkedIn")
    print()
    print("="*80)
    print()
    
    all_content = {}
    
    for product in PRODUCTS:
        print(f"\n{'='*80}")
        print(f"📦 PRODUCT {product['index']}/{len(PRODUCTS)}: {product['name']}")
        print(f"{'='*80}")
        print(f"Price: {product['price']}")
        print(f"Hook: {product['hook']}")
        print(f"CTA: {product['cta']}")
        print(f"Link: {product['link']}")
        print()
        
        content = {
            "tiktok": generate_tiktok_caption(product),
            "instagram": generate_instagram_caption(product),
            "facebook": generate_facebook_caption(product),
            "x": generate_x_caption(product),
            "linkedin": generate_linkedin_caption(product)
        }
        
        all_content[product['index']] = {
            "product": product,
            "content": content
        }
        
        # Show first platform as sample
        print(f"📱 SAMPLE CAPTION (TikTok):")
        print("-"*80)
        print(content['tiktok'][:500] + "...")
        print()
    
    # Save to JSON
    import json
    output_file = "/home/openclaw/.openclaw/workspace/content/all_captions.json"
    with open(output_file, "w") as f:
        json.dump(all_content, f, indent=2)
    
    print()
    print("="*80)
    print("✅ CONTENT GENERATION COMPLETE")
    print("="*80)
    print()
    print(f"Total Products: {len(PRODUCTS)}")
    print(f"Total Captions: {len(PRODUCTS) * 5} (5 platforms per product)")
    print(f"Output File: {output_file}")
    print()
    print("="*80)
    print("📊 SUMMARY")
    print("="*80)
    print()
    
    for i, product in enumerate(PRODUCTS, 1):
        print(f"{i}. {product['name']} ({product['price']})")
        print("   Hooks ready for:")
        print("   • TikTok")
        print("   • Instagram Reels")
        print("   • Facebook")
        print("   • X (Twitter)")
        print("   • LinkedIn")
        print()
    
    print("="*80)
    print("📋 NEXT STEPS")
    print("="*80)
    print()
    print("✅ Review captions above")
    print("✅ Copy caption for each platform")
    print("✅ Attach image (nvidia_hook_final.png)")
    print("✅ Post manually via PostBridge app or platforms")
    print()
    print("="*80)

if __name__ == "__main__":
    generate_all_content()