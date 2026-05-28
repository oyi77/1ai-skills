"""
calendar_generator.py - Auto-generate 30-day content calendar for BerkahKarya
Main orchestrator that combines pillars, platforms, and seasonal events.
"""

import json
import random
import sys
import os
from datetime import date, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from pillar_rotator import (
    PILLARS, PRODUCTS, get_pillar_sequence, get_content_type,
    get_caption_template, select_product, get_hashtags
)
from platform_optimizer import (
    ACCOUNTS, PLATFORM_RULES, build_daily_schedule,
    get_content_format, get_media_needed
)
from seasonal_calendar import (
    get_event_for_date, get_seasonal_hashtags,
    get_best_times_override, get_seasonal_hook_prefix,
    get_monthly_theme
)


def generate_caption(
    pillar: str,
    product: Dict,
    content_type: str,
    hook: str,
    platform: str
) -> str:
    """Generate a full caption for a post."""
    template = get_caption_template(pillar)
    caption = template.format(
        product=product["name"],
        hook=hook,
        price=product.get("price", "IDR 49K"),
        lynk_url=product["lynk_url"],
    )
    
    # Trim to platform limit
    limit = PLATFORM_RULES.get(platform, {}).get("caption_limit", 2200)
    if len(caption) > limit:
        caption = caption[:limit-3] + "..."
    
    return caption.strip()


def generate_hook(pillar: str, product: Dict, seasonal_prefix: str = "") -> str:
    """Generate a hook for the post."""
    hooks = product.get("hook_templates", [])
    if not hooks:
        hooks = [
            f"Kamu harus lihat {product['name']} sekarang! 🔥",
            f"{product['name']} - game changer untuk {pillar.replace('_', ' ')} 🚀",
        ]
    
    hook = random.choice(hooks)
    
    if seasonal_prefix:
        hook = f"{seasonal_prefix} {hook}"
    
    return hook


def create_post_entry(
    post_date: date,
    scheduled_time: str,
    platform: str,
    account: Dict,
    pillar: str,
    product: Dict,
    content_type: str,
    day_index: int,
    seasonal_event: Optional[Any] = None,
) -> Dict:
    """Create a single post entry in the calendar format."""
    
    # Seasonal modifiers
    seasonal_prefix = ""
    extra_hashtags = []
    if seasonal_event:
        event_type, event_data = seasonal_event
        seasonal_prefix = event_data.get("hook_prefix", "")
        extra_hashtags = event_data.get("hashtag_additions", [])
    
    # Generate content
    hook = generate_hook(pillar, product, seasonal_prefix)
    caption = generate_caption(pillar, product, content_type, hook, platform)
    hashtags = get_hashtags(pillar, platform, product["name"])
    
    # Add seasonal hashtags
    for tag in extra_hashtags:
        if tag not in hashtags:
            hashtags.append(tag)
    
    # Limit hashtags by platform
    max_hashtags = PLATFORM_RULES.get(platform, {}).get("hashtag_limit", 30)
    hashtags = hashtags[:max_hashtags]
    
    # Get media needed
    media_needed = get_media_needed(content_type)
    
    return {
        "time": scheduled_time,
        "platform": platform,
        "account_id": account["id"],
        "account_name": account.get("username", ""),
        "pillar": pillar,
        "product": product["name"],
        "content_type": content_type,
        "hook": hook,
        "caption": caption,
        "hashtags": hashtags,
        "media_needed": media_needed,
        "lynk_url": product["lynk_url"],
        "seasonal_event": seasonal_event[0] if seasonal_event else None,
    }


def generate_daily_calendar(
    day_date: date,
    day_index: int,
    pillar_sequence: List[str],
) -> Dict:
    """Generate calendar entry for a single day."""
    posts = []
    
    # Get seasonal event for this day
    seasonal_event = get_event_for_date(day_date)
    
    # Get base schedule (time + platform + account)
    schedule_slots = build_daily_schedule(day_date, day_index)
    
    # Assign pillars to slots
    daily_pillars = []
    num_slots = len(schedule_slots)
    
    # Use the pillar sequence, cycling through for each day
    base_pillar_idx = day_index % len(pillar_sequence)
    for i in range(num_slots):
        pillar_idx = (base_pillar_idx + i) % len(pillar_sequence)
        daily_pillars.append(pillar_sequence[pillar_idx])
    
    # If seasonal event increases promo, replace some pillars
    if seasonal_event:
        event_type, _ = seasonal_event
        if event_type in ["harbolnas", "11_11", "12_12", "lebaran"]:
            # Replace up to 2 non-promo slots with promo_cta
            replacements = 0
            for i, pillar in enumerate(daily_pillars):
                if replacements < 2 and pillar not in ["promo_cta"]:
                    daily_pillars[i] = "promo_cta"
                    replacements += 1
    
    # Create post entries
    for i, slot in enumerate(schedule_slots):
        pillar = daily_pillars[i % len(daily_pillars)]
        platform = slot["platform"]
        account = slot["account"]
        
        # Get content format for this platform + pillar
        content_type = get_content_format(platform, pillar)
        
        # Select product (rotating)
        product = select_product(pillar, day_index + i)
        
        # Check for time overrides from seasonal events
        scheduled_time = slot["time"]
        if seasonal_event:
            event_type, event_data = seasonal_event
            time_override = event_data.get("best_times_override", {})
            if time_override and platform in time_override:
                override_times = time_override[platform]
                if override_times:
                    scheduled_time = override_times[i % len(override_times)]
        
        post = create_post_entry(
            post_date=day_date,
            scheduled_time=scheduled_time,
            platform=platform,
            account=account,
            pillar=pillar,
            product=product,
            content_type=content_type,
            day_index=day_index,
            seasonal_event=seasonal_event,
        )
        posts.append(post)
    
    # Sort posts by time
    posts.sort(key=lambda x: x["time"])
    
    return {
        "date": day_date.isoformat(),
        "day_name": day_date.strftime("%A"),
        "monthly_theme": get_monthly_theme(day_date.month),
        "seasonal_event": seasonal_event[0] if seasonal_event else None,
        "total_posts": len(posts),
        "posts": posts,
    }


def generate_calendar(
    start_date: date,
    num_days: int = 30,
    output_path: Optional[str] = None,
) -> Dict:
    """
    Generate a complete content calendar.
    
    Args:
        start_date: First day of the calendar
        num_days: How many days to generate (default: 30)
        output_path: Optional path to save JSON output
    
    Returns:
        Complete calendar dictionary
    """
    print(f"🗓️  Generating {num_days}-day content calendar starting {start_date.isoformat()}...")
    
    # Generate pillar rotation sequence
    pillar_sequence = get_pillar_sequence(start_date, num_days * 10)
    
    # Generate each day
    days = []
    total_posts = 0
    
    for i in range(num_days):
        day_date = start_date + timedelta(days=i)
        day_calendar = generate_daily_calendar(day_date, i, pillar_sequence)
        days.append(day_calendar)
        total_posts += day_calendar["total_posts"]
        print(f"  ✅ {day_date.strftime('%Y-%m-%d %A')}: {day_calendar['total_posts']} posts")
    
    # Build summary
    pillar_counts = {}
    platform_counts = {}
    product_counts = {}
    
    for day in days:
        for post in day["posts"]:
            pillar = post["pillar"]
            platform = post["platform"]
            product = post["product"]
            pillar_counts[pillar] = pillar_counts.get(pillar, 0) + 1
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
            product_counts[product] = product_counts.get(product, 0) + 1
    
    calendar = {
        "meta": {
            "generated_at": date.today().isoformat(),
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=num_days - 1)).isoformat(),
            "num_days": num_days,
            "total_posts": total_posts,
            "version": "1.0.0",
        },
        "summary": {
            "posts_per_day_avg": round(total_posts / num_days, 1),
            "pillar_distribution": {
                k: f"{round(v/total_posts*100, 1)}%" 
                for k, v in sorted(pillar_counts.items(), key=lambda x: -x[1])
            },
            "platform_distribution": {
                k: v for k, v in sorted(platform_counts.items(), key=lambda x: -x[1])
            },
            "product_distribution": {
                k: v for k, v in sorted(product_counts.items(), key=lambda x: -x[1])
            },
        },
        "days": days,
    }
    
    # Save to file if requested
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(calendar, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Calendar saved to: {output_path}")
    
    print(f"\n✅ Calendar generated: {total_posts} total posts over {num_days} days")
    print(f"   Avg posts/day: {round(total_posts/num_days, 1)}")
    
    return calendar


def print_day_summary(day: Dict) -> None:
    """Print a human-readable summary of a single day's posts."""
    print(f"\n📅 {day['date']} ({day['day_name']})")
    if day.get("seasonal_event"):
        print(f"   🎉 Seasonal: {day['seasonal_event']}")
    print(f"   Total posts: {day['total_posts']}")
    
    for post in day["posts"]:
        emoji = {
            "tiktok": "🎵",
            "instagram": "📸",
            "youtube_shorts": "▶️",
            "facebook": "👥",
        }.get(post["platform"], "📱")
        
        print(f"   {post['time']} {emoji} {post['platform']} | {post['pillar']} | {post['product']}")
        print(f"      Hook: {post['hook'][:60]}...")
        print(f"      Media: {post['media_needed']} | Account: {post['account_name']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate BerkahKarya content calendar")
    parser.add_argument("--start", type=str, default=date.today().isoformat(), 
                        help="Start date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=7, help="Number of days")
    parser.add_argument("--output", type=str, help="Output JSON file path")
    parser.add_argument("--print", action="store_true", help="Print human-readable output")
    
    args = parser.parse_args()
    
    start = date.fromisoformat(args.start)
    output = args.output or f"/tmp/calendar_{args.start}_{args.days}days.json"
    
    calendar = generate_calendar(start, args.days, output)
    
    if args.print:
        print("\n" + "="*60)
        print("CONTENT CALENDAR PREVIEW")
        print("="*60)
        for day in calendar["days"]:
            print_day_summary(day)
    
    print("\n📊 SUMMARY:")
    print(json.dumps(calendar["summary"], indent=2, ensure_ascii=False))
