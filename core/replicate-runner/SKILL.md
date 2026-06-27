---
name: replicate-runner
description: Run AI models on Replicate cloud API. Deploy image generation, video creation, audio processing, and custom models without managing infrastructure.
domain: core
tags:
- ai
- replicate
- models
- image-generation
- video
- api
---

# Replicate Runner

## When to Use

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

## Workflow

1. **Install SDK** — `npm install replicate` or `pip install replicate`
2. **Choose model** — Browse replicate.com/models or use model IDs
3. **Run prediction** — Submit input, poll for output
4. **Handle output** — Download files, process results
5. **Chain models** — Pipe output of one model as input to another

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will set up my own GPU server" | Replicate handles scaling, GPU management, and billing per-second |
| "API is too expensive" | Pay-per-use is cheaper than idle GPU time for most workloads |
| "I need full control" | Use custom models on Replicate for full control with managed infra |

## Code Example (Python)

```python
import replicate

output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "A cyberpunk city at sunset, neon lights, rain",
        "num_outputs": 1,
        "aspect_ratio": "16:9"
    }
)
print(output[0].url())
```

## Verification

- [ ] API token authenticated
- [ ] Model predictions complete successfully
- [ ] Output files download correctly
- [ ] Error handling for rate limits and failures
- [ ] Cost tracking per prediction

