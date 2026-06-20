---
name: video-gen
description: AI video generation — Sora, Runway, Pika, Kling. Text-to-video, image-to-video, video editing with AI
domain: content
tags:
- content-creation
- digital-content
- gen
- media
- video
---



## Overview

AI video generation creates video content from text prompts or images using diffusion-based models. This skill covers text-to-video, image-to-video, video extension, and integration with production video pipelines.

## Capabilities

- Generate videos from text prompts (Sora, Runway Gen-3, Pika, Kling)
- Animate still images into video (image-to-video)
- Extend existing videos with AI-generated continuation
- Control motion, camera movement, and scene transitions
- Integrate video generation into content pipelines
- Post-process AI video (upscaling, interpolation, stabilization)

## When to Use

- Creating social media video content at scale
- Generating B-roll footage for videos
- Prototyping video concepts before filming
- Creating product demos and explainer animations
- Building faceless YouTube channels

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The video-gen workflow follows a standard pipeline pattern.

Core flow:
```
# video-gen primary flow
input = prepare(raw_data)
result = process(input, config={editing, gen, generation, image, kling})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# video-gen primary flow
input = prepare(raw_data)
result = process(input, config={editing, gen, generation, image, kling})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Runway API (Text-to-Video)
```python
import requests

# Create generation task
response = requests.post(
    "https://api.dev.runwayml.com/v1/image_to_video",
    headers={
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gen3a_turbo",
        "promptImage": "https://example.com/frame.png",
        "promptText": "Camera slowly pans right, subject walks forward",
        "duration": 5,
        "ratio": "16:9",
    },
)

task_id = response.json()["id"]

# Poll for completion
import time
while True:
    status = requests.get(
        f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {RUNWAY_API_KEY}"},
    ).json()
    if status["status"] == "SUCCEEDED":
        video_url = status["output"][0]
        break
    time.sleep(5)
```

### Kling API (Text-to-Video)
```python
import requests

response = requests.post(
    "https://api.klingai.com/v1/videos/text2video",
    headers={"Authorization": f"Bearer {KLING_API_KEY}"},
    json={
        "prompt": "A golden retriever running through autumn leaves, slow motion, cinematic",
        "model_version": "kling-v1",
        "duration": "5",
        "aspect_ratio": "16:9",
    },
)
```

### Video Prompt Engineering
```
Structure: [subject] [action] [camera] [style] [mood]

Good prompt:
"Wide shot of a cyberpunk city street at dusk, rain falling,
neon signs reflecting in puddles, camera slowly dollies forward,
cinematic, 4K, Blade Runner aesthetic"

Camera keywords:
- "tracking shot" — camera follows subject
- "dolly zoom" — vertigo effect
- "aerial view" — top-down
- "close-up" — tight framing
- "slow motion" — time manipulation
- "time-lapse" — sped up
```

### Image-to-Video Pipeline
```python
import asyncio

async def animate_image(image_path: str, prompt: str):
    """Animate a still image into video"""
    # Upload image
    with open(image_path, "rb") as f:
        upload = requests.post(
            "https://api.runwayml.com/v1/uploads",
            files={"file": f},
            headers={"Authorization": f"Bearer {RUNWAY_API_KEY}"},
        )
    image_url = upload.json()["url"]

    # Generate video from image
    response = requests.post(
        "https://api.dev.runwayml.com/v1/image_to_video",
        json={"promptImage": image_url, "promptText": prompt, "duration": 5},
        headers={"Authorization": f"Bearer {RUNWAY_API_KEY}"},
    )
    return response.json()["id"]

# Batch animate product images
images = ["product1.png", "product2.png", "product3.png"]
tasks = [animate_image(img, "Product rotates slowly, studio lighting") for img in images]
```

## Common Patterns

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Faceless YouTube Pipeline
```python
# 1. Generate script from topic
script = generate_script("AI trends in 2026")

# 2. Generate voiceover
audio = generate_tts(script, voice="narrator")

# 3. Generate video clips for each section
clips = []
for section in script.sections:
    clip = generate_video(section.visual_prompt, duration=5)
    clips.append(clip)

# 4. Combine with ffmpeg
concatenate_videos(clips, audio, output="final.mp4")
```

### Video Upscaling (Post-Processing)
```python
# Use Real-ESRGAN for upscaling AI video frames
import cv2
from realesrgan import RealESRGAN

model = RealESRGAN(scale=4)
model.load_weights("RealESRGAN_x4.pth")

cap = cv2.VideoCapture("input.mp4")
while True:
    ret, frame = cap.read()
    if not ret: break
    upscaled = model.predict(frame)
    cv2.imwrite(f"frames/{frame_num:06d}.png", upscaled)
```

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior
