#!/usr/bin/env python3
"""
Compile Maya betrayal story video using FFmpeg
"""

import subprocess
import json
import os
from pathlib import Path

# Configuration
scenes_dir = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories/scenes"
output_dir = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories"
final_video = os.path.join(output_dir, "maya_betrayal_story_001_short_916.mp4")

# Scene durations (in seconds) based on script timing
durations = [
    3.0,   # 01_hook_intro (0-3s)
    17.0,  # 02_partnership (3-20s)
    5.0,   # 03_success (20-25s)
    10.0,  # 04_betrayal (25-35s)
    5.0,   # 05_transfer (35-40s)
    5.0,   # 06_lawsuit (40-45s)
    10.0,  # 07_lesson (45-55s)
    5.0,   # 08_cta (55-60s)
]

scene_files = [
    "scene_01_hook_intro.png",
    "scene_02_partnership.png",
    "scene_03_success.png",
    "scene_04_betrayal.png",
    "scene_05_transfer.png",
    "scene_06_lawsuit.png",
    "scene_07_lesson.png",
    "scene_08_cta.png",
]

print("=" * 60)
print("Compiling Maya Betrayal Story Video")
print("=" * 60)

# Step 1: Create FFmpeg concat file
concat_file = os.path.join(output_dir, "scenes_concat.txt")
with open(concat_file, 'w') as f:
    for i, (scene_file, duration) in enumerate(zip(scene_files, durations)):
        scene_path = os.path.join(scenes_dir, scene_file)
        f.write(f"file '{scene_path}'\n")
        f.write(f"duration {duration}\n")

print(f"✓ Created concat file: {concat_file}")
print(f"  Total duration: {sum(durations)} seconds")

# Step 2: Compile video with crossfade transitions
raw_video = os.path.join(output_dir, "maya_raw.mp4")
transition_duration = 0.5  # seconds

# Use ffmpeg concat filter with transitions
ffmpeg_cmd = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_file,
    "-vf",
    # Add slow zoom-in effect for cinematic feel
    "zoompan=z='min(zoom+0.0015,1.5)':d=700:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)",
    "-c:v", "libx264",
    "-preset", "fast",
    "-crf", "23",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-y",
    raw_video
]

print(f"\nStep 2/4: Creating video with zoom effect...")
print(f"Command: {' '.join(ffmpeg_cmd)}")

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

if result.returncode != 0:
    print(f"✗ FFmpeg error: {result.stderr}")
    exit(1)

print(f"✓ Created temporary video: {raw_video}")

# Step 3: Check and fix video duration if needed
# Get actual duration
probe_cmd = [
    "ffprobe",
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    raw_video
]

result = subprocess.run(probe_cmd, capture_output=True, text=True)
if result.returncode == 0:
    actual_duration = float(result.stdout.strip())
    print(f"✓ Video duration: {actual_duration:.2f} seconds")
else:
    print(f"✗ Could not probe video duration")
    actual_duration = 60.0  # Assume

# Target duration: 60 seconds
target_duration = 60.0
if actual_duration < target_duration - 1 or actual_duration > target_duration + 1:
    print(f"\nStep 3/4: Adjusting duration to {target_duration}s...")

    adjusted_video = os.path.join(output_dir, "maya_adjusted.mp4")

    # Truncate or extend to exactly 60 seconds
    adjust_cmd = [
        "ffmpeg",
        "-i", raw_video,
        "-t", str(target_duration),
        "-c", "copy",
        "-y",
        adjusted_video
    ]

    subprocess.run(adjust_cmd, capture_output=True, text=True)

    # If too short, loop the last scene
    if actual_duration < target_duration:
        print(f"  Video too short, will extend last scene")
        extend_cmd = [
            "ffmpeg",
            "-stream_loop", "1",
            "-i", raw_video,
            "-t", str(target_duration),
            "-c", "copy",
            "-y",
            adjusted_video
        ]
        subprocess.run(extend_cmd, capture_output=True, text=True)

    working_video = adjusted_video
    print(f"✓ Adjusted video: {working_video}")
else:
    working_video = raw_video
    print(f"✓ Duration already correct, skipping adjustment")

# Step 4: Final compression
print(f"\nStep 4/4: Final compression for optimal file size...")

final_cmd = [
    "ffmpeg",
    "-i", working_video,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "26",
    "-c:a", "copy",
    "-movflags", "+faststart",
    "-y",
    final_video
]

result = subprocess.run(final_cmd, capture_output=True, text=True)

if result.returncode != 0:
    print(f"✗ Compression error: {result.stderr}")
    exit(1)

# Verify final video
verify_cmd = [
    "ffprobe",
    "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=width,height,duration,r_frame_rate",
    "-of", "json",
    final_video
]

result = subprocess.run(verify_cmd, capture_output=True, text=True)

print(f"\n✓ Final video created: {final_video}")

if result.returncode == 0:
    probe_data = json.loads(result.stdout)
    stream = probe_data['streams'][0]
    width = stream['width']
    height = stream['height']
    duration = float(stream['duration'])
    fps = eval(stream['r_frame_rate'])

    print(f"\nVideo Stats:")
    print(f"  Resolution: {width}x{height}")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  FPS: {fps}")

    # Check file size
    file_size = os.path.getsize(final_video) / (1024 * 1024)
    print(f"  File size: {file_size:.2f} MB")

    # Verify against requirements
    print(f"\nRequirements Check:")
    print(f"  Duration 45-60s: {'✓' if 45 <= duration <= 60 else '✗'} ({duration:.1f}s)")
    print(f"  Aspect ratio 9:16: {'✓' if width*1.777 < height*1.001 and width*1.777 > height*0.999 else '✗'} ({width}:{height})")
    print(f"  FPS ~30: {'✓' if 28 <= fps <= 32 else '✗'} ({fps:.1f})")
    print(f"  File size < 16MB: {'✓' if file_size < 16 else '✗'} ({file_size:.2f}MB)")

print("=" * 60)