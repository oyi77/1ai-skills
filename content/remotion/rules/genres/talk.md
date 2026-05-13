# Live Talk / Motivation Video — TED Talk Quality in Remotion

## The TED Standard

TED Talk production quality is defined by five non-negotiables:
1. **Restraint** — every graphic element must earn its place; nothing decorative without purpose
2. **The red circle** — recognisable red-on-black / red-on-white brand language (if TED-style)
3. **Typography-first** — ideas are communicated through words, not visuals; text must be pristine
4. **Lower thirds with authority** — speaker name + title appears once, cleanly, then disappears
5. **Concept graphics** — single diagrams/stats that reinforce the spoken word, not distract

---

## Layer Stack (Talk Scene Compositor)

```tsx
export const TalkScene: React.FC<{
  children: React.ReactNode;         // Speaker video / stage image
  style?: TalkStyle;
}> = ({ children, style = 'ted' }) => (
  <AbsoluteFill style={{ backgroundColor: '#000' }}>
    {/* 1. Stage / speaker layer */}
    {children}

    {/* 2. Subtle vignette — focuses eye to speaker */}
    <StageVignette />

    {/* 3. Brand colour overlay — very subtle */}
    {style === 'ted' && <TEDBrandOverlay />}
  </AbsoluteFill>
);

type TalkStyle = 'ted' | 'motivation' | 'keynote' | 'corporate' | 'podcast';
```

---

## 1. Stage Design

### TED-Style Stage (Dark Background, Speaker Lit)

```tsx
export const TEDStage: React.FC<{
  speakerVideo?: string;
  speakerImage?: string;
  showCircle?: boolean;
}> = ({ speakerVideo, speakerImage, showCircle = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const circleScale = spring({ frame, fps, config: { damping: 60, stiffness: 80 } });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* Stage floor reflection — subtle gradient */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0, height: '40%',
        background: 'linear-gradient(to top, rgba(180,30,30,0.06), transparent)',
      }} />

      {/* The Red Circle — TED's iconic stage element */}
      {showCircle && (
        <div style={{
          position: 'absolute',
          bottom: 120,
          left: '50%',
          transform: `translateX(-50%) scale(${circleScale})`,
          width: 320, height: 320,
          borderRadius: '50%',
          border: '4px solid #E62B1E',
          opacity: 0.9,
        }} />
      )}

      {/* Speaker */}
      {speakerVideo && (
        <OffthreadVideo
          src={staticFile(speakerVideo)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      )}
      {speakerImage && !speakerVideo && (
        <Img
          src={staticFile(speakerImage)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      )}

      {/* Three-point lighting simulation (if no real footage) */}
      {!speakerVideo && !speakerImage && (
        <>
          {/* Key light — left-of-centre */}
          <div style={{
            position: 'absolute',
            top: 0, left: '25%',
            width: 400, height: '70%',
            background: 'radial-gradient(ellipse at top, rgba(255,240,220,0.18) 0%, transparent 70%)',
          }} />
          {/* Fill light — right */}
          <div style={{
            position: 'absolute',
            top: 0, right: '20%',
            width: 300, height: '60%',
            background: 'radial-gradient(ellipse at top, rgba(200,220,255,0.08) 0%, transparent 70%)',
          }} />
        </>
      )}
    </AbsoluteFill>
  );
};
```

---

## 2. Lower Third (Speaker Identification)

TED uses exactly this: white text on dark pill, slides in from left, holds 4 seconds, fades out. Never flashes. Never bounces.

```tsx
export const TalkLowerThird: React.FC<{
  name: string;
  title: string;
  organisation?: string;
  triggerFrame?: number;
  holdDuration?: number;   // frames to hold before fade
  accentColor?: string;
}> = ({
  name, title, organisation,
  triggerFrame = 0,
  holdDuration = 150,   // 5 seconds at 30fps
  accentColor = '#E62B1E',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - triggerFrame;
  const fadeOutStart = holdDuration - 20;

  // Slide in
  const slideIn = spring({
    frame: localFrame,
    fps,
    config: { damping: 80, stiffness: 120 },
  });
  const x = interpolate(slideIn, [0, 1], [-500, 0]);

  // Fade out
  const opacity = localFrame > fadeOutStart
    ? interpolate(localFrame, [fadeOutStart, holdDuration], [1, 0], {
        extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
      })
    : localFrame > 0 ? 1 : 0;

  if (localFrame < 0 || localFrame > holdDuration) return null;

  return (
    <div style={{
      position: 'absolute',
      bottom: 120,
      left: 80,
      transform: `translateX(${x}px)`,
      opacity,
    }}>
      {/* Accent bar */}
      <div style={{
        width: 4, height: '100%',
        backgroundColor: accentColor,
        position: 'absolute', left: 0, top: 0,
        borderRadius: 2,
      }} />

      {/* Text block */}
      <div style={{
        paddingLeft: 20,
        backgroundColor: 'rgba(0,0,0,0.82)',
        padding: '14px 24px 14px 20px',
        borderRadius: '0 8px 8px 0',
        borderLeft: `4px solid ${accentColor}`,
      }}>
        <div style={{
          color: 'white',
          fontSize: 32,
          fontWeight: 700,
          letterSpacing: 0.5,
          lineHeight: 1.2,
          fontFamily: oswaldFont,
        }}>
          {name}
        </div>
        <div style={{
          color: 'rgba(255,255,255,0.75)',
          fontSize: 22,
          fontWeight: 400,
          marginTop: 4,
          fontFamily: oswaldFont,
          letterSpacing: 1,
        }}>
          {title}{organisation ? ` · ${organisation}` : ''}
        </div>
      </div>
    </div>
  );
};
```

---

## 3. Quote / Key Idea Card

The most powerful visual in a talk is a single, well-set sentence. No decoration. Maximum white space.

```tsx
export const QuoteCard: React.FC<{
  quote: string;
  attribution?: string;
  style?: 'ted' | 'dark' | 'white' | 'minimal';
  triggerFrame?: number;
}> = ({ quote, attribution, style = 'ted', triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - triggerFrame;
  const appear = spring({ frame: localFrame, fps, config: { damping: 70, stiffness: 100 } });

  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const y = interpolate(appear, [0, 1], [24, 0]);

  const STYLES = {
    ted:     { bg: '#0a0a0a', text: '#FFFFFF', accent: '#E62B1E', quote: 52 },
    dark:    { bg: '#111111', text: '#F0F0F0', accent: '#ffffff', quote: 52 },
    white:   { bg: '#FFFFFF', text: '#111111', accent: '#E62B1E', quote: 52 },
    minimal: { bg: 'transparent', text: '#FFFFFF', accent: '#ffffff', quote: 60 },
  };
  const s = STYLES[style];

  return (
    <AbsoluteFill style={{
      backgroundColor: s.bg,
      justifyContent: 'center',
      alignItems: 'center',
      padding: '80px 160px',
    }}>
      {/* Opening quotation mark */}
      <div style={{
        position: 'absolute',
        top: 80, left: 120,
        fontSize: 200,
        color: s.accent,
        opacity: 0.25,
        lineHeight: 1,
        fontFamily: 'Georgia, serif',
        transform: `translateY(${y}px)`,
        opacity: opacity * 0.25,
      }}>
        "
      </div>

      <div style={{
        transform: `translateY(${y}px)`,
        opacity,
        textAlign: 'center',
        maxWidth: 1400,
      }}>
        <p style={{
          fontSize: s.quote,
          fontWeight: 700,
          color: s.text,
          lineHeight: 1.4,
          margin: 0,
          fontFamily: playfairFont ?? 'Georgia, serif',
          fontStyle: 'italic',
        }}>
          "{quote}"
        </p>

        {attribution && (
          <p style={{
            fontSize: 28,
            color: s.accent,
            marginTop: 32,
            fontWeight: 400,
            letterSpacing: 3,
            textTransform: 'uppercase',
            fontFamily: oswaldFont,
          }}>
            — {attribution}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 4. Concept Diagram / Big Number

One graphic, one idea. TED never clutters.

```tsx
export const BigStat: React.FC<{
  value: number | string;
  label: string;
  subLabel?: string;
  accentColor?: string;
  triggerFrame?: number;
}> = ({ value, label, subLabel, accentColor = '#E62B1E', triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - triggerFrame;
  const appear = spring({ frame: localFrame, fps, config: { damping: 80, stiffness: 100 } });
  const isNumber = typeof value === 'number';
  const display = isNumber
    ? Math.round(interpolate(appear, [0, 1], [0, value]))
    : value;

  const opacity = interpolate(appear, [0, 0.4], [0, 1]);
  const scale = interpolate(appear, [0, 1], [0.88, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0a0a0a',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 16,
    }}>
      {/* The number — massive, unapologetic */}
      <div style={{
        fontSize: 240,
        fontWeight: 900,
        color: accentColor,
        lineHeight: 1,
        fontVariantNumeric: 'tabular-nums',
        opacity,
        transform: `scale(${scale})`,
        fontFamily: oswaldFont ?? 'sans-serif',
      }}>
        {isNumber ? display.toLocaleString() : display}
      </div>

      {/* Label */}
      <div style={{
        fontSize: 48,
        fontWeight: 300,
        color: 'white',
        letterSpacing: 8,
        textTransform: 'uppercase',
        opacity,
        fontFamily: oswaldFont,
      }}>
        {label}
      </div>

      {subLabel && (
        <div style={{
          fontSize: 28,
          color: 'rgba(255,255,255,0.5)',
          fontWeight: 300,
          opacity,
          fontFamily: oswaldFont,
          letterSpacing: 2,
        }}>
          {subLabel}
        </div>
      )}

      {/* Subtle rule underneath */}
      <div style={{
        width: interpolate(localFrame, [8, 30], [0, 200], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        }),
        height: 3,
        backgroundColor: accentColor,
        marginTop: 8,
        borderRadius: 2,
      }} />
    </AbsoluteFill>
  );
};
```

---

## 5. Slide / Chapter Transition

TED talks use simple, purposeful cuts and fades — never flashy wipes.

```tsx
export const TalkTransition: React.FC<{
  title: string;
  chapterNumber?: number;
  accentColor?: string;
}> = ({ title, chapterNumber, accentColor = '#E62B1E' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60, stiffness: 80 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0a0a0a',
      justifyContent: 'center', alignItems: 'flex-start',
      padding: '0 160px',
      flexDirection: 'column', gap: 20,
    }}>
      {chapterNumber && (
        <div style={{
          fontSize: 24,
          color: accentColor,
          fontWeight: 700,
          letterSpacing: 6,
          textTransform: 'uppercase',
          opacity,
          fontFamily: oswaldFont,
        }}>
          Part {chapterNumber}
        </div>
      )}

      <h2 style={{
        fontSize: 96,
        fontWeight: 700,
        color: 'white',
        margin: 0,
        lineHeight: 1.1,
        maxWidth: 1000,
        opacity,
        fontFamily: playfairFont ?? 'Georgia, serif',
      }}>
        {title}
      </h2>

      {/* Accent rule */}
      <div style={{
        height: 4,
        backgroundColor: accentColor,
        width: interpolate(frame, [5, 20], [0, 120], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        }),
        borderRadius: 2,
        opacity,
      }} />
    </AbsoluteFill>
  );
};
```

---

## 6. Motivation / Inspirational Style

For non-TED but same quality level — Simon Sinek, Tony Robbins, Gary Vee style.

```tsx
export const MOTIVATION_PALETTE = {
  dark: { bg: '#0a0a0a', accent: '#FFD700', text: '#FFFFFF' },
  fire: { bg: '#1a0500', accent: '#FF4500', text: '#FFFFFF' },
  blue: { bg: '#020d1a', accent: '#00AAFF', text: '#FFFFFF' },
  clean:{ bg: '#FFFFFF', accent: '#111111', text: '#111111' },
};

// Word-by-word spoken text reveal (synced to TTS audio)
export const SpokenWordReveal: React.FC<{
  words: Array<{ text: string; startFrame: number; endFrame: number }>;
  style?: 'bold' | 'clean';
  accentEvery?: number;  // accent every N words
}> = ({ words, style = 'bold', accentEvery = 5 }) => {
  const frame = useCurrentFrame();

  const active = words.filter((w) => frame >= w.startFrame);
  const current = words.find((w) => frame >= w.startFrame && frame <= w.endFrame);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', padding: '0 120px' }}>
      <div style={{ textAlign: 'center', maxWidth: 1400 }}>
        {active.map((w, i) => {
          const isCurrent = w === current;
          const isAccent = (i + 1) % accentEvery === 0;
          const entryOpacity = interpolate(frame - w.startFrame, [0, 6], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });

          return (
            <span key={i} style={{
              fontSize: style === 'bold' ? 80 : 64,
              fontWeight: style === 'bold' ? 900 : 400,
              color: isCurrent ? '#FFD700' : isAccent ? '#FF4500' : 'white',
              marginRight: 18,
              display: 'inline-block',
              opacity: entryOpacity,
              transform: `scale(${isCurrent ? 1.08 : 1})`,
              transition: 'none',
              fontFamily: isCurrent && style === 'bold' ? oswaldFont : oswaldFont,
              textShadow: isCurrent ? '0 0 30px rgba(255,215,0,0.4)' : 'none',
            }}>
              {w.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

---

## 7. Talk Structure Template

```tsx
// 18-minute TED Talk → video breakdown
const TED_STRUCTURE = [
  { id: 'cold-open',   sec: 60,  scene: 'speaker-hook'     },  // 0–60s
  { id: 'title',       sec: 5,   scene: 'talk-title-card'  },  // 60–65s
  { id: 'part1',       sec: 180, scene: 'speaker + stats'  },  // 65–245s
  { id: 'stat1',       sec: 8,   scene: 'big-number'       },
  { id: 'part2',       sec: 240, scene: 'speaker + diagram'},
  { id: 'quote',       sec: 10,  scene: 'quote-card'       },
  { id: 'part3',       sec: 240, scene: 'speaker + story'  },
  { id: 'call-action', sec: 60,  scene: 'call-to-action'   },
  { id: 'outro',       sec: 15,  scene: 'speaker-exit'     },
];

// Shorter motivation video (3–5 min)
const MOTIVATION_STRUCTURE = [
  { id: 'hook',   sec: 15, type: 'spoken-word-reveal' },  // Start with the punchline
  { id: 'pain',   sec: 30, type: 'speaker'            },  // Establish the problem
  { id: 'stat',   sec: 8,  type: 'big-number'         },  // Prove with data
  { id: 'shift',  sec: 45, type: 'speaker'            },  // The reframe
  { id: 'quote',  sec: 8,  type: 'quote-card'         },  // Crystallise it
  { id: 'path',   sec: 60, type: 'speaker'            },  // The solution
  { id: 'call',   sec: 20, type: 'cta'                },  // Call to action
];
```

---

## 8. Typography System

```tsx
import { loadFont as loadOswald }   from '@remotion/google-fonts/Oswald';
import { loadFont as loadPlayfair } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadInter }    from '@remotion/google-fonts/Inter';

const { fontFamily: oswaldFont }   = loadOswald();
const { fontFamily: playfairFont } = loadPlayfair();
const { fontFamily: interFont }    = loadInter();

export const TALK_TYPE = {
  // Talk title: authoritative, measured
  title: {
    fontFamily: playfairFont,
    fontSize: 96,
    fontWeight: 700,
    color: '#FFFFFF',
    letterSpacing: 2,
    lineHeight: 1.15,
  } as React.CSSProperties,

  // Speaker name: clear, direct
  speakerName: {
    fontFamily: oswaldFont,
    fontSize: 36,
    fontWeight: 600,
    color: '#FFFFFF',
    letterSpacing: 1,
    textTransform: 'uppercase' as const,
  } as React.CSSProperties,

  // Speaker title: subdued
  speakerTitle: {
    fontFamily: oswaldFont,
    fontSize: 24,
    fontWeight: 300,
    color: 'rgba(255,255,255,0.7)',
    letterSpacing: 2,
  } as React.CSSProperties,

  // Body text: readable at all sizes
  body: {
    fontFamily: interFont,
    fontSize: 40,
    fontWeight: 400,
    color: '#F0F0F0',
    lineHeight: 1.6,
  } as React.CSSProperties,

  // Pull quote: italic, commanding
  quote: {
    fontFamily: playfairFont,
    fontSize: 56,
    fontWeight: 700,
    fontStyle: 'italic' as const,
    color: '#FFFFFF',
    lineHeight: 1.4,
  } as React.CSSProperties,
};
```

---

## Required Packages

```bash
npm i @remotion/google-fonts @remotion/noise @remotion/captions
```

## Cross-References
- `rules/audio.md` → TTS narration, audio sync, Edge TTS for narration voice
- `rules/tts-pipeline.md` → full script → audio → timing → render pipeline
- `rules/captions.md` → @remotion/captions for word-level subtitle sync
- `rules/charts.md` → animated data visualisation for stats slides
- `rules/text.md` → SpokenWordReveal pattern, word-by-word timing
