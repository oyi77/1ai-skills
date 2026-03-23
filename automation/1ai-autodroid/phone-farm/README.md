# Phone Farm — Android Device Farm Automation

Production-grade Android device farm orchestrator built on top of 1ai-autodroid.

## Architecture

```
phonefarm CLI → device_manager.py (ADB abstraction layer)
                     ↑
farm_daemon.py ──────┘ (autonomous orchestrator)
     │
     ├── Health checks (every 5 min)
     ├── Screenshots (every 2 min)
     ├── Auto-reconnect (every 1 min)
     └── Active tasks (every 10 min, active mode only)
```

## Components

| File | Purpose |
|------|---------|
| `device_manager.py` | ADB abstraction: connect, screenshot, tap, swipe, type, UI dump, health monitor, auto-reconnect |
| `task_runner.py` | 10 built-in tasks: health_check, screenshot, app_check, tiktok_inbox, shopee_orders, whatsapp_unread, instagram_dms, etc. |
| `farm_daemon.py` | Autonomous daemon with 3 modes: monitor, active, dashboard (HTTP API) |
| `farm_cli.py` | Unified CLI interface (`phonefarm` command) |

## Quick Start

```bash
# Symlink for easy access
ln -sf /path/to/farm_cli.py ~/.local/bin/phonefarm

# Check status
phonefarm status

# Start daemon (monitor mode — health + screenshots only)
phonefarm daemon start --mode monitor

# Start daemon (active mode — full app automation)
phonefarm daemon start --mode active

# Run specific tasks
phonefarm health
phonefarm screenshot
phonefarm task shopee_orders
phonefarm task tiktok_inbox --device SERIAL

# Add new device
phonefarm add SERIAL my-phone-name

# View logs
phonefarm logs --lines 100
```

## Daemon Modes

| Mode | What it does | Safe? |
|------|-------------|-------|
| `monitor` | Health checks + screenshots + reconnect only | ✅ Very safe |
| `active` | All of monitor + opens apps + checks inboxes | ⚠️ Interacts with apps |
| `dashboard` | HTTP API only (port 8889), no autonomous tasks | ✅ Safe |

## Systemd Service

```bash
# Enable auto-start on boot
systemctl --user enable phone-farm.service
systemctl --user start phone-farm.service

# Check status
systemctl --user status phone-farm.service
```

## Device Config

Edit `config/devices.json` to register devices and assign skills:

```json
{
  "devices": {
    "SERIAL_NUMBER": {
      "name": "farm-hp1",
      "assigned_skills": ["tiktok", "shopee", "whatsapp"],
      "installed_apps": {
        "shopee": "com.shopee.id",
        "whatsapp": "com.whatsapp"
      },
      "enabled": true
    }
  }
}
```

## Auto-Recovery

- **Disconnect**: Auto-reconnect attempts every 60s
- **Battery critical** (<10%): Alert sent
- **Crash**: Systemd auto-restarts within 30s
- **ADB server death**: Kills and restarts ADB server

## Support

If this saves you time, consider tipping: 👉 https://www.tip.md/oyi77
