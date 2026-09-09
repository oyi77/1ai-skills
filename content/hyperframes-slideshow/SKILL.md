---
name: hyperframes-slideshow
description: "Build a presentation, pitch deck, or interactive deck using HyperFrames. Use when the user wants slides with fragment reveals, branching navigation, hotspot links, or presenter mode. Output is a navigable deck, not a rendered MP4. Teaches slide-as-scene composition, fragment timing, and deck navigation patterns."
domain: "content-creation"
tags:
  - hyperframes
  - slideshow
  - presentation
  - pitch-deck
  - slides
  - interactive
  - branching
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
---

# HyperFrames — Slideshow / Deck

A presentation, pitch deck, or interactive deck. Discrete slides, fragment reveals, branching, hotspot navigation, presenter mode. Output is a navigable deck, not a rendered video.

## When to Use

- User wants a **presentation** or **pitch deck**
- User wants **slides** with animated reveals
- User wants an **interactive deck** (branching, hotspots)
- User wants a **slide deck** that can also render to video
- User says "make me slides" or "pitch deck"

## When NOT to Use

- User wants a rendered MP4 video (use `hyperframes-product-launch-video`)
- User wants a PowerPoint file (use `document-creator` skill)
- User wants a single motion graphic (use `hyperframes-motion-graphics`)

## Workflow

### 1 · Plan the deck

- **Slide count:** 5-15 for pitches, 10-30 for deep dives
- **Structure:** title → problem → solution → proof → CTA
- **Timing:** if rendering to video, 5-10s per slide

### 2 · Author slides as scenes

Each slide is a clip with full-canvas duration:

```html
<div class="slide" data-start="0" data-duration="8" data-track-index="0">
  <h1 class="slide-title">Problem</h1>
  <p class="slide-body">Customers waste 3 hours daily on manual reports.</p>
</div>
<div class="slide" data-start="8" data-duration="8" data-track-index="1">
  <h1 class="slide-title">Solution</h1>
  <p class="slide-body">Automated pipeline in one click.</p>
</div>
```

### 3 · Add fragment reveals

Within a slide, stagger element entrances for presenter-paced reveals:

```css
.fragment { opacity: 0; }
.fragment.visible { animation: fadeInUp 0.5s forwards; }
.fragment:nth-child(2) { animation-delay: 0.3s; }
.fragment:nth-child(3) { animation-delay: 0.6s; }
```

### 4 · Wire navigation (interactive mode)

- **Linear:** arrow keys / click advance `__player.seek(nextSlide)`
- **Branching:** hotspot buttons jump to named slides
- **Presenter mode:** speaker notes in separate pane, synced via same clock

### 5 · Preview and render

```bash
npx hyperframes preview      # interactive deck navigation
npx hyperframes render --output deck.mp4   # linear video version
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll put everything on one slide" | One idea per slide — split dense slides |
| "I'll skip fragment reveals" | Staggered reveals control pacing and focus |
| "I'll use tiny text to fit more" | 28px minimum for body, 48px+ for titles |
| "I'll make 50 slides" | 5-15 for pitches — cut ruthlessly |

## Verification

- [ ] One idea per slide
- [ ] Fragment reveals stagger correctly
- [ ] Navigation works (linear + branching if needed)
- [ ] Text readable (28px+ body, 48px+ titles)
- [ ] Renders cleanly to MP4 if requested
