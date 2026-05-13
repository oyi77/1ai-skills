# News / Motion Graphics / Data Explainer Video in Remotion

## The Format

News-style motion graphics combine journalistic authority with visual storytelling. Think Bloomberg, Vox, CNBC explainers, Al Jazeera segments. High-information density, clean kinetic typography, animated charts, maps, and data.

This format builds credibility instantly — it signals research, authority, and professionalism.

---

## Breaking News Ticker / Lower Third

```tsx
export const NewsTicker: React.FC<{
  headline: string;
  subline?: string;
  category?: string;
  style?: 'breaking' | 'live' | 'update' | 'exclusive';
  accentColor?: string;
}> = ({
  headline, subline, category = 'NEWS',
  style = 'breaking', accentColor = '#CC0000',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = interpolate(
    spring({ frame, fps, config: { damping: 80, stiffness: 100 } }),
    [0, 1], [-1920, 0]
  );

  const STYLE_LABELS = {
    breaking:  { label: 'BREAKING', bg: '#CC0000', blink: true },
    live:      { label: '● LIVE',   bg: '#CC0000', blink: true },
    update:    { label: 'UPDATE',   bg: '#FF6600', blink: false },
    exclusive: { label: 'EXCLUSIVE',bg: '#6600CC', blink: false },
  };
  const s = STYLE_LABELS[style];

  // Blink animation for LIVE / BREAKING
  const blinkOpacity = s.blink
    ? Math.round(frame / Math.round(fps * 0.6)) % 2 === 0 ? 1 : 0.4
    : 1;

  return (
    <div style={{
      position: 'absolute', bottom: 60, left: 0, right: 0,
      transform: `translateX(${slideIn}px)`,
    }}>
      <div style={{ display: 'flex', alignItems: 'stretch' }}>
        {/* Category badge */}
        <div style={{
          backgroundColor: s.bg,
          color: 'white',
          fontSize: 26,
          fontWeight: 900,
          padding: '10px 20px',
          letterSpacing: 3,
          display: 'flex', alignItems: 'center',
          opacity: blinkOpacity,
        }}>
          {s.label}
        </div>

        {/* Headline */}
        <div style={{
          backgroundColor: 'rgba(10,10,10,0.95)',
          color: 'white',
          fontSize: 28,
          fontWeight: 600,
          padding: '10px 24px',
          flex: 1,
          display: 'flex', alignItems: 'center',
          borderTop: `3px solid ${accentColor}`,
        }}>
          {headline}
        </div>
      </div>
      {subline && (
        <div style={{
          backgroundColor: 'rgba(20,20,20,0.9)',
          color: '#ccc', fontSize: 20, padding: '6px 24px 6px',
          marginLeft: 120,
          borderBottom: `1px solid ${accentColor}40`,
        }}>
          {subline}
        </div>
      )}
    </div>
  );
};
```

---

## Animated World Map / Data Map

```tsx
export const DataMap: React.FC<{
  title?: string;
  highlights?: Array<{
    country: string;
    x: number; y: number;  // position as % of 1920×1080
    value: string;
    color?: string;
  }>;
  accentColor?: string;
}> = ({ title, highlights = [], accentColor = '#CC0000' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const mapOpacity = interpolate(frame, [0, fps * 0.8], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0d1117' }}>
      {/* Map background image */}
      <AbsoluteFill style={{ opacity: mapOpacity }}>
        <Img
          src={staticFile('images/world-map.svg')}
          style={{ width: '100%', height: '100%', objectFit: 'contain', opacity: 0.25, filter: 'invert(1)' }}
        />
      </AbsoluteFill>

      {/* Grid lines */}
      <AbsoluteFill style={{ opacity: 0.08 }}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080">
          {Array.from({ length: 12 }).map((_, i) => (
            <line key={`v${i}`} x1={i * 160} y1={0} x2={i * 160} y2={1080}
              stroke="white" strokeWidth={1} />
          ))}
          {Array.from({ length: 7 }).map((_, i) => (
            <line key={`h${i}`} x1={0} y1={i * 154} x2={1920} y2={i * 154}
              stroke="white" strokeWidth={1} />
          ))}
        </svg>
      </AbsoluteFill>

      {/* Highlight points */}
      {highlights.map((h, i) => {
        const delay = fps * 0.5 + i * 8;
        const appear = spring({ frame: frame - delay, fps, config: { damping: 10, stiffness: 300 } });
        const scale = interpolate(appear, [0, 1], [0, 1]);

        return (
          <div key={h.country} style={{
            position: 'absolute',
            left: `${h.x}%`, top: `${h.y}%`,
            transform: `translate(-50%, -50%) scale(${scale})`,
          }}>
            {/* Pulse ring */}
            <div style={{
              position: 'absolute',
              width: 40, height: 40,
              borderRadius: '50%',
              border: `2px solid ${h.color ?? accentColor}`,
              top: '50%', left: '50%',
              transform: `translate(-50%, -50%) scale(${interpolate(
                frame - delay, [0, fps * 2], [1, 2.5], { extrapolateRight: 'clamp' }
              )})`,
              opacity: interpolate(frame - delay, [0, fps * 2], [0.8, 0], { extrapolateRight: 'clamp' }),
            }} />
            {/* Dot */}
            <div style={{
              width: 14, height: 14,
              borderRadius: '50%',
              backgroundColor: h.color ?? accentColor,
              position: 'absolute', top: '50%', left: '50%',
              transform: 'translate(-50%, -50%)',
            }} />
            {/* Label */}
            <div style={{
              position: 'absolute', top: 20, left: 16, whiteSpace: 'nowrap',
            }}>
              <div style={{ color: 'white', fontSize: 18, fontWeight: 700 }}>{h.country}</div>
              <div style={{ color: h.color ?? accentColor, fontSize: 22, fontWeight: 900 }}>{h.value}</div>
            </div>
          </div>
        );
      })}

      {/* Title */}
      {title && (
        <div style={{
          position: 'absolute', top: 40, left: 60,
          backgroundColor: 'rgba(0,0,0,0.85)',
          color: 'white', fontSize: 32, fontWeight: 700,
          padding: '10px 24px', borderRadius: 8,
          borderLeft: `4px solid ${accentColor}`,
          opacity: mapOpacity,
        }}>
          {title}
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Kinetic Typography (Vox / Johnny Harris Style)

```tsx
export const KineticTitle: React.FC<{
  lines: Array<{
    text: string;
    size?: number;
    weight?: number;
    color?: string;
    delay?: number;
    animation?: 'slide-left' | 'slide-up' | 'scale' | 'fade';
  }>;
  backgroundColor?: string;
}> = ({ lines, backgroundColor = '#0d1117' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor,
      justifyContent: 'center',
      alignItems: 'flex-start',
      flexDirection: 'column',
      padding: '0 120px',
      gap: 8,
    }}>
      {lines.map((line, i) => {
        const delay = (line.delay ?? i * 8);
        const localF = frame - delay;
        const appear = spring({ frame: Math.max(0, localF), fps, config: { damping: 60, stiffness: 120 } });

        const animStyles: Record<string, React.CSSProperties> = {
          'slide-left': {
            transform: `translateX(${interpolate(appear, [0, 1], [-80, 0])}px)`,
            opacity: interpolate(appear, [0, 0.4], [0, 1]),
          },
          'slide-up': {
            transform: `translateY(${interpolate(appear, [0, 1], [40, 0])}px)`,
            opacity: interpolate(appear, [0, 0.4], [0, 1]),
          },
          'scale': {
            transform: `scale(${interpolate(appear, [0, 1], [0.7, 1])})`,
            opacity: interpolate(appear, [0, 0.3], [0, 1]),
          },
          'fade': { opacity: interpolate(localF, [0, 20], [0, 1], { extrapolateRight: 'clamp' }) },
        };

        const style = animStyles[line.animation ?? 'slide-left'];

        return (
          <div key={i} style={{
            fontSize: line.size ?? 72,
            fontWeight: line.weight ?? 700,
            color: line.color ?? 'white',
            lineHeight: 1.15,
            ...style,
          }}>
            {line.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

## Source / Fact Citation Overlay

```tsx
export const SourceCitation: React.FC<{
  source: string;
  year?: number;
}> = ({ source, year }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.4], [0, 0.7], { extrapolateRight: 'clamp' });

  return (
    <div style={{
      position: 'absolute', bottom: 12, right: 24,
      fontSize: 16, color: 'rgba(255,255,255,0.7)',
      fontStyle: 'italic', opacity,
    }}>
      Source: {source}{year ? `, ${year}` : ''}
    </div>
  );
};
```

---

## News Explainer Structure (3–5 min)

```tsx
const NEWS_EXPLAINER_STRUCTURE = [
  { sec: 8,   type: 'hook-question',   note: '"Why is [X] happening right now?"' },
  { sec: 5,   type: 'breaking-ticker', note: 'News lower third slides in' },
  { sec: 30,  type: 'context',         note: 'Kinetic typography + data map' },
  { sec: 40,  type: 'data',            note: 'Animated bar chart / timeline' },
  { sec: 40,  type: 'cause-effect',    note: 'Diagram + voiceover' },
  { sec: 30,  type: 'global-impact',   note: 'World map with data points' },
  { sec: 30,  type: 'conclusion',      note: 'Key takeaways — 3 points max' },
  { sec: 10,  type: 'cta',             note: '"Subscribe for daily explainers"' },
];
```

---

## Cross-References
- `genres/viral-formula.md` — hook with urgent question, curiosity gap
- `rules/charts.md` — animated bar charts, line charts, counters
- `rules/text.md` — kinetic typography patterns
- `rules/tts-pipeline.md` — AI voiceover narration
- `rules/captions.md` — always include captions for news content
