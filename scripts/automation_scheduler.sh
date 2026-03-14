#!/bin/bash
# JENDRALBOT AUTOMATION SCHEDULER
# Runs all automation tasks automatically with rate limiting

WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/automation_scheduler.log"

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Main scheduler
main() {
    log "=== JENDRALBOT AUTOMATION SCHEDULER STARTED ==="
    
    # Check if rate limit reset (has it been 24 hours since first 500 error?)
    # Simple heuristic: check last HTTP 500 time in logs
    LAST_ERROR=$(grep '"error"' "$WORKSPACE/logs/postbridge_upload_log.txt" | tail -1)
    
    if [ -n "$LAST_ERROR" ]; then
        # Wait 24 hours from last error
        log "Rate limit recovery detected. Waiting 24 hours..."
        sleep 86400  # 24 hours
    fi
    
    # Start Instagram uploads with rate limiting
    log "Starting Instagram uploads..."
    cd "$WORKSPACE"
    
    # Batch 1: Complete failed Instagram posts (47 posts)
    for i in {1..5}; do
        log "Instagram batch $i (10 posts each)..."
        python3 scripts/rate_limit_aware_upload.py --platform instagram --batch 10
        sleep 300  # 5 minutes between batches
    done
    
    log "Instagram uploads complete. Waiting 1 hour..."
    sleep 3600  # 1 hour
    
    # Batch 2: Remaining Instagram posts (101 more)
    for i in {1..10}; do
        log "Instagram batch $((5+i)) (10 posts each)..."
        python3 scripts/rate_limit_aware_upload.py --platform instagram --batch 10
        sleep 300
    done
    
    log "Instagram phase complete!"
    
    # Wait 1 hour before Facebook
    log "Waiting 1 hour before Facebook phase..."
    sleep 3600
    
    # Start Facebook uploads
    log "Starting Facebook uploads..."
    
    # Facebook batches (156 posts)
    for i in {1..16}; do
        log "Facebook batch $i (10 posts each)..."
        python3 scripts/rate_limit_aware_upload.py --platform facebook --batch 10
        sleep 300
    done
    
    log "Facebook uploads complete!"
    log "=== ALL AUTOMATION TASKS COMPLETE ==="
    
    # Send notification
    log "JENDRALBOT automation complete. Check LYNK dashboard for revenue."
}

main "$@"