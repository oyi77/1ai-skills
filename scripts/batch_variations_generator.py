#!/usr/bin/env python3
"""
Batch Content Generator - Generate MANY variations easily
Uses existing tools (video_shorts, gemini, etc.)
"""

import subprocess
from pathlib import Path
import json

workspace = Path.home() / ".openclaw" / "workspace"
videos_dir = workspace / "videos"
images_dir = workspace / "variations" / "images"
images_dir.mkdir(parents=True, exist_ok=True)

# Load variation plan
variation_file = workspace / "jendralbot_variations.json"

# Product info
PRODUCTS = {
    "starter_ai_content": {
        "name": "Starter AI Content",
        "price": "Rp 49.000",
        "base_video": "videos/starter_ai_content_shorts.mp4"
    },
    "studio_marketplace_pro": {
        "name": "Studio Marketplace Pro",
        "price": "Rp 75.000",
        "base_video": "videos/studio_marketplace_pro_shorts.mp4"
    },
    "mesin_cetak_kuliner": {
        "name": "Mesin Cetak Kuliner",
        "price": "Rp 75.000",
        "base_video": "videos/mesin_cetak_kuliner_shorts.mp4"
    },
    "ai_content_pro": {
        "name": "AI Content Pro",
        "price": "Rp 89.000",
        "base_video": "videos/ai_content_pro_shorts.mp4"
    }
}

def generate_youtube_shorts_variations(product_key, num_variations=5):
    """Generate multiple YouTube Shorts with different durations"""
    product = PRODUCTS[product_key]
    base_video = workspace / product["base_video"]

    if not base_video.exists():
        print(f"❌ Base video not found: {base_video}")
        return []

    variations = []
    durations = [15, 20, 30, 45, 60]  # Different durations

    for i, duration in enumerate(durations[:num_variations]):
        output_file = videos_dir / f"{product_key}_shorts_{duration}s.mp4"

        # FFmpeg command with different duration
        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(base_video),
            "-vf",
            f"scale=1080:1920,zoompan=z='min(zoom+0.0015,1.5)':d={duration*30}:s=1080x1920",
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            str(output_file)
        ]

        print(f"🎬 Generating {product_key} - {duration}s version...")

        try:
            subprocess.run(cmd, capture_output=True, timeout=60)
            if output_file.exists():
                size_mb = output_file.stat().st_size / (1024 * 1024)
                print(f"   ✅ Created: {output_file.name} ({size_mb:.1f}MB)")
                variations.append(str(output_file))
            else:
                print(f"   ❌ Failed to create")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    return variations

def generate_captions_from_plan(product_key, num_variations=5):
    """Load captions from variation plan"""
    if not variation_file.exists():
        print(f"❌ Variation plan not found: {variation_file}")
        return []

    with open(variation_file) as f:
        plan = json.load(f)

    variations = plan["products"][product_key]["variations"][:num_variations]

    captions = []
    for var in variations:
        captions.append({
            "variation_id": var["variation_id"],
            "caption": var["caption"],
            "tags": var["tags"]
        })

    return captions

def main():
    print("=" * 80)
    print("🎨 BATCH CONTENT GENERATOR - VARIATIONS")
    print("=" * 80)
    print()

    # Generate variations for all products
    all_results = {}

    for product_key in PRODUCTS:
        print(f"\n{'='*80}")
        print(f"📦 Product: {PRODUCTS[product_key]['name']}")
        print(f"{'='*80}\n")

        # Generate video variations
        print("🎬 Generating YouTube Shorts variations...")
        videos = generate_youtube_shorts_variations(product_key, num_variations=5)

        # Load caption variations
        print(f"\n📝 Loading caption variations...")
        captions = generate_captions_from_plan(product_key, num_variations=5)

        # Save results
        all_results[product_key] = {
            "product": PRODUCTS[product_key]["name"],
            "videos": videos,
            "captions": captions
        }

        print(f"\n✅ Generated for {product_key}:")
        print(f"   Videos: {len(videos)}")
        print(f"   Captions: {len(captions)}")

    # Save batch results
    output_file = workspace / "batch_variations.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print()
    print("=" * 80)
    print("📊 BATCH GENERATION SUMMARY")
    print("=" * 80)
    print()

    for product_key, data in all_results.items():
        print(f"📦 {data['product']}")
        print(f"   Video variations: {len(data['videos'])}")
        print(f"   Caption variations: {len(data['captions'])}")
        print()

    print(f"✅ Results saved to: {output_file}")
    print()
    print("📋 NEXT STEPS:")
    print("1. Review generated videos in: videos/")
    print("2. Pick different video + caption combinations")
    print("3. Upload to YouTube")
    print("4. Post to TikTok via PostBridge")
    print("=" * 80)

if __name__ == "__main__":
    main()