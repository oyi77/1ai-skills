# Remotion Templates — Complete Catalogue

All templates are production-ready, fully self-contained, and designed to be copy-pasted into a new Remotion project (`npx create-video@latest → blank`).

## How to Use Any Template

1. Run `npx create-video@latest` → choose **blank**
2. Copy the template `.tsx` file into `src/`
3. Rename `RemotionRoot` export to match your `src/index.ts` entry point
4. Replace placeholder footage/images with your own files in `public/`
5. Customize the `CUSTOMIZE` block at the top of each file
6. Run `npm run dev` to preview in Remotion Studio
7. Run `npx remotion render` to export

---

## Template Index

### 🎬 Production / Film

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| Movie Trailer | `movie-trailer-cinematic.tsx` | 16:9 1080p | 90s | Hollywood cinematic |
| Anime Opening | `anime-opening.tsx` | 16:9 1080p | 90s | Japan anime / sakuga |
| Music Video + Lyrics | `music-video-lyric.tsx` | 16:9 1080p | 3–4 min | MV / lyric video |

### 📣 Marketing & Sales

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| Product Launch | `product-launch-commercial.tsx` | 16:9 1080p | 60s | Product commercial |
| UGC Testimonial Ad | `ugc-testimonial-ad.tsx` | 9:16 1920p | 30s | UGC authentic ad |
| Video Sales Letter (VSL) | `sales-vsl.tsx` | 16:9 1080p | 90s | Sales funnel |
| E-Commerce Story Pack | `ecommerce-story-pack.tsx` | 9:16 1920p | 6s×N | Instagram Stories |
| Brand Logo Intro | `brand-logo-intro.tsx` | 16:9 1080p | 10s | Brand ident |
| ASMR Product Reveal | `asmr-product-reveal.tsx` | 16:9 / 9:16 | 45s | ASMR sensory |

### 📱 Social & Viral

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| TikTok Viral Short | `tiktok-viral-short.tsx` | 9:16 1920p | 30s | Influencer / short-form |
| Viral Challenge | `viral-challenge-mrbeast.tsx` | 16:9 1080p | 8 min | MrBeast-style challenge |
| Year in Review / Wrapped | `year-in-review-wrapped.tsx` | 9:16 1920p | ~45s | Spotify Wrapped style |
| Comedy / Meme / POV | `comedy-meme-pov.tsx` | 9:16 or 16:9 | 15–30s | Comedy sketch |

### 🎓 Education & Authority

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| YouTube Tutorial | `youtube-tutorial.tsx` | 16:9 1080p | 5–15 min | Education / how-to |
| TED Talk / Motivation | `ted-talk-motivation.tsx` | 16:9 1080p | ~8 min | Talk / keynote |
| News Motion Graphics | `news-motion-graphics.tsx` | 16:9 1080p | 3 min | News explainer |
| Data Story Infographic | `data-story-infographic.tsx` | 16:9 1080p | 60s | Data visualisation |

### 🎙️ Content & Storytelling

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| Podcast Talking Head | `podcast-talking-head.tsx` | 16:9 1080p | Variable | Podcast / narration |
| Documentary Mini-Doc | `documentary-minidoc.tsx` | 16:9 1080p | 3 min | Documentary |
| Narrated Video Starter | `narrated-video-starter.tsx` | 16:9 1080p | Variable | TTS narration base |

### 🎮 Entertainment

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| Gaming Montage | `gaming-montage.tsx` | 16:9 1080p | Variable | Gaming / esports |
| Countdown Event Promo | `countdown-event-promo.tsx` | 16:9 1080p | 30s | Event / countdown |

### 📊 Data & Business

| Template | File | Format | Duration | Genre |
|---|---|---|---|---|
| Data Story Infographic | `data-story-infographic.tsx` | 16:9 1080p | 60s | Data viz |
| Video Sales Letter | `sales-vsl.tsx` | 16:9 1080p | 90s | Conversion |

---

## Quick Customization Guide

Every template has a clearly marked `// ── CUSTOMIZE ──` block at the top. This is the only section you normally need to edit:

```tsx
// ── CUSTOMIZE ──────────────────────────────────────────────
const PRODUCT_NAME  = 'Your Product Name';   // ← change this
const ACCENT_COLOR  = '#6366f1';             // ← change this
const FEATURES = [ ... ];                    // ← change this
// ───────────────────────────────────────────────────────────
```

## Required Assets (Public Folder)

Most templates reference assets in `/public/`. Create this structure:

```
public/
├── audio/          ← MP3 files (narration, music, sfx)
├── footage/        ← MP4 video clips
├── products/       ← Product images (JPG/PNG/WebP)
├── characters/     ← Character art (PNG with transparency)
├── contestants/    ← Challenge participant photos
└── images/         ← General images
```

## Audio Generation

For narrated templates, run the TTS pipeline:

```bash
pip install edge-tts
python scripts/pipeline.py --voice id     # Indonesian (Bahasa)
python scripts/pipeline.py --voice en     # English
python scripts/pipeline.py --voice zh     # Chinese
```

## Rendering

```bash
# Standard 1080p
npx remotion render MyComposition out/video.mp4 --crf 18

# 4K
npx remotion render MyComposition out/video-4k.mp4 --scale 2

# GIF (for social preview)
npx remotion render MyComposition out/preview.gif --codec gif

# Vertical 9:16
# (dimensions set in template — just render normally)
npx remotion render MyComposition out/reel.mp4
```
