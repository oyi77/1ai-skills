// ============================================================
// VIRAL CHALLENGE / GAME SHOW TEMPLATE
// Style: MrBeast-inspired — prize reveal, timer, contestant cards
// Format: 16:9 1080p, scalable duration
// Customize: CHALLENGE_*, PRIZE_*, CONTESTANTS, ACCENT
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence,
  useCurrentFrame, useVideoConfig,
  interpolate, spring,
} from 'remotion';
import { noise2D } from '@remotion/noise';

// ── CONFIG ───────────────────────────────────────────────────
const CHALLENGE_TITLE = 'LAST TO LEAVE WINS';
const CHALLENGE_RULE  = 'Siapa yang bertahan paling lama dapat hadiahnya!';
const PRIZE_AMOUNT    = 10_000_000;
const PRIZE_CURRENCY  = 'Rp ';
const ACCENT          = '#FF4500';
const GOLD            = '#FFD700';

// Contestants: update status as challenge progresses
const CONTESTANTS: Array<{
  name: string;
  status: 'active' | 'eliminated' | 'winner';
  duration?: string;  // e.g. '4.5h'
}> = [
  { name: 'Budi',    status: 'active',     duration: '6h' },
  { name: 'Sari',    status: 'eliminated', duration: '2.1h' },
  { name: 'Adi',     status: 'active',     duration: '6h' },
  { name: 'Maya',    status: 'eliminated', duration: '3.8h' },
  { name: 'Rizky',   status: 'winner',     duration: '6h' },
];

const WINNER_NAME = 'Rizky';

const FPS      = 30;
const DURATION = FPS * 90;

const T = {
  HOOK:       { from: 0,        dur: FPS * 8  },
  CONTESTANT: { from: FPS * 8,  dur: FPS * 20 },
  MIDGAME:    { from: FPS * 28, dur: FPS * 30 },
  TENSION:    { from: FPS * 58, dur: FPS * 12 },
  WINNER:     { from: FPS * 70, dur: FPS * 20 },
};

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="ChallengeVideo"
    component={ChallengeVideo}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const ChallengeVideo: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#050505' }}>

    <Sequence from={T.HOOK.from}       durationInFrames={T.HOOK.dur}>
      <HookScene />
    </Sequence>
    <Sequence from={T.CONTESTANT.from} durationInFrames={T.CONTESTANT.dur}>
      <ContestantRevealScene />
    </Sequence>
    <Sequence from={T.MIDGAME.from}    durationInFrames={T.MIDGAME.dur}>
      <MidgameScene />
    </Sequence>
    <Sequence from={T.TENSION.from}    durationInFrames={T.TENSION.dur}>
      <TensionScene />
    </Sequence>
    <Sequence from={T.WINNER.from}     durationInFrames={T.WINNER.dur}>
      <WinnerRevealScene />
    </Sequence>

  </AbsoluteFill>
);

// ── HOOK SCENE ───────────────────────────────────────────────
const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleScale = spring({ frame, fps, config: { damping: 8, stiffness: 400 } });
  const prizeScale = spring({ frame: frame - fps * 0.8, fps, config: { damping: 6, stiffness: 300 } });

  // Gold shimmer
  const shimmer = ((frame * 4) % 200) - 100;

  return (
    <AbsoluteFill style={{
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 24,
      background: 'radial-gradient(ellipse at 50% 50%, #1a0500, #050505)',
    }}>
      {/* Challenge title */}
      <div style={{
        fontSize: 100, fontWeight: 900, color: 'white',
        transform: `scale(${titleScale})`,
        textShadow: `0 0 40px ${ACCENT}88`,
        letterSpacing: 6, textAlign: 'center',
      }}>
        {CHALLENGE_TITLE}
      </div>

      {/* Prize */}
      <div style={{
        transform: `scale(${prizeScale})`,
        textAlign: 'center',
      }}>
        <div style={{ fontSize: 32, color: '#aaa', letterSpacing: 4, textTransform: 'uppercase' }}>
          HADIAH
        </div>
        <div style={{
          fontSize: 140, fontWeight: 900, lineHeight: 1,
          background: `linear-gradient(135deg, ${GOLD} 0%, #fff8a0 ${50 + shimmer * 0.2}%, ${GOLD} 100%)`,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          filter: `drop-shadow(0 0 24px ${GOLD}66)`,
        }}>
          {PRIZE_CURRENCY}{PRIZE_AMOUNT.toLocaleString('id-ID')}
        </div>
      </div>

      {/* Rule */}
      <div style={{
        fontSize: 32, color: '#888', textAlign: 'center',
        opacity: interpolate(frame, [fps * 1.5, fps * 2.5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        maxWidth: 1000,
      }}>
        {CHALLENGE_RULE}
      </div>
    </AbsoluteFill>
  );
};

// ── CONTESTANT REVEAL SCENE ──────────────────────────────────
const ContestantRevealScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const activeContestants = CONTESTANTS.filter(c => c.status !== 'winner' || true);

  return (
    <AbsoluteFill style={{ padding: '60px 100px' }}>
      <div style={{ color: ACCENT, fontSize: 28, fontWeight: 700, letterSpacing: 4, textTransform: 'uppercase', marginBottom: 40 }}>
        PESERTA ({CONTESTANTS.length} orang)
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {activeContestants.map((c, i) => {
          const delay  = i * 8;
          const appear = spring({ frame: frame - delay, fps, config: { damping: 70 } });
          const x      = interpolate(appear, [0, 1], [-200, 0]);
          const opacity = interpolate(appear, [0, 0.5], [0, 1]);
          const statusColor = { active: '#00CC44', eliminated: '#FF2244', winner: GOLD }[c.status];
          const statusLabel = { active: '✓ AKTIF', eliminated: '✗ GUGUR', winner: '🏆 JUARA' }[c.status];

          return (
            <div key={c.name} style={{
              display: 'flex', alignItems: 'center', gap: 20,
              backgroundColor: c.status === 'winner' ? `${GOLD}18` : 'rgba(255,255,255,0.05)',
              border: `2px solid ${statusColor}`,
              borderRadius: 12, padding: '16px 24px',
              transform: `translateX(${x}px)`, opacity,
              filter: c.status === 'eliminated' ? 'grayscale(0.6)' : 'none',
            }}>
              <div style={{
                width: 52, height: 52, borderRadius: '50%',
                backgroundColor: statusColor,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 24, fontWeight: 900, color: '#000',
                flexShrink: 0,
              }}>
                {i + 1}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ color: 'white', fontSize: 28, fontWeight: 700 }}>{c.name}</div>
                {c.duration && <div style={{ color: '#888', fontSize: 18 }}>{c.duration} bertahan</div>}
              </div>
              <div style={{ color: statusColor, fontSize: 22, fontWeight: 900 }}>
                {statusLabel}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ── MIDGAME SCENE ────────────────────────────────────────────
const MidgameScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Clock ticking
  const elapsedSeconds = frame / fps;
  const hours   = Math.floor(elapsedSeconds / 3600);
  const minutes = Math.floor((elapsedSeconds % 3600) / 60);
  const secs    = Math.floor(elapsedSeconds % 60);
  const timeStr = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  // Countdown pulses every second
  const secPhase = (frame % fps) / fps;
  const pulse    = Math.max(0, 1 - secPhase * 3) * 0.15;

  const activeCount = CONTESTANTS.filter(c => c.status === 'active').length;

  return (
    <AbsoluteFill style={{
      backgroundColor: '#050505',
      background: `radial-gradient(ellipse at 50% 30%, rgba(255,69,0,${pulse}), #050505)`,
      justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 40,
    }}>
      {/* Timer */}
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.9)',
        border: `2px solid ${ACCENT}`,
        borderRadius: 16, padding: '20px 48px',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: 20, color: ACCENT, letterSpacing: 4, textTransform: 'uppercase', marginBottom: 8 }}>
          WAKTU BERLANGSUNG
        </div>
        <div style={{ fontSize: 96, fontWeight: 900, color: 'white', fontVariantNumeric: 'tabular-nums', letterSpacing: 4 }}>
          {timeStr}
        </div>
      </div>

      {/* Remaining count */}
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: 56, fontWeight: 900, color: ACCENT }}>{activeCount}</div>
        <div style={{ fontSize: 24, color: '#888', letterSpacing: 4, textTransform: 'uppercase' }}>
          Peserta Tersisa
        </div>
      </div>

      {/* Tension text */}
      <div style={{
        fontSize: 32, color: '#555', textAlign: 'center',
        opacity: Math.sin(frame * 0.08) * 0.5 + 0.5,
      }}>
        Siapa yang akan menyerah selanjutnya?
      </div>
    </AbsoluteFill>
  );
};

// ── TENSION SCENE ────────────────────────────────────────────
const TensionScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Red flashing urgency
  const flashOpacity = Math.max(0, Math.sin(frame * 0.4) * 0.12);

  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
      {/* Red pulse bg */}
      <AbsoluteFill style={{ backgroundColor: '#FF0000', opacity: flashOpacity }} />

      <div style={{ textAlign: 'center', zIndex: 10 }}>
        <div style={{
          fontSize: 96, fontWeight: 900, color: 'white',
          textShadow: '0 0 30px rgba(255,0,0,0.8)',
          letterSpacing: 4,
        }}>
          ⚡ SIAPA YANG MENANG?
        </div>
        <div style={{ fontSize: 36, color: '#FF4500', marginTop: 16, fontWeight: 600 }}>
          Terus tonton sampai habis...
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── WINNER REVEAL SCENE ──────────────────────────────────────
const WinnerRevealScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const nameScale  = spring({ frame, fps, config: { damping: 6, stiffness: 400 } });
  const prizeScale = spring({ frame: frame - fps * 0.8, fps, config: { damping: 8, stiffness: 300 } });

  // Confetti
  const confetti = Array.from({ length: 50 }, (_, i) => ({
    x: (i * 2.1) % 100,
    speed: 80 + (i % 7) * 30,
    color: [GOLD, ACCENT, '#00DDFF', '#FF69B4', '#00CC44'][i % 5],
    size: 8 + (i % 4) * 4,
    startOffset: (i * 17) % 40,
  }));

  return (
    <AbsoluteFill style={{ backgroundColor: '#050505' }}>
      {/* Confetti */}
      {confetti.map((c, i) => {
        const y = ((frame * c.speed / fps) + c.startOffset) % 120;
        return (
          <div key={i} style={{
            position: 'absolute',
            left: `${c.x}%`, top: `${y}%`,
            width: c.size, height: c.size,
            backgroundColor: c.color,
            borderRadius: i % 2 === 0 ? '50%' : 3,
            transform: `rotate(${frame * 4 + i * 20}deg)`,
            opacity: 0.8,
          }} />
        );
      })}

      {/* Winner announcement */}
      <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 20, zIndex: 10 }}>
        <div style={{ fontSize: 48, color: GOLD, fontWeight: 900, letterSpacing: 6 }}>
          🏆 PEMENANG 🏆
        </div>
        <div style={{
          fontSize: 140, fontWeight: 900, color: 'white',
          transform: `scale(${nameScale})`,
          textShadow: `0 0 60px ${GOLD}88`,
        }}>
          {WINNER_NAME}
        </div>
        <div style={{
          transform: `scale(${prizeScale})`,
          textAlign: 'center',
        }}>
          <div style={{
            fontSize: 80, fontWeight: 900,
            background: `linear-gradient(135deg, ${GOLD}, #fff8a0, ${GOLD})`,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>
            {PRIZE_CURRENCY}{PRIZE_AMOUNT.toLocaleString('id-ID')}
          </div>
          <div style={{ color: '#888', fontSize: 28, marginTop: 8, letterSpacing: 4 }}>
            BAWA PULANG!
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
