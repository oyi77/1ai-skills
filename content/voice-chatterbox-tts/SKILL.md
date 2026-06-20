---
name: voice-chatterbox-tts
description: Free local TTS with voice cloning using Chatterbox. Zero API costs, word-level timing, whisper integration. Clone
  any voice with 10-60s reference audio. Use when generating narration, voiceovers, or custom AI voices.
domain: content
tags:
- tts
- voice-cloning
- local
- free
- whisper
- narration
- audio
---

# Voice Chatterbox TTS

Free, local text-to-speech with voice cloning using Chatterbox TTS. Zero API costs, word-level timing for perfect subtitle synchronization, and automatic speed control.

**Source:** [MoneyPrinterTurbo-Extended](https://github.com/Asad-Ismail/MoneyPrinterTurbo-Extended)

## When to Use

**Trigger phrases:**
- "Generate voiceover for video"
- "Clone this voice for narration"
- "Create TTS without API costs"
- "Sync subtitles with audio"
- "Text-to-speech with word highlighting"

**Use cases:**
- YouTube video narration
- Podcast intro/outro generation
- Audiobook production
- Course content voiceovers
- Custom AI voice assistants
- Multilingual content creation

**When NOT to use:**
 When real-time streaming is required (use other TTS services)
- When you need 100+ voices (use Azure/Google TTS)
- When computing resources are extremely limited

## Key Advantages

| Feature | Chatterbox | Azure TTS | OpenAI TTS |
|---------|------------|-----------|------------|
| **Cost** | Free (local) | $0.01/1K chars | $0.015/1K chars |
| **Voice Cloning** | ✅ 10-60s audio | ❌ | ❌ |
| **Word Timing** | ✅ WhisperX | ❌ | ❌ |
| **Speed Control** | ✅ | ✅ | ✅ |
| **Offline** | ✅ | ❌ | ❌ |
| **API Key** | Not needed | Required | Required |

## Installation

```bash
# Install Chatterbox TTS
pip install chatterbox-tts

# Install WhisperX for word-level timing
pip install whisperx

# Verify installation
python3 -c "from chatterbox.tts import ChatterboxTTS; print('✅ Chatterbox ready')"
```

**Requirements:**
- Python 3.10+
- 8GB+ RAM (16GB recommended)
- GPU optional but 5-10x faster

## Quick Start

### Basic TTS

```python
from chatterbox.tts import ChatterboxTTS

# Initialize
model = ChatterboxTTS.from_pretrained(device="cpu")  # or "cuda"

# Generate speech
text = "Welcome to our channel. Today we're exploring AI agents."
wav = model.generate(text)

# Save audio
torchaudio.save("output.wav", wav, model.sr)
```

### Voice Cloning

```python
from chatterbox.tts import ChatterboxTTS

# Initialize
model = ChatterboxTTS.from_pretrained(device="cuda")

# Clone voice from reference audio (10-60 seconds)
reference_audio = "path/to/reference_voice.wav"
text = "This is cloned speech using the reference voice."

# Generate with voice cloning
wav = model.generate(
    text,
    audio_prompt_path=reference_audio,
    # Optional: adjust speed (0.5 = slow, 2.0 = fast)
    speed=1.0
)

torchaudio.save("cloned_output.wav", wav, model.sr)
```

### With Word-Level Timing

```python
import whisperx
from chatterbox.tts import ChatterboxTTS

def generate_with_timing(text, reference_audio=None):
    # Generate audio
    model = ChatterboxTTS.from_pretrained(device="cuda")
    wav = model.generate(text, audio_prompt_path=reference_audio)
    
    # Save temp audio
    torchaudio.save("temp.wav", wav, model.sr)
    
    # Get word-level timing with WhisperX
    audio = whisperx.load_audio("temp.wav")
    result = whisperx_model.transcribe(audio, batch_size=16)
    
    # Align words
    result = whisperx.align(result["segments"], model_a, metadata, audio, device)
    
    # Return audio + timing data
    return wav, result["segments"]

# Usage
audio, timing = generate_with_timing(
    "Today we're building something amazing.",
    reference_audio="narrator.wav"
)

# timing contains word-level timestamps for subtitle sync
for segment in timing:
    for word in segment["words"]:
        print(f"{word['start']:.2f}s - {word['end']:.2f}s: {word['word']}")
```

## Configuration

### Environment Variables

```bash
# Speed control (0.5 = slow, 1.0 = normal, 2.0 = fast)
export CHATTERBOX_SPEED=1.0

# Output sample rate (default: 24000)
export CHATTERBOX_SAMPLE_RATE=24000

# Device (cpu, cuda, mps)
export CHATTERBOX_DEVICE=cuda

# Max text length per chunk (default: 500 chars)
export CHATTERBOX_MAX_CHUNK=500
```

### Advanced Options

```python
wav = model.generate(
    text,
    audio_prompt_path=reference_audio,  # Voice cloning reference
    speed=1.0,                          # Speech speed
    # Temperature (0.0 = deterministic, 1.0 = creative)
    temperature=0.8,
    # Top-p sampling (0.0-1.0)
    top_p=0.9,
    # Repetition penalty
    repetition_penalty=1.2
)
```

## Common Workflows

### YouTube Video Narration

```python
from chatterbox.tts import ChatterboxTTS
import json

def generate_youtube_narration(script_path, reference_voice):
    """Generate narration with word-level timing for subtitles."""
    
    # Load script
    with open(script_path) as f:
        script = json.load(f)
    
    model = ChatterboxTTS.from_pretrained(device="cuda")
    
    all_audio = []
    all_timing = []
    
    for scene in script["scenes"]:
        # Generate narration for each scene
        wav = model.generate(
            scene["narration"],
            audio_prompt_path=reference_voice
        )
        all_audio.append(wav)
        
        # Get timing for subtitles
        timing = get_word_timing(wav)
        all_timing.append({
            "scene": scene["id"],
            "words": timing
        })
    
    # Concatenate audio
    final_audio = torch.cat(all_audio, dim=1)
    
    # Save
    torchaudio.save("narration.wav", final_audio, model.sr)
    
    # Save timing for subtitle generation
    with open("timing.json", "w") as f:
        json.dump(all_timing, f, indent=2)
    
    return "narration.wav", "timing.json"
```

### Podcast Generation

```python
def generate_podcast_episode(host_voice, guest_voice, script):
    """Generate podcast with multiple voices."""
    
    model = ChatterboxTTS.from_pretrained(device="cuda")
    
    segments = []
    
    for line in script:
        # Select voice based on speaker
        voice = host_voice if line["speaker"] == "host" else guest_voice
        
        # Generate audio
        wav = model.generate(line["text"], audio_prompt_path=voice)
        segments.append(wav)
        
        # Add pause between speakers
        pause = torch.zeros(1, model.sr * 0.5)  # 0.5s pause
        segments.append(pause)
    
    # Combine all segments
    episode = torch.cat(segments, dim=1)
    
    return episode
```

### Voice Library Management

```python
import os
import json

class VoiceLibrary:
    """Manage voice references for consistent narration."""
    
    def __init__(self, library_path="voices/"):
        self.library_path = library_path
        self.voices = self._load_library()
    
    def _load_library(self):
        """Load voice library metadata."""
        index_path = os.path.join(self.library_path, "index.json")
        if os.path.exists(index_path):
            with open(index_path) as f:
                return json.load(f)
        return {}
    
    def add_voice(self, name, audio_path, metadata=None):
        """Add a new voice to the library."""
        # Copy audio to library
        dest = os.path.join(self.library_path, f"{name}.wav")
        shutil.copy(audio_path, dest)
        
        # Update index
        self.voices[name] = {
            "path": dest,
            "added": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self._save_library()
    
    def get_voice(self, name):
        """Get voice reference path."""
        return self.voices[name]["path"]
    
    def _save_library(self):
        """Save library metadata."""
        index_path = os.path.join(self.library_path, "index.json")
        with open(index_path, "w") as f:
            json.dump(self.voices, f, indent=2)

# Usage
library = VoiceLibrary("voices/")
library.add_voice("narrator", "reference.wav", {
    "gender": "male",
    "tone": "professional",
    "language": "en"
})

voice_path = library.get_voice("narrator")
wav = model.generate("Hello world", audio_prompt_path=voice_path)
```

## Integration with Other Skills

### Video Production Pipeline

1. **This skill** → Generate narration audio
2. `skill://video-semantic-match` → Find relevant video clips
3. `skill://remotion` → Compose video with synced subtitles
4. `skill://video-editor` → Final editing and effects

### Podcast Production

1. **This skill** → Multi-voice generation
2. `skill://content-factory` → Script generation
 `skill://video-editor` → Post-processing
4. `skill://content-publisher` → Distribution

### Voice Assistant

1. **This skill** → Custom voice generation
2. `skill://voice-ai-agent` → Call handling
 `skill://voice-ai-agent` → Conversation logic
 `skill://para-memory-files` → Context retention

## Performance Benchmarks

| Hardware | Speed | 10min Audio |
|----------|-------|-------------|
| CPU (i7-12700) | 0.3x realtime | ~33 min |
| GPU (RTX 3060) | 3x realtime | ~3.3 min |
| GPU (RTX 4090) | 8x realtime | ~1.25 min |
| Apple M1 Pro | 1.5x realtime | ~6.6 min |

**Voice cloning:** +20% processing time

## Troubleshooting

### CUDA out of memory
```bash
# Use CPU instead
export CHATTERBOX_DEVICE=cpu

# Or reduce batch size
export CHATTERBOX_MAX_CHUNK=200
```

### Audio quality issues
```python
# Increase temperature for more natural speech
wav = model.generate(text, temperature=0.9)

# Use repetition penalty to avoid loops
wav = model.generate(text, repetition_penalty=1.3)
```

### Reference audio too short
- Minimum: 10 seconds
- Optimal: 30-60 seconds
- Ensure clean audio (no background noise)

## Verification Checklist

- [ ] Chatterbox installed and imports work
- [ ] WhisperX installed for word timing
- [ ] GPU detected (if available)
- [ ] Test TTS generation works
- [ ] Test voice cloning with reference audio
- [ ] Word-level timing matches audio
- [ ] Speed control works (0.5x, 1x, 2x)

## Related Skills

- `skill://voice-ai-agent` — Call handling with custom voices
- `skill://remotion` — Video with synced subtitles
- `skill://content-factory` — Automated content generation

## Overview

> Section content — see SKILL.md body for full details.
