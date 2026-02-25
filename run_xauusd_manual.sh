#!/bin/bash
# VILONA FINAL - MANUAL BACKTEST XAUUSD 3 TIMEFRAMES
cd skills/1ai-skills/trading

echo "================================================================================"
echo "VILONA FINAL BACKTEST - XAUUSD ASIA 7-CANDLE - 3 TIMEFRAMES"
echo "================================================================================"

echo ""
echo "[1/3] XAUUSD H1..."
~/.trading-venv/bin/python strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py backtest 2025-01-01 2025-12-31 --initial-balance 100 > /tmp/xauusd_h1.json 2>&1
echo "✅ Done"

echo ""
echo "[2/3] XAUUSD H4..."
~/.trading-venv/bin/python strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py backtest 2025-01-01 2025-12-31 --initial-balance 100 > /tmp/xauusd_h4.json 2>&1
echo "✅ Done"

echo ""
echo "[3/3] XAUUSD D1..."
~/.trading-venv/bin/python strategy/tradfi/commodities/xauusd_asia_7c_breakout/xauusd_asia_7c_breakout.py backtest 2025-01-01 2025-12-31 --initial-balance 100 > /tmp/xauusd_d1.json 2>&1
echo "✅ Done"

echo ""
echo "================================================================================"
echo "RESULTS"
echo "================================================================================"

echo ""
echo "H1:"
cat /tmp/xauusd_h1.json | grep -A2 "win_rate"

echo ""
echo "H4:"
cat /tmp/xauusd_h4.json | grep -A2 "win_rate"

echo ""
echo "D1:"
cat /tmp/xauusd_d1.json | grep -A2 "win_rate"

echo ""
echo "================================================================================"
echo "COMPLETE"
echo "================================================================================"
