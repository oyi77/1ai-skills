# ASMR / Sensory Video in Remotion

## Why ASMR Converts

ASMR is the #3 most-watched content category globally (Statista 2025, behind music and comedy). Sensory content creates parasocial trust faster than any other format — viewers relax, their guard drops, and they absorb brand messaging subconsciously. Brands using ASMR UGC see significantly higher completion rates and lower CPM on paid placements.

ASMR in Remotion = **extreme close-ups, slow motion, macro textures, satisfying reveals, organic colour palettes**.

---

## The ASMR Visual Grammar

ASMR is not just sound — it has a precise visual language:

```tsx
export const ASMR_RULES = {
  movement:   'Slow, deliberate, unhurried — never fast cuts',
  focus:      'Shallow depth of field — extreme macro, soft background blur',
  colour:     'Warm pastels, earth tones, soft neutrals — never harsh neons',
  lighting:   'Soft diffused light — no harsh shadows, no flicker',
  composition:'Center-heavy — subject fills 60-80% of frame',
  cuts:       'Slow dissolves or wipes — never jump cuts',
  pace:       'Min 3 seconds per shot — preferably 6-12',
};

// Colour palette: earth tones + pastels
export const ASMR_PALETTE = {
  cream:      '#F5F0E8',
  warm_white: '#FDF6EC',
  sage:       '#B7C9A8',
  terracotta: '#C97B4B',
  dusty_pink: '#D4A5A5',
  slate:      '#8DA3A6',
  walnut:     '#5C3D2E',
  honey:      '#E8A838',
};
```

---

## Macro Texture Scene

Simulating extreme close-up textures — the core ASMR visual:

```tsx
export const MacroTextureScene: React.FC<{
  imageSrc: string;
  revealDirection?: 'top' | 'left' | 'zoom-in' | 'dissolve';
  durationSecs?: number;
  slowZoom?: boolean;
}> = ({ imageSrc, revealDirection = 'dissolve', durationSecs = 4, slowZoom = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const totalFrames = durationSecs * fps;

  // ASMR signature: ultra-slow Ken Burns zoom
  const zoomScale = slowZoom
    ? interpolate(frame, [0, totalFrames], [1.0, 1.08], { extrapolateRight: 'clamp' })
    : 1;

  const zoomX = slowZoom
    ? interpolate(frame, [0, totalFrames], [0, -2], { extrapolateRight: 'clamp' })
    : 0;

  // Reveal animation
  const revealProgress = interpolate(frame, [0, fps * 1.5], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  const revealStyle: React.CSSProperties = {
    dissolve: { opacity: revealProgress },
    'zoom-in': { transform: `scale(${interpolate(revealProgress, [0, 1], [1.15, 1])})`, opacity: revealProgress },
    top: { clipPath: `inset(${(1 - revealProgress) * 100}% 0 0 0)` },
    left: { clipPath: `inset(0 ${(1 - revealProgress) * 100}% 0 0)` },
  }[revealDirection] ?? { opacity: revealProgress };

  return (
    <AbsoluteFill style={{
      ...revealStyle,
      overflow: 'hidden',
    }}>
      <Img
        src={staticFile(imageSrc)}
        style={{
          width: '100%', height: '100%',
          objectFit: 'cover',
          transform: `scale(${zoomScale}) translateX(${zoomX}%)`,
          // Soft, slightly desaturated for ASMR warmth
          filter: 'contrast(1.04) saturate(0.88) brightness(1.06)',
        }}
      />
    </AbsoluteFill>
  );
};
```

---

## Slow-Motion Product Reveal

ASMR brand content hallmark — products revealed at 0.25× speed with soft lighting:

```tsx
export const ASMRProductReveal: React.FC<{
  productVideo: string;
  productName: string;
  tagline?: string;
  bgColor?: string;
}> = ({
  productVideo, productName, tagline,
  bgColor = '#F5F0E8',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Product name fades in after 2 seconds
  const textOpacity = interpolate(frame, [fps * 2, fps * 3.5], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const textY = interpolate(frame, [fps * 2, fps * 3.5], [12, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      {/* Slow-motion video */}
      <OffthreadVideo
        src={staticFile(productVideo)}
        playbackRate={0.3}   // Extreme slow motion
        style={{
          width: '100%', height: '100%', objectFit: 'cover',
          filter: 'saturate(0.85) brightness(1.08)',
        }}
        muted
      />

      {/* Soft vignette — ASMR essential */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 50% 50%, transparent 50%, rgba(0,0,0,0.2) 100%)',
      }} />

      {/* Product name — minimal, tasteful */}
      <div style={{
        position: 'absolute', bottom: 80, left: 0, right: 0,
        textAlign: 'center',
        opacity: textOpacity,
        transform: `translateY(${textY}px)`,
      }}>
        <div style={{
          fontSize: 48, fontWeight: 300, color: '#3d2b1a',
          letterSpacing: 8, textTransform: 'uppercase',
          fontFamily: 'Georgia, serif',
        }}>
          {productName}
        </div>
        {tagline && (
          <div style={{
            fontSize: 24, color: '#8b6914', marginTop: 8,
            letterSpacing: 4, fontStyle: 'italic',
          }}>
            {tagline}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Satisfying Sequence (The Loop)

The most viral ASMR format — something satisfying that loops seamlessly:

```tsx
// Honey pour, soap cut, kinetic sand — implemented via CSS animation on frame
export const SatisfyingLoop: React.FC<{
  type: 'pour' | 'cut' | 'swirl' | 'bubble';
  color?: string;
}> = ({ type, color = '#E8A838' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Loop every 3 seconds
  const loopFrame = frame % (fps * 3);
  const progress = loopFrame / (fps * 3);

  const TYPES = {
    pour: () => {
      // Simulate honey pour with SVG path
      const pourHeight = interpolate(progress, [0, 0.8, 1], [0, 400, 0]);
      const droop = Math.sin(progress * Math.PI * 2) * 20;
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'flex-start', paddingTop: 100 }}>
          <svg viewBox="0 0 400 500" style={{ width: 400, height: 500 }}>
            {/* Pour stream */}
            <path
              d={`M 180 0 Q ${200 + droop} ${pourHeight / 2} 200 ${pourHeight}`}
              stroke={color} strokeWidth={12} fill="none"
              strokeLinecap="round"
              opacity={0.8}
            />
            {/* Pool at bottom */}
            <ellipse cx={200} cy={pourHeight} rx={60 + progress * 20} ry={12}
              fill={color} opacity={0.7} />
          </svg>
        </AbsoluteFill>
      );
    },

    swirl: () => {
      const rotation = progress * 720; // 2 full rotations per loop
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
          <div style={{
            width: 500, height: 500, borderRadius: '50%',
            background: `conic-gradient(${color}, ${color}88, ${color}, ${color}44, ${color})`,
            transform: `rotate(${rotation}deg)`,
            filter: `blur(${interpolate(progress, [0, 0.5, 1], [0, 4, 0])}px)`,
          }} />
        </AbsoluteFill>
      );
    },

    bubble: () => {
      const scale = spring({ frame: loopFrame, fps: fps, config: { damping: 8, stiffness: 200 } });
      const burstOpacity = interpolate(loopFrame, [fps * 2.5, fps * 3], [1, 0], {
        extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
      });
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
          <div style={{
            width: 200, height: 200,
            borderRadius: '50%',
            border: `4px solid ${color}`,
            background: `radial-gradient(circle at 35% 35%, white, ${color}44)`,
            transform: `scale(${interpolate(scale, [0, 1], [0.2, 1.3])})`,
            opacity: burstOpacity,
          }} />
        </AbsoluteFill>
      );
    },

    cut: () => {
      const cutX = interpolate(progress, [0, 0.6], [0, 600], { extrapolateRight: 'clamp' });
      return (
        <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
          <div style={{ position: 'relative', width: 600, height: 300 }}>
            {/* Object being cut */}
            <div style={{
              position: 'absolute', inset: 0,
              backgroundColor: color,
              borderRadius: 12,
              clipPath: `polygon(${cutX}px 0%, 100% 0%, 100% 100%, ${cutX}px 100%)`,
            }} />
            <div style={{
              position: 'absolute', inset: 0,
              backgroundColor: `${color}cc`,
              borderRadius: 12,
              clipPath: `polygon(0% 0%, ${cutX}px 0%, ${cutX}px 100%, 0% 100%)`,
              transform: `translateX(${progress > 0.6 ? (progress - 0.6) * 60 : 0}px)`,
            }} />
          </div>
        </AbsoluteFill>
      );
    },
  };

  return TYPES[type]?.() ?? null;
};
```

---

## ASMR Colour Grade

```tsx
export const ASMRGrade: React.FC<{
  children: React.ReactNode;
  warmth?: 'cool' | 'neutral' | 'warm';
}> = ({ children, warmth = 'warm' }) => {
  const FILTERS = {
    cool:    'contrast(1.04) saturate(0.82) brightness(1.05) hue-rotate(-8deg)',
    neutral: 'contrast(1.05) saturate(0.88) brightness(1.06)',
    warm:    'contrast(1.04) saturate(0.90) brightness(1.08) sepia(0.06)',
  };

  return (
    <AbsoluteFill style={{ filter: FILTERS[warmth] }}>
      {children}
    </AbsoluteFill>
  );
};
```

---

## ASMR Video Structure (30–60 seconds)

```tsx
const ASMR_AD_STRUCTURE = [
  { sec: 2,  type: 'macro-open',    note: 'Extreme close-up of texture — no logo, no text' },
  { sec: 8,  type: 'slow-reveal',   note: 'Product pulled into frame in slow motion' },
  { sec: 12, type: 'texture-detail',note: 'Pan across surfaces — tactile visual language' },
  { sec: 8,  type: 'use-moment',    note: 'Product used at 0.5× speed' },
  { sec: 6,  type: 'result',        note: 'Satisfying payoff shot' },
  { sec: 4,  type: 'product-beauty',note: 'Clean product-on-surface final frame' },
  // No aggressive CTA — soft text overlay: website or handle only
];
```

---

## Cross-References
- `genres/viral-formula.md` — ASMR drives completion → algorithm rewards
- `genres/product.md` — combine ASMR aesthetic with product showcase
- `rules/video.md` — `playbackRate={0.25}` for slow motion
- `rules/effects.md` — `noise2D` for organic camera drift
- `rules/audio.md` — ASMR requires spatial/binaural audio design notes
