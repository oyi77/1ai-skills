// ============================================================
// ANIME OPENING SEQUENCE TEMPLATE
// Style: Japan studio quality — cel-shading, speed lines, impact frames
// Format: 16:9 1080p, 90 seconds (typical OP length)
// Requires: @remotion/noise @remotion/google-fonts @remotion/motion-blur
// Customize: SHOW_TITLE, EPISODE_TITLE, PALETTE, character images
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile,
  Easing, Img, Freeze,
} from 'remotion';
import { noise2D } from '@remotion/noise';
import { loadFont as loadBebas } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadOswald } from '@remotion/google-fonts/Oswald';

const { fontFamily: BEBAS } = loadBebas();
const { fontFamily: OSWALD } = loadOswald();

// ── CUSTOMIZE ──────────────────────────────────────────────
const SHOW_TITLE    = 'SHADOW BLADE';
const EPISODE_TITLE = 'Episode 1 — The Awakening';
const THEME_SONG    = 'opening-theme.mp3'; // place in public/audio/

const PALETTE = {
  primary: '#FF4500',
  accent:  '#FFD700',
  dark:    '#0a0500',
  outline: '#000000',
};

// Duration constants (at 30fps)
const FPS = 30;
const COLD_OPEN_END     = FPS * 8;   // 0–8s:  action cold open
const TITLE_SMASH       = FPS * 10;  // 8–10s: white flash + title
const CHAR_MONTAGE_END  = FPS * 60;  // 10–60s: character showcase
const EPIC_SEQUENCE_END = FPS * 80;  // 60–80s: epic combined action
const EPISODE_TITLE_END = FPS * 90;  // 80–90s: episode title card
// ───────────────────────────────────────────────────────────

// Cel-shading filter — the core anime look
const CEL_FILTER = 'contrast(1.35) saturate(1.5) brightness(1.02)';

// Speed lines — radial burst
const SpeedLines: React.FC<{ opacity?: number; rotate?: boolean }> = ({
  opacity = 0.65, rotate = false,
}) => {
  const frame = useCurrentFrame();
  const rotation = rotate ? (frame * 0.8) % 360 : 0;
  return (
    <AbsoluteFill style={{ opacity, pointerEvents: 'none' }}>
      <svg viewBox="0 0 1920 1080" style={{ width: '100%', height: '100%' }}>
        <g transform={`rotate(${rotation}, 960, 540)`}>
          {Array.from({ length: 40 }).map((_, i) => {
            const angle = (i / 40) * 2 * Math.PI;
            const inner = 50 + (i % 3) * 20;
            const outer = 600 + (i % 5) * 120;
            return (
              <line key={i}
                x1={960 + Math.cos(angle) * inner}
                y1={540 + Math.sin(angle) * inner}
                x2={960 + Math.cos(angle) * outer}
                y2={540 + Math.sin(angle) * outer}
                stroke="white" strokeWidth={1 + (i % 4)} opacity={0.2 + (i % 3) * 0.12}
              />
            );
          })}
        </g>
      </svg>
    </AbsoluteFill>
  );
};

// Impact white flash
const WhiteFlash: React.FC<{ triggerFrame: number; duration?: number }> = ({
  triggerFrame, duration = 4,
}) => {
  const frame = useCurrentFrame();
  const local = frame - triggerFrame;
  const opacity = interpolate(local, [0, 1, duration], [0, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  return <AbsoluteFill style={{ backgroundColor: 'white', opacity, zIndex: 300 }} />;
};

// Organic screen shake using noise
const ScreenShake: React.FC<{ children: React.ReactNode; intensity?: number }> = ({
  children, intensity = 14,
}) => {
  const frame = useCurrentFrame();
  const x = noise2D('sx', frame * 0.9, 0) * intensity;
  const y = noise2D('sy', frame * 0.9, 1) * intensity * 0.6;
  const r = noise2D('sr', frame * 0.7, 2) * 1.2;
  return (
    <AbsoluteFill style={{ transform: `translate(${x}px,${y}px) rotate(${r}deg)` }}>
      {children}
    </AbsoluteFill>
  );
};

// Halftone manga background
const HalftoneBg: React.FC<{ color?: string; dot?: string }> = ({
  color = '#fff5e6', dot = '#ffe0b2',
}) => (
  <AbsoluteFill style={{ backgroundColor: color }}>
    <svg width="100%" height="100%" style={{ position: 'absolute' }}>
      <defs>
        <pattern id="dots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
          <circle cx="12" cy="12" r="5" fill={dot} />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#dots)" />
    </svg>
  </AbsoluteFill>
);

// Character showcase card
const CharacterCard: React.FC<{
  name: string;
  title: string;
  imageSrc: string;
  enterFrom?: 'left' | 'right';
  triggerOffset?: number;
}> = ({ name, title, imageSrc, enterFrom = 'left', triggerOffset = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = frame - triggerOffset;

  const slideProgress = spring({ frame: local, fps, config: { damping: 70, stiffness: 120 } });
  const slideX = interpolate(slideProgress, [0, 1], [enterFrom === 'left' ? -400 : 400, 0]);
  const opacity = interpolate(local, [0, 12], [0, 1], { extrapolateRight: 'clamp' });

  const nameReveal = interpolate(local, [8, 30], [0, name.length], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ opacity, transform: `translateX(${slideX}px)` }}>
      {/* Character image */}
      <AbsoluteFill style={{ filter: CEL_FILTER }}>
        <Img src={staticFile(imageSrc)} style={{
          width: '100%', height: '100%', objectFit: 'contain',
          filter: `drop-shadow(4px 4px 0 #000) drop-shadow(-4px -4px 0 #000)`,
        }} />
      </AbsoluteFill>

      {/* Name bar — diagonal slash style */}
      <div style={{
        position: 'absolute', bottom: 120, left: 0,
        background: `linear-gradient(135deg, ${PALETTE.primary} 0%, ${PALETTE.primary}cc 70%, transparent 100%)`,
        padding: '16px 80px 16px 40px',
        clipPath: 'polygon(0 0, 90% 0, 100% 100%, 0 100%)',
      }}>
        <div style={{
          color: 'white', fontSize: 64, fontWeight: 900,
          fontFamily: BEBAS, letterSpacing: 4,
          textShadow: '2px 2px 0 #000',
        }}>
          {name.slice(0, Math.round(nameReveal))}
          {Math.round(nameReveal) < name.length && <span style={{ opacity: 0.4 }}>|</span>}
        </div>
        <div style={{ color: 'rgba(255,255,255,0.8)', fontSize: 24, fontFamily: OSWALD, letterSpacing: 3 }}>
          {title}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Episode title card
const EpisodeTitleCard: React.FC<{ showTitle: string; episodeTitle: string }> = ({
  showTitle, episodeTitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const showScale = spring({ frame, fps, config: { damping: 60, stiffness: 120 } });
  const epOpacity = interpolate(frame, [fps * 0.8, fps * 1.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill>
      <HalftoneBg />

      {/* Diagonal slash */}
      <div style={{
        position: 'absolute', inset: 0,
        background: `linear-gradient(135deg, ${PALETTE.primary} 45%, transparent 46%)`,
      }} />

      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 16 }}>
        <h1 style={{
          fontSize: 140, margin: 0, fontFamily: BEBAS,
          color: 'white', letterSpacing: 8,
          textShadow: `4px 4px 0 ${PALETTE.outline}, -4px -4px 0 ${PALETTE.outline}, 4px -4px 0 ${PALETTE.outline}, -4px 4px 0 ${PALETTE.outline}`,
          transform: `scale(${showScale})`,
        }}>
          {showTitle}
        </h1>
        <p style={{
          fontSize: 36, fontFamily: OSWALD, color: '#000',
          letterSpacing: 6, textTransform: 'uppercase',
          opacity: epOpacity, margin: 0,
        }}>
          {episodeTitle}
        </p>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const AnimeOpening: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: PALETTE.dark }}>
      {/* Theme song */}
      <Audio src={staticFile(`audio/${THEME_SONG}`)} startFrom={0} />

      {/* === COLD OPEN (0–8s): Action scene with speed lines === */}
      <Sequence from={0} durationInFrames={COLD_OPEN_END}>
        <AbsoluteFill style={{ filter: CEL_FILTER }}>
          <HalftoneBg color="#1a0500" dot="#2d0a00" />
          <SpeedLines opacity={0.5} />
          <ScreenShake intensity={10}>
            {/* Replace with your character action image */}
            <div style={{
              position: 'absolute', inset: 0,
              display: 'flex', justifyContent: 'center', alignItems: 'center',
            }}>
              <div style={{
                width: 400, height: 400,
                borderRadius: '50%',
                backgroundColor: PALETTE.primary,
                opacity: 0.3,
              }} />
            </div>
          </ScreenShake>
        </AbsoluteFill>
      </Sequence>

      {/* === TITLE SMASH (8–10s): White flash → show title === */}
      <Sequence from={COLD_OPEN_END} durationInFrames={FPS * 2}>
        <AbsoluteFill>
          <WhiteFlash triggerFrame={0} duration={6} />
          <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
            <h1 style={{
              fontSize: 200, fontFamily: BEBAS, color: 'white',
              letterSpacing: 16,
              textShadow: `6px 6px 0 ${PALETTE.primary}, -6px -6px 0 ${PALETTE.outline}`,
              opacity: interpolate(frame - COLD_OPEN_END, [3, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
            }}>
              {SHOW_TITLE}
            </h1>
          </AbsoluteFill>
          <SpeedLines opacity={0.3} rotate />
        </AbsoluteFill>
      </Sequence>

      {/* === CHARACTER MONTAGE (10–60s) === */}
      {/* Character 1 */}
      <Sequence from={TITLE_SMASH} durationInFrames={FPS * 10}>
        <CharacterCard
          name="RYUUJI KEN"
          title="The Shadow Blade"
          imageSrc="characters/hero.png"
          enterFrom="left"
          triggerOffset={0}
        />
      </Sequence>

      {/* Flash between characters */}
      <Sequence from={TITLE_SMASH + FPS * 9} durationInFrames={FPS * 1}>
        <WhiteFlash triggerFrame={0} duration={6} />
      </Sequence>

      {/* Character 2 */}
      <Sequence from={TITLE_SMASH + FPS * 10} durationInFrames={FPS * 10}>
        <CharacterCard
          name="MIKASA YURI"
          title="The Ice Empress"
          imageSrc="characters/rival.png"
          enterFrom="right"
          triggerOffset={0}
        />
      </Sequence>

      {/* Characters 3–N: duplicate the pattern above, adjusting from/triggerOffset */}

      {/* === EPIC SEQUENCE (60–80s): Full-power visual === */}
      <Sequence from={CHAR_MONTAGE_END} durationInFrames={EPIC_SEQUENCE_END - CHAR_MONTAGE_END}>
        <AbsoluteFill style={{ filter: CEL_FILTER }}>
          <HalftoneBg color="#0a0000" dot="#200000" />
          <SpeedLines opacity={0.8} rotate />
          <ScreenShake intensity={8}>
            {/* Epic combined scene — replace with your artwork */}
            <AbsoluteFill style={{
              justifyContent: 'center', alignItems: 'center',
              background: `radial-gradient(circle, ${PALETTE.primary}40 0%, transparent 70%)`,
            }}>
              <div style={{
                fontSize: 200, fontFamily: BEBAS, color: 'white',
                opacity: 0.12, letterSpacing: 20,
              }}>
                {SHOW_TITLE}
              </div>
            </AbsoluteFill>
          </ScreenShake>
        </AbsoluteFill>
      </Sequence>

      {/* === EPISODE TITLE (80–90s) === */}
      <Sequence from={EPIC_SEQUENCE_END} durationInFrames={EPISODE_TITLE_END - EPIC_SEQUENCE_END}>
        <EpisodeTitleCard showTitle={SHOW_TITLE} episodeTitle={EPISODE_TITLE} />
      </Sequence>
    </AbsoluteFill>
  );
};

// Root registration
export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  return (
    <Composition
      id="AnimeOpening"
      component={AnimeOpening}
      durationInFrames={EPISODE_TITLE_END}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
