#!/usr/bin/env python3
"""
Content Calendar Generator
Generates a structured content calendar as CSV.
Used by the marketing-ops skill for /marketing-ops calendar.

Usage:
    python content_calendar.py --weeks 4 --platforms "linkedin,instagram,blog"
    python content_calendar.py --weeks 4 --platforms "all" --pillars "educational,promotional,social-proof"
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_PILLARS = [
    "Educational",
    "Social Proof",
    "Thought Leadership",
    "Promotional",
    "Community"
]

DEFAULT_PLATFORMS = ["LinkedIn", "Instagram", "Twitter/X", "Blog", "Email"]

PLATFORM_SPECS = {
    "LinkedIn": {"frequency": "5/week", "best_days": "Tue-Thu", "format": "Post/Carousel/Article"},
    "Instagram": {"frequency": "5/week", "best_days": "Tue-Fri", "format": "Feed/Reel/Story"},
    "Twitter/X": {"frequency": "daily", "best_days": "Mon-Fri", "format": "Tweet/Thread"},
    "TikTok": {"frequency": "daily", "best_days": "Tue-Thu", "format": "Video 30-60s"},
    "Facebook": {"frequency": "5/week", "best_days": "Wed-Fri", "format": "Post/Video/Live"},
    "Blog": {"frequency": "2/week", "best_days": "Tue,Thu", "format": "Article 1500-2500 words"},
    "Email": {"frequency": "1/week", "best_days": "Tue,Thu", "format": "Newsletter"},
    "YouTube": {"frequency": "1-2/week", "best_days": "Sat-Sun", "format": "Video 8-15 min"},
}

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def generate_calendar(weeks: int, platforms: list, pillars: list, start_date: datetime = None):
    """Generate a content calendar structure."""
    if start_date is None:
        start_date = datetime.now()
        # Start from next Monday
        days_ahead = 0 - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        start_date += timedelta(days=days_ahead)

    rows = []
    pillar_cycle = pillars * 10  # enough for cycling

    for week in range(weeks):
        week_start = start_date + timedelta(weeks=week)
        week_pillar = pillar_cycle[week % len(pillars)]

        for day_offset in range(7):
            current_date = week_start + timedelta(days=day_offset)
            day_name = WEEKDAYS[current_date.weekday()]

            # Skip weekends for most business platforms
            if current_date.weekday() >= 5:  # Saturday, Sunday
                for platform in platforms:
                    if platform in ["YouTube", "Instagram", "TikTok"]:
                        rows.append({
                            "Week": week + 1,
                            "Date": current_date.strftime("%Y-%m-%d"),
                            "Day": day_name,
                            "Theme": week_pillar,
                            "Platform": platform,
                            "Content Type": "",
                            "Topic": "",
                            "CTA": "",
                            "Funnel Stage": "",
                            "Status": "Planned",
                            "Notes": ""
                        })
                continue

            for platform in platforms:
                rows.append({
                    "Week": week + 1,
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Day": day_name,
                    "Theme": week_pillar,
                    "Platform": platform,
                    "Content Type": PLATFORM_SPECS.get(platform, {}).get("format", ""),
                    "Topic": "",
                    "CTA": "",
                    "Funnel Stage": "",
                    "Status": "Planned",
                    "Notes": ""
                })

    return rows


def write_csv(rows: list, output_path: str):
    """Write calendar to CSV file."""
    if not rows:
        return

    fieldnames = rows[0].keys()
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate a marketing content calendar")
    parser.add_argument("--weeks", type=int, default=4, help="Number of weeks (default: 4)")
    parser.add_argument("--platforms", type=str, default="linkedin,instagram,blog",
                       help="Comma-separated platforms or 'all'")
    parser.add_argument("--pillars", type=str, default=None,
                       help="Comma-separated content pillars")
    parser.add_argument("--output", type=str, default=None,
                       help="Output file path (default: content-calendar-YYYY-MM-DD.csv)")
    parser.add_argument("--start", type=str, default=None,
                       help="Start date YYYY-MM-DD (default: next Monday)")

    args = parser.parse_args()

    # Parse platforms
    if args.platforms.lower() == "all":
        platforms = DEFAULT_PLATFORMS
    else:
        platforms = [p.strip().title() for p in args.platforms.split(",")]
        # Fix casing for known platforms
        platform_map = {p.lower(): p for p in PLATFORM_SPECS.keys()}
        platforms = [platform_map.get(p.lower(), p) for p in platforms]

    # Parse pillars
    pillars = DEFAULT_PILLARS
    if args.pillars:
        pillars = [p.strip().title() for p in args.pillars.split(",")]

    # Parse start date
    start_date = None
    if args.start:
        start_date = datetime.strptime(args.start, "%Y-%m-%d")

    # Generate
    rows = generate_calendar(args.weeks, platforms, pillars, start_date)

    # Output
    output_path = args.output or f"content-calendar-{datetime.now().strftime('%Y-%m-%d')}.csv"
    write_csv(rows, output_path)

    print(f"✅ Calendar generated: {output_path}")
    print(f"   {args.weeks} weeks × {len(platforms)} platforms = {len(rows)} slots")
    print(f"   Platforms: {', '.join(platforms)}")
    print(f"   Pillars: {', '.join(pillars)}")


if __name__ == "__main__":
    main()
