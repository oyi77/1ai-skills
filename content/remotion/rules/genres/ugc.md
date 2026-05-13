# UGC / Authentic Ad Video in Remotion

## Why UGC Outperforms Traditional Ads

- **4× higher click-through rate** than polished brand ads
- **50% lower cost-per-click** on paid platforms
- **76%** of consumers find UGC more trustworthy than brand content
- **50%** of TikTok users have bought something after seeing UGC

The paradox: **authenticity is the most effective production value**. Over-polished = distrust. Raw + real = conversion.

---

## The UGC Aesthetic Toolkit

UGC looks intentionally unpolished. These are the specific visual markers that signal "real person, real experience":

```tsx
// Simulate smartphone camera characteristics
export const UGCLens: React.FC<{ children: React.ReactNode; handheld?: boolean }> = ({
  children, handheld = true,
}) => {
  const frame = useCurrentFrame();

  // Subtle handheld shake (organic, not random)
  const shakeX = handheld ? noise2D('ugc-x', frame * 0.04, 0) * 5 : 0;
  const shakeY = handheld ? noise2D('ugc-y', frame * 0.04, 1) * 3 : 0;
  const tilt   = handheld ? noise2D('ugc-r', frame * 0.03, 2) * 0.4 : 0;

  return (
    <AbsoluteFill style={{
      // Smartphone sensor: warm, slightly-washed colour
      filter: 'contrast(1.05) saturate(0.95) brightness(1.06)',
      transform: `translate(${shakeX}px, ${shakeY}px) rotate(${tilt}deg)`,
    }}>
      {children}
    </AbsoluteFill>
  );
};

// Vertical format — smartphone native
export const UGC_FORMATS = {
  tiktok:    { width: 1080, height: 1920, fps: 30 },
  reels:     { width: 1080, height: 1920, fps: 30 },
  square:    { width: 1080, height: 1080, fps: 30 },
  landscape: { width: 1920, height: 1080, fps: 30 }, // rare for UGC
};
```

---

## UGC Video Types (Each With Remotion Pattern)

### 1. Review / Testimonial

The most converting UGC format. Real person, real opinion.

```tsx
export const ReviewVideo: React.FC<{
  productName: string;
  rating: 1 | 2 | 3 | 4 | 5;
  reviewLines: string[];
  hook: string;
}> = ({ productName, rating, reviewLines, hook }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const lineIndex = Math.floor(frame / (fps * 2.5));
  const currentLine = reviewLines[Math.min(lineIndex, reviewLines.length - 1)];
  const lineOpacity = interpolate(
    frame - lineIndex * fps * 2.5,
    [0, 8, fps * 2.3, fps * 2.5],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#fff' }}>
      <UGCLens>
        {/* Hook text — first 3 seconds */}
        {frame < fps * 3 && (
          <div style={{
            position: 'absolute', top: '15%',
            left: 0, right: 0, textAlign: 'center', padding: '0 40px',
            opacity: interpolate(frame, [0, 6, fps * 2.8, fps * 3], [0, 1, 1, 0], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
            }),
          }}>
            <div style={{
              fontSize: 64, fontWeight: 900, color: '#000',
              backgroundColor: '#FFE000',
              padding: '8px 24px', borderRadius: 8, display: 'inline-block',
            }}>
              {hook}
            </div>
          </div>
        )}

        {/* Star rating */}
        <div style={{
          position: 'absolute', top: '8%', left: 32,
          fontSize: 40, color: '#FFD700',
        }}>
          {'⭐'.repeat(rating)}
        </div>

        {/* Review text cards */}
        {frame >= fps * 3 && (
          <div style={{
            position: 'absolute', bottom: '20%',
            left: 32, right: 32,
            backgroundColor: 'rgba(0,0,0,0.85)',
            borderRadius: 16, padding: 24,
            opacity: lineOpacity,
          }}>
            <p style={{
              color: 'white', fontSize: 40,
              margin: 0, lineHeight: 1.4, fontWeight: 500,
            }}>
              {currentLine}
            </p>
          </div>
        )}

        {/* Product name bottom */}
        <div style={{
          position: 'absolute', bottom: 60, left: 0, right: 0,
          textAlign: 'center', fontSize: 28, color: '#666',
          fontWeight: 600,
        }}>
          {productName}
        </div>
      </UGCLens>
    </AbsoluteFill>
  );
};
```

### 2. Unboxing / Haul

```tsx
// Unboxing text overlays — the key visual element
export const UnboxingOverlay: React.FC<{
  productName: string;
  price?: string;
  reactionEmoji?: string;
}> = ({ productName, price, reactionEmoji = '😍' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({ frame, fps, config: { damping: 8, stiffness: 400 } });

  return (
    <>
      {/* Big emoji reaction */}
      <div style={{
        position: 'absolute', top: '10%', right: '8%',
        fontSize: 100,
        transform: `scale(${pop})`,
        zIndex: 50,
      }}>
        {reactionEmoji}
      </div>

      {/* Product name badge */}
      <div style={{
        position: 'absolute', bottom: '25%', left: 0, right: 0,
        textAlign: 'center',
        opacity: interpolate(frame, [fps * 0.5, fps * 1], [0, 1], { extrapolateRight: 'clamp' }),
      }}>
        <div style={{
          display: 'inline-block',
          backgroundColor: '#000',
          color: 'white',
          fontSize: 36,
          fontWeight: 800,
          padding: '10px 28px',
          borderRadius: 100,
        }}>
          {productName} {price && `· ${price}`}
        </div>
      </div>
    </>
  );
};
```

### 3. Before / After Transformation

```tsx
export const BeforeAfterUGC: React.FC<{
  beforeText: string;
  afterText: string;
  productName: string;
  daysUsed?: number;
}> = ({ beforeText, afterText, productName, daysUsed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const showAfter = frame > fps * 4;
  const swipeProgress = interpolate(frame, [fps * 3.5, fps * 4.5], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#f5f5f5' }}>
      <UGCLens handheld>
        {/* BEFORE / AFTER label */}
        <div style={{
          position: 'absolute', top: 40, left: 0, right: 0,
          display: 'flex', justifyContent: 'center',
          gap: 20, zIndex: 10,
        }}>
          {['BEFORE', 'AFTER'].map((label, i) => (
            <div key={label} style={{
              fontSize: 32, fontWeight: 900,
              color: i === 0 ? (showAfter ? '#999' : '#FF2244') : (showAfter ? '#00CC44' : '#999'),
              transition: 'none',
            }}>
              {label}
            </div>
          ))}
        </div>

        {/* Before state */}
        {!showAfter && (
          <div style={{
            position: 'absolute', inset: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 48, color: '#333', fontWeight: 700, padding: '0 60px',
            textAlign: 'center',
          }}>
            {beforeText}
          </div>
        )}

        {/* After reveal — wipe in */}
        {showAfter && (
          <div style={{
            position: 'absolute', inset: 0,
            clipPath: `inset(0 ${(1 - swipeProgress) * 100}% 0 0)`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            backgroundColor: '#e8f5e9',
            fontSize: 48, color: '#1b5e20', fontWeight: 700, padding: '0 60px',
            textAlign: 'center',
          }}>
            {afterText}
          </div>
        )}

        {/* Product CTA */}
        {showAfter && (
          <div style={{
            position: 'absolute', bottom: 80, left: 0, right: 0,
            textAlign: 'center',
            opacity: interpolate(frame - fps * 4.5, [0, 15], [0, 1], { extrapolateRight: 'clamp' }),
          }}>
            <div style={{
              display: 'inline-block',
              backgroundColor: '#000',
              color: 'white', fontSize: 32, fontWeight: 800,
              padding: '12px 32px', borderRadius: 100,
            }}>
              {daysUsed ? `${daysUsed} days of ` : ''}{productName} ✓
            </div>
          </div>
        )}
      </UGCLens>
    </AbsoluteFill>
  );
};
```

### 4. Tutorial / How-To UGC

```tsx
export const TutorialStep: React.FC<{
  stepNumber: number;
  totalSteps: number;
  instruction: string;
  tip?: string;
}> = ({ stepNumber, totalSteps, instruction, tip }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 70 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);

  return (
    <div style={{
      position: 'absolute', bottom: 100, left: 24, right: 24,
      opacity,
    }}>
      {/* Step indicator */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
        {Array.from({ length: totalSteps }).map((_, i) => (
          <div key={i} style={{
            height: 4,
            flex: 1,
            backgroundColor: i < stepNumber ? '#00CC44' : 'rgba(255,255,255,0.3)',
            borderRadius: 2,
          }} />
        ))}
      </div>

      {/* Instruction */}
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.88)',
        borderRadius: 16, padding: 20,
      }}>
        <div style={{ color: '#00CC44', fontSize: 18, marginBottom: 6, fontWeight: 700 }}>
          STEP {stepNumber} OF {totalSteps}
        </div>
        <p style={{ color: 'white', fontSize: 36, margin: 0, fontWeight: 600, lineHeight: 1.3 }}>
          {instruction}
        </p>
        {tip && (
          <p style={{ color: '#aaa', fontSize: 24, margin: '8px 0 0', fontStyle: 'italic' }}>
            💡 {tip}
          </p>
        )}
      </div>
    </div>
  );
};
```

---

## UGC Text Styles (Platform-Native)

```tsx
// TikTok native caption style
export const TikTokCaption: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const words = text.split(' ');
  const activeWords = Math.floor((frame / fps) * 3.5); // ~3.5 words/second

  return (
    <div style={{
      position: 'absolute', bottom: '18%',
      left: 24, right: 24, textAlign: 'center',
    }}>
      {words.map((word, i) => (
        <span key={i} style={{
          display: 'inline-block',
          fontSize: 56, fontWeight: 900,
          color: i < activeWords ? 'white' : 'rgba(255,255,255,0.3)',
          textShadow: '2px 2px 4px rgba(0,0,0,0.8)',
          marginRight: 10,
          transform: `scale(${i === activeWords - 1 ? 1.1 : 1})`,
          transition: 'none',
          backgroundColor: i < activeWords ? 'rgba(0,0,0,0.5)' : 'transparent',
          padding: '0 4px',
          borderRadius: 4,
        }}>
          {word}
        </span>
      ))}
    </div>
  );
};

// Text overlay sticker (native TikTok look)
export const TextSticker: React.FC<{
  text: string;
  color?: string;
  rotation?: number;
  x?: number; y?: number;
}> = ({ text, color = '#FFE000', rotation = -3, x = 50, y = 30 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 6, stiffness: 500 } });

  return (
    <div style={{
      position: 'absolute', left: `${x}%`, top: `${y}%`,
      transform: `rotate(${rotation}deg) scale(${pop})`,
      transformOrigin: 'center',
      backgroundColor: color,
      color: '#000', fontSize: 36, fontWeight: 900,
      padding: '8px 20px', borderRadius: 8,
      boxShadow: '3px 3px 0 rgba(0,0,0,0.3)',
      whiteSpace: 'nowrap',
    }}>
      {text}
    </div>
  );
};
```

---

## UGC Ad Formula (15–30 Second)

```tsx
const UGC_AD_STRUCTURE = [
  { sec: 3,  type: 'hook',        content: 'Bold claim or question — stop the scroll' },
  { sec: 5,  type: 'pain-point',  content: 'Relate to the problem' },
  { sec: 8,  type: 'product',     content: 'Show product in action naturally' },
  { sec: 7,  type: 'result',      content: 'Before/after or transformation' },
  { sec: 4,  type: 'social-proof',content: 'Star rating, "1,000+ reviews"' },
  { sec: 3,  type: 'cta',         content: 'Link in bio / Swipe up / Shop now' },
];
// Total: 30 seconds — optimal for paid TikTok/Meta ads
```

---

## Cross-References
- `genres/viral-formula.md` — hook formula, open loops, CTA science
- `genres/influencer.md` — platform formats, zoom punches, progress bars
- `rules/captions.md` — always-on subtitles for sound-off viewing
- `rules/audio.md` — trending audio tracks for TikTok
- `rules/effects.md` — `noise2D` for authentic handheld shake
