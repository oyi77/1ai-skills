---
name: video-generation
description: AI video generation — Sora, Runway, Kling, Pika, Luma. Text-to-video, image-to-video, video editing with AI
---

## Overview

Generate and edit videos using AI. Covers text-to-video, image-to-video, and AI-powered video editing workflows.

## Capabilities

- Generate videos from text prompts (Sora, Runway Gen-3, Kling, Pika)
- Animate still images into video (image-to-video)
- Edit existing videos with AI (style transfer, object removal, background swap)
- Upscale and enhance video quality
- Create batch video variations for content testing
- Integrate video generation into content pipelines

## When to Use

- Creating social media video content at scale
- Generating product demos or explainer videos
- Turning blog posts or scripts into visual content
- Creating short-form video for TikTok, Reels, YouTube Shorts
- Prototyping video concepts before full production

## Pseudo Code

### Runway Gen-3 API
```python
import requests

# Generate video from text
response = requests.post(
    "https://api.runwayml.com/v1/generation",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "gen3a_turbo",
        "promptText": "A golden retriever running through autumn leaves, slow motion, cinematic",
        "duration": 5,
        "ratio": "16:9"
    }
)
```

### Kling API
```python
import requests

response = requests.post(
    "https://api.klingai.com/v1/videos/generations",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "prompt": "Sunrise over a misty mountain lake, aerial drone shot",
        "model": "kling-v1",
        "duration": "5",
        "aspect_ratio": "16:9"
    }
)
```

### Image-to-Video (Animate Still Images)
```python
# Runway image-to-video
response = requests.post(
    "https://api.runwayml.com/v1/generation",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "gen3a_turbo",
        "promptText": "Camera slowly pans right, subject comes to life",
        "initImage": "https://example.com/image.png",
        "duration": 5
    }
)
```

### Batch Video Generation
```python
prompts = [
    "A coffee cup steaming on a rainy window sill",
    "Time-lapse of a flower blooming",
    "Ocean waves crashing on rocks at sunset"
]

for i, prompt in enumerate(prompts):
    response = generate_video(
        model="gen3a_turbo",
        prompt=prompt,
        duration=5,
        ratio="9:16"  # Vertical for social
    )
    save_video(response.url, f"clip_{i}.mp4")
```

### AI Video Editing (FFmpeg + AI)
```bash
# Style transfer on video
python style_transfer.py --input video.mp4 --style "van gogh" --output styled.mp4

# Remove background
python rembg_video.py --input video.mp4 --output nobg.mp4

# Upscale 2x
ffmpeg -i input.mp4 -vf "scale=3840:2160" -c:v libx264 output_4k.mp4
```

## Common Patterns

### Prompt Structure for Video
```
[Camera movement] + [Subject] + [Action] + [Environment] + [Style/Mood]

Example: "Slow dolly forward, a woman reading in a cozy library,
warm golden lighting, cinematic 4k, shallow depth of field"
```

### Camera Movements (Keywords)
```
- "drone shot" / "aerial view" — overhead perspective
- "dolly forward" / "push in" — camera moves toward subject
- "pan left/right" — horizontal camera rotation
- "tracking shot" — follows moving subject
- "static shot" / "locked off" — no camera movement
- "zoom in/out" — lens zoom effect
```

### Platform Selection
```
Sora (OpenAI): Best quality, longest videos (up to 60s), limited access
Runway Gen-3: Fast, good quality, API-first, 5-10s clips
Kling: Great motion, 1080p, good for action scenes
Pika: Simple, good for stylized/animated content
Luma Dream Machine: Fast, decent quality, good for prototyping
```

### Content Pipeline
```
1. Write script / prompts (multi-platform-distribution skill)
2. Generate video clips (5-10s each)
3. Edit together with transitions (video-editor skill)
4. Add voiceover (voice-ai skill)
5. Export for each platform (9:16, 16:9, 1:1)
```
