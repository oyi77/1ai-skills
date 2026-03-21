#!/usr/bin/env python3
"""
Portfolio Manager — track positions, P&L, exposure, rebalancing.

Usage:
    python portfolio.py track --asset XAUUSD --entry 2300 --size 0.1 --direction long
    python portfolio.py pnl
    python portfolio.py exposure
    python portfolio.py rebalance
    python portfolio.py show
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PORTFOLIO_FILE = Path(__file__).parent.parent / "portfolio.json"
OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"

TICKER_MAP = {
    "XAUUSD": "GC=F", "XAGUSD": "SI=F", "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X", "USDJPY": "USDJPY=X", "BTC": "BTC-USD",
    "ETH": "ETH-USD", "SPX": "^GSPC", "DXY": "DX-Y.NYB", "OIL": "CL=F",
}


def load_portfolio():
    if PORTFOLIO_FILE.exists():
        return json.loads(PORTFOLIO_FILE.read_text())
    return {"positions": [], "updated": None}


def save_portfolio(data):
    data["updated"] = datetime.now().isoformat()
    PORTFOLIO_FILE.write_text(json.dumps(data, indent=2))


def track_position(asset, entry, size, direction):
    """Add or update a position."""
    data = load_portfolio()
    pos = {
        "asset": asset.upper(),
        "entry": float(entry),
        "size": float(size),
        "direction": direction.lower(),
        "opened": datetime.now().isoformat(),
    }
    # Update existing or append
    for i, p in enumerate(data["positions"]):
        if p["asset"] == pos["asset"] and p["direction"] == pos["direction"]:
            data["positions"][i] = pos
            save_portfolio(data)
            print(f"Updated {pos['direction']} {pos['asset']} @ {pos['entry']} x{pos['size']}")
            return pos
    data["positions"].append(pos)
    save_portfolio(data)
    print(f"Tracked {pos['direction']} {pos['asset']} @ {pos['entry']} x{pos['size']}")
    return pos


def get_current_price(asset):
    """Fetch current price via yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        return None
    ticker = TICKER_MAP.get(asset.upper(), asset)
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception:
        pass
    return None


def get_pnl(positions=None):
    """Calculate unrealized P&L for all positions."""
    data = load_portfolio()
    positions = positions or data["positions"]
    results = []
    for pos in positions:
        price = get_current_price(pos["asset"])
        if price is None:
            results.append({**pos, "current": None, "pnl": None, "pnl_pct": None})
            continue
        if pos["direction"] == "long":
            pnl = (price - pos["entry"]) * pos["size"]
            pnl_pct = (price - pos["entry"]) / pos["entry"] * 100
        else:
            pnl = (pos["entry"] - price) * pos["size"]
            pnl_pct = (pos["entry"] - price) / pos["entry"] * 100
        results.append({
            **pos, "current": round(price, 4),
            "pnl": round(pnl, 2), "pnl_pct": round(pnl_pct, 2),
        })
    return results


def get_exposure():
    """Calculate total risk exposure across all positions."""
    data = load_portfolio()
    total_exposure = 0
    breakdown = []
    for pos in data["positions"]:
        price = get_current_price(pos["asset"]) or pos["entry"]
        notional = price * pos["size"]
        total_exposure += notional
        breakdown.append({
            "asset": pos["asset"], "direction": pos["direction"],
            "notional": round(notional, 2),
        })
    return {"total_exposure": round(total_exposure, 2), "positions": breakdown}


def rebalance_suggestion():
    """Get LLM-based rebalancing advice."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai not installed. Run: pip install openai")
        return None

    data = load_portfolio()
    pnl_data = get_pnl()
    exposure = get_exposure()

    client = OpenAI(base_url=OMNIROUTE_BASE, api_key=OMNIROUTE_KEY)
    prompt = f"""Analyze this trading portfolio and suggest rebalancing:

Positions with P&L:
{json.dumps(pnl_data, indent=2)}

Total Exposure: {json.dumps(exposure, indent=2)}

Provide:
1. Overall portfolio health assessment
2. Concentration risk warnings
3. Specific rebalancing suggestions (reduce/add/close)
4. Correlation risk between positions
Keep it concise and actionable."""

    try:
        resp = client.chat.completions.create(
            model=OMNIROUTE_MODEL,
            messages=[
                {"role": "system", "content": "You are a portfolio risk advisor. Be direct and specific."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[LLM Error: {e}]"


def show_positions():
    """Display all positions with P&L."""
    pnl_data = get_pnl()
    if not pnl_data:
        print("No positions tracked.")
        return
    print(f"{'Asset':<10} {'Dir':<6} {'Entry':>10} {'Current':>10} {'Size':>8} {'P&L':>10} {'%':>8}")
    print("-" * 64)
    for p in pnl_data:
        current = f"{p['current']:.2f}" if p["current"] else "N/A"
        pnl = f"{p['pnl']:.2f}" if p["pnl"] is not None else "N/A"
        pct = f"{p['pnl_pct']:.2f}%" if p["pnl_pct"] is not None else "N/A"
        print(f"{p['asset']:<10} {p['direction']:<6} {p['entry']:>10.2f} {current:>10} {p['size']:>8.3f} {pnl:>10} {pct:>8}")


def main():
    parser = argparse.ArgumentParser(description="Portfolio Manager")
    sub = parser.add_subparsers(dest="command")

    t = sub.add_parser("track", help="Track a position")
    t.add_argument("--asset", required=True)
    t.add_argument("--entry", required=True, type=float)
    t.add_argument("--size", required=True, type=float)
    t.add_argument("--direction", required=True, choices=["long", "short"])

    sub.add_parser("pnl", help="Show P&L")
    sub.add_parser("exposure", help="Show exposure")
    sub.add_parser("rebalance", help="Get rebalancing advice")
    sub.add_parser("show", help="Show all positions")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "track":
        track_position(args.asset, args.entry, args.size, args.direction)
    elif args.command == "pnl":
        show_positions()
    elif args.command == "exposure":
        exp = get_exposure()
        print(json.dumps(exp, indent=2))
    elif args.command == "rebalance":
        result = rebalance_suggestion()
        if result:
            print(result)
    elif args.command == "show":
        show_positions()


if __name__ == "__main__":
    main()
