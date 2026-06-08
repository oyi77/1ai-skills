"""
viral_pattern_db.py — Database of viral content patterns

Store, query, and rank viral content patterns for Indonesian market.
Tracks: hook types, formats, engagement rates, time slots.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent / "data" / "viral-patterns-db.json"


# Master viral pattern database
VIRAL_PATTERNS_DB = {
    "version": "1.0.0",
    "last_updated": datetime.now().isoformat(),
    "market": "Indonesia",
    "patterns": [
        {
            "id": "hook_001",
            "name": "Old Way vs New Way",
            "hook_template": "Kamu masih {old_way}? Coba {new_way}...",
            "hook_examples": [
                "Kamu masih edit video manual? Coba AI tools ini...",
                "Kamu masih cari resep di Google? Coba cara ini...",
                "Kamu masih jualan offline aja? Coba strategi ini...",
            ],
            "format": "Tutorial",
            "niche_fit": ["ai_tools", "digital_marketing", "side_hustle"],
            "avg_engagement_rate": 0.065,
            "avg_completion_rate": 0.72,
            "virality_score": 8.2,
            "best_times": ["07:00", "12:00", "19:00"],
            "cta": "Follow untuk tips {niche} setiap hari",
            "length_seconds": {"min": 30, "max": 60, "optimal": 45},
        },
        {
            "id": "hook_002",
            "name": "Shocking Number",
            "hook_template": "{number} {thing} yang {bisa} {outcome} dalam {timeframe}",
            "hook_examples": [
                "5 AI tools yang bisa bantu kamu cuan Rp 5 juta dalam seminggu",
                "3 kesalahan yang bikin konten kamu gak viral",
                "7 bisnis sampingan yang bisa jalan autopilot",
            ],
            "format": "Listicle",
            "niche_fit": ["ai_tools", "side_hustle", "education", "digital_marketing"],
            "avg_engagement_rate": 0.082,
            "avg_completion_rate": 0.68,
            "virality_score": 9.1,
            "best_times": ["08:00", "12:30", "20:00"],
            "cta": "Save ini, banyak yang butuh",
            "length_seconds": {"min": 45, "max": 90, "optimal": 60},
        },
        {
            "id": "hook_003",
            "name": "Personal Confession",
            "hook_template": "Jujur, gue dulu {situation}. Sekarang {outcome}. Caranya?",
            "hook_examples": [
                "Jujur, gue dulu gabisa masak. Sekarang omzet 30juta/bulan dari warung online.",
                "Jujur, gue dulu scroll TikTok 6 jam sehari. Sekarang dapet duit dari sana.",
                "Jujur, gue dulu gapunya modal. Sekarang bisnis berjalan tanpa modal.",
            ],
            "format": "Storytelling",
            "niche_fit": ["kuliner", "side_hustle", "education"],
            "avg_engagement_rate": 0.091,
            "avg_completion_rate": 0.78,
            "virality_score": 9.4,
            "best_times": ["07:00", "19:00", "21:00"],
            "cta": "Komen 'mau tau' untuk cerita lengkapnya",
            "length_seconds": {"min": 45, "max": 90, "optimal": 75},
        },
        {
            "id": "hook_004",
            "name": "Warning / STOP",
            "hook_template": "STOP {doing_thing}. {Reason}. {Better_alternative}.",
            "hook_examples": [
                "STOP jualan di marketplace sebelum kamu tau ini...",
                "STOP pakai ChatGPT cara ini — kamu rugi sendiri",
                "STOP buka warung sebelum kamu tau margin yang benar",
            ],
            "format": "Controversy",
            "niche_fit": ["digital_marketing", "side_hustle", "ai_tools"],
            "avg_engagement_rate": 0.108,
            "avg_completion_rate": 0.81,
            "virality_score": 9.7,
            "best_times": ["12:00", "19:00", "20:00"],
            "cta": "Follow agar gak ketinggalan update",
            "length_seconds": {"min": 30, "max": 60, "optimal": 45},
        },
        {
            "id": "hook_005",
            "name": "Before After Transformation",
            "hook_template": "{Before_state} → {After_state} dalam {timeframe}",
            "hook_examples": [
                "Omzet Rp 0 → Rp 10 juta dalam 30 hari pakai strategi ini",
                "0 followers → 10.000 followers dalam 2 minggu",
                "Modal 500ribu → untung 3 juta sebulan",
            ],
            "format": "Before/After",
            "niche_fit": ["kuliner", "side_hustle", "digital_marketing"],
            "avg_engagement_rate": 0.076,
            "avg_completion_rate": 0.74,
            "virality_score": 8.8,
            "best_times": ["08:00", "12:00", "20:00"],
            "cta": "DM gue 'info' untuk caranya",
            "length_seconds": {"min": 30, "max": 60, "optimal": 45},
        },
        {
            "id": "hook_006",
            "name": "Question Hook",
            "hook_template": "Tau gak kamu bisa {outcome} cuma dengan {simple_thing}?",
            "hook_examples": [
                "Tau gak kamu bisa otomatisasi bisnis cuma dengan 1 tools gratis?",
                "Tau gak ada cara posting konten 30 hari hanya dalam 2 jam?",
                "Tau gak kamu bisa dapat 1000 followers pertama dalam seminggu?",
            ],
            "format": "Tutorial",
            "niche_fit": ["ai_tools", "digital_marketing", "side_hustle"],
            "avg_engagement_rate": 0.058,
            "avg_completion_rate": 0.65,
            "virality_score": 7.5,
            "best_times": ["07:00", "12:00", "19:00"],
            "cta": "Save untuk kamu coba sendiri",
            "length_seconds": {"min": 30, "max": 60, "optimal": 45},
        },
        {
            "id": "hook_007",
            "name": "Secret Reveal",
            "hook_template": "Rahasia {expert_type} yang {gak_banyak_orang_tau}",
            "hook_examples": [
                "Rahasia content creator 1 juta followers yang gak banyak orang tau",
                "Rahasia chef berbintang yang bikin makanan selalu laris",
                "Rahasia trader sukses yang dipake tiap hari",
            ],
            "format": "Storytelling + Tutorial",
            "niche_fit": ["education", "kuliner", "digital_marketing"],
            "avg_engagement_rate": 0.079,
            "avg_completion_rate": 0.76,
            "virality_score": 8.6,
            "best_times": ["19:00", "20:00", "21:00"],
            "cta": "Simpan sebelum dihapus",
            "length_seconds": {"min": 45, "max": 90, "optimal": 60},
        },
        {
            "id": "hook_008",
            "name": "FOMO / Fear of Missing Out",
            "hook_template": "Kalau kamu gak {action} sekarang, kamu bakal {negative_outcome}",
            "hook_examples": [
                "Kalau kamu gak pake AI sekarang, bisnis kamu ketinggalan 5 tahun",
                "Kalau kamu gak mulai invest sekarang, inflasi bakal makan tabunganmu",
                "Kalau kamu gak belajar skill ini, kamu bakal digantikan AI",
            ],
            "format": "Educational + Warning",
            "niche_fit": ["ai_tools", "side_hustle", "education"],
            "avg_engagement_rate": 0.094,
            "avg_completion_rate": 0.79,
            "virality_score": 9.3,
            "best_times": ["08:00", "13:00", "20:00"],
            "cta": "Follow biar gak ketinggalan info penting",
            "length_seconds": {"min": 30, "max": 60, "optimal": 45},
        },
    ],
    "format_performance": {
        "Tutorial": {
            "avg_engagement": 0.062,
            "avg_completion": 0.71,
            "best_niche": ["ai_tools", "kuliner"],
        },
        "Before/After": {
            "avg_engagement": 0.074,
            "avg_completion": 0.74,
            "best_niche": ["side_hustle", "kuliner"],
        },
        "Storytelling": {
            "avg_engagement": 0.088,
            "avg_completion": 0.79,
            "best_niche": ["kuliner", "education"],
        },
        "Controversy": {
            "avg_engagement": 0.102,
            "avg_completion": 0.82,
            "best_niche": ["digital_marketing", "side_hustle"],
        },
        "Listicle": {
            "avg_engagement": 0.071,
            "avg_completion": 0.68,
            "best_niche": ["ai_tools", "education"],
        },
        "Case Study": {
            "avg_engagement": 0.085,
            "avg_completion": 0.77,
            "best_niche": ["digital_marketing", "side_hustle"],
        },
        "Behind the Scenes": {
            "avg_engagement": 0.079,
            "avg_completion": 0.80,
            "best_niche": ["kuliner", "education"],
        },
    },
    "best_posting_times": {
        "tiktok": {
            "weekday": ["07:00-09:00", "12:00-13:30", "18:00-22:00"],
            "weekend": ["09:00-11:00", "14:00-16:00", "19:00-23:00"],
            "peak_days": ["Tuesday", "Wednesday", "Friday", "Sunday"],
        },
        "instagram": {
            "weekday": ["06:00-09:00", "11:00-13:00", "19:00-21:00"],
            "weekend": ["09:00-11:00", "15:00-17:00", "20:00-22:00"],
            "peak_days": ["Monday", "Wednesday", "Thursday", "Saturday"],
        },
        "youtube_shorts": {
            "weekday": ["08:00-10:00", "14:00-16:00", "20:00-23:00"],
            "weekend": ["10:00-12:00", "15:00-18:00", "20:00-24:00"],
            "peak_days": ["Friday", "Saturday", "Sunday"],
        },
    },
}


def load_db() -> dict:
    """Load the viral patterns database."""
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return VIRAL_PATTERNS_DB


def save_db(db: dict) -> None:
    """Save the viral patterns database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def get_top_patterns(niche: Optional[str] = None, limit: int = 5) -> list[dict]:
    """Get top viral patterns, optionally filtered by niche."""
    db = load_db()
    patterns = db["patterns"]

    if niche:
        patterns = [p for p in patterns if niche in p.get("niche_fit", [])]

    # Sort by virality score
    patterns.sort(key=lambda x: x.get("virality_score", 0), reverse=True)
    return patterns[:limit]


def get_best_format(niche: str) -> dict:
    """Get the best-performing content format for a niche."""
    db = load_db()
    formats = db["format_performance"]

    best = None
    best_score = 0

    for fmt_name, fmt_data in formats.items():
        if niche in fmt_data.get("best_niche", []):
            score = fmt_data["avg_engagement"] * 0.6 + fmt_data["avg_completion"] * 0.4
            if score > best_score:
                best_score = score
                best = {
                    "format": fmt_name,
                    **fmt_data,
                    "combined_score": round(score, 4),
                }

    return best or {"format": "Tutorial", "note": "Default format — niche not found"}


def get_posting_schedule(platform: str = "tiktok") -> dict:
    """Get optimal posting schedule for a platform."""
    db = load_db()
    return db["best_posting_times"].get(platform, {})


def add_pattern(pattern: dict) -> str:
    """Add a new viral pattern to the database."""
    db = load_db()

    # Generate ID
    existing_ids = [p["id"] for p in db["patterns"]]
    next_num = len(existing_ids) + 1
    pattern["id"] = f"hook_{next_num:03d}"
    pattern["added_at"] = datetime.now().isoformat()

    db["patterns"].append(pattern)
    db["last_updated"] = datetime.now().isoformat()
    save_db(db)

    return pattern["id"]


def initialize_db() -> str:
    """Initialize the database with default patterns."""
    save_db(VIRAL_PATTERNS_DB)
    print(f"✅ Viral patterns DB initialized: {DB_PATH}")
    print(f"   Patterns loaded: {len(VIRAL_PATTERNS_DB['patterns'])}")
    return str(DB_PATH)


if __name__ == "__main__":
    # Initialize and test
    initialize_db()

    print("\n🔥 TOP VIRAL PATTERNS:")
    top = get_top_patterns(limit=5)
    for p in top:
        print(f"  [{p['virality_score']}] {p['name']}: {p['hook_template'][:60]}...")

    print("\n📊 BEST FORMATS BY NICHE:")
    for niche in ["ai_tools", "kuliner", "side_hustle"]:
        fmt = get_best_format(niche)
        print(
            f"  {niche}: {fmt['format']} (engagement: {fmt.get('avg_engagement', 0)*100:.1f}%)"
        )

    print("\n⏰ TIKTOK BEST TIMES:")
    schedule = get_posting_schedule("tiktok")
    print(f"  Weekday peaks: {', '.join(schedule.get('weekday', []))}")
    print(f"  Best days: {', '.join(schedule.get('peak_days', []))}")
