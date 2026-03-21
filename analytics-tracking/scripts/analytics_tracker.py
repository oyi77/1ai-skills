#!/usr/bin/env python3
"""
Analytics Tracker - Aggregates daily metrics from multiple sources.

Sources:
  1. PostBridge API analytics
  2. LYNK monitoring log (clicks/views)
  3. Revenue gaps log (cashflow data)

Usage:
  python analytics_tracker.py [--date 2026-03-21]
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, date
from pathlib import Path

# --- Paths ---
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
LYNK_LOG = WORKSPACE / "logs" / "lynk_monitoring_log.txt"
REVENUE_LOG = WORKSPACE / "logs" / "revenue_gaps.log"
OUTPUT_FILE = WORKSPACE / "logs" / "analytics_daily.json"

# --- PostBridge config ---
POSTBRIDGE_API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
POSTBRIDGE_ENDPOINT = "https://api.postbridge.io/v1/analytics"


def fetch_postbridge_stats(target_date: str) -> dict:
    """Fetch analytics from PostBridge API. Returns empty dict on failure."""
    try:
        url = f"{POSTBRIDGE_ENDPOINT}?date={target_date}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {POSTBRIDGE_API_KEY}",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError, Exception) as exc:
        print(f"[analytics] PostBridge API unavailable: {exc}", file=sys.stderr)
        return {}


def parse_lynk_clicks(target_date: str) -> int:
    """Parse LYNK monitoring log for clicks/visits on the target date.

    The log is a JSON array of checkpoint objects. Each has:
      - timestamp (ISO format)
      - checkpoint.last_clicks (int or null)
      - checkpoint.last_views (int or null)
    We sum all non-null last_clicks values for entries matching target_date.
    """
    if not LYNK_LOG.exists():
        print(f"[analytics] LYNK log not found: {LYNK_LOG}", file=sys.stderr)
        return 0

    total_clicks = 0
    try:
        raw = LYNK_LOG.read_text(encoding="utf-8", errors="replace")
        data = json.loads(raw)
        if not isinstance(data, list):
            data = [data]

        for entry in data:
            ts = entry.get("timestamp", "")
            if not ts.startswith(target_date):
                continue

            cp = entry.get("checkpoint", {})
            if isinstance(cp, dict):
                clicks = cp.get("last_clicks")
                views = cp.get("last_views")
                if isinstance(clicks, (int, float)) and clicks > 0:
                    total_clicks += int(clicks)
                # Fall back to views as a proxy for clicks if clicks is null
                elif isinstance(views, (int, float)) and views > 0:
                    total_clicks += int(views)

    except json.JSONDecodeError:
        # Try line-by-line parsing for non-standard JSON
        try:
            for line in raw.splitlines():
                line = line.strip()
                if not line or line.startswith("-"):
                    continue
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")
                    if not ts.startswith(target_date):
                        continue
                    for key in ("last_clicks", "clicks", "last_views", "views"):
                        val = entry.get(key) or (entry.get("checkpoint", {}) or {}).get(key)
                        if isinstance(val, (int, float)) and val > 0:
                            total_clicks += int(val)
                            break
                except json.JSONDecodeError:
                    continue
        except Exception:
            pass
    except Exception as exc:
        print(f"[analytics] Error parsing LYNK log: {exc}", file=sys.stderr)

    return total_clicks


def parse_revenue_gaps(target_date: str) -> float:
    """Parse revenue_gaps.log for revenue-related data on the target date.

    The log contains JSON objects separated by '---' lines. Each entry has:
      - timestamp, gap_hours, level/gap_level, source, last_activity
    We look for entries on the target date and try to extract any revenue figures.
    """
    if not REVENUE_LOG.exists():
        print(f"[analytics] Revenue log not found: {REVENUE_LOG}", file=sys.stderr)
        return 0.0

    revenue = 0.0
    entries_on_date = 0
    emergency_count = 0

    try:
        raw = REVENUE_LOG.read_text(encoding="utf-8", errors="replace")

        # Split by separator lines
        blocks = re.split(r'-{10,}', raw)

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            # Handle lines that might have plain text before JSON
            json_match = re.search(r'\{.*\}', block, re.DOTALL)
            if not json_match:
                continue

            try:
                entry = json.loads(json_match.group())
            except json.JSONDecodeError:
                continue

            ts = entry.get("timestamp", "")
            if not ts.startswith(target_date):
                continue

            entries_on_date += 1

            # Extract revenue if present
            for key in ("revenue", "last_revenue", "revenue_amount", "amount"):
                val = entry.get(key)
                if isinstance(val, (int, float)) and val > 0:
                    revenue += float(val)

            # Track gap levels
            level = entry.get("level") or entry.get("gap_level", "")
            if level == "EMERGENCY":
                emergency_count += 1

    except Exception as exc:
        print(f"[analytics] Error parsing revenue log: {exc}", file=sys.stderr)

    return revenue


def estimate_posts_and_reach(postbridge_stats: dict) -> tuple:
    """Extract posts_published and total_reach from PostBridge stats if available."""
    posts = postbridge_stats.get("posts_published", 0)
    reach = postbridge_stats.get("total_reach", 0)
    top_content = postbridge_stats.get("top_performing_content", [])

    if not isinstance(posts, int):
        posts = 0
    if not isinstance(reach, int):
        reach = 0
    if not isinstance(top_content, list):
        top_content = []

    return posts, reach, top_content


def run(target_date: str):
    """Main tracking routine."""
    print(f"[analytics] Tracking metrics for {target_date}")

    # 1. PostBridge
    print("[analytics] Fetching PostBridge stats...")
    pb_stats = fetch_postbridge_stats(target_date)

    # 2. LYNK clicks
    print("[analytics] Parsing LYNK clicks...")
    lynk_clicks = parse_lynk_clicks(target_date)

    # 3. Revenue
    print("[analytics] Parsing revenue gaps...")
    revenue = parse_revenue_gaps(target_date)

    # 4. Derive posts/reach from PostBridge if available
    posts, reach, top_content = estimate_posts_and_reach(pb_stats)

    # Build output
    metrics = {
        "date": target_date,
        "posts_published": posts,
        "total_reach": reach,
        "revenue_estimate": round(revenue, 2),
        "top_performing_content": top_content,
        "lynk_clicks": lynk_clicks,
        "postbridge_stats": pb_stats,
    }

    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[analytics] Saved daily metrics to {OUTPUT_FILE}")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Track and aggregate daily analytics metrics.")
    parser.add_argument(
        "--date",
        type=str,
        default=date.today().isoformat(),
        help="Target date in YYYY-MM-DD format (default: today)",
    )
    args = parser.parse_args()

    # Validate date format
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print(f"[analytics] Invalid date format: {args.date}. Use YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    run(args.date)


if __name__ == "__main__":
    main()
