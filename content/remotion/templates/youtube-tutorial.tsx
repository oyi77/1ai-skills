// ============================================================
// YOUTUBE TUTORIAL / EDUCATION TEMPLATE
// Style: Modern edu — clean, typographic, authoritative
// Format: 16:9 1080p, 3 minutes (customizable)
// Customize: TOPIC, STEPS, CHANNEL_NAME, ACCENT
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const CHANNEL_NAME  = 'BerkahKarya';
const VIDEO_TITLE   = 'How to Grow Your UMKM Online in 2025';
const HOOK_STAT     = '97%';
const HOOK_STAT_LABEL = 'of small businesses fail online — because of this one mistake.';
const ACCENT        = '#6366f1';
const BG_DARK       = '#0f172a';

const STEPS = [
  {
    number: '01',
    title: 'Fix Your Foundation First',
    body: 'Before running ads, make sure your offer is clear and your landing page converts.',
    tip: 'A bad landing page kills good traffic. Fix the leak before turning on the tap.',
    icon: '🏗️',
  },
  {
    number: '02',
    title: 'Start With Content, Not Ads',
    body: 'Create 30 days of organic content before spending a single rupiah on ads.',
    tip: 'Organic content validates your message. If it doesn\'t work free, it won\'t work paid.',
    icon: '📝',
  },
  {
    number: '03',
    title: 'Pick ONE Platform',
    body: 'Master TikTok or Instagram — not both. Depth beats breadth for new accounts.',
    tip: 'The algorithm rewards consistency. Post 1× daily on one platform for 90 days.',
    icon: '🎯',
  },
  {
    number: '04',
    title: 'Measure What Matters',
    body: 'Track saves and shares, not just likes. Saves = people want to remember this.',
    tip: 'Saves are the strongest signal that your content is valuable, not just entertaining.',
    icon: '📊',
  },
];

const MISTAKE_TEXT = 'Most businesses try to do everything at once — and do nothing well.';
const SUMMARY_POINTS = STEPS.map(s => `${s.number}. ${s.title}`);

const FPS      = 30;
const STEP_DUR = FPS * 28; // 28s per step
const DURATION = FPS * 20 + STEPS.length * STEP_DUR + FPS * 20; // hook + steps + outro

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="Tutorial"
    component={Tutorial}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const Tutorial: React.FC = () => {
  const stepStart = FPS * 20;

  return (
    <AbsoluteFill style={{ backgroundColor: BG_DARK }}>

      {/* Hook */}
      <Sequence from={0} durationInFrames={FPS * 20}>
        <HookScene />
      </Sequence>

      {/* Steps */}
      {STEPS.map((step, i) => (
        <Sequence key={i} from={stepStart + i * STEP_DUR} durationInFrames={STEP_DUR}>
          <StepScene step={step} stepIndex={i} totalSteps={STEPS.length} />
        </Sequence>
      ))}

      {/* Outro / Summary */}
      <Sequence from={stepStart + STEPS.length * STEP_DUR} durationInFrames={FPS * 20}>
        <OutroScene />
      </Sequence>

      {/* Persistent channel watermark */}
      <ChannelWatermark />

    </AbsoluteFill>
  );
};

// ── HOOK SCENE ───────────────────────────────────────────────
const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Stat pops first
  const statScale = spring({ frame, fps, config: { damping: 8, stiffness: 400 } });
  // Title slides in
  const titleX = interpolate(
    spring({ frame: frame - fps * 1.2, fps, config: { damping: 70 } }),
    [0, 1], [-80, 0]
  );
  const titleOpacity = interpolate(frame - fps * 1.2, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 32, padding: '0 160px' }}>

      {/* Big stat */}
      <div style={{ textAlign: 'center', transform: `scale(${statScale})` }}>
        <div style={{ fontSize: 200, fontWeight: 900, color: ACCENT, lineHeight: 1 }}>
          {HOOK_STAT}
        </div>
        <div style={{ fontSize: 40, color: '#94a3b8', lineHeight: 1.5, maxWidth: 1000 }}>
          {HOOK_STAT_LABEL}
        </div>
      </div>

      {/* Mistake text */}
      <div style={{
        backgroundColor: 'rgba(239,68,68,0.1)',
        border: '1px solid rgba(239,68,68,0.3)',
        borderRadius: 16, padding: '24px 48px',
        opacity: titleOpacity,
        transform: `translateX(${titleX}px)`,
      }}>
        <p style={{ color: '#fca5a5', fontSize: 36, margin: 0, fontStyle: 'italic', textAlign: 'center' }}>
          "{MISTAKE_TEXT}"
        </p>
      </div>

      {/* Promise */}
      <div style={{ opacity: interpolate(frame, [fps * 2.5, fps * 3.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }), textAlign: 'center' }}>
        <p style={{ color: 'white', fontSize: 44, fontWeight: 700, margin: 0 }}>
          In this video: {STEPS.length} steps that actually fix it.
        </p>
      </div>

    </AbsoluteFill>
  );
};

// ── STEP SCENE ───────────────────────────────────────────────
const StepScene: React.FC<{ step: typeof STEPS[0]; stepIndex: number; totalSteps: number }> = ({
  step, stepIndex, totalSteps,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Entrance
  const appear  = spring({ frame, fps, config: { damping: 60, stiffness: 100 } });
  const contentOpacity = interpolate(appear, [0, 0.5], [0, 1]);
  const contentY = interpolate(appear, [0, 1], [20, 0]);

  // Icon pop
  const iconScale = spring({ frame: frame - 5, fps, config: { damping: 8, stiffness: 400 } });

  // Tip appears halfway through
  const tipOpacity = interpolate(frame, [fps * 8, fps * 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Step progress bar
  const stepProgress = frame / durationInFrames;

  return (
    <AbsoluteFill style={{ backgroundColor: BG_DARK }}>

      {/* Progress dots */}
      <div style={{ position: 'absolute', top: 48, right: 60, display: 'flex', gap: 10 }}>
        {Array.from({ length: totalSteps }).map((_, i) => (
          <div key={i} style={{
            width: 12, height: 12, borderRadius: '50%',
            backgroundColor: i < stepIndex ? ACCENT : i === stepIndex ? 'white' : '#334155',
            outline: i === stepIndex ? `2px solid ${ACCENT}` : 'none',
            outlineOffset: 2,
          }} />
        ))}
      </div>

      {/* Step progress bar bottom */}
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 3, backgroundColor: '#1e293b' }}>
        <div style={{ height: '100%', width: `${stepProgress * 100}%`, backgroundColor: ACCENT }} />
      </div>

      {/* Main content */}
      <div style={{
        padding: '80px 120px',
        display: 'flex', gap: 80, alignItems: 'center',
        opacity: contentOpacity, transform: `translateY(${contentY}px)`,
      }}>

        {/* Left: number + icon */}
        <div style={{ textAlign: 'center', minWidth: 200 }}>
          <div style={{ fontSize: 120, fontWeight: 900, color: ACCENT, lineHeight: 1 }}>
            {step.number}
          </div>
          <div style={{ fontSize: 80, transform: `scale(${iconScale})`, marginTop: 8 }}>
            {step.icon}
          </div>
        </div>

        {/* Right: title + body + tip */}
        <div style={{ flex: 1 }}>
          <h2 style={{ fontSize: 72, fontWeight: 900, color: 'white', margin: '0 0 24px', lineHeight: 1.1 }}>
            {step.title}
          </h2>
          <p style={{ fontSize: 36, color: '#94a3b8', lineHeight: 1.7, margin: '0 0 32px' }}>
            {step.body}
          </p>

          {/* Pro tip */}
          <div style={{
            backgroundColor: `${ACCENT}15`,
            border: `1px solid ${ACCENT}40`,
            borderRadius: 12, padding: '16px 24px',
            opacity: tipOpacity,
          }}>
            <div style={{ color: ACCENT, fontSize: 18, fontWeight: 700, letterSpacing: 3, textTransform: 'uppercase', marginBottom: 6 }}>
              💡 PRO TIP
            </div>
            <p style={{ color: '#c7d2fe', fontSize: 28, margin: 0, lineHeight: 1.5, fontStyle: 'italic' }}>
              {step.tip}
            </p>
          </div>
        </div>

      </div>
    </AbsoluteFill>
  );
};

// ── OUTRO SCENE ──────────────────────────────────────────────
const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor: BG_DARK,
      justifyContent: 'center', alignItems: 'flex-start',
      flexDirection: 'column', padding: '0 120px', gap: 20,
    }}>
      <div style={{
        fontSize: 28, color: ACCENT, letterSpacing: 4, textTransform: 'uppercase',
        opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        Summary
      </div>
      <h2 style={{
        fontSize: 64, fontWeight: 900, color: 'white',
        margin: '0 0 32px', lineHeight: 1.1,
        opacity: interpolate(frame, [5, 20], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        {VIDEO_TITLE}
      </h2>

      {SUMMARY_POINTS.map((point, i) => {
        const delay = 15 + i * 10;
        const appear = spring({ frame: frame - delay, fps, config: { damping: 70 } });
        return (
          <div key={i} style={{
            fontSize: 36, color: '#e2e8f0', fontWeight: 500,
            opacity: interpolate(appear, [0, 0.5], [0, 1]),
            transform: `translateX(${interpolate(appear, [0, 1], [-30, 0])}px)`,
            display: 'flex', alignItems: 'center', gap: 16,
          }}>
            <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: ACCENT }} />
            {point}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ── CHANNEL WATERMARK (persistent) ───────────────────────────
const ChannelWatermark: React.FC = () => (
  <div style={{
    position: 'absolute', top: 40, left: 60,
    backgroundColor: 'rgba(0,0,0,0.5)',
    color: 'rgba(255,255,255,0.5)',
    fontSize: 20, fontWeight: 600,
    padding: '6px 16px', borderRadius: 20,
    letterSpacing: 1,
  }}>
    @{CHANNEL_NAME}
  </div>
);
