#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
from datetime import datetime

# Paths
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
QUEUE_FILE = WORKSPACE / "autopilot_affiliate_engine" / "postbridge_queue_jendralbot.json"
RECOVERY_DIR = WORKSPACE / "output" / "mass_recovery_test_v1"
RECOVERY_DIR.mkdir(parents=True, exist_ok=True)
RECOVERY_LOG = RECOVERY_DIR / "recovery.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RECOVERY_LOG, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def run_recovery_test(limit=10):
    log(f"🚀 Starting Mass Recovery (Limit: {limit} items)")
    
    if not QUEUE_FILE.exists():
        log("❌ Queue file not found!")
        return

    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)
        
    log(f"📋 Loaded queue with {len(queue)} items")
    
    processed_count = 0
    for item in queue:
        if processed_count >= limit:
            break
            
        item_id = item.get("id")
        platform = item.get("platform")
        content = item.get("content", {})
        caption = content.get("caption", "No caption")
        
        # Check if already processed
        output_path = RECOVERY_DIR / f"rec_{item_id}.jpg"
        if output_path.exists():
            log(f"⏭️ Skipping {item_id} (Already exists)")
            continue

        log(f"--- Processing Item: {item_id} ({platform}) ---")
        log(f"Caption: {caption[:50]}...")
        
        # Step: Generate Content for this item using Smart Router
        # Using the prompt from caption as a base
        prompt = f"Viral marketing image for: {caption[:100]}"
        
        cmd = f"python3 {WORKSPACE}/scripts/smart_content_generator.py --prompt \"{prompt}\" --name \"rec_{item_id}\" --type image"
        
        import subprocess
        log(f"Running Smart Router for {item_id}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            res_json = json.loads(result.stdout)
            log(f"✅ Success: {res_json.get('image')}")
            processed_count += 1
        else:
            log(f"❌ Failed: {result.stderr}")
            
    log(f"🏁 Recovery Test Finished. Processed {processed_count} items.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    
    run_recovery_test(limit=args.limit)
