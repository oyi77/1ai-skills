#!/usr/bin/env python3
"""
JENDRALBOT Campaign Rebuild with Media
Uploads images and creates posts with proper media for Instagram/TikTok/Facebook
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Config
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LOG_FILE = os.path.join(WORKSPACE, "logs/campaign_rebuild.json")
TZ = ZoneInfo("Asia/Jakarta")

# Social accounts
INSTAGRAM_IDS = [48186]
TIKTOK_IDS = [48374, 48373, 48372, 48338, 48337, 48336, 48335]
FACEBOOK_IDS = [48178, 48177, 48176, 48175]

# Products → image mapping
PRODUCTS = [
    {
        "id": 1,
        "name": "JobMagnet Ai",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/45r5yvze3vy4",
        "image": "output/ai_content_pro_seller_indo_polished.png",
        "emoji": "💼",
        "hook": "Capek nganggur? AI ini auto cariin kerja buat kamu!",
        "benefit": "JobMagnet AI bantu kamu bikin CV, cover letter, dan lamaran kerja OTOMATIS. Ribuan lowongan dianalisa dalam detik.",
        "hashtags": "#JobMagnetAI #CariKerja #AIIndonesia #LamararanKerja #KarirImpian #ToolsAI #CareerBoost"
    },
    {
        "id": 2,
        "name": "AI Creative & Performance Ad Engine",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/9r8rj1o38q59",
        "image": "output/meta_ads_v4_perfect.jpg",
        "emoji": "🚀",
        "hook": "Iklan kamu gak pernah konversi? Ini penyebabnya!",
        "benefit": "AI Ad Engine bikin iklan performa tinggi OTOMATIS. CTR naik 300%, budget gak kebuang sia-sia.",
        "hashtags": "#AIAds #DigitalMarketing #IklanFacebook #PerformanceAds #AdsIndonesia #MarketingAI #ROITinggi"
    },
    {
        "id": 3,
        "name": "Food Menu AI Studio",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/l4q49jj3z383",
        "image": "output/mesin_cetak_kuliner_indo_polished.png",
        "emoji": "🍜",
        "hook": "Punya warung tapi menu masih tulisan tangan? Malu dong!",
        "benefit": "Food Menu AI Studio bikin menu restoran profesional DALAM MENIT. Desain cakep, harga terjangkau.",
        "hashtags": "#FoodMenuAI #KulinerIndonesia #MenuMakanan #UsahaKuliner #FoodBusiness #DesainMenu #WarungModern"
    },
    {
        "id": 4,
        "name": "Studio Marketplace Pro (SellPix AI)",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/emne05mm7v25",
        "image": "output/marketplace_pro_indo_polished.png",
        "emoji": "🛒",
        "hook": "Foto produk jelek = penjualan jelek. Ini solusinya!",
        "benefit": "SellPix AI ubah foto biasa jadi foto produk KELAS MARKETPLACE dalam hitungan detik. Penjualan langsung naik!",
        "hashtags": "#SellPixAI #FotoProduktor #Marketplace #Shopee #Tokopedia #JualOnline #ProductPhoto"
    },
    {
        "id": 5,
        "name": "AI Creative Tools",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/89d30qd3ddnj",
        "image": "output/ai_content_pro_seller_indo.png",
        "emoji": "🎨",
        "hook": "Desainer mahal? Gak perlu! AI ini gantiin mereka.",
        "benefit": "AI Creative Tools — bikin konten visual, banner, thumbnail, dan materi marketing PROFESIONAL tanpa skill desain.",
        "hashtags": "#AICreativeTools #DesainAI #ContentCreator #ToolsKreasi #DigitalContent #AIDesign #CreatorIndonesia"
    },
    {
        "id": 6,
        "name": "Guru Pintar AI",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/6821op5e24kn",
        "image": "output/guru_pintar_ai_indonesia.png",
        "emoji": "🧠",
        "hook": "Belajar apapun dalam 1 jam dengan AI tutor personal!",
        "benefit": "Guru Pintar AI — asisten belajar cerdas yang jawab semua pertanyaan kamu 24/7. Seperti punya guru privat!",
        "hashtags": "#GuruPintarAI #BelajarOnline #AITutor #Edukasi #PendidikanIndonesia #SmartLearning #TutorAI"
    },
    {
        "id": 7,
        "name": "Mesin Cetak Bisnis Kulinermu",
        "price": "IDR 75.000",
        "link": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "image": "output/mesin_cetak_kuliner_indo.png",
        "emoji": "🍕",
        "hook": "Bisnis kuliner kamu stagnan? Ini mesinnya!",
        "benefit": "Mesin Cetak Bisnis Kuliner — sistem lengkap untuk scale up bisnis makanan kamu. Dari operasional hingga marketing.",
        "hashtags": "#BisnisKuliner #MesinCetakBisnis #UsahaMakanan #KulinerIndonesia #ScaleUpBisnis #FoodBusiness #UMKMIndonesia"
    },
    {
        "id": 8,
        "name": "Belanja Tetap Jalan Tapi Duit Balik Lagi",
        "price": "GRATIS",
        "link": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "image": "output/belanja_duit_balik_indo_polished.png",
        "emoji": "💰",
        "hook": "GRATIS! Cara belanja tapi uangmu balik lagi 100%!",
        "benefit": "Strategi LEGAL belanja online tapi dapat cashback berlipat. Sudah dibuktikan ribuan orang Indonesia!",
        "hashtags": "#BelanjaGratis #CashbackIndonesia #UangKembali #TipsHemat #ShoppingHack #GratisIndonesia #FinancialFreedom"
    },
    {
        "id": 9,
        "name": "Kelas Affiliate Pesugihan TikTok",
        "price": "IDR 1.000.000",
        "link": "https://lynk.id/jendralbot/regxdn7xkpz6",
        "image": "output/meta_ads_text_v2.jpg",
        "emoji": "💸",
        "hook": "TikTok = ATM berjalan. Ini buktinya!",
        "benefit": "Kelas Affiliate Pesugihan TikTok — sistem menghasilkan jutaan dari TikTok tanpa modal, tanpa followers banyak.",
        "hashtags": "#AffiliateTikTok #TikTokAffiliate #CuanTikTok #PesugihanTikTok #MakeMoneyOnline #AffiliatMarketing #TikTokIndonesia"
    },
]

# Caption variations per product
def make_captions(product):
    """Generate 3 caption variations for a product"""
    name = product["name"]
    price = product["price"]
    link = product["link"]
    emoji = product["emoji"]
    hook = product["hook"]
    benefit = product["benefit"]
    tags = product["hashtags"]

    if price == "GRATIS":
        price_str = "✅ GRATIS — Ambil sekarang!"
        urgency = "📣 Stok link terbatas, ambil sebelum ditutup!"
    elif price == "IDR 1.000.000":
        price_str = f"💎 Investasi: Rp 1.000.000 (balik modal dari 1 sale!)"
        urgency = "⚡ Slot kelas terbatas — daftar sekarang sebelum penuh!"
    else:
        price_str = f"~~Rp 299.000~~ → Rp 75.000 (hemat 75%!)"
        urgency = "⏳ Harga naik sewaktu-waktu, grab sekarang!"

    v1 = f"""{emoji} {hook}

{benefit}

{price_str}
{urgency}

🔗 Link: {link}

{tags}"""

    v2 = f"""🔥 STOP! Baca ini dulu sebelum scroll...

Kalau kamu belum punya {name}, kamu udah ketinggalan jauh dari kompetitor!

✅ {benefit}

{price_str}
{urgency}

👇 Klik link di bio atau langsung:
{link}

{tags}"""

    v3 = f"""📢 Jujur aja — ini salah satu tools terbaik yang pernah aku temuin!

{name} beneran ubah cara aku kerja:
• Lebih cepat ⚡
• Lebih profesional 💪
• Lebih untung 💰

{benefit}

{price_str}
{urgency}

📲 {link}

{tags}"""

    return [v1, v2, v3]


def upload_media(image_path):
    """Upload image to PostBridge and return media_id"""
    full_path = os.path.join(WORKSPACE, image_path)
    if not os.path.exists(full_path):
        print(f"  ⚠️  Image not found: {full_path}")
        return None

    file_size = os.path.getsize(full_path)
    ext = os.path.splitext(full_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    fname = os.path.basename(full_path)

    print(f"  📤 Uploading {fname} ({file_size} bytes)...")

    # Step 1: Get upload URL
    r = requests.post(
        f"{BASE_URL}/media/create-upload-url",
        headers=HEADERS,
        json={"name": fname, "mime_type": mime, "size_bytes": file_size}
    )
    if r.status_code not in (200, 201):
        print(f"  ❌ Failed to get upload URL: {r.status_code} {r.text[:200]}")
        return None

    data = r.json()
    media_id = data.get("media_id") or data.get("id") or (data.get("data", {}) or {}).get("media_id")
    upload_url = data.get("upload_url") or (data.get("data", {}) or {}).get("upload_url")

    if not media_id or not upload_url:
        # Try nested structures
        if "data" in data:
            d = data["data"]
            media_id = d.get("media_id") or d.get("id")
            upload_url = d.get("upload_url")
        print(f"  📋 API response keys: {list(data.keys())}")
        if not media_id:
            print(f"  ❌ No media_id in response: {json.dumps(data)[:300]}")
            return None

    # Step 2: PUT file bytes
    with open(full_path, "rb") as f:
        file_bytes = f.read()

    put_headers = {"Content-Type": mime, "Content-Length": str(file_size)}
    r2 = requests.put(upload_url, data=file_bytes, headers=put_headers)
    if r2.status_code not in (200, 201, 204):
        print(f"  ❌ Upload failed: {r2.status_code} {r2.text[:200]}")
        return None

    print(f"  ✅ Uploaded! media_id={media_id}")
    return media_id


def create_post(caption, scheduled_at, account_ids, media_ids):
    """Create a post via PostBridge API"""
    payload = {
        "caption": caption,
        "scheduled_at": scheduled_at,
        "social_accounts": account_ids,
        "media": media_ids
    }
    r = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=payload)
    return r.status_code, r.json() if r.text else {}


def main():
    print("=" * 60)
    print("🚀 JENDRALBOT Campaign Rebuild with Media")
    print("=" * 60)

    results = {
        "started_at": datetime.now(TZ).isoformat(),
        "posts_created": [],
        "errors": [],
        "summary": {}
    }

    # Build schedule: starting March 13, 2026
    # 3 slots per day: 06:00, 12:00, 18:00 UTC+7
    base_date = datetime(2026, 3, 13, tzinfo=TZ)
    time_slots = [6, 12, 18]

    # Generate schedule slots across 7 days
    schedule_slots = []
    for day_offset in range(7):
        for hour in time_slots:
            dt = base_date + timedelta(days=day_offset, hours=hour)
            schedule_slots.append(dt)

    # Total 21 slots per platform day-round
    # We need 27+ posts (9 products × 3 variations)
    # Strategy: Instagram first, then TikTok batches, then Facebook

    # Platform assignments per post index
    # Posts 0-8: Instagram (9 posts, one per product, variation 1)
    # Posts 9-17: TikTok batch (rotate through TikTok IDs)
    # Posts 18-26: Facebook batch (rotate through FB IDs)
    # Then continue with variation 2 and 3 for all platforms

    post_queue = []

    # Build all 27 posts (9 products × 3 variations)
    for variation_idx in range(3):
        for prod in PRODUCTS:
            captions = make_captions(prod)
            caption = captions[variation_idx]
            post_queue.append({
                "product": prod,
                "caption": caption,
                "variation": variation_idx + 1
            })

    print(f"\n📋 Total posts to create: {len(post_queue)}")
    print(f"📅 Scheduling from March 13-19, 2026")
    print(f"⏰ Time slots: 06:00, 12:00, 18:00 (UTC+7)")

    # Upload images first (cache by image path)
    print("\n📤 Uploading product images...")
    media_cache = {}
    unique_images = list(set(p["image"] for p in PRODUCTS))

    for img_path in unique_images:
        print(f"\n  Processing: {img_path}")
        media_id = upload_media(img_path)
        if media_id:
            media_cache[img_path] = media_id
        else:
            print(f"  ⚠️  Skipping image, will try fallback")
            # Try polished version
            polished = img_path.replace(".png", "_polished.png").replace(".jpg", "_polished.jpg")
            fallback_path = os.path.join(WORKSPACE, polished)
            if os.path.exists(fallback_path):
                media_id = upload_media(polished)
                if media_id:
                    media_cache[img_path] = media_id
        time.sleep(0.15)  # Rate limit: max 10 req/sec

    print(f"\n✅ Uploaded {len(media_cache)}/{len(unique_images)} images")

    # Assign platforms to post slots
    # Distribute: posts 0-8 → Instagram, 9-17 → TikTok (rotate IDs), 18-26 → Facebook (rotate)
    # Then additional variations continue on same platforms

    platform_assignments = []
    for i in range(len(post_queue)):
        if i < 9:
            platform_assignments.append(("instagram", INSTAGRAM_IDS))
        elif i < 18:
            tiktok_id = TIKTOK_IDS[i % len(TIKTOK_IDS)]
            platform_assignments.append(("tiktok", [tiktok_id]))
        else:
            fb_id = FACEBOOK_IDS[i % len(FACEBOOK_IDS)]
            platform_assignments.append(("facebook", [fb_id]))

    # Create posts
    print(f"\n📝 Creating posts...")
    created_count = 0
    error_count = 0

    for idx, (item, (platform, account_ids)) in enumerate(zip(post_queue, platform_assignments)):
        prod = item["product"]
        caption = item["caption"]
        variation = item["variation"]

        # Get media
        media_id = media_cache.get(prod["image"])
        if not media_id:
            # Use any available media as fallback
            if media_cache:
                media_id = list(media_cache.values())[0]
                print(f"  ⚠️  Using fallback media for {prod['name']}")
            else:
                print(f"  ❌ No media available for {prod['name']}, skipping")
                error_count += 1
                results["errors"].append({
                    "product": prod["name"],
                    "reason": "no_media_available"
                })
                continue

        # Get schedule slot
        slot = schedule_slots[idx % len(schedule_slots)]
        scheduled_at = slot.strftime("%Y-%m-%dT%H:%M:%S+07:00")

        print(f"\n  [{idx+1}/{len(post_queue)}] {prod['emoji']} {prod['name']} (v{variation}) → {platform}")
        print(f"  📅 {scheduled_at}")

        status_code, response = create_post(
            caption=caption,
            scheduled_at=scheduled_at,
            account_ids=account_ids,
            media_ids=[media_id]
        )

        if status_code in (200, 201):
            post_id = None
            if isinstance(response, dict):
                post_id = response.get("id") or (response.get("data") or {}).get("id")
            print(f"  ✅ Created! post_id={post_id}")
            created_count += 1
            results["posts_created"].append({
                "product": prod["name"],
                "variation": variation,
                "platform": platform,
                "account_ids": account_ids,
                "scheduled_at": scheduled_at,
                "post_id": post_id,
                "media_id": media_id
            })
        else:
            print(f"  ❌ Failed: {status_code} - {str(response)[:200]}")
            error_count += 1
            results["errors"].append({
                "product": prod["name"],
                "variation": variation,
                "platform": platform,
                "status_code": status_code,
                "response": str(response)[:300]
            })

        # Rate limiting
        time.sleep(0.15)

    # Summary
    results["summary"] = {
        "total_posts_attempted": len(post_queue),
        "posts_created": created_count,
        "errors": error_count,
        "images_uploaded": len(media_cache),
        "platforms": {
            "instagram": sum(1 for p in results["posts_created"] if p["platform"] == "instagram"),
            "tiktok": sum(1 for p in results["posts_created"] if p["platform"] == "tiktok"),
            "facebook": sum(1 for p in results["posts_created"] if p["platform"] == "facebook"),
        },
        "schedule_range": "2026-03-13 to 2026-03-19",
        "completed_at": datetime.now(TZ).isoformat()
    }

    # Save log
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("📊 CAMPAIGN REBUILD RESULTS")
    print("=" * 60)
    print(f"✅ Posts created: {created_count}/{len(post_queue)}")
    print(f"❌ Errors: {error_count}")
    print(f"🖼️  Images uploaded: {len(media_cache)}")
    print(f"📱 Instagram: {results['summary']['platforms']['instagram']} posts")
    print(f"🎵 TikTok: {results['summary']['platforms']['tiktok']} posts")
    print(f"👥 Facebook: {results['summary']['platforms']['facebook']} posts")
    print(f"📅 Schedule: March 13-19, 2026")
    print(f"📋 Log: {LOG_FILE}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    main()
