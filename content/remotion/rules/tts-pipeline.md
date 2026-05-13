# Remotion TTS Pipeline Rule

## Complete Pipeline Overview

```
Script (JSON/text)
    ↓
TTS Generation (Edge TTS / Azure / ElevenLabs)
    ↓
Audio Duration Detection (ffprobe / @remotion/media-utils)
    ↓
timing.json (scene durations in frames)
    ↓
Remotion Render (audio + visuals synced)
    ↓
FFmpeg Post-Process (BGM mixing, subtitle burn)
    ↓
Final MP4
```

## Step 1 — Write Your Script JSON

```json
// public/script.json
{
  "title": "Judul Video Saya",
  "scenes": [
    {
      "id": "intro",
      "title": "Pembukaan",
      "narration": "Selamat datang di video ini. Hari ini kita akan membahas topik penting.",
      "background": "gradient-blue",
      "duration": null
    },
    {
      "id": "main",
      "title": "Isi Utama",
      "narration": "Inilah poin-poin utama yang perlu Anda ketahui tentang bisnis digital.",
      "background": "dark",
      "duration": null
    },
    {
      "id": "outro",
      "title": "Penutup",
      "narration": "Terima kasih sudah menonton. Jangan lupa subscribe!",
      "background": "gradient-purple",
      "duration": null
    }
  ]
}
```

## Step 2 — Generate TTS Audio (Edge TTS — Free)

```python
# scripts/generate_tts.py
import asyncio
import json
import os
import edge_tts

# Voice options
VOICES = {
  'id': 'id-ID-ArdiNeural',        # Indonesian male
  'id-f': 'id-ID-GadisNeural',     # Indonesian female
  'en': 'en-US-JennyNeural',       # English female
  'en-m': 'en-US-GuyNeural',       # English male
  'zh': 'zh-CN-XiaoxiaoNeural',    # Chinese female
}

async def generate_scene_audio(scene_id: str, text: str, voice: str, output_dir: str):
    output_path = os.path.join(output_dir, f"{scene_id}.mp3")
    if os.path.exists(output_path):
        print(f"  Skip {scene_id} (already exists)")
        return output_path
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"  Generated: {output_path}")
    return output_path

async def main():
    with open("public/script.json") as f:
        script = json.load(f)

    os.makedirs("public/audio", exist_ok=True)
    voice = VOICES.get("id", VOICES["en"])

    for scene in script["scenes"]:
        await generate_scene_audio(
            scene["id"],
            scene["narration"],
            voice,
            "public/audio"
        )
    print("✅ TTS generation complete")

asyncio.run(main())
```

**Install & Run:**
```bash
pip install edge-tts
python scripts/generate_tts.py
```

## Step 3 — Detect Audio Durations → timing.json

```python
# scripts/generate_timing.py
import json
import subprocess
import os

def get_audio_duration(filepath: str) -> float:
    """Get duration in seconds using ffprobe"""
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json", filepath
        ],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])

def main():
    FPS = 30

    with open("public/script.json") as f:
        script = json.load(f)

    timing = {"fps": FPS, "scenes": []}
    cumulative_frame = 0

    for scene in script["scenes"]:
        audio_path = f"public/audio/{scene['id']}.mp3"

        if os.path.exists(audio_path):
            duration_sec = get_audio_duration(audio_path)
        else:
            duration_sec = 5.0  # fallback
            print(f"  Warning: No audio for {scene['id']}, using 5s")

        # Add padding (0.5s before + 0.3s after narration)
        total_sec = 0.5 + duration_sec + 0.3
        duration_frames = round(total_sec * FPS)

        timing["scenes"].append({
            "id": scene["id"],
            "title": scene.get("title", ""),
            "audioFile": f"{scene['id']}.mp3",
            "durationSeconds": round(duration_sec, 3),
            "totalDurationSeconds": round(total_sec, 3),
            "durationFrames": duration_frames,
            "startFrame": cumulative_frame,
            "endFrame": cumulative_frame + duration_frames,
            "background": scene.get("background", "dark"),
        })

        cumulative_frame += duration_frames

    timing["totalFrames"] = cumulative_frame
    timing["totalSeconds"] = round(cumulative_frame / FPS, 2)

    with open("public/timing.json", "w") as f:
        json.dump(timing, f, indent=2)

    print(f"✅ Timing generated: {cumulative_frame} frames ({timing['totalSeconds']}s)")

main()
```

**Install & Run:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

python scripts/generate_timing.py
```

## Step 4 — Remotion Composition Using timing.json

```tsx
// src/Composition.tsx
import { AbsoluteFill, Sequence, Audio, staticFile } from 'remotion';
import timingData from '../public/timing.json';
import { SceneRenderer } from './SceneRenderer';

export const NarratedVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a' }}>
      {/* Background music (full duration, low volume) */}
      <Audio src={staticFile('audio/bgm.mp3')} volume={0.12} />

      {/* Scenes with narration */}
      {timingData.scenes.map((scene) => (
        <Sequence
          key={scene.id}
          from={scene.startFrame}
          durationInFrames={scene.durationFrames}
        >
          {/* Narration audio */}
          <Audio
            src={staticFile(`audio/${scene.audioFile}`)}
            startFrom={Math.round(0.5 * timingData.fps)} // start after 0.5s padding
          />
          {/* Visual scene */}
          <SceneRenderer scene={scene} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

```tsx
// src/Root.tsx
import { Composition } from 'remotion';
import { NarratedVideo } from './Composition';
import timingData from '../public/timing.json';

export const RemotionRoot = () => (
  <Composition
    id="NarratedVideo"
    component={NarratedVideo}
    durationInFrames={timingData.totalFrames}
    fps={timingData.fps}
    width={1920}
    height={1080}
  />
);
```

```tsx
// src/SceneRenderer.tsx
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';

interface SceneData {
  id: string;
  title: string;
  durationFrames: number;
  background: string;
}

const BACKGROUNDS: Record<string, string> = {
  'dark': '#0f172a',
  'gradient-blue': 'linear-gradient(135deg, #1e3a8a, #3b82f6)',
  'gradient-purple': 'linear-gradient(135deg, #4c1d95, #7c3aed)',
  'gradient-green': 'linear-gradient(135deg, #064e3b, #10b981)',
};

export const SceneRenderer: React.FC<{ scene: SceneData }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance fade
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  // Exit fade
  const exitOpacity = interpolate(
    frame,
    [scene.durationFrames - 12, scene.durationFrames],
    [1, 0],
    { extrapolateLeft: 'clamp' }
  );

  // Title spring entrance
  const titleY = spring({ frame: frame - 10, fps, config: { damping: 80 } });
  const titleTranslate = interpolate(titleY, [0, 1], [30, 0]);

  const bg = BACKGROUNDS[scene.background] || BACKGROUNDS['dark'];
  const isGradient = bg.startsWith('linear-gradient');

  return (
    <AbsoluteFill
      style={{
        opacity: Math.min(opacity, exitOpacity),
        background: isGradient ? bg : undefined,
        backgroundColor: !isGradient ? bg : undefined,
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: 24,
        padding: 80,
      }}
    >
      <h1 style={{
        color: 'white',
        fontSize: 72,
        fontWeight: 'bold',
        textAlign: 'center',
        transform: `translateY(${titleTranslate}px)`,
        opacity: titleY,
        margin: 0,
      }}>
        {scene.title}
      </h1>
    </AbsoluteFill>
  );
};
```

## Step 5 — Render + Post-Process

```bash
# Render video
npx remotion render NarratedVideo out/video-raw.mp4

# Mix in BGM with FFmpeg (if not done in Remotion)
ffmpeg -i out/video-raw.mp4 -i public/audio/bgm.mp3 \
  -filter_complex "[1:a]volume=0.12[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy \
  out/final.mp4

# Add subtitles (optional)
ffmpeg -i out/final.mp4 \
  -vf "subtitles=public/subtitles.srt" \
  out/final-with-subs.mp4
```

## Complete Run Script

```bash
#!/bin/bash
# run_pipeline.sh — Full pipeline from script to final video

echo "🎙️ Step 1: Generate TTS audio..."
python scripts/generate_tts.py

echo "⏱️ Step 2: Generate timing..."
python scripts/generate_timing.py

echo "🎬 Step 3: Render video..."
npx remotion render NarratedVideo out/video-raw.mp4 --codec h264 --crf 18

echo "🎵 Step 4: Mix BGM..."
ffmpeg -y -i out/video-raw.mp4 -i public/audio/bgm.mp3 \
  -filter_complex "[1:a]volume=0.12,afade=t=out:st=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video-raw.mp4 | awk '{print $1-3}'):d=3[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy \
  out/final.mp4

echo "✅ Done! Output: out/final.mp4"
```

## ElevenLabs TTS (Premium, most realistic)

```python
import requests, os

def generate_elevenlabs_tts(text: str, output_path: str,
                              voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
    )
    with open(output_path, "wb") as f:
        f.write(response.content)
```
