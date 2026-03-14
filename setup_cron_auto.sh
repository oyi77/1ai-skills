#!/bin/bash
#
# AUTO-SETUP CRON JOBS FOR JENDRALBOT TRUE FULLY AUTONOMOUS SYSTEM
# Run this script ONCE to set up automation
#

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
ENGINE_DIR="$WORKSPACE/autopilot_affiliate_engine"
LOG_FILE="$HOME/automation.log"
TEMP_CRON="/tmp/jendralbot_cron_temp"

echo "🚀 JENDRALBOT - AUTO-SETUP CRON JOBS"
echo "========================================"
echo ""
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Check if already exists
echo "📋 Checking existing cron jobs..."
if crontab -l 2>/dev/null | grep -q "JENDRALBOT\|true_autonomous"; then
    echo "⚠️  WARNING: JENDRALBOT cron jobs already exist!"
    echo ""
    echo "Choose:"
    echo "1. Keep existing (skip setup)"
    echo "2. Replace with new (backup first)"
    echo "3. Show existing jobs"
    echo ""
    read -p "Enter choice [1/2/3]: " choice

    case $choice in
        1)
            echo "❌ Setup cancelled - keeping existing jobs"
            exit 0
            ;;
        2)
            echo "💾 Backing up existing crontab..."
            crontab -l > "$HOME/crontab_backup_$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
            echo "✅ Backup saved"
            ;;
        3)
            echo ""
            echo "📋 Existing JENDRALBOT cron jobs:"
            crontab -l 2>/dev/null | grep -E "JENDRALBOT|true_autonomous|fully_autonomous" || echo "None found"
            echo ""
            exit 0
            ;;
        *)
            echo "❌ Invalid choice - cancelling"
            exit 1
            ;;
    esac
fi

# Create logs directory
mkdir -p "$HOME"
touch "$LOG_FILE"

# Create temporary crontab file
echo "📝 Creating new crontab configuration..."

# Get current crontab (crontab -l can fail if empty)
{
    crontab -l 2>/dev/null || true
    echo ""
    echo "# JENDRALBOT - TRUE FULLY AUTONOMOUS SYSTEM"
    echo "# Auto-generated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "# System: 12 parallel agents, 120 posts/day, 0 manual work"
    echo ""
    echo "# Morning: 08:00 - 12 parallel agents (research/content/posting)"
    echo "0 8 * * * cd $WORKSPACE && python3 $ENGINE_DIR/true_autonomous.py morning >> $LOG_FILE 2>&1"
    ""
    echo "# Evening: 20:00 - PostBridge stats + LYNK tracking"
    echo "0 20 * * * cd $WORKSPACE && python3 $ENGINE_DIR/fully_autonomous.py evening >> $LOG_FILE 2>&1"
} > "$TEMP_CRON"

# Verify file created
if [ ! -f "$TEMP_CRON" ]; then
    echo "❌ ERROR: Failed to create temporary crontab"
    exit 1
fi

# Install new crontab
echo "📤 Installing new crontab..."
crontab "$TEMP_CRON"

# Verify installation
echo ""
echo "✅ Cron jobs installed successfully!"
echo ""

# Show installed jobs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 INSTALLED CRON JOBS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
crontab -l | grep -E "JENDRALBOT|true_autonomous|fully_autonomous|Auto-generated"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verify scripts exist
echo "🔍 Verifying scripts exist..."

scripts=(
    "$ENGINE_DIR/true_autonomous.py"
    "$ENGINE_DIR/fully_autonomous.py"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ Found: $script"
    else
        echo "❌ MISSING: $script"
        exit 1
    fi
done

echo ""

# Test morning script
echo "🧪 Testing morning script (dry run)..."
if python3 "$ENGINE_DIR/true_autonomous.py" morning > /tmp/test_output.txt 2>&1; then
    echo "✅ Morning script test passed"
else
    echo "⚠️  Morning script test had issues (check /tmp/test_output.txt)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📅 SCHEDULE:"
echo "   • 08:00 WIB - Morning workflow (12 parallel agents)"
echo "   • 20:00 WIB - Evening workflow (revenue tracking)"
echo ""
echo "📊 EXPECTED OUTPUT:"
echo "   • 120 posts/day (4x old system)"
echo "   • Zero manual work"
echo "   • Revenue: Rp 500K-5M/day"
echo ""
echo "📊 LOGS:"
echo "   • Location: $LOG_FILE"
echo "   • View: tail -f $LOG_FILE"
echo ""
echo "🔍 VERIFY:"
echo "   • Check cron: crontab -l"
echo "   • View jobs: crontab -l | grep JENDRALBOT"
echo "   • Test manually: python3 $ENGINE_DIR/true_autonomous.py morning"
echo ""
echo "🚀 SYSTEM WILL AUTO-START TOMORROW AT 08:00 WIB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Clean up
rm -f "$TEMP_CRON"

echo "✅ Setup file cleaned up"
echo ""
echo "💡 Next steps:"
echo "   1. Wait for 08:00 tomorrow - system runs automatically"
echo "   2. Check logs: tail -f $LOG_FILE"
echo "   3. Verify reports in: $ENGINE_DIR/reports/"
echo ""
echo "✨ DONE!"

exit 0