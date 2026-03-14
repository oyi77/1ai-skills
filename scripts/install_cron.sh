#!/bin/bash
# Install JENDRALBOT Cron Jobs
# Creates automated daily execution for all automation tasks

echo "Setting up JENDRALBOT automation schedule..."
echo ""

# Create log directory
mkdir -p ~/.openclaw/workspace/logs

# Backup existing crontab
crontab -l > ~/.crontab.backup 2>/dev/null
echo "✅ Backed up existing crontab to ~/.crontab.backup"
echo ""

# Add new cron jobs
(crontab -l 2>/dev/null; cat <<'EOF'

# JENDRALBOT Automation Schedule

# Job 1: Daily heartbeat (every 2 hours)
# Checks LYNK dashboard, revenue, rate limit status
0 */2 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py --heartbeat >> logs/daily_heartbeat.log 2>&1

# Job 2: Instagram upload resume (daily at 12:00 PM UTC+7 / 5:00 UTC)
# Automatically resumes Instagram uploads when rate limit clears
0 5 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py --resume instagram >> logs/daily_Instagram.log 2>&1

# Job 3: Facebook automation start (daily at 6:00 PM UTC+7 / 11:00 UTC)
# Starts Facebook uploads when Instagram is complete (≥ 150 posts)
0 11 * * * cd ~/.openclaw/workspace && bash scripts/automation_scheduler.sh >> logs/automator.log 2>&1

# Job 4: Daily summary at 10:00 PM UTC+7
# Generates daily revenue and performance report
0 15 * * * cd ~/.openclaw/workspace && python3 scripts/daily_schedule.py >> logs/daily_summary.log 2>&1

EOF
) | crontab -

echo "✅ Cron jobs installed!"
echo ""
echo "JENDRALBOT automation schedule:"
echo "  - Heartbeat: Every 2 hours"
echo "  - Instagram resume: Daily at 12:00 PM"
echo "  - Facebook start: Daily at 6:00 PM"
echo "  - Daily summary: Daily at 10:00 PM"
echo ""
echo "To view cron jobs: crontab -l"
echo "To edit: crontab -e"
echo "To remove cron jobs: crontab -e (delete JENDRALBOT lines)"
echo ""
echo "✅ Automation scheduled!"