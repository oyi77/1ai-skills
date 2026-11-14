---
name: geminigen-ai
description: Use when choosing which media-generation provider/model to route a request to — image, video, or TTS — and applying failover + cost discipline. Conceptual router; concrete API calls live in the linked sibling skills.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- api
- image-generation
- video-generation
- tts
- provider
- routing
- failover
version: 1.0.0
category: content
---

# Geminigen AI — Media Generation Router

> ⚠️ **Scope honesty.** This skill defines *how to choose and sequence* providers. It does **not** ship a verified unified gateway. The provider/model names below are real public offerings, but there is **no single `api.geminigen.ai` endpoint** — each provider has its own SDK/key. Do the actual generation through the sibling skills listed in the matrix, which carry their own (provider-specific) instructions.

## When to Use

**Trigger phrases:**
- "which model should I use for X?" · "route this generation request"
- "failover when a provider errors" · "compare cost across providers"
- "image vs video vs tts — pick the tool"

**Use cases:**
- Deciding between many available models for one brief
- Sequencing primary → fallback when a provider rate-limits or fails
- Keeping a cost ledger across many generation calls

## When NOT to Use

- You need ready-to-run API code — go straight to `image-gen` / `video/gen` / `voice/*`
- Real-time inference inside a request — most video models take 30 s–5 min
- Editing existing footage — use `video/editor`

## Provider Matrix (real models, provider-specific access)

| Task | Options | Where the real how-to lives |
|---|---|---|
| Text-to-image | Nano Banana Pro, Imagen 4, Flux Kontext, Midjourney, Ideogram, Recraft, Stable Diffusion | [image-gen](../image-gen/SKILL.md) |
| Image/text-to-video | Runway, Kling, Sora, Pika, Seedance, Grok Imagine | [video/gen](../video/gen/SKILL.md) |
| TTS (multilingual) | OmniVoice (600+ langs, local) | [voice/omnivoice](../voice/omnivoice/SKILL.md) |
| TTS (free local, retired upstream) | Chatterbox | [voice-chatterbox-tts](../voice-chatterbox-tts/SKILL.md) |

Pick **primary** by quality/latency budget, **fallback** by availability. Never assume two providers share auth.

## Workflow

### Routing Pattern (framework-agnostic)

```python
# router.py — pure decision logic, no network calls
from dataclasses import dataclass
from typing import Callable, Literal

Task = Literal["t2i", "i2v", "t2v", "tts"]
ORDER = {
    "t2i": ["nano-banana-pro", "flux-kontext", "imagen-4"],
    "i2v": ["kling", "runway", "seedance"],
    "t2v": ["sora", "veo"],
    "tts": ["omnivoice", "chatterbox"],
}

@dataclass
class Attempt:
    provider: str
    ok: bool
    detail: str = ""

def route(task: Task, call: Callable[[str, dict], str], **kw) -> tuple[str, list[Attempt]]:
    """Try providers in ORDER[task]; `call(provider, kw)` must do the real
    provider-specific generation and return an asset URL/path. Records attempts."""
    log: list[Attempt] = []
    last = None
    for provider in ORDER[task]:
        try:
            url = call(provider, kw)
            log.append(Attempt(provider, True, url))
            return url, log
        except Exception as e:
            last = e
            log.append(Attempt(provider, False, repr(e)))
    raise RuntimeError(f"all providers failed for task={task}: {last}")
```

The caller supplies `call` — a thin adapter wrapping whichever provider SDK it holds keys for. This skill owns the ordering and logging, not the transport.

## Cost Ledger

Log every attempt regardless of success. Without it you cannot tell whether spend went to good generations or retries:

```python
import csv, datetime

def log_attempts(log: list[Attempt], task: str):
    with open("gen_ledger.csv", "a", newline="") as f:
        for a in log:
            csv.writer(f).writerow([
                datetime.datetime.now(datetime.timezone.utc).isoformat(),
                task, a.provider, a.ok, a.detail,
            ])
```

## Verify Every Asset

Never trust a returned URL alone — download and probe:

```bash
curl -sSL "$ASSET_URL" -o clip.mp4
ffprobe -v error -show_entries format=duration,size -of compact clip.mp4
# Expect duration within ±0.2 s of request; size > 100 KB for video
```

Signed URLs expire; partial uploads happen. Probe before shipping.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "One unified gateway exists" | It doesn't. Each provider has its own SDK/key. This skill routes; siblings execute. |
| "The URL in the response is fine" | Download and `ffprobe` it. Signed-URL expiry and partial uploads are common. |
| "I'll batch 50 video calls at once" | Rate limits will eat them. Serialize with jittered backoff. |
| "Cost tracking is for finance" | You'll burn budget on silent retries without a ledger. |

## Verification

- [ ] Correct sibling skill chosen for the task type
- [ ] Provider order reflects quality→cost tradeoff for the brief
- [ ] Caller-supplied `call` adapter uses real provider credentials
- [ ] Every returned URL downloaded and probed (`ffprobe`)
- [ ] Every attempt appended to `gen_ledger.csv`
- [ ] Jittered exponential backoff on 429 / 5xx (max 3 retries)
