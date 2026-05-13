# Music Video (MV) in Remotion

## Visual Identity

Music videos are beat-synchronized. Every cut, flash, zoom, and effect fires ON the beat. Key elements: BPM-driven timing, waveform/spectrum visualizers, lyric overlays, color strobes, glitch effects, and high-energy transitions.

## BPM-Driven Timing

**The most important concept:** convert BPM to frames so animations fire on the beat.

```tsx
// BPM utilities
export const bpmToFrames = (bpm: number, fps: number, beats: number = 1) =>
  Math.round((60 / bpm) * fps * beats);

// Example: 128 BPM at 30fps
const fps = 30;
const bpm = 128;
const beat = bpmToFrames(bpm, fps);        // 14 frames per beat
const bar = bpmToFrames(bpm, fps, 4);      // 56 frames per bar (4 beats)
const halfBar = bpmToFrames(bpm, fps, 2);  // 28 frames per half-bar

// Flash on every beat
const isBeat = frame % beat < 3;  // true for first 3 frames of each beat

// Pulse scale on beat
const beatPhase = frame % beat;
const beatScale = 1 + interpolate(beatPhase, [0, 4, beat], [0.06, 0, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

## Beat Flash / Strobe

```tsx
const BeatFlash: React.FC<{ bpm: number; color?: string }> = ({
  bpm, color = 'white',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const beat = bpmToFrames(bpm, fps);
  const beatPhase = frame % beat;

  const opacity = interpolate(beatPhase, [0, 3, 10, beat], [0.6, 0.3, 0, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: color,
      opacity,
      mixBlendMode: 'screen',
      pointerEvents: 'none',
      zIndex: 80,
    }} />
  );
};
```

## Audio Spectrum Visualizer

```tsx
import { useAudioData, visualizeAudio } from '@remotion/media-utils';

const SpectrumBars: React.FC<{
  audioFile: string;
  bars?: number;
  color?: string;
  height?: number;
}> = ({ audioFile, bars = 64, color = '#ff6b35', height = 300 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const audioData = useAudioData(staticFile(audioFile));
  if (!audioData) return null;

  const spectrum = visualizeAudio({ fps, frame, audioData, numberOfSamples: bars });

  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-end',
      gap: 2,
      height,
    }}>
      {spectrum.map((value, i) => {
        const barH = value * height;
        const hue = (i / bars) * 60 + 10; // orange to red gradient
        return (
          <div key={i} style={{
            flex: 1,
            height: barH,
            backgroundColor: `hsl(${hue}, 100%, 55%)`,
            borderRadius: '2px 2px 0 0',
          }} />
        );
      })}
    </div>
  );
};

// Waveform (center-symmetric)
const Waveform: React.FC<{ audioFile: string }> = ({ audioFile }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const audioData = useAudioData(staticFile(audioFile));
  if (!audioData) return null;

  const samples = visualizeAudio({ fps, frame, audioData, numberOfSamples: 128 });
  const W = 1920, H = 200;
  const midY = H / 2;
  const barW = W / samples.length;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%' }}>
      {samples.map((v, i) => {
        const barH = v * H;
        return (
          <rect
            key={i}
            x={i * barW}
            y={midY - barH / 2}
            width={barW - 1}
            height={barH}
            fill="#00ffff"
            opacity={0.8}
          />
        );
      })}
    </svg>
  );
};
```

## Glitch Effect

```tsx
const GlitchText: React.FC<{ text: string; intensity?: number }> = ({
  text, intensity = 1,
}) => {
  const frame = useCurrentFrame();

  // Trigger glitch randomly every ~15 frames
  const isGlitch = frame % 15 < 3 && intensity > 0.5;
  const glitchX = isGlitch ? (Math.random() - 0.5) * 20 * intensity : 0;
  const glitchY = isGlitch ? (Math.random() - 0.5) * 6 * intensity : 0;

  return (
    <div style={{ position: 'relative', fontSize: 120, fontWeight: 900 }}>
      {/* RGB channel split */}
      {isGlitch && (
        <>
          <div style={{
            position: 'absolute',
            color: 'red',
            transform: `translate(${glitchX + 6}px, ${glitchY}px)`,
            opacity: 0.7,
            mixBlendMode: 'screen',
          }}>{text}</div>
          <div style={{
            position: 'absolute',
            color: 'cyan',
            transform: `translate(${glitchX - 6}px, ${glitchY}px)`,
            opacity: 0.7,
            mixBlendMode: 'screen',
          }}>{text}</div>
        </>
      )}
      {/* Main text */}
      <div style={{
        color: 'white',
        transform: `translate(${isGlitch ? glitchX * 0.3 : 0}px, 0)`,
      }}>
        {text}
      </div>
    </div>
  );
};
```

## Lyric Overlay (Karaoke-Style)

```tsx
interface Lyric {
  text: string;
  startFrame: number;
  endFrame: number;
  highlighted?: boolean; // active word
}

const LyricDisplay: React.FC<{ lyrics: Lyric[] }> = ({ lyrics }) => {
  const frame = useCurrentFrame();

  const current = lyrics.find((l) => frame >= l.startFrame && frame <= l.endFrame);
  const next = lyrics.find((l) => l.startFrame > frame);

  if (!current) return null;

  const progress = (frame - current.startFrame) / (current.endFrame - current.startFrame);
  const opacity = interpolate(frame, [current.startFrame, current.startFrame + 8], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
      <div style={{
        marginBottom: 140,
        textAlign: 'center',
        padding: '0 80px',
      }}>
        {/* Current lyric with fill animation */}
        <div style={{ position: 'relative', display: 'inline-block' }}>
          {/* Base text */}
          <h2 style={{
            fontSize: 72,
            fontWeight: 800,
            color: 'rgba(255,255,255,0.3)',
            margin: 0,
            opacity,
          }}>
            {current.text}
          </h2>
          {/* Fill overlay */}
          <div style={{
            position: 'absolute',
            top: 0, left: 0,
            width: `${progress * 100}%`,
            overflow: 'hidden',
          }}>
            <h2 style={{
              fontSize: 72,
              fontWeight: 800,
              color: '#FFD700',
              margin: 0,
              opacity,
              whiteSpace: 'nowrap',
            }}>
              {current.text}
            </h2>
          </div>
        </div>

        {/* Upcoming lyric preview */}
        {next && (
          <p style={{
            fontSize: 40,
            color: 'rgba(255,255,255,0.4)',
            margin: '8px 0 0',
            fontWeight: 400,
          }}>
            {next.text}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

## Color Strobe / Scene Flash Transition

```tsx
const ColorStrobe: React.FC<{ colors: string[]; bpm: number }> = ({ colors, bpm }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const beat = bpmToFrames(bpm, fps);
  const colorIndex = Math.floor(frame / beat) % colors.length;

  return (
    <AbsoluteFill style={{
      backgroundColor: colors[colorIndex],
      opacity: 0.15,
      mixBlendMode: 'screen',
    }} />
  );
};
```

## MV Structure Template

```tsx
// Typical 3-minute music video structure
const MV_SECTIONS = [
  { id: 'intro',    startBeat: 0,   durationBeats: 8,  type: 'ambient' },
  { id: 'verse1',   startBeat: 8,   durationBeats: 16, type: 'performance' },
  { id: 'chorus1',  startBeat: 24,  durationBeats: 16, type: 'high-energy' },
  { id: 'verse2',   startBeat: 40,  durationBeats: 16, type: 'performance' },
  { id: 'chorus2',  startBeat: 56,  durationBeats: 16, type: 'high-energy' },
  { id: 'bridge',   startBeat: 72,  durationBeats: 8,  type: 'breakdown' },
  { id: 'drop',     startBeat: 80,  durationBeats: 8,  type: 'climax' },
  { id: 'outro',    startBeat: 88,  durationBeats: 8,  type: 'fade' },
];

// Convert to frames
const BPM = 128;
const sections = MV_SECTIONS.map((s) => ({
  ...s,
  startFrame: bpmToFrames(BPM, 30, s.startBeat),
  durationFrames: bpmToFrames(BPM, 30, s.durationBeats),
}));
```

## Vinyl / Album Art Spin

```tsx
const VinylSpin: React.FC<{ albumArt: string }> = ({ albumArt }) => {
  const frame = useCurrentFrame();
  const rotation = (frame / 30) * 33; // 33 RPM equivalent

  return (
    <div style={{
      width: 400, height: 400,
      borderRadius: '50%',
      overflow: 'hidden',
      transform: `rotate(${rotation}deg)`,
      boxShadow: '0 0 60px rgba(0,0,0,0.8)',
    }}>
      <Img src={staticFile(albumArt)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      {/* Center hole */}
      <div style={{
        position: 'absolute',
        top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 30, height: 30,
        backgroundColor: '#000',
        borderRadius: '50%',
      }} />
    </div>
  );
};
```

## Cross-References
- For audio spectrum data: load `rules/audio.md` → @remotion/media-utils (visualizeAudio, useAudioData, createSmoothSvgPath)
- For draw-on waveform paths: load `rules/effects.md` → @remotion/paths (evolvePath)
- For geometric shapes in visualizer: load `rules/effects.md` → @remotion/shapes
- For Lottie/Rive animated assets: load `rules/ecosystem.md`
- For noise-based organic movement: load `rules/effects.md` → @remotion/noise
