"""
report_generator.py — Auto-generate daily/weekly markdown reports
Saves to ~/.openclaw/workspace/reports/YYYY-MM-DD-analytics.md
Also outputs JSON for skill consumption
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

REPORTS_DIR = Path("/home/openclaw/.openclaw/workspace/reports")


def _stars(score: float, max_score: float = 100) -> str:
    """Convert score to visual stars."""
    pct = score / max(max_score, 1)
    if pct >= 0.8:
        return "⭐⭐⭐⭐⭐"
    elif pct >= 0.6:
        return "⭐⭐⭐⭐"
    elif pct >= 0.4:
        return "⭐⭐⭐"
    elif pct >= 0.2:
        return "⭐⭐"
    else:
        return "⭐"


def _trend_arrow(value: float) -> str:
    if value > 10:
        return "🚀 ↑↑"
    elif value > 0:
        return "📈 ↑"
    elif value == 0:
        return "➡️ →"
    elif value > -10:
        return "📉 ↓"
    else:
        return "🔴 ↓↓"


def generate_daily_report(dataset: dict, date: str = None) -> str:
    """Generate daily performance report in Markdown."""
    from performance_analyzer import full_analysis, compute_engagement_rate
    from funnel_analyzer import compute_funnel
    from trend_detector import weekly_trend_report
    from optimization_engine import generate_content_recommendations

    date = date or datetime.now().strftime("%Y-%m-%d")
    analysis = full_analysis(dataset)
    funnel = compute_funnel(dataset["analytics"])
    trend = weekly_trend_report(dataset["analytics"])
    recommendations = generate_content_recommendations(
        dataset["analytics"], dataset["posts"]
    )

    summary = analysis["summary"]
    platforms = analysis["platform_breakdown"]
    errors = analysis["error_analysis"]

    lines = [
        f"# 📊 BerkahKarya Content Analytics Report",
        f"**Date:** {date}",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M WIB')}",
        f"**Campaign:** JENDRALBOT Affiliate Marketing",
        "",
        "---",
        "",
        "## 🎯 Executive Summary",
        "",
        f"| Metric | Value | Target | Status |",
        f"|--------|-------|--------|--------|",
        f"| Total Views | {summary['total_views']:,} | 10,000 | {'✅' if summary['total_views'] >= 10000 else '🔴'} |",
        f"| Total Likes | {summary['total_likes']:,} | 100 | {'✅' if summary['total_likes'] >= 100 else '🔴'} |",
        f"| Total Comments | {summary['total_comments']:,} | 20 | {'✅' if summary['total_comments'] >= 20 else '🔴'} |",
        f"| Total Shares | {summary['total_shares']:,} | 10 | {'✅' if summary['total_shares'] >= 10 else '🔴'} |",
        f"| Engagement Rate | {summary['overall_engagement_rate']}% | 1%+ | {'✅' if summary['overall_engagement_rate'] >= 1 else '🔴'} |",
        f"| LYNK Clicks | {funnel['raw_counts']['lynk_clicks']:,} | 500 | {'✅' if funnel['raw_counts']['lynk_clicks'] >= 500 else '🔴'} |",
        f"| Sales | {funnel['raw_counts']['sales']:,} | 5 | {'✅' if funnel['raw_counts']['sales'] >= 5 else '🔴'} |",
        "",
        "---",
        "",
        "## 📱 Platform Breakdown",
        "",
        "| Platform | Posts | Views | Avg Views/Post | ER% |",
        "|----------|-------|-------|----------------|-----|",
    ]

    for platform, data in platforms.items():
        lines.append(
            f"| {platform.upper()} | {data['posts']} | {data['views']:,} "
            f"| {data['avg_views_per_post']} | {data['avg_engagement_rate']}% |"
        )

    lines += [
        "",
        "---",
        "",
        "## 🏆 Top Performing Posts",
        "",
    ]

    top_posts = analysis.get("top_posts_by_views", [])[:5]
    for i, post in enumerate(top_posts, 1):
        views = post.get("view_count", 0) or 0
        platform = post.get("platform", "unknown")
        url = post.get("share_url", "")
        desc = (post.get("video_description", "") or "")[:80]
        er = compute_engagement_rate(post)
        lines.append(f"{i}. **[{platform.upper()}]** {views:,} views | ER: {er}%")
        lines.append(f"   > {desc}...")
        if url:
            lines.append(f"   > 🔗 {url}")
        lines.append("")

    lines += [
        "---",
        "",
        "## 💀 Worst Performing Posts",
        "",
    ]

    worst_posts = analysis.get("worst_posts", [])[:3]
    for post in worst_posts:
        views = post.get("view_count", 0) or 0
        platform = post.get("platform", "unknown")
        desc = (post.get("video_description", "") or "")[:60]
        lines.append(f"- [{platform.upper()}] {views} views: {desc}...")

    lines += [
        "",
        "---",
        "",
        "## 🎯 Funnel Analysis",
        "",
        "```",
        "FUNNEL: Views → Engagement → Profile Visits → LYNK Clicks → Sales",
        "",
    ]

    for stage, info in funnel["funnel_stages"].items():
        bar = "█" * min(
            int(info["count"] / max(funnel["raw_counts"]["views"], 1) * 20), 20
        )
        est_note = " (est.)" if info.get("is_estimate") else ""
        lines.append(f"{info['label'][:40]:40} {info['count']:>6,}{est_note}")

    lines += [
        "```",
        "",
        f"**View→Click Rate:** {funnel['conversion_rates']['view_to_click']}",
        f"**Click→Sale Rate:** {funnel['conversion_rates']['click_to_sale']}",
        f"**Bottleneck:** {funnel['bottleneck'].upper()} 🚨",
        f"**Fix:** {funnel['recommendation']}",
        "",
        "---",
        "",
        "## 📈 Trend Analysis",
        "",
        f"**Overall Trend:** {trend['growth_analysis']['trend'].upper()} {_trend_arrow(trend['growth_analysis']['growth_pct'])}",
        f"**Growth Rate:** {trend['growth_analysis']['growth_pct']}%",
        "",
        "### Platform Trends",
    ]

    for p, t in trend["platform_trends"].items():
        arrow = _trend_arrow(t.get("growth_pct", 0))
        lines.append(
            f"- **{p.upper()}:** {t.get('trend', 'n/a').upper()} {arrow} ({t.get('growth_pct', 0)}%)"
        )

    lines += [
        "",
        "### Best Posting Times (UTC+7)",
        "",
        "**Best Hours:**",
    ]
    for h in trend["timing"]["best_hours"]:
        lines.append(
            f"- {h['hour']}: {h.get('avg_views', 0)} avg views ({h.get('posts', 0)} posts)"
        )

    lines += [
        "",
        "**Best Days:**",
    ]
    for d in trend["timing"]["best_days"]:
        lines.append(f"- {d['day']}: {d.get('avg_views', 0)} avg views")

    # Error analysis
    lines += [
        "",
        "---",
        "",
        "## ⚠️ Error Analysis",
        "",
        "| Platform | Success | Failed | Success Rate |",
        "|----------|---------|--------|--------------|",
    ]

    for platform, err_data in errors.items():
        lines.append(
            f"| {platform.upper()} | {err_data['success']} | {err_data['failed']} | {err_data['success_rate']}% |"
        )
        if err_data["error_types"]:
            for err, count in err_data["error_types"].items():
                lines.append(f"| ↳ | | {count}x {err} | |")

    # Recommendations
    lines += [
        "",
        "---",
        "",
        "## ⚡ Action Items",
        "",
    ]

    critical = [r for r in recommendations if r["priority"] == "CRITICAL"]
    high = [r for r in recommendations if r["priority"] == "HIGH"]
    medium = [r for r in recommendations if r["priority"] == "MEDIUM"]

    if critical:
        lines.append("### 🔴 CRITICAL (Do Today)")
        for r in critical:
            lines.append(f"- **{r['action']}**")
            lines.append(f"  - Why: {r['reason']}")
            if r.get("suggestions"):
                for s in r["suggestions"][:3]:
                    lines.append(f"    - {s}")
        lines.append("")

    if high:
        lines.append("### 🟡 HIGH Priority")
        for r in high:
            lines.append(f"- {r['action']}")
            lines.append(f"  - {r['reason']}")
        lines.append("")

    if medium:
        lines.append("### 🟢 MEDIUM Priority")
        for r in medium:
            lines.append(f"- {r['action']}")
        lines.append("")

    lines += [
        "---",
        "",
        f"*Generated by BerkahKarya Content Analytics Engine v1.0 | {date}*",
        "",
    ]

    return "\n".join(lines)


def generate_weekly_report(dataset: dict, week_start: str = None) -> str:
    """Generate weekly summary report."""
    from trend_detector import weekly_trend_report
    from roi_calculator import compute_roi

    date = datetime.now().strftime("%Y-%m-%d")
    trend = weekly_trend_report(dataset["analytics"])
    roi = compute_roi(dataset["analytics"], dataset["posts"])

    analytics = dataset["analytics"]
    total_views = sum(a.get("view_count", 0) or 0 for a in analytics)

    lines = [
        f"# 📊 BerkahKarya Weekly Analytics Report",
        f"**Week ending:** {date}",
        "",
        "## Summary",
        f"- Total Views: {total_views:,}",
        f"- Growth Trend: {trend['growth_analysis']['trend'].upper()}",
        f"- Growth Rate: {trend['growth_analysis']['growth_pct']}%",
        f"- Campaign ROI Status: {roi['status']}",
        f"- Break-even: {roi['break_even']['explanation']}",
        "",
        "## Platform Performance",
    ]

    for p, t in trend["platform_trends"].items():
        lines.append(
            f"- **{p.upper()}:** {t.get('trend', 'n/a')} ({t.get('growth_pct', 0)}%)"
        )

    lines += [
        "",
        "## Key Insights",
        "1. "
        + (
            trend["growth_analysis"]["trend"].upper()
            + " trend — "
            + (
                "Keep pushing!"
                if trend["growth_analysis"]["trend"] == "growing"
                else (
                    "Need to change strategy"
                    if trend["growth_analysis"]["trend"] == "declining"
                    else "Steady, need to accelerate"
                )
            )
        ),
        "",
        f"*Generated: {date}*",
    ]

    return "\n".join(lines)


def save_report(content: str, report_type: str = "daily", date: str = None) -> str:
    """Save report to disk and return path."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    date = date or datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-analytics-{report_type}.md"
    path = REPORTS_DIR / filename
    with open(path, "w") as f:
        f.write(content)
    return str(path)


def save_json_output(data: dict, report_type: str = "daily", date: str = None) -> str:
    """Save JSON output for consumption by other skills."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    date = date or datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-analytics-{report_type}.json"
    path = REPORTS_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return str(path)


def generate_all_reports(dataset: dict, date: str = None) -> dict:
    """Generate all report types and save to disk."""
    from performance_analyzer import full_analysis
    from funnel_analyzer import compute_funnel, platform_funnel_breakdown
    from trend_detector import weekly_trend_report
    from optimization_engine import full_optimization_report
    from ab_test_tracker import run_all_auto_tests
    from roi_calculator import compute_roi

    date = date or datetime.now().strftime("%Y-%m-%d")

    print(f"[REPORT] Generating daily report for {date}...")
    daily_md = generate_daily_report(dataset, date)
    daily_path = save_report(daily_md, "daily", date)
    print(f"[REPORT] Saved: {daily_path}")

    print(f"[REPORT] Generating weekly report...")
    weekly_md = generate_weekly_report(dataset, date)
    weekly_path = save_report(weekly_md, "weekly", date)
    print(f"[REPORT] Saved: {weekly_path}")

    print(f"[REPORT] Building JSON output...")
    analysis = full_analysis(dataset)
    funnel = compute_funnel(dataset["analytics"])
    trend = weekly_trend_report(dataset["analytics"])
    optimization = full_optimization_report(dataset)
    ab_tests = run_all_auto_tests(dataset["analytics"])
    roi = compute_roi(dataset["analytics"], dataset["posts"])

    json_output = {
        "date": date,
        "summary": analysis["summary"],
        "platform_breakdown": analysis["platform_breakdown"],
        "content_types": analysis["content_types"],
        "funnel": funnel,
        "trend": {
            "growth": trend["growth_analysis"],
            "platform_trends": trend["platform_trends"],
            "best_times": trend["timing"]["best_hours"][:3],
            "best_days": trend["timing"]["best_days"][:3],
        },
        "roi": roi,
        "optimization": {
            "critical_count": optimization["critical_count"],
            "recommendations": optimization["recommendations"][:10],
            "action_plan": optimization["action_plan"],
        },
        "ab_tests": {
            "hook_winner": ab_tests["hook_test"]["winner"],
            "platform_winner": ab_tests["platform_test"]["winner"],
            "caption_length_winner": ab_tests["length_test"]["winner"],
        },
        "errors": analysis["error_analysis"],
        "generated_at": datetime.now().isoformat(),
    }

    json_path = save_json_output(json_output, "full", date)
    print(f"[REPORT] Saved JSON: {json_path}")

    return {
        "daily_md": daily_path,
        "weekly_md": weekly_path,
        "json": json_path,
        "date": date,
    }


if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")
    from analytics_collector import collect_all

    import argparse

    parser = argparse.ArgumentParser(description="Generate analytics reports")
    parser.add_argument("--sync", action="store_true", help="Sync analytics first")
    parser.add_argument("--cache", action="store_true", help="Use cached data")
    parser.add_argument("--date", type=str, help="Report date (YYYY-MM-DD)")
    args = parser.parse_args()

    data = collect_all(use_cache=args.cache, force_sync=args.sync)
    paths = generate_all_reports(data, date=args.date)

    print(f"\n✅ Reports generated:")
    print(f"  Daily MD: {paths['daily_md']}")
    print(f"  Weekly MD: {paths['weekly_md']}")
    print(f"  JSON: {paths['json']}")
