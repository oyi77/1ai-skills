#!/usr/bin/env python3
"""
BerkahKarya Viral TikTok Automation System

Full automation: Research → Generate → Upload → Track → Learn

Workflow:
1. Hourly research — Scan trending TikTok topics
2. Auto-generation — Run multi-stage I2V for top hooks
3. Post-Bridge — Upload as draft
4. Performance tracking — Log views, update confidence
5. Continuous improvement — System learns what works

Usage:
    python3 berkah_viral_automation.py --auto
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────
# Paths
VIRAL_SYSTEM_PATH = Path(__file__).parent / "viral_research_system.py"
MULTI_STAGE_PATH = Path(__file__).parent / "muli_stage_i2v.py"
WORKSPACE = Path(
    "/home/openclaw/.openclaw/workspace/skills/1ai-skills/content/content-generator/scripts"
)

OUTPUT_DIR = Path("/tmp/berkah_viral_automation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR = OUTPUT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

JAKARTA_OFFSET = timedelta(hours=7)

# Environment keys
POST_BRIDGE_KEY = os.environ.get("POST_BRIDGE_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
BYTEPLUS_API_KEY = os.environ.get("BYTEPLUS_API_KEY", "")


# ── LOGGING ──────────────────────────────────────────────────────────
def log(message: str, level: str = "INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)

    log_file = LOG_DIR / f"automation_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a") as f:
        f.write(log_line + "\n")


def log_json(data: dict, filename: str):
    """Save JSON data to file."""
    path = OUTPUT_DIR / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log(f"Saved: {path.name}", "INFO")


# ── MODULE 1: RESEARCH SYSTEM (viral_research_system.py) ─────
def run_research() -> dict:
    """Run viral research module."""
    log("Starting research module...", "INFO")

    # Run research mode
    cmd = ["python3", str(VIRAL_SYSTEM_PATH), "--mode", "research"]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(WORKSPACE),
        timeout=120,
    )

    if result.returncode != 0:
        log(f"Research failed: {result.stderr[-200:]}", "ERROR")
        return {}

    try:
        research_output = json.loads(result.stdout)
        log(
            f"Research complete: {len(research_output.get('topics', []))} topics found",
            "INFO",
        )
        return research_output
    except json.JSONDecodeError as e:
        log(f"Failed to parse research output: {e}", "ERROR")
        return {}


# ── MODULE 2: MULTI-STAGE I2V (muli_stage_i2v.py) ─────────────
def run_viral_generation(hook_type: str, room_type: str = "kitchen_small") -> dict:
    """Run multi-stage I2V video generation."""
    log(f"Starting video generation: {hook_type} + {room_type}", "INFO")

    # Run multi-stage I2V
    cmd = [
        "python3",
        str(MULTI_STAGE_PATH),
        "--room",
        room_type,
        "--hook",
        hook_type,
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(WORKSPACE),
        timeout=600,  # 10 minutes
    )

    if result.returncode != 0:
        log(f"Video generation failed: {result.stderr[-500:]}", "ERROR")
        return {}

    try:
        # Parse output path
        output_lines = result.stdout.split("\n")
        final_video = None

        for line in output_lines:
            if "Final:" in line:
                parts = line.split("Final:")
                if len(parts) > 1:
                    final_video = parts[1].strip()

        if not final_video:
            log("Could not find final video path in output", "ERROR")
            return {}

        log(f"Video generated: {Path(final_video).name}", "INFO")

        return {
            "video_path": final_video,
            "hook_type": hook_type,
            "room_type": room_type,
            "success": True,
        }
    except Exception as e:
        log(f"Failed to parse video output: {e}", "ERROR")
        return {}


# ── MODULE 3: PERFORMANCE TRACKING & CONFIDENCE ───────────────
def load_confidence_memory() -> dict:
    """Load confidence scores from research system."""
    memory_file = Path("/tmp/viral_research/memory/performance_memory.json")
    if memory_file.exists():
        with open(memory_file, "r") as f:
            return json.load(f)

    # Default confidence scores
    return {
        "landlord_kitchen": {"confidence": 0.9, "avg_views": 234000},
        "parent_bedroom": {"confidence": 0.75, "avg_views": 80000},
        "roommate_living": {"confidence": 0.65, "avg_views": 60000},
    }


def update_confidence(hook_type: str, views: int, memory: dict) -> dict:
    """Update confidence score based on performance."""
    current = memory.get(hook_type, {"confidence": 0.5, "avg_views": 50000})

    target_views = current["avg_views"]

    if views >= target_views:
        # Success — increase confidence
        new_conf = min(current["confidence"] + 0.1, 1.0)
        change = "UP"
    elif views < target_views * 0.5:
        # Failure — decrease confidence
        new_conf = max(current["confidence"] - 0.15, 0.2)
        change = "DOWN"
    else:
        # Neutral
        new_conf = current["confidence"]
        change = "STABLE"

    memory[hook_type] = {
        "confidence": new_conf,
        "avg_views": target_views,
    }

    log(
        f"Confidence {hook_type}: {change} ({current['confidence']:.2f} → {new_conf:.2f})",
        "INFO",
    )

    # Save updated memory
    memory_file = Path("/tmp/viral_research/memory/performance_memory.json")
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=2)

    return memory


def get_top_hooks(memory: dict, top_n: int = 2) -> list[str]:
    """Get top performing hooks based on confidence."""
    sorted_hooks = sorted(
        memory.items(),
        key=lambda x: x[1]["confidence"],
        reverse=True,
    )
    return [hook for hook, _ in sorted_hooks[:top_n]]


# ── ORCHESTRATION: MAIN AUTO LOOP ─────────────────────────────
def auto_loop(interval_hours: int = 1, max_iterations: int = None):
    """
    Run full automation loop:
    1. Research (every interval)
    2. Generate viral content (top hooks)
    3. Log performance
    4. Learn and improve
    """
    log("=" * 70)
    log("BERKAHKARYA VIRAL TIKTOK AUTOMATION SYSTEM", "INFO")
    log("=" * 70)
    log()
    log(f"Research interval: {interval_hours} hour(s)", "INFO")
    log(f"Max iterations: {max_iterations if max_iterations else 'unlimited'}", "INFO")
    log()

    iteration = 0
    last_research_time = datetime.now() - timedelta(
        hours=24
    )  # Force research on first run

    try:
        while True:
            iteration += 1
            now = datetime.now()
            now_wib = (now + JAKARTA_OFFSET).strftime("%Y-%m-%d %H:%M WIB")

            log("=" * 70)
            log(f"ITERATION {iteration} — {now_wib}", "INFO")
            log("=" * 70)
            log()

            # STEP 1: Research (every interval hours)
            time_since_research = (now - last_research_time).total_seconds()
            if time_since_research >= interval_hours * 3600:
                log("Running research module...", "INFO")
                research_data = run_research()
                last_research_time = now
                log_json(
                    research_data, f"research_{now.strftime('%Y%m%d_%H%M%S')}.json"
                )
            else:
                log(
                    f"Skipping research (last run: {int(time_since_research/3600)}h ago)",
                    "INFO",
                )
                research_data = {}

            # STEP 2: Get top hooks for generation
            memory = load_confidence_memory()
            top_hooks = get_top_hooks(memory, top_n=3)

            log(f"Top hooks by confidence: {', '.join(top_hooks)}", "INFO")

            # STEP 3: Generate viral content for each top hook
            generated_videos = []

            for hook_type in top_hooks:
                log(f"\nGenerating content for hook: {hook_type}", "INFO")

                # Pick room type (cycle through options)
                rooms = ["kitchen_small", "living_room_cozy", "bedroom_minimal"]
                room_type = rooms[iteration % len(rooms)]

                # Run multi-stage I2V generation
                result = run_viral_generation(hook_type, room_type)

                if result.get("success"):
                    video_path = Path(result["video_path"])
                    if video_path.exists():
                        size_mb = video_path.stat().st_size / (1024 * 1024)
                        log(f"  Video: {video_path.name} ({size_mb:.2f}MB)", "INFO")
                        generated_videos.append(
                            {
                                "hook_type": hook_type,
                                "room_type": room_type,
                                "video_path": str(video_path),
                                "video_size_mb": size_mb,
                                "timestamp": now.isoformat(),
                            }
                        )
                else:
                    log(f"  Failed: video not found", "ERROR")

            # STEP 4: Save generation summary
            summary = {
                "iteration": iteration,
                "timestamp": now.isoformat(),
                "timestamp_wib": now_wib,
                "research_data": research_data,
                "top_hooks": top_hooks,
                "generated_videos": generated_videos,
                "total_videos": len(generated_videos),
            }

            log_json(summary, f"iteration_{iteration:04d}.json")

            log()
            log("Iteration Summary:", "INFO")
            log(f"  Videos generated: {len(generated_videos)}", "INFO")
            log(
                f"  Total size: {sum(v['video_size_mb'] for v in generated_videos):.2f}MB",
                "INFO",
            )
            log()

            # Check max iterations
            if max_iterations and iteration >= max_iterations:
                log("Max iterations reached. Stopping.", "INFO")
                break

            # Wait before next iteration (default: 1 hour)
            log(f"Waiting {interval_hours} hour(s) before next iteration...", "INFO")
            log()
            time.sleep(interval_hours * 3600)

    except KeyboardInterrupt:
        log()
        log("=" * 70)
        log("System stopped by user", "INFO")
        log("=" * 70)
    except Exception as e:
        log()
        log(f"Error in automation loop: {e}", "ERROR")
        log("=" * 70)


# ── CLI ENTRY POINT ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Viral TikTok Automation System"
    )
    parser.add_argument("--auto", action="store_true", help="Run automatic loop")
    parser.add_argument(
        "--interval",
        type=int,
        default=1,
        help="Research interval in hours (default: 1)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Max number of iterations (default: unlimited)",
    )
    parser.add_argument(
        "--research-only", action="store_true", help="Run research module only"
    )
    parser.add_argument(
        "--generate-only", action="store_true", help="Run video generation only"
    )
    args = parser.parse_args()

    log()
    log("BerkahKarya Viral TikTok Automation System", "INFO")
    log("Version 1.0.0", "INFO")
    log()

    if args.research_only:
        log("Mode: Research Only", "INFO")
        research_data = run_research()
        log_json(research_data, "research_latest.json")
        log("Research complete", "INFO")

    elif args.generate_only:
        log("Mode: Generate Only", "INFO")

        memory = load_confidence_memory()
        top_hooks = get_top_hooks(memory, top_n=3)

        for hook_type in top_hooks:
            rooms = ["kitchen_small", "learning_room_cozy", "bedroom_minimal"]
            room_type = rooms[0]

            log(f"Generating: {hook_type} + {room_type}", "INFO")
            result = run_viral_generation(hook_type, room_type)

            if result.get("success"):
                log(f"Success: {result['video_path']}", "INFO")
            else:
                log(f"Failed: {result}", "ERROR")

    elif args.auto:
        log("Mode: Full Auto Loop", "INFO")
        log("Starting automation...", "INFO")
        log()
        auto_loop(interval_hours=args.interval, max_iterations=args.max_iterations)

    else:
        log(
            "No mode specified. Use --auto, --research-only, or --generate-only", "INFO"
        )
        parser.print_help()


if __name__ == "__main__":
    main()
