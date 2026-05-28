"""
pillar_rotator.py - Rotate content pillars based on BerkahKarya strategy
Ensures correct pillar distribution: AI Demo 40%, Tips 25%, Social Proof 15%, BTS 10%, Promo 10%
"""

import random
from datetime import date
from typing import List, Dict, Optional

# BerkahKarya products with LYNK URLs
PRODUCTS = [
    {
        "name": "JobMagnet Ai",
        "category": "ai_tools",
        "lynk_url": "https://lynk.id/jendralbot/45r5yvze3vy4",
        "price": "IDR 49K",
        "hook_templates": [
            "Kamu masih apply kerja manual? 😱",
            "AI yang bikin CV kamu langsung dilirik HRD 👀",
            "1000 lamaran vs 1 AI — siapa yang menang?",
            "Cara dapet kerja 10x lebih cepat pakai AI 🚀",
        ]
    },
    {
        "name": "ContentAI Pro",
        "category": "ai_tools",
        "lynk_url": "https://lynk.id/jendralbot/contentai",
        "price": "IDR 79K",
        "hook_templates": [
            "Bikin 30 konten dalam 10 menit pakai AI 🤖",
            "Content creator yang nggak pakai AI bakal ketinggalan 😬",
            "Viral formula yang AI pelajari dari 1 juta TikTok 📱",
        ]
    },
    {
        "name": "TradingBot Ai",
        "category": "ai_tools",
        "lynk_url": "https://lynk.id/jendralbot/tradingbot",
        "price": "IDR 89K",
        "hook_templates": [
            "Bot yang bisa analisis XAUUSD lebih cepat dari manusia ⚡",
            "Kenapa trader pro pakai AI untuk entry signal? 📊",
            "GRATIS vs AI signal — perbandingan yang bikin shock 😮",
        ]
    },
    {
        "name": "CopywriterAi",
        "category": "ai_tools",
        "lynk_url": "https://lynk.id/jendralbot/copywriter",
        "price": "IDR 59K",
        "hook_templates": [
            "Caption yang convert 10x lebih banyak — bikin pakai AI 💰",
            "Copywriter 10 tahun pengalaman vs AI — hasilnya mengejutkan 🤯",
            "Script iklan yang selalu viral — formula AI-nya bocor! 🔥",
        ]
    },
    {
        "name": "Free AI Toolkit",
        "category": "ai_tools",
        "lynk_url": "https://lynk.id/jendralbot/freetoolkit",
        "price": "FREE",
        "hook_templates": [
            "5 AI tools GRATIS yang wajib kamu pakai sekarang 🎁",
            "Nggak perlu bayar mahal — AI gratis ini udah powerful 💪",
            "Download gratis! AI toolkit buat freelancer Indonesia 🇮🇩",
        ]
    },
]

# Content pillar definitions
PILLARS = {
    "ai_tools_demo": {
        "weight": 0.40,
        "name": "AI Tools Demo",
        "content_types": {
            "tiktok": ["video_demo", "tutorial_short"],
            "instagram": ["reel", "carousel"],
            "youtube_shorts": ["demo_short"],
            "facebook": ["video", "link_post"],
        },
        "caption_templates": [
            "Gue udah coba {product} selama seminggu. Hasilnya? {hook}\n\nBerikut step-by-step cara pakainya:\n👉 Step 1: Download/buka {product}\n👉 Step 2: [explain feature]\n👉 Step 3: [show result]\n\nDapatkan akses di link bio! 🔗\n\n",
            "Review jujur {product}: Worth it atau nggak?\n\n✅ Kelebihan:\n- [feature 1]\n- [feature 2]\n- [feature 3]\n\n❌ Kekurangan:\n- [minor issue]\n\nKesimpulan: {hook}\n\nLink di bio 👆\n\n",
        ],
    },
    "tips_tricks": {
        "weight": 0.25,
        "name": "Tips & Tricks",
        "content_types": {
            "tiktok": ["tip_video", "list_video"],
            "instagram": ["carousel", "story_series"],
            "youtube_shorts": ["tips_short"],
            "facebook": ["text_post", "video"],
        },
        "caption_templates": [
            "5 tips pakai AI yang jarang orang tahu 🤫\n\n1️⃣ [Tip 1]\n2️⃣ [Tip 2]\n3️⃣ [Tip 3]\n4️⃣ [Tip 4]\n5️⃣ [Tip 5]\n\nSave post ini biar nggak lupa! 📌\n\n",
            "Kesalahan yang sering dilakukan pemula pakai AI:\n\n❌ [Mistake 1]\n❌ [Mistake 2]\n❌ [Mistake 3]\n\n✅ Yang benar:\n[Correct approach]\n\nFollow untuk tips AI lainnya! 🔔\n\n",
        ],
    },
    "social_proof": {
        "weight": 0.15,
        "name": "Social Proof",
        "content_types": {
            "tiktok": ["testimonial_video", "results_video"],
            "instagram": ["carousel_testimony", "story_result"],
            "youtube_shorts": ["case_study_short"],
            "facebook": ["testimonial_post"],
        },
        "caption_templates": [
            "Customer kami berhasil [hasil] dalam [waktu] pakai {product} 🎉\n\n[Screenshot/Quote testimonial]\n\n\"[Kutipan dari customer]\"\n\nKamu bisa achieve hasil yang sama! Link di bio 🔗\n\n",
            "Real results dari pengguna {product}:\n\nSebelum: [before state]\nSesudah: [after state]\n\nPerbedaan yang bikin gue speechless 😱\n\nCoba sekarang → link di bio 👆\n\n",
        ],
    },
    "behind_the_scenes": {
        "weight": 0.10,
        "name": "Behind the Scenes",
        "content_types": {
            "tiktok": ["bts_video", "day_in_life"],
            "instagram": ["reel_bts", "story_series"],
            "youtube_shorts": ["bts_short"],
            "facebook": ["bts_post"],
        },
        "caption_templates": [
            "Day in the life: Kerja di startup AI Indonesia 🇮🇩\n\n[Behind the scenes content]\n\nFollow perjalanan BerkahKarya di bio! 🔗\n\n",
            "Proses bikin {product} dari 0:\n\n💡 Idea → Research → Build → Launch\n\n[Story content]\n\nBuild in public journey kita terus berlanjut 🚀\n\n",
        ],
    },
    "promo_cta": {
        "weight": 0.10,
        "name": "Promo/CTA",
        "content_types": {
            "tiktok": ["promo_video", "flash_sale"],
            "instagram": ["promo_reel", "discount_story"],
            "youtube_shorts": ["promo_short"],
            "facebook": ["promo_post", "ad_creative"],
        },
        "caption_templates": [
            "⚡ FLASH SALE {product}!\n\nNormal: {price}\nSekarang: DISKON SPESIAL\n\nHanya untuk [X] pembeli pertama!\n\n🔗 Grab sekarang → link di bio\n\nJangan sampai kehabisan! ⏰\n\n",
            "Kenapa kamu harus punya {product} sekarang:\n\n✅ [Benefit 1]\n✅ [Benefit 2]\n✅ [Benefit 3]\n✅ [Benefit 4]\n\nInvestasi terbaik untuk [use case]!\n\nDapatkan di: {lynk_url}\n\n",
        ],
    },
}


def get_pillar_sequence(start_date: date, num_days: int = 30) -> List[str]:
    """
    Generate a deterministic pillar sequence based on date seed.
    Respects weight distribution across the period.
    """
    pillar_names = list(PILLARS.keys())
    weights = [PILLARS[p]["weight"] for p in pillar_names]

    # Use date as seed for reproducibility
    seed = int(start_date.strftime("%Y%m%d"))
    rng = random.Random(seed)

    # Generate weighted sequence
    sequence = []
    pool = []
    for pillar, weight in zip(pillar_names, weights):
        count = max(1, round(weight * num_days))
        pool.extend([pillar] * count)

    # Shuffle with seed
    rng.shuffle(pool)

    # Trim or extend to exact length
    while len(pool) < num_days:
        pool.append(rng.choices(pillar_names, weights=weights, k=1)[0])

    return pool[:num_days]


def get_content_type(pillar: str, platform: str) -> str:
    """Get appropriate content type for platform + pillar combo."""
    content_types = PILLARS[pillar]["content_types"].get(platform, ["video"])
    return random.choice(content_types)


def get_caption_template(pillar: str) -> str:
    """Get a caption template for a given pillar."""
    templates = PILLARS[pillar]["caption_templates"]
    return random.choice(templates)


def select_product(pillar: str, day_index: int) -> Dict:
    """Select product based on pillar and day (rotating through products)."""
    if pillar == "tips_tricks" or pillar == "behind_the_scenes":
        # These pillars are not always product-specific
        # Return a random product for reference
        return PRODUCTS[day_index % len(PRODUCTS)]
    return PRODUCTS[day_index % len(PRODUCTS)]


def get_hashtags(pillar: str, platform: str, product_name: str) -> List[str]:
    """Generate relevant hashtags for the post."""
    base_hashtags = {
        "ai_tools_demo": ["#aitools", "#kecerdasanbuatan", "#teknologiai", "#aiindonesia", "#digitaltools"],
        "tips_tricks": ["#tipsdantricks", "#belajarai", "#tipsai", "#produktivitas", "#digitalskills"],
        "social_proof": ["#testimoni", "#hasil", "#successstory", "#review", "#buktihasil"],
        "behind_the_scenes": ["#buildinpublic", "#startup", "#dibalikLayar", "#berkahkarya", "#entrepreneurindonesia"],
        "promo_cta": ["#promosi", "#diskon", "#sale", "#dapatkansekarang", "#limitedoffer"],
    }

    platform_hashtags = {
        "tiktok": ["#fyp", "#foryou", "#viral", "#tiktokindo", "#tiktokindonesia"],
        "instagram": ["#instagood", "#instadaily", "#instaindonesia", "#igdaily"],
        "youtube_shorts": ["#shorts", "#youtubeshorts", "#ytshorts"],
        "facebook": ["#facebook", "#facebookindonesia"],
    }

    product_hashtag = f"#{product_name.lower().replace(' ', '')}"

    tags = (
        base_hashtags.get(pillar, [])[:3]
        + platform_hashtags.get(platform, [])[:3]
        + [product_hashtag, "#berkahkarya", "#jendralbot"]
    )

    return list(dict.fromkeys(tags))[:15]  # Deduplicate, max 15
