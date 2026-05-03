---
persona:
  name: "Domain Expert"
  title: "Master of Ai Interceptor"
  expertise: ['1Ai-Autodroid Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# AI Interceptor — Universal AI Middleware

> **Global, provider-agnostic middleware** for any skill or automation.
> Intercept, transform, validate, and route AI calls across any provider.

---

## Overview

AI Interceptor is a **hook-based middleware** that sits between your automation code
and AI providers. It runs configurable PRE / POST / ERROR hooks around every AI call:

- **PRE hooks** — enhance prompts, validate inputs, select providers, rate-limit
- **POST hooks** — score output quality, filter content, compress, log results
- **ERROR hooks** — retry with fallbacks, alert, circuit-break

It supports **any provider** (Kling, Grok, Flow, PixVerse, PostBridge) and any
automation context (Python scripts, cron jobs, API servers, ADB automation).

---

## Architecture

```
Your Automation Code
        │
        ▼
┌──────────────────────────────────────────────────────┐
│                    AIInterceptor                     │
│                                                      │
│  ┌─────────┐     ┌─────────┐     ┌──────────────┐   │
│  │  PRE    │────▶│ ROUTE   │────▶│    POST      │   │
│  │ Hooks   │     │Provider │     │   Hooks      │   │
│  └─────────┘     └────┬────┘     └──────────────┘   │
│                       │               ▲              │
│                 ┌─────▼─────┐         │              │
│                 │  ERROR    │─────────┘              │
│                 │  Hooks    │   (retry / fallback)   │
│                 └───────────┘                        │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│               Provider Registry                      │
│  kling │ grok │ flow │ pixverse │ postbridge │ ...   │
└──────────────────────────────────────────────────────┘
```

---

## Supported Providers

| Provider     | Capabilities                      | Cost (credits)         | Config Key    |
|--------------|-----------------------------------|------------------------|---------------|
| **Kling**    | text2video, image2video, text2image | 60 / 144 / 10        | `kling`       |
| **Grok**     | text_generation                   | token-based            | `grok`        |
| **Flow**     | text2video, image2video           | 50 / 100               | `flow`        |
| **PixVerse** | text2video, image2video           | 40 / 80                | `pixverse`    |
| **PostBridge**| social_post                      | 0 (subscription)       | `postbridge`  |

---

## Quick Start

### 1. Provider Registry

```python
from scripts.providers import get_registry

registry = get_registry()

# Get a specific provider
kling = registry.get("kling", config={"cookie": "your_cookie_here"})

# Find the best available provider for a task
best = registry.best_for("text2video", min_credits=60)

# Health check all providers
for h in registry.health_report():
    print(f"{h['provider']}: available={h['available']} credits={h['credits']}")
```

### 2. Decorator Pattern (AIInterceptor)

```python
from scripts.ai_interceptor import AIInterceptor, intercept

interceptor = AIInterceptor(config_path="config/ai_interceptor_config.json")

@intercept(interceptor, task_type="text2video")
def generate_video(prompt: str, **kwargs):
    # Your generation code here
    return {"output": "video.mp4", "success": True}

result = generate_video("A mountain at sunset")
# PRE hooks ran before → POST hooks ran after
```

### 3. Full Kling Pipeline

```python
from scripts.kling_pipeline import KlingPipeline

pipeline = KlingPipeline(config={
    "output_dir": "/tmp/kling_output",
    "min_credits": 60,
})

result = pipeline.text_to_video(
    prompt="Epic cinematic mountain landscape at golden hour",
    remove_watermark=True,
    enhance_quality=True,
    duration="5",
    mode="std",
)

print(result["video_path"])       # Final polished video
print(result["credits_used"])     # Credits consumed
print(result["quality_score"])    # AI quality score
```

---

## Video Enhancement Pipeline

Wraps [KLing-Video-WatermarkRemover-Enhancer](../KLing-Video-WatermarkRemover-Enhancer) for:

| Step | Tool       | Description                               |
|------|------------|-------------------------------------------|
| 1    | STTN       | Inpainting at Kling watermark region      |
| 2    | Real-ESRGAN| 2× upscale with AI super-resolution       |
| 3    | GFPGAN     | Facial detail enhancement                 |

```python
from scripts.video_enhancer import VideoEnhancer

enhancer = VideoEnhancer()

# Full pipeline (remove watermark + enhance)
output = enhancer.process("raw_video.mp4", remove_wm=True, enhance=True)

# Or step-by-step
no_wm = enhancer.remove_watermark("raw_video.mp4")
final = enhancer.enhance(no_wm, upscale=2)
```

### Setup (download weights)

```bash
cd scripts/
python - <<'EOF'
from video_enhancer import VideoEnhancer
e = VideoEnhancer()
e.setup()  # Downloads RealESRGAN + GFPGAN; sttn.pth needs manual DL
EOF
```

**Manual sttn.pth download:**
```
https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view
→ Save to: KLing-Video-WatermarkRemover-Enhancer/weights/sttn.pth
```

**Watermark bounding box** (Kling 9:16 1080p):
```python
KLING_WATERMARK_BOX = [556, 1233, 701, 1267]  # [x1, y1, x2, y2]
```

---

## Account Manager (Multi-Account Credit Pooling)

```python
from scripts.kling_account_manager import KlingAccountManager

mgr = KlingAccountManager()

# Add accounts to the pool
mgr.add_account("email@gmail.com", "password123")

# Get account with most credits (above threshold)
account = mgr.get_best_account(min_credits=60)

# Claim daily login bonus for ALL accounts
result = mgr.claim_all_daily_bonuses()
print(f"Bonus claimed for {len(result['claimed'])} accounts")

# Check total credit pool
total = mgr.get_total_credits()
print(f"Total pool: {total:.0f} credits")

# Rotate when credits drop below threshold
new_account = mgr.rotate_if_low(current_credits=30, threshold=60)
```

### Accounts File Format

Located at: `~/.openclaw/workspace/config/kling_accounts.json`

```json
[
  {
    "email": "account1@gmail.com",
    "password": "password",
    "cookie": "",
    "credits": 1200,
    "active": true,
    "last_bonus_claimed": null
  }
]
```

Copy template: `config/kling_accounts.json.example`

---

## Configuration Reference

### `config/ai_interceptor_config.json`

```json
{
  "hooks": {
    "pre": ["prompt_enhance", "validate_input", "rate_limit"],
    "post": ["quality_score", "content_filter", "log"],
    "error": ["retry", "fallback_provider", "alert"]
  },
  "providers": {
    "kling": {
      "api_key": "",
      "cookie": "",
      "poll_interval": 10,
      "max_wait": 600
    },
    "grok": {
      "api_key": "",
      "model": "grok-beta",
      "max_tokens": 2048
    },
    "postbridge": {
      "api_key": "pb_live_...",
      "social_accounts": [49678, 49682]
    }
  },
  "video_enhancer": {
    "repo_path": null,
    "weights_dir": null,
    "watermark_box": [556, 1233, 701, 1267]
  },
  "account_manager": {
    "accounts_file": null,
    "min_credits": 60,
    "rotation_threshold": 60
  }
}
```

---

## File Structure

```
automation/ai-interceptor/
├── SKILL.md                              ← This file
├── scripts/
│   ├── ai_interceptor.py                 ← Core middleware (hooks engine)
│   ├── adb_interceptor.py                ← Android ADB specialization
│   ├── content_interceptor.py            ← Content-specific hooks
│   ├── prompt_interceptor.py             ← Prompt enhancement hooks
│   ├── ai_visual_validator.py            ← Vision-based output scoring
│   ├── test_interceptor.py               ← Test suite
│   ├── video_enhancer.py                 ← Watermark removal + upscaling
│   ├── kling_account_manager.py          ← Multi-account credit manager
│   ├── kling_pipeline.py                 ← End-to-end generation pipeline
│   └── providers/
│       ├── __init__.py                   ← Public API
│       ├── base_provider.py              ← Abstract base class
│       ├── kling_provider.py             ← Kling AI
│       ├── grok_provider.py              ← Grok (xAI)
│       ├── flow_provider.py              ← Flow video generation
│       ├── pixverse_provider.py          ← PixVerse video generation
│       ├── postbridge_provider.py        ← PostBridge social media
│       └── provider_registry.py          ← Registry + auto-discovery
├── config/
│   ├── ai_interceptor_config.json        ← Main config
│   └── kling_accounts.json.example      ← Account template
└── examples/
    ├── kling_with_interceptor.py         ← Kling + hooks example
    ├── postbridge_with_interceptor.py    ← PostBridge example
    ├── full_pipeline_example.py          ← Full E2E pipeline demo
    └── multi_account_example.py         ← Account manager demo
```

---

## Examples

Run examples:

```bash
cd /mnt/data/berkahkarya/skills/1ai-skills/automation/ai-interceptor/

# Full pipeline (needs KLING_COOKIE or KLING_API_KEY)
KLING_COOKIE="your_cookie" python examples/full_pipeline_example.py

# Multi-account manager demo
python examples/multi_account_example.py

# Existing examples
python examples/kling_with_interceptor.py
python examples/postbridge_with_interceptor.py
```

---

## Adding a New Provider

1. Create `scripts/providers/myprovider_provider.py`
2. Inherit from `BaseProvider` and implement `generate()`, `check_credits()`, `is_available()`
3. Add to `provider_registry.py` `auto_register()` list
4. Export from `__init__.py`

```python
# scripts/providers/myprovider_provider.py
from .base_provider import BaseProvider, ProviderCapability

class MyProvider(BaseProvider):
    name = "myprovider"
    capabilities = [ProviderCapability.TEXT2VIDEO]
    cost_per_call = {ProviderCapability.TEXT2VIDEO: 50}

    def generate(self, task_type, **kwargs):
        # ... your implementation
        return {"success": True, "output": "path/to/output", "cost": 50, "metadata": {}, "error": None}

    def check_credits(self):
        return 500.0

    def is_available(self):
        return bool(self._config.get("api_key"))
```

---

## Logging

All operations are logged to `~/.openclaw/workspace/logs/`:

| File                           | Contents                        |
|--------------------------------|---------------------------------|
| `kling_pipeline.log`           | Pipeline runs (JSON lines)      |
| `kling_account_manager.log`    | Account operations              |
| `video_enhancer.log`           | Enhancement operations          |

```bash
tail -f ~/.openclaw/workspace/logs/kling_pipeline.log | jq .
```

---

---

## Account Generator

Automates Kling AI account registration to get free credits via temp email + proxy rotation.

**Location:**
```
automation/autodroid-kling-agent/kling_api/kling_account_generator.py
automation/autodroid-kling-agent/kling_api/kling_account_generator_cli.py
```

**Dependencies:**
```bash
pip install pynator primp requests
```

**Quick usage:**
```bash
# Generate 1 account
python3 kling_account_generator_cli.py --count 1

# Generate 5 accounts with proxy rotation
python3 kling_account_generator_cli.py --count 5 --proxy-list proxies.txt

# List saved accounts
python3 kling_account_generator_cli.py --list

# Export as JSON (for piping)
python3 kling_account_generator_cli.py --list --json
```

**Python API:**
```python
from kling_account_generator import KlingAccountGenerator

gen = KlingAccountGenerator()

# Single account
result = gen.generate_account(proxy="http://user:pass@host:port")
# {"success": True, "email": "...", "password": "...", "cookie": "...", "credits": 66.0}

# Batch with proxy rotation
results = gen.batch_generate(count=10, proxy_list=["http://p1", "http://p2"])
```

**Flow:**
1. Generate temp @googlemail.com via Emailnator (pynator)
2. Visit klingai.com with primp browser fingerprint → get `kGateway-identity` cookie
3. `POST /api/user/sendEmailCode` → trigger OTP email
4. Poll Emailnator inbox until 6-digit OTP arrives (timeout: 90s)
5. `POST /api/user/register` (tries 3 endpoints) → register account
6. `POST id.klingai.com/pass/ksi18n/web/login/emailPassword` → login
7. `POST /api/user/signIn` → claim daily bonus
8. Save to `~/.openclaw/workspace/config/kling_accounts.json`

**Endpoints (ordered by priority):**

| Endpoint | Status | Notes |
|----------|--------|-------|
| `POST /api/user/sendEmailCode` | Needs session | Returns 500 without valid cookies |
| `POST /api/user/register` | Primary | Tried first |
| `POST /api/user/emailRegister` | Fallback | If primary 404s |
| `POST /api/user/registerByEmail` | Fallback | Last resort |
| `POST id.klingai.com/.../login/emailPassword` | ✅ Known working | From klingCreator lib |

**Error handling:**
- OTP timeout (90s) → skip account, retry with next proxy
- CAPTCHA detected → log and skip (no bypass attempted)
- All register endpoints fail → log full request/response for debugging
- Any single account failure → does NOT crash batch; continues to next

**Output files:**
- Accounts: `~/.openclaw/workspace/config/kling_accounts.json`
- Logs: `~/.openclaw/workspace/logs/kling_generator.log`

---

*AI Interceptor — Universal AI Middleware for BerkahKarya automation stack* 🔥
