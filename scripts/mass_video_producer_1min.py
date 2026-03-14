#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
from datetime import datetime
import subprocess

# Paths
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
QUEUE_FILE = WORKSPACE / "autopilot_affiliate_engine" / "postbridge_queue_jendralbot.json"
OUTPUT_DIR = WORKSPACE / "output" / "mass_video_production"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

PYTHON = "/home/openclaw/.openclaw/workspace/venv/bin/python3"

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def run_production(limit=5):
    log(f"🎬 Starting 1-Minute Mass Production (Limit: {limit} items)")
    
    if not QUEUE_FILE.exists():
        log("❌ Queue file not found!")
        return

    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)
        
    processed_count = 0
    for item in queue:
        if processed_count >= limit:
            break
            
        item_id = item.get("id")
        content = item.get("content", {})
        caption = content.get("caption", "No caption")
        
        final_video = OUTPUT_DIR / f"final_{item_id}_1min.mp4"
        if final_video.exists():
            log(f"⏭️ Skipping {item_id} (Already done)")
            continue

        log(f"--- 🚀 Processing: {item_id} ---")

        try:
            # 1. Expand Script using Groq
            log("   📝 Step 1: Expanding script to 60s narrative...")
            script_cmd = [PYTHON, str(WORKSPACE / "scripts/expand_tiktok_script.py"), "--text", caption]
            script_res = subprocess.run(script_cmd, capture_output=True, text=True)
            expanded_text = script_res.stdout.strip()
            
            # 2. Generate TTS
            log("   🎙️ Step 2: Generating Neural TTS (Ardi)...")
            tts_path = TEMP_DIR / f"{item_id}_vo.mp3"
            tts_cmd = [PYTHON, str(WORKSPACE / "scripts/generate_audio.py"), "--text", expanded_text, "--output", str(tts_path)]
            subprocess.run(tts_cmd, capture_output=True)

            # 3. Get Base Video (From existing samples or Pexels)
            # For this mass run, we'll use a high-quality office loop
            bg_video = WORKSPACE / "output" / "test_results" / "background.mp4"
            bgm_audio = WORKSPACE / "output" / "bgm_library" / "elegant_luxury.mp3"

            # 4. Produce Final 1-Min Video
            log("   🎬 Step 3: Producing 1-Minute Synced MP4...")
            prod_cmd = [
                PYTHON, str(WORKSPACE / "scripts/produce_1min_video.py"),
                "--video", str(bg_video),
                "--tts", str(tts_path),
                "--bgm", str(bgm_audio),
                "--output", str(final_video)
            ]
            subprocess.run(prod_cmd, capture_output=True)

            if final_video.exists():
                log(f"✅ SUCCESS: {final_video.name}")
                processed_count += 1
            else:
                log(f"❌ Failed to produce final video for {item_id}")

        except Exception as e:
            log(f"❌ Error during {item_id}: {e}")
            
    log(f"🏁 Finished. Produced {processed_count} videos.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    run_production(limit=args.limit)
