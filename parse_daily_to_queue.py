#!/usr/bin/env python3
"""
Parse daily content file and create PostBridge queue
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

CONTENT_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/daily_content_scheduled/daily_2026-03-05.txt"
OUTPUT_FILE = "/home/openclaw/.openclaw/workspace/autopilot_affiliate_engine/postbridge_queue_jendralbot.json"

PLATFORM_MAP = {
    'TIKTOK': 'tiktok',
    'INSTAGRAM': 'instagram',
    'FACEBOOK': 'facebook',
    'TWITTER': 'twitter',
    'YOUTUBE': 'youtube'
}

def parse_daily_content():
    """Parse daily content file"""
    content = Path(CONTENT_FILE).read_text()

    posts = []
    current_post = {}
    post_id = 1

    for line in content.split('\n'):
        line = line.strip()

        if line.startswith('📦'):
            if current_post:
                current_post['id'] = f"jb_{post_id:03d}"
                posts.append(current_post)
                post_id += 1
            current_post = {'product': line.replace('📦', '').strip()}

        elif line.startswith('📱'):
            parts = line.replace('📱', '').strip().split(' - ')
            current_post['platform'] = PLATFORM_MAP.get(parts[0].strip(), parts[0].strip().lower())
            current_post['time'] = parts[1].strip()

        elif line.startswith('🔗'):
            current_post['link'] = line.replace('🔗', '').strip()

        elif line.startswith('📝'):
            current_post['caption'] = line.replace('📝', '').strip()

        elif line.startswith('🏷️'):
            current_post['hashtags'] = line.replace('🏷️', '').strip()

    # Add last post
    if current_post:
        current_post['id'] = f"jb_{post_id:03d}"
        posts.append(current_post)

    return posts

def create_postbridge_queue(posts):
    """Create PostBridge queue format"""
    now = datetime.now()

    queue = []

    for i, post in enumerate(posts):
        product_name = post['product']
        platform = post['platform']
        time_str = post['time']
        link = post['link']
        caption = post['caption']
        hashtags = post.get('hashtags', '')

        # Parse time and schedule
        time_parts = time_str.split(':')
        post_time = now.replace(
            hour=int(time_parts[0]),
            minute=int(time_parts[1]),
            second=0,
            microsecond=0
        )

        # If time has passed today, schedule for tomorrow
        if post_time < now:
            post_time = post_time + timedelta(days=1)

        # Determine post type
        if platform == 'instagram':
            post_type = 'reel'
        elif platform == 'youtube':
            post_type = 'shorts'
        elif platform == 'tiktok':
            post_type = 'video'
        else:
            post_type = 'post'

        # Combine caption and hashtags
        full_caption = f"{caption}\n\n{hashtags}\n\n{link}"

        queue_item = {
            'id': post['id'],
            'platform': platform,
            'type': post_type,
            'content': {
                'caption': full_caption,
                'url': link,
                'hashtags': hashtags
            },
            'schedule': {
                'publish_at': post_time.isoformat(),
                'time_zone': 'Asia/Jakarta'
            },
            'metadata': {
                'product': product_name,
                'campaign_id': 'jendralbot_day1',
                'asset_id': f"{platform}_jb{i:03d}"
            },
            'media': {
                'type': 'image' if post_type in ['post', 'carousel'] else 'video',
                'format': 'vertical' if post_type in ['reel', 'video', 'shorts'] else 'square'
            }
        }

        queue.append(queue_item)

    return queue

def save_queue(queue):
    """Save queue to file"""
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

    print(f"✅ Queue saved to: {OUTPUT_FILE}")
    print(f"📦 Total posts: {len(queue)}")

def main():
    print("="*60)
    print("📋 PARSING DAILY CONTENT TO POSTBRIDGE QUEUE")
    print("="*60)
    print()

    posts = parse_daily_content()
    print(f"✅ Parsed {len(posts)} posts")
    print()

    queue = create_postbridge_queue(posts)
    print(f"✅ Created {len(queue)} PostBridge queue items")
    print()

    save_queue(queue)

    print("\n" + "="*60)
    print("📊 QUEUE SUMMARY")
    print("="*60)

    # Group by platform
    by_platform = {}
    for item in queue:
        platform = item['platform']
        if platform not in by_platform:
            by_platform[platform] = []
        by_platform[platform].append(item)

    print()
    for platform, items in sorted(by_platform.items()):
        emoji = {'tiktok': '📱', 'instagram': '📸', 'facebook': '📘',
                 'twitter': '🐦', 'youtube': '▶️'}.get(platform, '📝')
        print(f"{emoji} {platform.upper()}: {len(items)} posts")

    print(f"\n📅 First post: {queue[0]['schedule']['publish_at']}")
    print(f"📅 Last post: {queue[-1]['schedule']['publish_at']}")

if __name__ == "__main__":
    main()