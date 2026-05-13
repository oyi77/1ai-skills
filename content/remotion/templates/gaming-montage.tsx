// ============================================================
// GAMING MONTAGE / ESPORTS HIGHLIGHT TEMPLATE
// Style: High-energy RGB — kills, plays, tier lists, rankings
// Format: 16:9 1080p OR 9:16 (change WIDTH/HEIGHT below)
// Requires: @remotion/google-fonts @remotion/noise
// Customize: GAME_TITLE, PLAYER_NAME, CLIPS, TIER_LIST
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile, Easing,
  OffthreadVideo, Img,
} from 'remotion';
import { noise2D } from '@remotion/noise';
import { loadFont as loadOswald } from '@remotion/google-fonts/Oswald';
import { loadFont as loadRoboto } from '@remotion/google-fonts/RobotoCondensed';

const { fontFamily: OSWALD } = loadOswald();
const { fontFamily: ROBOTO } = loadRoboto();

// ── CUSTOMIZE ──────────────────────────────────────────────
const GAME_TITLE   = 'Mobile Legends';
const PLAYER_NAME  = 'ShadowBlade_ID';
const PLAYER_RANK  = 'Mythical Glory';
const SEASON       = 'Season 32';

// Colour palette
const PRIMARY_COLOR = '#00FF88';   // neon green — change to your game's colour
const SECONDARY     = '#FF00AA';
const BG_COLOR      = '#050518';

// Video clips for montage (place in public/footage/)
const CLIPS = [
  { src: 'footage/clip1.mp4', label: '5-Kill Streak',    durationSec: 6  },
  { src: 'footage/clip2.mp4', label: 'Game-Winner',      durationSec: 5  },
  { src: 'footage/clip3.mp4', label: 'Insane Comeback',  durationSec: 7  },
  { src: 'footage/clip4.mp4', label: 'Perfect Execute',  durationSec: 5  },
];

// Tier list data
const TIER_LIST = [
  { tier: 'S', items: ['Ling', 'Fanny', 'Lancelot'],      color: '#FF4444' },
  { tier: 'A', items: ['Kagura', 'Harley', 'Lunox'],      color: '#FF9944' },
  { tier: 'B', items: ['Esmeralda', 'Vale', 'Cecilion'], color: '#FFEE44' },
  { tier: 'C', items: ['Gord', 'Eudora', 'Aurora'],       color: '#44FF88' },
];

// Stats
const STATS = [
  { label: 'Win Rate', value: 68.4, suffix: '%' },
  { label: 'KDA',      value: 4.2,  suffix: '' },
  { label: 'Matches',  value: 1840, suffix: '' },
];

const FPS = 30;
const s   = (sec: number) => Math.round(sec * FPS);
// ───────────────────────────────────────────────────────────

// RGB glow cycling
const useRGBColor = (speed = 1) => {
  const frame = useCurrentFrame();
  const hue   = (frame * speed * 2) % 360;
  return `hsl(${hue}, 100%, 55%)`;
};

// Scan line effect
const ScanLines: React.FC<{ opacity?: number }> = ({ opacity = 0.06 }) => (
  <AbsoluteFill style={{ pointerEvents: 'none', zIndex: 40 }}>
    <svg width="100%" height="100%">
      <defs>
        <pattern id="scanlines" x="0" y="0" width="1920" height="4" patternUnits="userSpaceOnUse">
          <rect width="1920" height="2" fill={`rgba(0,0,0,${opacity})`} />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#scanlines)" />
    </svg>
  </AbsoluteFill>
);

// RGB border glow
const RGBBorder: React.FC = () => {
  const frame = useCurrentFrame();
  const hue   = (frame * 2) % 360;

  return (
    <div style={{
      position: 'absolute', inset: 0,
      border: `3px solid hsl(${hue}, 100%, 55%)`,
      boxShadow: `inset 0 0 30px hsl(${hue}, 100%, 20%), 0 0 20px hsl(${hue}, 100%, 30%)`,
      pointerEvents: 'none', zIndex: 60,
    }} />
  );
};

// === INTRO CARD: Player reveal ===
const IntroCard: React.FC = () => {
  const frame     = useCurrentFrame();
  const { fps }   = useVideoConfig();
  const rgbColor  = useRGBColor(1.2);

  const slideUp = spring({ frame, fps, config: { damping: 12, stiffness: 300 } });
  const nameY   = interpolate(slideUp, [0, 1], [120, 0]);
  const opacity = interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' });

  // Scan line reveal
  const scanProgress = interpolate(frame, [0, fps * 0.8], [100, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: BG_COLOR }}>
      {/* Grid background */}
      <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
        {Array.from({ length: 13 }).map((_, i) => (
          <line key={`v${i}`} x1={i * 160} y1={0} x2={i * 160} y2={1080}
            stroke={`${PRIMARY_COLOR}12`} strokeWidth={1} />
        ))}
        {Array.from({ length: 8 }).map((_, i) => (
          <line key={`h${i}`} x1={0} y1={i * 135} x2={1920} y2={i * 135}
            stroke={`${PRIMARY_COLOR}12`} strokeWidth={1} />
        ))}
      </svg>

      {/* Scan line reveal effect */}
      <AbsoluteFill style={{
        backgroundColor: PRIMARY_COLOR,
        clipPath: `inset(${100 - scanProgress}% 0 0 0)`,
        opacity: 0.05,
      }} />

      <AbsoluteFill style={{
        justifyContent: 'center', alignItems: 'center',
        flexDirection: 'column', gap: 16, opacity,
      }}>
        {/* Game title */}
        <div style={{
          fontSize: 24, color: rgbColor, fontFamily: OSWALD,
          letterSpacing: 8, textTransform: 'uppercase',
        }}>
          {GAME_TITLE} · {SEASON}
        </div>

        {/* Player name */}
        <div style={{
          fontSize: 120, fontWeight: 900, color: 'white',
          fontFamily: OSWALD, lineHeight: 1, letterSpacing: -2,
          transform: `translateY(${nameY}px)`,
          textShadow: `0 0 60px ${PRIMARY_COLOR}80`,
        }}>
          {PLAYER_NAME}
        </div>

        {/* Rank badge */}
        <div style={{
          backgroundColor: 'rgba(0,255,136,0.12)',
          border: `2px solid ${PRIMARY_COLOR}`,
          borderRadius: 999, padding: '8px 28px',
          color: PRIMARY_COLOR, fontSize: 28, fontWeight: 700, fontFamily: OSWALD,
          letterSpacing: 4,
        }}>
          ★ {PLAYER_RANK}
        </div>

        {/* Stats row */}
        <div style={{ display: 'flex', gap: 48, marginTop: 16 }}>
          {STATS.map((stat, i) => {
            const delay   = 20 + i * 8;
            const localF  = frame - delay;
            const appear  = spring({ frame: Math.max(0, localF), fps, config: { damping: 80 } });
            const opacity2 = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
            const count   = localF > 0 ? interpolate(appear, [0, 1], [0, stat.value]) : 0;

            return (
              <div key={i} style={{ textAlign: 'center', opacity: opacity2 }}>
                <div style={{ fontSize: 56, fontWeight: 900, color: PRIMARY_COLOR, fontFamily: OSWALD, lineHeight: 1 }}>
                  {stat.value % 1 === 0 ? Math.round(count) : count.toFixed(1)}{stat.suffix}
                </div>
                <div style={{ color: '#666', fontSize: 18, fontFamily: ROBOTO, letterSpacing: 3, textTransform: 'uppercase' }}>
                  {stat.label}
                </div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>

      <RGBBorder />
      <ScanLines />
    </AbsoluteFill>
  );
};

// === CLIP SCENE: Gameplay highlight ===
const ClipScene: React.FC<{
  src: string;
  label: string;
  clipIndex: number;
  totalClips: number;
}> = ({ src, label, clipIndex, totalClips }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Flash on clip start
  const flashOpacity = interpolate(frame, [0, 4, 10], [0.8, 0.2, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  // Kill notification pop
  const killPop = spring({ frame: frame - fps * 0.5, fps, config: { damping: 8, stiffness: 500 } });

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* Gameplay footage */}
      {src ? (
        <OffthreadVideo src={staticFile(src)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      ) : (
        <AbsoluteFill style={{ background: `linear-gradient(135deg, #050518 0%, #0a0a2e 100%)` }} />
      )}

      {/* Flash on cut */}
      <AbsoluteFill style={{ backgroundColor: 'white', opacity: flashOpacity, pointerEvents: 'none' }} />

      {/* RGB corner accents */}
      {[['top-0 left-0', '0 0'], ['top-0 right-0', '0 180deg'], ['bottom-0 left-0', '270deg 0'], ['bottom-0 right-0', '180deg 0']].map((_, i) => (
        <div key={i} style={{
          position: 'absolute',
          ...(i === 0 && { top: 0, left: 0 }),
          ...(i === 1 && { top: 0, right: 0 }),
          ...(i === 2 && { bottom: 0, left: 0 }),
          ...(i === 3 && { bottom: 0, right: 0 }),
          width: 60, height: 60,
          border: `3px solid ${PRIMARY_COLOR}`,
          ...(i === 0 && { borderRight: 'none', borderBottom: 'none' }),
          ...(i === 1 && { borderLeft: 'none', borderBottom: 'none' }),
          ...(i === 2 && { borderRight: 'none', borderTop: 'none' }),
          ...(i === 3 && { borderLeft: 'none', borderTop: 'none' }),
          zIndex: 30,
        }} />
      ))}

      {/* Kill/Highlight notification */}
      <div style={{
        position: 'absolute', top: 40, left: '50%',
        transform: `translateX(-50%) scale(${killPop})`,
        backgroundColor: 'rgba(0,0,0,0.9)',
        border: `2px solid ${PRIMARY_COLOR}`,
        borderRadius: 8, padding: '10px 28px',
        color: PRIMARY_COLOR, fontSize: 28, fontWeight: 900, fontFamily: OSWALD,
        letterSpacing: 4, textTransform: 'uppercase',
        whiteSpace: 'nowrap',
        boxShadow: `0 0 20px ${PRIMARY_COLOR}60`,
        zIndex: 40,
      }}>
        ⚡ {label}
      </div>

      {/* Clip counter */}
      <div style={{
        position: 'absolute', bottom: 24, right: 24,
        color: 'rgba(255,255,255,0.4)', fontSize: 18, fontFamily: ROBOTO,
        zIndex: 40,
      }}>
        {clipIndex + 1}/{totalClips}
      </div>

      <ScanLines opacity={0.04} />
    </AbsoluteFill>
  );
};

// === TIER LIST CARD ===
const TierListCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: BG_COLOR, padding: '60px 80px', flexDirection: 'column', gap: 8 }}>
      {/* Header */}
      <div style={{
        fontSize: 40, fontWeight: 900, color: 'white', fontFamily: OSWALD,
        letterSpacing: 4, marginBottom: 24,
        opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        {GAME_TITLE} TIER LIST — META PATCH
      </div>

      {TIER_LIST.map((row, i) => {
        const delay   = i * 12;
        const localF  = frame - delay;
        const appear  = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
        const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
        const x       = localF > 0 ? interpolate(appear, [0, 1], [-60, 0]) : -60;

        return (
          <div key={row.tier} style={{
            display: 'flex', alignItems: 'center',
            opacity, transform: `translateX(${x}px)`,
            borderBottom: '1px solid rgba(255,255,255,0.05)',
          }}>
            {/* Tier badge */}
            <div style={{
              width: 80, height: 64,
              backgroundColor: row.color,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 40, fontWeight: 900, color: 'white', fontFamily: OSWALD,
              flexShrink: 0,
              boxShadow: `0 0 20px ${row.color}60`,
            }}>
              {row.tier}
            </div>

            {/* Items */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, padding: '8px 16px', flex: 1 }}>
              {row.items.map((item, j) => (
                <div key={j} style={{
                  backgroundColor: 'rgba(255,255,255,0.06)',
                  border: `1px solid ${row.color}40`,
                  color: 'white', fontSize: 22, fontWeight: 600, fontFamily: OSWALD,
                  padding: '6px 18px', borderRadius: 6,
                }}>
                  {item}
                </div>
              ))}
            </div>
          </div>
        );
      })}

      <div style={{
        color: '#333', fontSize: 16, fontFamily: ROBOTO, marginTop: 16,
        opacity: interpolate(frame, [fps * 2, fps * 2.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
      }}>
        Based on current meta — patch 1.8.62
      </div>
    </AbsoluteFill>
  );
};

// === OUTRO: Subscribe ===
const OutroCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);
  const scale   = interpolate(appear, [0, 1], [0.9, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: BG_COLOR,
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 24,
      opacity, transform: `scale(${scale})`,
    }}>
      <RGBBorder />

      <div style={{ fontSize: 32, color: PRIMARY_COLOR, fontFamily: OSWALD, letterSpacing: 6 }}>
        {PLAYER_NAME}
      </div>
      <div style={{
        fontSize: 80, fontWeight: 900, color: 'white',
        fontFamily: OSWALD, textAlign: 'center',
      }}>
        SUBSCRIBE
        <br />
        <span style={{ fontSize: 36, fontWeight: 400, color: '#666' }}>for daily {GAME_TITLE} content</span>
      </div>

      {/* Pulsing like button */}
      <div style={{
        backgroundColor: SECONDARY,
        color: 'white', fontSize: 32, fontWeight: 900, fontFamily: OSWALD,
        padding: '16px 48px', borderRadius: 12, letterSpacing: 4,
        transform: `scale(${1 + Math.sin(frame * 0.12) * 0.04})`,
        boxShadow: `0 0 40px ${SECONDARY}80`,
      }}>
        👍 LIKE + FOLLOW
      </div>

      <ScanLines />
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const GamingMontage: React.FC = () => {
  // Build scene timeline
  let cumulativeFrames = 0;
  const scenes: Array<{ from: number; frames: number; component: React.ReactNode }> = [];

  // Intro (6 seconds)
  scenes.push({ from: 0, frames: s(6), component: <IntroCard /> });
  cumulativeFrames = s(6);

  // Clips
  CLIPS.forEach((clip, i) => {
    scenes.push({
      from: cumulativeFrames,
      frames: s(clip.durationSec),
      component: <ClipScene src={clip.src} label={clip.label} clipIndex={i} totalClips={CLIPS.length} />,
    });
    cumulativeFrames += s(clip.durationSec);
  });

  // Tier list (8 seconds)
  scenes.push({ from: cumulativeFrames, frames: s(8), component: <TierListCard /> });
  cumulativeFrames += s(8);

  // Outro (5 seconds)
  scenes.push({ from: cumulativeFrames, frames: s(5), component: <OutroCard /> });
  cumulativeFrames += s(5);

  return (
    <AbsoluteFill style={{ backgroundColor: BG_COLOR }}>
      {/* <Audio src={staticFile('audio/montage-music.mp3')} volume={0.7} /> */}
      {scenes.map((scene, i) => (
        <Sequence key={i} from={scene.from} durationInFrames={scene.frames}>
          {scene.component}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const total = s(6) + CLIPS.reduce((acc, c) => acc + s(c.durationSec), 0) + s(8) + s(5);
  return (
    <Composition id="GamingMontage" component={GamingMontage} durationInFrames={total} fps={FPS} width={1920} height={1080} />
  );
};
