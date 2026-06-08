---
name: content-kingdom
description: ">\n  Content Kingdom Orchestrator — the BRAIN that coordinates all 12\
  \ content phases\n  for BerkahKarya / JENDRALBOT. Sequences research → plan → script\
  \ → create →\n  review → schedule → post → engage → analyze → optimize → repurpose\
  \ → scale.\n  Thin coordinator: imports existing autopilot_affiliate_engine and\
  \ content-generator\n  scripts; only builds truly new modules (comment_manager,\
  \ engagement_engine).\n  v2.0: GeminiGen API as primary media provider + Veris Design\
  \ System enforced.\n"
version: 2.0.0
author: Vilona / BerkahKarya AI
tags:
- content
- automation
- tiktok
- instagram
- postbridge
- jendralbot
- berkahkarya
- geminigen
- veris
skill_dir: skills/1ai-skills/content/content-kingdom
symlink: skills/content-kingdom
domain: content
---


# Content Kingdom Orchestrator

## Overview

A **lean 12-phase pipeline** that turns raw trends into scheduled, analyzed, and scaled social media content — fully automated, with Paperclip issue tracking.

**SOLID design:**
- Each phase = single responsibility, independently runnable
- New phases: add to `PHASE_REGISTRY` in `orchestrator.py` — no other edits
- All new modules extend `BaseModule` (dependency inversion)
- Public API: 4 methods only (`run_daily_pipeline`, `run_phase`, `get_status`, `create_paperclip_issues`)

**KISS design:**
- Existing scripts called via subprocess — no reimplementation
- Only 2 truly new modules: `comment_manager.py`, `engagement_engine.py`
- Config extends `autopilot_affiliate_engine/config.py` at runtime

---

## File Structure

```
skills/1ai-skills/content/content-kingdom/
├── SKILL.md                       ← you are here
├── orchestrator.py                ← BRAIN: thin coordinator
├── base_module.py                 ← BaseModule + PhaseResult (DI foundation)
├── config.json                    ← config (extends engine config at runtime)
├── state.json                     ← auto-generated: pipeline state
├── modules/
│   ├── __init__.py
│   ├── persona_manager.py         ← brand voice + caption generation
│   ├── comment_manager.py         ← Phase 8: ENGAGE (new)
│   ├── engagement_engine.py       ← Phase 12: SCALE (new)
│   ├── veris_design.py            ← v2.0: Veris Design System (prompts + palette)
│   └── geminigen_client.py        ← v2.0: GeminiGen API client (images + videos)
├── output/                        ← phase outputs (today_plan.json, scripts_*.json, …)
├── logs/                          ← daily orchestrator logs
├── templates/                     ← caption/storyboard templates
└── tests/                         ← unit tests
```

**Symlink:** `skills/content-kingdom → skills/1ai-skills/content/content-kingdom`

---

---

## Veris Design Principles (v2.0)

Extracted from **Veris** (Ads Master, 10+ years) training session. Applied automatically in Phase 4: CREATE.

### Core Rules (NON-NEGOTIABLE)
1. **Pure black background** — `#000000`, no exceptions, ever
2. **High contrast white text** — headlines in `#FFFFFF`, nothing below 60% opacity
3. **Three-zone vertical layout** — every ad must have: Hook / Body / CTA zones
4. **No vibrant colors** — accent palette limited to dark trust/urgency signals
5. **No emoji in visuals** — emoji in captions are OK, never in images
6. **Minimalist premium** — less elements = more premium feel = higher trust

### Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| `bg_primary` | `#000000` | Main background (mandatory) |
| `bg_secondary` | `#000020` | Secondary surfaces |
| `text_primary` | `#FFFFFF` | Headlines, CTA text |
| `text_secondary` | `#808080` | Supporting copy |
| `accent_trust` | `#202040` | Borders, trust badges |
| `accent_urgency` | `#200000` | Scarcity signals |
| `accent_soft` | `#606080` | Decorative elements |

### Three-Zone Layout

```
┌─────────────────────────────┐
│  HOOK ZONE (top 20-30%)     │  ← Bold headline, stops the scroll
│  "Bisa Cuan 1 Juta/Hari?"  │
├─────────────────────────────┤
│  BODY ZONE (middle 40-50%) │  ← Product detail, builds desire
│  What it is, what it does  │
├─────────────────────────────┤
│  CTA ZONE (bottom 20-30%)  │  ← Action button, price, frame
│  [Lihat Sekarang → Rp 49K] │
└─────────────────────────────┘
```

### Platform Priority (Veris Approach)
1. **Instagram** — PRIMARY (where ads convert)
2. **Facebook** — SECONDARY (older, higher spend audience)
3. **Threads** — TERTIARY (IG companion, free reach)
4. **TikTok** — QUATERNARY (volume play, lower CPM)

### Formats

| Platform | Width | Height | Ratio |
|----------|-------|--------|-------|
| Instagram Portrait | 1024 | 1280 | 4:5 ← PRIMARY |
| Instagram Feed | 800 | 800 | 1:1 |
| TikTok | 1080 | 1920 | 9:16 |

### Using Veris in Code

```python
from modules.veris_design import build_veris_prompt, veris_prompt_for_platform
from modules.geminigen_client import GeminiGenClient

# Build Veris-style prompt
payload = veris_prompt_for_platform(
    product_name="Guru Pintar AI",
    hook_text="Bisa Cuan Rp 1 Juta/Hari?",
    platform="instagram",
)

# Generate via GeminiGen
client = GeminiGenClient()
resp = client.generate_image(**payload)
url = client.generate_image_sync(**payload)  # sync version → returns URL
```

---

## GeminiGen API (v2.0 — Primary Media Provider)

**Base URL:** `https://api.geminigen.ai`  
**Auth:** `x-api-key` header  
**Key config:** `workspace/config/geminigen_api.json` → `{"api_key": "..."}`

### Supported Operations

| Endpoint | Purpose | Module |
|----------|---------|--------|
| `POST /uapi/v1/generate_image` | Image generation | `GeminiGenClient.generate_image()` |
| `POST /uapi/v1/video-gen/grok` | Video generation (Grok) | `GeminiGenClient.generate_video_grok()` |
| `GET /uapi/v1/history/:uuid` | Poll job status | `GeminiGenClient.get_status()` |

### Status Codes
- `1` = processing (keep polling)
- `2` = completed (extract URL)
- `3` = failed (raise error)

### Phase 4 CREATE Provider Chain (v2.0)

**Images:**
```
GeminiGen (nano-banana-pro + Veris prompt)
  ↓ on failure
NVIDIA (Flux) via legacy media_generator  
  ↓ on failure
PIL placeholder (last resort — never blocks pipeline)
```

**Videos:**
```
GeminiGen (Grok-3, 480p portrait)
  ↓ on failure
BytePlus (Seedance T2V)
```

---

## When to Use

- Running the full daily content pipeline (`--pipeline`)
- Running a specific phase only (`--phase research`, `--phase schedule`, etc.)
- Checking pipeline status after a run (`--status`)
- Creating Paperclip tracking issues for a run (`--paperclip-issues`)
- Debugging a broken phase in isolation

---

## When NOT to Use

- ❌ Direct PostBridge posting → use `autopilot_affiliate_engine/auto_postbridge_robust_v2.py`
- ❌ Generating images only → use `skills/nano-banana-pro/scripts/generate_image.py`
- ❌ Research only → use `autopilot_affiliate_engine/research_agent.py`
- ❌ Revenue tracking only → use `autopilot_affiliate_engine/revenue_tracker.py`
- ❌ Storyboard only → use `content/content-generator/scripts/storyboard.py`

---

## Quick Reference

```bash
# Full daily pipeline (morning run)
python3 orchestrator.py --pipeline

# Single phase (independently runnable)
python3 orchestrator.py --phase research
python3 orchestrator.py --phase plan
python3 orchestrator.py --phase script
python3 orchestrator.py --phase create
python3 orchestrator.py --phase review
python3 orchestrator.py --phase schedule
python3 orchestrator.py --phase post
python3 orchestrator.py --phase engage
python3 orchestrator.py --phase analyze
python3 orchestrator.py --phase optimize
python3 orchestrator.py --phase repurpose
python3 orchestrator.py --phase scale

# Status check
python3 orchestrator.py --status

# Seed Paperclip issues without running pipeline
python3 orchestrator.py --paperclip-issues

# Custom config
python3 orchestrator.py --pipeline --config /path/to/custom_config.json
```

---

## The 12 Phases

| # | Phase | Delegates To | New Code? |
|---|-------|-------------|-----------|
| 1 | RESEARCH | `autopilot_affiliate_engine/research_agent.py` + `viral_research_system.py` | No |
| 2 | PLAN | Engine weekly plan + config products | Thin logic only |
| 3 | SCRIPT | `content-generator/scripts/storyboard.py` + `modules/persona_manager.py` | No |
| 4 | CREATE | `skills/nano-banana-pro/scripts/generate_image.py` | No |
| 5 | REVIEW | `content-generator/scripts/quality_gate.py` | No |
| 6 | SCHEDULE | `autopilot_affiliate_engine/auto_postbridge_robust_v2.py` | No |
| 7 | POST | PostBridge `/post-results` API + retry via robust_v2 | No |
| 8 | ENGAGE | `modules/comment_manager.py` | **Yes — new** |
| 9 | ANALYZE | `evening_report.py` + `revenue_tracker.py` + PostBridge analytics | No |
| 10 | OPTIMIZE | Engagement rate calc + `revenue_tracker_REAL.py` | Thin logic only |
| 11 | REPURPOSE | `skills/auto-clipper/scripts/auto_clipper.py` | No |
| 12 | SCALE | `modules/engagement_engine.py` | **Yes — new** |

---

## Cron Setup

```bash
# Add to crontab (crontab -e)
# Morning pipeline — 08:00 WIB
0 8 * * * cd /home/openclaw/.openclaw/workspace/skills/content-kingdom && python3 orchestrator.py --pipeline >> logs/cron.log 2>&1

# Evening analysis — 20:00 WIB
0 20 * * * cd /home/openclaw/.openclaw/workspace/skills/content-kingdom && python3 orchestrator.py --phase analyze >> logs/cron.log 2>&1

# Engagement check — every 2 hours
0 */2 * * * cd /home/openclaw/.openclaw/workspace/skills/content-kingdom && python3 orchestrator.py --phase engage >> logs/cron.log 2>&1
```

---

## Configuration

Edit `config.json` to change:

| Key | Purpose | Example |
|-----|---------|---------|
| `products` | Products to promote (hooks, prices) | Add new LYNK product |
| `personas` | Brand voices (JENDRALBOT, BerkahKarya) | Add new persona |
| `platforms` | Enable/disable platforms | `"youtube": {"enabled": true}` |
| `schedule` | Posting times per platform | `"tiktok": ["07:00", "19:00"]` |
| `quality_gates` | Review pass/fail thresholds | `"min_caption_length": 80` |
| `scoring_weights` | Engagement scoring for scale phase | `"shares": 10.0` |
| `winner_thresholds` | Min score to be a "winner" | `"tiktok": 2000` |

**Do NOT duplicate** values already in `autopilot_affiliate_engine/config.py` — they're merged at runtime.

---

## Paperclip Integration

Each pipeline run creates:
- 1 parent issue: `Content Kingdom — YYYY-MM-DD`
- 12 sub-issues: one per phase
- Status auto-updates as phases complete (`todo → done` or `blocked`)

Paperclip server must be running at `http://localhost:3100`.

---

## Adding a New Phase

1. Write a `_phase_newphase(cfg, **kwargs) -> dict` function in `orchestrator.py`
2. Add entry to `PHASES` dict: `"newphase": {"fn": _phase_newphase, "label": "Phase 13: NEWPHASE", "deps": [...]}`
3. Done. No other changes needed (Open/Closed principle).

---

## Adding a New Module

If the new phase needs a real class:

```python
# modules/my_new_module.py
from base_module import BaseModule

class MyNewModule(BaseModule):
    @property
    def name(self) -> str:
        return "my_phase"

    def _execute(self, **kwargs) -> dict:
        # single responsibility: do ONE thing
        return {"result": "done"}
```

Instantiate in the phase function, call `module.run()`.

---

## Common Mistakes

| ❌ Wrong | ✅ Right |
|---------|---------|
| Creating new PostBridge wrapper | Import/subprocess `auto_postbridge_robust_v2.py` |
| Duplicating product list in config | Add products only to `config.json`, merge from engine at runtime |
| Running orchestrator as a library import | Use `--phase` CLI or instantiate `ContentKingdomOrchestrator` |
| Editing phase logic inside `run_phase()` | Edit the `_phase_*()` function, not the coordinator |
| Adding config to `orchestrator.py` directly | All config in `config.json` — orchestrator reads it |

---

## Dependencies

**Python stdlib only + requests:**
```bash
pip install requests
```

**External scripts (must exist):**
- `autopilot_affiliate_engine/research_agent.py`
- `autopilot_affiliate_engine/auto_postbridge_robust_v2.py`
- `autopilot_affiliate_engine/evening_report.py`
- `autopilot_affiliate_engine/revenue_tracker.py`
- `content/content-generator/scripts/storyboard.py`
- `content/content-generator/scripts/quality_gate.py`
- `skills/nano-banana-pro/scripts/generate_image.py` *(optional — CREATE fallback chain)*
- `skills/auto-clipper/scripts/auto_clipper.py` *(optional — REPURPOSE phase degrades gracefully)*

**v2.0 additions:**
- `workspace/config/geminigen_api.json` — `{"api_key": "YOUR_KEY"}` *(required for GeminiGen primary provider)*
- `curl` — CLI dependency for GeminiGen API calls (already available system-wide)

---

## Example Output

```json
{
  "run_id": "run_20260313_080000",
  "date": "2026-03-13",
  "phases": {
    "research": {"status": "success", "data": {"sources": ["research_agent", "viral_research_system"]}},
    "plan":     {"status": "success", "data": {"product_focus": "jendralbot_bundle", "platforms": ["tiktok", "instagram"]}},
    "script":   {"status": "success", "data": {"scripts_generated": 6}},
    "schedule": {"status": "success", "data": {"queue_file": "...postbridge_queue_jendralbot.json"}},
    "engage":   {"status": "success", "data": {"replies_queued": 4, "dm_leads": 2}},
    "scale":    {"status": "success", "data": {"winners": 3, "top_3": [...]}}
  }
}
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
