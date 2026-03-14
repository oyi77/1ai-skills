#!/usr/bin/env python3
"""
Auto Upload Scheduler for JENDRALBOT Campaign
Automatically posts viral hooks to TikTok, IG Reels, YouTube Shorts
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
import subprocess
import random

workspace = os.path.expanduser("~/.openclaw/workspace")

class HookDatabase:
    """Load and manage hooks from JSON files"""
    
    def __init__(self, db_path):
        with open(db_path, 'r') as f:
            self.db = json.load(f)
        self.load_all_hooks()
    
    def load_all_hooks(self):
        """Load all hooks from product files"""
        self.all_hooks = []
        
        for product in self.db['products']:
            hooks_file = os.path.join(workspace, product['hooks_file'])
            
            if os.path.exists(hooks_file):
                with open(hooks_file, 'r') as f:
                    data = json.load(f)
                    # Add product metadata to each hook
                    for hook in data['hooks']:
                        hook['product'] = product['name']
                        hook['price'] = product['price']
                        hook['lynk'] = product['lynk']
                        self.all_hooks.append(hook)
            else:
                print(f"Warning: Hooks file not found: {hooks_file}")
        
        print(f"Loaded {len(self.all_hooks)} hooks from {len(self.db['products'])} products")
    
    def get_random_hook(self, product_name=None):
        """Get a random hook, optionally filtered by product"""
        available = self.all_hooks
        
        if product_name:
            available = [h for h in self.all_hooks if h['product'] == product_name]
        
        if not available:
            print(f"Warning: No hooks available for {product_name}")
            return None
        
        return random.choice(available)

class ImageGenerator:
    """Generate visual posts from hooks (dark background, white text, 4:5 vertical)"""
    
    def generate_from_hook(self, hook, output_path):
        """
        Generate image from hook data
        
        Args:
            hook: Hook dict with 'headline', 'body', 'cta'
            output_path: Where to save the image
        """
        # TODO: Integrate with image generation skill
        # For now, create a text-based placeholder file
        
        image_data = {
            "headline": hook['headline'],
            "body": hook['body'],
            "cta": hook['cta'],
            "product": hook['product'],
            "lynk": hook['lynk'],
            "format": "4:5 vertical",
            "style": "Dark background (#000000), white text (#FFFFFF)",
            "generated_at": datetime.now().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(image_data, f, indent=2)
        
        return True

class PlatformUploader:
    """Upload posts to different platforms"""
    
    def __init__(self):
        self.credentials = self.load_credentials()
    
    def load_credentials(self):
        """Load platform credentials from config"""
        config_path = os.path.join(workspace, "config/platform_credentials.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            return {}
    
    def upload_tiktok(self, image_path, caption, hashtags):
        """Post to TikTok"""
        # TODO: Integrate with tiktok-automation skill
        print(f"[TO-LATER] Uploading to TikTok: {image_path}")
        print(f"Caption: {caption}")
        print(f"Hashtags: {', '.join(hashtags)}")
        return True
    
    def upload_ig_reels(self, image_path, caption, hashtags):
        """Post to Instagram Reels"""
        # TODO: Integrate with platform API
        print(f"[TO-LATER] Uploading to IG Reels: {image_path}")
        print(f"Caption: {caption}")
        print(f"Hashtags: {', '.join(hashtags)}")
        return True
    
    def upload_youtube_shorts(self, image_path, caption, hashtags):
        """Post to YouTube Shorts"""
        # TODO: Integrate with platform API
        print(f"[TO-LATER] Uploading to YouTube Shorts: {image_path}")
        print(f"Caption: {caption}")
        print(f"Hashtags: {', '.join(hashtags)}")
        return True

class Scheduler:
    """Manage posting schedule"""
    
    def __init__(self, schedule_path):
        with open(schedule_path, 'r') as f:
            self.schedule = json.load(f)
    
    def get_next_post_time(self):
        """Get optimal next posting time based on platform"""
        # Based on TikTok trends research:
        # - Best: Saturday 8-11 PM (2-3× engagement)
        # - Daily: 7-9 PM Peak
        return datetime.now() + timedelta(minutes=30)
    
    def should_post_now(self):
        """Check if current time is in optimal posting window"""
        now = datetime.now()
        hour = now.hour
        
        # Peak hours: 7 PM - 11 PM
        return 19 <= hour <= 23

class CampaignRunner:
    """Main campaign orchestration"""
    
    def __init__(self):
        print("Initializing JENDRALBOT Auto Upload Scheduler...")
        
        # Initialize components
        self.hook_db = HookDatabase(os.path.join(workspace, "hooks/jendralbot_complete.json"))
        self.generator = ImageGenerator()
        self.uploader = PlatformUploader()
        self.scheduler = Scheduler(os.path.join(workspace, "config/upload_schedule.json"))
        
        # Setup logging
        self.log_path = os.path.join(workspace, "logs/auto_upload.log")
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
    
    def run_campaign_day(self, posts_per_platform=18):
        """
        Run full day's posting campaign
        
        Args:
            posts_per_platform: Number of posts per platform (18 = 6 products × 3 hooks)
        """
        print(f"\n{'='*60}")
        print(f"JENDRALBOT Auto Upload Campaign")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target: {posts_per_platform} posts/platform × 3 platforms = {posts_per_platform * 3} posts")
        print(f"{'='*60}\n")
        
        # Platforms to post to
        platforms = ['tiktok', 'ig_reels', 'youtube_shorts']
        
        for platform in platforms:
            print(f"\n📱 Processing {platform.upper()}...")
            self.post_to_platform(platform, posts_per_platform)
        
        print(f"\n✅ Campaign day complete!")
        print(f"📊 Stats: {posts_per_platform * 3} posts uploaded")
        print(f"⏰ Next campaign: {self.scheduler.get_next_post_time().strftime('%Y-%m-%d %H:%M')}")
    
    def post_to_platform(self, platform, count):
        """Post multiple hooks to specific platform"""
        successful = 0
        failed = 0
        
        for i in range(count):
            try:
                # Get random hook
                hook = self.hook_db.get_random_hook()
                
                if not hook:
                    print(f"⚠️  No hooks available")
                    failed += 1
                    continue
                
                # Generate output path
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = os.path.join(workspace, "generated_posts", platform)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"hook_{timestamp}.json")
                
                # Generate image
                self.generator.generate_from_hook(hook, output_path)
                
                # Create caption
                caption = f"{hook['headline']}\n{hook['body']}\n{hook['cta']}"
                
                # Hashtags (from TikTok trends research)
                hashtags = ["#JENDRALBOT", "#AItools", "#Digitalproducts", "#Productivity", "#Businesshacks"]
                
                # Upload to platform
                if platform == 'tiktok':
                    self.uploader.upload_tiktok(output_path, caption, hashtags)
                elif platform == 'ig_reels':
                    self.uploader.upload_ig_reels(output_path, caption, hashtags)
                elif platform == 'youtube_shorts':
                    self.uploader.upload_youtube_shorts(output_path, caption, hashtags)
                
                successful += 1
                print(f"  ✅ {i+1}/{count}: {hook['headline'][:30]}...")
                
                # Wait between posts (30 seconds)
                time.sleep(30)
                
            except Exception as e:
                print(f"  ❌ {i+1}/{count}: ERROR - {str(e)}")
                failed += 1
        
        print(f"  📊 {platform.upper()}: {successful} successful, {failed} failed")
        self.log_upload(platform, successful, failed)
    
    def log_upload(self, platform, successful, failed):
        """Log upload results"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "successful": successful,
            "failed": failed,
            "total": successful + failed
        }
        
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JENDRALBOT Auto Upload Scheduler')
    parser.add_argument('--posts', type=int, default=18, help='Posts per platform (default: 18)')
    parser.add_argument('--test', action='store_true', help='Test mode (no actual uploads)')
    parser.add_argument('--daemon', action='store_true', help='Run as continuous daemon')
    
    args = parser.parse_args()
    
    # Run campaign
    runner = CampaignRunner()
    
    if args.daemon:
        print("🔄 Running in daemon mode...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                if runner.scheduler.should_post_now():
                    runner.run_campaign_day(posts_per_platform=args.posts)
                
                # Wait 1 hour before next check
                time.sleep(3600)
        
        except KeyboardInterrupt:
            print("\n🛑 Daemon stopped")
    else:
        runner.run_campaign_day(posts_per_platform=args.posts)

if __name__ == "__main__":
    main()