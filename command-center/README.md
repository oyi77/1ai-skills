# ⚡ OpenClaw Command Center

**BerkahKarya AI Operations Dashboard** — Real-time monitoring for OpenClaw agents, system vitals, LLM quotas, and scheduled tasks.

## Quick Start

```bash
cd ~/.openclaw/workspace/command-center
node server.js

# Open in browser:
# http://127.0.0.1:3337
```

## Features

### Phase 1 ✅
- **Dashboard**: Full-screen operations center at `localhost:3337`
- **Session Monitoring**: Active OpenClaw sessions with model/status info
- **System Vitals**: Real-time CPU, memory, disk via SSE (every 5s)
- **LLM Fuel Gauges**: Quota/model status display
- **Cron Visibility**: All scheduled tasks from crontab + workspace files
- **Privacy Mode**: Hide sensitive topics for screenshots
- **Process Monitor**: Running Python/Node/OpenClaw processes

### Phase 2 (Ready to extend)
- Slack threading hooks (add `/api/slack` endpoint)
- External notification integration
- Custom metric dashboards

## Architecture

```
command-center/
├── server.js       # Pure Node.js HTTP server (no npm install needed)
├── dashboard.html  # Vanilla JS UI (no React/CDN/bundler)
└── README.md       # This file
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard HTML |
| GET | `/events` | SSE stream (real-time updates) |
| GET | `/api/all` | All data in one call |
| GET | `/api/system` | CPU, memory, disk, uptime |
| GET | `/api/sessions` | OpenClaw sessions |
| GET | `/api/crons` | Scheduled cron jobs |
| GET | `/api/quotas` | LLM provider quotas |
| GET | `/api/logs` | Recent log files |
| GET | `/api/processes` | Running processes |
| GET | `/api/revenue` | Revenue stats |
| GET | `/api/status` | Server health |
| POST | `/api/refresh` | Force data refresh |
| POST | `/api/privacy` | Toggle privacy mode |

## Options

```bash
node server.js --port 3338   # Custom port
node server.js --host 0.0.0.0  # Expose to LAN (⚠️ only on trusted network)
```

## Security

- **Localhost only** by default (`127.0.0.1`)
- **No external calls** — all data from local system
- **No secrets in UI** — API keys shown as `***xxxx`
- **Privacy mode** — toggle to hide sensitive data for screenshots
- **Whitelist-only exec** — only safe read-only commands allowed via `/api/exec`

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Alt+1` | Overview tab |
| `Alt+2` | Sessions tab |
| `Alt+3` | System tab |
| `Alt+4` | Cron Jobs tab |
| `Alt+5` | LLM Fuel tab |
| `Alt+6` | Logs tab |
| `Alt+7` | Processes tab |
| `Ctrl+R` | Manual refresh |

## Extending

### Add Slack Integration (Phase 2)

```javascript
// In server.js, add to handleRequest():
if (pathname === '/api/slack' && method === 'POST') {
  // Parse body, call Slack API
  // Keep secrets server-side only
}
```

### Add Custom Metrics

```javascript
// Add to refreshAllData():
myMetric: await getMyMetric(),
```

---

*Made for BerkahKarya Business Kingdom. No CDNs. No telemetry. No BS.* 🔥
