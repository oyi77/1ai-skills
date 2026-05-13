// ============================================================
// MUSIC VIDEO / LYRIC VIDEO TEMPLATE
// Style: Beat-synced, lyric reveal, visualizer
// Format: 16:9 1080p — change width/height for vertical
// Customize: BPM, LYRICS, PALETTE, AUDIO_FILE
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence, Audio, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const BPM        = 128;       // beats per minute of your track
const AUDIO_FILE = 'audio/track.mp3';   // put in /public/

const PALETTE = {
  bg:      '#050518',
  primary: '#FF4EC7',    // neon pink
  accent:  '#00FFEE',    // cyan
  text:    '#FFFFFF',
};

// Lyrics array: { text, beatStart }
// beatStart = which beat number this lyric starts on (0-indexed)
const LYRICS: Array<{ text: string; beatStart: number }> = [
  { text: 'Baris pertama lirik lagu',    beatStart: 0  },
  { text: 'Sambung ke baris kedua',       beatStart: 4  },
  { text: 'Terus dan terus mengalir',     beatStart: 8  },
  { text: 'Sampai ke akhir',              beatStart: 12 },
  { text: 'CHORUS — bagian reff di sini', beatStart: 16 },
  { text: 'Bersama-sama kita bernyanyi',  beatStart: 20 },
  { text: 'Dan dunia terasa lebih indah', beatStart: 24 },
  { text: 'Bersama kamu',                 beatStart: 28 },
];

const FPS      = 30;
const DURATION = FPS * 120; // 2 minutes — adjust to song length

// ── HELPERS ──────────────────────────────────────────────────
const beatToFrame  = (beat: number) => Math.round((60 / BPM) * FPS * beat);
const beatDuration = beatToFrame(1); // frames per beat

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="MusicVideo"
    component={MusicVideo}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const MusicVideo: React.FC = () => {
  const frame = useCurrentFrame();

  // Current beat (fractional)
  const currentBeat = frame / beatDuration;
  const beatPhase   = currentBeat % 1; // 0→1 within each beat

  // Beat flash on every beat
  const beatFlash = interpolate(beatPhase, [0, 0.08, 0.3, 1], [0.5, 0, 0, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  // Find current lyric
  const currentLyricIndex = LYRICS.reduce((acc, lyric, i) => {
    return frame >= beatToFrame(lyric.beatStart) ? i : acc;
  }, -1);
  const currentLyric = LYRICS[currentLyricIndex] ?? null;
  const nextLyric    = LYRICS[currentLyricIndex + 1] ?? null;

  return (
    <AbsoluteFill style={{ backgroundColor: PALETTE.bg }}>

      {/* Audio */}
      <Audio src={staticFile(AUDIO_FILE)} />

      {/* Animated gradient background */}
      <AnimatedBg frame={frame} beatPhase={beatPhase} />

      {/* Spectrum bars */}
      <SpectrumBars frame={frame} beatPhase={beatPhase} />

      {/* Lyric display */}
      {currentLyric && (
        <LyricDisplay
          lyric={currentLyric}
          nextLyric={nextLyric}
          lyricFrame={frame - beatToFrame(currentLyric.beatStart)}
          lyricDuration={nextLyric
            ? beatToFrame(nextLyric.beatStart - currentLyric.beatStart)
            : FPS * 4}
        />
      )}

      {/* Beat flash overlay */}
      <AbsoluteFill style={{
        backgroundColor: PALETTE.primary,
        opacity: beatFlash * 0.15,
        mixBlendMode: 'screen',
        pointerEvents: 'none',
      }} />

      {/* Waveform bottom */}
      <WaveformDecor frame={frame} beatPhase={beatPhase} />

    </AbsoluteFill>
  );
};

// ── ANIMATED BACKGROUND ──────────────────────────────────────
const AnimatedBg: React.FC<{ frame: number; beatPhase: number }> = ({ frame, beatPhase }) => {
  const rotation   = (frame * 0.08) % 360;
  const brightness = 1 + beatPhase * 0.06;

  return (
    <AbsoluteFill style={{ opacity: 0.4 }}>
      {/* Rotating colour blobs */}
      <div style={{
        position: 'absolute',
        width: 800, height: 800,
        borderRadius: '50%',
        top: '50%', left: '50%',
        transform: `translate(-50%, -50%) rotate(${rotation}deg)`,
        background: `conic-gradient(${PALETTE.primary}44, transparent, ${PALETTE.accent}44, transparent)`,
        filter: `blur(80px) brightness(${brightness})`,
      }} />
      <div style={{
        position: 'absolute',
        width: 500, height: 500,
        borderRadius: '50%',
        top: '20%', right: '10%',
        background: `radial-gradient(circle, ${PALETTE.accent}33, transparent)`,
        filter: 'blur(60px)',
      }} />
    </AbsoluteFill>
  );
};

// ── LYRIC DISPLAY ────────────────────────────────────────────
const LyricDisplay: React.FC<{
  lyric: typeof LYRICS[0];
  nextLyric: typeof LYRICS[0] | null;
  lyricFrame: number;
  lyricDuration: number;
}> = ({ lyric, nextLyric, lyricFrame, lyricDuration }) => {
  const { fps } = useVideoConfig();

  // Fill progress for karaoke effect
  const fillProgress = Math.min(lyricFrame / lyricDuration, 1);

  // Entrance
  const appear = spring({ frame: lyricFrame, fps, config: { damping: 15, stiffness: 400 } });
  const scale  = interpolate(appear, [0, 1], [0.88, 1]);
  const opacity = interpolate(appear, [0, 0.3], [0, 1]);

  // Exit fade
  const exitOpacity = interpolate(
    lyricFrame, [lyricDuration - 8, lyricDuration], [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 32 }}>

      {/* Current lyric — karaoke fill */}
      <div style={{
        position: 'relative',
        display: 'inline-block',
        opacity: Math.min(opacity, exitOpacity),
        transform: `scale(${scale})`,
      }}>
        {/* Base text (dim) */}
        <div style={{
          fontSize: 92, fontWeight: 900,
          color: 'rgba(255,255,255,0.25)',
          textShadow: 'none',
          letterSpacing: 2,
          textAlign: 'center',
        }}>
          {lyric.text}
        </div>
        {/* Filled text (bright) — clip to fill progress */}
        <div style={{
          position: 'absolute', inset: 0,
          overflow: 'hidden',
          width: `${fillProgress * 100}%`,
        }}>
          <div style={{
            fontSize: 92, fontWeight: 900,
            color: PALETTE.primary,
            textShadow: `0 0 40px ${PALETTE.primary}88`,
            letterSpacing: 2,
            whiteSpace: 'nowrap',
            textAlign: 'center',
          }}>
            {lyric.text}
          </div>
        </div>
      </div>

      {/* Next lyric preview (dim) */}
      {nextLyric && (
        <div style={{
          fontSize: 48, color: 'rgba(255,255,255,0.2)',
          fontWeight: 500, letterSpacing: 1,
          opacity: interpolate(fillProgress, [0.6, 1], [0, 0.6], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }}>
          {nextLyric.text}
        </div>
      )}
    </AbsoluteFill>
  );
};

// ── SPECTRUM BARS ────────────────────────────────────────────
const SpectrumBars: React.FC<{ frame: number; beatPhase: number }> = ({ frame, beatPhase }) => {
  const BAR_COUNT = 64;
  const bars = Array.from({ length: BAR_COUNT }, (_, i) => {
    // Simulate spectrum with sine waves that react to beat
    const freq  = (i / BAR_COUNT) * Math.PI * 2;
    const time  = frame * 0.04;
    const beat  = Math.max(0, 1 - beatPhase * 3) * (1 - Math.abs(i - BAR_COUNT / 2) / BAR_COUNT);
    const value = (Math.sin(freq * 3 + time) * 0.4 + 0.5) * (0.3 + beat * 0.7);
    return Math.max(0.04, value);
  });

  return (
    <AbsoluteFill style={{ alignItems: 'flex-end', justifyContent: 'center' }}>
      <div style={{ display: 'flex', gap: 3, height: 200, alignItems: 'flex-end', marginBottom: 40 }}>
        {bars.map((v, i) => {
          const hue = (i / BAR_COUNT) * 60 + 280; // pink → cyan
          return (
            <div key={i} style={{
              width: 22,
              height: v * 200,
              backgroundColor: `hsl(${hue}, 100%, 60%)`,
              borderRadius: '3px 3px 0 0',
              opacity: 0.7 + v * 0.3,
            }} />
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── WAVEFORM DECOR ───────────────────────────────────────────
const WaveformDecor: React.FC<{ frame: number; beatPhase: number }> = ({ frame, beatPhase }) => {
  const W = 1920, H = 80;
  const POINTS = 80;

  const points = Array.from({ length: POINTS }, (_, i) => {
    const x = (i / (POINTS - 1)) * W;
    const base = Math.sin((i / POINTS) * Math.PI * 6 + frame * 0.1) * 24;
    const beat = Math.max(0, 1 - beatPhase * 2) * 16;
    const y    = H / 2 + base + beat * Math.sin((i / POINTS) * Math.PI * 12);
    return `${x},${y}`;
  }).join(' ');

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end' }}>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: H, display: 'block' }}>
        <polyline
          points={points}
          fill="none"
          stroke={PALETTE.accent}
          strokeWidth={2}
          opacity={0.5}
        />
      </svg>
    </AbsoluteFill>
  );
};
