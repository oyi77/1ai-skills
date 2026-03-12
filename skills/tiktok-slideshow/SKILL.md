---
name: tiktok-slideshow
description: >
  Creates TikTok image carousels with text overlays using Pexels API & FFmpeg, then uploads via PostBridge API.
  Use when the user wants to: create TikTok slideshows or carousels, search images for social media content,
  post or upload slideshow content to TikTok, edit slide text, or manage image collections for content creation.
  Do NOT use for: general TikTok account management, TikTok analytics or metrics, video editing or
  video creation (this is for photo slideshows only), non-TikTok social media platforms, or any task unrelated
  to creating visual slideshow content for TikTok.
metadata:
  {
    "openclaw": {
      "emoji": "📱",
      "requires": { "bins": ["ffmpeg", "curl"], "env": ["PEXELS_API_KEY"] }
    }
  }
---

# TikTok Slideshow (Pexels + FFmpeg + PostBridge)

**Custom implementation for BerkahKarya** - Creates TikTok carousels with professional text overlays.

## Architecture

**Flow:**
```
Topic Research → Pexels Image Search → FFmpeg Text Overlay → PostBridge Upload → TikTok Carousel
```

**Stack:**
- **Image Search**: Pexels API (high-quality stock photos/videos)
- **Text Overlay**: FFmpeg (professional text rendering)
- **Upload**: PostBridge API (multi-platform posting)
- **Format**: TikTok Carousel 1080×1920px (9:16 vertical)

---

## Prerequisites

### 1. Pexels API Key

Get FREE API key at: https://www.pexels.com/api/

Set environment variable:
```bash
export PEXELS_API_KEY="your_pexels_api_key_here"
```

### 2. PostBridge API Key

Already configured in PostBridge Client:

```bash
export POST_BRIDGE_API_KEY="pb_live_Kyc2gafDF7Qc8c2ALELtEC"
export POST_BRIDGE_BASE_URL="https://api.post-bridge.com/v1"
```

### 3. FFmpeg Installation

Check if installed:
```bash
ffmpeg -version
```

**Install:**
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Alternative: Use Docker
docker run -v $(pwd):/workdir -it jrottenberg/ffmpeg:latest
```

### 4. Directory Structure

Skill will create:
```
~/.tiktok-slideshow/
├── images/          # Downloaded from Pexels
├── rendered/        # FFmpeg rendered slides
├── scripts/         # Helper scripts
└── projects/        # Project metadata
```

---

## TikTok Carousel Best Practices (2026)

**Algorithm Metrics** (from latest research):
- **Swipe-through rate**: Percentage of users who swipe all slides
- **Dwell time**: Time spent viewing each slide
- **Reverse swipes**: Users swiping back to re-view

**Optimal Format:**
```
Resolution: 1080 × 1920px (9:16 vertical)
Slides: 5-10 images (best engagement)
Image size: < 100KB per slide (fast loading)
Aspect ratio: 9:16 (native TikTok)
```

**Engagement Tips:**
1. **Hook in first slide**: Bold, attention-grabbing text
2. **Storytelling progression**: Each slide builds on previous
3. **CTA on last slide**: Follow, save, share, or link
4. **Consistent visual style**: Same font, color palette
5. **High-quality images**: Use high-res Pexels images

**Text Overlay Best Practices:**
- Font size: 32-48px for titles, 24-32px for subtitles
- Position: Centered with margins
- Color: White text with black outline (high contrast)
- Background: Semi-transparent dark box for readability
- Length: Max 2-3 lines per slide

---

## Complete Workflow

### Step 1: Search Images with Pexels API

```bash
POST https://api.pexels.com/v1/search
Authorization: {PEXELS_API_KEY}

Query Parameters:
- query: "morning routine aesthetic"
- orientation: "vertical"  # For TikTok 9:16
- size: "large"
- per_page: 20

Response:
{
  "photos": [
    {
      "id": 123456,
      "url": "https://...",
      "src": {
        "original": "https://...",
        "large2x": "https://...",
        "large": "https://...",
        "medium": "https://...",
        "small": "https://..."
      },
      "photographer": "John Doe",
      "alt": "Aesthetic morning routine"
    }
  ]
}
```

**Recommendation**: Download `large` quality (best balance of quality + size).

### Step 2: Download Images

```python
import requests

def download_image(url, filename):
    """Download image from Pexels URL."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Downloaded: {filename}")
```

### Step 3: Create Text Overlay with FFmpeg

**Basic FFmpeg command:**
```bash
ffmpeg -i input.jpg \
  -vf "drawtext=text='Your Text':fontfile=/path/to/font.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=3:bordercolor=black" \
  -vf "scale=1080:-1" \
  output.jpg
```

**Advanced FFmpeg command (with background box):**
```bash
ffmpeg -i input.jpg \
  -vf "
    scale=1080:1920,
    drawtext=text='Hook Text Here':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=4:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=10
  " \
  -q:v 2 \
  output.jpg
```

**Parameter explanations:**
- `scale=1080:1920`: Resize to TikTok format
- `fontsize=48`: Title font size (use 32 for subtitle)
- `fontcolor=white`: Text color
- `borderw=4:bordercolor=black`: Text outline
- `box=1:boxcolor=black@0.5`: Semi-transparent background box
- `boxborderw=10`: Box padding around text
- `-q:v 2`: JPEG quality (lower = better, 2-5 recommended)

**Multiple lines + subtitle:**
```bash
ffmpeg -i input.jpg \
  -vf "
    scale=1080:1920,
    drawtext=text='Main Title':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=4:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=10,
    drawtext=text='Subtitle here':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=32:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+80:borderw=3:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=8
  " \
  -q:v 2 \
  output.jpg
```

### Step 4: Upload to TikTok via PostBridge

Using PostBridge client:

```python
from skills_1ai_skills.marketing.post_bridge_client import PostBridgeClient

client = PostBridgeClient()

# Get TikTok account
tiktok_accounts = client.get_accounts_by_platform("tiktok")
if not tiktok_accounts:
    raise Exception("No TikTok account connected")

account_id = tiktok_accounts[0]['id']

# Prepare media URLs (host your images)
# You'll need to host rendered images on a CDN or use temporary URLs
media_urls = [
    "https://your-cdn.com/slide-1.jpg",
    "https://your-cdn.com/slide-2.jpg",
    # ...
]

# Create post
result = client.create_post(
    caption="""
Your carousel caption here...

Save this for later! 👇

#tiktokcarousel #slideshow #viralcontent
    """.strip(),
    account_ids=[account_id],
    media_urls=media_urls,
)

if "error" in result:
    print(f"❌ Upload failed: {result['error']}")
else:
    print(f"✅ Uploaded successfully! Post ID: {result['id']}")
```

---

## Complete Example Script

```python
#!/usr/bin/env python3
"""
tiktok_slideshow.py - Create TikTok carousels with Pexels + FFmpeg + PostBridge

Usage:
    python tiktok_slideshow.py create "topic" "hook" 5
    python tiktok_slideshow.py upload project_name
"""

import os
import json
import requests
import subprocess
from pathlib import Path
from typing import List, Dict

# Configuration
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
POST_BRIDGE_API_KEY = os.environ.get("POST_BRIDGE_API_KEY", "pb_live_Kyc2gafDF7Qc8c2ALELtEC")

# Directories
BASE_DIR = Path.home() / ".tiktok-slideshow"
IMAGES_DIR = BASE_DIR / "images"
RENDERED_DIR = BASE_DIR / "rendered"
PROJECTS_DIR = BASE_DIR / "projects"

for dir_path in [BASE_DIR, IMAGES_DIR, RENDERED_DIR, PROJECTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def search_pexels_images(query: str, count: int = 10) -> List[Dict]:
    """Search images on Pexels."""
    if not PEXELS_API_KEY:
        raise Exception("PEXELS_API_KEY not set")

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": "vertical",
        "size": "large",
        "per_page": count
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    photos = response.json().get("photos", [])
    print(f"📸 Found {len(photos)} images for: {query}")

    return photos


def download_image(url: str, filename: Path) -> Path:
    """Download image from URL."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Downloaded: {filename}")
    return filename


def create_text_overlay(input_path: Path, output_path: Path, text: str, subtitle: str = "") -> Path:
    """Add text overlay to image using FFmpeg."""
    # FFmpeg command for text overlay
    command = [
        "ffmpeg",
        "-i", str(input_path),
        "-vf", f"scale=1080:1920,drawtext=text='{text}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=4:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=10",
        "-q:v", "2",
        "-y",  # Overwrite output
        str(output_path)
    ]

    if subtitle:
        # Add subtitle as second drawtext chain
        command[3] = f"scale=1080:1920,drawtext=text='{text}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=4:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=10,drawtext=text='{subtitle}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=32:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+80:borderw=3:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=8"

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"FFmpeg failed: {result.stderr}")

    print(f"✅ Rendered: {output_path}")
    return output_path


def create_slideshow(topic: str, hook: str, num_slides: int = 5) -> str:
    """Create a TikTok slideshow."""
    print(f"\n📱 Creating slideshow for: {topic}")
    print(f"🎯 Hook: {hook}")
    print(f"📊 Slides: {num_slides}\n")

    # Search images
    photos = search_pexels_images(topic, num_slides)

    # Download & render slides
    slides = []

    for i, photo in enumerate(photos, 1):
        # Download
        img_url = photo['src']['large']
        img_filename = IMAGES_DIR / f"temp_{i}.jpg"
        download_image(img_url, img_filename)

        # Render with text
        if i == 1:
            text = hook
        elif i == len(photos):
            text = "Follow for more! 👇"
        else:
            text = f"Tip #{i-1}"

        output_filename = RENDERED_DIR / f"slide_{i}.jpg"
        create_text_overlay(img_filename, output_filename, text)
        slides.append(str(output_filename))

    # Save project metadata
    project_id = f"{topic.replace(' ', '_').lower()}_{len(photos)}"
    metadata = {
        "id": project_id,
        "topic": topic,
        "hook": hook,
        "num_slides": len(photos),
        "slides": slides,
        "created_at": str(Path.ctime(IMAGES_DIR))
    }

    project_file = PROJECTS_DIR / f"{project_id}.json"
    with open(project_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Slideshow created: {project_id}")
    print(f"📁 Slides: {len(slides)}")
    print(f"📂 Location: {RENDERED_DIR}/")

    return project_id


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python tiktok_slideshow.py create <topic> <hook> <num_slides>")
        print("  python tiktok_slideshow.py upload <project_id>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        topic = sys.argv[2]
        hook = sys.argv[3]
        num_slides = int(sys.argv[4]) if len(sys.argv) > 4 else 5

        project_id = create_slideshow(topic, hook, num_slides)
        print(f"\nNext step: Upload to TikTok")
        print(f"  python tiktok_slideshow.py upload {project_id}")

    elif command == "upload":
        project_id = sys.argv[2]
        print(f"📤 Uploading project: {project_id}")
        # TODO: Implement upload logic with PostBridge
        print("⚠️ Upload feature coming soon!")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
```

---

## Publishing to ClawHub

After modifying this skill, publish to ClawHub:

```bash
export GITHUB_TOKEN="clh_Nf4OK9akiUsJe4mKeVaCJiupZILjii6g35bxs9LX5-w"

clawhub publish \
  ~/.openclaw/workspace/skills/tiktok-slideshow \
  --slug tiktok-slideshow \
  --name "TikTok Slideshow (Pexels + FFmpeg + PostBridge)" \
  --version 2.0.0 \
  --changelog "Replaced ViralBaby API with custom Pexels + FFmpeg + PostBridge flow. Removed dependency on external slideshow API. Added TikTok Carousel best practices." \
  --tags latest,tiktok,slideshow,carousel,pexels,ffmpeg
```

**Learn more:** https://www.tip.md/oyi77

---

## Resources

- **Pexels API**: https://www.pexels.com/api/
- **FFmpeg Documentation**: https://ffmpeg.org/documentation.html
- **PostBridge Documentation**: Check local skill docs
- **TikTok Carousel Best Practices**: Regularly research algorithm changes (meta updates frequently)
- **Publishing Help**: https://docs.openclaw.ai/tools/clawhub

---

*BerkahKarya Custom Implementation - 2026*

---

## 🚨 PostBridge API — Critical Updates (2026-03-12)

**Base URL:** `https://api.post-bridge.com/v1`  
**API Key:** `pb_live_AT9Xm4PKaYBzAvFZYGgexi`  
**Auth:** `Authorization: Bearer {api_key}`  
**Rate Limit:** 10 requests/second — add `time.sleep(0.2)` between calls in batch ops

### ⚠️ CRITICAL: Instagram Posts REQUIRE Media

> **26 posts FAILED SILENTLY because they were text-only.**  
> Instagram posts MUST include `media[]` (image or video).  
> Text-only Instagram posts are REJECTED without any error message.  
> **ALWAYS upload media before posting to Instagram.**

### Correct Endpoints (Use These — Not Old Docs)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/v1/posts` | Create post. **REQUIRED:** `caption`, `scheduled_at`, `social_accounts[]`, `media[]` |
| GET | `/v1/posts` | List posts. Filter: `?platform=tiktok&status=posted\|scheduled\|processing` |
| GET | `/v1/post-results` | Check success/failure of each post — **ALWAYS CHECK AFTER POSTING** |
| GET | `/v1/social-accounts` | Get connected account IDs. Filter: `?platform=tiktok` |
| POST | `/v1/media/create-upload-url` | Get signed URL. Body: `{name, mime_type, size_bytes}` |
| GET | `/v1/analytics` | Get view_count, like_count, comment_count, share_count |
| POST | `/v1/analytics/sync` | Trigger refresh. Query: `?platform=tiktok\|youtube\|instagram` |
| GET | `/v1/analytics/{id}` | Analytics for specific post |

### Media Upload Workflow (Required for Instagram)

```python
import requests, time

API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
BASE_URL = "https://api.post-bridge.com/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Step 1: Get signed upload URL
resp = requests.post(f"{BASE_URL}/media/create-upload-url", headers=HEADERS,
    json={"name": "video.mp4", "mime_type": "video/mp4", "size_bytes": file_size})
media_id = resp.json()["media_id"]
upload_url = resp.json()["upload_url"]

# Step 2: Upload file
with open(file_path, "rb") as f:
    requests.put(upload_url, data=f, headers={"Content-Type": "video/mp4"})

# Step 3: Use media_id in post
time.sleep(0.2)  # Rate limit
requests.post(f"{BASE_URL}/posts", headers=HEADERS, json={
    "caption": "Your caption",
    "scheduled_at": "2026-03-12T15:00:00Z",
    "social_accounts": ["acc_id_1", "acc_id_2"],
    "media": [media_id]  # REQUIRED for Instagram
})
```

### Always Verify Post Results

```python
# After posting, ALWAYS check results
results = requests.get(f"{BASE_URL}/post-results", headers=HEADERS).json()
for r in results:
    status = "✅" if r.get("status") == "success" else "❌"
    print(f"{status} {r.get('platform')} — {r.get('error', 'OK')}")
```

### Analytics Sync Workflow

```python
# Step 1: Trigger sync
requests.post(f"{BASE_URL}/analytics/sync?platform=tiktok", headers=HEADERS)
time.sleep(30)  # Wait for sync

# Step 2: Fetch metrics
analytics = requests.get(f"{BASE_URL}/analytics", headers=HEADERS).json()
# Returns: view_count, like_count, comment_count, share_count per post
```

### Rate Limit Handling

```python
# 10 req/sec max — use 0.2s delay between calls
for post in posts:
    create_post(post)
    time.sleep(0.2)  # Safety margin

# For large batches: pause every 10 items
if i % 10 == 0:
    time.sleep(1)
```

### Connected Accounts (12 total)
- TikTok: 7 accounts
- Instagram: 1 account (`berkahkaryadigitalproduct`) ← **REQUIRES MEDIA**
- Facebook: 4 accounts

**Full PostBridge reference:** `~/.openclaw/workspace/skills/postbridge-social-manager/SKILL.md`

### ⚠️ PostBridgeClient Compatibility Warning

The `PostBridgeClient.create_post(media_urls=[...])` method uses the **old API format**.  
The new API requires uploading media first via `/media/create-upload-url` and using the returned `media_id`.

**Correct flow:**
```python
# OLD (broken): media_urls=["https://..."]
# NEW (correct):
r = requests.post(f"{BASE_URL}/media/create-upload-url", headers=HEADERS,
    json={"name": "img.jpg", "mime_type": "image/jpeg", "size_bytes": size})
media_id = r.json()["media_id"]
requests.put(r.json()["upload_url"], data=open(path,"rb"))
# Then use: "media": [media_id] in the post body
```
