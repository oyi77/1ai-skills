// ============================================================
// UGC / AUTHENTIC TESTIMONIAL AD TEMPLATE
// Style: Raw, smartphone-feel, trust-first
// Format: 9:16 vertical, 30 seconds — optimal for paid TikTok/Meta ads
// Customize: PRODUCT_NAME, HOOK, REVIEW_LINES, RESULT, CTA
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence, Img, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring,
} from 'remotion';
import { noise2D } from '@remotion/noise';

// ── CONFIG ───────────────────────────────────────────────────
const PRODUCT_NAME  = 'Nama Produkmu';
const HOOK          = 'Saya hampir nyesal nggak coba ini lebih awal 😭';
const REVIEW_LINES  = [
  'Awalnya skeptis banget...',
  'Tapi setelah 7 hari pakai...',
  'Hasilnya nggak nyangka sama sekali.',
  'Kulit saya jadi jauh lebih cerah.',
  'Dan ini beneran produk halal, no BS.',
];
const RESULT_TEXT   = 'Sebelum vs Sesudah — 7 hari';
const RATING        = 5;
const SOCIAL_PROOF  = '4,812 pembeli bulan ini';
const CTA           = 'Link di bio — gratis ongkir hari ini aja!';
const PRODUCT_IMAGE = 'product.png';       // put in /public/
const ACCENT        = '#FF4500';

const FPS      = 30;
const DURATION = FPS * 30;

// Timing
const T = {
  HOOK:   { from: 0,        dur: FPS * 4  },
  LINE_0: { from: FPS * 4,  dur: FPS * 4  },
  LINE_1: { from: FPS * 8,  dur: FPS * 4  },
  LINE_2: { from: FPS * 12, dur: FPS * 4  },
  LINE_3: { from: FPS * 16, dur: FPS * 4  },
  LINE_4: { from: FPS * 20, dur: FPS * 4  },
  CTA:    { from: FPS * 24, dur: FPS * 6  },
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="UGCTestimonialAd"
    component={UGCTestimonialAd}
    durationInFrames={DURATION}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const UGCTestimonialAd: React.FC = () => {
  const frame = useCurrentFrame();

  // Organic handheld camera shake
  const shakeX = noise2D('ugc-x', frame * 0.04, 0) * 4;
  const shakeY = noise2D('ugc-y', frame * 0.04, 1) * 3;
  const tilt   = noise2D('ugc-r', frame * 0.03, 2) * 0.3;

  return (
    <AbsoluteFill style={{
      backgroundColor: '#f5f0e8',   // warm white — feels authentic
      filter: 'contrast(1.04) saturate(0.92) brightness(1.06)',
      transform: `translate(${shakeX}px, ${shakeY}px) rotate(${tilt}deg)`,
    }}>

      {/* Star rating — top left, always visible */}
      <div style={{
        position: 'absolute', top: 60, left: 40,
        fontSize: 36, zIndex: 50,
      }}>
        {'⭐'.repeat(RATING)}
      </div>

      {/* Social proof — top right */}
      <div style={{
        position: 'absolute', top: 60, right: 40,
        backgroundColor: 'rgba(0,0,0,0.7)',
        color: 'white', fontSize: 22, fontWeight: 600,
        padding: '8px 18px', borderRadius: 20, zIndex: 50,
      }}>
        🔥 {SOCIAL_PROOF}
      </div>

      {/* HOOK */}
      <Sequence from={T.HOOK.from} durationInFrames={T.HOOK.dur}>
        <HookScene />
      </Sequence>

      {/* Review lines */}
      {REVIEW_LINES.map((line, i) => {
        const segKey = `LINE_${i}` as keyof typeof T;
        const seg    = T[segKey];
        if (!seg) return null;
        return (
          <Sequence key={i} from={seg.from} durationInFrames={seg.dur}>
            <ReviewLine text={line} index={i} total={REVIEW_LINES.length} />
          </Sequence>
        );
      })}

      {/* CTA */}
      <Sequence from={T.CTA.from} durationInFrames={T.CTA.dur}>
        <CTAScene />
      </Sequence>

      {/* Product badge — bottom, always */}
      <ProductBadge frame={frame} />

    </AbsoluteFill>
  );
};

// ── HOOK SCENE ───────────────────────────────────────────────
const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 8, stiffness: 500 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: '0 50px' }}>
      <div style={{
        backgroundColor: '#000',
        color: 'white',
        fontSize: 60,
        fontWeight: 900,
        padding: '28px 36px',
        borderRadius: 20,
        textAlign: 'center',
        lineHeight: 1.3,
        transform: `scale(${pop})`,
        boxShadow: '0 8px 40px rgba(0,0,0,0.4)',
      }}>
        {HOOK}
      </div>
    </AbsoluteFill>
  );
};

// ── REVIEW LINE ──────────────────────────────────────────────
const ReviewLine: React.FC<{ text: string; index: number; total: number }> = ({
  text, index, total,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const y       = interpolate(appear, [0, 1], [20, 0]);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: '0 50px', flexDirection: 'column', gap: 32 }}>

      {/* Progress dots */}
      <div style={{ display: 'flex', gap: 10 }}>
        {Array.from({ length: total }).map((_, i) => (
          <div key={i} style={{
            width: 10, height: 10, borderRadius: '50%',
            backgroundColor: i <= index ? ACCENT : 'rgba(0,0,0,0.2)',
          }} />
        ))}
      </div>

      {/* Text */}
      <div style={{
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderRadius: 20, padding: '28px 36px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.12)',
        opacity, transform: `translateY(${y}px)`,
        textAlign: 'center',
      }}>
        <p style={{ fontSize: 58, fontWeight: 700, color: '#111', margin: 0, lineHeight: 1.4 }}>
          {text}
        </p>
      </div>

    </AbsoluteFill>
  );
};

// ── CTA SCENE ────────────────────────────────────────────────
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 6, stiffness: 400 } });

  // Pulsing urgency
  const pulse = 1 + Math.sin(frame * 0.3) * 0.03;

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 32, padding: '0 50px' }}>

      {/* Product image */}
      <div style={{
        transform: `scale(${spring({ frame, fps, config: { damping: 60 } })})`,
      }}>
        <Img src={staticFile(PRODUCT_IMAGE)} style={{ width: 280, height: 280, objectFit: 'contain' }} />
      </div>

      {/* CTA button */}
      <div style={{
        backgroundColor: ACCENT,
        color: 'white', fontSize: 48, fontWeight: 900,
        padding: '24px 48px', borderRadius: 20,
        textAlign: 'center', lineHeight: 1.3,
        transform: `scale(${pop * pulse})`,
        boxShadow: `0 0 40px ${ACCENT}66`,
        maxWidth: 900,
      }}>
        {CTA}
      </div>

      {/* Guarantee */}
      <div style={{
        fontSize: 28, color: '#555',
        opacity: interpolate(frame, [fps * 0.5, fps * 1], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        textAlign: 'center',
      }}>
        ✅ 30-hari garansi uang kembali
      </div>

    </AbsoluteFill>
  );
};

// ── PRODUCT BADGE (always visible) ───────────────────────────
const ProductBadge: React.FC<{ frame: number }> = ({ frame }) => {
  const opacity = interpolate(frame, [15, 30], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <div style={{
      position: 'absolute', bottom: 100, left: 0, right: 0,
      display: 'flex', justifyContent: 'center',
      opacity, zIndex: 100, pointerEvents: 'none',
    }}>
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.75)',
        color: 'white', fontSize: 26, fontWeight: 700,
        padding: '8px 24px', borderRadius: 100,
      }}>
        {PRODUCT_NAME}
      </div>
    </div>
  );
};
