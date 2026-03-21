#!/usr/bin/env python3
"""
Technical Analysis — SMA, EMA, RSI, MACD, Bollinger Bands, Support/Resistance.

Usage:
    python technical_analysis.py --ticker GC=F --timeframe 1d
    python technical_analysis.py --ticker BTC-USD --timeframe 1h --json
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import numpy as np
    import pandas as pd
    import yfinance as yf
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Run: pip install yfinance numpy pandas")
    sys.exit(1)


TIMEFRAME_PERIODS = {
    "1m": "7d", "5m": "60d", "15m": "60d", "30m": "60d",
    "1h": "730d", "1d": "2y", "1wk": "5y",
}


def fetch_data(ticker, timeframe="1d"):
    """Fetch OHLCV data via yfinance."""
    period = TIMEFRAME_PERIODS.get(timeframe, "1y")
    t = yf.Ticker(ticker)
    df = t.history(period=period, interval=timeframe)
    if df.empty:
        print(f"ERROR: No data for {ticker} at {timeframe}")
        sys.exit(1)
    return df


def sma(data, period):
    """Simple Moving Average."""
    return data["Close"].rolling(window=period).mean()


def ema(data, period):
    """Exponential Moving Average."""
    return data["Close"].ewm(span=period, adjust=False).mean()


def rsi(data, period=14):
    """Relative Strength Index."""
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def macd(data, fast=12, slow=26, signal=9):
    """MACD line, signal line, histogram."""
    ema_fast = data["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = data["Close"].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(data, period=20, std_dev=2):
    """Bollinger Bands — upper, middle, lower."""
    middle = data["Close"].rolling(window=period).mean()
    std = data["Close"].rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower


def support_resistance(data, window=20):
    """Identify key support and resistance levels from recent highs/lows."""
    recent = data.tail(window * 3) if len(data) > window * 3 else data

    highs = recent["High"].rolling(window=window, center=True).max()
    lows = recent["Low"].rolling(window=window, center=True).min()

    resistance_levels = sorted(recent.loc[recent["High"] == highs, "High"].unique(), reverse=True)[:3]
    support_levels = sorted(recent.loc[recent["Low"] == lows, "Low"].unique())[:3]

    # Fallback: use simple percentile-based levels if not enough detected
    if len(resistance_levels) < 2:
        resistance_levels = [
            round(float(recent["High"].quantile(0.95)), 4),
            round(float(recent["High"].quantile(0.85)), 4),
        ]
    if len(support_levels) < 2:
        support_levels = [
            round(float(recent["Low"].quantile(0.05)), 4),
            round(float(recent["Low"].quantile(0.15)), 4),
        ]

    return {
        "resistance": [round(float(r), 4) for r in resistance_levels],
        "support": [round(float(s), 4) for s in support_levels],
    }


def analyze_asset(ticker, timeframe="1d"):
    """Full technical analysis snapshot."""
    data = fetch_data(ticker, timeframe)
    close = data["Close"]
    latest = float(close.iloc[-1])
    prev = float(close.iloc[-2]) if len(close) > 1 else latest

    # Indicators
    sma_20 = sma(data, 20)
    sma_50 = sma(data, 50)
    sma_200 = sma(data, 200)
    ema_12 = ema(data, 12)
    ema_26 = ema(data, 26)
    rsi_14 = rsi(data, 14)
    macd_line, signal_line, hist = macd(data)
    bb_upper, bb_middle, bb_lower = bollinger_bands(data)
    sr = support_resistance(data)

    def safe_last(series):
        val = series.iloc[-1] if not series.empty else None
        return round(float(val), 4) if val is not None and not (isinstance(val, float) and np.isnan(val)) else None

    # Signal assessment
    signals = []
    if safe_last(sma_20) and latest > safe_last(sma_20):
        signals.append("Price > SMA20 (bullish)")
    elif safe_last(sma_20):
        signals.append("Price < SMA20 (bearish)")

    rsi_val = safe_last(rsi_14)
    if rsi_val:
        if rsi_val > 70:
            signals.append(f"RSI {rsi_val} — overbought")
        elif rsi_val < 30:
            signals.append(f"RSI {rsi_val} — oversold")
        else:
            signals.append(f"RSI {rsi_val} — neutral")

    macd_val = safe_last(macd_line)
    sig_val = safe_last(signal_line)
    if macd_val and sig_val:
        if macd_val > sig_val:
            signals.append("MACD above signal (bullish)")
        else:
            signals.append("MACD below signal (bearish)")

    return {
        "ticker": ticker,
        "timeframe": timeframe,
        "timestamp": datetime.now().isoformat(),
        "price": {
            "current": round(latest, 4),
            "previous_close": round(prev, 4),
            "change": round(latest - prev, 4),
            "change_pct": round((latest - prev) / prev * 100, 2),
        },
        "indicators": {
            "sma_20": safe_last(sma_20),
            "sma_50": safe_last(sma_50),
            "sma_200": safe_last(sma_200),
            "ema_12": safe_last(ema_12),
            "ema_26": safe_last(ema_26),
            "rsi_14": rsi_val,
            "macd": {"line": macd_val, "signal": sig_val, "histogram": safe_last(hist)},
            "bollinger": {
                "upper": safe_last(bb_upper),
                "middle": safe_last(bb_middle),
                "lower": safe_last(bb_lower),
            },
        },
        "support_resistance": sr,
        "signals": signals,
    }


def main():
    parser = argparse.ArgumentParser(description="Technical Analysis")
    parser.add_argument("--ticker", required=True, help="Ticker symbol (e.g., GC=F, BTC-USD)")
    parser.add_argument("--timeframe", default="1d", choices=list(TIMEFRAME_PERIODS.keys()))
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    result = analyze_asset(args.ticker, args.timeframe)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        p = result["price"]
        print(f"=== {result['ticker']} Technical Analysis ({result['timeframe']}) ===")
        print(f"Price: {p['current']}  ({p['change']:+.4f} / {p['change_pct']:+.2f}%)")
        print()
        ind = result["indicators"]
        print(f"SMA 20: {ind['sma_20']}  |  SMA 50: {ind['sma_50']}  |  SMA 200: {ind['sma_200']}")
        print(f"EMA 12: {ind['ema_12']}  |  EMA 26: {ind['ema_26']}")
        print(f"RSI(14): {ind['rsi_14']}")
        m = ind["macd"]
        print(f"MACD: {m['line']}  Signal: {m['signal']}  Hist: {m['histogram']}")
        bb = ind["bollinger"]
        print(f"BB Upper: {bb['upper']}  Middle: {bb['middle']}  Lower: {bb['lower']}")
        print()
        sr = result["support_resistance"]
        print(f"Resistance: {sr['resistance']}")
        print(f"Support: {sr['support']}")
        print()
        print("Signals:")
        for s in result["signals"]:
            print(f"  • {s}")


if __name__ == "__main__":
    main()
