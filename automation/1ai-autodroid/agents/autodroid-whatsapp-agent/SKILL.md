# autodroid-whatsapp-agent

Control WhatsApp Android app via ADB automation. No API key required.

## Package
- `com.whatsapp`

## Quick Start

```bash
cd /mnt/data/berkahkarya/skills/1ai-skills/automation/autodroid-whatsapp-agent

# Status check
python3 scripts/whatsapp_agent.py status

# Open WhatsApp
python3 scripts/whatsapp_agent.py open

# List chats
python3 scripts/whatsapp_agent.py chats

# Send message
python3 scripts/whatsapp_agent.py send --contact "John" --message "Halo bro"

# Screenshot
python3 scripts/whatsapp_agent.py screenshot

# Start API server
python3 scripts/whatsapp_agent.py server --port 8768
```

## API Endpoints (port 8768)

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /status | — | Device + app info |
| POST | /open | — | Launch WhatsApp |
| GET | /chats | — | List recent chats |
| POST | /send | `{contact, message}` | Send message |
| GET | /screenshot | — | Take screenshot |
| GET | /docs | — | Swagger UI |

## Output Format

```json
// status
{"ok": true, "installed": true, "package": "com.whatsapp", "device": "...", "model": "..."}

// chats
{"ok": true, "chats": [{"name": "John", "preview": "Halo..."}], "screenshot_path": "..."}

// send
{"ok": true, "contact": "John", "message_sent": "Halo bro", "screenshot_path": "..."}
```

## Features
- ✅ Auto-dismiss popups & permission dialogs
- ✅ Chat list parsing from UI dump
- ✅ Contact search + type-and-send
- ✅ Word-by-word typing (reliable on Android)
- ✅ 3x retry with state verification
- ✅ FastAPI server
