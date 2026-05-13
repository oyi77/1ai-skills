// ============================================================
// YEAR IN REVIEW / WRAPPED TEMPLATE
// Style: Spotify Wrapped energy — bold stats, colour bursts, personal data story
// Format: 9:16 vertical (1080×1920) — native mobile, OR 16:9 for YouTube
// Requires: @remotion/google-fonts @remotion/noise
// Customize: STATS, PERSON_NAME, YEAR, ACCENT colours
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile, Easing,
} from 'remotion';
import { noise2D } from '@remotion/noise';
import { loadFont as loadMontserrat } from '@remotion/google-fonts/Montserrat';
import { loadFont as loadOswald }     from '@remotion/google-fonts/Oswald';

const { fontFamily: MONT }   = loadMontserrat();
const { fontFamily: OSWALD } = loadOswald();

// ── CUSTOMIZE ──────────────────────────────────────────────
const YEAR        = '2025';
const PERSON_NAME = 'BerkahKarya';

const STATS = [
  { label: 'Minutes Listening',  value: 87240,  suffix: '',   prefix: '',  color: '#1DB954' },
  { label: 'Songs Played',       value: 4821,   suffix: '',   prefix: '',  color: '#FF4500' },
  { label: 'Top Genre',          value: 'K-Pop', suffix: '',  prefix: '',  color: '#FF69B4', isText: true },
  { label: 'Podcast Hours',      value: 312,    suffix: 'h',  prefix: '',  color: '#9147FF' },
  { label: 'New Artists Found',  value: 143,    suffix: '',   prefix: '',  color: '#FFD700' },
  { label: 'Countries Explored', value: 28,     suffix: '',   prefix: '',  color: '#00AAFF' },
];

const TOP_ITEMS = [
  { rank: 1, name: 'Taylor Swift',      sub: '1,240 plays' },
  { rank: 2, name: 'NewJeans',          sub: '890 plays' },
  { rank: 3, name: 'Arctic Monkeys',    sub: '712 plays' },
  { rank: 4, name: 'The Weeknd',        sub: '645 plays' },
  { rank: 5, name: 'IU (아이유)',        sub: '598 plays' },
];

// Format — 9:16 vertical
const WIDTH  = 1080;
const HEIGHT = 1920;
// For 16:9: WIDTH=1920, HEIGHT=1080

const FPS = 30;
const s   = (sec: number) => Math.round(sec * FPS);
// ───────────────────────────────────────────────────────────

// Animated gradient background — the Wrapped signature
const WrappedBg: React.FC<{ colors: string[] }> = ({ colors }) => {
  const frame = useCurrentFrame();

  const angle  = (frame * 0.4) % 360;
  const color1 = colors[0];
  const color2 = colors[1] ?? '#000';

  return (
    <AbsoluteFill style={{
      background: `linear-gradient(${angle}deg, ${color1} 0%, ${color2} 100%)`,
    }} />
  );
};

// Confetti burst on stat reveal
const ConfettiBurst: React.FC<{ triggerFrame: number; color: string }> = ({
  triggerFrame, color,
}) => {
  const frame  = useCurrentFrame();
  const localF = frame - triggerFrame;
  if (localF < 0 || localF > 45) return null;

  const pieces = Array.from({ length: 20 }, (_, i) => ({
    x: WIDTH * 0.5 + Math.cos((i / 20) * 2 * Math.PI) * (80 + (i % 4) * 40),
    y: HEIGHT * 0.4 + Math.sin((i / 20) * 2 * Math.PI) * (60 + (i % 3) * 30),
    size: 6 + (i % 4) * 4,
    vx: (Math.cos((i / 20) * 2 * Math.PI) * 8),
    vy: (Math.sin((i / 20) * 2 * Math.PI) * 8) + localF * 0.4,
  }));

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {pieces.map((p, i) => (
        <div key={i} style={{
          position: 'absolute',
          left: p.x + p.vx * localF,
          top: p.y + p.vy * localF,
          width: p.size, height: p.size,
          backgroundColor: i % 3 === 0 ? color : i % 3 === 1 ? 'white' : '#FFD700',
          borderRadius: i % 2 === 0 ? '50%' : 2,
          transform: `rotate(${localF * 8 + i * 30}deg)`,
          opacity: interpolate(localF, [30, 45], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }} />
      ))}
    </AbsoluteFill>
  );
};

// Opening card
const OpeningCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 8, stiffness: 300 } });
  const nameY = interpolate(frame, [fps * 0.5, fps * 1.5], [50, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const nameOp = interpolate(frame, [fps * 0.5, fps * 1.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 20 }}>
      <WrappedBg colors={['#1a0533', '#4B0082']} />

      <div style={{ transform: `scale(${scale})`, textAlign: 'center', zIndex: 10 }}>
        <div style={{
          fontSize: 36, color: 'rgba(255,255,255,0.7)', fontFamily: MONT,
          letterSpacing: 6, textTransform: 'uppercase',
        }}>
          {PERSON_NAME}'s
        </div>
        <div style={{
          fontSize: 140, fontWeight: 900, color: 'white',
          fontFamily: OSWALD, lineHeight: 1, letterSpacing: -2,
        }}>
          {YEAR}
        </div>
        <div style={{
          fontSize: 52, fontWeight: 900, color: '#1DB954',
          fontFamily: OSWALD, letterSpacing: 4, textTransform: 'uppercase',
        }}>
          Wrapped
        </div>
      </div>

      <div style={{
        color: 'rgba(255,255,255,0.6)', fontSize: 28,
        fontFamily: MONT, transform: `translateY(${nameY}px)`, opacity: nameOp,
        zIndex: 10,
      }}>
        Your year in music →
      </div>
    </AbsoluteFill>
  );
};

// Single stat card
const StatCard: React.FC<{
  stat: typeof STATS[0];
  index: number;
}> = ({ stat, index }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 10, stiffness: 400 } });
  const scale   = interpolate(appear, [0, 1], [0.3, 1]);
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  const bgColors = [
    [stat.color + '33', '#050505'],
    ['#050505', stat.color + '22'],
  ][index % 2];

  const count = stat.isText
    ? stat.value
    : Math.round(interpolate(appear, [0, 1], [0, Number(stat.value)]));

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <WrappedBg colors={bgColors} />
      <ConfettiBurst triggerFrame={8} color={stat.color} />

      <div style={{
        textAlign: 'center', padding: '0 80px',
        transform: `scale(${scale})`, opacity, zIndex: 10,
      }}>
        <div style={{ fontSize: 28, color: 'rgba(255,255,255,0.5)', fontFamily: MONT, marginBottom: 24 }}>
          This year, your
        </div>

        <div style={{
          fontSize: stat.isText ? 100 : 160,
          fontWeight: 900, color: 'white', fontFamily: OSWALD,
          lineHeight: 1, letterSpacing: -2,
          textShadow: `0 0 60px ${stat.color}80`,
        }}>
          {stat.prefix}{stat.isText ? stat.value : count.toLocaleString()}{stat.suffix}
        </div>

        <div style={{
          marginTop: 24, fontSize: 40, fontWeight: 700,
          color: stat.color, fontFamily: OSWALD, letterSpacing: 4,
          textTransform: 'uppercase',
        }}>
          {stat.label}
        </div>
      </div>

      {/* Bottom accent line */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0, height: 4,
        backgroundColor: stat.color,
        boxShadow: `0 0 20px ${stat.color}`,
      }} />
    </AbsoluteFill>
  );
};

// Top 5 list card
const TopFiveCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ padding: '100px 60px', flexDirection: 'column', gap: 28 }}>
      <WrappedBg colors={['#0a1a0a', '#051a05']} />

      <div style={{
        color: '#1DB954', fontSize: 24, fontFamily: MONT,
        letterSpacing: 6, textTransform: 'uppercase', zIndex: 10,
        opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        Your Top Artists
      </div>

      {TOP_ITEMS.map((item, i) => {
        const delay  = i * 10;
        const localF = frame - delay;
        const appear = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
        const x      = localF > 0 ? interpolate(appear, [0, 1], [-300, 0]) : -300;
        const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;

        const rankColors = ['#FFD700', '#C0C0C0', '#CD7F32', 'white', 'white'];

        return (
          <div key={i} style={{
            display: 'flex', alignItems: 'center', gap: 28,
            transform: `translateX(${x}px)`, opacity, zIndex: 10,
            borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: 20,
          }}>
            <div style={{
              fontSize: 64, fontWeight: 900, fontFamily: OSWALD,
              color: rankColors[i], lineHeight: 1, minWidth: 72, textAlign: 'center',
            }}>
              {item.rank}
            </div>
            <div>
              <div style={{ color: 'white', fontSize: 40, fontWeight: 700, fontFamily: MONT }}>
                {item.name}
              </div>
              <div style={{ color: '#1DB954', fontSize: 24, fontFamily: MONT }}>
                {item.sub}
              </div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Closing card
const ClosingCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale   = spring({ frame, fps, config: { damping: 8, stiffness: 300 } });
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 24 }}>
      <WrappedBg colors={['#1DB954', '#006633']} />

      <div style={{
        textAlign: 'center', transform: `scale(${scale})`,
        opacity, zIndex: 10,
      }}>
        <div style={{ fontSize: 48, color: 'white', fontFamily: MONT, marginBottom: 12 }}>
          Here's to
        </div>
        <div style={{
          fontSize: 120, fontWeight: 900, color: 'white',
          fontFamily: OSWALD, lineHeight: 1,
        }}>
          {Number(YEAR) + 1}
        </div>
        <div style={{ fontSize: 36, color: 'rgba(255,255,255,0.8)', fontFamily: MONT, marginTop: 16 }}>
          Keep listening 🎵
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
const CARD_DURATION = s(5);  // 5 seconds per stat card

export const YearInReview: React.FC = () => {
  const cards = [
    { id: 'opening',  from: s(0),                        frames: s(6),    component: <OpeningCard /> },
    ...STATS.map((stat, i) => ({
      id: `stat-${i}`, from: s(6 + i * 5), frames: CARD_DURATION,
      component: <StatCard stat={stat} index={i} />,
    })),
    { id: 'top5',    from: s(6 + STATS.length * 5),       frames: s(8),    component: <TopFiveCard /> },
    { id: 'closing', from: s(6 + STATS.length * 5 + 8),   frames: s(5),    component: <ClosingCard /> },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505' }}>
      {/* <Audio src={staticFile('audio/wrapped-music.mp3')} volume={0.6} /> */}
      {cards.map((card) => (
        <Sequence key={card.id} from={card.from} durationInFrames={card.frames}>
          {card.component}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const totalSec  = 6 + STATS.length * 5 + 8 + 5;
  return (
    <Composition
      id="YearInReview"
      component={YearInReview}
      durationInFrames={s(totalSec)}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
