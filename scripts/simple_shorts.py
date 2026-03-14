#!/usr/bin/env python3
"""
Simple YouTube Shorts Generator - No Complex Filters
Convert images to vertical videos (zoom effect only)
"""

import subprocess
from pathlib import Path

def create_simple_video(image_path, output_path, duration=15):
    """
    Create simple video with zoom effect from image

    Args:
        image_path: Path to source image
        output_path: Path for output video
        duration: Video duration in seconds
    """
    if not Path(image_path).exists():
        print(f"❌ Image not found: {image_path}")
        return False

    # Simple zoom effect - scale from 1080:1350 to 1080:1920 (vertical padding)
    # Then zoom in slightly over duration
    cmd = [
        "ffmpeg",
        "-loop", "1",
        "-i", image_path,
        "-vf",
        # 1. Scale image to fit (width=1080, keep aspect ratio)
        # 2. Pad to 1080x1920 (vertical video format)
        # 3. Zoom in effect
        "scale=1080:1350:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"zoompan=z='min(zoom+0.0015,1.3)':d={duration*30}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
        "-c:v", "libx264",
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-y",
        output_path
    ]

    print(f"🎬 Creating: {output_path}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print(f"✅ Created: {output_path}")
            return True
        else:
            print(f"❌ Error:\n{result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout creating {output_path}")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("🎬 SIMPLE YOUTUBE SHORTS GENERATOR")
    print("=" * 80)

    workspace = Path.home() / ".openclaw" / "workspace"
    images_dir = workspace / "images"
    videos_dir = workspace / "videos"
    videos_dir.mkdir(exist_ok=True)

    # List all placeholder images
    images = list(images_dir.glob("*_placeholder.jpg"))

    print(f"\n📸 Found {len(images)} images")

    if not images:
        print("❌ No images found!")
        return

    # Generate videos
    success_count = 0
    for image in images:
        product_name = image.stem.replace("_placeholder", "")
        output_path = str(videos_dir / f"{product_name}_shorts.mp4")

        if create_simple_video(str(image), output_path, duration=15):
            success_count += 1

    print("\n" + "=" * 80)
    print(f"✅ Done! Created {success_count}/{len(images)} videos")
    print(f"📁 Output: {videos_dir}")
    print("\n📋 Next steps:")
    print("1. Videos are ready (15s each, 1080x1920, zoom effect)")
    print("2. Upload to YouTube Shorts")
    print("3. Add your own text/overlay in YouTube editor")
    print("4. Add trending audio")
    print("=" * 80)

if __name__ == "__main__":
    main()