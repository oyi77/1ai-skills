#!/usr/bin/env python3
"""
Image to YouTube Shorts Converter
Convert static images to vertical video for YouTube Shorts
"""

import subprocess
import os
import json
from pathlib import Path

# Products with image ideas
PRODUCT_IMAGE_CONFIGS = {
    "starter_ai_content": {
        "text": "STARTER AI CONTENT",
        "subtitle": "Rp 49.000",
        "cta": "Link in bio!",
        "duration": 15,
        "background": "#1a1a2e"
    },
    "studio_marketplace_pro": {
        "text": "STUDIO MARKETPLACE PRO",
        "subtitle": "Rp 75.000",
        "cta": "Tap link in bio",
        "duration": 15,
        "background": "#16213e"
    },
    "mesin_cetak_kuliner": {
        "text": "MESIN CETAK KULINER",
        "subtitle": "Rp 75.000",
        "cta": "Order now!",
        "duration": 15,
        "background": "#0f3460"
    },
    "ai_content_pro": {
        "text": "AI CONTENT PRO",
        "subtitle": "Rp 89.000",
        "cta": "Get it now",
        "duration": 20,
        "background": "#533483"
    },
    "guru_pintar_ai": {
        "text": "GURU PINTAR AI",
        "subtitle": "GRATIS!",
        "cta": "Free training",
        "duration": 15,
        "background": "#e94560"
    },
    "belanja_duit_balik": {
        "text": "BELANJA DUIT BALIK",
        "subtitle": "GRATIS!",
        "cta": "Cashback time",
        "duration": 15,
        "background": "#53354a"
    }
}

def create_video_from_image(image_path, output_path, config, image_only=False):
    """
    Create YouTube Shorts video from image

    Args:
        image_path: Path to source image
        output_path: Path for output video
        config: Product config dict
        image_only: If True, just output the image with text overlay
    """
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False

    duration = config.get("duration", 15)
    width = 1080
    height = 1920

    # If image_only True, create image with text overlay (no video)
    if image_only:
        # Create image with text overlay using FFmpeg
        text = config["text"]
        subtitle = config["subtitle"]
        cta = config["cta"]
        bg_color = config["background"]

        cmd = [
            "ffmpeg",
            "-i", image_path,
            "-vf",
            f"scale=1080:1350:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color={bg_color},"
            f"drawtext=text='{text}':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=h-500,"
            f"drawtext=text='{subtitle}':fontsize=60:fontcolor=#ffff00:x=(w-text_w)/2:y=h-380,"
            f"drawtext=text='{cta}':fontsize=50:fontcolor=#00ff00:x=(w-text_w)/2:y=h-280",
            "-frames:v", "1",
            "-y",
            output_path.replace(".mp4", ".jpg")
        ]
    else:
        # Create video with zoom effect
        text = config["text"]
        subtitle = config["subtitle"]
        cta = config["cta"]
        bg_color = config["background"]

        # Zoom in effect over duration
        zoom_cmd = f"zoompan=z='min(zoom+0.0015,1.5)':d={duration*30}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"

        cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", image_path,
            "-vf",
            f"scale=1080:1350:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color={bg_color},"
            f"{zoom_cmd},"
            f"drawtext=text='{text}':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=h-500,"
            f"drawtext=text='{subtitle}':fontsize=60:fontcolor=#ffff00:x=(w-text_w)/2:y=h-380,"
            f"drawtext=text='{cta}':fontsize=50:fontcolor=#00ff00:x=(w-text_w)/2:y=h-280",
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-r", "30",
            "-y",
            output_path
        ]

    print(f"🎬 Creating video: {output_path}")
    print(f"   Text: {text}")
    print(f"   Duration: {duration}s")
    print(f"   Output: {'Image with text' if image_only else 'Video with zoom'}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success! Output: {output_path}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def find_product_images():
    """Find product images in workspace"""
    workspace = Path.home() / ".openclaw" / "workspace"
    possible_paths = [
        workspace / "images",
        workspace / "content" / "images",
        Path.home() / "Pictures" / "jendralbot",
        Path.home() / "Downloads",
    ]

    found_images = {}
    for path in possible_paths:
        if path.exists():
            for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
                for img in path.glob(ext):
                    # Try to match product name
                    img_lower = img.name.lower()
                    for product_key in PRODUCT_IMAGE_CONFIGS:
                        if product_key.replace("_", "") in img_lower.replace("_", "").replace("-", ""):
                            if product_key not in found_images:
                                found_images[product_key] = str(img)

    return found_images

def generate_placeholder_images():
    """Generate simple colored placeholder images for products"""
    from PIL import Image, ImageDraw, ImageFont

    output_dir = Path.home() / ".openclaw" / "workspace" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    for product_key, config in PRODUCT_IMAGE_CONFIGS.items():
        # Create image
        img = Image.new('RGB', (1080, 1350), config["background"])
        draw = ImageDraw.Draw(img)

        # Draw product name
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)
        except:
            font_large = ImageFont.load_default()
            font_medium = font_large

        # Text positioning
        text = config["text"]
        bbox = draw.textbbox((0, 0), text, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (1080 - text_width) / 2
        y = (1350 - text_height) / 2 - 100

        draw.text((x, y), text, fill="white", font=font_large)

        subtitle = config["subtitle"]
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_medium)
        subtitle_width = bbox2[2] - bbox2[0]
        draw.text(((1080 - subtitle_width) / 2, y + 120), subtitle, fill="yellow", font=font_medium)

        cta = config["cta"]
        bbox3 = draw.textbbox((0, 0), cta, font=font_medium)
        cta_width = bbox3[2] - bbox3[0]
        draw.text(((1080 - cta_width) / 2, y + 220), cta, fill="#00ff00", font=font_medium)

        # Save
        output_path = output_dir / f"{product_key}_placeholder.jpg"
        img.save(output_path, quality=95)
        print(f"✅ Created placeholder: {output_path}")

def main():
    print("🎬 IMAGE TO YOUTUBE SHORTS CONVERTER")
    print("=" * 80)

    # Generate placeholder images first
    print("\n📸 Generating placeholder images...")
    generate_placeholder_images()

    # Find images
    found_images = find_product_images()
    print(f"\n🔍 Found {len(found_images)} product images")

    # Use placeholder images if no real images found
    workspace = Path.home() / ".openclaw" / "workspace"
    placeholder_dir = workspace / "images"

    if not found_images:
        print("⚠️  No product images found, using placeholders")

    # Create output directory
    output_dir = workspace / "videos"
    output_dir.mkdir(exist_ok=True)

    # Generate videos for all products
    print("\n🎬 Generating YouTube Shorts videos...")
    for product_key, config in PRODUCT_IMAGE_CONFIGS.items():
        # Use found image or placeholder
        image_path = found_images.get(product_key) or str(placeholder_dir / f"{product_key}_placeholder.jpg")

        output_path = str(output_dir / f"{product_key}_shorts.mp4")

        # Create video
        success = create_video_from_image(image_path, output_path, config, image_only=False)

        if success:
            # Also create image version for Instagram story
            img_output = output_path.replace(".mp4", "_image.jpg")
            create_video_from_image(image_path, img_output, config, image_only=True)

    print("\n" + "=" * 80)
    print("✅ DONE! Videos created in:")
    print(f"   {output_dir}")
    print("\n📋 Next steps:")
    print("1. Review videos")
    print("2. Upload to YouTube Shorts")
    print("3. Add trending audio in YouTube editor")
    print("=" * 80)

if __name__ == "__main__":
    main()