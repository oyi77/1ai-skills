---
name: voice-chatterbox-tts
description: Use for free local text-to-speech with voice cloning via Chatterbox. Zero API cost, word-level timing export, Whisper alignment. Clone a voice from 10–60 s reference audio for narration, voiceovers, and custom AI voices.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- tts
- voice-cloning
- local
- free
- whisper
- narration
- audio
version: 1.0.0
category: content
---

# Voice Chatterbox TTS — Local, Free, Cloneable

## When to Use

**Trigger phrases:**
- "generate voiceover for video" · "clone this voice for narration"
- "create TTS without API costs" · "sync subtitles with audio"
- "text-to-speech with word highlighting"

**Use cases:**
- YouTube / podcast narration without ElevenLabs fees
- Audiobook production (long-form, local)
- Course voiceovers
- Word-level timestamps for karaoke captions or auto-subtitles

## When NOT to Use

- Real-time streaming — Chatterbox is batch; use `voice-ai` or cloud TTS for live
- 100+ preset voices — use Azure / Google TTS
- Sub-200 ms latency needed — cloud APIs are faster
- Under 16 GB RAM / no CUDA GPU — use `voice/omnivoice` with CPU offload or a cloud TTS

## Overview

Chatterbox (Resemble AI, Apache-2.0) runs entirely on your machine. No API key, no usage cap. It supports **zero-shot voice cloning** from a 10–60 s reference clip and emits **word-level timestamps** you can align to subtitles with Whisper.

Prerequisites: Python 3.10+, CUDA GPU recommended (16 GB VRAM for fp16; CPU works but ~10× slower).

## Setup

```bash
pip install chatterbox-tts
# First run downloads model weights (~2 GB) to ~/.cache/chatterbox/
python -c "from chatterbox.tts import ChatterboxTTS; print('chatterbox ok')"
```

## Workflow

### 1. Plain TTS (no cloning)

```python
import soundfile as sf
from chatterbox.tts import ChatterboxTTS

tts = ChatterboxTTS.from_pretrained()            # or from_pretrained(device="cpu")
wav = tts.generate(
    text="Meet the future of claymation — powered by AI.",
    audio_prompt_path=None,                      # no reference = default voice
)
sf.write("narration.wav", wav["wav"], tts.sr)    # tts.sr = 24000 Hz
print("saved narration.wav", len(wav["wav"]) / tts.sr, "s")
```

### 2. Voice cloning

Use a clean 10–60 s reference: one speaker, no music, no reverb, −23…−16 LUFS.

```python
wav = tts.generate(
    text="My clone now speaks in every language you ship.",
    audio_prompt_path="reference.wav",           # 10–60 s, mono or stereo
    exaggeration=0.5,                            # 0 = calm, 1 = very expressive
    temperature=0.7,                             # higher = more variation
)
sf.write("cloned.wav", wav["wav"], tts.sr)
```

- `exaggeration` 0.3–0.6 for narration; 0.7–1.0 for ads.
- `temperature` 0.5–0.8; raise if output sounds monotone.

### 3. Word-level timing (for subtitles)

Chatterbox has **no native alignment API**. Derive timestamps from the rendered audio with Whisper:

```python
import whisper

model = whisper.load_model("base")
seg = model.transcribe("narration.wav", word_timestamps=True)
words = [w for s in seg["segments"] for w in s["words"]]
# words = [{"word": "Meet", "start": 0.0, "end": 0.24}, ...]
```

Write an SRT directly:

```python
def fmt(ts):
    h, m, s = int(ts // 3600), int((ts % 3600) // 60), ts % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")

def to_srt(words, path="captions.srt"):
    with open(path, "w") as f:
        for i, w in enumerate(words, 1):
            f.write(f"{i}\n{fmt(w['start'])} --> {fmt(w['end'])}\n{w['word'].strip()}\n\n")
    print("wrote", path, f"({len(words)} words)")
```

Spot-check the first few lines against the audio — Whisper mis-hears proper nouns and numbers, so hand-fix those before shipping captions.

### 4. Verify output before shipping

```bash
ffprobe -v error -show_entries stream=codec_name,sample_rate:format=duration \
  -of compact narration.wav
# Expect: duration ≈ len(text)/2.7 words-per-second; sample_rate=24000

ffmpeg -nostats -i narration.wav -af ebur128 -f null - 2>&1 | grep "I:"
# Target: −14 to −20 LUFS (headroom for mixing into a video)
```

Always listen to the first render end-to-end. Cloned voices occasionally mangle proper nouns and numbers.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Free means no quality cost" | Chatterbox ≈ ElevenLabs Turbo, but still audit proper nouns / numbers. |
| "10 s reference is enough" | <10 s loses accent and rhythm. Cut a full, representative 30 s. |
| "Native timestamps are perfect" | There are none — derive them with Whisper and spot-check proper nouns / numbers. |
| "CPU is fine" | 15 s of speech takes ~2 min on CPU vs ~8 s on GPU. Budget accordingly. |

## Verification

- [ ] `chatterbox-tts` importable, weights cached
- [ ] Reference audio 10–60 s, single speaker, −23…−16 LUFS, no background music
- [ ] Rendered file probes as 24 kHz WAV with expected duration (±0.5 s)
- [ ] Word timestamps written to SRT and spot-checked against audio
- [ ] Loudness normalized to −14 LUFS when mixed into final video
- [ ] First 5 s + last 5 s listened to by a human (names, numbers, acronyms)
