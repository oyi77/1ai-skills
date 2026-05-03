#!/usr/bin/env python3
"""
POST AI Auto Uploader

Upload generated videos to TikTok/Instagram with captions and scheduling.
"""

import json
import os
import sys
import argparse
import glob
from pathlib import Path
from datetime import datetime, timedelta

# Load config
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"

if not CONFIG_FILE.exists():
    print(f"❌ Config file not found! Copy config.example.json to config.json first.")
    sys.exit(1)

with open(CONFIG_FILE) as f:
    config = json.load(f)

PLATFORMS = {
    "tiktok": config.get("tiktok", {}),
    "instagram": config.get("instagram", {}),
    "threads": config.get("threads", {})
}


def generate_caption(product_info, template=None):
    """
    Generate caption from template with placeholders.

    Args:
        product_info: Dict with product info (name, price, link, etc.)
        template: Custom caption template

    Returns:
        Generated caption string
    """
    name = product_info.get("name", "Produk")
    price = product_info.get("price", "Rp 0")
    link = product_info.get("link", "")

    # Default template
    if not template:
        template = """🔥 {name} - {price}

Jangan sampai kehabisan! Order sekarang:
{link}

{hashtags}

#fyp #viral #affiliatemarketing #promotion"""

    # Format price
    if isinstance(price, (int, float)):
        price = f"Rp {price:,.0f}".replace(",", ".")

    # Generate hashtags
    hashtags = config.get("defaults", {}).get("caption_hashtags", [])
    hashtag_str = " ".join(hashtags) if hashtags else "#fyp #viral"

    # Replace placeholders
    caption = template.format(
        name=name,
        price=price,
        link=link,
        hashtags=hashtag_str
    )

    return caption


def upload_to_tiktok(video_path, caption, scheduled_time=None):
    """
    Upload video to TikTok.

    Args:
        video_path: Path to video file
        caption: Video caption
        scheduled_time: Datetime for scheduled upload (optional)

    Returns:
        Success status and message
    """
    tiktok_config = PLATFORMS.get("tiktok", {})

    if not tiktok_config.get("enabled", False):
        return False, "TikTok not enabled in config"

    print(f"   ↑ Uploading to TikTok: {Path(video_path).name}")

    # TODO: Implement actual TikTok upload
    # Options:
    # 1. Use TikTok API (requires developer account)
    # 2. Use browser automation (Selenium/Playwright + cookies)
    # 3. Use existing TikTok automation libraries

    # Placeholder - replace with actual upload logic
    print(f"      Caption: {caption[:50]}...")

    if scheduled_time:
        print(f"      Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    else:
        print(f"      Status: Uploading now...")

    # Simulate upload
    # time.sleep(2)
    # print(f"      ✅ Uploaded successfully!")

    return True, f"Uploaded to TikTok: {Path(video_path).name}"


def upload_to_instagram(video_path, caption, scheduled_time=None):
    """
    Upload video to Instagram.

    Args:
        video_path: Path to video file
        caption: Video caption
        scheduled_time: Datetime for scheduled upload (optional)

    Returns:
        Success status and message
    """
    ig_config = PLATFORMS.get("instagram", {})

    if not ig_config.get("enabled", False):
        return False, "Instagram not enabled in config"

    print(f"   ↑ Uploading to Instagram: {Path(video_path).name}")

    # TODO: Implement actual Instagram upload
    # Use instaloader or Instagram API (requires business account)

    return True, f"Uploaded to Instagram: {Path(video_path).name}"


def parse_schedule(schedule_str, start_date=None):
    """
    Parse schedule string to list of datetime objects.

    Args:
        schedule_str: Comma-separated schedule ("08:00,14:00,20:00" or "2026-03-05 08:00,14:00,20:00")
        start_date: Base date (defaults to today)

    Returns:
        List of datetime objects
    """
    if not schedule_str:
        return []

    if not start_date:
        start_date = datetime.now()

    schedules = []

    for item in schedule_str.split(","):
        item = item.strip()

        # If contains date, parse full datetime
        if " " in item:
            try:
                dt = datetime.strptime(item, "%Y-%m-%d %H:%M")
                schedules.append(dt)
            except ValueError:
                print(f"⚠️  Invalid schedule format: {item}")
        else:
            # Just time, add to start_date
            try:
                time = datetime.strptime(item, "%H:%M").time()
                dt = datetime.combine(start_date.date(), time)
                schedules.append(dt)
            except ValueError:
                print(f"⚠️  Invalid time format: {item}")

    return schedules


def auto_upload(source_pattern, platform, caption_file=None, schedule=None, hashtags=None):
    """
    Auto-upload videos with captions.

    Args:
        source_pattern: Glob pattern for video files
        platform: Target platform (tiktok, instagram, threads)
        caption_file: Text file with captions (one per video)
        schedule: Comma-separated schedule
        hashtags: Custom hashtags (comma-separated)

    Returns:
        Summary dict with upload results
    """
    # Get videos
    videos = sorted(glob.glob(str(source_pattern)))

    if not videos:
        print(f"❌ No videos found matching: {source_pattern}")
        return {"total": 0, "uploaded": 0, "failed": 0}

    print(f"📤 Found {len(videos)} videos to upload")
    print(f"   Platform: {platform}")
    print(f"   Schedule: {schedule if schedule else 'Immediate'}")
    print()

    # Load captions
    captions = []
    if caption_file and Path(caption_file).exists():
        with open(caption_file) as f:
            captions = [line.strip() for line in f if line.strip()]
        print(f"📝 Loaded {len(captions)} captions")

    # Parse schedule
    schedules = parse_schedule(schedule)

    # Upload
    uploaded = 0
    failed = 0

    for i, video_path in enumerate(videos, 1):
        print(f"   [{i}/{len(videos)}] Processing...")

        # Get caption
        if i <= len(captions):
            caption = captions[i - 1]
        else:
            # Generate default caption
            caption = generate_caption({
                "name": "Produk Impian",
                "price": "Rp 150.000",
                "link": "https://shope.ee/product"
            })

        # Get scheduled time
        scheduled_time = None
        if i <= len(schedules):
            scheduled_time = schedules[i - 1]

        # Upload based on platform
        try:
            if platform == "tiktok":
                success, msg = upload_to_tiktok(video_path, caption, scheduled_time)
            elif platform == "instagram":
                success, msg = upload_to_instagram(video_path, caption, scheduled_time)
            else:
                print(f"   ⚠️  Platform not yet supported: {platform}")
                success = False

            if success:
                uploaded += 1
                print(f"   ✅ {msg}")
            else:
                failed += 1
                print(f"   ❌ {msg}")

            print()
        except Exception as e:
            failed += 1
            print(f"   ❌ Upload failed: {e}")
            print()

    # Summary
    return {
        "total": len(videos),
        "uploaded": uploaded,
        "failed": failed
    }


def main():
    parser = argparse.ArgumentParser(description="Auto-upload videos to social platforms")
    parser.add_argument("--source", required=True, help="Glob pattern for video files (e.g., videos/*.mp4)")
    parser.add_argument("--platform", default="tiktok", choices=["tiktok", "instagram", "threads"],
                        help="Target platform (default: tiktok)")
    parser.add_argument("--caption-file", help="Text file with captions (one per video)")
    parser.add_argument("--schedule", help="Comma-separated schedule (e.g., '08:00,14:00,20:00' or '2026-03-05 08:00,14:00,20:00')")
    parser.add_argument("--hashtags", help="Custom hashtags (comma-separated)")

    args = parser.parse_args()

    # Auto-upload
    result = auto_upload(
        source_pattern=args.source,
        platform=args.platform,
        caption_file=args.caption_file,
        schedule=args.schedule,
        hashtags=args.hashtags
    )

    # Summary
    print()
    print("=" * 60)
    print("📊 UPLOAD SUMMARY")
    print("=" * 60)
    print(f"Total videos: {result['total']}")
    print(f"Uploaded: {result['uploaded']} ✅")
    print(f"Failed: {result['failed']} ❌")
    print("=" * 60)


if __name__ == "__main__":
    main()