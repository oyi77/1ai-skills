#!/usr/bin/env python3
"""
PostBridge Monitor & Auto-Scaler
- Monitors post results (success/fail rates)
- Triggers analytics sync
- Auto-scales: if success rate > 80%, increase posting frequency
- Alerts on failures
- Runs via cron every 2 hours
"""
import requests, json, time, os
from datetime import datetime, timedelta

API = "https://api.post-bridge.com/v1"

# ================================================================
# PostBridge API Quick Reference (from official spec)
# POST /v1/posts required: caption, social_accounts
# Optional: media (IDs), media_urls (public URLs), scheduled_at,
#           platform_configurations, account_configurations,
#           use_queue, processing_enabled, is_draft
#
# platform_configurations per platform:
#   youtube:   caption, media, title
#   tiktok:    caption, media, title, video_cover_timestamp_ms, draft, is_aigc
#   instagram: caption, media, cover_image, placement, is_trial_reel
#   facebook:  caption, media, placement
#   threads:   caption, media, location (reels|timeline)
#   twitter:   caption, media
#   linkedin:  caption, media
#   bluesky:   caption, media
#   pinterest: caption, media, board_ids, link, title
# ================================================================
HDR = {"Authorization": "Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi", "Content-Type": "application/json"}

# ============================================================
# PLATFORM MEDIA RULES — Source: PostBridge API spec + platform native
# Updated 2026-03-14 after reading actual TiktokConfiguration schema
# ============================================================
YOUTUBE_ACCTS   = {49678}                       # VIDEO ONLY (mp4)
INSTAGRAM_ACCTS = {49682, 49676}                # image/video WAJIB, no text-only
TIKTOK_ACCTS    = set()                         # if connected: image OR video, NOT text-only
THREADS_ACCTS   = {49683, 49680, 49677}         # all formats OK
FACEBOOK_ACCTS  = {49675, 49674, 49673, 49672}  # all formats OK

# TikTok supports: video, image carousel/slideshow — NOT video-only
# YouTube supports: video ONLY — NOT image, NOT text

def filter_accounts_for_media(social_accounts, media=None, media_type=None):
    """
    Auto-remove incompatible accounts based on media type.
    media_type: 'video' | 'image' | None (text-only)
    Returns safe account list.
    """
    accts = set(social_accounts)
    removed = []

    # YouTube: video ONLY — remove if no media or media is image
    if not media or media_type == "image":
        bad = accts & YOUTUBE_ACCTS
        if bad:
            removed += list(bad)
            accts -= bad

    # Instagram: needs image or video — remove if text-only
    if not media:
        bad = accts & INSTAGRAM_ACCTS
        if bad:
            removed += list(bad)
            accts -= bad

    # TikTok: needs image or video — remove if text-only
    if not media and TIKTOK_ACCTS:
        bad = accts & TIKTOK_ACCTS
        if bad:
            removed += list(bad)
            accts -= bad

    if removed:
        print(f"  ⚠️  Removed incompatible accounts {removed} (media_type={media_type or 'text-only'})")
    return list(accts)

def validate_post_media(social_accounts, media=None, media_type=None):
    """Raises ValueError on platform media violations."""
    accts = set(social_accounts)
    errors = []
    if accts & YOUTUBE_ACCTS and (not media or media_type != "video"):
        errors.append(f"YouTube requires VIDEO — got media_type={media_type}")
    if accts & INSTAGRAM_ACCTS and not media:
        errors.append(f"Instagram requires image or video — got text-only")
    if accts & TIKTOK_ACCTS and not media:
        errors.append(f"TikTok requires image or video — got text-only")
    if errors:
        raise ValueError("Platform media violation:\n" + "\n".join(errors))
LOG = os.path.expanduser("~/.openclaw/workspace/logs/postbridge_monitor.log")
ANALYTICS_LOG = os.path.expanduser("~/.openclaw/workspace/logs/analytics.log")

def get_all(endpoint, **params):
    items, offset = [], 0
    while True:
        r = requests.get(f"{API}{endpoint}", headers=HDR, params={**params, "limit": 100, "offset": offset}, timeout=30)
        d = r.json()
        items.extend(d.get("data", []))
        if offset + 100 >= d.get("meta", {}).get("total", 0): break
        offset += 100
        time.sleep(0.2)
    return items

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def log_analytics(data):
    os.makedirs(os.path.dirname(ANALYTICS_LOG), exist_ok=True)
    with open(ANALYTICS_LOG, "a") as f:
        f.write(json.dumps(data) + "\n")

# 1. Trigger analytics sync
log("=== PostBridge Monitor Run ===")
try:
    r = requests.post(f"{API}/analytics/sync", headers=HDR, json={}, timeout=15)
    synced = r.json().get("triggered", [])
    platforms = [s.get("platform") for s in synced]
    log(f"Analytics sync: {', '.join(platforms)}")
except Exception as e:
    log(f"Analytics sync failed: {e}")

# 2. Get accounts
accounts = get_all("/social-accounts")
by_platform = {}
for a in accounts:
    by_platform.setdefault(a["platform"], []).append(a)
log(f"Accounts: {len(accounts)} ({', '.join(f'{k}:{len(v)}' for k,v in sorted(by_platform.items()))})")

# 3. Get recent post results
results = get_all("/post-results")
total = len(results)
ok = sum(1 for r in results if r.get("success"))
fail = total - ok
rate = ok / total * 100 if total > 0 else 0
log(f"Results: {total} total | ✅ {ok} ({rate:.0f}%) | ❌ {fail}")

# Error breakdown
errors = {}
for r in results:
    if not r.get("success"):
        e = (r.get("error") or "unknown")[:50]
        errors[e] = errors.get(e, 0) + 1

if errors:
    log("Error breakdown:")
    for e, c in sorted(errors.items(), key=lambda x: -x[1])[:5]:
        log(f"  [{c}x] {e}")

# 4. Get analytics data
try:
    r = requests.get(f"{API}/analytics", headers=HDR, timeout=15)
    analytics = r.json()
    if isinstance(analytics, dict) and analytics.get("data"):
        data = analytics["data"]
        if isinstance(data, list):
            total_views = sum(d.get("views", 0) for d in data)
            total_likes = sum(d.get("likes", 0) for d in data)
            total_comments = sum(d.get("comments", 0) for d in data)
            total_shares = sum(d.get("shares", 0) for d in data)
            log(f"Analytics: {total_views} views | {total_likes} likes | {total_comments} comments | {total_shares} shares")
            
            log_analytics({
                "timestamp": datetime.now().isoformat(),
                "accounts": len(accounts),
                "results_total": total,
                "success": ok,
                "fail": fail,
                "success_rate": round(rate, 1),
                "views": total_views,
                "likes": total_likes,
                "comments": total_comments,
                "shares": total_shares,
            })
        else:
            log(f"Analytics response: {str(analytics)[:200]}")
    else:
        log(f"Analytics: {str(analytics)[:200]}")
except Exception as e:
    log(f"Analytics fetch failed: {e}")

# 5. Get scheduled posts count
try:
    r = requests.get(f"{API}/posts", headers=HDR, params={"status": "scheduled", "limit": 1}, timeout=10)
    sched = r.json().get("meta", {}).get("total", 0)
    log(f"Scheduled posts: {sched}")
except:
    sched = 0

# 6. Auto-scaling logic
posted = get_all("/posts", status="posted")
today_posts = [p for p in posted if datetime.now().strftime("%Y-%m-%d") in (p.get("scheduled_at") or "")]
log(f"Posts today: {len(today_posts)}")

# If success rate > 80% and fewer than 15 posts today, scale up
if rate > 80 and len(today_posts) < 15:
    log("📈 SCALING UP: Success rate high, posting more...")
    # Import and run daily poster
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("poster", 
            os.path.expanduser("~/.openclaw/workspace/scripts/daily_content_poster.py"))
        poster = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(poster)
        poster.main()
        log("Auto-scale: Additional posts created")
    except Exception as e:
        log(f"Auto-scale failed: {e}")

elif rate < 50 and fail > 20:
    log("⚠️ HIGH FAILURE RATE — checking for patterns...")
    # Identify which accounts are failing
    fail_accounts = {}
    for r in results:
        if not r.get("success"):
            aid = r.get("social_account_id", "?")
            fail_accounts[aid] = fail_accounts.get(aid, 0) + 1
    
    top_fail = sorted(fail_accounts.items(), key=lambda x: -x[1])[:5]
    for aid, count in top_fail:
        log(f"  Account {aid}: {count} failures")

log("=== Monitor Complete ===\n")
