# autodroid-gemini-agent — Production Ready

Control Google Gemini Android app via ADB. No API key needed.

## Status: ✅ VERIFIED

- ✅ Chat: tested & working
- ✅ Image generation: tested & working (saves actual PNG from device)
- ✅ API server: FastAPI + uvicorn ready
- ✅ Multi-device: supports --device SERIAL
- ✅ Documentation: flows + coordinates + learnings

## Quick Start

```bash
# Chat
python3 scripts/gemini_agent.py chat --prompt "hello gemini"

# Image
python3 scripts/gemini_agent.py imagine --prompt "sunset over mountains"

# Server
python3 scripts/gemini_agent.py server --port 8765

# Then: curl -X POST http://localhost:8765/chat -H "Content-Type: application/json" -d '{"prompt":"hello"}'
```

## Key Files

- `scripts/gemini_agent.py` — 300+ lines, all subcommands + API
- `SKILL.md` — Full reference
- `references/flows.md` — UI flows + actual coordinates

## What's Inside

```
scripts/gemini_agent.py
├── status       — check app installed
├── chat         — send prompt, get response
├── imagine      — generate image, save PNG file
├── screenshot   — capture device screen
└── server       — FastAPI + uvicorn (POST /chat, POST /imagine, GET /status)
```

## Real-World Learnings

- `keyevent 224` for WAKEUP (not 26)
- `adb exec-out screencap -p` for direct screenshot
- Type word-by-word (avoids URL encoding)
- Tap "Kirim" button, not ENTER
- Image save: dump UI → find node → tap → MediaStore query
- Always new chat before typing
- 25s+ for image generation

## Hardware Tested

- Device: Redmi 2409BRN2CY (Android 14)
- Resolution: 720x1640
- Package: com.google.android.apps.bard

## Performance

- Chat response: 15-45s
- Image generation: 25-40s
- Screenshot: <1s
- API overhead: <100ms
