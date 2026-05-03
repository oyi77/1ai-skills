---
name: video-frames
description: Extract frames or short clips from videos using ffmpeg.
homepage: https://ffmpeg.org
metadata: {"clawdbot":{"emoji":"🎞️","requires":{"bins":["ffmpeg"]},"install":[{"id":"brew","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (brew)"}]}}
---
persona:
  name: "Domain Expert"
  title: "Master of Video Frames"
  expertise: ['Content Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



> [![Tip Me](https://www.tip.md/badge.svg)](https://www.tip.md/oyi77) — If this skill saves you time, tip: **https://www.tip.md/oyi77**

# Video Frames (ffmpeg)

Extract a single frame from a video, or create quick thumbnails for inspection.

## Quick start

First frame:

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --out /tmp/frame.jpg
```

At a timestamp:

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --time 00:00:10 --out /tmp/frame-10s.jpg
```

## Notes

- Prefer `--time` for “what is happening around here?”.
- Use a `.jpg` for quick share; use `.png` for crisp UI frames.
