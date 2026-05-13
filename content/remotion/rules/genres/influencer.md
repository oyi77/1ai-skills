# Influencer-Style Video in Remotion

## Visual Identity

Influencer content = fast edits, bold text overlays, emoji reactions, trending color schemes, face-cam style framing, "hook" first 3 seconds, zoom punches on key words, and platform-optimized formats (Reels 9:16, TikTok 9:16, YouTube 16:9 + Shorts 9:16).

## Platform Presets

```tsx
export const PLATFORM_CONFIGS = {
  tiktok:    { width: 1080, height: 1920, fps: 30, maxDuration: 60 * 30 },  // 60s
  reels:     { width: 1080, height: 1920, fps: 30, maxDuration: 90 * 30 },  // 90s
  shorts:    { width: 1080, height: 1920, fps: 60, maxDuration: 60 * 60 },  // 60s @60fps
  youtube:   { width: 1920, height: 1080, fps: 30, maxDuration: Infinity },
  linkedin:  { width: 1920, height: 1080, fps: 30, maxDuration: 10 * 60 * 30 },
  instagram: { width: 1080, height: 1080, fps: 30, maxDuration: 60 * 30 },  // Square
};
```

## Hook Text (First 3 Seconds)

The hook must appear in the first 3 seconds with bold, large text to stop the scroll:

```tsx
const HookText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 10, stiffness: 500 } });
  const opacity = interpolate(frame, [0, 6], [0, 1], { extrapolateRight: 'clamp' });

  // Highlight alternating words
  const words = text.split(' ');

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: '0 40px' }}>
      <div style={{
        transform: `scale(${scale})`,
        opacity,
        textAlign: 'center',
      }}>
        {words.map((word, i) => (
          <span key={i} style={{
            fontSize: 96,
            fontWeight: 900,
            display: 'inline-block',
            marginRight: 16,
            color: i % 2 === 0 ? '#FFFFFF' : '#FFE500',
            textShadow: '3px 3px 0 #000, -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000',
            lineHeight: 1.1,
          }}>
            {word}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

## Zoom Punch on Keyword

```tsx
// Zoom into a specific area of the frame on a keyword
const ZoomPunch: React.FC<{
  children: React.ReactNode;
  triggerFrame: number;
  targetX?: number;  // 0-1
  targetY?: number;  // 0-1
  zoomAmount?: number;
}> = ({ children, triggerFrame, targetX = 0.5, targetY = 0.5, zoomAmount = 1.15 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const punch = spring({ frame: frame - triggerFrame, fps, config: { damping: 12, stiffness: 600 } });
  const scale = interpolate(punch, [0, 1], [1, zoomAmount]);
  const recovery = spring({ frame: frame - triggerFrame - 8, fps, config: { damping: 40 } });
  const finalScale = frame < triggerFrame + 8 ? scale : interpolate(recovery, [0, 1], [zoomAmount, 1]);

  return (
    <AbsoluteFill style={{
      transform: `scale(${finalScale})`,
      transformOrigin: `${targetX * 100}% ${targetY * 100}%`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
```

## Lower Third (Name Tag)

```tsx
const LowerThird: React.FC<{
  name: string;
  title?: string;
  triggerFrame?: number;
}> = ({ name, title, triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = spring({ frame: frame - triggerFrame, fps, config: { damping: 80 } });
  const x = interpolate(slideIn, [0, 1], [-600, 0]);

  return (
    <div style={{
      position: 'absolute',
      bottom: 200, left: 60,
      transform: `translateX(${x}px)`,
    }}>
      {/* Accent bar */}
      <div style={{ width: 6, height: '100%', backgroundColor: '#FF4500', position: 'absolute', left: -12 }} />
      <div style={{ backgroundColor: 'rgba(0,0,0,0.85)', padding: '12px 24px', borderRadius: 4 }}>
        <div style={{ color: 'white', fontSize: 36, fontWeight: 800 }}>{name}</div>
        {title && <div style={{ color: '#FF4500', fontSize: 24, fontWeight: 500 }}>{title}</div>}
      </div>
    </div>
  );
};
```

## Emoji Reaction Pop-Up

```tsx
const EmojiReaction: React.FC<{ emoji: string; x: number; y: number; triggerFrame: number }> = ({
  emoji, x, y, triggerFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame: frame - triggerFrame, fps, config: { damping: 6, stiffness: 400 } });
  const fadeOut = interpolate(frame, [triggerFrame + 30, triggerFrame + 50], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const floatY = interpolate(frame - triggerFrame, [0, 60], [0, -80], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      position: 'absolute',
      left: x, top: y,
      transform: `scale(${pop}) translateY(${floatY}px)`,
      opacity: fadeOut,
      fontSize: 80,
      zIndex: 90,
    }}>
      {emoji}
    </div>
  );
};
```

## Progress / Countdown Bar

```tsx
const ProgressBar: React.FC<{ label?: string; color?: string }> = ({
  label, color = '#FF4500',
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;

  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, zIndex: 100 }}>
      <div style={{ height: 6, backgroundColor: 'rgba(255,255,255,0.2)' }}>
        <div style={{ height: '100%', width: `${progress * 100}%`, backgroundColor: color }} />
      </div>
    </div>
  );
};
```

## Jump Cut Simulation

```tsx
// Simulate jump cuts by switching between clips at intervals
const JumpCutMontage: React.FC<{ clips: string[]; cutInterval?: number }> = ({
  clips, cutInterval = 30,
}) => {
  const frame = useCurrentFrame();
  const clipIndex = Math.floor(frame / cutInterval) % clips.length;

  return (
    <OffthreadVideo
      src={staticFile(clips[clipIndex])}
      startFrom={(Math.floor(frame / cutInterval) * cutInterval) % 90}
      muted
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
    />
  );
};
```

## B-Roll Text Overlay Style

```tsx
// Bold word-by-word reveal (talking head + B-roll text)
const BRollCaption: React.FC<{ text: string; style?: 'bold' | 'minimal' | 'tiktok' }> = ({
  text, style = 'tiktok',
}) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');
  const framesPerWord = 7;

  const activeWordIndex = Math.floor(frame / framesPerWord);

  const styles = {
    bold: { fontSize: 80, fontWeight: 900, color: '#fff', stroke: '#000' },
    minimal: { fontSize: 60, fontWeight: 400, color: '#fff' },
    tiktok: { fontSize: 72, fontWeight: 800, color: '#fff', backgroundColor: '#000' },
  };

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ textAlign: 'center', padding: '0 60px' }}>
        {words.map((word, i) => (
          <span key={i} style={{
            ...styles[style],
            display: 'inline-block',
            marginRight: 12,
            opacity: i <= activeWordIndex ? 1 : 0.3,
            transform: `scale(${i === activeWordIndex ? 1.15 : 1})`,
            transition: 'none',
            padding: style === 'tiktok' ? '4px 8px' : 0,
            borderRadius: style === 'tiktok' ? 6 : 0,
          }}>
            {word}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

## Trending Visual Effects

```tsx
// Vignette (darkened edges)
const Vignette: React.FC<{ intensity?: number }> = ({ intensity = 0.5 }) => (
  <AbsoluteFill style={{
    background: `radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,${intensity}) 100%)`,
    pointerEvents: 'none',
    zIndex: 40,
  }} />
);

// Color overlay (mood)
const MoodOverlay: React.FC<{ color: string; opacity?: number }> = ({
  color, opacity = 0.1,
}) => (
  <AbsoluteFill style={{
    backgroundColor: color,
    opacity,
    mixBlendMode: 'multiply',
    pointerEvents: 'none',
  }} />
);

// Trending: Pink/Purple aesthetic
<MoodOverlay color="#ff69b4" opacity={0.12} />
// Dark/Moody
<MoodOverlay color="#001133" opacity={0.3} />
```

## Recommended Fonts

```bash
npm install @remotion/google-fonts
```

```tsx
import { loadFont as loadMontserrat } from '@remotion/google-fonts/Montserrat';
import { loadFont as loadPoppins } from '@remotion/google-fonts/Poppins';
import { loadFont as loadBebas } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadOswald } from '@remotion/google-fonts/Oswald';
```

## Cross-References
- For word-by-word TikTok captions: load `rules/captions.md` → @remotion/captions
- For SRT subtitle files: load `rules/ecosystem.md` → remotion-subtitle
- For declarative animation shortcuts: load `rules/ecosystem.md` → remotion-animated / remotion-kit
- For glitch effect on hook text: load `rules/effects.md` → Glitch section
- For text animation library: load `rules/ecosystem.md` → remotion-animate-text
