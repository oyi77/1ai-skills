# Remotion Podcast & Long-Form Video Rule

## Overview

For video podcasts, tutorial videos, explainer content, and social media posts with narration. This pattern handles: research → script → TTS → timing → render → output.

## Recommended Folder Structure

```
my-podcast-video/
├── src/
│   ├── Root.tsx
│   └── components/
│       ├── SceneRenderer.tsx
│       ├── TitleCard.tsx
│       ├── ContentScene.tsx
│       ├── Subtitle.tsx
│       └── ProgressBar.tsx
├── public/
│   ├── audio/          # Generated TTS files + BGM
│   ├── images/         # Scene images/thumbnails
│   ├── script.json     # Raw script
│   └── timing.json     # Generated timing data
├── scripts/
│   ├── generate_tts.py
│   ├── generate_timing.py
│   └── run_pipeline.sh
├── music/              # Background music tracks
└── out/                # Rendered output
```

## Podcast-Style Layout (Widescreen 16:9)

```tsx
// components/PodcastScene.tsx
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';

interface PodcastSceneProps {
  title: string;
  chapterNumber: number;
  totalChapters: number;
  durationFrames: number;
  audioFile: string;
  audioPaddingFrames?: number;
  backgroundColor?: string;
  accentColor?: string;
}

export const PodcastScene: React.FC<PodcastSceneProps> = ({
  title, chapterNumber, totalChapters, durationFrames,
  audioFile, audioPaddingFrames = 15,
  backgroundColor = '#0f172a',
  accentColor = '#6366f1',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [durationFrames - 15, durationFrames], [1, 0], {
    extrapolateLeft: 'clamp',
  });
  const opacity = Math.min(fadeIn, fadeOut);

  const titleSpring = spring({ frame: frame - 10, fps, config: { damping: 80 } });
  const titleY = interpolate(titleSpring, [0, 1], [20, 0]);

  // Chapter progress bar
  const chapterProgress = frame / durationFrames;

  return (
    <AbsoluteFill style={{ backgroundColor, opacity }}>
      <Audio
        src={staticFile(`audio/${audioFile}`)}
        startFrom={audioPaddingFrames}
      />

      {/* Chapter number badge */}
      <div style={{
        position: 'absolute', top: 60, left: 80,
        backgroundColor: accentColor,
        color: 'white', fontSize: 20, fontWeight: 'bold',
        padding: '8px 20px', borderRadius: 999,
      }}>
        {chapterNumber} / {totalChapters}
      </div>

      {/* Main title */}
      <div style={{
        position: 'absolute',
        left: 80, right: 80,
        top: '50%', transform: `translateY(calc(-50% + ${titleY}px))`,
        opacity: titleSpring,
      }}>
        <h1 style={{
          color: 'white',
          fontSize: 80,
          fontWeight: 'bold',
          lineHeight: 1.15,
          margin: 0,
        }}>
          {title}
        </h1>
      </div>

      {/* Chapter progress bar */}
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0,
        height: 6, backgroundColor: 'rgba(255,255,255,0.1)',
      }}>
        <div style={{
          height: '100%',
          width: `${chapterProgress * 100}%`,
          backgroundColor: accentColor,
        }} />
      </div>

      {/* Overall progress dots */}
      <div style={{
        position: 'absolute', bottom: 24, right: 80,
        display: 'flex', gap: 8,
      }}>
        {Array.from({ length: totalChapters }).map((_, i) => (
          <div key={i} style={{
            width: 10, height: 10, borderRadius: '50%',
            backgroundColor: i < chapterNumber ? accentColor : 'rgba(255,255,255,0.3)',
          }} />
        ))}
      </div>
    </AbsoluteFill>
  );
};
```

## Vertical Video (TikTok / Reels / Shorts — 9:16)

```tsx
// Composition dimensions for vertical video
<Composition
  id="ShortVideo"
  component={ShortVideo}
  durationInFrames={300}
  fps={30}
  width={1080}
  height={1920}
/>

// Layout optimized for vertical
export const ShortVideo = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0f172a',
      flexDirection: 'column',
      justifyContent: 'space-between',
      padding: 60,
    }}>
      {/* Top: channel branding */}
      <div style={{ color: '#94a3b8', fontSize: 32 }}>@berkahkarya</div>

      {/* Middle: main content */}
      <div style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <h1 style={{ color: 'white', fontSize: 80, textAlign: 'center' }}>
          Tip of the Day
        </h1>
      </div>

      {/* Bottom: subtitle captions */}
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.5)',
        padding: 24,
        borderRadius: 16,
        fontSize: 52,
        color: 'white',
        textAlign: 'center',
      }}>
        {/* Caption text here */}
      </div>
    </AbsoluteFill>
  );
};
```

## Multi-Format Rendering (One Composition, Multiple Outputs)

```bash
# 16:9 widescreen
npx remotion render Podcast --props='{"format":"landscape"}' out/landscape.mp4

# 9:16 vertical (TikTok/Reels)
npx remotion render Podcast --props='{"format":"portrait"}' out/portrait.mp4

# 1:1 square (Instagram feed)
npx remotion render Podcast --props='{"format":"square"}' out/square.mp4
```

```tsx
// Responsive composition
const FORMAT_CONFIG = {
  landscape: { width: 1920, height: 1080, fontSize: 72 },
  portrait: { width: 1080, height: 1920, fontSize: 80 },
  square: { width: 1080, height: 1080, fontSize: 68 },
};

export const calculateMetadata: CalculateMetadataFunction<{ format: string }> = ({ props }) => {
  const config = FORMAT_CONFIG[props.format] ?? FORMAT_CONFIG.landscape;
  return { width: config.width, height: config.height };
};
```

## Thumbnail / Still Generation

```bash
# Generate thumbnail from frame 30
npx remotion still MyVideo out/thumbnail.jpg --frame=30 --jpeg-quality=95

# Generate multiple thumbnails
for frame in 0 30 60 90; do
  npx remotion still MyVideo out/thumb-$frame.jpg --frame=$frame
done
```

## YouTube Chapter Markers from timing.json

```python
# scripts/generate_chapters.py
import json

with open("public/timing.json") as f:
    timing = json.load(f)

print("YouTube Chapter Markers:")
print("0:00 Intro")

for scene in timing["scenes"]:
    start_sec = scene["startFrame"] / timing["fps"]
    m = int(start_sec // 60)
    s = int(start_sec % 60)
    print(f"{m}:{s:02d} {scene['title']}")
```

## Bilibili / YouTube Upload Script

```python
# After rendering, auto-generate metadata
with open("public/script.json") as f:
    script = json.load(f)

print(f"Title: {script['title']}")
print(f"Duration: {timing['totalSeconds']:.0f}s")
print(f"\nDescription:")
for i, scene in enumerate(script["scenes"], 1):
    print(f"{i}. {scene['title']}")
```
