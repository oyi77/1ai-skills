---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Pixverse Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# PixVerse Android Automation Agent

> ADB-based automation for PixVerse AI Video Generator on Android.
> Pure Python, no root, UIAutomator-based, FastAPI server on port 8775.

## Overview

Automates PixVerse app (`com.pixverse.app`) on Android via ADB UIAutomation.
Follows the same pattern as Gemini/Grok agents in this automation suite.

**Device:** Redmi 2409BRN2CY, Android 14, 720×1640  
**ADB Serial:** SGZTONV4OBL74TJZ  
**Port:** 8775  
**Free tier:** ~5 videos/day, no watermark

## Usage

```bash
# Status check
python scripts/pixverse_agent.py status --device SGZTONV4OBL74TJZ

# Open app
python scripts/pixverse_agent.py open --device SGZTONV4OBL74TJZ

# Login
python scripts/pixverse_agent.py login --method google --device SGZTONV4OBL74TJZ

# Generate video from text
python scripts/pixverse_agent.py text2video \
  --prompt "A cat dancing in neon lights at night" \
  --device SGZTONV4OBL74TJZ

# Animate an image
python scripts/pixverse_agent.py image2video \
  --image /path/to/image.jpg \
  --prompt "Slow zoom out with particle effects" \
  --device SGZTONV4OBL74TJZ

# Screenshot
python scripts/pixverse_agent.py screenshot --device SGZTONV4OBL74TJZ

# Scroll feed
python scripts/pixverse_agent.py scroll --direction down --count 3 --device SGZTONV4OBL74TJZ

# Start FastAPI server
python scripts/pixverse_agent.py server --port 8775 --device SGZTONV4OBL74TJZ
```

## FastAPI Endpoints

```
GET  /health               → {"ok": true, "service": "pixverse-agent"}
GET  /status               → device + app status
POST /open                 → wake + launch app
POST /login                → {"method": "google"|"email"}
POST /text2video           → {"prompt": "...", "timeout": 180}
POST /image2video          → {"image_path": "...", "prompt": "...", "timeout": 180}
GET  /screenshot           → returns PNG image
GET  /scroll               → ?direction=down&count=3
```

## Output Paths

- **Videos:** `~/.openclaw/workspace/downloads/pixverse_video_{timestamp}.mp4`
- **Screenshots:** `~/.openclaw/workspace/downloads/screenshots/`

## Error Codes

| Error | Meaning |
|-------|---------|
| `app_not_installed` | PixVerse not installed — see `install` field for Play Store command |
| `daily_limit_reached` | Free tier quota exhausted — resets in 24h |
| `login_required` | User must login first |
| `generation_failed` | Generation error — screenshot saved |
| `generation_timeout` | Did not complete within timeout — increase `--timeout` |
| `device_not_found` | ADB device not connected/authorized |

## Dependencies

```bash
# Core (always needed)
pip install fastapi uvicorn pydantic

# ADB must be in PATH
adb --version
```

## Architecture

- **ADB helpers:** `adb()`, `wake()`, `dump_ui()`, `tap()`, `type_prompt()`
- **State detection:** `detect_state()` — HOME | CREATE | GENERATING | RESULT | LOGIN | DAILY_LIMIT
- **Video detection:** MediaStore query via `content://media/external_primary/video/media`
- **Retry:** 3× exponential backoff on all critical operations
- **Natural delays:** randomized 0.3–0.8s between taps

## Notes

- Xiaomi keyboard (no autocorrect) used for text input
- UI dump saved to `/sdcard/pv.xml` → pulled to `/tmp/pv_ui.xml`
- Video pulled from device gallery after download completes
- MediaStore timestamp comparison used to detect newly generated videos
