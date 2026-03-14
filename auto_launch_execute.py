#!/usr/bin/env python3
"""
AUTO-EXECUTE: JENDRALBOT Launch via PostBridge
Posts all scheduled content automatically
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

POST_BRIDGE_API_KEY = "pb_live_LzxK4Q4428kb1b6KETgdue"
POST_BRIDGE_URL = "https://post-bridge.com/api/v1"

CONTENT_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/daily_content_scheduled/daily_2026-03-05.txt"
LOG_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/post_execution_log.json"

def parse_daily_content():
    """Parse daily content file into structured posts"""
    content = Path(CONTENT_FILE).read_text()

    posts = []
    current_post = {}

    for line in content.split('\n'):
        line = line.strip()

        # Product name
        if line.startswith('📦'):
            if current_post:
                posts.append(current_post)
            current_post = {'product': line.replace('📦', '').strip()}

        # Platform and time
        elif line.startswith('📱'):
            parts = line.replace('📱', '').strip().split(' - ')
            current_post['platform'] = parts[0].strip()
            current_post['time'] = parts[1].strip()

        # Link
        elif line.startswith('🔗'):
            current_post['link'] = line.replace('🔗', '').strip()

        # Content
        elif line.startswith('📝'):
            current_post['content'] = line.replace('📝', '').strip()

        # Hashtags
        elif line.startswith('🏷️'):
            current_post['hashtags'] = line.replace('🏷️', '').strip()

    # Add last post
    if current_post:
        posts.append(current_post)

    return posts

def post_to_platform(platform, content, hashtags, link, scheduled_time=None):
    """Post to platform using PostBridge API"""
    platform_map = {
        'TIKTOK': 'tiktok',
        'INSTAGRAM': 'instagram',
        'FACEBOOK': 'facebook',
        'TWITTER': 'twitter',
        'YOUTUBE': 'youtube'
    }

    platform_id = platform_map.get(platform.upper(), platform.lower())
    full_content = f"{content} {hashtags}\n\n{link}"

    payload = {
        'content': full_content,
        'platforms': [platform_id],
        'media_urls': []  # We'll add actual images later
    }

    if scheduled_time:
        payload['scheduled_at'] = scheduled_time.isoformat()

    try:
        response = requests.post(
            f"{POST_BRIDGE_URL}/posts",
            headers={
                'Authorization': f"Bearer {POST_BRIDGE_API_KEY}",
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            return {
                'success': True,
                'platform': platform_id,
                'response': response.json()
            }
        else:
            return {
                'success': False,
                'platform': platform_id,
                'error': response.text
            }
    except Exception as e:
        return {
            'success': False,
            'platform': platform_id,
            'error': str(e)
        }

def execute_launch():
    """Execute the full launch"""
    posts = parse_daily_content()
    print(f"🚀 Found {len(posts)} posts to publish")

    now = datetime.now()
    execution_log = {
        'date': now.strftime('%Y-%m-%d'),
        'started_at': now.isoformat(),
        'posts': []
    }

    success_count = 0
    failed_count = 0

    for i, post in enumerate(posts, 1):
        print(f"\n📤 [{i}/{len(posts)}] {post['platform']} - {post['product']}")

        # Parse time (HH:MM format)
        time_parts = post['time'].split(':')
        post_time = now.replace(
            hour=int(time_parts[0]),
            minute=int(time_parts[1]),
            second=0,
            microsecond=0
        )

        # If time has passed today, schedule for tomorrow
        if post_time < now:
            post_time = post_time + timedelta(days=1)
            print(f"   ⏰ Time passed, scheduling for tomorrow {post_time.strftime('%H:%M')}")

        # Post to platform
        result = post_to_platform(
            post['platform'],
            post['content'],
            post.get('hashtags', ''),
            post['link'],
            post_time
        )

        log_entry = {
            'index': i,
            'platform': post['platform'],
            'product': post['product'],
            'scheduled_at': post_time.isoformat(),
            'result': result
        }

        execution_log['posts'].append(log_entry)

        if result['success']:
            print(f"   ✅ SUCCESS: Post scheduled")
            success_count += 1
        else:
            print(f"   ❌ FAILED: {result.get('error', 'Unknown error')}")
            failed_count += 1

    # Save log
    execution_log['completed_at'] = datetime.now().isoformat()
    execution_log['summary'] = {
        'total': len(posts),
        'success': success_count,
        'failed': failed_count,
        'success_rate': f"{(success_count/len(posts)*100):.1f}%"
    }

    with open(LOG_FILE, 'w') as f:
        json.dump(execution_log, f, indent=2)

    # Summary
    print("\n" + "="*60)
    print("🎯 LAUNCH SUMMARY")
    print("="*60)
    print(f"Total Posts: {len(posts)}")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Success Rate: {(success_count/len(posts)*100):.1f}%")
    print(f"\nLog saved to: {LOG_FILE}")
    print("="*60)

    return execution_log

if __name__ == "__main__":
    execute_launch()