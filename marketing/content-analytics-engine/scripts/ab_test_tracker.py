"""
ab_test_tracker.py — Track A/B test results
Compares hooks, content types, platforms, posting times
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from performance_analyzer import compute_engagement_rate, detect_hook_type, detect_content_type

AB_TESTS_FILE = Path("/home/openclaw/.openclaw/workspace/reports/ab_tests.json")


def load_ab_tests() -> list:
    """Load existing A/B test records."""
    if AB_TESTS_FILE.exists():
        with open(AB_TESTS_FILE) as f:
            return json.load(f)
    return []


def save_ab_tests(tests: list):
    """Save A/B test records."""
    AB_TESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AB_TESTS_FILE, "w") as f:
        json.dump(tests, f, indent=2, default=str)


def create_ab_test(name: str, variant_a: str, variant_b: str,
                   hypothesis: str, metric: str = "avg_views") -> dict:
    """Create a new A/B test."""
    tests = load_ab_tests()
    test = {
        "id": f"ab_{len(tests)+1:03d}",
        "name": name,
        "variant_a": variant_a,
        "variant_b": variant_b,
        "hypothesis": hypothesis,
        "metric": metric,
        "status": "running",
        "created_at": datetime.now().isoformat(),
        "results": None
    }
    tests.append(test)
    save_ab_tests(tests)
    return test


def auto_detect_hook_tests(analytics: list) -> dict:
    """
    Automatically detect hook type performance from analytics data.
    Treats different hook types as natural A/B test variants.
    """
    hook_groups = defaultdict(list)

    for a in analytics:
        desc = a.get("video_description", "") or ""
        hook = detect_hook_type(desc)
        views = a.get("view_count", 0) or 0
        er = compute_engagement_rate(a)
        hook_groups[hook].append({"views": views, "er": er})

    results = {}
    for hook, data in hook_groups.items():
        views = [d["views"] for d in data]
        ers = [d["er"] for d in data]
        results[hook] = {
            "posts": len(data),
            "avg_views": round(sum(views) / len(views), 1) if views else 0,
            "max_views": max(views) if views else 0,
            "avg_engagement_rate": round(sum(ers) / len(ers), 4) if ers else 0,
        }

    # Rank hooks
    ranked = sorted(results.items(), key=lambda x: x[1]["avg_views"], reverse=True)
    winner = ranked[0][0] if ranked else "unknown"

    return {
        "test_name": "Hook Type Performance (Auto-Detected)",
        "metric": "avg_views",
        "variants": dict(ranked),
        "winner": winner,
        "recommendation": f"Use '{winner}' hook style — {results.get(winner, {}).get('avg_views', 0)} avg views",
        "analyzed_at": datetime.now().isoformat()
    }


def auto_detect_platform_tests(analytics: list) -> dict:
    """Compare platform performance as A/B variants."""
    platform_groups = defaultdict(list)

    for a in analytics:
        p = a.get("platform", "unknown")
        views = a.get("view_count", 0) or 0
        er = compute_engagement_rate(a)
        platform_groups[p].append({"views": views, "er": er})

    results = {}
    for platform, data in platform_groups.items():
        views = [d["views"] for d in data]
        results[platform] = {
            "posts": len(data),
            "avg_views": round(sum(views) / len(views), 1) if views else 0,
            "total_views": sum(views),
        }

    ranked = sorted(results.items(), key=lambda x: x[1]["avg_views"], reverse=True)
    winner = ranked[0][0] if ranked else "unknown"

    return {
        "test_name": "Platform Comparison (Auto-Detected)",
        "metric": "avg_views",
        "variants": dict(ranked),
        "winner": winner,
        "recommendation": f"Focus on {winner.upper()} — best avg views per post",
        "analyzed_at": datetime.now().isoformat()
    }


def auto_detect_content_length_tests(analytics: list) -> dict:
    """Compare short vs long captions."""
    length_groups = defaultdict(list)

    for a in analytics:
        desc = a.get("video_description", "") or ""
        length = len(desc)
        views = a.get("view_count", 0) or 0

        if length < 50:
            bucket = "short (<50 chars)"
        elif length < 200:
            bucket = "medium (50-200 chars)"
        else:
            bucket = "long (200+ chars)"

        length_groups[bucket].append(views)

    results = {}
    for bucket, views_list in length_groups.items():
        results[bucket] = {
            "posts": len(views_list),
            "avg_views": round(sum(views_list) / len(views_list), 1),
            "total_views": sum(views_list),
        }

    ranked = sorted(results.items(), key=lambda x: x[1]["avg_views"], reverse=True)
    winner = ranked[0][0] if ranked else "unknown"

    return {
        "test_name": "Caption Length Test (Auto-Detected)",
        "metric": "avg_views",
        "variants": dict(ranked),
        "winner": winner,
        "recommendation": f"Use {winner} captions — {results.get(winner, {}).get('avg_views', 0)} avg views",
        "analyzed_at": datetime.now().isoformat()
    }


def run_all_auto_tests(analytics: list) -> dict:
    """Run all automatic A/B tests from analytics data."""
    return {
        "hook_test": auto_detect_hook_tests(analytics),
        "platform_test": auto_detect_platform_tests(analytics),
        "length_test": auto_detect_content_length_tests(analytics),
        "manual_tests": load_ab_tests(),
        "note": "Auto-tests derived from existing post performance data. Run more posts for statistical significance.",
        "min_sample_warning": len(analytics) < 30,
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from analytics_collector import collect_all

    data = collect_all(use_cache=True)
    tests = run_all_auto_tests(data["analytics"])

    print("🧪 A/B TEST RESULTS")
    print(f"\n🪝 Hook Test Winner: {tests['hook_test']['winner']}")
    print(f"📱 Platform Winner: {tests['platform_test']['winner']}")
    print(f"📝 Caption Length Winner: {tests['length_test']['winner']}")

    if tests["min_sample_warning"]:
        print(f"\n⚠️  Warning: Only {len(data['analytics'])} analytics records — need 30+ for significance")
