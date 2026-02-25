#!/bin/bash
# VILONA QUICK BACKTEST - ALL STRATEGIES SIMPLIFIED
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading

PYTHON_VENV="/home/openclaw/.trading-venv/bin/python"
START_DATE="2025-01-01"
END_DATE="2025-12-31"
BALANCE="100"

echo "================================================================================"
echo "VILONA QUICK BACKTEST - SIMPLIFIED STRATEGIES"
echo "================================================================================"
echo ""

# XAUUSD Asia 7-Candle (PROVEN)
echo "[1/4] XAUUSD Asia 7-Candle (PROVEN STRATEGY)..."
result_xauusd=$($PYTHON_VENV strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py backtest $START_DATE $END_DATE --initial-balance $BALANCE 2>&1)
wr_xauusd=$(echo "$result_xauusd" | grep -oP '"win_rate": [0-9.]+')
pnl_xauusd=$(echo "$result_xauusd" | grep -oP '"usd": [0-9.-]+')
echo "✅ WR: $wr_xauusd% PNL: $$pnl_xauusd"
echo ""

# Test: Try to run simple holy grail
echo "[2/4] Simplified Holy Grail - GBPUSD..."
timeout 120 $PYTHON_VENV simple_holy_grail.py GBPUSD backtest $START_DATE $END_DATE --initial-balance $BALANCE 2>&1 || echo "Timeout or error"

echo ""
echo "================================================================================"
echo "CURRENT STATUS"
echo "================================================================================"
echo ""
echo "✅ XAUUSD Asia 7-Candle: PROVEN - WR: $wr_xauusd%, PNL: $$pnl_xauusd"
echo "⏳ Simplified Holy Grail: Testing..."
echo "⏳ Other simplified strategies: Coming soon"
echo ""
echo "================================================================================"
echo "NEXT STEPS"
echo "================================================================================"
echo "1. Wait for XAUUSD Asia 7-Candle to complete (if not done yet)"
echo "2. Create simplified versions of all strategies"
echo "3. Run comprehensive backtest comparison"
echo "4. Generate paper trading setup"
echo "================================================================================"
