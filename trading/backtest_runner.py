#!/usr/bin/env python3
"""
BerkahKarya Backtest Runner
============================
Run backtests for XAUUSD strategies using yfinance (GC=F) historical data.

Supported strategies:
  asia7c   — Asia 7-Candle Breakout (07:00-15:00 WIB)
  london   — London Session Breakout (15:00-17:00 WIB)
  ny       — NY Open Momentum (20:30-22:00 WIB)
  all      — Run all three and compare

Usage:
  python backtest_runner.py --strategy all --start 2025-01-01 --end 2025-12-31
  python backtest_runner.py --strategy asia7c --start 2025-01-01 --end 2025-12-31 --balance 5000
  python backtest_runner.py --strategy london --verbose
"""

import argparse
import sys
from datetime import datetime, time, timedelta
from typing import Dict, Any, List, Optional, Tuple

import pytz

try:
    import yfinance as yf
    import pandas as pd
    HAS_YFINANCE = True
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance pandas")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────
JAKARTA_TZ = pytz.timezone("Asia/Jakarta")
YF_TICKER  = "GC=F"   # Gold futures (XAUUSD proxy)

# Session windows (WIB)
ASIA_START   = time(7, 0)
ASIA_END     = time(15, 0)
LONDON_START = time(15, 0)
LONDON_END   = time(17, 0)
NY_START     = time(20, 30)
NY_END       = time(22, 0)


# ─────────────────────────────────────────────────────────────────────────────
# Data helpers
# ─────────────────────────────────────────────────────────────────────────────

def download_data(start: str, end: str, interval: str = "1h") -> pd.DataFrame:
    """Download XAUUSD (GC=F) data from yfinance."""
    print(f"[Data] Downloading {YF_TICKER} from {start} to {end} ({interval}) ...")
    ticker = yf.Ticker(YF_TICKER)
    df = ticker.history(start=start, end=end, interval=interval)

    if df.empty:
        print("ERROR: No data downloaded. Check date range and internet connection.")
        sys.exit(1)

    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df.index = df.index.tz_convert(JAKARTA_TZ)

    print(f"[Data] Downloaded {len(df)} bars spanning {df.index[0].date()} → {df.index[-1].date()}")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# Metrics helper
# ─────────────────────────────────────────────────────────────────────────────

def calc_metrics(trades: List[Dict], initial_balance: float, label: str) -> Dict[str, Any]:
    """Compute standard backtest metrics from a trade list."""
    if not trades:
        return {"label": label, "total_trades": 0, "initial_balance": initial_balance}

    pnls         = [t["pnl_usd"] for t in trades]
    wins         = [t for t in trades if t["win"]]
    losses       = [t for t in trades if not t["win"]]
    gross_profit = sum(p for p in pnls if p > 0)
    gross_loss   = abs(sum(p for p in pnls if p < 0))
    pf           = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    # Running balance for drawdown
    balance  = initial_balance
    peak     = initial_balance
    max_dd   = 0.0
    for t in trades:
        balance += t["pnl_usd"]
        peak     = max(peak, balance)
        max_dd   = max(max_dd, peak - balance)
    final_balance = balance

    return {
        "label":           label,
        "total_trades":    len(trades),
        "wins":            len(wins),
        "losses":          len(losses),
        "win_rate":        round(len(wins) / len(trades) * 100, 1),
        "net_pnl":         round(sum(pnls), 2),
        "gross_profit":    round(gross_profit, 2),
        "gross_loss":      round(-gross_loss, 2),
        "profit_factor":   round(pf, 2),
        "avg_win":         round(gross_profit / len(wins), 2) if wins else 0.0,
        "avg_loss":        round(-gross_loss / len(losses), 2) if losses else 0.0,
        "max_drawdown":    round(max_dd, 2),
        "max_drawdown_pct": round(max_dd / initial_balance * 100, 2),
        "initial_balance": initial_balance,
        "final_balance":   round(final_balance, 2),
        "return_pct":      round((final_balance - initial_balance) / initial_balance * 100, 2),
        "trades":          trades,
    }


def print_metrics(m: Dict[str, Any], verbose: bool = False):
    """Pretty-print backtest metrics."""
    print()
    print("=" * 64)
    print(f"  {m['label']}")
    print("=" * 64)

    if m["total_trades"] == 0:
        print("  No trades generated.")
        print("=" * 64)
        return

    print(f"  Total Trades    : {m['total_trades']}")
    print(f"  Win / Loss      : {m['wins']}W / {m['losses']}L  ({m['win_rate']}%)")
    print(f"  Profit Factor   : {m['profit_factor']:.2f}")
    print("-" * 64)
    print(f"  Initial Balance : ${m['initial_balance']:>10,.2f}")
    print(f"  Final Balance   : ${m['final_balance']:>10,.2f}")
    print(f"  Net PnL         : ${m['net_pnl']:>+10,.2f}  ({m['return_pct']:+.2f}%)")
    print(f"  Gross Profit    : ${m['gross_profit']:>10,.2f}")
    print(f"  Gross Loss      : ${m['gross_loss']:>10,.2f}")
    print(f"  Avg Win         : ${m['avg_win']:>10,.2f}")
    print(f"  Avg Loss        : ${m['avg_loss']:>10,.2f}")
    print(f"  Max Drawdown    : ${m['max_drawdown']:>10,.2f}  ({m['max_drawdown_pct']:.2f}%)")
    print("=" * 64)

    if verbose and m.get("trades"):
        print("\n  Trade List:")
        print(f"  {'Date':<12} {'Dir':<6} {'Entry':>8} {'PnL':>8}  {'W/L'}")
        print(f"  {'-'*12} {'-'*6} {'-'*8} {'-'*8}  {'-'*3}")
        for t in m["trades"]:
            wl = "WIN" if t["win"] else "LOSS"
            entry = t.get("entry", t.get("buy_stop", t.get("sell_stop", 0)))
            print(
                f"  {t['date']:<12} {t['direction']:<6} "
                f"{entry:>8.2f} {t['pnl_usd']:>+8.2f}  {wl}"
            )


# ─────────────────────────────────────────────────────────────────────────────
# Asia 7-Candle Breakout Backtest
# ─────────────────────────────────────────────────────────────────────────────

def backtest_asia7c(
    df: pd.DataFrame,
    initial_balance: float = 1000.0,
    rr_ratio: float = 2.0,
    risk_pct: float = 0.01,
) -> Dict[str, Any]:
    """
    Backtest XAUUSD Asia 7-Candle Breakout.

    Session : 07:00–15:00 WIB
    Window  : first 7 H1 candles of Asia session (07:00–13:59 WIB)
    Entry   : BUY_STOP at HH+buffer, SELL_STOP at LL-buffer
    SL/TP   : 1R SL, 2R TP (R = range of 7 candles)
    """
    trades   = []
    balance  = initial_balance
    dates    = sorted(set(df.index.date))

    for day in dates:
        day_data = df[df.index.date == day]

        # --- 7-candle Asia window: 07:00–13:59 WIB (7 H1 bars) ---
        window = day_data[
            (day_data.index.time >= ASIA_START) &
            (day_data.index.time < time(14, 0))
        ].head(7)

        if len(window) < 4:
            continue

        hh = float(window["High"].max())
        ll = float(window["Low"].min())
        r  = hh - ll

        if r <= 0:
            continue

        buffer    = min(0.5, r * 0.01)   # 0.5 pt or 1% of range
        buy_stop  = hh + buffer
        sell_stop = ll - buffer
        buy_tp    = buy_stop  + r * rr_ratio
        buy_sl    = buy_stop  - r
        sell_tp   = sell_stop - r * rr_ratio
        sell_sl   = sell_stop + r

        # --- Simulate trigger on London + NY bars (15:00–23:59 WIB) ---
        post_asia = day_data[day_data.index.time >= ASIA_END]

        if post_asia.empty:
            continue

        triggered   = None
        entry_price = None
        tp_price    = None
        sl_price    = None
        direction   = None

        for _, bar in post_asia.iterrows():
            bh = float(bar["High"])
            bl = float(bar["Low"])

            if triggered is None:
                if bh >= buy_stop:
                    triggered   = "BUY"
                    entry_price = buy_stop
                    tp_price    = buy_tp
                    sl_price    = buy_sl
                    direction   = 1
                elif bl <= sell_stop:
                    triggered   = "SELL"
                    entry_price = sell_stop
                    tp_price    = sell_tp
                    sl_price    = sell_sl
                    direction   = -1
                continue

            # Check TP/SL
            if direction == 1:
                if bh >= tp_price:
                    pnl_pts, win = tp_price - entry_price, True
                    break
                elif bl <= sl_price:
                    pnl_pts, win = sl_price - entry_price, False
                    break
            else:
                if bl <= tp_price:
                    pnl_pts, win = entry_price - tp_price, True
                    break
                elif bh >= sl_price:
                    pnl_pts, win = entry_price - sl_price, False
                    break
        else:
            if triggered and entry_price is not None:
                last_close = float(post_asia.iloc[-1]["Close"])
                pnl_pts    = direction * (last_close - entry_price)
                win        = pnl_pts > 0
            else:
                continue

        # Position sizing: risk_pct of balance, SL = r pts, gold = $100/pt per lot
        lot_size = (balance * risk_pct) / (r * 100 + 1e-9)
        lot_size = max(0.01, round(lot_size, 2))
        pnl_usd  = round(pnl_pts * 100 * lot_size, 2)
        balance  += pnl_usd

        trades.append({
            "date":      day.isoformat(),
            "direction": triggered,
            "entry":     round(entry_price, 2),
            "tp":        round(tp_price, 2),
            "sl":        round(sl_price, 2),
            "range":     round(r, 2),
            "lot":       lot_size,
            "pnl_usd":   pnl_usd,
            "win":       win,
        })

    return calc_metrics(trades, initial_balance, "Asia 7-Candle Breakout (07:00-15:00 WIB)")


# ─────────────────────────────────────────────────────────────────────────────
# London Breakout Backtest
# ─────────────────────────────────────────────────────────────────────────────

def backtest_london(
    df: pd.DataFrame,
    initial_balance: float = 1000.0,
    tp_mult: float = 1.5,
    sl_mult: float = 0.5,
    risk_pct: float = 0.01,
) -> Dict[str, Any]:
    """
    Backtest London Breakout.

    Session : 15:00–17:00 WIB
    Range   : Asia session (07:00–14:59 WIB) HH and LL
    Entry   : BUY_STOP above Asia high, SELL_STOP below Asia low
    """
    trades  = []
    balance = initial_balance
    dates   = sorted(set(df.index.date))

    for day in dates:
        day_data = df[df.index.date == day]

        asia = day_data[
            (day_data.index.time >= ASIA_START) &
            (day_data.index.time < LONDON_START)
        ]
        if asia.empty:
            continue

        asia_high = float(asia["High"].max())
        asia_low  = float(asia["Low"].min())
        range_pts = asia_high - asia_low
        if range_pts <= 0:
            continue

        buffer    = asia_high * 0.0002
        buy_stop  = round(asia_high + buffer, 2)
        sell_stop = round(asia_low  - buffer, 2)
        buy_tp    = round(buy_stop  + tp_mult * range_pts, 2)
        buy_sl    = round(buy_stop  - sl_mult * range_pts, 2)
        sell_tp   = round(sell_stop - tp_mult * range_pts, 2)
        sell_sl   = round(sell_stop + sl_mult * range_pts, 2)

        london = day_data[
            (day_data.index.time >= LONDON_START) &
            (day_data.index.time < LONDON_END)
        ]
        if london.empty:
            continue

        triggered   = None
        entry_price = None
        tp_price    = None
        sl_price    = None
        direction   = None

        for _, bar in london.iterrows():
            bh = float(bar["High"])
            bl = float(bar["Low"])

            if triggered is None:
                if bh >= buy_stop:
                    triggered   = "BUY"
                    entry_price = buy_stop
                    tp_price    = buy_tp
                    sl_price    = buy_sl
                    direction   = 1
                elif bl <= sell_stop:
                    triggered   = "SELL"
                    entry_price = sell_stop
                    tp_price    = sell_tp
                    sl_price    = sell_sl
                    direction   = -1
                continue

            if direction == 1:
                if bh >= tp_price:
                    pnl_pts, win = tp_price - entry_price, True
                    break
                elif bl <= sl_price:
                    pnl_pts, win = sl_price - entry_price, False
                    break
            else:
                if bl <= tp_price:
                    pnl_pts, win = entry_price - tp_price, True
                    break
                elif bh >= sl_price:
                    pnl_pts, win = entry_price - sl_price, False
                    break
        else:
            if triggered and entry_price is not None:
                last_close = float(london.iloc[-1]["Close"])
                pnl_pts    = direction * (last_close - entry_price)
                win        = pnl_pts > 0
            else:
                continue

        sl_distance = abs(entry_price - sl_price)
        lot_size = (balance * risk_pct) / (sl_distance * 100 + 1e-9)
        lot_size = max(0.01, round(lot_size, 2))
        pnl_usd  = round(pnl_pts * 100 * lot_size, 2)
        balance  += pnl_usd

        trades.append({
            "date":      day.isoformat(),
            "direction": triggered,
            "entry":     round(entry_price, 2),
            "tp":        round(tp_price, 2),
            "sl":        round(sl_price, 2),
            "range":     round(range_pts, 2),
            "lot":       lot_size,
            "pnl_usd":   pnl_usd,
            "win":       win,
        })

    return calc_metrics(trades, initial_balance, "London Session Breakout (15:00-17:00 WIB)")


# ─────────────────────────────────────────────────────────────────────────────
# NY Momentum Backtest
# ─────────────────────────────────────────────────────────────────────────────

def backtest_ny(
    df: pd.DataFrame,
    initial_balance: float = 1000.0,
    tp_mult: float = 2.0,
    risk_pct: float = 0.01,
) -> Dict[str, Any]:
    """
    Backtest NY Open Momentum.

    Session   : 20:00–22:00 WIB (using 20:00 H1 bar as proxy for 20:30 candle)
    Signal    : Hourly bar that opens at/after 20:00 WIB
    Entry     : Close of first bar
    SL        : Opposite end (low for long, high for short)
    TP        : Entry ± tp_mult × risk
    Exit      : TP/SL or session end (22:00 WIB)

    Note: yfinance H1 bars are bar-open indexed. The 20:00 bar covers
    20:00-21:00 WIB and is used as the NY momentum trigger candle.
    Simulation runs on subsequent bars up to 22:00 WIB.
    """
    # Use 20:00 as the NY signal bar start (closest hourly boundary to 20:30)
    NY_SIGNAL_START = time(20, 0)

    trades  = []
    balance = initial_balance
    dates   = sorted(set(df.index.date))

    for day in dates:
        day_data = df[df.index.date == day]

        # First bar at or after 20:00 WIB (the NY signal bar)
        ny_bars = day_data[day_data.index.time >= NY_SIGNAL_START]
        if ny_bars.empty:
            continue

        first = ny_bars.iloc[0]
        o = float(first["Open"])
        h = float(first["High"])
        l = float(first["Low"])
        c = float(first["Close"])

        if abs(c - o) < 0.10:
            continue   # near-doji — skip

        bullish = c > o
        entry   = c
        sl      = l if bullish else h
        risk    = abs(entry - sl)
        if risk <= 0:
            continue
        tp = entry + tp_mult * risk if bullish else entry - tp_mult * risk

        direction = 1 if bullish else -1

        # Simulate on bars AFTER the signal bar, up to 23:00 WIB (allow extra hour)
        post_signal = ny_bars.iloc[1:]   # skip first (signal) bar
        post_signal = post_signal[post_signal.index.time < time(23, 0)]

        pnl_pts = None
        win     = None

        for _, bar in post_signal.iterrows():
            bh = float(bar["High"])
            bl = float(bar["Low"])

            if direction == 1:
                if bh >= tp:
                    pnl_pts, win = tp - entry, True
                    break
                elif bl <= sl:
                    pnl_pts, win = sl - entry, False
                    break
            else:
                if bl <= tp:
                    pnl_pts, win = entry - tp, True
                    break
                elif bh >= sl:
                    pnl_pts, win = entry - sl, False
                    break

        if win is None:
            # Session ended without TP/SL — exit at last bar close
            if not post_signal.empty:
                last_close = float(post_signal.iloc[-1]["Close"])
                pnl_pts    = direction * (last_close - entry)
                win        = pnl_pts > 0
            else:
                # No follow-up bars — use next day's open proxy
                continue

        lot_size = (balance * risk_pct) / (risk * 100 + 1e-9)
        lot_size = max(0.01, round(lot_size, 2))
        pnl_usd  = round(pnl_pts * 100 * lot_size, 2)
        balance  += pnl_usd

        trades.append({
            "date":      day.isoformat(),
            "direction": "BUY" if bullish else "SELL",
            "entry":     round(entry, 2),
            "sl":        round(sl, 2),
            "tp":        round(tp, 2),
            "risk":      round(risk, 2),
            "lot":       lot_size,
            "pnl_usd":   pnl_usd,
            "win":       win,
        })

    return calc_metrics(trades, initial_balance, "NY Open Momentum (20:00-23:00 WIB)")


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Backtest Runner — XAUUSD (GC=F) via yfinance"
    )
    parser.add_argument(
        "--strategy", "-s",
        default="all",
        choices=["asia7c", "london", "ny", "all"],
        help="Strategy to backtest (default: all)"
    )
    parser.add_argument(
        "--start",
        default="2025-01-01",
        help="Backtest start date YYYY-MM-DD (default: 2025-01-01)"
    )
    parser.add_argument(
        "--end",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Backtest end date YYYY-MM-DD (default: today)"
    )
    parser.add_argument(
        "--balance", "-b",
        type=float,
        default=1000.0,
        help="Initial balance USD (default: 1000)"
    )
    parser.add_argument(
        "--risk",
        type=float,
        default=0.01,
        help="Risk per trade as fraction (default: 0.01 = 1%%)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show individual trade list"
    )
    args = parser.parse_args()

    print(f"\nBerkahKarya Backtest Runner")
    print(f"Symbol    : XAUUSD (GC=F via yfinance)")
    print(f"Period    : {args.start} → {args.end}")
    print(f"Balance   : ${args.balance:,.2f}")
    print(f"Risk/trade: {args.risk*100:.1f}%")
    print(f"Strategy  : {args.strategy}")

    # Download hourly data (1h = best for all three sessions)
    df = download_data(args.start, args.end, interval="1h")

    results = []

    if args.strategy in ("asia7c", "all"):
        m = backtest_asia7c(df, args.balance, risk_pct=args.risk)
        print_metrics(m, args.verbose)
        results.append(m)

    if args.strategy in ("london", "all"):
        m = backtest_london(df, args.balance, risk_pct=args.risk)
        print_metrics(m, args.verbose)
        results.append(m)

    if args.strategy in ("ny", "all"):
        m = backtest_ny(df, args.balance, risk_pct=args.risk)
        print_metrics(m, args.verbose)
        results.append(m)

    # Summary comparison if "all"
    if args.strategy == "all" and len(results) > 1:
        print()
        print("=" * 64)
        print("  COMPARISON SUMMARY")
        print("=" * 64)
        print(f"  {'Strategy':<38} {'WR%':>5} {'PF':>5} {'Net PnL':>10} {'Ret%':>7}")
        print(f"  {'-'*38} {'-'*5} {'-'*5} {'-'*10} {'-'*7}")
        for m in results:
            if m["total_trades"] == 0:
                print(f"  {m['label'][:38]:<38}  n/a   n/a        n/a    n/a")
            else:
                print(
                    f"  {m['label'][:38]:<38} "
                    f"{m['win_rate']:>5.1f} "
                    f"{m['profit_factor']:>5.2f} "
                    f"${m['net_pnl']:>9,.2f} "
                    f"{m['return_pct']:>+6.2f}%"
                )
        print("=" * 64)

    return results


if __name__ == "__main__":
    main()
