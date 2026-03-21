# autodroid-dashboard Skill

Master orchestrator for all Android ADB agents. Manages lifecycle, health checks, and smoke tests for the entire autodroid agent suite.

## Commands

| Command | Description |
|---------|-------------|
| `status` | Show health of all agents + connected ADB devices |
| `devices` | List connected ADB devices with model/Android version |
| `start [agent]` | Start one or all agent servers |
| `stop [agent]` | Stop one or all agent servers |
| `restart [agent]` | Restart one or all agent servers |
| `test [agent]` | Run smoke tests against one or all agents |
| `server [--port 8800]` | Start FastAPI dashboard API server |

## Usage

```bash
# Health check all agents
python3 scripts/autodroid_dashboard.py status

# List ADB devices
python3 scripts/autodroid_dashboard.py devices

# Start all agents
python3 scripts/autodroid_dashboard.py start

# Start a specific agent
python3 scripts/autodroid_dashboard.py start gemini --device SGZTONV4OBL74TJZ

# Stop all
python3 scripts/autodroid_dashboard.py stop

# Restart specific agent
python3 scripts/autodroid_dashboard.py restart shopee

# Smoke test all
python3 scripts/autodroid_dashboard.py test

# Start dashboard API server (port 8800)
python3 scripts/autodroid_dashboard.py server --port 8800
```

## Agent Registry

| Agent | Port | Package |
|-------|------|---------|
| gemini | 8765 | com.google.android.apps.bard |
| tiktok | 8766 | com.ss.android.ugc.trill |
| shopee | 8767 | com.shopee.id |
| whatsapp | 8768 | com.whatsapp |
| instagram | 8769 | com.instagram.android |
| youtube | 8770 | com.google.android.youtube |
| playstore | 8771 | com.android.vending |
| device | 8772 | system |

## Dashboard API (port 8800)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | All agents status |
| `/devices` | GET | Connected ADB devices |
| `/start/{agent}` | POST | Start agent (use `all` for all) |
| `/stop/{agent}` | POST | Stop agent |
| `/restart/{agent}` | POST | Restart agent |
| `/test/{agent}` | GET | Smoke test agent |
| `/health` | GET | Dashboard heartbeat |
| `/ports` | GET | All agent ports |
| `/docs` | GET | Swagger UI |

## Device Requirements

- ADB connected and authorized
- Serial: SGZTONV4OBL74TJZ (or set via `--device`)
- Individual apps installed on device per agent

## Output Format

All CLI commands output JSON. Example `status` output:

```json
{
  "timestamp": "2026-03-22T00:00:00",
  "devices": [{"serial": "SGZTONV4OBL74TJZ", "model": "Redmi Note 13", "android": "14"}],
  "device_count": 1,
  "agents": {
    "gemini": {"running": true, "pid": 12345, "port": 8765, "port_alive": true, "installed": true}
  },
  "running_count": 3,
  "installed_count": 7
}
```

## Dependencies

```bash
pip install fastapi uvicorn requests
```

## AI Interceptor

Optional integration available. Add to script for prompt enhancement and quality scoring across all managed agents.
