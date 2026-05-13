// ============================================================
// ANIMATED LOGO / BRAND INTRO TEMPLATE
// Style: Clean, professional brand reveal — 5 seconds
// Usage: Use as intro bump for any other video
// Customize: BRAND_NAME, TAGLINE, LOGO_SVG_PATH, BRAND_COLOR
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Img, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const BRAND_NAME   = 'BerkahKarya';
const TAGLINE      = 'Digital Solutions for UMKM';
const LOGO_FILE    = 'logo.png';       // put in /public/
const BRAND_COLOR  = '#6366f1';
const BG_STYLE     = 'dark';          // 'dark' | 'light' | 'brand'

const FPS      = 30;
const DURATION = FPS * 5;   // 5-second ident — extend if needed

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="BrandIntro"
    component={BrandIntro}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const BrandIntro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const BG_COLORS = {
    dark:  '#050505',
    light: '#FAFAFA',
    brand: BRAND_COLOR,
  };
  const TEXT_COLOR = BG_STYLE === 'light' ? '#111' : '#FFF';
  const bgColor    = BG_COLORS[BG_STYLE] ?? BG_COLORS.dark;

  // ── Staggered animation sequence ──
  // 1. Circle expand (0–10f)
  const circleScale = spring({ frame, fps, config: { damping: 30, stiffness: 200 } });
  const circleOpacity = interpolate(frame, [0, 6], [0, 1], { extrapolateRight: 'clamp' });

  // 2. Logo reveal inside circle (8–20f)
  const logoScale   = spring({ frame: frame - 8, fps, config: { damping: 15, stiffness: 300 } });
  const logoOpacity = interpolate(frame - 8, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  // 3. Brand name letters (15–35f)
  const letters = BRAND_NAME.split('');
  const framesPerLetter = 2.5;

  // 4. Tagline (after all letters)
  const taglineStart  = 15 + letters.length * framesPerLetter + 5;
  const taglineOpacity = interpolate(frame - taglineStart, [0, 12], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  // 5. Rule line
  const ruleW = interpolate(
    frame, [taglineStart - 5, taglineStart + 15], [0, 200],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // 6. Fade out at end
  const fadeOut = interpolate(frame, [DURATION - 12, DURATION], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor, opacity: fadeOut }}>

      {/* Subtle radial gradient bg */}
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at 50% 50%, ${BRAND_COLOR}15, transparent 65%)`,
      }} />

      {/* Horizontal line — left */}
      <div style={{
        position: 'absolute',
        left: 0, top: '50%',
        height: 1,
        width: interpolate(frame, [12, 35], [0, '42%' as any], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        }),
        backgroundColor: `${BRAND_COLOR}40`,
      }} />

      {/* Horizontal line — right */}
      <div style={{
        position: 'absolute',
        right: 0, top: '50%',
        height: 1,
        width: interpolate(frame, [12, 35], [0, '42%' as any], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        }),
        backgroundColor: `${BRAND_COLOR}40`,
      }} />

      {/* Centre group */}
      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 20 }}>

        {/* Logo circle */}
        <div style={{
          width: 120, height: 120,
          borderRadius: '50%',
          backgroundColor: BRAND_COLOR,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          transform: `scale(${circleScale})`,
          opacity: circleOpacity,
          boxShadow: `0 0 60px ${BRAND_COLOR}60`,
        }}>
          <Img
            src={staticFile(LOGO_FILE)}
            style={{
              width: 72, height: 72,
              objectFit: 'contain',
              transform: `scale(${logoScale})`,
              opacity: logoOpacity,
            }}
          />
        </div>

        {/* Brand name */}
        <div style={{ display: 'flex' }}>
          {letters.map((letter, i) => {
            const delay   = 15 + i * framesPerLetter;
            const lOpacity = interpolate(frame - delay, [0, 8], [0, 1], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            });
            const lY = interpolate(frame - delay, [0, 10], [12, 0], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
              easing: Easing.out(Easing.cubic),
            });
            return (
              <span key={i} style={{
                fontSize: 72, fontWeight: 900,
                color: TEXT_COLOR,
                letterSpacing: 4,
                opacity: lOpacity,
                transform: `translateY(${lY}px)`,
                display: 'inline-block',
              }}>
                {letter}
              </span>
            );
          })}
        </div>

        {/* Rule + tagline */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ width: ruleW, height: 2, backgroundColor: BRAND_COLOR, borderRadius: 1 }} />
          <div style={{
            fontSize: 22, color: TEXT_COLOR,
            opacity: taglineOpacity * 0.65,
            letterSpacing: 3, textTransform: 'uppercase', fontWeight: 300,
          }}>
            {TAGLINE}
          </div>
          <div style={{ width: ruleW, height: 2, backgroundColor: BRAND_COLOR, borderRadius: 1 }} />
        </div>

      </AbsoluteFill>

    </AbsoluteFill>
  );
};
