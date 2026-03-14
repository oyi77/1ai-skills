# Revenue Gap Auto-Detection System

## Overview

Automated monitoring system for detecting and alerting on revenue gaps in crisis mode. Tracks time since last revenue-generating activity across multiple sources and triggers tiered alerts.

**Crisis Mode**: BerkahKarya near bankruptcy - immediate action required when revenue gaps occur.

## Components

- **Main Script**: `scripts/revenue_gap_detector.py`
- **Configuration**: `config/revenue_gap_config.json`
- **Log File**: `logs/revenue_gaps.log`
- **Daily Memory**: `memory/YYYY-MM-DD.md`

## Alert Tiers

| Level | Threshold | Icon | Required Action |
|-------|-----------|------|-----------------|
| WARNING | Gap > 4 hours | ⚠️ | Post content, check pending activities |
| CRITICAL | Gap > 8 hours | 🚨 | IMMEDIATE posting, execute trade, contact leads |
| EMERGENCY | Gap > 12 hours | 🆘 | All hands on deck - execute ALL revenue plans |

## Data Sources

1. **PostBridge API** - JENDRALBOT social media posts (TikTok/IG/YouTube)
2. **Trading Monitor** - XAUUSD trade executions
3. **Manual Cashflow** - Recorded sales and revenue
4. **LYNK Dashboard** - Affiliate conversions (manual check required)

## Usage

### Manual Run
```bash
cd /home/openclaw/.openclaw/workspace
python3 scripts/revenue_gap_detector.py
```

### Exit Codes
- `0` - OK (revenue within acceptable range)
- `1` - WARNING level
- `2` - CRITICAL or EMERGENCY level
- `3` - Fatal error

### Cron Job Setup

Add this to crontab (`crontab -e`):

```bash
# Revenue Gap Detection - Every 2 hours
0 */2 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_gap_detector.py >> logs/revenue_gaps_cron.log 2>&1

# System startup check (optional - if using systemd/cron @reboot is supported)
@reboot cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_gap_detector.py >> logs/revenue_gaps_startup.log 2>&1
```

## Output Format

```json
{
  "timestamp": "2026-03-07T19:03:30",
  "gap_duration_hours": 14.0,
  "gap_level": "EMERGENCY",
  "last_revenue_activity": "2026-03-07T04:20:00+07:00",
  "last_activity_type": "JENDRALBOT post upload (TikTok)",
  "activities_checked": 1,
  "recommendation": "🆘 URGENT: All hands on deck - generate revenue NOW\n...",
  "config": {
    "warning_threshold_hours": 4,
    "critical_threshold_hours": 8,
    "emergency_threshold_hours": 12
  }
}
```

## Configuration

Edit `config/revenue_gap_config.json` to customize:

```json
{
  "warning_threshold_hours": 4,
  "critical_threshold_hours": 8,
  "emergency_threshold_hours": 12,
  "activity_sources": ["postbridge", "trading", "manual", "lynk"],
  "alert_channels": ["memory", "log"],
  "postbridge_api_url": "http://localhost:8080",
  "trading_log_path": "/home/openclaw/.openclaw/workspace/.trading/trades.log",
  "manual_cashflow_path": "/home/openclaw/.openclaw/workspace/.cashflow",
  "lynk_dashboard_url": "https://lynk.id/jendralbot",
  "memory_file_path": "/home/openclaw/.openclaw/workspace/memory",
  "log_file_path": "/home/openclaw/.openclaw/workspace/logs/revenue_gaps.log",
  "timezone": "Asia/Jakarta"
}
```

## How It Works

1. **Load Configuration**: Reads thresholds and source configs
2. **Check Each Source**:
   - PostBridge API: Most recent post timestamp
   - Trading logs: Last trade execution
   - Cashflow files: Last manual sale recorded
   - LYNK: Placeholder for future automation
3. **Find Most Recent Activity**: Uses the latest timestamp across all sources
4. **Calculate Gap**: Time elapsed since last revenue activity
5. **Determine Alert Level**: Based on threshold configuration
6. **Generate Alert**: JSON output + memory entry + log file entry
7. **Exit with Code**: For monitoring/alerting systems

## Error Handling

- Missing config file: Exits with error
- Invalid JSON: Exits with error
- API failures: Logged as warnings, continues processing
- Missing log files: Logged as warnings, continues processing
- Fallback: If no activity found, assumes 12-hour gap (conservative for crisis mode)

## Integration Notes

### PostBridge Integration
Configure PostBridge API URL if running locally. Default: `http://localhost:8080`

### Trading Integration
Trading logs should write to the configured path with timestamps in format:
```
2026-03-07 15:00:00 TRADE EXECUTED: XAUUSD Buy 0.01 lot @ 2350.50
```

### Manual Cashflow Integration
Cashflow files should be in format:
```json
{
  "date": "2026-03-07",
  "total_revenue": 150000,
  "revenue": {
    "jendralbot": 150000,
    "other": 0
  }
}
```

### LYNK Integration
Currently manual check required. Future automation could scrape LYNK dashboard for conversion timestamps.

## Crisis Mode Context

**Current Situation (March 7, 2026):**
- BerkahKarya near bankruptcy
- Revenue pipeline empty for 14+ hours today
- Need immediate action to generate cashflow

**Immediate Actions When EMERGENCY Alert Triggers:**
1. Post ALL pending content to social media NOW
2. Execute trade if market opportunity exists
3. Follow up with all leads directly
4. Send promotional messages
5. Review and update crisis protocols

## Maintenance

- **Log Rotation**: Add logrotate for `logs/revenue_gaps.log` if needed
- **Memory Cleanup**: Old alerts in daily memory files (kept for historical reference)
- **Config Updates**: Adjust thresholds as crisis situation evolves
- **Source Testing**: Regularly test each data source integration

## Dependencies

```bash
# System packages
sudo apt-get install python3 python3-requests

# Python packages
pip3 install requests python-dateutil
```

---

**Author**: Vilona (OpenClaw agent)  
**Version**: 1.0  
**Last Updated**: 2026-03-07  
**Status**: ✅ Operational - Crisis Mode Active