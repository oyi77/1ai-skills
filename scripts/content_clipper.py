#!/usr/bin/env python3
"""
Content Clipper Pipeline — Download viral content, remix unique, clean metadata, schedule.

Usage:
  python3 scripts/content_clipper.py --niche health --count 50
  python3 scripts/content_clipper.py --niche electronics --count 30
  python3 scripts/content_clipper.py --niche restoration --count 100
  python3 scripts/content_clipper.py --niche health --count 50 --schedule
"""

import os, json, sys, subprocess, random, time, ssl, urllib.request, urllib.error, hashlib, re
from pathlib import Path
from datetime import datetime, timedelta, timezone

FFMPEG = "/usr/bin/ffmpeg"
YTDLP = "/home/openclaw/.local/bin/yt-dlp"
EXIFTOOL = "/usr/bin/exiftool"
CTX = ssl.create_default_context()

PB_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
PB_BASE = "https://api.post-bridge.com/v1"

OUTPUT_BASE = Path("/home/openclaw/.openclaw/workspace/output/clipper")
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

# ─── Niche configs ───
NICHES = {
    "health": {
        "search_queries": [
            "tips kesehatan viral tiktok",
            "healthy lifestyle tips short",
            "home remedy natural health",
            "morning routine sehat",
            "diet tips indonesia viral",
            "workout di rumah shorts",
            "herbal alami untuk kesehatan",
            "tips tidur berkualitas",
            "detox alami tubuh",
            "makanan sehat murah",
            "cara menurunkan berat badan alami",
            "tips kulit glowing alami",
            "olahraga ringan di rumah",
            "minuman sehat pagi hari",
            "yoga pemula indonesia",
        ],
        "accounts": [49642, 48372, 48338, 48373, 48335, 48177],
        "hashtags": "#TipsKesehatan #SehatAlami #HealthTips #HidupSehat #Wellness #KesehatanTubuh #TipsSehat #GayaHidupSehat",
        "captions": [
            "💊 Tips kesehatan yang WAJIB kamu tau!\n\nSave & Share! 📌\n\n{hashtags}",
            "🌿 Rahasia hidup sehat yang jarang diketahui\n\nCoba dan rasakan bedanya! ✨\n\n{hashtags}",
            "💪 Jaga kesehatan itu investasi terbaik\n\nTag teman yang butuh ini! 🏷️\n\n{hashtags}",
            "🍃 Tips alami untuk tubuh lebih sehat\n\nSimple tapi POWERFUL! 🔥\n\n{hashtags}",
            "❤️ Kesehatan nomor 1! Coba tips ini\n\nComment kalau bermanfaat! 💬\n\n{hashtags}",
        ],
    },
    "electronics": {
        "search_queries": [
            "gadget review indonesia shorts",
            "tech unboxing viral tiktok",
            "smartphone tips tricks shorts",
            "laptop review murah shorts",
            "earbuds TWS review shorts",
            "gadget murah berkualitas viral",
            "tech hack indonesia",
            "review smartwatch murah",
            "powerbank terbaik review",
            "aksesoris hp viral tiktok",
            "speaker bluetooth review shorts",
            "keyboard mechanical murah",
            "mouse gaming review shorts",
            "charger fast charging review",
            "gadget unik viral 2026",
        ],
        "accounts": [49816],  # grahaelektroniktws (YouTube) - actually need the right ID
        "hashtags": "#GadgetReview #TechIndonesia #ReviewGadget #ElectronicsReview #TechTips #GadgetMurah #Unboxing",
        "captions": [
            "🔌 Gadget ini WORTH IT banget!\n\nWorth the price? Comment! 💬\n\n{hashtags}",
            "📱 Review jujur gadget viral!\n\nBeli atau skip? 🤔\n\n{hashtags}",
            "⚡ Tech tip yang bikin hidup lebih mudah\n\nSave untuk referensi! 📌\n\n{hashtags}",
            "🎧 Gadget murah tapi kualitas WOW\n\nLink di bio! 🔗\n\n{hashtags}",
            "💡 Review gadget hari ini\n\nSubscribe untuk review lainnya! 🔔\n\n{hashtags}",
        ],
    },
    "restoration": {
        "search_queries": [
            "restoration satisfying shorts",
            "rust removal satisfying viral",
            "metal restoration asmr",
            "car restoration shorts",
            "tool restoration viral",
            "knife restoration satisfying",
            "vintage restoration shorts",
            "gun cleaning restoration",
            "old tool makeover shorts",
            "rusty to shiny transformation",
            "antique restoration viral",
            "engine restoration shorts",
            "motorcycle restoration timelapse",
            "furniture restoration satisfying",
            "watch restoration viral",
        ],
        "accounts": [49660],  # berkah karya digital agency YT + bkjaya TikTok etc
        "hashtags": "#Restoration #Satisfying #RestoreIt #DIY #BeforeAfter #Transformation #ASMR #SatisfyingVideo",
        "captions": [
            "🔧 From rusty to BRAND NEW!\n\nSatisfying? 😍\n\n{hashtags}",
            "✨ Restoration magic! Watch till the end\n\nLike if satisfied! 👍\n\n{hashtags}",
            "🛠️ Old → NEW transformation\n\nWhich part was most satisfying? Comment! 💬\n\n{hashtags}",
            "⚡ The satisfaction of restoration\n\nSave this! 📌\n\n{hashtags}",
            "🔥 Best restoration you'll see today\n\nFollow for more! ➕\n\n{hashtags}",
        ],
    },
}


def search_videos(query, max_results=10):
    """Search YouTube for short videos."""
    cmd = [
        YTDLP,
        f"ytsearch{max_results}:{query}",
        "--print", "%(id)s|||%(title)s|||%(duration)s|||%(view_count)s",
        "--no-download",
        "--match-filter", "duration<=120",  # Max 2 min
        "--match-filter", "duration>=10",   # Min 10s
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        videos = []
        for line in result.stdout.strip().split("\n"):
            if "|||" in line:
                parts = line.split("|||")
                if len(parts) >= 4:
                    videos.append({
                        "id": parts[0],
                        "title": parts[1],
                        "duration": parts[2],
                        "views": parts[3],
                    })
        return videos
    except Exception as e:
        print(f"  Search error: {e}")
        return []


def download_video(video_id, output_dir):
    """Download video."""
    output_path = str(output_dir / f"raw_{video_id}.mp4")
    if os.path.exists(output_path):
        return output_path
    
    cmd = [
        YTDLP,
        f"https://youtube.com/watch?v={video_id}",
        "-f", "best[height<=1080][ext=mp4]/best[ext=mp4]/best",
        "-o", output_path,
        "--no-playlist",
        "--quiet",
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
        if os.path.exists(output_path):
            return output_path
    except Exception as e:
        print(f"  Download error: {e}")
    return None


def remix_video(input_path, output_path, style="random"):
    """Remix video to make it unique — mirror, crop, speed, color, overlay."""
    if style == "random":
        style = random.choice(["mirror", "crop_zoom", "speed", "color", "combo"])
    
    # Get video info
    probe = subprocess.run(
        [FFMPEG, "-i", input_path, "-f", "null", "-"],
        capture_output=True, text=True, timeout=10
    )
    
    # Build filter based on style
    filters = []
    
    if style in ("mirror", "combo"):
        filters.append("hflip")
    
    if style in ("crop_zoom", "combo"):
        # Random crop + scale back (slight zoom effect)
        crop_pct = random.uniform(0.85, 0.95)
        filters.append(f"crop=iw*{crop_pct}:ih*{crop_pct}")
    
    if style in ("color", "combo"):
        # Slight color adjustment
        brightness = random.uniform(-0.03, 0.03)
        contrast = random.uniform(0.95, 1.05)
        saturation = random.uniform(0.9, 1.1)
        filters.append(f"eq=brightness={brightness}:contrast={contrast}:saturation={saturation}")
    
    # Always scale to 1080x1920 (9:16)
    filters.append("scale=1080:1920:force_original_aspect_ratio=decrease")
    filters.append("pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black")
    
    # Speed adjustment
    speed = 1.0
    if style in ("speed", "combo"):
        speed = random.choice([0.95, 1.05, 1.1, 0.9])
    
    vf = ",".join(filters)
    
    cmd = [
        FFMPEG, "-y", "-i", input_path,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
    ]
    
    if speed != 1.0:
        cmd.extend(["-filter:a", f"atempo={speed}"])
    
    cmd.extend([
        "-t", "60",  # Max 60s
        "-pix_fmt", "yuv420p",
        "-r", "24",
        output_path
    ])
    
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
        return os.path.exists(output_path)
    except Exception as e:
        print(f"  Remix error: {e}")
        return False


def clean_metadata(video_path):
    """Strip all metadata from video."""
    temp = video_path + ".clean.mp4"
    
    # FFmpeg: strip metadata
    cmd = [
        FFMPEG, "-y", "-i", video_path,
        "-map_metadata", "-1",
        "-fflags", "+bitexact",
        "-flags:v", "+bitexact",
        "-flags:a", "+bitexact",
        "-c", "copy",
        temp
    ]
    subprocess.run(cmd, capture_output=True, timeout=60)
    
    if os.path.exists(temp):
        os.replace(temp, video_path)
    
    # Exiftool: double clean
    subprocess.run(
        [EXIFTOOL, "-all=", "-overwrite_original", video_path],
        capture_output=True, timeout=30
    )
    
    return True


def upload_and_schedule(video_path, caption, schedule_time, accounts):
    """Upload to PostBridge and schedule."""
    headers = {"Authorization": f"Bearer {PB_KEY}", "Content-Type": "application/json"}
    
    fsize = os.path.getsize(video_path)
    fname = os.path.basename(video_path)
    
    data = json.dumps({"name": fname, "mime_type": "video/mp4", "size_bytes": fsize}).encode()
    req = urllib.request.Request(f"{PB_BASE}/media/create-upload-url", data=data, headers=headers)
    resp = urllib.request.urlopen(req, context=CTX, timeout=15)
    result = json.loads(resp.read())
    upload_url = result.get("upload_url", "")
    media_id = result.get("id", "")
    
    with open(video_path, "rb") as f:
        file_data = f.read()
    put_req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    put_req.add_header("Content-Type", "video/mp4")
    urllib.request.urlopen(put_req, context=CTX, timeout=300)
    
    post_data = json.dumps({
        "caption": caption,
        "social_accounts": accounts,
        "media": [media_id],
        "scheduled_at": schedule_time,
    }).encode()
    post_req = urllib.request.Request(f"{PB_BASE}/posts", data=post_data, headers=headers)
    post_resp = urllib.request.urlopen(post_req, context=CTX, timeout=30)
    post_result = json.loads(post_resp.read())
    return post_result.get("id", "unknown")


def run_niche(niche_name, count=50, schedule=False, start_date=None):
    """Run clipper pipeline for a niche."""
    niche = NICHES[niche_name]
    niche_dir = OUTPUT_BASE / niche_name
    niche_dir.mkdir(parents=True, exist_ok=True)
    
    if not start_date:
        start_date = datetime.now(timezone.utc) + timedelta(days=1)
    
    print(f"\n{'='*60}")
    print(f"🎬 CLIPPER: {niche_name.upper()} — Target: {count} videos")
    print(f"{'='*60}")
    
    # Step 1: Search for videos across all queries
    all_videos = []
    seen_ids = set()
    
    for query in niche["search_queries"]:
        print(f"\n🔍 Searching: {query}")
        videos = search_videos(query, max_results=8)
        for v in videos:
            if v["id"] not in seen_ids:
                seen_ids.add(v["id"])
                all_videos.append(v)
        print(f"   Found {len(videos)} videos (total unique: {len(all_videos)})")
        time.sleep(1)
        
        if len(all_videos) >= count * 2:  # Get 2x to have buffer
            break
    
    print(f"\n📊 Total unique videos found: {len(all_videos)}")
    
    # Step 2: Download, remix, clean, schedule
    success = 0
    failed = 0
    posts_per_day = 5
    
    # Prime times WIB → UTC
    prime_utc = ["00:00", "03:00", "05:00", "08:00", "11:00",
                 "14:00", "00:30", "03:30", "05:30", "08:30"]
    
    for idx, video in enumerate(all_videos):
        if success >= count:
            break
        
        vid = video["id"]
        print(f"\n--- [{success+1}/{count}] {video['title'][:50]}... ---")
        
        # Download
        raw_path = download_video(vid, niche_dir)
        if not raw_path:
            print(f"  ❌ Download failed")
            failed += 1
            continue
        print(f"  ✅ Downloaded")
        
        # Remix with random style
        remix_path = str(niche_dir / f"remix_{success+1:04d}.mp4")
        style = random.choice(["mirror", "crop_zoom", "combo", "color"])
        if not remix_video(raw_path, remix_path, style):
            print(f"  ❌ Remix failed")
            failed += 1
            continue
        print(f"  ✅ Remixed ({style})")
        
        # Clean metadata
        clean_metadata(remix_path)
        fsize = os.path.getsize(remix_path) / 1024 / 1024
        print(f"  ✅ Metadata cleaned ({fsize:.1f}MB)")
        
        # Delete raw to save space
        try:
            os.remove(raw_path)
        except:
            pass
        
        # Schedule
        if schedule:
            day_offset = success // posts_per_day
            time_idx = success % len(prime_utc)
            sched_dt = start_date + timedelta(days=day_offset)
            sched_time = f"{sched_dt.strftime('%Y-%m-%d')}T{prime_utc[time_idx]}:00.000Z"
            
            caption = random.choice(niche["captions"]).format(hashtags=niche["hashtags"])
            
            try:
                post_id = upload_and_schedule(
                    remix_path, caption, sched_time, niche["accounts"]
                )
                print(f"  ✅ Scheduled: {sched_time} → {post_id}")
            except Exception as e:
                print(f"  ❌ Schedule failed: {e}")
                failed += 1
                continue
        
        success += 1
        
        # Clean up remix to save disk (already uploaded)
        if schedule:
            try:
                os.remove(remix_path)
            except:
                pass
        
        time.sleep(2)  # Rate limit
    
    print(f"\n{'='*60}")
    print(f"🏁 {niche_name.upper()} COMPLETE: {success}/{count} videos")
    print(f"   Failed: {failed}")
    print(f"{'='*60}")
    
    return success


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", required=True, choices=list(NICHES.keys()))
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--schedule", action="store_true")
    parser.add_argument("--start-date", default=None)
    args = parser.parse_args()
    
    start = None
    if args.start_date:
        start = datetime.strptime(args.start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    
    run_niche(args.niche, args.count, args.schedule, start)
