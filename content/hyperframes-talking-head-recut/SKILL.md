---
name: hyperframes-talking-head-recut
description: "Package an existing talking-head / interview / podcast video with timed, designed graphic overlays using HyperFrames. Use when the user wants kinetic titles, lower-thirds, data callouts, pull-quotes, side panels, or picture-in-picture on top of existing footage. The clip plays untouched underneath. Not plain subtitles (use hyperframes-embedded-captions)."
domain: "content-creation"
tags:
  - hyperframes
  - talking-head
  - graphic-overlays
  - lower-thirds
  - data-callouts
  - video-packaging
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
---

# HyperFrames — Talking Head Recut

Layer timed, designed graphic cards onto an existing talking-head video — titles, lower-thirds, data callouts, quotes, side panels, PiP — synced to the transcript. The clip plays untouched underneath.

## When to Use

- User wants **graphic overlays** on a talking-head video
- User wants **lower-thirds** with names/titles
- User wants **data callouts** synced to spoken numbers
- User wants **pull-quotes** or **side panels**
- User wants **picture-in-picture** layout
- User says "package my video" or "add graphics to my interview"

## When NOT to Use

- User wants plain subtitles/captions (use `hyperframes-embedded-captions`)
- User wants to build a video from scratch (use `hyperframes-product-launch-video`)
- User wants a faceless explainer (use `hyperframes-faceless-explainer`)
- User wants to edit the footage itself (this skill leaves footage untouched)

## Workflow

### 1 · Check environment

```bash
npx hyperframes doctor          # ffmpeg, headless browser, render deps
ls "<SKILL_DIR>/assets/fonts" "<SKILL_DIR>/assets/vendor/gsap.min.js"
```

Required: `ffmpeg` / `ffprobe` (system), bundled fonts + GSAP (in skill assets).

### 2 · Create work directory

```bash
VIDEO_PATH="/absolute/path/input.mp4"
WORK_DIR="videos/$(basename "$VIDEO_PATH" | sed 's/\.[^.]*$//')"
mkdir -p "$WORK_DIR"
```

### 3 · Extract audio and metadata

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate \
  -show_entries format=duration -of json "$VIDEO_PATH" > "$WORK_DIR/metadata.json"

ffmpeg -y -i "$VIDEO_PATH" -vn -acodec libmp3lame -q:a 2 "$WORK_DIR/audio.mp3"
```

### 4 · Transcribe (local Whisper)

```bash
npx hyperframes transcribe "$WORK_DIR/audio.mp3" -d "$WORK_DIR" --json --model small.en
```

Writes word-level `transcript.json` (word `text` + `start` / `end` timestamps). No API key needed.

### 5 · Correct transcript

Read `transcript.json` and fix obvious ASR errors (homophones, product names, technical terms). Preserve `start` / `end` timestamps.

### 6 · Draft storyboard

Design cards directly from the transcript. Each card has:

| Field | Purpose |
|-------|---------|
| `id` | stable id for HTML/GSAP selectors |
| `intent` | natural-language description |
| `startSec` / `endSec` | timing in seconds |
| `accentIndex` | which of 5 theme accent colors |
| `zone` | canvas position (fullscreen, lower-third, side-panel, whiteboard-area, video-overlay) |
| `contentHints` | kicker/title/detail/data/quote |

**Card count formula:**

```
secPerCard = basePace × densityMultiplier
cardCount  = max(5, round(videoDurationSec / secPerCard))
```

| Video duration | Base pace |
|----------------|-----------|
| < 60s | 6-8s |
| 60s - 3 min | 8-12s |
| 3 - 10 min | 12-20s |
| 10 - 30 min | 20-35s |
| > 30 min | 30-60s |

| Density signal | Multiplier |
|----------------|------------|
| High (many numbers, staccato) | × 0.7 |
| Medium (mixed) | × 1.0 |
| Low (one extended story) | × 1.5 |

### 7 · Decide render strategy

Ask the user to pick:
1. **Output ratio:** 16:9 (wide source), 9:16 (tall source), 4:5 (near-square)
2. **Layout:** standard, side-panel, picture-in-picture
3. **Style:** noir, editorial, bold-poster, blue-professional, etc.
4. **Card density:** auto (from formula), sparse, dense

### 8 · Design cards

Write each card's HTML directly in the conversation. Card zones:

| Zone | Bounds | Use for |
|------|--------|---------|
| fullscreen | whole canvas | hero moments, big numbers |
| lower-third | bottom 30% | annotation over visible video |
| side-panel | right 42% (landscape) / bottom 40% (portrait) | data side |
| whiteboard-area | inset 40px margin | dense data / annotated content |
| video-overlay | full canvas, mostly-transparent | annotation overlays |

### 9 · Assemble composition

Build `index.html` with:
- Video layer: `<video>` element with the source footage
- Card layers: absolutely-positioned divs with `data-start` / `data-duration`
- GSAP timeline: animating card entry/exit synced to transcript timestamps

```html
<div id="video-wrap">
  <video src="input.mp4" muted></video>
</div>
<div class="card" id="card-01" data-start="0.5" data-duration="12.5" data-track-index="1">
  <div class="card-kicker">AN HONEST QUESTION</div>
  <div class="card-title">The soul-searching question at 11 PM</div>
</div>
```

### 10 · Render

```bash
npx hyperframes render --output output.mp4
```

Verify the output:
```bash
ffmpeg -ss 10 -i output.mp4 -frames:v 1 frame-10s.png
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll add a card every 2 seconds" | Use the formula — density matters, not arbitrary frequency |
| "I'll skip transcription and guess timings" | Transcript word timestamps are the clock — cards must sync to speech |
| "I'll use a fixed card structure" | Cards emerge from what the transcript actually says |
| "I'll edit the footage to match the cards" | Footage plays untouched — cards overlay, don't replace |
| "I'll center content at 42% to avoid overlap" | Cards are positioned in zones — video fills the frame |
| "I'll add an outro automatically" | No fixed brand outro — design one only if the user asks |

## Verification

- [ ] `hyperframes doctor` passes
- [ ] `transcript.json` has word-level timestamps
- [ ] Card count ≥ 5 (floor)
- [ ] Each card has `startSec` < `endSec`
- [ ] Card timings clamped to video duration
- [ ] Output MP4 has visible synced overlays on 3+ sampled frames
- [ ] Footage plays untouched underneath
