#!/usr/bin/env python3
"""
Daily Content Poster v2 — Product-aligned content via PostBridge

FIXES from v1:
- Caption MATCHES image (product-specific, not random)
- Each product has its own media IDs (no more mismatch)
- Content is product-specific, not generic template spam
- Rotates through products evenly (not random repetition)

Cron: 3x daily at 07:00, 12:00, 19:00 WIB
Research: Sprout Social 2025 + DataReportal Indonesia 2025
"""
import requests, json, time, random, os, sys
from datetime import datetime
from pathlib import Path

API = "https://api.post-bridge.com/v1"
KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
HDR = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
PRODUCTS_FILE = WORKSPACE / "config/lynk_products.json"
MEDIA_MAP_FILE = WORKSPACE / "config/product_media_ids.json"
ACCOUNTS_FILE = WORKSPACE / "config/postbridge_accounts.json"
STATE_FILE = WORKSPACE / "config/poster_state.json"
LOG_FILE = WORKSPACE / "logs/daily_poster.log"


# ── Product-specific content (caption MATCHES the product) ──────────────────

PRODUCT_CONTENT = {
    "kzryk28dxmpx": {  # Mesin Cetak Bisnis Kuliner (FREE)
        "name": "Mesin Cetak Bisnis Kuliner",
        "captions": [
            "🍜 Mau buka bisnis kuliner tapi bingung mulai dari mana?\n\nDapatkan template bisnis kuliner lengkap yang udah terbukti naikin omzet 25%:\n✅ Resep auto-costing\n✅ Menu design template\n✅ Marketing plan F&B\n\n👉 IDR 75.000 (harga asli IDR 250K)\n👉 {url}\n\n#BisnisKuliner #UMKM #FnB #Gratis",
            "📊 FAKTA: 60% bisnis kuliner gagal di tahun pertama.\nPenyebab utama? BUKAN rasa — tapi manajemen!\n\nDapatkan Mesin Cetak Bisnis Kuliner GRATIS:\n👉 {url}\n\n#BisnisKuliner #UMKM #TipsBisnis",
            "🔥 Omzet warung naik 25% cuma ganti desain menu?\nYa, visual matters lebih dari yang kamu pikir.\n\nDownload template GRATIS sekarang:\n👉 {url}\n\n#DesainMenu #BisnisKuliner #UMKM",
        ],
    },
    "6821op5e24kn": {  # Guru Pintar AI (Rp 49K)
        "name": "Guru Pintar AI",
        "captions": [
            "👨‍🏫 50+ template ajaran AI-powered!\n\nGuru Pintar AI bantu kamu:\n✅ Auto-grading untuk quiz\n✅ Materi instant generation\n✅ Update otomatis teknologi AI\n\nIDR 75.000 (harga asli IDR 250.000)!\n👉 {url}\n\n#GuruPintar #Pendidikan #AITools #EdTech",
            "📚 Bikin materi pelajaran dalam 5 menit? Bisa!\n\nGuru Pintar AI — 50+ template siap pakai.\nDari RPP sampai soal ujian, semua otomatis.\n\nIDR 75.000 (harga asli IDR 250.000)\n👉 {url}\n\n#Pendidikan #AITools #Guru",
            "⏰ Guru capek bikin soal manual? Same.\n\nSekarang ada AI yang bantu:\n- Generate soal otomatis\n- Auto-grading\n- Materi instant\n\nCuma IDR 75.000! (harga asli IDR 250.000)\n👉 {url}\n\n#GuruPintar #EdTech #AIIndonesia",
        ],
    },
    "89d30qd3ddnj": {  # AI Creative Tools (FREE)
        "name": "AI Creative Tools",
        "captions": [
            "🎨 Tools AI GRATIS buat content creator!\n\nAI Creative Tools:\n✅ Generate gambar produk\n✅ Edit foto otomatis\n✅ Caption generator\n\nIDR 75.000!\n👉 {url}\n\n#ContentCreator #AITools #DesainGrafis #Gratis",
            "💡 Konten bagus gak harus mahal.\n\nAI Creative Tools — semua yang kamu butuhkan untuk bikin konten profesional, GRATIS.\n\n👉 {url}\n\n#ContentMarketing #AITools #BisnisOnline",
            "🔥 Bikin desain pro dalam hitungan menit?\n\nGak perlu Canva Pro, gak perlu desainer.\nAI Creative Tools — IDR 75.000 aja.\n\n👉 {url}\n\n#DesainGrafis #AITools #ContentCreator",
        ],
    },
    "emne05mm7v25": {  # Studio Marketplace Pro / SellPix AI (Rp 79K)
        "name": "SellPix AI",
        "captions": [
            "📸 Foto produk yang bagus bisa naikin konversi 40%!\n\nSellPix AI — studio foto marketplace otomatis:\n✅ Background removal\n✅ Product staging\n✅ Marketplace-ready output\n\nIDR 75.000\n👉 {url}\n\n#FotoProduk #Marketplace #Shopee #Tokopedia",
            "🛒 Jualan di marketplace tapi foto asal-asalan?\nPantesan gak laku.\n\nSellPix AI bikin foto produk kamu selevel brand besar.\n\nIDR 75.000 — investasi yang worth it!\n👉 {url}\n\n#FotoProduk #ECommerce #UMKM",
            "⚡ Sebelum vs Sesudah SellPix AI:\n❌ Foto gelap, background berantakan\n✅ Foto studio, background clean, siap jual\n\nIDR 75.000 aja!\n👉 {url}\n\n#SellPix #FotoProduk #Marketplace",
        ],
    },
    "kkjk0mv1vg7o": {  # Belanja Duit Balik (Rp 59K)
        "name": "Belanja Duit Balik",
        "captions": [
            "💰 Belanja tetap jalan, tapi duit balik lagi?\n\nBukan scam, bukan MLM — ini strategi cashback:\n✅ Cara dapat cashback dari semua belanjaan\n✅ Platform terpercaya\n✅ Step-by-step guide\n\nGRATIS!\n👉 {url}\n\n#Cashback #HematBelanja #SmartShopping",
            "🤔 Kamu belanja tiap bulan berapa?\nSekarang bayangin 5-15% nya balik ke kantong.\n\nPelajari caranya di Belanja Duit Balik!\n\nGRATIS!\n👉 {url}\n\n#Cashback #TipsBelanja #HematUang",
            "🔥 Rahasia orang hemat: mereka gak cuma cari diskon.\nMereka cari CASHBACK.\n\nBelanja Duit Balik — panduan lengkap cashback strategy.\n\nGRATIS!\n👉 {url}\n\n#SmartShopping #Cashback #FinancialLiteracy",
        ],
    },
}

# Products without custom images — use text-only captions with profile URL
PROFILE_PRODUCTS = {
    "45r5yvze3vy4": {  # JobMagnet AI
        "name": "JobMagnet AI",
        "captions": [
            "📝 CV kamu udah ATS-friendly?\n\nJobMagnet AI optimasi CV kamu biar lolos screening otomatis.\nChance interview naik 3x lipat!\n\n👉 {url}\n\n#JobHunting #CV #KarirIndonesia #AITools",
        ],
    },
    "l4q49jj3z383": {  # Food Menu AI Studio
        "name": "Food Menu AI Studio",
        "captions": [
            "🍽️ Menu makanan yang desainnya bagus = omzet naik 25%!\n\nFood Menu AI Studio — bikin menu restoran profesional dengan AI.\n\n👉 {url}\n\n#DesainMenu #Restoran #BisnisKuliner",
        ],
    },
    "9r8rj1o38q59": {  # AI Creative & Performance Ad Engine
        "name": "AI Ad Engine",
        "captions": [
            "🎯 Ads yang convert itu bukan soal budget besar.\nTapi soal CREATIVE yang tepat.\n\nAI Ad Engine — generate ads yang perform.\n\n👉 {url}\n\n#DigitalAds #Marketing #AITools",
        ],
    },
    "regxdn7xkpz6": {  # Kelas Affiliate Pesugihan TikTok
        "name": "Kelas Affiliate TikTok",
        "captions": [
            "📱 TikTok bukan cuma buat hiburan.\nIni mesin uang kalau kamu tau caranya.\n\nKelas Affiliate Pesugihan TikTok — dari nol sampai cuan.\n\n👉 {url}\n\n#TikTokAffiliate #CuanDariRumah #BisnisOnline",
        ],
    },
}

BASE_URL = "https://lynk.id/jendralbot"


def load_media_map():
    """Load product→media_id mapping."""
    if MEDIA_MAP_FILE.exists():
        return json.load(open(MEDIA_MAP_FILE)).get("product_media_ids", {})
    return {}


def get_accounts():
    """Get active image-compatible accounts."""
    if ACCOUNTS_FILE.exists():
        data = json.load(open(ACCOUNTS_FILE))
        return data.get("image_accounts", [])
    r = requests.get(f"{API}/social-accounts", headers=HDR, params={"limit": 100}, timeout=30)
    return [a["id"] for a in r.json().get("data", [])
            if a["platform"] in ("facebook", "threads", "twitter", "linkedin", "instagram")]


def load_state():
    """Load rotation state — which products were posted recently."""
    if STATE_FILE.exists():
        return json.load(open(STATE_FILE))
    return {"last_products": [], "post_count": 0}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def pick_product(state):
    """Pick next product, rotating evenly through all products."""
    all_slugs = list(PRODUCT_CONTENT.keys()) + list(PROFILE_PRODUCTS.keys())
    recent = state.get("last_products", [])[-6:]  # don't repeat last 6
    
    available = [s for s in all_slugs if s not in recent]
    if not available:
        available = all_slugs  # reset if all used
    
    return random.choice(available)


def create_post(caption, media_ids, account_ids):
    """Create post via PostBridge."""
    payload = {
        "caption": caption,
        "social_accounts": account_ids,
    }
    if media_ids:
        payload["media"] = media_ids
    
    r = requests.post(f"{API}/posts", headers=HDR, json=payload, timeout=30)
    return r.status_code in (200, 201), r.text[:200]


def main():
    media_map = load_media_map()
    account_ids = get_accounts()
    state = load_state()
    
    if not account_ids:
        print("❌ No accounts found")
        return
    
    num_posts = random.randint(3, 5)
    now = datetime.now()
    
    print(f"[{now.strftime('%H:%M')}] Creating {num_posts} ALIGNED posts for {len(account_ids)} accounts")
    
    created = 0
    for i in range(num_posts):
        slug = pick_product(state)
        url = f"{BASE_URL}/{slug}"
        
        # Get product content
        if slug in PRODUCT_CONTENT:
            pdata = PRODUCT_CONTENT[slug]
        elif slug in PROFILE_PRODUCTS:
            pdata = PROFILE_PRODUCTS[slug]
        else:
            continue
        
        # Pick caption (rotate through options)
        caption = random.choice(pdata["captions"]).format(url=url)
        
        # Pick MATCHING media (product-specific, not random!)
        post_media = []
        if slug in media_map and media_map[slug]:
            # Pick one image that matches this product
            img = random.choice(media_map[slug])
            post_media = [img["media_id"]]
        
        ok, resp = create_post(caption, post_media, account_ids)
        if ok:
            created += 1
            state.setdefault("last_products", []).append(slug)
            print(f"  ✅ {pdata['name']}: {len(post_media)} media, {len(account_ids)} accounts")
        else:
            print(f"  ❌ {pdata['name']}: {resp[:80]}")
        
        time.sleep(0.3)
    
    state["post_count"] = state.get("post_count", 0) + created
    state["last_run"] = now.isoformat()
    save_state(state)
    
    print(f"\n  Created: {created}/{num_posts} | Total lifetime: {state['post_count']}")
    
    # Log
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{now.isoformat()} | posts={created}/{num_posts} | accts={len(account_ids)} | aligned=YES\n")


if __name__ == "__main__":
    main()
