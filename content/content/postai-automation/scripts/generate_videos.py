#!/usr/bin/env python3
"""
POST AI Video Generator

Generate multiple TikTok/Instagram video variants from a single product image.
"""

import json
import os
import sys
import argparse
import requests
from pathlib import Path
from datetime import datetime

# Load config
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"

if not CONFIG_FILE.exists():
    print(f"❌ Config file not found! Copy config.example.json to config.json first.")
    sys.exit(1)

with open(CONFIG_FILE) as f:
    config = json.load(f)

POSTAI_API = config.get("postai", {})


def generate_videos(image_path, count=5, platform="tiktok", style="hype", language="id", output_dir=None):
    """
    Generate videos using POST AI API.

    Args:
        image_path: Path to product image
        count: Number of video variants to generate
        platform: Target platform (tiktok, instagram, threads)
        style: Video style (hype, calm, energetic, professional)
        language: Language for voice-over (id, en)
        output_dir: Output directory for videos

    Returns:
        List of generated video paths
    """
    api_key = POSTAI_API.get("api_key")
    endpoint = POSTAI_API.get("endpoint", "https://api.postai.com/v1")

    if not api_key:
        print("❌ POST AI API key not configured in config.json")
        return []

    # Setup output directory
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = SKILL_DIR / "outputs" / datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Generating {count} videos...")
    print(f"   Image: {image_path}")
    print(f"   Platform: {platform}")
    print(f"   Style: {style}")
    print(f"   Language: {language}")
    print(f"   Output: {output_path}")
    print()

    # TODO: Integrate with actual POST AI API
    # This is a placeholder - replace with actual API calls
    generated = []

    for i in range(1, count + 1):
        output_file = output_path / f"video_{i:03d}.mp4"

        # Simulate API call
        print(f"   → Generating video {i}/{count}...")

        # Placeholder: Replace with actual POST AI API call
        # Example:
        # response = requests.post(
        #     f"{endpoint}/generate",
        #     headers={"Authorization": f"Bearer {api_key}"},
        #     json={
        #         "image": image_path,
        #         "platform": platform,
        #         "style": style,
        #         "language": language,
        #         "count": 1
        #     }
        # )
        #
        # if response.status_code == 200:
        #     video_url = response.json()["video_url"]
        #     # Download video...
        #     generated.append(output_file)

        generated.append(str(output_file))

    print()
    print(f"✅ Generated {len(generated)} videos!")
    print(f"📁 Location: {output_path}")

    return generated


def main():
    parser = argparse.ArgumentParser(description="Generate TikTok/Instagram videos with POST AI")
    parser.add_argument("--image", required=True, help="Path to product image")
    parser.add_argument("--count", type=int, default=5, help="Number of videos to generate (default: 5)")
    parser.add_argument("--platform", default="tiktok", choices=["tiktok", "instagram", "threads"],
                        help="Target platform (default: tiktok)")
    parser.add_argument("--style", default="hype", choices=["hype", "calm", "energetic", "professional"],
                        help="Video style (default: hype)")
    parser.add_argument("--language", default="id", choices=["id", "en"],
                        help="Language for voice-over (default: id)")
    parser.add_argument("--output", help="Output directory (default: auto-generated)")

    args = parser.parse_args()

    # Validate image exists
    if not Path(args.image).exists():
        print(f"❌ Image not found: {args.image}")
        sys.exit(1)

    # Generate videos
    generated = generate_videos(
        image_path=args.image,
        count=args.count,
        platform=args.platform,
        style=args.style,
        language=args.language,
        output_dir=args.output
    )

    # Summary
    print()
    print("=" * 60)
    print("📊 GENERATION SUMMARY")
    print("=" * 60)
    print(f"Total videos: {len(generated)}")
    print(f"Platform: {args.platform}")
    print(f"Style: {args.style}")
    print()
    print("Next steps:")
    print("1. Preview videos: python scripts/previews.py --source <output_dir>")
    print("2. Upload videos: python scripts/auto_upload.py --source <output_dir>")
    print("=" * 60)


if __name__ == "__main__":
    main()