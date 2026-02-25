#!/bin/bash
# VILONA ALTERNATIVE - JALANKAN DARI FOLDER YANG BENAR

cd "/home/openclaw/C:\Users\EX PC\.openclaw\workspace/skills/1ai-skills/trading"

echo "=== WORKING DIR ==="
echo "$PWD"
echo ""

echo "=== PYTHONPATH TEST ==="
PYTHONPATH="$PWD" ~/.trading-venv/bin/python -c "from trading.brokers.base import OHLCV; print('✅ SUCCESS: trading module found')"
