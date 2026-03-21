# autodroid-instagram-agent

Control Instagram Android app via ADB automation. No API key required.

## Package
- `com.instagram.android`

## Install Instagram First

```bash
# Check if installed
python3 scripts/instagram_agent.py status

# Install via Play Store agent
python3 ../autodroid-playstore-agent/scripts/playstore_agent.py install --package com.instagram.android
```

## Quick Start

```bash
cd /mnt/data/berkahkarya/skills/1ai-skills/automation/autodroid-instagram-agent

# Status
python3 scripts/instagram_agent.py status

# Open Instagram
python3 scripts/instagram_agent.py open

# View feed
python3 scripts/instagram_agent.py feed

# Open DM inbox
python3 scripts/instagram_agent.py inbox

# Screenshot
python3 scripts/instagram_agent.py screenshot

# Start API server
python3 scripts/instagram_agent.py server --port 8769
```

## API Endpoints (port 8769)

| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Device + install status |
| POST | /open | Launch Instagram |
| GET | /feed | View main feed |
| GET | /inbox | Open DM inbox |
| GET | /screenshot | Take screenshot |
| GET | /docs | Swagger UI |

## Output Format

```json
{"ok": true, "installed": false, "package": "com.instagram.android", "device": "..."}
```

## Features
- ✅ State-based retry (3x)
- ✅ Popup/permission dismissal
- ✅ DM inbox navigation
- ✅ FastAPI server
