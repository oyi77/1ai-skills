#!/bin/bash
export SIMMER_API_KEY="sk_live_269696a939dec0c28c8165da1e3ba2a7f0367a1362a2b1cd412db1b033c07f1e"
export SIM_TRADE_AMOUNT="5.0"
export SIM_MAX_TRADES="3"
cd /home/openclaw/.openclaw/workspace
timeout 30 python3 scripts/simmer_quick_trade.py >> logs/simmer_trader.log 2>&1
