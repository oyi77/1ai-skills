#!/usr/bin/env python3
"""
YouTube Upload Helper - Upload videos and get hosted URLs
Manual upload instructions because YouTube requires OAuth
"""

from pathlib import Path
import subprocess
import json

WORKSPACE = Path.home() / ".openclaw" / "workspace"
VIDEOS_DIR = WORKSPACE / "videos"
UPLOADS = []

def list_videos():
    """List all generated videos"""
    videos = list(VIDEOS_DIR.glob("*_shorts.mp4"))

    print("=" * 80)
    print("📹 AVAILABLE VIDEOS FOR UPLOAD")
    print("=" * 80)
    print(f"Location: {VIDEOS_DIR}")
    print(f"Total Videos: {len(videos)}")
    print()

    for i, video in enumerate(videos, 1):
        size_mb = video.stat().st_size / (1024 * 1024)
        print(f"{i}. {video.name}")
        print(f"   Size: {size_mb:.1f} MB")
        print(f"   Path: {video}")
        print()

    return videos

def get_upload_instructions():
    """Get YouTube upload instructions"""

    instructions = """
═════════════════════════════════════════════════════════════════════
🎬 YOUTUBE UPLOAD INSTRUCTIONS (MANUAL)
═════════════════════════════════════════════════════════════════════

Step 1: Open YouTube Studio
   → Go to: https://studio.youtube.com
   → Login with your YouTube account

Step 2: Upload Videos
   → Click "Create" → "Upload videos"
   → Select videos from: ~/.openclaw/workspace/videos/

Step 3: Upload Settings (For each video)
   Privacy: "Unlisted" or "Public" (Recommended: Unlisted first)
   Title: [Product Name] - [Price] - Jendralbot
   Example: "Starter AI Content - Rp 49.000 - Jendralbot"

Step 4: Description
   Copy caption from POSTING_GUIDE_TODAY.md

Step 5: Tags
   Copy hashtags from caption

Step 6: After Upload Complete:
   → Click "Share" or copy video URL
   → Format: https://www.youtube.com/watch?v=VIDEO_ID
   → Copy this URL!

═════════════════════════════════════════════════════════════════════
📋 VIDEOS TO UPLOAD:
═════════════════════════════════════════════════════════════════════

"""

    return instructions

def generate_upload_form():
    """Generate form for users to fill after uploading"""

    form = """
╔═══════════════════════════════════════════════════════════════════╗
║  YOUTUBE UPLOAD FORM - FILL AFTER UPLOADING EACH VIDEO            ║
╚═══════════════════════════════════════════════════════════════════╝

Copy each video URL here after uploading to YouTube:

1. Starter AI Content (Rp 49.000)
   Video: starter_ai_content_shorts.mp4
   URL: ______________________________________________

2. Studio Marketplace Pro (Rp 75.000)
   Video: studio_marketplace_pro_shorts.mp4
   URL: ______________________________________________

3. Mesin Cetak Kuliner (Rp 75.000)
   Video: mesin_cetak_kuliner_shorts.mp4
   URL: ______________________________________________

4. AI Content Pro (Rp 89.000)
   Video: ai_content_pro_shorts.mp4
   URL: ______________________________________________

5. Guru Pintar AI (GRATIS)
   Video: guru_pintar_ai_shorts.mp4
   URL: ______________________________________________

6. Belanja Duit Balik (GRATIS)
   Video: belanja_duit_balik_shorts.mp4
   URL: ______________________________________________

═════════════════════════════════════════════════════════════════════

After filling ALL URLs:
→ Run: python3 scripts/postbridge_poster.py
→ Enter each URL when prompted
→ Videos will be posted to all TikTok accounts!

═════════════════════════════════════════════════════════════════════
"""

    return form

def main():
    print("=" * 80)
    print("🎬 YOUTUBE UPLOAD HELPER")
    print("=" * 80)
    print()

    # List videos
    videos = list_videos()

    # Show instructions
    print(get_upload_instructions())

    # Show form
    print()
    print(generate_upload_form())

    # Save form to file
    form_file = WORKSPACE / "youtube_upload_form.txt"
    with open(form_file, "w") as f:
        f.write(get_upload_instructions())
        f.write("\n")
        f.write(generate_upload_form())

    print()
    print(f"✅ Form saved to: {form_file}")
    print()
    print("=" * 80)
    print("📋 NEXT STEPS:")
    print("=" * 80)
    print("1. Open YouTube Studio: https://studio.youtube.com")
    print("2. Upload all 6 videos from: ~/.openclaw/workspace/videos/")
    print("3. Get URLs for each video")
    print("4. Run: python3 scripts/postbridge_poster.py")
    print("5. Enter video URLs when prompted")
    print("6. Videos will post to all 5 TikTok accounts!")
    print("=" * 80)

if __name__ == "__main__":
    main()