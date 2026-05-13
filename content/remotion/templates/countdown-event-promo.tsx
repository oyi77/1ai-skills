// ============================================================
// COUNTDOWN / EVENT PROMO TEMPLATE
// Style: High-energy event announcement with live countdown
// Format: 16:9 OR 9:16 — configure FORMAT below
// Customize: EVENT_*, SPEAKERS, BRAND_COLOR
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence,
  useCurrentFrame, useVideoConfig,
  interpolate, spring,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const EVENT_NAME     = 'UMKM Digital Summit 2025';
const EVENT_TAGLINE  = 'Scale your business to the next level';
const EVENT_DATE_STR = '15 Desember 2025';
const EVENT_LOCATION = 'Jakarta Convention Center';

// Days remaining until event (update before rendering)
const DAYS_REMAINING    = 21;
const HOURS_REMAINING   = 14;
const MINUTES_REMAINING = 30;

const SPEAKERS = [
  { name: 'Budi Santoso',   role: 'CEO, TechStartup ID',      emoji: '🚀' },
  { name: 'Sari Wijaya',    role: 'Head of Growth, Tokopedia', emoji: '📈' },
  { name: 'Rizky Pratama',  role: 'Founder, BerkahKarya',     emoji: '💡' },
];

const BRAND_COLOR = '#FF4500';
const BG_COLOR    = '#0a0a0a';

const FORMAT = '16:9';
const WIDTH  = FORMAT === '9:16' ? 1080 : 1920;
const HEIGHT = FORMAT === '9:16' ? 1920 : 1080;

const FPS      = 30;
const DURATION = FPS * 30;   // 30-second promo

const T = {
  HOOK:      { from: 0,        dur: FPS * 6  },
  SPEAKERS:  { from: FPS * 6,  dur: FPS * 12 },
  COUNTDOWN: { from: FPS * 18, dur: FPS * 12 },
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="EventPromo"
    component={EventPromo}
    durationInFrames={DURATION}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const EventPromo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: BG_COLOR }}>

    <Sequence from={T.HOOK.from}      durationInFrames={T.HOOK.dur}>
      <HookScene />
    </Sequence>
    <Sequence from={T.SPEAKERS.from}  durationInFrames={T.SPEAKERS.dur}>
      <SpeakersScene />
    </Sequence>
    <Sequence from={T.COUNTDOWN.from} durationInFrames={T.COUNTDOWN.dur}>
      <CountdownScene />
    </Sequence>

  </AbsoluteFill>
);

// ── HOOK ─────────────────────────────────────────────────────
const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 8, stiffness: 300 } });
  const dateOpacity = interpolate(frame, [fps, fps * 2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const locationOpacity = interpolate(frame, [fps * 1.5, fps * 2.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      background: `radial-gradient(ellipse at 50% 40%, ${BRAND_COLOR}20, ${BG_COLOR})`,
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 20,
      padding: '0 100px',
    }}>
      {/* Event name */}
      <div style={{
        fontSize: 80, fontWeight: 900, color: 'white',
        textAlign: 'center', lineHeight: 1.1,
        transform: `scale(${titleScale})`,
        textShadow: `0 0 40px ${BRAND_COLOR}66`,
      }}>
        {EVENT_NAME}
      </div>

      {/* Tagline */}
      <div style={{
        fontSize: 32, color: '#888', fontStyle: 'italic',
        opacity: dateOpacity, textAlign: 'center',
      }}>
        {EVENT_TAGLINE}
      </div>

      {/* Date + location chips */}
      <div style={{ display: 'flex', gap: 16, opacity: locationOpacity }}>
        {[`📅 ${EVENT_DATE_STR}`, `📍 ${EVENT_LOCATION}`].map((chip, i) => (
          <div key={i} style={{
            backgroundColor: 'rgba(255,255,255,0.08)',
            border: '1px solid rgba(255,255,255,0.15)',
            color: 'white', fontSize: 24, fontWeight: 600,
            padding: '10px 24px', borderRadius: 100,
          }}>
            {chip}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ── SPEAKERS ─────────────────────────────────────────────────
const SpeakersScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerOpacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ padding: '60px 100px' }}>
      <div style={{
        fontSize: 28, color: BRAND_COLOR, letterSpacing: 4,
        textTransform: 'uppercase', marginBottom: 40,
        opacity: headerOpacity,
      }}>
        Pembicara Utama
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        {SPEAKERS.map((speaker, i) => {
          const delay  = i * 10;
          const appear = spring({ frame: frame - delay, fps, config: { damping: 70 } });
          const x      = interpolate(appear, [0, 1], [-100, 0]);
          const opacity = interpolate(appear, [0, 0.4], [0, 1]);

          return (
            <div key={i} style={{
              display: 'flex', alignItems: 'center', gap: 20,
              backgroundColor: 'rgba(255,255,255,0.05)',
              border: `1px solid rgba(255,69,0,0.2)`,
              borderRadius: 16, padding: '20px 28px',
              transform: `translateX(${x}px)`, opacity,
            }}>
              <div style={{ fontSize: 48 }}>{speaker.emoji}</div>
              <div>
                <div style={{ color: 'white', fontSize: 32, fontWeight: 700 }}>{speaker.name}</div>
                <div style={{ color: BRAND_COLOR, fontSize: 20, marginTop: 3 }}>{speaker.role}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── COUNTDOWN ────────────────────────────────────────────────
const CountdownScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Simulate countdown ticking (add frame-elapsed seconds)
  const elapsed = frame / fps;
  const totalSecsRemaining = Math.max(0,
    DAYS_REMAINING * 86400 + HOURS_REMAINING * 3600 + MINUTES_REMAINING * 60 - elapsed
  );

  const d = Math.floor(totalSecsRemaining / 86400);
  const h = Math.floor((totalSecsRemaining % 86400) / 3600);
  const m = Math.floor((totalSecsRemaining % 3600) / 60);
  const s = Math.floor(totalSecsRemaining % 60);

  const appear = spring({ frame, fps, config: { damping: 60 } });

  const CountUnit: React.FC<{ value: number; label: string }> = ({ value, label }) => {
    // Flip animation on change
    const displayVal = String(value).padStart(2, '0');

    return (
      <div style={{ textAlign: 'center' }}>
        <div style={{
          backgroundColor: 'rgba(255,255,255,0.06)',
          border: `2px solid ${BRAND_COLOR}60`,
          borderRadius: 16, padding: '16px 32px',
          minWidth: 140,
        }}>
          <div style={{
            fontSize: 96, fontWeight: 900, color: 'white',
            fontVariantNumeric: 'tabular-nums', lineHeight: 1,
          }}>
            {displayVal}
          </div>
        </div>
        <div style={{
          color: '#666', fontSize: 20, letterSpacing: 4,
          textTransform: 'uppercase', marginTop: 10,
        }}>
          {label}
        </div>
      </div>
    );
  };

  return (
    <AbsoluteFill style={{
      background: `radial-gradient(ellipse at 50% 50%, ${BRAND_COLOR}15, ${BG_COLOR})`,
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 40,
      opacity: interpolate(appear, [0, 0.5], [0, 1]),
    }}>
      <div style={{ fontSize: 32, color: BRAND_COLOR, letterSpacing: 6, textTransform: 'uppercase', fontWeight: 700 }}>
        ⏱️ COUNTDOWN TO EVENT
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
        <CountUnit value={d} label="Hari" />
        <div style={{ fontSize: 80, color: BRAND_COLOR, fontWeight: 900, lineHeight: 1, paddingBottom: 32 }}>:</div>
        <CountUnit value={h} label="Jam" />
        <div style={{ fontSize: 80, color: BRAND_COLOR, fontWeight: 900, lineHeight: 1, paddingBottom: 32 }}>:</div>
        <CountUnit value={m} label="Menit" />
        <div style={{ fontSize: 80, color: BRAND_COLOR, fontWeight: 900, lineHeight: 1, paddingBottom: 32 }}>:</div>
        <CountUnit value={s} label="Detik" />
      </div>

      <div style={{
        fontSize: 28, color: '#555', textAlign: 'center',
        opacity: interpolate(frame, [fps, fps * 2], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
      }}>
        {EVENT_DATE_STR} · {EVENT_LOCATION}
      </div>
    </AbsoluteFill>
  );
};
