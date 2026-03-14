#!/bin/bash

# Configuration
SERVICE_NAME="PostBridge"
PORT=8080
LOG_FILE="/home/openclaw/.openclaw/workspace/logs/postbridge_guard.log"
RESTART_CMD="npm start --prefix /home/openclaw/.openclaw/workspace/autopilot_affiliate_engine"
MAX_RETRIES=3

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

check_service() {
    if lsof -i :$PORT > /dev/null; then
        return 0
    else
        return 1
    fi
}

start_service() {
    log "⚠️ Service $SERVICE_NAME is DOWN on port $PORT. Attempting restart..."
    
    # Kill any lingering process just in case
    pkill -f "autopilot_affiliate_engine" 2>/dev/null
    
    # Start service in background
    nohup $RESTART_CMD > /home/openclaw/.openclaw/workspace/logs/postbridge_service.log 2>&1 &
    
    # Wait for startup
    sleep 10
    
    if check_service; then
        log "✅ Service $SERVICE_NAME successfully RESTARTED."
        return 0
    else
        log "❌ Failed to restart $SERVICE_NAME."
        return 1
    fi
}

# Main Logic
if check_service; then
    # Service is running, do nothing (silent success)
    exit 0
else
    # Service is down, try to restart
    attempt=1
    while [ $attempt -le $MAX_RETRIES ]; do
        if start_service; then
            exit 0
        fi
        log "Retry $attempt/$MAX_RETRIES failed. Waiting..."
        sleep 5
        ((attempt++))
    done
    
    log "🆘 CRITICAL: $SERVICE_NAME failed to start after $MAX_RETRIES attempts."
    exit 1
fi
