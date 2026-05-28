"""
trend_detector.py — Detect engagement trends over time
Answers: Is engagement growing or declining? Which day/hour is best?
"""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any


def parse_dt(dt_str: str) -> datetime | None:
    """Parse ISO datetime string with timezone."""
    if not dt_str:
        return None
    try:
        # Handle +00:00 and Z suffixes
        dt_str = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None


def group_by_date(analytics: list) -> dict:
    """Group analytics by published date (UTC+7)."""
    daily = defaultdict(lambda: {
        "views": 0, "likes": 0, "comments": 0, "shares": 0, "posts": 0
    })

    for a in analytics:
        dt = parse_dt(a.get("platform_created_at"))
        if not dt:
            continue
        # Convert to UTC+7
        dt_local = dt + timedelta(hours=7)
        date_key = dt_local.strftime("%Y-%m-%d")

        daily[date_key]["views"] += a.get("view_count", 0) or 0
        daily[date_key]["likes"] += a.get("like_count", 0) or 0
        daily[date_key]["comments"] += a.get("comment_count", 0) or 0
        daily[date_key]["shares"] += a.get("share_count", 0) or 0
        daily[date_key]["posts"] += 1

    # Sort by date
    return dict(sorted(daily.items()))


def group_by_hour(analytics: list) -> dict:
    """Group analytics by hour-of-day (UTC+7) — time-of-day analysis."""
    hourly = defaultdict(lambda: {
        "views": 0, "likes": 0, "posts": 0, "engagement": 0
    })

    for a in analytics:
        dt = parse_dt(a.get("platform_created_at"))
        if not dt:
            continue
        dt_local = dt + timedelta(hours=7)
        hour = dt_local.hour

        views = a.get("view_count", 0) or 0
        likes = a.get("like_count", 0) or 0
        comments = a.get("comment_count", 0) or 0
        shares = a.get("share_count", 0) or 0

        hourly[hour]["views"] += views
        hourly[hour]["likes"] += likes
        hourly[hour]["posts"] += 1
        hourly[hour]["engagement"] += likes + comments + shares

    result = {}
    for hour in range(24):
        d = hourly[hour]
        result[f"{hour:02d}:00"] = {
            "posts": d["posts"],
            "total_views": d["views"],
            "total_engagement": d["engagement"],
            "avg_views": round(d["views"] / d["posts"], 1) if d["posts"] else 0,
        }
    return result


def group_by_day_of_week(analytics: list) -> dict:
    """Group by day of week to find best publishing days."""
    dow_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow = defaultdict(lambda: {"views": 0, "posts": 0, "engagement": 0})

    for a in analytics:
        dt = parse_dt(a.get("platform_created_at"))
        if not dt:
            continue
        dt_local = dt + timedelta(hours=7)
        day = dt_local.weekday()  # 0=Monday

        views = a.get("view_count", 0) or 0
        dow[day]["views"] += views
        dow[day]["posts"] += 1
        dow[day]["engagement"] += (
            (a.get("like_count", 0) or 0)
            + (a.get("comment_count", 0) or 0)
            + (a.get("share_count", 0) or 0)
        )

    result = {}
    for i, name in enumerate(dow_names):
        d = dow[i]
        result[name] = {
            "posts": d["posts"],
            "total_views": d["views"],
            "avg_views": round(d["views"] / d["posts"], 1) if d["posts"] else 0,
        }
    return result


def compute_growth_rate(daily: dict) -> dict:
    """
    Compute week-over-week growth using daily view data.
    Returns: {trend, growth_pct, week1_views, week2_views}
    """
    dates = sorted(daily.keys())
    if len(dates) < 2:
        return {"trend": "insufficient_data", "growth_pct": 0, "days": len(dates)}

    # Split into two halves
    mid = len(dates) // 2
    first_half = dates[:mid]
    second_half = dates[mid:]

    v1 = sum(daily[d]["views"] for d in first_half)
    v2 = sum(daily[d]["views"] for d in second_half)

    if v1 == 0:
        growth = 100.0 if v2 > 0 else 0.0
    else:
        growth = round((v2 - v1) / v1 * 100, 1)

    trend = "growing" if growth > 5 else "declining" if growth < -5 else "stable"

    return {
        "trend": trend,
        "growth_pct": growth,
        "first_half_views": v1,
        "second_half_views": v2,
        "first_period": f"{first_half[0]} → {first_half[-1]}",
        "second_period": f"{second_half[0]} → {second_half[-1]}"
    }


def best_posting_times(analytics: list) -> dict:
    """Identify top 3 best hours and days for posting."""
    hourly = group_by_hour(analytics)
    dow = group_by_day_of_week(analytics)

    # Best hours (by avg views, only count hours with posts)
    active_hours = {h: d for h, d in hourly.items() if d["posts"] > 0}
    best_hours = sorted(active_hours.items(), key=lambda x: x[1]["avg_views"], reverse=True)[:3]

    # Best days
    active_days = {d: v for d, v in dow.items() if v["posts"] > 0}
    best_days = sorted(active_days.items(), key=lambda x: x[1]["avg_views"], reverse=True)[:3]

    return {
        "best_hours": [{"hour": h, **d} for h, d in best_hours],
        "best_days": [{"day": d, **v} for d, v in best_days],
        "hourly_breakdown": hourly,
        "daily_breakdown": dow
    }


def weekly_trend_report(analytics: list) -> dict:
    """Full weekly trend analysis."""
    daily = group_by_date(analytics)
    growth = compute_growth_rate(daily)
    timing = best_posting_times(analytics)

    # Platform-specific trends
    platforms = set(a.get("platform") for a in analytics)
    platform_trends = {}
    for platform in platforms:
        p_analytics = [a for a in analytics if a.get("platform") == platform]
        p_daily = group_by_date(p_analytics)
        platform_trends[platform] = compute_growth_rate(p_daily)

    return {
        "daily_breakdown": daily,
        "growth_analysis": growth,
        "platform_trends": platform_trends,
        "timing": timing,
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from analytics_collector import collect_all
    import json

    data = collect_all(use_cache=True)
    report = weekly_trend_report(data["analytics"])

    print("📈 TREND ANALYSIS")
    print(f"Trend: {report['growth_analysis']['trend'].upper()}")
    print(f"Growth: {report['growth_analysis']['growth_pct']}%")
    print(f"\nBest posting hours: {[x['hour'] for x in report['timing']['best_hours']]}")
    print(f"Best posting days: {[x['day'] for x in report['timing']['best_days']]}")
