---
name: hyperframes-music-to-video
description: "Turn a music track into a beat-synced HyperFrames video — lyric, slideshow, or kinetic promo. Use when the user provides an audio file, a video to pull audio from, or a mood brief for generated music. Music drives pacing. Teaches beat-map extraction, section-based scene planning, and audio-reactive visuals."
domain: "content-creation"
tags:
  - hyperframes
  - music
  - beat-sync
  - lyric-video
  - slideshow
  - kinetic-promo
  - audio-reactive
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill generates a video that visualizes audio — waveform or beat-synced elements — from a music file using a HyperFrames composition. Use it when a track needs a companion visual without manual editing. It renders the final MP4 from the composition.


# HyperFrames — Music to Video

A music track → a beat-synced video. Lyric, slideshow, or kinetic promo. Music drives pacing.

## When to Use

- User provides an **audio file** and wants a video for it
- User provides a **video to pull audio from** (music extraction)
- User provides a **mood brief** ("upbeat lofi for product launch")
- User wants a **lyric video** (words synced to vocals)
- User wants a **beat-synced slideshow** (images changing on beats)
- User wants a **kinetic promo** (typography pulsing with the track)

## When NOT to Use

- User wants a product launch from a URL (use `hyperframes-product-launch-video`)
- User wants a talking-head video (use `hyperframes-talking-head-recut`)
- User wants narration/voiceover (use `hyperframes-faceless-explainer`)
- No music involved (use `hyperframes-motion-graphics`)

## Workflow

### 1 · Resolve the audio

Three input paths:
- **Audio file provided:** probe with `ffprobe` for duration, BPM (estimate or detect)
- **Video provided:** extract with `ffmpeg -i input.mp4 -vn -acodec libmp3lame audio.mp3`
- **Mood brief:** generate via TTS/music model, or pick from catalog BGM

### 2 · Map the beat structure

Listen (or analyze) for sections:
- **Intro** (0-8s) → title/establishing
- **Verse** → content/slideshow
- **Chorus/Drop** → climax/kinetic peak
- **Outro** → CTA/fade

Write a beat map: `[{ time: 0, section: "intro" }, { time: 8, section: "verse" }, ...]`

### 3 · Plan scenes to sections

Each musical section gets a visual treatment:
- **Intro:** slow fade-in, minimal motion
- **Verse:** steady reveals, one element per 2-4 beats
- **Chorus:** maximum energy — scale bursts, color shifts, rapid cuts
- **Bridge:** visual breather — static hold or slow pan
- **Outro:** resolve to end card

### 4 · Build the composition

Anchor every animation start time to the beat map. Use CSS keyframes or GSAP with absolute times matching section boundaries.

```html
<div id="main" data-composition-id="music-video"
     data-start="0" data-duration="60" data-width="1080" data-height="1920" data-fps="30">
  <div class="clip chorus-hit" data-start="32" data-duration="8" data-track-index="1">
    <h1 class="lyric-line">CHORUS LYRIC HERE</h1>
  </div>
  <audio data-start="0" data-duration="60" src="./track.mp3"></audio>
</div>
```

### 5 · Render

```bash
npx hyperframes render --output music-video.mp4
```

Verify sync: sample frames at section boundaries, confirm visual changes land on beats (±2 frames tolerance).

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll eyeball the timing" | Beat map first — every scene anchored to section times |
| "I'll use the same energy throughout" | Chorus hits harder than verse — dynamics matter |
| "I'll skip the audio probe" | Duration/BPM mismatch breaks the whole render |
| "I'll animate to wall-clock" | All animations seekable — absolute times in composition |

## Verification

- [ ] Audio resolved (file, extracted, or generated)
- [ ] Beat map written with section boundaries
- [ ] Each section has a distinct visual treatment
- [ ] Animation times match beat map (±2 frames)
- [ ] Output duration matches audio duration
- [ ] Chorus/climax is visually distinct from verse
