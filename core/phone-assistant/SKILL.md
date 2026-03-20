# Phone-Based Personal Assistant

> Access OpenClaw via voice -- phone calls or Telegram voice messages

## Overview

Voice interface for OpenClaw. Two options:
- **Option A (Twilio)** -- phone call webhook: STT -> agent -> TTS response
- **Option B (Telegram voice)** -- zero setup, already works via Telegram bot

Option B is recommended as it requires no additional setup.

## Option A: Twilio (Phone Calls)

### Architecture
```
Phone call -> Twilio -> Webhook (Flask/FastAPI)
  -> STT (Whisper) -> Agent (OmniRoute) -> TTS -> Twilio response
```

### Setup
1. Create Twilio account, get phone number
2. Set webhook URL to your server endpoint
3. Configure environment:
   ```bash
   export TWILIO_ACCOUNT_SID="..."
   export TWILIO_AUTH_TOKEN="..."
   export TWILIO_PHONE_NUMBER="+1..."
   ```
4. Deploy webhook handler

### Cost
- Twilio: ~$1/month for number + per-minute charges
- Whisper API: ~$0.006/minute (or free with local whisper)

## Option B: Telegram Voice (Recommended)

### Architecture
```
Telegram voice message -> Bot receives audio
  -> Whisper transcription -> OmniRoute processing -> Text reply
```

### Setup
Already configured via existing Telegram bot. Just send voice messages.

### How It Works
1. User sends voice message to Telegram bot
2. Bot downloads .ogg audio file
3. `voice_handler.py` transcribes via Whisper
4. Transcription sent to OmniRoute for processing
5. Response sent back as text (or TTS audio)

## Usage

```bash
# Process a voice file directly
python scripts/voice_handler.py --file /path/to/audio.ogg

# Process with explicit model
python scripts/voice_handler.py --file audio.mp3 --whisper-model base

# Transcribe only (no agent processing)
python scripts/voice_handler.py --file audio.ogg --transcribe-only

# Process text as if it were voice input (for testing)
python scripts/voice_handler.py --text "What's the weather like?"
```

## Dependencies

```bash
# Option 1: OpenAI Whisper (local, free)
pip install openai-whisper

# Option 2: Faster Whisper (faster, less memory)
pip install faster-whisper
```

## Files

- `SKILL.md` -- this file
- `../../scripts/voice_handler.py` -- voice processing script
