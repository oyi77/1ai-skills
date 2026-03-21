# autodroid-flow-agent

Android automation agent for **Google Flow** (labs.google/flow) video generation.
Automates the Chrome browser on Android via ADB UIAutomation to generate MP4 videos using Google's Veo 3.1 model.

## Overview

- **Platform:** Google Flow (web app in Chrome)
- **Model:** Veo 3.1 (Google's best video model)
- **Free tier:** 100 credits on signup + 50 daily credits
- **Port:** 8774
- **Output:** MP4 video pulled to `~/.openclaw/workspace/downloads/`

## Device Config

| Property | Value |
|----------|-------|
| Device | Redmi 2409BRN2CY |
| Android | 14 |
| Resolution | 720x1640 |
| ADB Serial | SGZTONV4OBL74TJZ |
| Chrome pkg | com.android.chrome |

## Usage

```bash
# Check device + Chrome status
python flow_agent.py status --device SGZTONV4OBL74TJZ

# Open Google Flow in Chrome
python flow_agent.py open --device SGZTONV4OBL74TJZ

# Handle Google login (if required)
python flow_agent.py login --device SGZTONV4OBL74TJZ

# Generate video from prompt (main command)
python flow_agent.py text2video \
  --prompt "A cinematic sunset over mountains with dramatic clouds" \
  --timeout 120 \
  --device SGZTONV4OBL74TJZ

# Take screenshot
python flow_agent.py screenshot --out /tmp/screen.png --device SGZTONV4OBL74TJZ

# Start FastAPI server
python flow_agent.py server --port 8774 --device SGZTONV4OBL74TJZ
```

## FastAPI Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /status | Device + Chrome status |
| POST | /open | Open URL in Chrome |
| POST | /text2video | Generate video from prompt |
| GET | /screenshot | Capture current screen |

### POST /text2video

```json
{
  "prompt": "A timelapse of city lights at night",
  "timeout": 120,
  "device": "SGZTONV4OBL74TJZ"
}
```

**Success response:**
```json
{
  "ok": true,
  "video_path": "/home/openclaw/.openclaw/workspace/downloads/flow_video_20260321_175423.mp4",
  "device_path": "/sdcard/Download/flow_video.mp4",
  "prompt": "A timelapse of city lights at night",
  "timestamp": "2026-03-21T17:54:23"
}
```

## Error Codes

| Error | Meaning | Action |
|-------|---------|--------|
| `login_required` | Not logged into Google | Run `login` command or sign in manually |
| `credits_exhausted` | Daily/total credits used up | Wait 24h for reset |
| `timeout` | Generation took too long | Increase `--timeout` or retry |
| `ui_not_found` | Flow page UI not detected | Check Chrome, scroll, retry |
| `generate_btn_not_found` | Generate button missing | Check if page loaded correctly |
| `video_on_screen` | Video ready but download failed | Download manually from device |

## text2video Flow

```
1. Open labs.google/flow in Chrome
2. Detect page state (login? credits? UI ready?)
3. Find text input field via UIAutomation XML dump
4. Type prompt word-by-word (Xiaomi KB, no autocorrect)
5. Click Generate button
6. Poll UI every 3s for generation completion (up to timeout)
7. Click Download button
8. Wait for .mp4 in /sdcard/Download/
9. adb pull → ~/.openclaw/workspace/downloads/flow_video_{ts}.mp4
10. Return JSON with local path
```

## Dependencies

- Python 3.8+
- `adb` in PATH
- `fastapi` + `uvicorn` (server mode only): `pip install fastapi uvicorn`

## Notes

- Login must be done manually (Google OAuth can't be automated via ADB)
- Xiaomi keyboard (`com.preff.kb.xm`) used to prevent autocorrect mangling prompts
- Generation time varies: typically 30-90s for Veo 3.1
- Script retries 3x with exponential backoff on transient failures
- All commands return JSON: `{"ok": true/false, ...}`
