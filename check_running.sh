#!/bin/bash
# Quick status check - is everything auto-running?

echo "======================================================================"
echo "🔍 AUTOMATION STATUS CHECK"
echo "======================================================================"
echo ""
echo "[1] Cron Jobs:"
crontab -l
echo ""
echo "[2] Last automation log:"
tail -20 ~/automation.log 2>/dev/null || echo "No log yet"
echo ""
echo "[3] PostBridge status:"
ls -lh autopilot_affiliate_engine/postbridge_queue_jendralbot.json 2>/dev/null | head -3
echo ""
echo "[4] Active processes:"
ps aux | grep -E "(auto_postbridge|fully_autonomous)" | grep -v grep || echo "No active processes"
echo ""
echo "======================================================================"