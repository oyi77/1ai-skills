#!/usr/bin/env python3
"""
Polymarket Market Scanner - Debug version
"""

import requests
import json

url = "https://clob.polymarket.com/markets"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    markets = data.get("data", [])
    
    if markets:
        # Print full first market
        print("First market structure:")
        print(json.dumps(markets[0], indent=2)[:2000])
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
