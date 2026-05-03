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

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL (Pillow) not found. Install with: pip3 install Pillow")

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
POST_BRIDGE_API_KEY = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_BBLz9mjZkkL8q41tb2pwxq")

# ImgBB API Key (optional - get free at https://api.imgbb.com/)
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")

# Hosting provider (imgbb, googledrive)
HOST_PROVIDER = os.environ.get("HOST_PROVIDER", "imgbb")

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
    Add text overlay to image using PIL (Python Imaging Library).

    Args:
        input_path: Path to source image
        output_path: Path for rendered output
        text: Main title text
        subtitle: Optional subtitle text
        font_size_title: Font size for title (default: 48)
        font_size_subtitle: Font size for subtitle (default: 32)
    """
    if not PIL_AVAILABLE:
        raise Exception(
            "PIL (Pillow) not available. Install with: pip3 install Pillow"
        )

    try:
        # Open image
        img = Image.open(input_path)

        # Convert to RGB if needed (PIL can handle various formats)
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        # Resize image

        # Target size for TikTok (9:16 vertical)
        target_width = 1080
        target_height = 1920

        # Resize maintaining aspect ratio, then crop to fit
        img_ratio = img.width / img.height
        target_ratio = target_width / target_height

        if img_ratio != target_ratio:
            # Calculate new dimensions maintaining aspect ratio
            if img_ratio > target_ratio:
                # Image is wider than target
                new_width = target_width
                new_height = int(target_width / img_ratio)
            else:
                # Image is taller than target
                new_height = target_height
                new_width = int(target_height * img_ratio)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            # Create blank canvas
            canvas = Image.new('RGB', (target_width, target_height), (0, 0, 0))

            # Center image on canvas
            offset_x = (target_width - new_width) // 2
            offset_y = (target_height - new_height) // 2
            canvas.paste(img, (offset_x, offset_y))
            img = canvas
        else:
            img = img.resize((target_width, target_height), Image.LANCZOS)

        # Convert to RGBA for text overlay with transparency
        img_rgba = img.convert('RGBA')

        # Create drawing context
        draw = ImageDraw.Draw(img_rgba)

        # Try to load fonts, fallback to default
        try:
            # Try system fonts
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_title)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size_subtitle)
        except Exception:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            # Adjust size for default font
            font_size_title = 24
            font_size_subtitle = 18

        # Helper function to add text with background box
        def add_text_with_background(text_str, font, y_position, is_subtitle=False):
            # Get text dimensions
            bbox = draw.textbbox((0, 0), text_str, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Calculate padding
            padding = 20 if not is_subtitle else 15

            # Calculate box dimensions and position
            box_x = (target_width - text_width) // 2 - padding
            box_y = y_position - padding
            box_width = text_width + (padding * 2)
            box_height = text_height + (padding * 2)

            # Draw semi-transparent background box
            box_layer = Image.new('RGBA', (box_width, box_height), (0, 0, 0, 128))  # Black with 50% transparency
            img_rgba.paste(box_layer, (box_x, box_y), box_layer)

            # Draw text with outline
            outline_color = (0, 0, 0, 255)  # Black
            text_color = (255, 255, 255, 255)  # White

            # Draw outline (multiple offset draws)
            for x_offset in [-2, -1, 0, 1, 2]:
                for y_offset in [-2, -1, 0, 1, 2]:
                    if x_offset == 0 and y_offset == 0:
                        continue  # Skip center point (will draw main text)
                    text_x = (target_width - text_width) // 2 + x_offset
                    text_y = y_position + y_offset
                    draw.text((text_x, text_y), text_str, font=font, fill=outline_color)

            # Draw main text
            text_x = (target_width - text_width) // 2
            text_y = y_position
            draw.text((text_x, text_y), text_str, font=font, fill=text_color)

        # Calculate vertical positions
        if subtitle:
            # Both title and subtitle
            total_height = font_size_title + font_size_subtitle + 40  # 40px gap
            title_y = (target_height - total_height) // 2
            subtitle_y = title_y + font_size_title + 40
        else:
            # Title only
            title_y = (target_height - font_size_title) // 2

        # Add title text
        add_text_with_background(text, title_font, title_y, is_subtitle=False)

        # Add subtitle if provided
        if subtitle:
            add_text_with_background(subtitle, subtitle_font, subtitle_y, is_subtitle=True)

        # Convert back to RGB for JPEG output
        img_rgb = Image.new('RGB', img_rgba.size, (255, 255, 255))  # White background
        img_rgb.paste(img_rgba, mask=img_rgba.split()[3])
        img = img_rgb

        # Save as JPEG with quality
        img.save(output_path, 'JPEG', quality=95, optimize=True)

        print(f"✅ Rendered: {output_path.name}")
        return output_path

    except Exception as e:
        raise Exception(f"Failed to create text overlay: {e}")


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


def upload_images_to_hosting(slides: List[str], provider: str = "imgbb", folder_id: str = "", account: str = "") -> List[str]:
    """
    Upload all slides to specified hosting provider.

    Args:
        slides: List of slide file paths
        provider: Hosting provider (imgbb, googledrive)
        folder_id: Optional folder ID for Google Drive
        account: Optional Google account email for gog CLI

    Returns:
        List of public URLs
    """
    media_urls = []

    if provider == "imgbb":
        print(f"\n🖼️  Uploading {len(slides)} slides to ImgBB hosting...")

        for i, slide in enumerate(slides, 1):
            slide_path = Path(slide)
            if slide_path.exists():
                img_url = upload_to_imgbb(slide_path)
                if img_url:
                    media_urls.append(img_url)
                    print(f"  Slide {i}: ✅ {img_url[:50]}...")
                else:
                    print(f"  Slide {i}: ❌ Upload failed")
            else:
                print(f"  Slide {i}: ❌ File not found: {slide}")

    elif provider == "googledrive":
        account_info = f" (account: {account})" if account else ""
        print(f"\n☁️  Uploading {len(slides)} slides to Google Drive{account_info}...")

        for i, slide in enumerate(slides, 1):
            slide_path = Path(slide)
            if slide_path.exists():
                img_url = upload_to_googledrive(slide_path, folder_id, account)
                if img_url:
                    media_urls.append(img_url)
                    print(f"  Slide {i}: ✅ {img_url[:60]}...")
                else:
                    print(f"  Slide {i}: ❌ Upload failed")
            else:
                print(f"  Slide {i}: ❌ File not found: {slide}")

    else:
        print(f"⚠️  Unknown provider: {provider}")
        print("Using local file paths - images need to be hosted manually")
        media_urls = [f"file://{p}" for p in slides]

    return media_urls


def upload_to_tiktok(project_id: str, caption: str = "", auto_host: bool = True, host_provider: str = "imgbb", folder_id: str = "", account: str = "") -> bool:
    """
    Upload slideshow to TikTok via PostBridge.

    Args:
        project_id: Project ID from create_slideshow
        caption: Optional caption for the post
        auto_host: Auto-upload images to hosting (default: True)
        host_provider: Hosting provider (imgbb, googledrive)
        folder_id: Optional folder ID for Google Drive
        account: Optional Google account email for gog CLI

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

    # Step 1: Host images
    media_urls = []

    if auto_host:
        media_urls = upload_images_to_hosting(slides, host_provider, folder_id, account)
    else:
        print(f"\n⚠️ Skipping hosting - manual upload required")
        media_urls = [f"file://{p}" for p in slides]

    if not media_urls:
        print("❌ No images uploaded to hosting")
        return False

    # Step 2: Upload to TikTok via PostBridge
    print(f"\n📱 Posting to TikTok via PostBridge...")

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

    # Generate caption
    if not caption:
        caption = f"""{metadata['hook']}

Swipe through for all the tips! 👆

TikTok Carousel | {metadata['num_slides']} slides

#tiktokcarousel #slideshow #viralcontent #{metadata['topic'].replace(' ', '')}

Learn more: https://www.tip.md/oyi77
        """.strip()

    # Create post via PostBridge
    result = client.create_post(
        caption=caption,
        account_ids=[account_id],
        media_urls=media_urls,
    )

    if "error" in result:
        print(f"❌ Post creation failed: {result['error']}")
        return False

    print(f"\n✅ Success! TikTok carousel uploaded!")
    print(f"📦 Post ID: {result.get('id', 'N/A')}")
    print(f"📝 Caption length: {len(caption)} characters")
    print(f"📊 Media URLs: {len(media_urls)} slides")

    # Update project metadata with upload info
    metadata["uploaded"] = True
    metadata["uploaded_at"] = datetime.now().isoformat()
    metadata["post_id"] = result.get('id')
    metadata["media_urls"] = media_urls
    metadata["host_provider"] = host_provider

    with open(project_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n📝 Updated project metadata with upload info")

    return True


def upload_to_googledrive(image_path: Path, folder_id: str = "", account: str = "") -> Optional[str]:
    """
    Upload image to Google Drive via gog CLI.

    Args:
        image_path: Path to image file
        folder_id: Optional destination folder ID
        account: Optional Google account email

    Returns:
        Public shareable URL of uploaded file, or None if failed
    """
    try:
        # Upload file to Google Drive
        args = ["gog", "drive", "upload", str(image_path), "--json", "--name", image_path.name]

        if account:
            args.extend(["--account", account])

        if folder_id:
            args.extend(["--parent", folder_id])

        result = subprocess.run(args, capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            print(f"❌ Google Drive upload failed: {result.stderr}")
            return None

        # Parse JSON response
        try:
            data = json.loads(result.stdout)
            file_id = data.get("id")

            if not file_id:
                print(f"❌ No file ID in response: {result.stdout}")
                return None

            # Get shareable link
            share_args = ["gog", "drive", "share", file_id, "--json", "--force"]
            share_result = subprocess.run(share_args, capture_output=True, text=True, timeout=30)

            if share_result.returncode != 0:
                print(f"⚠️  Could not get share link: {share_result.stderr}")
                # Try to construct URL manually (Drive preview URL)
                preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                print(f"✅ Uploaded to Drive (manual link): {image_path.name}")
                return preview_url

            share_data = json.loads(share_result.stdout)
            share_url = share_data.get("webViewLink", share_data.get("webContentLink"))

            if share_url:
                print(f"✅ Uploaded to Google Drive: {image_path.name}")
                return share_url
            else:
                # Fallback to preview URL
                preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
                print(f"✅ Uploaded to Drive: {image_path.name}")
                return preview_url

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            return None

    except subprocess.TimeoutExpired:
        print(f"❌ Google Drive upload timeout")
        return None
    except Exception as e:
        print(f"❌ Google Drive upload failed: {e}")
        return None


def upload_to_imgbb(image_path: Path) -> Optional[str]:
    """
    Upload image to ImgBB hosting.

    Args:
        image_path: Path to image file

    Returns:
        Public URL of uploaded image, or None if failed
    """
    if not IMGBB_API_KEY:
        print("⚠️ IMGBB_API_KEY not set. Get free API key at: https://api.imgbb.com/")
        return None

    try:
        # Read and encode image as base64
        with open(image_path, 'rb') as f:
            image_data = f.read()

        import base64
        import io

        # Convert to base64
        buffered = io.BytesIO(image_data)
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Upload to ImgBB
        url = "https://api.imgbb.com/1/upload"
        params = {"key": IMGBB_API_KEY}

        data = {
            "image": img_base64,
            "name": image_path.stem,  # Filename without extension
        }

        response = requests.post(url, params=params, data=data, timeout=30)
        response.raise_for_status()

        result = response.json()

        if result.get("success"):
            img_url = result["data"]["url"]
            print(f"✅ Uploaded to ImgBB: {image_path.name}")
            return img_url
        else:
            print(f"❌ ImgBB upload failed: {result.get('error', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ ImgBB upload failed: {e}")
        return None


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
        print("  host <project_id> [--provider imgbb|googledrive] [--folder FOLDER_ID] [--account EMAIL]")
        print("  upload <project_id> [--no-host] [--provider imgbb|googledrive] [--folder FOLDER_ID] [--account EMAIL]")
        print("  list")
        print("\nExamples:")
        print("  python tiktok_slideshow.py create 'morning routine' 'Your routine is broken' 5")
        print("  python tiktok_slideshow.py host morning_routine_20260306_123456")
        print("  python tiktok_slideshow.py host morning_routine_20260306_123456 --provider googledrive")
        print("  python tiktok_slideshow.py host morning_routine_20260306_123456 --account you@gmail.com")
        print("  python tiktok_slideshow.py upload morning_routine_20260306_123456")
        print("  python tiktok_slideshow.py upload morning_routine_20260306_123456 --no-host")
        print("  python tiktok_slideshow.py upload morning_routine_20260306_123456 --provider googledrive --account you@gmail.com")
        print("  python tiktok_slideshow.py list")
        print("\nHosting Providers:")
        print("  imgbb        - Free image hosting (default)")
        print("  googledrive  - Google Drive (requires gog CLI setup)")
        print("\nEnvironment Variables:")
        print("  PEXELS_API_KEY        - Required for image search")
        print("  IMGBB_API_KEY         - Required for ImgBB hosting (https://api.imgbb.com/)")
        print("  POST_BRIDGE_API_KEY   - Required for TikTok upload")
        print("\nGoogle Drive Setup:")
        print("  gog auth add              # Add Google account")
        print("  gog auth status           # Check accounts")
        print("  python ... --account you@gmail.com  # Use specific account")
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
            print(f"  2. Host images:")
            print(f"     python tiktok_slideshow.py host {project_id}")
            print(f"  3. Upload to TikTok:")
            print(f"     python tiktok_slideshow.py upload {project_id}")

        elif command == "host":
            if len(sys.argv) < 3:
                print("❌ Usage: host <project_id> [--provider imgbb|googledrive] [--folder FOLDER_ID] [--account EMAIL]")
                sys.exit(1)

            project_id = sys.argv[2]

            # Parse flags
            provider = "imgbb"
            folder_id = ""
            account = ""

            if "--provider" in sys.argv:
                idx = sys.argv.index("--provider")
                if idx + 1 < len(sys.argv):
                    provider = sys.argv[idx + 1]
                    if provider not in ["imgbb", "googledrive"]:
                        print(f"❌ Invalid provider: {provider}")
                        print("   Use: imgbb or googledrive")
                        sys.exit(1)

            if "--folder" in sys.argv:
                idx = sys.argv.index("--folder")
                if idx + 1 < len(sys.argv):
                    folder_id = sys.argv[idx + 1]

            if "--account" in sys.argv:
                idx = sys.argv.index("--account")
                if idx + 1 < len(sys.argv):
                    account = sys.argv[idx + 1]

            # Load project metadata
            project_file = PROJECTS_DIR / f"{project_id}.json"
            if not project_file.exists():
                print(f"❌ Project not found: {project_id}")
                sys.exit(1)

            with open(project_file, 'r') as f:
                metadata = json.load(f)

            slides = metadata.get("slides", [])
            account_info = f" (account: {account})" if account else ""
            print(f"\n📤 Uploading {len(slides)} slides to {provider}{account_info}...")

            media_urls = upload_images_to_hosting(slides, provider, folder_id, account)

            if media_urls:
                print(f"\n✅ Uploaded {len(media_urls)} slides to {provider}!")
                print("\nMedia URLs:")
                for i, url in enumerate(media_urls, 1):
                    print(f"  {i}. {url}")

                # Save to file for reference
                urls_file = PROJECTS_DIR / f"{project_id}_urls.txt"
                with open(urls_file, 'w') as f:
                    for url in media_urls:
                        f.write(f"{url}\n")
                print(f"\n📝 URLs saved to: {urls_file}")
            else:
                print("\n❌ No images uploaded")
                sys.exit(1)

        elif command == "upload":
            if len(sys.argv) < 3:
                print("❌ Usage: upload <project_id> [--no-host] [--provider imgbb|googledrive] [--folder FOLDER_ID] [--account EMAIL]")
                sys.exit(1)

            project_id = sys.argv[2]

            # Parse flags
            auto_host = "--no-host" not in sys.argv
            provider = "imgbb"  # default
            folder_id = ""
            account = ""

            if "--provider" in sys.argv:
                idx = sys.argv.index("--provider")
                if idx + 1 < len(sys.argv):
                    provider = sys.argv[idx + 1]
                    if provider not in ["imgbb", "googledrive"]:
                        print(f"❌ Invalid provider: {provider}")
                        print("   Use: imgbb or googledrive")
                        sys.exit(1)

            if "--folder" in sys.argv:
                idx = sys.argv.index("--folder")
                if idx + 1 < len(sys.argv):
                    folder_id = sys.argv[idx + 1]

            if "--account" in sys.argv:
                idx = sys.argv.index("--account")
                if idx + 1 < len(sys.argv):
                    account = sys.argv[idx + 1]

            success = upload_to_tiktok(project_id, auto_host=auto_host, host_provider=provider, folder_id=folder_id, account=account)

            if success:
                print("\n✅ Upload process completed!")
            else:
                sys.exit(1)

        elif command == "list":
            list_projects()

        else:
            print(f"❌ Unknown command: {command}")
            print("   Use: create | upload | host | list")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()