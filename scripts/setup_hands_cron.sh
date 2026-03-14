#!/bin/bash
# Setup OpenFang-Style Hands Cron Jobs
# Adds hands to existing autonomous monitoring schedule

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"

echo "========================================="
echo "OpenFang Hands - Cron Setup"
echo "========================================="
echo ""

# Function to check if hands already in crontab
has_hands() {
    crontab -l 2>/dev/null | grep -q "OpenFang Hands"
    return $?
}

# Function to add hands to crontab
add_hands_to_crontab() {
    local tmp_cron=$(mktemp)

    # Add OpenFang Hands section
    cat << EOThands >> "$tmp_cron"
# OpenFang Hands - Autonomous Execution
# Generated: $(date '+%Y-%m-%d %H:%M:%S')

# LEAD Hand - Daily at 10 AM (prospect discovery, enrichment, scoring)
0 10 * * * cd $WORKSPACE && bash scripts/run_hand.sh lead >> logs/lead_schedule.log 2>&1

# COLLECTOR Hand - Every 6 hours (intelligence gathering)
0 */6 * * * cd $WORKSPACE && bash scripts/run_hand.sh collector >> logs/collector_schedule.log 2>&1

# CLIP Hand - Every 4 hours (video processing queue)
0 */4 * * * cd $WORKSPACE && bash scripts/run_hand.sh clip >> logs/clip_schedule.log 2>&1
EOThands

    # If crontab exists, append
    if crontab -l > /dev/null 2>&1; then
        crontab -l >> "$tmp_cron.bak"
        cat "$tmp_cron.bak" | grep -v "OpenFang Hands" | grep -v "$WORKSPACE/scripts/run_hand.sh" > "$tmp_cron.new"
        cat "$tmp_cron.new" >> "$tmp_cron"
        mv "$tmp_cron" "$tmp_cron.tmp"
        mv "$tmp_cron.tmp" "$tmp_cron"
        rm -f "$tmp_cron.bak" "$tmp_cron.new"
    fi

    # Install new crontab
    crontab "$tmp_cron"
    rm -f "$tmp_cron"

    echo "✅ OpenFang Hands added to crontab"
}

# Check if already installed
if has_hands; then
    echo "⚠️  Existing OpenFang Hands detected in crontab"
    echo ""
    echo "Options:"
    echo "  1) Keep existing hands (skip installation)"
    echo "  2) Replace with new schedules"
    echo ""
    read -p "Choose [1/2]: " choice

    case $choice in
        2)
            add_hands_to_crontab
            ;;
        *)
            echo "Keeping existing hands"
            ;;
    esac
else
    # Install new hands
    add_hands_to_crontab
fi

# Show hands schedule
echo ""
echo "========================================="
echo "OpenFang Hands Schedule (Autonomous):"
echo "========================================="
echo "LEAD (Lead Generation):     Daily 10 AM"
echo "COLLECTOR (Intelligence):    Every 6 hours (00:00, 06:00, 12:00, 18:00)"
echo "CLIP (Video Processing):    Every 4 hours (00:00, 04:00, ...)"
echo ""
echo "Logs location: $WORKSPACE/logs/"
echo "  - lead.log (detailed)"
echo "  - collector.log (detailed)"
echo "  - clip.log (detailed)"
echo "  - *_schedule.log (cron execution)"
echo ""
echo "✅ Hands setup complete!"
echo ""
echo "To view all cron jobs:"
echo "  crontab -l"
echo ""
echo "To run a specific hand manually:"
echo "  cd $WORKSPACE && bash scripts/run_hand.sh {clip|lead|collector|all}"
echo "========================================="