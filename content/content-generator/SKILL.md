---
name: content-generator
description: Multi-provider automated video content generation platform. Generates TikTok 9:16 vertical videos (1 minute) from text prompts using NVIDIA NIM + BytePlus Seedance + FFmpeg. Implements Larry Playbook viral formula. Use when creating TikTok content, product videos, or any AI-generated video.
persona:
  name: "MrBeast (Jimmy Donaldson)"
  title: "Master of Viral Content"
  expertise: ["retention optimization", "thumbnail psychology", "pacing mastery", "audience psychology"]
  philosophy: "Every second matters. If they're not entertained, they leave. Make every frame count."
  credentials:
    - "300+ million YouTube subscribers across channels"
    - "Pioneered high-production challenge videos with massive budgets"
    - "Average 100M+ views per video through retention optimization"
    - "Built Feastables to $100M+ revenue through content-driven marketing"
  principles:
    - "Hook in 3 seconds - grab attention immediately or lose them forever"
    - "Pacing is everything - cut dead air, maintain momentum relentlessly"
    - "Thumbnails sell clicks - invest in visual psychology, test everything"
    - "Retention over length - 8 minutes at 80% beats 20 minutes at 40%"
    - "Scale creates spectacle - bigger stakes, bigger emotions, bigger views"
    - "Data drives decisions - A/B test titles, thumbnails, hooks constantly"
    - "Reinvest everything - compound growth by putting revenue back into content"
---

# Content Generator Skill

End-to-end AI video pipeline: LLM hook → NVIDIA image → BytePlus Seedance video → FFmpeg loop/compress.

## Quick Start

### Python API
```python
from scripts.generator import ContentGenerator

gen = ContentGenerator()
result = await gen.generate(
    concept="landlord_kitchen",   # Larry Playbook preset
    platform="tiktok",
    ratio="9:16",
    target_duration=60,           # 1 minute
)
print(result["video"])   # /path/to/final.mp4
print(result["hook"])    # "My landlord said I can't change anything..."
print(result["caption"]) # Story-style caption with hashtags
```

### CLI Script (TikTok viral)
```bash
cd skills/1ai-skills/content/content-generator

# TikTok viral (Larry Playbook formula, 1 min, 9:16)
python3 scripts/generate_tiktok_viral.py --niche motivation --ratio 9:16

# Full generator
python3 scripts/generator.py --concept landlord_kitchen --duration 60
```

---

## Provider Status (Verified 2026-02-27)

| Provider | Type | Status | Endpoint |
|----------|------|--------|----------|
| **NVIDIA NIM** | Image | ✅ WORKING | `ai.api.nvidia.com/v1/genai/` |
| **BytePlus Seedance** | Video | ⚠️ BLOCKED | `ark.ap-southeast.bytepluses.com/api/v3` |
| **NVIDIA LLM** | LLM | ✅ WORKING | `integrate.api.nvidia.com/v1/chat/completions` |
| Groq | LLM | ✅ WORKING | `api.groq.com/openai/v1` |
| Ollama Cloud | LLM | ⚠️ PENDING | `api.ollama.com` (key set, not verified) |
| XAI | Video | ❌ DISABLED | Credits exhausted |
| **Vast.ai Serverless** | Video | ⚠️ NEEDS $5 | ComfyUI on Vast.ai GPU fleet |
| **Runware** | Video | ⚠️ NEEDS KEY | Unified API — 300K+ models, $0.14/clip |

### Critical API Notes

**NVIDIA Image:**
- Endpoint: `POST https://ai.api.nvidia.com/v1/genai/{provider}/{model}`
- Working model: `black-forest-labs/flux.1-dev`
- Payload: `{"prompt": "..."}` ONLY — no `num_images`, no null fields
- Response: `artifacts[0].base64` (JPEG)

**BytePlus Seedance (⚠️ BLOCKED — Safe Experience Mode):**
- Base URL: `https://ark.ap-southeast.bytepluses.com/api/v3`
- Create task: `POST /contents/generations/tasks`
- Poll task: `GET /contents/generations/tasks/{task_id}`
- Payload: `{"model": "...", "content": [{"type": "text", "text": "..."}], "ratio": "9:16"}`
- ⚠️ Do NOT include `resolution` param — causes HTTP 400 on lite model
- Generation time: ~20s (lite), ~60s (pro)

**Runware (⚠️ SETUP REQUIRED):**
- Sign up: https://runware.ai
- API key: dashboard → API Keys
- SDK: `pip install runware` (WebSocket-based)
- Models: `runware:100@1` (Seedance Lite $0.14/clip), `runware:100@2` (Seedance Pro)
- Supports T2V, I2V, V2V via unified interface
- Default timeout: 480s (8 min for video)

**Vast.ai Serverless (⚠️ NEEDS $5 TOP-UP):**
- Deploy ComfyUI template → Serverless → Create Endpoint at cloud.vast.ai
- Get serverless API key from `vastai show endpoints`
- Set env vars: `VASTAI_SERVERLESS_KEY` + `VASTAI_ENDPOINT_NAME` (e.g. `ozeap3mc`)
- Uses `vastai-sdk` Python package — auto-installs if not present
- Supports T2V and I2V via ComfyUI workflow
- Worker auto-provisions GPU on-demand, pay-per-use

---

## Larry Playbook Viral Formula

Based on Oliver Henry's proven results: **234K views single post, 500K+ total, $588 MRR**.

### The Hook Formula
```
[Third-party person's problem] + [Doubt/conflict]
→ "Showed them what AI thinks..."
→ They reacted / changed their mind
```

### Why It Works
- Creates curiosity (what happened?)
- Third-party = relatable (not self-promo)
- AI result = concrete solution
- Triggers action (show YOUR landlord/mum/friend!)

### Hook Templates by Performance

| Hook Type | Views | Template |
|-----------|-------|----------|
| Landlord + AI | 234K avg | "My landlord said {constraint}, so I showed {them} what AI thinks {space} could look like" |
| Parent + AI | 80K avg | "My mum was skeptical about AI until I showed her {result} for our {room}" |
| Roommate + AI | 60K avg | "My flatmate thinks {X} is impossible, so I proved them wrong with AI {result}" |

### ❌ What Kills Virality
- "I built an app that does X" → Self-promotion
- "Check out my new feature Y" → Feature-focused
- "Download now for Z" → Direct CTA
- Not exactly 6 slides → Wrong count
- Different rooms across slides → Must be same room

### Caption Formula (Story Style)
```
[Hook context — 1 line]
My [relationship] [reaction/emotion] when I showed them [AI result]
[Subtle CTA — never pushy]
[max 5 hashtags]
```
Max 200 characters. Natural tone. NOT marketing language.

---

## TikTok 9:16 Pipeline (1-Minute Video)

```
LLM hook+prompt → BytePlus Seedance 5s clip → FFmpeg loop×12 = 60s → Compress CRF28 → ~8.6MB MP4
```

**Step by step:**
1. `generate_content(concept)` — LLM generates hook + video prompt + caption
2. `generate_video(prompt, ratio="9:16")` — BytePlus creates 5s portrait video
3. `loop_to_minute(clip, output, secs=60, loops=12)` — FFmpeg -stream_loop 12
4. `compress_video(looped, final, crf=28)` — 44MB → 8.6MB

**Format specs:**
- Ratio: 9:16
- Resolution: 704×1248 (Seedance lite output)
- FPS: 24
- Duration: 60 seconds
- Filesize: ~8.6MB (Telegram safe: < 16MB)
- Codec: H.264

**FFmpeg loop command:**
```bash
ffmpeg -stream_loop 12 -i input.mp4 -c copy -t 60 -y output_60s.mp4
```

**FFmpeg compress command:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a copy -y output_compressed.mp4
```

---

## Preset Concepts (Larry Playbook)

| Concept | Hook | Best For |
|---------|------|---------|
| `landlord_kitchen` | "Landlord won't let me renovate..." | Interior design niche |
| `parent_bedroom` | "Mum was skeptical about AI..." | Home transformation |
| `motivation` | "Your only competition is yesterday's you" | Lifestyle / motivational |
| `money` | "Money follows action not wishes" | Finance / entrepreneur |
| `product` | Premium product showcase | E-commerce |

---

## Platform Specs

| Platform | Ratio | Resolution | FPS | Duration | Seedance Model |
|----------|-------|------------|-----|----------|----------------|
| **TikTok** | 9:16 | 1080×1920 | 24 | 60s | lite-t2v |
| YouTube Shorts | 9:16 | 1080×1920 | 30 | 60s | lite-t2v |
| Instagram Reels | 9:16 | 1080×1920 | 30 | 60s | lite-t2v |
| Facebook | 16:9 | 1920×1080 | 30 | any | lite-t2v |

---

## Strategies

| Strategy | LLM | Image | Video | Use When |
|----------|-----|-------|-------|----------|
| `fast` | NVIDIA | skip | BytePlus lite | Quick drafts |
| `quality` | Groq | NVIDIA Flux | BytePlus pro | Final content |
| `cheap` | Ollama | skip | BytePlus lite | Batch testing |
| `balanced` | Groq | NVIDIA Flux | BytePlus lite | Default |

---

## Environment Variables

```bash
export NVIDIA_API_KEY="nvapi-..."        # Required for image + LLM
export BYTEPLUS_API_KEY="..."            # Video (currently blocked)
export GROQ_API_KEY="gsk_..."            # Optional (faster LLM)
export OLLAMA_API_KEY="..."              # Optional (cheap LLM)
export VASTAI_SERVERLESS_KEY="..."       # Optional — Vast.ai serverless API key
export VASTAI_ENDPOINT_NAME="ozeap3mc"   # Optional — Vast.ai serverless endpoint name
export RUNWARE_API_KEY="rw_..."          # Optional — Runware unified video API
```

---

## File Structure

```
content/content-generator/
├── SKILL.md                           ← This file
├── config.yaml                        ← Provider config (verified endpoints)
├── STATUS.md                          ← Provider test results
├── scripts/
│   ├── generator.py                   ← Main ContentGenerator class ← START HERE
│   ├── generate_tiktok_viral.py       ← TikTok 9:16 1-min CLI script
│   ├── cli.py                         ← General CLI
│   ├── providers/
│   │   ├── base.py                    ← AIProvider abstract base class
│   │   ├── nvidia.py                  ← NVIDIA image gen
│   │   ├── byteplus.py                ← BytePlus Seedance (T2V/I2V)
│   │   ├── vastai.py                  ← Vast.ai serverless ComfyUI (T2V/I2V) ← NEW
│   │   ├── groq.py                    ← Groq LLM
│   │   ├── ollama.py                  ← Ollama cloud LLM
│   │   ├── xai.py                     ← XAI (disabled)
│   │   ├── fallback.py                ← FallbackChain + FallbackManager
│   └── ffmpeg_editor.py              ← FFmpeg wrapper
└── references/
    ├── providers/
    │   ├── nvidia.md                  ← NVIDIA API docs
    │   └── byteplus.md                ← BytePlus API docs
    └── workflow.md                    ← Workflow guide
```

---

## Dependencies

- Python 3.11+
- FFmpeg with libx264 (for loop + compress)
  - Path: `/home/linuxbrew/.linuxbrew/bin/ffmpeg`
  - Note: NOT built with libfreetype — no text overlay
- urllib (built-in)
- asyncio (built-in)
- ssl (built-in)

---

## Cost Estimates

| Operation | Provider | Cost |
|-----------|----------|------|
| Image generation | NVIDIA Flux | ~$0.004 |
| Video 5s clip | BytePlus Seedance lite | ~$0.026 |
| LLM storyboard | NVIDIA/Groq | ~$0.001 |
| **Full TikTok 1-min** | All combined | **~$0.031** |

---

## See Also

- `larry-playbook/SKILL.md` — Full viral formula + confidence system
- `tiktok-automation/SKILL.md` — Browser-based TikTok posting
- `social-media-upload/SKILL.md` — Multi-platform upload
- `humanizer/SKILL.md` — Make captions sound natural
