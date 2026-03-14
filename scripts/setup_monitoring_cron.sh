#!/bin/bash
# Setup Cron Jobs for Autonomous Monitoring
# This script installs all monitoring tasks to crontab

set -e

# Paths
WORKSPACE="/home/openclaw/.openclaw/workspace"
LOGS_DIR="$WORKSPACE/logs"

# Ensure logs directory exists
mkdir -p "$LOGS_DIR"

# Create crontab entry
create_crontab() {
    cat << EOTCRON
# Vilona Autonomous Monitoring Schedule
# Generated: $(date '+%Y-%m-%d %H:%M:%S')

# Heartbeat - Every 6 hours (send regular status reports)
0 */6 * * * cd $WORKSPACE && python3 scripts/heartbeat_run.py >> $LOGS_DIR/heartbeat.log 2>&1

# Revenue Gap Check - Every 2 hours (CRITICAL - revenue monitoring)
0 */2 * * * cd $WORKSPACE && python3 scripts/revenue_gap_detector_standalone.py >> $LOGS_DIR/revenue_gaps.log 2>&1

# LYNK Monitoring - Every 3 hours (manual check reminders)
0 */3 * * * cd $WORKSPACE && python3 scripts/lynk_monitor.py >> $LOGS_DIR/lynk_monitoring.log 2>&1

# Cashflow Monitoring - Daily at 9 AM (tracking reminders)
0 9 * * * cd $WORKSPACE && python3 scripts/cashflow_monitor.py >> $LOGS_DIR/cashflow.log 2>&1

# PostBridge Health Check - Every 30 minutes (API monitoring)
*/30 * * * * cd $WORKSPACE && python3 scripts/postbridge_health.py >> $LOGS_DIR/postbridge_health.log 2>&1

# Auto-compaction - Daily at 3 AM (memory cleanup)
0 3 * * * cd $WORKSPACE && python3 scripts/memory_compaction.py >> $LOGS_DIR/compaction.log 2>&1

# Disk Cleanup Check - Every 6 hours (disk space monitoring)
0 */6 * * * cd $WORKSPACE && python3 scripts/disk_cleanup_automation.py --dry-run >> $LOGS_DIR/disk_monitor.log 2>&1
EOTCRON
}

# Function to check if crontab already has our jobs
has_vilona_jobs() {
    crontab -l 2>/dev/null | grep -q "Vilona Autonomous Monitoring"
    return $?
}

# Function to add jobs to crontab
add_to_crontab() {
    local tmp_cron=$(mktemp)
    create_crontab > "$tmp_cron"

    # If crontab exists, append
    if crontab -l > /dev/null 2>&1; then
        crontab -l > "$tmp_cron.bak"
        cat "$tmp_cron.bak" >> "$tmp_cron"
    fi

    # Install new crontab
    crontab "$tmp_cron"
    rm "$tmp_cron" "$tmp_cron.bak"

    echo "✅ Crontab updated"
}

# Function to remove existing vilona jobs
remove_vilona_jobs() {
    local tmp_cron=$(mktemp)

    if crontab -l > /dev/null 2>&1; then
        crontab -l | grep -v "Vilona Autonomous Monitoring" | grep -v "$WORKSPACE/scripts/" > "$tmp_cron"
        crontab "$tmp_cron"
    fi

    rm -f "$tmp_cron"
    echo "✅ Existing Vilona jobs removed"
}

echo "========================================="
echo "Vilona Autonomous Monitoring Setup"
echo "========================================="
echo ""

# Check if already installed
if has_vilona_jobs; then
    echo "⚠️  Existing Vilona cron jobs detected"
    echo ""
    echo "Options:"
    echo "  1) Keep existing jobs (skip installation)"
    echo "  2) Replace with new jobs"
    echo ""
    read -p "Choose [1/2]: " choice

    case $choice in
        2)
            remove_vilona_jobs
            add_to_crontab
            ;;
        *)
            echo "Keeping existing jobs"
            ;;
    esac
else
    # Install new jobs
    add_to_crontab
fi

# Show installed jobs
echo ""
echo "========================================="
echo "Current Crontab:"
echo "========================================="
crontab -l | grep -A 20 "Vilona Autonomous Monitoring" || echo "No Vilona jobs found in crontab"

echo ""
echo "========================================="
echo "Monitoring Schedule:"
echo "========================================="
echo "Heartbeat:           Every 6 hours (regular reports)"
echo "Revenue Gap:         Every 2 hours (CRITICAL)"
echo "LYNK Dashboard:      Every 3 hours (manual check)"
echo "Cashflow:            Daily 9 AM (tracking)"
echo "PostBridge Health:   Every 30 minutes (API checks)"
echo "Memory Compaction:   Daily 3 AM (cleanup)"
echo "Disk Monitor:        Every 6 hours (space check)"
echo ""
echo "Logs location: $LOGS_DIR"
echo ""
echo "✅ Setup complete!"
echo ""
echo "To view active jobs:"
echo "  crontab -l"
echo ""
echo "To remove all jobs:"
echo "  crontab -e"
echo "Then delete Vilona sections"
echo "========================================="