---
name: hyperframes-changelog-video
description: "Turn a weekly changelog .md into a finished branded changelog video using HyperFrames. Use when the user provides a changelog/digest markdown and wants the weekly video, or says 'changelog video'. Self-contained — fonts, background, lexicon, and scripts ship in the skill. Produces square 1080, ~45-60s videos with animated brand mock-UIs."
domain: "content-creation"
tags:
  - hyperframes
  - changelog
  - video
  - branded-content
  - digest
  - weekly
  - mock-ui
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill turns a release changelog into a polished video composition using HyperFrames HTML-based rendering. Use it when a product update deserves a visual announcement — hero frames, key bullet callouts, and a background pattern. It produces an MP4 rendered from the changelog entries you feed it.


# HyperFrames — Changelog Video

Input: a changelog .md (themes + items). Output: a lint-clean, seam-gate-green HyperFrames project. Render only when asked.

## When to Use

- User provides a **changelog/digest markdown** and wants the weekly video
- User says **"changelog video"** or **"weekly digest video"**
- User wants a **branded video** with animated mock-UIs and voiceover

## When NOT to Use

- User wants a product launch (use `hyperframes-product-launch-video`)
- User wants a motion graphic (use `hyperframes-motion-graphics`)
- User wants a talking-head video (use `hyperframes-embedded-captions`)

## The Prime Directive: Visualize, Don't List

Every theme is illustrated by an **animated mock of the actual UI or a faithful analog** acting out the change in experience — never text bullets. Route every theme/item through the visualization registry BEFORE writing the script.

## Workflow

### 0 · Bootstrap from skill assets (non-negotiable)

```bash
mkdir -p project/assets/fonts
cp <SKILL_DIR>/assets/fonts/*.woff2 project/assets/fonts/
cp <SKILL_DIR>/assets/bgm.mp3 project/bgm.mp3
ffmpeg -y -stream_loop 15 -i <SKILL_DIR>/assets/bg-pattern.mp4 -t <TOTAL> \
  -vf "scale=1080:1080,fps=30,eq=saturation=0.72,drawbox=c=black@0.5:t=fill" \
  -an -c:v libx264 -crf 20 -pix_fmt yuv420p project/assets/bg-pattern-<TOTAL>s.mp4
cp <SKILL_DIR>/examples/master-skeleton.html project/index.html
```

Then read `references/build-spec.md` end-to-end — it defines the brand tokens.

### 1 · Parse + editorial cut

- Extract: week range, headline stats, themes, items
- **Budget: 45-60s total.** Title ≤2s, outro ≤3.5s, 4 themes ≈ 9-12s each
- Per theme keep ONE hero visualization + at most 3 spoken items
- Order themes by story: marquee feature → product surface → performance → reliability

### 2 · Visualization routing

For each theme, pick the surface from the visualization registry and write one line: `theme → surface → the 2-4 sequenced actions the mock performs, each tied to a script phrase`.

### 3 · Two-layer script (spoken vs display)

Write the script as token lines: conversational register, every technical term carrying a `spoken` phonetic form while `display` keeps standard spelling. Captions show `display`; the VO reads `spoken`.

### 4 · VO + word timestamps

```bash
node scripts/heygen-tts.mjs ./vo-spoken.txt -o voiceover.mp3 --words vo-words.json --voice <voice_id>
node scripts/align-captions.mjs --tokens script-tokens.json --words vo-words.json --out captions.json
```

**Word-timings are a hard gate.** Before moving on, verify `vo-words.json` is non-empty and has a `words: [...]` array with `start`/`end` per word.

### 5 · Build

Follow `references/build-spec.md` exactly: brand tokens + fonts + the animated background encode + scene scaffold + chrome + caption rail. Then the doctrine order: vector ledger → seam-stamp → internal beats on VO words → seam-gate verify.

**Captions are non-optional.** Populate the `LINES` array from `captions.json` before proceeding.

### 6 · Gates (all green before presenting)

1. `hyperframes check` — 0 errors
2. `seam-gate.mjs verify` — 0 fail
3. Restart preview server, spot-check 3-4 beats
4. Do NOT render unless the user asks
5. **Caption presence gate** — sample 3-4 frames, confirm caption rail visible

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "Bullet-point slides for UI changes" | Mock the surface acting out the change |
| "Fake UI for un-representable items" | Honest checklist scene |
| "Plain 'JSON' in the TTS text" | Lexicon spoken forms; display stays standard |
| "Guessing pronunciation" | Ask, then grow the lexicon |
| "Speaking every changelog item" | ≤3 per theme; digest link carries the rest |
| "Green accents everywhere" | One green moment per scene |
| "Starting from a prior video's index.html" | Copy master-skeleton.html, always |
| "Empty LINES array is fine" | Empty LINES = uncaptioned ship = re-do the run |

## Verification

- [ ] `hyperframes check` passes with 0 errors
- [ ] `seam-gate.mjs verify` passes with 0 fail
- [ ] Caption rail visible on 3+ sampled frames
- [ ] Word timestamps align with audio
- [ ] Brand tokens match build-spec.md
- [ ] Only rendered when user explicitly asks
