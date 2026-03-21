#!/usr/bin/env python3
"""
Proactive Agent Lite — Lightweight proactive health check.

Checks memory files for open loops, scans logs for errors,
checks disk space, and suggests proactive actions.

Usage:
    python proactive_check.py --output json
    python proactive_check.py --output text
    python proactive_check.py --date 2026-03-21
"""

import argparse
import glob
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta

WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE",
                           os.path.expanduser("~/.openclaw/workspace"))
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
LOGS_DIR = os.path.join(WORKSPACE, "logs")


def check_memory_open_loops(date_str=None):
    """Scan memory files for open loops, TODOs, and unresolved items."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    open_loops = []

    # Check today's and yesterday's memory files
    dates_to_check = [date_str]
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        yesterday = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
        dates_to_check.append(yesterday)
    except ValueError:
        pass

    for d in dates_to_check:
        mem_file = os.path.join(MEMORY_DIR, f"{d}.md")
        if not os.path.exists(mem_file):
            continue

        with open(mem_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Find open loop patterns
        patterns = [
            (r"(?:TODO|FIXME|HACK|XXX)[:\s]+(.+)", "todo"),
            (r"(?:- \[ \])\s+(.+)", "unchecked_task"),
            (r"(?:need to|should|must|waiting for|pending)[:\s]+(.+)", "action_needed"),
            (r"(?:blocked|stuck|error|failed)[:\s]+(.+)", "blocker"),
        ]

        for pattern, loop_type in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                open_loops.append({
                    "type": loop_type,
                    "text": match.group(1).strip()[:200],
                    "source": f"memory/{d}.md"
                })

    return open_loops


def check_logs_for_errors(max_lines=500):
    """Scan recent log files for errors and warnings."""
    errors = []

    if not os.path.isdir(LOGS_DIR):
        return errors

    log_files = glob.glob(os.path.join(LOGS_DIR, "*.log"))

    for log_file in log_files:
        try:
            size = os.path.getsize(log_file)
            if size == 0:
                continue

            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                # Read tail of file
                if size > 50000:
                    f.seek(size - 50000)
                    f.readline()  # skip partial line
                lines = f.readlines()[-max_lines:]

            log_name = os.path.basename(log_file)
            error_count = 0
            last_error = None

            for line in lines:
                line_lower = line.lower()
                if any(kw in line_lower for kw in ["error", "exception", "critical", "fatal"]):
                    error_count += 1
                    last_error = line.strip()[:200]

            if error_count > 0:
                errors.append({
                    "log": log_name,
                    "error_count": error_count,
                    "last_error": last_error
                })

        except (OSError, IOError):
            continue

    return sorted(errors, key=lambda e: e["error_count"], reverse=True)


def check_disk_space():
    """Check disk space usage."""
    usage = shutil.disk_usage("/")
    total_gb = usage.total / (1024 ** 3)
    used_gb = usage.used / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)
    pct_used = (usage.used / usage.total) * 100

    workspace_size = 0
    for dirpath, dirnames, filenames in os.walk(WORKSPACE):
        for f in filenames:
            try:
                workspace_size += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass

    return {
        "total_gb": round(total_gb, 1),
        "used_gb": round(used_gb, 1),
        "free_gb": round(free_gb, 1),
        "pct_used": round(pct_used, 1),
        "workspace_mb": round(workspace_size / (1024 ** 2), 1),
        "warning": pct_used > 85
    }


def generate_suggestions(open_loops, log_errors, disk_info):
    """Generate up to 3 proactive suggestions based on findings."""
    suggestions = []

    # Suggestion from open loops
    if open_loops:
        blockers = [l for l in open_loops if l["type"] == "blocker"]
        todos = [l for l in open_loops if l["type"] in ("todo", "unchecked_task")]

        if blockers:
            suggestions.append({
                "priority": "high",
                "action": f"Resolve blocker: {blockers[0]['text']}",
                "reason": f"Found {len(blockers)} blocker(s) in memory files"
            })
        elif todos:
            suggestions.append({
                "priority": "medium",
                "action": f"Complete pending task: {todos[0]['text']}",
                "reason": f"Found {len(todos)} unclosed TODO(s) in memory"
            })

    # Suggestion from log errors
    if log_errors:
        worst = log_errors[0]
        suggestions.append({
            "priority": "high" if worst["error_count"] > 10 else "medium",
            "action": f"Investigate errors in {worst['log']} ({worst['error_count']} errors)",
            "reason": f"Last error: {worst['last_error']}"
        })

    # Suggestion from disk space
    if disk_info["warning"]:
        suggestions.append({
            "priority": "high",
            "action": "Free disk space — usage above 85%",
            "reason": f"Disk {disk_info['pct_used']}% used, {disk_info['free_gb']}GB free"
        })

    # Fill remaining slots with general suggestions
    general = [
        {"priority": "low", "action": "Review and compact old log files",
         "reason": "Routine maintenance keeps workspace clean"},
        {"priority": "low", "action": "Check for stale memory entries to archive",
         "reason": "Memory hygiene improves agent context quality"},
        {"priority": "low", "action": "Verify all scheduled tasks ran successfully",
         "reason": "Proactive monitoring prevents silent failures"},
    ]

    while len(suggestions) < 3 and general:
        suggestions.append(general.pop(0))

    return suggestions[:3]


def run_check(date_str=None):
    """Run all proactive checks and return results."""
    open_loops = check_memory_open_loops(date_str)
    log_errors = check_logs_for_errors()
    disk_info = check_disk_space()
    suggestions = generate_suggestions(open_loops, log_errors, disk_info)

    return {
        "timestamp": datetime.now().isoformat(),
        "open_loops": open_loops[:10],
        "log_errors": log_errors[:5],
        "disk": disk_info,
        "suggestions": suggestions,
        "summary": {
            "open_loop_count": len(open_loops),
            "error_log_count": len(log_errors),
            "disk_warning": disk_info["warning"],
            "suggestion_count": len(suggestions)
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Proactive agent health check")
    parser.add_argument("--output", choices=["json", "text"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--date", help="Date to check (YYYY-MM-DD, default: today)")
    args = parser.parse_args()

    result = run_check(args.date)

    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Proactive Check — {result['timestamp']}")
        print("=" * 50)

        print(f"\nOpen Loops: {result['summary']['open_loop_count']}")
        for loop in result["open_loops"][:5]:
            print(f"  [{loop['type']}] {loop['text']}")

        print(f"\nLog Errors: {result['summary']['error_log_count']} logs with errors")
        for err in result["log_errors"][:3]:
            print(f"  {err['log']}: {err['error_count']} errors")

        disk = result["disk"]
        warn = " ⚠️ WARNING" if disk["warning"] else ""
        print(f"\nDisk: {disk['pct_used']}% used ({disk['free_gb']}GB free){warn}")
        print(f"Workspace: {disk['workspace_mb']}MB")

        print(f"\nSuggestions:")
        for i, s in enumerate(result["suggestions"], 1):
            print(f"  {i}. [{s['priority']}] {s['action']}")
            print(f"     Reason: {s['reason']}")


if __name__ == "__main__":
    main()
