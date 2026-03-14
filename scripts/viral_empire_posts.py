#!/usr/bin/env python3
"""
Viral Empire Posts - "The AI Empire" Formula
Schedule 5 viral Indonesian AI content posts via PostBridge
"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta

API_BASE = "https://api.post-bridge.com/v1"
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Account IDs
TIKTOK_IDS = [48374, 48373, 48372, 48338, 48337, 48336, 48335]
INSTAGRAM_IDS = [48186]
FACEBOOK_IDS = [48178, 48177]

# WIB = UTC+7
WIB = timezone(timedelta(hours=7))

def wib_to_iso(year, month, day, hour, minute=0):
    """Convert WIB time to ISO 8601 UTC string for PostBridge"""
    dt_wib = datetime(year, month, day, hour, minute, tzinfo=WIB)
    dt_utc = dt_wib.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

# ============================================================
# POST CONTENT
# ============================================================

POSTS = [
    {
        "id": 1,
        "topic": "10 Prompt Gemini untuk Bikin Channel YouTube AI dari Nol",
        "caption": """🚨 BREAKING: Gemini AI sekarang bisa bantu kamu bikin channel YouTube dari NOL sampai CUAN — GRATIS.

Ini 10 prompt yang udah terbukti:

1️⃣ "Buatkan 10 ide video YouTube niche AI tools untuk pemula Indonesia, dengan judul yang clickbait dan edukatif"
2️⃣ "Tulis skrip video YouTube 5 menit tentang [topik AI], gaya santai, untuk audiens 18-35 tahun Indonesia"
3️⃣ "Buat deskripsi YouTube SEO-friendly + 15 hashtag viral untuk video tentang [topik]"
4️⃣ "Buatkan thumbnail concept untuk video YouTube dengan hook visual yang bikin penonton WAJIB klik"
5️⃣ "Analisa 5 channel YouTube AI terpopuler Indonesia dan temukan gap konten yang bisa aku isi"
6️⃣ "Buat content calendar 30 hari untuk channel YouTube AI, mix antara tutorial, review, dan news"
7️⃣ "Tulis hook pembuka video yang bikin penonton stay 3 menit pertama (pattern interrupt technique)"
8️⃣ "Buat skrip end screen CTA yang convert penonton jadi subscriber + klik link di deskripsi"
9️⃣ "Buatkan judul A/B test untuk 5 video — versi curiosity gap vs versi how-to"
🔟 "Analisa komentar negatif dari video [kompetitor] dan jadikan konten 'solusi' yang viral"

💡 Channel YouTube AI bisa hasilin IDR 5-50 juta/bulan dari AdSense + affiliate.

Mau tools AI yang langsung bisa dipake untuk bikin konten edukatif? 
👉 Guru Pintar AI: https://lynk.id/jendralbot/6821op5e24kn

Save buat nanti 📌

#YouTubeAI #PromptGemini #BikinChannelYouTube #AIIndonesia #ContenCreator #YouTubeIndonesia #MonetisasiYouTube #AIGratis #DigitalMarketing #BerkahKarya""",
        "image": "guru_pintar_ai_indo_polished.png",
        "scheduled_wib": (2026, 3, 13, 7, 0),
        "platforms": INSTAGRAM_IDS + FACEBOOK_IDS,
    },
    {
        "id": 2,
        "topic": "10 Prompt ChatGPT untuk Bisnis Kuliner Autopilot",
        "caption": """🚨 BREAKING: ChatGPT sekarang bisa jalanin bisnis kuliner kamu hampir AUTOPILOT — dan ini GRATIS!

10 prompt wajib pemilik warung & resto:

1️⃣ "Buat menu digital lengkap untuk [nama warung] dengan deskripsi menggugah selera + estimasi HPP untuk setiap menu"
2️⃣ "Analisa tren makanan viral di Indonesia 2026 dan rekomendasikan 5 menu baru yang cocok untuk [konsep warung aku]"
3️⃣ "Tulis caption Instagram untuk foto [nama makanan] yang bikin orang langsung order — pakai emotional trigger"
4️⃣ "Buat SOP operasional harian untuk warung makan 1 kasir, 2 koki — dari buka sampai tutup"
5️⃣ "Hitung food cost ratio untuk [menu] dengan bahan: [list bahan + harga] dan tentukan harga jual optimal"
6️⃣ "Buat strategi promo weekend yang bisa naikkan omset 30% tanpa bakar uang iklan"
7️⃣ "Tulis template balas review negatif di Google Maps yang profesional dan bikin pelanggan balik lagi"
8️⃣ "Buat paket bundling menu yang psikologis bikin orang pilih paket paling mahal"
9️⃣ "Buat script video TikTok 60 detik untuk promosi [nama warung] yang bisa viral"
🔟 "Analisa kenapa bisnis kuliner di [lokasi] sering gagal dan berikan solusi step by step"

💰 Dengan AI, 1 orang bisa kelola 3 outlet sekaligus!

Mau template menu digital + sistem AI lengkap untuk kuliner? 
👉 Mesin Cetak Bisnis Kuliner: https://lynk.id/jendralbot/kzryk28dxmpx

Save buat nanti 📌

#BisnisKuliner #ChatGPTIndonesia #AIRestoran #WarungModern #KulinerIndonesia #DigitalWarung #AIBisnis #FoodBusiness #AutopilotBisnis #BerkahKarya""",
        "image": "mesin_cetak_kuliner_indo_polished.png",
        "scheduled_wib": (2026, 3, 13, 12, 0),
        "platforms": INSTAGRAM_IDS + FACEBOOK_IDS,
    },
    {
        "id": 3,
        "topic": "10 Prompt AI untuk Jadi Affiliate TikTok Penghasilan Jutaan",
        "caption": """🚨 BREAKING: AI sekarang bisa bikin kamu jadi affiliate TikTok JUTAWAN — bahkan tanpa modal awal!

10 prompt yang udah terbukti convert:

1️⃣ "Analisa 10 produk trending di TikTok Shop Indonesia minggu ini dan pilih yang commission-nya paling tinggi"
2️⃣ "Tulis script video TikTok 30 detik untuk review [produk] dengan teknik AIDA — Attention, Interest, Desire, Action"
3️⃣ "Buat hook TikTok 3 detik pertama yang bikin orang STOP scroll untuk produk [kategori]"
4️⃣ "Analisa kenapa video affiliate [kompetitor] viral dan replikasi strateginya untuk produk aku"
5️⃣ "Buat daftar 20 hashtag TikTok yang lagi trending untuk niche [kategori produk] di Indonesia"
6️⃣ "Tulis 5 variasi caption TikTok yang soft-selling untuk produk [nama] — jangan keliatan jualan"
7️⃣ "Buat konten series 7 video untuk satu produk affiliate — dari awareness sampai purchase"
8️⃣ "Cari angle unik untuk review [produk] yang belum pernah dipakai kompetitor lain"
9️⃣ "Buat template DM untuk follow up calon pembeli yang klik link tapi belum checkout"
🔟 "Tentukan jam posting optimal TikTok untuk target audiens ibu rumah tangga / mahasiswa / pekerja di Indonesia"

💸 Affiliate TikTok bisa hasilin IDR 3-50 juta/bulan dari rumah!

Mau blueprint lengkap Affiliate TikTok dari A-Z?
👉 Kelas Affiliate TikTok: https://lynk.id/jendralbot/regxdn7xkpz6

Save buat nanti 📌

#AffiliateTikTok #TikTokShop #CaraKayaTikTok #AIAffiliate #TikTokIndonesia #JualanOnline #PenghasilanTambahan #AIMarketing #DigitalIncome #BerkahKarya""",
        "image": "marketplace_pro_indo_polished.png",
        "scheduled_wib": (2026, 3, 13, 18, 0),
        "platforms": INSTAGRAM_IDS + TIKTOK_IDS,
    },
    {
        "id": 4,
        "topic": "10 Tool AI Gratis yang Bisa Gantikan Karyawan Rp 5 Juta/Bulan",
        "caption": """🚨 BREAKING: Ada 10 tool AI GRATIS yang bisa gantikan karyawan bergaji Rp 5 juta/bulan — dan LEGAL!

Ini dia daftarnya:

1️⃣ **ChatGPT Free** → Gantiin admin copywriter (hemat Rp 3-5 juta/bulan)
2️⃣ **Canva AI** → Gantiin desainer grafis untuk konten harian (hemat Rp 3-8 juta/bulan)
3️⃣ **Gemini** → Gantiin research analyst + content strategist (hemat Rp 4-7 juta/bulan)
4️⃣ **CapCut AI** → Gantiin video editor TikTok/Reels (hemat Rp 2-5 juta/bulan)
5️⃣ **Google NotebookLM** → Gantiin analyst yang baca & rangkum dokumen (hemat Rp 3-6 juta/bulan)
6️⃣ **Claude.ai Free** → Gantiin customer service AI 24 jam (hemat Rp 3-5 juta/bulan)
7️⃣ **ElevenLabs Free** → Gantiin voice over artist (hemat Rp 1-3 juta/bulan)
8️⃣ **Runway Free** → Gantiin video content creator (hemat Rp 3-8 juta/bulan)
9️⃣ **Perplexity AI** → Gantiin market researcher (hemat Rp 3-5 juta/bulan)
🔟 **Make.com Free** → Gantiin operations manager untuk automasi (hemat Rp 4-8 juta/bulan)

💡 Total penghematan potensial: Rp 29-60 juta/bulan!

Mau paket lengkap AI Creative Tools untuk bisnis?
👉 AI Creative Tools: https://lynk.id/jendralbot/89d30qd3ddnj

Save buat nanti 📌

#AIGratis #ToolAI #HematKaryawan #AIBisnis #DigitalTransformasi #AIIndonesia #AutomasiAI #BisnisCerdas #TechIndonesia #BerkahKarya""",
        "image": "ai_content_pro_seller_indo_polished.png",
        "scheduled_wib": (2026, 3, 14, 7, 0),
        "platforms": INSTAGRAM_IDS + FACEBOOK_IDS,
    },
    {
        "id": 5,
        "topic": "10 Cara AI Bantu UMKM Indonesia Naik Kelas (Step by Step)",
        "caption": """🚨 BREAKING: AI udah bantu ribuan UMKM Indonesia naik kelas — dan kamu bisa mulai HARI INI!

10 cara step by step:

1️⃣ **Branding Profesional** → Pakai AI buat logo, tagline, dan visual brand dalam 1 hari (dulu butuh Rp 5-20 juta)
2️⃣ **Website/Toko Online** → AI bisa buat website jual produk dalam 2 jam tanpa coding
3️⃣ **Konten Sosmed Autopilot** → Generate 30 hari konten IG/TikTok sekaligus pakai 1 prompt
4️⃣ **Customer Service 24 Jam** → Chatbot AI balas WA/IG customer jam 3 pagi sekalipun
5️⃣ **Iklan yang Convert** → AI analisa target market + tulis copy iklan Meta/TikTok yang proven
6️⃣ **Manajemen Stok** → AI prediksi stok yang bakal habis sebelum kehabisan
7️⃣ **Laporan Keuangan** → Upload data Excel → AI langsung analisa profit/loss + rekomendasi
8️⃣ **Ekspansi ke Marketplace** → AI bantu optimasi listing Shopee/Tokopedia untuk rank #1
9️⃣ **Email Marketing** → AI tulis campaign email yang open rate-nya 40%+ (rata-rata industri 20%)
🔟 **Hiring & Training** → AI buat JD, screening soal, bahkan onboarding document otomatis

📈 UMKM yang pakai AI tumbuh 3x lebih cepat (Data McKinsey 2025)

Mau sistem lengkap untuk UMKM naik kelas?
👉 Studio Marketplace Pro: https://lynk.id/jendralbot/emne05mm7v25

Save buat nanti 📌

#UMKMIndonesia #AIuntukUMKM #NaikKelas #DigitalUMKM #BisnisMaju #AIBisnis #UMKMDigital #TransformasiDigital #BerkahKarya #EkonomiKreatif""",
        "image": "bundle_master_infographic.jpg",
        "scheduled_wib": (2026, 3, 14, 12, 0),
        "platforms": INSTAGRAM_IDS + TIKTOK_IDS,
    },
]

OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/output")


def upload_media(image_filename):
    """Upload media to PostBridge and return media_id"""
    image_path = os.path.join(OUTPUT_DIR, image_filename)
    if not os.path.exists(image_path):
        print(f"  ❌ Image not found: {image_path}")
        return None

    # Step 1: Get upload URL
    ext = image_filename.rsplit(".", 1)[-1].lower()
    mime_type = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    file_size = os.path.getsize(image_path)

    payload = {
        "name": image_filename,
        "mime_type": mime_type,
        "size_bytes": file_size
    }
    resp = requests.post(f"{API_BASE}/media/create-upload-url", headers=HEADERS, json=payload)
    
    if resp.status_code not in (200, 201):
        print(f"  ❌ Failed to get upload URL: {resp.status_code} {resp.text[:300]}")
        return None

    data = resp.json()
    print(f"  📤 Upload URL response: {json.dumps(data)[:200]}")
    
    upload_url = data.get("upload_url") or data.get("url") or data.get("uploadUrl")
    media_id = data.get("media_id") or data.get("id") or data.get("mediaId")

    if not upload_url:
        print(f"  ❌ No upload_url in response: {data}")
        return media_id  # might already have media_id without upload step

    # Step 2: Upload file
    with open(image_path, "rb") as f:
        file_data = f.read()

    put_headers = {"Content-Type": mime_type, "Content-Length": str(len(file_data))}
    put_resp = requests.put(upload_url, data=file_data, headers=put_headers)
    
    if put_resp.status_code not in (200, 201, 204):
        print(f"  ❌ Upload PUT failed: {put_resp.status_code} {put_resp.text[:200]}")
        return None

    print(f"  ✅ Media uploaded successfully, media_id={media_id}")
    return media_id


def create_post(caption, scheduled_wib, account_ids, media_id=None):
    """Create a scheduled post via PostBridge"""
    scheduled_at = wib_to_iso(*scheduled_wib)
    
    payload = {
        "caption": caption,
        "scheduled_at": scheduled_at,
        "social_accounts": account_ids,
    }
    
    if media_id:
        payload["media"] = [{"media_id": media_id}]

    resp = requests.post(f"{API_BASE}/posts", headers=HEADERS, json=payload)
    return resp.status_code, resp.json()


def main():
    print("=" * 60)
    print("🔥 VIRAL EMPIRE POSTS - AI Formula Scheduler")
    print("=" * 60)

    results = []

    for post in POSTS:
        print(f"\n📝 POST {post['id']}: {post['topic'][:50]}...")
        
        scheduled_str = f"{post['scheduled_wib'][2]:02d}/{post['scheduled_wib'][1]:02d} {post['scheduled_wib'][3]:02d}:00 WIB"
        platforms = []
        if any(pid in INSTAGRAM_IDS for pid in post["platforms"]):
            platforms.append("Instagram")
        if any(pid in FACEBOOK_IDS for pid in post["platforms"]):
            platforms.append("Facebook")
        if any(pid in TIKTOK_IDS for pid in post["platforms"]):
            platforms.append(f"TikTok x{len([p for p in post['platforms'] if p in TIKTOK_IDS])}")
        print(f"  📅 Scheduled: {scheduled_str}")
        print(f"  📱 Platforms: {', '.join(platforms)}")
        print(f"  🖼️  Image: {post['image']}")

        # Upload media
        media_id = upload_media(post["image"])

        # Create post
        # For Instagram accounts, always include media
        # For TikTok/Facebook without media, skip media requirement
        ig_accounts = [pid for pid in post["platforms"] if pid in INSTAGRAM_IDS]
        non_ig_accounts = [pid for pid in post["platforms"] if pid not in INSTAGRAM_IDS]

        post_results = []

        # Post to Instagram + any FB (with media)
        if ig_accounts or (non_ig_accounts and not any(pid in TIKTOK_IDS for pid in non_ig_accounts)):
            combined_with_media = ig_accounts + [pid for pid in non_ig_accounts if pid in FACEBOOK_IDS]
            if combined_with_media and media_id:
                status, resp = create_post(post["caption"], post["scheduled_wib"], combined_with_media, media_id)
                post_id = resp.get("id") or resp.get("post_id") or "?"
                print(f"  {'✅' if status in (200,201) else '❌'} IG+FB post: HTTP {status} | post_id={post_id}")
                if status not in (200, 201):
                    print(f"  Response: {json.dumps(resp)[:300]}")
                post_results.append({"accounts": "IG+FB", "status": status, "post_id": post_id})
            elif combined_with_media and not media_id:
                # Try without media for FB only
                fb_only = [pid for pid in combined_with_media if pid in FACEBOOK_IDS]
                if fb_only:
                    status, resp = create_post(post["caption"], post["scheduled_wib"], fb_only, None)
                    post_id = resp.get("id") or resp.get("post_id") or "?"
                    print(f"  {'✅' if status in (200,201) else '❌'} FB-only (no media): HTTP {status} | post_id={post_id}")
                    post_results.append({"accounts": "FB", "status": status, "post_id": post_id})
                if ig_accounts:
                    print(f"  ⚠️  Skipping Instagram (no media available)")

        # Post to TikTok accounts (no media required for TikTok text-only, but they need video typically)
        # Try scheduling anyway — PostBridge may handle it
        tiktok_in_post = [pid for pid in post["platforms"] if pid in TIKTOK_IDS]
        if tiktok_in_post:
            if media_id:
                status, resp = create_post(post["caption"], post["scheduled_wib"], tiktok_in_post, media_id)
            else:
                status, resp = create_post(post["caption"], post["scheduled_wib"], tiktok_in_post, None)
            post_id = resp.get("id") or resp.get("post_id") or "?"
            print(f"  {'✅' if status in (200,201) else '❌'} TikTok x{len(tiktok_in_post)}: HTTP {status} | post_id={post_id}")
            if status not in (200, 201):
                print(f"  Response: {json.dumps(resp)[:300]}")
            post_results.append({"accounts": f"TikTok x{len(tiktok_in_post)}", "status": status, "post_id": post_id})

        results.append({
            "post_id": post["id"],
            "topic": post["topic"],
            "scheduled": scheduled_str,
            "results": post_results
        })

    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    
    total_success = 0
    total_fail = 0
    
    for r in results:
        print(f"\nPost {r['post_id']}: {r['topic'][:45]}...")
        print(f"  Scheduled: {r['scheduled']}")
        for pr in r["results"]:
            ok = pr["status"] in (200, 201)
            if ok:
                total_success += 1
            else:
                total_fail += 1
            print(f"  {'✅' if ok else '❌'} {pr['accounts']} → post_id={pr['post_id']}")

    print(f"\n🎯 Total: {total_success} scheduled successfully, {total_fail} failed")


if __name__ == "__main__":
    main()
