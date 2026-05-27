---
name: image-gen
description: AI image generation — Stable Diffusion, Midjourney, DALL-E, ComfyUI. Prompt engineering for images, inpainting, outpainting, ControlNet
---

## Overview

AI image generation creates images from text prompts using diffusion models. This skill covers prompt engineering for consistent results, inpainting/outpainting for editing, ControlNet for precise control, and API integration for production workflows.

## Capabilities

- Generate images from text prompts (DALL-E, Stable Diffusion, Midjourney)
- Engineer prompts with positive/negative prompts, style modifiers, and weights
- Edit existing images with inpainting and outpainting
- Use ControlNet for pose, depth, and edge-guided generation
- Batch generate images for content pipelines
- Integrate via API (OpenAI, Stability AI, Replicate)
- Set up local generation with ComfyUI or Automatic1111

## When to Use

- Creating marketing visuals, thumbnails, social media images
- Generating product mockups and concept art
- Building content pipelines that need custom images
- Editing photos (remove backgrounds, change styles)
- Creating consistent character/brand imagery

## Pseudo Code

### OpenAI DALL-E API
```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A minimalist logo for a tech startup called Nova, flat design, blue and white",
    size="1024x1024",
    quality="hd",
    n=1,
)

image_url = response.data[0].url
```

### Stability AI API
```python
import requests

response = requests.post(
    "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
    headers={"Authorization": f"Bearer {STABILITY_API_KEY}"},
    json={
        "text_prompts": [
            {"text": "cyberpunk cityscape at night, neon lights, rain", "weight": 1},
            {"text": "blurry, low quality, watermark", "weight": -1},
        ],
        "cfg_scale": 7,
        "steps": 30,
        "width": 1024,
        "height": 1024,
    },
)
```

### Prompt Engineering for Images
```
Structure: [subject] [style] [details] [lighting] [camera] [quality]

Good prompt:
"A portrait of a cyberpunk hacker, neon lighting, rain-soaked streets,
cinematic composition, 8k, photorealistic, volumetric lighting,
shot on Sony A7III, f/1.4 bokeh"

Negative prompt:
"blurry, low quality, watermark, text, deformed, ugly, extra limbs,
bad anatomy, bad hands, cropped, worst quality"

Weights (Automatic1111):
"(neon:1.5) city at night" — emphasize neon
"ugly, (deformed:1.3)" — strongly avoid deformed
```

### ComfyUI Workflow (Local)
```python
# Load ComfyUI workflow JSON
import json

with open("workflow.json") as f:
    workflow = json.load(f)

# Modify prompt
workflow["6"]["inputs"]["text"] = "a cat wearing a space helmet, digital art"

# Queue generation
import requests
requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow})
```

### Batch Generation Pipeline
```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def generate_image(prompt: str, index: int):
    response = await client.images.generate(
        model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard"
    )
    return {"index": index, "url": response.data[0].url}

prompts = [
    "Minimalist tech blog header, abstract circuits",
    "Team collaboration illustration, flat design",
    "Cloud infrastructure diagram, isometric",
]

results = await asyncio.gather(*[generate_image(p, i) for i, p in enumerate(prompts)])
```

## Common Patterns

### Consistent Characters
```
Prompt template with fixed descriptors:
"Character NAME, [fixed appearance], [scene description], [style]"

Example:
"Luna, young woman with silver hair and blue eyes, standing in a cyberpunk market,
anime style, studio lighting"
```

### Style Transfer
```python
# img2img: transform existing image
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    prompt="Transform into watercolor painting style",
    size="1024x1024",
)
```

### Inpainting (Edit Part of Image)
```python
response = client.images.edit(
    model="dall-e-2",
    image=open("photo.png", "rb"),
    mask=open("mask.png", "rb"),  # White = edit area
    prompt="Replace background with beach sunset",
)
```
