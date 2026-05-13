# Gaming / Esports Video in Remotion

## Format Overview

Gaming content covers: montages, highlights, esports match intros, player cards, tournament brackets, stream overlays, game trailers, and review/tier-list videos. High energy, RGB aesthetic, sharp transitions, scoreboard graphics.

---

## Gaming Colour Palette

```tsx
export const GAMING_PALETTES = {
  // RGB / cyberpunk — most universal gaming aesthetic
  rgb:      { primary: '#00FF88', secondary: '#FF00AA', accent: '#00AAFF', bg: '#050518' },
  // Esports competitive
  esports:  { primary: '#E5B000', secondary: '#CC0000', accent: '#FFFFFF', bg: '#0a0a0a' },
  // Streaming / Twitch
  twitch:   { primary: '#9147FF', secondary: '#00B8D4', accent: '#FFFFFF', bg: '#0e0e10' },
  // Dark fantasy (RPG, WoW)
  fantasy:  { primary: '#8B4513', secondary: '#4B0082', accent: '#FFD700', bg: '#0d0d1a' },
  // FPS / tactical
  tactical: { primary: '#00E5FF', secondary: '#FF6600', accent: '#FFFFFF', bg: '#0a0f0a' },
};
```

---

## Player Card / Character Reveal

```tsx
export const PlayerCard: React.FC<{
  playerName: string;
  gamertag?: string;
  role?: string;
  team?: string;
  imageSrc?: string;
  accentColor?: string;
  stats?: Array<{ label: string; value: string }>;
}> = ({
  playerName, gamertag, role, team, imageSrc,
  accentColor = '#00FF88',
  stats = [],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dramatic entrance
  const slideUp = spring({ frame, fps, config: { damping: 12, stiffness: 300 } });
  const cardY = interpolate(slideUp, [0, 1], [200, 0]);

  // Scan line effect on reveal
  const scanOpacity = interpolate(frame, [0, fps * 0.3, fps * 0.6], [0.8, 0.3, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      <div style={{
        transform: `translateY(${cardY}px)`,
        position: 'relative',
        width: 520,
      }}>
        {/* Glow behind card */}
        <div style={{
          position: 'absolute', inset: -20,
          borderRadius: 24,
          background: `radial-gradient(ellipse, ${accentColor}30, transparent 70%)`,
          filter: 'blur(20px)',
        }} />

        {/* Card */}
        <div style={{
          backgroundColor: 'rgba(5,5,24,0.95)',
          border: `1px solid ${accentColor}60`,
          borderRadius: 16,
          overflow: 'hidden',
          boxShadow: `0 0 40px ${accentColor}30`,
        }}>
          {/* Accent header bar */}
          <div style={{ height: 4, backgroundColor: accentColor }} />

          {/* Player image */}
          {imageSrc && (
            <div style={{ position: 'relative', height: 280 }}>
              <Img src={staticFile(imageSrc)}
                style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              {/* Scan line reveal */}
              <div style={{
                position: 'absolute', inset: 0,
                background: `linear-gradient(to bottom, transparent ${(1 - scanOpacity) * 100}%, ${accentColor}44 ${(1 - scanOpacity) * 100}%, transparent)`,
              }} />
            </div>
          )}

          {/* Player info */}
          <div style={{ padding: 24 }}>
            {gamertag && (
              <div style={{ color: accentColor, fontSize: 14, letterSpacing: 4, fontWeight: 700, textTransform: 'uppercase' }}>
                {gamertag}
              </div>
            )}
            <div style={{ color: 'white', fontSize: 48, fontWeight: 900, lineHeight: 1.1, margin: '4px 0' }}>
              {playerName}
            </div>
            {role && <div style={{ color: '#888', fontSize: 20 }}>{role} {team ? `· ${team}` : ''}</div>}

            {/* Stats */}
            {stats.length > 0 && (
              <div style={{
                display: 'flex', gap: 16, marginTop: 20,
                borderTop: `1px solid rgba(255,255,255,0.08)`, paddingTop: 16,
              }}>
                {stats.map((s, i) => (
                  <div key={i} style={{ flex: 1, textAlign: 'center' }}>
                    <div style={{ color: accentColor, fontSize: 28, fontWeight: 900 }}>{s.value}</div>
                    <div style={{ color: '#666', fontSize: 14, textTransform: 'uppercase', letterSpacing: 2 }}>{s.label}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

---

## Tournament Bracket Display

```tsx
export const TournamentBracket: React.FC<{
  matches: Array<{
    round: number;
    team1: string; score1?: number;
    team2: string; score2?: number;
    winner?: 1 | 2;
  }>;
  title?: string;
  accentColor?: string;
}> = ({ matches, title = 'BRACKET', accentColor = '#E5B000' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const rounds = [...new Set(matches.map(m => m.round))].sort();

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', padding: 60 }}>
      {title && (
        <div style={{
          color: accentColor, fontSize: 28, fontWeight: 900,
          letterSpacing: 6, textTransform: 'uppercase', marginBottom: 40,
        }}>
          {title}
        </div>
      )}

      <div style={{ display: 'flex', gap: 60, alignItems: 'center' }}>
        {rounds.map((round) => (
          <div key={round} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <div style={{ color: '#666', fontSize: 14, letterSpacing: 3, textTransform: 'uppercase', marginBottom: 8 }}>
              Round {round}
            </div>
            {matches.filter(m => m.round === round).map((match, i) => {
              const delay = round * 8 + i * 5;
              const appear = spring({ frame: frame - delay, fps, config: { damping: 80 } });
              const opacity = interpolate(appear, [0, 0.5], [0, 1]);

              return (
                <div key={i} style={{
                  backgroundColor: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 8, overflow: 'hidden',
                  opacity, minWidth: 220,
                }}>
                  {[
                    { name: match.team1, score: match.score1, won: match.winner === 1 },
                    { name: match.team2, score: match.score2, won: match.winner === 2 },
                  ].map((team, j) => (
                    <div key={j} style={{
                      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                      padding: '10px 16px',
                      backgroundColor: team.won ? `${accentColor}18` : 'transparent',
                      borderBottom: j === 0 ? '1px solid rgba(255,255,255,0.08)' : 'none',
                    }}>
                      <span style={{
                        color: team.won ? 'white' : '#666',
                        fontSize: 20, fontWeight: team.won ? 700 : 400,
                      }}>
                        {team.name}
                      </span>
                      {team.score !== undefined && (
                        <span style={{
                          color: team.won ? accentColor : '#444',
                          fontSize: 22, fontWeight: 900,
                        }}>
                          {team.score}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

---

## Kill Feed / Event Notification

```tsx
export const KillFeedItem: React.FC<{
  killer: string;
  victim: string;
  weapon?: string;
  index?: number;
}> = ({ killer, victim, weapon = '⚔️', index = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const delay = index * 10;
  const slideIn = spring({ frame: frame - delay, fps, config: { damping: 60, stiffness: 200 } });
  const x = interpolate(slideIn, [0, 1], [400, 0]);

  const holdEnd = delay + fps * 3;
  const fadeOut = interpolate(frame, [holdEnd, holdEnd + 20], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 10,
      backgroundColor: 'rgba(0,0,0,0.82)',
      border: '1px solid rgba(255,255,255,0.12)',
      borderRadius: 6, padding: '8px 16px',
      transform: `translateX(${x}px)`,
      opacity: fadeOut,
    }}>
      <span style={{ color: '#00FF88', fontWeight: 700, fontSize: 20 }}>{killer}</span>
      <span style={{ fontSize: 20 }}>{weapon}</span>
      <span style={{ color: '#FF4444', fontWeight: 700, fontSize: 20, textDecoration: 'line-through' }}>
        {victim}
      </span>
    </div>
  );
};
```

---

## Tier List / Ranking Card

```tsx
type Tier = 'S' | 'A' | 'B' | 'C' | 'D' | 'F';

export const TierList: React.FC<{
  items: Array<{ tier: Tier; name: string; imageSrc?: string }>;
  title?: string;
}> = ({ items, title = 'TIER LIST' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const TIER_COLORS: Record<Tier, string> = {
    S: '#FF4444', A: '#FF9944', B: '#FFEE44',
    C: '#44FF88', D: '#4488FF', F: '#AA44FF',
  };

  const tiers = ['S', 'A', 'B', 'C', 'D', 'F'] as Tier[];

  return (
    <AbsoluteFill style={{ backgroundColor: '#111', padding: 60, flexDirection: 'column', gap: 4 }}>
      <div style={{ color: 'white', fontSize: 36, fontWeight: 900, marginBottom: 20 }}>{title}</div>
      {tiers.map((tier, ti) => {
        const tierItems = items.filter(i => i.tier === tier);
        if (tierItems.length === 0) return null;

        const delay = ti * 8;
        const appear = spring({ frame: frame - delay, fps, config: { damping: 70 } });

        return (
          <div key={tier} style={{
            display: 'flex', alignItems: 'center',
            opacity: interpolate(appear, [0, 0.5], [0, 1]),
            transform: `translateX(${interpolate(appear, [0, 1], [-40, 0])}px)`,
            borderBottom: '1px solid rgba(255,255,255,0.06)',
          }}>
            {/* Tier label */}
            <div style={{
              width: 72, height: 60,
              backgroundColor: TIER_COLORS[tier],
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 36, fontWeight: 900, color: 'white',
              flexShrink: 0,
            }}>
              {tier}
            </div>

            {/* Items */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, padding: '4px 8px', flex: 1 }}>
              {tierItems.map((item, i) => (
                <div key={i} style={{
                  backgroundColor: 'rgba(255,255,255,0.08)',
                  color: 'white', fontSize: 20, fontWeight: 600,
                  padding: '6px 16px', borderRadius: 4,
                }}>
                  {item.name}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
```

---

## RGB Glow Effect

```tsx
// Apply to any element for gaming RGB glow
export const RGBGlow: React.FC<{ children: React.ReactNode; speed?: number }> = ({
  children, speed = 1,
}) => {
  const frame = useCurrentFrame();

  const hue = (frame * speed * 2) % 360;
  const glowColor = `hsl(${hue}, 100%, 60%)`;

  return (
    <div style={{
      filter: `drop-shadow(0 0 12px ${glowColor}) drop-shadow(0 0 4px ${glowColor})`,
    }}>
      {children}
    </div>
  );
};
```

---

## Cross-References
- `genres/influencer.md` — short-form clip formats, zoom punches
- `genres/mv.md` — BPM sync for montage beat drops
- `rules/3d.md` — Three.js for 3D game element rendering
- `rules/effects.md` — CameraMotionBlur for high-speed gameplay
- `rules/transitions.md` — smash cuts for highlight reels
