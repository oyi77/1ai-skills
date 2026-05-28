"""
optimization_engine.py — Recommend what to post more/less of
Analyzes patterns to generate actionable content strategy recommendations
"""

from datetime import datetime
from collections import defaultdict
from performance_analyzer import (
    platform_summary, content_type_summary, compute_engagement_rate,
    detect_content_type, detect_hook_type
)
from trend_detector import best_posting_times


def score_platform(platform_data: dict) -> dict:
    """Score each platform on a 0-100 scale based on performance."""
    scores = {}
    # Find max values for normalization
    max_views = max((d["avg_views_per_post"] for d in platform_data.values()), default=1)
    max_er = max((d["avg_engagement_rate"] for d in platform_data.values()), default=0.01)

    for platform, data in platform_data.items():
        view_score = (data["avg_views_per_post"] / max(max_views, 1)) * 60  # 60% weight
        er_score = (data["avg_engagement_rate"] / max(max_er, 0.01)) * 40   # 40% weight
        scores[platform] = {
            "total_score": round(view_score + er_score, 1),
            "view_score": round(view_score, 1),
            "engagement_score": round(er_score, 1),
            "avg_views_per_post": data["avg_views_per_post"],
            "avg_engagement_rate": data["avg_engagement_rate"],
        }

    return dict(sorted(scores.items(), key=lambda x: x[1]["total_score"], reverse=True))


def generate_content_recommendations(analytics: list, posts: list) -> list:
    """
    Generate specific actionable recommendations based on data.
    Returns list of recommendations sorted by priority.
    """
    recommendations = []

    total_views = sum(a.get("view_count", 0) or 0 for a in analytics)
    total_engagement = sum(
        (a.get("like_count", 0) or 0) + (a.get("comment_count", 0) or 0)
        + (a.get("share_count", 0) or 0) for a in analytics
    )

    platform_data = platform_summary(analytics)
    content_data = content_type_summary(analytics, posts)
    timing = best_posting_times(analytics)

    # === PLATFORM RECOMMENDATIONS ===
    platform_scores = score_platform(platform_data)
    if platform_scores:
        top_platform = list(platform_scores.keys())[0]
        top_data = platform_scores[top_platform]
        recommendations.append({
            "priority": "HIGH",
            "category": "platform",
            "action": f"DOUBLE DOWN on {top_platform.upper()}",
            "reason": f"Best performer: {top_data['avg_views_per_post']} avg views/post, score {top_data['total_score']}/100",
            "metric": f"{top_platform}: {top_data['avg_views_per_post']} avg views vs others",
            "urgency": "immediate"
        })

        # Low performers
        bottom_platforms = list(platform_scores.keys())[-2:]
        for p in bottom_platforms:
            d = platform_scores[p]
            if d["avg_views_per_post"] < 10:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "platform",
                    "action": f"REDUCE or AUDIT {p.upper()} posting",
                    "reason": f"Only {d['avg_views_per_post']} avg views/post — minimal ROI",
                    "metric": f"{p}: score {d['total_score']}/100",
                    "urgency": "this_week"
                })

    # === CONTENT TYPE RECOMMENDATIONS ===
    if content_data:
        top_content = list(content_data.keys())[0]
        top_cdata = content_data[top_content]
        recommendations.append({
            "priority": "HIGH",
            "category": "content_type",
            "action": f"CREATE MORE '{top_content.upper()}' content",
            "reason": f"Best content type: {top_cdata['avg_views_per_post']} avg views, {top_cdata['avg_engagement_rate']}% ER",
            "metric": f"{top_cdata['posts']} posts → {top_cdata['total_views']} total views",
            "urgency": "immediate"
        })

    # === VOLUME RECOMMENDATIONS ===
    if total_views < 1000:
        recommendations.append({
            "priority": "CRITICAL",
            "category": "volume",
            "action": "POST MORE — current volume is too low",
            "reason": f"Only {total_views} total views. Need 10K+ for meaningful funnel data.",
            "metric": f"Target: 50+ posts/day across all platforms",
            "urgency": "today"
        })

    # === ENGAGEMENT RECOMMENDATIONS ===
    er = round(total_engagement / max(total_views, 1) * 100, 4)
    if er < 0.5:
        recommendations.append({
            "priority": "HIGH",
            "category": "engagement",
            "action": "IMPROVE HOOKS — engagement rate critically low",
            "reason": f"Engagement rate: {er}% (industry target: 1-3%)",
            "metric": f"Only {total_engagement} engagements from {total_views} views",
            "urgency": "immediate",
            "suggestions": [
                "Use personal story hooks ('Bun, aku baru tau...')",
                "Add direct question in first 3 seconds",
                "End with clear CTA ('Klik link di bio!')",
                "Test emoji-heavy openings"
            ]
        })

    # === TIMING RECOMMENDATIONS ===
    if timing["best_hours"]:
        best_hour = timing["best_hours"][0]["hour"]
        recommendations.append({
            "priority": "MEDIUM",
            "category": "timing",
            "action": f"SCHEDULE POSTS for {best_hour} WIB (peak time)",
            "reason": f"Highest avg views at {best_hour}",
            "metric": f"Data from {timing['best_hours'][0]['posts']} posts",
            "urgency": "this_week"
        })

    # === INSTAGRAM FIX ===
    recommendations.append({
        "priority": "CRITICAL",
        "category": "technical",
        "action": "FIX Instagram — ALL posts need media (images/videos)",
        "reason": "40 Instagram posts FAILED due to missing media",
        "metric": "0% success rate on Instagram text-only posts",
        "urgency": "today",
        "fix": "Always attach image/video when posting to Instagram. Use /v1/media/create-upload-url first."
    })

    # === CONVERSION RECOMMENDATIONS ===
    recommendations.append({
        "priority": "CRITICAL",
        "category": "conversion",
        "action": "AUDIT LYNK.ID landing page — 196 clicks → 0 sales is broken",
        "reason": "CTR exists but conversion is 0%. Page or product is not converting.",
        "metric": "196 clicks, 0 sales = 0% conversion (industry: 1-3%)",
        "urgency": "today",
        "suggestions": [
            "Review LYNK page product descriptions",
            "Check if price IDR 49-89K is appropriate for audience",
            "Add social proof / testimonials",
            "Test free product funnel first (MOVA)",
            "Add urgency / scarcity messaging"
        ]
    })

    # Sort by priority
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 99))

    return recommendations


def what_to_post_more(content_data: dict) -> list:
    """Return list of content types ranked by performance."""
    sorted_types = sorted(
        content_data.items(),
        key=lambda x: x[1]["avg_views_per_post"],
        reverse=True
    )
    return [
        {
            "content_type": ctype,
            "avg_views": data["avg_views_per_post"],
            "posts": data["posts"],
            "verdict": "POST MORE ✅" if i < 2 else "TEST MORE 🔄" if i < 4 else "POST LESS ❌"
        }
        for i, (ctype, data) in enumerate(sorted_types)
    ]


def generate_weekly_action_plan(recommendations: list) -> dict:
    """Convert recommendations into a concrete weekly action plan."""
    today_actions = [r for r in recommendations if r.get("urgency") == "today"]
    immediate_actions = [r for r in recommendations if r.get("urgency") == "immediate"]
    week_actions = [r for r in recommendations if r.get("urgency") == "this_week"]

    return {
        "today": [r["action"] for r in today_actions],
        "this_week": [r["action"] for r in week_actions],
        "ongoing": [r["action"] for r in immediate_actions],
        "priority_count": {
            "CRITICAL": sum(1 for r in recommendations if r["priority"] == "CRITICAL"),
            "HIGH": sum(1 for r in recommendations if r["priority"] == "HIGH"),
            "MEDIUM": sum(1 for r in recommendations if r["priority"] == "MEDIUM"),
        }
    }


def full_optimization_report(dataset: dict) -> dict:
    """Run full optimization analysis."""
    analytics = dataset["analytics"]
    posts = dataset["posts"]
    social_accounts = dataset["social_accounts"]

    platform_data = platform_summary(analytics)
    platform_scores = score_platform(platform_data)
    content_data = content_type_summary(analytics, posts)
    recommendations = generate_content_recommendations(analytics, posts)
    action_plan = generate_weekly_action_plan(recommendations)
    post_more = what_to_post_more(content_data)

    return {
        "platform_rankings": platform_scores,
        "content_type_rankings": post_more,
        "recommendations": recommendations,
        "action_plan": action_plan,
        "critical_count": sum(1 for r in recommendations if r["priority"] == "CRITICAL"),
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import sys, json
    sys.path.insert(0, ".")
    from analytics_collector import collect_all

    data = collect_all(use_cache=True)
    report = full_optimization_report(data)

    print("⚡ OPTIMIZATION RECOMMENDATIONS")
    print(f"🚨 CRITICAL actions needed: {report['critical_count']}")
    print("\nToday's must-do:")
    for a in report["action_plan"]["today"]:
        print(f"  🔴 {a}")
    print("\nThis week:")
    for a in report["action_plan"]["this_week"]:
        print(f"  🟡 {a}")
