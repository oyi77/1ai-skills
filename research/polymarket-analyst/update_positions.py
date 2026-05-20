#!/usr/bin/env python3
"""
Polymarket Trading Update Script
Add existing positions and generate full report
"""

import json
from datetime import datetime
from pathlib import Path

data_file = Path(__file__).parent / "paper_trading_data.json"

# Load current data
if data_file.exists():
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {
        "balance": 100.0,
        "positions": [],
        "trade_history": [],
        "decision_log": [],
        "last_updated": datetime.now().isoformat(),
    }

# Add existing Trump deport trades from earlier
trump_trade_1 = {
    "id": "trade_trump_deport_250k_500k",
    "market_id": "trump_deport_250k_500k",
    "market_title": "Will Trump deport 250,000-500,000 people?",
    "side": "YES",
    "amount": 10,
    "entry_odds": 0.887,
    "entry_time": "2026-02-14T14:55:00",
    "status": "OPEN",
    "unrealized_pnl": 0.0,
    "realized_pnl": 0.0,
    "strategy": "Strategy: High confidence deport range",
}

trump_trade_2 = {
    "id": "trade_trump_deport_500k_750k",
    "market_id": "trump_deport_500k_750k",
    "market_title": "Will Trump deport 500,000-750,000 people?",
    "side": "NO",
    "amount": 10,
    "entry_odds": 0.057,  # 94.6% NO means YES is 94.6%, so NO is 5.4%
    "entry_time": "2026-02-14T14:55:00",
    "status": "OPEN",
    "unrealized_pnl": 0.0,
    "realized_pnl": 0.0,
    "strategy": "Strategy: Avoid upper range",
}

# Check if Trump trades already exist
trump_ids = [t["id"] for t in data.get("positions", [])]

if trump_trade_1["id"] not in trump_ids:
    data["positions"].append(trump_trade_1)
    data["trade_history"].append(trump_trade_1)
    data["decision_log"].append(
        {
            "timestamp": trump_trade_1["entry_time"],
            "action": "PLACE_TRADE",
            "market": trump_trade_1["market_title"],
            "side": trump_trade_1["side"],
            "amount": trump_trade_1["amount"],
            "odds": trump_trade_1["entry_odds"],
            "reasoning": trump_trade_1["strategy"],
        }
    )

if trump_trade_2["id"] not in trump_ids:
    data["positions"].append(trump_trade_2)
    data["trade_history"].append(trump_trade_2)
    data["decision_log"].append(
        {
            "timestamp": trump_trade_2["entry_time"],
            "action": "PLACE_TRADE",
            "market": trump_trade_2["market_title"],
            "side": trump_trade_2["side"],
            "amount": trump_trade_2["amount"],
            "odds": trump_trade_2["entry_odds"],
            "reasoning": trump_trade_2["strategy"],
        }
    )

# Update balance
total_locked = sum(p["amount"] for p in data["positions"])
data["balance"] = 100.0  # Keep initial as virtual reference

data["last_updated"] = datetime.now().isoformat()

# Save
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated trading data with all positions")
print(f"Total open positions: {len(data['positions'])}")
print(f"Total locked: ${total_locked}")
print(f"Available: ${100 - total_locked}")
