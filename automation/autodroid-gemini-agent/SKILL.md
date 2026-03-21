# AutoDroid Gemini Agent

> Control Google Gemini Android app via ADB automation. Chat + image generation — no API key needed.

---

## Overview

| Property | Value |
|----------|-------|
| Port | 8765 |
| Package | `com.google.android.apps.bard` |
| Device | Redmi 2409BRN2CY (Android 14, 720x1640) |
| Status | ✅ Production Ready — FULLY TESTED |

---

## Commands

### `status`
```bash
python3 scripts/gemini_agent.py status
```

### `open`
```bash
python3 scripts/gemini_agent.py open
```

### `login`
```bash
python3 scripts/gemini_agent.py login
# Uses device Google account (auto-detect)
```

### `chat`
```bash
python3 scripts/gemini_agent.py chat --prompt "What is quantum computing?"
python3 scripts/gemini_agent.py chat --prompt "Jelaskan ini" --timeout 45
```
**Response:**
```json
{
  "ok": true,
  "response": "Quantum computing adalah...",
  "screenshot_path": "/path/to/screenshot.png",
  "attempt": 1
}
```

### `imagine`
Generate AI image. Saves actual PNG pulled from device sdcard.
```bash
python3 scripts/gemini_agent.py imagine --prompt "sunrise over mountain"
python3 scripts/gemini_agent.py imagine --prompt "robot in Jakarta" --timeout 60
```
**Response:**
```json
{
  "ok": true,
  "image_path": "/home/openclaw/.openclaw/workspace/downloads/gemini_imagine_1.png",
  "prompt": "sunrise over mountain"
}
```
**Notes:**
- Gemini does NOT use FLAG_SECURE → images can be pulled directly
- File saved via MediaStore query (no root needed)
- Free tier: ~5 images/day limit

### `screenshot`
```bash
python3 scripts/gemini_agent.py screenshot --out /tmp/screen.png
```

### `server`
```bash
python3 scripts/gemini_agent.py server --port 8765
# Docs: http://localhost:8765/docs
```

---

## HTTP API

| Endpoint | Method |
|----------|--------|
| `/health` | GET |
| `/api/gemini/status` | POST |
| `/api/gemini/chat` | POST |
| `/api/gemini/imagine` | POST |
| `/api/gemini/screenshot` | POST |

```bash
# Chat
curl -X POST http://localhost:8765/api/gemini/chat \
  -d '{"prompt": "Hello Gemini", "timeout": 30}'

# Imagine
curl -X POST http://localhost:8765/api/gemini/imagine \
  -d '{"prompt": "cat cartoon", "timeout": 60}'
```

---

## Feature Status

| Feature | Tier | Status |
|---------|------|--------|
| Chat | Free | ✅ Working |
| Image Generation | Free | ✅ Working — file saved locally |
| Video Generation | ❌ Not in Gemini app | Use Google Flow instead |

**No FLAG_SECURE** — screencap + file pull works normally.

---

## Last Tested
- **Date:** 2026-03-21
- **Chat:** ✅ Working
- **Imagine:** ✅ Working (PNG pulled from `/sdcard/Pictures/`)
- **Video:** ❌ Not available in Gemini Android app
