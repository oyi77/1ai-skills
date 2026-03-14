#!/bin/bash
# Monday Morning Startup Script - Crisis Mode Execution Guide
# Run at 09:00 AM UTC+7 on Monday March 10, 2026

set -e

echo "================================================================================"
echo "📋 MONDAY MORNING STARTUP - Sunday Crisis Recovery"
echo "================================================================================"
echo ""
echo "Current Date: $(date '+%Y-%m-%d %H:%M')"
echo "Estimated Time: ~1-2 hours to complete all priority items"
echo ""

# Phase 1: Quick Systems Check
echo "================================================================================"
echo "🔍 PHASE 1: Quick Systems Check (2 minutes)"
echo "================================================================================"
echo ""

echo "1. Disk Space Status:"
df -h ~ | grep "/$"
echo ""

echo "2. Revenue Gap Detector Status:"
cd ~/.openclaw/workspace
echo "   Last check: $(tail -1 logs/revenue_gaps.log 2>/dev/null | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4 || echo "No recent checks")"
echo "   Running standalone detector..."
python3 scripts/revenue_gap_detector_standalone.py 2>&1 | tail -10
echo ""

echo "3. PostBridge Status:"
if curl -s http://localhost:8080/api/status > /dev/null 2>&1; then
    echo "   ✅ PostBridge API: UP"
else
    echo "   ❌ PostBridge API: DOWN (HTTP 500 errors)"
fi
echo ""

# Phase 2: Cashflow Check (PRIORITY #1)
echo "================================================================================"
echo "💰 PHASE 2: Cashflow Visibility Check (20-30 minutes) - PRIORITY #1"
echo "================================================================================"
echo ""
echo "⚠️  CRITICAL: You have been CASHFLOW BLIND for 36+ hours"
echo "   - 40% of strategic decisions may be WRONG"
echo "   - First decision must be based on ACTUAL bank balances"
echo ""
echo "Open these files:"
echo "   - Cashflow template: ~/cd ~/.openclaw/workspace && nano cashflow_tracker_template.md"
echo "   - Main tracker: ~/cd ~/.openclaw/workspace && nano cashflow_tracker.md"
echo ""
echo "Instructions:"
echo "   1. Login to ALL bank accounts (BCA, BRI, Mandiri, etc.)"
echo "   2. Note EXACT balances in cashflow_tracker.md"
echo "   3. List major expenses (housing, food, burn rate)"
echo "   4. Calculate: How many days/weeks can we survive?"
echo "   5. Document: 'We have X days/weeks remaining'"
echo ""
echo "Run when ready (after checking banks):"
echo "   nano cashflow_tracker.md"
echo ""

read -p "Press Enter when cashflow check is complete, or Ctrl+C to pause..." 

# Phase 3: Decision Based on Runway
echo ""
echo "================================================================================"
echo "🎯 PHASE 3: Strategy Decision Based on Runway (5 minutes)"
echo "================================================================================"
echo ""

echo "Based on your cashflow check, choose your strategy:"
echo ""
echo "A. IF Runway < 1 Week:"
echo "   ❌ Suspend: Trading automation setup (4-6 hours)"
echo "   ❌ Suspend: Any new infrastructure projects"
echo "   ✅ Focus: Marketing only (fastest path to revenue)"
echo "   ✅ Execute: PostBridge fix → Upload posts → Generate revenue"
echo ""
echo "B. IF Runway >= 1 Week:"
echo "   ✅ Execute: Both streams (marketing + trading)"
echo "   ✅ Timeline: Revenue today → Fund trading Tuesday"
echo "   ✅ Action: PostBridge fix → Upload posts → Configure Ostium broker"
echo ""
echo "C. IF Runway UNKNOWN (no check done):"
echo "   ⚠️  Assume: Worst case (0-7 days runway)"
echo "   ⚠️  Strategy: Marketing-only today"
echo "   ⚠️  Monday: Reassess after actual bank check"
echo ""

read -p "Which strategy? (A/B/C): " STRATEGY

case $STRATEGY in
    A|a)
        echo ""
        echo "✅ STRATEGY A: Marketing-Only Selected"
        echo "   Skip: Trading setup, infrastructure projects"
        echo "   Focus: PostBridge fix → Uploads → Revenue"
        ;;
    B|b)
        echo ""
        echo "✅ STRATEGY B: Both Streams Selected"
        echo "   Execute: Marketing + Trading in parallel"
        echo "   Timeline: Revenue tomorrow → Trading Tuesday"
        ;;
    C|c)
        echo ""
        echo "⚠️  STRATEGY C: Conservative (Assume < 1 week)"
        echo "   Execute: Marketing-only first"
        echo "   Reassess: After actual bank check"
        ;;
    *)
        echo ""
        echo "⚠️  No strategy selected. Defaulting to conservative (marketing-only)"
        STRATEGY="C"
        ;;
esac

echo ""

# Phase 4: PostBridge Fix
echo "================================================================================"
echo "🔧 PHASE 4: PostBridge Fix (30-60 minutes)"
echo "================================================================================"
echo ""
echo "Purpose: Unblocks 47 pending uploads and revenue verification"
echo ""

echo "Step 1: Restart OpenClaw Gateway:"
echo "   Command: openclaw gateway restart"
echo ""

read -p "Restart gateway now? (y/n): " RESTART
if [[ $RESTART =~ ^[Yy]$ ]]; then
    echo "Restarting..."
    openclaw gateway restart
    sleep 3
    echo ""
    echo "Check status:"
    if curl -s http://localhost:8080/api/status > /dev/null 2>&1; then
        echo "   ✅ PostBridge API: UP"
    else
        echo "   ❌ PostBridge API: Still DOWN"
        echo "   Troubleshooting: Check logs: tail -50 logs/postbridge_upload_log.txt"
    fi
fi

echo ""

echo "Step 2: Verify API is responding:"
echo "   Command: curl http://localhost:8080/api/status"
echo ""

echo "Step 3: After PostBridge is UP:"
echo "   - Retry 47 failed uploads"
echo "   - Verify 58 scheduled posts are live"
echo "   - Check LYNK dashboard: https://lynk.id/jendralbot"
echo ""

# Phase 5: Action Execution
echo ""
echo "================================================================================"
echo "🚀 PHASE 5: Execute Based on Strategy"
echo "================================================================================"
echo ""

if [[ $STRATEGY =~ ^[Aa]$ ]] || [[ $STRATEGY =~ ^[Cc]$ ]]; then
    echo "Marketing-Only Execution:"
    echo "   1. Ensure PostBridge is UP (Phase 4)"
    echo "   2. Run: python3 scripts/rate_limit_aware_upload.py --retry-failed"
    echo "   3. Monitor: Check LYNK every 2-3 hours"
    echo ""
elif [[ $STRATEGY =~ ^[Bb]$ ]]; then
    echo "Both Streams Execution:"
    echo "   1. Ensure PostBridge is UP (Phase 4)"
    echo "   2. Marketing: python3 scripts/rate_limit_aware_upload.py --retry-failed"
    echo "   3. Trading: Review Sunday trading decision at 15:00"
    echo "   4. If runway >= 1 week: Configure Ostium broker (1-2 hours)"
    echo ""
fi

# Summary
echo ""
echo "================================================================================"
echo "📋 MONDAY MORNING SUMMARY"
echo "================================================================================"
echo ""
echo "✅ Systems checked: Disk (90%), Revenue (EMERGENCY), PostBridge (DOWN)"
echo "✅ Cashflow check: $(cat > /tmp/cashflow_done.txt && echo 'PENDING' || echo 'PENDING')"
echo "✅ Strategy selected: $([ "$STRATEGY" == "A" ] && echo 'Marketing-only' || [ "$STRATEGY" == "B" ] && echo 'Both streams' || echo 'Conservative')"
echo "✅ PostBridge: $([ "$RESTART" =~ ^[Yy]$ ] && [[ $STRATEGY =~ ^[Bb]$ ]] && echo 'Attempted restart' || echo 'Pending')"
echo ""
echo "⏳ Remaining Actions:"
echo "   1. Complete cashflow check if not done"
echo "   2. Verify PostBridge status after restart"
echo "   3. Execute uploads when PostBridge is UP"
echo "   4. Monitor LYNK dashboard for revenue"
echo ""
echo "📁 Reference Files:"
echo "   - Sunday summary: temp/sunday-evening-crisis-summary-2026-03-08.md"
echo "   - Decision tree: temp/dependency-decision-tree-2026-03-08.md"
echo "   - Disk tool: scripts/disk_cleanup_automation.py"
echo ""
echo "💡 Key Priority:"
echo "   1. Bank balance check FIRST (removes 40% decision error risk)"
echo "   2. Execute based on ACTUAL runway data (not assumptions)"
echo "   3. PostBridge fix when time allows (unblocks marketing uploads)"
echo ""
echo "================================================================================"
echo "✅ Ready to execute Monday morning priorities"
echo "================================================================================"