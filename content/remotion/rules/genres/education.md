# Educational / Tutorial Video in Remotion

## Why Education Converts

Educational content builds the deepest audience trust. People who learn from you buy from you. The YouTube algorithm rewards it with long watch times. Tutorial videos average 8–12 min watch time vs 2–3 min for entertainment.

**The education formula:** Teach something valuable → Viewer feels smart → Viewer trusts you → Viewer buys from you.

---

## Screen Recording + Annotation Layer

For coding, software, or screen-based tutorials:

```tsx
export const ScreenAnnotation: React.FC<{
  x: number; y: number;
  width: number; height: number;
  label: string;
  style?: 'highlight' | 'arrow' | 'circle' | 'underline';
  color?: string;
  triggerFrame?: number;
}> = ({ x, y, width, height, label, style = 'highlight', color = '#FF6B35', triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF = frame - triggerFrame;
  const appear = spring({ frame: localF, fps, config: { damping: 60, stiffness: 120 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  const STYLES = {
    highlight: (
      <div style={{
        position: 'absolute', left: x, top: y, width, height,
        border: `3px solid ${color}`,
        borderRadius: 8,
        backgroundColor: `${color}18`,
        boxShadow: `0 0 0 4px ${color}30`,
        opacity,
      }} />
    ),
    circle: (
      <div style={{
        position: 'absolute',
        left: x - width / 2, top: y - height / 2,
        width, height,
        borderRadius: '50%',
        border: `3px solid ${color}`,
        backgroundColor: `${color}18`,
        opacity,
      }} />
    ),
    underline: (
      <div style={{
        position: 'absolute', left: x, top: y + height - 3, width,
        height: 3, backgroundColor: color, borderRadius: 2, opacity,
      }} />
    ),
    arrow: (
      <svg style={{ position: 'absolute', left: x - 40, top: y - 40, overflow: 'visible' }}
        viewBox="0 0 80 80" width={80} height={80}>
        <path d="M 10 10 L 50 50" stroke={color} strokeWidth={3}
          strokeLinecap="round" opacity={opacity}
          strokeDasharray={`${interpolate(appear, [0, 1], [0, 60])} 60`} />
        <polygon points="50,44 50,56 56,50" fill={color} opacity={opacity} />
      </svg>
    ),
  };

  return (
    <>
      {STYLES[style]}
      {/* Label */}
      <div style={{
        position: 'absolute', left: x, top: y + height + 8,
        backgroundColor: color, color: '#000',
        fontSize: 20, fontWeight: 700, padding: '4px 14px',
        borderRadius: 6, opacity, whiteSpace: 'nowrap',
      }}>
        {label}
      </div>
    </>
  );
};
```

---

## Concept Explainer — Animated Diagram

```tsx
export const ConceptDiagram: React.FC<{
  nodes: Array<{ id: string; label: string; x: number; y: number; color?: string }>;
  edges: Array<{ from: string; to: string; label?: string }>;
  triggerFrame?: number;
}> = ({ nodes, edges, triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Nodes appear staggered
  // Edges draw between nodes after both appear

  const nodePos = Object.fromEntries(nodes.map(n => [n.id, { x: n.x, y: n.y }]));

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a' }}>
      <svg width="100%" height="100%" viewBox="0 0 1920 1080">
        {/* Draw edges */}
        {edges.map((edge, i) => {
          const fromNode = nodes.find(n => n.id === edge.from);
          const toNode   = nodes.find(n => n.id === edge.to);
          if (!fromNode || !toNode) return null;

          const delay = triggerFrame + (nodes.length + i) * 6;
          const localF = frame - delay;
          const progress = interpolate(
            spring({ frame: Math.max(0, localF), fps, config: { damping: 60 } }),
            [0, 1], [0, 1]
          );
          const opacity = localF > 0 ? 1 : 0;

          const len = Math.hypot(toNode.x - fromNode.x, toNode.y - fromNode.y);

          return (
            <g key={`${edge.from}-${edge.to}`} opacity={opacity}>
              <line
                x1={fromNode.x} y1={fromNode.y}
                x2={fromNode.x + (toNode.x - fromNode.x) * progress}
                y2={fromNode.y + (toNode.y - fromNode.y) * progress}
                stroke="rgba(99,102,241,0.6)" strokeWidth={2}
                strokeDasharray="6 4"
              />
              {edge.label && progress > 0.5 && (
                <text
                  x={(fromNode.x + toNode.x) / 2}
                  y={(fromNode.y + toNode.y) / 2 - 10}
                  fill="rgba(255,255,255,0.5)"
                  fontSize={18} textAnchor="middle"
                >
                  {edge.label}
                </text>
              )}
            </g>
          );
        })}

        {/* Draw nodes */}
        {nodes.map((node, i) => {
          const delay = triggerFrame + i * 8;
          const localF = frame - delay;
          const scale = interpolate(
            spring({ frame: Math.max(0, localF), fps, config: { damping: 10, stiffness: 300 } }),
            [0, 1], [0, 1]
          );
          const opacity = localF > 0 ? 1 : 0;

          return (
            <g key={node.id} transform={`translate(${node.x}, ${node.y})`} opacity={opacity}>
              <circle r={50} fill={node.color ?? '#4f46e5'} style={{ transform: `scale(${scale})` }} />
              <text textAnchor="middle" dominantBaseline="middle"
                fill="white" fontSize={20} fontWeight={700}>
                {node.label}
              </text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
```

---

## Code Block Reveal (for Dev Tutorials)

```tsx
export const CodeReveal: React.FC<{
  code: string;
  language?: string;
  highlightLines?: number[];
  triggerFrame?: number;
}> = ({ code, language = 'tsx', highlightLines = [], triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const lines = code.split('\n');
  const visibleLines = Math.floor(
    interpolate(frame - triggerFrame, [0, fps * 3], [0, lines.length], {
      extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    })
  );

  return (
    <div style={{
      backgroundColor: '#1e1e2e',
      borderRadius: 16,
      padding: 32,
      border: '1px solid rgba(255,255,255,0.08)',
      fontFamily: "'Fira Code', 'Cascadia Code', monospace",
    }}>
      {/* Window chrome */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {['#ff5f57', '#ffbd2e', '#28ca41'].map((c) => (
          <div key={c} style={{ width: 14, height: 14, borderRadius: '50%', backgroundColor: c }} />
        ))}
        <span style={{ color: '#666', fontSize: 14, marginLeft: 8 }}>{language}</span>
      </div>

      {/* Code lines */}
      {lines.slice(0, visibleLines).map((line, i) => (
        <div key={i} style={{
          fontSize: 28,
          lineHeight: 1.7,
          color: highlightLines.includes(i + 1) ? '#fbbf24' : '#cdd6f4',
          backgroundColor: highlightLines.includes(i + 1) ? 'rgba(251,191,36,0.1)' : 'transparent',
          padding: '0 8px',
          borderLeft: highlightLines.includes(i + 1) ? '3px solid #fbbf24' : '3px solid transparent',
          fontFamily: 'monospace',
          whiteSpace: 'pre',
        }}>
          <span style={{ color: '#6c7086', marginRight: 20, userSelect: 'none', fontSize: 20 }}>
            {String(i + 1).padStart(2, ' ')}
          </span>
          {line}
        </div>
      ))}
    </div>
  );
};
```

---

## Numbered Steps (How-To Format)

```tsx
export const NumberedSteps: React.FC<{
  steps: Array<{ title: string; description: string; icon?: string }>;
  activeStep?: number;
}> = ({ steps, activeStep }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {steps.map((step, i) => {
        const delay = i * 12;
        const appear = spring({ frame: frame - delay, fps, config: { damping: 70 } });
        const isActive = activeStep === i;

        return (
          <div key={i} style={{
            display: 'flex', gap: 20, alignItems: 'flex-start',
            opacity: interpolate(appear, [0, 0.5], [0, 1]),
            transform: `translateX(${interpolate(appear, [0, 1], [-30, 0])}px)`,
          }}>
            {/* Step number circle */}
            <div style={{
              width: 52, height: 52, minWidth: 52,
              borderRadius: '50%',
              backgroundColor: isActive ? '#4f46e5' : 'rgba(79,70,229,0.2)',
              border: `2px solid ${isActive ? '#4f46e5' : 'rgba(79,70,229,0.4)'}`,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 26, fontWeight: 900,
              color: isActive ? 'white' : '#94a3b8',
            }}>
              {step.icon ?? (i + 1)}
            </div>

            <div>
              <div style={{
                fontSize: 32, fontWeight: 700,
                color: isActive ? 'white' : '#94a3b8',
                marginBottom: 4,
              }}>
                {step.title}
              </div>
              <div style={{ fontSize: 24, color: '#64748b', lineHeight: 1.5 }}>
                {step.description}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

---

## Infographic / Key Takeaways

```tsx
export const KeyTakeaway: React.FC<{
  number: string;
  title: string;
  body: string;
  triggerFrame?: number;
  accentColor?: string;
}> = ({ number, title, body, triggerFrame = 0, accentColor = '#4f46e5' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF = frame - triggerFrame;
  const appear = spring({ frame: localF, fps, config: { damping: 70 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);
  const y = interpolate(appear, [0, 1], [20, 0]);

  return (
    <div style={{
      backgroundColor: '#1e293b',
      border: `1px solid ${accentColor}40`,
      borderLeft: `4px solid ${accentColor}`,
      borderRadius: 12,
      padding: '24px 32px',
      opacity, transform: `translateY(${y}px)`,
    }}>
      <div style={{ display: 'flex', gap: 20, alignItems: 'flex-start' }}>
        <div style={{
          fontSize: 48, fontWeight: 900,
          color: accentColor, lineHeight: 1, minWidth: 60,
        }}>
          {number}
        </div>
        <div>
          <div style={{ fontSize: 28, fontWeight: 700, color: 'white', marginBottom: 8 }}>
            {title}
          </div>
          <div style={{ fontSize: 22, color: '#94a3b8', lineHeight: 1.6 }}>
            {body}
          </div>
        </div>
      </div>
    </div>
  );
};
```

---

## Educational Video Structures

```tsx
// Tutorial video (5–15 min YouTube)
const TUTORIAL_STRUCTURE = [
  { sec: 15,  type: 'hook',          note: 'Show end result first, then: "Here\'s how I did it"' },
  { sec: 20,  type: 'intro',         note: 'Brief who-you-are + what they\'ll learn' },
  { sec: 60,  type: 'concept',       note: 'Explain the theory / context' },
  { sec: 180, type: 'step-by-step',  note: 'Numbered steps with screen annotation' },
  { sec: 30,  type: 'common-mistakes', note: '"Don\'t do this..." — high retention' },
  { sec: 20,  type: 'recap',         note: 'Summary of all steps' },
  { sec: 15,  type: 'cta',           note: 'Subscribe + next video + resource link' },
];

// Explainer (60–90 second social)
const EXPLAINER_STRUCTURE = [
  { sec: 5,  type: 'hook',       note: '"You\'ve been doing X wrong"' },
  { sec: 15, type: 'concept',    note: 'Animated diagram of the idea' },
  { sec: 25, type: 'example',    note: 'Real example, visual proof' },
  { sec: 15, type: 'application',note: '"Here\'s how to use this"' },
  { sec: 10, type: 'cta',        note: 'Follow for more' },
];
```

---

## Cross-References
- `genres/viral-formula.md` — hook formula for educational hooks
- `rules/charts.md` — data visualisation for concept slides
- `rules/text.md` — animated text reveals for key points
- `rules/captions.md` — subtitles always (85% watch muted)
- `rules/tts-pipeline.md` — AI narration for faceless edu content
