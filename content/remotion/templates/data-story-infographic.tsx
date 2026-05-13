// ============================================================
// DATA STORY / ANIMATED INFOGRAPHIC TEMPLATE
// Style: Bloomberg / Vox — authoritative, clean, bold data
// Format: 16:9 1080p, ~90 seconds
// Customize: TITLE, STATS, BAR_DATA, LINE_DATA, PALETTE
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence,
  useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const STORY_TITLE    = 'The Indonesian Digital Economy';
const STORY_SUBTITLE = 'From $40B to $130B in just 4 years.';
const SOURCE         = 'Google, Temasek, Bain — e-Conomy SEA 2025';
const ACCENT         = '#E5B000';   // gold
const BG             = '#0d1117';

const STATS = [
  { value: 212,  suffix: 'M',  label: 'Internet Users' },
  { value: 77,   suffix: '%',  label: 'Social Media Penetration' },
  { value: 130,  suffix: 'B',  label: 'GMV (USD)' },
];

const BAR_DATA = [
  { label: '2020', value: 44,  color: '#3b82f6' },
  { label: '2021', value: 61,  color: '#6366f1' },
  { label: '2022', value: 77,  color: '#8b5cf6' },
  { label: '2023', value: 90,  color: '#a78bfa' },
  { label: '2024', value: 110, color: '#c4b5fd' },
  { label: '2025', value: 130, color: ACCENT     },
];

const LINE_POINTS = [
  { year: '2019', value: 28  },
  { year: '2020', value: 44  },
  { year: '2021', value: 61  },
  { year: '2022', value: 77  },
  { year: '2023', value: 90  },
  { year: '2024', value: 110 },
  { year: '2025', value: 130 },
];

const CALLOUT_TEXT = 'E-commerce drives 72% of all digital GMV — dominated by Tokopedia, Shopee, and Lazada.';

const FPS      = 30;
const DURATION = FPS * 90;

// Segment timing
const SEG = {
  TITLE:   { from: 0,        dur: FPS * 10 },
  STATS:   { from: FPS * 10, dur: FPS * 18 },
  BARS:    { from: FPS * 28, dur: FPS * 22 },
  LINE:    { from: FPS * 50, dur: FPS * 20 },
  CALLOUT: { from: FPS * 70, dur: FPS * 20 },
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="DataStory"
    component={DataStory}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const DataStory: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: BG }}>

    {/* Title card */}
    <Sequence from={SEG.TITLE.from} durationInFrames={SEG.TITLE.dur}>
      <TitleCard />
    </Sequence>

    {/* Big stats */}
    <Sequence from={SEG.STATS.from} durationInFrames={SEG.STATS.dur}>
      <StatsScene />
    </Sequence>

    {/* Bar chart */}
    <Sequence from={SEG.BARS.from} durationInFrames={SEG.BARS.dur}>
      <BarChartScene />
    </Sequence>

    {/* Line chart */}
    <Sequence from={SEG.LINE.from} durationInFrames={SEG.LINE.dur}>
      <LineChartScene />
    </Sequence>

    {/* Callout */}
    <Sequence from={SEG.CALLOUT.from} durationInFrames={SEG.CALLOUT.dur}>
      <CalloutScene />
    </Sequence>

    {/* Source watermark */}
    <SourceTag />

  </AbsoluteFill>
);

// ── TITLE CARD ───────────────────────────────────────────────
const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleAppear = spring({ frame, fps, config: { damping: 60 } });
  const subAppear   = spring({ frame: frame - fps * 0.8, fps, config: { damping: 60 } });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'flex-start', padding: '0 120px' }}>
      {/* Accent line */}
      <div style={{
        position: 'absolute', left: 0, top: 0, bottom: 0,
        width: 6, backgroundColor: ACCENT,
        transform: `scaleY(${interpolate(frame, [0, fps * 0.5], [0, 1], { extrapolateRight: 'clamp' })})`,
        transformOrigin: 'top',
      }} />

      <div>
        <h1 style={{
          fontSize: 96, fontWeight: 900, color: 'white',
          margin: '0 0 20px', lineHeight: 1.1,
          opacity: interpolate(titleAppear, [0, 0.5], [0, 1]),
          transform: `translateY(${interpolate(titleAppear, [0, 1], [20, 0])}px)`,
        }}>
          {STORY_TITLE}
        </h1>
        <p style={{
          fontSize: 48, color: '#94a3b8', margin: 0,
          opacity: interpolate(subAppear, [0, 0.5], [0, 1]),
          transform: `translateY(${interpolate(subAppear, [0, 1], [16, 0])}px)`,
        }}>
          {STORY_SUBTITLE}
        </p>
      </div>
    </AbsoluteFill>
  );
};

// ── STATS SCENE ──────────────────────────────────────────────
const StatsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      justifyContent: 'center', alignItems: 'center', gap: 80,
      flexDirection: 'row', padding: '0 80px',
    }}>
      {STATS.map((stat, i) => {
        const delay  = i * 12;
        const appear = spring({ frame: frame - delay, fps, config: { damping: 80 } });
        const countP = spring({ frame: frame - delay, fps, config: { damping: 100 } });
        const count  = Math.round(interpolate(countP, [0, 1], [0, stat.value]));

        return (
          <div key={i} style={{
            textAlign: 'center', flex: 1,
            opacity: interpolate(appear, [0, 0.5], [0, 1]),
            transform: `translateY(${interpolate(appear, [0, 1], [30, 0])}px)`,
          }}>
            <div style={{
              fontSize: 128, fontWeight: 900, lineHeight: 1,
              color: i === STATS.length - 1 ? ACCENT : 'white',
            }}>
              {count}{stat.suffix}
            </div>
            <div style={{
              fontSize: 28, color: '#64748b', marginTop: 12,
              textTransform: 'uppercase', letterSpacing: 4,
            }}>
              {stat.label}
            </div>
            <div style={{
              width: interpolate(appear, [0, 1], [0, 60]),
              height: 3, backgroundColor: ACCENT, borderRadius: 2,
              margin: '16px auto 0',
            }} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ── BAR CHART SCENE ──────────────────────────────────────────
const BarChartScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const maxVal = Math.max(...BAR_DATA.map(d => d.value));
  const MAX_H  = 480;

  const titleAppear = spring({ frame, fps, config: { damping: 70 } });

  return (
    <AbsoluteFill style={{ padding: '60px 100px' }}>

      {/* Title */}
      <div style={{
        fontSize: 40, fontWeight: 700, color: 'white',
        marginBottom: 60, letterSpacing: 1,
        opacity: interpolate(titleAppear, [0, 0.5], [0, 1]),
      }}>
        Indonesia Digital GMV (USD Billion)
      </div>

      {/* Bars */}
      <div style={{
        display: 'flex', alignItems: 'flex-end',
        gap: 20, height: MAX_H,
      }}>
        {BAR_DATA.map((bar, i) => {
          const delay  = i * 6;
          const appear = spring({ frame: frame - delay, fps, config: { damping: 80 } });
          const barH   = interpolate(appear, [0, 1], [0, (bar.value / maxVal) * MAX_H]);
          const valueOpacity = interpolate(appear, [0.5, 1], [0, 1]);

          return (
            <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
              {/* Value label */}
              <div style={{ fontSize: 28, fontWeight: 700, color: bar.color, opacity: valueOpacity }}>
                ${bar.value}B
              </div>
              {/* Bar */}
              <div style={{
                width: '100%', height: barH,
                backgroundColor: bar.color,
                borderRadius: '6px 6px 0 0',
                boxShadow: `0 0 20px ${bar.color}44`,
              }} />
              {/* Label */}
              <div style={{ fontSize: 24, color: '#64748b', marginTop: 4 }}>{bar.label}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── LINE CHART SCENE ─────────────────────────────────────────
const LineChartScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const W = 1600, H = 500;
  const PAD = { l: 80, r: 60, t: 40, b: 60 };
  const chartW = W - PAD.l - PAD.r;
  const chartH = H - PAD.t - PAD.b;

  const maxVal = Math.max(...LINE_POINTS.map(p => p.value));
  const minVal = Math.min(...LINE_POINTS.map(p => p.value));

  const toX = (i: number) => PAD.l + (i / (LINE_POINTS.length - 1)) * chartW;
  const toY = (v: number) => H - PAD.b - ((v - minVal) / (maxVal - minVal)) * chartH;

  const revealProgress = interpolate(frame, [0, fps * 1.8], [0, 1], {
    extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
  });
  const pointsToShow   = Math.ceil(revealProgress * LINE_POINTS.length);
  const partialFraction = (revealProgress * LINE_POINTS.length) % 1;

  // Build path
  const pts = LINE_POINTS.slice(0, pointsToShow);
  if (pointsToShow < LINE_POINTS.length && partialFraction > 0) {
    const a = LINE_POINTS[pointsToShow - 1];
    const b = LINE_POINTS[pointsToShow];
    if (b) {
      pts.push({
        year: '',
        value: a.value + (b.value - a.value) * partialFraction,
      });
    }
  }

  const pathD = pts.map((p, i) => {
    const x = PAD.l + (i / (LINE_POINTS.length - 1)) * chartW;
    const y = toY(p.value);
    return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
  }).join(' ');

  const titleAppear = spring({ frame, fps, config: { damping: 70 } });

  return (
    <AbsoluteFill style={{ padding: '60px 160px', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 24 }}>
      <div style={{
        fontSize: 40, fontWeight: 700, color: 'white', alignSelf: 'flex-start',
        opacity: interpolate(titleAppear, [0, 0.5], [0, 1]),
      }}>
        Growth Trajectory — 2019 to 2025
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%' }}>
        {/* Grid lines */}
        {[0.25, 0.5, 0.75, 1].map((pct) => {
          const y = H - PAD.b - pct * chartH;
          const val = Math.round(minVal + pct * (maxVal - minVal));
          return (
            <g key={pct}>
              <line x1={PAD.l} y1={y} x2={W - PAD.r} y2={y} stroke="rgba(255,255,255,0.08)" strokeWidth={1} />
              <text x={PAD.l - 10} y={y + 5} fill="#64748b" fontSize={18} textAnchor="end">${val}B</text>
            </g>
          );
        })}

        {/* Area fill */}
        {pts.length > 1 && (
          <path
            d={`${pathD} L ${toX(pts.length - 1)} ${H - PAD.b} L ${PAD.l} ${H - PAD.b} Z`}
            fill={`url(#lineGrad)`}
            opacity={0.25}
          />
        )}

        {/* Gradient def */}
        <defs>
          <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={ACCENT} />
            <stop offset="100%" stopColor={ACCENT} stopOpacity={0} />
          </linearGradient>
        </defs>

        {/* Line */}
        <path d={pathD} fill="none" stroke={ACCENT} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" />

        {/* Year labels */}
        {LINE_POINTS.map((p, i) => (
          <text key={i} x={toX(i)} y={H - PAD.b + 30} textAnchor="middle" fill="#64748b" fontSize={20}>
            {p.year}
          </text>
        ))}

        {/* Dots on revealed points */}
        {LINE_POINTS.slice(0, Math.floor(revealProgress * LINE_POINTS.length)).map((p, i) => (
          <circle key={i} cx={toX(i)} cy={toY(p.value)} r={6} fill={ACCENT}
            filter={`drop-shadow(0 0 6px ${ACCENT})`} />
        ))}
      </svg>
    </AbsoluteFill>
  );
};

// ── CALLOUT SCENE ────────────────────────────────────────────
const CalloutScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const scale   = interpolate(appear, [0, 1], [0.94, 1]);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: '0 160px' }}>
      <div style={{
        opacity, transform: `scale(${scale})`,
        textAlign: 'center',
      }}>
        {/* Large quote mark */}
        <div style={{ fontSize: 160, color: ACCENT, opacity: 0.2, lineHeight: 0.6, marginBottom: 20 }}>
          "
        </div>
        <p style={{
          fontSize: 56, fontWeight: 700, color: 'white',
          lineHeight: 1.4, margin: 0,
        }}>
          {CALLOUT_TEXT}
        </p>
        <div style={{
          width: 80, height: 4, backgroundColor: ACCENT, borderRadius: 2,
          margin: '40px auto 0',
        }} />
      </div>
    </AbsoluteFill>
  );
};

// ── SOURCE TAG ───────────────────────────────────────────────
const SourceTag: React.FC = () => (
  <div style={{
    position: 'absolute', bottom: 24, right: 40,
    fontSize: 18, color: 'rgba(255,255,255,0.3)', fontStyle: 'italic',
  }}>
    Source: {SOURCE}
  </div>
);
