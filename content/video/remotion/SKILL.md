---
name: remotion
description: >
  Create, render, and manage programmatic videos using Remotion (React-based video framework).
  Covers compositions, frame-driven animation, transitions, effects, captions, audio, voiceover,
  FFmpeg post-production, and professional SaaS-grade motion design.
domain: content
tags:
  - content-creation
  - video-production
  - remotion
  - react
  - animation
  - motion-design
  - programmatic-video
  - ffmpeg
  - transitions
---
# Remotion — Professional Programmatic Video

Canonical source: [remotion-dev/skills](https://github.com/remotion-dev/skills) (401K+ installs on skills.sh).
Companion skills: [video-editor](../video-editor/SKILL.md) · [video-gen](../video-gen/SKILL.md) · [faceless-youtube](../faceless-youtube/SKILL.md) · [auto-clipper](../auto-clipper/SKILL.md) · [b-roll-finder](../b-roll-finder/SKILL.md) · Frontend: [tailwind-advanced](../../tailwind-advanced/SKILL.md) · [frontend-design](../../frontend-design/SKILL.md) · [shadcn-ui](../../shadcn-ui/SKILL.md) · [design-tokens](../../design-tokens/SKILL.md)

## When to Use

**Trigger phrases:**
- "remotion" · "make a video with code" · "animate this" · "create a video ad"
- "product demo video" · "SaaS hero video" · "explainer video" · "motion graphics"
- "video with captions" · "music visualizer" · "podcast video"

**Use cases:**
- Programmatic video generation from React components
- Data-driven video content (dashboards, charts, metrics)
- Brand/product videos with consistent visual identity
- TikTok/Reels/Shorts with captions and overlays
- Music videos with beat-synced animations
- Podcast audiograms with waveform visualization
- Cinematic trailers with scene transitions
- Faceless YouTube channels at scale

**When NOT to use:**
- When a screen recording suffices
- When real camera footage is the primary element
- For live streaming (Remotion renders to file, not real-time)

---

## Overview

Remotion is a React-based framework for creating real MP4 videos programmatically. You write React components that read `useCurrentFrame()` and render what should appear at that instant. Remotion stitches every frame into a video file via headless Chromium + ffmpeg.

**Key capabilities:** frame-precise animation via `interpolate`/`spring`, timeline management via `<Sequence>`/`<TransitionSeries>`, WebGL effects, captions (`@remotion/captions`), audio visualization (`@remotion/media-utils`), AI voiceover (ElevenLabs), bundled FFmpeg, and programmatic rendering via `@remotion/renderer`.

## Process

1. **Scaffold** — `npx create-video@latest my-video` to bootstrap
2. **Design** — Define color palette, typography, timing structure (acts/scenes)
3. **Build components** — Create reusable animated components (cards, text, charts)
4. **Compose timeline** — Use `<Sequence>` / `<TransitionSeries>` to orchestrate scenes
5. **Polish motion** — Tune easing curves, spring configs, stagger delays
6. **Add audio** — Background music, sound effects, voiceover
7. **Add captions** — Transcribe or import SRT, display with `@remotion/captions`
8. **Render draft** — `npx remotion render` with fast settings (jpeg, high crf)
9. **Review** — Watch the actual MP4, check timing and motion quality
10. **Render final** — Production settings (png or jpeg 80+, crf 18)

---

## Core Mental Model

```
Frame 0    Frame 1    Frame 2    ...    Frame N
  │          │          │                 │
  ▼          ▼          ▼                 ▼
React      React      React             React
render     render     render            render
  │          │          │                 │
  ▼          ▼          ▼                 ▼
PNG        PNG        PNG        ...    PNG  → ffmpeg → MP4
```

---

## Project Setup

### Scaffold

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
cd my-video
npx remotion studio   # Opens Remotion Studio preview
```

### Project Structure

```
my-video/
├── src/
│   ├── Root.tsx              # Register compositions
│   ├── MyVideo.tsx           # Main composition component
│   └── components/           # Reusable animated components
├── public/                   # Static assets (images, audio, fonts)
├── package.json
└── remotion.config.ts
```

### Root.tsx — Composition Registry

```tsx
import { Composition } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="MyVideo"
    component={MyVideo}
    durationInFrames={900}   // 30 seconds at 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

### Dynamic Metadata with `calculateMetadata`

For data-driven duration/dimensions/props:

```tsx
import { CalculateMetadataFunction } from "remotion";

const calculateMetadata: CalculateMetadataFunction<MyProps> = async ({
  props, abortSignal,
}) => {
  const data = await fetch(`https://api.example.com/video/${props.id}`, {
    signal: abortSignal,
  }).then(r => r.json());

  return {
    durationInFrames: Math.ceil(data.duration * 30),
    width: 1920,
    height: 1080,
    props: { ...props, videoUrl: data.url },
  };
};
```

---

## The Four Primitives

### 1. `useCurrentFrame()` — The Clock

Returns the current frame number (0-indexed). Inside a `<Sequence>`, this is relative to the sequence start.

### 2. `useVideoConfig()` — The Constants

```tsx
const { fps, durationInFrames, width, height } = useVideoConfig();
```

### 3. `interpolate()` — The Mapper (PREFERRED)

Your primary animation tool. **Prefer `interpolate()` over `spring()`** unless physics-based motion is explicitly needed.

```tsx
import { interpolate, Easing } from "remotion";

// Basic fade — always clamp
const opacity = interpolate(frame, [0, 2 * fps], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp",
});

// With Bézier easing (identical to CSS cubic-bezier)
const enter = interpolate(frame, [0, 45], [0, 1], {
  easing: Easing.bezier(0.16, 1, 0.3, 1),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

#### Studio-Editable Animation (IMPORTANT)

Keep `interpolate()` inline in the `style` prop. Use individual CSS transform properties, NOT `transform` strings:

```tsx
// ✅ CORRECT — editable in Remotion Studio
style={{
  scale: interpolate(frame, [0, 100], [0, 1]),
  translate: interpolate(frame, [0, 100], ["0px 0px", "100px 100px"]),
  rotate: interpolate(frame, [0, 100], ["20deg", "90deg"]),
  opacity: interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" }),
}}

// ❌ WRONG — not Studio-editable
const scale = interpolate(frame, [0, 100], [0, 1]);
style={{ transform: `scale(${scale})` }}
```

Only use `transform` strings for `skew()`, `perspective()`, or order-sensitive multi-transform chains.

#### Copy-Paste Bézier Curves

| Curve | cubic-bezier | Use |
|---|---|---|
| **Crisp UI entrance** | `(0.16, 1, 0.3, 1)` | Strong ease-out, no overshoot |
| **Editorial fade** | `(0.45, 0, 0.55, 1)` | Balanced ease-in-out |
| **Snappy pop** | `(0.34, 1.56, 0.64, 1)` | Overshoot, then settle |
| **Dramatic slow-in** | `(0.7, 0, 0.84, 0)` | Long hold, fast release |
| **Smooth decel** | `(0, 0, 0.2, 1)` | Gentle landing |

### 4. `spring()` — The Physics Engine

Use only when physics-based motion is explicitly needed. Always pass `fps`.

```tsx
import { spring } from "remotion";

const scale = spring({
  frame,
  fps,
  config: {
    damping: 20,
    stiffness: 200,
    mass: 0.5,
    overshootClamping: true,
  },
});
```

#### Spring Config Presets

| Style | damping | stiffness | mass | overshootClamping |
|---|---|---|---|---|
| **Snappy** (UI) | 20 | 200 | 0.5 | true |
| **Smooth** (text) | 15 | 100 | 1 | true |
| **Bouncy** (playful) | 8 | 180 | 1 | false |
| **Gentle** (bg) | 30 | 80 | 1.5 | true |
| **Elastic** (accent) | 5 | 150 | 0.8 | false |

---

## Layout — Video-First Design

Videos are watched differently than web pages are read. Design for quick understanding from the full frame.

### Rules

- **One focal point per scene.** One main text message, one supporting visual, one or two background accents.
- **Safe area:** Keep key text ≥80px from sides, ≥100px from top/bottom on 1080p.
- **Use flex/grid/gap** for readable content. Absolute positioning is for backgrounds, decorative shapes, particles.
- **Solve crowding with time.** Reveal elements sequentially instead of showing everything at once.
- **Text sizing minimums** (1080px-wide):
  - Main headline: **84px**
  - Supporting text: **44px**
  - Labels/callouts: **32px**
  - Scale proportionally for other widths.

### `<AbsoluteFill>`

Base layer for everything. Later children render on top.

```tsx
import { AbsoluteFill } from "remotion";

<AbsoluteFill style={{
  backgroundColor: "#FAFBFE",
  justifyContent: "center",
  alignItems: "center",
}}>
  <MyContent />
</AbsoluteFill>
```

### `<Sequence>` — Timeline Management

Use sequences to mount/unmount components at specific times. Never use `if (frame > X)` for lifecycle.

```tsx
import { Sequence } from "remotion";

<AbsoluteFill>
  <Sequence durationInFrames={90}>
    <Intro />
  </Sequence>
  <Sequence from={90} durationInFrames={630}>
    <MainContent />
  </Sequence>
  <Sequence from={720} durationInFrames={180}>
    <Outro />
  </Sequence>
</AbsoluteFill>
```

- `useCurrentFrame()` inside is relative to `from`
- Children unmounted after `durationInFrames` (performance win)
- Default: wraps in `<AbsoluteFill>`. Use `layout="none"` for flex/grid children.

---

## Using Frontend Skills in Video Context

Remotion components are React — you can (and should) use frontend skills for styling, layout, and component design. But video has different constraints than web.

### What transfers from web → video

| Web Skill | How to use in Remotion |
|---|---|
| [tailwind-advanced](../../tailwind-advanced/SKILL.md) | Install per [rules/tailwind.md](https://github.com/remotion-dev/skills/blob/main/skills/remotion/rules/tailwind.md). Use for rapid styling of cards, badges, layouts. |
| [frontend-design](../../frontend-design/SKILL.md) | Typography hierarchy, spacing rhythm, visual hierarchy — all apply to video frames. |
| [shadcn-ui](../../shadcn-ui/SKILL.md) | Use shadcn components (Card, Badge, Button) as visual building blocks in product demos and dashboard mockups. |
| [design-tokens](../../design-tokens/SKILL.md) | Define brand colors, spacing, typography tokens once, use across all compositions. |
| [styled-components](../../styled-components/SKILL.md) | Works in Remotion. Good for dynamic styles driven by frame number. |

### What does NOT transfer

| Web Pattern | Why it fails in video |
|---|---|
| `@media` queries / responsive breakpoints | Video has **fixed dimensions** (1920×1080). No responsive design. |
| CSS transitions / animations | **FORBIDDEN** — they desync from the frame clock. Use `interpolate()`. |
| Hover / focus states | No mouse in video. No interactive states. |
| `rem` / `em` units | Use `px` — there's no root font-size to scale against. |
| Lazy loading / code splitting | Remotion renders every frame synchronously. No lazy loading. |
| Browser-specific hacks | Remotion uses headless Chromium. No cross-browser concerns. |
| SEO / accessibility | Not applicable to video output. |

### Video-first frontend rules

1. **Fixed canvas** — Always `px`, never relative units
2. **Inline styles for animation** — Keep `interpolate()` calls in `style` prop for Studio editability
3. **Individual transform properties** — Use `scale`, `translate`, `rotate` (not `transform` string)
4. **Large text** — Main headline ≥84px, supporting ≥44px, labels ≥32px at 1080p
5. **One focal point per scene** — Not a dense dashboard; a clear visual message
6. **No z-index wars** — Stacking is controlled by JSX source order in `<AbsoluteFill>`

### Example: shadcn Card in a promo video

```tsx
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";

const FeatureCard: React.FC<{ title: string; delay: number }> = ({ title, delay }) => {
  const frame = useCurrentFrame();

  const enter = interpolate(
    Math.max(0, frame - delay),
    [0, 20], [0, 1],
    { easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateRight: "clamp" }
  );

  return (
    <div style={{
      opacity: enter,
      translate: `0px ${interpolate(enter, [0, 1], [30, 0])}px`,
      background: "white",
      borderRadius: 12,
      padding: 32,
      boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
      maxWidth: 400,
    }}>
      <div style={{ fontSize: 28, fontWeight: 700, color: "#1a1a2e" }}>{title}</div>
    </div>
  );
};
```

---
## Transitions — `<TransitionSeries>`

Install: `npx remotion add @remotion/transitions`

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />
  <TransitionSeries.Sequence durationInFrames={90}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

### Available Transitions

| Transition | Import | Effect |
|---|---|---|
| `fade` | `@remotion/transitions/fade` | Crossfade between scenes |
| `slide` | `@remotion/transitions/slide` | Slide in direction |
| `wipe` | `@remotion/transitions/wipe` | Wipe reveal |
| `clockWipe` | `@remotion/transitions/clock-wipe` | Clock wipe |

### Overlays (Light Leaks)

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { LightLeak } from "@remotion/light-leaks";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>
  <TransitionSeries.Overlay durationInFrames={30}>
    <LightLeak />
  </TransitionSeries.Overlay>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

---

## Visual Effects

Install: `npx remotion add @remotion/effects`

Effects use WebGL2. Enable for renders:
```ts
import { Config } from '@remotion/cli/config';
Config.setChromiumOpenGlRenderer('angle');
```

```tsx
import { Video } from '@remotion/media';
import { blur } from '@remotion/effects/blur';

<Video src="https://remotion.media/video.mp4" effects={[blur({ radius: 8 })]} />
```

### Available Effects

`blur` · `brightness` · `contrast` · `colorKey` · `duotone` · `grayscale` · `hue` · `invert` · `saturation` · `tint` · `thermalVision` · `linearProgressiveBlur` · `zoomBlur` · `dropShadow` · `glow` · `lightTrail` · `evolve` · `mirror` · `scale` · `chromaticAberration` · `fisheye` · `barrelDistortion` · `wave` · `pixelate` · `noise` · `vignette` · `scanlines` · `halftone` · `dotGrid` · `contourLines` · `whiteNoise` · `tvSignalOff`

---

## Audio

### Background Music

```tsx
import { Audio } from "@remotion/media";
import { staticFile } from "remotion";

<Audio src={staticFile("bg-music.mp3")} volume={0.3} />
```

### Sound Effects

Use built-in SFX from `@remotion/sfx`:

```tsx
import { Audio } from "@remotion/sfx";

<Audio src="https://remotion.media/whoosh.wav" />
```

**Available SFX:** `whoosh` · `whip` · `page-turn` · `switch` · `mouse-click` · `shutter-modern` · `shutter-old` · `ding` · `snapchat-notification` · `record-scratch` · `anime-wow` · `wilhelm-scream` · `vine-boom` · `mac-quack` · `skedaddle` + more at remotion.media

### Audio Visualization (Podcast/Audiogram)

Install: `npx remotion add @remotion/media-utils`

```tsx
import { useWindowedAudioData, visualizeAudio } from "@remotion/media-utils";
import { staticFile, useCurrentFrame, useVideoConfig } from "remotion";

const { audioData, dataOffsetInSeconds } = useWindowedAudioData({
  src: staticFile("podcast.wav"),
  frame, fps,
  windowInSeconds: 30,
});

const frequencies = visualizeAudio({
  fps, frame, audioData,
  numberOfSamples: 256,
  optimizeFor: "speed",
  dataOffsetInSeconds,
});

// Render spectrum bars
<div style={{ display: "flex", alignItems: "flex-end", height: 200 }}>
  {frequencies.map((v, i) => (
    <div key={i} style={{
      flex: 1, height: `${v * 100}%`,
      backgroundColor: "#0b84f3", margin: "0 1px",
    }} />
  ))}
</div>
```

---

## Voiceover (ElevenLabs TTS)

Generate speech per scene, then use `calculateMetadata` to size the composition:

```ts
// generate-voiceover.ts
const response = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
  {
    method: "POST",
    headers: {
      "xi-api-key": process.env.ELEVENLABS_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: "Welcome to the show.",
      model_id: "eleven_multilingual_v2",
      voice_settings: { stability: 0.5, similarity_boost: 0.75, style: 0.3 },
    }),
  },
);
const audioBuffer = Buffer.from(await response.arrayBuffer());
writeFileSync(`public/voiceover/scene-01.mp3`, audioBuffer);
```

Use `calculateMetadata` + `getAudioDuration` to dynamically set duration from audio length.

---

## Captions & Subtitles

Install: `npx remotion add @remotion/captions`

```ts
import type { Caption } from "@remotion/captions";

type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
};
```

- **Transcribe:** Use Whisper or ElevenLabs to generate captions from audio
- **Import SRT:** Parse `.srt` files into `Caption[]`
- **Display:** Use `<CaptionRenderer>` for word-by-word highlighting

---

## Fonts

### Google Fonts (Recommended)

Never use CSS `@import` or `<link>` — Remotion blocks rendering until `loadFont()` completes.

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont("normal", {
  weights: ["400", "600", "700"],
  subsets: ["latin"],
});

<AbsoluteFill style={{ fontFamily }}>
  <h1 style={{ fontWeight: 700, fontSize: 84 }}>Hello</h1>
</AbsoluteFill>
```

---

## Assets

### `staticFile()` — Reference Public Assets

```tsx
import { Img, staticFile } from "remotion";
import { Video, Audio } from "@remotion/media";

<Img src={staticFile("logo.png")} style={{ width: 200 }} />
<Video src={staticFile("bg.mp4")} />
<Audio src={staticFile("music.mp3")} />
```

### Remote URLs

```tsx
<Video src="https://remotion.media/video.mp4" />
```

---

## FFmpeg (Bundled)

FFmpeg is bundled with Remotion — no separate install needed.

```bash
npx remotion ffmpeg -i input.mp4 output.mp3
npx remotion ffprobe input.mp4
```

### Trimming (In-Component)

```tsx
import { Video } from "@remotion/media";

<Video src={staticFile("video.mp4")} trimBefore={5 * fps} trimAfter={10 * fps} />
```

### Post-Production (CLI)

```bash
# Add captions
npx remotion ffmpeg -i input.mp4 -vf subtitles=captions.srt output.mp4

# Merge clips
npx remotion ffmpeg -f concat -safe 0 -i filelist.txt -c copy merged.mp4

# Optimize for platform
npx remotion ffmpeg -i input.mp4 -vf "scale=1080:1920" -c:v libx264 -preset slow -crf 22 tiktok.mp4

# Add watermark
npx remotion ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=W-w-10:H-h-10" watermarked.mp4
```

### Platform Specifications

| Platform | Resolution | Aspect | Max Length | Format |
|---|---|---|---|---|
| YouTube | 1920×1080 | 16:9 | Unlimited | MP4 |
| Instagram Feed | 1080×1080 | 1:1 | 60s | MP4 |
| Instagram Reels | 1080×1920 | 9:16 | 90s | MP4 |
| TikTok | 1080×1920 | 9:16 | 10min | MP4 |
| LinkedIn | 1920×1080 | 16:9 | 10min | MP4 |
| X / Twitter | 1280×720 | 16:9 | 2:20 | MP4 |

---

## Professional Motion Design Patterns

### Pattern 1: SaaS Hero Video (Capitalise.ai style)

Clean white background, dashboard mockups floating in with orchestrated timing.

```tsx
// Brand reveal → dashboard showcase → CTA
<AbsoluteFill>
  <Sequence from={0} durationInFrames={150}>
    <BrandReveal />           {/* Logo + tagline fade in */}
  </Sequence>
  <Sequence from={150} durationInFrames={900}>
    <DashboardScene />        {/* Sidebar + floating cards */}
  </Sequence>
  <Sequence from={1050} durationInFrames={300}>
    <ClosingCTA />            {/* Fade to white, CTA */}
  </Sequence>
</AbsoluteFill>
```

### Pattern 2: Floating Card Entry

```tsx
const FloatingCard: React.FC<{
  delay: number;
  direction: "left" | "right" | "up";
  children: React.ReactNode;
}> = ({ delay, direction, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enter = interpolate(
    Math.max(0, frame - delay),
    [0, 20], [0, 1],
    { easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateRight: "clamp" }
  );

  const offsets = { left: [-120, 0], right: [120, 0], up: [0, -80] };
  const [dx, dy] = offsets[direction];

  return (
    <div style={{
      opacity: enter,
      translate: `${interpolate(enter, [0, 1], [dx, 0])}px ${interpolate(enter, [0, 1], [dy, 0])}px`,
      scale: interpolate(enter, [0, 1], [0.95, 1]),
    }}>
      {children}
    </div>
  );
};
```

### Pattern 3: Staggered List Reveal

```tsx
{items.map((item, i) => {
  const delay = i * 8;
  const enter = interpolate(
    Math.max(0, frame - delay),
    [0, 20], [0, 1],
    { easing: Easing.bezier(0.16, 1, 0.3, 1), extrapolateRight: "clamp" }
  );
  return (
    <div key={i} style={{
      opacity: enter,
      translate: `0px ${interpolate(enter, [0, 1], [30, 0])}px`,
    }}>
      {item}
    </div>
  );
})}
```

### Pattern 4: Typewriter Effect

```tsx
const TypewriterText: React.FC<{ text: string; cps?: number; startFrame?: number }> = ({
  text, cps = 30, startFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const elapsed = Math.max(0, frame - startFrame);
  const chars = Math.min(text.length, Math.floor(elapsed * (cps / fps)));

  return (
    <span>
      {text.slice(0, chars)}
      <span style={{ opacity: frame % 16 < 8 ? 1 : 0 }}>|</span>
    </span>
  );
};
```

### Pattern 5: Parallax Background

```tsx
const ParallaxScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ translate: `${interpolate(frame, [0, durationInFrames], [0, -200])}px 0` }}>
        {/* Background — sky, gradient */}
      </AbsoluteFill>
      <AbsoluteFill style={{ translate: `${interpolate(frame, [0, durationInFrames], [0, -400])}px 0` }}>
        {/* Mid-ground — buildings */}
      </AbsoluteFill>
      <AbsoluteFill style={{ translate: `${interpolate(frame, [0, durationInFrames], [0, -600])}px 0` }}>
        {/* Foreground — text, CTA */}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

### Pattern 6: Beat-Synced Pulse

```tsx
const BeatPulse: React.FC<{ bpm: number }> = ({ bpm }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const framesPerBeat = (fps * 60) / bpm;
  const beatPhase = (frame % framesPerBeat) / framesPerBeat;
  const pulse = interpolate(beatPhase, [0, 0.1, 0.3], [1, 1.05, 1], { extrapolateRight: "clamp" });

  return <div style={{ scale: pulse }}>{/* Content */}</div>;
};
```

---

## Color Palettes

### SaaS / Corporate

```ts
{
  background: "#FAFBFE",     // Near-white with blue tint
  surface: "#FFFFFF",        // Pure white cards
  dark: "#1A1A2E",           // Dark navy
  text: "#1A1A2E",
  textSecondary: "#6B7280",  // Gray-500
  accent: "#DDF2EE",         // Mint green
  accentDark: "#10B981",     // Emerald-500
  danger: "#EF4444",
  border: "#E5E7EB",
}
```

### Dark Mode

```ts
{
  background: "#0F0F1A",
  surface: "#1A1A2E",
  text: "#F1F1F1",
  textSecondary: "#9CA3AF",
  accent: "#818CF8",         // Indigo-400
  accentDark: "#6366F1",
  border: "#2D2D44",
}
```

---

## Rendering

### Preview

```bash
npx remotion studio
```

### Single Frame Check

```bash
npx remotion still MyVideo --scale=0.25 --frame=30
```

### Local Render

```bash
npx remotion render src/index.ts MyVideo out/video.mp4
```

### Programmatic Render (Node.js)

```tsx
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";

const bundled = await bundle({ entryPoint: "./src/index.ts" });
const composition = await selectComposition({ serveUrl: bundled, id: "MyVideo" });

await renderMedia({
  composition, serveUrl: bundled,
  codec: "h264",
  outputLocation: "out/video.mp4",
  crf: 18,
  concurrency: 8,
  imageFormat: "jpeg",
});
```

### Cloud Render (inference.sh)

Via [halt-catch-fire/skills/remotion-render](https://skills.sh/halt-catch-fire/skills/remotion-render) (262K installs):

```bash
npx skills add belt-sh/cli
belt login
belt render ./my-video --provider inference-sh
```

### Render Quality Settings

| Setting | Fast Draft | Production | Max Quality |
|---|---|---|---|
| `imageFormat` | jpeg | jpeg | png |
| `crf` | 28 | 18 | 10 |
| `concurrency` | 16 | 8 | 4 |
| `jpegQuality` | 50 | 80 | 100 |

---

## AI Video Generation (Complementary)

For AI-generated clips to embed in Remotion compositions, use these skills.sh models via RunComfy CLI:

| Model | Best For | Installs |
|---|---|---|
| [HappyHorse 1.0](https://skills.sh/agentspace-so/runcomfy-agent-skills/ai-video-generation) | Arena #1, native audio | 272K |
| [Kling 3.0](https://skills.sh/agentspace-so/runcomfy-agent-skills/ai-video-generation) | 4K, multi-shot identity | 303K |
| [Seedance 2.0 Pro](https://skills.sh/doany-ai/skills/seedance-v2) | Multi-modal cinematic, lip-sync | 220K |
| [Veo 3-1](https://skills.sh/doany-ai/skills/video-extend) | Physics-respecting, video extend | 220K |
| [Wan 2.7](https://skills.sh/agentspace-so/runcomfy-agent-skills/image-to-video) | Audio-driven lip-sync | 327K |

### Prompt Engineering Formula

```
[Subject] + [Action] + [Camera] + [Style] + [Audio]
```

**Camera vocabulary:** tracking shot · dolly zoom · aerial view · close-up · slow motion · time-lapse · pan left/right · zoom in/out · static · handheld

**Style vocabulary:** cinematic · 4K · film grain · shallow DOF · golden hour · dramatic shadows · soft diffused light · Blade Runner aesthetic · moody · vibrant

---

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "CSS animations are simpler" | CSS animations desync from the frame clock. Every pixel will be wrong on render. |
| "I'll use `transform: scale()`" | Not editable in Remotion Studio. Use individual `scale`, `translate`, `rotate` properties. |
| "spring() looks better" | Official guidance: prefer `interpolate()` unless physics is explicitly needed. |
| "I'll hardcode frame numbers" | Breaks when fps changes. Always use `fps` from `useVideoConfig()`. |
| "Regular `<img>` is fine" | Doesn't block render. Images flicker. Use Remotion's `<Img>`. |
| "CSS @import for fonts" | Render starts before fonts load. Use `@remotion/google-fonts`. |
| "Small text looks clean" | Video is watched at distance. Main headline ≥84px at 1080p. |
| "Show everything at once" | Crowded frames lose viewers. Solve crowding with time — reveal sequentially. |
| "Good enough motion" | Jarring timing and amateur easing are immediately visible. Polish the motion. |
| "I don't need `extrapolateRight: clamp`" | Values continue past range — elements fly off screen. |

## Verification

- [ ] Every animation uses `useCurrentFrame()` — zero CSS animations/transitions
- [ ] All frame calculations use `fps` from `useVideoConfig()` — zero hardcoded frame numbers
- [ ] All `interpolate` calls have `extrapolateRight: "clamp"`
- [ ] Individual CSS transform properties used (not `transform` strings) where possible
- [ ] `interpolate` preferred over `spring` for standard animations
- [ ] Fonts loaded via `@remotion/google-fonts`, not CSS
- [ ] Images use `<Img>` from Remotion, not `<img>`
- [ ] Videos use `<Video>` from `@remotion/media`
- [ ] Assets referenced via `staticFile()`
- [ ] Sequences used for lifecycle, not `if (frame > X)`
- [ ] Main headline ≥84px at 1080p width
- [ ] One focal point per scene, no crowding
- [ ] Transitions use `<TransitionSeries>`, not manual opacity hacks
- [ ] Colors from a defined palette
- [ ] Test render at draft quality before final render
- [ ] Final render verified by watching the actual MP4

