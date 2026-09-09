---
name: hyperframes-product-launch-video
description: "Create product launch videos from a URL, brief, or script using HyperFrames (HTML→MP4). Use when the user wants a product launch video, site tour, social clip featuring a product's own visuals, or marketing/promoting a product. Up to ~3 min (sweet spot 30-90s). Teaches the HyperFrames production loop: plan → write HTML → wire seekable animations → add media → lint → preview → render."
domain: "content-creation"
tags:
  - hyperframes
  - video
  - product-launch
  - html-to-video
  - animation
  - motion-graphics
  - marketing
  - agent-native
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill assembles a product launch video — hero shot, feature callouts, timing — as a HyperFrames composition. Use it when a new release needs a tight, brandable announcement clip. It renders the final MP4 from the product assets you supply.


# HyperFrames — Product Launch Video

Create product launch videos by writing HTML compositions that HyperFrames renders to deterministic MP4. The agent-native video pipeline: LLMs write HTML (their first language), HyperFrames renders frame-exact video via headless Chrome + FFmpeg.

## When to Use

- User wants a **product launch video** from a URL, brief, or script
- User wants a **site tour / showcase** featuring the product's own visuals
- User wants a **social clip** (TikTok/Reels/Shorts) with kinetic captions and branding
- User wants a **marketing/promo video** with animated overlays and music
- User says "make me a video" and provides a product URL or description

## When NOT to Use

- User wants real-person / UGC / studio content (needs camera, not HTML)
- User wants live streaming / live commerce (needs RTMP ingest)
- User wants a talking-head interview (use `hyperframes-embedded-captions` or `hyperframes-talking-head-recut`)
- User wants a pure explainer with no product/URL (use `hyperframes-faceless-explainer`)
- User wants a presentation/deck (use `hyperframes-slideshow`)

## Workflow

### 0 · Bootstrap the project

```bash
npx hyperframes init my-launch-video
cd my-launch-video
```

This creates the project scaffold with `index.html`, `package.json`, and the HyperFrames CLI configured.

### 1 · Plan the video

- **Input:** product URL, brief, or script
- **Output:** 3-6 scene storyboard with timing (total 30-90s sweet spot)
- **Budget:** title ≤2s, outro ≤3s, middle scenes ≈8-12s each
- **Pick a design language:** browse `hyperframes.heygen.com/design` for frame.md templates

### 2 · Write the composition HTML

The composition contract:

```html
<!doctype html>
<html lang="en">
  <body>
    <div
      id="main"
      data-composition-id="intro"
      data-start="0"
      data-duration="15"
      data-width="1080"
      data-height="1920"
      data-fps="30"
    >
      <div
        class="clip"
        data-start="0"
        data-duration="5"
        data-track-index="0"
      >
        <!-- Scene content -->
      </div>
    </div>
  </body>
</html>
```

Key attributes:
- `data-composition-id`: unique ID for the composition
- `data-start` / `data-duration`: timing in seconds
- `data-width` / `data-height`: viewport dimensions (1080×1920 for 9:16)
- `data-fps`: frame rate (30 standard)
- `class="clip"`: marks timed elements
- `data-track-index`: layer order (higher = on top)

### 3 · Wire seekable animations

Use GSAP (recommended), CSS keyframes, or WAAPI. All animations must be **seekable** (deterministic — same frame at same time, every render).

**GSAP pattern (recommended):**

```javascript
const tl = gsap.timeline({ paused: true });
tl.to("#title", { opacity: 1, y: 0, duration: 0.8, ease: "power4.out" }, 0.5);
tl.to("#image", { scale: 1, opacity: 1, duration: 1.2, ease: "power3.out" }, 1.0);
window.__timelines = { main: tl };
```

**CSS keyframes pattern:**

```css
@keyframes fadeInUp {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.animate-in {
  animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

### 4 · Add media

- **Images:** download to `public/` dir, reference via `staticFile()` or relative path
- **Video backgrounds:** place in `assets/`, loop via `data-loop`
- **Audio/BGM:** add via `<audio data-start="0" data-duration="15" src="./bgm.mp3">`
- **Voiceover:** generate via TTS, align captions to word timestamps

### 5 · Lint and check

```bash
npx hyperframes check        # validate composition contract
npx hyperframes lint         # check for common errors
```

Fix all errors before proceeding. Warnings are acceptable but should be reviewed.

### 6 · Preview

```bash
npx hyperframes preview      # opens Hyperframes Studio with HMR
```

Spot-check 3-4 beats via `__player.seek(time)` on the raw comp page. Verify:
- Animations trigger at the right time
- No white flashes at cuts (opaque stage ground)
- Captions visible and readable
- Audio levels balanced

### 7 · Render

```bash
npx hyperframes render --output launch-video.mp4
```

Verify the output:
```bash
ffmpeg -ss 3 -i launch-video.mp4 -frames:v 1 frame-3s.png  # check captions
ffmpeg -ss 15 -i launch-video.mp4 -frames:v 1 frame-15s.png # check scene
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll just use a video editor" | GUI editors aren't agent-native; HTML is what LLMs write best |
| "I'll skip the lint step" | Lint catches composition contract errors that break renders |
| "I'll use Remotion instead" | Remotion requires React reasoning; HTML is simpler for agents |
| "I'll add idle animations to fill time" | Idle wobble is banned — every phase must perform (see `hyperframes-cut-the-curve`) |
| "I'll center content at 42% to leave room for captions" | Captions are an overlay — center on true center (y = H/2) |
| "I'll use a crossfade between scenes" | Crossfades have no carrier — use cut-the-curve for default boundaries |
| "I'll write one big HTML file without scenes" | Scenes are the unit of composition — each gets its own clip wrapper |
| "I'll skip the preview and just render" | Preview catches timing errors that waste render time |

## Code Example

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 100%; height: 100%; overflow: hidden; background: #0a0a0a; }
      #main {
        position: relative;
        width: 1080px;
        height: 1920px;
        overflow: hidden;
      }
      .scene {
        position: absolute;
        inset: 0;
        opacity: 0;
        transition: opacity 0.5s ease;
      }
      .scene.active { opacity: 1; }
      .hook-bg {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 80px;
        text-align: center;
        color: white;
        font-family: system-ui, sans-serif;
      }
      .hook-text {
        font-size: 72px;
        font-weight: 800;
        line-height: 1.1;
        transform: translateY(40px);
        opacity: 0;
      }
      .animate-in {
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
      @keyframes fadeInUp {
        from { transform: translateY(40px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
    </style>
  </head>
  <body>
    <div
      id="main"
      data-composition-id="product-ad"
      data-start="0"
      data-duration="15"
      data-width="1080"
      data-height="1920"
      data-fps="30"
    >
      <div class="scene hook-bg" data-start="0" data-duration="5" data-track-index="0">
        <h1 class="hook-text animate-in" data-start="0.5" data-duration="4">
          Product Name
        </h1>
      </div>
    </div>
    <script>
      // Scene activation via IntersectionObserver or manual timing
      const scenes = document.querySelectorAll('.scene');
      scenes.forEach(scene => {
        const start = parseFloat(scene.dataset.start);
        const duration = parseFloat(scene.dataset.duration);
        setTimeout(() => scene.classList.add('active'), start * 1000);
        setTimeout(() => scene.classList.remove('active'), (start + duration) * 1000);
      });
    </script>
  </body>
</html>
```

## Verification

- [ ] Composition passes `npx hyperframes check` with 0 errors
- [ ] All scenes have `data-start`, `data-duration`, `data-track-index`
- [ ] Animations are seekable (deterministic, not wall-clock dependent)
- [ ] Preview shows correct timing on 3+ spot-checked beats
- [ ] Rendered MP4 has no white flashes, frozen frames, or missing captions
- [ ] Audio levels are balanced (voiceover carve applied if needed)
- [ ] Output resolution matches target (1080×1920 for 9:16, 1920×1080 for 16:9)
