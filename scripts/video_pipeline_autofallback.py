#!/usr/bin/env python3
"""
Video Pipeline with Autofallback — End-to-end content generation
Flow: Script → NVIDIA Image → BytePlus Video → Edge-TTS VO → FFmpeg Assembly → PostBridge Upload

Usage:
  python3 scripts/video_pipeline_autofallback.py --topic "stop loss" --lang id
  python3 scripts/video_pipeline_autofallback.py --topic "risk management" --lang id --post
"""

import os, json, sys, ssl, time, base64, subprocess, asyncio, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timedelta

FFMPEG = "/usr/bin/ffmpeg"
OUTPUT_DIR = Path("/home/openclaw/.openclaw/workspace/output/video_pipeline")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CTX = ssl.create_default_context()

# ─── Provider Config ───
NVIDIA_KEY = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_KEY = os.environ.get("BYTEPLUS_API_KEY", "")
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
POSTBRIDGE_KEY = os.environ.get("POSTBRIDGE_API_KEY", "pb_live_AT9Xm4PKaYBzAvFZYGgexi")

# BytePlus model fallback chain
VIDEO_MODELS = [
    "seedance-1-0-pro-fast-251015",
    "seedance-1-5-pro-251215",
    "seedance-1-0-lite-t2v-250428",
    "seedance-1-0-pro-250528",
]

# Edge-TTS voices
VOICES = {
    "id": "id-ID-ArdiNeural",       # Indonesian male
    "id_f": "id-ID-GadisNeural",    # Indonesian female
    "en": "en-US-GuyNeural",        # English male
    "en_f": "en-US-JennyNeural",    # English female
}

# ─── Trading Education Topics (Indonesian) ───
TOPICS = {
    "stop_loss": {
        "title": "Stop Loss: Pelindung Modal Trading Kamu",
        "scenes": [
            {"prompt": "3D clay animation, dramatic red candlestick chart crashing down rapidly, dark moody background, cinematic lighting, financial crisis feeling", 
             "vo": "Pernah nggak, kamu trading dan tiba-tiba harga anjlok? Modal kamu habis dalam hitungan detik."},
            {"prompt": "3D clay animation, golden shield with glowing STOP LOSS text appearing to protect a trading chart, dramatic lighting, hopeful mood",
             "vo": "Itulah kenapa STOP LOSS itu wajib. Stop loss adalah pelindung modal kamu dari kerugian besar."},
            {"prompt": "3D clay animation, a hand setting a stop loss line on a trading chart, clean professional look, tutorial style, green and gold colors",
             "vo": "Caranya gampang. Tentukan berapa persen kerugian maksimal yang kamu sanggup. Biasanya satu sampai dua persen dari total modal."},
            {"prompt": "3D clay animation, split screen showing two traders - one losing everything panicking, one calmly protected by golden shield, dramatic contrast",
             "vo": "Trader tanpa stop loss? Bisa kehilangan semua modal dalam satu hari. Trader dengan stop loss? Rugi kecil, dan bisa trading lagi besok."},
            {"prompt": "3D clay animation, golden text PROTECT YOUR CAPITAL glowing with trading charts in background, triumphant mood, cinematic quality",
             "vo": "Ingat, trader profesional bukan yang selalu untung. Tapi yang bisa bertahan. Pasang stop loss, lindungi modal kamu. Follow untuk tips trading lainnya."},
        ],
        "caption": "🛡️ Stop Loss = Pelindung Modal! 💰\n\nTrader pro bukan yang selalu profit, tapi yang bisa BERTAHAN.\n\n✅ Pasang stop loss SEBELUM entry\n✅ Maksimal 1-2% risiko per trade\n✅ Jangan pernah geser stop loss lebih jauh\n\nSave ini biar inget! 📌\n\n#TradingTips #StopLoss #ForexIndonesia #BelajarTrading #TradingEducation #RiskManagement #BerkahKarya",
    },
    "risk_management": {
        "title": "Risk Management: Kunci Sukses Trading",
        "scenes": [
            {"prompt": "3D clay animation, pile of gold coins slowly disappearing one by one from a trading desk, sad mood, dark background, cinematic",
             "vo": "Banyak trader pemula yang fokus cari profit besar. Tapi lupa hal paling penting: risk management."},
            {"prompt": "3D clay animation, a balanced scale with RISK on one side and REWARD on the other, golden glow, professional look",
             "vo": "Risk management itu sederhana. Pastikan potensi keuntungan kamu LEBIH BESAR dari potensi kerugian. Minimal rasio satu banding dua."},
            {"prompt": "3D clay animation, a calculator showing 1-2% with money stacks beside it, clean educational style, green accents",
             "vo": "Aturan emas: jangan pernah risiko lebih dari satu sampai dua persen modal di satu trade. Kalau modal kamu sepuluh juta, maksimal rugi dua ratus ribu per trade."},
            {"prompt": "3D clay animation, 10 trading positions displayed as doors - 6 green open doors and 4 red closed doors, balanced composition",
             "vo": "Dengan risk management yang benar, kamu bisa salah enam dari sepuluh trade dan TETAP PROFIT. Karena yang benar menghasilkan lebih besar."},
            {"prompt": "3D clay animation, golden trophy with text CONSISTENT PROFIT rising from a well-managed trading chart, triumphant cinematic mood",
             "vo": "Jadi ingat: kontrol risiko dulu, profit akan mengikuti. Follow untuk tips trading selanjutnya."},
        ],
        "caption": "📊 Risk Management = Kunci Sukses! 🔑\n\nTrader sukses bukan yang paling sering benar, tapi yang RISIKONYA TERKONTROL.\n\n✅ Rasio minimal 1:2 (risk:reward)\n✅ Max 1-2% risiko per trade\n✅ Bisa salah 60% dan tetap profit!\n\nShare ke teman trader kamu! 🔄\n\n#RiskManagement #TradingTips #ForexIndonesia #BelajarTrading #TradingEducation #BerkahKarya",
    },
    "fibonacci": {
        "title": "Fibonacci Retracement: Senjata Rahasia Trader Pro",
        "scenes": [
            {"prompt": "3D clay animation, mysterious golden spiral fibonacci sequence floating above a trading chart, magical glowing particles, dark background",
             "vo": "Ada satu tools yang dipakai trader profesional di seluruh dunia. Namanya: Fibonacci Retracement."},
            {"prompt": "3D clay animation, trading chart with golden horizontal lines at key fibonacci levels 38.2 50 61.8, clean educational look, highlighted zones",
             "vo": "Fibonacci menunjukkan level-level kunci di mana harga kemungkinan besar akan bounce atau berbalik arah. Level terpenting: tiga puluh delapan koma dua, lima puluh, dan enam puluh satu koma delapan persen."},
            {"prompt": "3D clay animation, price bouncing off a glowing golden fibonacci 61.8 level on chart, satisfying bounce animation, green arrow up",
             "vo": "Cara pakainya: tarik dari swing low ke swing high. Lalu tunggu harga retrace ke level fibonacci. Entry di level golden ratio enam puluh satu koma delapan untuk akurasi terbaik."},
            {"prompt": "3D clay animation, a magnifying glass examining fibonacci levels with buy and sell signals appearing, professional trading setup",
             "vo": "Kombinasikan fibonacci dengan support resistance dan candlestick pattern. Konfirmasi dari dua sampai tiga sinyal sekaligus meningkatkan win rate kamu drastis."},
            {"prompt": "3D clay animation, golden fibonacci spiral transforming into rising profit chart, triumphant mood, glowing green, cinematic quality",
             "vo": "Fibonacci bukan magic, tapi matematika. Dan matematika tidak berbohong. Follow untuk belajar lebih dalam."},
        ],
        "caption": "🌀 Fibonacci Retracement — Senjata Rahasia Trader Pro! ✨\n\nLevel yang WAJIB kamu tahu:\n📍 38.2% — Support/Resistance ringan\n📍 50.0% — Level psikologis\n📍 61.8% — Golden Ratio (PALING KUAT!)\n\nKombinasikan dengan S/R + candlestick = 🔥\n\nSave & Share! 📌\n\n#Fibonacci #TradingTips #ForexIndonesia #BelajarTrading #TradingEducation #GoldenRatio #BerkahKarya",
    },
}


def api_request(url, data=None, headers=None, method=None, timeout=30):
    """Make HTTP request with error handling."""
    if data and isinstance(data, dict):
        data = json.dumps(data).encode()
    if method is None:
        method = "POST" if data else "GET"
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    resp = urllib.request.urlopen(req, context=CTX, timeout=timeout)
    return json.loads(resp.read())


def generate_image(prompt, output_path):
    """Generate image via NVIDIA Flux."""
    print(f"  🖼️  Generating image...")
    url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
    data = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {NVIDIA_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    resp = urllib.request.urlopen(req, context=CTX, timeout=120)
    result = json.loads(resp.read())
    img_bytes = base64.b64decode(result["artifacts"][0]["base64"])
    with open(output_path, "wb") as f:
        f.write(img_bytes)
    print(f"  ✅ Image saved: {output_path} ({len(img_bytes)//1024}KB)")
    return output_path


def generate_video_t2v(prompt, ratio="9:16"):
    """Generate video via BytePlus Seedance with model fallback."""
    for model in VIDEO_MODELS:
        print(f"  🎬 Trying video model: {model}...")
        try:
            # Create task
            payload = {"model": model, "content": [{"type": "text", "text": prompt}], "ratio": ratio}
            result = api_request(
                f"{BYTEPLUS_BASE}/contents/generations/tasks",
                data=payload,
                headers={"Authorization": f"Bearer {BYTEPLUS_KEY}", "Content-Type": "application/json"},
                timeout=30
            )
            task_id = result.get("id", "")
            if not task_id:
                print(f"    ❌ No task ID returned")
                continue
            
            print(f"    Task: {task_id}, polling...")
            # Poll for completion
            for i in range(40):  # 10 min max
                time.sleep(15)
                poll = api_request(
                    f"{BYTEPLUS_BASE}/contents/generations/tasks/{task_id}",
                    headers={"Authorization": f"Bearer {BYTEPLUS_KEY}"},
                    timeout=15
                )
                status = poll.get("status", "unknown")
                if status == "succeeded":
                    content = poll.get("content", {})
                    video_url = content.get("video_url", "") if isinstance(content, dict) else ""
                    if not video_url and isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and "video_url" in c:
                                video_url = c["video_url"]
                                break
                    duration = poll.get("duration", 5)
                    resolution = poll.get("resolution", "unknown")
                    print(f"    ✅ Video ready! {resolution}, {duration}s")
                    return video_url, duration, model
                elif status == "failed":
                    err = poll.get("error", {})
                    code = err.get("code", "") if isinstance(err, dict) else str(err)
                    print(f"    ❌ Failed: {code}")
                    if "SetLimitExceeded" in str(code):
                        break  # Try next model
                    break
                else:
                    if i % 4 == 0:
                        print(f"    ⏳ {status} ({(i+1)*15}s)")
        except Exception as e:
            print(f"    ❌ Error: {e}")
            continue
    
    return None, 0, None


def download_video(url, output_path):
    """Download video from URL."""
    resp = urllib.request.urlopen(url, context=CTX, timeout=120)
    data = resp.read()
    with open(output_path, "wb") as f:
        f.write(data)
    print(f"  ✅ Downloaded: {output_path} ({len(data)//1024//1024:.1f}MB)")
    return output_path


async def generate_voiceover(text, output_path, voice="id-ID-ArdiNeural", rate="+5%"):
    """Generate voiceover via Edge-TTS."""
    import edge_tts
    print(f"  🎤 Generating VO...")
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)
    print(f"  ✅ VO saved: {output_path}")
    return output_path


def get_audio_duration(path):
    """Get duration of audio file in seconds."""
    result = subprocess.run(
        [FFMPEG, "-i", path, "-f", "null", "-"],
        capture_output=True, text=True, timeout=10
    )
    for line in result.stderr.split("\n"):
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
    return 5.0


def merge_video_audio(video_path, audio_path, output_path):
    """Merge video with audio, adjusting video speed to match VO duration."""
    vo_dur = get_audio_duration(audio_path)
    vid_dur = get_audio_duration(video_path)
    
    if vid_dur <= 0:
        vid_dur = 5.0
    
    # If VO is longer than video, slow down video OR loop it
    if vo_dur > vid_dur * 1.5:
        # Loop video to match VO length
        cmd = [
            FFMPEG, "-y",
            "-stream_loop", "-1", "-i", video_path,
            "-i", audio_path,
            "-t", str(vo_dur + 0.5),
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-map", "0:v:0", "-map", "1:a:0",
            output_path
        ]
    else:
        # Speed adjust video to match VO
        speed = vid_dur / vo_dur if vo_dur > 0 else 1.0
        speed = max(0.5, min(2.0, speed))  # Clamp speed
        cmd = [
            FFMPEG, "-y",
            "-i", video_path, "-i", audio_path,
            "-filter:v", f"setpts={1/speed}*PTS",
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v:0", "-map", "1:a:0",
            "-shortest",
            output_path
        ]
    
    subprocess.run(cmd, capture_output=True, timeout=120)
    print(f"  ✅ Merged: {output_path}")
    return output_path


def concat_videos(video_paths, output_path):
    """Concatenate multiple videos into one."""
    # Create concat file
    concat_file = output_path.replace(".mp4", "_concat.txt")
    with open(concat_file, "w") as f:
        for vp in video_paths:
            f.write(f"file '{vp}'\n")
    
    # Re-encode to ensure compatible streams
    normalized = []
    for i, vp in enumerate(video_paths):
        norm_path = vp.replace(".mp4", "_norm.mp4")
        cmd = [
            FFMPEG, "-y", "-i", vp,
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-r", "24",
            "-s", "1080x1920",  # 9:16
            "-pix_fmt", "yuv420p",
            norm_path
        ]
        subprocess.run(cmd, capture_output=True, timeout=60)
        normalized.append(norm_path)
    
    # Update concat file
    with open(concat_file, "w") as f:
        for vp in normalized:
            f.write(f"file '{vp}'\n")
    
    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, timeout=120)
    
    # Cleanup normalized files
    for vp in normalized:
        try: os.remove(vp)
        except: pass
    try: os.remove(concat_file)
    except: pass
    
    final_dur = get_audio_duration(output_path)
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"  ✅ Final video: {output_path} ({final_dur:.1f}s, {size_mb:.1f}MB)")
    return output_path


def upload_to_postbridge(video_path, caption, schedule_time=None):
    """Upload video to PostBridge and schedule post."""
    base = "https://api.post-bridge.com/v1"
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_KEY}",
        "Content-Type": "application/json"
    }
    
    # Step 1: Get upload URL
    filename = os.path.basename(video_path)
    size = os.path.getsize(video_path)
    upload_req = api_request(
        f"{base}/media/create-upload-url",
        data={"filename": filename, "content_type": "video/mp4", "file_size": size},
        headers=headers,
        timeout=15
    )
    upload_url = upload_req.get("upload_url", "")
    media_id = upload_req.get("id", "")
    
    if not upload_url:
        print(f"  ❌ No upload URL: {upload_req}")
        return None
    
    # Step 2: Upload file
    with open(video_path, "rb") as f:
        video_data = f.read()
    
    put_req = urllib.request.Request(upload_url, data=video_data, method="PUT")
    put_req.add_header("Content-Type", "video/mp4")
    urllib.request.urlopen(put_req, context=CTX, timeout=300)
    print(f"  ✅ Uploaded to PostBridge: {media_id}")
    
    # Step 3: Create post — video accounts only
    # YouTube=49678, Instagram=49682,49676, Threads=49683,49680,49677, Facebook=49675,49674,49673,49672
    video_accounts = [49678, 49682, 49676, 49683, 49680, 49677, 49675, 49674, 49673, 49672]
    
    if not schedule_time:
        schedule_time = (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    post_data = {
        "caption": caption,
        "social_accounts": video_accounts,
        "media": [media_id],
        "scheduled_at": schedule_time,
    }
    
    result = api_request(f"{base}/posts", data=post_data, headers=headers, timeout=30)
    post_id = result.get("id", "unknown")
    print(f"  ✅ Post scheduled: {post_id} at {schedule_time}")
    return post_id


async def generate_topic(topic_key, lang="id", post=False):
    """Generate full video for a topic."""
    topic = TOPICS.get(topic_key)
    if not topic:
        print(f"❌ Unknown topic: {topic_key}. Available: {list(TOPICS.keys())}")
        return None
    
    print(f"\n{'='*60}")
    print(f"🎬 GENERATING: {topic['title']}")
    print(f"{'='*60}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_dir = OUTPUT_DIR / f"{topic_key}_{timestamp}"
    topic_dir.mkdir(parents=True, exist_ok=True)
    
    voice = VOICES.get(lang, VOICES["id"])
    scene_videos = []
    
    for i, scene in enumerate(topic["scenes"]):
        print(f"\n--- Scene {i+1}/{len(topic['scenes'])} ---")
        
        # 1. Generate video (T2V)
        video_url, duration, model = generate_video_t2v(scene["prompt"])
        if not video_url:
            print(f"  ⚠️ Video gen failed for scene {i+1}, trying image fallback...")
            # Fallback: generate image instead
            img_path = str(topic_dir / f"scene_{i+1}_img.jpg")
            try:
                generate_image(scene["prompt"], img_path)
                # Convert image to 5s video
                vid_from_img = str(topic_dir / f"scene_{i+1}_from_img.mp4")
                subprocess.run([
                    FFMPEG, "-y", "-loop", "1", "-i", img_path,
                    "-c:v", "libx264", "-t", "8", "-pix_fmt", "yuv420p",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.001,1.3)':d=192:s=1080x1920",
                    "-r", "24", vid_from_img
                ], capture_output=True, timeout=60)
                raw_video = vid_from_img
            except Exception as e:
                print(f"  ❌ Image fallback also failed: {e}")
                continue
        else:
            # Download video
            raw_video = str(topic_dir / f"scene_{i+1}_raw.mp4")
            download_video(video_url, raw_video)
        
        # 2. Generate voiceover
        vo_path = str(topic_dir / f"scene_{i+1}_vo.mp3")
        await generate_voiceover(scene["vo"], vo_path, voice=voice)
        
        # 3. Merge video + VO
        merged_path = str(topic_dir / f"scene_{i+1}_merged.mp4")
        merge_video_audio(raw_video, vo_path, merged_path)
        scene_videos.append(merged_path)
        
        print(f"  ✅ Scene {i+1} complete!")
        time.sleep(2)  # Rate limit between scenes
    
    if not scene_videos:
        print("❌ No scenes generated!")
        return None
    
    # 4. Concatenate all scenes
    final_path = str(topic_dir / f"{topic_key}_final.mp4")
    concat_videos(scene_videos, final_path)
    
    # 5. Post if requested
    if post and os.path.exists(final_path):
        try:
            post_id = upload_to_postbridge(final_path, topic["caption"])
            print(f"\n🚀 POSTED! ID: {post_id}")
        except Exception as e:
            print(f"\n⚠️ Post failed: {e}")
            print(f"   Video saved at: {final_path}")
    
    print(f"\n{'='*60}")
    print(f"✅ COMPLETE: {topic['title']}")
    print(f"   Final: {final_path}")
    print(f"{'='*60}")
    return final_path


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Video Pipeline with Autofallback")
    parser.add_argument("--topic", default="stop_loss", help="Topic key")
    parser.add_argument("--lang", default="id", help="Language (id/en)")
    parser.add_argument("--post", action="store_true", help="Upload to PostBridge")
    parser.add_argument("--all", action="store_true", help="Generate all topics")
    args = parser.parse_args()
    
    if args.all:
        for topic_key in TOPICS:
            await generate_topic(topic_key, args.lang, args.post)
            time.sleep(5)
    else:
        await generate_topic(args.topic, args.lang, args.post)


if __name__ == "__main__":
    asyncio.run(main())
