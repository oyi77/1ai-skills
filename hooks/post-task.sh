#!/bin/bash
SKILL_USED="${1:-unknown}"
TASK_TYPE="${2:-unknown}"
SUCCESS="${3:-unknown}"
DURATION="${4:-0}"

LOG_FILE=".hooks/performance.log"

echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] skill=$SKILL_USED task=$TASK_TYPE success=$SUCCESS duration=${DURATION}ms" >> "$LOG_FILE"

tail -1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"

echo "[post-task] Logged: $SKILL_USED ($SUCCESS in ${DURATION}ms)"
