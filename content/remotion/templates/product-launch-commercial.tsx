// ============================================================
// PRODUCT LAUNCH / COMMERCIAL TEMPLATE
// Style: Apple-inspired — minimal, dramatic, high-quality
// Format: 16:9 1080p, 60 seconds
// Customize: PRODUCT_*, FEATURES, CTA_*, BRAND_COLOR
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence, Img, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const PRODUCT_NAME    = 'ProMax X1';
const PRODUCT_TAGLINE = 'Rethink Everything.';
const PRODUCT_IMAGE   = 'product.png';       // put in /public/
const BRAND_COLOR     = '#6366f1';            // your brand colour
const ACCENT_GOLD     = '#c8a96e';

const FEATURES = [
  { icon: '⚡', title: 'Instant Results',    body: 'See the difference in 24 hours or your money back.' },
  { icon: '🔒', title: 'Built to Last',       body: 'Premium materials, lifetime warranty included.' },
  { icon: '🌍', title: 'Loved Worldwide',     body: 'Trusted by 50,000+ customers across 40 countries.' },
];

const PRICE         = '299';
const PRICE_CROSSED = '499';
const CURRENCY      = 'Rp ';
const CTA_TEXT      = 'Order Now — Free Shipping';
const CTA_URL       = 'yourbrand.com/shop';
const URGENCY       = 'Only 47 units left at this price';

const FPS      = 30;
const DURATION = FPS * 60; // 60 seconds

// ── TIMING ───────────────────────────────────────────────────
const T = {
  COLD_OPEN:    { from: 0,         to: FPS * 4   },
  PRODUCT_IN:   { from: FPS * 4,   to: FPS * 12  },
  FEATURE_1:    { from: FPS * 12,  to: FPS * 22  },
  FEATURE_2:    { from: FPS * 22,  to: FPS * 32  },
  FEATURE_3:    { from: FPS * 32,  to: FPS * 42  },
  PRICING:      { from: FPS * 42,  to: FPS * 52  },
  CTA:          { from: FPS * 52,  to: FPS * 60  },
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="ProductLaunch"
    component={ProductLaunch}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const ProductLaunch: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#050505' }}>

    {/* Cold open — black with tagline */}
    <Sequence from={T.COLD_OPEN.from} durationInFrames={T.COLD_OPEN.to - T.COLD_OPEN.from}>
      <ColdOpen />
    </Sequence>

    {/* Product reveal */}
    <Sequence from={T.PRODUCT_IN.from} durationInFrames={T.PRODUCT_IN.to - T.PRODUCT_IN.from}>
      <ProductReveal />
    </Sequence>

    {/* Feature scenes */}
    {FEATURES.map((feature, i) => {
      const key = `FEATURE_${i + 1}` as keyof typeof T;
      const seg = T[key];
      return (
        <Sequence key={i} from={seg.from} durationInFrames={seg.to - seg.from}>
          <FeatureScene feature={feature} index={i} />
        </Sequence>
      );
    })}

    {/* Pricing */}
    <Sequence from={T.PRICING.from} durationInFrames={T.PRICING.to - T.PRICING.from}>
      <PricingScene />
    </Sequence>

    {/* CTA */}
    <Sequence from={T.CTA.from} durationInFrames={T.CTA.to - T.CTA.from}>
      <CTAScene />
    </Sequence>

  </AbsoluteFill>
);

// ── COLD OPEN ────────────────────────────────────────────────
const ColdOpen: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const scale   = interpolate(appear, [0, 1], [0.9, 1]);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ textAlign: 'center', opacity, transform: `scale(${scale})` }}>
        <div style={{ fontSize: 28, color: BRAND_COLOR, letterSpacing: 8, textTransform: 'uppercase', marginBottom: 20 }}>
          Introducing
        </div>
        <div style={{ fontSize: 120, fontWeight: 900, color: 'white', letterSpacing: 4 }}>
          {PRODUCT_NAME}
        </div>
        <div style={{ fontSize: 36, color: '#666', marginTop: 16, fontStyle: 'italic' }}>
          {PRODUCT_TAGLINE}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── PRODUCT REVEAL ───────────────────────────────────────────
const ProductReveal: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spotlight swings in from above
  const spotY = interpolate(frame, [0, fps * 1.2], [-300, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Product scales up
  const productScale = spring({ frame: frame - fps * 0.5, fps, config: { damping: 50, stiffness: 100 } });

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505', justifyContent: 'center', alignItems: 'center' }}>
      {/* Spotlight */}
      <div style={{
        position: 'absolute', width: 700, height: 700,
        borderRadius: '50%', top: '50%', left: '50%',
        transform: `translate(-50%, calc(-50% + ${spotY}px))`,
        background: `radial-gradient(circle, ${BRAND_COLOR}18 0%, transparent 70%)`,
      }} />

      {/* Product */}
      <div style={{
        transform: `scale(${productScale})`,
        filter: `drop-shadow(0 40px 80px ${BRAND_COLOR}40)`,
      }}>
        <Img
          src={staticFile(PRODUCT_IMAGE)}
          style={{ width: 560, height: 560, objectFit: 'contain' }}
        />
      </div>

      {/* Name fades in */}
      <div style={{
        position: 'absolute', bottom: 120, textAlign: 'center',
        opacity: interpolate(frame, [fps * 2, fps * 3], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
      }}>
        <div style={{ fontSize: 56, fontWeight: 300, color: 'white', letterSpacing: 8 }}>
          {PRODUCT_NAME}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── FEATURE SCENE ────────────────────────────────────────────
const FeatureScene: React.FC<{ feature: typeof FEATURES[0]; index: number }> = ({ feature, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 70, stiffness: 100 } });
  const x = interpolate(appear, [0, 1], [-120, 0]);
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);

  const iconScale = spring({ frame: frame - 5, fps, config: { damping: 8, stiffness: 400 } });

  const bgColors = ['#0d0d1a', '#0d1a0d', '#1a0d0d'];

  return (
    <AbsoluteFill style={{ backgroundColor: bgColors[index % 3], justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ maxWidth: 1200, textAlign: 'center', opacity, transform: `translateX(${x}px)` }}>

        {/* Icon */}
        <div style={{
          fontSize: 120,
          transform: `scale(${iconScale})`,
          marginBottom: 40,
          display: 'block',
          lineHeight: 1,
        }}>
          {feature.icon}
        </div>

        {/* Title */}
        <div style={{ fontSize: 80, fontWeight: 900, color: 'white', marginBottom: 24, lineHeight: 1.1 }}>
          {feature.title}
        </div>

        {/* Body */}
        <div style={{ fontSize: 40, color: '#888', lineHeight: 1.6, fontWeight: 300 }}>
          {feature.body}
        </div>

        {/* Accent line */}
        <div style={{
          width: interpolate(frame, [5, 25], [0, 120], { extrapolateRight: 'clamp' }),
          height: 3, backgroundColor: BRAND_COLOR, borderRadius: 2,
          margin: '40px auto 0',
        }} />
      </div>
    </AbsoluteFill>
  );
};

// ── PRICING SCENE ────────────────────────────────────────────
const PricingScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  // Cross-out animation on old price
  const crossWidth = interpolate(frame, [fps * 0.8, fps * 1.2], [0, 100], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  // New price pops in
  const priceScale = spring({ frame: frame - fps * 1.5, fps, config: { damping: 8, stiffness: 300 } });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 32,
    }}>
      <div style={{ opacity }}>

        {/* Crossed out original price */}
        <div style={{ position: 'relative', display: 'inline-block', marginBottom: 8 }}>
          <div style={{ fontSize: 48, color: '#444', fontWeight: 300 }}>
            {CURRENCY}{PRICE_CROSSED}
          </div>
          <div style={{
            position: 'absolute', top: '50%', left: 0,
            height: 2, backgroundColor: '#CC2200',
            width: `${crossWidth}%`,
          }} />
        </div>

        {/* New price */}
        <div style={{
          fontSize: 140, fontWeight: 900,
          color: ACCENT_GOLD,
          transform: `scale(${priceScale})`,
          lineHeight: 1,
          filter: `drop-shadow(0 0 30px ${ACCENT_GOLD}44)`,
        }}>
          {CURRENCY}{PRICE}
        </div>

        {/* Urgency */}
        <div style={{
          fontSize: 28, color: '#CC4400', fontWeight: 600, marginTop: 16,
          backgroundColor: 'rgba(200,68,0,0.12)',
          padding: '8px 24px', borderRadius: 8, display: 'inline-block',
          opacity: interpolate(frame, [fps * 2, fps * 2.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }}>
          ⚠️ {URGENCY}
        </div>

      </div>
    </AbsoluteFill>
  );
};

// ── CTA SCENE ────────────────────────────────────────────────
const CTAScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 8, stiffness: 300 } });
  const urlOpacity = interpolate(frame, [fps * 0.8, fps * 1.4], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  // Pulsing glow on button
  const glowSize = 30 + Math.sin(frame * 0.15) * 10;

  return (
    <AbsoluteFill style={{
      background: `linear-gradient(135deg, #0d0d2e, #050505)`,
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 40,
    }}>
      <div style={{
        backgroundColor: BRAND_COLOR,
        color: 'white',
        fontSize: 52,
        fontWeight: 900,
        padding: '28px 80px',
        borderRadius: 20,
        transform: `scale(${pop})`,
        boxShadow: `0 0 ${glowSize}px ${BRAND_COLOR}88`,
        textAlign: 'center',
      }}>
        {CTA_TEXT}
      </div>

      <div style={{ color: '#666', fontSize: 28, opacity: urlOpacity }}>
        {CTA_URL}
      </div>
    </AbsoluteFill>
  );
};
