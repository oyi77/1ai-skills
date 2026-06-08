"""
comment_templates.py — Natural-sounding Indonesian reply templates
Revenue-critical: Convert comment engagement → LYNK sales
"""

import random

# ─── PRODUCT CATALOG ───────────────────────────────────────────────────────────
PRODUCTS = {
    "jobmagnet_ai": {
        "name": "JobMagnet Ai",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/45r5yvze3vy4",
        "benefit": "bantu kamu dapet kerja lebih cepet dengan AI",
        "keywords": [
            "kerja",
            "job",
            "karir",
            "cv",
            "resume",
            "lamaran",
            "interview",
            "hiring",
            "loker",
        ],
    },
    "ai_creative_ad_engine": {
        "name": "AI Creative Ad Engine",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/9r8rj1o38q59",
        "benefit": "bikin iklan yang convert pakai AI",
        "keywords": [
            "iklan",
            "ads",
            "fb ads",
            "meta ads",
            "copywriting",
            "marketing",
            "creative",
            "konten iklan",
        ],
    },
    "food_menu_ai_studio": {
        "name": "Food Menu AI Studio",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/l4q49jj3z383",
        "benefit": "desain menu makanan profesional pakai AI",
        "keywords": [
            "menu",
            "makanan",
            "restoran",
            "cafe",
            "kuliner",
            "food",
            "warung",
            "masakan",
        ],
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/emne05mm7v25",
        "benefit": "boost penjualan marketplace kamu pakai AI",
        "keywords": [
            "shopee",
            "tokopedia",
            "marketplace",
            "jualan",
            "toko online",
            "seller",
            "olshop",
        ],
    },
    "ai_creative_tools": {
        "name": "AI Creative Tools",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/89d30qd3ddnj",
        "benefit": "lengkap tools AI buat content creator",
        "keywords": [
            "tools",
            "ai tools",
            "content creator",
            "desain",
            "grafis",
            "edit foto",
            "thumbnail",
        ],
    },
    "guru_pintar_ai": {
        "name": "Guru Pintar AI",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/6821op5e24kn",
        "benefit": "jadi guru/pengajar lebih efektif dengan AI",
        "keywords": [
            "guru",
            "mengajar",
            "pendidikan",
            "les",
            "bimbel",
            "edukasi",
            "murid",
            "kelas",
        ],
    },
    "mesin_cetak_bisnis_kuliner": {
        "name": "Mesin Cetak Bisnis Kuliner",
        "price": 75000,
        "price_str": "75rb",
        "url": "https://lynk.id/jendralbot/kzryk28dxmpx",
        "benefit": "scale bisnis kuliner kamu dengan sistem AI",
        "keywords": [
            "bisnis kuliner",
            "usaha makanan",
            "fnb",
            "franchise",
            "catering",
            "snack",
        ],
    },
    "belanja_duit_balik": {
        "name": "Belanja Duit Balik",
        "price": 0,
        "price_str": "GRATIS",
        "url": "https://lynk.id/jendralbot/kkjk0mv1vg7o",
        "benefit": "dapet cashback tiap belanja online",
        "keywords": ["gratis", "cashback", "hemat", "diskon", "belanja", "promo"],
    },
    "kelas_affiliate_tiktok": {
        "name": "Kelas Affiliate TikTok",
        "price": 1000000,
        "price_str": "1jt",
        "url": "https://lynk.id/jendralbot/regxdn7xkpz6",
        "benefit": "hasilin uang dari TikTok Affiliate",
        "keywords": [
            "tiktok",
            "affiliate",
            "penghasilan",
            "income",
            "cuan",
            "passive income",
            "commission",
        ],
    },
}

DEFAULT_PRODUCT = PRODUCTS["ai_creative_tools"]

# ─── REPLY TEMPLATES ───────────────────────────────────────────────────────────

POSITIVE_REPLIES = [
    "Makasih kak! 🔥 Udah coba belum? Link di bio ya",
    "Seneng banget kak, semoga bermanfaat ya! 💪 Cek link di bio",
    "Wah makasih kakk! 😊 Kalau mau coba langsung, link di bio ya",
    "Hehe makasih kak 🙏 Jangan lupa cek link di bio, lagi promo!",
    "Thank you kak! 🔥 Drop link di bio buat yang mau langsung coba",
]

QUESTION_REPLIES = [
    "Hai kak, {product} bisa {benefit}. Cek link di bio ya, lagi promo! 🎁",
    "Kak, {product} itu {benefit}. Harganya cuma {price} lho! Link di bio 🔥",
    "Halo kak! {product} ini {benefit}. Mau tahu lebih lanjut? Link di bio atau DM aku 😊",
    "Wah pertanyaan bagus kak! {product} dirancang khusus buat {benefit}. Cek bionya ya! 🎁",
]

INTEREST_REPLIES = [
    "Wah tertarik ya kak? DM aku buat info lengkapnya 😊",
    "Kak mau tau lebih? DM aku sekarang ya, ada penjelasan lengkapnya! 🔥",
    "Hehe iyaa kak, makasih udah tertarik! DM aku ya biar aku jelasin 😊",
    "Bagus banget kak tertariknya! Langsung DM aku buat detail + promo spesialnya 🎁",
]

NEGATIVE_REPLIES = [
    "Makasih feedbacknya kak, appreciate it 🙏",
    "Terima kasih masukannya kak, noted banget! 🙏",
    "Makasih udah jujur kak, feedback kamu berharga buat kita 🙏",
    "Noted kak, kita terus improve! Makasih ya 🙏",
]

PRICE_REPLIES = [
    "Kak, harganya {price} aja! Langsung cek link di bio ya 🔥 Lagi ada promo",
    "Cuma {price} kak! Itu udah dapet {product} yang bisa {benefit} 🎁",
    "Murah banget kak, {price} doang! Link pembelian di bio ya 😊",
]

GENERIC_ENGAGEMENT = [
    "Makasih udah mampir kak! 😊 Cek link di bio buat produk-produk AI terbaik",
    "Halo kak! Kalo butuh tools AI keren, cek link di bio ya 🔥",
    "Salam kenal kak! Ada tools AI bagus di link bio, cek ya! 🎁",
]

DM_PUBLIC_REPLY = [
    "DM ya kak buat detail lengkapnya! 🔥",
    "Kak, DM aku sekarang buat info lengkap + promo spesial! 😊",
    "Langsung DM aku aja kak, aku jelasin semua! 🎁",
]

DM_MESSAGE_TEMPLATE = """Hai kak! Makasih udah tertarik sama {product} 😊

Ini linknya: {url}

{product} bisa {benefit}.

Harganya {price} aja — lagi ada promo spesial hari ini! 🎁

Kalau ada pertanyaan, langsung tanya aja ya kak. Aku siap bantu! 🔥"""

FREE_DM_MESSAGE_TEMPLATE = """Hai kak! Makasih udah tertarik sama {product} 😊

Ini linknya (GRATIS!): {url}

{product} bisa {benefit}.

Langsung klik aja kak, 100% gratis! 🎁

Kalau ada pertanyaan, tanya aja ya 🔥"""


# ─── TEMPLATE GETTERS ──────────────────────────────────────────────────────────


def get_positive_reply() -> str:
    return random.choice(POSITIVE_REPLIES)


def get_question_reply(product: dict) -> str:
    tpl = random.choice(QUESTION_REPLIES)
    return tpl.format(
        product=product["name"],
        benefit=product["benefit"],
        price=f"IDR {product['price_str']}" if product["price"] > 0 else "GRATIS",
    )


def get_interest_reply() -> str:
    return random.choice(INTEREST_REPLIES)


def get_negative_reply() -> str:
    return random.choice(NEGATIVE_REPLIES)


def get_price_reply(product: dict) -> str:
    tpl = random.choice(PRICE_REPLIES)
    return tpl.format(
        product=product["name"],
        price=f"IDR {product['price_str']}" if product["price"] > 0 else "GRATIS",
    )


def get_dm_public_reply() -> str:
    return random.choice(DM_PUBLIC_REPLY)


def get_dm_message(product: dict) -> str:
    if product["price"] == 0:
        return FREE_DM_MESSAGE_TEMPLATE.format(
            product=product["name"],
            url=product["url"],
            benefit=product["benefit"],
        )
    return DM_MESSAGE_TEMPLATE.format(
        product=product["name"],
        url=product["url"],
        benefit=product["benefit"],
        price=f"IDR {product['price_str']}",
    )


def get_generic_reply() -> str:
    return random.choice(GENERIC_ENGAGEMENT)


def find_product_by_keywords(text: str) -> dict:
    """Match comment text to most relevant product."""
    text_lower = text.lower()
    best_match = None
    best_score = 0
    for product in PRODUCTS.values():
        score = sum(1 for kw in product["keywords"] if kw in text_lower)
        if score > best_score:
            best_score = score
            best_match = product
    return best_match if best_match else DEFAULT_PRODUCT


if __name__ == "__main__":
    p = find_product_by_keywords("gimana cara dapet kerja cepet ya")
    print("Product matched:", p["name"])
    print("Question reply:", get_question_reply(p))
    print("DM message:\n", get_dm_message(p))
