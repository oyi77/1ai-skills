// ============================================================
// COMEDY / MEME / POV SHORT-FORM TEMPLATE
// Style: High-share comedy — setup/pause/punchline structure
// Format: 9:16 vertical (TikTok/Reels) OR 16:9, 30–60 seconds
// Requires: @remotion/google-fonts
// Customize: COMEDY_TYPE, SETUP_TEXT, PUNCHLINE, scenes
// ============================================================

import React from 'react';
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Sequence, Freeze, Easing,
  Audio, staticFile, Img, OffthreadVideo,
} from 'remotion';
import { loadFont as loadOswald } from '@remotion/google-fonts/Oswald';
import { loadFont as loadInter }  from '@remotion/google-fonts/Inter';

const { fontFamily: OSWALD } = loadOswald();
const { fontFamily: INTER }  = loadInter();

// ── CUSTOMIZE ──────────────────────────────────────────────
// Choose your comedy format:
type ComedyFormat = 'pov' | 'when' | 'nobody' | 'comparison' | 'expectation-vs-reality';
const FORMAT: ComedyFormat = 'pov';

// Text content
const SETUP_TEXT     = 'You just launched your product for the first time';
const PUNCHLINE_TEXT = '2 sales. Both from your mum. 😭';
const REACTION_EMOJI = '💀';

// Visual sources (replace with your footage)
const SETUP_SRC     = '';   // path to setup image/video in public/
const PUNCHLINE_SRC = '';   // path to punchline image/video in public/

// Comparison mode (format === 'comparison')
const LEFT_LABEL  = 'Expectation';
const RIGHT_LABEL = 'Reality';
const LEFT_SRC    = '';
const RIGHT_SRC   = '';

// Colours
const ACCENT = '#FFE000';  // yellow — classic meme energy
const WIDTH  = 1080;
const HEIGHT = 1920;  // change to 1920/1080 for landscape

const FPS = 30;
const s   = (sec: number) => Math.round(sec * FPS);
// ───────────────────────────────────────────────────────────

// Impact-style meme text
const MemeText: React.FC<{
  text: string;
  position?: 'top' | 'bottom' | 'center';
  color?: string;
  fontSize?: number;
}> = ({ text, position = 'top', color = 'white', fontSize = HEIGHT > 1200 ? 80 : 64 }) => {
  const strokeShadow = [
    '-4px -4px 0 #000', '4px -4px 0 #000',
    '-4px 4px 0 #000',  '4px 4px 0 #000',
    '-4px 0 0 #000',    '4px 0 0 #000',
    '0 -4px 0 #000',    '0 4px 0 #000',
  ].join(', ');

  const posStyle: React.CSSProperties = {
    top:    { top: 30,                left: 0, right: 0, textAlign: 'center' as const },
    bottom: { bottom: 80,             left: 0, right: 0, textAlign: 'center' as const },
    center: { top: '50%', left: 0, right: 0, textAlign: 'center' as const, transform: 'translateY(-50%)' },
  }[position];

  return (
    <div style={{ position: 'absolute', ...posStyle, padding: '0 32px', zIndex: 50 }}>
      <span style={{
        color, fontSize, fontFamily: 'Impact, Arial Black, sans-serif',
        fontWeight: 900, textTransform: 'uppercase' as const,
        textShadow: strokeShadow, lineHeight: 1.15, display: 'block',
      }}>
        {text}
      </span>
    </div>
  );
};

// POV / When prefix card
const FORMAT_PREFIXES: Record<ComedyFormat, { line1: string; line2?: string }> = {
  pov:                       { line1: 'POV:' },
  when:                      { line1: 'When' },
  nobody:                    { line1: 'Nobody:', line2: 'Absolutely nobody:' },
  comparison:                { line1: '' },
  'expectation-vs-reality':  { line1: '' },
};

// Media layer (image or video)
const MediaLayer: React.FC<{ src: string; objectFit?: 'cover' | 'contain' }> = ({
  src, objectFit = 'cover',
}) => {
  if (!src) {
    return (
      <AbsoluteFill style={{
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
      }} />
    );
  }
  const isVideo = src.match(/\.(mp4|mov|webm)$/i);
  if (isVideo) {
    return (
      <OffthreadVideo src={staticFile(src)}
        style={{ width: '100%', height: '100%', objectFit }} />
    );
  }
  return (
    <Img src={staticFile(src)}
      style={{ width: '100%', height: '100%', objectFit }} />
  );
};

// Zoom smash on punchline
const ZoomSmash: React.FC<{ children: React.ReactNode; startFrame?: number }> = ({
  children, startFrame = 0,
}) => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();
  const localF  = frame - startFrame;

  const zoomIn  = spring({ frame: localF, fps, config: { damping: 4, stiffness: 800 } });
  const zoomOut = spring({ frame: localF - 5, fps, config: { damping: 15, stiffness: 250 } });
  const scale   = localF < 5
    ? interpolate(zoomIn, [0, 1], [1, 1.35])
    : interpolate(zoomOut, [0, 1], [1.35, 1]);

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      {children}
    </AbsoluteFill>
  );
};

// Comparison split screen
const ComparisonSplit: React.FC = () => {
  const frame   = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear  = spring({ frame, fps, config: { damping: 60, stiffness: 100 } });
  const dividerX = interpolate(appear, [0, 1], [-WIDTH, 0]);

  const isHorizontal = HEIGHT < WIDTH;
  const midPoint = isHorizontal ? '50%' : '50%';

  return (
    <AbsoluteFill>
      {/* Left / Top */}
      <AbsoluteFill style={{ [isHorizontal ? 'width' : 'height']: midPoint }}>
        <MediaLayer src={LEFT_SRC} />
        <MemeText text={LEFT_LABEL} position="top" color={ACCENT} fontSize={40} />
      </AbsoluteFill>

      {/* Right / Bottom */}
      <AbsoluteFill style={{
        [isHorizontal ? 'left' : 'top']: midPoint,
        [isHorizontal ? 'width' : 'height']: midPoint,
      }}>
        <MediaLayer src={RIGHT_SRC} />
        <MemeText text={RIGHT_LABEL} position="top" color="#FF4500" fontSize={40} />
      </AbsoluteFill>

      {/* Divider */}
      <div style={{
        position: 'absolute',
        [isHorizontal ? 'left' : 'top']: midPoint,
        [isHorizontal ? 'top' : 'left']: 0,
        [isHorizontal ? 'bottom' : 'right']: 0,
        [isHorizontal ? 'width' : 'height']: 4,
        backgroundColor: 'white',
        transform: `translateX(${dividerX}px)`,
        zIndex: 10,
      }} />
    </AbsoluteFill>
  );
};

// ── MAIN COMPOSITION ────────────────────────────────────────
export const ComedyMeme: React.FC = () => {
  // Comedy timing (seconds)
  const SETUP_DURATION    = 6;   // setup
  const BEAT_DURATION     = 0.6; // the pause — comedic timing
  const PUNCHLINE_DURATION = 4;  // punchline
  const REACTION_DURATION = 2;   // emoji reaction

  const BEAT_START      = s(SETUP_DURATION);
  const PUNCHLINE_START = BEAT_START + s(BEAT_DURATION);
  const REACTION_START  = PUNCHLINE_START + s(PUNCHLINE_DURATION);
  const TOTAL           = REACTION_START + s(REACTION_DURATION);

  if (FORMAT === 'comparison' || FORMAT === 'expectation-vs-reality') {
    return (
      <AbsoluteFill>
        <ComparisonSplit />
      </AbsoluteFill>
    );
  }

  const prefix = FORMAT_PREFIXES[FORMAT];

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* === SETUP === */}
      <Sequence from={0} durationInFrames={BEAT_START}>
        <AbsoluteFill>
          <MediaLayer src={SETUP_SRC} />

          {/* Dark overlay for text readability */}
          <AbsoluteFill style={{ backgroundColor: 'rgba(0,0,0,0.3)' }} />

          {/* Format prefix */}
          {prefix.line2 ? (
            <div style={{ position: 'absolute', top: 20, left: 0, right: 0, textAlign: 'center', padding: '0 32px', zIndex: 50 }}>
              <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: 44, fontFamily: OSWALD, textTransform: 'uppercase' }}>
                {prefix.line1}
              </div>
              <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: 44, fontFamily: OSWALD, textTransform: 'uppercase' }}>
                {prefix.line2}
              </div>
            </div>
          ) : (
            prefix.line1 && <MemeText text={prefix.line1} position="top" color="rgba(255,255,255,0.6)" fontSize={44} />
          )}

          {/* Setup text at bottom */}
          <MemeText text={SETUP_TEXT} position="bottom" />
        </AbsoluteFill>
      </Sequence>

      {/* === THE BEAT (comedic pause) === */}
      <Sequence from={BEAT_START} durationInFrames={s(BEAT_DURATION)}>
        {/* Freeze the last frame of setup — the pause */}
        <Freeze frame={BEAT_START - 1}>
          <AbsoluteFill>
            <MediaLayer src={SETUP_SRC} />
            <AbsoluteFill style={{ backgroundColor: 'rgba(0,0,0,0.3)' }} />
            <MemeText text={SETUP_TEXT} position="bottom" />
          </AbsoluteFill>
        </Freeze>
      </Sequence>

      {/* === PUNCHLINE === */}
      <Sequence from={PUNCHLINE_START} durationInFrames={s(PUNCHLINE_DURATION)}>
        <ZoomSmash startFrame={0}>
          <AbsoluteFill>
            <MediaLayer src={PUNCHLINE_SRC || SETUP_SRC} />
            <AbsoluteFill style={{ backgroundColor: 'rgba(0,0,0,0.4)' }} />
            <MemeText text={PUNCHLINE_TEXT} position="center" color={ACCENT} />
          </AbsoluteFill>
        </ZoomSmash>
      </Sequence>

      {/* === REACTION EMOJI === */}
      <Sequence from={REACTION_START} durationInFrames={s(REACTION_DURATION)}>
        <AbsoluteFill>
          <MediaLayer src={PUNCHLINE_SRC || SETUP_SRC} />
          <AbsoluteFill style={{ backgroundColor: 'rgba(0,0,0,0.4)' }} />
          <MemeText text={PUNCHLINE_TEXT} position="center" color={ACCENT} />

          {/* Emoji pop */}
          <div style={{
            position: 'absolute', top: '20%', right: '10%',
            fontSize: 120,
            transform: `scale(${spring({
              frame: useCurrentFrame(),
              fps: FPS,
              config: { damping: 6, stiffness: 600 },
            })})`,
            zIndex: 80,
          }}>
            {REACTION_EMOJI}
          </div>
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};

export const RemotionRoot: React.FC = () => {
  const { Composition } = require('remotion');
  const BEAT_START      = s(6);
  const PUNCHLINE_START = BEAT_START + s(0.6);
  const total           = PUNCHLINE_START + s(4) + s(2);
  return (
    <Composition
      id="ComedyMeme"
      component={ComedyMeme}
      durationInFrames={total}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
