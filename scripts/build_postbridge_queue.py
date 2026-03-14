#!/usr/bin/env python3
"""
JENDRALBOT Post Bridge - Build Upload Queue
Creates queue.json for 156 posts to 10 connected accounts
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

workspace = os.path.expanduser("~/.openclaw/workspace")

# Account IDs (from auto_postbridge_v2.py - these should still be connected)
ACCOUNT_IDS = {
    'tiktok': '45648',
    'instagram': '47681',  # berkahkaryadigitalproduct
    'facebook': '47664'
}

# Account IDs from memory (if different)
# Instagram berkahkaryadigitalproduct: need to verify
# Facebook: 9 accounts (need to get all IDs)

# Platform connection status
PLATFORMS = ['instagram', 'facebook']  # TikTok maybe not in current setup

def load_hooks():
    """Load hooks from database"""
    hooks_path = os.path.join(workspace, "hooks/jendralbot_complete.json")
    
    with open(hooks_path, 'r') as f:
        db = json.load(f)
    
    hooks = []
    
    for product in db['products']:
        hooks_file = os.path.join(workspace, product['hooks_file'])
        
        if os.path.exists(hooks_file):
            with open(hooks_file, 'r') as hf:
                data = json.load(hf)
                for hook in data['hooks']:
                    hook['product'] = product['name']
                    hook['lynk'] = product['lynk']
                    hooks.append(hook)
    
    return hooks

def get_image_path(hook_index):
    """Get image file path"""
    images_dir = os.path.join(workspace, "generated_posts/images")
    return f"{images_dir}/hook_{hook_index:04d}_*.png"  # Wildcard for product name

def create_postbridge_queue(hooks, platforms=PLATFORMS):
    """Create Post Bridge upload queue"""
    print(f"\n📤 Creating Post Bridge upload queue...")
    print(f"   Total hooks: {len(hooks)}")
    print(f"   Platforms: {platforms}")
    print(f"   Accounts: Instagram berkahkaryadigitalproduct, Facebook (9 accounts)")
    print()
    
    queue = []
    base_time = datetime.now() + timedelta(minutes=10)  # Start 10 min from now
    
    for platform in platforms:
        account_id = ACCOUNT_IDS.get(platform)
        
        if not account_id:
            print(f"   ⚠️  No account ID for {platform}")
            continue
        
        for i, hook in enumerate(hooks):
            # Stagger posts (5 min apart)
            scheduled_time = base_time + timedelta(minutes=i*5)
            
            # Build caption
            caption = f"{hook['headline']}\n\n{hook['body']}\n\n{hook['cta']}\n{hook['lynk']}"
            
            # Add hashtags
            hashtags = "#JENDRALBOT #AItools #Digitalproducts #Businesshacks #Indonesia"
            caption = f"{caption}\n\n{hashtags}"
            
            queue_item = {
                "platform": platform,
                "type": "image",
                "schedule": {
                    "publish_at": scheduled_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "time_zone": "Asia/Jakarta"
                },
                "content": {
                    "caption": caption,
                    "hashtag": hashtags.split(),
                    "lynk_url": hook['lynk']
                },
                "media": {
                    "type": "image",
                    "path": get_image_path(i),
                    "format": "4:5 vertical",
                    "style": "Dark background, white text"
                },
                "metadata": {
                    "product": hook['product'],
                    "hook_type": hook['type'],
                    "headline": hook['headline'],
                    "hook_index": i,
                    "campaign_id": "jendralbot_phase1"
                }
            }
            
            # Add account
            if account_id:
                queue_item["account_id"] = account_id
            
            queue.append(queue_item)
            
            if (i+1) % 20 == 0:
                print(f"   Progress: {i+1}/{len(hooks)} items added to queue")
    
    return queue

def save_queue(queue):
    """Save queue to JSON file"""
    queue_path = os.path.join(workspace, "postbridge_queue_jendralbot.json")
    
    queue_data = {
        "campaign_id": "jendralbot_phase1",
        "campaign_name": "JENDRALBOT Automation Phase 1",
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "platforms": PLATFORMS,
        "accounts": ACCOUNT_IDS,
        "total_posts": len(queue),
        "posts": queue
    }
    
    with open(queue_path, 'w') as f:
        json.dump(queue_data, f, indent=2)
    
    print(f"\n✅ Queue saved to: {queue_path}")
    print(f"   Total posts: {len(queue)}")
    print(f"   Platforms: {', '.join(PLATFORMS)}")
    
    # Show breakdown by platform
    breakdown = {}
    for item in queue:
        platform = item['platform']
        breakdown[platform] = breakdown.get(platform, 0) + 1
    
    print(f"   Breakdown: {breakdown}")
    
    return queue_path

def main():
    """Main execution"""
    print("="*70)
    print("JENDRALBOT - Post Bridge Upload Queue Builder")
    print("="*70)
    
    # Load hooks
    hooks = load_hooks()
    print(f"✅ Loaded {len(hooks)} hooks")
    
    # Create queue
    queue = create_postbridge_queue(hooks)
    
    # Save queue
    queue_path = save_queue(queue)
    
    print("\n" + "="*70)
    print("📤 QUEUE READY FOR UPLOAD")
    print("="*70)
    print(f"\nNext step: Run Post Bridge upload script")
    print(f"\nTo upload manually:")
    print(f"  1. Load queue: {queue_path}")
    print(f"  2. Start posting to Instagram & Facebook")
    print(f"  3. Monitor LYNK dashboard: https://lynk.id/jendralbot")
    print(f"\nOr use auto_postbridge_v2.py:")
    print(f"  python3 auto_postbridge_v2.py")

if __name__ == "__main__":
    main()