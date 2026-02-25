#!/bin/bash
# Auto fix and run backtests

echo "VILONA - AUTO BACKTEST FIX & RUN"
echo "====================================="
echo ""

# Navigate to trading directory
if [ -d "skills/trading" ]; then
    cd skills/trading
    echo "Changed to: $(pwd)"
elif [ -d "trading" ]; then
    cd trading
    echo "Changed to: $(pwd)"
else
    echo "ERROR: trading directory not found"
    exit 1
fi

echo ""
echo "Running backtests..."
echo "====================================="

# Run all 3 tests in parallel
~/.trading-venv/bin/python scripts/working_runner.py

echo ""
echo "====================================="
echo "COMPLETE"
