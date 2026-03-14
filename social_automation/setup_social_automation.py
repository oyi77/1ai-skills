#!/usr/bin/env python3
"""
SOCIAL MEDIA AUTOMATION SETUP
Prepare social media posts for automated posting
"""

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
LEAD_GEN_DIR = WORKSPACE / "lead_gen_machine"
SOCIAL_DIR = WORKSPACE / "social_automation"

SOCIAL_DIR.mkdir(parents=True, exist_ok=True)

print("="*70)
print("📱 SOCIAL MEDIA AUTOMATION SETUP")
print("="*70)
print()

# Load latest campaign
campaigns = list((LEAD_GEN_DIR / "campaigns").glob("campaign_*.json"))
latest_campaign = max(campaigns, key=lambda f: f.stat().st_mtime)

print(f"[INFO] Loading campaign: {latest_campaign.name}")
with open(latest_campaign) as f:
    campaign = json.load(f)

generated_content = campaign.get('generated_content', [])

print(f"[INFO] Found {len(generated_content)} content items")
print()

# Organize by platform
tiktok_posts = []
instagram_posts = []
facebook_posts = []

for item in generated_content:
    social = item.get('social_posts', {})
    
    if 'tiktok' in social:
        tiktok_posts.append({
            "platform": "tiktok",
            "content": social['tiktok'],
            "business_name": item.get('business_name'),
            "campaign": campaign.get('campaign_id')
        })
    
    if 'instagram' in social:
        instagram_posts.append({
            "platform": "instagram",
            "content": social['instagram'],
            "business_name": item.get('platform_name'),
            "campaign": campaign.get('campaign_id')
        })
    
    if 'facebook' in social:
        facebook_posts.append({
            "platform": "facebook",
            "content": social['facebook'],
            "business_name": item.get('business_name'),
            "campaign": campaign.get('platform_id')
        })

print(f"[INFO] Posts by platform:")
print(f"   TikTok: {len(tiktok_posts)}")
print(f"   Instagram: {len(instagram_posts)}")
print(f"   Facebook: {len(facebook_posts)}")
print()

# Save platform-specific files
for platform, posts in [("tiktok", tiktok_posts), ("instagram", instagram_posts), ("facebook", facebook_posts)]:
    file_path = SOCIAL_DIR / f"{platform}_posts_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    
    with open(file_path, 'w') as f:
        data = {
            "platform": platform,
            "total_posts": len(posts),
            "campaign_id": campaign.get('campaign_id'),
            "posts": posts[:20],  # First 20
            "generated_at": datetime.now().isoformat()
        }
        json.dump(data, f, indent=2)
    
    # Also create text version for easy posting
    text_file = SOCIAL_DIR / f"{platform}_posts_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    
    with open(text_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write(f"{platform.upper()} POSTS - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("="*70 + "\n\n")
        f.write(f"Total posts: {len(posts)}\n")
        f.write(f"\nINSTRUCTIONS:\n")
        f.write(f"1. Copy each post\n")
        f.write(f"2. Post to {platform} at optimal time:\n")
        f.write(f"   • TikTok: 12:00-15:00 or 19:00-21:00\n")
        f.write(f"   • Instagram: 11:00-14:00 or 19:00-21:00\n")
        f.write(f"   • Facebook: 12:00-15:00 or 18:00-21:00\n")
        f.write(f"3. Engage with responses\n")
        f.write(f"4. DM interested people\n")
        f.write(f"5. Track comments and DMs\n\n")
        f.write("="*70 + "\n\n")
        
        for i, post in enumerate(posts[:20], 1):
            f.write(f"POST {i}\n")
            f.write(f"{'─'*70}\n\n")
            f.write(f"{post['content']}\n\n")
            f.write(f"{'='*70}\n\n")
    
    print(f"✅ {platform.title()} files saved: {file_path} (JSON) + {text_file} (TXT)")

print()
print("="*70)
print("📱 SOCIAL MEDIA AUTOMATION SETUP COMPLETE!")
print("="*70)
print()
print("MODE: MANUAL START (Ready to upgrade to full automation)")
print()
print(f"Platforms: TikTok, Instagram, Facebook")
print(f"Total posts: {len(tiktok_posts) + len(instagram_posts) + len(facebook_posts)}")
print()
print("🚀 READY TO POST:")
print()
print("Option 1: Manual post (current mode)")
print("  1. Open the TXT files above")
print("  2. Copy posts")
print("  3. Manually post to each platform")
print()
print("Option 2: Social Media Automation Skill (recommended)")
print("  1. Use social-media-upload skill")
print("  2. Upload all posts at once")
print("  3. Schedule for optimal times")
print()
print("Option 3: PostBridge Integration (JendralBot)")
print("  1. Use existing PostBridge integration")
print(" 2. Post to JendralBot accounts")
print("  3. Already integrated with autopilot")
print()
print("⚡ TO UPGRADE TO FULL AUTOMATION:")
print("   - Use social-media-upload skill")
print("   - Integrate with PostBridge")
print("   - Add more platforms (LinkedIn, Pinterest, Twitter)")
print("   - Set up scheduling algorithms")
print()