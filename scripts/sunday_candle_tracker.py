#!/usr/bin/env python3
"""
XAUUSD Candle Tracker - Sunday Protocol C Automation
Tracks 15-minute candles from 07:00-14:00 UTC+7
At 14:50, calculates 7-candle range and generates entry decision
Works WITHOUT broker connection (uses public price APIs)
"""

import json
import requests
import sys
from datetime import datetime, timedelta

# Configuration
CONFIG = {
    # Sunday March 8, 2026 UTC+7 trading window
    "start_hour_utc7": 7,      # 07:00 UTC+7
    "end_hour_utc7": 14,       # 14:00 UTC+7
    "calculation_hour_utc7": 14.83,  # 14:50 UTC+7 (14 + 50/60)
    "entry_hour_utc7": 15.0,       # 15:00 UTC+7

    # API Configuration (free gold price API)
    "price_api": "https://api Metals.live/v1/spot/gold",
    "fallback_api": "https://api.exchangerate-api.com/v4/latest/USD",  # Has gold in commodities

    # Output files
    "candle_log": "/home/openclaw/.openclaw/workspace/temp/sunday-candles-2026-03-08.json",
    "decision_log": "/home/openclaw/.openclaw/workspace/temp/sunday-decision-2026-03-08.md",
}

def get_current_price():
    """Get current XAUUSD price from API"""
    try:
        # Try primary API
        response = requests.get(CONFIG["price_api"], timeout=10)
        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
    except Exception as e:
        print(f"Primary API failed: {e}")

    try:
        # Try fallback - note: this may not have gold directly
        response = requests.get(CONFIG["fallback_api"], timeout=10)
        if response.status_code == 200:
            data = response.json()
            # This API might have gold in different format
            # Adjust based on actual API response structure
            return data.get("rates", {}).get("XAU", 0.0)
    except Exception as e:
        print(f"Fallback API failed: {e}")

    return None

def get_utc7_hour():
    """Get current hour in UTC+7 timezone"""
    # For simplicity in this script, we'll use system time and assume it's UTC+7
    # In production, use pytz or zoneinfo for proper timezone handling
    now = datetime.now()
    return now.hour + now.minute / 60.0

def parse_existing_candles():
    """Load existing candle data"""
    try:
        with open(CONFIG["candle_log"], 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"candles": [], "last_update": None}

def save_candles(candles_data):
    """Save candle data"""
    with open(CONFIG["candle_log"], 'w') as f:
        json.dump(candles_data, f, indent=2)

def log_candle(candle_num, time, high, low, close):
    """Log a candle's data"""
    candles_data = parse_existing_candles()
    candles_data["candles"].append({
        "candle": candle_num,
        "time": time,
        "high": high,
        "low": low,
        "close": close
    })
    candles_data["last_update"] = datetime.now().isoformat()
    save_candles(candles_data)

def track_candles():
    """Main candle tracking loop"""
    current_hour = get_utc7_hour()

    # Check if we're within the tracking window (07:00-14:00 UTC+7)
    if not (CONFIG["start_hour_utc7"] <= current_hour < CONFIG["end_hour_utc7"]):
        print(f"Outside tracking window (07:00-14:00 UTC+7). Current: {current_hour:.2f}")
        return

    # Determine which candle we're tracking (15-minute intervals)
    elapsed_hours = current_hour - CONFIG["start_hour_utc7"]
    candle_index = int(elapsed_hours * 60 / 15)  # Convert hours to candle number

    if candle_index < 0 or candle_index >= 7:
        print("Outside 7-candle range")
        return

    # Get current price
    price = get_current_price()
    if price is None:
        print("Failed to get price from API")
        return

    # For this simple implementation, we'll just log snapshot prices
    # In production, you'd want to track high/low for each 15-minute candle
    print(f"Candle {candle_index + 1}: ${price:.2f}")

    # This is a simplified version - real implementation would:
    # 1. Start a new candle at each 15-minute mark
    # 2. Track high/low/close for the candle duration
    # 3. Finalize candle at the end of 15 minutes

def calculate_range():
    """Calculate 7-candle range"""
    candles_data = parse_existing_candles()
    candles = candles_data.get("candles", [])

    if len(candles) < 7:
        print("Need 7 candles to calculate range")
        return None, None, None

    # Find highest high and lowest low across all 7 candles
    highest_high = max(c["high"] for c in candles)
    lowest_low = min(c["low"] for c in candles)

    # Calculate range
    range_pips = highest_high - lowest_low

    return highest_high, lowest_low, range_pips

def generate_decision(range_pips):
    """Generate entry decision based on range"""
    if range_pips < 5:
        decision = "NO ENTRY"
        reason = f"Range ({range_pips:.2f} pips) too small (< 5 pips)"
        action = "Market consolidation, breakout signal too weak"
    elif range_pips >= 5:
        decision = "ENTRY QUALIFIED"
        reason = f"Range ({range_pips:.2f} pips) meets minimum (>= 5 pips)"
        action = f"Ready for entry: BUY above ${highest_high:.2f} or SELL below ${lowest_low:.2f}"
    else:
        decision = "INDECISIVE"
        reason = "Range calculation failed"
        action = "Manual review required"

    return decision, reason, action

def generate_decision_file(highest_high, lowest_low, range_pips):
    """Generate the decision report file"""
    decision, reason, action = generate_decision(range_pips)

    report = f"""# Sunday Trading Entry Decision - March 8, 2026

## 🕐 Current Time UTC+7
- Decision Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC+7
- Target Time: 15:00-15:05 UTC+7
- Status: {decision}

---

## 📊 7-Candle Range Summary

**Candle Data:**
- Highest High: ${highest_high:.2f}
- Lowest Low: ${lowest_low:.2f}
- **Range: {range_pips:.2f} pips**

---

## 🎯 Entry Decision

**Decision:** {decision}

**Reason:** {reason}

**Action Required:** {action}

---

## 📋 Decision Matrix

| Range (pips) | Qualification | Action |
|--------------|---------------|--------|
| < 5 pips | ❌ Too small | NO ENTRY |
| >= 5 pips | ✅ Qualified | ENTRY |

**Current: {range_pips:.2f} pips** {'✅ QUALIFIED' if range_pips >= 5 else '❌ TOO SMALL'}

---

## 💡 Next Steps

### If ENTRY QUALIFIED (range >= 5 pips):
- [ ] Monitor price at 15:00 UTC+7
- [ ] If price breaks ABOVE ${highest_high:.2f}: Consider BUY order
- [ ] If price breaks BELOW ${lowest_low:.2f}: Consider SELL order
- [ ] Note: Without broker connection, this is documentation-only

### If NO ENTRY (range < 5 pips):
- [ ] Market is consolidating, no clear breakout
- [ ] Watch next session (Monday 07:00 UTC+7)
- [ ] Consider larger timeframe analysis

---

## 🔮 Outlook

**Today's Session:**
- Strategy: Asia 7-candle breakout
- Entry Time: 15:00 UTC+7
- Confidence Level: {9 if range_pips >= 10 else 7 if range_pips >= 5 else 3}/10

**Monday's Session:**
- If no entry today: Review strategy, watch 4H timeframe
- If qualified today: Monitor position, adjust stop loss

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC+7
**Method:** Automated candle tracking + range calculation
**Next Update:** After 15:00 UTC+7 (if entry happens)

"""

    with open(CONFIG["decision_log"], 'w') as f:
        f.write(report)

    return report

def main():
    """Main execution"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sunday candle tracker running...")

    current_hour = get_utc7_hour()

    # Phase 1: Track candles (07:00-14:00)
    if CONFIG["start_hour_utc7"] <= current_hour < CONFIG["end_hour_utc7"]:
        print("Phase 1: Tracking candles...")
        track_candles()

    # Phase 2: Calculate range (14:50)
    elif CONFIG["end_hour_utc7"] <= current_hour < CONFIG["calculation_hour_utc7"]:
        print("Phase 2: Preparation phase - waiting for 14:50...")

    # Phase 3: Generate decision (14:50-15:00)
    elif CONFIG["calculation_hour_utc7"] <= current_hour < CONFIG["entry_hour_utc7"]:
        print("Phase 3: Calculating range and generating decision...")
        highest_high, lowest_low, range_pips = calculate_range()
        if highest_high and lowest_low and range_pips:
            report = generate_decision_file(highest_high, lowest_low, range_pips)
            print("\n" + "="*80)
            print(report)
            print("="*80)
            print(f"\nDecision report saved to: {CONFIG['decision_log']}")
        else:
            print("Failed to calculate range - insufficient candle data")

    # Phase 4: Entry window (15:00+)
    elif current_hour >= CONFIG["entry_hour_utc7"]:
        print("Phase 4: Entry window passed. Check decision report or wait for Monday.")
        if highest_high and lowest_low and range_pips:
            decision, _, _ = generate_decision(range_pips)
            print(f"Decision was: {decision}")
            print(f"Report: {CONFIG['decision_log']}")

    else:
        print(f"Before trading window (starts at {CONFIG['start_hour_utc7']}:00 UTC+7)")

if __name__ == "__main__":
    main()