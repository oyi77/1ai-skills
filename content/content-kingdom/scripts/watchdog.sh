#!/bin/bash
# Content Kingdom Watchdog — auto-run pipeline, detect failures, self-heal
# Called by cron every 30 minutes

set -euo pipefail

SKILL_DIR="/home/openclaw/.openclaw/workspace/skills/content-kingdom"
LOG="$SKILL_DIR/logs/watchdog.log"
STATE="$SKILL_DIR/state.json"
MAX_FAILURES=3
ALERT_CHAT="5220170786"

mkdir -p "$SKILL_DIR/logs"
cd "$SKILL_DIR"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"; }

# ── Check if pipeline needs to run ──────────────────────────────────────────
HOUR=$(date '+%-H')
LAST_RUN=$(python3 -c "
import json,os
try:
    d=json.load(open('state.json'))
    print(d.get('last_run','never'))
except:
    print('never')
" 2>/dev/null)

LAST_RUN_EPOCH=0
if [[ "$LAST_RUN" != "never" ]]; then
    # Extract date from run_YYYYMMDD_HHMMSS
    RUN_DATE=$(echo "$LAST_RUN" | sed 's/run_//' | sed 's/_/ /' | sed 's/\([0-9]\{4\}\)\([0-9]\{2\}\)\([0-9]\{2\}\)/\1-\2-\3/')
    LAST_RUN_EPOCH=$(date -d "$RUN_DATE" +%s 2>/dev/null || echo 0)
fi

NOW_EPOCH=$(date +%s)
HOURS_AGO=$(( (NOW_EPOCH - LAST_RUN_EPOCH) / 3600 ))

log "Last run: $LAST_RUN ($HOURS_AGO hours ago)"

# Run if: morning window (7-9), evening window (19-21), or pipeline hasn't run in 12+ hours
SHOULD_RUN=0
if [[ $HOUR -ge 7 && $HOUR -le 9 ]]; then SHOULD_RUN=1; fi
if [[ $HOUR -ge 19 && $HOUR -le 21 ]]; then SHOULD_RUN=1; fi
if [[ $HOURS_AGO -ge 12 ]]; then SHOULD_RUN=1; fi

if [[ $SHOULD_RUN -eq 0 ]]; then
    log "Outside run window and recent run OK. Skipping."
    exit 0
fi

# ── Run pipeline ─────────────────────────────────────────────────────────────
log "Starting pipeline..."
PIPELINE_LOG="$SKILL_DIR/logs/pipeline_$(date +%Y%m%d_%H%M%S).log"

if timeout 1800 python3 "$SKILL_DIR/orchestrator.py" --pipeline > "$PIPELINE_LOG" 2>&1; then
    log "✅ Pipeline completed successfully"
    # Run self-improve after success
    python3 "$SKILL_DIR/scripts/self_improve.py" >> "$LOG" 2>&1 || true
else
    EXIT_CODE=$?
    log "❌ Pipeline failed (exit $EXIT_CODE)"

    # Read failure count
    FAILURES=$(python3 -c "
import json,os
try:
    d=json.load(open('$SKILL_DIR/logs/failure_state.json'))
    print(d.get('count',0))
except:
    print(0)
" 2>/dev/null)
    FAILURES=$((FAILURES + 1))

    # Save failure count
    echo "{\"count\": $FAILURES, \"last_error\": \"exit $EXIT_CODE\", \"ts\": \"$(date -Iseconds)\"}" > "$SKILL_DIR/logs/failure_state.json"

    # Try self-heal
    log "Attempting self-heal (failure $FAILURES/$MAX_FAILURES)..."
    python3 "$SKILL_DIR/scripts/self_heal.py" >> "$LOG" 2>&1 || true

    # Alert if too many failures
    if [[ $FAILURES -ge $MAX_FAILURES ]]; then
        log "🚨 $MAX_FAILURES consecutive failures — alerting"
        # Send Telegram alert via openclaw
        curl -s -X POST "http://localhost:18789/api/message/send" \
            -H "Content-Type: application/json" \
            -d "{\"channel\":\"telegram\",\"target\":\"$ALERT_CHAT\",\"message\":\"🚨 Content Kingdom GAGAL $FAILURES kali berturut-turut. Pipeline mati. Cek log: $(basename $PIPELINE_LOG)\"}" 2>/dev/null || true
        echo "{\"count\": 0}" > "$SKILL_DIR/logs/failure_state.json"
    fi
    exit 1
fi

# Reset failure count on success
echo "{\"count\": 0}" > "$SKILL_DIR/logs/failure_state.json"
