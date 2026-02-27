#!/usr/bin/env python3
"""
Vilona CLI - Command interface for self-improvement system
"""

import sys
import json
from pathlib import Path

VILONA_DIR = Path("/home/openclaw/.openclaw/workspace/.vilona")

def cmd_status():
    """Show current performance metrics"""
    from datetime import datetime
    metrics_file = VILONA_DIR / "metrics" / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    
    if metrics_file.exists():
        with open(metrics_file) as f:
            data = json.load(f)
        print("📊 Vilona Performance Today")
        print("=" * 50)
        print(f"Tasks: {data['daily_metrics']['tasks']['completed']}/{data['daily_metrics']['tasks']['total']} (Rate: {data['daily_metrics']['tasks']['completion_rate']}%)")
        print(f"Decisions: {data['daily_metrics']['decisions']['accuracy_rate']}% accuracy")
        print(f"Proactive: {data['daily_metrics']['proactive']['actions_taken']} actions")
        print(f"Learning: {data['learning']['articles_read']} articles")
    else:
        print("No metrics for today yet.")

def cmd_review():
    """Generate daily review template"""
    import subprocess
    subprocess.run(["bash", str(VILONA_DIR / "cron" / "daily-review.sh")])

def cmd_learn(topic: str, source: str, insight: str):
    """Log a learning insight"""
    import subprocess
    subprocess.run([
        sys.executable, 
        str(VILONA_DIR / "core" / "proactive_monitor.py"),
        "learning", topic, source, insight
    ])
    print(f"✅ Logged learning: {topic}")

def cmd_decision(context: str, decision: str, expected: str, confidence: str = "7"):
    """Log a decision for tracking"""
    import subprocess
    subprocess.run([
        sys.executable, 
        str(VILONA_DIR / "core" / "decision_tracker.py"),
        context, decision, expected, confidence
    ])
    print(f"✅ Logged decision: {decision}")

def cmd_help():
    print("""
Vilona Self-Improvement CLI

Commands:
  status              Show today's performance metrics
  review              Generate daily review template
  learn <topic> <source> <insight>   Log learning
  decision <context> <decision> <expected> [confidence]  Log decision
  help                Show this help

Examples:
  vilona status
  vilona learn "trading" "ostium-docs" "Use stop-loss at 2% max"
  vilona decision "cashflow" "cut marketing spend" "survive 3 more months" 8
""")

def main():
    if len(sys.argv) < 2:
        cmd_help()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        cmd_status()
    elif cmd == "review":
        cmd_review()
    elif cmd == "learn" and len(sys.argv) >= 5:
        cmd_learn(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "decision" and len(sys.argv) >= 5:
        cmd_decision(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "7")
    else:
        cmd_help()

if __name__ == "__main__":
    main()
