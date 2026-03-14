#!/usr/bin/env python3
"""Fix Instagram posts that failed due to missing size_bytes in media upload"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta

API_BASE = "https://api.post-bridge.com/v1"
API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

INSTAGRAM_IDS = [48186]
FACEBOOK_IDS = [48178, 48177]
TIKTOK_IDS = [48374, 48373, 48372, 48338, 48337, 48336, 48335]

WIB = timezone(timedelta(hours=7))
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/output")


def wib_to_iso(year, month, day, hour, minute=0):
    dt_wib = datetime(year, month, day, hour, minute, tzinfo=WIB)
    dt_utc = dt_wib.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def upload_media(image_filename):
    image_path = os.path.join(OUTPUT_DIR, image_filename)
    if not os.path.exists(image_path):
        print(f"  ❌ Image not found: {image_path}")
        return None

    ext = image_filename.rsplit(".", 1)[-1].lower()
    mime_type = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    file_size = os.path.getsize(image_path)

    payload = {"name": image_filename, "mime_type": mime_type, "size_bytes": file_size}
    resp = requests.post(f"{API_BASE}/media/create-upload-url", headers=HEADERS, json=payload)
    
    if resp.status_code not in (200, 201):
        print(f"  ❌ Upload URL failed: {resp.status_code} {resp.text[:300]}")
        return None

    data = resp.json()
    print(f"  📤 Upload URL response keys: {list(data.keys())}")
    
    # Find upload URL and media_id from response
    upload_url = (data.get("upload_url") or data.get("url") or 
                  data.get("uploadUrl") or data.get("signed_url"))
    media_id = (data.get("media_id") or data.get("id") or 
                data.get("mediaId") or data.get("file_id"))
    
    if not upload_url:
        print(f"  ❌ No upload URL in: {json.dumps(data)[:400]}")
        return None

    # Upload file
    with open(image_path, "rb") as f:
        file_data = f.read()

    put_resp = requests.put(upload_url, data=file_data, headers={"Content-Type": mime_type})
    
    if put_resp.status_code not in (200, 201, 204):
        print(f"  ❌ PUT failed: {put_resp.status_code} {put_resp.text[:200]}")
        return None

    # Check if media_id comes back after upload
    if not media_id:
        try:
            put_data = put_resp.json()
            media_id = put_data.get("media_id") or put_data.get("id")
        except:
            pass

    print(f"  ✅ Uploaded! media_id={media_id}")
    return media_id


def create_post(caption, scheduled_wib, account_ids, media_id=None):
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


# Instagram posts to fix
IG_POSTS = [
    {
        "id": 1,
        "image": "guru_pintar_ai_indo_polished.png",
        "scheduled_wib": (2026, 3, 13, 7, 0),
        "accounts": INSTAGRAM_IDS,
        "caption": """🚨 BREAKING: Gemini AI sekarang bisa bantu kamu bikin channel YouTube dari NOL sampai CUAN — GRATIS.

Ini 10 prompt yang udah terbukti:

1️⃣ "Buatkan 10 ide video YouTube niche AI tools untuk pemula Indonesia"
2️⃣ "Tulis skrip video YouTube 5 menit tentang [topik AI], gaya santai"
3️⃣ "Buat deskripsi YouTube SEO-friendly + 15 hashtag viral"
4️⃣ "Buatkan thumbnail concept yang bikin penonton WAJIB klik"
5️⃣ "Analisa 5 channel YouTube AI terpopuler & temukan gap konten"
6️⃣ "Buat content calendar 30 hari untuk channel YouTube AI"
7️⃣ "Tulis hook pembuka video yang bikin penonton stay 3 menit"
8️⃣ "Buat skrip end screen CTA yang convert jadi subscriber"
9️⃣ "Buatkan judul A/B test: curiosity gap vs how-to"
🔟 "Analisa komentar negatif & jadikan konten 'solusi' viral"

💡 Channel YouTube AI bisa hasilin IDR 5-50 juta/bulan!

Guru Pintar AI: https://lynk.id/jendralbot/6821op5e24kn

Save buat nanti 📌

#YouTubeAI #PromptGemini #BikinChannelYouTube #AIIndonesia #ContentCreator #YouTubeIndonesia #MonetisasiYouTube #AIGratis #DigitalMarketing #BerkahKarya"""
    },
    {
        "id": 2,
        "image": "mesin_cetak_kuliner_indo_polished.png",
        "scheduled_wib": (2026, 3, 13, 12, 0),
        "accounts": INSTAGRAM_IDS,
        "caption": """🚨 BREAKING: ChatGPT sekarang bisa jalanin bisnis kuliner kamu hampir AUTOPILOT!

10 prompt wajib pemilik warung & resto:

1️⃣ "Buat menu digital lengkap dengan deskripsi menggugah selera + estimasi HPP"
2️⃣ "Analisa tren makanan viral Indonesia 2026 & rekomendasikan menu baru"
3️⃣ "Tulis caption Instagram yang bikin orang langsung order"
4️⃣ "Buat SOP operasional harian warung 1 kasir, 2 koki"
5️⃣ "Hitung food cost ratio & tentukan harga jual optimal"
6️⃣ "Buat strategi promo weekend yang naikkan omset 30%"
7️⃣ "Tulis template balas review negatif di Google Maps"
8️⃣ "Buat paket bundling yang bikin orang pilih paket paling mahal"
9️⃣ "Buat script video TikTok 60 detik untuk promosi warung"
🔟 "Analisa kenapa bisnis kuliner sering gagal & berikan solusi"

💰 Dengan AI, 1 orang bisa kelola 3 outlet sekaligus!

Mesin Cetak Bisnis Kuliner: https://lynk.id/jendralbot/kzryk28dxmpx

Save buat nanti 📌

#BisnisKuliner #ChatGPTIndonesia #AIRestoran #WarungModern #KulinerIndonesia #DigitalWarung #AIBisnis #FoodBusiness #AutopilotBisnis #BerkahKarya"""
    },
    {
        "id": 4,
        "image": "ai_content_pro_seller_indo_polished.png",
        "scheduled_wib": (2026, 3, 14, 7, 0),
        "accounts": INSTAGRAM_IDS,
        "caption": """🚨 BREAKING: 10 tool AI GRATIS yang bisa gantikan karyawan Rp 5 juta/bulan!

1️⃣ ChatGPT Free → Gantiin admin copywriter (hemat Rp 3-5 juta/bulan)
2️⃣ Canva AI → Gantiin desainer grafis (hemat Rp 3-8 juta/bulan)
3️⃣ Gemini → Gantiin research analyst (hemat Rp 4-7 juta/bulan)
4️⃣ CapCut AI → Gantiin video editor (hemat Rp 2-5 juta/bulan)
5️⃣ Google NotebookLM → Gantiin analyst dokumen (hemat Rp 3-6 juta/bulan)
6️⃣ Claude.ai Free → Gantiin customer service 24 jam (hemat Rp 3-5 juta/bulan)
7️⃣ ElevenLabs Free → Gantiin voice over artist (hemat Rp 1-3 juta/bulan)
8️⃣ Runway Free → Gantiin video content creator (hemat Rp 3-8 juta/bulan)
9️⃣ Perplexity AI → Gantiin market researcher (hemat Rp 3-5 juta/bulan)
🔟 Make.com Free → Gantiin operations manager (hemat Rp 4-8 juta/bulan)

💡 Total hemat potensial: Rp 29-60 juta/bulan!

AI Creative Tools: https://lynk.id/jendralbot/89d30qd3ddnj

Save buat nanti 📌

#AIGratis #ToolAI #HematKaryawan #AIBisnis #DigitalTransformasi #AIIndonesia #AutomasiAI #BisnisCerdas #TechIndonesia #BerkahKarya"""
    },
    {
        "id": 5,
        "image": "bundle_master_infographic.jpg",
        "scheduled_wib": (2026, 3, 14, 12, 0),
        "accounts": INSTAGRAM_IDS,
        "caption": """🚨 BREAKING: AI udah bantu ribuan UMKM Indonesia naik kelas — kamu bisa mulai HARI INI!

10 cara step by step:

1️⃣ Branding Profesional → Logo & visual brand dalam 1 hari
2️⃣ Website/Toko Online → Buat dalam 2 jam tanpa coding
3️⃣ Konten Sosmed Autopilot → Generate 30 hari konten sekaligus
4️⃣ Customer Service 24 Jam → Chatbot balas WA/IG jam 3 pagi
5️⃣ Iklan yang Convert → AI analisa target + tulis copy iklan
6️⃣ Manajemen Stok → AI prediksi stok sebelum kehabisan
7️⃣ Laporan Keuangan → Upload Excel → AI analisa profit/loss
8️⃣ Ekspansi Marketplace → AI optimasi listing Shopee/Tokopedia rank #1
9️⃣ Email Marketing → Campaign dengan open rate 40%+
🔟 Hiring & Training → JD, screening soal, onboarding otomatis

📈 UMKM yang pakai AI tumbuh 3x lebih cepat!

Studio Marketplace Pro: https://lynk.id/jendralbot/emne05mm7v25

Save buat nanti 📌

#UMKMIndonesia #AIuntukUMKM #NaikKelas #DigitalUMKM #BisnisMaju #AIBisnis #UMKMDigital #TransformasiDigital #BerkahKarya #EkonomiKreatif"""
    },
]


def main():
    print("=" * 60)
    print("🔧 FIX: Instagram Posts with Media Upload")
    print("=" * 60)

    success = 0
    fail = 0

    for post in IG_POSTS:
        print(f"\n📸 Post {post['id']} → Instagram")
        print(f"  Image: {post['image']}")
        
        media_id = upload_media(post["image"])
        
        if not media_id:
            # Try without media_id if upload failed (will likely fail for IG but try)
            print(f"  ⚠️  Trying without media...")
            status, resp = create_post(post["caption"], post["scheduled_wib"], post["accounts"], None)
        else:
            status, resp = create_post(post["caption"], post["scheduled_wib"], post["accounts"], media_id)
        
        post_id = resp.get("id") or resp.get("post_id") or "?"
        ok = status in (200, 201)
        if ok:
            success += 1
        else:
            fail += 1
        print(f"  {'✅' if ok else '❌'} HTTP {status} | post_id={post_id}")
        if not ok:
            print(f"  Response: {json.dumps(resp)[:300]}")

    print(f"\n{'='*60}")
    print(f"✅ Instagram posts: {success} scheduled, {fail} failed")


if __name__ == "__main__":
    main()
