---
name: remotion
description: "Create, render, and manage programmatic videos using Remotion (React-based video framework). Use this skill whenever the user wants to make a video with code — including anime, music videos, movie/cinematic trailers, influencer/TikTok/Reels content, product showcases, brand promos, podcast videos, data visualizations, explainers, or any promotional/production video. Also trigger when using Remotion as a fallback for AI video generation (Kling, Sora, HeyGen, etc.). Trigger for vague requests like 'make me a video about X', 'animate this', 'create a video ad', or any Remotion-specific concepts: compositions, useCurrentFrame, interpolate, spring, AbsoluteFill, staticFile, calculateMetadata, renderMedia."
---

# Remotion Video Skill

Remotion is a React-based framework for creating real MP4 videos programmatically. It gives you a frame number and a canvas — you render React components that change per frame to produce animations and videos.

## New User? Start Here

**If the user is new to Remotion or asks "how do I start", "where do I begin", or "I've never used this before":**
→ Load `references/ONBOARDING.md` and walk them through it interactively.

**Quick orientation (for Claude):**
- Ask: *"What kind of video do you want to make?"* if not already stated
- Check: Do they have Node.js, Python, ffmpeg installed? (see ONBOARDING prerequisites)
- Route: Match to a Path (A=narrated, B=TikTok, C=music, D=captions, E=template)
- Give: The exact commands to run, in order, no guessing

**The fastest path for 90% of users:**
```bash
npx create-video@latest my-video   # 1. create project
cd my-video && npm install          # 2. install
python scripts/pipeline.py --voice id  # 3. generate TTS (after editing script.json)
npm run dev                         # 4. preview
npx remotion render [Id] out/video.mp4  # 5. render
./scripts/postprocess.sh            # 6. post-process
```

---

## Core Mental Model

A video is a function of images over time. Remotion renders each frame as a React component snapshot. **All animations MUST be driven by `useCurrentFrame()`** — never use CSS transitions, setTimeout, or setInterval inside Remotion components.

## Quick Reference: Core APIs

```tsx
import {
  AbsoluteFill,       // Full-screen container (position: absolute, 100% w/h)
  useCurrentFrame,    // Returns current frame number (0-indexed)
  useVideoConfig,     // Returns { fps, durationInFrames, width, height }
  interpolate,        // Map frame range → value range
  spring,             // Physics-based animation (0→1)
  Sequence,           // Time-shift children (from, durationInFrames)
  Series,             // Show components one after another
  Audio,              // Sync audio with timeline
  Video,              // Embed video (<OffthreadVideo> preferred for rendering)
  Img,                // Load image and wait for it
  staticFile,         // Reference files in /public folder
  Freeze,             // Freeze children at a specific frame
  Loop,               // Loop children repeatedly
} from 'remotion';
```

## Getting Started (New Project)

```bash
npx create-video@latest
# Choose: blank / hello-world / next / react-router
cd my-video
npm install
npm run dev   # Opens Remotion Studio at localhost:3000
```

**Render to file:**
```bash
npx remotion render MyComposition out/video.mp4
npx remotion render                     # Interactive picker
npx remotion render --codec gif         # Render as GIF
npx remotion render --sequence          # Image sequence
```

## Project Structure

```
my-video/
├── src/
│   ├── Root.tsx          # Register compositions here
│   ├── Composition.tsx   # Main video component
│   └── scenes/           # Scene components
├── public/               # Static assets (images, audio, fonts)
│   └── audio/
├── package.json
└── remotion.config.ts    # Config (optional)
```

## Fundamentals

### Composition (register a video)
```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { MyVideo } from './Composition';

export const RemotionRoot = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={150}   // 5 seconds at 30fps
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{ title: 'Hello' }}
  />
);
```

### Basic Component
```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';

export const MyVideo = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#fff' }}>
      <h1>Frame {frame} of {durationInFrames}</h1>
    </AbsoluteFill>
  );
};
```

## Animation Patterns

Load `rules/animations.md` for deep animation patterns. Summary:

### interpolate() — map frames to values
```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
// Always use clamp to prevent values going out of range
```

### spring() — physics-based (bouncy) animation
```tsx
const { fps } = useVideoConfig();
const scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });
// Default: animates 0→1. Use with interpolate() to map to other ranges.

// Delayed spring:
const delayedScale = spring({ frame: frame - 20, fps }); // starts at frame 20
```

### Sequencing scenes
```tsx
// <Sequence> time-shifts children — useCurrentFrame() resets to 0 inside
<>
  <Sequence from={0} durationInFrames={90}>
    <Scene1 />
  </Sequence>
  <Sequence from={90} durationInFrames={90}>
    <Scene2 />
  </Sequence>
</>

// <Series> for consecutive scenes
import { Series } from '@remotion/series';
<Series>
  <Series.Sequence durationInFrames={60}><Intro /></Series.Sequence>
  <Series.Sequence durationInFrames={120}><Main /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><Outro /></Series.Sequence>
</Series>
```



## Scripts — All Free, No API Required

Every script in `scripts/` runs 100% locally. No API keys. No subscriptions. The only internet access needed is one-time package downloads.

### Install All Dependencies (One-Time)
```bash
# Python packages — all free, all local
pip install edge-tts openai-whisper librosa soundfile numpy Pillow

# ffmpeg — free, local video processing
brew install ffmpeg        # macOS
apt install ffmpeg         # Ubuntu/Debian
# Windows: https://ffmpeg.org/download.html
```

### Script Reference

| Script | Purpose | Run With |
|---|---|---|
| `pipeline.py` | TTS audio generation + timing.json | `python scripts/pipeline.py --voice id` |
| `setup.py` | Scaffold project folders + starter files | `python scripts/setup.py --type narrated` |
| `transcribe.py` | Speech-to-text → captions.json + .srt (local Whisper, no API) | `python scripts/transcribe.py public/audio/narration.mp3` |
| `bpm_detect.py` | Detect BPM for music videos | `python scripts/bpm_detect.py public/audio/track.mp3 --save` |
| `caption_to_srt.py` | Convert captions.json ↔ .srt | `python scripts/caption_to_srt.py public/captions.json` |
| `prepare_assets.py` | Resize images + convert video to Remotion-ready formats | `python scripts/prepare_assets.py --format 9:16` |
| `postprocess.sh` | FFmpeg: mix BGM, burn subtitles, export all formats | `./scripts/postprocess.sh --formats mp4,vertical,gif` |
| `batch_render.sh` | Render all compositions in one command | `./scripts/batch_render.sh` |

### Full Pipeline (Narrated Video — Zero API)

```bash
# 1. Set up project structure
python scripts/setup.py --type narrated

# 2. Edit your script
# → public/script.json

# 3. Generate TTS audio (edge-tts, free, no key)
python scripts/pipeline.py --voice id   # id=Indonesian, en=English, zh=Chinese

# 4. Preview in Remotion Studio
npm run dev

# 5. Render raw video
npx remotion render NarratedVideo out/video-raw.mp4

# 6. Post-process: mix BGM + burn subs + export formats
./scripts/postprocess.sh --formats mp4,vertical,gif
```

### Full Pipeline (Music Video — Zero API)

```bash
# 1. Detect BPM of your track
python scripts/bpm_detect.py public/audio/track.mp3 --save
# → writes public/bpm.json

# 2. Preview
npm run dev

# 3. Render
npx remotion render MusicVideo out/video-raw.mp4

# 4. Post-process
./scripts/postprocess.sh --no-bgm --formats mp4,vertical
```

### Full Pipeline (Video with Captions — Zero API)

```bash
# 1. Transcribe speech to captions (local Whisper, no API)
python scripts/transcribe.py public/audio/narration.mp3 --lang id

# 2. Captions are imported directly in Remotion (captions.json)
#    OR converted to SRT for FFmpeg burning:
python scripts/caption_to_srt.py public/captions.json

# 3. Render
npx remotion render MyVideo out/video-raw.mp4

# 4. Burn subtitles + mix BGM
./scripts/postprocess.sh --formats mp4
```

---
## Templates — Copy-Paste Starters

All templates live in `templates/`. Each is a complete, runnable Remotion project. Copy into `src/` of a new `npx create-video@latest` project, customize the CONFIG block at the top, and render.

| File | Genre | Format | Duration |
|---|---|---|---|
| `narrated-video-starter.tsx` | Narrated / Podcast | 16:9 | TTS-driven |
| `tiktok-viral-short.tsx` | TikTok / Short-Form | 9:16 | 30s |
| `product-launch-commercial.tsx` | Product Launch | 16:9 | 60s |
| `youtube-tutorial.tsx` | Education / Tutorial | 16:9 | 3–15 min |
| `music-video-lyric.tsx` | Music Video / Lyric | 16:9 | Song length |
| `data-story-infographic.tsx` | Data / Infographic | 16:9 | 90s |
| `movie-trailer-cinematic.tsx` | Cinematic Trailer | 16:9 | 90s |
| `ugc-testimonial-ad.tsx` | UGC / Authentic Ad | 9:16 | 30s |
| `podcast-talking-head.tsx` | Podcast / Talk | 16:9 | Episode |
| `brand-logo-intro.tsx` | Logo Ident / Bumper | 16:9 | 5s |
| `viral-challenge-gameshow.tsx` | Challenge Video | 16:9 | 90s |
| `asmr-product-reveal.tsx` | ASMR / Sensory | 9:16 or 16:9 | 45s |
| `countdown-event-promo.tsx` | Event Promo | 16:9 or 9:16 | 30s |

**How to use a template:**
```bash
npx create-video@latest my-video  # select "blank"
cd my-video
# Copy chosen template file into src/
# Edit the CONFIG block at the top of the file
npm run dev   # preview in Remotion Studio
npx remotion render [CompositionId] out/video.mp4
```

---
## Step 1 — Identify the Video Genre

Read this table first. Load the matching genre file BEFORE writing any code.

| User says / wants | Genre Rule File |
|---|---|
| Anime, manga, action cartoon, cel-shading, speed lines, otaku | `rules/genres/anime.md` |
| Movie, film, short film, trailer, cinematic, Netflix-style | `rules/genres/movie.md` |
| Music video, MV, lyric video, visualizer, beat-sync, waveform | `rules/genres/mv.md` |
| Podcast, talking head, narrated video, YouTube video, explainer with voice | `rules/podcast.md` |
| Influencer, TikTok, Reels, Shorts, vlog-style, scroll-stopper, hook | `rules/genres/influencer.md` |
| Product showcase, product demo, ad, commercial, before/after, SaaS promo | `rules/genres/product.md` |
| Promo, brand video, corporate, explainer animation, event, countdown, tutorial | `rules/genres/promo.md` |
| Live talk, keynote, motivation, TEDx, speaking video, inspiration, coach | `rules/genres/talk.md` |
| Documentary, mini-doc, brand story, Netflix-style, trust video | `rules/genres/documentary.md` |
| Viral challenge, MrBeast-style, prize reveal, competition, last-to-leave | `rules/genres/challenge.md` |
| UGC ad, authentic ad, testimonial, unboxing, before/after, review | `rules/genres/ugc.md` |
| Tutorial, how-to, education, explainer, course, coding walkthrough | `rules/genres/education.md` |
| ASMR, sensory, satisfying, slow-motion, macro, relaxing, calming | `rules/genres/asmr.md` |
| News, motion graphics, data explainer, kinetic typography, infographic | `rules/genres/news.md` |
| Comedy, sketch, meme, POV, reaction, parody, satire | `rules/genres/comedy.md` |
| Gaming, esports, montage, highlight reel, tier list, stream overlay | `rules/genres/gaming.md` |


**Load `genres/viral-formula.md` first** for ANY video intended to go viral or sell — it is the meta-layer on top of all genres.

**If the genre is unclear:** default to `rules/genres/promo.md` (most general) and ask the user to clarify.

**Multiple genres:** load multiple files. E.g. an "influencer-style anime review" → load both `genres/anime.md` + `genres/influencer.md`.

---

## Step 2 — Load Technical Rules As Needed

After loading the genre file, pull in specific technical rules based on what the video needs:

| Task | Rule File |
|------|-----------|
| Animations, timing, easing | `rules/animations.md` |
| Audio, TTS, music | `rules/audio.md` |
| Video embedding | `rules/video.md` |
| Text animations | `rules/text.md` |
| Scene-based structure | `rules/scenes.md` |
| Assets (images, fonts, GIFs) | `rules/assets.md` |
| Rendering & output formats | `rules/rendering.md` |
| Captions & subtitles | `rules/captions.md` |
| Data visualization / charts | `rules/charts.md` |
| 3D with Three.js / R3F | `rules/3d.md` |
| Scene transitions | `rules/transitions.md` |
| Parametrize / Zod schema | `rules/parameters.md` |
| Full TTS narration pipeline | `rules/tts-pipeline.md` |
| Long-form podcast video | `rules/podcast.md` |
| Advanced effects (motion blur, noise, paths, shapes, shaders) | `rules/effects.md` |
| All packages, plugins & component libraries | `rules/ecosystem.md` |

## Quickest Wins — Recommended Additions to Any Project

```bash
# Declarative animation (replaces most raw interpolate calls)
npm i remotion-animated

# Official effects packages (pin to same version as remotion)
npm i --save-exact @remotion/motion-blur @remotion/noise @remotion/paths @remotion/shapes

# Google Fonts
npm i @remotion/google-fonts

# Transitions
npm i @remotion/transitions
```

**`remotion-animated`** eliminates boilerplate for common animations:
```tsx
import { Animated, Move, Fade, Scale } from 'remotion-animated';

// Instead of multiple interpolate() calls:
<Animated animations={[
  Fade({ initial: 0, duration: 20 }),
  Move({ initialY: 30, duration: 25 }),
  Scale({ initial: 0.9, duration: 20 }),
]}>
  <YourElement />
</Animated>
```

> For the full plugin/package reference (all 20+ packages, 5 component libraries, 10 GitHub repos): load `rules/ecosystem.md`
> For motion blur, noise, SVG paths, shapes, shaders: load `rules/effects.md`

---

## Common Mistakes to Avoid

1. **Never use CSS transitions** — they won't render correctly. Use `interpolate()` + `useCurrentFrame()`.
2. **Never use `useState` for animations** — state resets between renders. Use frame math.
3. **Always use `<Img>` not `<img>`** — Remotion's `<Img>` waits for the image to load before rendering.
4. **Always use `<OffthreadVideo>` not `<Video>` for rendering** — `<Html5Video>` can cause frame drops.
5. **Always `clamp` `extrapolateRight`** in interpolate to prevent runaway values.
6. **Use `fps` from `useVideoConfig()`** in timing, not hardcoded numbers: `durationInFrames={5 * fps}` not `durationInFrames={150}`.
7. **All assets must go in `/public`** and be referenced via `staticFile('filename.mp3')`.

## License Note

Remotion is free for individuals and teams up to 3 people. Companies with 4+ people need a paid license ($250/mo minimum). Always mention this when creating commercial projects.
