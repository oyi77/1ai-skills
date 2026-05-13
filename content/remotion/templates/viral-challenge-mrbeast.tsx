// ============================================================
// VIRAL CHALLENGE TEMPLATE — MrBeast Style
// Structure: Hook → Setup → Escalation → Re-hook → Payoff
// Format: 16:9 1080p, 8 minutes
// Requires: @remotion/google-fonts @remotion/noise
// Customize: CHALLENGE_*, PRIZE_*, CONTESTANTS
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Audio, staticFile,
  Img, Easing,
} from 'remotion';
import { noise2D } from '@remotion/noise';
import { loadFont as loadOswald } from '@remotion/google-fonts/Oswald';

const { fontFamily: OSWALD } = loadOswald();

// ── CUSTOMIZE ──────────────────────────────────────────────
const CHALLENGE_TITLE = 'LAST TO LEAVE WINS $10,000';
const CHALLENGE_RULE  = 'Stay inside the circle. Winner takes all.';
const PRIZE_AMOUNT    = 10000;
const PRIZE_CURRENCY  = '$';
const TOTAL_HOURS     = 24;

const CONTESTANTS = [
  { id: 'p1', name: 'Alex',   color: '#FF4500', imageSrc: 'contestants/alex.png',   eliminatedAtSec: -1 },
  { id: 'p2', name: 'Priya',  color: '#00AAFF', imageSrc: 'contestants/priya.png',  eliminatedAtSec: 180 },
  { id: 'p3', name: 'Marcus', color: '#00CC44', imageSrc: 'contestants/marcus.png', eliminatedAtSec: 300 },
  { id: 'p4', name: 'Yuki',   color: '#FFD700', imageSrc: 'contestants/yuki.png',   eliminatedAtSec: -1 },
];

// Section timing (seconds)
const T = {
  hook:        { start: 0,   end: 8   },  // Prize + challenge stated
  setup:       { start: 8,   end: 40  },  // Intro contestants
  early:       { start: 40,  end: 180 },  // First eliminations
  midgame:     { start: 180, end: 360 },  // Escalation
  rehook:      { start: 360, end: 375 },  // "You won't believe what happened"
  finale:      { start: 375, end: 450 },  // Final two, max tension
  winner:      { start: 450, end: 475 },  // Winner reveal
  cta:         { start: 475, end: 480 },  // Subscribe
};

const FPS = 30;
const sec = (s: number) => Math.round(s * FPS);
// ───────────────────────────────────────────────────────────

const ACCENT = '#FF4500';
const GOLD   = '#FFD700';

// Animated challenge timer
const Timer: React.FC<{ totalSec: number; startSec: number }> = ({ totalSec, startSec }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const elapsed = frame / fps + startSec;
  const display = Math.min(elapsed, totalSec * 3600);

  const h = Math.floor(display / 3600);
  const m = Math.floor((display % 3600) / 60);
  const s = Math.floor(display % 60);

  const fmt = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;

  // Pulse every minute
  const pulseFrame = frame % Math.round(fps * 60);
  const pulse = pulseFrame < 10
    ? spring({ frame: pulseFrame, fps, config: { damping: 6, stiffness: 500 } })
    : 1;

  return (
    <div style={{
      position: 'absolute', top: 24, right: 24,
      backgroundColor: 'rgba(0,0,0,0.9)',
      border: `2px solid ${ACCENT}`,
      borderRadius: 12, padding: '10px 20px',
      textAlign: 'center',
      transform: `scale(${pulse})`,
      zIndex: 100,
    }}>
      <div style={{ fontSize: 12, color: ACCENT, letterSpacing: 4, fontFamily: OSWALD }}>ELAPSED</div>
      <div style={{
        fontSize: 52, fontWeight: 900, color: 'white',
        fontVariantNumeric: 'tabular-nums', fontFamily: OSWALD,
      }}>
        {fmt}
      </div>
    </div>
  );
};

// Contestant status card
const ContestantGrid: React.FC<{
  contestants: typeof CONTESTANTS;
  currentSec: number;
}> = ({ contestants, currentSec }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{
      position: 'absolute', top: 24, left: 24,
      display: 'flex', flexDirection: 'column', gap: 8,
      zIndex: 100,
    }}>
      {contestants.map((c, i) => {
        const eliminated = c.eliminatedAtSec > 0 && currentSec >= c.eliminatedAtSec;
        const delay = i * 6;
        const appear = spring({ frame: frame - delay, fps, config: { damping: 80 } });

        return (
          <div key={c.id} style={{
            display: 'flex', alignItems: 'center', gap: 10,
            backgroundColor: eliminated ? 'rgba(0,0,0,0.6)' : 'rgba(0,0,0,0.85)',
            border: `2px solid ${eliminated ? '#333' : c.color}`,
            borderRadius: 10, padding: '8px 14px',
            filter: eliminated ? 'grayscale(0.8)' : 'none',
            opacity: interpolate(appear, [0, 0.4], [0, 1]),
            transform: `translateX(${interpolate(appear, [0, 1], [-200, 0])}px)`,
            minWidth: 200,
          }}>
            <div style={{
              width: 10, height: 10, borderRadius: '50%',
              backgroundColor: eliminated ? '#333' : c.color,
            }} />
            <span style={{ color: eliminated ? '#555' : 'white', fontSize: 20, fontWeight: 700, fontFamily: OSWALD }}>
              {c.name}
            </span>
            <span style={{
              marginLeft: 'auto',
              color: eliminated ? '#FF2244' : c.color,
              fontSize: 16, fontWeight: 900, fontFamily: OSWALD,
            }}>
              {eliminated ? '✗ OUT' : '✓ IN'}
            </span>
          </div>
        );
      })}
    </div>
  );
};

// Prize display
const PrizeDisplay: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 6, stiffness: 500 } });
  const shimX = (frame * 3) % 200 - 100;

  return (
    <AbsoluteFill style={{
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 12,
    }}>
      <div style={{ fontSize: 28, color: GOLD, fontWeight: 900, letterSpacing: 6, fontFamily: OSWALD }}>
        GRAND PRIZE
      </div>
      <div style={{
        fontSize: 160, fontWeight: 900, lineHeight: 1,
        background: `linear-gradient(135deg, ${GOLD} 0%, #FFF8A0 ${50 + shimX * 0.3}%, ${GOLD} 100%)`,
        WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
        filter: `drop-shadow(0 0 30px rgba(255,215,0,0.5))`,
        transform: `scale(${scale})`,
        fontFamily: OSWALD,
      }}>
        {PRIZE_CURRENCY}{PRIZE_AMOUNT.toLocaleString()}
      </div>
      <div style={{ fontSize: 36, color: '#fff', fontFamily: OSWALD, letterSpacing: 4 }}>
        {CHALLENGE_RULE}
      </div>
    </AbsoluteFill>
  );
};

// Hook section
const HookScene: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleScale = spring({ frame: frame - 4, fps, config: { damping: 8, stiffness: 400 } });
  const titleOpacity = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505' }}>
      <AbsoluteFill style={{ opacity: titleOpacity, transform: `scale(${titleScale})` }}>
        <div style={{
          position: 'absolute', inset: 0,
          display: 'flex', flexDirection: 'column',
          justifyContent: 'center', alignItems: 'center', gap: 24,
        }}>
          <div style={{
            backgroundColor: ACCENT, color: 'white',
            fontSize: 28, fontWeight: 900, fontFamily: OSWALD,
            padding: '8px 32px', borderRadius: 999, letterSpacing: 4,
          }}>
            CHALLENGE
          </div>
          <h1 style={{
            fontSize: 100, fontFamily: OSWALD, color: 'white',
            margin: 0, textAlign: 'center',
            textShadow: `4px 4px 0 ${ACCENT}`,
            letterSpacing: 2, maxWidth: 1400, lineHeight: 1.1,
          }}>
            {CHALLENGE_TITLE}
          </h1>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Re-hook text card ("What happens next...")
const ReHookCard: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const appear  = spring({ frame, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.4], [0, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#000',
      justifyContent: 'center', alignItems: 'center',
      flexDirection: 'column', gap: 20, opacity,
    }}>
      <div style={{ fontSize: 28, color: ACCENT, fontFamily: OSWALD, letterSpacing: 6 }}>BUT THEN...</div>
      <h2 style={{
        fontSize: 80, color: 'white', fontFamily: OSWALD,
        textAlign: 'center', margin: 0, maxWidth: 1400,
      }}>
        Something nobody expected happened.
      </h2>
    </AbsoluteFill>
  );
};

// Winner reveal
const WinnerReveal: React.FC<{ winnerName: string }> = ({ winnerName }) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const burst = spring({ frame, fps, config: { damping: 5, stiffness: 600 } });
  const scale = interpolate(burst, [0, 1], [0.2, 1]);

  const confetti = Array.from({ length: 50 }, (_, i) => ({
    x: 5 + (i * 1.9) % 92,
    y: ((frame * (80 + (i % 5) * 30) / fps) + (i * 8) % 20) % 110,
    color: [GOLD, ACCENT, '#00AAFF', '#FF69B4', '#00CC44'][i % 5],
    size: 8 + (i % 4) * 4,
  }));

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505' }}>
      {confetti.map((p, i) => (
        <div key={i} style={{
          position: 'absolute', left: `${p.x}%`, top: `${p.y}%`,
          width: p.size, height: p.size,
          backgroundColor: p.color,
          borderRadius: i % 2 === 0 ? '50%' : 2,
          transform: `rotate(${frame * 5 + i * 18}deg)`,
        }} />
      ))}

      <AbsoluteFill style={{
        justifyContent: 'center', alignItems: 'center',
        flexDirection: 'column', gap: 24,
        transform: `scale(${scale})`,
      }}>
        <div style={{ fontSize: 60, color: GOLD, fontFamily: OSWALD, letterSpacing: 6 }}>🏆 WINNER 🏆</div>
        <div style={{
          fontSize: 140, fontWeight: 900, color: 'white',
          fontFamily: OSWALD,
          textShadow: `0 0 60px ${GOLD}`,
        }}>
          {winnerName}
        </div>
        <div style={{ fontSize: 56, color: GOLD, fontFamily: OSWALD }}>
          {PRIZE_CURRENCY}{PRIZE_AMOUNT.toLocaleString()}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const ViralChallenge: React.FC = () => {
  const winner = CONTESTANTS.find(c => c.eliminatedAtSec < 0) ?? CONTESTANTS[0];

  return (
    <AbsoluteFill style={{ backgroundColor: '#080808' }}>

      {/* HOOK: Prize reveal */}
      <Sequence from={sec(T.hook.start)} durationInFrames={sec(T.hook.end - T.hook.start)}>
        <HookScene />
      </Sequence>

      {/* SETUP: Contestant intros + prize */}
      <Sequence from={sec(T.setup.start)} durationInFrames={sec(T.setup.end - T.setup.start)}>
        <AbsoluteFill style={{ backgroundColor: '#050505' }}>
          <PrizeDisplay />
          <ContestantGrid contestants={CONTESTANTS} currentSec={0} />
        </AbsoluteFill>
      </Sequence>

      {/* EARLY GAME */}
      <Sequence from={sec(T.early.start)} durationInFrames={sec(T.early.end - T.early.start)}>
        <AbsoluteFill style={{ backgroundColor: '#080808' }}>
          {/* Replace with actual footage */}
          <div style={{
            position: 'absolute', inset: 0,
            background: 'linear-gradient(135deg, #080810 0%, #100808 100%)',
          }} />
          <ContestantGrid contestants={CONTESTANTS} currentSec={T.early.start} />
          <Timer totalSec={TOTAL_HOURS} startSec={0} />
        </AbsoluteFill>
      </Sequence>

      {/* MID GAME */}
      <Sequence from={sec(T.midgame.start)} durationInFrames={sec(T.midgame.end - T.midgame.start)}>
        <AbsoluteFill style={{ backgroundColor: '#080808' }}>
          <ContestantGrid contestants={CONTESTANTS} currentSec={T.midgame.start} />
          <Timer totalSec={TOTAL_HOURS} startSec={T.midgame.start} />
        </AbsoluteFill>
      </Sequence>

      {/* RE-HOOK */}
      <Sequence from={sec(T.rehook.start)} durationInFrames={sec(T.rehook.end - T.rehook.start)}>
        <ReHookCard />
      </Sequence>

      {/* FINALE */}
      <Sequence from={sec(T.finale.start)} durationInFrames={sec(T.finale.end - T.finale.start)}>
        <AbsoluteFill style={{ backgroundColor: '#050505' }}>
          <ContestantGrid
            contestants={CONTESTANTS.filter(c => c.eliminatedAtSec < 0)}
            currentSec={T.finale.start}
          />
          <Timer totalSec={TOTAL_HOURS} startSec={T.finale.start} />
          {/* Tension indicator */}
          <div style={{
            position: 'absolute', bottom: 0, left: 0, right: 0, height: 6,
            background: `linear-gradient(90deg, ${ACCENT}, ${GOLD})`,
            boxShadow: `0 0 20px ${ACCENT}`,
          }} />
        </AbsoluteFill>
      </Sequence>

      {/* WINNER */}
      <Sequence from={sec(T.winner.start)} durationInFrames={sec(T.winner.end - T.winner.start)}>
        <WinnerReveal winnerName={winner.name} />
      </Sequence>

      {/* CTA */}
      <Sequence from={sec(T.cta.start)} durationInFrames={sec(T.cta.end - T.cta.start)}>
        <AbsoluteFill style={{
          backgroundColor: '#000',
          justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 16,
        }}>
          <div style={{ fontSize: 80, fontFamily: OSWALD, color: 'white', fontWeight: 900 }}>SUBSCRIBE</div>
          <div style={{ fontSize: 36, fontFamily: OSWALD, color: '#888' }}>
            for more challenges like this
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  return (
    <Composition
      id="ViralChallenge"
      component={ViralChallenge}
      durationInFrames={sec(T.cta.end)}
      fps={FPS}
      width={1920}
      height={1080}
    />
  );
};
