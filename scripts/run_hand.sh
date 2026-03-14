#!/bin/bash
# OpenFang-Style Hands Scheduler
# Runs all hands autonomously based on schedule

set -e

# Paths
WORKSPACE="/home/openclaw/.openclaw/workspace"
LOGS_DIR="$WORKSPACE/logs"

# Logs
HANDS_LOG="$LOGS_DIR/openfang_hands.log"

# Log function
log_hand() {
    local hand=$1
    local result=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') | Hand[$hand]: $result" >> "$HANDS_LOG"
    echo "✅ Hand[$hand]: $result"
}

# Run HAND: CLIP
run_clip_hand() {
    log_hand "CLIP" "Starting..."

    python3 "$WORKSPACE/hands/clip/hand.py" >> "$LOGS_DIR/clip.log" 2>&1

    if [ $? -eq 0 ]; then
        log_hand "CLIP" "Complete"
        return 0
    else
        log_hand "CLIP" "Failed (see logs/clip.log)"
        return 1
    fi
}

# Run HAND: LEAD
run_lead_hand() {
    log_hand "LEAD" "Starting..."

    python3 "$WORKSPACE/hands/lead/hand.py" >> "$LOGS_DIR/lead.log" 2>&1

    if [ $? -eq 0 ]; then
        log_hand "LEAD" "Complete"
        return 0
    else
        log_hand "LEAD" "Failed (see logs/lead.log)"
        return 1
    fi
}

# Run HAND: COLLECTOR
run_collector_hand() {
    log_hand "COLLECTOR" "Starting..."

    python3 "$WORKSPACE/hands/collector/hand.py" >> "$LOGS_DIR/collector.log" 2>&1

    if [ $? -eq 0 ]; then
        log_hand "COLLECTOR" "Complete"
        return 0
    else
        log_hand "COLLECTOR" "Failed (see logs/collector.log)"
        return 1
    fi
}

# Main scheduler
case "$1" in
    clip)
        run_clip_hand
        ;;
    lead)
        run_lead_hand
        ;;
    collector)
        run_collector_hand
        ;;
    all)
        echo "Running all hands..."
        run_collector_hand
        run_lead_hand
        run_clip_hand
        ;;
    *)
        echo "Usage: $0 {clip|lead|collector|all}"
        exit 1
        ;;
esac

exit $?