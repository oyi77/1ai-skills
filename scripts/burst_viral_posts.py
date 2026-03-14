#!/usr/bin/env python3
"""
Burst Viral Posts — Prime Time Saturday
Deploy 5 posts with viral hooks at 17:00-21:00 WIB
Target: TikTok, Instagram, Facebook, Threads (NOT YouTube for images)
"""
import requests, json, time
from datetime import datetime, timezone, timedelta

API = "https://api.post-bridge.com/v1"
KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
HDR = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

# WIB = UTC+7
WIB = timezone(timedelta(hours=7))

# Account groups by platform (NO YouTube for images)
TIKTOK_IDS = [49663, 49659, 49642, 48374, 48373, 48372, 48338, 48337, 48336, 48335]
INSTAGRAM_IDS = [49682, 49676, 49661, 49644, 49640, 49630, 49619, 49612, 48186, 47681]
FACEBOOK_IDS = [49675, 49674, 49673, 49672, 49671, 49670, 49669, 49668, 49667, 49666,
                49665, 49664, 49611, 49609, 49607, 49606, 49605, 49604, 49603, 49602,
                49601, 49600, 49599, 49598, 48178, 48177, 48176, 48175, 48174, 48173,
                48172, 48171, 48170, 47664, 45675, 45673, 45629]
THREADS_IDS = [49683, 49680, 49677, 49662, 49658, 49646, 49641, 49635, 49631, 49618,
               49614, 49613]
TWITTER_IDS = [49814, 47682]

# All non-YouTube accounts
ALL_ACCOUNTS = list(set(TIKTOK_IDS + INSTAGRAM_IDS + FACEBOOK_IDS + THREADS_IDS + TWITTER_IDS))

# Images per product (from product_media_ids.json)
PRODUCT_IMAGES = {
    "jobmagnet": {
        "media_ids": ["4732235b-33af-45d2-9bec-4e393bdf26d5"],
        "url": "lynk.id/jendralbot"
    },
    "sellpix": {
        "media_ids": ["24d56899-9385-4e9d-b9d4-cc42ffd0768a"],
        "url": "lynk.id/jendralbot"
    },
    "guru_pintar": {
        "media_ids": ["2c87eaab-8a1e-4c88-973a-f6281cbdf22f"],
        "url": "lynk.id/jendralbot"
    },
    "ai_creative": {
        "media_ids": ["a0d01422-dbd0-4892-afd3-95cdbe7362b4"],
        "url": "lynk.id/jendralbot"
    },
    "kuliner": {
        "media_ids": ["3f02277e-d12e-4fb6-b5f7-fd44d09fa1bf"],
        "url": "lynk.id/jendralbot"
    }
}

# VIRAL CAPTIONS — 5 angles, 5 products
BURST_POSTS = [
    {
        "hour_wib": 17,
        "product": "jobmagnet",
        "caption": """Teman saya ketawa waktu gue bilang bayar IDR 75K buat tools AI...

3 minggu kemudian, dia DM nanya link-nya. 🤣

JobMagnet AI ngebantu gue:
✅ Bikin CV yang lolos ATS (Applicant Tracking System)
✅ Jawab interview pakai framework STAR otomatis
✅ Nego gaji dengan data pasar yang akurat

Gue apply 10 perusahaan, dipanggil 7. Sebelumnya? Apply 20, dipanggil 2.

Bukan karena gue tiba-tiba jadi lebih pinter.
Tapi karena sekarang CV gue *kelihatan* lebih pinter. 😏

Tools ini cuma IDR 75K. Harga 1x makan di mall.
Tapi bisa naikin gaji kamu IDR 2-5 juta/bulan.

ROI? Kamu hitung sendiri.

👉 lynk.id/jendralbot

#JobMagnet #CariKerja #Karir #AITools #Interview #CV #HiringIndonesia #TipsCariKerja""",
        "hashtag_group": "career"
    },
    {
        "hour_wib": 18,
        "product": "sellpix",
        "caption": """FAKTA yang bikin seller Shopee/Tokopedia sedih:

Foto produk jelek = konversi rendah = pendapatan mampet.
Padahal produknya BAGUS. 😭

Dulu gue bayar fotografer IDR 300K-500K per sesi.
10 foto produk = IDR 30K-50K per foto.
Sebulan bisa habis IDR 2-3 juta cuma buat foto.

Sekarang? 
Pake SellPix AI, hasilnya sama — bahkan lebih konsisten.
Biaya? Sekali bayar IDR 75K. Selamanya.

Algoritma marketplace rewarding foto berkualitas tinggi.
Kompetitor yang belum tau ini? Ketinggalan terus. 

Gak percaya? Coba dulu 7 hari. Ada garansi uang kembali.

👉 lynk.id/jendralbot

#SellPix #FotoProduk #Shopee #Tokopedia #JualanOnline #Marketplace #UMKM #SellerIndonesia""",
        "hashtag_group": "seller"
    },
    {
        "hour_wib": 19,
        "product": "guru_pintar",
        "caption": """Guru-guru, jujur: berapa jam per minggu kamu habiskan buat bikin soal ujian?

3 jam? 5 jam? Lebih? 

Sementara yang kamu SEHARUSNYA kerjain:
- Komunikasi dengan murid
- Inovasi metode belajar  
- Self-development

Guru Pintar AI ngerjain yang ribet buat kamu:
⚡ Generate 50 soal dalam 30 detik
⚡ Buat materi dari outline doang
⚡ RPP otomatis sesuai kurikulum
⚡ Laporan nilai auto-calculated

Teman saya sesama guru bilang:
"Waktu produktif naik 60%. Murid lebih engaged. Gue gak burnout lagi."

IDR 75.000. Sekali beli, seumur hidup.
Bandingkan dengan 5+ jam kerja manual tiap minggu.

Waktu kamu lebih berharga dari itu. ❤️

👉 lynk.id/jendralbot

#GuruPintar #Guru #Pendidikan #EdTech #AIGuru #RPP #BuatSoal #TipsGuru #Indonesia""",
        "hashtag_group": "education"
    },
    {
        "hour_wib": 20,
        "product": "ai_creative",
        "caption": """⚠️ HARGA NAIK BESOK PAGI JAM 06:00 WIB ⚠️

Masih IDR 75.000 sampai malam ini.
Besok? Balik ke harga asli IDR 250.000.

AI Creative Tools — yang udah dipakai 500+ content creator Indonesia:

🎨 Generate gambar produk (no photographer needed)
✍️ Caption & copy otomatis  
📱 Template konten siap pakai 50+
🔥 Hook generator untuk TikTok/IG/YouTube

Kalau kamu masih bikin konten manual, kompetitormu udah 10 langkah lebih maju.

Tinggal 6 jam lagi di harga ini.

Gak mau nyesel? Grab sekarang:
👉 lynk.id/jendralbot

#AICreativeTools #ContentCreator #TikTok #Instagram #DigitalMarketing #ContentMarketing #Viral #FOMO""",
        "hashtag_group": "creator"
    },
    {
        "hour_wib": 21,
        "product": "kuliner",
        "caption": """60% bisnis kuliner tutup di tahun pertama.

Bukan karena makanannya gak enak.
Tapi karena MANAGEMEN yang berantakan. 📊

Yang sering salah:
❌ Harga jual gak cover HPP
❌ Menu terlalu banyak → operasional chaos
❌ Gak ada food costing yang benar

Mesin Cetak Bisnis Kuliner ngasi kamu:
✅ Template food costing otomatis
✅ Desain menu profesional (bisnis kamu kelihatan legit)
✅ Marketing plan F&B yang proven
✅ SOP operasional ready-to-use

Banyak warung & cafe naik omzet 25-40% setelah pake ini.
Bukan janji — itu data dari pengguna kami.

IDR 75.000 saja. Seharga 2 porsi nasi goreng.
Tapi bisa selamatkan bisnis kamu.

👉 lynk.id/jendralbot

#BisnisKuliner #UMKM #Warung #Cafe #Restoran #FoodBusiness #FoodCost #MenuDesign #TipsBisnis #Indonesia""",
        "hashtag_group": "culinary"
    }
]

def make_utc_schedule(hour_wib, minute=0):
    """Convert WIB hour to UTC datetime string"""
    now_wib = datetime.now(WIB)
    target_wib = now_wib.replace(hour=hour_wib, minute=minute, second=0, microsecond=0)
    if target_wib <= now_wib:
        target_wib += timedelta(days=1)
    return target_wib.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

def post_burst(post_config):
    product_key = post_config["product"]
    product = PRODUCT_IMAGES[product_key]
    schedule_time = make_utc_schedule(post_config["hour_wib"])
    
    payload = {
        "caption": post_config["caption"],
        "social_accounts": ALL_ACCOUNTS,
        "media": product["media_ids"],
        "scheduled_at": schedule_time
    }
    
    r = requests.post(f"{API}/posts", headers=HDR, json=payload)
    result = r.json()
    
    if r.status_code in [200, 201]:
        post_id = result.get("data", {}).get("id", "?")
        print(f"✅ {post_config['hour_wib']}:00 WIB | {product_key} | id={post_id} | accounts={len(ALL_ACCOUNTS)}")
        return post_id
    else:
        print(f"❌ {post_config['hour_wib']}:00 WIB | {product_key} | Error: {r.status_code} | {str(result)[:100]}")
        return None

print(f"=== BURST VIRAL POSTING — Saturday Prime Time ===")
print(f"Target accounts: {len(ALL_ACCOUNTS)}")
print(f"Posts: {len(BURST_POSTS)} (17:00-21:00 WIB)")
print("")

results = []
for i, post in enumerate(BURST_POSTS):
    result = post_burst(post)
    results.append(result)
    if i < len(BURST_POSTS) - 1:
        time.sleep(1)

success = sum(1 for r in results if r)
print(f"\n=== DONE ===")
print(f"Success: {success}/{len(BURST_POSTS)}")
print(f"Accounts per post: {len(ALL_ACCOUNTS)}")
print(f"Total post deliveries: {success * len(ALL_ACCOUNTS)}")
