#!/usr/bin/env python3
"""
Quick debug of Polymarket API data
"""

import requests

url = "https://clob.polymarket.com/markets"

try:
    response = requests.get(url, timeout=30)
    data = response.json()
    markets = data.get("data", [])

    print(f"Total markets received: {len(markets)}")

    if markets:
        sample = markets[3]  # Get 4th market
        print("\nSample market values:")
        print(f"  active: {sample.get('active')}")
        print(f"  closed: {sample.get('closed')}")
        print(f"  archived: {sample.get('archived')}")
        print(f"  accepting_orders: {sample.get('accepting_orders')}")
        print(f"  end_date_iso: {sample.get('end_date_iso')}")

        # Count by status
        counts = {
            "active_True": 0,
            "active_False": 0,
            "closed_True": 0,
            "closed_False": 0,
        }
        for m in markets:
            if m.get("active"):
                counts["active_True"] += 1
            else:
                counts["active_False"] += 1
            if m.get("closed"):
                counts["closed_True"] += 1
            else:
                counts["closed_False"] += 1

        print("\nStatus counts:")
        print(f"  Active=True: {counts['active_True']}")
        print(f"  Active=False: {counts['active_False']}")
        print(f"  Closed=True: {counts['closed_True']}")
        print(f"  Closed=False: {counts['closed_False']}")

        # What does accepting_orders mean?
        accepting = sum(1 for m in markets if m.get("accepting_orders"))
        print(f"\n  Accepting orders: {accepting}")

except Exception as e:
    print(f"Error: {e}")
