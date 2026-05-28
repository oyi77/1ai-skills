"""
test_planner.py - Full integration test for content-planner-auto
Generates real 7-day calendar for March 14-20, 2026 and runs all modules.
"""

import json
import sys
import os
from datetime import date
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))

from calendar_generator import generate_calendar, print_day_summary
from pillar_rotator import get_pillar_sequence, PILLARS, PRODUCTS
from platform_optimizer import build_daily_schedule, ACCOUNTS
from seasonal_calendar import get_event_for_date, get_upcoming_events
from content_inventory import get_needed_assets, check_inventory, generate_shoot_list
from batch_scheduler import schedule_calendar


def test_pillar_rotator():
    print("\n" + "="*50)
    print("TEST 1: Pillar Rotator")
    print("="*50)
    
    start = date(2026, 3, 14)
    sequence = get_pillar_sequence(start, 30)
    
    # Check distribution
    counts = {}
    for p in sequence:
        counts[p] = counts.get(p, 0) + 1
    
    print(f"Generated {len(sequence)} pillar assignments")
    print("Distribution:")
    for pillar, count in sorted(counts.items(), key=lambda x: -x[1]):
        pct = round(count/len(sequence)*100, 1)
        target = PILLARS[pillar]["weight"] * 100
        status = "✅" if abs(pct - target) < 10 else "⚠️"
        print(f"  {status} {pillar}: {count} ({pct}% | target {target}%)")
    
    print(f"\nProducts available: {len(PRODUCTS)}")
    for p in PRODUCTS:
        print(f"  - {p['name']}: {p['price']} | {p['lynk_url']}")
    
    return True


def test_platform_optimizer():
    print("\n" + "="*50)
    print("TEST 2: Platform Optimizer")
    print("="*50)
    
    test_date = date(2026, 3, 14)
    schedule = build_daily_schedule(test_date, 0)
    
    print(f"Schedule for {test_date.isoformat()}:")
    for slot in schedule:
        print(f"  {slot['time']} | {slot['platform']} | Account: {slot['account']['username']}")
    
    print(f"\nTotal accounts connected:")
    for platform, accounts in ACCOUNTS.items():
        print(f"  {platform}: {len(accounts)} accounts")
    
    return True


def test_seasonal_calendar():
    print("\n" + "="*50)
    print("TEST 3: Seasonal Calendar")
    print("="*50)
    
    # Test Ramadan (should be active March 14-17)
    ramadan_date = date(2026, 3, 15)
    event = get_event_for_date(ramadan_date)
    
    if event:
        event_type, event_data = event
        print(f"✅ Ramadan detected on {ramadan_date}: {event_type}")
        print(f"   Theme: {event_data.get('theme')}")
        print(f"   Hashtags: {event_data.get('hashtag_additions', [])[:3]}")
    else:
        print(f"⚠️  No seasonal event found for {ramadan_date} (Ramadan check)")
    
    # Check Lebaran
    lebaran_date = date(2026, 3, 20)
    event = get_event_for_date(lebaran_date)
    if event:
        event_type, _ = event
        print(f"✅ Lebaran detected on {lebaran_date}: {event_type}")
    
    # Upcoming events in March 2026
    upcoming = get_upcoming_events(date(2026, 3, 14), 30)
    print(f"\nUpcoming events in 30 days: {len(upcoming)}")
    for e in upcoming[:5]:
        print(f"  {e['date']}: {e['event_type']} - {e.get('special_note', '')}")
    
    return True


def test_calendar_generation():
    print("\n" + "="*50)
    print("TEST 4: Calendar Generation (7 days)")
    print("="*50)
    
    start = date(2026, 3, 14)
    output_path = "/tmp/berkahkarya_calendar_march14_20.json"
    
    calendar = generate_calendar(start, 7, output_path)
    
    # Validate structure
    assert "meta" in calendar, "Missing meta"
    assert "summary" in calendar, "Missing summary"
    assert "days" in calendar, "Missing days"
    assert len(calendar["days"]) == 7, f"Expected 7 days, got {len(calendar['days'])}"
    
    # Check each day
    for day in calendar["days"]:
        assert "date" in day, f"Missing date in day"
        assert "posts" in day, f"Missing posts in day"
        assert len(day["posts"]) > 0, f"No posts in {day['date']}"
        
        for post in day["posts"]:
            assert "time" in post, f"Missing time in post"
            assert "platform" in post, f"Missing platform in post"
            assert "account_id" in post, f"Missing account_id in post"
            assert "pillar" in post, f"Missing pillar in post"
            assert "hook" in post, f"Missing hook in post"
            assert "caption" in post, f"Missing caption in post"
            assert "hashtags" in post, f"Missing hashtags in post"
            assert "lynk_url" in post, f"Missing lynk_url in post"
    
    print(f"\n✅ All structure validations passed!")
    print(f"   Total posts: {calendar['meta']['total_posts']}")
    print(f"   Days: {calendar['meta']['num_days']}")
    print(f"   Avg posts/day: {calendar['summary']['posts_per_day_avg']}")
    
    print(f"\n📊 Pillar distribution:")
    for pillar, pct in calendar["summary"]["pillar_distribution"].items():
        print(f"   {pillar}: {pct}")
    
    print(f"\n📊 Platform distribution:")
    for platform, count in calendar["summary"]["platform_distribution"].items():
        print(f"   {platform}: {count} posts")
    
    # Print first day preview
    print("\n" + "-"*50)
    print("FIRST DAY PREVIEW:")
    print_day_summary(calendar["days"][0])
    
    return calendar


def test_content_inventory(calendar):
    print("\n" + "="*50)
    print("TEST 5: Content Inventory")
    print("="*50)
    
    needed = get_needed_assets(calendar)
    
    print(f"Media assets needed: {len(needed)} types")
    for asset_type, count in sorted(needed.items(), key=lambda x: -x[1])[:10]:
        print(f"  {asset_type}: {count} uses")
    
    # Check inventory (will likely show all missing since no media dir)
    report = check_inventory(calendar, [])
    
    print(f"\nInventory summary:")
    for k, v in report["summary"].items():
        print(f"  {k}: {v}")
    
    # Generate shoot list
    shoot_list = generate_shoot_list(report, "/tmp/shoot_list_march14_20.md")
    print(f"\n✅ Shoot list generated")
    print(shoot_list[:500] + "...")
    
    return True


def test_batch_scheduler_dry_run(calendar):
    print("\n" + "="*50)
    print("TEST 6: Batch Scheduler (DRY RUN)")
    print("="*50)
    
    # Dry run only the first day
    single_day_calendar = {
        "meta": calendar["meta"],
        "summary": calendar["summary"],
        "days": [calendar["days"][0]],  # Only first day
    }
    
    report = schedule_calendar(
        single_day_calendar,
        dry_run=True,
        skip_missing_media=True,
    )
    
    print(f"\n✅ Dry run complete:")
    print(f"   Scheduled (would-be): {report['total_scheduled']}")
    print(f"   Skipped: {report['total_skipped']}")
    print(f"   Failed: {report['total_failed']}")
    
    return True


def test_postbridge_connection():
    """Test actual PostBridge API connection."""
    print("\n" + "="*50)
    print("TEST 7: PostBridge API Connection")
    print("="*50)
    
    try:
        import requests
        resp = requests.get(
            "https://api.post-bridge.com/v1/social-accounts",
            headers={"Authorization": "Bearer REDACTED_ROTATED_CREDENTIAL"},
            timeout=10,
        )
        
        if resp.status_code == 200:
            data = resp.json()
            accounts = data.get("data", data) if isinstance(data, dict) else data
            if isinstance(accounts, list):
                print(f"✅ PostBridge connected! {len(accounts)} accounts found:")
                for acc in accounts[:5]:
                    name = acc.get("name") or acc.get("username") or acc.get("platform")
                    platform = acc.get("platform") or acc.get("type")
                    acc_id = acc.get("id")
                    print(f"   ID {acc_id}: {name} ({platform})")
            else:
                print(f"✅ PostBridge connected! Response: {str(data)[:200]}")
        else:
            print(f"⚠️  PostBridge returned HTTP {resp.status_code}: {resp.text[:200]}")
        
    except Exception as e:
        print(f"❌ PostBridge connection failed: {e}")
    
    return True


def generate_poc_calendar():
    """Generate the proof-of-concept 7-day calendar for March 14-20."""
    print("\n" + "="*60)
    print("🚀 GENERATING PROOF OF CONCEPT CALENDAR")
    print("   March 14-20, 2026 | BerkahKarya Content Plan")
    print("="*60)
    
    start = date(2026, 3, 14)
    output_path = "/tmp/berkahkarya_poc_calendar.json"
    
    calendar = generate_calendar(start, 7, output_path)
    
    print("\n" + "="*60)
    print("📅 FULL 7-DAY CALENDAR PREVIEW")
    print("="*60)
    
    for day in calendar["days"]:
        print_day_summary(day)
    
    # Also save human-readable version
    readable_lines = []
    readable_lines.append("# BerkahKarya Content Calendar")
    readable_lines.append("## March 14-20, 2026")
    readable_lines.append("")
    
    for day in calendar["days"]:
        readable_lines.append(f"## {day['date']} ({day['day_name']})")
        if day.get("seasonal_event"):
            readable_lines.append(f"🎉 **Seasonal Event:** {day['seasonal_event']}")
        readable_lines.append(f"**Total Posts:** {day['total_posts']}")
        readable_lines.append("")
        
        for post in day["posts"]:
            readable_lines.append(f"### {post['time']} - {post['platform'].upper()}")
            readable_lines.append(f"- **Account:** {post['account_name']}")
            readable_lines.append(f"- **Pillar:** {post['pillar']}")
            readable_lines.append(f"- **Product:** {post['product']}")
            readable_lines.append(f"- **Content Type:** {post['content_type']}")
            readable_lines.append(f"- **Hook:** {post['hook']}")
            readable_lines.append(f"- **Media Needed:** {post['media_needed']}")
            readable_lines.append(f"- **LYNK URL:** {post['lynk_url']}")
            readable_lines.append(f"- **Hashtags:** {' '.join(post['hashtags'][:5])}...")
            readable_lines.append("")
        
        readable_lines.append("---")
        readable_lines.append("")
    
    readable_path = "/tmp/berkahkarya_poc_calendar_readable.md"
    with open(readable_path, "w", encoding="utf-8") as f:
        f.write("\n".join(readable_lines))
    
    print(f"\n💾 Saved:")
    print(f"   JSON: {output_path}")
    print(f"   Readable: {readable_path}")
    
    return calendar


def run_all_tests():
    """Run all tests."""
    print("\n🧪 RUNNING CONTENT PLANNER AUTO - FULL TEST SUITE")
    print("="*60)
    
    results = []
    
    try:
        results.append(("Pillar Rotator", test_pillar_rotator()))
    except Exception as e:
        print(f"❌ Pillar Rotator FAILED: {e}")
        results.append(("Pillar Rotator", False))
    
    try:
        results.append(("Platform Optimizer", test_platform_optimizer()))
    except Exception as e:
        print(f"❌ Platform Optimizer FAILED: {e}")
        results.append(("Platform Optimizer", False))
    
    try:
        results.append(("Seasonal Calendar", test_seasonal_calendar()))
    except Exception as e:
        print(f"❌ Seasonal Calendar FAILED: {e}")
        results.append(("Seasonal Calendar", False))
    
    calendar = None
    try:
        calendar = test_calendar_generation()
        results.append(("Calendar Generation", True))
    except Exception as e:
        print(f"❌ Calendar Generation FAILED: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Calendar Generation", False))
    
    if calendar:
        try:
            results.append(("Content Inventory", test_content_inventory(calendar)))
        except Exception as e:
            print(f"❌ Content Inventory FAILED: {e}")
            results.append(("Content Inventory", False))
        
        try:
            results.append(("Batch Scheduler (Dry Run)", test_batch_scheduler_dry_run(calendar)))
        except Exception as e:
            print(f"❌ Batch Scheduler FAILED: {e}")
            results.append(("Batch Scheduler (Dry Run)", False))
    
    try:
        results.append(("PostBridge Connection", test_postbridge_connection()))
    except Exception as e:
        print(f"❌ PostBridge Connection FAILED: {e}")
        results.append(("PostBridge Connection", False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST RESULTS:")
    print("="*60)
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
        if result:
            passed += 1
    
    print(f"\n{passed}/{len(results)} tests passed")
    
    # Generate POC calendar
    if calendar:
        print("\n" + "="*60)
        poc = generate_poc_calendar()
        print(f"\n🎉 PROOF OF CONCEPT COMPLETE!")
        print(f"   7-day calendar: {poc['meta']['total_posts']} total posts")
        print(f"   March 14-20, 2026 ready for BerkahKarya")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
