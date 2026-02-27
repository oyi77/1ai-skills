#!/bin/bash
# Cron Job Setup for TikTok Content Agency Automation

# This script sets up automated daily tasks for:
# - Lead management
# - Social media posting
# - Reporting

echo "Setting up TikTok Content Agency automation..."

# Create log directory
mkdir -p /home/openclaw/.openclaw/workspace/output/logs

# Create reports directory
mkdir -p /home/openclaw/.openclaw/workspace/output/reports

# Add cron job to run daily at 9:00 AM
(crontab -l 2>/dev/null; echo "0 9 * * * /home/openclaw/.trading-venv/bin/python /home/openclaw/.openclaw/workspace/scripts/daily_automation.py >> /home/openclaw/.openclaw/workspace/output/logs/cron.log 2>&1") | crontab -

# Verify cron job is set
echo ""
echo "✅ Cron job setup complete!"
echo ""
echo "Current cron jobs:"
crontab -l
echo ""
echo "Automation will run daily at 09:00 AM"
echo ""
echo "To view logs:"
echo "  tail -f /home/openclaw/.openclaw/workspace/output/logs/cron.log"
echo ""
echo "To view reports:"
echo "  ls -la /home/openclaw/.openclaw/workspace/output/reports/"
echo ""
echo "To stop automation:"
echo "  crontab -l | grep -v daily_automation | crontab -"
echo ""
echo "To restart automation:"
echo "  Run this script again"
