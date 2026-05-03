---
persona:
  name: "Domain Expert"
  title: "Master of Autodroid Playstore Agent"
  expertise: ['Agents Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']

---

# autodroid-playstore-agent v2.0

Robust Play Store automation via ADB. Install/uninstall apps, search, take screenshots.

## Install Strategy (3 layers)

1. **market:// URI** → direct package page → find Instal button by UI dump
2. **Search by name** → tap first result → find Instal button
3. Graceful failure → JSON error + screenshot of current state

## Quick Start

```bash
cd /mnt/data/berkahkarya/skills/1ai-skills/automation/autodroid-playstore-agent

# List devices
python3 scripts/playstore_agent.py devices

# Check if installed
python3 scripts/playstore_agent.py status --package com.instagram.android

# Install by package ID (most reliable)
python3 scripts/playstore_agent.py install --package com.instagram.android

# Install by name (fallback)
python3 scripts/playstore_agent.py install --name "Instagram"

# Install by both (safest)
python3 scripts/playstore_agent.py install --package com.instagram.android --name "Instagram"

# Search
python3 scripts/playstore_agent.py search --query "photo editor"

# Uninstall
python3 scripts/playstore_agent.py uninstall --package com.instagram.android

# Screenshot
python3 scripts/playstore_agent.py screenshot

# Start API server
python3 scripts/playstore_agent.py server --port 8771
```

## Output (always JSON)

```json
// status
{"ok": true, "installed": true, "package": "com.instagram.android", "device": "SGZTONV4OBL74TJZ"}

// install - success
{"ok": true, "installed": true, "package": "...", "strategy": "market_uri", "screenshot_path": "..."}

// install - already installed
{"ok": true, "already_installed": true, "package": "..."}

// install - by name only (can't verify)
{"ok": true, "installed": null, "note": "Install tapped but cannot verify (no --package given)"}

// install - failed
{"ok": false, "error": "Install button not found after all strategies", "strategies_tried": [...], "screenshot_path": "..."}
```

## API Endpoints (port 8771)

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| GET | /health | — | Server health |
| GET | /devices | — | List ADB devices |
| GET | /status | `?package=` | Check install |
| POST | /open-store | — | Launch Play Store |
| GET | /search | `?query=` | Search apps |
| POST | /install | `{package, name, wait}` | Install app |
| POST | /uninstall | `{package}` | Uninstall |
| GET | /screenshot | — | Screenshot |
| GET | /docs | — | Swagger UI |

## Graceful Error Handling

- Missing `--package` and `--name` → `{"ok": false, "error": "Provide --package or --name"}`
- Already installed → `{"ok": true, "already_installed": true, ...}` (idempotent)
- Instal button not found → tries next strategy
- All strategies failed → returns screenshot for debugging

## Multi-Device

```bash
python3 scripts/playstore_agent.py install --package com.instagram.android --device SERIAL1
```

## Features
- ✅ 3-strategy install with auto-fallback
- ✅ Always returns JSON (never crashes with argparse error)
- ✅ Already-installed check (idempotent)
- ✅ Wake device before all operations
- ✅ Popup/promo dismissal
- ✅ Wait-for-install polling (120s timeout)
- ✅ FastAPI server
- ✅ Multi-device support
