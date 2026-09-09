---
name: hyperframes-motion-graphics
description: "Create short, unnarrated, design-led motion graphics (~under 10s) using HyperFrames. Use when the user wants kinetic type, stat/chart hits, logo stings, lower-thirds, animated tweets/headlines, or transparent overlay motion graphics. MP4 or transparent overlay output. Teaches seek-safe keyframe authoring and the 2-3 transition budget rule."
domain: "content-creation"
tags:
  - hyperframes
  - motion-graphics
  - animation
  - kinetic-type
  - lower-third
  - logo-sting
  - transparent-overlay
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill produces motion-graphics sequences — animated titles, transitions, and kinetic elements — as HyperFrames compositions. Use it for brand stings, intro cards, or animated data callouts. It renders frame-accurate MP4 output from the HTML/CSS animation timeline.


# HyperFrames — Motion Graphics

Short, unnarrated, design-led motion graphics (~under 10s). Kinetic type, stat hits, logo stings, lower-thirds, animated headlines. MP4 or transparent overlay.

## When to Use

- User wants a **kinetic type** animation (text that moves with energy)
- User wants a **stat/chart hit** (animated number or data visualization)
- User wants a **logo sting** (short brand animation, <5s)
- User wants a **lower-third** (news-style name/title overlay)
- User wants an **animated tweet/headline** (social media motion graphic)
- User wants a **transparent overlay** (video overlay with alpha channel)

## When NOT to Use

- User wants a full video with narration (use `hyperframes-product-launch-video`)
- User wants an explainer with voiceover (use `hyperframes-faceless-explainer`)
- User wants a talking-head video (use `hyperframes-embedded-captions`)
- User wants a product showcase (use `hyperframes-product-launch-video`)

## Workflow

### 1 · Plan (≤10s total)

- Single concept: one stat, one logo, one headline
- Budget: entry ≈ 1-2s, hold ≈ 5-7s, exit ≈ 1-2s
- Pick a transition vocabulary: only 2-3 inter-scene transitions per film (repeat them)

### 2 · Author seek-safe keyframes

All animations must be **seekable** — same frame at same time, every render. No wall-clock dependencies.

**GSAP (recommended):**

```javascript
const tl = gsap.timeline({ paused: true });
tl.fromTo("#stat-number", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.8, ease: "back.out(1.7)" }, 0);
tl.to("#stat-number", { scale: 1.1, duration: 0.3, ease: "power2.out" }, 1.0);
window.__timelines = { main: tl };
```

**CSS keyframes:**

```css
@keyframes countUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.stat { animation: countUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
```

### 3 · Stage ground

`#root` must be opaque (`background: var(--canvas-deep, var(--canvas, #000))`) — the mid-window cut opens a summed-opacity < 1 window that flashes white otherwise.

### 4 · Transitions (the 2-3 budget)

Default boundary: **cut-the-curve** in the current's direction (LEFT). Use only 2-3 transition types per film.

| Technique | Scope | Axis | Travel |
|-----------|-------|------|--------|
| Cut the Curve | Between scenes | X/Y | ~12% frame (±230px at 1920) |
| Zoom-Through | Within-scene text swap | Z (toward) | scale 1→1.2 then 0.75→1 |
| Inverse Zoom | Arrival/payoff | Z (away) | scale 1→0.8 then 1.25→1 |
| Waterfall Cut | Text-to-text seam | X, per-word | ±230px stagger |

### 5 · Render

```bash
npx hyperframes render --output motion-gif.mp4 --fps 30
```

For transparent overlay:
```bash
npx hyperframes render --output overlay.mp4 --format prores_4444
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll use 5 different transitions" | Budget is 2-3 per film — repetition creates cohesion |
| "I'll add bounce/elastic to everything" | Forbidden eases: bounce.out / elastic.out as sustained motion |
| "I'll start each element from rest" | Entry must be mid-flight (≥50% through notional path) |
| "I'll use idle animations to fill time" | Every phase performs — staged reveals, camera with intent, or sequenced UI |
| "I'll center at 42% to leave room for captions" | Captions are overlay — center on true center (y = H/2) |
| "I'll use a white background for transparency" | Transparent overlay needs alpha channel, not white |

## Verification

- [ ] Total duration ≤ 10s
- [ ] Only 2-3 transition types used
- [ ] All animations are seekable (deterministic)
- [ ] Stage ground is opaque
- [ ] No idle wobble — every phase performs
- [ ] Text-scale blur ≤ 10px (not 20px)
- [ ] Output format matches use case (MP4 vs ProRes 4444)
