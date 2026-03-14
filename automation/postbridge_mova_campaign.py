#!/usr/bin/env python3
"""
MOVA Campaign - PostBridge API Automation
Upload & schedule posts via PostBridge API
"""

import json
import urllib.request
import urllib.error
import time
from datetime import datetime, timedelta
from pathlib import Path

# PostBridge API Credentials
POST_BRIDGE_API_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
POST_BRIDGE_BASE_URL = "https://api.post-bridge.com/v1"

# Files
QUEUE_FILE = Path(__file__).parent.parent / "autopilot_affiliate_engine" / "postbridge_queue.json"
LOG_FILE = Path(__file__).parent / "postbridge_submission_log.json"

def make_api_request(endpoint, method="GET", data=None):
    """Make API request to PostBridge"""
    url = f"{POST_BRIDGE_BASE_URL}/{endpoint}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {POST_BRIDGE_API_KEY}")
    req.add_header("Content-Type", "application/json")

    if method == "POST":
        json_data = json.dumps(data).encode("utf-8")
        req.data = json_data
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {
            "error": True,
            "status_code": e.code,
            "message": e.read().decode("utf-8")
        }

def get_social_accounts():
    """Get connected social media accounts"""
    print("\n📱 Fetching connected social accounts...")

    result = make_api_request("social-accounts?limit=50&offset=0")

    if result.get("error"):
        print(f"❌ Error fetching accounts: {result.get('message')}")
        return []

    accounts = result.get("data", [])
    print(f"✅ Found {len(accounts)} connected accounts:\n")

    # Group by platform
    by_platform = {}
    for acc in accounts:
        platform = acc.get("platform", "Unknown")
        if platform not in by_platform:
            by_platform[platform] = []
        by_platform[platform].append(acc)

    # Display
    for platform, accs in sorted(by_platform.items()):
        emoji = {'tiktok': '📱', 'instagram': '📸', 'facebook': '📘',
                 'twitter': '🐦', 'youtube': '▶️', 'linkedin': '💼'}.get(platform, '📝')
        print(f"{emoji} {platform.upper()}")
        for acc in accs:
            name = acc.get("username", acc.get("name", "Unknown"))
            acc_id = acc.get("id", "N/A")
            print(f"   └─ {name} (ID: {acc_id})")
        print()

    return accounts

def load_queue():
    """Load campaign queue"""
    try:
        with open(QUEUE_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading queue: {e}")
        return []

def format_post_for_postbridge(post, media_url):
    """Format post data for PostBridge API"""

    # Caption
    caption = post['content']['caption']

    # Add link to caption if available
    if 'ct' in post['content']:
        link = post['content']['ct']
        if link not in caption:
            caption = f"{caption}\n\n{link}"

    payload = {
        "caption": caption,
        "social_accounts": [],  # Will fill with account IDs from submit function
        "media": [{"url": media_url}],
        "scheduled_at": post['schedule']['publish_at'],
        "type": post['type']
    }

    return payload

def submit_post_to_postbridge(post, accounts, media_url):
    """Submit post to PostBridge"""
    platform = post['platform']

    # Find account for this platform
    relevant_accounts = [a for a in accounts if a.get('platform') == platform]

    if not relevant_accounts:
        return {
            "status": "error",
            "error": f"No connected account for platform: {platform}"
        }

    # Use first account (or implement account selection logic)
    account = relevant_accounts[0]

    # Format payload
    payload = format_post_for_postbridge(post, media_url)
    payload['social_accounts'] = [account['id']]  # Array of account IDs

    print(f"\n📤 Submitting to {platform.upper()}...")
    print(f"   Account: {account.get('username', account.get('name', 'Unknown'))}")
    print(f"   Type: {post['type']}")
    print(f"   Media URL: {media_url}")
    print(f"   Scheduled: {post['schedule']['publish_at']}")
    print(f"   Caption: {post['content']['caption'][:60]}...")

    # Submit
    result = make_api_request("posts", method="POST", data=payload)

    if result.get("error"):
        print(f"   ❌ Error: {result.get('message', result)}")
        return {
            "status": "error",
            "error": result.get("message") or str(result),
            "platform": platform
        }

    print(f"   ✅ Success! Post ID: {result.get('id', 'N/A')}")

    return {
        "status": "success",
        "post_id": result.get('id'),
        "platform": platform,
        "scheduled_at": post['schedule']['publish_at']
    }

def run_campaign_submission(media_urls=None):
    """Run full campaign submission to PostBridge

    Args:
        media_urls: Dict mapping post_id to media URL
                  Example: {"tt_001": "https://cdn.example.com/video1.mp4", ...}
    """
    print("\n" + "="*70)
    print("🚀 MOVA CAMPAIGN - POSTBRIDGE API SUBMISSION")
    print("="*70)

    # Load queue
    queue = load_queue()
    if not queue:
        print("❌ No queue data found")
        return

    print(f"\n✅ Loaded {len(queue)} posts from queue")

    # Check media URLs
    if not media_urls:
        print("\n⚠️  NO MEDIA URLS PROVIDED!")
        print("   You need to provide media URLs for each post.")
        print("\n   Format:")
        print("   {")
        print('     "tt_001": "https://cdn.example.com/video1.mp4",')
        print('     "ig_r001": "https://cdn.example.com/reel1.mp4",')
        print("     ...")
        print("   }")
        print("\n   Or generate media first, then run again.")
        return

    # Get connected accounts
    accounts = get_social_accounts()

    if not accounts:
        print("\n⚠️  No social accounts connected to PostBridge!")
        print("   Please connect accounts first at https://post-bridge.com")
        return

    # Check which platforms are available
    available_platforms = {acc.get('platform') for acc in accounts}
    needed_platforms = {post['platform'] for post in queue}

    print("\n" + "="*70)
    print("📊 PLATFORM COVERAGE:")
    print("="*70)

    for platform in sorted(needed_platforms):
        status = "✅ Available" if platform in available_platforms else "❌ NOT CONNECTED"
        emoji = {'tiktok': '📱', 'instagram': '📸', 'facebook': '📘',
                 'twitter': '🐦', 'youtube': '▶️'}.get(platform, '📝')
        print(f"{emoji} {platform.upper()}: {status}")

    # Filter posts that can be submitted
    submittable = [p for p in queue if p['platform'] in available_platforms]
    missing_platforms = needed_platforms - available_platforms

    # Show what will be submitted
    print("\n" + "="*70)
    print(f"📤 SUBMITTING {len(submittable)} POSTS")
    print("="*70)

    if missing_platforms:
        print(f"\n⚠️  Skipping {len([p for p in queue if p['platform'] in missing_platforms])} posts for unconnected platforms:")
        for platform in sorted(missing_platforms):
            print(f"   • {platform.upper()}")
        print()

    # Submit posts
    results = []
    for i, post in enumerate(submittable, 1):
        asset_id = post.get('asset_id', post.get('metadata', {}).get('asset_id', ''))

        # Get media URL for this post
        media_url = media_urls.get(asset_id)
        if not media_url:
            print(f"\n[{i}/{len(submittable)}] ⚠️  Skipping {asset_id} - No media URL provided")
            results.append({
                "status": "skipped",
                "error": "No media URL",
                "asset_id": asset_id,
                "platform": post['platform']
            })
            continue

        print(f"\n[{i}/{len(submittable)}]", end=" ")
        result = submit_post_to_postbridge(post, accounts, media_url)
        results.append(result)

        # Rate limiting (just in case)
        if i < len(submittable):
            time.sleep(0.5)

    # Summary
    print("\n" + "="*70)
    print("📊 SUBMISSION SUMMARY")
    print("="*70)

    success = sum(1 for r in results if r.get('status') == 'success')
    skipped = sum(1 for r in results if r.get('status') == 'skipped')
    failed = sum(1 for r in results if r.get('status') == 'error')

    print(f"\n✅ Successful: {success}")
    print(f"⚠️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")

    if success > 0:
        print(f"\n📅 Scheduled posts:")
        for r in results:
            if r.get('status') == 'success':
                emoji = {'tiktok': '📱', 'instagram': '📸', 'facebook': '📘',
                         'twitter': '🐦', 'youtube': '▶️'}.get(r.get('platform'), '📝')
                print(f"   {emoji} {r.get('platform').upper()}: {r.get('scheduled_at')}")

    # Save log
    log = {
        "timestamp": datetime.now().isoformat(),
        "total_posts": len(queue),
        "submitted": len(submittable),
        "successful": success,
        "skipped": skipped,
        "failed": failed,
        "results": results,
        "media_urls": media_urls
    }

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    print(f"\n📝 Log saved to: {LOG_FILE}")

    print("\n" + "="*70)
    print("✅ CAMPAIGN SUBMISSION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    """
    Load media URLs from JSON file or provide manually
    """

    # Load from file first
    media_urls_file = Path(__file__).parent / "media_urls_for_postbridge.json"

    media_urls = {}

    if media_urls_file.exists():
        print(f"📂 Loading media URLs from: {media_urls_file}")
        with open(media_urls_file) as f:
            media_urls = json.load(f)

    if not media_urls:
        print("\n⚠️  No media URLs provided!")
        print("\n📝 Create media_urls_for_postbridge.json with:")
        print('{')
        print('  "tt_001": "https://cdn.example.com/video1.mp4",')
        print('  "ig_r001": "https://cdn.example.com/reel1.mp4",')
        print('  ...')
        print('}')
        print("\nOr edit queue file and add media_url field.")
    else:
        print(f"✅ Loaded {len(media_urls)} media URLs")

    run_campaign_submission(media_urls=media_urls)