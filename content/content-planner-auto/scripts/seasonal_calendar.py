"""
seasonal_calendar.py - Indonesian seasonal events and content adjustments
Ramadan, Harbolnas, 11.11, Lebaran, Independence Day, etc.
"""

from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple

# 2026 seasonal events for Indonesia
SEASONAL_EVENTS_2026 = {
    # Ramadan 2026 (approximate - exact dates depend on moon sighting)
    "ramadan_start": date(2026, 2, 17),
    "ramadan_end": date(2026, 3, 17),
    "lebaran": date(2026, 3, 20),  # Idul Fitri 1447H
    "lebaran_period": (date(2026, 3, 18), date(2026, 3, 27)),  # Lebaran week
    
    # National holidays
    "independence_day": date(2026, 8, 17),
    "new_year": date(2026, 1, 1),
    "chinese_new_year": date(2026, 2, 17),
    
    # Shopping events (Harbolnas = Hari Belanja Online Nasional)
    "harbolnas_1212": date(2026, 12, 12),
    "harbolnas_1111": date(2026, 11, 11),
    "harbolnas_1010": date(2026, 10, 10),
    "harbolnas_1001": date(2026, 10, 1),
    "shopee_anniversary": date(2026, 9, 15),
    "tokopedia_anniversary": date(2026, 8, 17),
    
    # Other important dates
    "valentine": date(2026, 2, 14),
    "womens_day": date(2026, 3, 8),
    "april_fools": date(2026, 4, 1),
    "labor_day": date(2026, 5, 1),
    "pancasila_day": date(2026, 6, 1),
    "year_end": date(2026, 12, 31),
}

# Content modifiers for seasonal events
SEASONAL_CONTENT_MODS = {
    "ramadan": {
        "best_times_override": {
            "tiktok": ["18:00", "19:00", "22:00", "23:00"],  # After iftar
            "instagram": ["18:00", "19:00", "21:00"],
            "facebook": ["18:00", "19:00"],
        },
        "hashtag_additions": ["#ramadan2026", "#ramadankareem", "#sahur", "#buka", "#puasa"],
        "theme": "Produktif di bulan Ramadan dengan AI",
        "hook_prefix": "Ramadan lebih produktif dengan AI! 🌙",
        "avoid_content": ["food_content_during_day"],
        "promo_type": "ramadan_sale",
    },
    "lebaran": {
        "best_times_override": None,
        "hashtag_additions": ["#lebaran2026", "#idulfitri", "#lebaran", "#taqabbalallah"],
        "theme": "Lebaran special content - AI untuk usaha baru",
        "hook_prefix": "Selamat Lebaran! 🎉 THR-mu bisa diinvestasikan untuk...",
        "avoid_content": [],
        "promo_type": "lebaran_special",
    },
    "harbolnas": {
        "best_times_override": {
            "tiktok": ["00:00", "11:00", "12:00"],  # Midnight flash sales
            "instagram": ["10:00", "11:00", "20:00"],
            "facebook": ["10:00", "11:00"],
        },
        "hashtag_additions": ["#harbolnas", "#harbolnas2026", "#shoppingday", "#sale", "#diskon"],
        "theme": "Harbolnas - AI tools sale",
        "hook_prefix": "HARBOLNAS! Diskon spesial untuk AI tools 🛒",
        "avoid_content": [],
        "promo_type": "harbolnas_flash",
    },
    "independence_day": {
        "best_times_override": None,
        "hashtag_additions": ["#hut80ri", "#dirgahayuri", "#indonesiamaju", "#merahputih"],
        "theme": "HUT RI - AI untuk kemajuan Indonesia",
        "hook_prefix": "Dirgahayu Indonesia ke-80! 🇮🇩 AI buatan anak bangsa",
        "avoid_content": [],
        "promo_type": "patriotic_promo",
    },
    "11_11": {
        "best_times_override": {
            "tiktok": ["00:00", "11:11", "11:00"],
            "instagram": ["11:00", "11:11"],
            "facebook": ["11:00"],
        },
        "hashtag_additions": ["#1111", "#11november", "#singlesday", "#flashsale"],
        "theme": "11.11 biggest sale",
        "hook_prefix": "11.11 FLASH SALE! 💥",
        "avoid_content": [],
        "promo_type": "flash_sale_1111",
    },
    "12_12": {
        "best_times_override": {
            "tiktok": ["00:00", "12:12", "12:00"],
        },
        "hashtag_additions": ["#1212", "#harbolnas1212", "#flashsale"],
        "theme": "12.12 Harbolnas biggest sale",
        "hook_prefix": "12.12 TERBESAR! 🔥",
        "avoid_content": [],
        "promo_type": "flash_sale_1212",
    },
}


def get_event_for_date(check_date: date) -> Optional[Tuple[str, Dict]]:
    """Check if a date falls within a seasonal event."""
    events = SEASONAL_EVENTS_2026
    
    # Check Ramadan
    if events["ramadan_start"] <= check_date <= events["ramadan_end"]:
        days_in = (check_date - events["ramadan_start"]).days + 1
        return ("ramadan", {
            **SEASONAL_CONTENT_MODS["ramadan"],
            "days_in": days_in,
            "special_note": f"Ramadan Day {days_in}",
        })
    
    # Check Lebaran period
    lebaran_start, lebaran_end = events["lebaran_period"]
    if lebaran_start <= check_date <= lebaran_end:
        return ("lebaran", SEASONAL_CONTENT_MODS["lebaran"])
    
    # Check Harbolnas 11.11 (3 days around it)
    harbolnas_11 = events["harbolnas_1111"]
    if abs((check_date - harbolnas_11).days) <= 3:
        return ("11_11", SEASONAL_CONTENT_MODS["11_11"])
    
    # Check Harbolnas 12.12 (3 days around it)
    harbolnas_12 = events["harbolnas_1212"]
    if abs((check_date - harbolnas_12).days) <= 3:
        return ("12_12", SEASONAL_CONTENT_MODS["12_12"])
    
    # Check Independence Day (3 days around)
    independence = events["independence_day"]
    if abs((check_date - independence).days) <= 3:
        return ("independence_day", SEASONAL_CONTENT_MODS["independence_day"])
    
    # Check other Harbolnas events (1 day)
    for key in ["harbolnas_1010", "harbolnas_1001"]:
        harbolnas_date = events[key]
        if abs((check_date - harbolnas_date).days) <= 1:
            return ("harbolnas", {
                **SEASONAL_CONTENT_MODS["harbolnas"],
                "special_note": f"Harbolnas {harbolnas_date.strftime('%m/%d')}",
            })
    
    return None


def get_upcoming_events(start_date: date, days: int = 30) -> List[Dict]:
    """Get all upcoming seasonal events in a date range."""
    upcoming = []
    for i in range(days):
        check = start_date + timedelta(days=i)
        event = get_event_for_date(check)
        if event:
            event_type, event_data = event
            upcoming.append({
                "date": check.isoformat(),
                "event_type": event_type,
                "theme": event_data.get("theme", ""),
                "special_note": event_data.get("special_note", ""),
            })
    return upcoming


def should_increase_promo(check_date: date) -> bool:
    """Check if we should increase promo content on this date."""
    event = get_event_for_date(check_date)
    if event:
        event_type, _ = event
        return event_type in ["harbolnas", "11_11", "12_12", "lebaran"]
    return False


def get_seasonal_hashtags(check_date: date) -> List[str]:
    """Get seasonal hashtags for the date."""
    event = get_event_for_date(check_date)
    if event:
        _, event_data = event
        return event_data.get("hashtag_additions", [])
    return []


def get_best_times_override(check_date: date, platform: str) -> Optional[List[str]]:
    """Get time override for seasonal events if applicable."""
    event = get_event_for_date(check_date)
    if event:
        _, event_data = event
        override = event_data.get("best_times_override")
        if override:
            return override.get(platform)
    return None


def get_seasonal_hook_prefix(check_date: date) -> str:
    """Get hook prefix for seasonal events."""
    event = get_event_for_date(check_date)
    if event:
        _, event_data = event
        return event_data.get("hook_prefix", "")
    return ""


# Generate 2026 content calendar hints
def get_monthly_theme(month: int) -> str:
    """Get monthly content theme."""
    themes = {
        1: "Resolusi 2026 - AI untuk tahun baru",
        2: "Cinta produktivitas - AI tools terbaik",
        3: "Ramadan produktif dengan AI",
        4: "Post-Lebaran momentum - rebuild",
        5: "May Day - kerja cerdas bukan keras",
        6: "Mid-year review - optimasi bisnis",
        7: "School holiday - edukasi AI",
        8: "HUT RI - AI buatan anak bangsa",
        9: "Back to school/work - AI tools",
        10: "Q4 push - maximalisasi revenue",
        11: "11.11 dan akhir tahun persiapan",
        12: "Harbolnas dan year-end closing",
    }
    return themes.get(month, "AI tools for productivity")
