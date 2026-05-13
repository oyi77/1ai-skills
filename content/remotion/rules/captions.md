# Remotion Captions & Subtitles Rule

## Using @remotion/captions

```bash
npm install @remotion/captions
```

```tsx
import { Caption, createTikTokStyleCaptions } from '@remotion/captions';

// Captions data format (can come from WhisperX, AssemblyAI, etc.)
const captions: Caption[] = [
  { text: 'Hello', startMs: 0, endMs: 500, confidence: 0.99 },
  { text: 'world', startMs: 500, endMs: 1000, confidence: 0.97 },
  { text: 'this is', startMs: 1000, endMs: 1500, confidence: 0.95 },
  { text: 'Remotion', startMs: 1500, endMs: 2200, confidence: 0.99 },
];
```

## TikTok-Style Word-by-Word Captions

```tsx
import { useCurrentFrame, useVideoConfig, AbsoluteFill } from 'remotion';
import { createTikTokStyleCaptions } from '@remotion/captions';

interface Props {
  captions: Caption[];
}

export const TikTokCaptions: React.FC<Props> = ({ captions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentTimeMs = (frame / fps) * 1000;

  const { pages } = createTikTokStyleCaptions({
    captions,
    combineTokensWithinMilliseconds: 1200,
  });

  const currentPage = pages.find(
    (p) => currentTimeMs >= p.startMs && currentTimeMs < p.endMs
  );

  if (!currentPage) return null;

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
      <div style={{
        fontSize: 72,
        fontWeight: 'bold',
        color: 'white',
        textAlign: 'center',
        padding: '0 60px',
        marginBottom: 120,
        lineHeight: 1.2,
      }}>
        {currentPage.tokens.map((token, i) => {
          const isActive =
            currentTimeMs >= token.fromMs && currentTimeMs < token.toMs;
          return (
            <span
              key={i}
              style={{
                color: isActive ? '#fbbf24' : 'white',
                textShadow: '2px 2px 8px rgba(0,0,0,0.8)',
              }}
            >
              {token.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
```

## Simple Frame-Based Subtitles (No Package)

```tsx
interface SubtitleLine {
  text: string;
  startFrame: number;
  endFrame: number;
}

// Convert from seconds to frames
const toFrame = (seconds: number, fps: number) => Math.round(seconds * fps);

const subtitles: SubtitleLine[] = [
  { text: "Welcome to my channel", startFrame: 0, endFrame: 60 },
  { text: "Today we'll talk about Remotion", startFrame: 65, endFrame: 130 },
  { text: "Let's get started!", startFrame: 135, endFrame: 180 },
];

export const Subtitles: React.FC = () => {
  const frame = useCurrentFrame();

  const current = subtitles.find(
    (s) => frame >= s.startFrame && frame <= s.endFrame
  );

  const opacity = current
    ? interpolate(frame - current.startFrame, [0, 8], [0, 1], {
        extrapolateRight: 'clamp',
      })
    : 0;

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center' }}>
      <div style={{
        backgroundColor: 'rgba(0,0,0,0.6)',
        padding: '12px 32px',
        borderRadius: 8,
        marginBottom: 80,
        opacity,
      }}>
        <p style={{ color: 'white', fontSize: 48, margin: 0, textAlign: 'center' }}>
          {current?.text ?? ''}
        </p>
      </div>
    </AbsoluteFill>
  );
};
```

## Generating Captions from Audio (WhisperX / OpenAI Whisper)

```python
# generate_captions.py — Run before rendering
import whisper
import json

model = whisper.load_model("base")
result = model.transcribe("public/audio/narration.mp3", word_timestamps=True)

captions = []
for segment in result["segments"]:
    for word in segment.get("words", []):
        captions.append({
            "text": word["word"].strip(),
            "startMs": round(word["start"] * 1000),
            "endMs": round(word["end"] * 1000),
            "confidence": word.get("probability", 1.0),
        })

with open("public/captions.json", "w") as f:
    json.dump(captions, f, indent=2)

print(f"Generated {len(captions)} caption tokens")
```

## Loading Captions in Composition

```tsx
// Using calculateMetadata to load captions
import captionsData from '../public/captions.json';

interface Props {
  showCaptions: boolean;
}

export const VideoWithCaptions: React.FC<Props> = ({ showCaptions }) => {
  return (
    <AbsoluteFill>
      <MainContent />
      {showCaptions && <TikTokCaptions captions={captionsData} />}
    </AbsoluteFill>
  );
};
```

## Burning Subtitles with FFmpeg (Post-Render)

After rendering video, burn SRT subtitles:

```bash
# Convert JSON captions to SRT first
python convert_to_srt.py

# Burn subtitles
ffmpeg -i out/video.mp4 \
  -vf "subtitles=public/subtitles.srt:force_style='FontSize=28,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" \
  out/final-with-subs.mp4
```

```python
# convert_to_srt.py
import json

def ms_to_srt_time(ms):
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

with open("public/captions.json") as f:
    captions = json.load(f)

# Group into lines of ~8 words
lines = []
buffer = []
buffer_start = None

for c in captions:
    if buffer_start is None:
        buffer_start = c["startMs"]
    buffer.append(c["text"])
    if len(buffer) >= 8 or c["endMs"] - buffer_start > 3000:
        lines.append({
            "text": " ".join(buffer),
            "startMs": buffer_start,
            "endMs": c["endMs"],
        })
        buffer = []
        buffer_start = None

with open("public/subtitles.srt", "w") as f:
    for i, line in enumerate(lines, 1):
        f.write(f"{i}\n")
        f.write(f"{ms_to_srt_time(line['startMs'])} --> {ms_to_srt_time(line['endMs'])}\n")
        f.write(f"{line['text']}\n\n")
```
