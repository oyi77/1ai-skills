"""
batch_scheduler.py - Schedule entire calendar to PostBridge API
Handles bulk scheduling of posts with rate limiting and error handling.
"""

import json
import time
import sys
import os
import requests
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

POSTBRIDGE_BASE = "https://api.post-bridge.com/v1"
POSTBRIDGE_KEY = "REDACTED_ROTATED_CREDENTIAL"
RATE_LIMIT_DELAY = 0.2  # 200ms between requests (max 10/sec)

HEADERS = {
    "Authorization": f"Bearer {POSTBRIDGE_KEY}",
    "Content-Type": "application/json",
}

# Map platform names to PostBridge platform identifiers
PLATFORM_MAP = {
    "tiktok": "tiktok",
    "instagram": "instagram",
    "youtube_shorts": "youtube",
    "facebook": "facebook",
}


def get_social_accounts() -> List[Dict]:
    """Fetch connected social accounts from PostBridge."""
    resp = requests.get(f"{POSTBRIDGE_BASE}/social-accounts", headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    accounts = data.get("data", data) if isinstance(data, dict) else data
    return accounts if isinstance(accounts, list) else []


def format_scheduled_at(post_date: str, post_time: str, timezone: str = "Asia/Jakarta") -> str:
    """Format scheduled_at for PostBridge API (ISO 8601 with timezone)."""
    # PostBridge expects ISO 8601 datetime
    # WIB = UTC+7
    dt_str = f"{post_date}T{post_time}:00+07:00"
    return dt_str


def create_post(
    account_id: int,
    caption: str,
    hashtags: List[str],
    scheduled_at: str,
    platform: str,
    media_ids: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Dict:
    """
    Create a scheduled post via PostBridge API.
    
    Returns:
        {"success": bool, "post_id": str, "error": str}
    """
    # Build full caption with hashtags
    hashtag_str = " ".join(hashtags)
    full_caption = f"{caption}\n\n{hashtag_str}".strip()
    
    payload = {
        "caption": full_caption,
        "scheduled_at": scheduled_at,
        "social_accounts": [account_id],
    }
    
    if media_ids:
        payload["media"] = media_ids
    
    if dry_run:
        print(f"    [DRY RUN] Would POST to {POSTBRIDGE_BASE}/posts:")
        print(f"    Account: {account_id}, Platform: {platform}")
        print(f"    Scheduled: {scheduled_at}")
        print(f"    Caption: {full_caption[:100]}...")
        return {"success": True, "post_id": "dry_run_id", "dry_run": True}
    
    try:
        resp = requests.post(
            f"{POSTBRIDGE_BASE}/posts",
            headers=HEADERS,
            json=payload,
            timeout=30,
        )
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            post_id = data.get("id") or data.get("data", {}).get("id", "unknown")
            return {"success": True, "post_id": post_id}
        else:
            return {
                "success": False,
                "post_id": None,
                "error": f"HTTP {resp.status_code}: {resp.text[:200]}",
            }
    except requests.RequestException as e:
        return {"success": False, "post_id": None, "error": str(e)}


def upload_media(file_path: str, content_type: str = "video/mp4") -> Optional[str]:
    """
    Upload media to PostBridge and return media_id.
    
    Args:
        file_path: Local path to the media file
        content_type: MIME type of the media
    
    Returns:
        media_id or None if failed
    """
    try:
        # Step 1: Get upload URL
        resp = requests.post(
            f"{POSTBRIDGE_BASE}/media/create-upload-url",
            headers=HEADERS,
            json={"content_type": content_type},
            timeout=15,
        )
        resp.raise_for_status()
        upload_data = resp.json()
        
        upload_url = upload_data.get("upload_url")
        media_id = upload_data.get("id") or upload_data.get("media_id")
        
        if not upload_url:
            print(f"    ❌ No upload_url in response: {upload_data}")
            return None
        
        # Step 2: Upload file to S3/CDN
        with open(file_path, "rb") as f:
            upload_resp = requests.put(
                upload_url,
                data=f,
                headers={"Content-Type": content_type},
                timeout=120,
            )
        
        if upload_resp.status_code in [200, 201, 204]:
            return media_id
        else:
            print(f"    ❌ Upload failed: HTTP {upload_resp.status_code}")
            return None
            
    except Exception as e:
        print(f"    ❌ Upload error: {e}")
        return None


def schedule_day(
    day: Dict,
    dry_run: bool = False,
    skip_missing_media: bool = True,
    media_dir: Optional[str] = None,
) -> Dict:
    """
    Schedule all posts for a single day to PostBridge.
    
    Returns:
        {"date": str, "scheduled": int, "failed": int, "skipped": int, "results": list}
    """
    results = []
    scheduled = 0
    failed = 0
    skipped = 0
    
    print(f"\n📅 Scheduling {day['date']} ({day['day_name']})...")
    
    for post in day["posts"]:
        print(f"  ⏰ {post['time']} | {post['platform']} | {post['pillar']} | {post['product']}")
        
        # Check if media is needed and available
        media_needed = post.get("media_needed")
        media_ids = []
        
        if media_needed and media_needed != "None":
            if media_dir:
                # Look for media file
                media_path = Path(media_dir) / f"{media_needed}.mp4"
                if not media_path.exists():
                    media_path = Path(media_dir) / f"{media_needed}.jpg"
                
                if media_path.exists():
                    print(f"    📁 Uploading: {media_path.name}")
                    media_id = upload_media(str(media_path))
                    if media_id:
                        media_ids.append(media_id)
                    else:
                        print(f"    ⚠️  Upload failed for {media_path.name}")
                else:
                    if skip_missing_media and post["platform"] in ["tiktok", "youtube_shorts"]:
                        print(f"    ⏭️  Skipping (media required but not found: {media_needed})")
                        skipped += 1
                        results.append({
                            "post": post,
                            "status": "skipped",
                            "reason": f"media not found: {media_needed}",
                        })
                        time.sleep(RATE_LIMIT_DELAY)
                        continue
            else:
                # No media dir, post text only if platform allows
                if PLATFORM_MAP.get(post["platform"]) in ["tiktok", "youtube"]:
                    if not dry_run:
                        print(f"    ⏭️  Skipping {post['platform']} (requires media, none available)")
                        skipped += 1
                        results.append({
                            "post": post,
                            "status": "skipped",
                            "reason": "media required",
                        })
                        time.sleep(RATE_LIMIT_DELAY)
                        continue
        
        # Format scheduled_at
        scheduled_at = format_scheduled_at(day["date"], post["time"])
        
        # Create post
        result = create_post(
            account_id=post["account_id"],
            caption=post["caption"],
            hashtags=post["hashtags"],
            scheduled_at=scheduled_at,
            platform=post["platform"],
            media_ids=media_ids if media_ids else None,
            dry_run=dry_run,
        )
        
        if result["success"]:
            scheduled += 1
            print(f"    ✅ Scheduled! Post ID: {result.get('post_id', 'N/A')}")
        else:
            failed += 1
            print(f"    ❌ Failed: {result.get('error', 'Unknown error')}")
        
        results.append({
            "post": post,
            "status": "scheduled" if result["success"] else "failed",
            "post_id": result.get("post_id"),
            "error": result.get("error"),
        })
        
        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)
    
    return {
        "date": day["date"],
        "scheduled": scheduled,
        "failed": failed,
        "skipped": skipped,
        "results": results,
    }


def schedule_calendar(
    calendar: Dict,
    dry_run: bool = False,
    skip_missing_media: bool = True,
    media_dir: Optional[str] = None,
    max_days: Optional[int] = None,
    start_from_date: Optional[str] = None,
) -> Dict:
    """
    Schedule an entire calendar to PostBridge.
    
    Args:
        calendar: Calendar dict from generate_calendar()
        dry_run: If True, don't actually post
        skip_missing_media: Skip posts missing required media
        media_dir: Directory containing media files
        max_days: Limit number of days to schedule
        start_from_date: Only schedule from this date onwards (YYYY-MM-DD)
    
    Returns:
        Scheduling report
    """
    print(f"\n🚀 Starting batch scheduling to PostBridge...")
    if dry_run:
        print("   [DRY RUN MODE - no actual posts]")
    
    total_scheduled = 0
    total_failed = 0
    total_skipped = 0
    day_reports = []
    
    days = calendar.get("days", [])
    
    # Filter by start_from_date
    if start_from_date:
        days = [d for d in days if d["date"] >= start_from_date]
    
    # Limit days
    if max_days:
        days = days[:max_days]
    
    for day in days:
        day_result = schedule_day(
            day,
            dry_run=dry_run,
            skip_missing_media=skip_missing_media,
            media_dir=media_dir,
        )
        
        total_scheduled += day_result["scheduled"]
        total_failed += day_result["failed"]
        total_skipped += day_result["skipped"]
        day_reports.append(day_result)
    
    report = {
        "total_scheduled": total_scheduled,
        "total_failed": total_failed,
        "total_skipped": total_skipped,
        "total_processed": total_scheduled + total_failed + total_skipped,
        "success_rate": f"{round(total_scheduled/(total_scheduled+total_failed)*100, 1)}%" if (total_scheduled+total_failed) > 0 else "N/A",
        "dry_run": dry_run,
        "day_reports": day_reports,
    }
    
    print(f"\n📊 SCHEDULING COMPLETE:")
    print(f"   ✅ Scheduled: {total_scheduled}")
    print(f"   ❌ Failed: {total_failed}")
    print(f"   ⏭️  Skipped: {total_skipped}")
    print(f"   📈 Success rate: {report['success_rate']}")
    
    return report


def load_and_schedule(
    calendar_path: str,
    dry_run: bool = False,
    media_dir: Optional[str] = None,
) -> Dict:
    """
    Load calendar from JSON file and schedule it.
    
    Convenience function for CLI usage.
    """
    with open(calendar_path, "r", encoding="utf-8") as f:
        calendar = json.load(f)
    
    return schedule_calendar(
        calendar,
        dry_run=dry_run,
        media_dir=media_dir,
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Schedule calendar to PostBridge")
    parser.add_argument("calendar_file", help="Path to calendar JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't post)")
    parser.add_argument("--media-dir", type=str, help="Directory with media files")
    parser.add_argument("--max-days", type=int, help="Max days to schedule")
    parser.add_argument("--from-date", type=str, help="Schedule from this date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    with open(args.calendar_file, "r", encoding="utf-8") as f:
        calendar = json.load(f)
    
    report = schedule_calendar(
        calendar,
        dry_run=args.dry_run,
        media_dir=args.media_dir,
        max_days=args.max_days,
        start_from_date=args.from_date,
    )
    
    # Save report
    report_path = args.calendar_file.replace(".json", "_schedule_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n💾 Schedule report saved to: {report_path}")
