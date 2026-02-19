---
name: content-generator
description: Multi-provider automated video content generation platform. Generates videos from text prompts using AI providers (NVIDIA, BytePlus, XAI, Groq) with FFmpeg processing. Supports single video, batch processing, scheduled posting, and multi-platform output (TikTok, YouTube, Instagram, Facebook). Use when user wants automated video creation, batch content generation, or scheduled social media posting.
---

# Content Generator Skill

End-to-end automated video content generation platform with multi-provider support.

## Quick Start

### Generate Single Video
```python
from generator import ContentGenerator

gen = ContentGenerator("config.yaml")
result = await gen.generate(
    prompt="Create a 30-second smartwatch ad",
    platform="tiktok",
    template="ad_short",
    strategy="balanced"
)
print(result["video"])  # Path to output video
```

### Batch Processing
```python
from batch_processor import BatchProcessor

processor = BatchProcessor(gen)
job = await processor.process_batch(
    prompts=[
        "Product 1 advertisement",
        "Product 2 advertisement", 
        "Product 3 advertisement"
    ],
    platform="tiktok",
    template="ad_short",
    max_concurrent=3
)
```

### CLI Usage
```bash
# Single video
python -m cli generate --prompt "Smartwatch ad" --platform tiktok --strategy balanced

# Batch
python -m cli batch --prompts-file prompts.txt --platform tiktok --max-concurrent 3

# FFmpeg editing
python -m ffmpeg_editor trim input.mp4 --start 5 --duration 30
python -m ffmpeg_editor text input.mp4 --text "Sale!" --position bottom
python -m ffmpeg_editor music input.mp4 --audio bgm.mp3 --volume 0.3
```

## Use This Skill When

- **Single video generation** - Create one video from text prompt
- **Batch content** - Generate multiple videos for content calendar
- **Automated posting** - Schedule videos for future posting
- **Video editing** - Edit videos (trim, text, filters, transitions)
- **Multi-platform** - Output for TikTok, YouTube, Instagram, Facebook
- **Cost optimization** - Use fallback chains and caching

## Do Not Use This Skill When

- **Real-time video** - Need instant video (use pre-made templates)
- **Simple image tasks** - Just need image generation (use individual providers)
- **No API keys** - Need provider credentials (NVIDIA, BytePlus, Groq, etc.)

## Core Features

### 1. Multi-Provider AI Generation

| Provider | Type | Best For |
|----------|------|----------|
| NVIDIA | Images | High-quality Flux/SD images |
| BytePlus | Video | Native video generation (Seedance) |
| XAI | Video | Video editing + generation |
| Groq | LLM | Fast transcript/storyboard |
| Replicate | Images | SD 3.5 images |
| HuggingFace | Images | Cost-effective images |
| Ollama | Both | Local/cheap processing |

### 2. Strategy Selection

| Strategy | Priority | Providers Used |
|----------|----------|----------------|
| `fast` | Speed | Groq → BytePlus → Replicate |
| `quality` | Quality | NVIDIA → XAI → Replicate |
| `cheap` | Cost | Ollama → HuggingFace → BytePlus |
| `balanced` | All | Groq → NVIDIA → Replicate |
| `failsafe` | Reliability | All providers in chain |

### 3. Video Templates

| Template | Duration | Use Case |
|----------|----------|----------|
| `ad_short` | 15-30s | Quick product ads |
| `product_showcase` | 30-60s | Feature demonstrations |
| `storytelling` | 60s+ | Narrative content |
| `tutorial` | 60-120s | Educational content |

### 4. Platform Specs

| Platform | Aspect Ratio | Resolution | Max Duration |
|----------|--------------|------------|---------------|
| TikTok | 9:16 | 1080x1920 | 180s |
| YouTube | 16:9 | 1920x1080 | 12 hours |
| Instagram | 9:16 | 1080x1920 | 60s |
| Facebook | 16:9 | 1920x1080 | 4 hours |

### 5. FFmpeg Editing

**Cutting:**
- Trim: `trim(input, start=5, duration=30)`
- Cut scenes: `cut_scenes(input, timestamps=[(0,10), (20,30)])`

**Speed:**
- Change speed: `change_speed(input, speed=2.0)` (2x faster)
- Slow motion: `slow_motion(input, factor=0.5)`

**Text & Overlays:**
- Text: `add_text(input, overlays=[TextOverlay(...)])`
- Subtitles: `add_subtitles(input, "subs.srt")`
- Watermark: `add_watermark(input, "logo.png", position="top_right")`

**Filters:**
- Color grade: `color_grade(input, preset="cinematic")`
- Filters: `apply_filters(input, brightness=0.1, contrast=1.2)`

**Transitions:**
- Between clips: `add_transition(clip1, clip2, transition="fade")`
- Sequence: `create_transition_sequence(clips, transition="dissolve")`

**Audio:**
- Music: `add_music(input, "bgm.mp3", volume=0.3, fade_in=2)`
- SFX: `add_sound_effect(input, "sfx.mp3", timestamp=5.0)`

**Composition:**
- Resize: `resize(input, width=1080, height=1920)`
- Aspect ratio: `convert_aspect_ratio(input, "9:16")`
- PiP: `picture_in_picture(main, pip, position="bottom_right")`
- Split: `split_screen([clip1, clip2], layout="horizontal")`

### 6. State Management

```python
from state import StateManager

state_mgr = StateManager()

# Save state on failure
state_mgr.save_state(GenerationState(
    state_id="abc123",
    prompt="...",
    current_step=2,  # Failed at step 2
    failed_step=2,
    error_message="API timeout"
))

# Resume from failure
result = state_mgr.resume_generation("abc123")
```

## Configuration

### Environment Variables

```bash
# Required for core functionality
NVIDIA_API_KEY="nvapi-..."
BYTEPLUS_API_KEY="..."
GROQ_API_KEY="gsk_..."

# Optional
REPLICATE_API_TOKEN="r8_..."
HF_API_KEY="hf_..."
XAI_API_KEY="xai-..."
OLLAMA_CLOUD_API_KEY="..."
IMGBB_API_KEY="..."
```

### config.yaml

```yaml
content_generation:
  strategy: "balanced"
  default_platform: "tiktok"
  
providers:
  nvidia:
    api_key: "${NVIDIA_API_KEY}"
    enabled: true
  byteplus:
    api_key: "${BYTEPLUS_API_KEY}"
    enabled: true
  groq:
    api_key: "${GROQ_API_KEY}"
    enabled: true
    
cost_limits:
  max_per_generation: 1.0
  max_per_month: 100.0
  alert_at_percent: 80
```

## Fallback Chain

When a provider fails:
1. Log failure reason
2. Switch to next provider in strategy chain
3. If all fail → raise AllProvidersFailedError

```python
# Example fallback behavior (balanced strategy)
# Image generation: NVIDIA → Replicate → HuggingFace → BytePlus
# Video generation: BytePlus → XAI
# LLM: Groq → NVIDIA → Ollama
```

## Output Structure

```
output/
├── videos/
│   ├── final_video.mp4
│   └── scenes/
│       ├── scene_001.mp4
│       └── scene_002.mp4
├── images/
│   ├── character.png
│   ├── product.png
│   └── background.png
├── metadata.json
├── provider_usage.json
└── cost_report.json
```

## Error Handling

| Error | Handling |
|-------|----------|
| Provider timeout | Fallback to next provider |
| API rate limit | Wait and retry with exponential backoff |
| Invalid API key | Skip provider, log error |
| Cost limit exceeded | Raise CostLimitExceededError |
| All providers fail | Raise AllProvidersFailedError |
| Partial failure | Return best-effort with error log |

## Dependencies

- Python 3.11+
- FFmpeg (for video processing)
- urllib (built-in)
- asyncio (built-in)

## See Also

- `references/workflow.md` - Detailed workflow guide
- `references/nvidia-api.md` - NVIDIA API docs
- `references/byteplus-api.md` - BytePlus Seedance docs
- `references/xai-video-api.md` - XAI video API docs
