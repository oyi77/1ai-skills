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
---

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
