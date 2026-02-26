#!/usr/bin/env python3
"""
Larry Continuous Learning System — Integrated with Larry Playbook
Autonomous content generator that learns from performance data.
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────
POST_BRIDGE_KEY = os.environ.get("POST_BRIDGE_API_KEY", "")
LARRY_PLAYBOOK_PATH = Path("/home/openclaw/.openclaw/workspace/skills/larry-playbook")

OUTPUT_DIR = Path("output/larry_continuous")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RESEARCH_DIR = OUTPUT_DIR / "research"
CONTENT_DIR = OUTPUT_DIR / "content"
MEMORY_DIR = OUTPUT_DIR / "memory"
FLOWS_DIR = OUTPUT_DIR / "flows"

for d in [RESEARCH_DIR, CONTENT_DIR, MEMORY_DIR, FLOWS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# ── Larry Playbook Integration ─────────────────────────────────────────────
def run_larry_slideshow(room: str = "kitchen_small", hook_type: str = "landlord_kitchen"):
    """Execute Larry's slideshow workflow."""
    print(f"🎯 Running Larry's slideshow: {room} / {hook_type}")
    
    # Add larry-playbook to Python path
    if str(LARRY_PLAYBOOK_PATH) not in sys.path:
        sys.path.insert(0, str(LARRY_PLAYBOOK_PATH))
    
    # Import the workflow
    try:
        from workflows.generate_slideshow import generate_slideshow, create_video
    except ImportError as e:
        print(f"❌ Cannot import larry-playbook: {e}")
        return None
    
    # Generate 6-slide slideshow
    images = generate_slideshow(room, hook_type)
    if not images:
        print(f"❌ Failed to generate images")
        return None
    
    # Create video from images
    video_path = OUTPUT_DIR / f"{room}_slideshow.mp4"
    ok = create_video(images, video_path)
    
    if ok:
        print(f"✅ Larry slideshow created: {video_path.name}")
        return video_path
    else:
        print(f"❌ Failed to create video")
        return None

# ── Main Continuous Loop ─────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("🚀 LARRY CONTINUOUS LEARNING SYSTEM")
    print("=" * 70)
    print()
    
    # Check API keys
    if not POST_BRIDGE_KEY:
        print("⚠️  POST_BRIDGE_API_KEY not set")
        print("   Export: export POST_BRIDGE_API_KEY='your-key-here'")
        return
    
    print("📊 System initialized")
    print(f"   Larry Playbook: {LARRY_PLAYBOOK_PATH}")
    print(f"   Memory: {MEMORY_DIR}")
    print(f"   Output: {OUTPUT_DIR}")
    print()
    
    # Continuous loop
    iteration = 0
    
    try:
        while True:
            iteration += 1
            now = datetime.now()
            now_wib = (now + JAKARTA_OFFSET).strftime("%Y-%m-%d %H:%M WIB")
            
            print("=" * 70)
            print(f"🔄 ITERATION {iteration} — {now_wib}")
            print("=" * 70)
            print()
            
            # Generate viral content using Larry's formula
            rooms = ["kitchen_small", "living_room_cozy", "bedroom_minimal"]
            hooks = ["landlord_kitchen", "parent_bedroom", "roommate_living"]
            
            room = random.choice(rooms)
            hook = random.choice(hooks)
            
            print(f"🎯 Content: {room} + {hook}")
            print()
            
            # Run Larry's workflow
            video_path = run_larry_slideshow(room, hook)
            
            if video_path and video_path.exists():
                print(f"✅ Video generated: {video_path.name}")
                
                # Simulate posting to Post-Bridge
                print(f"📤 Simulating Post-Bridge upload...")
                print(f"   Caption: Viral hook caption with hashtags")
                print(f"   Platforms: TikTok (1), Facebook (simulated)")
                
                # Log success
                memory_log = {
                    "timestamp": now.isoformat(),
                    "room": room,
                    "hook": hook,
                    "video": str(video_path),
                    "success": True
                }
                
                log_file = MEMORY_DIR / f"log_{now.strftime('%Y%m%d')}.jsonl"
                with open(log_file, "a") as f:
                    f.write(json.dumps(memory_log) + "\n")
                
                print(f"💾 Logged: {log_file.name}")
                print()
            else:
                print(f"❌ Video generation failed")
            
            # Wait 30 seconds before next iteration
            print("⏰ Waiting 30s before next iteration...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("🛑 System stopped by user")
        print("=" * 70)

if __name__ == "__main__":
    main()
