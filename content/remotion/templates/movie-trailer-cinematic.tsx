// ============================================================
// CINEMATIC MOVIE TRAILER TEMPLATE
// Style: Hollywood blockbuster — letterbox, grade, grain, blur
// Format: 16:9 1080p, 90 seconds
// Requires: @remotion/motion-blur @remotion/google-fonts
// Customize: TITLE, TAGLINE, SCENES, COLOR_GRADE
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence, OffthreadVideo, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';
import { CameraMotionBlur } from '@remotion/motion-blur';

// ── CONFIG ───────────────────────────────────────────────────
const FILM_TITLE   = 'BEYOND THE HORIZON';
const TAGLINE      = 'Some journeys change everything.';
const STUDIO_NAME  = 'BERKAH KARYA FILMS';
const RATING       = 'PG-13';
const RELEASE      = 'Coming Soon';

// Color grade — pick one: 'teal-orange' | 'bleach-bypass' | 'golden' | 'noir'
const COLOR_GRADE = 'teal-orange';

// Your video clips — put in /public/video/
// Replace with your actual scene files
const SCENES = [
  { file: 'video/scene1.mp4', duration: FPS_REF * 5,  muted: true },
  { file: 'video/scene2.mp4', duration: FPS_REF * 5,  muted: true },
  { file: 'video/scene3.mp4', duration: FPS_REF * 5,  muted: true },
  { file: 'video/scene4.mp4', duration: FPS_REF * 5,  muted: true },
  { file: 'video/scene5.mp4', duration: FPS_REF * 5,  muted: true },
];

// Must be declared before SCENES uses it
const FPS_REF = 30;
const FPS      = 30;
const DURATION = FPS * 90;

// ── COLOR GRADES ─────────────────────────────────────────────
const GRADES: Record<string, string> = {
  'teal-orange':   'contrast(1.18) saturate(1.35) brightness(0.97) hue-rotate(2deg)',
  'bleach-bypass': 'contrast(1.45) saturate(0.45) brightness(0.88)',
  'golden':        'contrast(1.08) saturate(1.25) sepia(0.18) brightness(1.06)',
  'noir':          'contrast(1.5)  saturate(0.15) brightness(0.82) hue-rotate(-15deg)',
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="MovieTrailer"
    component={MovieTrailer}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const MovieTrailer: React.FC = () => {
  let cursor = 0;

  // Build scene timing
  const builtScenes = SCENES.map((s) => {
    const from = cursor;
    cursor += s.duration;
    return { ...s, from };
  });

  const titleStart   = cursor;
  const creditStart  = cursor + FPS * 12;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>

      {/* All footage through motion blur + color grade */}
      <CameraMotionBlur shutterAngle={180} samples={8}>
        <AbsoluteFill style={{ filter: GRADES[COLOR_GRADE] ?? GRADES['teal-orange'] }}>

          {/* Scene clips */}
          {builtScenes.map((scene, i) => (
            <Sequence key={i} from={scene.from} durationInFrames={scene.duration}>
              <FilmScene file={scene.file} duration={scene.duration} />
            </Sequence>
          ))}

          {/* Title card */}
          <Sequence from={titleStart} durationInFrames={FPS * 12}>
            <TitleCard />
          </Sequence>

          {/* Credit crawl */}
          <Sequence from={creditStart} durationInFrames={FPS * 18}>
            <CreditBlock />
          </Sequence>

        </AbsoluteFill>
      </CameraMotionBlur>

      {/* Film grain — applied AFTER grade */}
      <FilmGrain />

      {/* Vignette */}
      <Vignette />

      {/* Letterbox bars — always on top */}
      <LetterboxBars />

      {/* Scene transition flashes */}
      {builtScenes.slice(0, -1).map((scene, i) => (
        <CutFlash key={i} triggerFrame={scene.from + scene.duration - 1} />
      ))}

    </AbsoluteFill>
  );
};

// ── FILM SCENE ───────────────────────────────────────────────
const FilmScene: React.FC<{ file: string; duration: number }> = ({ file, duration }) => {
  const frame = useCurrentFrame();

  // Slow Ken Burns pan — cinematic feel for static images too
  const zoom = interpolate(frame, [0, duration], [1.0, 1.05], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill>
      <OffthreadVideo
        src={staticFile(file)}
        muted
        style={{
          width: '100%', height: '100%',
          objectFit: 'cover',
          transform: `scale(${zoom})`,
        }}
      />
    </AbsoluteFill>
  );
};

// ── TITLE CARD ───────────────────────────────────────────────
const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const letters = FILM_TITLE.split('');
  const framesPerLetter = 3;

  const taglineOpacity = interpolate(
    frame,
    [letters.length * framesPerLetter + 15, letters.length * framesPerLetter + 35],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const ruleW = interpolate(
    frame,
    [letters.length * framesPerLetter + 10, letters.length * framesPerLetter + 30],
    [0, 500],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{
      backgroundColor: 'rgba(0,0,0,0.5)',
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 24,
    }}>
      {/* Title letters */}
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
        {letters.map((letter, i) => {
          const delay = i * framesPerLetter;
          const opacity = interpolate(frame - delay, [0, 10], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });
          const y = interpolate(frame - delay, [0, 12], [18, 0], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            easing: Easing.out(Easing.quad),
          });
          return (
            <span key={i} style={{
              fontSize: 140, fontWeight: 900, color: 'white',
              letterSpacing: 10, textTransform: 'uppercase',
              opacity, transform: `translateY(${y}px)`,
              display: 'inline-block',
              textShadow: '0 4px 24px rgba(0,0,0,0.8)',
            }}>
              {letter === ' ' ? '\u00A0' : letter}
            </span>
          );
        })}
      </div>

      {/* Gold rule */}
      <div style={{ width: ruleW, height: 3, backgroundColor: '#c8a96e', borderRadius: 2 }} />

      {/* Tagline */}
      <p style={{
        fontSize: 36, color: 'rgba(255,255,255,0.75)',
        fontStyle: 'italic', margin: 0,
        letterSpacing: 4, fontWeight: 300,
        opacity: taglineOpacity,
      }}>
        {TAGLINE}
      </p>
    </AbsoluteFill>
  );
};

// ── CREDIT BLOCK ─────────────────────────────────────────────
const CreditBlock: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const items = [
    { text: STUDIO_NAME,  size: 24, color: '#c8a96e', delay: 0   },
    { text: 'PRESENTS',    size: 18, color: '#888',    delay: 8   },
    { text: FILM_TITLE,    size: 72, color: 'white',   delay: fps },
    { text: RELEASE,       size: 32, color: '#c8a96e', delay: fps * 1.5 },
    { text: RATING,        size: 20, color: '#666',    delay: fps * 2   },
  ];

  return (
    <AbsoluteFill style={{
      backgroundColor: '#000',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 16,
    }}>
      {items.map((item, i) => {
        const localF = frame - item.delay;
        const appear = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
        return (
          <div key={i} style={{
            fontSize: item.size,
            color: item.color,
            fontWeight: 700,
            letterSpacing: item.size > 40 ? 8 : 6,
            textTransform: 'uppercase',
            opacity: localF > 0 ? interpolate(appear, [0, 0.5], [0, 1]) : 0,
          }}>
            {item.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ── FILM GRAIN (animated per frame) ──────────────────────────
const FilmGrain: React.FC = () => {
  const frame = useCurrentFrame();
  const seed  = (frame * 7919) % 9973;

  return (
    <AbsoluteFill style={{ opacity: 0.055, mixBlendMode: 'overlay', pointerEvents: 'none', zIndex: 50 }}>
      <svg width="100%" height="100%">
        <filter id={`grain-${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="4" seed={seed} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#grain-${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};

// ── VIGNETTE ─────────────────────────────────────────────────
const Vignette: React.FC = () => (
  <AbsoluteFill style={{
    background: 'radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,0.5) 100%)',
    pointerEvents: 'none', zIndex: 60,
  }} />
);

// ── LETTERBOX BARS (2.39:1) ───────────────────────────────────
const LetterboxBars: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const barH = interpolate(
    spring({ frame, fps, config: { damping: 120, stiffness: 80 } }),
    [0, 1], [0, 113]
  );
  return (
    <>
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: barH, backgroundColor: '#000', zIndex: 200 }} />
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: barH, backgroundColor: '#000', zIndex: 200 }} />
    </>
  );
};

// ── CUT FLASH (hard cut transition) ──────────────────────────
const CutFlash: React.FC<{ triggerFrame: number }> = ({ triggerFrame }) => {
  const frame = useCurrentFrame();
  const localF = frame - triggerFrame;
  const opacity = localF >= 0 && localF < 3
    ? interpolate(localF, [0, 1, 3], [0, 0.4, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : 0;
  return (
    <AbsoluteFill style={{ backgroundColor: 'white', opacity, pointerEvents: 'none', zIndex: 180 }} />
  );
};
