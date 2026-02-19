# Content Generator

A multi-provider automated video content generation platform that creates videos from text prompts using AI providers with FFmpeg processing. Supports single video generation, batch processing, scheduled posting, and multi-platform output.

## Overview

Content Generator is a Python-based tool that generates video content from text prompts using various AI providers. It handles the complete pipeline from prompt to published content, including storyboard generation, image creation, video assembly, and platform-specific formatting.

### Key Features

- **Multi-Provider Support**: NVIDIA, BytePlus, XAI, Groq, Replicate, HuggingFace, Ollama
- **Batch Processing**: Generate multiple videos concurrently
- **Scheduled Posting**: Queue content for future publication
- **Multi-Platform**: Output for TikTok, YouTube, Instagram, Facebook
- **FFmpeg Integration**: Full video editing capabilities
- **Cost Tracking**: Monitor and control generation costs
- **Caching**: Avoid redundant generations
- **Fallback Chains**: Automatic provider failover

## Installation

### Prerequisites

- Python 3.11 or higher
- FFmpeg (for video processing)

### Install Dependencies

```bash
cd content/content-generator
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file or set these environment variables for the providers you want to use:

```bash
# Core providers
export NVIDIA_API_KEY="nvapi-..."
export BYTEPLUS_API_KEY="your_byteplus_key"
export GROQ_API_KEY="gsk_..."

# Optional providers
export REPLICATE_API_TOKEN="r8_..."
export HF_API_KEY="hf_..."
export XAI_API_KEY="xai-..."
export IMGBB_API_KEY="your_imgbb_key"

# Local LLM (if using Ollama)
# Ensure Ollama is running locally on port 11434
```

## Configuration

Copy the provided `config.yaml` and customize as needed:

```bash
cp config.yaml config.yaml.custom
```

Key configuration sections:

- **content_generation**: Strategy selection, default platform, concurrent limits
- **providers**: API keys and model preferences for each provider
- **cost_limits**: Budget controls and alert thresholds
- **platforms**: Platform-specific video specifications
- **cache**: Caching behavior and storage settings

### Strategy Options

| Strategy | Priority | Best For |
|----------|----------|----------|
| `fast` | Speed | Quick iterations |
| `quality` | Quality | Final outputs |
| `cheap` | Cost | Budget-conscious |
| `balanced` | All | General use |
| `failsafe` | Reliability | Production systems |

## CLI Usage

### Generate Single Content

Generate content from a single prompt:

```bash
python -m scripts.cli generate \
    --prompt "Create a 30-second smartwatch advertisement" \
    --platform tiktok \
    --template ad_short \
    --strategy balanced \
    --provider ollama \
    --output result.json
```

Options:
- `--prompt, -p`: Content prompt (required)
- `--platform`: Target platform (tiktok, youtube, instagram, facebook)
- `--template`: Template to use (ad_short, product_showcase, storytelling, tutorial)
- `--strategy`: Generation strategy (fast, quality, cheap, balanced, failsafe)
- `--provider`: LLM provider to use (ollama, groq, nvidia)
- `--output, -o`: Output file path

### Batch Generation

Process multiple prompts concurrently:

```bash
python -m scripts.cli batch \
    --prompts "Product 1 ad" "Product 2 ad" "Product 3 ad" \
    --platform tiktok \
    --template ad_short \
    --max-concurrent 3 \
    --output batch_results.json
```

Options:
- `--prompts, -p`: List of prompts to process (space-separated)
- `--platform`: Target platform
- `--template`: Template to apply
- `--strategy`: Generation strategy
- `--provider`: LLM provider
- `--max-concurrent, -c`: Maximum concurrent jobs (default: 3)
- `--output, -o`: Output file path

### Schedule Content

Schedule content for future posting:

```bash
python -m scripts.cli schedule \
    --prompt "New product launch announcement" \
    --platform youtube \
    --time "+2h" \
    --output schedule.json
```

Time format options:
- ISO format: `2026-02-20T15:00:00`
- Relative: `+30m` (30 minutes from now)
- Relative: `+2h` (2 hours from now)
- Relative: `+1d` (1 day from now)

### Post Content

Generate and post directly to a platform:

```bash
python -m scripts.cli post \
    --prompt "Quick update video" \
    --platform instagram \
    --template ad_short \
    --output post_result.json
```

## Providers

### Supported AI Providers

| Provider | Type | Models | Best For |
|----------|------|--------|----------|
| **NVIDIA** | Image | Flux, SDXL | High-quality images |
| **BytePlus** | Video | Seedance | Native video generation |
| **XAI** | Video | grok-2-vision | Video editing |
| **Groq** | LLM | llama-3.3-70b-versatile | Fast text generation |
| **Replicate** | Image | SD 3.5 | Alternative image generation |
| **HuggingFace** | Image | Stable Diffusion 3.5 | Cost-effective images |
| **Ollama** | Both | llama3.2, mistral | Local processing |

### Provider Fallback Order

When a provider fails, the system automatically tries the next in chain:

- **Image**: NVIDIA → Replicate → HuggingFace
- **Video**: BytePlus → XAI
- **LLM**: Groq → Ollama

## Platforms

### Supported Platforms

| Platform | Aspect Ratio | Resolution | Max Duration |
|----------|--------------|------------|--------------|
| **TikTok** | 9:16 | 1080x1920 | 180 seconds |
| **YouTube** | 16:9 | 1920x1080 | 12 hours |
| **Instagram** | 9:16 | 1080x1920 | 60 seconds |
| **Facebook** | 16:9 | 1920x1080 | 4 hours |

## Examples

### Single Video Generation

```python
import asyncio
from scripts.cli import generate_content

async def main():
    result = await generate_content(
        prompt="A dramatic product reveal for a new fitness tracker",
        platform="tiktok",
        template="ad_short",
        strategy="balanced",
        provider_name="groq"
    )
    print(result)

asyncio.run(main())
```

### Batch Processing

```python
import asyncio
from scripts.cli import batch_generate

async def main():
    results = await batch_generate(
        prompts=[
            "Product launch video for headphones",
            "Product launch video for camera",
            "Product launch video for laptop"
        ],
        platform="youtube",
        template="product_showcase",
        max_concurrent=3
    )
    print(f"Generated {len(results)} videos")

asyncio.run(main())
```

### Scheduling

```python
from datetime import datetime, timedelta
from scripts.cli import schedule_content

# Schedule for 3 days from now
scheduled_time = datetime.now() + timedelta(days=3)

schedule = schedule_content(
    prompt="Weekly product highlights",
    platform="instagram",
    scheduled_time=scheduled_time
)

print(f"Scheduled for: {schedule.scheduled_time}")
```

## Video Editing

The FFmpeg editor provides powerful video manipulation:

```python
from scripts.ffmpeg_editor import FFmpegEditor

editor = FFmpegEditor()

# Trim video
editor.trim("input.mp4", start=5, duration=30, output="trimmed.mp4")

# Add text overlay
editor.add_text(
    "input.mp4",
    text="Limited Time Offer",
    position="bottom",
    output="with_text.mp4"
)

# Add background music
editor.add_music(
    "input.mp4",
    audio="bgm.mp3",
    volume=0.3,
    fade_in=2,
    output="with_music.mp4"
)

# Resize for platform
editor.resize("input.mp4", width=1080, height=1920, output="vertical.mp4")
```

### Available Editing Operations

- **Cutting**: trim, cut_scenes
- **Speed**: change_speed, slow_motion
- **Text**: add_text, add_subtitles, add_watermark
- **Filters**: color_grade, apply_filters
- **Transitions**: add_transition, create_transition_sequence
- **Audio**: add_music, add_sound_effect
- **Composition**: resize, convert_aspect_ratio, picture_in_picture, split_screen

## Cost Management

The system tracks generation costs and can enforce limits:

```yaml
cost_limits:
  max_per_generation: 1.00    # Maximum cost per single generation
  max_per_month: 100.00       # Monthly budget
  alert_at_percent: 80        # Alert when 80% of budget used
  enabled: true
```

Costs are tracked in a SQLite database for monitoring and reporting.

## State Management

Save and resume failed generations:

```python
from scripts.state import StateManager, GenerationState

state_mgr = StateManager()

# Save state on failure
state_mgr.save_state(GenerationState(
    state_id="gen_123",
    prompt="...",
    current_step=2,
    failed_step=2,
    error_message="API timeout"
))

# Resume from failure
result = state_mgr.resume_generation("gen_123")
```

## Programmatic Usage

### Import and Initialize

```python
from scripts.providers.ollama import OllamaProvider
from scripts.providers.groq import GroqProvider
from scripts.platforms.base import Platform

# Initialize provider
provider = GroqProvider(api_key="your_api_key")

# Generate content
result = await provider.generate("Your prompt here")
```

### Custom Provider

```python
from scripts.providers.base import AIProvider, GenerationResult

class MyProvider(AIProvider):
    async def generate(self, prompt: str) -> GenerationResult:
        # Your implementation
        return GenerationResult(
            success=True,
            data={"output": "..."},
            cost=0.01,
            provider="my_provider",
            model="my_model"
        )
```

## Troubleshooting

### Common Issues

**Provider authentication fails**
- Verify your API key is correct
- Check the provider status page
- Ensure environment variables are set

**FFmpeg not found**
- Install FFmpeg: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux)
- Or specify path in config.yaml: `ffmpeg_path: /usr/local/bin/ffmpeg`

**Rate limiting**
- The system automatically handles rate limits with exponential backoff
- Consider reducing `max_concurrent` for batch jobs

**Cost exceeds limit**
- Check current usage with cost tracker
- Adjust limits in config.yaml or set higher limits

## File Structure

```
content-generator/
├── scripts/
│   ├── cli.py              # Command-line interface
│   ├── batch_processor.py # Batch processing
│   ├── scheduler.py        # Scheduling
│   ├── ffmpeg_editor.py    # Video editing
│   ├── providers/          # AI providers
│   │   ├── nvidia.py
│   │   ├── byteplus.py
│   │   ├── groq.py
│   │   └── ...
│   └── platforms/          # Platform adapters
│       ├── tiktok.py
│       ├── youtube.py
│       └── ...
├── config.yaml             # Configuration template
├── SKILL.md               # Skill definition
└── README.md              # This file
```

## License

See project repository for license information.
