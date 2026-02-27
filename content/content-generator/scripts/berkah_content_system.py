#!/usr/bin/env python3
"""
BerkahKarya Flexible Content System

On-demand video generation + hourly research (NOT forced generation).

Features:
1. Hourly Research — Every 1 hour, scan trending topics
2. 5 Viral Flows Available — Use based on needs
3. Performance Tracking — Log views, update confidence
4. Smart Selector — Choose best flow for situation

Usage:
    # Research (otomatis tiap 1 jam)
    python3 berkah_content_system.py --auto-research

    # Multi-Stage I2V (25s continuous, scene transitions)
    python3 berkah_content_system.py --flow multi-stage --room kitchen_small --hook landlord_kitchen

    # Larry Slideshow (15s, 6 slides)
    python3 berkah_content_system.py --flow larry-slideshow --room bedroom_minimal --hook parent_bedroom

    # TikTok 1-Minute (60s, looped 9:16)
    python3 berkah_content_system.py --flow tiktok-1min --niche motivation

    # Basic (custom duration)
    python3 berkah_content_system.py --flow basic --prompt "My custom prompt" --duration 30

    # Analyze Performance
    python3 berkah_content_system.py --mode analyze

    # Log Performance
    python3 berkah_content_system.py --mode log --hook-type landlord_kitchen --views 234000
"""

import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

# ── CONFIG ────────────────────────────────────────────────────────────
RESEARCH_INTERVAL_HOURS = 1  # Research tiap 1 jam
WORKSPACE = Path("/home/openclaw/.openclaw/workspace/skills/1ai-skills/content/content-generator/scripts")

OUTPUT_DIR = Path("/tmp/berkah_content")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# Environment keys
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Memory for performance tracking
MEMORY_DIR = OUTPUT_DIR / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_FILE = MEMORY_DIR / "performance_memory.json"

# Confidence scores per hook type (from Larry Playbook)
HOOK_CONFIDENCE = {
    "landlord_kitchen": {"confidence": 0.9, "avg_views": 234000, "count": 0, "avg_per_post": 0},
    "parent_bedroom": {"confidence": 0.75, "avg_views": 80000, "count": 0, "avg_per_post": 0},
    "roommate_living": {"confidence": 0.65, "avg_views": 60000, "count": 0, "avg_per_post": 0},
}


# ── HTTP HELPERS ────────────────────────────────────────────────────
def load_memory() -> Dict:
    """Load performance memory."""
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {k: v for k, v in HOOK_CONFIDENCE.items()}


def save_memory(memory: Dict):
    """Save performance memory."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def update_confidence(hook_type: str, views: int, memory: Dict) -> tuple:
    """Update confidence score based on performance."""
    current = memory.get(hook_type, HOOK_CONFIDENCE[hook_type])
    target_views = current["avg_views"]

    if views >= target_views:
        # Success — increase confidence
        new_conf = min(current["confidence"] + 0.1, 1.0)
        change = "📈 UP"
    elif views < target_views * 0.5:
        # Failure — decrease confidence
        new_conf = max(current["confidence"] - 0.15, 0.2)
        change = "📉 DOWN"
    else:
        # Neutral — keep confidence
        new_conf = current["confidence"]
        change = "➡️ STABLE"

    # Update stats
    total_posts = current["count"] + 1
    avg_views = (current["avg_per_post"] * current["count"] + views) / total_posts

    memory[hook_type] = {
        "confidence": new_conf,
        "avg_views": target_views,
        "count": total_posts,
        "avg_per_post": avg_views,
        "last_updated": datetime.now().isoformat(),
    }

    return change, new_conf


# ── MODULES ─────────────────────────────────────────────────────────
def run_research() -> bool:
    """Run TikTok viral hook research (hourly)."""
    print("\n🔍 Running hourly research...")

    # Run research system (tiktok_hook_research.py)
    cmd = [str(WORKSPACE / "tiktok_hook_research.py"), "--mode", "search"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE), timeout=120)

    if result.returncode != 0:
        print(f"  ❌ Research failed: {result.stderr[-200:]}")
        return False

    print("  ✅ Research complete")
    return True


def run_multi_stage(room: str, hook: str) -> bool:
    """Run multi-stage I2V generator (25s continuous)."""
    print(f"\n🎬 Multi-Stage I2V: {room} + {hook}")

    cmd = [str(WORKSPACE / "multi_stage_i2v.py"), "--room", room, "--hook", hook]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE), timeout=600)

    if result.returncode != 0:
        print(f"  ❌ Generation failed: {result.stderr[-500:]}")
        return False

    print("  ✅ Generation complete")
    print(f"  📁 Output: /tmp/multi_stage_i2v/")
    return True


def run_larry_slideshow(room: str, hook: str) -> bool:
    """Run Larry viral slideshow generator (15s, 6 slides)."""
    print(f"\n🎞 Larry Slideshow: {room} + {hook}")

    cmd = [str(WORKSPACE / "larry_viral_generator.py"), "--room", room, "--hook", hook]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE), timeout=600)

    if result.returncode != 0:
        print(f"  ❌ Generation failed: {result.stderr[-500:]}")
        return False

    print("  ✅ Generation complete")
    return True


def run_tiktok_1min(niche: str) -> bool:
    """Run TikTok 1-minute generator (60s, 9:16)."""
    print(f"\n📱 TikTok 1-Minute: {niche}")

    cmd = [str(WORKSPACE / "generate_tiktok_viral.py"), "--niche", niche]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE), timeout=600)

    if result.returncode != 0:
        print(f"  ❌ Generation failed: {result.stderr[-500:]}")
        return False

    print("  ✅ Generation complete")
    print(f"  📁 Output: /tmp/tiktok_viral/")
    return True


def run_basic(prompt: str, duration: int) -> bool:
    """Run basic generator (custom duration)."""
    print(f"\n🎯 Basic: {prompt[:60]}... ({duration}s)")

    cmd = [str(WORKSPACE / "generator.py"), "--prompt", prompt, "--duration", str(duration)]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE), timeout=600)

    if result.returncode != 0:
        print(f"  ❌ Generation failed: {result.stderr[-500:]}")
        return False

    print("  ✅ Generation complete")
    return True


def analyze_performance() -> Dict:
    """Analyze hook performance and provide recommendations."""
    print("\n📊 Analyzing performance...")

    memory = load_memory()

    analysis = {}
    for hook_type, data in memory.items():
        if data["count"] == 0:
            continue

        avg_views = data["avg_per_post"]
        confidence = data["confidence"]
        total = data["count"]

        # Rating
        if avg_views >= data["avg_views"]:
            rating = "🔥 VIRAL"
            score = 5
        elif avg_views >= data["avg_views"] * 0.7:
            rating = "⭐ STRONG"
            score = 4
        elif avg_views >= data["avg_views"] * 0.4:
            rating = "✅ GOOD"
            score = 3
        elif avg_views >= data["avg_views"] * 0.2:
            rating = "⚠️ WEAK"
            score = 2
        else:
            rating = "❌ FAILING"
            score = 1

        analysis[hook_type] = {
            "avg_views": avg_views,
            "total_posts": total,
            "confidence": confidence,
            "rating": rating,
            "score": score,
        }

    # Sort by score
    ranked = sorted(analysis.items(), key=lambda x: x[1]["score"], reverse=True)

    print(f"\nTop performer: {ranked[0][0]} ({ranked[0][1]['rating']})")
    print(f"Bottom performer: {ranked[-1][0]} ({ranked[-1][1]['rating']})")

    return {
        "by_type": analysis,
        "ranked": ranked,
        "top_3": ranked[:3],
    }


def log_performance(hook_type: str, views: int):
    """Log performance and update confidence."""
    print(f"\n📝 Logging: {hook_type} = {views:,} views")

    memory = load_memory()
    change, new_conf = update_confidence(hook_type, views, memory)
    save_memory(memory)

    print(f"  {change} confidence: {memory[hook_type]['confidence']:.2f} → {new_conf:.2f}")

    # Log to history
    history_file = MEMORY_DIR / f"history_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(history_file, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "hook_type": hook_type,
            "views": views,
            "confidence": new_conf,
        }) + "\n")

    print(f"  💾 Logged to: {history_file.name}")
    return memory


# ── AUTO RESEARCH LOOP ─────────────────────────────────────────────
def auto_research_loop():
    """Run research every 1 hour."""
    print("=" * 70)
    print("🚀 BERKAHKARYA FLEXIBLE CONTENT SYSTEM")
    print("=" * 70)
    print(f"Research Interval: {RESEARCH_INTERVAL_HOURS} hour(s)")
    print(f"Memory: {MEMORY_FILE}")
    print()

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

            # Research
            print("🔍 Running hourly research...")
            success = run_research()

            if success:
                # Load latest memory
                memory = load_memory()

                # Get top performers
                top_hooks = sorted(
                    memory.items(),
                    key=lambda x: x[1]["confidence"],
                    reverse=True,
                )[:3]

                print(f"\n📊 Top hooks by confidence:")
                for htype, data in top_hooks:
                    print(f"  {htype}: {data['confidence']:.2f} ({data['count']} posts, {data['avg_per_post']:,} avg views)")

                print("\n💡 Ready for on-demand generation!")
                print("Use:")
                print("  python3 berkah_content_system.py --flow multi-stage --room kitchen_small --hook landlord_kitchen")
                print("  python3 berkah_content_system.py --flow larry-slideshow --room bedroom_minimal --hook parent_bedroom")
                print("  python3 berkah_content_system.py --flow tiktok-1min --niche motivation")
                print("  python3 berkah_content_system.py --mode analyze")

            else:
                print("❌ Research failed — skipping this cycle")

            # Wait for next research cycle
            print(f"\n⏰ Next research in {RESEARCH_INTERVAL_HOURS} hour(s)...")
            print()

            time.sleep(RESEARCH_INTERVAL_HOURS * 3600)

    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("🛑 System stopped by user")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Error in auto loop: {e}")


# ── MAIN ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Flexible Content System"
    )
    parser.add_argument("--auto-research", action="store_true",
                        help="Run hourly research loop (default: 1 hour interval)")
    parser.add_argument("--flow", required=False,
                        choices=["multi-stage", "larry-slideshow", "tiktok-1min", "basic"],
                        help="Video generation flow")
    parser.add_argument("--room", help="Room type (for multi-stage, larry-slideshow)")
    parser.add_argument("--hook", help="Hook type (for multi-stage, larry-slideshow)")
    parser.add_argument("--niche", help="Niche (for tiktok-1min)")
    parser.add_argument("--prompt", help="Custom prompt (for basic)")
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds (for basic)")
    parser.add_argument("--mode", choices=["analyze", "log"], help="Operation mode")
    parser.add_argument("--hook-type", help="Hook type for log mode")
    parser.add_argument("--views", type=int, help="Views count for log mode")
    args = parser.parse_args()

    print("=" * 70)
    print("🚀 BERKAHKARYA FLEXIBLE CONTENT SYSTEM")
    print("=" * 70)
    print()

    if args.auto_research:
        print("Mode: Auto Research Loop")
        auto_research_loop()

    elif args.flow == "multi-stage":
        if not args.room or not args.hook:
            print("❌ --room and --hook required for multi-stage flow")
            return
        run_multi_stage(args.room, args.hook)

    elif args.flow == "larry-slideshow":
        if not args.room or not args.hook:
            print("❌ --room and --hook required for larry-slideshow flow")
            return
        run_larry_slideshow(args.room, args.hook)

    elif args.flow == "tiktok-1min":
        if not args.niche:
            print("❌ --niche required for tiktok-1min flow")
            return
        run_tiktok_1min(args.niche)

    elif args.flow == "basic":
        if not args.prompt:
            print("❌ --prompt required for basic flow")
            return
        run_basic(args.prompt, args.duration)

    elif args.mode == "analyze":
        analysis = analyze_performance()
        print("\n✅ Analysis complete")
        print(f"   Total hook types: {len(analysis)}")
        print(f"   Top 3: {[x[0] for x in analysis['top_3']]}")

    elif args.mode == "log":
        if not args.hook_type or args.views is None:
            print("❌ --hook-type and --views required for log mode")
            return
        log_performance(args.hook_type, args.views)
        print("\n✅ Logged performance")

    else:
        print("\n❌ No mode specified!")
        print("\n📋 AVAILABLE MODES:")
        print("1. Auto Research: --auto-research")
        print("2. Generate Content:")
        print("   --flow multi-stage --room <room> --hook <hook>")
        print("   --flow larry-slideshow --room <room> --hook <hook>")
        print("   --flow tiktok-1min --niche <niche>")
        print("   --flow basic --prompt <text> --duration <seconds>")
        print("3. Analytics: --mode analyze")
        print("4. Log Performance: --mode log --hook-type <type> --views <n>")
        print()
        parser.print_help()


if __name__ == "__main__":
    main()
