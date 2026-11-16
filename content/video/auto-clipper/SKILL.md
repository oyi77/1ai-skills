---
name: auto-clipper
description: Use when automatically clip long videos into short, engaging highlights for TikTok, Reels, and YouTube Shorts. Auto-detects scene changes, audio energy peaks, and transitions to create viral clips with professional quality.
domain: content
category: content
tags:
- auto
- clipper
- video
- shorts
- reels
- highlights
- viral
- video-editing
- ffmpeg
version: 1.0.0
author: oyi77
license: Apache-2.0
subdomain: video-production
type: content
---

# Auto Clipper — Auto-Generated Video Highlights

## When to Use

**Trigger phrases:**
- "clip this video" · "make shorts from this" · "turn this into TikTok"
- "auto clip" · "extract highlights" · "repurpose long video"
- "create Reels from" · "viral clips from" · "short-form from long-form"

**Use cases:**
- Convert podcast/webinar into multiple short clips
- Extract highlights from long YouTube videos
- Create TikTok/Reels from existing content
- Auto-detect engaging moments via scene + audio analysis
- Batch process multiple long videos into shorts

**When NOT to use:**
- When the content requires deep domain expertise you do not have
- For legal, medical, or financial advice content
- When real-time data is required (use live data feeds)

## Overview

Auto Clipper uses ffmpeg and Python to automatically detect engaging moments in long videos and generate professional short clips. Works with any video format ffmpeg supports.

## Workflow

1. **Define brief** — Set objectives, audience, and style guidelines
2. **Analyze video** — Detect scene changes and audio energy peaks
3. **Find engaging moments** — Combine visual and audio signals to identify highlights
4. **Extract clips** — Cut segments around identified moments
5. **Optimize & publish** — Apply quality filters and export for target platforms

## Quality Checklist

- [ ] Clip duration: 5-15 seconds (optimal for social platforms)
- [ ] Scene change at start/end of clip
- [ ] Audio peak at key moment
- [ ] No black frames or technical glitches
- [ ] Consistent visual style across clips
- [ ] Clear call-to-action or value proposition

## Tools

- ffmpeg (core engine)
- Python (for analysis logic)
- JSON (for configuration)
- ffmpeg-python (optional wrapper)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |

## Implementation Example

```bash
# Basic usage with default settings
python3 auto_clipper.py --input long_video.mp4 --output clips/

# Custom parameters
python3 auto_clipper.py \
  --input long_video.mp4 \
  --output clips/ \
  --min-duration 5 \
  --max-duration 15 \
  --scene-threshold 0.3 \
  --audio-threshold 0.7 \
  --fade-in 0.5 \
  --fade-out 0.5
```

## Technical Approach

1. **Scene Detection**: 
   ```bash
   ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep "pts_time"
   ```
   - `scene` filter detects visual cuts
   - `showinfo` provides timing metadata

2. **Audio Analysis**:
   ```bash
   ffmpeg -i input.mp4 -af "astats=reset=0:measure_perframe=1" -f null - 2>&1 | grep "stdburst"
   ```
   - Measures audio energy per frame
   - Identifies loud/quiet segments

3. **Clip Extraction**:
   ```bash
   ffmpeg -i input.mp4 -ss 00:00:05 -t 00:00:10 -c copy output.mp4
   ```
   - `-ss` = start time
   - `-t` = duration
   - `-c copy` = no re-encoding (fast)

4. **Beat-Snapped Cutting** (optional, requires librosa):
   - `librosa.beat.beat_track(tightness=400, units="time")` detects beats
   - Least-squares fit to an isochronous grid; residual ≤±15 ms = grid trustworthy
   - `--beat-align` snaps clip starts to nearest beat within 0.25 s
   - Falls back to scene-cut times if grid residual >30 ms or librosa unavailable

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--min-duration` | 5 | Minimum clip length (seconds) |
| `--max-duration` | 15 | Maximum clip length (seconds) |
| `--scene-threshold` | 0.3 | Scene change sensitivity (0.0-1.0) |
| `--audio-threshold` | 0.7 | Audio energy threshold (0.0-1.0) |
| `--fade-in` | 0.5 | Fade-in duration (seconds) |
| `--fade-out` | 0.5 | Fade-out duration (seconds) |
| `--quality` | 20 | CRF value for encoding (lower = better) |
| `--beat-align` | off | Snap clip starts to a trustworthy librosa beat grid |

## Verification Checklist

- [ ] All clips are 5-15 seconds
- [ ] Each clip starts/ends at scene change
- [ ] Audio peaks at key moments
- [ ] With `--beat-align`: grid residual ≤30 ms; cuts snapped within 0.25 s
- [ ] No black frames or encoding artifacts
- [ ] Consistent aspect ratio and quality
- [ ] Output files verified with ffprobe
- [ ] Contact sheet generated for QA

## Dependencies

- ffmpeg ≥ 4.0 (must be in PATH)
- Python 3.7+
- numpy, scipy (optional for advanced analysis)
- librosa + numpy (required only with `--beat-align`)
