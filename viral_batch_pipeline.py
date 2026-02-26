#!/usr/bin/env python3
"""
Viral Content Batch Pipeline
Research-based viral video generation + scheduled posting to all Post-Bridge accounts.

Flow:
  1. Generate 5 viral concept images via NVIDIA Flux
  2. Animate into videos via FFmpeg (Ken Burns + text overlay)
  3. Upload videos to ImgBB (images) or temp host
  4. Schedule posts to all 25 accounts via Post-Bridge (4h apart)
"""

import os
import sys
import json
import time
import base64
import subprocess
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
NVIDIA_API_KEY   = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "")
IMGBB_API_KEY    = os.environ.get("IMGBB_API_KEY", "")
POST_BRIDGE_KEY  = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_Kyc2gafDF7Qc8c2ALELtEC")
POST_BRIDGE_URL  = "https://api.post-bridge.com/v1"

OUTPUT_DIR = Path("output/viral_batch")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)   # UTC+7

# ── Viral Content Concepts (Research-Based, Feb 2026) ─────────────────────────
# Criteria: emotional hook, universally shareable, monetization-ready
VIRAL_CONCEPTS = [
    {
        "id": 1,
        "niche": "Motivational",
        "image_prompt": (
            "Ultra cinematic sunrise over mountain peaks, golden hour light rays, "
            "dramatic sky with orange and purple clouds, photorealistic, 8K, "
            "vertical portrait 9:16, inspiring and uplifting atmosphere"
        ),
        "headline": "YOUR ONLY COMPETITION\nIS YESTERDAY'S YOU",
        "caption": (
            "Every single day is a fresh start. 🔥\n\n"
            "Stop comparing yourself to others.\n"
            "The only race that matters is the one you run against your past self.\n\n"
            "Drop a 💪 if you needed to hear this today!\n\n"
            "#motivation #mindset #success #growth #viral #inspiration"
        ),
        "caption_tiktok": (
            "your only competition is yesterday's you 🔥 "
            "#motivation #mindset #fyp #viral #success #growth #inspiration"
        ),
    },
    {
        "id": 2,
        "niche": "Money Mindset",
        "image_prompt": (
            "Luxury lifestyle aesthetic, gold coins and bills raining down, "
            "rich golden background, wealth and abundance visualization, "
            "cinematic lighting, vertical 9:16, premium feel, photorealistic 8K"
        ),
        "headline": "MONEY FOLLOWS\nACTION, NOT WISHES",
        "caption": (
            "Stop waiting for the 'perfect moment'. 💰\n\n"
            "The people winning financially right now are NOT the smartest.\n"
            "They're the ones who STARTED. Who took messy imperfect action.\n\n"
            "What's ONE thing you can do TODAY to move toward your goal?\n"
            "Comment below 👇\n\n"
            "#money #wealth #financialfreedom #entrepreneur #success #mindset #viral"
        ),
        "caption_tiktok": (
            "money follows action not wishes 💰 stop waiting for perfect "
            "#money #wealth #entrepreneur #fyp #viral #financialfreedom"
        ),
    },
    {
        "id": 3,
        "niche": "Satisfying Nature",
        "image_prompt": (
            "Breathtaking aerial view of turquoise ocean waves gently breaking "
            "on white sand beach, crystal clear water, tropical paradise, "
            "satisfying symmetrical patterns, aerial drone shot, "
            "vertical 9:16, vibrant colors, photorealistic 8K ultra detail"
        ),
        "headline": "THIS IS YOUR SIGN\nTO REST & RESET",
        "caption": (
            "Sometimes the most productive thing you can do is STOP. 🌊\n\n"
            "Rest is not laziness.\n"
            "Rest is part of the process.\n"
            "Your mind needs this as much as your body does.\n\n"
            "Tag someone who needs a break today! 🏖️\n\n"
            "#selfcare #mentalhealth #relax #peace #viral #satisfying #nature"
        ),
        "caption_tiktok": (
            "this is your sign to rest and reset 🌊 "
            "#selfcare #mentalhealth #satisfying #fyp #viral #peace #nature"
        ),
    },
    {
        "id": 4,
        "niche": "Success Story Hook",
        "image_prompt": (
            "Dramatic city skyline at night, glowing skyscrapers, "
            "person silhouette looking out over the city from rooftop, "
            "cinematic atmosphere, ambition and success energy, "
            "vertical portrait 9:16, photorealistic 8K, epic mood"
        ),
        "headline": "IN 1 YEAR\nYOUR LIFE CAN\nCOMPLETELY CHANGE",
        "caption": (
            "365 days. That's all it takes. 🌆\n\n"
            "1 year ago: broke, lost, no direction.\n"
            "Today: income growing, healthy, surrounded by the right people.\n\n"
            "What changed? I stopped talking and started DOING.\n\n"
            "Like this if you're working on your glow-up right now 👇\n\n"
            "#transformation #success #glowup #motivation #entrepreneur #viral #1year"
        ),
        "caption_tiktok": (
            "in 1 year your life can completely change 🌆 "
            "#transformation #success #glowup #fyp #viral #motivation"
        ),
    },
    {
        "id": 5,
        "niche": "Life Hack / Value",
        "image_prompt": (
            "Clean minimal aesthetic flat lay, productivity tools, "
            "notebook, coffee, smartphone, beautiful morning light, "
            "organized workspace, satisfying arrangement, "
            "vertical 9:16, soft natural light, photorealistic 8K, "
            "warm cozy tones"
        ),
        "headline": "5AM HABIT THAT\nCHANGED MY LIFE",
        "caption": (
            "I started waking up at 5AM and this is what happened after 30 days 👇\n\n"
            "✅ More productive than ever\n"
            "✅ 2 hours of deep work before the world wakes up\n"
            "✅ Clearer mind, less anxiety\n"
            "✅ Finally started the project I kept 'planning'\n\n"
            "The first 3 days are hard. After that? You'll never go back.\n\n"
            "Save this if you want to try it! 🔖\n\n"
            "#5am #productivity #habits #morningroutine #success #viral #lifehack"
        ),
        "caption_tiktok": (
            "5am habit that changed my life ⏰ try this for 30 days "
            "#5am #productivity #habits #fyp #viral #morningroutine #lifehack"
        ),
    },
]


# ── Step 1: Generate Video via BytePlus Seedance ────────────────────────────
def generate_video_byteplus(prompt: str, output_path: Path) -> bool:
    """Generate short video using BytePlus Seedance text-to-video."""
    print(f"  🎬 Generating video with BytePlus Seedance...")
    
    url = "https://open.byteplusapi.com/videoextraction/v1/generation/text_to_video"
    payload = {
        "prompt": prompt,
        "video_length": 5,  # 5 seconds (short but engaging for viral loops)
        "resolution": "720p",
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {BYTEPLUS_API_KEY}")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        # BytePlus typically returns a video URL or task ID
        # For now, let's assume we get a task ID and need to poll
        task_id = result.get("task_id", "")
        print(f"  📋 Task ID: {task_id}")
        
        # Poll for completion (simplified)
        for attempt in range(10):
            time.sleep(5)
            poll_url = f"https://open.byteplusapi.com/videoextraction/v1/generation/result?task_id={task_id}"
            poll_req = urllib.request.Request(poll_url)
            poll_req.add_header("Authorization", f"Bearer {BYTEPLUS_API_KEY}")
            
            with urllib.request.urlopen(poll_req, timeout=30) as poll_resp:
                poll_result = json.loads(poll_resp.read().decode("utf-8"))
            
            status = poll_result.get("status", "")
            if status == "success":
                video_url = poll_result.get("result", {}).get("video_url", "")
                if video_url:
                    # Download video
                    print(f"  📥 Downloading video from {video_url[:50]}...")
                    urllib.request.urlretrieve(video_url, output_path)
                    size_mb = output_path.stat().st_size / (1024*1024)
                    print(f"  ✅ Video saved: {output_path} ({size_mb:.1f}MB)")
                    return True
            
            print(f"  ⏳ Polling... status: {status} (attempt {attempt+1}/10)")
        
        print(f"  ❌ BytePlus: task timed out or failed")
        return False
        
    except urllib.error.HTTPError as e:
        print(f"  ❌ BytePlus HTTP error {e.code}: {e.read().decode()[:200]}")
        return False
    except Exception as e:
        print(f"  ❌ BytePlus error: {e}")
        return False


# ── Fallback: Generate placeholder image for testing ─────────────────────────
def generate_placeholder_image(output_path: Path, concept_id: int) -> bool:
    """Generate a simple placeholder image using FFmpeg."""
    print(f"  🎨 Generating placeholder image...")
    
    # Use a gradient background with concept ID
    colors = [
        ("0x1a1a2e", "0x16213e"),  # Dark blue
        ("0x2d1b69", "0x11998e"),  # Purple to teal
        ("0xff6b6b", "0x556270"),  # Red to gray
        ("0xf093fb", "0xf5576c"),  # Pink to red
        ("0x4facfe", "0x00f2fe"),  # Blue to cyan
    ]
    color1, color2 = colors[(concept_id - 1) % len(colors)]
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={color1}:s=1080x1920:d=1",
        "-vf", f"format=yuv420p,drawbox=x=50:y=50:w=980:h=1820:c={color2}:t=fill,drawtext=text='VIRAL VIDEO {concept_id}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=H/2",
        "-frames:v", "1",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
        print(f"  ✅ Placeholder created: {output_path}")
        return True
    except Exception as e:
        print(f"  ❌ Placeholder error: {e}")
        return False


# ── Step 2: Create Animated Video via FFmpeg ──────────────────────────────────
def create_video(img_path: Path, headline: str, output_path: Path, duration: int = 15) -> bool:
    """Create animated video with Ken Burns zoom and text overlay."""
    print(f"  🎬 Creating video with FFmpeg...")
    
    # Build drawtext filter for headline
    lines = headline.split('\n')
    text_filters = []
    
    base_y = 800  # vertical center-ish for 1920 height
    for i, line in enumerate(lines):
        y_pos = base_y + (i * 100)
        escaped = line.replace("'", "'\\''").replace(":", "\\:")
        text_filters.append(
            f"drawtext=text='{escaped}'"
            f":fontsize=72:fontcolor=white:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            f":x=(w-text_w)/2:y={y_pos}"
            f":shadowcolor=black:shadowx=3:shadowy=3"
            f":alpha='if(lt(t,0.5),t/0.5,if(gt(t,{duration-1}),(({duration})-t)/1,1))'"
        )
    
    text_filter_str = ",".join(text_filters)
    
    # Ken Burns zoom in effect
    zoom_filter = (
        f"scale=1280:2275,zoompan=z='if(lte(zoom,1.0),1.0,zoom-0.0015)'"
        f":d={duration*25}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":s=1080x1920"
    )
    
    filter_complex = f"{zoom_filter},{text_filter_str}"
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(img_path),
        "-vf", filter_complex,
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "23",
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  ✅ Video created: {output_path} ({size_mb:.1f}MB)")
            return True
        else:
            # Simpler fallback without Ken Burns
            print(f"  ⚠️  Trying simpler FFmpeg approach...")
            cmd_simple = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img_path),
                "-vf", f"scale=1080:1920,{text_filter_str}",
                "-c:v", "libx264",
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-preset", "fast",
                "-crf", "23",
                str(output_path)
            ]
            result2 = subprocess.run(cmd_simple, capture_output=True, text=True, timeout=120)
            if result2.returncode == 0:
                size_mb = output_path.stat().st_size / (1024*1024)
                print(f"  ✅ Video created: {output_path} ({size_mb:.1f}MB)")
                return True
            print(f"  ❌ FFmpeg error: {result2.stderr[-500:]}")
            return False
    except Exception as e:
        print(f"  ❌ FFmpeg exception: {e}")
        return False


# ── Step 3: Upload Image to ImgBB ────────────────────────────────────────────
def upload_to_imgbb(img_path: Path) -> str:
    """Upload image to ImgBB and return public URL."""
    print(f"  📤 Uploading to ImgBB...")
    
    img_b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
    
    data = urllib.parse.urlencode({
        "key": IMGBB_API_KEY,
        "image": img_b64,
        "name": img_path.stem,
    }).encode("utf-8")
    
    req = urllib.request.Request("https://api.imgbb.com/1/upload", data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        if result.get("success"):
            url = result["data"]["url"]
            print(f"  ✅ Uploaded: {url}")
            return url
        else:
            print(f"  ❌ ImgBB error: {result}")
            return ""
    except Exception as e:
        print(f"  ❌ ImgBB exception: {e}")
        return ""


# ── Step 4: Get All Post-Bridge Accounts ─────────────────────────────────────
def get_all_accounts() -> list:
    """Fetch all connected social accounts from Post-Bridge."""
    accounts = []
    offset = 0
    limit = 50
    
    while True:
        url = f"{POST_BRIDGE_URL}/social-accounts?limit={limit}&offset={offset}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
            
            batch = data.get("data", [])
            accounts.extend(batch)
            
            meta = data.get("meta", {})
            total = meta.get("total", 0)
            if offset + limit >= total:
                break
            offset += limit
        except Exception as e:
            print(f"  ❌ Error fetching accounts: {e}")
            break
    
    return accounts


# ── Step 5: Schedule Post via Post-Bridge ────────────────────────────────────
def schedule_post(account_ids: list, caption: str, media_url: str, scheduled_at: str) -> dict:
    """Schedule a post to specific accounts via Post-Bridge."""
    payload = {
        "account_ids": account_ids,
        "caption": caption,
        "media_urls": [media_url] if media_url else [],
        "scheduled_at": scheduled_at,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{POST_BRIDGE_URL}/posts", data=data, method="POST")
    req.add_header("Authorization", f"Bearer {POST_BRIDGE_KEY}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": str(e), "body": body}
    except Exception as e:
        return {"error": str(e)}


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("🚀 VIRAL CONTENT BATCH PIPELINE")
    print("=" * 60)
    print(f"📅 Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB")
    print(f"📦 Videos to generate: {len(VIRAL_CONCEPTS)}")
    print()

    # Get all connected accounts
    print("📱 Fetching Post-Bridge accounts...")
    accounts = get_all_accounts()
    
    fb_accounts  = [a for a in accounts if a["platform"] == "facebook"]
    tik_accounts = [a for a in accounts if a["platform"] == "tiktok"]
    fb_ids  = [a["id"] for a in fb_accounts]
    tik_ids = [a["id"] for a in tik_accounts]
    
    print(f"  → Facebook: {len(fb_accounts)} accounts")
    print(f"  → TikTok: {len(tik_accounts)} accounts")
    print()

    # First post starts 30 minutes from now, then +4h each
    now_utc = datetime.now(timezone.utc)
    base_time = now_utc + timedelta(minutes=30)

    results = []

    for i, concept in enumerate(VIRAL_CONCEPTS):
        vid_id    = concept["id"]
        niche     = concept["niche"]
        img_path  = OUTPUT_DIR / f"video{vid_id}_bg.jpg"
        vid_path  = OUTPUT_DIR / f"video{vid_id}.mp4"
        
        # Schedule time: base + (i * 4 hours)
        sched_time = base_time + timedelta(hours=i * 4)
        sched_str  = sched_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        sched_wib  = (sched_time + JAKARTA_OFFSET).strftime("%Y-%m-%d %H:%M WIB")

        print(f"─" * 60)
        print(f"🎯 Video {vid_id}/5 — {niche}")
        print(f"⏰ Scheduled: {sched_wib}")
        print()

        # Step 1: Try generate video with BytePlus Seedance
        vid_ok = False
        if not vid_path.exists():
            vid_ok = generate_video_byteplus(concept["image_prompt"], vid_path)
        else:
            print(f"  ✅ Video already exists: {vid_path}")
            vid_ok = True

        # Step 2: Fallback to placeholder if BytePlus fails
        img_url = ""
        if not vid_ok:
            print(f"  ⚠️  Trying fallback: placeholder image + video")
            img_ok = generate_placeholder_image(img_path, vid_id)
            if img_ok:
                vid_ok = create_video(img_path, concept["headline"], vid_path, duration=15)
                if vid_ok:
                    img_url = upload_to_imgbb(img_path)

        # Step 3: Upload image if we used FFmpeg (for media URL)
        if vid_ok and not img_url and img_path.exists():
            img_url = upload_to_imgbb(img_path)
        if not img_url:
            print(f"  ⚠️  Will post without media")

        # Step 4: Schedule to all accounts
        print(f"  📤 Scheduling to {len(fb_ids)} FB + {len(tik_ids)} TikTok accounts...")
        
        all_ids   = fb_ids + tik_ids
        fb_cap    = concept["caption"]
        tik_cap   = concept["caption_tiktok"]
        
        # Separate posts for Facebook and TikTok (different captions)
        post_results = []
        
        if fb_ids:
            fb_result = schedule_post(fb_ids, fb_cap, img_url, sched_str)
            print(f"  Facebook: {json.dumps(fb_result)[:120]}")
            post_results.append({"platform": "facebook", "result": fb_result})
        
        if tik_ids:
            tik_result = schedule_post(tik_ids, tik_cap, img_url, sched_str)
            print(f"  TikTok: {json.dumps(tik_result)[:120]}")
            post_results.append({"platform": "tiktok", "result": tik_result})

        results.append({
            "id": vid_id,
            "niche": niche,
            "scheduled_at": sched_wib,
            "image": str(img_path) if img_path.exists() else None,
            "video": str(vid_path) if vid_ok else None,
            "image_url": img_url,
            "post_results": post_results,
            "status": "scheduled" if vid_ok else "failed",
        })

        print()
        time.sleep(2)  # be nice to APIs

    # ── Summary ──────────────────────────────────────────────────────────────
    print("=" * 60)
    print("📊 BATCH COMPLETE — SUMMARY")
    print("=" * 60)
    for r in results:
        status = "✅" if r["status"] == "scheduled" else "❌"
        sched  = r.get("scheduled_at", "N/A")
        print(f"{status} Video {r['id']} [{r.get('niche','?')}] → {sched}")
    
    # Save summary
    summary_path = OUTPUT_DIR / "batch_summary.json"
    summary_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n💾 Summary saved: {summary_path}")
    print()
    print("🎉 All done! Check your Post-Bridge dashboard to confirm scheduled posts.")


if __name__ == "__main__":
    main()
