"""
test_comment_manager.py — Full integration tests
Run: python3 test_comment_manager.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
from datetime import datetime

# ─── TEST RUNNERS ──────────────────────────────────────────────────────────────

def test_sentiment_analyzer():
    print("\n" + "="*60)
    print("TEST: Sentiment Analyzer")
    print("="*60)

    from sentiment_analyzer import analyze_sentiment

    test_cases = [
        # (comment, expected_category)
        ("Kak harganya berapa?", "price_ask"),
        ("Mau dong, gimana cara belinya?", "interest"),
        ("Ini bisa buat apa ya?", "question"),
        ("Bagus banget kontennya 🔥", "positive"),
        ("Scam! Penipuan!", "negative"),
        ("Follow back dong hehe", "spam"),
        ("Halo kak", "neutral"),
        ("Pengen beli TikTok affiliate class", "interest"),
        ("Harganya worth it ga?", "price_ask"),
    ]

    passed = 0
    failed = 0
    for comment, expected in test_cases:
        result = analyze_sentiment(comment)
        status = "✅" if result.category == expected else "❌"
        if result.category == expected:
            passed += 1
        else:
            failed += 1
        print(f"  {status} [{result.category:12s}] conf={result.confidence:.2f} dm={result.is_dm_trigger} | '{comment}'")
        if result.category != expected:
            print(f"       Expected: {expected}")

    print(f"\n  Result: {passed}/{len(test_cases)} passed")
    return passed, failed


def test_faq_responder():
    print("\n" + "="*60)
    print("TEST: FAQ Responder")
    print("="*60)

    from faq_responder import find_faq_response

    test_cases = [
        ("Kak harganya berapa?", True),
        ("Bisa refund ga?", True),
        ("Cara belinya gimana?", True),
        ("Ini scam ga?", True),
        ("Ada promo ga kak?", True),
        ("Random totally unrelated comment xyz", False),
        ("Udah beli nih mantap!", True),
        ("Gimana cara pakainya?", True),
    ]

    passed = 0
    for comment, expect_match in test_cases:
        response = find_faq_response(comment)
        got_match = response is not None
        status = "✅" if got_match == expect_match else "❌"
        if got_match == expect_match:
            passed += 1
        print(f"  {status} Match={got_match} | '{comment}'")
        if response:
            print(f"       → {response[:70]}...")

    print(f"\n  Result: {passed}/{len(test_cases)} passed")
    return passed, len(test_cases) - passed


def test_comment_templates():
    print("\n" + "="*60)
    print("TEST: Comment Templates")
    print("="*60)

    from comment_templates import (
        get_positive_reply, get_question_reply, get_interest_reply,
        get_negative_reply, get_price_reply, get_dm_public_reply,
        get_dm_message, find_product_by_keywords, PRODUCTS,
    )

    passed = 0
    tests = 0

    # Test product matching
    matches = [
        ("cara cari kerja pakai AI", "jobmagnet_ai"),
        ("TikTok affiliate income", "kelas_affiliate_tiktok"),
        ("menu restoran kuliner", "food_menu_ai_studio"),
        ("shopee marketplace jualan online", "studio_marketplace_pro"),
        ("cashback belanja gratis", "belanja_duit_balik"),
    ]

    for query, expected_key in matches:
        tests += 1
        product = find_product_by_keywords(query)
        expected_product = PRODUCTS[expected_key]
        if product["name"] == expected_product["name"]:
            passed += 1
            print(f"  ✅ '{query}' → {product['name']}")
        else:
            print(f"  ❌ '{query}' → {product['name']} (expected: {expected_product['name']})")

    # Test template generation (no crash)
    tests += 1
    try:
        sample_product = PRODUCTS["ai_creative_tools"]
        replies = [
            get_positive_reply(),
            get_question_reply(sample_product),
            get_interest_reply(),
            get_negative_reply(),
            get_price_reply(sample_product),
            get_dm_public_reply(),
            get_dm_message(sample_product),
        ]
        for r in replies:
            assert len(r) > 10, f"Reply too short: {r}"
        passed += 1
        print(f"  ✅ All template types generate valid responses")
    except Exception as e:
        print(f"  ❌ Template generation error: {e}")

    print(f"\n  Result: {passed}/{tests} passed")
    return passed, tests - passed


def test_auto_replier():
    print("\n" + "="*60)
    print("TEST: Auto Replier (Decision Engine)")
    print("="*60)

    from auto_replier import decide_reply, process_comments

    test_comments = [
        {"id": "t1", "platform": "tiktok", "username": "buyer_a", "text": "Harganya berapa kak?", "post_caption": "AI Tools"},
        {"id": "t2", "platform": "tiktok", "username": "fan_b", "text": "Keren banget! 🔥", "post_caption": ""},
        {"id": "t3", "platform": "instagram", "username": "curious_c", "text": "Mau beli dong, cara ordernya?", "post_caption": "JobMagnet"},
        {"id": "t4", "platform": "tiktok", "username": "hater_d", "text": "Produk sampah!", "post_caption": ""},
        {"id": "t5", "platform": "tiktok", "username": "spammer_e", "text": "Follow back ya!", "post_caption": ""},
        {"id": "t6", "platform": "tiktok", "username": "asker_f", "text": "Ini bisa buat apa ya?", "post_caption": "Studio"},
    ]

    expected_dms = {"t1", "t3"}  # Price ask and interest should trigger DM
    expected_skip_spam = {"t5"}

    passed = 0
    total = len(test_comments)

    for comment in test_comments:
        decision = decide_reply(comment)
        cid = comment["id"]
        print(f"\n  Comment [{cid}]: '{comment['text']}'")
        print(f"  Reply:          '{decision.reply_text[:70]}'")
        print(f"  DM trigger:     {decision.should_dm}")

        # Basic validation
        is_spam_comment = cid in expected_skip_spam
        if is_spam_comment and "[SKIP" in decision.reply_text:
            passed += 1  # correctly skipped spam
        elif not is_spam_comment and "[SKIP" not in decision.reply_text and len(decision.reply_text) > 10:
            passed += 1  # valid reply
        elif not is_spam_comment and "[SKIP" in decision.reply_text:
            print(f"  ❌ Non-spam comment incorrectly skipped")

    print(f"\n  Valid decisions: {passed}/{total}")

    # Test stats from process_comments
    stats = process_comments(test_comments, dry_run=True)
    print(f"\n  Process stats: {stats}")

    return passed, total - passed


def test_dm_funnel():
    print("\n" + "="*60)
    print("TEST: DM Funnel")
    print("="*60)

    # Reset state for clean test
    import dm_funnel as _dmf
    _dmf.save_dm_cooldowns({})

    from dm_funnel import build_dm_content, process_dm_funnel, PRODUCTS

    # Test DM content building
    dm_data = build_dm_content(
        "test_user",
        "Mau beli dong, buat cari kerja",
        "JobMagnet AI"
    )
    assert dm_data["product"] == "JobMagnet Ai", f"Wrong product: {dm_data['product']}"
    assert "lynk.id" in dm_data["message"], "No LYNK URL in DM"
    assert len(dm_data["message"]) > 50, "DM too short"
    print(f"  ✅ DM content built: product={dm_data['product']}")
    print(f"     URL in message: {'lynk.id' in dm_data['message']}")
    print(f"     Message preview: {dm_data['message'][:80]}...")

    # Test full funnel (dry run)
    candidates = [
        {"username": "buyer1", "platform": "tiktok", "comment_text": "Mau beli!", "post_caption": "AI Tools", "post_url": ""},
        {"username": "buyer2", "platform": "instagram", "comment_text": "Harganya berapa?", "post_caption": "", "post_url": ""},
        {"username": "buyer1", "platform": "tiktok", "comment_text": "Still want to buy", "post_caption": "", "post_url": ""},  # cooldown
    ]

    stats = process_dm_funnel(candidates, dry_run=True)
    print(f"\n  DM funnel stats: {stats}")

    assert stats["total_candidates"] == 3
    assert stats["skipped_cooldown"] == 1  # buyer1 is duplicated
    print(f"  ✅ Cooldown detection working: {stats['skipped_cooldown']} skipped")

    return 2, 0


def test_postbridge_connection():
    print("\n" + "="*60)
    print("TEST: PostBridge API Connection")
    print("="*60)

    from comment_monitor import fetch_posts, fetch_post_results

    try:
        posts = fetch_posts(limit=5)
        print(f"  ✅ Posts API: returned {len(posts)} posts")

        results = fetch_post_results(limit=5)
        print(f"  ✅ Post results API: returned {len(results)} results")

        if results:
            first = results[0]
            print(f"     Sample result keys: {list(first.keys())[:8]}")

        return 1, 0
    except Exception as e:
        print(f"  ❌ PostBridge connection failed: {e}")
        return 0, 1


# ─── RUN ALL TESTS ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "🔥"*20)
    print("COMMENT-REPLY-MANAGER — Full Test Suite")
    print("🔥"*20)

    total_passed = 0
    total_failed = 0

    tests = [
        ("Sentiment Analyzer", test_sentiment_analyzer),
        ("FAQ Responder", test_faq_responder),
        ("Comment Templates", test_comment_templates),
        ("Auto Replier", test_auto_replier),
        ("DM Funnel", test_dm_funnel),
        ("PostBridge API", test_postbridge_connection),
    ]

    results = []
    for name, fn in tests:
        try:
            p, f = fn()
            total_passed += p
            total_failed += f
            results.append((name, p, f, "✅" if f == 0 else "⚠️"))
        except Exception as e:
            print(f"  ❌ TEST CRASHED: {e}")
            import traceback
            traceback.print_exc()
            total_failed += 1
            results.append((name, 0, 1, "❌"))

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, p, f, status in results:
        print(f"  {status} {name}: {p} passed, {f} failed")
    print(f"\n  TOTAL: {total_passed} passed, {total_failed} failed")
    print("="*60)

    if total_failed == 0:
        print("\n✅ ALL TESTS PASSED — Production ready!")
    else:
        print(f"\n⚠️  {total_failed} failures — review above")

    sys.exit(0 if total_failed == 0 else 1)
