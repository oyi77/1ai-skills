---
name: hyperframes-general-video
description: "The fallback HyperFrames workflow for anything that doesn't fit other skills — longer multi-scene pieces, brand/sizzle reels, title cards, static loops, freeform compositions. Input- and length-agnostic. Also the home of companion mode (co-create with the full toolbox). Use when no other HyperFrames skill matches, or when the user wants a freeform video."
domain: "content-creation"
tags:
  - hyperframes
  - general-video
  - freeform
  - sizzle-reel
  - title-card
  - fallback
  - companion-mode
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill is the general-purpose HyperFrames video composition path: any HTML/CSS layout with timed clips and animations rendered to a deterministic MP4. Use it when a video fits no specialized template but is still code-defined. It handles the full compose → render loop.


# HyperFrames — General Video (Fallback)

The fallback for anything that doesn't fit other skills. Longer multi-scene pieces, brand/sizzle reels, title cards, static loops, freeform compositions. Input- and length-agnostic.

## When to Use

- No other HyperFrames skill matches the request
- User wants a **brand/sizzle reel** (montage of best moments)
- User wants a **title card** (show open, segment bumper)
- User wants a **static loop** (ambient background, waiting screen)
- User wants a **freeform composition** (experimental, artistic)
- User wants **companion mode** (co-create interactively with the agent)

## When NOT to Use

- Request matches a specific skill (product-launch, motion-graphics, explainer, etc.) — use that instead
- User wants a presentation (use `hyperframes-slideshow`)
- User wants captions only (use `hyperframes-embedded-captions`)

## Workflow

### 1 · Clarify the shape

Ask (max 2 questions):
1. **Duration:** "How long? (under 10s, 30-60s, 1-3 min, longer)"
2. **Style:** "What vibe? (bold, minimal, cinematic, playful, corporate)"

### 2 · Plan loosely

Unlike strict workflows, general video allows flexible structure:
- **Sizzle reel:** 8-12 clips, 2-3s each, music-driven cuts
- **Title card:** single hero moment, 3-5s, one animation
- **Static loop:** seamless 5-10s loop, no beginning/end
- **Freeform:** follow the user's description beat by beat

### 3 · Build the composition

Standard composition contract applies:

```html
<div id="main" data-composition-id="general"
     data-start="0" data-duration="30" data-width="1920" data-height="1080" data-fps="30">
  <!-- Scenes here -->
</div>
```

### 4 · Companion mode (optional)

For interactive co-creation:
1. Build a rough first pass
2. Preview with the user
3. Iterate on specific beats ("make the title bigger", "slow down the second scene")
4. Re-render until approved

### 5 · Render

```bash
npx hyperframes render --output general-video.mp4
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll skip planning because it's freeform" | Even freeform needs a beat list — 3-5 beats minimum |
| "I'll use this instead of learning the right skill" | If a specific skill matches, use it — this is the fallback |
| "I'll make it 10 minutes long" | Longer isn't better — tighten to the essential beats |

## Verification

- [ ] No specific skill matches better (checked router first)
- [ ] Beat list written (3+ beats)
- [ ] Composition follows standard contract
- [ ] Output matches requested duration and style

## Sub-Skills & Specialized Playbooks
| Sub-Skill | Trigger / Kasus Penggunaan | Berkas Referensi |
| :--- | :--- | :--- |
| `hyperframes-changelog-video` | Turn a weekly changelog .md into a finished branded changelog video using HyperFrames. Use w... | [SKILL.md](../hyperframes-changelog-video/SKILL.md) |
| `hyperframes-cut-the-curve` | Use when authoring any transition, text-beat handoff, or kinetic text entry in HyperFrames v... | [SKILL.md](../hyperframes-cut-the-curve/SKILL.md) |
| `hyperframes-embedded-captions` | Add captions/subtitles to talking-head or launch videos using HyperFrames. Use when the user... | [SKILL.md](../hyperframes-embedded-captions/SKILL.md) |
| `hyperframes-faceless-explainer` | Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video ... | [SKILL.md](../hyperframes-faceless-explainer/SKILL.md) |
| `hyperframes-motion-graphics` | Create short, unnarrated, design-led motion graphics (~under 10s) using HyperFrames. Use whe... | [SKILL.md](../hyperframes-motion-graphics/SKILL.md) |
| `hyperframes-music-to-video` | Turn a music track into a beat-synced HyperFrames video — lyric, slideshow, or kinetic promo... | [SKILL.md](../hyperframes-music-to-video/SKILL.md) |
| `hyperframes-oversized-cursor` | House-style oversized macOS cursor technique for HyperFrames videos. Use when a scene involv... | [SKILL.md](../hyperframes-oversized-cursor/SKILL.md) |
| `hyperframes-pr-to-video` | Turn a GitHub pull request into a changelog, feature-reveal, fix, or refactor explainer vide... | [SKILL.md](../hyperframes-pr-to-video/SKILL.md) |
| `hyperframes-product-launch-video` | Create product launch videos from a URL, brief, or script using HyperFrames (HTML→MP4). Use ... | [SKILL.md](../hyperframes-product-launch-video/SKILL.md) |
| `hyperframes-seam-craft` | Render-correctness doctrine for scene-to-scene seams in HyperFrames videos. Use when assembl... | [SKILL.md](../hyperframes-seam-craft/SKILL.md) |
| `hyperframes-slideshow` | Build a presentation, pitch deck, or interactive deck using HyperFrames. Use when the user w... | [SKILL.md](../hyperframes-slideshow/SKILL.md) |
| `hyperframes-talking-head-recut` | Package an existing talking-head / interview / podcast video with timed, designed graphic ov... | [SKILL.md](../hyperframes-talking-head-recut/SKILL.md) |
