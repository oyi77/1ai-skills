# Comedy / Sketch / Meme Video in Remotion

## Why Comedy Converts

Comedy is the #2 most-watched content globally. It drives the highest share rate of any format — people share things that made them laugh. Meme-format videos have extremely low CPM on paid ads because organic reach replaces paid.

The comedy formula: **Setup → Subversion → Payoff**. Every joke is a broken expectation.

---

## Comedy Visual Grammar

```tsx
// The typography of comedy
export const COMEDY_TEXT_RULES = {
  // Impact meme font — all-caps, white, black stroke
  meme:     { fontFamily: 'Impact, Arial Black', fontWeight: 900, textTransform: 'uppercase' as const },
  // Sarcastic subtitle style
  caption:  { fontFamily: 'Arial, sans-serif', fontWeight: 600, fontStyle: 'italic' as const },
  // Reaction text — large, centred
  reaction: { fontFamily: 'Arial Black', fontWeight: 900 },
};
```

---

## Meme Text Overlay (Impact Font Style)

```tsx
export const MemeText: React.FC<{
  topText?: string;
  bottomText?: string;
  color?: string;
}> = ({ topText, bottomText, color = 'white' }) => {
  const strokeStyle: React.CSSProperties = {
    color,
    fontFamily: 'Impact, Arial Black, sans-serif',
    fontWeight: 900,
    textTransform: 'uppercase',
    fontSize: 72,
    textAlign: 'center',
    lineHeight: 1.1,
    padding: '0 40px',
    // CSS text-stroke approximation
    textShadow: [
      '-3px -3px 0 #000', '3px -3px 0 #000',
      '-3px 3px 0 #000', '3px 3px 0 #000',
      '-3px 0 0 #000', '3px 0 0 #000',
      '0 -3px 0 #000', '0 3px 0 #000',
    ].join(', '),
  };

  return (
    <AbsoluteFill>
      {topText && (
        <div style={{ position: 'absolute', top: 20, left: 0, right: 0, textAlign: 'center' }}>
          <span style={strokeStyle}>{topText}</span>
        </div>
      )}
      {bottomText && (
        <div style={{ position: 'absolute', bottom: 20, left: 0, right: 0, textAlign: 'center' }}>
          <span style={strokeStyle}>{bottomText}</span>
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Reaction / POV Text Card

```tsx
export const POVCard: React.FC<{
  setup: string;
  reaction?: string;
  style?: 'pov' | 'when' | 'me-when' | 'nobody' | 'that-moment';
}> = ({ setup, reaction, style = 'pov' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const PREFIXES = {
    pov:          'POV:',
    when:         'When',
    'me-when':    'Me when',
    nobody:       'Nobody:\nAbsolutely nobody:\nMe:',
    'that-moment':'That moment when',
  };

  const appear = spring({ frame, fps, config: { damping: 8, stiffness: 400 } });
  const setupOpacity = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: 'clamp' });
  const reactionOpacity = interpolate(frame, [fps * 1.5, fps * 2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#000',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 24,
      padding: '0 80px',
    }}>
      <div style={{
        color: 'rgba(255,255,255,0.5)',
        fontSize: 32, fontWeight: 700,
        textTransform: 'uppercase', letterSpacing: 4,
        opacity: setupOpacity,
        whiteSpace: 'pre-line', textAlign: 'center',
      }}>
        {PREFIXES[style]}
      </div>
      <div style={{
        color: 'white', fontSize: 64, fontWeight: 900,
        textAlign: 'center', lineHeight: 1.2,
        opacity: setupOpacity,
        transform: `scale(${appear})`,
      }}>
        {setup}
      </div>
      {reaction && (
        <div style={{
          color: '#FFD700', fontSize: 72, fontWeight: 900,
          textAlign: 'center',
          opacity: reactionOpacity,
          transform: `scale(${spring({ frame: frame - fps * 1.5, fps, config: { damping: 6, stiffness: 500 } })})`,
        }}>
          {reaction}
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Comedic Timing — The Pause

The most important comedy technique: the pause before the punchline. In Remotion, implement as a held frame:

```tsx
// Beat — deliberate held moment before reveal
export const ComedyBeat: React.FC<{
  children: React.ReactNode;
  beatDurationFrames?: number;
}> = ({ children, beatDurationFrames = 18 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Freeze on the beat frame for comedic timing
  // Use with <Freeze> from Remotion for held expressions
  return <>{children}</>;
};

// Usage pattern:
// <Sequence from={60} durationInFrames={18}>
//   <Freeze frame={60}><FunnyCutaway /></Freeze>   ← hold face for 18 frames
// </Sequence>
// <Sequence from={78} durationInFrames={30}>
//   <Punchline />   ← release the joke
// </Sequence>
```

---

## Zoom Smash — Comedy Cut

The sudden crash-zoom on a surprising moment:

```tsx
export const ZoomSmash: React.FC<{
  children: React.ReactNode;
  triggerFrame: number;
  intensity?: number;
}> = ({ children, triggerFrame, intensity = 1.4 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF = frame - triggerFrame;
  const zoomIn = spring({ frame: localF, fps, config: { damping: 4, stiffness: 800 } });
  const zoomOut = spring({ frame: localF - 6, fps, config: { damping: 12, stiffness: 200 } });

  const scale = localF >= 6
    ? interpolate(zoomOut, [0, 1], [intensity, 1])
    : interpolate(zoomIn, [0, 1], [1, intensity]);

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      {children}
    </AbsoluteFill>
  );
};
```

---

## Split-Screen Comparison (Comedy Format)

```tsx
export const CompareSplit: React.FC<{
  leftLabel: string;
  rightLabel: string;
  leftContent: React.ReactNode;
  rightContent: React.ReactNode;
  leftColor?: string;
  rightColor?: string;
}> = ({
  leftLabel, rightLabel,
  leftContent, rightContent,
  leftColor = '#4f46e5', rightColor = '#e11d48',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const splitIn = spring({ frame, fps, config: { damping: 60, stiffness: 100 } });
  const dividerX = interpolate(splitIn, [0, 1], [-960, 0]);

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      {/* Left */}
      <AbsoluteFill style={{
        width: '50%', left: 0,
        borderRight: `4px solid ${leftColor}`,
        backgroundColor: '#0a0a0a',
      }}>
        {leftContent}
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          backgroundColor: leftColor, color: 'white',
          fontSize: 36, fontWeight: 900,
          textAlign: 'center', padding: '12px 0',
          textTransform: 'uppercase', letterSpacing: 3,
        }}>
          {leftLabel}
        </div>
      </AbsoluteFill>

      {/* Right */}
      <AbsoluteFill style={{
        width: '50%', left: '50%',
        backgroundColor: '#0a0a0a',
      }}>
        {rightContent}
        <div style={{
          position: 'absolute', bottom: 0, left: 0, right: 0,
          backgroundColor: rightColor, color: 'white',
          fontSize: 36, fontWeight: 900,
          textAlign: 'center', padding: '12px 0',
          textTransform: 'uppercase', letterSpacing: 3,
        }}>
          {rightLabel}
        </div>
      </AbsoluteFill>

      {/* Center divider */}
      <div style={{
        position: 'absolute', left: '50%', top: 0, bottom: 0,
        width: 4, backgroundColor: 'white',
        transform: `translateX(${dividerX}px)`,
      }} />
    </AbsoluteFill>
  );
};
```

---

## Comedy Timing Guide

```tsx
// Comedy frame timing reference at 30fps
const COMEDY_TIMING = {
  setup:           { minFrames: 45,  maxFrames: 90  }, // 1.5–3s
  pause_before:    { minFrames: 12,  maxFrames: 24  }, // 0.4–0.8s — THE BEAT
  punchline:       { minFrames: 30,  maxFrames: 60  }, // 1–2s
  reaction_hold:   { minFrames: 18,  maxFrames: 36  }, // 0.6–1.2s
  callback_setup:  { minFrames: 60,  maxFrames: 120 }, // 2–4s
  callback_payoff: { minFrames: 24,  maxFrames: 48  }, // 0.8–1.6s
};

// Rule of threes — setups with three beats always deliver on the third:
// Beat 1: Expected
// Beat 2: Confirms pattern
// Beat 3: SUBVERTS pattern → the laugh
```

---

## Cross-References
- `genres/viral-formula.md` — comedy drives highest share rates; open loop = setup
- `genres/influencer.md` — zoom punches, jump cuts for comedic effect
- `rules/transitions.md` — fast smash cuts are the comedy edit language
- `rules/text.md` — meme text, reaction text overlays
