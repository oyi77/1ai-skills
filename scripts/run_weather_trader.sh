#!/bin/bash
export SIMMER_API_KEY="sk_live_269696a939dec0c28c8165da1e3ba2a7f0367a1362a2b1cd412db1b033c07f1e"
export WALLET_PRIVATE_KEY="0xddb6e8b389f667e5da21ad73d1becdc5159832027a280e86c545f2df50dec537"
export TRADING_VENUE="sim"
export SIMMER_WEATHER_LOCATIONS="NYC,Chicago,Seattle,Atlanta,Dallas,Miami"
cd /home/openclaw/.openclaw/workspace
python3 skills/polymarket-weather-trader/weather_trader.py --live --quiet >> logs/weather_trader.log 2>&1
