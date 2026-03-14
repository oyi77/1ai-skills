#!/bin/bash
# Revenue Gap Detector - Installation and Setup Script

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
SCRIPT="$WORKSPACE/scripts/revenue_gap_detector.py"
CONFIG="$WORKSPACE/config/revenue_gap_config.json"
CRON_LOG="$WORKSPACE/logs/revenue_gaps_cron.log"

echo "==============================================="
echo "Revenue Gap Detector - Installation & Setup"
echo "==============================================="
echo ""

# Check if files exist
echo "1. Checking files..."
if [ ! -f "$SCRIPT" ]; then
    echo "❌ Error: Script not found at $SCRIPT"
    exit 1
fi
if [ ! -f "$CONFIG" ]; then
    echo "❌ Error: Config not found at $CONFIG"
    exit 1
fi
echo "✅ Files found"
echo ""

# Check Python dependencies
echo "2. Checking Python dependencies..."
python3 -c "import requests, dateutil" 2>/dev/null && echo "✅ Dependencies installed" || {
    echo "⚠️ Installing dependencies..."
    pip3 install requests python-dateutil
}
echo ""

# Run manual test
echo "3. Running manual test..."
cd "$WORKSPACE"
python3 "$SCRIPT"
EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Test run: OK (revenue within range)"
elif [ $EXIT_CODE -eq 1 ]; then
    echo "⚠️ Test run: WARNING level alert"
elif [ $EXIT_CODE -eq 2 ]; then
    echo "🚨 Test run: CRITICAL/EMERGENCY alert"
else
    echo "❌ Test run: Fatal error (code $EXIT_CODE)"
fi
echo ""

# Check existing cron
echo "4. Checking existing cron jobs..."
EXISTING=$(crontab -l 2>/dev/null | grep -c "revenue_gap_detector" || echo "0")
if [ "$EXISTING" -gt 0 ]; then
    echo "⚠️ Found $EXISTING existing revenue_gap_detector cron job(s)"
    echo ""
    read -p "Replace existing cron jobs? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping cron setup"
        exit 0
    fi
    # Remove existing entries
    crontab -l | grep -v "revenue_gap_detector" | crontab -
fi
echo ""

# Setup cron
echo "5. Setting up cron job (runs every 2 hours)..."
(crontab -l 2>/dev/null | grep -v "revenue_gap_detector"; echo "") | crontab -
(crontab -l 2>/dev/null; cat <<EOF

# Revenue Gap Detection - Every 2 hours
0 */2 * * * cd $WORKSPACE && python3 scripts/revenue_gap_detector.py >> logs/revenue_gaps_cron.log 2>&1
EOF
) | crontab -
echo "✅ Cron job installed"
echo ""

# Verify cron
echo "6. Verifying cron installation..."
crontab -l | grep "revenue_gap_detector"
echo ""

echo "==============================================="
echo "✅ Installation Complete!"
echo "==============================================="
echo ""
echo "Files:"
echo "  - Script: $SCRIPT"
echo "  - Config: $CONFIG"
echo "  - Logs: $WORKSPACE/logs/revenue_gaps.log"
echo "  - Cron logs: $CRON_LOG"
echo ""
echo "Next runs (every 2 hours):"
echo "  - Next: $(date -d '2 hours' +'%H:%M') ($(date -d '2 hours' +'%Y-%m-%d %H:%M'))"
echo "  - Then: $(date -d '4 hours' +'%H:%M') ($(date -d '4 hours' +'%Y-%m-%d %H:%M'))"
echo ""
echo "Manual test anytime:"
echo "  cd $WORKSPACE"
echo "  python3 scripts/revenue_gap_detector.py"
echo ""
echo "View cron logs:"
echo "  tail -f $CRON_LOG"
echo ""