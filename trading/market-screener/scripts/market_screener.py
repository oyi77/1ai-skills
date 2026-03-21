#!/usr/bin/env python3
"""
Market Screener — top movers, volume spikes, assets near key levels.

Usage:
    python market_screener.py --market all --output json
    python market_screener.py movers
    python market_screener.py volume
    python market_screener.py levels
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import numpy as np
    import yfinance as yf
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Run: pip install yfinance numpy")
    sys.exit(1)

WATCHLIST = {
    "GC=F": "Gold",
    "BTC-USD": "Bitcoin",
    "DX-Y.NYB": "US Dollar Index",
    "^GSPC": "S&P 500",
    "CL=F": "Crude Oil",
    "SI=F": "Silver",
    "ETH-USD": "Ethereum",
    "EURUSD=X": "EUR/USD",
}


def get_ticker_data(ticker, period="5d"):
    """Fetch recent data for a ticker."""
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period)
        if df.empty:
            return None
        return df
    except Exception:
        return None


def screen_movers(tickers=None):
    """Screen for top gainers and losers."""
    tickers = tickers or WATCHLIST
    results = []

    for ticker, name in (tickers.items() if isinstance(tickers, dict) else [(t, t) for t in tickers]):
        df = get_ticker_data(ticker, "5d")
        if df is None or len(df) < 2:
            continue
        current = float(df["Close"].iloc[-1])
        prev = float(df["Close"].iloc[-2])
        change_pct = (current - prev) / prev * 100

        results.append({
            "ticker": ticker,
            "name": name,
            "price": round(current, 4),
            "change": round(current - prev, 4),
            "change_pct": round(change_pct, 2),
        })

    results.sort(key=lambda x: x["change_pct"], reverse=True)
    return {"gainers": results[:5], "losers": results[-5:][::-1], "timestamp": datetime.now().isoformat()}


def screen_volume_spikes(tickers=None):
    """Detect unusual volume (> 1.5x 20-day average)."""
    tickers = tickers or WATCHLIST
    results = []

    for ticker, name in (tickers.items() if isinstance(tickers, dict) else [(t, t) for t in tickers]):
        df = get_ticker_data(ticker, "1mo")
        if df is None or len(df) < 5 or "Volume" not in df.columns:
            continue

        vol = df["Volume"]
        if vol.sum() == 0:
            continue

        avg_vol = float(vol[:-1].mean()) if len(vol) > 1 else float(vol.mean())
        latest_vol = float(vol.iloc[-1])

        if avg_vol > 0:
            ratio = latest_vol / avg_vol
            if ratio > 1.5:
                results.append({
                    "ticker": ticker,
                    "name": name,
                    "latest_volume": int(latest_vol),
                    "avg_volume": int(avg_vol),
                    "ratio": round(ratio, 2),
                    "spike": True,
                })

    results.sort(key=lambda x: x["ratio"], reverse=True)
    return {"volume_spikes": results, "timestamp": datetime.now().isoformat()}


def screen_near_levels(tickers=None):
    """Find assets near their support or resistance levels."""
    tickers = tickers or WATCHLIST
    results = []

    for ticker, name in (tickers.items() if isinstance(tickers, dict) else [(t, t) for t in tickers]):
        df = get_ticker_data(ticker, "3mo")
        if df is None or len(df) < 20:
            continue

        current = float(df["Close"].iloc[-1])
        high_20 = float(df["High"].tail(20).max())
        low_20 = float(df["Low"].tail(20).min())
        range_20 = high_20 - low_20

        if range_20 == 0:
            continue

        # Check proximity to levels (within 1% of range)
        threshold = range_20 * 0.03
        near_resistance = abs(current - high_20) < threshold
        near_support = abs(current - low_20) < threshold

        if near_resistance or near_support:
            results.append({
                "ticker": ticker,
                "name": name,
                "price": round(current, 4),
                "resistance_20d": round(high_20, 4),
                "support_20d": round(low_20, 4),
                "near_resistance": near_resistance,
                "near_support": near_support,
                "distance_to_resistance_pct": round((high_20 - current) / current * 100, 2),
                "distance_to_support_pct": round((current - low_20) / current * 100, 2),
            })

    return {"near_levels": results, "timestamp": datetime.now().isoformat()}


def screen_all():
    """Run all screens."""
    return {
        "movers": screen_movers(),
        "volume_spikes": screen_volume_spikes(),
        "near_levels": screen_near_levels(),
        "timestamp": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Market Screener")
    parser.add_argument("command", nargs="?", default="all", choices=["all", "movers", "volume", "levels"])
    parser.add_argument("--market", default="all")
    parser.add_argument("--output", default="text", choices=["text", "json"])

    args = parser.parse_args()

    if args.command == "movers":
        result = screen_movers()
    elif args.command == "volume":
        result = screen_volume_spikes()
    elif args.command == "levels":
        result = screen_near_levels()
    else:
        result = screen_all()

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        if "gainers" in result:
            print("=== Top Movers ===")
            print(f"{'Ticker':<12} {'Name':<20} {'Price':>10} {'Change':>10} {'%':>8}")
            print("-" * 62)
            for g in result.get("gainers", []):
                print(f"{g['ticker']:<12} {g['name']:<20} {g['price']:>10.4f} {g['change']:>+10.4f} {g['change_pct']:>+7.2f}%")
            print()
            for l in result.get("losers", []):
                print(f"{l['ticker']:<12} {l['name']:<20} {l['price']:>10.4f} {l['change']:>+10.4f} {l['change_pct']:>+7.2f}%")
        elif "movers" in result:
            # Full screen_all output
            movers = result["movers"]
            print("=== Top Gainers ===")
            for g in movers.get("gainers", [])[:3]:
                print(f"  {g['name']}: {g['price']:.4f} ({g['change_pct']:+.2f}%)")
            print("=== Top Losers ===")
            for l in movers.get("losers", [])[:3]:
                print(f"  {l['name']}: {l['price']:.4f} ({l['change_pct']:+.2f}%)")

            spikes = result.get("volume_spikes", {}).get("volume_spikes", [])
            if spikes:
                print("\n=== Volume Spikes ===")
                for s in spikes:
                    print(f"  {s['name']}: {s['ratio']:.1f}x average volume")

            levels = result.get("near_levels", {}).get("near_levels", [])
            if levels:
                print("\n=== Near Key Levels ===")
                for lv in levels:
                    tag = "RESISTANCE" if lv["near_resistance"] else "SUPPORT"
                    print(f"  {lv['name']}: {lv['price']:.4f} (near {tag})")
        else:
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
