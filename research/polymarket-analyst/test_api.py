#!/usr/bin/env python3
"""
Polymarket Market Scanner - Lightweight version
Quick market scan with basic categorization
"""

import requests
import json
from datetime import datetime

# Test API call
url = "https://clob.polymarket.com/markets"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()

    print(f"API Response Type: {type(data)}")
    print(f"Data Keys: {data.keys() if isinstance(data, dict) else 'N/A'}")

    if isinstance(data, dict):
        if "markets" in data:
            markets = data["markets"]
        elif "data" in data:
            markets = data["data"]
        else:
            markets = data
    else:
        markets = data

    print(f"Number of items: {len(markets)}")
    print(f"First item type: {type(markets[0]) if markets else 'Empty'}")

    if markets and isinstance(markets[0], dict):
        print(f"First market keys: {list(markets[0].keys())[:10]}")
    elif markets:
        print(f"First item: {markets[0]}")

except Exception as e:
    print(f"Error: {e}")
