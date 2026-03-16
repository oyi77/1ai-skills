#!/bin/bash
# 1ai Autonomous Revenue Loop
# This is the "Heartbeat" of the Business Kingdom.
# It pulls stats, assesses them, and set directives for the agent.

CDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"

cd "$WORKSPACE"

echo "[$(date)] --- STARTING AUTONOMOUS LOOP ---"

# 1. Collect State (Pull from APIs/Banks)
echo "[$(date)] step 1: collecting business state..."
python3 scripts/collect_business_state.py

# 2. Assess & Direct (Logic Engine)
echo "[$(date)] step 2: assessing kingdom health..."
python3 scripts/orchestrator_boss.py

# 3. Synchronize with Paperclip (The Task Brain)
if [ -f "scripts/openclaw_paperclip_bridge.py" ]; then
    echo "[$(date)] step 3: syncing with Paperclip..."
    python3 scripts/openclaw_paperclip_bridge.py analytics
fi

# 4. Report to Telegram (The Notification)
# If DIRECTIVE.md exists, send a summary
if [ -f "DIRECTIVE.md" ]; then
    DIRECTIVE_SUMMARY=$(head -n 10 DIRECTIVE.md)
    # Note: Assistance with message sending is handled by the model in its turn, 
    # but the loop can log it for the model to see at startup.
    echo "[$(date)] NEW DIRECTIVE DETECTED:"
    cat DIRECTIVE.md
fi

echo "[$(date)] --- LOOP COMPLETE ---"
