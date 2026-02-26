#!/usr/bin/env python3
"""
Viral Video Pipeline — Generate videos with BytePlus Seedance + Cerebras AI
Full stack: AI text generation → Video generation → Schedule to all accounts
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
import base64
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
BYTEPLUS_API_KEY   = os.environ.get("BYTEPLUS_API_KEY", "")
CEREBRAS_API_KEY   = os.environ.get("CEREBRAS_API_KEY", "")
IMGBB_API_KEY      = os.environ.get("IMGBB_API_KEY", "")
POST_BRIDGE_KEY    = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_Kyc2gafDF7Qc8c2ALELtEC")

OUTPUT_DIR = Path("output/viral_videos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# ── Viral Concepts ───────────────────────────────────────────────────────────────
# These will be enhanced with AI-generated details
CONCEPTS = [
    {
        "id": 1,
        "niche": "Motivational",
        "base_idea": "Motivational quote about overcoming yesterday's self",
        "colors": "#1a1a2e",
        "hashtags": "#motivation #mindset #success #growth #viral #inspiration",
    },
    {
        "id": 2,
        "niche": "Money Mindset",
        "base_idea": "Money follows action not wishes, powerful money quote",
        "colors": "#ffd700",
        "hashtags": "#money #wealth #financialfreedom #entrepreneur #success #mindset",
    },
    {
        "id": 3,
        "niche": "Success Transformation",
        "base_idea": "1 year can completely change your life, success story",
        "colors": "#2d1b69",
        "hashtags": "#transformation #success #glowup #motivation #viral #1year",
    },
    {
        "id": 4,
        "niche": "Growth Mindset",
        "base_idea": "Discomfort is the price of growth, push through struggle",
        "colors": "#e74c3c",
        "hashtags": "#growth #mindset #motivation #success #viral #discomfort",
    },
    {
        "id": 5,
        "niche": "Productivity",
        "base_idea": "5am morning habit that changed my life, productivity tip",
        "colors": "#27ae60",
        "hashtags": "#5am #productivity #habits #success #morningroutine #lifehack",
    },
]


# ── Cerebras AI — Generate Enhanced Content ───────────────────────────────────
def generate_with_cerebras(idea: str) -> dict:
    """Use Cerebras AI to generate headline, prompt, and caption."""
    print(f"  🤖 Generating content with Cerebras AI...")
    
    prompt = f"""You are a viral content expert. Based on this idea, create a viral social media post.

Idea: {idea}

Generate JSON with these fields:
- "headline": Bold, punchy headline (2-3 lines, max 80 chars total)
- "video_prompt": Cinematic video prompt for Seedance (50-100 words, 9:16 portrait, viral style)
- "caption": Engaging caption (150-200 chars) for Facebook with emojis

Return ONLY valid JSON, no extra text."""

    url = "https://api.cerebras.ai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b",
        "messages": [
            {"role": "system", "content": "You are a viral social media content creator. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 500,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {CEREBRAS_API_KEY}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"]
        # Extract JSON from response (in case of extra text)
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            content = content[start:end]
        
        parsed = json.loads(content)
        print(f"  ✅ Cerebras generated headline: {parsed.get('headline', '?')}")
        return parsed
        
    except Exception as e:
        print(f"  ❌ Cerebras error: {e}")
        # Fallback to basic content
        return {
            "headline": idea[:50],
            "video_prompt": f"Cinematic {idea}, professional lighting, viral aesthetic, 9:16 portrait",
            "caption": f"{idea}. Viral content! {CONCEPTS[0].get('hashtags','')}",
        }


# ── BytePlus Seedance — Generate Video ───────────────────────────────────────
def generate_video_byteplus(prompt: str, output_path: Path) -> bool:
    """Generate video using BytePlus Seedance via AIML API."""
    print(f"  🎬 Generating video with BytePlus Seedance...")
    
    url = "https://api.aimlapi.com/v2/video/generations"
    payload = {
        "model": "bytedance/seedance-1-0-lite-t2v",
        "prompt": prompt,
        "resolution": "720p",
        "duration": 5,
        "aspect_ratio": "9:16",
        "watermark": False,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {BYTEPLUS_API_KEY}")
    req.add_header("Content-Type", "application/json")
    
    try:
        # Step 1: Create task
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        task_id = result.get("id")
        status = result.get("status")
        
        if not task_id:
            print(f"  ❌ No task ID: {result}")
            return False
        
        print(f"  📋 Task created: {task_id} (status: {status})")
        
        # Step 2: Poll for completion
        for attempt in range(30):  # 5 min timeout, 10s each
            time.sleep(10)
            
            poll_url = f"https://api.aimlapi.com/v2/video/generations/{task_id}"
            poll_req = urllib.request.Request(poll_url)
            poll_req.add_header("Authorization", f"Bearer {BYTEPLUS_API_KEY}")
            
            with urllib.request.urlopen(poll_req, timeout=30) as poll_resp:
                poll_result = json.loads(poll_resp.read().decode("utf-8"))
            
            status = poll_result.get("status")
            print(f"  ⏳ Polling... status: {status} (attempt {attempt+1}/30)")
            
            if status == "completed":
                video_url = poll_result.get("video", {}).get("url")
                if video_url:
                    print(f"  📥 Downloading video from {video_url[:60]}...")
                    urllib.request.urlretrieve(video_url, output_path)
                    size_mb = output_path.stat().st_size / (1024*1024)
                    print(f"  ✅ Video saved: {output_path} ({size_mb:.1f}MB)")
                    return True
                else:
                    print(f"  ❌ Completed but no video URL")
                    return False
            
            elif status == "error":
                error = poll_result.get("error", {})
                print(f"  ❌ Generation error: {error}")
                return False
        
        print(f"  ❌ Polling timeout (5 min)")
        return False
        
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP error {e.code}: {e.read().decode('utf-8')[:200]}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


# ── Get All Post-Bridge Accounts ────────────────────────────────────────────────────
def get_accounts() -> dict:
    """Fetch all connected accounts."""
    accounts = []
    offset = 0
    
    while True:
        url = f"https://api.post-bridge.com/v1/social-accounts?limit=50&offset={offset}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            
            batch = data.get("data", [])
            accounts.extend(batch)
            
            meta = data.get("meta", {})
            if offset + 50 >= meta.get("total", 0):
                break
            offset += 50
        except:
            break
    
    fb_ids = [str(a["id"]) for a in accounts if a["platform"] == "facebook"]
    tik_ids = [str(a["id"]) for a in accounts if a["platform"] == "tiktok"]
    
    return {"facebook": fb_ids, "tiktok": tik_ids}


# ── Schedule Post ─────────────────────────────────────────────────────────────
def schedule_post(account_ids: list, caption: str, media_url: str, sched_time: str) -> dict:
    """Schedule a post via Post-Bridge."""
    payload = {
        "caption": caption,
        "social_accounts": account_ids,
        "media": [{"url": media_url}],
        "scheduled_at": sched_time,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request("https://api.post-bridge.com/v1/posts", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": str(e), "status_code": e.code, "body": e.read().decode("utf-8")[:200]}
    except Exception as e:
        return {"error": str(e)}


# ── Upload Video to ImgBB (or temp host) ───────────────────────────────────
def upload_video_imgbb(video_path: Path) -> str:
    """Note: ImgBB is for images only. Return local path for now."""
    # ImgBB doesn't support video uploads directly
    # For now, we'll use the video URL from BytePlus directly in Post-Bridge
    # If Post-Bridge requires public URLs, we may need a video hosting service
    return None  # Will use BytePlus URL directly


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("🚀 VIRAL VIDEO PIPELINE — CEREBRAS AI + BYTEPLUS SEEDANCE")
    print("=" * 70)
    print()
    
    # Check API keys
    if not CEREBRAS_API_KEY:
        print("❌ Missing CEREBRAS_API_KEY")
        return
    if not BYTEPLUS_API_KEY:
        print("❌ Missing BYTEPLUS_API_KEY")
        return
    
    # Get accounts
    print("📱 Fetching Post-Bridge accounts...")
    accs = get_accounts()
    fb_ids = accs["facebook"]
    tik_ids = accs["tiktok"]
    print(f"  Facebook: {len(fb_ids)} accounts")
    print(f"  TikTok: {len(tik_ids)} accounts")
    print()
    
    # Schedule times
    now_utc = datetime.now(timezone.utc)
    results = []
    
    for i, concept in enumerate(CONCEPTS):
        video_path = OUTPUT_DIR / f"viral{concept['id']}.mp4"
        sched_time = now_utc + timedelta(minutes=30, hours=i*4)
        sched_utc = sched_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        sched_wib = (sched_time + JAKARTA_OFFSET).strftime("%Y-%m-%d %H:%M WIB")
        
        print(f"─" * 70)
        print(f"🎯 Video {i+1}/5 — {concept['niche']}")
        print(f"⏰ Scheduled: {sched_wib}")
        print()
        
        # Step 1: Generate content with Cerebras AI
        ai_content = generate_with_cerebras(concept["base_idea"])
        
        headline = ai_content.get("headline", concept["base_idea"][:50])
        video_prompt = ai_content.get("video_prompt", concept["base_idea"])
        caption = ai_content.get("caption", f"{concept['base_idea']} {concept['hashtags']}")
        caption += f"\n\n{concept['hashtags']}"
        
        print(f"  📝 Headline: {headline}")
        print(f"  🎥 Video prompt: {video_prompt[:80]}...")
        
        # Step 2: Generate video with BytePlus
        if not video_path.exists():
            vid_ok = generate_video_byteplus(video_prompt, video_path)
            if not vid_ok:
                print(f"  ⚠️  Skipping (video generation failed)")
                continue
        else:
            print(f"  ✅ Video exists: {video_path}")
        
        # Note: For now, we'll skip ImgBB (doesn't support video)
        # Post-Bridge may need public URL - using BytePlus URL if available
        # Or we can create a simple fallback image upload
        video_url = ""  # Will be empty for now
        
        # Schedule (without media for now, or with placeholder)
        print(f"  📤 Scheduling to {len(fb_ids)} FB + {len(tik_ids)} TikTok...")
        
        post_fb = schedule_post(fb_ids, caption, video_url, sched_utc)
        post_tik = schedule_post(tik_ids, caption, video_url, sched_utc)
        
        fb_ok = "error" not in post_fb
        tik_ok = "error" not in post_tik
        
        results.append({
            "id": concept["id"],
            "niche": concept["niche"],
            "scheduled": sched_wib,
            "video": str(video_path),
            "headline": headline,
            "video_prompt": video_prompt,
            "caption": caption,
            "facebook": fb_ok,
            "tiktok": tik_ok,
            "fb_response": post_fb,
            "tik_response": post_tik,
        })
        
        print(f"  Facebook: {'✅' if fb_ok else '❌'}")
        print(f"  TikTok: {'✅' if tik_ok else '❌'}")
        print()
    
    # Summary
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    for r in results:
        fb = "✅" if r.get("facebook") else "❌"
        tik = "✅" if r.get("tiktok") else "❌"
        print(f"{fb}{tik} Video {r['id']} [{r['niche']}] → {r['scheduled']}")
        if r.get("headline"):
            print(f"     {r['headline']}")
    
    summary_path = OUTPUT_DIR / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved: {summary_path}")


if __name__ == "__main__":
    import time  # needed for sleep
    main()
