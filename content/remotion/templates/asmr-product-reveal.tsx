// ============================================================
// ASMR / SENSORY PRODUCT REVEAL TEMPLATE
// Style: Warm, slow, macro textures, satisfying reveals
// Format: 9:16 vertical OR 16:9 — configure below
// Customize: PRODUCT_*, COLOR_*, TAGLINE
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence, OffthreadVideo, Img, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';
import { noise2D } from '@remotion/noise';

// ── CONFIG ───────────────────────────────────────────────────
const PRODUCT_NAME    = 'Nama Produkmu';
const PRODUCT_TAGLINE = 'Handcrafted with love.';
const PRODUCT_IMAGE   = 'product.png';          // put in /public/
const TEXTURE_VIDEO   = 'video/texture.mp4';   // close-up of product texture

// ASMR earth-tone palette
const COLORS = {
  bg:      '#F5F0E8',
  warm:    '#E8A838',
  sage:    '#B7C9A8',
  brown:   '#5C3D2E',
  cream:   '#FDF6EC',
  text:    '#3d2b1a',
};

// 9:16 for TikTok/Reels or 16:9 for YouTube — change here
const FORMAT = '9:16';  // '9:16' | '16:9'
const WIDTH  = FORMAT === '9:16' ? 1080 : 1920;
const HEIGHT = FORMAT === '9:16' ? 1920 : 1080;

const FPS      = 30;
const DURATION = FPS * 45;   // 45 seconds

const T = {
  TEXTURE_OPEN: { from: 0,        dur: FPS * 8  },
  REVEAL:       { from: FPS * 8,  dur: FPS * 10 },
  DETAIL_1:     { from: FPS * 18, dur: FPS * 8  },
  DETAIL_2:     { from: FPS * 26, dur: FPS * 8  },
  PRODUCT_HERO: { from: FPS * 34, dur: FPS * 11 },
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="ASMRProductReveal"
    component={ASMRProductReveal}
    durationInFrames={DURATION}
    fps={FPS}
    width={WIDTH}
    height={HEIGHT}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const ASMRProductReveal: React.FC = () => {
  const frame = useCurrentFrame();

  // Ultra-subtle organic camera drift (not shake — just drift)
  const driftX = noise2D('asmr-x', frame * 0.01, 0) * 3;
  const driftY = noise2D('asmr-y', frame * 0.01, 1) * 2;

  return (
    <AbsoluteFill style={{
      backgroundColor: COLORS.bg,
      filter: 'contrast(1.04) saturate(0.88) brightness(1.06)',
      transform: `translate(${driftX}px, ${driftY}px)`,
    }}>

      {/* Texture open — extreme close-up */}
      <Sequence from={T.TEXTURE_OPEN.from} durationInFrames={T.TEXTURE_OPEN.dur}>
        <TextureScene />
      </Sequence>

      {/* Product slow reveal */}
      <Sequence from={T.REVEAL.from} durationInFrames={T.REVEAL.dur}>
        <SlowRevealScene />
      </Sequence>

      {/* Detail shots */}
      <Sequence from={T.DETAIL_1.from} durationInFrames={T.DETAIL_1.dur}>
        <DetailScene detail="Dibuat dari bahan alami pilihan terbaik." />
      </Sequence>
      <Sequence from={T.DETAIL_2.from} durationInFrames={T.DETAIL_2.dur}>
        <DetailScene detail="Setiap butir diramu dengan penuh perhatian." />
      </Sequence>

      {/* Product hero — name + tagline */}
      <Sequence from={T.PRODUCT_HERO.from} durationInFrames={T.PRODUCT_HERO.dur}>
        <ProductHeroScene />
      </Sequence>

      {/* Soft vignette — always */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 50% 50%, transparent 50%, rgba(0,0,0,0.2) 100%)',
        pointerEvents: 'none',
      }} />

    </AbsoluteFill>
  );
};

// ── TEXTURE SCENE ────────────────────────────────────────────
const TextureScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Ultra-slow Ken Burns
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.06], { extrapolateRight: 'clamp' });

  const fadeIn = interpolate(frame, [0, fps * 1.5], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: fadeIn }}>
      <OffthreadVideo
        src={staticFile(TEXTURE_VIDEO)}
        playbackRate={0.3}   // slow motion
        muted
        style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})` }}
      />
      {/* "No sound needed" suggestion for ASMR feel */}
      <div style={{
        position: 'absolute', top: 40, right: 40,
        fontSize: 20, color: 'rgba(100,80,60,0.5)',
        letterSpacing: 3, textTransform: 'uppercase',
      }}>
        🎧 best with headphones
      </div>
    </AbsoluteFill>
  );
};

// ── SLOW REVEAL SCENE ────────────────────────────────────────
const SlowRevealScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dissolve-in
  const opacity = interpolate(frame, [0, fps * 2], [0, 1], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });

  // Gentle float-up
  const y = interpolate(frame, [0, fps * 2], [20, 0], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });

  // Ultra-slow zoom
  const scale = interpolate(frame, [0, fps * 10], [1.08, 1.0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: COLORS.cream,
      justifyContent: 'center', alignItems: 'center',
      opacity, transform: `translateY(${y}px)`,
    }}>
      <div style={{
        transform: `scale(${scale})`,
        filter: `drop-shadow(0 20px 60px rgba(92,61,46,0.25))`,
      }}>
        <Img
          src={staticFile(PRODUCT_IMAGE)}
          style={{ width: 600, height: 600, objectFit: 'contain' }}
        />
      </div>
    </AbsoluteFill>
  );
};

// ── DETAIL SCENE ─────────────────────────────────────────────
const DetailScene: React.FC<{ detail: string }> = ({ detail }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps, fps * 6, fps * 8], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const textOpacity = interpolate(frame, [fps * 1.5, fps * 2.5], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const textY = interpolate(frame, [fps * 1.5, fps * 2.5], [10, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Slow-motion product B-roll — use video or image
  const zoom = interpolate(frame, [0, fps * 8], [1.0, 1.06], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* Background image zoom */}
      <Img
        src={staticFile(PRODUCT_IMAGE)}
        style={{
          width: '100%', height: '100%', objectFit: 'cover',
          transform: `scale(${zoom})`,
          filter: 'blur(2px) brightness(0.7)',
        }}
      />

      {/* Detail text */}
      <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', padding: '0 80px 120px' }}>
        <div style={{
          backgroundColor: 'rgba(253,246,236,0.92)',
          borderRadius: 16, padding: '24px 40px',
          opacity: textOpacity, transform: `translateY(${textY}px)`,
          maxWidth: 900, textAlign: 'center',
        }}>
          <p style={{
            fontSize: 40, color: COLORS.text,
            fontStyle: 'italic', margin: 0, lineHeight: 1.5,
            fontWeight: 500,
          }}>
            {detail}
          </p>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── PRODUCT HERO SCENE ───────────────────────────────────────
const ProductHeroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear   = spring({ frame, fps, config: { damping: 60, stiffness: 80 } });
  const opacity  = interpolate(appear, [0, 0.5], [0, 1]);
  const nameY    = interpolate(appear, [0, 1], [16, 0]);

  // Fade out at very end
  const { durationInFrames } = useVideoConfig();
  const fadeOut = interpolate(frame, [durationInFrames - fps, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: COLORS.cream,
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 24,
      opacity: Math.min(opacity, fadeOut),
    }}>
      {/* Product */}
      <Img src={staticFile(PRODUCT_IMAGE)} style={{
        width: 400, height: 400, objectFit: 'contain',
        filter: `drop-shadow(0 16px 40px rgba(92,61,46,0.2))`,
        transform: `scale(${spring({ frame, fps, config: { damping: 60 } })})`,
      }} />

      {/* Name */}
      <div style={{ textAlign: 'center', transform: `translateY(${nameY}px)` }}>
        <div style={{
          fontSize: 56, fontWeight: 300, color: COLORS.text,
          letterSpacing: 8, textTransform: 'uppercase',
        }}>
          {PRODUCT_NAME}
        </div>
        <div style={{
          fontSize: 24, color: COLORS.warm, marginTop: 8,
          fontStyle: 'italic', letterSpacing: 3,
          opacity: interpolate(frame, [fps * 1.5, fps * 2.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }}>
          {PRODUCT_TAGLINE}
        </div>
      </div>

      {/* Thin accent line */}
      <div style={{
        height: 1, backgroundColor: COLORS.warm,
        width: interpolate(frame, [fps, fps * 1.8], [0, 160], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        opacity: 0.6,
      }} />
    </AbsoluteFill>
  );
};

// Helper (used in TextureScene)
const fps = 30;
