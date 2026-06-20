---
name: postai-automation
description: Automate TikTok and Instagram video creation from product images using POST AI — generates dozens of captioned,
  voiced-over variants for affiliate and e-commerce marketing.
domain: automation
tags:
- automation
- postai
- productivity
- video
- voice
- workflow
---
# POST AI Automation

Automate TikTok/Instagram video creation and posting using POST AI platform.

## What is POST AI?

POST AI is an AI-powered tool that turns 1 product image into dozens of TikTok FYP videos with auto-caption and voice-over.

## Use Cases

- **Affiliate Marketing**: Generate 10-20 videos per product automatically
- **E-commerce**: Create product showcases at scale
- **Content Automation**: Daily posting without manual effort
- **A/B Testing**: Test multiple video variants to see what works

## Setup

1. Purchase POST AI: https://postai.myscalev.com/
2. Extract credentials from email/confirmation
3. Copy `config.example.json` to `config.json`
4. Fill in your credentials:

```json
{
  "postai": {
    "api_key": "your_api_key",
    "account_id": "your_account_id",
    "endpoint": "https://api.postai.com/v1"
  },
  "tiktok": {
    "account": "@youraccount",
    "cookie_file": "/path/to/cookies.json",
    "session_id": "your_session_id"
  },
  "instagram": {
    "account": "@youraccount",
    "cookie_file": "/path/to/cookies.json"
  }
}
```

## Commands

Available commands and their usage.


### Generate Videos

Generate multiple video variants from a single product image:

```bash
python scripts/generate_videos.py \
  --image products/shirt.jpg \
  --count 10 \
  --platform tiktok \
  --style hype \
  --language id \
  --output videos/shirt/
```

**Options:**
- `--image`: Path to product image
- `--count`: Number of videos to generate (default: 5)
- `--platform`: Target platform (tiktok, instagram, threads)
- `--style`: Video style (hype, calm, energetic, professional)
- `--language`: Language for voice-over (id, en)
- `--output`: Output directory

### Auto Upload

Upload generated videos with automatic scheduling:

```bash
python scripts/auto_upload.py \
  --source videos/shirt/*.mp4 \
  --platform tiktok \
  --caption-file captions/shirt.txt \
  --schedule "2026-03-05 08:00,14:00,20:00"
```

**Options:**
- `--source`: Glob pattern for video files
- `--platform`: Target platform
- `--caption-file`: Text file with captions (one per line)
- `--schedule`: Comma-separated schedule (YYYY-MM-DD HH:MM)
- `--hashtags`: Custom hashtags (comma-separated)

### Batch Process

Process multiple products from CSV:

```bash
python scripts/batch_process.py \
  --input products.csv \
  --platforms tiktok,instagram \
  --videos-per-product 10 \
  --schedule "08:00,14:00,20:00"
```

**CSV Format (products.csv):**
```csv
product_name,image_url,price,affiliate_link,caption_template
T-Shirt Merah,https://example.com/shirt.jpg,150000,https://aff.link/shirt,Promo {price}!
Kemeja Hijau,https://example.com/shirt2.jpg,200000,https://aff.link/shirt2,Fashion terbaru!
```

## Workflow Examples

End-to-end workflow examples showing how to combine commands.


### Quick Start (Single Product)

```bash
# 1. Generate videos
python scripts/generate_videos.py --image produk.jpg --count 10 --platform tiktok

# 2. Preview before upload
python scripts/previews.py --source videos/produk/

# 3. Upload manually or scheduled
python scripts/auto_upload.py --source videos/produk/*.mp4 --platform tiktok
```

### Daily Automation (Cron)

Add to crontab for daily 3x posting:

```bash
# Post at 8 AM, 2 PM, 8 PM every day
0 8,14,20 * * * cd ~/.openclaw/workspace/skills/postai-automation && python scripts/daily_post.py
```

### A/B Testing

Generate multiple styles for the same product:

```bash
python scripts/generate_videos.py \
  --image produk.jpg \
  --styles hype,calm,professional \
  --count 5 \
  --platform tiktok
```

Then upload all variants and track performance to find best-performing style.

## Performance Tracking

Track which videos generate the most engagement/sales:

```bash
python scripts/track_performance.py \
  --days 7 \
  --metrics views,likes,comments,sales
```

Output:
```
Video            Views   Likes  Comments  Sales  Conversion Rate
produk_v1.mp4    15.2K   2.3K   156       23     0.15%
produk_v2.mp4    8.5K    1.2K   89        12     0.14%
produk_v3.mp4    22.1K   4.5K   234       67     0.30% ⭐ Best
```

## Caption Templates

Use placeholders in caption templates:

- `{product_name}`: Product name
- `{price}`: Price (formatted: Rp 150.000)
- `{affiliate_link}`: Your affiliate link
- `{hashtag}`: Auto-generated hashtags
- `{emoji}`: Relevant emojis based on product

Example template:
```
🔥 {product_name} - {price}

Jangan sampai kehabisan! Order sekarang:
{affiliate_link}

{hashtag}

#fyp #affiliatemarketing #promotion
```

## Troubleshooting

**Videos not uploading to TikTok:**
- Check if cookies are expired: Re-export cookies from browser
- Verify session_id is correct
- Check TikTok account status (not banned/limited)

**POST AI API errors:**
- Verify API key is valid
- Check your subscription status
- Ensure account has remaining credits

**Caption generation issues:**
- Check language settings
- Ensure caption template is valid
- Verify hashtags are not blacklisted

## Best Practices

1. **A/B Test Everything**: Generate multiple variants to find what works
2. **Schedule Strategically**: Test different posting times (8, 14, 20 are good starts)
3. **Mix Styles**: Don't use same style every time - variety keeps audience engaged
4. **Track Performance**: Use tracking script to identify winning patterns
5. **Quality Over Quantity**: 5 great videos > 20 mediocre videos

## Limitations

- POST AI relies on external API service - check their status if issues occur
- TikTok has rate limits - don't spam upload
- Instagram has stricter anti-bot measures than TikTok
- Voice-over quality depends on POST AI's TTS engine

## Integration with Other Skills

- **content-generator**: Generate script ideas for videos
- **social-media-upload**: Cross-platform posting
- **analytics-dashboard**: Track performance across campaigns
- **humanizer**: Make AI-generated captions more natural

## Support

For POST AI platform issues: Contact their support via https://postai.myscalev.com/

For skill issues: Open issue at BerkahKarya or contact Veris directly.

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

## When to Use

- Automating social media posting across platforms
- Scheduling content for multiple accounts
- Cross-posting from one platform to another
- Managing social media automation workflows
- Building social media content pipelines

## When NOT to Use

- Task is about social media posting, not automation
- You need to build a custom social media tool (use development)
- Task requires real-time engagement (use social media tools)
- You don't have PostAI account
- Task is about content creation (use content tools)
- You need analytics (use analytics tools)

## Red Flags

- Posting too frequently (risk of account suspension)
- Not customizing content per platform
- Ignoring platform-specific content guidelines
- Not testing posts before scheduling
- Missing error handling for failed posts

## Verification

- [ ] Posts are scheduled correctly
- [ ] Content is customized per platform
- [ ] Rate limits are respected
- [ ] Error handling is in place
- [ ] Posts can be cancelled if needed

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
