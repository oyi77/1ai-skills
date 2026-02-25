#!/bin/bash
# VILONA COMPREHENSIVE BACKTEST - SEMUA STRATEGI
cd /home/openclaw/.openclaw/workspace/skills/1ai-skills/trading

PYTHON_VENV="/home/openclaw/.trading-venv/bin/python"

echo "================================================================================"
echo "VILONA COMPREHENSIVE BACKTEST - ALL STRATEGIES"
echo "================================================================================"
echo ""

# Config
START_DATE="2025-01-01"
END_DATE="2025-12-31"
INITIAL_BALANCE="100"

# Tests
TESTS=(
    # Holy Grail (Forex)
    "holy_grail GBPUSD"
    "holy_grail EURUSD"
    "holy_grail USDJPY"

    # Momentum Elder (Forex)
    "momentum_elder GBPUSD"
    "momentum_elder EURUSD"
    "momentum_elder USDJPY"

    # Kumo Breakout (Forex)
    "kumo_breakout GBPUSD"
    "kumo_breakout EURUSD"
    "kumo_breakout USDJPY"

    # Volume Momentum (Crypto)
    "volume_momentum BTCUSDT"
    "volume_momentum ETHUSDT"
    "volume_momentum SOLUSDT"
)

# Run tests
for test in "${TESTS[@]}"; do
    read -r strategy symbol <<< "$test"

    echo "[$counter/12] $strategy on $symbol..."

    result=$($PYTHON_VENV strategy_wrapper.py $strategy $symbol backtest $START_DATE $END_DATE --initial-balance $INITIAL_BALANCE 2>&1)

    # Save to file
    filename="backtest_${strategy}_${symbol}.json"
    echo "$result" > "/tmp/$filename"

    if echo "$result" | grep -q "win_rate"; then
        # Extract metrics
        wr=$(echo "$result" | grep -oP '"win_rate": \K[0-9.]+')
        pnl=$(echo "$result" | grep -oP '"usd": [0-9.-]+')
        trades=$(echo "$result" | grep -oP '"total_trades": \K[0-9]+')
        echo "✅ WR: $wr% PNL: $$pnl Trades: $trades"
    else
        error=$(echo "$result" | grep -oP '"error": "[^"]+' | head -c 50)
        echo "❌ FAILED: $error"
    fi

    counter=$((counter + 1))
    echo ""
done

echo "================================================================================"
echo "BACKTEST COMPLETE"
echo "================================================================================"
echo ""
echo "All results saved in /tmp/"
ls -lh /tmp/backtest_*.json
echo ""
echo "================================================================================"
echo "NEXT: Parse all results and generate comparison report"
echo "================================================================================"
