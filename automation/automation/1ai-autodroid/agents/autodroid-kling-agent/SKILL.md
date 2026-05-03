---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Kling Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# autodroid-kling-agent

Android automation agent for **Kling AI: AI Image&Video (Kling 3.0)** — generates videos via ADB UIAutomation without root.

> **v2.0** — Rewritten with ALL learnings from live testing sessions (March 2026)

## App Info (CONFIRMED from live testing)

- **Package:** `kling.ai.video.chat`
- **Main Activity:** `kling.ai.video.chat/.MainActivityPagerActivity`
- **Device:** Redmi Note 12, Android 14, 720x1640px
- **ADB Serial:** `SGZTONV4OBL74TJZ`
- **Login:** favstore649@gmail.com (Google OAuth)
- **I2V Cost:** ~144 credits per 5s generation (192 → 48 confirmed)

## Setup

```bash
# Verify ADB connection
adb -s SGZTONV4OBL74TJZ devices

# Install optional dependencies (server mode only)
pip install fastapi uvicorn

# Make executable
chmod +x scripts/kling_agent.py

# Quick test
python3 scripts/kling_agent.py status
```

## CLI Usage

```bash
# Generate video from text (T2V)
python3 scripts/kling_agent.py t2v --prompt "A serene mountain lake at sunset"
python3 scripts/kling_agent.py t2v --prompt "Cinematic aerial city shot" --duration 10s

# Generate video from image (I2V Motion Control)
python3 scripts/kling_agent.py i2v --image /path/photo.jpg
python3 scripts/kling_agent.py i2v --image /path/photo.jpg --motion "Chinese trend"
python3 scripts/kling_agent.py i2v --image /path/photo.jpg --prompt "gentle breeze"

# Check credits
python3 scripts/kling_agent.py credits

# Check device/app status
python3 scripts/kling_agent.py status

# Download latest video from My Space
python3 scripts/kling_agent.py download

# Wake device + launch app
python3 scripts/kling_agent.py open

# Take screenshot
python3 scripts/kling_agent.py screenshot --out /tmp/screen.png

# Debug UI dump (for development)
python3 scripts/kling_agent.py debug

# Use specific device
python3 scripts/kling_agent.py --device SGZTONV4OBL74TJZ t2v --prompt "..."

# Start HTTP server (port 8775)
python3 scripts/kling_agent.py server --port 8775
```

## JSON Response Format

All commands output JSON to stdout.

### Success (T2V)
```json
{
  "status": "success",
  "type": "t2v",
  "output": "/home/openclaw/.openclaw/workspace/downloads/kling_t2v_1711012345.mp4",
  "device_path": "/storage/emulated/0/DCIM/Kling/video.mp4",
  "prompt": "A serene mountain lake at sunset",
  "duration": "5s",
  "credits_used": 144,
  "credits_remaining": 48,
  "duration_seconds": 47
}
```

### Success (I2V)
```json
{
  "status": "success",
  "type": "i2v",
  "output": "/home/openclaw/.openclaw/workspace/downloads/kling_i2v_1711012345.mp4",
  "image_path": "/path/to/input.jpg",
  "motion_template": "Chinese trend",
  "prompt": "",
  "credits_used": 144,
  "credits_remaining": 48,
  "duration_seconds": 52
}
```

### Error
```json
{
  "status": "error",
  "error": "insufficient_credits"
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| `app_not_installed` | Kling AI not found on device |
| `no_devices_connected` | No ADB devices available |
| `launch_failed` | Could not bring Kling to foreground |
| `image_not_found` | Input image path doesn't exist |
| `image_upload_failed` | adb push failed |
| `creator_screen_not_reached` | Could not navigate to create screen |
| `generate_button_not_found` | Generate button not found in UI |
| `insufficient_credits` | Not enough credits for generation |
| `credits_exhausted` | Daily/total credits used up |
| `generation_failed` | Video generation error in app |
| `network_error` | Network error during generation |
| `timeout` | Generation exceeded timeout |

## Architecture

```
kling_agent.py (~1500 lines)
├── Constants (exact coords from live testing)
├── Core ADB helpers (adb, screencap, tap, swipe, wake)
├── Text input (type_prompt_safe — + for spaces workaround)
├── UI dump/parse (dump_ui, find_element_by_text, tap_element_by_text)
├── Screen state detection (get_screen_state → home|creator|gallery|processing|video|myspace)
├── App lifecycle (launch_kling, ensure_kling_foreground, force_stop_kling)
├── Credits (get_credits — parses "🔥 NNN Generate" pattern)
├── Image upload (upload_image → adb push + MediaScanner)
├── Gallery picker (_select_image_in_gallery — avoids Camera cell)
├── Generate button (tap_generate_button — taps clickable parent, not text)
├── Generation waiter (wait_for_generation — 5min timeout, progress logging)
├── Video download (download_latest_output, wait_for_new_video)
├── Commands: t2v_generate, i2v_motion_control, cmd_status, cmd_credits, cmd_download
└── FastAPI server (port 8775) + CLI entry point
```

## Critical Learnings (from live testing)

### ⚠️ Navigation Coordinates (720x1640)
```
Bottom nav bar (y=1413):
  Home:     (72,  1413)
  Explore:  (216, 1413)
  Create:   (263, 1413)  ← Primary
  Assets:   (368, 1413)
  My Space: (476, 1413)

CRITICAL: Never tap y > 1530 — hits Android device nav buttons!
```

### ⚠️ Generate Button
```
The "Generate" text node at (603, 843) is NOT clickable.
The PARENT node at (573, 843) with bounds [475,811][672,875] IS clickable.
Agent taps parent coords, not text.
```

### ⚠️ Text Input (+ for spaces)
```python
# adb input text doesn't handle spaces reliably
# Workaround: use + as word separator (Kling accepts this)
adb shell input text "word1+word2+word3"
```

### ⚠️ Gallery Upload
```
- Camera is at Row1 Col1 (x=90, y=167) — AVOID!
- Most recent photo: Row1 Col2 (x=270, y=167) 
- Permission dialog: "Izinkan semua" at (360, 1304)
- Done/confirm: (589, 1303)
```

### ⚠️ Green Send Arrow (T2V Omni mode)
```
Green ImageView: (644, 1362), bounds [616,1334][672,1390]
Green pixel: RGB(71, 169, 46)
```

### Credit Costs
- I2V 5s: ~144 credits (confirmed: 192→48)
- Credits displayed as: "🔥 192 Generate" in UI

## Motion Templates (I2V)

Available motion templates (select via `--motion`):
- `Chinese trend`
- `Slight movement`
- `Zoom in`
- `Zoom out`
- `Pan left`
- `Pan right`
- `Rotate`
- `Wave`

## FastAPI Server

```bash
python3 scripts/kling_agent.py server
# Starts at http://0.0.0.0:8775
```

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/status` | Device + app status |
| GET | `/credits` | Credit balance |
| POST | `/open` | Launch app |
| POST | `/t2v` | Text-to-video |
| POST | `/i2v` | Image-to-video |
| GET | `/download` | Download latest video |
| GET | `/screenshot` | Capture screen |
| GET | `/debug/ui` | Dump UI hierarchy |

## Output Files

- Videos: `~/.openclaw/workspace/downloads/kling_{t2v|i2v}_{timestamp}.mp4`
- Screenshots: `~/.openclaw/workspace/downloads/kling_ss_{timestamp}.png`
- UI dumps: `~/.openclaw/workspace/downloads/kling_ui_dump_{timestamp}.xml`

## Notes

- **Retry:** All main commands retry 3x with exponential backoff
- **Timeout:** Generation waits up to 5 minutes (300s) by default
- **FLAG_SECURE:** If screenshots appear black, `flag_secure: true` is returned
- **Login:** Pre-authenticated as favstore649@gmail.com — no login flow needed
- **Screen safety:** Taps below y=1530 are automatically blocked (Android nav bar protection)
