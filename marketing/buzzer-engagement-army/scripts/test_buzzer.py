"""
Test Suite — validates all buzzer-engagement-army components.
Run this to verify the system works before production deployment.

Usage:
  cd scripts/
  python test_buzzer.py
  python test_buzzer.py --fast   # Skip slow tests
  python test_buzzer.py --api    # Include real API calls
"""

import sys
import os
import json
import argparse
import traceback
from pathlib import Path
from datetime import datetime

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

PASS = "✅"
FAIL = "❌"
SKIP = "⏭️"
WARN = "⚠️"


def test(name: str, fn, *args, **kwargs):
    """Run a single test and report result."""
    try:
        result = fn(*args, **kwargs)
        print(f"  {PASS} {name}")
        return True, result
    except Exception as e:
        print(f"  {FAIL} {name}: {e}")
        if os.environ.get("DEBUG"):
            traceback.print_exc()
        return False, None


results = {"passed": 0, "failed": 0, "skipped": 0}


def run_test(name, fn, *args, **kwargs):
    ok, val = test(name, fn, *args, **kwargs)
    if ok:
        results["passed"] += 1
    else:
        results["failed"] += 1
    return ok, val


# ============================================================
# TEST: Comment Library
# ============================================================
def test_comment_library():
    print("\n[1] Comment Library")
    from comment_library import (
        get_comment,
        detect_niche,
        get_comments_for_post,
        count_comments,
        COMMENTS,
    )

    def check_niches():
        counts = count_comments()
        total = sum(counts.values())
        assert total >= 150, f"Expected 150+ comments, got {total}"
        return counts

    def check_niche_detection():
        assert detect_niche("tips kesehatan harian") == "health"
        assert detect_niche("review AI tools terbaru") == "tech"
        assert detect_niche("resep masak nasi goreng") == "food"
        assert detect_niche("ootd fashion style") == "fashion"
        assert detect_niche("cara scale bisnis online") == "business"
        assert detect_niche("random content") == "general"
        return True

    def check_unique_comments():
        comments = get_comments_for_post("tips kesehatan harian", count=5)
        assert len(comments) == 5, f"Expected 5 comments, got {len(comments)}"
        assert len(set(comments)) == 5, "Comments should be unique"
        return comments

    def check_all_niches_have_comments():
        for niche in COMMENTS:
            c = get_comment(niche)
            assert c, f"Empty comment for niche: {niche}"
        return True

    run_test("Comment counts (150+ total)", check_niches)
    run_test("Niche detection", check_niche_detection)
    run_test("Unique comments per post", check_unique_comments)
    run_test("All niches have comments", check_all_niches_have_comments)


# ============================================================
# TEST: Account Manager
# ============================================================
def test_account_manager():
    print("\n[2] Account Manager")
    from account_manager import (
        KNOWN_ACCOUNTS,
        get_account_warmup_level,
        get_actions_today,
        can_act,
        get_account_status_report,
    )

    def check_known_accounts():
        assert len(KNOWN_ACCOUNTS["tiktok"]) == 7
        assert len(KNOWN_ACCOUNTS["instagram"]) == 1
        assert len(KNOWN_ACCOUNTS["facebook"]) == 4
        return KNOWN_ACCOUNTS

    def check_warmup_levels():
        # Test with a known ID
        level = get_account_warmup_level(48374)
        assert level in [5, 15, 30], f"Invalid warmup level: {level}"
        return level

    def check_can_act():
        result = can_act(48374)
        assert isinstance(result, bool)
        return result

    def check_status_report():
        report = get_account_status_report()
        assert "tiktok" in report
        assert "instagram" in report
        assert "facebook" in report
        assert len(report["tiktok"]) == 7
        return report

    run_test("Known accounts (7 TT, 1 IG, 4 FB)", check_known_accounts)
    run_test("Warmup level returns 5/15/30", check_warmup_levels)
    run_test("can_act returns bool", check_can_act)
    run_test("Status report structure", check_status_report)


# ============================================================
# TEST: Warmup Manager
# ============================================================
def test_warmup_manager():
    print("\n[3] Warmup Manager")
    from warmup_manager import (
        get_warmup_phase,
        days_active,
        get_safe_accounts,
        register_new_account,
        get_all_account_warmup_status,
    )

    def check_warmup_phase():
        phase = get_warmup_phase(48374)
        assert phase in ["COLD (Day 1-3)", "WARMING (Day 4-7)", "ACTIVE (Day 8+)"]
        return phase

    def check_days_active():
        d = days_active(48374)
        assert isinstance(d, int)
        assert d >= 0
        return d

    def check_safe_accounts():
        safe = get_safe_accounts(min_remaining=0)  # min 0 = all accounts
        assert isinstance(safe, list)
        return len(safe)

    def check_all_status():
        statuses = get_all_account_warmup_status()
        assert len(statuses) == 12  # 7 TT + 1 IG + 4 FB
        for s in statuses:
            assert "platform" in s
            assert "id" in s
            assert "daily_limit" in s
        return len(statuses)

    run_test("Warmup phase labels", check_warmup_phase)
    run_test("Days active >= 0", check_days_active)
    run_test("Safe accounts list", check_safe_accounts)
    run_test("All 12 accounts in status", check_all_status)


# ============================================================
# TEST: Engagement Scheduler
# ============================================================
def test_engagement_scheduler():
    print("\n[4] Engagement Scheduler")
    from engagement_scheduler import (
        random_delay,
        generate_engagement_schedule,
        print_schedule,
    )

    def check_random_delay():
        for _ in range(10):
            d = random_delay(120, 300)
            assert 120 <= d <= 300, f"Delay {d} out of range"
        return True

    def check_schedule_generation():
        ids = [48374, 48373, 48372]
        schedule = generate_engagement_schedule(ids, actions=["like", "comment"])
        assert len(schedule) == 6  # 3 accounts × 2 actions
        for item in schedule:
            assert "account_id" in item
            assert "action" in item
            assert "scheduled_at" in item
        return schedule

    def check_schedule_staggering():
        ids = [48374, 48373]
        schedule = generate_engagement_schedule(ids, actions=["like"])
        times = [item["delay_from_start_sec"] for item in schedule]
        # Accounts should be at different times
        assert times[0] != times[1], "Accounts should be staggered"
        return times

    def check_all_7_tiktok():
        ids = [48374, 48373, 48372, 48338, 48337, 48336, 48335]
        schedule = generate_engagement_schedule(ids, actions=["like", "comment"])
        assert len(schedule) == 14  # 7 × 2
        return len(schedule)

    run_test("Random delay in range", check_random_delay)
    run_test("Schedule generation (3 accs × 2 actions = 6)", check_schedule_generation)
    run_test("Schedule staggering (different times)", check_schedule_staggering)
    run_test("All 7 TikTok accounts scheduled", check_all_7_tiktok)


# ============================================================
# TEST: Like Bot (dry run)
# ============================================================
def test_like_bot():
    print("\n[5] Like Bot (dry run)")
    from like_bot import simulate_like, run_like_campaign

    def check_simulate_like():
        result = simulate_like(
            48374, "https://tiktok.com/@test/123", "tiktok", dry_run=True
        )
        assert result == True
        return result

    def check_campaign_dry_run():
        result = run_like_campaign(
            account_ids=[48374, 48373, 48372],
            post_url="https://tiktok.com/@test/123",
            platform="tiktok",
            delay_range=(0, 0.1),  # No delay in test
            dry_run=True,
        )
        assert "success" in result
        assert "failed" in result
        assert "skipped" in result
        return result

    run_test("simulate_like dry run", check_simulate_like)
    run_test("Campaign dry run returns counts", check_campaign_dry_run)


# ============================================================
# TEST: Comment Bot (dry run)
# ============================================================
def test_comment_bot():
    print("\n[6] Comment Bot (dry run)")
    from comment_bot import post_comment_via_api, run_comment_campaign

    def check_post_comment():
        result = post_comment_via_api(
            48374, "test_post_001", "tiktok", "Test comment!", dry_run=True
        )
        assert result == True
        return result

    def check_comment_campaign():
        result = run_comment_campaign(
            account_ids=[48374, 48373],
            post_id="test_post_001",
            post_caption="tips kesehatan harian",
            platform="tiktok",
            delay_range=(0, 0.1),
            dry_run=True,
        )
        assert "success" in result
        assert "comments" in result
        # Each successful comment should have unique text
        comment_texts = [c["comment"] for c in result["comments"]]
        assert len(set(comment_texts)) == len(
            comment_texts
        ), "Duplicate comments detected!"
        return result

    run_test("post_comment_via_api dry run", check_post_comment)
    run_test("Comment campaign unique comments", check_comment_campaign)


# ============================================================
# TEST: PostBridge API connectivity
# ============================================================
def test_api_connectivity(skip=False):
    print("\n[7] PostBridge API Connectivity")
    if skip:
        print(f"  {SKIP} Skipped (use --api to enable)")
        results["skipped"] += 3
        return

    import requests

    POSTBRIDGE_KEY = "REDACTED_ROTATED_CREDENTIAL"
    HEADERS = {"Authorization": f"Bearer {POSTBRIDGE_KEY}"}
    BASE = "https://api.post-bridge.com/v1"

    def check_social_accounts():
        resp = requests.get(f"{BASE}/social-accounts", headers=HEADERS, timeout=10)
        assert resp.status_code == 200, f"Status {resp.status_code}"
        data = resp.json()
        accounts = data if isinstance(data, list) else data.get("data", [])
        return len(accounts)

    def check_posts():
        resp = requests.get(
            f"{BASE}/posts", headers=HEADERS, params={"limit": 5}, timeout=10
        )
        assert resp.status_code == 200, f"Status {resp.status_code}"
        data = resp.json()
        posts = data if isinstance(data, list) else data.get("data", [])
        return len(posts)

    def check_post_results():
        resp = requests.get(
            f"{BASE}/post-results", headers=HEADERS, params={"limit": 5}, timeout=10
        )
        assert resp.status_code == 200, f"Status {resp.status_code}"
        return True

    run_test("GET /social-accounts", check_social_accounts)
    run_test("GET /posts", check_posts)
    run_test("GET /post-results", check_post_results)


# ============================================================
# TEST: Integration — coordinator dry run
# ============================================================
def test_coordinator():
    print("\n[8] Engagement Coordinator (dry run)")

    def check_coordinator_import():
        from engagement_coordinator import ACCOUNTS, fetch_posts, select_posts_for_boost

        assert len(ACCOUNTS["tiktok"]) == 7
        return True

    def check_post_selection():
        from engagement_coordinator import fetch_posts

        posts = fetch_posts(limit=3)
        assert isinstance(posts, list)
        return len(posts)

    run_test("Coordinator imports", check_coordinator_import)
    run_test("Post fetching returns list", check_post_selection)


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Buzzer Engagement Army Test Suite")
    parser.add_argument("--api", action="store_true", help="Include real API calls")
    parser.add_argument("--fast", action="store_true", help="Skip slow tests")
    args = parser.parse_args()

    print("=" * 60)
    print("  BUZZER ENGAGEMENT ARMY — TEST SUITE")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    test_comment_library()
    test_account_manager()
    test_warmup_manager()
    test_engagement_scheduler()
    test_like_bot()
    test_comment_bot()
    test_api_connectivity(skip=not args.api)
    test_coordinator()

    # Summary
    total = results["passed"] + results["failed"]
    print("\n" + "=" * 60)
    print(
        f"  RESULTS: {results['passed']}/{total} passed | "
        f"{results['failed']} failed | {results['skipped']} skipped"
    )

    if results["failed"] == 0:
        print(f"  {PASS} ALL TESTS PASSED — System ready for production!")
    else:
        print(f"  {FAIL} {results['failed']} test(s) failed — fix before production")
    print("=" * 60)

    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
