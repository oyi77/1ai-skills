# autodroid-youtube-agent

Control YouTube Android app via ADB automation. No API key required.

## Package
- `com.google.android.youtube`

## Quick Start

```bash
cd /mnt/data/berkahkarya/skills/1ai-skills/automation/autodroid-youtube-agent

# Status
python3 scripts/youtube_agent.py status

# Open YouTube
python3 scripts/youtube_agent.py open

# Search video
python3 scripts/youtube_agent.py search --query "resep rendang"

# Screenshot
python3 scripts/youtube_agent.py screenshot

# Start API server
python3 scripts/youtube_agent.py server --port 8770
```

## API Endpoints (port 8770)

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | /status | — | Device + app info |
| POST | /open | — | Launch YouTube |
| POST | /search | `{query}` | Search + return results |
| GET | /screenshot | — | Take screenshot |
| GET | /docs | — | Swagger UI |

## Output Format

```json
// search
{
  "ok": true,
  "query": "resep rendang",
  "results": ["Resep Rendang Padang", "Cara Masak Rendang", "Rendang Viral"],
  "screenshot_path": "/path/to/screenshot.png",
  "device": "SGZTONV4OBL74TJZ"
}
```

## Features
- ✅ Label-first + coordinate fallback for search icon
- ✅ Word-by-word typing (reliable)
- ✅ TextViews extraction for top 3 results
- ✅ 3x retry
- ✅ FastAPI server
