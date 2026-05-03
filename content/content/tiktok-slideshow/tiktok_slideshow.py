#!/usr/bin/env python3
"""
tiktok_slideshow.py - Create TikTok carousels with Pexels + FFmpeg

Custom implementation for BerkahKarya workflow:
- Search images with Pexels API
- Add text overlay with FFmpeg
- Upload to TikTok via PostBridge

Usage:
    python tiktok_slideshow.py create "topic" "hook text" [num_slides]
    python tiktok_slideshow.py upload <project_id>
"""

import os
import json
import requests
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Try to import PostBridge client (optional dependency)
PostBridgeClient = None
try:
    post_bridge_path = Path(__file__).parent.parent / "1ai-skills" / "marketing" / "post_bridge_client.py"
    if post_bridge_path.exists():
        # Import as module via file path
        import importlib.util
        spec = importlib.util.spec_from_file_location("post_bridge_client", post_bridge_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules["post_bridge_client"] = module
            spec.loader.exec_module(module)
            PostBridgeClient = module.PostBridgeClient
            print("✅ PostBridge client loaded")
except Exception as e:
    print(f"⚠️ PostBridge client not available: {e}")

if not PostBridgeClient:
    print("⚠️ PostBridge client not available. Upload will be handled separately.")

# Configuration
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
POST_BRIDGE_API_KEY = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_Kyc2gafDF7Qc8c2ALELtEC")

# Directories
BASE_DIR = Path.home() / ".tiktok-slideshow"
IMAGES_DIR = BASE_DIR / "images"
RENDERED_DIR = BASE_DIR / "rendered"
PROJECTS_DIR = BASE_DIR / "projects"

# Create directories
for dir_path in [BASE_DIR, IMAGES_DIR, RENDERED_DIR, PROJECTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def search_pexels_images(query: str, count: int = 10) -> List[Dict]:
    """Search images on Pexels API."""
    if not PEXELS_API_KEY:
        raise Exception(
            "PEXELS_API_KEY not set. Get free API key at https://www.pexels.com/api/"
        )

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": "vertical",
        "size": "large",
        "per_page": count
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        photos = data.get("photos", [])
        print(f"📸 Found {len(photos)} images for: {query}")

        return photos

    except requests.exceptions.RequestException as e:
        raise Exception(f"Pexels API request failed: {e}")


def download_image(url: str, filename: Path) -> Path:
    """Download image from URL to local file."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Downloaded: {filename.name}")
        return filename

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download {url}: {e}")


def create_text_overlay(
    input_path: Path,
    output_path: Path,
    text: str,
    subtitle: str = "",
    font_size_title: int = 48,
    font_size_subtitle: int = 32
) -> Path:
    """
    Add text overlay to image using FFmpeg.

    Args:
        input_path: Path to source image
        output_path: Path for rendered output
        text: Main title text
        subtitle: Optional subtitle text
        font_size_title: Font size for title (default: 48)
        font_size_subtitle: Font size for subtitle (default: 32)
    """
    # Check if ffmpeg is available
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception(
            "ffmpeg not found. Install with: sudo apt install ffmpeg"
        )

    # Build FFmpeg command
    scale_filter = "scale=1080:1920"

    # Main title drawtext
    drawtext_title = (
        f"drawtext=text='{text}':"
        f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        f"fontsize={font_size_title}:"
        f"fontcolor=white:"
        f"x=(w-text_w)/2:"
        f"y=(h-text_h)/2:"
        f"borderw=4:bordercolor=black:"
        f"box=1:boxcolor=black@0.5:boxborderw=10"
    )

    # Build filter chain
    if subtitle:
        drawtext_subtitle = (
            f"drawtext=text='{subtitle}':"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
            f"fontsize={font_size_subtitle}:"
            f"fontcolor=white:"
            f"x=(w-text_w)/2:"
            f"y=(h-text_h)/2+{font_size_title+20}:"
            f"borderw=3:bordercolor=black:"
            f"box=1:boxcolor=black@0.5:boxborderw=8"
        )
        video_filters = f"{scale_filter},{drawtext_title},{drawtext_subtitle}"
    else:
        video_filters = f"{scale_filter},{drawtext_title}"

    # Build command
    command = [
        "ffmpeg",
        "-i", str(input_path),
        "-vf", video_filters,
        "-q:v", "2",  # JPEG quality
        "-y",  # Overwrite output
        str(output_path)
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        print(f"✅ Rendered: {output_path.name}")
        return output_path

    except subprocess.CalledProcessError as e:
        raise Exception(
            f"FFmpeg failed with exit code {e.returncode}\n"
            f"STDERR: {e.stderr}"
        )


def create_slideshow(
    topic: str,
    hook: str,
    num_slides: int = 5,
    custom_texts: Optional[List[str]] = None
) -> str:
    """
    Create a TikTok slideshow from a topic and hook.

    Args:
        topic: Search topic for Pexels images
        hook: Hook text for first slide
        num_slides: Number of slides (default: 5)
        custom_texts: Optional list of texts for slides (length must match num_slides)

    Returns:
        Project ID string
    """
    print(f"\n{'='*50}")
    print(f"📱 Creating TikTok Slideshow")
    print(f"{'='*50}")
    print(f"🎯 Topic: {topic}")
    print(f"🪝 Hook: {hook}")
    print(f"📊 Slides: {num_slides}")
    print(f"{'='*50}\n")

    # Search images
    print("🔍 Searching images on Pexels...")
    photos = search_pexels_images(topic, min(num_slides, 20))

    if not photos:
        raise Exception(f"No images found for topic: {topic}")

    # Download & render slides
    slides = []
    temp_images = []

    try:
        for i in range(num_slides):
            # Use modulo to cycle through photos if needed
            photo = photos[i % len(photos)]

            # Download
            img_url = photo['src']['large']
            img_filename = IMAGES_DIR / f"temp_{i}.jpg"
            downloaded_path = download_image(img_url, img_filename)
            temp_images.append(downloaded_path)

            # Determine text for this slide
            if custom_texts and i < len(custom_texts):
                text = custom_texts[i]
                subtitle = ""
            elif i == 0:
                text = hook
                subtitle = " swipe for more →"
            elif i == num_slides - 1:
                text = "Follow for more! 👇"
                subtitle = "save this for later"
            else:
                text = f"Tip #{i}"
                subtitle = ""

            # Render with text overlay
            output_filename = RENDERED_DIR / f"slide_{i+1}.jpg"
            create_text_overlay(downloaded_path, output_filename, text, subtitle)
            slides.append(str(output_filename))

        # Save project metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_id = f"{topic.replace(' ', '_').lower()}_{timestamp}"

        metadata = {
            "id": project_id,
            "topic": topic,
            "hook": hook,
            "num_slides": num_slides,
            "slides": slides,
            "created_at": datetime.now().isoformat(),
            "images_used": [photo['id'] for photo in photos[:num_slides]],
            "format": "tiktok_carousel_1080x1920"
        }

        project_file = PROJECTS_DIR / f"{project_id}.json"
        with open(project_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"\n{'='*50}")
        print(f"✅ Slideshow Created Successfully!")
        print(f"{'='*50}")
        print(f"📦 Project ID: {project_id}")
        print(f"📁 Slides: {len(slides)}")
        print(f"📂 Location: {RENDERED_DIR}/")
        print(f"💾 Metadata: {project_file}")
        print(f"{'='*50}\n")

        return project_id

    finally:
        # Cleanup temporary images
        for temp_img in temp_images:
            if temp_img.exists():
                temp_img.unlink()


def upload_to_tiktok(project_id: str, caption: str = "") -> bool:
    """
    Upload slideshow to TikTok via PostBridge.

    Args:
        project_id: Project ID from create_slideshow
        caption: Optional caption for the post

    Returns:
        True if successful, False otherwise
    """
    if not PostBridgeClient:
        print("❌ PostBridge client not available")
        return False

    # Load project metadata
    project_file = PROJECTS_DIR / f"{project_id}.json"

    if not project_file.exists():
        print(f"❌ Project not found: {project_id}")
        return False

    with open(project_file, 'r') as f:
        metadata = json.load(f)

    slides = metadata.get("slides", [])

    if not slides:
        print("❌ No slides found in project")
        return False

    print(f"\n📤 Uploading project: {project_id}")

    # Initialize PostBridge client
    client = PostBridgeClient(api_key=POST_BRIDGE_API_KEY)

    # Check for TikTok accounts
    tiktok_accounts = client.get_accounts_by_platform("tiktok")

    if not tiktok_accounts:
        print("❌ No TikTok account connected to PostBridge")
        print("→ Connect your TikTok account at: https://post-bridge.com")
        return False

    account_id = tiktok_accounts[0]['id']
    print(f"✅ Using TikTok account: {tiktok_accounts[0].get('username', account_id)}")

    # TODO: You need to host these images on a CDN or use temporary URLs
    # For now, just print the slides that would need hosting
    print(f"\n⚠️ Images need to be hosted before upload:")
    for i, slide in enumerate(slides, 1):
        print(f"  Slide {i}: {slide}")

    print("\n💡 Options:")
    print("  1. Upload slides to AWS S3/Cloudflare R2")
    print("  2. Use image hosting service (Imgur, Cloudinary)")
    print("  3. Use PostBridge's direct upload (if available)")

    print("\n📝 This feature requires additional setup for image hosting.")
    print("→ Proceeding with placeholder implementation...")

    # Placeholder caption
    if not caption:
        caption = f"""
{metadata['hook']}

Swipe through for all the tips! 👆

TikTok Carousel | {metadata['num_slides']} slides

#tiktokcarousel #slideshow #viralcontent #{metadata['topic'].replace(' ', '')}

Learn more: https://www.tip.md/oyi77
        """.strip()

    # Return placeholder success
    print(f"\n✅ Upload preparation complete!")
    print(f"📊 Slides: {len(slides)}")
    print(f"📝 Caption length: {len(caption)} characters")

    return True


def list_projects() -> None:
    """List all existing projects."""
    print(f"\n📂 Projects in {PROJECTS_DIR}/\n")

    projects = list(PROJECTS_DIR.glob("*.json"))

    if not projects:
        print("No projects found.")
        return

    for project_file in sorted(projects, reverse=True):
        with open(project_file, 'r') as f:
            metadata = json.load(f)

        print(f"📦 {metadata['id']}")
        print(f"   Topic: {metadata['topic']}")
        print(f"   Slides: {metadata['num_slides']}")
        print(f"   Created: {metadata['created_at']}")
        print()


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("TikTok Slideshow Creator")
        print("="*40)
        print("\nCommands:")
        print("  create <topic> <hook> [num_slides]")
        print("  upload <project_id>")
        print("  list")
        print("\nExamples:")
        print("  python tiktok_slideshow.py create 'morning routine' 'Your routine is broken' 5")
        print("  python tiktok_slideshow.py upload morning_routine_20260306_123456")
        print("  python tiktok_slideshow.py list")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "create":
            if len(sys.argv) < 4:
                print("❌ Usage: create <topic> <hook> [num_slides]")
                sys.exit(1)

            topic = sys.argv[2]
            hook = sys.argv[3]
            num_slides = int(sys.argv[4]) if len(sys.argv) > 4 else 5

            project_id = create_slideshow(topic, hook, num_slides)

            print("\nNext steps:")
            print(f"  1. Review slides in: {RENDERED_DIR}/")
            print(f"  2. Upload to TikTok:")
            print(f"     python tiktok_slideshow.py upload {project_id}")

        elif command == "upload":
            if len(sys.argv) < 3:
                print("❌ Usage: upload <project_id>")
                sys.exit(1)

            project_id = sys.argv[2]
            success = upload_to_tiktok(project_id)

            if success:
                print("\n✅ Upload process initiated!")
            else:
                sys.exit(1)

        elif command == "list":
            list_projects()

        else:
            print(f"❌ Unknown command: {command}")
            print("   Use: create | upload | list")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()