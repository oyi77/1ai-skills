#!/usr/bin/env python3
"""
POST AI Batch Processor

Process multiple products from CSV - generate videos and upload automatically.
"""

import json
import csv
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen

# Load config
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"

if not CONFIG_FILE.exists():
    print(f"❌ Config file not found! Copy config.example.json to config.json first.")
    sys.exit(1)

with open(CONFIG_FILE) as f:
    config = json.load(f)

DEFAULTS = config.get("defaults", {})


def load_products(csv_path):
    """
    Load products from CSV file.

    Args:
        csv_path: Path to CSV file

    Returns:
        List of product dicts
    """
    products = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            products.append({
                "name": row.get("product_name", "").strip(),
                "image_url": row.get("image_url", "").strip(),
                "image_path": row.get("image_path", "").strip(),
                "price": row.get("price", "").strip(),
                "affiliate_link": row.get("affiliate_link", "").strip(),
                "caption_template": row.get("caption_template", "").strip()
            })

    return products


def download_image(url, output_path):
    """
    Download image from URL.

    Args:
        url: Image URL
        output_path: Destination path
    """
    try:
        print(f"   ↓ Downloading: {url}")

        with urlopen(url) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())

        print(f"   ✅ Saved to: {output_path}")
        return True
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
        return False


def generate_caption_for_product(product):
    """
    Generate caption for a product.

    Args:
        product: Product dict

    Returns:
        Generated caption string
    """
    template = product.get("caption_template") or """🔥 {name} - {price}

Jangan sampai kehabisan! Order sekarang:
{link}

{hashtags}"""

    # Format price
    price = product.get("price", "Rp 0")
    try:
        price_num = int("".join(c for c in price if c.isdigit()))
        price = f"Rp {price_num:,.0f}".replace(",", ".")
    except:
        pass

    # Generate hashtags
    hashtags = " ".join(DEFAULTS.get("caption_hashtags", ["#fyp", "#viral", "#affiliatemarketing"]))

    caption = template.format(
        name=product["name"],
        price=price,
        link=product["affiliate_link"],
        hashtags=hashtags
    )

    return caption


def process_product(product, platforms, videos_per_product, schedule):
    """
    Process a single product: download image, generate videos, upload.

    Args:
        product: Product dict
        platforms: Comma-separated platforms
        videos_per_product: Number of videos per product
        schedule: Comma-separated schedule

    Returns:
        Result dict
    """
    print(f"\n{'=' * 60}")
    print(f"📦 Processing: {product['name']}")
    print(f"{'=' * 60}")

    # Get or download image
    if product.get("image_path") and Path(product["image_path"]).exists():
        image_path = product["image_path"]
        print(f"✅ Using existing image: {image_path}")
    elif product.get("image_url"):
        # Download image
        image_dir = SKILL_DIR / "temp" / "images"
        image_dir.mkdir(parents=True, exist_ok=True)

        image_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{product['name'][:20].replace(' ', '_')}.jpg"
        image_path = image_dir / image_name

        if not download_image(product["image_url"], image_path):
            return {"success": False, "error": "Failed to download image"}
    else:
        return {"success": False, "error": "No image URL or path provided"}

    # Generate captions
    captions = []
    for _ in range(videos_per_product):
        caption = generate_caption_for_product(product)
        captions.append(caption)

    caption_file = SKILL_DIR / "temp" / f"captions_{product['name'][:20].replace(' ', '_')}.txt"
    caption_file.write_text("\n\n".join(captions))
    print(f"📝 Generated {len(captions)} captions")

    # Generate videos
    output_dir = SKILL_DIR / "outputs" / product['name'][:20].replace(' ', '_')

    print(f"\n🎬 Generating {videos_per_product} videos...")

    # Call generate_videos.py
    cmd = [
        sys.executable,
        str(SKILL_DIR / "scripts" / "generate_videos.py"),
        "--image", str(image_path),
        "--count", str(videos_per_product),
        "--platform", platforms.split(",")[0],  # Use first platform
        "--output", str(output_dir)
    ]

    print(f"   Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Generation failed:")
        print(result.stderr)
        return {"success": False, "error": "Video generation failed"}

    print(f"✅ Videos generated to: {output_dir}")

    # Upload to platforms
    print(f"\n📤 Uploading to platforms: {platforms}")

    for platform in platforms.split(","):
        platform = platform.strip()

        cmd = [
            sys.executable,
            str(SKILL_DIR / "scripts" / "auto_upload.py"),
            "--source", str(output_dir / "*.mp4"),
            "--platform", platform,
            "--caption-file", str(caption_file)
        ]

        if schedule:
            cmd.extend(["--schedule", schedule])

        print(f"\n   Uploading to {platform.upper()}...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"   ✅ Uploaded to {platform}")
        else:
            print(f"   ❌ Upload failed to {platform}")
            print(result.stderr)

    return {
        "success": True,
        "product": product['name'],
        "videos_generated": videos_per_product,
        "platforms": platforms,
        "output_dir": str(output_dir)
    }


def main():
    parser = argparse.ArgumentParser(description="Batch process products from CSV")
    parser.add_argument("--input", required=True, help="Path to CSV file")
    parser.add_argument("--platforms", default="tiktok",
                        help="Comma-separated platforms (default: tiktok)")
    parser.add_argument("--videos-per-product", type=int, default=10,
                        help="Number of videos per product (default: 10)")
    parser.add_argument("--schedule", help="Comma-separated schedule (e.g., '08:00,14:00,20:00')")

    args = parser.parse_args()

    # Load products
    print(f"📂 Loading products from: {args.input}")
    products = load_products(args.input)

    if not products:
        print("❌ No products found in CSV!")
        sys.exit(1)

    print(f"✅ Loaded {len(products)} products")

    # Process each product
    results = {
        "total": len(products),
        "success": 0,
        "failed": 0,
        "products": []
    }

    for i, product in enumerate(products, 1):
        print(f"\n\n{'#' * 60}")
        print(f"# Product {i}/{len(products)}")
        print(f"{'#' * 60}")

        result = process_product(
            product=product,
            platforms=args.platforms,
            videos_per_product=args.videos_per_product,
            schedule=args.schedule
        )

        results["products"].append(result)

        if result["success"]:
            results["success"] += 1
        else:
            results["failed"] += 1

        # Save summary after each product
        summary_file = SKILL_DIR / "batch_summary.jsonl"
        with open(summary_file, "a") as f:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "result": result
            }) + "\n")

    # Final summary
    print(f"\n\n{'=' * 60}")
    print("📊 BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total products: {results['total']}")
    print(f"Success: {results['success']} ✅")
    print(f"Failed: {results['failed']} ❌")
    print()
    print(f"Summary saved to: batch_summary.jsonl")
    print("=" * 60)


if __name__ == "__main__":
    main()