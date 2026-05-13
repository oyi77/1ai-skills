// ============================================================
// REMOTION NARRATED VIDEO STARTER TEMPLATE
// Usage: Copy contents to src/ in a new Remotion project
// Run: npx create-video@latest (select "blank"), then replace
// ============================================================

// ---- src/Root.tsx ----
import React from 'react';
import { Composition } from 'remotion';
import { NarratedVideo } from './Composition';

// Import timing after running: python scripts/generate_timing.py
// import timingData from '../public/timing.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="NarratedVideo"
    component={NarratedVideo}
    durationInFrames={300}   // Replace with timingData.totalFrames
    fps={30}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ---- src/Composition.tsx ----
import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';

// After generating timing.json:
// import timingData from '../public/timing.json';

// Placeholder scenes for development
const PLACEHOLDER_SCENES = [
  { id: 'intro', title: 'Pembukaan', startFrame: 0, durationFrames: 90 },
  { id: 'main', title: 'Konten Utama', startFrame: 90, durationFrames: 150 },
  { id: 'outro', title: 'Penutup', startFrame: 240, durationFrames: 60 },
];

export const NarratedVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#0f172a' }}>
    {/* Background music — place bgm.mp3 in public/audio/ */}
    {/* <Audio src={staticFile('audio/bgm.mp3')} volume={0.12} /> */}

    {PLACEHOLDER_SCENES.map((scene) => (
      <Sequence
        key={scene.id}
        from={scene.startFrame}
        durationInFrames={scene.durationFrames}
      >
        {/* Uncomment after generating audio:
        <Audio
          src={staticFile(`audio/${scene.id}.mp3`)}
          startFrom={15}
        /> */}
        <PlaceholderScene title={scene.title} durationFrames={scene.durationFrames} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

// Placeholder scene component — replace with your actual scene components
const PlaceholderScene: React.FC<{ title: string; durationFrames: number }> = ({
  title, durationFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  const exitOpacity = interpolate(
    frame, [durationFrames - 12, durationFrames], [1, 0],
    { extrapolateLeft: 'clamp' }
  );
  const scale = spring({ frame, fps, config: { damping: 80 } });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#1e293b',
      justifyContent: 'center',
      alignItems: 'center',
      opacity: Math.min(opacity, exitOpacity),
    }}>
      <h1 style={{
        color: 'white',
        fontSize: 72,
        fontWeight: 'bold',
        transform: `scale(${scale})`,
        margin: 0,
        textAlign: 'center',
        padding: '0 80px',
      }}>
        {title}
      </h1>
      <p style={{ color: '#64748b', fontSize: 28, marginTop: 16 }}>
        Frame {frame} / {durationFrames}
      </p>
    </AbsoluteFill>
  );
};
