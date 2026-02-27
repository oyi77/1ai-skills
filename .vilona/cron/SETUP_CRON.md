# Cron Setup Instructions

## Manual Setup (Run Once)

```bash
# 1. Daily Self-Review at 23:00
crontab -e
# Add: 0 23 * * * bash /home/openclaw/.openclaw/workspace/.vilona/cron/daily-review.sh

# 2. Knowledge Update (rotation)
# Add: 0 6 * * * bash /home/openclaw/.openclaw/workspace/.vilona/cron/knowledge-update.sh

# 3. Trading Monitors (4x daily)
# Add: 0 9,12,15,18 * * * openclaw message send "Check Ostium positions"
```

## Via openclaw CLI (Preferred)

```bash
# List existing
openclaw cron list

# Add daily review
openclaw cron add daily-review "0 23 * * *" "bash /home/openclaw/.openclaw/workspace/.vilona/cron/daily-review.sh"

# Add knowledge update
openclaw cron add knowledge-update "0 6 * * *" "bash /home/openclaw/.openclaw/workspace/.vilona/cron/knowledge-update.sh"

# Add trading monitor
openclaw cron add trading-monitor "0 9,12,15,18 * * *" "trading-monitor-task"

# Enable
openclaw cron enable daily-review
openclaw cron enable knowledge-update
```
