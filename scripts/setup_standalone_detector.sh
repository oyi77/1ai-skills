#!/bin/bash
# Standalone Revenue Gap Detector - Install to Cron
# Version: PostBridge-independent, works even when infrastructure is down

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
STANDALONE_SCRIPT="$WORKSPACE/scripts/revenue_gap_detector_standalone.py"
CRON_LOG="$WORKSPACE/logs/revenue_gaps_cron.log"

echo "==============================================="
echo "Standalone Revenue Gap Detector - Cron Setup"
echo "==============================================="
echo ""

# Check if standalone script exists
echo "1. Checking standalone detector..."
if [ ! -f "$STANDALONE_SCRIPT" ]; then
    echo "❌ Error: Standalone script not found at $STANDALONE_SCRIPT"
    exit 1
fi
echo "✅ Standalone detector found"
echo ""

# Run manual test first
echo "2. Running manual test..."
cd "$WORKSPACE"
python3 "$STANDALONE_SCRIPT"
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
    exit 1
fi
echo ""

# Remove any existing revenue detector cron jobs (both original and standalone)
echo "3. Removing existing revenue detector cron jobs..."
EXISTING=$(crontab -l 2>/dev/null | grep -c "revenue_gap_detector" || echo "0")
if [ "$EXISTING" -gt 0 ]; then
    echo "⚠️ Removing $EXISTING existing revenue detector cron job(s)..."
    crontab -l 2>/dev/null | grep -v "revenue_gap_detector" | crontab -
    echo "✅ Existing jobs removed"
else
    echo "✅ No existing jobs to remove"
fi
echo ""

# Setup cron for standalone detector
echo "4. Setting up standalone detector cron job (every 2 hours)..."
(crontab -l 2>/dev/null | grep -v "revenue_gap_detector"; echo "") | crontab -
(crontab -l 2>/dev/null; cat <<EOF

# Standalone Revenue Gap Detection - Every 2 hours (PostBridge-independent)
0 */2 * * * cd $WORKSPACE && python3 scripts/revenue_gap_detector_standalone.py >> logs/revenue_gaps_cron.log 2>&1
EOF
) | crontab -
echo "✅ Standalone detector cron job installed"
echo ""

# Verify cron
echo "5. Verifying cron installation..."
crontab -l | grep "revenue_gap_detector_standalone"
echo ""

echo "==============================================="
echo "✅ Installation Complete!"
echo "==============================================="
echo ""
echo "Benefits of Standalone Detector:"
echo "  ✓ Works WITHOUT PostBridge API"
echo "  ✓ Uses local files only (trading logs, cashflow files, memory)"
echo "  ✓ Same alert levels (WARNING, CRITICAL, EMERGENCY)"
echo "  ✓ Same exit codes (0=OK, 1=WARNING, 2=CRITICAL)"
echo "  ✓ Infrastructure-independent (works even when services down)"
echo ""
echo "Files:"
echo "  - Script: $STANDALONE_SCRIPT"
echo "  - Logs: $WORKSPACE/logs/revenue_gaps.log"
echo "  - Cron logs: $CRON_LOG"
echo ""
echo "Schedule: Every 2 hours (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22)"
echo ""
echo "Next runs:"
for i in 0 2 4 6 8; do
    hours_from_now=$((2 + i))
    next_run=$(date -d "+$hours_from_now hours" +'%Y-%m-%d %H:%M' 2>/dev/null || echo "N/A")
    echo "  - $(date -d "+$hours_from_now hours" +'%H:%M' 2>/dev/null || echo "N/A") +${hours_from_now}h ($next_run)"
done
echo ""
echo "Manual test anytime:"
echo "  cd $WORKSPACE"
echo "  python3 scripts/revenue_gap_detector_standalone.py"
echo ""
echo "View cron logs:"
echo "  tail -f $CRON_LOG"
echo ""
echo "View revenue gap alerts:"
echo "  tail -f logs/revenue_gaps.log"
echo ""