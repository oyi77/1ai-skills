# Viral Challenge / MrBeast-Style Video in Remotion

## The Challenge Formula (Reverse-Engineered)

MrBeast's leaked production guide and analysis of 100M+ view videos reveals a rigid structure:

```
HOOK (0–5s):      Stakes stated immediately. "Last to leave wins $100,000."
TEASE (5–30s):    Show contestants/setup. Plant curiosity about who will win.
ESCALATION:       Stakes rise continuously. Never plateau. Add complications.
RE-HOOK (3 min):  Second major hook — something nobody expected.
BACK-HALF:        Faster cuts, higher stakes, more reactions.
PAYOFF:           Reveal/winner/result that justifies every second of watching.
```

**The retention secret:** the payoff is **withheld until the end**. Every frame before it is designed to make leaving feel costly.

---

## Visual Language

Challenge videos use a specific aesthetic: high energy, bright colours, constant motion, text overlays, reaction shots, timer graphics, and progress indicators.

```tsx
export const CHALLENGE_PALETTE = {
  primary:    '#FF4500',  // orange-red — excitement, urgency
  secondary:  '#FFD700',  // gold — prize money, winner
  accent:     '#00DDFF',  // cyan — contrast, pop
  dark:       '#0a0a0a',
  success:    '#00CC44',
  danger:     '#FF2244',
};
```

---

## Challenge Timer / Countdown

The most important visual element — creates pressure and tracks progress.

```tsx
export const ChallengeTimer: React.FC<{
  totalSeconds: number;
  label?: string;
  style?: 'countdown' | 'countup' | 'elapsed';
  accentColor?: string;
  position?: 'top-right' | 'top-left' | 'top-center';
}> = ({
  totalSeconds, label = 'TIME', style = 'countup',
  accentColor = '#FF4500', position = 'top-right',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const elapsed = frame / fps;
  const remaining = Math.max(0, totalSeconds - elapsed);
  const display = style === 'countdown' ? remaining : elapsed;

  const hours   = Math.floor(display / 3600);
  const minutes = Math.floor((display % 3600) / 60);
  const secs    = Math.floor(display % 60);

  const timeStr = hours > 0
    ? `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    : `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  // Pulse on round minutes
  const isPulseFrame = secs === 0 && frame % (fps * 60) < fps * 0.5;
  const pulse = isPulseFrame
    ? spring({ frame: frame % Math.round(fps * 60), fps, config: { damping: 6, stiffness: 500 } })
    : 1;

  const positionStyle: React.CSSProperties = {
    'top-right':  { top: 24, right: 24 },
    'top-left':   { top: 24, left: 24 },
    'top-center': { top: 24, left: '50%', transform: 'translateX(-50%)' },
  }[position] ?? { top: 24, right: 24 };

  return (
    <div style={{
      position: 'absolute',
      ...positionStyle,
      backgroundColor: 'rgba(0,0,0,0.88)',
      border: `2px solid ${accentColor}`,
      borderRadius: 12,
      padding: '10px 20px',
      textAlign: 'center',
      transform: `scale(${isPulseFrame ? pulse : 1})`,
      zIndex: 100,
    }}>
      <div style={{ fontSize: 14, color: accentColor, letterSpacing: 3, textTransform: 'uppercase' }}>
        {label}
      </div>
      <div style={{
        fontSize: 48,
        fontWeight: 900,
        color: remaining < 60 && style === 'countdown' ? '#FF2244' : 'white',
        fontVariantNumeric: 'tabular-nums',
        lineHeight: 1,
      }}>
        {timeStr}
      </div>
    </div>
  );
};
```

---

## Contestant / Participant Cards

```tsx
export const ContestantCard: React.FC<{
  name: string;
  status: 'active' | 'eliminated' | 'winner';
  hours?: number;
  avatarSrc?: string;
  index?: number;
}> = ({ name, status, hours, avatarSrc, index = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 6;
  const appear = spring({ frame: frame - delay, fps, config: { damping: 80 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);

  const statusColor = { active: '#00CC44', eliminated: '#FF2244', winner: '#FFD700' }[status];
  const statusLabel = { active: '✓ IN', eliminated: '✗ OUT', winner: '🏆 WINNER' }[status];

  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 12,
      backgroundColor: status === 'winner' ? 'rgba(255,215,0,0.15)' : 'rgba(0,0,0,0.75)',
      border: `2px solid ${statusColor}`,
      borderRadius: 12, padding: '12px 16px',
      opacity,
      filter: status === 'eliminated' ? 'grayscale(0.7)' : 'none',
    }}>
      {avatarSrc && (
        <Img src={staticFile(avatarSrc)} style={{
          width: 48, height: 48, borderRadius: '50%',
          objectFit: 'cover', border: `2px solid ${statusColor}`,
        }} />
      )}
      <div>
        <div style={{ color: 'white', fontSize: 22, fontWeight: 700 }}>{name}</div>
        {hours !== undefined && (
          <div style={{ color: '#aaa', fontSize: 16 }}>{hours.toFixed(1)}h in</div>
        )}
      </div>
      <div style={{ marginLeft: 'auto', color: statusColor, fontSize: 18, fontWeight: 800 }}>
        {statusLabel}
      </div>
    </div>
  );
};
```

---

## Prize / Stakes Display

The prize must be visual, large, and repeated.

```tsx
export const PrizeDisplay: React.FC<{
  amount: number;
  currency?: string;
  label?: string;
  animate?: boolean;
}> = ({ amount, currency = '$', label = 'PRIZE', animate = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = animate
    ? spring({ frame, fps, config: { damping: 8, stiffness: 400 } })
    : 1;

  // Gold shimmer animation
  const shimmerX = (frame * 3) % 200 - 100;

  return (
    <div style={{
      position: 'relative',
      display: 'inline-flex',
      flexDirection: 'column',
      alignItems: 'center',
      transform: `scale(${scale})`,
    }}>
      <div style={{ fontSize: 24, color: '#FFD700', letterSpacing: 6, fontWeight: 700 }}>
        {label}
      </div>
      <div style={{
        fontSize: 140,
        fontWeight: 900,
        lineHeight: 1,
        background: `linear-gradient(135deg, #FFD700 0%, #FFF8A0 ${50 + shimmerX * 0.3}%, #FFD700 100%)`,
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        textShadow: 'none',
        filter: 'drop-shadow(0 0 20px rgba(255,215,0,0.4))',
      }}>
        {currency}{amount.toLocaleString()}
      </div>
    </div>
  );
};
```

---

## Reaction / Emotion Cutaway

Challenge videos cut to reactions every 30–45 seconds.

```tsx
export const ReactionCutaway: React.FC<{
  reactorVideo?: string;
  reactorImage?: string;
  emotion: 'shock' | 'laugh' | 'pain' | 'triumph' | 'nervous';
  name?: string;
}> = ({ reactorVideo, reactorImage, emotion, name }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Zoom punch in on reaction face
  const zoomScale = spring({ frame, fps, config: { damping: 20, stiffness: 300 } });
  const scale = interpolate(zoomScale, [0, 1], [0.85, 1]);

  // Emoji overlay for emotion
  const emojiMap = {
    shock:   '😱', laugh: '😂', pain: '😭',
    triumph: '🎉', nervous: '😰',
  };

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      {reactorVideo && (
        <OffthreadVideo src={staticFile(reactorVideo)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      )}
      {reactorImage && !reactorVideo && (
        <Img src={staticFile(reactorImage)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      )}

      {/* Emoji pop */}
      <div style={{
        position: 'absolute', top: '8%', right: '8%',
        fontSize: 96,
        transform: `scale(${spring({ frame: frame - 3, fps, config: { damping: 6, stiffness: 500 } })})`,
      }}>
        {emojiMap[emotion]}
      </div>

      {name && (
        <div style={{
          position: 'absolute', bottom: 40, left: 40,
          backgroundColor: 'rgba(0,0,0,0.8)',
          color: 'white', fontSize: 28, fontWeight: 700,
          padding: '8px 20px', borderRadius: 8,
        }}>
          {name}
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Progress / Leaderboard

Shows who's winning — creates investment.

```tsx
export const Leaderboard: React.FC<{
  contestants: Array<{ name: string; score: number; rank: number }>;
  title?: string;
}> = ({ contestants, title = 'STANDINGS' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const sorted = [...contestants].sort((a, b) => b.score - a.score);
  const maxScore = sorted[0]?.score ?? 1;

  return (
    <div style={{
      position: 'absolute', top: 24, left: 24,
      backgroundColor: 'rgba(0,0,0,0.9)',
      border: '2px solid rgba(255,255,255,0.1)',
      borderRadius: 16, padding: '16px 24px',
      minWidth: 320, zIndex: 100,
    }}>
      <div style={{
        fontSize: 16, color: '#FF4500',
        letterSpacing: 4, textTransform: 'uppercase',
        marginBottom: 12, fontWeight: 700,
      }}>
        {title}
      </div>
      {sorted.slice(0, 5).map((c, i) => {
        const barW = spring({ frame: frame - i * 5, fps, config: { damping: 80 } });
        const pct = (c.score / maxScore) * 100;
        return (
          <div key={c.name} style={{ marginBottom: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
              <span style={{ color: 'white', fontSize: 16 }}>
                {i === 0 ? '🏆 ' : `${i + 1}. `}{c.name}
              </span>
              <span style={{ color: '#FFD700', fontSize: 16, fontWeight: 700 }}>
                {c.score.toLocaleString()}
              </span>
            </div>
            <div style={{
              height: 4, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 2,
            }}>
              <div style={{
                height: '100%',
                width: `${interpolate(barW, [0, 1], [0, pct])}%`,
                backgroundColor: i === 0 ? '#FFD700' : '#FF4500',
                borderRadius: 2,
              }} />
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

---

## Winner Reveal Scene

The emotional payoff — the most important moment.

```tsx
export const WinnerReveal: React.FC<{
  name: string;
  prize: string;
  imageSrc?: string;
}> = ({ name, prize, imageSrc }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Everything explodes into frame
  const burst = spring({ frame, fps, config: { damping: 6, stiffness: 500 } });
  const scale = interpolate(burst, [0, 1], [0.3, 1]);

  // Confetti
  const confettiPieces = Array.from({ length: 40 }, (_, i) => ({
    x: 10 + (i * 2.5) % 95,
    startY: -5 - (i * 7) % 30,
    color: ['#FFD700', '#FF4500', '#00DDFF', '#FF69B4', '#00CC44'][i % 5],
    size: 8 + (i % 4) * 4,
    speed: 120 + (i % 5) * 40,
  }));

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505' }}>
      {/* Confetti rain */}
      {confettiPieces.map((p, i) => {
        const y = ((frame * p.speed / fps) + p.startY) % 120;
        return (
          <div key={i} style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: `${y}%`,
            width: p.size, height: p.size,
            backgroundColor: p.color,
            borderRadius: i % 2 === 0 ? '50%' : 2,
            transform: `rotate(${frame * 4 + i * 15}deg)`,
          }} />
        );
      })}

      {/* Winner spotlight */}
      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', gap: 32, flexDirection: 'column' }}>
        <div style={{ fontSize: 48, color: '#FFD700', fontWeight: 900, letterSpacing: 6 }}>
          🏆 WINNER 🏆
        </div>
        <div style={{
          fontSize: 120, fontWeight: 900, color: 'white',
          transform: `scale(${scale})`,
          textShadow: '0 0 60px rgba(255,215,0,0.6)',
        }}>
          {name}
        </div>
        <div style={{ fontSize: 60, color: '#FFD700', fontWeight: 700 }}>
          {prize}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

---

## Challenge Video Structure Template

```tsx
const FPS = 30;
const CHALLENGE_SCENES = [
  // HOOK: State prize + challenge in 5 seconds
  { id: 'hook',       frames: FPS * 5,   type: 'prize-reveal + rule-statement' },
  // SETUP: Introduce contestants, rules
  { id: 'setup',      frames: FPS * 25,  type: 'contestant-cards + leaderboard' },
  // EARLY GAME: Build investment
  { id: 'early',      frames: FPS * 90,  type: 'b-roll + reactions + timer' },
  // COMPLICATION: Someone almost quits / twist
  { id: 'twist',      frames: FPS * 30,  type: 'reaction-cutaway + text-overlay' },
  // RE-HOOK (3 min): Something unexpected
  { id: 're-hook',    frames: FPS * 15,  type: 'text-card: "What happened next..."' },
  // MID GAME: Escalate
  { id: 'midgame',    frames: FPS * 120, type: 'timer + leaderboard updates' },
  // FINAL STRETCH: Tension maximum
  { id: 'finale',     frames: FPS * 60,  type: 'fast-cuts + countdown' },
  // WINNER REVEAL: Payoff
  { id: 'winner',     frames: FPS * 20,  type: 'winner-reveal + confetti' },
  // CTA
  { id: 'cta',        frames: FPS * 10,  type: 'subscribe + next video' },
];
```

---

## Cross-References
- `genres/viral-formula.md` — the hook/escalation/payoff science
- `genres/influencer.md` — zoom punches, jump cuts, text overlays
- `rules/text.md` — bold text overlays on every key moment
- `rules/transitions.md` — fast cuts every 3–7 seconds
- `rules/audio.md` — tension music lifts before reveals
