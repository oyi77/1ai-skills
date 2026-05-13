# Hollywood-Quality Cinematic Video in Remotion

## The Hollywood Standard

Professional Hollywood output means every frame passes these five tests:
1. **Aspect ratio** — 2.39:1 anamorphic letterbox, bars animate in at scene start
2. **Color grade** — intentional per-genre LUT (teal-orange blockbuster, bleach-bypass thriller, warm golden drama, desaturated horror)
3. **Film grain** — organic animated noise every frame, not static
4. **Motion blur** — `<CameraMotionBlur>` on all fast motion (`@remotion/motion-blur`)
5. **Typography** — Bebas Neue / Oswald / Playfair, not system fonts

Miss any one of these and it reads as amateur. Apply all five and it reads as studio.

---

## Layer Stack (Apply In This Order)

```tsx
export const HollywoodScene: React.FC<{ children: React.ReactNode; grade?: ColorGrade }> = ({
  children, grade = 'teal-orange',
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* 1. Content with motion blur */}
      <CameraMotionBlur shutterAngle={180} samples={10}>
        <AbsoluteFill style={{ filter: COLOR_GRADES[grade] }}>
          {children}
        </AbsoluteFill>
      </CameraMotionBlur>

      {/* 2. Film grain overlay */}
      <FilmGrain opacity={0.055} />

      {/* 3. Vignette */}
      <Vignette intensity={0.45} />

      {/* 4. Letterbox bars — always last, always on top */}
      <LetterboxBars />
    </AbsoluteFill>
  );
};
```

---

## 1. Letterbox Bars (2.39:1 Anamorphic)

```tsx
import { interpolate, spring, useCurrentFrame, useVideoConfig, AbsoluteFill } from 'remotion';

// Bar heights for common resolutions (2.39:1)
// 1920×1080 → 113px  |  3840×2160 → 226px  |  1080×1920 (vertical) → 0px (already taller)
const BAR_HEIGHT: Record<number, number> = { 1080: 113, 2160: 226, 720: 75 };

export const LetterboxBars: React.FC<{ animateIn?: boolean }> = ({ animateIn = true }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();

  const targetH = BAR_HEIGHT[height] ?? Math.round(height * (1 - 1 / 2.39) / 2);

  const barH = animateIn
    ? interpolate(spring({ frame, fps, config: { damping: 120, stiffness: 80 } }), [0, 1], [0, targetH])
    : targetH;

  const barStyle: React.CSSProperties = {
    position: 'absolute', left: 0, right: 0,
    height: barH, backgroundColor: '#000', zIndex: 200,
  };

  return (
    <>
      <div style={{ ...barStyle, top: 0 }} />
      <div style={{ ...barStyle, bottom: 0 }} />
    </>
  );
};
```

---

## 2. Hollywood Color Grades

Implement as CSS filter stacks — each is a named preset matching a real film look.

```tsx
type ColorGrade =
  | 'teal-orange'    // Marvel / Fast & Furious / blockbuster action
  | 'golden-hour'    // La La Land / romantic drama / warm nostalgia
  | 'bleach-bypass'  // Saving Private Ryan / war / thriller / grit
  | 'horror'         // Hereditary / The Ring / desaturated dread
  | 'noir'           // neo-noir / crime / monochrome cool
  | 'sci-fi'         // Blade Runner / Arrival / cold cyan future
  | 'western'        // golden dust / Tarantino / sun-baked warm
  | 'natural';       // no grade — clean Rec.709

export const COLOR_GRADES: Record<ColorGrade, string> = {
  // Teal in shadows, orange in highlights — the most recognisable Hollywood look.
  // Works because skin tones (orange) pop against cooled backgrounds (teal).
  'teal-orange':
    'contrast(1.18) saturate(1.35) brightness(0.97) hue-rotate(2deg)',

  // Warm, slightly faded, lifted blacks — romance and nostalgia.
  'golden-hour':
    'contrast(1.08) saturate(1.25) sepia(0.18) brightness(1.06)',

  // Desaturated, high contrast, metallic — war, desperation, severity.
  'bleach-bypass':
    'contrast(1.45) saturate(0.45) brightness(0.88)',

  // Deep crushed blacks, colour nearly gone, cold.
  'horror':
    'contrast(1.6) saturate(0.25) brightness(0.72) hue-rotate(-8deg)',

  // Near-monochrome, blue-shifted shadows, stark.
  'noir':
    'contrast(1.5) saturate(0.15) brightness(0.82) hue-rotate(-15deg)',

  // Cold cyan / teal everywhere, clinical, futuristic.
  'sci-fi':
    'contrast(1.2) saturate(0.8) brightness(0.93) hue-rotate(-18deg)',

  // Warm dust and gold — sun-bleached outdoor daylight.
  'western':
    'contrast(1.12) saturate(1.1) sepia(0.28) brightness(1.04) hue-rotate(8deg)',

  'natural': 'none',
};

// Apply to any scene or the whole composition
<AbsoluteFill style={{ filter: COLOR_GRADES['teal-orange'] }}>
  <YourScene />
</AbsoluteFill>
```

### Shadow → Teal / Highlight → Orange (SVG Filter, More Accurate)

For the authentic teal-orange separation (CSS filter only approximates it), use an SVG `feComponentTransfer`:

```tsx
export const TealOrangeGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill>
    <svg width="0" height="0" style={{ position: 'absolute' }}>
      <defs>
        <filter id="teal-orange-grade">
          {/* Push shadows toward teal: boost G+B in darks */}
          <feComponentTransfer>
            <feFuncR type="gamma" amplitude="1.05" exponent="1.1" offset="-0.02" />
            <feFuncG type="gamma" amplitude="1.02" exponent="0.95" offset="0.01" />
            <feFuncB type="gamma" amplitude="1.08" exponent="0.9" offset="0.04" />
          </feComponentTransfer>
          {/* Lift contrast */}
          <feComponentTransfer>
            <feFuncR type="linear" slope="1.15" intercept="-0.05" />
            <feFuncG type="linear" slope="1.1"  intercept="-0.04" />
            <feFuncB type="linear" slope="1.1"  intercept="-0.04" />
          </feComponentTransfer>
        </filter>
      </defs>
    </svg>
    <AbsoluteFill style={{ filter: 'url(#teal-orange-grade) saturate(1.3)' }}>
      {children}
    </AbsoluteFill>
  </AbsoluteFill>
);
```

---

## 3. Animated Film Grain

Key: grain must be **different every frame** to feel organic. A static noise texture looks fake.

```tsx
export const FilmGrain: React.FC<{ opacity?: number; size?: number }> = ({
  opacity = 0.055,
  size = 180,   // lower = finer grain; higher = coarser
}) => {
  const frame = useCurrentFrame();
  const seed = (frame * 7919) % 9973; // large primes to avoid repetition

  return (
    <AbsoluteFill style={{ opacity, mixBlendMode: 'overlay', pointerEvents: 'none', zIndex: 150 }}>
      <svg width="100%" height="100%" style={{ position: 'absolute' }}>
        <filter id={`grain-${seed}`}>
          <feTurbulence
            type="fractalNoise"
            baseFrequency={`${0.75 / (size / 100)}`}
            numOctaves="4"
            seed={seed}
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
          <feBlend in="SourceGraphic" mode="overlay" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#grain-${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

// Grain intensity guide:
// 0.03  — barely perceptible (clean digital look)
// 0.055 — standard 35mm film (recommended default)
// 0.09  — heavy grain, pushed film / night scene
// 0.14  — very grainy, Super-8 / found footage
```

---

## 4. Motion Blur (Requires @remotion/motion-blur)

```bash
npm i @remotion/motion-blur
```

```tsx
import { CameraMotionBlur } from '@remotion/motion-blur';

// Wrap any scene with fast camera movement or action
<CameraMotionBlur
  shutterAngle={180}  // 180° = industry standard; higher = dreamier
  samples={10}        // 8–14 is the sweet spot for quality vs render time
>
  <AbsoluteFill>
    <ActionScene />
  </AbsoluteFill>
</CameraMotionBlur>

// Common shutter angles by genre:
// Action blockbuster:  180° (saves Private Ryan had 45° for hyper-realism)
// Drama / romance:     180°–270°
// Horror slow-burn:    90° (crisp, slightly uncanny)
// Dream sequence:      270°–360°
```

---

## 5. Vignette (Focuses Eye to Center)

```tsx
export const Vignette: React.FC<{ intensity?: number }> = ({ intensity = 0.45 }) => (
  <AbsoluteFill style={{
    background: `radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,${intensity}) 100%)`,
    pointerEvents: 'none',
    zIndex: 160,
  }} />
);
```

---

## 6. Hollywood Title Typography

```bash
npm i @remotion/google-fonts
```

```tsx
import { loadFont as loadBebas }    from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadOswald }   from '@remotion/google-fonts/Oswald';
import { loadFont as loadPlayfair } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadRoboto }   from '@remotion/google-fonts/RobotoCondensed';

const { fontFamily: bebasFont }    = loadBebas();
const { fontFamily: oswaldFont }   = loadOswald();
const { fontFamily: playfairFont } = loadPlayfair();

// Main title — Bebas Neue (action / thriller)
const TITLE_STYLE: React.CSSProperties = {
  fontFamily: bebasFont,
  fontSize: 160,
  fontWeight: 400,       // Bebas has no weight variation — 400 is correct
  letterSpacing: 12,
  color: 'white',
  textTransform: 'uppercase',
  lineHeight: 1,
};

// Tagline — Oswald Light (subdued)
const TAGLINE_STYLE: React.CSSProperties = {
  fontFamily: oswaldFont,
  fontSize: 32,
  fontWeight: 300,
  letterSpacing: 8,
  color: 'rgba(255,255,255,0.7)',
  textTransform: 'uppercase',
};

// Drama — Playfair Display (elegant / prestige)
const DRAMA_TITLE_STYLE: React.CSSProperties = {
  fontFamily: playfairFont,
  fontSize: 120,
  fontWeight: 700,
  fontStyle: 'italic',
  color: '#c8a96e',   // champagne gold
  letterSpacing: 4,
};
```

### Letter-by-Letter Title Reveal (Hollywood Standard)

```tsx
export const HollywoodTitle: React.FC<{
  title: string;
  tagline?: string;
  style?: 'action' | 'drama' | 'thriller';
}> = ({ title, tagline, style = 'action' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const letters = title.toUpperCase().split('');
  const framesPerLetter = 3;
  const titleDone = letters.length * framesPerLetter + 20;

  const accentColor = { action: '#c8a96e', drama: '#c8a96e', thriller: '#cc2200' }[style];

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 24 }}>
      {/* Title letters */}
      <div style={{ display: 'flex', alignItems: 'center' }}>
        {letters.map((letter, i) => {
          const start = i * framesPerLetter;
          const opacity = interpolate(frame - start, [0, 8], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });
          const y = interpolate(frame - start, [0, 10], [16, 0], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            easing: Easing.out(Easing.quad),
          });
          return (
            <span key={i} style={{
              ...TITLE_STYLE,
              opacity,
              transform: `translateY(${y}px)`,
              display: 'inline-block',
            }}>
              {letter === ' ' ? '\u00A0' : letter}
            </span>
          );
        })}
      </div>

      {/* Accent rule */}
      <div style={{
        height: 2,
        backgroundColor: accentColor,
        width: interpolate(frame, [titleDone - 20, titleDone], [0, 480], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        }),
      }} />

      {/* Tagline */}
      {tagline && (
        <span style={{
          ...TAGLINE_STYLE,
          opacity: interpolate(frame, [titleDone, titleDone + 20], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          }),
        }}>
          {tagline}
        </span>
      )}
    </AbsoluteFill>
  );
};
```

---

## 7. Cinematic Lens Flare

```tsx
export const LensFlare: React.FC<{
  x?: number; y?: number;
  triggerFrame?: number;
  color?: string;
}> = ({ x = 320, y = 240, triggerFrame = 0, color = '#fff5cc' }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [triggerFrame, triggerFrame + 6, triggerFrame + 28, triggerFrame + 48],
    [0, 0.92, 0.55, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  if (opacity <= 0) return null;

  // Opposite orbs travel across frame from light source
  const cx = 960, cy = 540;
  const orbs = [0.28, 0.5, 0.72, 0.9].map((t) => ({
    x: cx + (cx - x) * t,
    y: cy + (cy - y) * t,
    r: [50, 28, 36, 18][Math.round(t * 3)] ?? 24,
  }));

  return (
    <AbsoluteFill style={{ opacity, pointerEvents: 'none', zIndex: 170 }}>
      {/* Main flare bloom */}
      <div style={{
        position: 'absolute',
        left: x - 100, top: y - 100,
        width: 200, height: 200, borderRadius: '50%',
        background: `radial-gradient(circle, ${color}cc 0%, ${color}44 40%, transparent 70%)`,
        filter: 'blur(6px)',
      }} />
      {/* Horizontal streak */}
      <div style={{
        position: 'absolute',
        left: 0, top: y - 2,
        width: '100%', height: 4,
        background: `linear-gradient(90deg, transparent, ${color}55 40%, ${color}99 50%, ${color}55 60%, transparent)`,
        filter: 'blur(2px)',
      }} />
      {/* Bokeh orbs */}
      {orbs.map((orb, i) => (
        <div key={i} style={{
          position: 'absolute',
          left: orb.x - orb.r, top: orb.y - orb.r,
          width: orb.r * 2, height: orb.r * 2, borderRadius: '50%',
          background: `radial-gradient(circle, ${color}88 0%, transparent 70%)`,
          filter: 'blur(3px)',
        }} />
      ))}
    </AbsoluteFill>
  );
};
```

---

## 8. Genre Scene Structures

```tsx
// BLOCKBUSTER TRAILER (2.5 min)
const BLOCKBUSTER = [
  { id: 'cold-open',   sec: 8,   grade: 'teal-orange', blur: 180 },
  { id: 'title-smash', sec: 3,   grade: 'natural',      blur: 90  },
  { id: 'act1',        sec: 25,  grade: 'teal-orange', blur: 180 },
  { id: 'rising',      sec: 20,  grade: 'teal-orange', blur: 180 },
  { id: 'climax',      sec: 15,  grade: 'teal-orange', blur: 270 },
  { id: 'main-title',  sec: 5,   grade: 'natural',      blur: 90  },
  { id: 'credits',     sec: 8,   grade: 'natural',      blur: 90  },
];

// DRAMA / PRESTIGE (per scene)
const DRAMA_GRADES = {
  'day-exterior':  'golden-hour',
  'night-city':    'teal-orange',
  'interior-warm': 'golden-hour',
  'flashback':     'western',
  'climax':        'bleach-bypass',
};

// HORROR (escalating desaturation)
// Start near-natural, degrade to full horror grade as tension rises
const horrorGradeAtFrame = (frame: number, fps: number): string => {
  const progress = Math.min(frame / (fps * 90), 1); // 90 second arc
  const sat = interpolate(progress, [0, 1], [0.8, 0.25]);
  const contrast = interpolate(progress, [0, 1], [1.1, 1.6]);
  const brightness = interpolate(progress, [0, 1], [0.95, 0.72]);
  return `contrast(${contrast}) saturate(${sat}) brightness(${brightness})`;
};
```

---

## 9. Rack Focus (Depth of Field)

```tsx
export const RackFocus: React.FC<{
  children: React.ReactNode;
  fromBlur?: number;
  toBlur?: number;
  startFrame?: number;
  durationFrames?: number;
}> = ({ children, fromBlur = 8, toBlur = 0, startFrame = 0, durationFrames = 24 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 60, stiffness: 120 },
    durationInFrames: durationFrames,
  });
  const blur = interpolate(progress, [0, 1], [fromBlur, toBlur]);

  return (
    <AbsoluteFill style={{ filter: `blur(${blur}px)` }}>
      {children}
    </AbsoluteFill>
  );
};

// Usage: rack focus IN to reveal character
<RackFocus fromBlur={10} toBlur={0} startFrame={30} durationFrames={20}>
  <CharacterScene />
</RackFocus>
```

---

## 10. Halation (Film Glow on Bright Edges)

A subtle film effect: bright areas bleed warm orange-red light onto their surroundings.

```tsx
export const Halation: React.FC<{ children: React.ReactNode; intensity?: number }> = ({
  children, intensity = 0.18,
}) => (
  <AbsoluteFill>
    {children}
    {/* Halation layer: multiply-blended warm blur over bright areas */}
    <AbsoluteFill style={{
      filter: 'blur(24px) saturate(2) hue-rotate(-15deg)',
      opacity: intensity,
      mixBlendMode: 'screen',
    }}>
      {children}
    </AbsoluteFill>
  </AbsoluteFill>
);
```

---

## Required Packages

```bash
npm i @remotion/motion-blur @remotion/google-fonts @remotion/noise @remotion/light-leaks
```

## Cross-References
- `rules/effects.md` → CameraMotionBlur, Trail, noise2D (organic camera shake), LightLeak
- `rules/transitions.md` → `@remotion/transitions` wipe/iris for cuts
- `rules/rendering.md` → `--crf 16 --codec h264` for high quality output, 4K render flags
