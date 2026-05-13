# Japan Anime / Sakuga-Quality Video in Remotion

## The Japan Studio Standard

Professional Japanese anime (sakuga level) is defined by six distinguishing techniques:
1. **Limited animation used deliberately** — holds, partial movement, and cuts ARE the style. Don't over-animate.
2. **Smear frames** — exaggerated distortion blur on fast hits, never motion blur
3. **Impact frames** — flash white/colour at the peak of every significant hit
4. **Anticipation + overshoot** — every action telegraphed, every spring overshoots
5. **Speed lines as SVG** — radial, directional, or rotation speed lines drawn fresh every frame
6. **Layered depth** — parallax separation between background, midground, and character layers

---

## Layer Architecture (Anime Compositor Stack)

```tsx
// Every anime scene reads bottom → top:
export const AnimeScene: React.FC<{
  children: React.ReactNode;
  grade?: AnimeGrade;
}> = ({ children, grade = 'shonen' }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      {/* 1. Background — parallax, painterly, static or slow pan */}
      <AnimeBackground grade={grade} />

      {/* 2. Midground effects (dust, atmospheric) */}
      <AtmosphericLayer grade={grade} />

      {/* 3. Character + action layer */}
      <AbsoluteFill style={{ filter: ANIME_CEL_FILTER }}>
        {children}
      </AbsoluteFill>

      {/* 4. Speed lines and impact effects on top of character */}
      <SpeedLineLayer frame={frame} />

      {/* 5. Flash / impact frame — absolute top */}
      <ImpactLayer frame={frame} />
    </AbsoluteFill>
  );
};
```

---

## 1. Cel-Shading Filter Stack

The exact CSS filter combination that mimics hand-painted anime cels:

```tsx
// Core cel-shading filter — apply to character/object layer
export const ANIME_CEL_FILTER =
  'contrast(1.35) saturate(1.5) brightness(1.02)';

// Hard ink outline — for characters against background
export const inkOutline = (px = 2): React.CSSProperties => ({
  filter: [
    `drop-shadow(${px}px ${px}px 0 #000)`,
    `drop-shadow(-${px}px -${px}px 0 #000)`,
    `drop-shadow(${px}px -${px}px 0 #000)`,
    `drop-shadow(-${px}px ${px}px 0 #000)`,
  ].join(' '),
});

// Usage
<div style={{ filter: ANIME_CEL_FILTER }}>
  <Img src={staticFile('character.png')} style={inkOutline(3)} />
</div>
```

---

## 2. Anime Color Palettes (Studio-Accurate)

```tsx
type AnimeGrade = 'shonen' | 'shoujo' | 'mecha' | 'isekai' | 'slice-of-life' | 'dark';

export const ANIME_PALETTES: Record<AnimeGrade, {
  primary: string; accent: string; shadow: string;
  bg: string; bgGrad: string; filter: string;
}> = {
  // Jump-style action: Naruto, MHA, Demon Slayer, Jujutsu Kaisen
  shonen: {
    primary: '#FF4500', accent: '#FFD700', shadow: '#1a0a00',
    bg: '#87CEEB', bgGrad: 'linear-gradient(180deg, #87CEEB 0%, #E0F0FF 60%, #F5E6C8 100%)',
    filter: 'contrast(1.3) saturate(1.6) brightness(1.05)',
  },
  // Romance: Sailor Moon, Cardcaptor, Fruits Basket
  shoujo: {
    primary: '#FF69B4', accent: '#9370DB', shadow: '#1a0011',
    bg: '#FFF0F8', bgGrad: 'linear-gradient(180deg, #FFD6EC 0%, #FFF0F8 50%, #E8D6FF 100%)',
    filter: 'contrast(1.1) saturate(1.4) brightness(1.08) hue-rotate(-5deg)',
  },
  // Gundam, Evangelion, Code Geass, mech battles
  mecha: {
    primary: '#00AAFF', accent: '#FF3300', shadow: '#000d1a',
    bg: '#0a0a1a', bgGrad: 'linear-gradient(180deg, #050510 0%, #0a0a2a 100%)',
    filter: 'contrast(1.4) saturate(1.3) brightness(0.95) hue-rotate(-10deg)',
  },
  // Another World: Re:Zero, Konosuba, Sword Art Online
  isekai: {
    primary: '#7B68EE', accent: '#FFD700', shadow: '#0a0514',
    bg: '#1a0f2e', bgGrad: 'linear-gradient(180deg, #0d0720 0%, #1a0f3a 50%, #2a1a50 100%)',
    filter: 'contrast(1.25) saturate(1.5) brightness(1.0)',
  },
  // Everyday: K-On, Clannad, Yotsuba, My Hero daily life
  'slice-of-life': {
    primary: '#4FC3F7', accent: '#FFCC80', shadow: '#1a1a1a',
    bg: '#FFF8E7', bgGrad: 'linear-gradient(180deg, #B3E5FC 0%, #FFF8E7 60%, #DCEDC8 100%)',
    filter: 'contrast(1.1) saturate(1.2) brightness(1.1)',
  },
  // Berserk, Vinland Saga, Attack on Titan — heavy, desaturated
  dark: {
    primary: '#8B0000', accent: '#C0A060', shadow: '#0a0000',
    bg: '#1a1008', bgGrad: 'linear-gradient(180deg, #0a0806 0%, #1a1008 100%)',
    filter: 'contrast(1.5) saturate(0.7) brightness(0.85)',
  },
};
```

---

## 3. Speed Lines (Sakuga Essential)

```tsx
// Radial speed lines — used for impact, reveal, power-up
export const RadialSpeedLines: React.FC<{
  count?: number;
  cx?: number; cy?: number;
  color?: string;
  opacity?: number;
  animate?: boolean;
}> = ({ count = 36, cx = 960, cy = 540, color = 'white', opacity = 1, animate = true }) => {
  const frame = useCurrentFrame();

  // Slight rotation animation for "charging" effect
  const rotation = animate ? (frame % 360) * 0.5 : 0;

  return (
    <AbsoluteFill style={{ opacity, pointerEvents: 'none' }}>
      <svg viewBox="0 0 1920 1080" style={{ width: '100%', height: '100%' }}>
        <g transform={`rotate(${rotation}, ${cx}, ${cy})`}>
          {Array.from({ length: count }).map((_, i) => {
            const angle = (i / count) * 2 * Math.PI;
            const innerR = 60 + (i % 3) * 20;
            const outerR = 640 + (i % 5) * 80;
            const lineW  = 1 + (i % 4);
            const alpha  = 0.25 + (i % 3) * 0.15;
            return (
              <line
                key={i}
                x1={cx + Math.cos(angle) * innerR}
                y1={cy + Math.sin(angle) * innerR}
                x2={cx + Math.cos(angle) * outerR}
                y2={cy + Math.sin(angle) * outerR}
                stroke={color}
                strokeWidth={lineW}
                opacity={alpha}
              />
            );
          })}
        </g>
      </svg>
    </AbsoluteFill>
  );
};

// Directional speed lines — used for movement, dash, charge
export const DirectionalSpeedLines: React.FC<{
  direction?: 'left' | 'right' | 'up' | 'down';
  count?: number;
  color?: string;
  opacity?: number;
}> = ({ direction = 'right', count = 24, color = 'white', opacity = 0.7 }) => {
  const frame = useCurrentFrame();
  const offset = (frame * 60) % 120; // lines scroll

  const isHorizontal = direction === 'left' || direction === 'right';

  return (
    <AbsoluteFill style={{ opacity, pointerEvents: 'none', overflow: 'hidden' }}>
      <svg viewBox="0 0 1920 1080" style={{ width: '100%', height: '100%' }}>
        {Array.from({ length: count }).map((_, i) => {
          const t = i / count;
          const len = 300 + Math.random() * 600;
          const thick = 1 + (i % 4) * 0.7;

          if (isHorizontal) {
            const y = t * 1080;
            const x = direction === 'right'
              ? ((i * 80 + offset) % 1920) - len
              : 1920 - ((i * 80 + offset) % 1920);
            return <line key={i} x1={x} y1={y} x2={x + len} y2={y}
              stroke={color} strokeWidth={thick} opacity={0.15 + t * 0.4} />;
          } else {
            const x = t * 1920;
            const y = direction === 'down'
              ? ((i * 60 + offset) % 1080) - len
              : 1080 - ((i * 60 + offset) % 1080);
            return <line key={i} x1={x} y1={y} x2={x} y2={y + len}
              stroke={color} strokeWidth={thick} opacity={0.15 + t * 0.4} />;
          }
        })}
      </svg>
    </AbsoluteFill>
  );
};
```

---

## 4. Smear Frames (The Sakuga Secret)

Smears are intentional distortion on fast-moving objects — not motion blur. They're exaggerated, stylised, and only last 1–3 frames. This is what separates good anime from great sakuga.

```tsx
// Apply to a character/object during the peak frame of a fast action
export const SmearFrame: React.FC<{
  children: React.ReactNode;
  triggerFrame: number;
  direction?: 'horizontal' | 'vertical' | 'diagonal';
  intensity?: number;  // 0–1
}> = ({ children, triggerFrame, direction = 'horizontal', intensity = 0.8 }) => {
  const frame = useCurrentFrame();

  // Smear is only active for 2 frames at peak
  const isSmearing = frame === triggerFrame || frame === triggerFrame + 1;
  const smearFrame = frame - triggerFrame; // 0 or 1

  if (!isSmearing) return <>{children}</>;

  // Peak smear on frame 0, slight recovery on frame 1
  const smearAmount = smearFrame === 0 ? intensity : intensity * 0.4;

  const smearFilter = {
    horizontal: `blur(${smearAmount * 18}px, 0)`,
    vertical:   `blur(0, ${smearAmount * 18}px)`,
    diagonal:   `blur(${smearAmount * 12}px)`,
  }[direction];

  return (
    <div style={{
      // CSS filter blur approximates smear — skew adds the stretch
      filter: `blur(${smearAmount * 8}px)`,
      transform: direction === 'horizontal'
        ? `scaleX(${1 + smearAmount * 0.6}) scaleY(${1 - smearAmount * 0.25})`
        : direction === 'vertical'
        ? `scaleY(${1 + smearAmount * 0.6}) scaleX(${1 - smearAmount * 0.25})`
        : `skewX(${smearAmount * 15}deg) scaleX(${1 + smearAmount * 0.3})`,
    }}>
      {children}
    </div>
  );
};
```

---

## 5. Impact Frames

Three types — white flash (standard hit), colour flash (elemental power), and manga halftone (comedic/dramatic).

```tsx
// Standard white flash — 1–3 frames, used for every significant hit
export const WhiteFlash: React.FC<{ triggerFrame: number; durationFrames?: number }> = ({
  triggerFrame, durationFrames = 3,
}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - triggerFrame;

  const opacity = interpolate(localFrame, [0, 1, durationFrames], [0, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: 'white',
      opacity,
      zIndex: 300,
      pointerEvents: 'none',
    }} />
  );
};

// Colour flash — use for power-ups, magic attacks, elemental hits
export const ColorFlash: React.FC<{
  triggerFrame: number;
  color: string;        // e.g. '#ff4400' for fire, '#00aaff' for water
  durationFrames?: number;
}> = ({ triggerFrame, color, durationFrames = 4 }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - triggerFrame;

  const opacity = interpolate(localFrame, [0, 1, durationFrames], [0, 0.85, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: color,
      opacity,
      mixBlendMode: 'screen',
      zIndex: 290,
      pointerEvents: 'none',
    }} />
  );
};

// Manga halftone impact — dramatic reveal or comedic moment
export const HalftoneFlash: React.FC<{ triggerFrame: number }> = ({ triggerFrame }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - triggerFrame;

  const opacity = interpolate(localFrame, [0, 2, 8], [0, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const scale = interpolate(localFrame, [0, 4], [1.4, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ opacity, transform: `scale(${scale})`, pointerEvents: 'none', zIndex: 280 }}>
      <svg width="100%" height="100%" viewBox="0 0 1920 1080">
        <defs>
          <pattern id="halftone-impact" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
            <circle cx="12" cy="12" r="9" fill="#ff2200" />
          </pattern>
          {/* Radial gradient mask to fade out from edges */}
          <radialGradient id="radial-mask" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="white" stopOpacity="1" />
            <stop offset="75%" stopColor="white" stopOpacity="0.5" />
            <stop offset="100%" stopColor="white" stopOpacity="0" />
          </radialGradient>
          <mask id="fade-mask">
            <rect width="1920" height="1080" fill="url(#radial-mask)" />
          </mask>
        </defs>
        <rect width="1920" height="1080" fill="url(#halftone-impact)" mask="url(#fade-mask)" opacity="0.85" />
      </svg>
    </AbsoluteFill>
  );
};
```

---

## 6. Screen Shake (Bure / 画ブレ)

Camera shake is a professional anime technique called *bure* (ぶれ). Use organic noise, not Math.random().

```tsx
import { noise2D } from '@remotion/noise';

export const ScreenShake: React.FC<{
  children: React.ReactNode;
  startFrame: number;
  durationFrames?: number;
  intensity?: number;   // pixels at peak
  decay?: boolean;      // true = shake decays over duration
}> = ({ children, startFrame, durationFrames = 16, intensity = 14, decay = true }) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;

  const isActive = localFrame >= 0 && localFrame < durationFrames;
  if (!isActive) return <>{children}</>;

  // Decay the shake over time
  const decayFactor = decay
    ? 1 - (localFrame / durationFrames)
    : 1;

  const x = noise2D('shake-x', localFrame * 0.8, 0) * intensity * decayFactor;
  const y = noise2D('shake-y', localFrame * 0.8, 1) * intensity * 0.6 * decayFactor;
  const r = noise2D('shake-r', localFrame * 0.6, 2) * 1.2 * decayFactor;

  return (
    <AbsoluteFill style={{
      transform: `translate(${x}px, ${y}px) rotate(${r}deg)`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
```

---

## 7. Dramatic Zoom (Power Reveal / Super Move)

```tsx
export const SakugaZoom: React.FC<{
  children: React.ReactNode;
  startFrame: number;
  fromScale?: number;
  toScale?: number;
  style?: 'slam' | 'rise' | 'burst';
}> = ({ children, startFrame, fromScale = 0.3, toScale = 1, style = 'slam' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const springConfig = {
    slam:  { damping: 6,  stiffness: 400, mass: 0.6 },  // hard snap with bounce
    rise:  { damping: 18, stiffness: 180, mass: 1.0 },  // smooth rise
    burst: { damping: 4,  stiffness: 600, mass: 0.4 },  // explosive pop
  }[style];

  const progress = spring({ frame: frame - startFrame, fps, config: springConfig });
  const scale = interpolate(progress, [0, 1], [fromScale, toScale]);
  const opacity = interpolate(frame - startFrame, [0, 5], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})`, opacity }}>
      {children}
    </AbsoluteFill>
  );
};
```

---

## 8. Anticipation + Overshoot Pattern

The animation principle at the core of sakuga: every action has a wind-up (anticipation) and every fast move overshoots slightly before settling.

```tsx
// Punch anticipation → strike → overshoot → settle
export const AnticipateAndStrike: React.FC<{
  children: React.ReactNode;
  startFrame: number;
}> = ({ children, startFrame }) => {
  const frame = useCurrentFrame();
  const f = frame - startFrame;

  // Phase 1: Anticipation — pull BACK (frames 0–8)
  // Phase 2: Strike — slam FORWARD past target (frames 8–14)
  // Phase 3: Settle (frames 14–28 via spring)

  const { fps } = useVideoConfig();

  let x = 0;
  if (f >= 0 && f < 8) {
    // Anticipation: pull back
    x = interpolate(f, [0, 8], [0, -40], { extrapolateRight: 'clamp' });
  } else if (f >= 8 && f < 14) {
    // Strike: blast forward past 0
    x = interpolate(f, [8, 11], [-40, 80], {
      extrapolateRight: 'clamp',
      easing: Easing.in(Easing.cubic),
    });
  } else {
    // Settle with spring
    const settle = spring({ frame: f - 14, fps, config: { damping: 12, stiffness: 300 } });
    x = interpolate(settle, [0, 1], [80, 0]);
  }

  return (
    <AbsoluteFill style={{ transform: `translateX(${x}px)` }}>
      {children}
    </AbsoluteFill>
  );
};
```

---

## 9. Parallax Background

Anime backgrounds are painted separately. Depth is created by moving layers at different rates.

```tsx
export const AnimeBackground: React.FC<{ grade: AnimeGrade; scrollX?: number }> = ({
  grade, scrollX = 0,
}) => {
  const { bgGrad } = ANIME_PALETTES[grade];

  return (
    <AbsoluteFill>
      {/* Sky */}
      <AbsoluteFill style={{ background: bgGrad }} />

      {/* Far background — moves 20% of camera speed */}
      <div style={{
        position: 'absolute', inset: 0,
        transform: `translateX(${scrollX * 0.2}px)`,
      }}>
        {/* Mountains / city silhouette — add image or SVG here */}
      </div>

      {/* Midground — moves 50% */}
      <div style={{
        position: 'absolute', inset: 0,
        transform: `translateX(${scrollX * 0.5}px)`,
      }}>
        {/* Trees / buildings mid-layer */}
      </div>

      {/* Foreground — moves 100% (same as character) */}
      <div style={{
        position: 'absolute', inset: 0,
        transform: `translateX(${scrollX}px)`,
      }}>
        {/* Ground / foreground elements */}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 10. Action Scene Full Template

```tsx
const ACTION_BEATS = [
  { frame: 0,   type: 'anticipate', smearDir: 'horizontal' },
  { frame: 14,  type: 'smear',      smearDir: 'horizontal' },
  { frame: 16,  type: 'impact-white' },
  { frame: 16,  type: 'shake',      duration: 14 },
  { frame: 30,  type: 'speedlines', radial: true },
  { frame: 45,  type: 'impact-color', color: '#ff4400' },
  { frame: 60,  type: 'dramatic-zoom' },
];

export const AnimeActionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const palette = ANIME_PALETTES['shonen'];

  return (
    <AbsoluteFill style={{ filter: palette.filter }}>
      <AnimeBackground grade="shonen" />

      {/* Speed lines (radial at impact) */}
      {frame >= 16 && frame < 60 && (
        <RadialSpeedLines cx={960} cy={540} color="white" opacity={0.6} animate />
      )}

      {/* Character with smear at frame 14 */}
      <ScreenShake startFrame={16} durationFrames={14} intensity={16}>
        <SmearFrame triggerFrame={14} direction="horizontal" intensity={0.85}>
          <CharacterLayer />
        </SmearFrame>
      </ScreenShake>

      {/* Impact frames */}
      <WhiteFlash triggerFrame={16} durationFrames={3} />
      <ColorFlash triggerFrame={45} color={palette.primary} durationFrames={4} />

      {/* Dramatic reveal */}
      {frame >= 60 && (
        <>
          <RadialSpeedLines opacity={0.9} animate={false} />
          <SakugaZoom startFrame={60} fromScale={0.2} style="burst">
            <TitleCard />
          </SakugaZoom>
        </>
      )}
    </AbsoluteFill>
  );
};
```

---

## Anime Typography

```tsx
// Bebas Neue — action titles with stroke
const ANIME_TITLE: React.CSSProperties = {
  fontFamily: bebasFont,
  fontSize: 120,
  fontWeight: 400,
  color: 'white',
  textShadow: '4px 4px 0 #000, -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000',
  letterSpacing: 6,
};

// Japanese title style — all-caps, gold accent
const ANIME_SUBTITLE: React.CSSProperties = {
  fontFamily: oswaldFont,
  fontSize: 36,
  fontWeight: 700,
  color: '#FFD700',
  letterSpacing: 12,
  textTransform: 'uppercase',
};
```

---

## Required Packages

```bash
npm i @remotion/noise @remotion/google-fonts @remotion/motion-blur
```

## Cross-References
- `rules/effects.md` → `noise2D` for organic shake, `@remotion/paths` for SVG speed-line paths
- `rules/effects.md` → `<Trail>` from @remotion/motion-blur for afterimage effects
- `rules/transitions.md` → cut-heavy editing (iris, flash cuts)
- `rules/text.md` → word-by-word Japanese subtitle display
