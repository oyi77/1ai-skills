// ============================================================
// MINI-DOCUMENTARY TEMPLATE
// Style: Netflix/Vice — journalistic, trustworthy, cinematic
// Format: 16:9 1080p, 3 minutes
// Requires: @remotion/google-fonts
// Customize: STORY_* constants, scene footage/images, narration audio
// Pipeline: run python scripts/pipeline.py --voice en to generate audio
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile,
  OffthreadVideo, Img, Easing,
} from 'remotion';
import { loadFont as loadPlayfair } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadOswald }   from '@remotion/google-fonts/Oswald';

const { fontFamily: PLAYFAIR } = loadPlayfair();
const { fontFamily: OSWALD }   = loadOswald();

// ── CUSTOMIZE ──────────────────────────────────────────────
const STORY_TITLE     = 'Against All Odds';
const STORY_YEAR      = '2025';
const STORY_DIRECTOR  = 'Your Name';

// Scene timings (seconds from start)
const SCENES = [
  {
    id: 'cold-open',
    startSec: 0, durationSec: 20,
    type: 'broll' as const,
    mediaSrc: 'footage/cold-open.mp4',
    caption: 'The story begins here.',
    grade: 'netflix' as const,
  },
  {
    id: 'title',
    startSec: 20, durationSec: 5,
    type: 'titlecard' as const,
    mediaSrc: '',
    caption: '',
    grade: 'natural' as const,
  },
  {
    id: 'interview-1',
    startSec: 25, durationSec: 35,
    type: 'interview' as const,
    mediaSrc: 'footage/interview-subject.mp4',
    caption: '',
    grade: 'natural' as const,
    speaker: { name: 'Maria Santos', title: 'Founder & CEO', audioSrc: 'audio/interview-1.mp3' },
  },
  {
    id: 'broll-context',
    startSec: 60, durationSec: 40,
    type: 'broll' as const,
    mediaSrc: 'footage/context.mp4',
    caption: '"It started with a single decision that changed everything."',
    grade: 'indie' as const,
  },
  {
    id: 'interview-2',
    startSec: 100, durationSec: 45,
    type: 'interview' as const,
    mediaSrc: 'footage/interview-2.mp4',
    caption: '',
    grade: 'natural' as const,
    speaker: { name: 'James Okoye', title: 'Business Partner', audioSrc: 'audio/interview-2.mp3' },
  },
  {
    id: 'archival',
    startSec: 145, durationSec: 20,
    type: 'archival' as const,
    mediaSrc: '',
    caption: 'Three years earlier.',
    grade: 'natural' as const,
    year: '2022 · Jakarta, Indonesia',
  },
  {
    id: 'resolution-broll',
    startSec: 165, durationSec: 30,
    type: 'broll' as const,
    mediaSrc: 'footage/resolution.mp4',
    caption: '"Today, everything is different."',
    grade: 'golden-hour' as const,
  },
  {
    id: 'end-card',
    startSec: 195, durationSec: 10,
    type: 'endcard' as const,
    mediaSrc: '',
    caption: 'This story is dedicated to everyone who dared to begin.',
    grade: 'natural' as const,
  },
];

const DOC_GRADES: Record<string, string> = {
  natural:      'contrast(1.06) saturate(0.92) brightness(1.03)',
  netflix:      'contrast(1.18) saturate(0.85) brightness(0.96) hue-rotate(-3deg)',
  indie:        'contrast(1.08) saturate(0.78) brightness(1.05) sepia(0.08)',
  'golden-hour':'contrast(1.08) saturate(1.25) sepia(0.18) brightness(1.06)',
  dark:         'contrast(1.3) saturate(0.6) brightness(0.85)',
};
// ───────────────────────────────────────────────────────────

// Subtle film vignette — always on
const Vignette: React.FC = () => (
  <AbsoluteFill style={{
    background: 'radial-gradient(ellipse at 50% 45%, transparent 50%, rgba(0,0,0,0.42) 100%)',
    pointerEvents: 'none', zIndex: 50,
  }} />
);

// Documentary lower third
const LowerThird: React.FC<{ name: string; title: string; triggerFrame?: number }> = ({
  name, title, triggerFrame = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const localF  = frame - triggerFrame;
  const holdEnd = fps * 4;

  const slideIn = spring({ frame: localF, fps, config: { damping: 100, stiffness: 80 } });
  const x       = interpolate(slideIn, [0, 1], [-480, 0]);
  const opacity = localF > holdEnd
    ? interpolate(localF, [holdEnd, holdEnd + 18], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : localF >= 0 ? 1 : 0;

  return (
    <div style={{
      position: 'absolute', bottom: 80, left: 80,
      transform: `translateX(${x}px)`, opacity,
    }}>
      <div style={{
        borderLeft: '3px solid white',
        paddingLeft: 16,
        backgroundColor: 'rgba(0,0,0,0.8)',
        padding: '12px 24px 12px 20px',
        backdropFilter: 'blur(4px)',
      }}>
        <div style={{ color: 'white', fontSize: 26, fontWeight: 600, fontFamily: OSWALD }}>{name}</div>
        <div style={{ color: 'rgba(255,255,255,0.65)', fontSize: 18, fontFamily: OSWALD, letterSpacing: 1 }}>{title}</div>
      </div>
    </div>
  );
};

// B-Roll scene with optional pull quote
const BRollScene: React.FC<{
  mediaSrc: string; caption?: string; grade: string;
}> = ({ mediaSrc, caption, grade }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textOpacity = caption
    ? interpolate(frame, [fps * 1, fps * 2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : 0;

  const hasMedia = mediaSrc.length > 0;

  return (
    <AbsoluteFill>
      {hasMedia && mediaSrc.endsWith('.mp4') && (
        <OffthreadVideo src={staticFile(mediaSrc)} muted
          style={{ width: '100%', height: '100%', objectFit: 'cover', filter: DOC_GRADES[grade] }} />
      )}
      {hasMedia && !mediaSrc.endsWith('.mp4') && (
        <Img src={staticFile(mediaSrc)}
          style={{ width: '100%', height: '100%', objectFit: 'cover', filter: DOC_GRADES[grade] }} />
      )}
      {!hasMedia && (
        <AbsoluteFill style={{ backgroundColor: '#050505', filter: DOC_GRADES[grade] }} />
      )}

      <Vignette />

      {caption && (
        <div style={{
          position: 'absolute', bottom: 80, left: 80, right: 80,
          opacity: textOpacity,
        }}>
          <p style={{
            fontSize: 40, color: 'rgba(255,255,255,0.92)', lineHeight: 1.5,
            fontStyle: 'italic', fontFamily: PLAYFAIR,
            textShadow: '0 1px 8px rgba(0,0,0,0.6)', margin: 0,
          }}>
            {caption}
          </p>
        </div>
      )}
    </AbsoluteFill>
  );
};

// Interview scene
const InterviewScene: React.FC<{
  mediaSrc: string; grade: string;
  speaker?: { name: string; title: string; audioSrc?: string };
}> = ({ mediaSrc, grade, speaker }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hasMedia = mediaSrc.length > 0;

  return (
    <AbsoluteFill>
      {hasMedia ? (
        <OffthreadVideo src={staticFile(mediaSrc)}
          style={{ width: '100%', height: '100%', objectFit: 'cover', filter: DOC_GRADES[grade] }} />
      ) : (
        <AbsoluteFill style={{ backgroundColor: '#080808' }} />
      )}

      {/* Interview depth vignette */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 35% 50%, transparent 30%, rgba(0,0,0,0.55) 100%)',
      }} />

      {speaker?.audioSrc && <Audio src={staticFile(speaker.audioSrc)} />}

      {speaker && <LowerThird name={speaker.name} title={speaker.title} triggerFrame={fps * 1.5} />}
    </AbsoluteFill>
  );
};

// Archival / text timestamp card
const ArchivalCard: React.FC<{ year: string; caption: string }> = ({ year, caption }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, fps * 0.6, fps * 3, fps * 3.5], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'flex-start',
      padding: '0 120px', flexDirection: 'column', gap: 16, opacity,
    }}>
      <div style={{ fontSize: 18, color: '#555', letterSpacing: 6, textTransform: 'uppercase' }}>{year}</div>
      <p style={{
        fontSize: 60, color: 'white', fontFamily: PLAYFAIR,
        margin: 0, lineHeight: 1.35, maxWidth: 1200, fontStyle: 'italic',
      }}>
        {caption}
      </p>
    </AbsoluteFill>
  );
};

// Title card
const TitleCard: React.FC<{ title: string; year: string; director: string }> = ({
  title, year, director,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn  = interpolate(frame, [0, fps * 1.2], [0, 1], { extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const titleOp = interpolate(frame, [fps * 0.6, fps * 1.8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const titleY  = interpolate(frame, [fps * 0.6, fps * 1.8], [10, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#020202',
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 20,
    }}>
      <div style={{ opacity: fadeIn, color: '#555', fontSize: 18, letterSpacing: 8, textTransform: 'uppercase' }}>
        {year}
      </div>
      <h1 style={{
        fontSize: 100, fontFamily: PLAYFAIR, fontStyle: 'italic',
        color: 'white', margin: 0, letterSpacing: 2,
        opacity: titleOp, transform: `translateY(${titleY}px)`,
      }}>
        {title}
      </h1>
      <div style={{
        height: 2, width: interpolate(frame, [fps * 1.8, fps * 2.5], [0, 320], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        backgroundColor: 'rgba(255,255,255,0.3)',
      }} />
      <div style={{
        opacity: interpolate(frame, [fps * 2.4, fps * 3], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        color: '#666', fontSize: 20, letterSpacing: 4,
      }}>
        A film by {director}
      </div>
    </AbsoluteFill>
  );
};

// End card
const EndCard: React.FC<{ message: string }> = ({ message }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, fps * 1], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#020202',
      justifyContent: 'center', alignItems: 'center',
      padding: '0 200px', opacity,
    }}>
      <p style={{
        fontSize: 44, color: 'rgba(255,255,255,0.85)',
        fontFamily: PLAYFAIR, fontStyle: 'italic',
        textAlign: 'center', lineHeight: 1.6, margin: 0,
      }}>
        {message}
      </p>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const MiniDoc: React.FC = () => {
  const FPS = 30;

  return (
    <AbsoluteFill style={{ backgroundColor: '#020202' }}>
      {SCENES.map((scene) => {
        const from   = Math.round(scene.startSec * FPS);
        const frames = Math.round(scene.durationSec * FPS);

        return (
          <Sequence key={scene.id} from={from} durationInFrames={frames}>
            {scene.type === 'broll'     && <BRollScene mediaSrc={scene.mediaSrc} caption={scene.caption} grade={scene.grade} />}
            {scene.type === 'interview' && <InterviewScene mediaSrc={scene.mediaSrc} grade={scene.grade} speaker={(scene as any).speaker} />}
            {scene.type === 'titlecard' && <TitleCard title={STORY_TITLE} year={STORY_YEAR} director={STORY_DIRECTOR} />}
            {scene.type === 'archival'  && <ArchivalCard year={(scene as any).year ?? ''} caption={scene.caption ?? ''} />}
            {scene.type === 'endcard'   && <EndCard message={scene.caption ?? ''} />}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const totalFrames = Math.round(SCENES.reduce((acc, s) => Math.max(acc, s.startSec + s.durationSec), 0) * 30);
  return (
    <Composition
      id="MiniDoc"
      component={MiniDoc}
      durationInFrames={totalFrames}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
