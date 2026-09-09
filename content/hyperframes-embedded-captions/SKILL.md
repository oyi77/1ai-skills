---
name: hyperframes-embedded-captions
description: "Add captions/subtitles to talking-head or launch videos using HyperFrames. Use when the user wants embedded captions, verbatim caption rails, or cinematic text behind the subject. Covers the drop/rail/embed caption model, the overlay law (captions are NOT a reserved band), matte occlusion for embedded climaxes, and word-timestamp alignment from TTS output."
domain: "content-creation"
tags:
  - hyperframes
  - captions
  - subtitles
  - talking-head
  - overlay
  - accessibility
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
---

# HyperFrames — Embedded Captions

Add captions/subtitles to talking-head or launch videos. The caption model (drop/rail/embed) and the overlay law (captions are NOT a reserved band).

## When to Use

- User wants **captions/subtitles** on a talking-head video
- User wants a **verbatim caption rail** (standard lower-third)
- User wants **cinematic embedded text** behind the subject (the climax beat)
- User wants to **add accessibility** to a video
- User wants to **burn in captions** for social media (no subtitle track)

## When NOT to Use

- User wants a full video workflow (use `hyperframes-product-launch-video`)
- User wants a full explainer (use `hyperframes-faceless-explainer`)
- User wants captions as a sidecar file (SRT/VTT) — this skill burns them in

## The Caption Model — Drop / Rail / Embed

| | What | How it's shown |
|---|------|----------------|
| **drop** | filler — um/uh, stutters | not shown |
| **rail** | the default — ordinary spoken content | clean lower-third subtitle, in front |
| **embed** | a promoted peak — the headline beat | one big word behind the subject (matte occlusion) |

**The rail carries most of the text; embed is the scarce, earned peak** — ≤1 per beat, never two adjacent, spaced ≥ a beat apart.

## The Overlay Law

A caption line is composited ON TOP of the film as an overlay; it is NOT a reserved zone.

- **Center the composition on the TRUE vertical center** (y = H/2). Do not shift content up to "make room" for captions.
- Content may extend to the canvas bottom.
- Avoid parking critical small readable text (URL, legal line) in the bottom ~80px center span where the caption line sits.
- No machine keep-out gate — judge legibility visually.

## Workflow

### 1 · Generate voiceover + word timestamps

```bash
# Using TTS with word-level timestamps
node scripts/heygen-tts.mjs ./vo-spoken.txt -o voiceover.mp3 --words vo-words.json --voice <voice_id>
```

### 2 · Align captions to display tokens

```bash
node scripts/align-captions.mjs --tokens script-tokens.json --words vo-words.json --out captions.json
```

`captions.json` is the caption-rail input (display spelling, spoken timing).

### 3 · Build the caption rail

```javascript
const LINES = /* contents of captions.json */ [
  { id: 0, end: 2.74, w: [["This", 0.0], ["week,", 0.30], ...] },
  ...
];
```

### 4 · Verify caption presence

Sample 3-4 frames across the VO's spoken window and confirm the caption rail renders visible text on each. If any frame in a spoken interval is missing captions, the build ships uncaptioned — treat as a red gate.

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll center at 42% to leave room for captions" | True center (y = H/2) — captions are overlay |
| "I'll embed every word" | Embed is scarce — rail carries most text |
| "I'll skip word timestamps" | Audio is the clock — all beat times come from word timestamps |
| "I'll use phonetic spelling in captions" | Captions always render the display layer |
| "I'll guess the pronunciation" | Ask the user, then grow the lexicon |

## Verification

- [ ] Caption rail present on 3+ sampled frames
- [ ] Display spelling matches script (not phonetic)
- [ ] Word timestamps align with audio
- [ ] Composition centered on true center (y = H/2)
- [ ] No critical text in caption overlay zone
