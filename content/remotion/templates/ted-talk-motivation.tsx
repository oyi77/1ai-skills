// ============================================================
// TED TALK / MOTIVATIONAL SPEAKING TEMPLATE
// Style: TED-quality stage — restrained, authoritative, powerful
// Format: 16:9 1080p — adapt duration to talk length
// Requires: @remotion/google-fonts @remotion/captions
// Pipeline: run python scripts/pipeline.py to generate narration audio
// Customize: TALK_*, SECTIONS array
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile,
  OffthreadVideo, Easing,
} from 'remotion';
import { loadFont as loadPlayfair } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadOswald }   from '@remotion/google-fonts/Oswald';
import { loadFont as loadInter }    from '@remotion/google-fonts/Inter';

const { fontFamily: PLAYFAIR } = loadPlayfair();
const { fontFamily: OSWALD }   = loadOswald();
const { fontFamily: INTER }    = loadInter();

// ── CUSTOMIZE ──────────────────────────────────────────────
const TALK_TITLE        = 'Why Everything You Know About Success Is Wrong';
const SPEAKER_NAME      = 'Dr. Andi Kusuma';
const SPEAKER_TITLE     = 'Author & Behavioral Scientist';
const SPEAKER_ORG       = 'Institute for Human Potential';
const ACCENT_COLOR      = '#E62B1E';   // TED red — change for non-TED style

const SECTIONS = [
  {
    id: 'cold-open',
    type: 'speaker' as const,
    startSec: 0, durationSec: 60,
    speakerVideo: 'footage/speaker.mp4',
    audioSrc: 'audio/intro.mp3',
  },
  {
    id: 'title-card',
    type: 'titlecard' as const,
    startSec: 60, durationSec: 5,
  },
  {
    id: 'stat-1',
    type: 'stat' as const,
    startSec: 65, durationSec: 8,
    statValue: 87,
    statSuffix: '%',
    statLabel: 'of people never achieve their primary life goal',
    statSource: 'Harvard Business Review, 2024',
  },
  {
    id: 'part-1',
    type: 'speaker' as const,
    startSec: 73, durationSec: 120,
    speakerVideo: 'footage/speaker.mp4',
    audioSrc: 'audio/part1.mp3',
  },
  {
    id: 'quote-1',
    type: 'quote' as const,
    startSec: 193, durationSec: 10,
    quoteText: 'The system is not broken. It was never designed for you.',
    quoteAttribution: SPEAKER_NAME,
  },
  {
    id: 'part-2',
    type: 'speaker' as const,
    startSec: 203, durationSec: 150,
    speakerVideo: 'footage/speaker.mp4',
    audioSrc: 'audio/part2.mp3',
  },
  {
    id: 'chapter-2',
    type: 'chapter' as const,
    startSec: 353, durationSec: 5,
    chapterNumber: 2,
    chapterTitle: 'The Hidden Variable',
  },
  {
    id: 'stat-2',
    type: 'stat' as const,
    startSec: 358, durationSec: 8,
    statValue: 3.4,
    statSuffix: '×',
    statLabel: 'more likely to succeed with a single daily ritual',
    statSource: 'Stanford Behavior Lab, 2025',
  },
  {
    id: 'part-3',
    type: 'speaker' as const,
    startSec: 366, durationSec: 120,
    speakerVideo: 'footage/speaker.mp4',
    audioSrc: 'audio/part3.mp3',
  },
  {
    id: 'cta',
    type: 'cta' as const,
    startSec: 486, durationSec: 15,
    ctaHeadline: 'Start with one question.',
    ctaQuestion: '"What would I attempt if I knew I could not fail?"',
  },
];

const FPS = 30;
const sec = (s: number) => Math.round(s * FPS);
// ───────────────────────────────────────────────────────────

// Vignette — subtle, draws focus to speaker
const StageVignette: React.FC = () => (
  <AbsoluteFill style={{
    background: 'radial-gradient(ellipse at 50% 40%, transparent 40%, rgba(0,0,0,0.48) 100%)',
    pointerEvents: 'none',
  }} />
);

// Lower third — speaker ID
const SpeakerLowerThird: React.FC<{ triggerFrame?: number }> = ({ triggerFrame = 45 }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const localF  = frame - triggerFrame;
  const holdEnd = fps * 5;

  const slideIn = spring({ frame: localF, fps, config: { damping: 80, stiffness: 120 } });
  const x       = interpolate(slideIn, [0, 1], [-500, 0]);
  const opacity = localF > holdEnd
    ? interpolate(localF, [holdEnd, holdEnd + 18], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : localF >= 0 ? 1 : 0;

  return (
    <div style={{
      position: 'absolute', bottom: 100, left: 80,
      transform: `translateX(${x}px)`, opacity,
    }}>
      <div style={{
        borderLeft: `4px solid ${ACCENT_COLOR}`,
        backgroundColor: 'rgba(0,0,0,0.85)',
        padding: '14px 28px 14px 20px',
        backdropFilter: 'blur(4px)',
      }}>
        <div style={{ color: 'white', fontSize: 30, fontWeight: 700, fontFamily: OSWALD }}>
          {SPEAKER_NAME}
        </div>
        <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: 20, fontFamily: OSWALD, letterSpacing: 1 }}>
          {SPEAKER_TITLE} · {SPEAKER_ORG}
        </div>
      </div>
    </div>
  );
};

// Speaker on stage
const SpeakerScene: React.FC<{
  speakerVideo?: string; audioSrc?: string; showLowerThird?: boolean;
}> = ({ speakerVideo, audioSrc, showLowerThird = true }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {speakerVideo ? (
        <OffthreadVideo src={staticFile(speakerVideo)}
          style={{ width: '100%', height: '100%', objectFit: 'cover',
            filter: 'contrast(1.04) saturate(0.9) brightness(0.97)' }} />
      ) : (
        // Placeholder stage
        <AbsoluteFill style={{
          background: `radial-gradient(ellipse at 50% 80%, rgba(180,30,30,0.07) 0%, transparent 60%)`,
        }}>
          <div style={{
            position: 'absolute', bottom: 100, left: '50%',
            transform: 'translateX(-50%)',
            width: 320, height: 320, borderRadius: '50%',
            border: `3px solid ${ACCENT_COLOR}`,
            opacity: 0.6,
          }} />
        </AbsoluteFill>
      )}

      <StageVignette />
      {audioSrc && <Audio src={staticFile(audioSrc)} />}
      {showLowerThird && <SpeakerLowerThird triggerFrame={fps * 1.5} />}
    </AbsoluteFill>
  );
};

// Big stat
const StatScene: React.FC<{
  value: number; suffix?: string; label: string; source?: string;
}> = ({ value, suffix = '', label, source }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear   = spring({ frame, fps, config: { damping: 80, stiffness: 100 } });
  const opacity  = interpolate(appear, [0, 0.4], [0, 1]);
  const scale    = interpolate(appear, [0, 1], [0.88, 1]);
  const display  = Number.isInteger(value)
    ? Math.round(interpolate(appear, [0, 1], [0, value]))
    : +(interpolate(appear, [0, 1], [0, value])).toFixed(1);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0a0a0a',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 16,
    }}>
      <div style={{
        fontSize: 220, fontWeight: 900, lineHeight: 1,
        color: ACCENT_COLOR, fontFamily: OSWALD,
        fontVariantNumeric: 'tabular-nums',
        opacity, transform: `scale(${scale})`,
      }}>
        {display}{suffix}
      </div>
      <div style={{
        fontSize: 44, fontFamily: OSWALD, fontWeight: 300,
        color: 'white', letterSpacing: 6, textTransform: 'uppercase',
        opacity, maxWidth: 900, textAlign: 'center',
      }}>
        {label}
      </div>
      {source && (
        <div style={{ color: '#444', fontSize: 18, fontFamily: INTER, opacity }}>
          — {source}
        </div>
      )}

      {/* Accent rule */}
      <div style={{
        height: 3, backgroundColor: ACCENT_COLOR,
        width: interpolate(frame, [12, 28], [0, 160], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        borderRadius: 2, opacity,
      }} />
    </AbsoluteFill>
  );
};

// Pull quote
const QuoteScene: React.FC<{ text: string; attribution?: string }> = ({ text, attribution }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 70, stiffness: 100 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const y       = interpolate(appear, [0, 1], [20, 0]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'center',
      padding: '0 180px',
    }}>
      <div style={{ opacity, transform: `translateY(${y}px)`, textAlign: 'center' }}>
        {/* Decorative quotation mark */}
        <div style={{
          fontSize: 220, color: ACCENT_COLOR, opacity: 0.12,
          lineHeight: 0.6, fontFamily: 'Georgia, serif',
          userSelect: 'none',
        }}>
          "
        </div>

        <p style={{
          fontSize: 56, fontFamily: PLAYFAIR, fontStyle: 'italic',
          color: 'white', lineHeight: 1.45, margin: '-40px 0 0',
        }}>
          "{text}"
        </p>

        {attribution && (
          <p style={{
            fontSize: 28, fontFamily: OSWALD,
            color: ACCENT_COLOR, letterSpacing: 4,
            textTransform: 'uppercase', marginTop: 32,
          }}>
            — {attribution}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};

// Chapter transition
const ChapterScene: React.FC<{ number: number; title: string }> = ({ number, title }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60, stiffness: 80 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0a0a0a',
      justifyContent: 'center', alignItems: 'flex-start',
      padding: '0 140px', flexDirection: 'column', gap: 20,
    }}>
      <div style={{ color: ACCENT_COLOR, fontSize: 22, fontFamily: OSWALD, letterSpacing: 6, opacity }}>
        PART {number}
      </div>
      <h2 style={{
        fontSize: 100, fontFamily: PLAYFAIR, fontStyle: 'italic',
        color: 'white', margin: 0, lineHeight: 1.1, opacity,
        transform: `translateY(${interpolate(appear, [0, 1], [20, 0])}px)`,
      }}>
        {title}
      </h2>
      <div style={{
        height: 4, backgroundColor: ACCENT_COLOR,
        width: interpolate(frame, [8, 22], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        borderRadius: 2, opacity,
      }} />
    </AbsoluteFill>
  );
};

// Talk title card
const TalkTitleCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn  = interpolate(frame, [0, fps * 1.2], [0, 1], { extrapolateRight: 'clamp' });
  const titleOp = interpolate(frame, [fps * 0.8, fps * 2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 24,
    }}>
      <div style={{ opacity: fadeIn, color: ACCENT_COLOR, fontSize: 20, letterSpacing: 8, fontFamily: OSWALD, textTransform: 'uppercase' }}>
        TED Talk
      </div>
      <h1 style={{
        fontSize: 72, fontFamily: PLAYFAIR, fontStyle: 'italic',
        color: 'white', margin: 0, textAlign: 'center',
        maxWidth: 1300, lineHeight: 1.2, opacity: titleOp,
      }}>
        {TALK_TITLE}
      </h1>
      <div style={{
        height: 2,
        width: interpolate(frame, [fps * 2, fps * 3], [0, 360], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        backgroundColor: ACCENT_COLOR, opacity: titleOp,
      }} />
      <div style={{ color: '#666', fontSize: 24, fontFamily: OSWALD, opacity: titleOp, letterSpacing: 2 }}>
        {SPEAKER_NAME}
      </div>
    </AbsoluteFill>
  );
};

// Call to action
const CTAScene: React.FC<{ headline: string; question: string }> = ({ headline, question }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 32, padding: '0 200px',
      opacity,
    }}>
      <div style={{ fontSize: 32, fontFamily: OSWALD, color: '#666', letterSpacing: 4, textTransform: 'uppercase' }}>
        {headline}
      </div>
      <p style={{
        fontSize: 64, fontFamily: PLAYFAIR, fontStyle: 'italic',
        color: 'white', textAlign: 'center', margin: 0, lineHeight: 1.4,
      }}>
        {question}
      </p>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const TEDStyleTalk: React.FC = () => {
  const totalDuration = Math.round(
    Math.max(...SECTIONS.map(s => s.startSec + s.durationSec)) * FPS
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505' }}>
      {SECTIONS.map((section) => (
        <Sequence
          key={section.id}
          from={sec(section.startSec)}
          durationInFrames={sec(section.durationSec)}
        >
          {section.type === 'speaker' && (
            <SpeakerScene
              speakerVideo={(section as any).speakerVideo}
              audioSrc={(section as any).audioSrc}
              showLowerThird={section.id === 'cold-open'}
            />
          )}
          {section.type === 'titlecard' && <TalkTitleCard />}
          {section.type === 'stat' && (
            <StatScene
              value={(section as any).statValue}
              suffix={(section as any).statSuffix}
              label={(section as any).statLabel}
              source={(section as any).statSource}
            />
          )}
          {section.type === 'quote' && (
            <QuoteScene text={(section as any).quoteText} attribution={(section as any).quoteAttribution} />
          )}
          {section.type === 'chapter' && (
            <ChapterScene number={(section as any).chapterNumber} title={(section as any).chapterTitle} />
          )}
          {section.type === 'cta' && (
            <CTAScene headline={(section as any).ctaHeadline} question={(section as any).ctaQuestion} />
          )}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const total = Math.round(Math.max(...SECTIONS.map(s => s.startSec + s.durationSec)) * FPS);
  return (
    <Composition
      id="TEDStyleTalk"
      component={TEDStyleTalk}
      durationInFrames={total}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
