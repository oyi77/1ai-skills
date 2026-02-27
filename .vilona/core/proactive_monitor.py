#!/usr/bin/env python3
"""
Vilona Proactive Monitor
Autonomous monitoring for BerkahKarya crisis mode
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

VILONA_DIR = Path("/home/openclaw/.openclaw/workspace/.vilona")
METRICS_DIR = VILONA_DIR / "metrics"
KNOWLEDGE_DIR = VILONA_DIR / "knowledge"

class VilonaMonitor:
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.metrics_file = METRICS_DIR / f"{self.today}.json"
        self.metrics = self._load_metrics()
    
    def _load_metrics(self):
        """Load or create today's metrics"""
        if self.metrics_file.exists():
            with open(self.metrics_file) as f:
                return json.load(f)
        # Copy template
        template_file = METRICS_DIR / "template.json"
        with open(template_file) as f:
            data = json.load(f)
        data["date"] = self.today
        return data
    
    def save_metrics(self):
        """Save metrics to file"""
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    # ====== TASK TRACKING ======
    
    def log_task(self, task_name: str, status: str, response_time_sec: float = 0):
        """Log task completion"""
        self.metrics["daily_metrics"]["tasks"]["total"] += 1
        if status == "completed":
            self.metrics["daily_metrics"]["tasks"]["completed"] += 1
        elif status == "failed":
            self.metrics["daily_metrics"]["tasks"]["failed"] += 1
        
        # Update completion rate
        total = self.metrics["daily_metrics"]["tasks"]["total"]
        completed = self.metrics["daily_metrics"]["tasks"]["completed"]
        self.metrics["daily_metrics"]["tasks"]["completion_rate"] = round((completed/total)*100, 1) if total > 0 else 0
        
        self.save_metrics()
    
    def log_decision(self, decision: str, expected: str, actual: str, accurate: bool):
        """Log decision outcome"""
        self.metrics["daily_metrics"]["decisions"]["total"] += 1
        if accurate:
            self.metrics["daily_metrics"]["decisions"]["accurate"] += 1
        
        total = self.metrics["daily_metrics"]["decisions"]["total"]
        accurate_count = self.metrics["daily_metrics"]["decisions"]["accurate"]
        self.metrics["daily_metrics"]["decisions"]["accuracy_rate"] = round((accurate_count/total)*100, 1) if total > 0 else 0
        
        self.save_metrics()
    
    def log_proactive(self, action_type: str, value_idr: int = 0):
        """Log proactive action"""
        self.metrics["daily_metrics"]["proactive"]["actions_taken"] += 1
        self.metrics["daily_metrics"]["proactive"]["value_generated_idr"] += value_idr
        self.save_metrics()
    
    # ====== KNOWLEDGE DEEPENING ======
    
    def log_learning(self, topic: str, source: str, insight: str):
        """Log learning activity"""
        self.metrics["learning"]["articles_read"] += 1
        self.metrics["learning"]["skills_practiced"].append(topic)
        
        # Also log to knowledge file
        kb_file = KNOWLEDGE_DIR / topic / "insights.md"
        kb_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(kb_file, 'a') as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Source:** {source}\n")
            f.write(f"**Insight:** {insight}\n\n")
        
        self.save_metrics()
    
    # ====== PROACTIVE MONITORS ======
    
    def check_trading_positions(self):
        """Check if trading positions need attention"""
        # TODO: Integrate with Ostium connector
        return {"status": "placeholder", "positions": [], "alerts": []}
    
    def check_cashflow(self):
        """Check cashflow status"""
        # TODO: Integrate with financial tracking
        return {"status": "placeholder", "burn_rate": 0, "runway_days": 0}
    
    def check_opportunities(self):
        """Check for new opportunities"""
        # TODO: Monitor competitor activity, market trends
        return {"status": "placeholder", "opportunities": []}

# ====== MAIN MONITOR LOOP ======

def main():
    monitor = VilonaMonitor()
    
    if len(sys.argv) < 2:
        print("Usage: python proactive_monitor.py [task|decision|proactive|learning|status]")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        print(json.dumps(monitor.metrics, indent=2))
    elif cmd == "task":
        task_name = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        status = sys.argv[3] if len(sys.argv) > 3 else "completed"
        monitor.log_task(task_name, status)
        print(f"Logged task: {task_name} - {status}")
    elif cmd == "proactive":
        action_type = sys.argv[2] if len(sys.argv) > 2 else "general"
        monitor.log_proactive(action_type)
        print(f"Logged proactive action: {action_type}")
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
