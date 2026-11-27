---
name: audio-reactive-animation
description: Use when syncing animation to audio — BPM/onset detection with librosa, word-level subtitles via WhisperX-class ASR, frame-accurate mapping into Remotion or HyperFrames, and final FFmpeg encode. Use for beat-synced cuts, music visualizers, karaoke captions, and podcast clips.
domain: content
category: content
subdomain: video-production
tags:
- audio
- animation
- beat-sync
- librosa
- whisperx
- subtitles
- remotion
- ffmpeg
version: 1.0.0
author: oyi77
license: MIT
triggers:
- "sync animation to music"
- "beat-synced video"
- "music visualizer"
- "karaoke captions"
- "audio reactive"
---

# Audio-Reactive Animation

Turn sound into frame-exact motion: detect beats and onsets, align words to timecode, map time to frames in the rendering engine, then encode with FFmpeg. The skill owns the timing contract; rendering stays with [remotion](../video/remotion/SKILL.md), [video-editor](../video/editor/SKILL.md), and [hyperframes-general-video](../hyperframes-general-video/SKILL.md).

## Overview

Audio-reactive output fails at boundaries: a beat detected at 12.37s lands on frame 742 at 60fps, not on the nearest cut you eyeballed. Work in seconds from analysis, convert once to integer frames using the composition's exact fps, and let every downstream element read the same frame clock. Captions use word-level timestamps; music uses onsets. Never mix the two timing sources in one track.

## When to Use

- Music visualizers, beat-synced cuts, kinetic type locked to a kick drum.
- Word-level or karaoke captions with verified in/out points.
- Podcast or interview clips where a highlight must start on a spoken word and end on a beat.
- Re-rendering a timed composition at a different fps.

## When NOT to Use

- Loosely "music-inspired" motion with no timing requirement — use [motion-dev](../motion-dev/SKILL.md).
- Voice synthesis or TTS itself — use [voice-ai](../voice-ai/SKILL.md).
- Simple trim/concat with no synchronization — use [ffmpeg-mcp](../../mcp/servers/ffmpeg-mcp/SKILL.md).

## Workflow

### 1. Fix the timing contract before analysis

Write down: source audio path, sample rate, composition fps, total duration, time origin (`0` = first audible sample), and the frame rounding rule. Use `frame = round(seconds * fps)` consistently; keep `seconds` as float in the intermediate file so a fps change is a re-derive, not a re-analysis.

### 2. Analyze audio once, save a machine-readable timeline

Install analysis tools only when needed: `python3 -m pip install librosa soundfile`. Use WhisperX-class ASR for word timestamps when captions are required; verify the binary and model before relying on it.

```python
import json
import librosa

AUDIO = "input.wav"
FPS = 30

y, sr = librosa.load(AUDIO, sr=None)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time")
timeline = {
    "fps": FPS,
    "duration": float(librosa.get_duration(y=y, sr=sr)),
    "tempo_bpm": float(tempo),
    "beats": [round(float(t), 4) for t in beats],
    "onsets": [round(float(t), 4) for t in onsets],
}
with open("timeline.json", "w", encoding="utf-8") as fh:
    json.dump(timeline, fh, indent=2)
print(timeline["tempo_bpm"], len(timeline["beats"]))
```

Keep `timeline.json` in the project, not in chat. Re-running analysis must be reproducible from the same audio file.

### 3. Derive frames, do not eyeball them

```python
import json

timeline = json.load(open("timeline.json", encoding="utf-8"))
fps = timeline["fps"]
beat_frames = [round(t * fps) for t in timeline["beats"]]
assert all(a < b for a, b in zip(beat_frames, beat_frames[1:])), "non-monotonic beat frames"
assert all(0 <= f <= round(timeline["duration"] * fps) for f in beat_frames)
print(beat_frames[:8])
```

Detect duplicate frames at high bpm/low fps; if two beats collapse to one frame, raise fps or drop to a stronger subdivision instead of emitting a double trigger on one frame.

### 4. Build the visual response

In Remotion, read `useCurrentFrame()` and interpolate between adjacent beat frames; never use wall-clock time or CSS `animation` for synchronized elements. In HyperFrames, seek-safe keyframes must land on the derived frame numbers. Define one response per event class (beat → scale, onset → flicker, word → highlight) and keep amplitude small enough that the primary content stays readable.

Respect `prefers-reduced-motion` for any web preview of the composition; static fallback must still convey the caption text.

### 5. Captions from word timestamps

ASR word timestamps come as `{word, start, end}`. Map both boundaries with the same `round(seconds * fps)` rule; clamp the last word to composition duration; verify no word has `end <= start`. Use the existing caption skills for styling: [hyperframes-embedded-captions](../hyperframes-embedded-captions/SKILL.md).

### 6. Render and verify

Render with the project's existing engine, then probe the result: duration within one frame of contract, fps exact, audio stream present, no clipped peaks. Use FFmpeg's `ffprobe` via the checked MCP server or CLI; do not invent flags.

```bash
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,r_frame_rate -of json output.mp4
```

## Common Pitfalls / Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Eyeballing the cut is good enough" | Human sync tolerance is ~50ms; at 30fps that is 1.5 frames. Derive frames from timecodes. |
| "I'll use CSS animation and hope it lines up" | CSS runs on the browser clock, not the frame clock; renders drift and re-renders differ. |
| "The ASR tool probably supports word timestamps" | Verify the tool and model first. Sentence-level timestamps cannot produce karaoke captions. |
| "I changed fps; the old keyframes still work" | Every time-derived frame must be regenerated. Keep the seconds file, not just the frame list. |
| "tempo means every beat is on the grid" | `beat_track` estimates tempo; use detected beat times, not `n * 60 / bpm`, for events. |

## Verification

- [ ] `timeline.json` exists with fps, duration, tempo, beats, and onsets from the actual audio file.
- [ ] Frame derivation runs without assertion errors; all frames monotonic and in range.
- [ ] Rendered duration matches contract within one frame; fps and audio stream confirmed by `ffprobe`.
- [ ] Caption word in/out follow the same rounding rule; no zero-length words.
- [ ] Reduced-motion/static preview checked where the composition is embedded in a web page.
