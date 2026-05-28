"""
performance_analyzer.py — Analyze content performance
Identifies best/worst posts, platform leaders, content type patterns
"""

import re
from collections import defaultdict
from typing import Any
from datetime import datetime


def _safe_get(obj: dict, *keys, default=0):
    for k in keys:
        if isinstance(obj, dict):
            obj = obj.get(k, default)
        else:
            return default
    return obj if obj is not None else default


def compute_engagement_rate(analytics_record: dict) -> float:
    """
    Engagement rate = (likes + comments + shares) / views * 100
    Returns 0 if views == 0
    """
    views = analytics_record.get("view_count", 0) or 0
    likes = analytics_record.get("like_count", 0) or 0
    comments = analytics_record.get("comment_count", 0) or 0
    shares = analytics_record.get("share_count", 0) or 0
    if views == 0:
        return 0.0
    return round(((likes + comments + shares) / views) * 100, 4)


def detect_content_type(caption: str) -> str:
    """
    Detect content type from caption text.
    Returns: product_promo | cashback | tutorial | story | brand | unknown
    """
    if not caption:
        return "unknown"
    caption_lower = caption.lower()

    patterns = {
        "cashback": ["cashback", "mova", "belanja tetap", "uang kembali", "hemat", "diskon"],
        "tutorial": ["cara", "langkah", "tips", "trik", "bagaimana", "how to", "tutorial"],
        "story": ["cerita", "dulu", "ternyata", "awalnya", "kaget", "bun,", "bun aku"],
        "product_promo": ["lynk.id", "link in bio", "klik", "beli sekarang", "jendralbot", "produk"],
        "brand": ["berkah karya", "content factory", "digital marketing", "talent agency", "manifesto"],
        "viral_hook": ["viral", "fyp", "trending", "#viral", "#fyp"],
    }

    scores = defaultdict(int)
    for ctype, keywords in patterns.items():
        for kw in keywords:
            if kw in caption_lower:
                scores[ctype] += 1

    if not scores:
        return "unknown"
    return max(scores, key=scores.__getitem__)


def detect_hook_type(caption: str) -> str:
    """Detect hook/opening style from first 100 chars of caption."""
    if not caption:
        return "unknown"
    opening = caption[:100].lower()

    if any(x in opening for x in ["bun,", "bun aku", "cerita"]):
        return "personal_story"
    if any(x in opening for x in ["🚀", "✨", "🔥", "💡"]):
        return "emoji_hook"
    if any(x in opening for x in ["dengan belanja", "cara ", "tips ", "trik "]):
        return "value_hook"
    if any(x in opening for x in ["manifesto", "kenapa", "mengapa"]):
        return "curiosity_hook"
    if any(x in opening for x in ["inside ", "behind ", "how we"]):
        return "behind_scenes"
    return "other"


def rank_posts_by_views(analytics: list) -> list:
    """Return analytics sorted by view_count descending."""
    return sorted(analytics, key=lambda x: x.get("view_count", 0) or 0, reverse=True)


def rank_posts_by_engagement(analytics: list) -> list:
    """Return analytics sorted by engagement rate descending."""
    enriched = []
    for a in analytics:
        a = dict(a)
        a["engagement_rate"] = compute_engagement_rate(a)
        enriched.append(a)
    return sorted(enriched, key=lambda x: x["engagement_rate"], reverse=True)


def platform_summary(analytics: list) -> dict:
    """
    Aggregate metrics by platform.
    Returns: {platform: {views, likes, comments, shares, posts, avg_engagement}}
    """
    summary = defaultdict(lambda: {
        "views": 0, "likes": 0, "comments": 0, "shares": 0,
        "posts": 0, "engagement_rates": []
    })

    for a in analytics:
        p = a.get("platform", "unknown")
        summary[p]["views"] += a.get("view_count", 0) or 0
        summary[p]["likes"] += a.get("like_count", 0) or 0
        summary[p]["comments"] += a.get("comment_count", 0) or 0
        summary[p]["shares"] += a.get("share_count", 0) or 0
        summary[p]["posts"] += 1
        summary[p]["engagement_rates"].append(compute_engagement_rate(a))

    result = {}
    for p, d in summary.items():
        rates = d["engagement_rates"]
        avg_eng = round(sum(rates) / len(rates), 4) if rates else 0.0
        result[p] = {
            "views": d["views"],
            "likes": d["likes"],
            "comments": d["comments"],
            "shares": d["shares"],
            "posts": d["posts"],
            "avg_views_per_post": round(d["views"] / d["posts"], 1) if d["posts"] else 0,
            "avg_engagement_rate": avg_eng,
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["views"], reverse=True))


def content_type_summary(analytics: list, posts: list) -> dict:
    """
    Cross-reference analytics with post captions to group by content type.
    """
    # Build result_id → post caption map
    # analytics has post_result_id; we need the chain: result → post → caption
    # We'll pass posts separately and match via description field as fallback
    caption_map = {}
    for p in posts:
        caption_map[p["id"]] = p.get("caption", "")

    type_stats = defaultdict(lambda: {
        "views": 0, "likes": 0, "comments": 0, "posts": 0,
        "engagement_rates": [], "examples": []
    })

    for a in analytics:
        # Use video_description from analytics as caption proxy
        desc = a.get("video_description", "") or ""
        ctype = detect_content_type(desc)
        hook = detect_hook_type(desc)

        type_stats[ctype]["views"] += a.get("view_count", 0) or 0
        type_stats[ctype]["likes"] += a.get("like_count", 0) or 0
        type_stats[ctype]["comments"] += a.get("comment_count", 0) or 0
        type_stats[ctype]["posts"] += 1
        type_stats[ctype]["engagement_rates"].append(compute_engagement_rate(a))
        if len(type_stats[ctype]["examples"]) < 3:
            type_stats[ctype]["examples"].append({
                "platform": a.get("platform"),
                "views": a.get("view_count", 0),
                "hook": hook,
                "url": a.get("share_url", "")
            })

    result = {}
    for ctype, d in type_stats.items():
        rates = d["engagement_rates"]
        result[ctype] = {
            "posts": d["posts"],
            "total_views": d["views"],
            "total_likes": d["likes"],
            "avg_views_per_post": round(d["views"] / d["posts"], 1) if d["posts"] else 0,
            "avg_engagement_rate": round(sum(rates) / len(rates), 4) if rates else 0,
            "examples": d["examples"]
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["avg_views_per_post"], reverse=True))


def error_analysis(post_results: list, social_accounts: list) -> dict:
    """Analyze post failures by platform and error type."""
    account_map = {a["id"]: a for a in social_accounts}

    errors = defaultdict(lambda: {"count": 0, "error_types": defaultdict(int), "examples": []})
    successes = defaultdict(int)

    for r in post_results:
        acct = account_map.get(r.get("social_account_id"), {})
        platform = acct.get("platform", "unknown")
        if r.get("success"):
            successes[platform] += 1
        else:
            errors[platform]["count"] += 1
            err_msg = r.get("error") or "unknown_error"
            # Normalize error
            if "media" in err_msg.lower() or "supported media" in err_msg.lower():
                err_key = "no_media_files"
            elif "caption" in err_msg.lower():
                err_key = "caption_error"
            elif "auth" in err_msg.lower() or "token" in err_msg.lower():
                err_key = "auth_error"
            else:
                err_key = err_msg[:50]
            errors[platform]["error_types"][err_key] += 1
            if len(errors[platform]["examples"]) < 2:
                errors[platform]["examples"].append(err_msg[:100])

    result = {}
    for p in set(list(errors.keys()) + list(successes.keys())):
        total = successes.get(p, 0) + errors.get(p, {}).get("count", 0)
        result[p] = {
            "success": successes.get(p, 0),
            "failed": errors.get(p, {}).get("count", 0),
            "total": total,
            "success_rate": round(successes.get(p, 0) / total * 100, 1) if total else 0,
            "error_types": dict(errors.get(p, {}).get("error_types", {})),
            "examples": errors.get(p, {}).get("examples", [])
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["total"], reverse=True))


def full_analysis(dataset: dict) -> dict:
    """Run all performance analyses and return combined result."""
    analytics = dataset["analytics"]
    posts = dataset["posts"]
    post_results = dataset["post_results"]
    social_accounts = dataset["social_accounts"]

    top_posts = rank_posts_by_views(analytics)
    by_engagement = rank_posts_by_engagement(analytics)

    total_views = sum(a.get("view_count", 0) or 0 for a in analytics)
    total_likes = sum(a.get("like_count", 0) or 0 for a in analytics)
    total_comments = sum(a.get("comment_count", 0) or 0 for a in analytics)
    total_shares = sum(a.get("share_count", 0) or 0 for a in analytics)
    overall_er = compute_engagement_rate({
        "view_count": total_views,
        "like_count": total_likes,
        "comment_count": total_comments,
        "share_count": total_shares
    })

    return {
        "summary": {
            "total_analytics_records": len(analytics),
            "total_posts": len(posts),
            "total_post_results": len(post_results),
            "total_views": total_views,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_shares": total_shares,
            "overall_engagement_rate": overall_er,
        },
        "platform_breakdown": platform_summary(analytics),
        "content_types": content_type_summary(analytics, posts),
        "top_posts_by_views": top_posts[:10],
        "top_posts_by_engagement": by_engagement[:10],
        "worst_posts": top_posts[-5:][::-1],
        "error_analysis": error_analysis(post_results, social_accounts),
        "analyzed_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    from analytics_collector import collect_all
    import json
    data = collect_all(use_cache=True)
    result = full_analysis(data)
    print(json.dumps(result["summary"], indent=2))
    print("\n📊 Platform breakdown:")
    for p, s in result["platform_breakdown"].items():
        print(f"  {p}: {s['views']} views, {s['posts']} posts, ER={s['avg_engagement_rate']}%")
