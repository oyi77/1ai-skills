// ============================================================
// E-COMMERCE STORY / REEL PACK TEMPLATE
// Style: Clean product-first — fashion, beauty, lifestyle
// Format: 9:16 (1080×1920) — Story/Reel native
// Requires: @remotion/google-fonts @remotion/noise
// Customize: BRAND_*, PRODUCTS, PALETTE
// Usage: Each card is a separate story slide — swipeable sequence
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, staticFile, Easing,
  Img, OffthreadVideo,
} from 'remotion';
import { loadFont as loadMontserrat } from '@remotion/google-fonts/Montserrat';
import { loadFont as loadPlayfair }   from '@remotion/google-fonts/PlayfairDisplay';

const { fontFamily: MONT }    = loadMontserrat();
const { fontFamily: PLAYFAIR} = loadPlayfair();

// ── CUSTOMIZE ──────────────────────────────────────────────
const BRAND_NAME     = 'LUMIÈRE';
const BRAND_HANDLE   = '@lumiere.id';
const BRAND_TAGLINE  = 'Glow From Within';

const PALETTE = {
  bg:       '#FDF9F3',   // warm white
  dark:     '#1a1008',
  accent:   '#C97B4B',   // terracotta
  text:     '#2d1a0a',
  subtle:   '#8B6914',
};

const PRODUCTS = [
  {
    id: 'p1',
    name: 'Glow Serum',
    price: 'Rp 285.000',
    originalPrice: 'Rp 380.000',
    badge: 'BESTSELLER',
    imageSrc: 'products/serum.jpg',
    videoSrc: '',
    description: 'Brightening vitamin C formula for radiant skin',
    ctaText: 'Shop Now →',
  },
  {
    id: 'p2',
    name: 'Hydra Cream',
    price: 'Rp 195.000',
    originalPrice: '',
    badge: 'NEW',
    imageSrc: 'products/cream.jpg',
    videoSrc: '',
    description: '72-hour moisture barrier for all skin types',
    ctaText: 'Discover →',
  },
  {
    id: 'p3',
    name: 'Complete Bundle',
    price: 'Rp 399.000',
    originalPrice: 'Rp 580.000',
    badge: 'SAVE 31%',
    imageSrc: 'products/bundle.jpg',
    videoSrc: '',
    description: 'Full routine: cleanser + serum + moisturiser',
    ctaText: 'Get the Bundle →',
  },
];

const WIDTH  = 1080;
const HEIGHT = 1920;
const FPS    = 30;
const s      = (sec: number) => Math.round(sec * FPS);
const CARD_DURATION = s(6);
// ───────────────────────────────────────────────────────────

// Soft vignette
const Vignette: React.FC<{ intensity?: number }> = ({ intensity = 0.15 }) => (
  <AbsoluteFill style={{
    background: `radial-gradient(ellipse at 50% 50%, transparent 50%, rgba(0,0,0,${intensity}) 100%)`,
    pointerEvents: 'none',
  }} />
);

// Story progress bars at top
const StoryProgress: React.FC<{ totalCards: number; activeIndex: number }> = ({
  totalCards, activeIndex,
}) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fillPct = Math.min((frame / CARD_DURATION) * 100, 100);

  return (
    <div style={{
      position: 'absolute', top: 24, left: 20, right: 20,
      display: 'flex', gap: 6, zIndex: 200,
    }}>
      {Array.from({ length: totalCards }).map((_, i) => (
        <div key={i} style={{
          flex: 1, height: 3,
          backgroundColor: 'rgba(255,255,255,0.35)',
          borderRadius: 2, overflow: 'hidden',
        }}>
          <div style={{
            height: '100%',
            width: i < activeIndex ? '100%' : i === activeIndex ? `${fillPct}%` : '0%',
            backgroundColor: 'white',
            borderRadius: 2,
          }} />
        </div>
      ))}
    </div>
  );
};

// Brand header
const BrandHeader: React.FC = () => (
  <div style={{
    position: 'absolute', top: 52, left: 24, right: 24,
    display: 'flex', alignItems: 'center', gap: 14, zIndex: 100,
  }}>
    {/* Brand avatar */}
    <div style={{
      width: 44, height: 44, borderRadius: '50%',
      backgroundColor: PALETTE.accent,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: 18, fontWeight: 900, color: 'white', fontFamily: MONT,
    }}>
      {BRAND_NAME[0]}
    </div>
    <div>
      <div style={{ color: 'white', fontSize: 18, fontWeight: 700, fontFamily: MONT, lineHeight: 1 }}>
        {BRAND_NAME}
      </div>
      <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: 14, fontFamily: MONT }}>
        {BRAND_HANDLE}
      </div>
    </div>
  </div>
);

// === STORY CARD: Opener ===
const OpenerCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale   = spring({ frame, fps, config: { damping: 10, stiffness: 300 } });
  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: PALETTE.dark, justifyContent: 'center', alignItems: 'center' }}>
      {/* Background texture pattern */}
      <AbsoluteFill>
        <svg width="100%" height="100%">
          <defs>
            <pattern id="dots-brand" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
              <circle cx="20" cy="20" r="1.5" fill={PALETTE.accent} opacity="0.3" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#dots-brand)" />
        </svg>
      </AbsoluteFill>

      <div style={{
        textAlign: 'center', zIndex: 10,
        transform: `scale(${scale})`, opacity,
      }}>
        <div style={{
          fontSize: 20, color: PALETTE.accent, fontFamily: MONT,
          letterSpacing: 8, textTransform: 'uppercase', marginBottom: 20,
        }}>
          {BRAND_TAGLINE}
        </div>
        <h1 style={{
          fontSize: 120, fontWeight: 900, color: 'white',
          fontFamily: MONT, lineHeight: 1, letterSpacing: -3, margin: 0,
        }}>
          {BRAND_NAME}
        </h1>
        <div style={{
          fontSize: 28, color: 'rgba(255,255,255,0.6)', fontFamily: PLAYFAIR,
          fontStyle: 'italic', marginTop: 16,
        }}>
          New Collection 2025
        </div>

        {/* Swipe up hint */}
        <div style={{
          marginTop: 60, fontSize: 20, color: 'rgba(255,255,255,0.5)',
          fontFamily: MONT, letterSpacing: 4,
          opacity: interpolate(frame, [fps * 2, fps * 2.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }}>
          SWIPE UP
          <br />↑
        </div>
      </div>
    </AbsoluteFill>
  );
};

// === STORY CARD: Product ===
const ProductCard: React.FC<{
  product: typeof PRODUCTS[0];
  cardIndex: number;
  totalCards: number;
}> = ({ product, cardIndex, totalCards }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Product image entrance
  const imageScale = spring({ frame, fps, config: { damping: 70, stiffness: 100 } });
  const infoOpacity = interpolate(frame, [fps * 0.8, fps * 1.4], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const infoY = interpolate(frame, [fps * 0.8, fps * 1.4], [20, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  const hasVideo = product.videoSrc.length > 0;

  return (
    <AbsoluteFill style={{ backgroundColor: PALETTE.bg }}>
      {/* Story progress */}
      <StoryProgress totalCards={totalCards} activeIndex={cardIndex} />
      <BrandHeader />

      {/* Product media — takes top 65% */}
      <div style={{
        position: 'absolute', top: 100, left: 0, right: 0, height: HEIGHT * 0.62,
        overflow: 'hidden',
        transform: `scale(${imageScale})`,
        transformOrigin: 'center top',
      }}>
        {hasVideo ? (
          <OffthreadVideo src={staticFile(product.videoSrc)} muted
            style={{ width: '100%', height: '100%', objectFit: 'cover',
              filter: 'contrast(1.04) saturate(0.9)' }} />
        ) : product.imageSrc ? (
          <Img src={staticFile(product.imageSrc)}
            style={{ width: '100%', height: '100%', objectFit: 'cover',
              filter: 'contrast(1.04) saturate(0.9)' }} />
        ) : (
          <div style={{
            width: '100%', height: '100%',
            background: `linear-gradient(135deg, ${PALETTE.accent}33 0%, ${PALETTE.bg} 100%)`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 80, color: PALETTE.accent, opacity: 0.3,
          }}>
            📦
          </div>
        )}
      </div>

      {/* Badge */}
      {product.badge && (
        <div style={{
          position: 'absolute', top: HEIGHT * 0.62 - 30, left: 40,
          backgroundColor: PALETTE.accent, color: 'white',
          fontSize: 18, fontWeight: 900, fontFamily: MONT,
          padding: '6px 20px', borderRadius: 999, letterSpacing: 3,
          transform: `scale(${spring({ frame: frame - fps * 0.6, fps, config: { damping: 8, stiffness: 400 } })})`,
          zIndex: 20,
        }}>
          {product.badge}
        </div>
      )}

      {/* Product info panel */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        height: HEIGHT * 0.38,
        backgroundColor: 'white',
        borderRadius: '32px 32px 0 0',
        padding: '40px 40px 60px',
        display: 'flex', flexDirection: 'column', gap: 16,
        opacity: infoOpacity, transform: `translateY(${infoY}px)`,
        boxShadow: '0 -4px 40px rgba(0,0,0,0.1)',
        zIndex: 10,
      }}>
        {/* Product name + price */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <div style={{
              fontSize: 36, fontWeight: 900, color: PALETTE.text,
              fontFamily: MONT, lineHeight: 1.1,
            }}>
              {product.name}
            </div>
            <div style={{ color: '#aaa', fontSize: 20, fontFamily: PLAYFAIR, fontStyle: 'italic', marginTop: 4 }}>
              {product.description}
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            {product.originalPrice && (
              <div style={{ color: '#aaa', fontSize: 20, textDecoration: 'line-through', fontFamily: MONT }}>
                {product.originalPrice}
              </div>
            )}
            <div style={{ fontSize: 36, fontWeight: 900, color: PALETTE.accent, fontFamily: MONT }}>
              {product.price}
            </div>
          </div>
        </div>

        {/* Star rating */}
        <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
          <span style={{ color: '#FFD700', fontSize: 24 }}>★★★★★</span>
          <span style={{ color: '#aaa', fontSize: 18, fontFamily: MONT }}>(4.9 · 2.1k reviews)</span>
        </div>

        {/* CTA button */}
        <div style={{
          backgroundColor: PALETTE.dark,
          color: 'white', fontSize: 28, fontWeight: 700, fontFamily: MONT,
          padding: '18px 0', borderRadius: 16,
          textAlign: 'center', letterSpacing: 2,
          transform: `scale(${1 + Math.sin(frame * 0.08) * 0.02})`,
          marginTop: 'auto',
        }}>
          {product.ctaText}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// === STORY CARD: Offer / Urgency ===
const OfferCard: React.FC<{ cardIndex: number; totalCards: number }> = ({ cardIndex, totalCards }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 10, stiffness: 300 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);
  const scale   = interpolate(appear, [0, 1], [0.8, 1]);

  // Countdown (48 hours)
  const secondsLeft = Math.max(0, 48 * 3600 - frame / fps);
  const h = Math.floor(secondsLeft / 3600);
  const m = Math.floor((secondsLeft % 3600) / 60);
  const s2 = Math.floor(secondsLeft % 60);

  return (
    <AbsoluteFill style={{ background: `linear-gradient(135deg, ${PALETTE.dark} 0%, #3d1500 100%)` }}>
      <StoryProgress totalCards={totalCards} activeIndex={cardIndex} />
      <BrandHeader />

      <AbsoluteFill style={{
        justifyContent: 'center', alignItems: 'center',
        flexDirection: 'column', gap: 28,
        opacity, transform: `scale(${scale})`,
        paddingTop: 80,
      }}>
        <div style={{ fontSize: 20, color: PALETTE.accent, fontFamily: MONT, letterSpacing: 6 }}>
          FLASH SALE
        </div>

        <div style={{ fontSize: 100, fontWeight: 900, color: 'white', fontFamily: MONT, lineHeight: 1, textAlign: 'center' }}>
          30%
          <br />
          <span style={{ fontSize: 48, fontWeight: 400, color: 'rgba(255,255,255,0.6)' }}>OFF EVERYTHING</span>
        </div>

        {/* Countdown */}
        <div style={{
          backgroundColor: 'rgba(255,255,255,0.08)',
          border: `2px solid ${PALETTE.accent}`,
          borderRadius: 20, padding: '24px 48px', textAlign: 'center',
        }}>
          <div style={{ color: PALETTE.accent, fontSize: 18, fontFamily: MONT, letterSpacing: 4, marginBottom: 12 }}>
            ENDS IN
          </div>
          <div style={{
            display: 'flex', gap: 20, fontSize: 64, fontWeight: 900,
            color: 'white', fontFamily: MONT, fontVariantNumeric: 'tabular-nums',
          }}>
            <div>
              <div>{String(h).padStart(2, '0')}</div>
              <div style={{ fontSize: 16, color: '#666', fontWeight: 400 }}>HRS</div>
            </div>
            <div style={{ color: PALETTE.accent }}>:</div>
            <div>
              <div>{String(m).padStart(2, '0')}</div>
              <div style={{ fontSize: 16, color: '#666', fontWeight: 400 }}>MIN</div>
            </div>
            <div style={{ color: PALETTE.accent }}>:</div>
            <div>
              <div>{String(s2).padStart(2, '0')}</div>
              <div style={{ fontSize: 16, color: '#666', fontWeight: 400 }}>SEC</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div style={{
          backgroundColor: PALETTE.accent, color: 'white',
          fontSize: 32, fontWeight: 900, fontFamily: MONT,
          padding: '20px 60px', borderRadius: 999,
          letterSpacing: 4, textTransform: 'uppercase',
          transform: `scale(${1 + Math.sin(frame * 0.1) * 0.03})`,
          boxShadow: `0 0 40px ${PALETTE.accent}80`,
        }}>
          SHOP NOW ↑
        </div>

        <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: 18, fontFamily: MONT }}>
          Link in bio → {BRAND_HANDLE}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const EcommerceStoryPack: React.FC = () => {
  const totalCards = 1 + PRODUCTS.length + 1; // opener + products + offer
  let from = 0;
  const sequences: Array<{ from: number; component: React.ReactNode }> = [];

  sequences.push({ from, component: <OpenerCard /> });
  from += CARD_DURATION;

  PRODUCTS.forEach((product, i) => {
    sequences.push({
      from,
      component: (
        <ProductCard
          product={product}
          cardIndex={i + 1}
          totalCards={totalCards}
        />
      ),
    });
    from += CARD_DURATION;
  });

  sequences.push({
    from,
    component: <OfferCard cardIndex={totalCards - 1} totalCards={totalCards} />,
  });
  from += CARD_DURATION;

  return (
    <AbsoluteFill style={{ backgroundColor: PALETTE.bg }}>
      {sequences.map((seq, i) => (
        <Sequence key={i} from={seq.from} durationInFrames={CARD_DURATION}>
          {seq.component}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const totalCards = 1 + PRODUCTS.length + 1;
  return (
    <Composition
      id="EcommerceStoryPack"
      component={EcommerceStoryPack}
      durationInFrames={totalCards * CARD_DURATION}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
