#!/usr/bin/env python3
"""
Fix video aspect ratio to 9:16 (vertical) - cropping strategy
"""

import subprocess
import json
import os

input_video = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories/maya_betrayal_story_001_short_916.mp4"
output_video = "/home/openclaw/.openclaw/workspace/animated_cartoon/maya_betrayal_stories/maya_betrayal_story_001_short_916_fixed.mp4"

print("=" * 60)
print("Fixing Aspect Ratio to 9:16")
print("=" * 60)

# Input: 1280x720 (16:9)
# Target: 1080x1920 (9:16)
# Strategy: Scale height to 1920, crop width to 1080 (center crop)

# New dimensions after scale:
# Height: 720 → 1920 (scale factor: 1920/720 = 2.6667)
# Width: 1280 × 2.6667 = 3413
# Then crop to 1080x1920

ffmpeg_cmd = [
    "ffmpeg",
    "-i", input_video,
    "-vf",
    "scale=-2:1920:flags=neighbor,crop=1080:1920:(iw-1080)/2:(ih-1920)/2",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "26",
    "-c:a", "copy",
    "-movflags", "+faststart",
    "-y",
    output_video
]

print(f"Converting 1280x720 to 1080x1920 (9:16)...")
print(f"Strategy: Scale height to 1920, crop width to 1080 (center crop)")

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

if result.returncode != 0:
    print(f"✗ Error: {result.stderr}")
    exit(1)

# Verify output
verify_cmd = [
    "ffprobe",
    "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=width,height,duration,r_frame_rate",
    "-of", "json",
    output_video
]

result = subprocess.run(verify_cmd, capture_output=True, text=True)

print(f"\n✓ Fixed video: {output_video}")

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
    print(f"  FPS: {fps:.1f}")
    print(f"  Aspect ratio: {width}:{height} = {width/height:.2f}")

    file_size = os.path.getsize(output_video) / (1024 * 1024)
    print(f"  File size: {file_size:.2f} MB")

    print(f"\nRequirements Check:")
    print(f"  Duration 45-60s: {'✓' if 45 <= duration <= 60 else '✗'} ({duration:.1f}s)")
    print(f"  Aspect ratio 9:16: {'✓' if abs(width/height - 9/16) < 0.01 else '✗'} ({width}:{height})")
    print(f"  FPS ~30: {'✓' if 28 <= fps <= 32 else '✗'} ({fps:.1f})")
    print(f"  File size < 16MB: {'✓' if file_size < 16 else '✗'} ({file_size:.2f}MB)")

    # Replace original with fixed version
    os.replace(output_video, input_video)
    print(f"\n✓ Replaced original with fixed version")
else:
    print(f"✗ Could not verify video")

print("=" * 60)