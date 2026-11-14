---
name: clay-art-video-generator
description: Use when creating claymation / plasticine stop-motion style short-form video (TikTok, Reels, Shorts) — frame-by-frame workflow using Blender or Stop Motion Studio, covering sculpt, rig, shoot, and export for 9:16 vertical.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- clay
- claymation
- stop-motion
- video
- tiktok
- reels
- shorts
- animation
version: 1.0.0
category: content
---

# Clay Art Video Generator

## When to Use

**Trigger phrases:**
- "clay art video" · "plasticine animation" · "stop motion diorama"
- "claymation" · "clay style video" · "plasticine video"
- "3D clay look" · "stop motion style" · "diorama video"

**Use cases:**
- 15–30 s TikTok/Reels/Shorts with clay/plasticine aesthetic
- Product showcase in stop-motion (snack, toy, food)
- Story-mode shorts with diorama sets
- Educational clay-animated explainers (anatomy, mechanics)

## When NOT to Use

- Talking-head or screen-recorded explainers — use `hyperframes-talking-head-recut` or `hyperframes-faceless-explainer`
- Legal, medical, or financial advice content
- Videos >60 s — stop-motion is slow; use 2D motion graphics instead
- Live-action footage — use `auto-clipper` or `video-editor`

## Overview

Clay animation is **frame-by-frame**: physically move a plasticine puppet 1–2 mm, shoot a frame, repeat. At 12 fps (industry standard for stop-motion), a 15 s clip = **180 frames**. Each frame takes 30–90 s to set up and shoot, so budget 2–5 hours per 15 s clip. For 3D-rendered clay look without physical sculpting, use Blender's **Sculpt** mode + **Cycles** with a subsurface-scattering material (see §3D Clay Look).

## Workflow

### 1. Pre-production (30 min)

1. Write a **shot list** — one line per beat, ≤10 beats for 15 s.
2. Storyboard each beat as a single frame (rough sketch, phone photo of clay is fine).
3. Pick aspect ratio: **9:16 vertical** for TikTok/Reels/Shorts, 1080×1920 px, 12 fps.
4. Choose a reference: search "claymation diorama" on Instagram; save 3 references for lighting + color.

### 2. Physical setup (60–90 min)

- **Armature:** 1.5 mm aluminum wire, twisted into a skeleton (head, spine, 2 arms, 2 legs).
- **Clay:** polymer clay (Sculpey, Fimo) for final shots; plasticine (Non-Hardening) for iteration.
- **Set:** foam board base, cardboard backdrops, mini props from dollhouse suppliers.
- **Lighting:** 2× softbox LED panels at 45° left/right, 5600 K, no flicker. Avoid overheads (hard shadows on clay).
- **Camera:** lock tripod, use a **wireless remote** to avoid nudging the rig. Disable autofocus — manual focus locked on the subject's eyes.

### 3. Shooting (2–5 hours per 15 s)

1. Set frame 0 pose. Shoot. Move puppet 1–2 mm toward next pose.
2. At 12 fps, **12 frames per second of screen time**. For 15 s: **180 frames**.
3. Use **Stop Motion Studio** (iOS/macOS, $10) or **Dragonframe** (Windows/macOS, $300) — both show onion-skin overlay so you can see the previous frame's position.
4. If a beat needs a "camera move" (dolly, pan), move the camera ~2 mm per frame in the same direction.
5. **Never re-use a pose.** Every frame must be a fresh physical adjustment.

### 4. Post-production (30 min)

```bash
# Import frames (Stop Motion Studio exports numbered PNGs: frame_0001.png …)
# Convert to MP4 at 12 fps, upscale to 30 fps for social (duplicates every frame 2.5×)
ffmpeg -framerate 12 -i frames/frame_%04d.png \
  -vf "scale=1080:1920:flags=lanczos,fps=30" \
  -c:v libx264 -crf 18 -pix_fmt yuv420p \
  out_silent.mp4

# Add music + SFX (see audio/ or voice/ skills for TTS)
ffmpeg -i out_silent.mp4 -i music.mp3 \
  -c:v copy -c:a aac -b:a 128k -shortest \
  out_final.mp4

# Verify
ffprobe -v error -show_entries stream=codec_name,width,height,duration out_final.mp4
```

### 5. Export checklist

- [ ] Duration ≤ 30 s (TikTok sweet spot: 15 s)
- [ ] 1080×1920 px, 30 fps output
- [ ] H.264, AAC audio
- [ ] Loudness normalized to −14 LUFS (see `video/editor` skill)
- [ ] No black frames at start/end (trim 0.2 s each side)

## 3D Clay Look (Blender alternative)

If physical sculpting is not feasible, fake the aesthetic in Blender:

1. **Sculpt mode:** use the Clay Strips brush on a subdivided sphere; add asymmetry manually.
2. **Material:** Principled BSDF with:
   - Subsurface: 0.3, Subsurface Radius (1.0, 0.4, 0.2)
   - Roughness: 0.6 (matte clay look)
   - Base Color: warm skin/earth tones
3. **Fingerprints:** add a Noise Texture → Bump node (Strength 0.1) to mimic hand-pressed clay.
4. **Lighting:** 3-point with a large area light as key; warm color temp.
5. **Render:** Cycles, 128 samples, 1080×1920, 12 fps.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll shoot at 24 fps for smoothness" | Stop-motion at 24 fps is 2× the work for marginal gain. Industry standard is 12 fps. |
| "I'll fix focus in post" | Clay has no edges to track. Lock manual focus before shooting. |
| "I'll add clay texture in post" | If you don't have it in-camera, no LUT will save it. Light it properly. |
| "AI-generated clay look is fine" | Midjourney/DALL·E output is a single image, not 180 sequential frames with consistent puppet. |

## Verification

- [ ] Frame count matches 12 fps × duration (e.g., 15 s = 180 frames)
- [ ] No flicker between frames (constant lighting, locked exposure)
- [ ] Puppet does not drift across frames (armature is stable)
- [ ] Output is 1080×1920, 30 fps, H.264
- [ ] Audio loudness at −14 LUFS ± 1
- [ ] Contact sheet from final MP4 reviewed (sample every 12th frame)
