#!/usr/bin/env python3
"""
Multi-Platform Auto-Poster for JENDRALBOT Campaign
Integrates TikTok, IG Reels, YouTube Shorts automation
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta
import random
import time

workspace = os.path.expanduser("~/.openclaw/workspace")

class MultiPlatformPoster:
    """Automated posting to TikTok, IG Reels, YouTube Shorts"""
    
    def __init__(self, hook_db_path):
        print(f"\n🚀 Initializing Multi-Platform Auto-Poster...")
        
        # Load hook database
        with open(hook_db_path, 'r') as f:
            self.hook_db = json.load(f)
        
        self.load_hooks()
        self.posted_hooks = set()
        
        # Setup logging
        self.log_path = os.path.join(workspace, "logs/multi_platform_posts.log")
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
    
    def load_hooks(self):
        """Load all hooks from database"""
        self.all_hooks = []
        
        for product in self.hook_db['products']:
            hooks_file = os.path.join(workspace, product['hooks_file'])
            
            if os.path.exists(hooks_file):
                with open(hooks_file, 'r') as f:
                    data = json.load(f)
                    for hook in data['hooks']:
                        hook['product'] = product['name']
                        hook['price'] = product['price']
                        hook['lynk'] = product['lynk']
                        self.all_hooks.append(hook)
        
        print(f"✅ Loaded {len(self.all_hooks)} hooks from {len(self.hook_db['products'])} products")
    
    def generate_post_content(self, hook, platform):
        """
        Generate platform-specific content from hook
        
        Args:
            hook: Hook dict with 'headline', 'body', 'cta'
            platform: 'tiktok', 'ig_reels', 'youtube_shorts'
        
        Returns:
            dict: Platform-specific content (caption, hashtags, tags)
        """
        platform_hashtags = self.get_platform_hashtags(platform)
        
        # Build caption
        if platform == 'tiktok':
            caption = f"{hook['headline']}\n\n{hook['body']}\n\n{hook['cta']}"
            # TikTok: Short, punchy, trending
            caption = self.truncate_text(caption, 2200)
        
        elif platform == 'ig_reels':
            caption = f"{hook['headline']}\n\n{hook['body']}\n\n{hook['cta']}"
            # Instagram: First line crucial, add line breaks
            caption = self.truncate_text(caption, 2200)
        
        elif platform == 'youtube_shorts':
            caption = f"{hook['headline']}\n\n{hook['body']}\n\n{hook['cta']}"
            # YouTube: SEO-friendly, longer description
            caption = self.truncate_text(caption, 5000)
        
        return {
            'caption': caption,
            'hashtags': platform_hashtags,
            'hook': hook,
            'platform': platform
        }
    
    def get_platform_hashtags(self, platform):
        """Get platform-specific hashtags"""
        
        base_hashtags = ['#JENDRALBOT', '#AItools', '#Digitalproducts', '#Productivity']
        
        if platform == 'tiktok':
            # TikTok: Mix trending + niche
            return base_hashtags + ['#fyp', '#viral', '#businesshacks', '#indonesia']
        
        elif platform == 'ig_reels':
            # Instagram: 3-5 hashtags max
            return base_hashtags[:3] + ['#AIcontent', '#digitalmarketing']
        
        elif platform == 'youtube_shorts':
            # YouTube: 5-10 tags
            return base_hashtags + ['#AI', '#ContentCreation', '#BusinessTips', '#HowTo']
    
    def truncate_text(self, text, max_length):
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def generate_visual_post(self, content, output_dir):
        """
        Generate visual post from hook (dark background, white text, 4:5 vertical)
        
        Args:
            content: Content dict from generate_post_content
            output_dir: Directory to save visual
        
        Returns:
            str: Path to generated visual
        """
        hook = content['hook']
        
        # Create visual data structure
        visual_data = {
            "product": hook['product'],
            "headline": hook['headline'],
            "body": hook['body'],
            "cta": hook['cta'],
            "lynk": hook['lynk'],
            "format": "4:5 vertical",
            "style": "Dark background (#000000), white text (#FFFFFF)",
            "font_size": {
                "headline": "48px",
                "body": "32px",
                "cta": "28px"
            },
            "generated_at": datetime.now().isoformat()
        }
        
        # Save as JSON (placeholder for actual visual generation)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        visual_path = os.path.join(output_dir, f"visual_{timestamp}.json")
        
        with open(visual_path, 'w') as f:
            json.dump(visual_data, f, indent=2)
        
        return visual_path
    
    def post_to_tiktok(self, content, visual_path):
        """Post to TikTok"""
        print(f"  [TikTok] Posting: {content['hook']['headline'][:30]}...")
        
        # Use TikTok automation skill
        tiktok_skill_path = os.path.join(workspace, "skills/tiktok-automation/script.sh")
        
        if os.path.exists(tiktok_skill_path):
            # Execute TikTok upload
            try:
                caption = content['caption'] + "\n" + " ".join(content['hashtags'])
                
                # Command structure placeholder
                cmd = [
                    tiktok_skill_path,
                    '--video', visual_path,  # Will be converted to video later
                    '--caption', caption,
                    '--tags', " ".join(content['hashtags'][:5])
                ]
                
                # Execute (placeholder - actual implementation needed)
                result = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"  ✅ TikTok post successful")
                    self.log_post('tiktok', content['hook'], 'success')
                    return True
                else:
                    print(f"  ❌ TikTok post failed: {result.stderr}")
                    self.log_post('tiktok', content['hook'], 'failed', result.stderr)
                    return False
            
            except Exception as e:
                print(f"  ❌ TikTok error: {str(e)}")
                self.log_post('tiktok', content['hook'], 'failed', str(e))
                return False
        else:
            print(f"  ⚠️  TikTok skill not found: {tiktok_skill_path}")
            self.log_post('tiktok', content['hook'], 'failed', 'Skill not found')
            return False
    
    def post_to_ig_reels(self, content, visual_path):
        """Post to Instagram Reels"""
        print(f"  [IG Reels] Posting: {content['hook']['headline'][:30]}...")
        
        # Placeholder for IG Reels automation
        # Similar structure to TikTok
        
        print(f"  ⏳ IG Reels automation ready (framework complete)")
        self.log_post('ig_reels', content['hook'], 'pending', 'API integration needed')
        return True
    
    def post_to_youtube_shorts(self, content, visual_path):
        """Post to YouTube Shorts"""
        print(f"  [YouTube Shorts] Posting: {content['hook']['headline'][:30]}...")
        
        # Placeholder for YouTube Shorts automation
        # Similar structure to TikTok
        
        print(f"  ⏳ YouTube Shorts automation ready (framework complete)")
        self.log_post('youtube_shorts', content['hook'], 'pending', 'API integration needed')
        return True
    
    def log_post(self, platform, hook, status, details=""):
        """Log post attempt"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "product": hook['product'],
            "headline": hook['headline'],
            "status": status,
            "details": details
        }
        
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def run_campaign(self, posts_per_platform):
        """
        Run full multi-platform campaign
        
        Args:
            posts_per_platform: Number of posts per platform
        """
        print(f"\n{'='*60}")
        print(f"MULTI-PLATFORM AUTO-POSTER CAMPAIGN")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: {posts_per_platform} posts/platform × 3 platforms = {posts_per_platform * 3} posts")
        print(f"{'='*60}\n")
        
        platforms = ['tiktok', 'ig_reels', 'youtube_shorts']
        
        for platform in platforms:
            print(f"\n📱 Processing {platform.upper()}...")
            self.post_to_platform(platform, posts_per_platform)
        
        print(f"\n✅ Campaign complete!\n")
    
    def post_to_platform(self, platform, count):
        """Post multiple hooks to specific platform"""
        successful = 0
        failed = 0
        pending = 0
        
        # Create output directory
        output_dir = os.path.join(workspace, "generated_posts", platform)
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(count):
            try:
                # Get random unposted hook
                available = [h for h in self.all_hooks 
                            if h['headline'] not in self.posted_hooks]
                
                if not available:
                    print(f"  ⚠️  All hooks posted for {platform}")
                    break
                
                hook = random.choice(available)
                
                # Generate content
                content = self.generate_post_content(hook, platform)
                
                # Generate visual (JSON placeholder)
                visual_path = self.generate_visual_post(content, output_dir)
                
                # Post to platform
                if platform == 'tiktok':
                    result = self.post_to_tiktok(content, visual_path)
                    if result:
                        successful += 1
                        self.posted_hooks.add(hook['headline'])
                    else:
                        failed += 1
                
                elif platform == 'ig_reels':
                    result = self.post_to_ig_reels(content, visual_path)
                    if result:
                        pending += 1
                
                elif platform == 'youtube_shorts':
                    result = self.post_to_youtube_shorts(content, visual_path)
                    if result:
                        pending += 1
                
                print(f"  [{i+1}/{count}] {'✅' if result else '❌'} {hook['headline'][:30]}...")
                
                # Wait between posts
                time.sleep(30)
            
            except Exception as e:
                print(f"  ❌ [{i+1}/{count}] ERROR: {str(e)}")
                failed += 1
        
        print(f"\n  📊 {platform.upper()}: {successful} posted, {failed} failed, {pending} pending")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Platform Auto-Poster')
    parser.add_argument('--posts', type=int, default=6, help='Posts per platform (default: 6)')
    parser.add_argument('--tiktok-only', action='store_true', help='Post to TikTok only')
    
    args = parser.parse_args()
    
    # Initialize poster
    poster = MultiPlatformPoster(
        hook_db_path=os.path.join(workspace, "hooks/jendralbot_complete.json")
    )
    
    # Run campaign
    if args.tiktok_only:
        print("\n📱 TikTok-only mode")
        poster.post_to_platform('tiktok', args.posts)
    else:
        poster.run_campaign(posts_per_platform=args.posts)

if __name__ == "__main__":
    main()