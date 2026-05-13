# Remotion Scenes Rule

## Scene-Based Architecture

The recommended pattern for multi-scene videos is to break each scene into its own component, then sequence them in the root composition.

## File Structure

```
src/
├── Root.tsx              # Register composition
├── Composition.tsx       # Main composition — sequences scenes
└── scenes/
    ├── Intro.tsx
    ├── Section1.tsx
    ├── Section2.tsx
    └── Outro.tsx
```

## Scene Component Pattern

Each scene receives `durationInFrames` as a prop so it knows when to start its exit animation:

```tsx
// src/scenes/Intro.tsx
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

interface Props {
  title: string;
  durationInFrames: number;
}

export const Intro: React.FC<Props> = ({ title, durationInFrames }) => {
  const frame = useCurrentFrame();

  // Entrance
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Exit
  const exitOpacity = interpolate(
    frame,
    [durationInFrames - 15, durationInFrames],
    [1, 0],
    { extrapolateLeft: 'clamp' }
  );

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#1a1a2e',
        justifyContent: 'center',
        alignItems: 'center',
        opacity: Math.min(opacity, exitOpacity),
      }}
    >
      <h1 style={{ color: 'white', fontSize: 80 }}>{title}</h1>
    </AbsoluteFill>
  );
};
```

## Main Composition with Sequences

```tsx
// src/Composition.tsx
import { AbsoluteFill, Sequence } from 'remotion';
import { Intro } from './scenes/Intro';
import { MainContent } from './scenes/MainContent';
import { Outro } from './scenes/Outro';

const INTRO_DURATION = 90;    // 3s at 30fps
const MAIN_DURATION = 300;    // 10s at 30fps
const OUTRO_DURATION = 60;    // 2s at 30fps

export const MyVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#000' }}>
    <Sequence from={0} durationInFrames={INTRO_DURATION}>
      <Intro title="My Video" durationInFrames={INTRO_DURATION} />
    </Sequence>

    <Sequence from={INTRO_DURATION} durationInFrames={MAIN_DURATION}>
      <MainContent durationInFrames={MAIN_DURATION} />
    </Sequence>

    <Sequence from={INTRO_DURATION + MAIN_DURATION} durationInFrames={OUTRO_DURATION}>
      <Outro durationInFrames={OUTRO_DURATION} />
    </Sequence>
  </AbsoluteFill>
);
```

## Dynamic Scene Timing from Audio

When TTS audio determines scene length:

```tsx
// scenes/SceneWithAudio.tsx
import { AbsoluteFill, Audio, staticFile, useVideoConfig } from 'remotion';

interface SceneData {
  id: string;
  text: string;
  audioFile: string;
  durationFrames: number;
}

export const DynamicScene: React.FC<{ scene: SceneData }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity }}>
      <Audio src={staticFile(`audio/${scene.audioFile}`)} />
      <div style={{ padding: 60, color: 'white', fontSize: 48 }}>
        {scene.text}
      </div>
    </AbsoluteFill>
  );
};

// In Root Composition:
let cumulativeFrame = 0;
{scenes.map((scene) => {
  const from = cumulativeFrame;
  cumulativeFrame += scene.durationFrames;
  return (
    <Sequence key={scene.id} from={from} durationInFrames={scene.durationFrames}>
      <DynamicScene scene={scene} />
    </Sequence>
  );
})}
```

## Background Music Across All Scenes

Put background music outside of any `<Sequence>` so it plays throughout:

```tsx
export const MyVideo = () => (
  <AbsoluteFill>
    {/* BGM plays entire duration */}
    <Audio src={staticFile('bgm.mp3')} volume={0.15} />

    {/* Scenes sequence on top */}
    <Sequence from={0} durationInFrames={90}><Scene1 /></Sequence>
    <Sequence from={90} durationInFrames={120}><Scene2 /></Sequence>
  </AbsoluteFill>
);
```

## Persistent HUD / Overlay

Elements that persist across all scenes (progress bar, watermark, etc.):

```tsx
export const MyVideo = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;

  return (
    <AbsoluteFill>
      {/* Scenes */}
      <Sequence from={0} durationInFrames={90}><Scene1 /></Sequence>

      {/* Persistent overlay — always visible */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        height: 4,
        width: `${progress * 100}%`,
        backgroundColor: '#4f46e5',
      }} />
    </AbsoluteFill>
  );
};
```
