---
name: tiktok-carousel-creator
description: ">\n  Creates TikTok image carousels with text overlays using Pexels API & FFmpeg, then uploads via PostBridge\
  \ API.\n  Use when the user wants to: create TikTok slideshows or carousels, search images for social media content,\n \
  \ post or upload slideshow content to TikTok, edit slide text, or manage image collections for content creation."
domain: marketing
tags:
- api
- carousel
- creator
- growth
- marketing
- seo
- social-media
- tiktok
metadata: "{\n    \"openclaw\": {\n      \"emoji\": \"\U0001F4F1\",\n      \"requires\": { \"bins\": [\"ffmpeg\", \"curl\"\
  ], \"env\": [\"PEXELS_API_KEY\"] }\n    }\n  }\n"
---


# TikTok Carousel Creator (Pexels + FFmpeg + PostBridge)
## When to Use

**Trigger phrases:**
- "tiktok carousel creator"
- "Help me with tiktok carousel creator"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


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

- Python 3.10+ or Node.js 18+
- API credentials configured in `.env`
- Network access to target services
- Understanding of account, analytics, carousel, carousels, collections concepts


### 1. Pexels API Key

Get FREE API key at: https://www.pexels.com/api/

Set environment variable:
```bash
export PEXELS_API_KEY="your_pexels_api_key_here"
```

**Important**: You need this key to search images. Without it, the script will fail.

### 2. PostBridge API Key

Already configured in PostBridge Client:

```bash
export POST_BRIDGE_API_KEY="REDACTED_ROTATED_CREDENTIAL"
export POST_BRIDGE_BASE_URL="https://api.post-bridge.com/v1"
```

### 3. Python PIL (Pillow)

Check if installed:
```bash
python3 -c "from PIL import Image; print('PIL available')"
```

**Install:**
```bash
pip3 install Pillow
```

### 4. FFmpeg (for optional resizing)

Check if installed:
```bash
ffmpeg -version
```

**Install (optional - PIL handles most tasks):**
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### 4. ImgBB API Key (OPTIONAL - for auto-hosting)

Get FREE API key at: https://api.imgbb.com/

Set environment variable (optional - for auto-upload to ImgBB):
```bash
export IMGBB_API_KEY="your_imgbb_api_key_here"
```

**Why ImgBB?**
- Free tier: 32MB per image upload
- No strict rate limit for free tier
- Simple REST API
- Permanent image hosting
- Public URLs for social media platforms

### 5. Directory Structure

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

## Usage

- Configure account, analytics, carousel, carousels, collections settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Create Slideshow

```bash
python3 tiktok_slideshow.py create "morning routine" "Your routine is broken" 5
```

**Parameters:**
- `topic`: Search theme for Pexels images
- `hook`: Hook text for first slide (attention-grabbing)
- `num_slides`: Number of slides (5-10 recommended)

**Example:**
```bash
python3 tiktok_slideshow.py create "productivity tips" "You're doing productivity wrong" 7
```

### List Projects

```bash
python3 tiktok_slideshow.py list
```

Shows all existing projects with metadata.

### Host Images Only (ImgBB)

Upload all carousel images to ImgBB hosting:

```bash
# Requires IMGBB_API_KEY
export IMGBB_API_KEY="your_imgbb_api_key"

python3 tiktok_slideshow.py host <project_id>
```

Outputs public URLs for all slides:
```
🖼️  Uploading 5 slides to ImgBB hosting...
✅ Uploaded to ImgBB: slide_1.jpg
✅ Uploaded to ImgBB: slide_2.jpg
✅ Uploaded to ImgBB: slide_3.jpg
✅ Uploaded to ImgBB: slide_4.jpg
✅ Uploaded to ImgBB: slide_5.jpg

✅ Uploaded 5 slides to ImgBB!

Media URLs:
  1. https://i.ibb.co/xxx/slide-1.jpg
  2. https://i.ibb.co/yyy/slide-2.jpg
  3. https://i.ibb.co/zzz/slide-3.jpg
  4. https://i.ibb.co/aaa/slide-4.jpg
  5. https://i.ibb.co/bbb/slide-5.jpg

📝 URLs saved to: /home/openclaw/.tiktok-slideshow/projects/project_id_urls.txt
```

### Upload to TikTok

**Option 1: Auto-host + upload (recommended)**
```bashpython3 tiktok_slideshow.py upload <project_id>
```
Automatically uploads images to ImgBB, then posts to TikTok via PostBridge.

**Option 2: Manual hosting + upload**
```bash
# Step 1: Host images manually (use ImgBB, S3, Cloudinary, etc.)
python3 tiktok_slideshow.py host <project_id>

# Step 2: Upload to TikTok (skip hosting)
python3 tiktok_slideshow.py upload <project_id> --no-host
```

**Note**: ImgBB hosting is FREE and recommended for social media uploads.

---

## Complete Example

```bash
# 1. Set your Pexels API key
export PEXELS_API_KEY="YOUR_PEXELS_API_KEY"

# 2. Create a slideshow
python3 tiktok_slideshow.py create "fitness motivation" "Stop making this mistake" 5

# Output:
# ==================================================
# 📱 Creating TikTok Slideshow
# ==================================================
# 🎯 Topic: fitness motivation
# 🪝 Hook: Stop making this mistake
# 📊 Slides: 5
# ==================================================
#
# 🔍 Searching images on Pexels...
# 📸 Found 5 images for: fitness motivation
# ✅ Downloaded: temp_0.jpg
# ✅ Rendered: slide_1.jpg
# ✅ Downloaded: temp_1.jpg
# ✅ Rendered: slide_2.jpg
# ...
#
# ==================================================
# ✅ Slideshow Created Successfully!
# ==================================================
# 📦 Project ID: fitness_motivation_20260306_044512
# 📁 Slides: 5
# 📂 Location: /home/openclaw/.tiktok-slideshow/rendered/
# 💾 Metadata: /home/openclaw/.tiktok-slideshow/projects/fitness_motivation_20260306_044512.json
# ==================================================

# 3. Review slides
ls /home/openclaw/.tiktok-slideshow/rendered/

# 4. Upload to TikTok (requires image hosting setup)
python3 tiktok_slideshow.py upload fitness_motivation_20260306_044512
```

---

## How It Works

- Configure account, analytics, carousel, carousels, collections settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Step 1: Search Images with Pexels API

```bash
POST https://api.pexels.com/v1/search
Authorization: {PEXELS_API_KEY}

Query Parameters:
- query: "fitness motivation"
- orientation: "vertical"  # For TikTok 9:16
- size: "large"
- per_page: 5

Response:
{
  "photos": [
    {
      "id": 123456,
      "src": {
        "large": "https://images.pexels.com/photos/123456/large.jpg"
      },
      "photographer": "Joe Smith"
    }
  ]
}
```

### Step 2: Download & Resize with FFmpeg

Resize to TikTok format and add professional text overlay:

```bash
ffmpeg -i input.jpg \
  -vf "scale=1080:1920,drawtext=text='Your Text Here':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:borderw=4:bordercolor=black:box=1:boxcolor=black@0.5:boxborderw=10" \
  -q:v 2 \
  output.jpg
```

**FFmpeg parameters explained:**
- `scale=1080:1920`: Resize to TikTok format
- `fontsize=48`: Title font size
- `fontcolor=white`: Text color
- `borderw=4:bordercolor=black`: Text outline
- `box=1:boxcolor=black@0.5`: Semi-transparent background
- `boxborderw=10`: Box padding
- `-q:v 2`: JPEG quality (2-5 recommended)

### Step 3: Upload via PostBridge

```python
from skills_1ai_skills.marketing.post_bridge_client import PostBridgeClient

client = PostBridgeClient(api_key=POST_BRIDGE_API_KEY)
tiktok_accounts = client.get_accounts_by_platform("tiktok")

client.create_post(
    caption="Here's my carousel...",
    account_ids=[tiktok_accounts[0]['id']],
    media_urls=[...your hosted image URLs...]
)
```

---

## Publishing to ClawHub

After publishing this skill:

```bash
GITHUB_TOKEN="REDACTED_ROTATED_CREDENTIAL"

clawhub publish \
  ~/.openclaw/workspace/skills/tiktok-carousel-creator \
  --slug tiktok-carousel-creator \
  --name "TikTok Carousel Creator (Pexels + FFmpeg + PostBridge)" \
  --version 1.0.0 \
  --changelog "Initial release. Custom TikTok carousel creator using Pexels API + FFmpeg + PostBridge. Designed for BerkahKarya workflow." \
  --tags latest,tiktok,carousel,slideshow,pexels,ffmpeg,postbridge
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

## Troubleshooting

- Configure account, analytics, carousel, carousels, collections settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Pexels API Key Not Set

```
Error: PEXELS_API_KEY not set
```

**Solution:**
```bash
export PEXELS_API_KEY="your_key_here"
```

Get free key at: https://www.pexels.com/api/

### FFmpeg Not Found

```
Error: ffmpeg not found
```

**Solution:**
```bash
sudo apt update && sudo apt install ffmpeg
```

### No Images Found

```
Error: No images found for topic: xyz
```

**Solution:**
- Try different search terms
- Check Pexels API key is valid
- Use more generic terms

---

*BerkahKarya Custom Implementation - 2026*
*Learn more: https://www.tip.md/oyi77*

---

## 🚨 PostBridge API — Critical Updates (2026-03-12)

**Base URL:** `https://api.post-bridge.com/v1`  
**API Key:** `REDACTED_ROTATED_CREDENTIAL`  
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

API_KEY = "REDACTED_ROTATED_CREDENTIAL"
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
The new API uses `media[]` with pre-uploaded media IDs, not direct URLs.

**Correct flow:**
```python
# OLD (broken): media_urls=[url]
# NEW (correct): upload first, then use media_id
r = requests.post(f"{BASE_URL}/media/create-upload-url", headers=HEADERS,
    json={"name": "img.jpg", "mime_type": "image/jpeg", "size_bytes": size})
media_id = r.json()["media_id"]
requests.put(r.json()["upload_url"], data=open(path,"rb"), headers={"Content-Type": "image/jpeg"})
# Then use: "media": [media_id] in post creation
```

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

## Verification

- Run A/B test with control group before full rollout
- Verify tracking pixels fire correctly on all conversion pages
- Check UTM parameters parse correctly in analytics dashboard
- Confirm email deliverability via seed list test
- Validate landing page speed (target < 3s load time)

## Overview

> Section content — see SKILL.md body for full details.
