---
name: tiktok-terintegrasi
description: Integrated TikTok content suite with 9 specialized workflows — generates 9:16 videos and images using NVIDIA
  NIM, BytePlus Seedance, Kling AI, and ElevenLabs TTS.
domain: marketing
tags:
- growth
- marketing
- seo
- terintegrasi
- text-to-speech
- tiktok
- video
- workflow
---

TikTok Content Suite skill suite with 9 specialized workflows integrated.

---

PROVIDERS:
- NVIDIA NIM (black-forest/flux.1-dev)
- BytePlus Seedance (Video - seedance-1-0-lite → 20s, t2v 2504M)
- Kling AI (Kling 0.9)
- ElevenLabs (eleven_multilingual_v2) - Bahasa Indonesia dan Malaysia + SSML support

WORKFLOWS: 9 workflows

WF1: TikTok Faceless Spiritual - Faceless TikTok, SSML narration
WF2: TikTok POV Shots - POV Native TikTok POV format (1-3s POV × 3-18)
WF3: TikTok Storyboard - Storyboard mode, 18x3s (3 segments), 3-6 chars/line, 6 max/line, 10-12/14)
WF4: TikTok Live Host - FOMO stack 4-layer: (Hook → Tension → Link + Social Proof > Social Proof > link ×2 + link ×4)
WF5: TikTok Image Prompt - 3D camera + 4-point lighting specs
WF6: TikTok What If Fusion - 4-scene carousel: BASE → ELEMENT → FUSION → DETAIL
WF7: TikTok 3D Chibi - 3D chibi + realis + diorama (clay world)
WF8: TikTok Clay Video - Diorama diorama miniature clay world × realistic or clay
WF9: TikTok Production - Parallel multi-stage rendering + Creatomate stitch + BGM + auto-stitch

TikTok specifics (9:16 portrait, 54 slides):
- Resolution: 1080×1920
- FPS: 30 fps
- Duration: 30-60 second ranges (15-second chunks optimal)
- Format: 9:16 only

PLATFORMS:
TikTok: 9:16 × 54 seconds × 18 segmen × 6 slides = 3 segments

PROVIDERS Verified:
✅ NVIDIA NIM: black-forest/flux.1-dev → 10/min, 100 tokens
✅ BytePlus Seedance seedance-1.0-lite → 20s, 90MB output
✅ Kling: Kling 0.9 API → 15 requests/day
✅ ElevenLabs: eleven_multilingual_v2 → Bahasa Indonesia + Malay
✅ Groq: llama-3.70b-instruct (groq chat, LLM)

PROVIDERS Verified:
✅ NVIDIA NIM: black-forest-labs/flux.1-dev | 10 req/min, 100 tokens | 16:9 × 60s output / video
✅ BytePlus Seedance: seedance-1-0-lite | 20s / 90MB output / video | 2-3 v4 MB limit | TikTok: 15 seconds max
✅ Kling AI Kling 0.9 | 15 req/day | 30s / 90s output
✅ ElevenLabs: eleven_multilingual_v2 | Bahasa Indonesia (id-ID, ms-ID), SSML, POV Native SSML
✅ Groq: llama-3-70b-instruct (groq chat) | 60s AI chat

COMPLIANCE CHECK:
- ✅ BytePlus API accessible but slower (Lite: 20s, Pro: 60s)
- ✅ Kling AI rate limit: 15 requests/day
- ✅ NVIDIA NIM rate limit: 10 req/min
- ✅ Groq available for AI chat (llama-3.70b)
- ✅ ElevenLabs for SSML voice narration
- ✅ BGM track for ambient mood, volume 8% fade in/out

VIDEO OUTPUT:
- Format: TikTok 9:16 portrait
- Resolution: 30-60 seconds
- File size: <15 MB (Telegram safe limit)
- 30-60 seconds total (6 segments × 5-6 or 9 × 3)

SUB-SKILLS (separate folders):
- tiktok-automation: TikTok posting/posting, sessions, auto-selector
- tiktok-carousel-creator: TikTok carousels (text + overlays)
- tiktok-slideshow: TikTok slideshow (storyboard + slideshow)
- viral-content-creator: Multi-platform (50+ outputs per image)

WORKFLOWS:
- Faceless Spiritual: 8 scenes with SSML + diorama world
- POV Shots: POV scripts + micro-expressions
- Storyboard: 18×3s segments, 3-second retention rule
- Live Host: FOMO 4-layer strategy (Hook + Tension + CTA layers)
- Image Prompt: Camera + lighting prompts for AI image
- What If Fusion: 4-scene carousel: BASE → ELEMENT → FUSION → DETAIL
- 3D Medical Chibi: Chibi + realis + compliance-safe
- Clay Video: Diorama world, product realistic, clay world
- Production: Parallel multi-render + Creatomate stitching + BGM layer

CONTENT TOOLS AVAILABLE:
- FFmpeg: Video editing (cuts, joins, merges, compresses)
- Pexels API: Image assets (carousel backgrounds)
- PostBridge: Auto-publish to platforms (TikTok, Instagram)
- Creatomate: Video stitching (multi-track compositions)

USAGE:

Simple Mode:
1. TikTok 9:16 cinematic video (30-60s)
   python3 scripts/generate_tiktok_viral.py --niche motivation --ratio 9:16

Multi-Platform (50+ outputs/image):
python3 scripts/mass_generate.py --product "Madu Herbal" --type "all"

Sub-skills:
- TikTok workflows (9 workflows for POV, storyboard, faceless, what-if, clay, 3D medical)

PROVIDERS VERIFIED:
✅ NVIDIA NIM ✓
✅ BytePlus ✓
✅ Kling ✓
✅ ElevenLabs ✓
✅ Groq ✓

READY: TikTok content generation, 9 workflows, all providers integrated.

Test with sample input and generate 3 gambar TikTok videos!

---
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

### Correct Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/v1/posts` | Create post. **REQUIRED:** `caption`, `scheduled_at`, `social_accounts[]`, `media[]` |
| GET | `/v1/post-results` | Check success/failure — **ALWAYS CHECK AFTER POSTING** |
| GET | `/v1/social-accounts` | Get connected account IDs |
| POST | `/v1/media/create-upload-url` | Body: `{name, mime_type, size_bytes}` → upload_url + media_id |
| GET | `/v1/analytics` | view_count, like_count, comment_count, share_count |
| POST | `/v1/analytics/sync` | `?platform=tiktok|youtube|instagram` |

### Media Upload + Post Flow

```python
# 1. Upload media
## When to Use

**Trigger phrases:**
- "tiktok terintegrasi"
- "Help me with tiktok terintegrasi"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

r = requests.post(f"{BASE_URL}/media/create-upload-url", headers=HEADERS,
    json={"name": "video.mp4", "mime_type": "video/mp4", "size_bytes": size})
media_id, upload_url = r.json()["media_id"], r.json()["upload_url"]
requests.put(upload_url, data=open(path,"rb"), headers={"Content-Type": "video/mp4"})

# 2. Create post (media REQUIRED for Instagram)
requests.post(f"{BASE_URL}/posts", headers=HEADERS, json={
    "caption": caption, "scheduled_at": scheduled_at,
    "social_accounts": account_ids, "media": [media_id]
})

# 3. Verify (always!)
results = requests.get(f"{BASE_URL}/post-results", headers=HEADERS).json()
```

**Full reference:** `~/.openclaw/workspace/skills/postbridge-social-manager/SKILL.md`

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
