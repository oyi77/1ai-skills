"""
niche_researcher.py — Research specific niches (AI tools, kuliner, etc.)

Deep-dives into niche-specific content opportunities, trending topics,
and audience behavior for Indonesian market.
"""

import json
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

NICHE_PROFILES = {
    "ai_tools": {
        "name": "AI Tools for Business",
        "audience": {
            "age_range": "22-40",
            "primary_gender": "Male 60%",
            "income": "Middle-upper class",
            "pain_points": [
                "Wasting time on repetitive tasks",
                "Can't afford to hire employees",
                "Don't know which AI tools to use",
                "Fear of being replaced by AI",
            ],
            "aspirations": [
                "Automate business processes",
                "Increase productivity 10x",
                "Learn AI without coding",
                "Save money on tools/team",
            ],
        },
        "trending_topics_2025": [
            "ChatGPT prompts untuk bisnis",
            "AI tools gratis terbaik 2025",
            "Cara otomatisasi jualan online dengan AI",
            "Vibe coding tanpa ngoding",
            "AI untuk buat konten viral",
            "Tools AI gantiin VA",
            "Gemini vs ChatGPT mana lebih baik",
            "NotionAI untuk manajemen bisnis",
            "Canva AI untuk desain gratis",
            "Perplexity vs Google untuk riset",
        ],
        "content_opportunities": [
            "Tutorial step-by-step AI tools specific use cases",
            "Comparison videos: AI tool A vs B",
            "Hidden features dari tools populer",
            "Real ROI case studies dari bisnis Indonesia",
        ],
        "competitor_weaknesses": [
            "Terlalu teknikal, tidak relate ke bisnis Indonesia",
            "Tidak ada bukti nyata ROI",
            "Bahasa Inggris dominan — gap konten Bahasa Indonesia",
        ],
        "monetization": [
            "Affiliate tool links",
            "Digital products",
            "Consulting",
            "Courses",
        ],
    },
    "digital_marketing": {
        "name": "Digital Marketing Tips",
        "audience": {
            "age_range": "20-35",
            "primary_gender": "Mixed 50/50",
            "income": "Middle class",
            "pain_points": [
                "Konten gak viral",
                "Followers tidak bertumbuh",
                "ROAS iklan jelek",
                "Gak tau cara jualan lewat sosmed",
            ],
            "aspirations": [
                "Jadi content creator populer",
                "Bisnis online profitable",
                "Brand awareness tinggi",
                "Passive income dari konten",
            ],
        },
        "trending_topics_2025": [
            "Algoritma TikTok 2025 cara terbaru",
            "Hook formula yang bikin stop scroll",
            "Cara dapat 1000 followers pertama cepat",
            "Konten viral tanpa modal",
            "Caption yang bikin orang beli",
            "Strategi hashtag yang masih works",
            "User Generated Content (UGC) strategy",
            "Cara repurpose 1 konten jadi 10",
            "Email marketing masih relevan?",
            "Short form vs long form content 2025",
        ],
        "content_opportunities": [
            "Case study konten viral Indonesia spesifik",
            "Behind the numbers: real analytics screenshot",
            "Debunking marketing myths",
            "Platform comparison untuk niche tertentu",
        ],
        "competitor_weaknesses": [
            "Generic tips, tidak ada spesifikasi niche",
            "Kurang data/angka konkret Indonesia",
            "Tidak ada series konten (episodik)",
        ],
        "monetization": ["Digital products", "Consulting", "Brand deals", "Affiliate"],
    },
    "kuliner": {
        "name": "Kuliner / Food Business",
        "audience": {
            "age_range": "20-45",
            "primary_gender": "Female 65%",
            "income": "All classes",
            "pain_points": [
                "Bingung mau bisnis apa",
                "Modal terbatas",
                "Takut gak ada yang beli",
                "Tidak tau cara marketing makanan",
            ],
            "aspirations": [
                "Bisnis kuliner sendiri",
                "Warung/resto yang ramai",
                "Jual makanan online sukses",
                "Resep khas yang viral",
            ],
        },
        "trending_topics_2025": [
            "Korean street food viral di Indonesia",
            "Makanan sehat yang tetap enak",
            "Bisnis snack modal minim",
            "Cloud kitchen / ghost kitchen",
            "Frozen food bisnis dari rumah",
            "Minuman kekinian yang laris 2025",
            "Packaging makanan yang menarik",
            "Cara jual makanan di GoFood/GrabFood",
            "Resep viral TikTok food",
            "Strategi harga untuk warung",
        ],
        "content_opportunities": [
            "Recipe + business angle (cost, margin, pricing)",
            "Day in the life bisnis kuliner",
            "Before/after warung makeover",
            "Sourcing bahan baku murah tips",
        ],
        "competitor_weaknesses": [
            "Fokus resep, tidak bahas bisnis side",
            "Video quality low, tidak ada audio yang baik",
            "Tidak follow up ke episode berikutnya",
        ],
        "monetization": [
            "Physical products (bumbu, frozen)",
            "Courses",
            "Consulting",
            "Affiliate",
        ],
    },
    "side_hustle": {
        "name": "Side Hustle / Passive Income",
        "audience": {
            "age_range": "22-38",
            "primary_gender": "Male 55%",
            "income": "Lower-middle class",
            "pain_points": [
                "Gaji tidak cukup",
                "Tidak ada modal untuk bisnis",
                "Tidak punya waktu ekstra",
                "Takut rugi / scam",
            ],
            "aspirations": [
                "Penghasilan tambahan dari HP",
                "Passive income yang jalan sendiri",
                "Resign dari kerja kantoran",
                "Financial freedom",
            ],
        },
        "trending_topics_2025": [
            "Dropship tanpa modal 2025",
            "Cara dapet duit dari TikTok",
            "Affiliate marketing untuk pemula",
            "Digital product yang laku dijual",
            "Reseller produk digital",
            "Freelance skill yang dibayar tinggi",
            "Cara monetize skill tanpa portofolio",
            "Platform kerja freelance terbaik",
            "Bisnis dari HP modal nol rupiah",
            "Passive income dari konten",
        ],
        "content_opportunities": [
            "Income proof yang credible (screenshot real)",
            "Step-by-step dari nol ke pertama kali dapat duit",
            "Scam alert + legit alternatives",
            "Niche side hustle yang belum ramai",
        ],
        "competitor_weaknesses": [
            "Klaim tidak credible, tidak ada bukti",
            "Promosi berlebihan produk sendiri",
            "Tidak actionable — terlalu high level",
        ],
        "monetization": ["Affiliate links", "Digital products", "Courses", "Community"],
    },
    "education": {
        "name": "Education / Self-Improvement",
        "audience": {
            "age_range": "18-35",
            "primary_gender": "Mixed",
            "income": "Middle class",
            "pain_points": [
                "Tidak tau harus belajar apa",
                "Merasa tertinggal dari peers",
                "Kurang motivasi",
                "Tidak punya uang untuk kursus",
            ],
            "aspirations": [
                "Naik gaji / karir",
                "Punya skill bernilai",
                "Financial literacy",
                "Jadi versi terbaik diri sendiri",
            ],
        },
        "trending_topics_2025": [
            "Skill yang wajib dikuasai di era AI",
            "Cara belajar cepat dan efektif",
            "Investasi untuk pemula 2025",
            "Cara keluar dari financial trap",
            "Belajar bahasa Inggris gratis",
            "Literasi keuangan dasar",
            "Growth mindset vs fixed mindset",
            "Cara membangun kebiasaan produktif",
            "Second brain / PKM system",
            "Belajar coding untuk non-IT",
        ],
        "content_opportunities": [
            "Book summary dalam 60 detik",
            "Mindset shifts yang mengubah hidup",
            "Financial mistakes to avoid",
            "Free learning resources yang underrated",
        ],
        "competitor_weaknesses": [
            "Terlalu verbose, penonton drop off",
            "Tidak ada visual / infographic yang menarik",
            "CTA tidak specific",
        ],
        "monetization": ["Courses", "Books", "Community", "Consulting"],
    },
}


def research_niche(niche_key: str) -> dict:
    """Deep research on a specific niche."""
    if niche_key not in NICHE_PROFILES:
        return {
            "error": f"Niche '{niche_key}' not found. Available: {list(NICHE_PROFILES.keys())}"
        }

    profile = NICHE_PROFILES[niche_key]

    # Build content calendar suggestions
    content_calendar = []
    for i, topic in enumerate(profile["trending_topics_2025"][:7]):
        content_calendar.append(
            {
                "day": i + 1,
                "topic": topic,
                "suggested_format": (
                    "Tutorial"
                    if i % 3 == 0
                    else ("Controversy" if i % 3 == 1 else "Storytelling")
                ),
                "platform": "TikTok" if i % 2 == 0 else "Instagram Reels",
            }
        )

    return {
        "niche_key": niche_key,
        "niche_name": profile["name"],
        "researched_at": datetime.now().isoformat(),
        "audience_profile": profile["audience"],
        "trending_topics": profile["trending_topics_2025"],
        "content_opportunities": profile["content_opportunities"],
        "competitor_weaknesses_to_exploit": profile["competitor_weaknesses"],
        "monetization_options": profile["monetization"],
        "7_day_content_calendar": content_calendar,
        "quick_wins": [
            f"Post about: {profile['trending_topics_2025'][0]}",
            f"Format: {profile.get('content_opportunities', ['Tutorial'])[0]}",
            f"Target audience pain: {profile['audience']['pain_points'][0]}",
        ],
    }


def research_all_niches() -> dict:
    """Research all 5 target niches."""
    print("🔬 Researching all niches...")
    results = {
        "generated_at": datetime.now().isoformat(),
        "market": "Indonesia",
        "niches": {},
    }

    for niche_key in NICHE_PROFILES:
        print(f"  📚 Researching: {NICHE_PROFILES[niche_key]['name']}")
        results["niches"][niche_key] = research_niche(niche_key)

    return results


def save_niche_research(output_dir: str = None) -> str:
    """Run and save niche research."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    data = research_all_niches()
    filepath = output_path / "niche-research.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: {filepath}")
    return str(filepath)


if __name__ == "__main__":
    # Quick single niche test
    print("🎯 Quick niche research test:")
    result = research_niche("ai_tools")
    print(f"  Niche: {result['niche_name']}")
    print(f"  Trending topics: {len(result['trending_topics'])}")
    print(f"  Quick wins:")
    for win in result["quick_wins"]:
        print(f"    → {win}")

    print("\n💡 7-Day Content Calendar (AI Tools):")
    for day in result["7_day_content_calendar"]:
        print(f"  Day {day['day']}: {day['topic'][:50]} [{day['suggested_format']}]")

    # Full research
    save_niche_research()
