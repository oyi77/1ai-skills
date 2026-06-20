---
name: geminigen-ai
description: Unified multimedia API for image generation (nano-banana-pro, imagen-4), video generation (Grok, Veo, Sora),
  and text-to-speech. Replaces grok-video-generation, seedance, and gemini-image-generator.
domain: content
tags:
- api
- content-creation
- digital-content
- geminigen
- media
- video
---

# GeminiGen AI - Multimedia AI Platform
## When to Use

**Trigger phrases:**
- "geminigen ai"
- "Help me with geminigen ai"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


> ✅ **CANONICAL PROVIDER** — This is the single source of truth for all media generation in the 1ai-skills stack.
> Image (nano-banana-pro) · Video (grok-3 / veo / sora) · TTS — all unified under this API.
> Replaces: `grok-video-generation`, `seedance`, `gemini-image-generator`, `content-generator` (media providers).

## API Key & Config

**Config file:** `skills/1ai-skills/config/geminigen_api.json`

```json
{
  "api_key": "<your-geminigen-api-key>",
  "base_url": "https://api.geminigen.ai/uapi/v1"
}
```

**Environment:**
```bash
export GEMINIGEN_API_KEY="$(jq -r .api_key skills/1ai-skills/config/geminigen_api.json)"
```

## Canonical Endpoints

| Service | Method | Endpoint | Notes |
|---------|--------|----------|-------|
| Image | POST | `/uapi/v1/generate_image` | nano-banana-pro (free), imagen-4 |
| Video Grok | POST | `/uapi/v1/video-gen/grok` | grok-aurora, primary video model |
| Video Veo | POST | `/uapi/v1/video-gen/veo` | veo-3.1, veo-2 |
| Video Sora | POST | `/uapi/v1/video-gen/sora` | sora-2, sora-2-pro |
| TTS | POST | `/uapi/v1/text-to-speech` | tts-flash, tts-pro |
| History | GET | `/uapi/v1/history/{uuid}` | Poll generation status |

**Auth:** `x-api-key: $GEMINIGEN_API_KEY` header on all requests
**Content-Type:** multipart/form-data (image/video), application/json (TTS)

## Quick Reference

| Service | Endpoint | Models |
|---------|----------|--------|
| Image | `/generate_image` | nano-banana-pro, nano-banana-2, imagen-4 |
| Video Veo | `/video-gen/veo` | veo-3.1, veo-3.1-fast, veo-2 |
| Video Sora | `/video-gen/sora` | sora-2, sora-2-pro, sora-2-pro-hd |
| Video Grok | `/video-gen/grok` | grok-aurora |
| TTS | `/text-to-speech` | tts-flash, tts-pro |
| History | `/histories/{uuid}` | - |

## Authentication

```bash
export GEMINIGEN_API_KEY="your-api-key"
```

Header: `x-api-key: $GEMINIGEN_API_KEY`

## Image Generation

```bash
curl -X POST https://api.geminigen.ai/uapi/v1/generate_image \
  -H "x-api-key: $GEMINIGEN_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  --form "prompt=Your image description" \
  --form "model=nano-banana-pro" \
  --form "aspect_ratio=9:16" \
  --form "style=Photorealistic" \
  --form "resolution=1K"
```

**Parameters:**
- `prompt` (required): Image description
- `model`: nano-banana-pro (free, 5rq/min), nano-banana-2, imagen-4
- `aspect_ratio`: 1:1, 16:9, 9:16, 4:3, 3:4
- `style`: None, 3D Render, Anime General, Photorealistic, Portrait, etc.
- `resolution`: 1K (default), 2K, 4K
- `output_format`: jpeg (default), png

## Video Generation - Veo (Google)

```bash
curl -X POST https://api.geminigen.ai/uapi/v1/video-gen/veo \
  -H "x-api-key: $GEMINIGEN_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  --form "prompt=Your video description" \
  --form "model=veo-2" \
  --form "resolution=720p" \
  --form "aspect_ratio=9:16"
```

**Models:**
| Model | Duration | Resolution | Aspect Ratios |
|-------|----------|------------|---------------|
| veo-3.1 | 8s | 720p, 1080p | 16:9 only |
| veo-3.1-fast | 8s | 720p, 1080p | 16:9 only |
| veo-2 | 8s | 720p only | 16:9, 9:16 |

## Video Generation - Sora (OpenAI)

```bash
curl -X POST https://api.geminigen.ai/uapi/v1/video-gen/sora \
  -H "x-api-key: $GEMINIGEN_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  --form "prompt=Your video description" \
  --form "model=sora-2" \
  --form "resolution=small" \
  --form "duration=10" \
  --form "aspect_ratio=portrait"
```

**Models:**
| Model | Duration | Resolution | Aspect Ratios |
|-------|----------|------------|---------------|
| sora-2 | 10s, 15s | small (720p) | landscape, portrait |
| sora-2-pro | 25s | small (720p) | landscape, portrait |
| sora-2-pro-hd | 15s | large (1080p) | landscape, portrait |

## Text-to-Speech

```bash
curl -X POST https://api.geminigen.ai/uapi/v1/text-to-speech \
  -H "x-api-key: $GEMINIGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-flash",
    "voices": [{"name": "Gacrux", "voice": {"id": "GM013", "name": "Gacrux"}}],
    "speed": 1,
    "input": "Your text here",
    "output_format": "mp3"
  }'
```

**Parameters:**
- `model`: tts-flash (fast), tts-pro (quality)
- `speed`: 1-4 (default: 1)
- `input`: Text to convert (max 10,000 chars)
- `output_format`: mp3 (default), wav
- `voices`: Array of voice objects (see Voice Library)

## Check Generation Status

```bash
# Get specific generation by UUID
curl -X GET "https://api.geminigen.ai/uapi/v1/history/{uuid}" \
  -H "x-api-key: $GEMINIGEN_API_KEY"

# List all history
curl -X GET "https://api.geminigen.ai/uapi/v1/histories?filter_by=all&page=1&items_per_page=10" \
  -H "x-api-key: $GEMINIGEN_API_KEY"
```

**Status Codes:**
- `1` = Processing
- `2` = Completed (result in `generate_result`)
- `3` = Failed (check `error_message`)

## Python Helper

```python
import requests
import time
import os

API_KEY = os.getenv("GEMINIGEN_API_KEY")
BASE_URL = "https://api.geminigen.ai/uapi/v1"
HEADERS = {"x-api-key": API_KEY}

def generate_image(prompt, model="nano-banana-pro", aspect="9:16", style="Photorealistic"):
    resp = requests.post(
        f"{BASE_URL}/generate_image",
        headers=HEADERS,
        data={"prompt": prompt, "model": model, "aspect_ratio": aspect, "style": style}
    )
    return resp.json()

def generate_video_veo(prompt, model="veo-2", aspect="9:16"):
    resp = requests.post(
        f"{BASE_URL}/video-gen/veo",
        headers=HEADERS,
        data={"prompt": prompt, "model": model, "aspect_ratio": aspect, "resolution": "720p"}
    )
    return resp.json()

def generate_video_sora(prompt, model="sora-2", duration=10, aspect="portrait"):
    resp = requests.post(
        f"{BASE_URL}/video-gen/sora",
        headers=HEADERS,
        data={"prompt": prompt, "model": model, "duration": duration, "aspect_ratio": aspect, "resolution": "small"}
    )
    return resp.json()

def text_to_speech(text, model="tts-flash", voice_id="GM013", voice_name="Gacrux"):
    resp = requests.post(
        f"{BASE_URL}/text-to-speech",
        headers=HEADERS,
        json={
            "model": model,
            "voices": [{"name": voice_name, "voice": {"id": voice_id, "name": voice_name}}],
            "speed": 1,
            "input": text,
            "output_format": "mp3"
        }
    )
    return resp.json()

def wait_for_result(uuid, max_wait=300, poll_interval=5):
    """Poll for generation result with timeout."""
    for _ in range(max_wait // poll_interval):
        resp = requests.get(f"{BASE_URL}/history/{uuid}", headers=HEADERS)
        data = resp.json()
        status = data.get("status", 1)
        if status == 2:  # Completed
            return data.get("generate_result") or \
                   (data.get("generated_image", [{}])[0].get("image_url")) or \
                   (data.get("generated_video", [{}])[0].get("video_url"))
        if status == 3:  # Failed
            raise Exception(data.get("error_message", "Generation failed"))
        print(f"Processing... {data.get('status_percentage', 0)}%")
        time.sleep(poll_interval)
    raise Exception(f"Timeout waiting for result after {max_wait}s")
```

## Use Cases

1. **TikTok/Reels Content**: veo-2 or sora-2 with 9:16 portrait
2. **YouTube Shorts**: veo-2 or sora-2-pro with portrait
3. **Marketing Images**: nano-banana-pro with Photorealistic style
4. **Voiceovers**: tts-pro for high quality narration
5. **Thumbnails**: imagen-4 with 16:9 aspect ratio

## Rate Limits

- `nano-banana-pro`: 5 req/min, 100 req/hour, 1000 req/day (FREE)
- Other models: No rate limit (credit-based)

## Webhooks

For async notifications, configure webhook at:
https://geminigen.ai/profile/integration/webhooks

Webhook payload includes `uuid`, `status`, and `generate_result` when complete.

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- Check readability score (target grade 8 or below for general audiences)
- Verify all images have alt text and proper dimensions per platform
- Confirm links work and point to correct destinations
- Test video/audio quality before publishing
- Validate content renders correctly on mobile devices

## Overview

> Section content — see SKILL.md body for full details.
