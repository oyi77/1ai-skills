"""
platform_optimizer.py - Platform-specific timing, format, and account rotation
"""

from datetime import date, time
from typing import List, Dict, Tuple, Optional
import random

# Connected PostBridge Account IDs
ACCOUNTS = {
    "tiktok": [
        {"id": 48187, "name": "tiktok_main", "username": "@berkahkarya"},
        {"id": 48188, "name": "tiktok_2", "username": "@berkahkarya2"},
        {"id": 48189, "name": "tiktok_3", "username": "@berkahkarya3"},
        {"id": 48190, "name": "tiktok_4", "username": "@jendralbot"},
        {"id": 48191, "name": "tiktok_5", "username": "@jendralbot2"},
        {"id": 48192, "name": "tiktok_6", "username": "@aiindonesia"},
        {"id": 48193, "name": "tiktok_7", "username": "@aitools_id"},
    ],
    "instagram": [
        {"id": 48186, "name": "instagram_main", "username": "@berkahkaryadigitalproduct"},
    ],
    "facebook": [
        {"id": 48194, "name": "facebook_main", "username": "BerkahKarya"},
        {"id": 48195, "name": "facebook_2", "username": "JendralBot"},
        {"id": 48196, "name": "facebook_3", "username": "AI Indonesia"},
        {"id": 48197, "name": "facebook_4", "username": "Digital Product ID"},
    ],
    "youtube": [
        {"id": 48198, "name": "youtube_main", "username": "BerkahKarya"},
    ],
}

# Platform posting rules
PLATFORM_RULES = {
    "tiktok": {
        "best_times": ["11:00", "12:00", "19:00", "20:00", "21:00"],
        "max_per_day": 3,
        "formats": ["video_demo", "tutorial_short", "tip_video", "list_video", "promo_video", "testimonial_video"],
        "aspect_ratio": "9:16",
        "max_duration_sec": 180,
        "caption_limit": 2200,
        "hashtag_limit": 100,
        "requires_media": True,
        "preferred_content": ["video"],
    },
    "instagram": {
        "best_times": ["07:00", "08:00", "17:00", "18:00", "19:00"],
        "max_per_day": 3,
        "formats": ["reel", "carousel", "story", "single_image"],
        "aspect_ratio": "9:16",  # for reels
        "max_duration_sec": 90,
        "caption_limit": 2200,
        "hashtag_limit": 30,
        "requires_media": True,
        "preferred_content": ["reel", "carousel"],
    },
    "youtube_shorts": {
        "best_times": ["14:00", "15:00", "16:00", "17:00"],
        "max_per_day": 2,
        "formats": ["demo_short", "tips_short", "bts_short", "promo_short", "case_study_short"],
        "aspect_ratio": "9:16",
        "max_duration_sec": 60,
        "caption_limit": 5000,
        "hashtag_limit": 15,
        "requires_media": True,
        "preferred_content": ["video"],
    },
    "facebook": {
        "best_times": ["09:00", "10:00", "11:00"],
        "max_per_day": 2,
        "formats": ["video", "link_post", "text_post", "image_post", "testimonial_post"],
        "aspect_ratio": "16:9",  # flexible
        "max_duration_sec": 240,
        "caption_limit": 63206,
        "hashtag_limit": 30,
        "requires_media": False,
        "preferred_content": ["video", "image", "link"],
    },
}

# Media type mapping by format
MEDIA_NEEDED = {
    "video_demo": "product_demo_video",
    "tutorial_short": "tutorial_video",
    "tip_video": "tips_video",
    "list_video": "list_animation_video",
    "promo_video": "promo_video",
    "testimonial_video": "testimonial_video",
    "reel": "product_demo_video",
    "carousel": "carousel_images",
    "story": "story_image",
    "single_image": "product_image",
    "demo_short": "product_demo_video",
    "tips_short": "tips_video",
    "bts_short": "bts_video",
    "promo_short": "promo_video",
    "case_study_short": "case_study_video",
    "video": "product_demo_video",
    "link_post": None,
    "text_post": None,
    "image_post": "product_image",
    "testimonial_post": "testimonial_image",
    "bts_video": "bts_video",
    "day_in_life": "bts_video",
    "reel_bts": "bts_video",
    "story_series": "story_image",
    "bts_post": "bts_image",
    "flash_sale": "promo_video",
    "promo_reel": "promo_video",
    "discount_story": "promo_image",
    "promo_short": "promo_video",
    "promo_post": "promo_image",
    "ad_creative": "ad_video",
    "carousel_testimony": "testimonial_carousel",
    "story_result": "result_image",
    "results_video": "results_video",
    "result_image": "result_image",
}


def get_platform_schedule(platform: str, day_date: date, post_index: int) -> str:
    """Get optimal posting time for a platform on a given day."""
    rules = PLATFORM_RULES[platform]
    best_times = rules["best_times"]
    return best_times[post_index % len(best_times)]


def get_account(platform: str, day_index: int, post_index: int) -> Dict:
    """Get account to post from, rotating across available accounts."""
    accounts = ACCOUNTS.get(platform, [])
    if not accounts:
        return {"id": 0, "name": "unknown", "username": "unknown"}
    
    # Rotate: different accounts on different days
    account_index = (day_index + post_index) % len(accounts)
    return accounts[account_index]


def get_content_format(platform: str, pillar: str) -> str:
    """Get best content format for platform + pillar combo."""
    from pillar_rotator import PILLARS
    
    pillar_formats = PILLARS.get(pillar, {}).get("content_types", {}).get(platform, [])
    platform_formats = PLATFORM_RULES[platform]["formats"]
    
    # Prefer pillar-specific formats, fall back to platform defaults
    available = [f for f in pillar_formats if f in platform_formats]
    if available:
        return available[0]
    return platform_formats[0]


def get_media_needed(content_type: str) -> Optional[str]:
    """Get what media asset is needed for this content type."""
    return MEDIA_NEEDED.get(content_type, "product_demo_video")


def build_daily_schedule(day_date: date, day_index: int) -> List[Dict]:
    """
    Build the full posting schedule for a single day across all platforms.
    Returns list of post slots sorted by time.
    """
    schedule = []
    
    # TikTok: 3 posts/day across 7 accounts
    for i in range(3):
        account = get_account("tiktok", day_index, i)
        schedule.append({
            "platform": "tiktok",
            "account": account,
            "time": get_platform_schedule("tiktok", day_date, i),
            "post_index": i,
        })
    
    # Instagram: up to 3 posts/day (1 account)
    for i in range(2):  # 2 posts per day to not spam
        account = get_account("instagram", day_index, i)
        schedule.append({
            "platform": "instagram",
            "account": account,
            "time": get_platform_schedule("instagram", day_date, i),
            "post_index": i,
        })
    
    # YouTube Shorts: 1-2 per day
    for i in range(1):
        account = get_account("youtube_shorts", day_index, i)
        schedule.append({
            "platform": "youtube_shorts",
            "account": account,
            "time": get_platform_schedule("youtube_shorts", day_date, i),
            "post_index": i,
        })
    
    # Facebook: 2 posts/day across 4 pages
    for i in range(2):
        account = get_account("facebook", day_index, i)
        schedule.append({
            "platform": "facebook",
            "account": account,
            "time": get_platform_schedule("facebook", day_date, i),
            "post_index": i,
        })
    
    # Sort by time
    schedule.sort(key=lambda x: x["time"])
    return schedule


def get_platform_constraints(platform: str) -> Dict:
    """Return platform constraints for validation."""
    return PLATFORM_RULES.get(platform, {})
