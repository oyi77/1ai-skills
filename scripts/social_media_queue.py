#!/usr/bin/env python3
"""
Social Media Content Queue System
Automated content scheduling and posting for TikTok and Instagram
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

# Configuration
CONTENT_QUEUE_FILE = Path('/home/openclaw/.openclaw/workspace/output/content_queue.json')
POSTED_LOG = Path('/home/openclaw/.openclaw/workspace/output/posted_log.json')
REPORTS_DIR = Path('/home/openclaw/.openclaw/workspace/output/reports')

# Social Media Platforms
PLATFORMS = {
    'tiktok': {
        'enabled': False,  # Needs TIKTOK_ACCESS_TOKEN
        'api_available': False
    },
    'instagram': {
        'enabled': False,  # Needs INSTAGRAM_ACCESS_TOKEN + INSTAGRAM_USER_ID
        'api_available': False
    },
    'facebook': {
        'enabled': True,  # Post-bridge connected
        'api_available': True,
        'client': 'skills/1ai-skills/marketing/post_bridge_client.py'
    }
}

class ContentItem:
    def __init__(self, platform: str, content_type: str, video_url: str, 
                 caption: str, hashtags: List[str], scheduled_time: str = None):
        self.platform = platform
        self.content_type = content_type
        self.video_url = video_url
        self.caption = caption
        self.hashtags = hashtags
        self.scheduled_time = scheduled_time
        self.status = 'queued'
        self.created_at = datetime.now().isoformat()
        self.posted_at = None
        self.posted_to = []

    def to_dict(self):
        return {
            'platform': self.platform,
            'content_type': self.content_type,
            'video_url': self.video_url,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'scheduled_time': self.scheduled_time,
            'status': self.status,
            'created_at': self.created_at,
            'posted_at': self.posted_at,
            'posted_to': self.posted_to
        }

class ContentQueue:
    def __init__(self):
        self.queue = self.load_queue()
        self.posted_log = self.load_posted_log()

    def load_queue(self) -> List[ContentItem]:
        """Load content queue"""
        if CONTENT_QUEUE_FILE.exists():
            with open(CONTENT_QUEUE_FILE, 'r') as f:
                data = json.load(f)
                return [ContentItem(**item) for item in data]
        return []

    def save_queue(self):
        """Save content queue"""
        data = [item.to_dict() for item in self.queue]
        with open(CONTENT_QUEUE_FILE, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_posted_log(self) -> List[Dict]:
        """Load posted content log"""
        if POSTED_LOG.exists():
            with open(POSTED_LOG, 'r') as f:
                return json.load(f)
        return []

    def save_posted_log(self):
        """Save posted content log"""
        with open(POSTED_LOG, 'w') as f:
            json.dump(self.posted_log, f, indent=2, ensure_ascii=False)

    def add_content(self, platform: str, content_type: str, video_url: str,
                   caption: str, hashtags: List[str], scheduled_time: str = None):
        """Add content to queue"""
        item = ContentItem(
            platform=platform,
            content_type=content_type,
            video_url=video_url,
            caption=caption,
            hashtags=hashtags,
            scheduled_time=scheduled_time
        )
        self.queue.append(item)
        self.save_queue()
        return item

    def get_queued_content(self, platform: str = None) -> List[ContentItem]:
        """Get queued content (optionally filtered by platform)"""
        queued = [item for item in self.queue if item.status == 'queued']
        if platform:
            queued = [item for item in queued if item.platform == platform]
        return queued

    def get_content_ready_to_post(self) -> List[ContentItem]:
        """Get content ready to post (scheduled time reached)"""
        now = datetime.now()
        ready_to_post = []
        
        for item in self.queue:
            if item.status == 'queued' and item.scheduled_time:
                scheduled = datetime.fromisoformat(item.scheduled_time)
                if scheduled <= now:
                    ready_to_post.append(item)
            elif item.status == 'queued' and not item.scheduled_time:
                # No scheduled time, ready now
                ready_to_post.append(item)
        
        return ready_to_post

    def mark_as_posted(self, item_id: int, posted_to: str):
        """Mark content as posted"""
        for item in self.queue:
            if item.video_url == self.queue[item_id].video_url:
                item.status = 'posted'
                item.posted_at = datetime.now().isoformat()
                item.posted_to.append(posted_to)
                break
        self.save_queue()
        
        # Add to posted log
        self.posted_log.append({
            'video_url': self.queue[item_id].video_url,
            'platform': self.queue[item_id].platform,
            'caption': self.queue[item_id].caption,
            'posted_at': datetime.now().isoformat(),
            'posted_to': posted_to
        })
        self.save_posted_log()

    def post_to_facebook(self, item: ContentItem):
        """Post content to Facebook via PostBridge"""
        try:
            sys.path.insert(0, '/home/openclaw/.openclaw/workspace/skills/1ai-skills/marketing')
            from post_bridge_client import PostBridgeClient
            
            client = PostBridgeClient()
            
            # Format caption with hashtags
            full_caption = f"{item.caption}\n\n{' '.join(item.hashtags)}"
            
            # Post to all connected Facebook accounts
            # Account IDs: 45667-45676
            results = []
            for account_id in range(45667, 45677):
                try:
                    result = client.create_post(
                        account_id=account_id,
                        content={
                            'text': full_caption,
                            'media_url': item.video_url
                        }
                    )
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})
            
            return results
            
        except Exception as e:
            return [{'error': str(e)}]

    def generate_content_suggestions(self) -> List[Dict]:
        """Generate content suggestions based on portfolio"""
        suggestions = []
        
        # Portfolio videos
        portfolio_videos = [
            'https://drive.google.com/file/d/1AZUX3uQu7kVaLkKx_MtS2nf0qzFiz-_s/view?usp=drivesdk',
            'https://drive.google.com/file/d/1RlAdstXdWSRlH4Wfza4jymnZTS6OYxG6/view?usp=drivesdk',
            'https://drive.google.com/file/d/1q95SpX29wOCXjhrpv_HeIFz_7czQD1as/view?usp=drivesdk'
        ]
        
        # Content types
        content_types = ['portfolio', 'before_after', 'showcase', 'tutorial', 'tips']
        
        # Hashtags
        hashtags_sets = {
            'general': ['#ShopeeSellers', '#TikTokMarketing', '#VideoContent', '#IndonesiaBusiness'],
            'flooring': ['#vinylfloor', '#renovation', '#homedesign', '#flooring', '#diy'],
            'viral': ['#viral', '#fyp', '#foryou', '#trending', '#viralvideo'],
            'business': ['#business', '#entrepreneur', '#sales', '#marketing', '#growth']
        }
        
        # Generate combinations
        for video_url in portfolio_videos:
            for content_type in content_types:
                for tag_category in ['general', 'flooring', 'viral']:
                    hashtags = hashtags_sets[tag_category]
                    
                    # Generate caption
                    captions = {
                        'portfolio': 'Cek portfolio kami! TikTok viral content untuk produk Shopee 🚀',
                        'before_after': 'Before & After transformation - lihat bedanya! 🔥',
                        'showcase': 'Premium showcase - tampilan mewah untuk produk Anda ✨',
                        'tutorial': 'Tutorial instalasi - gampang banget! 🛠️',
                        'tips': 'Tips: Tingkatkan penjualan dengan video viral 💡'
                    }
                    
                    suggestions.append({
                        'video_url': video_url,
                        'content_type': content_type,
                        'caption': captions.get(content_type, captions['portfolio']),
                        'hashtags': hashtags,
                        'platform': 'facebook'  # Only Facebook is enabled
                    })
        
        return suggestions

    def generate_scheduling_plan(self) -> List[Dict]:
        """Generate 7-day content scheduling plan"""
        now = datetime.now()
        suggestions = self.generate_content_suggestions()
        
        scheduled_content = []
        
        # Schedule for next 7 days (1-2 posts per day)
        scheduled_date = now
        
        for day in range(7):
            # Morning post
            scheduled_date = now + timedelta(days=day, hours=9)
            if suggestions:
                item = suggestions.pop(0)
                scheduled_content.append({
                    **item,
                    'scheduled_time': scheduled_date.isoformat(),
                    'post_time': 'morning'
                })
            
            # Evening post
            scheduled_date = now + timedelta(days=day, hours=18)
            if suggestions:
                item = suggestions.pop(0)
                scheduled_content.append({
                    **item,
                    'scheduled_time': scheduled_date.isoformat(),
                    'post_time': 'evening'
                })
        
        return scheduled_content

    def generate_weekly_report(self) -> str:
        """Generate weekly social media report"""
        now = datetime.now()
        week_start = now - timedelta(days=7)
        
        # Get posts from last 7 days
        recent_posts = [
            post for post in self.posted_log
            if datetime.fromisoformat(post['posted_at']) >= week_start
        ]
        
        # Analyze by platform
        by_platform = {}
        for post in recent_posts:
            platform = post['platform']
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(post)
        
        # Generate report
        report = f"""
# Weekly Social Media Report
Week of: {week_start.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}

## Summary
- Total Posts: {len(recent_posts)}
- Posts This Week: {len(recent_posts)}

## By Platform
"""
        
        for platform, posts in by_platform.items():
            report += f"\n### {platform.capitalize()}"
            report += f"- Posts: {len(posts)}"
            report += f"- Accounts: {set([post.get('posted_to', 'unknown') for post in posts])}"

        report += f"""

## Scheduled Content
- Queued: {len([item for item in self.queue if item.status == 'queued'])}
- Ready to Post: {len(self.get_content_ready_to_post())}
"""

        return report

def main():
    """Main automation loop"""
    queue = ContentQueue()
    
    # Generate content suggestions
    print("Generating content suggestions...")
    suggestions = queue.generate_content_suggestions()
    print(f"✅ Generated {len(suggestions)} content suggestions")
    
    # Generate scheduling plan
    print("Generating 7-day scheduling plan...")
    schedule = queue.generate_scheduling_plan()
    print(f"✅ Generated {len(schedule)} scheduled posts")
    
    # Save schedule
    for item in schedule:
        queue.add_content(
            platform=item['platform'],
            content_type=item['content_type'],
            video_url=item['video_url'],
            caption=item['caption'],
            hashtags=item['hashtags'],
            scheduled_time=item['scheduled_time']
        )
    
    # Get ready-to-post content
    print("Checking for ready-to-post content...")
    ready_to_post = queue.get_content_ready_to_post()
    print(f"✅ Found {len(ready_to_post)} items ready to post")
    
    # Auto-post to Facebook (enabled platform)
    if ready_to_post and PLATFORMS['facebook']['enabled']:
        print(f"\nAuto-posting to Facebook...")
        for item in ready_to_post:
            try:
                results = queue.post_to_facebook(item)
                success_count = len([r for r in results if 'error' not in r])
                print(f"✅ Posted to {success_count}/{len(results)} accounts: {item.caption[:30]}...")
                
                # Mark as posted
                queue.mark_as_posted(queue.queue.index(item), 'facebook')
                
            except Exception as e:
                print(f"❌ Error posting: {e}")
    
    # Generate weekly report
    report = queue.generate_weekly_report()
    report_file = REPORTS_DIR / f"social_media_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"✅ Weekly report saved: {report_file}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SOCIAL MEDIA QUEUE SUMMARY")
    print(f"{'='*60}")
    print(f"Total in queue: {len(queue.queue)}")
    print(f"Ready to post: {len(ready_to_post)}")
    print(f"Posted this week: {len(queue.posted_log)}")
    print(f"Scheduled next 7 days: {len([item for item in queue.queue if item.status == 'queued'])}")
    
    print(f"\n📊 Platforms enabled:")
    for platform, config in PLATFORMS.items():
        status = "✅" if config['enabled'] else "❌"
        print(f"  - {platform.capitalize()}: {status}")

if __name__ == '__main__':
    main()
