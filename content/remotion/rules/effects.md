# Remotion Advanced Effects

Load this file for: motion blur, organic noise movement, SVG path animations, geometric shapes, GPU shaders, light leaks, glitch, CRT effects.

---

## Motion Blur (@remotion/motion-blur)

```bash
npm i @remotion/motion-blur
```

### CameraMotionBlur — Film-Quality Blur
```tsx
import { CameraMotionBlur } from '@remotion/motion-blur';

<CameraMotionBlur
  shutterAngle={180}  // 180° = standard film. Range: 0–360
  samples={10}        // Higher = better quality, slower render
>
  <AbsoluteFill>
    <YourFastMovingContent />
  </AbsoluteFill>
</CameraMotionBlur>
```

Shutter angle guide:
- `90°` — crisp, sports camera look
- `180°` — standard cinematic (recommended)
- `270°` — dreamy/flowing movement
- `360°` — maximum blur

### Trail — Ghost Echo Effect
```tsx
import { Trail } from '@remotion/motion-blur';

<Trail extraFrames={4} decay={0.6}>
  <MovingElement />
</Trail>
```
Great for: anime speed effect, ball trails, particle trails, neon streaks.

---

## Noise Functions (@remotion/noise)

```bash
npm i @remotion/noise
```

All noise functions are **deterministic** — same seed + same frame = same result.

```tsx
import { noise2D, noise3D, noise4D } from '@remotion/noise';

// Returns value between -1 and 1
const value = noise2D('seed-string', x, y);
```

### Organic Camera Shake
```tsx
const shakeX = noise2D('cam-x', frame * 0.05, 0) * 20;
const shakeY = noise2D('cam-y', frame * 0.05, 1) * 15;
const shakeRot = noise2D('cam-r', frame * 0.04, 2) * 1.5;

<AbsoluteFill style={{
  transform: `translate(${shakeX}px, ${shakeY}px) rotate(${shakeRot}deg)`
}}>
  {children}
</AbsoluteFill>
```

### Floating Particles
```tsx
{particles.map((p, i) => {
  const nx = noise2D(`p${i}-x`, frame * 0.02, 0) * 80;
  const ny = noise2D(`p${i}-y`, frame * 0.02, 0) * 80;
  const scale = 0.5 + noise2D(`p${i}-s`, frame * 0.01, 0) * 0.5;

  return (
    <div key={i} style={{
      position: 'absolute',
      left: p.x + nx,
      top: p.y + ny,
      transform: `scale(${scale})`,
      width: 8, height: 8,
      borderRadius: '50%',
      backgroundColor: '#6366f1',
    }} />
  );
})}
```

### Noise Waveform
```tsx
const W = 1920, H = 200, POINTS = 100;

const points = Array.from({ length: POINTS }, (_, i) => {
  const x = (i / POINTS) * W;
  const y = H / 2 + noise2D('wave', i * 0.1, frame * 0.03) * 80;
  return `${x},${y}`;
}).join(' ');

<svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%' }}>
  <polyline points={points} fill="none" stroke="#6366f1" strokeWidth={3} />
</svg>
```

### Breathing / Pulsing Effect
```tsx
const breathe = noise2D('breathe', frame * 0.02, 0);
const scale = 1 + breathe * 0.04; // subtle ±4% scale breathing
```

---

## SVG Path Animation (@remotion/paths)

```bash
npm i @remotion/paths
```

### Draw-On Line Animation
```tsx
import { evolvePath, getLength } from '@remotion/paths';

const svgPath = 'M 100 200 C 200 100 400 300 500 200 S 700 100 800 200';
const progress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
const { strokeDasharray, strokeDashoffset } = evolvePath(progress, svgPath);

<svg viewBox="0 0 900 400" style={{ width: '100%' }}>
  <path
    d={svgPath}
    fill="none"
    stroke="#6366f1"
    strokeWidth={5}
    strokeLinecap="round"
    strokeDasharray={strokeDasharray}
    strokeDashoffset={strokeDashoffset}
  />
</svg>
```

### Move Object Along Path
```tsx
import { getLength, getPointAtLength, getTangentAtLength } from '@remotion/paths';

const path = 'M 0 300 Q 600 0 1200 300';
const pathLength = getLength(path);
const progress = interpolate(frame, [0, 90], [0, 1], { extrapolateRight: 'clamp' });
const dist = progress * pathLength;

const { x, y } = getPointAtLength(path, dist);
const { x: tx, y: ty } = getTangentAtLength(path, dist);
const angle = Math.atan2(ty, tx) * (180 / Math.PI);

// Rocket follows the path, rotates with tangent
<div style={{
  position: 'absolute',
  left: x - 20,
  top: y - 20,
  transform: `rotate(${angle}deg)`,
  fontSize: 40,
}}>
  🚀
</div>
```

### Morphing Paths
```tsx
import { interpolatePath } from '@remotion/paths';

const pathA = 'M 100 200 L 400 100 L 700 200';
const pathB = 'M 100 100 C 300 300 500 0 700 100';

const morphProgress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
const morphedPath = interpolatePath(morphProgress, pathA, pathB);

<svg viewBox="0 0 800 400">
  <path d={morphedPath} fill="#6366f1" />
</svg>
```

### Signature Draw Effect
```tsx
// Draw handwriting signature
const signaturePath = 'M 50 100 C 80 60 120 80 150 100 ...'; // your SVG path
const drawProgress = interpolate(frame, [0, 90], [0, 1], { extrapolateRight: 'clamp' });
const { strokeDasharray, strokeDashoffset } = evolvePath(drawProgress, signaturePath);

<svg viewBox="0 0 400 200">
  <path
    d={signaturePath}
    fill="none"
    stroke="#1a1a1a"
    strokeWidth={3}
    strokeLinecap="round"
    strokeLinejoin="round"
    strokeDasharray={strokeDasharray}
    strokeDashoffset={strokeDashoffset}
  />
</svg>
```

---

## Geometric Shapes (@remotion/shapes)

```bash
npm i @remotion/shapes
```

```tsx
import { Star, Triangle, Pie, Rect } from '@remotion/shapes';
import { makeCircle, makeStar } from '@remotion/shapes'; // pure function versions

const { fps } = useVideoConfig();
const rotation = (frame / fps) * 90; // 90° per second
const scale = spring({ frame, fps });

// Spinning star
<Star
  points={6}
  innerRadius={50}
  outerRadius={100}
  fill="#fbbf24"
  stroke="#f59e0b"
  strokeWidth={2}
  style={{ transform: `rotate(${rotation}deg) scale(${scale})` }}
/>

// Animated pie (loading circle)
const pieProgress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
<Pie progress={pieProgress} radius={80} fill="#6366f1" />

// Triangle reveal
const triScale = spring({ frame: frame - 10, fps });
<Triangle length={150} fill="#ef4444" style={{ transform: `scale(${triScale})` }} />

// Use as SVG path string (combine with @remotion/paths)
import { makeCircle } from '@remotion/shapes';
const circlePath = makeCircle({ cx: 100, cy: 100, r: 50 });
const { strokeDasharray, strokeDashoffset } = evolvePath(progress, circlePath);
```

---

## Light Leaks (@remotion/light-leaks)

```bash
npm i @remotion/light-leaks
```

```tsx
import { LightLeak } from '@remotion/light-leaks';

// Overlay over your content
<AbsoluteFill>
  <YourContent />
  <LightLeak
    speed={0.5}
    intensity={0.3}
  />
</AbsoluteFill>
```

Great for: vintage/film aesthetic, romantic/emotional scenes, cinematic transitions.

---

## @remotion/skia — GPU Shaders & 2D Drawing

```bash
npm i @remotion/skia @shopify/react-native-skia
```

Add to `remotion.config.ts`:
```ts
import { enableSkia } from '@remotion/skia/enable';
Config.overrideWebpackConfig((config) => enableSkia(config));
```

```tsx
import { SkiaCanvas } from '@remotion/skia';
import {
  Paint, Path, Circle, Rect,
  LinearGradient, RadialGradient,
  Blur, ColorMatrix,
  vec, Skia,
} from '@shopify/react-native-skia';

const { width, height } = useVideoConfig();

// Gradient background
<SkiaCanvas width={width} height={height}>
  <Rect x={0} y={0} width={width} height={height}>
    <LinearGradient
      start={vec(0, 0)}
      end={vec(width, height)}
      colors={['#0f172a', '#1e1b4b', '#312e81']}
    />
  </Rect>

  {/* Glowing circle */}
  <Circle cx={width / 2} cy={height / 2} r={200}>
    <RadialGradient
      c={vec(width / 2, height / 2)}
      r={200}
      colors={['rgba(99,102,241,0.8)', 'transparent']}
    />
    <Blur blur={20} />
  </Circle>
</SkiaCanvas>
```

When to use Skia over CSS:
- WebGL-style shader effects
- Per-pixel manipulation
- Blur effects that must render accurately
- Complex gradient meshes
- Drawing arcs, Bézier curves with GPU precision

---

## Glitch Effect (No Package)

```tsx
// RGB channel split + scanlines + noise
const GlitchOverlay: React.FC<{ intensity?: number }> = ({ intensity = 1 }) => {
  const frame = useCurrentFrame();
  const isGlitching = frame % 20 < 4;
  const offsetX = isGlitching ? (Math.random() - 0.5) * 16 * intensity : 0;

  if (!isGlitching) return null;

  return (
    <AbsoluteFill style={{ mixBlendMode: 'screen', opacity: 0.6, pointerEvents: 'none' }}>
      {/* Red channel */}
      <AbsoluteFill style={{ filter: 'url(#red-only)', transform: `translateX(${offsetX + 4}px)` }} />
      {/* Cyan channel */}
      <AbsoluteFill style={{ filter: 'url(#cyan-only)', transform: `translateX(${-offsetX - 4}px)` }} />
      {/* Horizontal scanline */}
      <div style={{
        position: 'absolute',
        top: Math.random() * 1080,
        left: 0, right: 0,
        height: 4,
        backgroundColor: 'rgba(255,255,255,0.4)',
      }} />
    </AbsoluteFill>
  );
};
```

## CRT / Retro TV Effect

```tsx
const CRTEffect: React.FC = () => {
  const frame = useCurrentFrame();
  const scanlineY = (frame * 4) % 1080; // moving scanline

  return (
    <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 50 }}>
      {/* Scanlines */}
      <AbsoluteFill>
        <svg width="100%" height="100%">
          <defs>
            <pattern id="scanlines" x="0" y="0" width="1920" height="4" patternUnits="userSpaceOnUse">
              <rect width="1920" height="2" fill="rgba(0,0,0,0.15)" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#scanlines)" />
        </svg>
      </AbsoluteFill>
      {/* Vignette */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,0.6) 100%)',
      }} />
      {/* Color aberration */}
      <AbsoluteFill style={{
        filter: 'hue-rotate(2deg)',
        opacity: 0.05,
        mixBlendMode: 'screen',
      }} />
    </AbsoluteFill>
  );
};
```
