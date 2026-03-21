#!/usr/bin/env python3
"""
Cashflow Analyzer — revenue summary, burn rate, runway, forecast.

Usage:
    python cashflow_analyzer.py summary --days 7
    python cashflow_analyzer.py burn-rate
    python cashflow_analyzer.py runway --balance 5000
    python cashflow_analyzer.py forecast --days 30
    python cashflow_analyzer.py report --balance 5000
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# Look for cashflow log in standard locations
LOG_CANDIDATES = [
    Path(__file__).parent.parent.parent.parent.parent / "logs" / "cashflow.log",
    Path.home() / ".openclaw" / "workspace" / "logs" / "cashflow.log",
]


def find_log():
    for p in LOG_CANDIDATES:
        if p.exists():
            return p
    return LOG_CANDIDATES[0]  # default path


def load_entries(log_path=None):
    """Load cashflow log entries."""
    log_path = log_path or find_log()
    if not log_path.exists():
        return []
    entries = []
    for line in log_path.read_text().strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            if "date" in entry:
                entry["_date"] = datetime.strptime(entry["date"], "%Y-%m-%d")
            entries.append(entry)
        except (json.JSONDecodeError, ValueError):
            continue
    return entries


def revenue_summary(days=7):
    """Total revenue and source breakdown for the last N days."""
    entries = load_entries()
    cutoff = datetime.now() - timedelta(days=days)

    total_revenue = 0
    total_expenses = 0
    sources = defaultdict(float)

    for e in entries:
        if "_date" not in e or e["_date"] < cutoff:
            continue
        amount = float(e.get("amount", 0))
        source = e.get("source", "unknown")
        if amount > 0:
            total_revenue += amount
            sources[source] += amount
        else:
            total_expenses += abs(amount)

    return {
        "period_days": days,
        "total_revenue": round(total_revenue, 2),
        "total_expenses": round(total_expenses, 2),
        "net": round(total_revenue - total_expenses, 2),
        "sources": {k: round(v, 2) for k, v in sorted(sources.items(), key=lambda x: -x[1])},
        "daily_avg_revenue": round(total_revenue / max(days, 1), 2),
    }


def burn_rate():
    """Calculate daily and monthly expense rate."""
    entries = load_entries()
    if not entries:
        return {"daily": 0, "monthly": 0, "note": "No data"}

    expenses = [e for e in entries if float(e.get("amount", 0)) < 0]
    if not expenses:
        return {"daily": 0, "monthly": 0, "note": "No expenses recorded"}

    dates = [e["_date"] for e in expenses if "_date" in e]
    if not dates:
        return {"daily": 0, "monthly": 0, "note": "No dated expenses"}

    span_days = max((max(dates) - min(dates)).days, 1)
    total_expenses = sum(abs(float(e.get("amount", 0))) for e in expenses)

    daily = total_expenses / span_days
    return {
        "total_expenses": round(total_expenses, 2),
        "span_days": span_days,
        "daily": round(daily, 2),
        "monthly": round(daily * 30, 2),
    }


def runway(balance):
    """How many months at current burn rate."""
    br = burn_rate()
    monthly = br.get("monthly", 0)
    if monthly <= 0:
        return {"balance": balance, "burn_monthly": 0, "runway_months": "infinite", "note": "No expenses"}
    months = balance / monthly
    return {
        "balance": balance,
        "burn_monthly": monthly,
        "runway_months": round(months, 1),
        "runway_date": (datetime.now() + timedelta(days=months * 30)).strftime("%Y-%m-%d"),
    }


def forecast(days=30):
    """Revenue projection based on recent trend."""
    entries = load_entries()
    revenue_entries = [e for e in entries if float(e.get("amount", 0)) > 0 and "_date" in e]

    if len(revenue_entries) < 2:
        return {"forecast_days": days, "projected": 0, "note": "Insufficient data"}

    # Group by date
    daily_rev = defaultdict(float)
    for e in revenue_entries:
        daily_rev[e["_date"].strftime("%Y-%m-%d")] += float(e["amount"])

    if not daily_rev:
        return {"forecast_days": days, "projected": 0, "note": "No daily data"}

    sorted_days = sorted(daily_rev.items())
    values = [v for _, v in sorted_days]

    # Simple trend: average of last 7 days (or all if fewer)
    recent = values[-7:] if len(values) >= 7 else values
    daily_avg = sum(recent) / len(recent)

    # Weighted: recent days weighted higher
    if len(values) >= 14:
        old_avg = sum(values[-14:-7]) / 7
        trend = daily_avg - old_avg
    else:
        trend = 0

    projected = daily_avg * days + (trend * days * 0.5)

    return {
        "forecast_days": days,
        "daily_avg_recent": round(daily_avg, 2),
        "daily_trend": round(trend, 2),
        "projected_revenue": round(max(projected, 0), 2),
        "data_points": len(sorted_days),
    }


def full_report(balance):
    """Full financial report."""
    return {
        "revenue_7d": revenue_summary(7),
        "revenue_30d": revenue_summary(30),
        "burn_rate": burn_rate(),
        "runway": runway(balance),
        "forecast_30d": forecast(30),
        "generated": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Cashflow Analyzer")
    sub = parser.add_subparsers(dest="command")

    s = sub.add_parser("summary", help="Revenue summary")
    s.add_argument("--days", type=int, default=7)

    sub.add_parser("burn-rate", help="Burn rate")

    r = sub.add_parser("runway", help="Runway calculation")
    r.add_argument("--balance", required=True, type=float)

    f = sub.add_parser("forecast", help="Revenue forecast")
    f.add_argument("--days", type=int, default=30)

    rp = sub.add_parser("report", help="Full report")
    rp.add_argument("--balance", required=True, type=float)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "summary":
        result = revenue_summary(args.days)
    elif args.command == "burn-rate":
        result = burn_rate()
    elif args.command == "runway":
        result = runway(args.balance)
    elif args.command == "forecast":
        result = forecast(args.days)
    elif args.command == "report":
        result = full_report(args.balance)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
