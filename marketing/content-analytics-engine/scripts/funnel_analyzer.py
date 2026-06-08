"""
funnel_analyzer.py — Views → Clicks → Sales drop-off analysis
Tracks the revenue funnel for JENDRALBOT affiliate campaign
"""

from datetime import datetime
from collections import defaultdict
from typing import Any

# LYNK click data must be injected manually or via config
# PostBridge doesn't have LYNK data — we track it here
LYNK_DATA = {
    "total_clicks": 196,  # From LYNK dashboard as of 2026-03-13
    "sales": 0,
    "products": {
        "MOVA": {"clicks": 0, "sales": 0, "price_idr": 0},  # Free product
        "paid_1": {"clicks": 0, "sales": 0, "price_idr": 49000},
        "paid_2": {"clicks": 0, "sales": 0, "price_idr": 49000},
        "paid_3": {"clicks": 0, "sales": 0, "price_idr": 49000},
        "paid_4": {"clicks": 0, "sales": 0, "price_idr": 59000},
        "paid_5": {"clicks": 0, "sales": 0, "price_idr": 89000},
    },
}


def compute_funnel(
    analytics: list, lynk_clicks: int = 196, lynk_sales: int = 0
) -> dict:
    """
    Compute full funnel: Views → Engagement → LYNK Clicks → Sales

    Stage 1: Views (from PostBridge analytics)
    Stage 2: Engagement (likes+comments+shares)
    Stage 3: LYNK Clicks (from LYNK dashboard — manual input)
    Stage 4: Sales (from LYNK dashboard — manual input)

    Returns drop-off rates at each stage.
    """
    total_views = sum(a.get("view_count", 0) or 0 for a in analytics)
    total_likes = sum(a.get("like_count", 0) or 0 for a in analytics)
    total_comments = sum(a.get("comment_count", 0) or 0 for a in analytics)
    total_shares = sum(a.get("share_count", 0) or 0 for a in analytics)
    total_engagement = total_likes + total_comments + total_shares

    # Estimate profile visits (typically 2-5% of views for short video)
    # No API for this — estimate based on industry benchmarks
    estimated_profile_visits = round(total_views * 0.03)

    stages = {
        "1_views": {
            "count": total_views,
            "label": "Total Video Views",
            "drop_off_pct": 0.0,
        },
        "2_engagement": {
            "count": total_engagement,
            "label": "Total Engagements (likes+comments+shares)",
            "drop_off_pct": round(
                (1 - total_engagement / max(total_views, 1)) * 100, 1
            ),
        },
        "3_profile_visits_est": {
            "count": estimated_profile_visits,
            "label": "Estimated Profile Visits (3% of views)",
            "drop_off_pct": round(
                (1 - estimated_profile_visits / max(total_views, 1)) * 100, 1
            ),
            "is_estimate": True,
        },
        "4_lynk_clicks": {
            "count": lynk_clicks,
            "label": "LYNK Link Clicks",
            "drop_off_pct": round(
                (1 - lynk_clicks / max(estimated_profile_visits, 1)) * 100, 1
            ),
        },
        "5_sales": {
            "count": lynk_sales,
            "label": "Confirmed Sales",
            "drop_off_pct": round((1 - lynk_sales / max(lynk_clicks, 1)) * 100, 1),
        },
    }

    # Conversion rates
    view_to_click_rate = round(lynk_clicks / max(total_views, 1) * 100, 4)
    click_to_sale_rate = round(lynk_sales / max(lynk_clicks, 1) * 100, 2)
    view_to_sale_rate = round(lynk_sales / max(total_views, 1) * 100, 4)

    # Diagnosis
    bottleneck = "unknown"
    recommendation = ""

    if total_views < 1000:
        bottleneck = "reach"
        recommendation = "CRITICAL: Need more views. Post more content, optimize hooks. Target 10K+ views."
    elif total_engagement == 0:
        bottleneck = "engagement"
        recommendation = "Views exist but zero engagement. Content is boring or CTA is weak. Add better hooks."
    elif lynk_clicks < total_views * 0.01:
        bottleneck = "cta_conversion"
        recommendation = "Weak CTA performance. Link in bio not compelling. Test direct URL in caption."
    elif lynk_sales == 0 and lynk_clicks > 50:
        bottleneck = "landing_page"
        recommendation = "196 clicks → 0 sales. LYNK page not converting. Check product positioning, pricing, copy."

    return {
        "funnel_stages": stages,
        "conversion_rates": {
            "view_to_click": f"{view_to_click_rate}%",
            "click_to_sale": f"{click_to_sale_rate}%",
            "view_to_sale": f"{view_to_sale_rate}%",
            "engagement_rate": f"{round(total_engagement / max(total_views, 1) * 100, 4)}%",
        },
        "bottleneck": bottleneck,
        "recommendation": recommendation,
        "raw_counts": {
            "views": total_views,
            "engagement": total_engagement,
            "lynk_clicks": lynk_clicks,
            "sales": lynk_sales,
        },
        "analyzed_at": datetime.now().isoformat(),
    }


def platform_funnel_breakdown(analytics: list) -> dict:
    """Break down funnel metrics by platform."""
    platforms = defaultdict(lambda: {"views": 0, "engagement": 0, "posts": 0})

    for a in analytics:
        p = a.get("platform", "unknown")
        v = a.get("view_count", 0) or 0
        e = (
            (a.get("like_count", 0) or 0)
            + (a.get("comment_count", 0) or 0)
            + (a.get("share_count", 0) or 0)
        )
        platforms[p]["views"] += v
        platforms[p]["engagement"] += e
        platforms[p]["posts"] += 1

    result = {}
    for p, d in platforms.items():
        result[p] = {
            "views": d["views"],
            "engagement": d["engagement"],
            "posts": d["posts"],
            "engagement_rate": f"{round(d['engagement'] / max(d['views'], 1) * 100, 4)}%",
            "views_per_post": round(d["views"] / max(d["posts"], 1), 1),
            # LYNK clicks can't be split by platform without UTM tracking
            "lynk_clicks_unknown": "UTM tracking needed for platform-level LYNK data",
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["views"], reverse=True))


def content_funnel_analysis(analytics: list) -> dict:
    """
    Identify which content descriptions mention LYNK links
    and correlate with view performance.
    """
    lynk_posts = []
    no_lynk_posts = []

    for a in analytics:
        desc = a.get("video_description", "") or ""
        views = a.get("view_count", 0) or 0
        has_lynk = "lynk.id" in desc.lower()
        if has_lynk:
            lynk_posts.append(views)
        else:
            no_lynk_posts.append(views)

    avg_lynk = round(sum(lynk_posts) / len(lynk_posts), 1) if lynk_posts else 0
    avg_no_lynk = (
        round(sum(no_lynk_posts) / len(no_lynk_posts), 1) if no_lynk_posts else 0
    )

    return {
        "with_lynk_link": {
            "posts": len(lynk_posts),
            "total_views": sum(lynk_posts),
            "avg_views": avg_lynk,
        },
        "without_lynk_link": {
            "posts": len(no_lynk_posts),
            "total_views": sum(no_lynk_posts),
            "avg_views": avg_no_lynk,
        },
        "insight": (
            "LYNK posts perform better"
            if avg_lynk > avg_no_lynk
            else "Non-LYNK posts perform better — check if LYNK in caption hurts algo"
        ),
    }


if __name__ == "__main__":
    import sys, json

    sys.path.insert(0, ".")
    from analytics_collector import collect_all

    data = collect_all(use_cache=True)
    funnel = compute_funnel(data["analytics"])

    print("🎯 FUNNEL ANALYSIS")
    for stage, info in funnel["funnel_stages"].items():
        print(
            f"  {stage}: {info['count']:,} ({info['label']}) — drop-off: {info['drop_off_pct']}%"
        )
    print(f"\n⚠️  BOTTLENECK: {funnel['bottleneck'].upper()}")
    print(f"💡 RECOMMENDATION: {funnel['recommendation']}")
