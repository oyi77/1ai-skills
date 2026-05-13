// ============================================================
// PODCAST / TALKING HEAD VIDEO TEMPLATE
// Style: Professional podcast — lower thirds, chapter marks,
//        quote cards, audio waveform, progress bar
// Format: 16:9 1080p — change w/h for 9:16 shorts cut
// Customize: SHOW_*, HOST_*, CHAPTERS, BRAND_COLOR
// ============================================================

import React from 'react';
import {
  AbsoluteFill, Composition, Sequence, Audio, OffthreadVideo, staticFile,
  useCurrentFrame, useVideoConfig,
  interpolate, spring,
} from 'remotion';

// ── CONFIG ───────────────────────────────────────────────────
const SHOW_NAME    = 'Ngobrol Bisnis Podcast';
const SHOW_TAGLINE = 'Tips praktis untuk UMKM Indonesia';
const HOST_NAME    = 'Nama Kamu';
const HOST_TITLE   = 'Founder, BerkahKarya';
const BRAND_COLOR  = '#6366f1';   // your brand colour
const EPISODE_NUM  = 42;

// Chapters: from = frame number when this chapter starts
const FPS = 30;
const CHAPTERS = [
  { from: 0,          title: 'Intro & Hook',          quote: null },
  { from: FPS * 45,   title: 'Masalah yang Sering Terjadi', quote: 'Kebanyakan UMKM gagal bukan karena produk jelek, tapi karena marketing yang salah.' },
  { from: FPS * 120,  title: 'Solusi yang Terbukti',  quote: null },
  { from: FPS * 220,  title: 'Case Study Nyata',      quote: 'Dari 0 ke 100 juta dalam 6 bulan — ini yang dia lakukan.' },
  { from: FPS * 320,  title: 'Action Steps',          quote: null },
  { from: FPS * 420,  title: 'Penutup & CTA',         quote: null },
];

// Replace with your actual video file paths
const TALKING_HEAD_VIDEO = 'video/talking-head.mp4';
const AUDIO_FILE         = 'audio/episode.mp3';

const DURATION = FPS * 480; // 8 minutes — adjust to your episode

// ── ROOT ─────────────────────────────────────────────────────
export const RemotionRoot: React.FC = () => (
  <Composition
    id="PodcastVideo"
    component={PodcastVideo}
    durationInFrames={DURATION}
    fps={FPS}
    width={1920}
    height={1080}
    defaultProps={{}}
  />
);

// ── MAIN COMPOSITION ─────────────────────────────────────────
const PodcastVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = frame / durationInFrames;

  // Find current chapter
  const currentChapterIndex = CHAPTERS.reduce((acc, ch, i) =>
    frame >= ch.from ? i : acc, 0
  );
  const currentChapter = CHAPTERS[currentChapterIndex];
  const nextChapter    = CHAPTERS[currentChapterIndex + 1];

  // Does current chapter have a quote card to show?
  const showQuote = currentChapter.quote && frame >= currentChapter.from + FPS * 5;

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a' }}>

      {/* Audio track */}
      <Audio src={staticFile(AUDIO_FILE)} />

      {/* Talking head footage */}
      <OffthreadVideo
        src={staticFile(TALKING_HEAD_VIDEO)}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        volume={0}   // audio comes from the Audio component above
      />

      {/* Subtle vignette */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 50% 40%, transparent 40%, rgba(0,0,0,0.5) 100%)',
      }} />

      {/* Show branding — top left */}
      <ShowBranding />

      {/* Chapter title — top right */}
      <ChapterIndicator
        chapter={currentChapter}
        chapterIndex={currentChapterIndex}
        totalChapters={CHAPTERS.length}
        frame={frame}
      />

      {/* Quote card — when chapter has one */}
      {showQuote && currentChapter.quote && (
        <QuoteCard
          quote={currentChapter.quote}
          triggerFrame={currentChapter.from + FPS * 5}
        />
      )}

      {/* Host lower third — shows at start of each chapter */}
      {frame >= 30 && frame < 30 + FPS * 5 && (
        <HostLowerThird triggerFrame={30} />
      )}

      {/* Chapter transition text */}
      {CHAPTERS.slice(1).map((ch, i) =>
        frame >= ch.from && frame < ch.from + FPS * 3 ? (
          <ChapterTransition key={i} title={ch.title} triggerFrame={ch.from} />
        ) : null
      )}

      {/* Waveform visualiser — bottom */}
      <AudioWaveform frame={frame} />

      {/* Progress bar */}
      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 4, backgroundColor: 'rgba(255,255,255,0.1)' }}>
        <div style={{ height: '100%', width: `${progress * 100}%`, backgroundColor: BRAND_COLOR }} />
      </div>

    </AbsoluteFill>
  );
};

// ── SHOW BRANDING ────────────────────────────────────────────
const ShowBranding: React.FC = () => (
  <div style={{
    position: 'absolute', top: 40, left: 60,
    display: 'flex', alignItems: 'center', gap: 12,
  }}>
    <div style={{
      width: 8, height: 40, backgroundColor: BRAND_COLOR, borderRadius: 2,
    }} />
    <div>
      <div style={{ color: 'white', fontSize: 22, fontWeight: 700 }}>{SHOW_NAME}</div>
      <div style={{ color: '#64748b', fontSize: 16 }}>EP. {EPISODE_NUM}</div>
    </div>
  </div>
);

// ── CHAPTER INDICATOR ────────────────────────────────────────
const ChapterIndicator: React.FC<{
  chapter: typeof CHAPTERS[0];
  chapterIndex: number;
  totalChapters: number;
  frame: number;
}> = ({ chapter, chapterIndex, totalChapters, frame }) => (
  <div style={{ position: 'absolute', top: 40, right: 60 }}>
    {/* Progress dots */}
    <div style={{ display: 'flex', gap: 6, justifyContent: 'flex-end', marginBottom: 8 }}>
      {Array.from({ length: totalChapters }).map((_, i) => (
        <div key={i} style={{
          width: 8, height: 8, borderRadius: '50%',
          backgroundColor: i <= chapterIndex ? BRAND_COLOR : 'rgba(255,255,255,0.2)',
        }} />
      ))}
    </div>
    <div style={{
      color: 'rgba(255,255,255,0.6)', fontSize: 18,
      textAlign: 'right', fontWeight: 500,
    }}>
      {chapter.title}
    </div>
  </div>
);

// ── HOST LOWER THIRD ─────────────────────────────────────────
const HostLowerThird: React.FC<{ triggerFrame: number }> = ({ triggerFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF  = frame - triggerFrame;
  const slideIn = spring({ frame: localF, fps, config: { damping: 80, stiffness: 120 } });
  const x       = interpolate(slideIn, [0, 1], [-500, 0]);
  const fadeOut = interpolate(localF, [fps * 4, fps * 5], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <div style={{
      position: 'absolute', bottom: 140, left: 60,
      transform: `translateX(${x}px)`, opacity: fadeOut,
    }}>
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.88)',
        padding: '14px 28px 14px 24px',
        borderRadius: '0 12px 12px 0',
        borderLeft: `4px solid ${BRAND_COLOR}`,
      }}>
        <div style={{ color: 'white', fontSize: 30, fontWeight: 700 }}>{HOST_NAME}</div>
        <div style={{ color: BRAND_COLOR, fontSize: 20, marginTop: 3 }}>{HOST_TITLE}</div>
      </div>
    </div>
  );
};

// ── QUOTE CARD ───────────────────────────────────────────────
const QuoteCard: React.FC<{ quote: string; triggerFrame: number }> = ({ quote, triggerFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF  = frame - triggerFrame;
  const appear  = spring({ frame: localF, fps, config: { damping: 60 } });
  const opacity = interpolate(appear, [0, 0.5], [0, 1]);
  const y       = interpolate(appear, [0, 1], [16, 0]);

  return (
    <div style={{
      position: 'absolute', right: 60, top: '50%',
      transform: `translateY(calc(-50% + ${y}px))`,
      width: 620, opacity,
    }}>
      <div style={{
        backgroundColor: 'rgba(10,10,30,0.9)',
        border: `1px solid ${BRAND_COLOR}40`,
        borderLeft: `4px solid ${BRAND_COLOR}`,
        borderRadius: '0 12px 12px 0',
        padding: '28px 32px',
        backdropFilter: 'blur(8px)',
      }}>
        <div style={{ fontSize: 60, color: BRAND_COLOR, lineHeight: 0.6, marginBottom: 12, opacity: 0.4 }}>
          "
        </div>
        <p style={{
          color: 'white', fontSize: 28, lineHeight: 1.5,
          margin: 0, fontStyle: 'italic',
        }}>
          {quote}
        </p>
      </div>
    </div>
  );
};

// ── CHAPTER TRANSITION ───────────────────────────────────────
const ChapterTransition: React.FC<{ title: string; triggerFrame: number }> = ({
  title, triggerFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localF  = frame - triggerFrame;
  const appear  = spring({ frame: localF, fps, config: { damping: 80 } });
  const fadeOut = interpolate(localF, [fps * 2.5, fps * 3], [1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: 'rgba(0,0,0,0.7)',
      justifyContent: 'center', alignItems: 'center',
      opacity: fadeOut,
    }}>
      <div style={{
        textAlign: 'center',
        transform: `scale(${spring({ frame: localF, fps, config: { damping: 60 } })})`,
        opacity: interpolate(appear, [0, 0.5], [0, 1]),
      }}>
        <div style={{ color: BRAND_COLOR, fontSize: 20, letterSpacing: 6, textTransform: 'uppercase', marginBottom: 12 }}>
          Next Up
        </div>
        <div style={{ color: 'white', fontSize: 56, fontWeight: 800 }}>
          {title}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ── AUDIO WAVEFORM DECOR ─────────────────────────────────────
const AudioWaveform: React.FC<{ frame: number }> = ({ frame }) => {
  const BAR_COUNT = 80;

  const bars = Array.from({ length: BAR_COUNT }, (_, i) => {
    const freq  = (i / BAR_COUNT) * Math.PI * 4;
    const value = (Math.sin(freq + frame * 0.07) * 0.4 + 0.5) * 0.6 + 0.1;
    return Math.max(0.05, value);
  });

  return (
    <div style={{
      position: 'absolute', bottom: 10, left: 0, right: 0,
      display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2,
      height: 40, opacity: 0.35,
    }}>
      {bars.map((v, i) => (
        <div key={i} style={{
          width: 18,
          height: v * 36,
          backgroundColor: BRAND_COLOR,
          borderRadius: 2,
        }} />
      ))}
    </div>
  );
};
