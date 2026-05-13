// ============================================================
// NEWS / MOTION GRAPHICS EXPLAINER TEMPLATE
// Style: Bloomberg/Vox/Johnny Harris — kinetic, authoritative, data-driven
// Format: 16:9 1080p, 3 minutes
// Requires: @remotion/google-fonts @remotion/noise
// Customize: NEWS_TOPIC, SECTIONS, DATA_POINTS
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile, Easing,
} from 'remotion';
import { loadFont as loadOswald }   from '@remotion/google-fonts/Oswald';
import { loadFont as loadRoboto }   from '@remotion/google-fonts/RobotoCondensed';
import { loadFont as loadPlayfair } from '@remotion/google-fonts/PlayfairDisplay';

const { fontFamily: OSWALD }   = loadOswald();
const { fontFamily: ROBOTO }   = loadRoboto();
const { fontFamily: PLAYFAIR } = loadPlayfair();

// ── CUSTOMIZE ──────────────────────────────────────────────
const NEWS_TOPIC    = 'Why Indonesia\'s Economy Is Booming in 2025';
const ACCENT_COLOR  = '#FF4500';
const BG_DARK       = '#0d1117';
const BG_GRID_LINE  = 'rgba(255,255,255,0.04)';

const DATA_POINTS = [
  { label: 'GDP Growth', value: 5.1, suffix: '%', comparison: 'vs 3.2% global average' },
  { label: 'FDI Inflow', value: 28, suffix: 'B', prefix: '$', comparison: 'record high' },
  { label: 'Digital Economy', value: 130, suffix: 'B', prefix: '$', comparison: 'by 2026' },
];

const SECTIONS = [
  { id: 'hook',    type: 'question',     startSec: 0,   durationSec: 8,  text: 'Why is Indonesia\none of the world\'s fastest growing economies?' },
  { id: 'ticker',  type: 'ticker',       startSec: 8,   durationSec: 5,  text: 'BREAKING: Indonesia GDP growth hits 5.1% in Q3 2025' },
  { id: 'context', type: 'kinetic',      startSec: 13,  durationSec: 20, lines: [
    { text: 'In 2020,', size: 48, weight: 300, delay: 0 },
    { text: '270 million people', size: 96, weight: 900, color: ACCENT_COLOR, delay: 8 },
    { text: 'were waiting for a reason to grow.', size: 48, weight: 300, delay: 20 },
  ]},
  { id: 'stat-1',  type: 'bigstat',      startSec: 33,  durationSec: 8,  stat: DATA_POINTS[0] },
  { id: 'stat-2',  type: 'bigstat',      startSec: 41,  durationSec: 8,  stat: DATA_POINTS[1] },
  { id: 'stat-3',  type: 'bigstat',      startSec: 49,  durationSec: 8,  stat: DATA_POINTS[2] },
  { id: 'factors', type: 'list',         startSec: 57,  durationSec: 30, title: 'Three Driving Forces', items: [
    { number: '01', label: 'Digital Infrastructure', desc: '400M mobile users + fastest 5G rollout in SE Asia' },
    { number: '02', label: 'Manufacturing Shift',    desc: 'Global supply chains relocating from China' },
    { number: '03', label: 'Young Demographics',     desc: 'Median age 29 — largest productive workforce in ASEAN' },
  ]},
  { id: 'chart',   type: 'barchart',     startSec: 87,  durationSec: 20, title: 'GDP Growth vs Peers', bars: [
    { label: 'Indonesia', value: 5.1, color: ACCENT_COLOR },
    { label: 'Vietnam',   value: 4.8, color: '#00AAFF' },
    { label: 'India',     value: 4.5, color: '#FF9944' },
    { label: 'Brazil',    value: 2.3, color: '#00CC44' },
    { label: 'Global',    value: 3.2, color: '#666' },
  ]},
  { id: 'outlook', type: 'kinetic',      startSec: 107, durationSec: 20, lines: [
    { text: 'By 2030,', size: 48, weight: 300, delay: 0 },
    { text: 'Indonesia could become', size: 60, weight: 400, delay: 10 },
    { text: 'the world\'s 5th largest economy.', size: 80, weight: 900, color: ACCENT_COLOR, delay: 20 },
  ]},
  { id: 'cta',     type: 'endcard',      startSec: 127, durationSec: 8,  text: 'Subscribe for daily economic explainers.' },
];

const FPS = 30;
const s   = (sec: number) => Math.round(sec * FPS);
// ───────────────────────────────────────────────────────────

// Grid background
const NewsGrid: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: BG_DARK }}>
    <svg width="100%" height="100%" style={{ position: 'absolute' }}>
      {Array.from({ length: 13 }).map((_, i) => (
        <line key={`v${i}`} x1={i * 160} y1={0} x2={i * 160} y2={1080}
          stroke={BG_GRID_LINE} strokeWidth={1} />
      ))}
      {Array.from({ length: 8 }).map((_, i) => (
        <line key={`h${i}`} x1={0} y1={i * 135} x2={1920} y2={i * 135}
          stroke={BG_GRID_LINE} strokeWidth={1} />
      ))}
    </svg>
  </AbsoluteFill>
);

// Breaking news ticker
const NewsTicker: React.FC<{ text: string }> = ({ text }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = spring({ frame, fps, config: { damping: 80, stiffness: 100 } });
  const x       = interpolate(slideIn, [0, 1], [-1920, 0]);

  return (
    <div style={{
      position: 'absolute', bottom: 60, left: 0, right: 0,
      transform: `translateX(${x}px)`,
      display: 'flex', alignItems: 'stretch',
    }}>
      <div style={{
        backgroundColor: ACCENT_COLOR, color: 'white',
        fontSize: 24, fontWeight: 900, fontFamily: OSWALD,
        padding: '12px 24px', letterSpacing: 3, display: 'flex', alignItems: 'center',
        animation: 'none',
      }}>
        ● BREAKING
      </div>
      <div style={{
        backgroundColor: 'rgba(10,10,20,0.96)', color: 'white',
        fontSize: 26, fontWeight: 500, fontFamily: ROBOTO,
        padding: '12px 28px', flex: 1, display: 'flex', alignItems: 'center',
        borderTop: `3px solid ${ACCENT_COLOR}`,
      }}>
        {text}
      </div>
    </div>
  );
};

// Hook / question card
const QuestionCard: React.FC<{ text: string }> = ({ text }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60, stiffness: 80 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const y       = interpolate(appear, [0, 1], [20, 0]);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'flex-start', padding: '0 120px' }}>
      <NewsGrid />
      <div style={{ opacity, transform: `translateY(${y}px)`, zIndex: 10 }}>
        <div style={{
          color: ACCENT_COLOR, fontSize: 20, fontFamily: OSWALD,
          letterSpacing: 6, textTransform: 'uppercase', marginBottom: 24,
        }}>
          Today's Question
        </div>
        <h1 style={{
          fontSize: 80, fontWeight: 900, color: 'white',
          fontFamily: OSWALD, margin: 0, lineHeight: 1.15,
          maxWidth: 1400, whiteSpace: 'pre-line',
        }}>
          {text}
        </h1>
      </div>
    </AbsoluteFill>
  );
};

// Kinetic typography
type KineticLine = { text: string; size?: number; weight?: number; color?: string; delay?: number };

const KineticCard: React.FC<{ lines: KineticLine[] }> = ({ lines }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'flex-start', padding: '0 120px', flexDirection: 'column', gap: 12 }}>
      <NewsGrid />
      {lines.map((line, i) => {
        const delay = line.delay ?? i * 12;
        const localF = frame - delay;
        const appear = spring({ frame: Math.max(0, localF), fps, config: { damping: 60, stiffness: 120 } });
        const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
        const x       = localF > 0 ? interpolate(appear, [0, 1], [-60, 0]) : -60;

        return (
          <div key={i} style={{
            fontSize: line.size ?? 72, fontWeight: line.weight ?? 700,
            color: line.color ?? 'white', fontFamily: OSWALD,
            lineHeight: 1.15, opacity, transform: `translateX(${x}px)`, zIndex: 10,
          }}>
            {line.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Big stat
const BigStat: React.FC<{ stat: typeof DATA_POINTS[0] }> = ({ stat }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 80, stiffness: 100 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);
  const count  = interpolate(appear, [0, 1], [0, stat.value]);
  const displayVal = stat.value % 1 === 0 ? Math.round(count) : count.toFixed(1);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 16, opacity }}>
      <NewsGrid />
      <div style={{
        fontSize: 200, fontWeight: 900, fontFamily: OSWALD,
        color: ACCENT_COLOR, lineHeight: 1,
        fontVariantNumeric: 'tabular-nums', zIndex: 10,
      }}>
        {stat.prefix ?? ''}{displayVal}{stat.suffix}
      </div>
      <div style={{
        fontSize: 44, fontFamily: OSWALD, fontWeight: 300,
        color: 'white', letterSpacing: 6, textTransform: 'uppercase',
        textAlign: 'center', zIndex: 10,
      }}>
        {stat.label}
      </div>
      <div style={{ color: '#555', fontSize: 24, fontFamily: ROBOTO, zIndex: 10 }}>
        {stat.comparison}
      </div>
      <div style={{
        height: 3, width: interpolate(frame, [10, 25], [0, 200], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        backgroundColor: ACCENT_COLOR, borderRadius: 2, zIndex: 10,
      }} />
    </AbsoluteFill>
  );
};

// Factor list
type FactorItem = { number: string; label: string; desc: string };
const FactorList: React.FC<{ title: string; items: FactorItem[] }> = ({ title, items }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ padding: '80px 120px', flexDirection: 'column', gap: 32 }}>
      <NewsGrid />
      <div style={{
        color: ACCENT_COLOR, fontSize: 22, fontFamily: OSWALD,
        letterSpacing: 6, textTransform: 'uppercase', zIndex: 10,
        opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        {title}
      </div>
      {items.map((item, i) => {
        const delay  = i * 15;
        const localF = frame - delay;
        const appear = spring({ frame: Math.max(0, localF), fps, config: { damping: 70 } });
        const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
        const x       = localF > 0 ? interpolate(appear, [0, 1], [-50, 0]) : -50;

        return (
          <div key={i} style={{
            display: 'flex', gap: 32, alignItems: 'flex-start',
            opacity, transform: `translateX(${x}px)`, zIndex: 10,
            borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: 24,
          }}>
            <div style={{
              fontSize: 60, fontWeight: 900, color: ACCENT_COLOR,
              fontFamily: OSWALD, lineHeight: 1, minWidth: 80,
            }}>
              {item.number}
            </div>
            <div>
              <div style={{ fontSize: 36, fontWeight: 700, color: 'white', fontFamily: OSWALD, marginBottom: 8 }}>
                {item.label}
              </div>
              <div style={{ fontSize: 24, color: '#64748b', fontFamily: ROBOTO, lineHeight: 1.5 }}>
                {item.desc}
              </div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Animated bar chart
type BarItem = { label: string; value: number; color: string };
const BarChart: React.FC<{ title: string; bars: BarItem[] }> = ({ title, bars }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const maxVal  = Math.max(...bars.map(b => b.value));

  return (
    <AbsoluteFill style={{ padding: '80px 120px', flexDirection: 'column', gap: 24 }}>
      <NewsGrid />
      <div style={{
        color: 'white', fontSize: 40, fontWeight: 700, fontFamily: OSWALD,
        zIndex: 10,
        opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        {title}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, zIndex: 10 }}>
        {bars.map((bar, i) => {
          const delay  = i * 8;
          const localF = frame - delay;
          const appear = spring({ frame: Math.max(0, localF), fps, config: { damping: 80 } });
          const pct    = (bar.value / maxVal) * 100;
          const width  = localF > 0 ? interpolate(appear, [0, 1], [0, pct]) : 0;
          const opacity = localF > 0 ? interpolate(appear, [0, 0.4], [0, 1]) : 0;
          const count  = localF > 0 ? interpolate(appear, [0, 1], [0, bar.value]) : 0;

          return (
            <div key={i} style={{ opacity }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                <span style={{ color: 'white', fontSize: 22, fontFamily: OSWALD }}>{bar.label}</span>
                <span style={{ color: bar.color, fontSize: 22, fontWeight: 900, fontFamily: OSWALD }}>
                  {count.toFixed(1)}%
                </span>
              </div>
              <div style={{ height: 12, backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: 6 }}>
                <div style={{
                  height: '100%', width: `${width}%`,
                  backgroundColor: bar.color, borderRadius: 6,
                  boxShadow: `0 0 12px ${bar.color}60`,
                }} />
              </div>
            </div>
          );
        })}
      </div>
      <div style={{ color: '#444', fontSize: 16, fontFamily: ROBOTO, zIndex: 10 }}>
        Source: World Bank, IMF (2025 Projections)
      </div>
    </AbsoluteFill>
  );
};

// End card
const EndCard: React.FC<{ text: string }> = ({ text }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: BG_DARK, justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 20, opacity,
    }}>
      <div style={{ fontSize: 64, fontWeight: 900, fontFamily: OSWALD, color: 'white' }}>
        Subscribe
      </div>
      <div style={{ fontSize: 28, fontFamily: ROBOTO, color: '#666' }}>{text}</div>
      <div style={{
        height: 3, backgroundColor: ACCENT_COLOR,
        width: interpolate(frame, [8, 24], [0, 200], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        borderRadius: 2,
      }} />
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const NewsExplainer: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: BG_DARK }}>
    {/* <Audio src={staticFile('audio/narration.mp3')} /> */}

    {SECTIONS.map((section) => (
      <Sequence key={section.id} from={s(section.startSec)} durationInFrames={s(section.durationSec)}>
        {section.type === 'question'  && <QuestionCard text={section.text!} />}
        {section.type === 'ticker'    && <><NewsGrid /><div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}><QuestionCard text={NEWS_TOPIC} /></div><NewsTicker text={section.text!} /></>}
        {section.type === 'kinetic'   && <KineticCard lines={(section as any).lines} />}
        {section.type === 'bigstat'   && <BigStat stat={(section as any).stat} />}
        {section.type === 'list'      && <FactorList title={(section as any).title} items={(section as any).items} />}
        {section.type === 'barchart'  && <BarChart title={(section as any).title} bars={(section as any).bars} />}
        {section.type === 'endcard'   && <EndCard text={section.text!} />}
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const total = s(Math.max(...SECTIONS.map(sc => sc.startSec + sc.durationSec)));
  return (
    <Composition id="NewsExplainer" component={NewsExplainer} durationInFrames={total} fps={FPS} width={1920} height={1080} />
  );
};
