---
name: voice-ai
description: Voice AI — text-to-speech (ElevenLabs, OpenAI TTS), speech-to-text (Whisper), voice cloning, real-time voice agents
---

## Overview

Voice AI covers TTS, STT, voice cloning, and real-time conversational agents. Integrates ElevenLabs, OpenAI TTS, Whisper, and Vapi/Bland/Retell.

## Capabilities

- Text-to-speech (ElevenLabs, OpenAI TTS)
- Audio transcription (Whisper, Deepgram)
- Voice cloning from samples
- Real-time voice agents (Vapi, Bland, Retell)
- Audio processing (pydub)

## When to Use

- Voiceovers for videos/podcasts
- Voice-based customer support
- Transcribing meetings/interviews
- Audiobook generation

## Pseudo Code

### OpenAI TTS
```python
from openai import OpenAI
client = OpenAI()
resp = client.audio.speech.create(model="tts-1-hd", voice="nova", input="Hello!")
resp.stream_to_file("output.mp3")
```

### ElevenLabs Clone
```python
import requests
resp = requests.post("https://api.elevenlabs.io/v1/voices/add",
    headers={"xi-api-key": KEY}, files={"files": [open("sample.mp3","rb")]}, data={"name":"Clone"})
voice_id = resp.json()["voice_id"]
resp = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    headers={"xi-api-key": KEY}, json={"text":"Hello!","model_id":"eleven_multilingual_v2"})
```

### Whisper Transcription
```python
from openai import OpenAI
client = OpenAI()
with open("meeting.mp3","rb") as f:
    t = client.audio.transcriptions.create(model="whisper-1", file=f, response_format="verbose_json")
for s in t.segments: print(f"[{s['start']:.1f}s] {s['text']}")
```

### Vapi Agent
```python
import requests
requests.post("https://api.vapi.ai/assistant",
    headers={"Authorization": f"Bearer {KEY}"},
    json={"name":"Agent","model":{"provider":"openai","model":"gpt-4o","systemPrompt":"Help user."},
           "voice":{"provider":"11labs","voiceId":"nova"},"firstMessage":"Hi!"})
```

## Common Patterns

- Podcast: script → TTS per speaker → mix with intro/outro → export
- Real-time: websocket stream → Deepgram/Whisper → live transcript
- Clone: 3+ min samples → ElevenLabs clone → generate speech
