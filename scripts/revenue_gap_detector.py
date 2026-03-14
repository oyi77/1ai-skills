#!/usr/bin/env python3
"""
Revenue Gap Detector
Monitors time since last revenue-generating activity across multiple sources.

Exit Codes:
- 0 = OK (gap < 4 hours)
- 2 = WARNING (gap 4-8 hours)
- 3 = CRITICAL (gap 8-12 hours)
- 4 = EMERGENCY (gap 12+ hours)
- 1 = ERROR (script error)
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Configuration
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
LOG_FILE = WORKSPACE / "logs" / "revenue_gaps.log"
CONFIG_FILE = WORKSPACE / "config" / "revenue_gap_config.json"

# Default thresholds (can be overridden by config)
DEFAULT_THRESHOLDS = {
    "warning_hours": 4,
    "critical_hours": 8,
    "emergency_hours": 12
}

# Data sources to check (in priority order)
DATA_SOURCES = [
    {
        "name": "postbridge_api",
        "type": "api",
        "url": "http://localhost:8080/api/posts/latest",
        "enabled": True
    },
    {
        "name": "trading_logs",
        "type": "file",
        "path": WORKSPACE / ".vilona" / "knowledge" / "trading" / "trading_log.json",
        "enabled": True
    },
    {
        "name": "cashflow_files",
        "type": "glob",
        "pattern": str(WORKSPACE / "cashflow" / "*.md"),
        "enabled": True
    }
]

def load_config():
    """Load configuration from file or use defaults."""
    config = {"thresholds": DEFAULT_THRESHOLDS, "sources": DATA_SOURCES}

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                config.update(user_config)
        except (json.JSONDecodeError, IOError):
            pass  # Use defaults on error

    return config

def check_postbridge_api():
    """Check latest post from PostBridge API."""
    try:
        response = requests.get(
            "http://localhost:8080/api/posts/latest",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get("timestamp") or data.get("created_at")
            if timestamp:
                return parse_timestamp(timestamp), "PostBridge API"
    except (requests.RequestException, requests.Timeout):
        pass  # API not available
    return None, None

def check_trading_logs(log_path):
    """Check last trade execution from trading log."""
    if not log_path.exists():
        return None, None

    try:
        with open(log_path, 'r') as f:
            data = json.load(f)

        # Look for latest trade or execution
        trades = data.get("trades", [])
        executions = data.get("executions", [])

        latest_timestamp = None
        source = "Trading Logs"

        if trades:
            latest = max(trades, key=lambda x: x.get("timestamp", ""))
            latest_timestamp = latest.get("timestamp")

        if executions:
            latest_exec = max(executions, key=lambda x: x.get("timestamp", ""))
            exec_timestamp = latest_exec.get("timestamp")
            if not latest_timestamp or exec_timestamp > latest_timestamp:
                latest_timestamp = exec_timestamp
                source = "Trading Executions"

        if latest_timestamp:
            return parse_timestamp(latest_timestamp), source

    except (json.JSONDecodeError, IOError, KeyError):
        pass

    return None, None

def check_cashflow_files(pattern):
    """Check latest cashflow entry."""
    from glob import glob

    files = glob(pattern)
    if not files:
        return None, None

    latest_mtime = None
    latest_file = None

    for filepath in files:
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if latest_mtime is None or mtime > latest_mtime:
                latest_mtime = mtime
                latest_file = filepath
        except OSError:
            continue

    if latest_mtime:
        # Extract date from filename or content
        try:
            with open(latest_file, 'r') as f:
                content = f.read()
                # Try to parse "Date: YYYY-MM-DD" format
                import re
                date_match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', content)
                if date_match:
                    file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                    if file_date > latest_mtime:
                        return file_date, f"Cashflow ({Path(latest_file).name})"
        except IOError:
            pass
        return latest_mtime, f"Cashflow ({Path(latest_file).name})"

    return None, None

def parse_timestamp(timestamp_str):
    """Parse various timestamp formats."""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 with microseconds
        "%Y-%m-%dT%H:%M:%SZ",     # ISO 8601
        "%Y-%m-%d %H:%M:%S",      # Common format
        "%Y-%m-%d",               # Date only
    ]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue

    return None

def get_last_activity(config):
    """Get most recent activity timestamp from all enabled sources."""
    latest_timestamp = None
    latest_source = None

    for source in config["sources"]:
        if not source.get("enabled", False):
            continue

        if source["name"] == "postbridge_api":
            timestamp, name = check_postbridge_api()
        elif source["name"] == "trading_logs":
            path = Path(source["path"])
            timestamp, name = check_trading_logs(path)
        elif source["name"] == "cashflow_files":
            timestamp, name = check_cashflow_files(source["pattern"])
        else:
            continue

        if timestamp and (latest_timestamp is None or timestamp > latest_timestamp):
            latest_timestamp = timestamp
            latest_source = name

    return latest_timestamp, latest_source

def determine_status(gap_hours, thresholds):
    """Determine status and exit code based on gap in hours."""
    if gap_hours < thresholds["warning_hours"]:
        return "OK", 0, "Activity within acceptable range.继续保持。"
    elif gap_hours < thresholds["critical_hours"]:
        return "WARNING", 2, f"⚠️ Gap > {thresholds['warning_hours']}h. Needs attention now.立即检查营销上传和交易执行。"
    elif gap_hours < thresholds["emergency_hours"]:
        return "CRITICAL", 3, f"🚨 Gap > {thresholds['critical_hours']}h. CRITICAL. 执行紧急协议：检查所有收入来源，立即上传新内容，执行交易。"
    else:
        return "EMERGENCY", 4, f"🆘 Gap > {thresholds['emergency_hours']}h. EMERGENCY MODE. 执行周末突破协议所有协议A+B+C。立即检查银行余额。"

def log_result(timestamp, gap_hours, status, recommendation, source):
    """Log result to JSON log file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "gap_hours": round(gap_hours, 2),
        "last_activity": timestamp.isoformat() if timestamp else None,
        "source": source,
        "status": status,
        "recommendation": recommendation
    }

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Append to log file
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

    return log_entry

def save_to_daily_memory(log_entry):
    """Save critical alerts to daily memory file."""
    if log_entry["status"] in ["WARNING", "CRITICAL", "EMERGENCY"]:
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = WORKSPACE / "memory" / f"{today}.md"
        memory_file.parent.mkdir(parents=True, exist_ok=True)

        alert_timestamp = datetime.now().strftime("%H:%M")
        with open(memory_file, 'a') as f:
            f.write(f"\n## 🚨 Revenue Gap Alert [{alert_timestamp}]\n\n")
            f.write(f"**Status:** {log_entry['status']}\n")
            f.write(f"**Gap:** {log_entry['gap_hours']}h\n")
            f.write(f"**Source:** {log_entry['source']}\n")
            f.write(f"**Recommendation:** {log_entry['recommendation']}\n\n")

def main():
    """Main execution function."""
    now = datetime.now()

    # Load configuration
    config = load_config()
    thresholds = config["thresholds"]

    # Check all data sources
    last_activity, source = get_last_activity(config)

    # Calculate gap
    if last_activity:
        gap = now - last_activity
        gap_hours = gap.total_seconds() / 3600
    else:
        # No activity detected - use conservative fallback
        gap_hours = thresholds["emergency_hours"] + 1
        source = "No Activity Detected"

    # Determine status
    status, exit_code, recommendation = determine_status(gap_hours, thresholds)

    # Log result
    log_entry = log_result(
        last_activity,
        gap_hours,
        status,
        recommendation,
        source
    )

    # Save to daily memory for critical alerts
    save_to_daily_memory(log_entry)

    # Print output for human review
    print(f"Revenue Gap Detection Result:")
    print(f"  Status: {status}")
    print(f"  Gap: {gap_hours:.2f}h")
    print(f"  Last Activity: {last_activity.isoformat() if last_activity else 'N/A'}")
    print(f"  Source: {source}")
    print(f"  Recommendation: {recommendation}")
    print(f"  Exit Code: {exit_code}")

    # Return exit code
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)