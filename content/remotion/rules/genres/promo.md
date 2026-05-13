# Promotional, Corporate & Explainer Video in Remotion

## Video Types Covered

- **Brand promo** — emotional storytelling, logo reveal, brand colors
- **Explainer / explainer animation** — concept breakdowns with icons + motion graphics
- **Corporate / company profile** — professional, data-driven, trust-building
- **Event promo** — countdown, date reveal, speakers
- **Educational / tutorial** — step-by-step screen + annotation
- **Social media ad** — short (6–30s), strong hook, fast CTA

---

## Logo Reveal

```tsx
const LogoReveal: React.FC<{ logoSrc: string; brandName: string }> = ({
  logoSrc, brandName,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Circle wipe reveals logo
  const wipeScale = spring({ frame: frame - 10, fps, config: { damping: 50, stiffness: 100 } });

  // Name types in after logo appears
  const nameProgress = interpolate(frame, [40, 70], [0, brandName.length], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const visibleName = brandName.slice(0, Math.round(nameProgress));

  return (
    <AbsoluteFill style={{ backgroundColor: '#fff', justifyContent: 'center', alignItems: 'center', gap: 32 }}>
      {/* Logo with clip circle */}
      <div style={{
        transform: `scale(${wipeScale})`,
        width: 180, height: 180,
        borderRadius: '50%',
        overflow: 'hidden',
        boxShadow: '0 12px 60px rgba(0,0,0,0.15)',
      }}>
        <Img src={staticFile(logoSrc)} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
      </div>

      {/* Brand name typewriter */}
      <h1 style={{
        fontSize: 80,
        fontWeight: 700,
        color: '#1a1a1a',
        letterSpacing: 4,
        margin: 0,
        minWidth: 600,
        textAlign: 'center',
      }}>
        {visibleName}
        <span style={{ opacity: frame % 20 < 10 ? 1 : 0 }}>|</span>
      </h1>
    </AbsoluteFill>
  );
};
```

## Animated Icon + Text Explainer

```tsx
interface ExplainerStep {
  icon: string;      // emoji or SVG
  title: string;
  description: string;
  color: string;
}

const ExplainerStep: React.FC<{ step: ExplainerStep; index: number }> = ({ step, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 15;
  const appear = spring({ frame: frame - delay, fps, config: { damping: 70 } });
  const scale = interpolate(appear, [0, 1], [0.7, 1]);
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: 16,
      width: 280,
      transform: `scale(${scale})`,
      opacity,
    }}>
      {/* Icon circle */}
      <div style={{
        width: 100, height: 100,
        borderRadius: '50%',
        backgroundColor: step.color + '22',
        border: `3px solid ${step.color}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 48,
      }}>
        {step.icon}
      </div>

      {/* Step number */}
      <div style={{
        fontSize: 20,
        fontWeight: 700,
        color: step.color,
        letterSpacing: 3,
        textTransform: 'uppercase',
      }}>
        LANGKAH {index + 1}
      </div>

      <h3 style={{ fontSize: 30, fontWeight: 800, color: 'white', margin: 0, textAlign: 'center' }}>
        {step.title}
      </h3>
      <p style={{ fontSize: 22, color: '#94a3b8', margin: 0, textAlign: 'center', lineHeight: 1.5 }}>
        {step.description}
      </p>
    </div>
  );
};

// 3-step explainer layout
const ThreeStepExplainer: React.FC<{ steps: ExplainerStep[] }> = ({ steps }) => (
  <AbsoluteFill style={{
    backgroundColor: '#0f172a',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column',
    gap: 60,
    padding: 80,
  }}>
    <h2 style={{ color: 'white', fontSize: 60, fontWeight: 800, margin: 0 }}>
      Cara Kerja
    </h2>

    <div style={{ display: 'flex', gap: 60, alignItems: 'flex-start' }}>
      {steps.map((step, i) => (
        <React.Fragment key={i}>
          <ExplainerStep step={step} index={i} />
          {i < steps.length - 1 && (
            <div style={{
              color: '#475569',
              fontSize: 48,
              marginTop: 24,
              opacity: interpolate(useCurrentFrame(), [i * 15 + 25, i * 15 + 35], [0, 1], {
                extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
              }),
            }}>
              →
            </div>
          )}
        </React.Fragment>
      ))}
    </div>
  </AbsoluteFill>
);
```

## Testimonial / Social Proof Card

```tsx
const TestimonialCard: React.FC<{
  quote: string;
  name: string;
  role: string;
  avatarSrc?: string;
  rating?: number;
}> = ({ quote, name, role, avatarSrc, rating = 5 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame, fps, config: { damping: 60 } });
  const scale = interpolate(appear, [0, 1], [0.9, 1]);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div style={{
        backgroundColor: '#1e293b',
        borderRadius: 24,
        padding: 60,
        maxWidth: 900,
        transform: `scale(${scale})`,
        boxShadow: '0 24px 80px rgba(0,0,0,0.4)',
        border: '1px solid rgba(255,255,255,0.08)',
      }}>
        {/* Stars */}
        <div style={{ fontSize: 36, marginBottom: 24 }}>
          {'⭐'.repeat(rating)}
        </div>

        {/* Quote */}
        <blockquote style={{
          color: 'white',
          fontSize: 40,
          fontStyle: 'italic',
          lineHeight: 1.5,
          margin: '0 0 40px',
        }}>
          "{quote}"
        </blockquote>

        {/* Author */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
          {avatarSrc && (
            <Img src={staticFile(avatarSrc)} style={{
              width: 72, height: 72, borderRadius: '50%', objectFit: 'cover',
            }} />
          )}
          <div>
            <div style={{ color: 'white', fontSize: 30, fontWeight: 700 }}>{name}</div>
            <div style={{ color: '#6366f1', fontSize: 24 }}>{role}</div>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

## Stats / Numbers Section

```tsx
interface StatItem { label: string; value: number; prefix?: string; suffix?: string; color?: string }

const StatsSection: React.FC<{ stats: StatItem[]; title?: string }> = ({ stats, title }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0f172a',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      gap: 60,
    }}>
      {title && (
        <h2 style={{
          color: 'white', fontSize: 60, fontWeight: 800, margin: 0,
          opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' }),
        }}>
          {title}
        </h2>
      )}

      <div style={{ display: 'flex', gap: 80 }}>
        {stats.map((stat, i) => {
          const delay = i * 10;
          const progress = spring({ frame: frame - delay, fps, config: { damping: 100 } });
          const value = Math.round(interpolate(progress, [0, 1], [0, stat.value]));
          const opacity = interpolate(frame - delay, [0, 15], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });

          return (
            <div key={i} style={{ textAlign: 'center', opacity }}>
              <div style={{
                fontSize: 96,
                fontWeight: 900,
                color: stat.color ?? '#6366f1',
              }}>
                {stat.prefix}{value.toLocaleString('id-ID')}{stat.suffix}
              </div>
              <div style={{ color: '#94a3b8', fontSize: 28, marginTop: 8 }}>{stat.label}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

## Event Countdown

```tsx
const EventCountdown: React.FC<{
  eventName: string;
  eventDate: string;
  daysRemaining: number;
}> = ({ eventName, eventDate, daysRemaining }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Flip number animation
  const secondsElapsed = frame / fps;
  const hoursRemaining = Math.max(0, daysRemaining * 24 - Math.floor(secondsElapsed / 60));
  const minutesRemaining = (daysRemaining * 24 * 60) - Math.floor(secondsElapsed);
  const secondsRemaining = (daysRemaining * 24 * 60 * 60) - Math.floor(secondsElapsed);

  const d = Math.floor(secondsRemaining / 86400);
  const h = Math.floor((secondsRemaining % 86400) / 3600);
  const m = Math.floor((secondsRemaining % 3600) / 60);
  const s = secondsRemaining % 60;

  const CountUnit: React.FC<{ value: number; label: string }> = ({ value, label }) => (
    <div style={{ textAlign: 'center' }}>
      <div style={{
        fontSize: 120,
        fontWeight: 900,
        color: 'white',
        fontVariantNumeric: 'tabular-nums',
        lineHeight: 1,
      }}>
        {String(value).padStart(2, '0')}
      </div>
      <div style={{ color: '#6366f1', fontSize: 24, letterSpacing: 4, textTransform: 'uppercase' }}>
        {label}
      </div>
    </div>
  );

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      gap: 40,
    }}>
      <h1 style={{ color: 'white', fontSize: 64, fontWeight: 800, margin: 0 }}>{eventName}</h1>
      <p style={{ color: '#94a3b8', fontSize: 32, margin: 0 }}>{eventDate}</p>

      <div style={{ display: 'flex', gap: 60, marginTop: 20 }}>
        <CountUnit value={d} label="Hari" />
        <div style={{ color: '#475569', fontSize: 100, alignSelf: 'flex-start', lineHeight: 1.2 }}>:</div>
        <CountUnit value={h} label="Jam" />
        <div style={{ color: '#475569', fontSize: 100, alignSelf: 'flex-start', lineHeight: 1.2 }}>:</div>
        <CountUnit value={m} label="Menit" />
        <div style={{ color: '#475569', fontSize: 100, alignSelf: 'flex-start', lineHeight: 1.2 }}>:</div>
        <CountUnit value={s} label="Detik" />
      </div>
    </AbsoluteFill>
  );
};
```

## Screen Recording Annotation

```tsx
// For tutorials: animated arrow + highlight box
const Annotation: React.FC<{
  x: number; y: number; w: number; h: number;
  label: string;
  triggerFrame: number;
}> = ({ x, y, w, h, label, triggerFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame: frame - triggerFrame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);

  return (
    <>
      {/* Highlight box */}
      <div style={{
        position: 'absolute',
        left: x, top: y, width: w, height: h,
        border: `3px solid #ff6b35`,
        borderRadius: 8,
        opacity,
        boxShadow: '0 0 0 4px rgba(255,107,53,0.3)',
        backgroundColor: 'rgba(255,107,53,0.08)',
      }} />
      {/* Label */}
      <div style={{
        position: 'absolute',
        left: x, top: y + h + 8,
        backgroundColor: '#ff6b35',
        color: 'white',
        fontSize: 22,
        fontWeight: 700,
        padding: '6px 16px',
        borderRadius: 6,
        opacity,
        whiteSpace: 'nowrap',
      }}>
        ↑ {label}
      </div>
    </>
  );
};
```

## Cross-References
- For declarative animations (faster dev): load `rules/ecosystem.md` → remotion-animated / remotion-kit
- For animated text libraries: load `rules/ecosystem.md` → remotion-animate-text / remotion-bits
- For draw-on SVG paths (logo/underline): load `rules/effects.md` → @remotion/paths
- For screen annotation shapes: load `rules/effects.md` → @remotion/shapes
- For noise-based organic feel: load `rules/effects.md` → @remotion/noise
- For copy-paste components: load `rules/ecosystem.md` → Clippkit / remocn
