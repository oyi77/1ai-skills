---
name: agent-self-improvement
description: Monitor performance of other skills, identify bottlenecks, suggest improvements,
  and auto-optimize the skill portfolio
domain: core
---

## Overview

A meta-skill that monitors the performance of all other skills in the portfolio, identifies bottlenecks and failure patterns, suggests improvements, and optionally applies optimizations. This is the flywheel that makes every other skill better over time. Track usage metrics, error rates, execution times, and user satisfaction to continuously improve the skill library.

## Required Tools

- **Metrics Storage**: SQLite (`.omc/metrics.db`) or JSON logs (`.omc/logs/skill-metrics.jsonl`)
- **Analysis**: Python with pandas for data analysis
- **Git**: For tracking skill changes and A/B testing variants
- **OMC State**: `.omc/state/` for skill execution tracking
- **Session Logs**: `.omc/sessions/` for historical performance data
- **Python 3.10+** with pandas, sqlite3

## Capabilities

- Track skill usage frequency, success rate, and execution time
- Identify skills with high error rates or poor user satisfaction
- Detect unused or redundant skills in the portfolio
- Generate improvement proposals based on failure patterns
- A/B test skill variants to measure improvement impact
- Monitor skill trigger accuracy (false positives/negatives)
- Track cross-skill dependencies and bottlenecks
- Generate weekly/monthly skill portfolio health reports

## When to Use

- Weekly maintenance routine for skill portfolio
- After adding new skills, check portfolio balance
- When a skill's error rate exceeds threshold (>10%)
- Before major skill updates, baseline current performance
- When planning which skills to add/improve/remove
- After user complaints about skill quality

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Metrics Collection

```python
import sqlite3
import json
from datetime import datetime, timedelta

DB_PATH = ".omc/metrics.db"

def init_metrics_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS skill_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            duration_ms INTEGER,
            success BOOLEAN,
            error_type TEXT,
            error_message TEXT,
            trigger_keyword TEXT,
            user_satisfied BOOLEAN,
            output_quality_score REAL,
            tokens_used INTEGER,
            context TEXT
        );

        CREATE TABLE IF NOT EXISTS skill_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            error_type TEXT NOT NULL,
            error_message TEXT,
            stack_trace TEXT,
            recovery_action TEXT,
            recovered BOOLEAN
        );

        CREATE TABLE IF NOT EXISTS skill_triggers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            trigger_keyword TEXT NOT NULL,
            triggered_at TEXT NOT NULL,
            correct_trigger BOOLEAN,
            false_positive BOOLEAN,
            user_overrode BOOLEAN
        );

        CREATE INDEX IF NOT EXISTS idx_exec_skill ON skill_executions(skill_name);
        CREATE INDEX IF NOT EXISTS idx_exec_time ON skill_executions(timestamp);
        CREATE INDEX IF NOT EXISTS idx_error_skill ON skill_errors(skill_name);
    """)
    conn.close()

def log_execution(skill_name, duration_ms, success, error=None, trigger=None, satisfaction=None, quality=None, tokens=None):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO skill_executions (skill_name, timestamp, duration_ms, success, error_type, error_message,
            trigger_keyword, user_satisfied, output_quality_score, tokens_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (skill_name, datetime.now().isoformat(), duration_ms, success,
          error.get("type") if error else None,
          error.get("message") if error else None,
          trigger, satisfaction, quality, tokens))
    conn.commit()
    conn.close()
```

### Performance Analysis

```python
import pandas as pd

def analyze_skill_performance(days=30):
    """Analyze all skills performance over the given period."""
    conn = sqlite3.connect(DB_PATH)
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()

    df = pd.read_sql_query("""
        SELECT skill_name,
               COUNT(*) as total_executions,
               AVG(duration_ms) as avg_duration_ms,
               SUM(CASE WHEN success THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
               AVG(user_satisfied) as satisfaction_rate,
               AVG(output_quality_score) as avg_quality,
               SUM(tokens_used) as total_tokens
        FROM skill_executions
        WHERE timestamp > ?
        GROUP BY skill_name
        ORDER BY total_executions DESC
    """, conn, params=[cutoff])

    conn.close()
    return df

def identify_bottlenecks():
    """Find skills that need improvement."""
    performance = analyze_skill_performance()
    bottlenecks = []

    for _, row in performance.iterrows():
        issues = []

        # High error rate
        if row["success_rate"] < 90:
            issues.append({
                "type": "high_error_rate",
                "severity": "critical" if row["success_rate"] < 80 else "warning",
                "value": f"{row['success_rate']:.1f}%",
                "threshold": "90%"
            })

        # Slow execution
        if row["avg_duration_ms"] > 30000:  # >30 seconds
            issues.append({
                "type": "slow_execution",
                "severity": "warning",
                "value": f"{row['avg_duration_ms']/1000:.1f}s",
                "threshold": "30s"
            })

        # Low satisfaction
        if row["satisfaction_rate"] and row["satisfaction_rate"] < 0.7:
            issues.append({
                "type": "low_satisfaction",
                "severity": "warning",
                "value": f"{row['satisfaction_rate']:.0%}",
                "threshold": "70%"
            })

        # High token usage
        if row["total_tokens"] and row["total_tokens"] > 1000000:
            issues.append({
                "type": "high_token_usage",
                "severity": "info",
                "value": f"{row['total_tokens']/1000000:.1f}M tokens",
                "threshold": "1M tokens"
            })

        if issues:
            bottlenecks.append({
                "skill": row["skill_name"],
                "executions": row["total_executions"],
                "issues": issues
            })

    return sorted(bottlenecks, key=lambda x: len(x["issues"]), reverse=True)
```

### Error Pattern Detection

```python
def detect_error_patterns(skill_name=None, days=30):
    """Find recurring error patterns across skills."""
    conn = sqlite3.connect(DB_PATH)
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()

    where_clause = "WHERE timestamp > ?"
    params = [cutoff]
    if skill_name:
        where_clause += " AND skill_name = ?"
        params.append(skill_name)

    df = pd.read_sql_query(f"""
        SELECT skill_name, error_type, error_message, COUNT(*) as occurrences
        FROM skill_errors
        {where_clause}
        GROUP BY skill_name, error_type, error_message
        HAVING occurrences >= 3
        ORDER BY occurrences DESC
    """, conn, params=params)

    conn.close()

    patterns = []
    for _, row in df.iterrows():
        patterns.append({
            "skill": row["skill_name"],
            "error_type": row["error_type"],
            "message": row["error_message"],
            "occurrences": row["occurrences"],
            "suggestion": suggest_fix(row["error_type"], row["error_message"])
        })

    return patterns

def suggest_fix(error_type, error_message):
    """Suggest fix based on error patterns."""
    FIXES = {
        "timeout": "Increase timeout threshold or optimize slow operations",
        "api_rate_limit": "Add rate limiting with exponential backoff",
        "file_not_found": "Add file existence check before operation",
        "auth_failure": "Refresh credentials or check API key rotation",
        "memory_limit": "Reduce batch size or add streaming processing",
        "parse_error": "Add input validation and error recovery",
        "network_error": "Add retry logic with circuit breaker"
    }
    return FIXES.get(error_type, f"Review error pattern: {error_message[:100]}")
```

### Improvement Proposal Generation

```python
def generate_improvement_proposals():
    """Generate actionable improvement proposals based on metrics."""
    proposals = []

    # 1. Fix high-error skills
    bottlenecks = identify_bottlenecks()
    for b in bottlenecks:
        if any(i["severity"] == "critical" for i in b["issues"]):
            proposals.append({
                "priority": "P0",
                "skill": b["skill"],
                "action": "fix_errors",
                "title": f"Fix critical error rate in {b['skill']}",
                "description": f"Success rate is {next(i['value'] for i in b['issues'] if i['type']=='high_error_rate')}",
                "steps": [
                    f"Analyze error patterns in {b['skill']}",
                    "Review top 5 most common errors",
                    "Add error handling for each pattern",
                    "Add retry logic where appropriate",
                    "Test with 100 simulated executions"
                ],
                "expected_impact": "Reduce error rate by 50%+"
            })

    # 2. Find unused skills
    all_skills = list_all_skills()
    performance = analyze_skill_performance()
    used_skills = set(performance["skill_name"].tolist())
    unused = [s for s in all_skills if s not in used_skills]

    if unused:
        proposals.append({
            "priority": "P2",
            "skill": "portfolio",
            "action": "review_unused",
            "title": f"Review {len(unused)} unused skills",
            "description": f"Skills not used in last 30 days: {', '.join(unused[:5])}",
            "steps": [
                "Check if unused skills have valid use cases",
                "Improve trigger keywords if skills should be triggered more",
                "Consider deprecating truly unused skills",
                "Update documentation for unclear skills"
            ],
            "expected_impact": "Reduce portfolio noise, improve trigger accuracy"
        })

    # 3. Optimize slow skills
    for b in bottlenecks:
        slow = [i for i in b["issues"] if i["type"] == "slow_execution"]
        if slow:
            proposals.append({
                "priority": "P1",
                "skill": b["skill"],
                "action": "optimize_speed",
                "title": f"Optimize execution speed of {b['skill']}",
                "description": f"Average execution: {slow[0]['value']}",
                "steps": [
                    "Profile skill execution to find slow points",
                    "Add caching for repeated operations",
                    "Consider parallel execution where possible",
                    "Reduce unnecessary API calls"
                ],
                "expected_impact": "Reduce execution time by 30%+"
            })

    # 4. Trigger accuracy improvement
    trigger_accuracy = analyze_trigger_accuracy()
    for skill, accuracy in trigger_accuracy.items():
        if accuracy["false_positive_rate"] > 0.1:
            proposals.append({
                "priority": "P1",
                "skill": skill,
                "action": "fix_triggers",
                "title": f"Reduce false positives for {skill}",
                "description": f"False positive rate: {accuracy['false_positive_rate']:.0%}",
                "steps": [
                    "Review false positive trigger keywords",
                    "Add negative keywords to reduce false matches",
                    "Add confidence scoring to trigger detection",
                    "Test with edge case inputs"
                ],
                "expected_impact": "Reduce false positives by 70%+"
            })

    return sorted(proposals, key=lambda x: {"P0": 0, "P1": 1, "P2": 2}[x["priority"]])
```

### A/B Testing Skill Variants

```python
def ab_test_skill(skill_name, variant_b_path, test_cases, metric="success_rate"):
    """
    A/B test a skill variant against the current version.

    Returns comparison results.
    """
    results_a = []
    results_b = []

    for test in test_cases:
        # Run current version
        start = time.time()
        result_a = run_skill(skill_name, test.input)
        duration_a = (time.time() - start) * 1000
        results_a.append({
            "success": result_a.success,
            "duration_ms": duration_a,
            "quality": evaluate_quality(result_a.output, test.expected)
        })

        # Run variant
        start = time.time()
        result_b = run_skill_variant(variant_b_path, test.input)
        duration_b = (time.time() - start) * 1000
        results_b.append({
            "success": result_b.success,
            "duration_ms": duration_b,
            "quality": evaluate_quality(result_b.output, test.expected)
        })

    # Compare results
    comparison = {
        "skill": skill_name,
        "test_cases": len(test_cases),
        "current": {
            "success_rate": sum(r["success"] for r in results_a) / len(results_a),
            "avg_duration_ms": sum(r["duration_ms"] for r in results_a) / len(results_a),
            "avg_quality": sum(r["quality"] for r in results_a) / len(results_a)
        },
        "variant": {
            "success_rate": sum(r["success"] for r in results_b) / len(results_b),
            "avg_duration_ms": sum(r["duration_ms"] for r in results_b) / len(results_b),
            "avg_quality": sum(r["quality"] for r in results_b) / len(results_b)
        }
    }

    comparison["winner"] = "variant" if comparison["variant"][metric] > comparison["current"][metric] else "current"
    comparison["improvement"] = abs(comparison["variant"][metric] - comparison["current"][metric])

    return comparison
```

### Weekly Portfolio Health Report

```python
def generate_weekly_report():
    """Generate comprehensive weekly skill portfolio report."""
    report = {
        "period": f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
        "summary": {},
        "top_performers": [],
        "needs_attention": [],
        "improvements_applied": [],
        "recommendations": []
    }

    # Summary stats
    performance = analyze_skill_performance(days=7)
    report["summary"] = {
        "total_executions": int(performance["total_executions"].sum()),
        "overall_success_rate": f"{performance['success_rate'].mean():.1f}%",
        "avg_execution_time": f"{performance['avg_duration_ms'].mean()/1000:.1f}s",
        "total_tokens_used": int(performance["total_tokens"].sum()),
        "active_skills": len(performance)
    }

    # Top performers (success rate > 95%, high usage)
    top = performance[(performance["success_rate"] > 95) & (performance["total_executions"] > 10)]
    report["top_performers"] = top[["skill_name", "success_rate", "total_executions"]].to_dict("records")

    # Needs attention
    report["needs_attention"] = identify_bottlenecks()[:5]

    # Recommendations
    report["recommendations"] = generate_improvement_proposals()[:5]

    return report
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `DB_LOCKED` | Concurrent access to metrics DB | Use WAL mode, retry with backoff |
| `INSUFFICIENT_DATA` | Not enough executions for analysis | Expand time window, note confidence level |
| `METRIC_SPIKE` | Sudden change in metrics | Investigate cause before acting, may be valid |
| `IMPROVEMENT_FAILED` | Applied improvement made things worse | Revert change, analyze why it failed |
| `TRIGGER_FALSE` | Skill triggered incorrectly | Update trigger keywords, add negative patterns |

## Common Patterns
- Use structured input/output schemas for reliable automation
- Add retry logic with exponential backoff for external calls
- Validate inputs before processing to fail fast
- Log execution steps for debugging and auditing


### Continuous Improvement Loop
```
1. Collect metrics (automated, every execution)
2. Analyze weekly (cron job or manual)
3. Generate proposals (automated)
4. Prioritize by impact (P0/P1/P2)
5. Implement top proposal (manual or automated)
6. A/B test variant (automated)
7. Deploy if better (manual approval)
8. Measure impact (automated)
9. Repeat from step 1
```

### Portfolio Health Score
```python
def portfolio_health_score():
    performance = analyze_skill_performance()
    return {
        "overall": weighted_average([
            (performance["success_rate"].mean(), 0.4),
            (performance["satisfaction_rate"].mean() * 100, 0.3),
            (100 - min(performance["avg_duration_ms"].mean() / 300, 100), 0.2),
            (len(performance[performance["success_rate"] > 90]) / len(performance) * 100, 0.1)
        ]),
        "grade": "A" if score > 90 else "B" if score > 80 else "C" if score > 70 else "D"
    }
```

### Trigger Keyword Optimization
- Track which keywords trigger each skill
- Flag keywords that trigger wrong skills (false positives)
- Suggest new keywords from successful executions that didn't auto-trigger
- Maintain negative keyword list per skill to reduce noise

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
