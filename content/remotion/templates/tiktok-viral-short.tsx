// ============================================================
// TIKTOK / SHORT-FORM VIRAL TEMPLATE
// Format: 9:16 vertical, 30s, hook-first structure
// Usage: npx create-video@latest → blank → replace src/
// Customize: HOOK_TEXT, BODY_LINES, CTA_TEXT, BG_COLOR
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const HOOK_TEXT = 'You\'ve been doing this WRONG 😱';
const BODY_LINES = [
  'Most people think they need hours to do this...',
  'But here\'s the 3-step shortcut nobody talks about.',
  'Step 1: Stop doing what everyone else does.',
  'Step 2: Focus on THIS one thing instead.',
  'Step 3: Watch what happens in 7 days.',
];
const CTA_TEXT = 'Follow for more tips like this 👆';
const BG_COLOR = '#0a0a0a';
const ACCENT = '#FFE500';
const FPS = 30;
const DURATION = FPS * 30; // 30 seconds

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="TikTokViral"
    component={TikTokViral}
    durationInFrames={DURATION}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const TikTokViral: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Progress bar across top
  const progress = frame / durationInFrames;

  return (
    <AbsoluteFill style={{ backgroundColor: BG_COLOR }}>

      {/* ── Progress bar (keeps viewers watching) */}
      <div style={{
        position: 'absolute', top: 0, left: 0, right: 0,
        height: 4, backgroundColor: 'rgba(255,255,255,0.15)', zIndex: 100,
      }}>
        <div style={{
          height: '100%',
          width: `${progress * 100}%`,
          backgroundColor: ACCENT,
        }} />
      </div>

      {/* ── HOOK: 0–3s ───────────────────────────── */}
      <Sequence from={0} durationInFrames={FPS * 3}>
        <HookScene text={HOOK_TEXT} />
      </Sequence>

      {/* ── BODY: 3–24s ──────────────────────────── */}
      {BODY_LINES.map((line, i) => {
        const from = FPS * 3 + i * FPS * 4.2;
        return (
          <Sequence key={i} from={Math.round(from)} durationInFrames={Math.round(FPS * 4.2)}>
            <BodyScene text={line} lineIndex={i} total={BODY_LINES.length} />
          </Sequence>
        );
      })}

      {/* ── CTA: last 3s ─────────────────────────── */}
      <Sequence from={DURATION - FPS * 3} durationInFrames={FPS * 3}>
        <CTAScene text={CTA_TEXT} />
      </Sequence>

      {/* ── Always-on caption strip ──────────────── */}
      <CaptionStrip frame={frame} />

    </AbsoluteFill>
  );
};

// ── HOOK SCENE ───────────────────────────────────────────────
const HookScene: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 8, stiffness: 500 } });
  const opacity = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: 'clamp' });

  const words = text.split(' ');

  return (
    <AbsoluteFill style={{
      justifyContent: 'center', alignItems: 'center',
      background: `radial-gradient(circle at 50% 50%, #1a1a00, ${BG_COLOR})`,
    }}>
      <div style={{
        transform: `scale(${scale})`, opacity,
        textAlign: 'center', padding: '0 60px',
      }}>
        {words.map((word, i) => (
          <span key={i} style={{
            display: 'inline-block',
            marginRight: 14,
            fontSize: 88,
            fontWeight: 900,
            color: i % 3 === 0 ? ACCENT : 'white',
            lineHeight: 1.15,
            textShadow: '3px 3px 0 rgba(0,0,0,0.5)',
          }}>
            {word}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ── BODY SCENE ───────────────────────────────────────────────
const BodyScene: React.FC<{ text: string; lineIndex: number; total: number }> = ({
  text, lineIndex, total,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60, stiffness: 120 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const y = interpolate(appear, [0, 1], [30, 0]);

  return (
    <AbsoluteFill style={{
      justifyContent: 'center', alignItems: 'center', padding: '0 60px',
    }}>
      {/* Step indicator dots */}
      <div style={{
        position: 'absolute', top: 80,
        display: 'flex', gap: 10,
      }}>
        {Array.from({ length: total }).map((_, i) => (
          <div key={i} style={{
            width: 10, height: 10, borderRadius: '50%',
            backgroundColor: i <= lineIndex ? ACCENT : 'rgba(255,255,255,0.2)',
          }} />
        ))}
      </div>

      <p style={{
        fontSize: 72,
        fontWeight: 800,
        color: 'white',
        textAlign: 'center',
        lineHeight: 1.3,
        margin: 0,
        opacity,
        transform: `translateY(${y}px)`,
      }}>
        {text}
      </p>
    </AbsoluteFill>
  );
};

// ── CTA SCENE ────────────────────────────────────────────────
const CTAScene: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 8, stiffness: 400 } });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center', alignItems: 'center',
      background: `linear-gradient(135deg, #1a1a00, #0a0a0a)`,
    }}>
      <div style={{
        backgroundColor: ACCENT,
        color: '#000',
        fontSize: 56,
        fontWeight: 900,
        padding: '24px 48px',
        borderRadius: 20,
        textAlign: 'center',
        transform: `scale(${pop})`,
        boxShadow: `0 0 60px ${ACCENT}88`,
        maxWidth: 900,
      }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

// ── CAPTION STRIP (bottom, always visible) ───────────────────
const CaptionStrip: React.FC<{ frame: number }> = ({ frame }) => {
  const allText = [HOOK_TEXT, ...BODY_LINES, CTA_TEXT].join(' ').split(' ');
  const fps = 30;
  const wordsPerSec = 2.5;
  const activeIndex = Math.floor((frame / fps) * wordsPerSec);
  const windowStart = Math.max(0, activeIndex - 4);
  const visible = allText.slice(windowStart, windowStart + 8);

  return (
    <div style={{
      position: 'absolute', bottom: 100, left: 40, right: 40,
      backgroundColor: 'rgba(0,0,0,0.7)',
      borderRadius: 12, padding: '12px 20px',
      textAlign: 'center',
    }}>
      <p style={{ color: 'white', fontSize: 36, margin: 0, lineHeight: 1.4, fontWeight: 500 }}>
        {visible.join(' ')}
      </p>
    </div>
  );
};
