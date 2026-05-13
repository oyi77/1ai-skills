# Remotion Charts & Data Visualization Rule

## Animated Bar Chart

```tsx
import { interpolate, spring, useCurrentFrame, useVideoConfig, AbsoluteFill } from 'remotion';

interface BarData {
  label: string;
  value: number;
  color: string;
}

const AnimatedBar: React.FC<{ bar: BarData; maxValue: number; index: number }> = ({
  bar, maxValue, index,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 5; // stagger per bar
  const progress = spring({
    frame: frame - delay,
    fps,
    config: { damping: 100, stiffness: 200 },
  });

  const barHeight = interpolate(progress, [0, 1], [0, (bar.value / maxValue) * 400]);
  const opacity = interpolate(frame - delay, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', opacity }}>
      <div style={{
        width: 60,
        height: barHeight,
        backgroundColor: bar.color,
        borderRadius: '4px 4px 0 0',
      }} />
      <div style={{ color: 'white', fontSize: 20, marginTop: 8 }}>{bar.label}</div>
      <div style={{ color: bar.color, fontSize: 18, fontWeight: 'bold' }}>
        {Math.round(interpolate(progress, [0, 1], [0, bar.value]))}
      </div>
    </div>
  );
};

export const BarChart: React.FC<{ data: BarData[] }> = ({ data }) => {
  const maxValue = Math.max(...data.map((d) => d.value));

  return (
    <AbsoluteFill style={{
      backgroundColor: '#1a1a2e',
      justifyContent: 'flex-end',
      alignItems: 'flex-end',
      padding: 80,
      gap: 20,
      flexDirection: 'row',
    }}>
      {data.map((bar, i) => (
        <AnimatedBar key={bar.label} bar={bar} maxValue={maxValue} index={i} />
      ))}
    </AbsoluteFill>
  );
};
```

## Animated Counter

```tsx
const AnimatedCounter: React.FC<{ target: number; prefix?: string; suffix?: string }> = ({
  target, prefix = '', suffix = '',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, durationInFrames: 60, config: { damping: 100 } });
  const value = Math.round(interpolate(progress, [0, 1], [0, target]));

  return (
    <div style={{ fontSize: 120, fontWeight: 'bold', color: 'white' }}>
      {prefix}{value.toLocaleString()}{suffix}
    </div>
  );
};

// Usage:
<AnimatedCounter target={1500000} prefix="Rp " suffix="+" />
<AnimatedCounter target={98} suffix="%" />
```

## Progress / Donut Circle

```tsx
const AnimatedCircle: React.FC<{ percentage: number }> = ({ percentage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, config: { damping: 100 } });
  const currentPct = interpolate(progress, [0, 1], [0, percentage]);

  const r = 80;
  const circumference = 2 * Math.PI * r;
  const strokeDashoffset = circumference * (1 - currentPct / 100);

  return (
    <svg width={200} height={200} viewBox="0 0 200 200">
      {/* Background circle */}
      <circle cx={100} cy={100} r={r} fill="none" stroke="#333" strokeWidth={12} />
      {/* Progress circle */}
      <circle
        cx={100} cy={100} r={r}
        fill="none" stroke="#4f46e5" strokeWidth={12}
        strokeDasharray={circumference}
        strokeDashoffset={strokeDashoffset}
        strokeLinecap="round"
        transform="rotate(-90 100 100)"
      />
      <text x={100} y={108} textAnchor="middle" fontSize={36} fill="white" fontWeight="bold">
        {Math.round(currentPct)}%
      </text>
    </svg>
  );
};
```

## Line Chart (SVG)

```tsx
const LineChart: React.FC<{ data: number[] }> = ({ data }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const W = 800, H = 400;
  const padding = 40;
  const maxVal = Math.max(...data);
  const minVal = Math.min(...data);

  // Reveal line progressively
  const revealProgress = interpolate(frame, [0, 60], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const pointsToShow = Math.ceil(revealProgress * data.length);

  const toX = (i: number) =>
    padding + (i / (data.length - 1)) * (W - padding * 2);
  const toY = (v: number) =>
    H - padding - ((v - minVal) / (maxVal - minVal)) * (H - padding * 2);

  const points = data
    .slice(0, pointsToShow)
    .map((v, i) => `${toX(i)},${toY(v)}`)
    .join(' ');

  return (
    <svg width={W} height={H}>
      <polyline
        points={points}
        fill="none"
        stroke="#4f46e5"
        strokeWidth={3}
        strokeLinejoin="round"
      />
      {data.slice(0, pointsToShow).map((v, i) => (
        <circle key={i} cx={toX(i)} cy={toY(v)} r={5} fill="#4f46e5" />
      ))}
    </svg>
  );
};
```

## Using Recharts with Remotion

Recharts works with Remotion but **disable all CSS animations** — drive everything via frame:

```tsx
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from 'recharts';

// Note: Recharts animations must be disabled (isAnimationActive={false})
// Animate using frame-based interpolation on the data values instead

const AnimatedBarChart: React.FC<{ data: DataPoint[] }> = ({ data }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({ frame, fps, config: { damping: 100 } });

  // Scale data values by progress
  const animatedData = data.map((d) => ({
    ...d,
    value: interpolate(progress, [0, 1], [0, d.value]),
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={animatedData}>
        <XAxis dataKey="name" stroke="white" />
        <YAxis stroke="white" />
        <Bar dataKey="value" fill="#4f46e5" isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
};
```

## Stat Card Grid

```tsx
const StatCard: React.FC<{ title: string; value: number; unit: string; delay: number }> = ({
  title, value, unit, delay,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame - delay, [0, 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const progress = spring({ frame: frame - delay, fps, config: { damping: 100 } });
  const displayValue = Math.round(interpolate(progress, [0, 1], [0, value]));

  return (
    <div style={{
      backgroundColor: '#1e293b',
      borderRadius: 16,
      padding: '32px 40px',
      opacity,
      textAlign: 'center',
    }}>
      <div style={{ color: '#94a3b8', fontSize: 20 }}>{title}</div>
      <div style={{ color: 'white', fontSize: 72, fontWeight: 'bold' }}>
        {displayValue.toLocaleString()}{unit}
      </div>
    </div>
  );
};
```
