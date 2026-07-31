---
name: replicate-runner
description: Run AI models on Replicate cloud API. Deploy image generation, video creation, audio processing, and custom models without managing infrastructure. Use when working with replicate runner.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai
- replicate
- models
- image-generation
- video
- api
version: 1.0.0
---

# Replicate Runner

## When to Use
**Trigger phrases:**
- "replicate runner"
- "Run AI models on Replicate cloud API"


- When running AI models without managing GPU infrastructure
- When generating images, videos, or audio with state-of-the-art models
- When deploying custom models to a cloud API
- When chaining multiple AI models in a pipeline

## When NOT to Use

- For local inference (use Ollama skills)
- For OpenAI-compatible endpoints (use OpenAI skills)
- For fine-tuning (use training-specific skills)

## Overview

Access 1000+ AI models via Replicate API. Run Flux, Stable Diffusion, Whisper, and custom models with a single API call. Pay per second of compute.


## Setup & Configuration

### 1. Get API Token

Sign up at [replicate.com](https://replicate.com), then create an API token in your account settings.

### 2. Environment Variable

```bash
export REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxx
```

Or store in `.env`:

```bash
REPLICATE_API_TOKEN=r8_xxxxxxxxxxxxxxxxxxxx
```

### 3. Install SDK

**Python:**
```bash
pip install replicate
```

**Node.js:**
```bash
npm install replicate
```

### 4. SDK Initialization

**Python:**
```python
import replicate
# Token auto-reads from REPLICATE_API_TOKEN env var
```

**Node.js:**
```javascript
import Replicate from "replicate";
const replicate = new Replicate();
```

### Pricing Model

| Plan | Compute Per Second |
|------|-------------------|
| Pay-as-you-go | $0.000113/s (base) |
| Annual Commitment | ~20% discount |
| Private Deployments | Custom pricing |

Most models also include a **free prediction** for first-time use.

## Workflow

1. **Install SDK** — `npm install replicate` or `pip install replicate`
2. **Choose model** — Browse replicate.com/models or use model IDs
3. **Run prediction** — Submit input, poll for output
4. **Handle output** — Download files, process results
5. **Chain models** — Pipe output of one model as input to another

---

## Core Usage — Synchronous Prediction

The simplest path: submit a prediction and wait for the result.

**Python:**
```python
import replicate

# Flux image generation
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "cyberpunk city at sunset, neon lights, rain",
        "num_outputs": 2,
        "aspect_ratio": "16:9",
        "num_inference_steps": 4,
    }
)
for item in output:
    print(item.url)
```

**Node.js:**
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const output = await replicate.run(
  "black-forest-labs/flux-schnell",
  {
    input: {
      prompt: "cyberpunk city at sunset, neon lights, rain",
      num_outputs: 2,
      aspect_ratio: "16:9",
    },
  }
);
console.log(output);
```

---

## Advanced Usage Patterns

### Async Prediction with Webhook Callback

For long-running models (video, upscaling), use webhooks so Replicate POSTs the result to your server instead of blocking.

**Python:**
```python
import replicate

prediction = replicate.predictions.create(
    version="lucataco/remove-bg:95fcc2a26d3899cd6c26964560f8e0e6a2f5b8c1e5c7e3c5e8f3c5e8d3c5e8f3",
    input={"image": "https://example.com/photo.jpg"},
    webhook="https://myapp.com/replicate-callback",
    webhook_events_filter=["completed"]
)

print(f"Prediction ID: {prediction.id}")
print(f"Started: {prediction.created_at}")
# Webhook will deliver {prediction.id} with output when done
```

**Node.js:**
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const prediction = await replicate.predictions.create({
  version: "lucataco/remove-bg:95fcc2a26d3899cd6c26964560f8e0e6a2f5b8c1e5c7e3c5e8f3c5e8d3c5e8f3",
  input: { image: "https://example.com/photo.jpg" },
  webhook: "https://myapp.com/replicate-callback",
  webhook_events_filter: ["completed"],
});
```

### Image-to-Image Pipeline

Generate an image, then use it as input to a second model.

**Python:**
```python
import replicate
from PIL import Image
import requests

# Step 1: Generate base image
base = replicate.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "mountain landscape", "num_outputs": 1}
)
base_url = base[0].url

# Step 2: Download image bytes
img_bytes = requests.get(base_url).content

# Step 3: Upscale with Real-ESRGAN
upscaled = replicate.run(
    "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d69",
    input={"image": img_bytes, "scale": 2}
)
print("Upscaled:", upscaled)
```

### Audio Transcription

**Python:**
```python
import replicate

output = replicate.run(
    "openai/whisper:4d50797390bb4d5e5e1b2b6c8c6b5a7a7b9f5b7c8d9e0f1a2b3c4d5e6f7a8b9c",
    input={
        "audio": "https://example.com/meeting.mp3",
        "model": "large-v3",
        "language": "en"
    }
)
print(output["text"])
```

**Node.js:**
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const output = await replicate.run(
  "openai/whisper:4d50797390bb4d5e5e1b2b6c8c6b5a7a7b9f5b7c8d9e0f1a2b3c4d5e6f7a8b9c",
  {
    input: {
      audio: "https://example.com/meeting.mp3",
      model: "large-v3",
      language: "en",
    },
  }
);
console.log(output.text);
```

### Video Generation

**Python:**
```python
import replicate
import time

# Start prediction (non-blocking)
prediction = replicate.predictions.create(
    version="stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
    input={
        "input_image": "https://example.com/photo.png",
        "video_length": 25,
        "sizing_strategy": "maintain_aspect_ratio",
    }
)

# Poll until complete
prediction = replicate.predictions.get(prediction.id)
while prediction.status not in ("succeeded", "failed", "canceled"):
    time.sleep(2)
    prediction = replicate.predictions.get(prediction.id)

if prediction.status == "succeeded":
    print("Video URL:", prediction.output)
```

**Node.js:**
```javascript
import Replicate from "replicate";
const replicate = new Replicate();

const prediction = await replicate.predictions.create({
  version:
    "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
  input: {
    input_image: "https://example.com/photo.png",
    video_length: 25,
  },
});

// Poll for completion
let result = await replicate.predictions.get(prediction.id);
while (result.status !== "succeeded" && result.status !== "failed") {
  await new Promise((r) => setTimeout(r, 2000));
  result = await replicate.predictions.get(prediction.id);
}

if (result.status === "succeeded") {
  console.log("Video URL:", result.output);
}
```

### Batch Processing with Error Isolation

When running many predictions, isolate failures so one error doesn't kill the batch.

**Python:**
```python
import replicate
from concurrent.futures import ThreadPoolExecutor, as_completed

prompts = [
    "cyberpunk city",
    "fantasy forest",
    "underwater temple",
]

def generate(prompt: str) -> dict:
    try:
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={"prompt": prompt, "num_outputs": 1}
        )
        return {"prompt": prompt, "url": str(output[0]), "status": "ok"}
    except Exception as e:
        return {"prompt": prompt, "error": str(e), "status": "failed"}

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(generate, p): p for p in prompts}
    for future in as_completed(futures):
        print(future.result())
```

---

## Common Issues & Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `401 Unauthorized` | Missing or invalid API token | Set `REPLICATE_API_TOKEN` env var or pass `api_token` to constructor |
| `402 Payment Required` | Insufficient account credits | Top up at replicate.com/account/billing |
| `429 Too Many Requests` | Rate limit exceeded | Add exponential backoff (start 1s, max 30s) |
| Model not found | Incorrect version hash or model ID | Always use `owner/name:version_hash` format from replicate.com |
| `CUDA out of memory` | Model too large for queue | Use a quantized version or smaller variant |
| `InputValidationError` | Wrong parameter name or type | Check model's schema: `replicate.models.get("owner/name").versions.list()` |
| Webhook never fires | URL unreachable from Replicate | Use a public HTTPS endpoint; test with webhook.site first |
| Prediction hangs at `processing` | Queue backlog for popular models | Switch to webhook pattern or set `replicate.predictions.create(..., webhook=...)` for visibility |
| File too large for input | Replicate has 50MB input limit | Host file on object storage (S3, R2) and pass the URL instead |
| `model_version` deprecated | SDK version mismatch | Upgrade: `pip install --upgrade replicate` or `npm install replicate@latest` |

### Rate Limit Handling
```python
import time
import replicate

def run_with_retry(model_id, input_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return replicate.run(model_id, input=input_data)
        except replicate.exceptions.ReplicateError as e:
            if "429" in str(e) and attempt < max_retries - 1:
                sleep = (2 ** attempt) + 1
                print(f"Rate limited, retrying in {sleep}s...")
                time.sleep(sleep)
                continue
            raise
```

### Cost Tracking

**Python:**
```python
import replicate

prediction = replicate.predictions.get("prediction_id")
cost = prediction.metrics.get("predict_time", 0) * 0.000113
print(f"Prediction {prediction.id}: {prediction.status}")
print(f"Compute time: {prediction.metrics.get('predict_time', 'N/A')}s")
print(f"Estimated cost: ${cost:.4f}")
```

---

## Monetization

Replicate's platform and per-second billing model open several revenue channels:

### 1. Custom Model Hosting Service
Deploy your own fine-tuned models (LoRA, DreamBooth) as private Replicate models, then resell API access at a markup.
- **Model:** Deploy as `you/your-model` on Replicate Cog
- **Pricing:** Replicate charges ~$0.000113/s; you resell at $0.0005–$0.001/s via your own API wrapper
- **Margin:** 4–10x on compute, zero GPU management overhead

### 2. White-Label Image/Video API
Bundles of curated models behind a single branded API.
- Integrate Flux + upscaling + background removal into one `/generate` endpoint
- Charge per-image ($0.01–$0.10) versus paying per-second to Replicate
- Target: e-commerce platforms needing product photography at scale

### 3. Async Media Processing Pipeline
Webhook-based batch processor for high-volume workloads.
- Accept bulk uploads, route through Replicate models, return results asynchronously
- Monetize via subscription tiers (100/mo free, $29/mo for 10K, enterprise custom)
- Models: upscaling, background removal, watermarking, format conversion

### 4. SaaS Frontend + Caching Layer
Wrap Replicate with caching (same prompt → same output → no API cost) and a better UI.
- Cache identical requests in object storage
- Tiered pricing: cache hits cost you $0, pass Replicate cost only on cache misses
- Add analytics dashboard, batch history, A/B testing for prompts

### 5. One-Click Model Deployment Service
Help non-technical customers deploy their own custom models (art style, face, product).
- Charge $99–$499/setup + monthly hosting fee
- Customer uploads 10–20 reference images, you train a LoRA and deploy to Replicate
- Replicate handles all GPU; you handle the training script, UI, and billing

### Cost Optimization Tips

| Strategy | Savings |
|----------|---------|
| Cache frequent prompts in object storage | Eliminates repeat compute cost |
| Use `flux-schnell` (4 steps) instead of `flux-dev` (28 steps) | ~7x cheaper |
| Batch parameters into single prediction when model supports it | One queue slot, one cold-start |
| Prefer smaller model variants (Quantized = Q4/Q8) | 2–4x faster, cheaper per second |
| Use webhooks instead of polling | No wasted compute on poll requests |
| Schedule batch jobs during off-peak hours | Lower queue wait (less idle billing) |

## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run replicate runner workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] API token authenticated
- [ ] Model predictions complete successfully
- [ ] Output files download correctly
- [ ] Error handling for rate limits and failures
- [ ] Cost tracking per prediction

