---
name: hyperframes-faceless-explainer
description: "Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video using HyperFrames. Use when the user wants a topic explainer, concept breakdown, how-to, or listicle with no product/website to capture. Every visual is invented per scene (typography, abstract graphics, diagrams, data-viz). Not a video built from a website (use hyperframes-product-launch-video)."
domain: "content-creation"
tags:
  - hyperframes
  - explainer
  - faceless
  - education
  - concept
  - how-to
  - data-viz
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill builds faceless explainer videos — narration-driven, no on-camera presenter — as HyperFrames compositions. Use it for product or concept explainers where voiceover plus visuals carry the message. It renders the final MP4 from a script you provide.


# HyperFrames — Faceless Explainer

Turn arbitrary text into an explainer video: pick a design system, plan a teaching story, and build it frame by frame. **Faceless** means every visual is invented — there is no capture step and no real asset inventory.

## When to Use

- User wants a **topic explainer** from an article, notes, or brief
- User wants a **concept breakdown** (how something works)
- User wants a **how-to** or **tutorial** (no screen capture)
- User wants a **listicle** or **animated list**
- User wants a **data-driven explainer** (charts, stats, comparisons)

## When NOT to Use

- User wants a product launch (use `hyperframes-product-launch-video`)
- User wants a talking-head video (use `hyperframes-embedded-captions`)
- User wants a motion graphic (use `hyperframes-motion-graphics`)
- User wants to capture a website (use `hyperframes-product-launch-video`)

## Workflow

### 0 · Setup

```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank --skill=faceless-explainer
```

Write `BRIEF.md` immediately after init (never before — `init` refuses a non-empty directory). Record preferences with `node <MEDIA_DIR>/scripts/prefs.mjs record --hyperframes .`.

### 1 · Brief (no capture)

Save the user's full input verbatim:

- `capture/extracted/visible-text.txt` — the full article/notes/topic/brief
- `capture/extracted/tokens.json` — `{ "title": "", "description": "", "colors": [], "fonts": [] }`

**Do NOT run `npx hyperframes capture`** — there is no URL. Faceless visuals are invented downstream.

### 2 · Design System

Pick a frame preset whose look fits the topic, tone, and audience:

```bash
node <SKILL_DIR>/scripts/build-frame.mjs --preset <name> --hyperframes .
```

This copies the preset's `FRAME.md` → `frame.md` and remixes brand tokens. A faceless explainer usually has no brand colors/fonts → the script keeps the preset's own palette.

### 3 · Storyboard and Script

Turn the text into a frame-by-frame teaching plan. The video's sequence comes from **narrative design, not the input text's paragraph order** — reorder, merge, omit, compress.

Write `STORYBOARD.md` and (when narration is needed) `SCRIPT.md`. Each frame needs:
- `focal` / `roles` — the invented visual elements (hero word, diagram node, data-viz series)
- `blueprint` — the shot shape (from `hyperframes-animation/blueprints/`)
- `transition_in` — how the frame enters

### 3.1 · Audio

```bash
node <SKILL_DIR>/scripts/audio.mjs --script ./SCRIPT.md --storyboard ./STORYBOARD.md --hyperframes . --out ./audio_meta.json --voice <voice-id> &
```

Pipeline default voice: **Marcia (female)** on HeyGen / `am_michael` on Kokoro. BGM mood comes from the storyboard's `music:` field.

**Canonical silent marker:** `music: none` in STORYBOARD.md top YAML block AND no `SCRIPT.md` = fully silent project.

### 4 · Frame Visual Design

For every frame, write a **time-coded shot sequence**:
- Pick the frame's blueprint (or compose)
- Instantiate it with THIS frame's **invented** content
- Pace each Scene's reveal to the voiceover so the frame develops across its full duration

State layout and motion **inline** per Scene. Add one video-wide `## Video direction` block.

### 5 · Build Frames

Wait for Step 3.1 audio to finish. Then:

```bash
node <SKILL_DIR>/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md
node <SKILL_DIR>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes .
node <SKILL_DIR>/scripts/frame-packets.mjs --project "$PROJECT_DIR" --storyboard "$PROJECT_DIR/STORYBOARD.md"
```

Dispatch one sub-agent per frame. Each worker gets:
- `_role.md` (the frame-worker role)
- That frame's packet (exact storyboard block + blueprint body + cited rule recipes, inlined)

Workers write only `compositions/frames/NN-*.html`. They never edit `STORYBOARD.md`.

**Full-bleed backgrounds ride on a `class="clip"` layer, never the `#root`.** A frame's ground is its own full-duration background clip.

Build captions in the background and assemble the index:

```bash
node <SKILL_DIR>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json &
node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .
```

### 6 · Finalize

```bash
node <SKILL_DIR>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .
node <SKILL_DIR>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html
npx hyperframes lint
npx hyperframes check
npx hyperframes snapshot --at <frame-midpoints>
```

Render only after user approval:

```bash
npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll capture the article's website" | Faceless = no capture. Visuals are invented, not captured |
| "I'll use the text's paragraph order" | Narrative design decides sequence, not source order |
| "I'll skip the design system" | frame.md is the source of truth for color/type/layout |
| "I'll front-load all content then freeze" | Pace reveals to voiceover — frame develops across full duration |
| "I'll write one blueprint and reuse it" | Each frame picks its own blueprint based on content |
| "I'll skip audio and just use text" | Audio is the clock — all beat times come from word timestamps |
| "I'll add idle animations between reveals" | Every phase performs — staged reveals, camera with intent, or sequenced UI |
| "I'll center at 42% to leave room for captions" | Captions are overlay — center on true center (y = H/2) |

## Verification

- [ ] `hyperframes.json` and `BRIEF.md` exist
- [ ] `frame.md` exists from a named preset
- [ ] `STORYBOARD.md` exists with required narrative fields
- [ ] `SCRIPT.md` exists when narration is needed
- [ ] Audio job started or project marked silent
- [ ] Every frame has a time-coded shot sequence paced to voiceover
- [ ] Each frame names invented `focal` and/or `roles`
- [ ] `index.html` exists
- [ ] Captions built or explicitly skipped
- [ ] `lint` and `check` passed before render
- [ ] User approved at the review pause
