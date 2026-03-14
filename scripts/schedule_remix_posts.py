#!/usr/bin/env python3
"""
Schedule REMIX restoration videos via PostBridge API
Routes content to correct account categories per mapping
"""
import requests
import json
import os
import sys
from datetime import datetime, timedelta

API_KEY = "pb_live_AFm842jzqKVNjREpJH8hTi"
BASE_URL = "https://api.post-bridge.com/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Account mapping per category
RESTORATION_ACCOUNTS = {
    "youtube": [49639, 49660],      # BK METAL, berkah karya digital agency
    "tiktok": [49663],               # bkjaya00
    "instagram": [49661],            # bkjayautama
    "threads": [49662],              # bkjayautama
}

# Facebook engagement for viral clips
FB_ENGAGEMENT = [49675, 49672, 49671, 49670, 49669, 49668, 49667, 49666, 49665, 49664]

DIGITAL_PRODUCT_ACCOUNTS = {
    "youtube": [49816],              # Algo Expert Hub
    "twitter": [49814],              # algoexperthub
    "instagram": [49810, 48186],     # algoexperthub, berkahkaryadigitalproduct
    "threads": [49811, 49680],       # algoexperthub, berkahkaryadigitalproduct
    "tiktok": [45648],               # jasakontenai
}

def upload_media(filepath):
    """Upload media to PostBridge and return media_id"""
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    # Step 1: Create upload URL
    print(f"  Creating upload URL for {filename} ({filesize/1024/1024:.1f}MB)...")
    resp = requests.post(f"{BASE_URL}/media/create-upload-url", 
                        headers=HEADERS,
                        json={"filename": filename, "content_type": "video/mp4"})
    
    if resp.status_code != 200 and resp.status_code != 201:
        print(f"  ❌ Failed to create upload URL: {resp.status_code} {resp.text[:200]}")
        return None
    
    data = resp.json()
    upload_url = data.get("upload_url") or data.get("url")
    media_id = data.get("media_id") or data.get("id")
    
    if not upload_url:
        print(f"  ❌ No upload URL in response: {json.dumps(data)[:200]}")
        return None
    
    # Step 2: Upload file
    print(f"  Uploading to storage...")
    with open(filepath, "rb") as f:
        upload_resp = requests.put(upload_url, data=f, 
                                   headers={"Content-Type": "video/mp4"})
    
    if upload_resp.status_code not in [200, 201, 204]:
        print(f"  ❌ Upload failed: {upload_resp.status_code}")
        return None
    
    print(f"  ✅ Uploaded! media_id={media_id}")
    return media_id


def create_post(caption, social_accounts, media_ids=None, scheduled_at=None, media_urls=None):
    """Create a post via PostBridge"""
    payload = {
        "caption": caption,
        "social_accounts": social_accounts,
    }
    
    if media_ids:
        payload["media"] = media_ids
    if media_urls:
        payload["media_urls"] = media_urls
    if scheduled_at:
        payload["scheduled_at"] = scheduled_at
    
    resp = requests.post(f"{BASE_URL}/posts", headers=HEADERS, json=payload)
    
    if resp.status_code in [200, 201]:
        data = resp.json()
        post_id = data.get("id") or data.get("post_id", "?")
        print(f"  ✅ Post created: ID={post_id}")
        return data
    else:
        print(f"  ❌ Post failed: {resp.status_code} {resp.text[:300]}")
        return None


def schedule_text_posts():
    """Schedule text-based posts (for platforms that support text-only)"""
    
    # Digital Product promo posts (text + link)
    product_posts = [
        {
            "caption": "🔥 500 Viral TikTok Hook Templates — READY TO USE!\n\nStop spending HOURS thinking of hooks. Get 500 proven templates that grab attention in 3 seconds.\n\n✅ 10 Categories (Storytelling, Controversy, Tutorial...)\n✅ Fill-in-the-blank format\n✅ Works for ANY niche\n\n📥 Get it now: https://lynk.id/jendralbot\n\n#tiktok #contentcreator #viraltiktok #socialmediatips #hooks #marketing",
            "accounts": (DIGITAL_PRODUCT_ACCOUNTS["twitter"] + 
                        DIGITAL_PRODUCT_ACCOUNTS["threads"] +
                        DIGITAL_PRODUCT_ACCOUNTS.get("tiktok", []))
        },
        {
            "caption": "🎓 AI Content Creation Masterclass — From Zero to Pro\n\n127-page complete guide covering:\n📌 ChatGPT prompt engineering\n📌 AI video generation (Runway, Pika, Kling)\n📌 AI image creation for marketing\n📌 Automation workflows\n📌 Monetization strategies\n\nPerfect for creators who want to 10x output with AI.\n\n📥 Link in bio: https://lynk.id/jendralbot\n\n#ai #contentcreation #masterclass #chatgpt #aitools #digitalproduct",
            "accounts": (DIGITAL_PRODUCT_ACCOUNTS["twitter"] + 
                        DIGITAL_PRODUCT_ACCOUNTS["threads"])
        },
        {
            "caption": "💡 Did you know? The average TikTok creator spends 45 minutes thinking of a hook.\n\nWith our 500 Hook Templates, that drops to 30 SECONDS.\n\nReal templates. Real results. Plug and play.\n\n🔗 https://lynk.id/jendralbot\n\n#productivity #tiktokgrowth #contentmarketing #templates",
            "accounts": (DIGITAL_PRODUCT_ACCOUNTS["twitter"] + 
                        DIGITAL_PRODUCT_ACCOUNTS["threads"] + 
                        [49658])  # berkahkaryadigitalmarketing threads
        }
    ]
    
    # Restoration teaser posts (text for threads/twitter)
    restoration_posts = [
        {
            "caption": "🔧 New on our channel: ZB 1940 Machine Gun — buried for 80 YEARS, restored to museum quality.\n\nEvery rust particle removed. Every mechanism rebuilt.\n\nFull video on YouTube → BK METAL\n\n#restoration #wwii #military #satisfying #history",
            "accounts": RESTORATION_ACCOUNTS["threads"] + [49658]
        },
        {
            "caption": "⚔️ Legendary Mauser K-98 German Rifle — from battlefield RELIC to museum MASTERPIECE.\n\nThe full restoration journey is INSANE.\n\nWatch now on YouTube → BK METAL\n\n#mauser #k98 #gunrestoration #wwii #history #craftsmanship",
            "accounts": RESTORATION_ACCOUNTS["threads"] + [49658]
        },
        {
            "caption": "🚛 Remember Mack from Disney's Cars? We found a REAL rusted Mack truck and restored it from scratch.\n\nFrom junkyard wreck to road legend.\n\nFull video → YouTube BK METAL\n\n#mack #cars #disney #restoration #trucking #satisfying",
            "accounts": RESTORATION_ACCOUNTS["threads"] + [49658]
        }
    ]
    
    now = datetime.utcnow()
    all_posts = product_posts + restoration_posts
    results = {"success": 0, "failed": 0}
    
    for i, post in enumerate(all_posts):
        # Schedule 30 min apart starting 1 hour from now
        schedule_time = now + timedelta(hours=1, minutes=30*i)
        scheduled_at = schedule_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        print(f"\n📝 Post {i+1}/{len(all_posts)} — scheduled {scheduled_at}")
        print(f"   Accounts: {post['accounts']}")
        print(f"   Caption: {post['caption'][:80]}...")
        
        result = create_post(
            caption=post["caption"],
            social_accounts=post["accounts"],
            scheduled_at=scheduled_at
        )
        
        if result:
            results["success"] += 1
        else:
            results["failed"] += 1
    
    return results


def main():
    print("=" * 60)
    print("🚀 POSTBRIDGE CONTENT SCHEDULER")
    print("=" * 60)
    
    # Phase 1: Schedule text posts (no upload needed)
    print("\n📝 PHASE 1: Text Posts (Digital Products + Restoration Teasers)")
    print("-" * 40)
    text_results = schedule_text_posts()
    print(f"\n✅ Text posts: {text_results['success']} success, {text_results['failed']} failed")
    
    # Phase 2: Upload TikTok clips for video posts
    clips_dir = "/home/openclaw/.openclaw/workspace/remix_factory/clips"
    clips = [
        os.path.join(clips_dir, "zb1940_short1_hook.mp4"),
        os.path.join(clips_dir, "zb1940_short2_transform.mp4"),
        os.path.join(clips_dir, "zb1940_short3_reveal.mp4"),
    ]
    
    existing_clips = [c for c in clips if os.path.exists(c)]
    
    if existing_clips:
        print(f"\n🎬 PHASE 2: Video Clips Upload ({len(existing_clips)} clips)")
        print("-" * 40)
        
        for clip in existing_clips:
            print(f"\nUploading: {os.path.basename(clip)}")
            media_id = upload_media(clip)
            
            if media_id:
                # Post clip to TikTok + IG restoration accounts
                clip_name = os.path.basename(clip)
                if "hook" in clip_name:
                    caption = "They said this gun was IMPOSSIBLE to restore... 😱🔧\n\n#restoration #wwii #satisfying #asmr #military #viral"
                elif "transform" in clip_name:
                    caption = "The transformation is INSANE 🔥 Watch every detail come back to life\n\n#restoration #satisfying #asmr #process #craftsmanship"
                else:
                    caption = "80 years buried... NOW LOOK AT IT ✨\n\nFull video on YouTube → BK METAL\n\n#restoration #reveal #beforeandafter #satisfying #military"
                
                # TikTok + IG (need media)
                video_accounts = (RESTORATION_ACCOUNTS["tiktok"] + 
                                 RESTORATION_ACCOUNTS["instagram"])
                
                schedule_time = datetime.utcnow() + timedelta(hours=2, minutes=30*existing_clips.index(clip))
                scheduled_at = schedule_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                
                print(f"  Scheduling to TikTok+IG: {video_accounts}")
                create_post(
                    caption=caption,
                    social_accounts=video_accounts,
                    media_ids=[media_id],
                    scheduled_at=scheduled_at
                )
    else:
        print("\n⚠️ No clips found for upload, skipping Phase 2")
    
    print("\n" + "=" * 60)
    print("🏁 SCHEDULING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
