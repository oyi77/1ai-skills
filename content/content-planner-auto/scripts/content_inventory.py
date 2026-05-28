"""
content_inventory.py - Track what media assets exist vs what's needed by the calendar
Scans local directories and matches against calendar requirements.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from datetime import date, timedelta

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Known media asset types and their typical file extensions
MEDIA_EXTENSIONS = {
    "video": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "carousel": [".jpg", ".jpeg", ".png"],  # Multiple images
}

# Asset type to media type mapping
ASSET_TYPE_MAP = {
    "product_demo_video": "video",
    "tutorial_video": "video",
    "tips_video": "video",
    "list_animation_video": "video",
    "promo_video": "video",
    "testimonial_video": "video",
    "bts_video": "video",
    "results_video": "video",
    "case_study_video": "video",
    "ad_video": "video",
    "carousel_images": "carousel",
    "testimonial_carousel": "carousel",
    "story_image": "image",
    "product_image": "image",
    "testimonial_image": "image",
    "result_image": "image",
    "promo_image": "image",
    "bts_image": "image",
    "ad_creative": "image",
}

# Default media directories to scan
DEFAULT_MEDIA_DIRS = [
    "~/Videos/berkahkarya",
    "~/Pictures/berkahkarya",
    "/tmp/content",
    "~/.openclaw/workspace/media",
    "~/.openclaw/workspace/content",
]


def scan_media_directory(directory: str) -> Dict[str, List[str]]:
    """
    Scan a directory for media files.
    
    Returns:
        Dict of {asset_type: [file_paths]}
    """
    dir_path = Path(directory).expanduser()
    
    if not dir_path.exists():
        return {}
    
    assets = {}
    
    for file_path in dir_path.rglob("*"):
        if not file_path.is_file():
            continue
        
        ext = file_path.suffix.lower()
        
        # Find matching asset types
        for asset_type, media_type in ASSET_TYPE_MAP.items():
            extensions = MEDIA_EXTENSIONS.get(media_type, [])
            if ext in extensions:
                # Check if filename hints at this asset type
                filename_lower = file_path.stem.lower()
                asset_keywords = asset_type.replace("_", " ").split()
                
                if any(kw in filename_lower for kw in asset_keywords):
                    if asset_type not in assets:
                        assets[asset_type] = []
                    assets[asset_type].append(str(file_path))
                    break
    
    return assets


def get_needed_assets(calendar: Dict) -> Dict[str, int]:
    """
    Extract all media assets needed by a calendar.
    
    Returns:
        Dict of {asset_type: count_needed}
    """
    needed = {}
    
    for day in calendar.get("days", []):
        for post in day.get("posts", []):
            media_needed = post.get("media_needed")
            if media_needed and media_needed != "None" and media_needed is not None:
                needed[media_needed] = needed.get(media_needed, 0) + 1
    
    return needed


def get_assets_by_platform(calendar: Dict) -> Dict[str, Dict[str, int]]:
    """Get assets needed broken down by platform."""
    by_platform = {}
    
    for day in calendar.get("days", []):
        for post in day.get("posts", []):
            platform = post.get("platform")
            media_needed = post.get("media_needed")
            
            if platform and media_needed and media_needed != "None":
                if platform not in by_platform:
                    by_platform[platform] = {}
                by_platform[platform][media_needed] = by_platform[platform].get(media_needed, 0) + 1
    
    return by_platform


def check_inventory(
    calendar: Dict,
    media_dirs: Optional[List[str]] = None,
) -> Dict:
    """
    Full inventory check against calendar requirements.
    
    Returns:
        Complete inventory report with gaps and available assets.
    """
    if media_dirs is None:
        media_dirs = DEFAULT_MEDIA_DIRS
    
    # Get what's needed
    needed = get_needed_assets(calendar)
    by_platform = get_assets_by_platform(calendar)
    
    # Scan available media
    available = {}
    scanned_dirs = []
    
    for media_dir in media_dirs:
        dir_path = Path(media_dir).expanduser()
        if dir_path.exists():
            scanned_dirs.append(str(dir_path))
            dir_assets = scan_media_directory(str(dir_path))
            for asset_type, files in dir_assets.items():
                if asset_type not in available:
                    available[asset_type] = []
                available[asset_type].extend(files)
    
    # Calculate gaps
    gaps = {}
    have = {}
    
    for asset_type, count_needed in needed.items():
        available_count = len(available.get(asset_type, []))
        
        if available_count == 0:
            gaps[asset_type] = {"needed": count_needed, "available": 0, "status": "MISSING"}
        elif available_count < count_needed:
            gaps[asset_type] = {
                "needed": count_needed,
                "available": available_count,
                "status": "INSUFFICIENT",
                "can_reuse": True,  # Can reuse same video multiple times
            }
        else:
            have[asset_type] = {
                "needed": count_needed,
                "available": available_count,
                "status": "OK",
            }
    
    # Calculate priority
    critical_gaps = [k for k, v in gaps.items() if "video" in k and v["available"] == 0]
    high_gaps = [k for k, v in gaps.items() if k not in critical_gaps]
    
    # Production queue - what to create
    production_queue = []
    
    for asset_type, gap_info in gaps.items():
        media_type = ASSET_TYPE_MAP.get(asset_type, "video")
        priority = "CRITICAL" if asset_type in critical_gaps else "HIGH"
        
        production_queue.append({
            "asset_type": asset_type,
            "media_type": media_type,
            "needed_count": gap_info["needed"],
            "available_count": gap_info["available"],
            "priority": priority,
            "can_reuse_existing": gap_info.get("can_reuse", False),
        })
    
    # Sort by priority and count
    production_queue.sort(key=lambda x: (x["priority"] == "HIGH", -x["needed_count"]))
    
    report = {
        "summary": {
            "total_asset_types_needed": len(needed),
            "asset_types_available": len(have),
            "asset_types_missing": len([g for g in gaps.values() if g["status"] == "MISSING"]),
            "asset_types_insufficient": len([g for g in gaps.values() if g["status"] == "INSUFFICIENT"]),
            "coverage_pct": f"{round(len(have)/len(needed)*100, 1)}%" if needed else "100%",
        },
        "needs_by_platform": by_platform,
        "gaps": gaps,
        "have": have,
        "production_queue": production_queue,
        "scanned_directories": scanned_dirs,
    }
    
    return report


def print_inventory_report(report: Dict) -> None:
    """Print human-readable inventory report."""
    summary = report["summary"]
    
    print("\n" + "="*60)
    print("📦 CONTENT INVENTORY REPORT")
    print("="*60)
    print(f"Coverage: {summary['coverage_pct']}")
    print(f"Asset types needed: {summary['total_asset_types_needed']}")
    print(f"✅ Available: {summary['asset_types_available']}")
    print(f"❌ Missing: {summary['asset_types_missing']}")
    print(f"⚠️  Insufficient: {summary['asset_types_insufficient']}")
    
    print("\n📋 PRODUCTION QUEUE (what to create):")
    for item in report["production_queue"]:
        priority_icon = "🔴" if item["priority"] == "CRITICAL" else "🟡"
        print(f"\n  {priority_icon} [{item['priority']}] {item['asset_type']}")
        print(f"     Type: {item['media_type']}")
        print(f"     Needed: {item['needed_count']} posts")
        print(f"     Have: {item['available_count']} files")
    
    print("\n📊 NEEDS BY PLATFORM:")
    for platform, needs in report["needs_by_platform"].items():
        print(f"\n  {platform}:")
        for asset, count in sorted(needs.items(), key=lambda x: -x[1]):
            status = "✅" if asset in report.get("have", {}) else "❌"
            print(f"    {status} {asset}: {count} posts")
    
    if report["scanned_directories"]:
        print(f"\n🔍 Scanned directories:")
        for d in report["scanned_directories"]:
            print(f"   {d}")


def generate_shoot_list(report: Dict, output_path: Optional[str] = None) -> str:
    """
    Generate a shoot/creation list for the production team.
    
    Returns formatted shoot list as string.
    """
    lines = [
        "# 🎬 CONTENT SHOOT LIST",
        f"Generated: {date.today().isoformat()}",
        "",
        "## PRIORITY 1 - CRITICAL (Videos needed immediately)",
        "",
    ]
    
    critical = [i for i in report["production_queue"] if i["priority"] == "CRITICAL"]
    high = [i for i in report["production_queue"] if i["priority"] == "HIGH"]
    
    if critical:
        for item in critical:
            lines.append(f"### {item['asset_type'].replace('_', ' ').upper()}")
            lines.append(f"- Type: {item['media_type']}")
            lines.append(f"- Used in: {item['needed_count']} posts")
            lines.append(f"- Format: 9:16 vertical (1080x1920)")
            lines.append(f"- Duration: 15-60 seconds")
            lines.append("")
    else:
        lines.append("None - all critical assets covered! ✅")
        lines.append("")
    
    lines.append("## PRIORITY 2 - HIGH")
    lines.append("")
    
    if high:
        for item in high:
            lines.append(f"### {item['asset_type'].replace('_', ' ').upper()}")
            lines.append(f"- Type: {item['media_type']}")
            lines.append(f"- Used in: {item['needed_count']} posts")
            lines.append("")
    else:
        lines.append("None - all high priority assets covered! ✅")
        lines.append("")
    
    lines.append("## NOTES")
    lines.append("- All videos: 9:16 aspect ratio (1080x1920 for TikTok/IG Reels)")
    lines.append("- All images: high quality, 1080px minimum")
    lines.append("- Can reuse same video across multiple posts/platforms")
    lines.append("- Product demo videos: show the product in action")
    
    shoot_list = "\n".join(lines)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(shoot_list)
        print(f"💾 Shoot list saved to: {output_path}")
    
    return shoot_list


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check content inventory against calendar")
    parser.add_argument("calendar_file", help="Calendar JSON file to check against")
    parser.add_argument("--media-dir", action="append", help="Media directory to scan (repeat for multiple)")
    parser.add_argument("--output", type=str, help="Output report JSON path")
    parser.add_argument("--shoot-list", type=str, help="Output shoot list markdown path")
    
    args = parser.parse_args()
    
    with open(args.calendar_file, "r", encoding="utf-8") as f:
        calendar = json.load(f)
    
    media_dirs = args.media_dir if args.media_dir else None
    report = check_inventory(calendar, media_dirs)
    
    print_inventory_report(report)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Report saved to: {args.output}")
    
    if args.shoot_list:
        generate_shoot_list(report, args.shoot_list)
