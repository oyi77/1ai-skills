#!/usr/bin/env python3
"""
Decision Tracker - Logs all significant decisions with outcomes
Builds decision quality dataset for self-improvement
"""

import json
from datetime import datetime
from pathlib import Path

DECISION_LOG = Path("/home/openclaw/.openclaw/workspace/.vilona/knowledge/decisions.jsonl")

def log_decision(
    context: str,
    decision: str,
    rationale: str,
    expected_outcome: str,
    confidence: int,  # 1-10
    impact_level: str,  # low/medium/high/critical
    stakeholders: list,
    review_date: str = None,
):
    """Log a decision for later review"""
    
    DECISION_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "context": context,
        "decision": decision,
        "rationale": rationale,
        "expected_outcome": expected_outcome,
        "confidence": confidence,
        "impact_level": impact_level,
        "stakeholders": stakeholders,
        "review_date": review_date or (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "actual_outcome": None,
        "outcome_accuracy": None,
        "lessons": None,
        "status": "pending_review"
    }
    
    with open(DECISION_LOG, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    return entry

def review_decision(decision_timestamp: str, actual_outcome: str, lessons: str):
    """Update a logged decision with actual outcome"""
    
    lines = []
    with open(DECISION_LOG, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        entry = json.loads(line)
        if entry["timestamp"].startswith(decision_timestamp):
            entry["actual_outcome"] = actual_outcome
            entry["outcome_accuracy"] = _calculate_accuracy(
                entry["expected_outcome"], actual_outcome
            )
            entry["lessons"] = lessons
            entry["status"] = "reviewed"
            entry["reviewed_at"] = datetime.now().isoformat()
            lines[i] = json.dumps(entry, ensure_ascii=False) + "\n"
            break
    
    with open(DECISION_LOG, 'w') as f:
        f.writelines(lines)

def _calculate_accuracy(expected, actual):
    """Simple accuracy scoring - can be made more sophisticated"""
    # This is a placeholder - real implementation would be domain-specific
    if expected.lower() in actual.lower() or actual.lower() in expected.lower():
        return 80
    return 30

def get_decision_stats(days: int = 30):
    """Get decision accuracy statistics"""
    
    cutoff = datetime.now() - timedelta(days=days)
    total = 0
    reviewed = 0
    accurate = 0
    
    with open(DECISION_LOG, 'r') as f:
        for line in f:
            entry = json.loads(line)
            entry_time = datetime.fromisoformat(entry["timestamp"])
            if entry_time >= cutoff:
                total += 1
                if entry["status"] == "reviewed":
                    reviewed += 1
                    if entry.get("outcome_accuracy", 0) >= 70:
                        accurate += 1
    
    return {
        "total_decisions": total,
        "reviewed": reviewed,
        "review_rate": round((reviewed/total)*100, 1) if total > 0 else 0,
        "accuracy_rate": round((accurate/reviewed)*100, 1) if reviewed > 0 else 0
    }

if __name__ == "__main__":
    import sys
    from datetime import timedelta
    
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        print(json.dumps(get_decision_stats(), indent=2))
    else:
        print("Usage: python decision_tracker.py [stats]")
