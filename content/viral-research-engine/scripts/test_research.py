"""
test_research.py — Integration test for viral-research-engine

Tests all modules and generates a full research report.
Run: python3 test_research.py
"""

import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"


def test_module(name: str, fn, *args, **kwargs):
    """Test a module function and return result."""
    try:
        result = fn(*args, **kwargs)
        print(f"  {PASS} {name}")
        return True, result
    except Exception as e:
        print(f"  {FAIL} {name}: {e}")
        traceback.print_exc()
        return False, None


def run_all_tests():
    """Run all module tests."""
    print("=" * 60)
    print("🧪 VIRAL RESEARCH ENGINE — INTEGRATION TESTS")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = {
        "test_run_at": datetime.now().isoformat(),
        "tests": {},
        "passed": 0,
        "failed": 0,
    }

    # ─── Test 1: Viral Pattern DB ───────────────────────────────
    print("\n📦 Module: viral_pattern_db")
    from viral_pattern_db import (
        initialize_db,
        get_top_patterns,
        get_best_format,
        get_posting_schedule,
    )

    ok, _ = test_module("initialize_db()", initialize_db)
    results["tests"]["viral_pattern_db_init"] = ok

    ok, patterns = test_module("get_top_patterns(limit=3)", get_top_patterns, limit=3)
    results["tests"]["viral_pattern_db_query"] = ok
    if patterns:
        print(f"     → {len(patterns)} patterns returned, top: {patterns[0]['name']}")

    ok, fmt = test_module("get_best_format('ai_tools')", get_best_format, "ai_tools")
    results["tests"]["viral_pattern_db_format"] = ok
    if fmt:
        print(f"     → Best format for ai_tools: {fmt['format']}")

    ok, sched = test_module(
        "get_posting_schedule('tiktok')", get_posting_schedule, "tiktok"
    )
    results["tests"]["viral_pattern_db_schedule"] = ok
    if sched:
        print(f"     → TikTok peak days: {', '.join(sched.get('peak_days', []))}")

    # ─── Test 2: Hashtag Analyzer ────────────────────────────────
    print("\n🏷️  Module: hashtag_analyzer")
    from hashtag_analyzer import (
        get_hashtag_recommendations,
        build_optimal_hashtag_set,
        save_hashtag_recommendations,
    )

    ok, recs = test_module(
        "get_hashtag_recommendations('ai_tools')",
        get_hashtag_recommendations,
        "ai_tools",
    )
    results["tests"]["hashtag_recommendations"] = ok
    if recs:
        print(f"     → {len(recs)} hashtags analyzed")
        print(
            f"     → Top hashtag: {recs[0]['hashtag']} (score: {recs[0]['relevance_score']})"
        )

    ok, opt = test_module(
        "build_optimal_hashtag_set('kuliner')", build_optimal_hashtag_set, "kuliner"
    )
    results["tests"]["hashtag_optimal_set"] = ok
    if opt:
        print(f"     → Optimal 10: {' '.join(opt['optimal_10'][:5])}...")

    ok, path = test_module(
        "save_hashtag_recommendations()", save_hashtag_recommendations
    )
    results["tests"]["hashtag_save"] = ok
    if path:
        print(f"     → Saved to: {path}")

    # ─── Test 3: Hook Generator ──────────────────────────────────
    print("\n🎣 Module: hook_generator")
    from hook_generator import (
        generate_hook,
        generate_full_content_brief,
        save_generated_hooks,
    )

    ok, hooks = test_module(
        "generate_hook('ai_tools', count=3)", generate_hook, "ai_tools", count=3
    )
    results["tests"]["hook_generator_basic"] = ok
    if hooks:
        print(f"     → {len(hooks)} hooks generated")
        print(
            f"     → Best hook [{hooks[0]['virality_score']}★]: {hooks[0]['hook'][:60]}..."
        )

    ok, brief = test_module(
        "generate_full_content_brief('side_hustle')",
        generate_full_content_brief,
        "side_hustle",
    )
    results["tests"]["hook_generator_brief"] = ok
    if brief:
        print(f"     → Brief format: {brief['format']}")

    ok, path = test_module("save_generated_hooks()", save_generated_hooks)
    results["tests"]["hook_generator_save"] = ok

    # ─── Test 4: Niche Researcher ────────────────────────────────
    print("\n🔬 Module: niche_researcher")
    from niche_researcher import research_niche, save_niche_research

    ok, niche_data = test_module("research_niche('kuliner')", research_niche, "kuliner")
    results["tests"]["niche_researcher_basic"] = ok
    if niche_data:
        print(f"     → {len(niche_data['trending_topics'])} trending topics")
        print(f"     → Quick win: {niche_data['quick_wins'][0]}")

    ok, path = test_module("save_niche_research()", save_niche_research)
    results["tests"]["niche_researcher_save"] = ok

    # ─── Test 5: Competitor Scraper ──────────────────────────────
    print("\n🕵️  Module: competitor_scraper")
    from competitor_scraper import analyze_niche_competitors, save_competitor_analysis

    ok, comp_data = test_module(
        "analyze_niche_competitors('digital_marketing')",
        analyze_niche_competitors,
        "digital_marketing",
    )
    results["tests"]["competitor_scraper_basic"] = ok
    if comp_data:
        benchmarks = comp_data.get("niche_benchmarks", {})
        print(
            f"     → Avg engagement: {benchmarks.get('avg_engagement_rate', 0)*100:.1f}%"
        )
        print(f"     → Common weakness: {comp_data['common_weaknesses'][0][:60]}")

    ok, path = test_module("save_competitor_analysis()", save_competitor_analysis)
    results["tests"]["competitor_scraper_save"] = ok

    # ─── Test 6: Content Gap Finder ──────────────────────────────
    print("\n🔍 Module: content_gap_finder")
    from content_gap_finder import get_quick_wins, save_content_gap_report

    ok, wins = test_module("get_quick_wins()", get_quick_wins)
    results["tests"]["content_gap_quick_wins"] = ok
    if wins:
        print(f"     → Top opportunity: {wins[0]['topic'][:60]}")
        print(f"     → Gap score: {wins[0]['gap_score']}")

    ok, path = test_module("save_content_gap_report()", save_content_gap_report)
    results["tests"]["content_gap_save"] = ok

    # ─── Summary ─────────────────────────────────────────────────
    total = len(results["tests"])
    passed = sum(1 for v in results["tests"].values() if v)
    failed = total - passed

    results["passed"] = passed
    results["failed"] = failed
    results["success_rate"] = f"{passed/total*100:.0f}%"

    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {passed}/{total} passed ({results['success_rate']})")

    if failed > 0:
        failed_tests = [k for k, v in results["tests"].items() if not v]
        print(f"   {FAIL} Failed: {', '.join(failed_tests)}")
    else:
        print(f"   {PASS} All tests passed!")

    print("=" * 60)

    # ─── Generate Full Research Report ───────────────────────────
    if passed >= total * 0.8:  # 80%+ pass rate
        print("\n📋 Generating full research report...")
        generate_full_report()

    return results


def generate_full_report():
    """Generate combined research report from all modules."""
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        from hashtag_analyzer import analyze_all_niches
        from hook_generator import batch_generate_hooks
        from niche_researcher import research_all_niches
        from competitor_scraper import full_competitor_analysis
        from content_gap_finder import generate_content_opportunities_report
        from viral_pattern_db import load_db

        report = {
            "report_type": "Full Viral Research Report",
            "generated_at": datetime.now().isoformat(),
            "market": "Indonesia",
            "sections": {
                "hashtag_analysis": analyze_all_niches(),
                "niche_research": research_all_niches(),
                "competitor_analysis": full_competitor_analysis(),
                "content_gaps": generate_content_opportunities_report(),
                "generated_hooks": batch_generate_hooks(hooks_per_niche=5),
                "viral_patterns": load_db(),
            },
            "executive_summary": {
                "top_niche_recommendation": "AI Tools for Business (highest growth + demand)",
                "top_content_format": "Controversy / STOP hooks (8-15% engagement rate)",
                "best_posting_times": ["07:00", "12:00", "19:00-21:00"],
                "top_hashtag_strategy": "Mix 2 mega + 4 macro + 4 mid = max reach",
                "quick_win_topics": [
                    "AI tools untuk UMKM Indonesia (gap score 7.1)",
                    "Side hustle income proof yang credible (gap score 8.3)",
                    "HPP kalkulator untuk bisnis kuliner (gap score 7.3)",
                ],
            },
        }

        filepath = output_dir / "full-research-report.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        size_kb = filepath.stat().st_size / 1024
        print(f"✅ Full report saved: {filepath} ({size_kb:.1f} KB)")

        # Print executive summary
        print("\n🎯 EXECUTIVE SUMMARY:")
        summary = report["executive_summary"]
        print(f"   Top niche: {summary['top_niche_recommendation']}")
        print(f"   Best format: {summary['top_content_format']}")
        print(f"   Best times: {', '.join(summary['best_posting_times'])}")
        print(f"\n   🏆 QUICK WIN TOPICS:")
        for topic in summary["quick_win_topics"]:
            print(f"      → {topic}")

        return str(filepath)

    except Exception as e:
        print(f"⚠️  Could not generate full report: {e}")
        return None


if __name__ == "__main__":
    results = run_all_tests()
    sys.exit(0 if results["failed"] == 0 else 1)
