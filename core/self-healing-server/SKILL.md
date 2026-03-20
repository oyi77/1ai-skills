# Self-Healing Home Server

> Monitor & auto-repair system services, disk, memory, and network

## Overview

Autonomous system health monitor that runs every 30 minutes via cron. Detects issues and attempts automatic repairs before they escalate. Generates markdown health reports and alerts via openclaw system events.

## When to Use

- **Proactive monitoring** -- catch issues before they cause outages
- **Auto-repair** -- fix common failures without manual intervention
- **Health reporting** -- generate system status snapshots
- **Incident response** -- automated first-response to failures

## Monitored Services

| Service | Check Method | Auto-Repair |
|---------|-------------|-------------|
| openclaw-gateway | `systemctl --user status` | Restart via systemctl --user |
| omniroute.service | `systemctl status` | Restart via systemctl |
| cloudflared.service | `systemctl status` | Restart via systemctl |
| xvfb.service | `systemctl status` | Restart via systemctl |
| Tailscale | `tailscale status` | `tailscale up` |

## Health Checks

### Disk
- Warn at >90% usage
- Auto-cleanup temp/logs at >95% (removes files older than 7 days from /tmp, truncates large log files)

### Memory
- Warn if available memory <500MB
- Kill zombie processes automatically
- Report top memory consumers

### Network
- Ping google.com for connectivity
- Restart systemd-networkd if down
- Check DNS resolution

## Setup

```bash
# Install to cron (every 30 minutes)
(crontab -l 2>/dev/null; echo "*/30 * * * * /usr/bin/python3 /home/openclaw/.openclaw/workspace/scripts/self_healer.py --cron 2>&1 >> /home/openclaw/.openclaw/workspace/logs/self_healer.log") | crontab -

# Manual run
python3 scripts/self_healer.py

# Generate report only (no repairs)
python3 scripts/self_healer.py --report-only

# JSON output
python3 scripts/self_healer.py --json
```

## Alert System

Alerts via: `openclaw system event --text "..." --mode now`

Alert levels:
- **INFO** -- routine health report
- **WARN** -- degraded state detected (disk >90%, low memory)
- **CRITICAL** -- service down, network unreachable, auto-repair failed

## Files

- `SKILL.md` -- this file
- `../../scripts/self_healer.py` -- main monitoring script
