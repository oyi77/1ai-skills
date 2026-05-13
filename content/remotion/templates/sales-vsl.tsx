// ============================================================
// VIDEO SALES LETTER (VSL) / SALES FUNNEL TEMPLATE
// Structure: PASM — Pain → Agitate → Solution → Momentum
// Format: 16:9 1080p, 90 seconds (optimal conversion length)
// Requires: @remotion/google-fonts
// Pipeline: run python scripts/pipeline.py to generate narration
// Customize: PRODUCT_*, PAIN_*, OFFER_*, TESTIMONIALS
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile, Easing,
} from 'remotion';
import { loadFont as loadOswald }   from '@remotion/google-fonts/Oswald';
import { loadFont as loadInter }    from '@remotion/google-fonts/Inter';
import { loadFont as loadPlayfair } from '@remotion/google-fonts/PlayfairDisplay';

const { fontFamily: OSWALD }   = loadOswald();
const { fontFamily: INTER }    = loadInter();
const { fontFamily: PLAYFAIR } = loadPlayfair();

// ── CUSTOMIZE ──────────────────────────────────────────────
const PRODUCT_NAME   = 'AdForge Pro';
const PRODUCT_TAGLINE= 'AI-Powered Facebook Ads That Actually Convert';
const ACCENT_COLOR   = '#6366f1';  // indigo
const DANGER_COLOR   = '#ef4444';  // red (pain phase)
const SUCCESS_COLOR  = '#22c55e';  // green (solution phase)

// PASM sections (in seconds)
const PAIN_TEXT = 'You\'re spending money on Facebook ads that don\'t work.';
const AGITATE_STATS = [
  '73% of small business ad budgets are wasted on wrong audiences',
  'Average SMB loses Rp 8.4M per month on underperforming ads',
  'Most ad managers take 3-6 months to learn — your business can\'t wait',
];

const FEATURES = [
  { icon: '🤖', title: 'AI Ad Copy Generator',   desc: 'Writes 50+ variants, picks the winner automatically' },
  { icon: '🎯', title: 'Smart Audience Finder',  desc: 'Reaches your buyer profile, not random scrollers' },
  { icon: '📊', title: 'Real-Time Optimizer',    desc: 'Adjusts bids and budgets every 15 minutes' },
  { icon: '⚡', title: '10-Minute Setup',         desc: 'Connect your account, launch your first campaign' },
];

const TESTIMONIALS = [
  { name: 'Sari W.', role: 'Clothing Store Owner', result: 'ROAS 6.2× dalam 30 hari' },
  { name: 'Budi K.', role: 'Restaurant Chain',     result: '340% more walk-ins from local ads' },
];

const OFFER = {
  originalPrice: 'Rp 2,400,000',
  currentPrice:  'Rp 890,000',
  period:        '/bulan',
  guarantee:     '30-day money-back guarantee',
  scarcity:      'Price increases in 48 hours',
  cta:           'Start Free Trial → No Credit Card',
  url:           'adforge.berkahkarya.org',
};

const FPS = 30;
const s   = (sec: number) => Math.round(sec * FPS);
// ───────────────────────────────────────────────────────────

// Progress bar — subliminal commitment device
const VideoProgress: React.FC = () => {
  const frame   = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = frame / durationInFrames;

  return (
    <div style={{
      position: 'absolute', top: 0, left: 0, right: 0, height: 3, zIndex: 200,
      backgroundColor: 'rgba(255,255,255,0.1)',
    }}>
      <div style={{
        height: '100%', width: `${progress * 100}%`,
        backgroundColor: ACCENT_COLOR,
      }} />
    </div>
  );
};

// === PHASE 1: PAIN (0–15s) ===
const PainScene: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);
  const scale   = interpolate(appear, [0, 1], [0.95, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0d0000',
      justifyContent: 'center', alignItems: 'center', padding: '0 160px',
    }}>
      <div style={{ opacity, transform: `scale(${scale})`, textAlign: 'center' }}>
        <div style={{
          fontSize: 24, color: DANGER_COLOR, fontFamily: OSWALD,
          letterSpacing: 6, textTransform: 'uppercase', marginBottom: 28,
        }}>
          Sound familiar?
        </div>
        <p style={{
          fontSize: 72, fontWeight: 900, color: 'white',
          fontFamily: OSWALD, lineHeight: 1.2, margin: 0,
        }}>
          {PAIN_TEXT}
        </p>
      </div>
    </AbsoluteFill>
  );
};

// === PHASE 2: AGITATE (15–35s) ===
const AgitateScene: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0d0505',
      flexDirection: 'column', justifyContent: 'center',
      padding: '0 120px', gap: 32,
    }}>
      <div style={{
        color: DANGER_COLOR, fontSize: 20, fontFamily: OSWALD, letterSpacing: 6,
        opacity: interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        The numbers don't lie:
      </div>

      {AGITATE_STATS.map((stat, i) => {
        const delay   = i * 20;
        const localF  = frame - delay;
        const appear  = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
        const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
        const x       = localF > 0 ? interpolate(appear, [0, 1], [-40, 0]) : -40;

        return (
          <div key={i} style={{
            display: 'flex', alignItems: 'flex-start', gap: 20,
            opacity, transform: `translateX(${x}px)`,
          }}>
            <div style={{
              width: 10, height: 10, minWidth: 10,
              borderRadius: '50%', backgroundColor: DANGER_COLOR,
              marginTop: 14,
            }} />
            <p style={{
              fontSize: 40, color: 'rgba(255,255,255,0.9)',
              fontFamily: INTER, lineHeight: 1.45, margin: 0,
            }}>
              {stat}
            </p>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// === PHASE 3: SOLUTION (35–65s) ===
const SolutionScene: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor: '#020d05',
      padding: '60px 100px', flexDirection: 'column', gap: 32,
    }}>
      {/* Product reveal */}
      <div style={{
        textAlign: 'center', marginBottom: 20,
        opacity: interpolate(frame, [0, 18], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        <div style={{ fontSize: 18, color: SUCCESS_COLOR, fontFamily: OSWALD, letterSpacing: 6 }}>
          INTRODUCING
        </div>
        <h2 style={{
          fontSize: 80, fontWeight: 900, color: 'white',
          fontFamily: OSWALD, margin: '8px 0 4px',
          textShadow: `0 0 40px ${ACCENT_COLOR}60`,
        }}>
          {PRODUCT_NAME}
        </h2>
        <div style={{ fontSize: 28, color: ACCENT_COLOR, fontFamily: INTER }}>{PRODUCT_TAGLINE}</div>
      </div>

      {/* Features */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {FEATURES.map((f, i) => {
          const delay   = 18 + i * 10;
          const localF  = frame - delay;
          const appear  = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
          const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
          const y       = localF > 0 ? interpolate(appear, [0, 1], [20, 0]) : 20;

          return (
            <div key={i} style={{
              backgroundColor: 'rgba(99,102,241,0.08)',
              border: '1px solid rgba(99,102,241,0.2)',
              borderRadius: 14, padding: 24,
              opacity, transform: `translateY(${y}px)`,
            }}>
              <div style={{ fontSize: 36, marginBottom: 8 }}>{f.icon}</div>
              <div style={{ fontSize: 26, fontWeight: 700, color: 'white', fontFamily: INTER, marginBottom: 6 }}>
                {f.title}
              </div>
              <div style={{ fontSize: 20, color: '#64748b', fontFamily: INTER, lineHeight: 1.45 }}>
                {f.desc}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// === PHASE 3b: TESTIMONIALS (65–75s) ===
const TestimonialsScene: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor: '#080810',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 32, padding: '0 120px',
    }}>
      <div style={{
        color: '#94a3b8', fontSize: 20, fontFamily: OSWALD, letterSpacing: 6,
        opacity: interpolate(frame, [0, 12], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        Real Results From Real Users
      </div>

      {TESTIMONIALS.map((t, i) => {
        const delay   = i * 20;
        const localF  = frame - delay;
        const appear  = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
        const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
        const scale   = localF > 0 ? interpolate(appear, [0, 1], [0.92, 1]) : 0.92;

        return (
          <div key={i} style={{
            backgroundColor: '#1e1b4b',
            border: `1px solid ${ACCENT_COLOR}40`,
            borderRadius: 20, padding: '32px 48px',
            width: '100%', maxWidth: 1200,
            opacity, transform: `scale(${scale})`,
          }}>
            <div style={{ fontSize: 48, color: SUCCESS_COLOR, fontWeight: 900, fontFamily: OSWALD, marginBottom: 12 }}>
              "{t.result}"
            </div>
            <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
              <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: SUCCESS_COLOR }} />
              <div style={{ color: 'white', fontSize: 24, fontFamily: INTER, fontWeight: 600 }}>{t.name}</div>
              <div style={{ color: '#64748b', fontSize: 20, fontFamily: INTER }}>{t.role}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// === PHASE 4: MOMENTUM / CTA (75–90s) ===
const CTAScene: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60 } });
  const scale   = interpolate(appear, [0, 1], [0.9, 1]);
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);

  // Urgency pulse on CTA button
  const btnPulse = 1 + Math.sin(frame * 0.15) * 0.03;

  return (
    <AbsoluteFill style={{
      background: `linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)`,
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 32,
      opacity, transform: `scale(${scale})`,
    }}>
      {/* Price */}
      <div style={{ textAlign: 'center' }}>
        <div style={{
          fontSize: 28, color: '#ef4444', fontFamily: INTER,
          textDecoration: 'line-through', opacity: 0.7,
        }}>
          Normal price: {OFFER.originalPrice}
        </div>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, justifyContent: 'center', marginTop: 8 }}>
          <span style={{ fontSize: 100, fontWeight: 900, color: 'white', fontFamily: OSWALD, lineHeight: 1 }}>
            {OFFER.currentPrice}
          </span>
          <span style={{ fontSize: 32, color: '#94a3b8', fontFamily: INTER }}>{OFFER.period}</span>
        </div>
      </div>

      {/* CTA button */}
      <div style={{
        backgroundColor: SUCCESS_COLOR,
        color: 'white', fontSize: 36, fontWeight: 900,
        padding: '24px 60px', borderRadius: 16,
        fontFamily: OSWALD, letterSpacing: 2,
        transform: `scale(${btnPulse})`,
        boxShadow: `0 0 60px ${SUCCESS_COLOR}60`,
      }}>
        {OFFER.cta}
      </div>

      {/* Guarantee + Scarcity */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10, alignItems: 'center' }}>
        <div style={{
          color: '#94a3b8', fontSize: 22, fontFamily: INTER,
          display: 'flex', alignItems: 'center', gap: 8,
        }}>
          <span>🛡️</span> {OFFER.guarantee}
        </div>
        <div style={{
          color: '#ef4444', fontSize: 22, fontFamily: INTER,
          display: 'flex', alignItems: 'center', gap: 8,
          fontWeight: 700,
        }}>
          <span>⏰</span> {OFFER.scarcity}
        </div>
        <div style={{ color: '#6366f1', fontSize: 24, fontFamily: INTER }}>
          {OFFER.url}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const VideoSalesLetter: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#050505' }}>
    <VideoProgress />
    {/* <Audio src={staticFile('audio/narration.mp3')} /> */}

    <Sequence from={s(0)}  durationInFrames={s(15)}><PainScene /></Sequence>
    <Sequence from={s(15)} durationInFrames={s(20)}><AgitateScene /></Sequence>
    <Sequence from={s(35)} durationInFrames={s(30)}><SolutionScene /></Sequence>
    <Sequence from={s(65)} durationInFrames={s(10)}><TestimonialsScene /></Sequence>
    <Sequence from={s(75)} durationInFrames={s(15)}><CTAScene /></Sequence>
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  return (
    <Composition
      id="VideoSalesLetter"
      component={VideoSalesLetter}
      durationInFrames={s(90)}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
