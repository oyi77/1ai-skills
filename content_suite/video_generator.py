#!/usr/bin/env python3
"""
Video Generator — Animate hook frame images into short-form video (15-30 sec)
Technique: Ken Burns (pan+zoom) + text fade-in + outro CTA slide
Output: MP4 1080x1920 (9:16 vertical) for TikTok/Reels/Shorts

Usage:
  python3 video_generator.py --persona trading-finance --headline "5 Kesalahan Fatal Trader"
  python3 video_generator.py --batch              # generate for all personas today
"""
from __future__ import annotations
import argparse, json, os, subprocess, tempfile
from pathlib import Path
from datetime import datetime

WORKSPACE  = Path("/home/openclaw/.openclaw/workspace")
OUTPUT_DIR = WORKSPACE / "content_suite/output"
CS_DIR     = WORKSPACE / "content_suite"

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg","-version"], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        return False

def image_to_video(
    img_path: Path,
    out_path: Path,
    duration: int = 20,
    persona_id: str = "_default",
) -> Path:
    """
    Convert static PNG to animated MP4:
    - Slow zoom-in (Ken Burns effect)
    - Fade in at start, fade out at end
    - 1080x1350 → padded to 1080x1920 (9:16) with blur background
    - 24fps, h264, optimized for mobile
    """
    if not img_path.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    # FFmpeg filter chain:
    # 1. Scale image to 1080x1350
    # 2. Pad to 1080x1920 (9:16) with blurred version of itself as bg
    # 3. Ken Burns: slow zoom from 1.0x to 1.08x over duration
    # 4. Fade in (0.5s) and fade out (0.5s)

    filter_complex = (
        f"[0:v]scale=1080:1350,setsar=1[fg];"
        f"[0:v]scale=1080:1920,boxblur=20:1,setsar=1[bg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2[base];"
        f"[base]"
        f"zoompan=z='min(zoom+0.0008,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":d={duration*25}:s=1080x1920:fps=25,"
        f"fade=t=in:st=0:d=0.5,"
        f"fade=t=out:st={duration-0.5}:d=0.5"
        f"[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", str(img_path),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error:\n{result.stderr[-500:]}")

    return out_path


def batch_generate(date_str: str = None):
    """Generate videos for all personas with images today."""
    from persona_visual_engine import PersonaVisualEngine
    engine = PersonaVisualEngine()

    date_str = date_str or datetime.now().strftime("%Y%m%d")
    img_dir  = OUTPUT_DIR / date_str
    vid_dir  = OUTPUT_DIR / date_str / "videos"
    vid_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for img_path in sorted(img_dir.glob("*.png")):
        persona_id = img_path.stem.split("_")[0] + "-" + img_path.stem.split("_")[1] \
            if "_" in img_path.stem else "_default"
        # Fix persona_id detection from filename
        for pid in engine.personas:
            if img_path.name.startswith(pid):
                persona_id = pid
                break

        out_vid = vid_dir / img_path.with_suffix(".mp4").name
        if out_vid.exists():
            print(f"  ⏭️  Skip (exists): {out_vid.name}")
            generated.append(out_vid)
            continue

        print(f"  🎬 Generating: {img_path.name} → {out_vid.name}")
        try:
            video_path = image_to_video(img_path, out_vid, duration=18, persona_id=persona_id)
            size_mb = video_path.stat().st_size / 1e6
            print(f"     ✅ {video_path.name} ({size_mb:.1f} MB)")
            generated.append(video_path)
        except Exception as e:
            print(f"     ❌ Failed: {e}")

    return generated


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--image", type=str, help="Path to specific image")
    parser.add_argument("--duration", type=int, default=18)
    args = parser.parse_args()

    if not check_ffmpeg():
        print("❌ FFmpeg not installed. Run: sudo apt install ffmpeg")
        exit(1)

    if args.batch:
        print("🎬 Batch video generation...")
        videos = batch_generate()
        print(f"\n✅ Generated {len(videos)} videos")

    elif args.image:
        img = Path(args.image)
        out = img.parent / "videos" / img.with_suffix(".mp4").name
        vid = image_to_video(img, out, args.duration)
        print(f"✅ {vid}")
    else:
        parser.print_help()
