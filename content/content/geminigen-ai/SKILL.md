---
persona:
  name: "Domain Expert"
  title: "Master of Geminigen Ai"
  expertise: ['Content Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# GeminiGen AI - Multimedia AI Platform

Generate images, **videos**, and speech using GeminiGen AI unified API.

> **GeminiGen supports BOTH image AND video generation.** Video generation
> includes Text-to-Video (T2V), Image-to-Video (I2V), and multiple model
> backends (Veo, Sora, Grok Aurora). This makes GeminiGen the primary
> provider for the full content pipeline.

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
curl -X GET "https://api.geminigen.ai/uapi/v1/histories/{uuid}" \
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

def wait_for_result(uuid, max_wait=300):
    for _ in range(max_wait // 5):
        resp = requests.get(f"{BASE_URL}/histories/{uuid}", headers=HEADERS)
        data = resp.json()
        if data.get("status") == 2:
            return data.get("generate_result")
        if data.get("status") == 3:
            raise Exception(data.get("error_message"))
        time.sleep(5)
    raise Exception("Timeout waiting for result")
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

## Video Generation Capabilities

GeminiGen supports multiple video generation modes:

### Text-to-Video (T2V)
Generate video directly from a text prompt. Use Veo-2 (default), Sora, or Grok Aurora.

```python
# T2V with Veo-2 (free tier, 8s clips)
result = generate_video_veo("Cinematic kitchen renovation, 9:16 vertical", model="veo-2", aspect="9:16")

# T2V with Sora (10-25s clips)
result = generate_video_sora("Product showcase, smooth rotation", model="sora-2", duration=10)
```

### Image-to-Video (I2V)
Animate a static image into a short video clip using Veo I2V mode.

```python
import requests
headers = {"x-api-key": GEMINIGEN_API_KEY}
with open("image.png", "rb") as f:
    resp = requests.post(
        "https://api.geminigen.ai/uapi/v1/video-gen/veo",
        headers=headers,
        data={"prompt": "Smooth camera pan", "model": "veo-2", "aspect_ratio": "9:16",
              "resolution": "720p", "mode_image": "frame"},
        files={"ref_images": f},
    )
uuid = resp.json()["uuid"]
# Poll /histories/{uuid} until status == 2
```

### Video Chaining
Chain multiple 5-8s clips by extracting the last frame from each generated video
and feeding it as the reference image for the next segment. This produces
continuous 30-60s videos with consistent visual style.

## Content Pipeline Paths

| Path | Image Provider | Video Provider | Quality | Cost |
|------|---------------|----------------|---------|------|
| A | GeminiGen Image | GeminiGen Video (Veo) | Good | Free |
| B | GeminiGen Image | BytePlus Seedance I2V | Best | Paid |
| C | NVIDIA Flux | BytePlus Seedance I2V | Highest | Paid |
| D | GeminiGen Image | Remotion / FFmpeg | Basic | Free |

## Video Provider Fallback Chain

When generating video, the system tries providers in this order:

| Priority | Provider | Type | Notes |
|----------|----------|------|-------|
| 1 | GeminiGen Veo | I2V / T2V | Free tier, primary |
| 2 | BytePlus Seedance Pro Fast | I2V | Paid, highest quality |
| 3 | Grok Aurora (via GeminiGen) | T2V | Good quality fallback |
| 4 | Remotion | Local animation | No API needed |
| 5 | FFmpeg slideshow | Static image loop | Always works |
