---
name: video-gen
description: AI video generation — Sora, Runway, Pika, Kling. Text-to-video, image-to-video, video editing with AI
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

## Pseudo Code

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
