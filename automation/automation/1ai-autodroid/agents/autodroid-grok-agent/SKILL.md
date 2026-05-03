---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Grok Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# AutoDroid Grok Agent

> Control Grok AI Android app via ADB automation. Chat, image generation, video creation — no API key needed.

---

## Overview

| Property | Value |
|----------|-------|
| Port | 8773 |
| Package | `ai.x.grok` |
| Device | Redmi 2409BRN2CY (Android 14, 720x1640) |
| Account | favstore649@gmail.com |
| Status | ✅ Production Ready |

---

## Commands

### `status`
Check Grok installation and connected device.
```bash
python3 scripts/grok_agent.py status
```

### `open`
Wake device and launch Grok app.
```bash
python3 scripts/grok_agent.py open
```

### `login`
Authenticate via Google, Email, or X.
```bash
python3 scripts/grok_agent.py login --method google
python3 scripts/grok_agent.py login --method email --email user@email.com --password pass
```

### `chat`
Send prompt, get response. Supports Think + DeepSearch modes.
```bash
python3 scripts/grok_agent.py chat --prompt "Siapa kamu?"
python3 scripts/grok_agent.py chat --prompt "Step by step plan" --think --deepsearch
python3 scripts/grok_agent.py chat --prompt "test" --timeout 60
```
**Response:**
```json
{
  "ok": true,
  "response": "Halo! Aku Grok...",
  "mode": {"think": false, "deepsearch": false},
  "screenshot_path": "/path/to/screen.png",
  "attempt": 1
}
```

### `imagine`
Generate AI image from text prompt. Returns 2 image variants.
```bash
python3 scripts/grok_agent.py imagine --prompt "mountain volcano sunset Indonesia"
python3 scripts/grok_agent.py imagine --prompt "cute cat piano cartoon" --timeout 90
```
**Response:**
```json
{
  "ok": true,
  "image_path": "/home/openclaw/.openclaw/workspace/downloads/grok_imagine_1.png",
  "prompt": "cute cat piano cartoon",
  "screenshot_path": "/path/to/screen.png"
}
```
**Notes:**
- Saves HQ PNG from device sdcard (`/sdcard/Pictures/`)
- 2 image variants generated per prompt
- Free tier: unlimited (subject to rate limits)

### `video`
Generate animated video via Grok "Animate your photos" feature.
```bash
python3 scripts/grok_agent.py video --timeout 120
python3 scripts/grok_agent.py video --photo /path/to/photo.jpg
```
**Response (free tier):**
```json
{
  "ok": true,
  "video_info": "Generated",
  "note": "Video visible on screen. Download requires SuperGrok.",
  "screenshot_path": "/path/to/screen.png"
}
```
**⚠️ Limitation: FLAG_SECURE**
- Grok enables Android `FLAG_SECURE` — screencap/screenrecord blocked inside app
- Video file stored in **internal app storage** (not accessible without root)
- Download button requires **SuperGrok premium** (Rp 489.000/bulan)
- Free tier: can generate + preview 6s 480p videos, cannot export

### `screenshot`
Capture current screen state.
```bash
python3 scripts/grok_agent.py screenshot --out /tmp/grok.png
```

### `scroll`
Scroll chat history.
```bash
python3 scripts/grok_agent.py scroll --direction down --count 3
```

### `server`
Start FastAPI HTTP server on port 8773.
```bash
python3 scripts/grok_agent.py server --port 8773
# Docs: http://localhost:8773/docs
```

---

## HTTP API (FastAPI)

Start server: `python3 scripts/grok_agent.py server`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/status` | POST | Device + app info |
| `/chat` | POST | Send chat prompt |
| `/imagine` | POST | Generate image |
| `/video` | POST | Generate video |
| `/screenshot` | GET | Capture screen |
| `/scroll` | GET | Scroll chat |

**Chat:**
```bash
curl -X POST http://localhost:8773/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello Grok", "timeout": 30}'
```

**Imagine:**
```bash
curl -X POST http://localhost:8773/imagine \
  -d '{"prompt": "sunset mountain Indonesia", "timeout": 90}'
```

**Video:**
```bash
curl -X POST http://localhost:8773/video \
  -d '{"timeout": 120}'
```

---

## Feature Status

| Feature | Tier | Status | Notes |
|---------|------|--------|-------|
| Chat | Free | ✅ Working | Clean responses, Indonesian support |
| Image Generation | Free | ✅ Working | 2 variants, HQ PNG saved locally |
| Video Preview | Free | ✅ Working | 6s 480p, viewable in-app |
| Video Download | SuperGrok | ❌ Paid | Rp 489K/bulan |
| HD 720p Video | SuperGrok | ❌ Paid | Requires subscription |
| 30s Videos | SuperGrok | ❌ Paid | Max 6s free tier |

---

## Known Limitations

### FLAG_SECURE
Grok enables Android `FLAG_SECURE` across the entire app. This means:
- `adb exec-out screencap -p` → black screen (blocked)
- `adb shell screenrecord` → black screen (blocked)
- Only screenshots taken BEFORE video player opens work

**Workaround:** Screenshot taken immediately after launch, before FLAG_SECURE activates.

### Keyboard Autocorrect
Indonesian Gboard corrupts text input (e.g., "siapa kamu" → "sip km").

**Fix applied:** Switch to Xiaomi keyboard:
```bash
adb shell settings put secure default_input_method \
  com.preff.kb.xm/com.preff.kb.LatinIME
```

### Age Verification
First launch shows age verification popup.

**Fix:** Script auto-selects year 1990 + taps Continue.

### Video File Access
Grok stores generated videos in internal app storage (`/data/data/ai.x.grok/`). Not accessible without:
- Root access, OR
- `adb backup` (blocked on Android 14), OR
- SuperGrok (enables Download button)

---

## UI Coordinates (720x1640, Android 14)

```
Tab Bar:
  Ask tab:     (271, 131)
  Imagine tab: (413, 131)
  New Chat:    (664, 132)

Chat Screen:
  Input field: bounds [16,790][704,1020], center (364,905)
  Send button: (646, 968)

Imagine/Video Screen:
  Create Videos: (559, 739) on Chat tab, or (559, 1250) after scroll
  Animate thumbnails: y=498, x=[157, 440, 655]
  Funky Dance template: (129, 1161)
  Try template button: (251, 1181)

Login/Onboarding:
  Google button:  (360, 878)
  Email button:   (360, 1014)
  X button:       (360, 1150)
  Skip:           (649, 131)
  
Age verification:
  Year 1990 area: scroll in picker
  Continue: bottom of screen
```

---

## File Locations

```
Script:     scripts/grok_agent.py
Server:     grok_server.py
Downloads:  ~/.openclaw/workspace/downloads/
  - grok_chat.png          (chat screenshot)
  - grok_imagine_*.png     (generated images — HQ from device)
  - grok_hq_volcano1.png   (mountain volcano at sunset, 1.3MB)
  - grok_hq_volcano2.png   (cat playing piano, 1.6MB)
  - grok_video_result.png  (video player screenshot)
Device images:
  /sdcard/Pictures/1774058207000.png  (1.3MB)
  /sdcard/Pictures/1774059817123.png  (1.6MB)
```

---

## Test Commands

```bash
# Full smoke test
python3 scripts/grok_agent.py status
python3 scripts/grok_agent.py chat --prompt "siapa kamu jelaskan singkat"
python3 scripts/grok_agent.py imagine --prompt "cat cartoon"
python3 scripts/grok_agent.py video --timeout 60

# Via HTTP
curl http://localhost:8773/health
curl -X POST http://localhost:8773/chat -d '{"prompt":"test"}'
```

---

## Last Tested
- **Date:** 2026-03-21
- **Device:** Redmi 2409BRN2CY (SGZTONV4OBL74TJZ)
- **Android:** 14
- **Grok version:** ~2026-03
- **Account:** favstore649@gmail.com
- **Chat:** ✅ Working (response: "Halo broo! Siap banget nih...")
- **Imagine:** ✅ Working (cat cartoon PNG saved locally)
- **Video:** ✅ Generated (6s 480p, preview only — download = paid)
