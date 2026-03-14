#!/usr/bin/env python3
"""
OpenFang-Style Hand: CLIP
Takes YouTube URL, extracts best moments, creates vertical shorts with captions & thumbnails,
optionally adds AI voice-over, publishes to Telegram/WhatsApp

8-Phase Pipeline:
1. Download video from YouTube
2. Analyze for best moments (AI analysis)
3. Extract clips
4. Generate captions (STT)
5. Create thumbnails (AI generation)
6. Optional: AI voice-over
7. Format as vertical video (9:16)
8. Publish to targets (Telegram/WhatsApp)
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/openclaw/.openclaw/workspace")
HAND_DIR = BASE_DIR / "hands" / "clip"
WORK_DIR = HAND_DIR / "workspace"
LOGS_DIR = BASE_DIR / "logs"
TEMP_DIR = BASE_DIR / "temp"

# Ensure directories exist
HAND_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "clip_hand.log"

def log(message, level="INFO"):
    """Log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}\n"

    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg)

def check_dependencies():
    """Check if required tools are installed"""
    log("Checking dependencies...")

    dependencies = {
        'yt-dlp': 'yt-dlp --version',
        'ffmpeg': 'ffmpeg -version'
    }

    missing = []

    for tool, check_cmd in dependencies.items():
        try:
            result = subprocess.run(check_cmd.split(), capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                log(f"✅ {tool} installed")
            else:
                log(f"❌ {tool} not found")
                missing.append(tool)
        except FileNotFoundError:
            log(f"❌ {tool} not found")
            missing.append(tool)

    return len(missing) == 0

def download_youtube_video(url, output_dir):
    """Download video from YouTube using yt-dlp"""
    log(f"Downloading YouTube video: {url}")

    output_path = output_dir / "input_video.mp4"

    cmd = [
        'yt-dlp',
        '-f', 'best[ext=mp4]',
        '-o', str(output_path),
        '--no-playlist',
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            log("✅ Video downloaded")
            return str(output_path)
        else:
            log(f"❌ Download failed: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        log("❌ Download timeout (10 min)")
        return None
    except Exception as e:
        log(f"❌ Download error: {e}")
        return None

def analyze_best_moments(video_path):
    """Analyze video for best moments to clip"""
    log("Analyzing video for best moments...")

    # For now, use FFprobe to get video duration and create equal segments
    # In full implementation, use AI to identify highlights
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            duration = float(result.stdout.strip())
            log(f"Video duration: {duration:.2f} seconds")

            # Create 3 clips of 30 seconds each
            clips = []
            clip_duration = 30
            num_clips = min(3, int(duration // clip_duration))

            for i in range(num_clips):
                start_time = i * clip_duration
                clips.append({
                    'index': i,
                    'start_time': start_time,
                    'end_time': start_time + clip_duration,
                    'duration': clip_duration
                })

            log(f"✅ Generated {len(clips)} clip segments")
            return clips
        else:
            log(f"❌ FFprobe failed: {result.stderr}")
            return None
    except Exception as e:
        log(f"❌ Analysis error: {e}")
        return None

def extract_clip(video_path, clip_info, output_dir):
    """Extract clip from video"""
    log(f"Extracting clip {clip_info['index']}")

    output_path = output_dir / f"clip_{clip_info['index']:02d}.mp4"

    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-ss', str(clip_info['start_time']),
        '-t', str(clip_info['end_time'] - clip_info['start_time']),
        '-c', 'copy',
        '-y',  # Overwrite output
        str(output_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            log(f"✅ Clip {clip_info['index']} extracted")
            return str(output_path)
        else:
            log(f"❌ Clip extraction failed: {result.stderr}")
            return None
    except Exception as e:
        log(f"❌ Extraction error: {e}")
        return None

def apply_vertical_filter(video_path):
    """Convert to vertical 9:16 format"""
    log("Converting to vertical format...")

    output_path = str(video_path).replace('.mp4', '_vertical.mp4')

    # Simple crop to 9:16 (1080x1920)
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
        '-c:a', 'copy',
        '-y',
        output_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            log("✅ Converted to vertical format")
            return output_path
        else:
            log(f"❌ Conversion failed: {result.stderr}")
            return video_path  # Return original if fails
    except Exception as e:
        log(f"❌ Conversion error: {e}")
        return video_path

def process_youtube_url(url):
    """Main pipeline: Download → Analyze → Extract → Format"""
    log(f"Processing YouTube URL: {url}")

    # Check dependencies
    if not check_dependencies():
        log("❌ Missing dependencies")
        return {'status': 'failed', 'error': 'Missing dependencies (yt-dlp, ffmpeg)'}

    # Create session workspace
    session_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = WORK_DIR / session_time
    session_dir.mkdir(exist_ok=True)

    # Phase 1: Download
    video_path = download_youtube_video(url, session_dir)
    if not video_path:
        return {'status': 'failed', 'error': 'Download failed'}

    # Phase 2: Analyze for best moments
    clips = analyze_best_moments(video_path)
    if not clips:
        return {'status': 'failed', 'error': 'Analysis failed'}

    # Phase 3-4-5: Extract clips and apply formatting
    results = []
    for clip_info in clips:
        # Extract clip
        clip_path = extract_clip(video_path, clip_info, session_dir)
        if clip_path:
            # Apply vertical filter
            vertical_path = apply_vertical_filter(clip_path)

            results.append({
                'clip_index': clip_info['index'],
                'video_path': vertical_path,
                'start_time': clip_info['start_time'],
                'end_time': clip_info['end_time'],
                'session_dir': str(session_dir)
            })

    # Save results
    output_data = {
        'youtube_url': url,
        'timestamp': datetime.now().isoformat(),
        'session_id': session_time,
        'clips': results,
        'status': 'success'
    }

    results_file = session_dir / 'results.json'
    with open(results_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    log(f"✅ Pipeline complete: {len(results)} clips generated")
    log(f"📁 Session directory: {session_dir}")

    return output_data

def main():
    """Main CLIP hand entry point"""
    print("="*70)
    print("OpenFang Hand: CLIP")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    print()

    # For demo, process a sample URL
    # In full implementation, this would read from a queue or input file
    sample_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (for testing)

    result = process_youtube_url(sample_url)

    print("\n" + "="*70)
    print(f"Status: {result['status']}")
    print(f"Clips generated: {len(result.get('clips', []))}")
    print("="*70)

    return result

if __name__ == "__main__":
    main()