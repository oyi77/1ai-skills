#!/usr/bin/env python3
"""
Create videos from PIL images using FFmpeg pan/zoom effects
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
import urllib.request
import urllib.parse

INPUT_DIR = Path("output/viral_pil")
OUTPUT_DIR = Path("output/viral_videos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMGBB_API_KEY = "8af9af090dc96e01640ba68b246759ba"
POST_BRIDGE_KEY = "pb_live_Kyc2gafDF7Qc8c2ALELtEC"

JAKARTA_OFFSET = timedelta(hours=7)

# Viral concepts with captions
CONCEPTS = [
    {
        "id": 1,
        "niche": "Motivational",
        "img_file": "viral1.jpg",
        "caption": "Every single day is a fresh start. Stop comparing yourself to others. The only race that matters is one you run against your past self. Drop a 💪 if you needed to hear this today! #motivation #mindset #success #growth #viral",
    },
    {
        "id": 2,
        "niche": "Money Mindset",
        "img_file": "viral2.jpg",
        "caption": "Stop waiting for the 'perfect moment'. The people winning financially are NOT the smartest. They're the ones who STARTED. What's ONE thing you can do TODAY? Comment below 👇 #money #wealth #entrepreneur #success #mindset",
    },
    {
        "id": 3,
        "niche": "Success Mindset",
        "img_file": "viral3.jpg",
        "caption": "365 days. That's all it takes. I stopped talking and started DOING. Like this if you're working on your glow-up right now 👇 #transformation #success #glowup #motivation #viral",
    },
    {
        "id": 4,
        "niche": "Growth Mindset",
        "img_file": "viral4.jpg",
        "caption": "Nothing grows in the comfort zone. Every breakthrough starts with being uncomfortable. Embrace the struggle. Growth is waiting on the other side. 💪 #growth #mindset #motivation #success #viral",
    },
    {
        "id": 5,
        "niche": "Productivity",
        "img_file": "viral5.jpg",
        "caption": "Started waking up at 5AM: more productive, clearer mind, less anxiety. First 3 days are hard. After that, you'll never go back. Save this if you want to try it! 🔖 #5am #productivity #habits #success",
    },
]

def create_video_from_image(img_path: Path, output_path: Path) -> bool:
    """Create 15s video with pan/zoom effect."""
    print(f"  🎬 Creating video: {img_path.name}")
    
    # Create a video with subtle pan/zoom effect
    # Input: 1080x1920, output: 1080x1920
    # Effect: Zoom in slowly over 15 seconds
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(img_path),
        "-vf",
        "scale=1080:1920, "
        "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=15:s=1080x1920:fps=30",
        "-c:v", "libx264",
        "-t", "15",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "23",
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  ✅ Video created: {output_path.name} ({size_mb:.1f}MB)")
            return True
        else:
            # Fallback: simple output without zoom
            print(f"  ⚠️  Trying simple output...")
            cmd_simple = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img_path),
                "-vf", "scale=1080:1920",
                "-c:v", "libx264",
                "-t", "15",
                "-pix_fmt", "yuv420p",
                "-preset", "fast",
                "-crf", "23",
                str(output_path)
            ]
            result2 = subprocess.run(cmd_simple, capture_output=True, text=True, timeout=60)
            if result2.returncode == 0:
                size_mb = output_path.stat().st_size / (1024*1024)
                print(f"  ✅ Video created: {output_path.name} ({size_mb:.1f}MB)")
                return True
            print(f"  ❌ FFmpeg error: {result2.stderr[-200:]}")
            return False
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False


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


def schedule_post(account_ids: list, caption: str, media_url: str, sched_time: str) -> dict:
    """Schedule a post."""
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


def main():
    print("=" * 70)
    print("🎬 CREATING VIDEOS FROM PIL IMAGES")
    print("=" * 70)
    print()
    
    # Check if input images exist
    if not INPUT_DIR.exists():
        print(f"❌ Input directory not found: {INPUT_DIR}")
        return
    
    # Get accounts
    print("📱 Fetching accounts...")
    accs = get_accounts()
    fb_ids = accs["facebook"]
    tik_ids = accs["tiktok"]
    print(f"  Facebook: {len(fb_ids)} accounts")
    print(f"  TikTok: {len(tik_ids)} accounts")
    print()
    
    now_utc = datetime.now(timezone.utc)
    results = []
    
    for i, concept in enumerate(CONCEPTS):
        img_path = INPUT_DIR / concept["img_file"]
        vid_path = OUTPUT_DIR / f"video{concept['id']}.mp4"
        
        sched_time = now_utc + timedelta(minutes=30, hours=i*4)
        sched_utc = sched_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        sched_wib = (sched_time + JAKARTA_OFFSET).strftime("%Y-%m-%d %H:%M WIB")
        
        print(f"─" * 70)
        print(f"🎯 Video {i+1}/5 — {concept['niche']}")
        print(f"⏰ Scheduled: {sched_wib}")
        print()
        
        if not img_path.exists():
            print(f"  ⚠️  Image not found: {img_path}")
            continue
        
        # Create video
        if not vid_path.exists():
            ok = create_video_from_image(img_path, vid_path)
            if not ok:
                print(f"  ⚠️  Skipping")
                continue
        else:
            print(f"  ✅ Video exists")
        
        # Schedule without media (for now)
        print(f"  📤 Scheduling (text only for now)...")
        post_fb = schedule_post(fb_ids, concept["caption"], "", sched_utc)
        post_tik = schedule_post(tik_ids, concept["caption"], "", sched_utc)
        
        fb_ok = "error" not in post_fb
        tik_ok = "error" not in post_tik
        
        results.append({
            "id": concept["id"],
            "niche": concept["niche"],
            "scheduled": sched_wib,
            "video": str(vid_path),
            "facebook": fb_ok,
            "tiktok": tik_ok,
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
        print(f"     📁 {r.get('video')}")
    
    # List video files
    print()
    print("📁 Generated videos:")
    vid_files = list(OUTPUT_DIR.glob("*.mp4"))
    for v in sorted(vid_files):
        size_mb = v.stat().st_size / (1024*1024)
        print(f"  - {v.name} ({size_mb:.1f}MB)")
    
    summary_path = OUTPUT_DIR / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Summary saved: {summary_path}")


if __name__ == "__main__":
    main()
