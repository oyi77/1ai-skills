"""
test_analytics.py — Integration tests with real PostBridge data
Tests all analytics modules end-to-end
"""

import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))


class TestAnalyticsCollector(unittest.TestCase):
    """Test data collection from PostBridge API."""

    def test_fetch_analytics_real(self):
        """Test real API call to analytics endpoint."""
        from analytics_collector import fetch_analytics

        data = fetch_analytics()
        self.assertIsInstance(data, list)
        print(f"  ✓ Analytics: {len(data)} records")

    def test_fetch_posts_real(self):
        """Test real API call to posts endpoint."""
        from analytics_collector import fetch_posts

        data = fetch_posts()
        self.assertIsInstance(data, list)
        print(f"  ✓ Posts: {len(data)} records")

    def test_fetch_post_results_real(self):
        """Test real API call to post-results endpoint."""
        from analytics_collector import fetch_post_results

        data = fetch_post_results()
        self.assertIsInstance(data, list)
        print(f"  ✓ Post results: {len(data)} records")

    def test_fetch_social_accounts_real(self):
        """Test real API call to social accounts endpoint."""
        from analytics_collector import fetch_social_accounts

        data = fetch_social_accounts()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        print(f"  ✓ Social accounts: {len(data)} accounts")

    def test_collect_all(self):
        """Test full data collection."""
        from analytics_collector import collect_all

        data = collect_all(use_cache=False)
        self.assertIn("analytics", data)
        self.assertIn("posts", data)
        self.assertIn("post_results", data)
        self.assertIn("social_accounts", data)
        self.assertIn("collected_at", data)
        print(
            f"  ✓ Full dataset: {sum(len(v) for v in [data['analytics'], data['posts'], data['post_results'], data['social_accounts']])} total records"
        )

    def test_build_lookup_maps(self):
        """Test lookup map construction."""
        from analytics_collector import collect_all, build_lookup_maps

        data = collect_all(use_cache=True)
        maps = build_lookup_maps(data)
        self.assertIn("post_by_id", maps)
        self.assertIn("account_by_id", maps)
        self.assertIn("results_by_post_id", maps)
        self.assertIn("analytics_by_result_id", maps)
        print(f"  ✓ Lookup maps built successfully")


class TestPerformanceAnalyzer(unittest.TestCase):
    """Test performance analysis functions."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_engagement_rate(self):
        from performance_analyzer import compute_engagement_rate

        er = compute_engagement_rate(
            {"view_count": 100, "like_count": 3, "comment_count": 0, "share_count": 0}
        )
        self.assertEqual(er, 3.0)

        er_zero = compute_engagement_rate({"view_count": 0, "like_count": 0})
        self.assertEqual(er_zero, 0.0)
        print("  ✓ Engagement rate calculation correct")

    def test_detect_content_type(self):
        from performance_analyzer import detect_content_type

        t = detect_content_type("Belanja tetap jalan tapi duit balik lagi cashback")
        self.assertEqual(t, "cashback")
        t2 = detect_content_type("Tips cara hemat belanja online")
        self.assertIn(t2, ["tutorial", "cashback", "viral_hook", "unknown"])
        print("  ✓ Content type detection working")

    def test_platform_summary(self):
        from performance_analyzer import platform_summary

        result = platform_summary(self.data["analytics"])
        self.assertIsInstance(result, dict)
        for p, d in result.items():
            self.assertIn("views", d)
            self.assertIn("posts", d)
            self.assertIn("avg_engagement_rate", d)
        print(f"  ✓ Platform summary: {list(result.keys())}")

    def test_full_analysis(self):
        from performance_analyzer import full_analysis

        result = full_analysis(self.data)
        self.assertIn("summary", result)
        self.assertIn("platform_breakdown", result)
        self.assertGreaterEqual(result["summary"]["total_views"], 0)
        print(f"  ✓ Full analysis: {result['summary']['total_views']} total views")


class TestTrendDetector(unittest.TestCase):
    """Test trend detection functions."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_group_by_date(self):
        from trend_detector import group_by_date

        daily = group_by_date(self.data["analytics"])
        self.assertIsInstance(daily, dict)
        for date, metrics in daily.items():
            self.assertIn("views", metrics)
            self.assertIn("posts", metrics)
        print(f"  ✓ Daily grouping: {len(daily)} days")

    def test_best_posting_times(self):
        from trend_detector import best_posting_times

        timing = best_posting_times(self.data["analytics"])
        self.assertIn("best_hours", timing)
        self.assertIn("best_days", timing)
        print(f"  ✓ Best times detected")

    def test_weekly_trend(self):
        from trend_detector import weekly_trend_report

        trend = weekly_trend_report(self.data["analytics"])
        self.assertIn("growth_analysis", trend)
        self.assertIn("trend", trend["growth_analysis"])
        self.assertIn(
            trend["growth_analysis"]["trend"],
            ["growing", "declining", "stable", "insufficient_data"],
        )
        print(f"  ✓ Trend: {trend['growth_analysis']['trend']}")


class TestFunnelAnalyzer(unittest.TestCase):
    """Test funnel analysis."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_compute_funnel(self):
        from funnel_analyzer import compute_funnel

        funnel = compute_funnel(self.data["analytics"])
        self.assertIn("funnel_stages", funnel)
        self.assertIn("conversion_rates", funnel)
        self.assertIn("bottleneck", funnel)
        stages = list(funnel["funnel_stages"].keys())
        self.assertGreaterEqual(len(stages), 4)
        print(f"  ✓ Funnel: {len(stages)} stages, bottleneck={funnel['bottleneck']}")

    def test_platform_funnel(self):
        from funnel_analyzer import platform_funnel_breakdown

        pf = platform_funnel_breakdown(self.data["analytics"])
        self.assertIsInstance(pf, dict)
        print(f"  ✓ Platform funnel breakdown: {list(pf.keys())}")


class TestROICalculator(unittest.TestCase):
    """Test ROI calculations."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_compute_roi(self):
        from roi_calculator import compute_roi

        roi = compute_roi(self.data["analytics"], self.data["posts"])
        self.assertIn("status", roi)
        self.assertIn("investment", roi)
        self.assertIn("break_even", roi)
        self.assertGreater(roi["investment"]["total_cost_idr"], 0)
        print(f"  ✓ ROI computed: {roi['status']}")
        print(f"    Cost: IDR {roi['investment']['total_cost_idr']:,}")
        print(f"    Break-even: {roi['break_even']['sales_needed']} sales")


class TestOptimizationEngine(unittest.TestCase):
    """Test optimization recommendations."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_recommendations(self):
        from optimization_engine import generate_content_recommendations

        recs = generate_content_recommendations(
            self.data["analytics"], self.data["posts"]
        )
        self.assertIsInstance(recs, list)
        self.assertGreater(len(recs), 0)
        # Should have at least one CRITICAL recommendation given 0 sales
        priorities = [r["priority"] for r in recs]
        self.assertIn("CRITICAL", priorities)
        print(
            f"  ✓ {len(recs)} recommendations, {priorities.count('CRITICAL')} CRITICAL"
        )

    def test_full_optimization(self):
        from optimization_engine import full_optimization_report

        report = full_optimization_report(self.data)
        self.assertIn("platform_rankings", report)
        self.assertIn("recommendations", report)
        self.assertIn("action_plan", report)
        print(f"  ✓ Full optimization report generated")


class TestABTracker(unittest.TestCase):
    """Test A/B test tracking."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_auto_tests(self):
        from ab_test_tracker import run_all_auto_tests

        tests = run_all_auto_tests(self.data["analytics"])
        self.assertIn("hook_test", tests)
        self.assertIn("platform_test", tests)
        self.assertIn("length_test", tests)
        print(f"  ✓ Hook winner: {tests['hook_test']['winner']}")
        print(f"  ✓ Platform winner: {tests['platform_test']['winner']}")


class TestReportGenerator(unittest.TestCase):
    """Test report generation."""

    def setUp(self):
        from analytics_collector import collect_all

        self.data = collect_all(use_cache=True)

    def test_generate_daily_report(self):
        from report_generator import generate_daily_report

        report = generate_daily_report(self.data)
        self.assertIn("BerkahKarya", report)
        self.assertIn("Platform Breakdown", report)
        self.assertIn("Funnel Analysis", report)
        self.assertIn("Action Items", report)
        print(f"  ✓ Daily report: {len(report)} chars")

    def test_generate_all_reports(self):
        from report_generator import generate_all_reports

        paths = generate_all_reports(self.data)
        self.assertIn("daily_md", paths)
        self.assertIn("weekly_md", paths)
        self.assertIn("json", paths)
        # Check files exist
        for key, path in paths.items():
            if key != "date":
                self.assertTrue(Path(path).exists(), f"Missing: {path}")
                print(f"  ✓ {key}: {path}")


def run_full_suite(verbose: bool = True) -> dict:
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestAnalyticsCollector,
        TestPerformanceAnalyzer,
        TestTrendDetector,
        TestFunnelAnalyzer,
        TestROICalculator,
        TestOptimizationEngine,
        TestABTracker,
        TestReportGenerator,
    ]

    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return {
        "total": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "success": result.wasSuccessful(),
    }


if __name__ == "__main__":
    print("🧪 Running Content Analytics Engine Test Suite")
    print("=" * 60)
    results = run_full_suite(verbose=True)
    print("=" * 60)
    print(f"\n{'✅ ALL PASSED' if results['success'] else '❌ SOME FAILED'}")
    print(
        f"Total: {results['total']} | Passed: {results['passed']} | Failed: {results['failed']} | Errors: {results['errors']}"
    )
