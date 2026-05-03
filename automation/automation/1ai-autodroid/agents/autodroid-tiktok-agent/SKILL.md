---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Tiktok Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# autodroid-tiktok-agent

Control TikTok Android app via ADB automation. No API key required.

## Package
- `com.ss.android.ugc.trill` (Indonesia/Global)

## Quick Start

```bash
cd /mnt/data/berkahkarya/skills/1ai-skills/automation/autodroid-tiktok-agent

# Status check
python3 scripts/tiktok_agent.py status

# Open TikTok
python3 scripts/tiktok_agent.py open

# Go to Inbox
python3 scripts/tiktok_agent.py inbox

# Go to Profile
python3 scripts/tiktok_agent.py profile

# Screenshot current state
python3 scripts/tiktok_agent.py screenshot

# Start API server
python3 scripts/tiktok_agent.py server --port 8766
```

## API Endpoints (port 8766)

| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Device + app info |
| POST | /open | Launch TikTok |
| GET | /inbox | Navigate to inbox |
| GET | /profile | Navigate to profile |
| GET | /screenshot | Take screenshot |
| GET | /docs | Swagger UI |

## Output Format

```json
{
  "ok": true,
  "installed": true,
  "package": "com.ss.android.ugc.trill",
  "device": "SGZTONV4OBL74TJZ",
  "model": "2409BRN2CY",
  "android_version": "14"
}
```

## Device Coordinates (720x1640)

| Element | X | Y |
|---------|---|---|
| Bottom: Beranda | 72 | 1505 |
| Bottom: Toko | 216 | 1505 |
| Bottom: Post (+) | 360 | 1505 |
| Bottom: KotakMasuk | 504 | 1505 |
| Bottom: Profil | 648 | 1505 |

## Multi-Device

```bash
python3 scripts/tiktok_agent.py status --device SERIAL1
python3 scripts/tiktok_agent.py server --port 8766 --device SERIAL1
```

## Features
- ✅ State-based retry (3x attempts)
- ✅ Popup/onboarding dismissal
- ✅ Always returns JSON
- ✅ Multi-device support
- ✅ FastAPI server with Swagger docs
