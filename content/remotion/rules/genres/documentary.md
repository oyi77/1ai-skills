# Documentary / Mini-Doc Video in Remotion

## Why This Format Converts

Documentary-style videos are **2.3× more trusted** than traditional ads (HubSpot 2025). They work because they don't feel like selling. Netflix-style docs get 81M+ viewing hours in 4 days. Mini-docs under 5 minutes are the fastest-growing branded content format.

**The documentary equation:** Authenticity × Cinematic Quality = Maximum Trust

---

## Documentary Color Science

Mini-docs use naturalistic, slightly-desaturated grades that feel real, not advertised:

```tsx
type DocGrade =
  | 'natural'        // Clean, warm — brand docs, lifestyle
  | 'netflix'        // Slightly cool, high contrast — prestige feel
  | 'indie'          // Faded shadows, warm mids — intimate stories
  | 'investigative'  // Desaturated, high contrast — truth-telling
  | 'nature'         // Rich greens, golden hour — environmental

export const DOC_GRADES: Record<DocGrade, string> = {
  natural:       'contrast(1.06) saturate(0.92) brightness(1.03)',
  netflix:       'contrast(1.18) saturate(0.85) brightness(0.96) hue-rotate(-3deg)',
  indie:         'contrast(1.08) saturate(0.78) brightness(1.05) sepia(0.08)',
  investigative: 'contrast(1.35) saturate(0.55) brightness(0.9)',
  nature:        'contrast(1.12) saturate(1.3) brightness(1.04) hue-rotate(5deg)',
};
```

---

## Title Card — Documentary Opening

```tsx
export const DocTitleCard: React.FC<{
  title: string;
  year?: number;
  director?: string;
  grade?: DocGrade;
}> = ({ title, year, director, grade = 'netflix' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Slow fade in — documentaries breathe
  const opacity = interpolate(frame, [0, fps * 1.5], [0, 1], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Title comes in slightly later
  const titleOpacity = interpolate(frame, [fps * 0.8, fps * 2], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const titleY = interpolate(frame, [fps * 0.8, fps * 2], [12, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      filter: DOC_GRADES[grade],
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 20,
    }}>
      <div style={{ opacity, textAlign: 'center' }}>
        {/* Documentary-style thin label above title */}
        <div style={{
          fontSize: 18, letterSpacing: 8, color: '#888',
          textTransform: 'uppercase', fontWeight: 300,
          marginBottom: 24, fontFamily: 'Georgia, serif',
          opacity,
        }}>
          {year ?? new Date().getFullYear()}
        </div>

        <h1 style={{
          fontSize: 96,
          fontWeight: 700,
          color: 'white',
          letterSpacing: 2,
          margin: 0,
          lineHeight: 1.1,
          opacity: titleOpacity,
          transform: `translateY(${titleY}px)`,
          fontFamily: 'Georgia, serif',
          fontStyle: 'italic',
        }}>
          {title}
        </h1>

        {director && (
          <div style={{
            fontSize: 22, color: '#666', marginTop: 32,
            letterSpacing: 4, textTransform: 'uppercase',
            opacity: interpolate(frame, [fps * 2, fps * 2.5], [0, 1], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            }),
          }}>
            A film by {director}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Interview / Talking Head Scene

The most-used doc format: person speaks to camera with title identifying them.

```tsx
export const InterviewScene: React.FC<{
  videoSrc?: string;
  imageSrc?: string;
  name: string;
  title: string;
  quote?: string;
  grade?: DocGrade;
}> = ({ videoSrc, imageSrc, name, title, quote, grade = 'natural' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>
      {/* Subject footage */}
      {videoSrc && (
        <OffthreadVideo
          src={staticFile(videoSrc)}
          style={{ width: '100%', height: '100%', objectFit: 'cover', filter: DOC_GRADES[grade] }}
        />
      )}
      {imageSrc && !videoSrc && (
        <Img src={staticFile(imageSrc)} style={{
          width: '100%', height: '100%', objectFit: 'cover', filter: DOC_GRADES[grade],
        }} />
      )}

      {/* Vignette for documentary feel */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 30% 50%, transparent 35%, rgba(0,0,0,0.6) 100%)',
      }} />

      {/* Pull quote — appears mid-interview */}
      {quote && (
        <div style={{
          position: 'absolute', left: 80, right: 240,
          bottom: 200,
          opacity: interpolate(frame, [fps * 2, fps * 3], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          }),
        }}>
          <p style={{
            fontSize: 44, color: 'white', lineHeight: 1.4,
            margin: 0, fontStyle: 'italic', fontFamily: 'Georgia, serif',
            textShadow: '0 2px 12px rgba(0,0,0,0.8)',
          }}>
            "{quote}"
          </p>
        </div>
      )}

      {/* Lower third — slides in at 1.5s */}
      <InterviewLowerThird
        name={name}
        title={title}
        triggerFrame={Math.round(fps * 1.5)}
      />
    </AbsoluteFill>
  );
};

// Minimal documentary lower third — less flashy than TED, more journalistic
const InterviewLowerThird: React.FC<{
  name: string; title: string; triggerFrame: number;
}> = ({ name, title, triggerFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF = frame - triggerFrame;
  const progress = spring({ frame: localF, fps, config: { damping: 100, stiffness: 80 } });
  const x = interpolate(progress, [0, 1], [-400, 0]);
  const opacity = localF > 120
    ? interpolate(localF, [120, 145], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
    : localF >= 0 ? 1 : 0;

  return (
    <div style={{
      position: 'absolute', bottom: 80, left: 80,
      transform: `translateX(${x}px)`, opacity,
    }}>
      <div style={{
        width: 3, height: '100%',
        backgroundColor: 'white',
        position: 'absolute', left: 0,
      }} />
      <div style={{ paddingLeft: 16 }}>
        <div style={{ color: 'white', fontSize: 28, fontWeight: 600 }}>{name}</div>
        <div style={{ color: 'rgba(255,255,255,0.65)', fontSize: 20, marginTop: 3 }}>{title}</div>
      </div>
    </div>
  );
};
```

---

## B-Roll / Cutaway Scene

```tsx
// B-roll with atmospheric overlay text (place quote on top of footage)
export const BRollScene: React.FC<{
  videoSrc: string;
  captionText?: string;
  grade?: DocGrade;
  playbackRate?: number;
}> = ({ videoSrc, captionText, grade = 'natural', playbackRate = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textOpacity = interpolate(frame, [fps * 0.5, fps * 1.5], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill>
      <OffthreadVideo
        src={staticFile(videoSrc)}
        style={{ width: '100%', height: '100%', objectFit: 'cover', filter: DOC_GRADES[grade] }}
        muted
        playbackRate={playbackRate}
      />

      {/* Film-style vignette */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 50% 60%, transparent 45%, rgba(0,0,0,0.45) 100%)',
      }} />

      {captionText && (
        <div style={{
          position: 'absolute', bottom: 80, left: 80, right: 80,
          opacity: textOpacity,
        }}>
          <p style={{
            fontSize: 38, color: 'rgba(255,255,255,0.9)',
            fontStyle: 'italic', fontFamily: 'Georgia, serif',
            textShadow: '0 1px 8px rgba(0,0,0,0.6)',
            lineHeight: 1.5, margin: 0,
          }}>
            {captionText}
          </p>
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Archival / Text Card

For docs without footage — title cards between sections.

```tsx
export const ArchivalCard: React.FC<{
  year: string;
  location?: string;
  context: string;
}> = ({ year, location, context }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps * 0.6, fps * 3, fps * 3.5], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'flex-start',
      padding: '0 120px', flexDirection: 'column', gap: 12,
      opacity,
    }}>
      <div style={{ fontSize: 20, color: '#666', letterSpacing: 6, textTransform: 'uppercase' }}>
        {year}{location ? ` · ${location}` : ''}
      </div>
      <p style={{
        fontSize: 56, color: 'white', fontFamily: 'Georgia, serif',
        margin: 0, lineHeight: 1.4, maxWidth: 1200, fontStyle: 'italic',
      }}>
        {context}
      </p>
    </AbsoluteFill>
  );
};
```

---

## Three-Act Mini-Doc Structure (5 Minutes)

```tsx
const MINI_DOC_STRUCTURE = [
  // ACT 1: HOOK (0:00–0:45) — Cold open with the most dramatic moment
  { id: 'cold-open',    sec: 20, type: 'b-roll',     note: 'Most dramatic moment first' },
  { id: 'title-card',   sec: 5,  type: 'title',      note: 'Simple, impactful title' },
  { id: 'setup',        sec: 20, type: 'interview',  note: 'Who is this person and why should I care?' },

  // ACT 2: CONFRONTATION (0:45–3:30) — The journey, struggle, transformation
  { id: 'context',      sec: 45, type: 'b-roll + interview', note: 'Build the world' },
  { id: 'conflict',     sec: 45, type: 'interview',          note: 'The challenge/problem' },
  { id: 'turning-pt',   sec: 30, type: 'b-roll',             note: 'The moment everything changed' },
  { id: 'stakes',       sec: 45, type: 'interview + stats',  note: 'What\'s at risk?' },

  // ACT 3: RESOLUTION (3:30–5:00) — Payoff, transformation, call to care
  { id: 'resolution',   sec: 40, type: 'b-roll',    note: 'Show the outcome' },
  { id: 'reflection',   sec: 35, type: 'interview', note: 'What does this mean?' },
  { id: 'end-card',     sec: 15, type: 'title',     note: 'Single impact statement' },
];
```

---

## Documentary Narration Styles

```tsx
// Style 1: Voiceover-led (Ken Burns style)
// TTS narration over B-roll — load rules/tts-pipeline.md

// Style 2: Interview-led (Vice / Netflix style)
// Subjects tell story in their own words — load rules/captions.md for subtitles

// Style 3: Text-card-led (social-first)
// No voiceover, just text overlays — maximum accessibility
export const TextCardDoc: React.FC<{ lines: string[] }> = ({ lines }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const lineIndex = Math.floor(frame / (fps * 1.5));
  const currentLine = lines[Math.min(lineIndex, lines.length - 1)];

  const lineOpacity = interpolate(
    frame - lineIndex * fps * 1.5,
    [0, 8, fps * 1.3, fps * 1.5],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      justifyContent: 'center', alignItems: 'center',
    }}>
      <p style={{
        fontSize: 64, color: 'white',
        textAlign: 'center', padding: '0 120px',
        lineHeight: 1.4, margin: 0,
        fontFamily: 'Georgia, serif', fontStyle: 'italic',
        opacity: lineOpacity,
      }}>
        {currentLine}
      </p>
    </AbsoluteFill>
  );
};
```

---

## Cross-References
- `genres/viral-formula.md` — documentary earns trust, trust drives conversion
- `rules/tts-pipeline.md` — voiceover narration generation
- `rules/captions.md` — subtitles for interview footage
- `rules/audio.md` — ambient sound design for authenticity
- `rules/rendering.md` — film grain overlay for documentary texture
