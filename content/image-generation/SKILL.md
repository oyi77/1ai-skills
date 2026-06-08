---
name: image-generation
description: AI image generation — Stable Diffusion, Midjourney, DALL-E, Flux. Prompt
  engineering for visuals, inpainting, outpainting, style transfer
domain: content
---



## Overview

Generate images using AI models. Covers prompt crafting, API integration, inpainting/outpainting, and batch workflows for content production.

## Capabilities

- Generate images via DALL-E, Midjourney, Stable Diffusion, Flux APIs
- Craft effective image prompts with style, composition, and negative prompts
- Inpaint and outpaint for editing existing images
- Use ControlNet for guided generation (pose, depth, edges)
- Batch generate image variations for A/B testing
- Integrate image generation into content pipelines

## When to Use

- Creating marketing visuals, thumbnails, or social media images
- Generating product mockups or concept art
- Editing photos with AI (remove objects, extend backgrounds)
- Building content pipelines that need automated image creation
- Creating variations of existing designs for testing

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The image-generation workflow follows a standard pipeline pattern.

Core flow:
```
# image-generation primary flow
input = prepare(raw_data)
result = process(input, config={dall, diffusion, engineering, flux, generation})
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
# image-generation primary flow
input = prepare(raw_data)
result = process(input, config={dall, diffusion, engineering, flux, generation})
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


### DALL-E via OpenAI API
```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A minimalist logo for a tech startup, clean lines, blue and white, modern",
    size="1024x1024",
    quality="hd",
    n=1
)

image_url = response.data[0].url
```

### Stable Diffusion via API
```python
import requests

# Automatic1111 API
response = requests.post("http://localhost:7860/sdapi/v1/txt2img", json={
    "prompt": "cyberpunk city at sunset, neon lights, highly detailed",
    "negative_prompt": "blurry, low quality, distorted",
    "steps": 30,
    "cfg_scale": 7,
    "width": 1024,
    "height": 1024,
    "sampler_name": "DPM++ 2M Karras"
})
```

### Flux via Replicate
```python
import replicate

output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "A cat wearing a top hat, oil painting style",
        "num_outputs": 4,
        "aspect_ratio": "1:1"
    }
)
```

### Inpainting (Edit Parts of Image)
```python
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),  # White areas get replaced
    prompt="A golden retriever sitting on the grass",
    size="1024x1024"
)
```

### Batch Generation
```python
prompts = [
    "Modern office workspace, minimalist",
    "Cozy home office with plants",
    "Standing desk setup, tech aesthetic"
]

for i, prompt in enumerate(prompts):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="hd"
    )
    download_image(response.data[0].url, f"image_{i}.png")
```

## Common Patterns

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Prompt Structure
```
[Subject] + [Style] + [Details] + [Lighting] + [Quality]

Example: "A mountain cabin at dusk, watercolor painting style,
misty atmosphere, warm golden light from windows, 4k detailed"
```

### Negative Prompt Template (SD/Flux)
```
blurry, low quality, distorted, deformed, ugly, bad anatomy,
bad proportions, extra limbs, duplicate, watermark, text, logo
```

### Platform Selection
```
DALL-E 3: Best for text rendering, creative concepts, API-first
Midjourney: Best aesthetic quality, Discord-based, artistic
Stable Diffusion: Self-hosted, full control, ControlNet support
Flux: Fast, high quality, good for batch production
```

### Cost Optimization
```
- Use DALL-E 2 ($0.02/image) for drafts, DALL-E 3 ($0.04-0.08) for finals
- Self-host SD for high-volume (GPU cost ~$200/mo, unlimited images)
- Cache and reuse base images, only inpaint variations
- Use smaller sizes for social media, larger for print
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
