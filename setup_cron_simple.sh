#!/bin/bash
#
# AUTO-SETUP CRON JOBS FOR JENDRALBOT
# Run this script ONCE
#

WORKSPACE="/home/openclaw/.openclaw/workspace"
ENGINE_DIR="$WORKSPACE/autopilot_affiliate_engine"
LOG_FILE="$HOME/automation.log"
BACKUP_FILE="$HOME/crontab_backup_$(date +%Y%m%d_%H%M%S)"

echo "🚀 JENDRALBOT - AUTO-SETUP CRON JOBS"
echo "========================================"
echo ""

# Backup
if crontab -l >/dev/null 2>&1; then
    echo "💾 Backing up existing crontab to $BACKUP_FILE..."
    crontab -l > "$BACKUP_FILE"
fi

# Create cron file
cat > /tmp/jendralbot_cron.txt << 'EOF'
# JENDRALBOT - TRUE FULLY AUTONOMOUS SYSTEM
# Auto-generated: 2026-03-06
# System: 12 parallel agents, 120 posts/day

# Morning 08:00 WIB
0 8 * * * cd /home/openclaw/.openclaw/workspace && python3 autopilot_affiliate_engine/true_autonomous.py morning >> ~/automation.log 2>&1

# Evening 20:00 WIB
0 20 * * * cd /home/openclaw/.openclaw/workspace && python3 autopilot_affiliate_engine/fully_autonomous.py evening >> ~/automation.log 2>&1
EOF

# Install
echo "📤 Installing cron jobs..."
crontab /tmp/jendralbot_cron.txt

echo ""
echo "✅ CRON JOBS INSTALLED!"
echo ""
echo "📋 Active jobs:"
crontab -l | grep JENDRALBOT
echo ""
echo "🚀 SYSTEM STARTS TOMORROW AT 08:00 WIB"
echo ""
echo "✅ DONE!"