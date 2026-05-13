# Remotion Ecosystem: Official Packages, Plugins & Component Libraries

This is the **master reference** for all installable packages and component sources. Load this file whenever the user asks what packages are available, or when you need a specific effect and want to find the best library for it.

---

## Official @remotion/* Packages

Install ALL at the **exact same version** as your `remotion` package. Remove `^` from version numbers to prevent conflicts.

```bash
# Always pin versions — no ^ allowed
npm i --save-exact @remotion/motion-blur@4.0.420 @remotion/noise@4.0.420 ...
```

### Animation & Effects

| Package | Install | What It Does |
|---|---|---|
| `@remotion/motion-blur` | `npm i @remotion/motion-blur` | `<Trail>` + `<CameraMotionBlur>` — film-quality motion blur |
| `@remotion/noise` | `npm i @remotion/noise` | Perlin noise functions (noise2D, noise3D, noise4D) — organic movement |
| `@remotion/shapes` | `npm i @remotion/shapes` | SVG shapes: `<Star>`, `<Triangle>`, `<Pie>`, `<Rect>` — animatable geometric primitives |
| `@remotion/paths` | `npm i @remotion/paths` | SVG path utilities: `evolvePath()` (draw-on), `getLength()`, `getPointAtLength()`, `interpolatePath()` |
| `@remotion/transitions` | `npm i @remotion/transitions` | `<TransitionSeries>` with fade, slide, wipe, flip, iris, clockWipe |
| `@remotion/light-leaks` | `npm i @remotion/light-leaks` | Film-style light leak overlay effects |

### Media & Assets

| Package | Install | What It Does |
|---|---|---|
| `@remotion/media-utils` | `npm i @remotion/media-utils` | `useAudioData()`, `visualizeAudio()`, `getAudioDurationInSeconds()`, `getVideoMetadata()`, `createSmoothSvgPath()` |
| `@remotion/gif` | `npm i @remotion/gif` | `<Gif>` component — GIF animations synced to timeline |
| `@remotion/lottie` | `npm i @remotion/lottie` | `<Lottie>` — After Effects JSON animations, frame-accurate |
| `@remotion/rive` | `npm i @remotion/rive` | `<RiveAnimation>` — Rive state machine animations (faster than Lottie) |
| `@remotion/google-fonts` | `npm i @remotion/google-fonts` | Tree-shakeable Google Fonts loader, 1000+ fonts |
| `@remotion/fonts` | `npm i @remotion/fonts` | Load local custom fonts with `loadFont()` |

### 3D & Advanced Rendering

| Package | Install | What It Does |
|---|---|---|
| `@remotion/three` | `npm i @remotion/three three @types/three` | `<ThreeCanvas>` — Three.js / React Three Fiber integration |
| `@remotion/skia` | `npm i @remotion/skia @shopify/react-native-skia` | `<SkiaCanvas>` — React Native Skia (GPU-accelerated 2D drawing, shaders) |

### Text & Captions

| Package | Install | What It Does |
|---|---|---|
| `@remotion/captions` | `npm i @remotion/captions` | `createTikTokStyleCaptions()`, word-level timing, caption pagination |

### Rendering & Infrastructure

| Package | Install | What It Does |
|---|---|---|
| `@remotion/lambda` | `npm i @remotion/lambda` | AWS Lambda serverless rendering |
| `@remotion/bundler` | `npm i @remotion/bundler` | SSR bundle creation |
| `@remotion/renderer` | `npm i @remotion/renderer` | Node.js `renderMedia()`, `renderStill()`, `selectComposition()` |
| `@remotion/tailwind` | `npm i @remotion/tailwind` | Tailwind CSS integration for Remotion |
| `@remotion/zod-types` | `npm i @remotion/zod-types` | `zColor()` and other Zod types for schema props |

---

## Third-Party Libraries (Community)

### Declarative Animation

**`remotion-animated`** — Move animation logic into JSX, great for simple animations fast.
```bash
npm i remotion-animated
```
```tsx
import { Animated, Move, Scale, Fade } from 'remotion-animated';

<Animated animations={[
  Fade({ initial: 0, duration: 20 }),
  Move({ initialY: 40, duration: 30 }),
  Scale({ initial: 0.8, duration: 25 }),
]}>
  <h1>This just works</h1>
</Animated>
```

**`remotion-kit`** — AnimatedElement + AnimatedText with presets.
```bash
npm i remotion-kit
```
```tsx
import { AnimatedElement, AnimatedText, presets } from 'remotion-kit';

<AnimatedElement animationIn={presets.fadeIn} animationOut={presets.fadeOut} durationInFrames={90}>
  <img src="my-image.jpg" />
</AnimatedElement>

<AnimatedText durationInFrames={120} wordAnimation={{ animation: presets.fadeIn, overlap: 0.5 }}>
  Word by word reveal
</AnimatedText>
```

### Text Animation

**`remotion-animate-text`** — Character/word level animation with multi-property support.
```bash
npm i remotion-animate-text
```
```tsx
import { AnimatedText } from 'remotion-animate-text';

<AnimatedText duration={60} animation={{
  delimiter: '',         // '' = chars, ' ' = words
  opacity: [0, 1],
  x: [1, 0],
  y: [1, 0],
  scale: [0, 1],
  rotate: [45, 0],
  durations: [40, 50],
}}>
  Hello world
</AnimatedText>
```

### Subtitles from SRT

**`remotion-subtitle`** — Load `.srt` files, get animated sequences with pre-built caption templates.
```bash
npm i remotion-subtitle
```
```tsx
import { SubtitleSequence } from 'remotion-subtitle';
import { TypewriterCaption as Caption } from 'remotion-subtitle';

const subtitles = new SubtitleSequence('audio.srt');
await subtitles.ready();
const Sequences = subtitles.getSequences(<Caption style={{ fontSize: '32px' }} />, fps);

// In your component:
return <>{Sequences}</>;

// Available caption styles:
// TypewriterCaption, FadeCaption, SlideCaption, PopCaption
```

### Component Libraries (Copy-Paste)

**`remotion-bits`** — Production-ready building blocks. Use the CLI or npm.
```bash
npm i remotion-bits
# OR copy individual bits:
npx remotion-bits find "text animation"
npx remotion-bits fetch bit-fade-in --json
```
Components include: `AnimatedText`, `StaggeredMotion`, `GradientTransition`, `ParticleSystem`, `Scene3D`

**Clippkit** — Copy-paste component library at [clippkit.com](https://www.clippkit.com)
No install needed — copy code directly from the docs. Includes:
- Popping Text, Glitch Text, Sliding Text
- Circular Waveform visualizer
- Scene intros, split-screen layouts
- Kinetic title templates

**remocn** — shadcn-style registry for Remotion components.
```bash
# Add components like shadcn/ui
npx shadcn add https://remocn.vercel.app/r/blur-reveal.json
npx shadcn add https://remocn.vercel.app/r/[component-name].json
```
Includes: blur-reveal, kinetic titles, gradient scenes, animated backgrounds.

---

## Key Packages Per Use Case

Quick lookup — what to install for each task:

| Goal | Install |
|---|---|
| Motion blur on fast-moving objects | `@remotion/motion-blur` |
| Draw-on SVG path animation | `@remotion/paths` |
| Star/triangle/pie shapes | `@remotion/shapes` |
| Organic noise movement (camera shake, particles) | `@remotion/noise` |
| GIF playback synced to timeline | `@remotion/gif` |
| After Effects animations | `@remotion/lottie` |
| High-performance vector animations | `@remotion/rive` |
| Google Fonts (Bebas Neue, Poppins, etc.) | `@remotion/google-fonts` |
| Film grain, grit, texture | `@remotion/noise` + SVG filter |
| Skia shaders / GPU effects | `@remotion/skia` |
| TikTok-style word captions | `@remotion/captions` |
| SRT subtitle files | `remotion-subtitle` |
| Declarative animation JSX | `remotion-animated` or `remotion-kit` |
| Scene transitions | `@remotion/transitions` |
| Light leak film effects | `@remotion/light-leaks` |
| Audio waveform / spectrum | `@remotion/media-utils` |
| 3D scenes | `@remotion/three` |
| Advanced 2D/shader art | `@remotion/skia` |
| Serverless rendering | `@remotion/lambda` |

---

## @remotion/motion-blur Usage

```tsx
import { CameraMotionBlur } from '@remotion/motion-blur';

// Wrap any content with motion blur
<CameraMotionBlur
  shutterAngle={180}  // typical film = 180°; more = blurrier
  samples={10}        // quality (higher = better, slower)
>
  <AbsoluteFill>
    <MovingObject />
  </AbsoluteFill>
</CameraMotionBlur>

// Trail effect (ghost copies)
import { Trail } from '@remotion/motion-blur';
<Trail
  extraFrames={3}      // how many ghost frames
  decay={0.7}          // opacity falloff
  style={{ opacity: 1 }}
>
  <FastMovingElement />
</Trail>
```

---

## @remotion/noise Usage

```tsx
import { noise2D, noise3D } from '@remotion/noise';

// Organic camera shake
const shakeX = noise2D('x-shake', frame * 0.05, 0) * 20;
const shakeY = noise2D('y-shake', frame * 0.05, 1) * 15;
<AbsoluteFill style={{ transform: `translate(${shakeX}px, ${shakeY}px)` }}>

// Floating particle with noise
const x = noise2D(`particle-${id}-x`, frame * 0.02, 0) * 100;
const y = noise2D(`particle-${id}-y`, frame * 0.02, 0) * 100;

// Noise waveform
const points = Array.from({ length: 100 }, (_, i) =>
  noise2D('wave', i * 0.1, frame * 0.02) * 80
);
```

---

## @remotion/paths Usage

```tsx
import { evolvePath, getLength, getPointAtLength } from '@remotion/paths';

const path = 'M 0 100 Q 300 0 600 100 Q 900 200 1200 100';

// Draw-on animation (SVG line drawing effect)
const progress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
const { strokeDasharray, strokeDashoffset } = evolvePath(progress, path);

<svg viewBox="0 0 1200 200">
  <path
    d={path}
    fill="none"
    stroke="#6366f1"
    strokeWidth={4}
    strokeDasharray={strokeDasharray}
    strokeDashoffset={strokeDashoffset}
  />
</svg>

// Move an object along a path
const len = getLength(path);
const dist = progress * len;
const { x, y } = getPointAtLength(path, dist);
<circle cx={x} cy={y} r={10} fill="red" />
```

---

## @remotion/shapes Usage

```tsx
import { Star, Triangle, Pie, Rect } from '@remotion/shapes';
import { makeCircle, makeStar, makeTriangle } from '@remotion/shapes'; // as pure functions

const { fps } = useVideoConfig();
const rotation = (frame / fps) * 180; // spin

// Star shape
<Star
  points={5}
  innerRadius={60}
  outerRadius={120}
  fill="#fbbf24"
  style={{ transform: `rotate(${rotation}deg)` }}
/>

// Pie chart segment
<Pie
  progress={0.75}   // 75%
  radius={100}
  fill="#6366f1"
/>

// Animated triangle
const scale = spring({ frame, fps });
<Triangle
  length={200}
  fill="#ef4444"
  style={{ transform: `scale(${scale})` }}
/>
```

---

## @remotion/skia (GPU Shaders)

```bash
npm i @remotion/skia @shopify/react-native-skia
```

```tsx
import { SkiaCanvas } from '@remotion/skia';
import { Paint, Path, Skia, LinearGradient, vec } from '@shopify/react-native-skia';

// Enable in webpack config (remotion.config.ts):
import { enableSkia } from '@remotion/skia/enable';
Config.overrideWebpackConfig((config) => enableSkia(config));

// In your composition:
const { width, height } = useVideoConfig();

<SkiaCanvas width={width} height={height}>
  <Paint>
    <LinearGradient
      start={vec(0, 0)}
      end={vec(width, height)}
      colors={['#ff6b35', '#f7c59f']}
    />
  </Paint>
  <Path path="M 100 100 L 400 400 Z" />
</SkiaCanvas>

// Shader effects (blur, distortion, etc.)
import { Blur, DisplacementMap } from '@shopify/react-native-skia';
```

---

## Tools & Utilities

**remotion-time** — Use seconds instead of frames:
```bash
npm i remotion-time
```
```tsx
import { seconds } from 'remotion-time';
<Sequence from={seconds(2.5)} durationInFrames={seconds(5)}>
```

**VS Code Extension** — Install "Remotion" by Karel Nagel from VS Code marketplace for syntax highlighting + preview.

**Timing Editor** — Visual timing editor at [remotion.dev/timing-editor](https://remotion.dev/timing-editor)

---

## GitHub Repos Worth Studying

| Repo | What to Learn From It |
|---|---|
| [github-unwrapped](https://github.com/remotion-dev/github-unwrapped) | Parametric personalized video, data-driven scenes, Lambda rendering |
| [template-audiogram](https://github.com/remotion-dev/template-audiogram) | Waveform visualization, audio-synced animations |
| [template-music-visualization](https://github.com/remotion-dev/template-music-visualization) | Beat detection, spectrum bars, reactive visuals |
| [Mockoops](https://github.com/Just-Moh-it/Mockoops) | Product mockup video generation |
| [podcast-maker](https://github.com/FelippeChemello/podcast-maker) | Full podcast-to-video pipeline |
| [d3-example](https://github.com/remotion-dev/d3-example) | D3.js + Remotion data viz |
| [bar-race-chart](https://github.com/hylarucoder/remotion-bar-race-chart) | Animated bar race chart |
| [clippkit](https://github.com/reactvideoeditor/clippkit) | Copy-paste components library |
| [remocn](https://github.com/kapishdima/remocn) | shadcn-style registry |
| [remotion-bits](https://github.com/av/remotion-bits) | MCP-integrated component kit |
