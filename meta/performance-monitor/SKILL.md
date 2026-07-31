---
name: performance-monitor
description: Track and analyze skill execution performance. Measure latency, success rates, accuracy, and resource usage for
  continuous improvement. Use when tracking and analyze skill execution performance. measure latency, success rates,.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- meta-learning
- monitor
- performance
- self-improvement
- skill-evolution
persona:
  name: Performance Engineer
  expertise: Metrics, monitoring, optimization
  philosophy: If you can't measure it, you can't improve it
  credentials: SRE at Google, built monitoring systems
version: 1.0.0
---
# Performance Monitor

## When to Use

**Trigger phrases:**
- "performance monitor"
- "Help me with performance monitor"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/performance-monitor start skill-name

# Get report
/performance-monitor report skill-name --days 7

# Compare skills
/performance-monitor compare skill1 skill2 --metric success_rate
```

### Features

- Real-time metric collection
- Historical trend analysis
- Anomaly detection
- Performance regression alerts
- Cost tracking per skill


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

The Performance Monitor is a meta-skill that provides execution telemetry for every skill in the ecosystem. It collects, stores, and analyzes key performance indicators — execution latency, success rates, accuracy against expected outcomes, resource consumption (tokens, memory, wall time), and invocation frequency — giving both the agent and its operator visibility into how skills actually perform in production.

The lifecycle of performance monitoring spans five phases: **instrumentation** (wrapping skill execution to capture raw data), **collection** (aggregating and normalizing metrics into a structured store), **analysis** (computing percentiles, trends, and anomaly scores), **alerting** (firing notifications when metrics cross configured thresholds), and **improvement** (feeding insights back into skill versioning to guide optimization). Each phase is independently configurable, so a skill can graduate from simple timer-based tracking to full token accounting as it matures.

Measurement granularity matters. The monitor captures per-invocation data — each call to a skill produces a record with latency, outcome status (success, failure, timeout, or error), error type when applicable, estimated token consumption, and a timestamp. These raw samples feed into rolling window statistics: p50/p95/p99 latency, success rate over the last 1000 invocations, daily active skill counts, and token burn rate per skill per session.

The design follows the principle that monitoring must never become the bottleneck. The metric writer operates with a write-behind buffer and batch-inserts to SQLite (the default backend) at sub-millisecond overhead per invocation. For larger deployments, the same interface can back Prometheus counters or TimescaleDB hypertables without changing instrumentation code.


## Workflow

1. **Instrument the skill** — Apply the `@track_performance` decorator to the skill's entry-point function, or register a global hook via the 1ai-skills hook system that wraps every skill invocation automatically. The instrumentation layer captures start time, function arguments (sanitized), and agent session metadata.

2. **Execute and capture** — As the skill runs, the monitor records elapsed wall time, exit status (success or exception with error type), and estimated token consumption. Failures are captured in the `finally` block so that even crashing skills produce a metric record.

3. **Persist to the metrics store** — Each invocation sample is buffered and batch-inserted into the configured backend (SQLite by default). The schema stores skill_name, latency_ms, status, error_type, tokens_estimated, and recorded_at. The batch interval is configurable to balance write overhead against data freshness.

4. **Aggregate and compute trends** — A periodic aggregation job reads raw samples and computes rolling statistics: success rate over sliding windows (100 / 1K / 10K invocations), latency percentiles (p50, p95, p99), invocation frequency per hour, and token burn rate. Results are stored in a summary table for fast querying.

5. **Analyze for anomalies and regressions** — Compare the latest aggregated values against the trailing 14-day baseline. A z-score exceeding the configured threshold (default 3.0) triggers a regression flag. The analyzer also detects missing metrics (a skill that suddenly stopped reporting) and volume anomalies (unusual spike in invocations).

6. **Alert on threshold breaches** — When a regression flag is raised, the monitor dispatches a notification through the configured channel (Slack webhook, Telegram bot, or log file). The alert includes the skill name, metric that crossed the threshold, baseline vs current value, and a link to the trend chart.

7. **Review and optimize** — Weekly trend reports are generated automatically. Skill maintainers review the report, correlate metric shifts with code changes, and prioritize optimization. When a skill version is updated, the pre- and post-change metrics are compared to confirm the fix and update the baseline.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for skill management
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Code Examples

### Tracking Decorator

```python
import time, functools, sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path.home() / ".1ai" / "metrics.db"

def track_performance(skill_name: str):
    """Decorator that records latency, success, and token usage for a skill call."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            try:
                result = fn(*args, **kwargs)
                status = "success"
                error_type = None
            except Exception as e:
                result = None
                status = "failure"
                error_type = type(e).__name__
                raise
            finally:
                elapsed_ms = (time.monotonic() - start) * 1000
                _write_metric(skill_name, elapsed_ms, status, error_type)
            return result
        return wrapper
    return decorator

def _write_metric(name, latency_ms, status, error_type):
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.execute(
            "INSERT INTO skill_metrics (skill_name, latency_ms, status, error_type, recorded_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, latency_ms, status, error_type, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()
```

### Report Generator

```python
def generate_report(skill_name: str, days: int = 7) -> dict:
    """Aggregate metrics and return summary statistics."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT latency_ms, status, error_type FROM skill_metrics "
        "WHERE skill_name = ? AND recorded_at >= datetime('now', ?)",
        (skill_name, f"-{days} days"),
    ).fetchall()
    conn.close()

    if not rows:
        return {"error": "no data for period"}

    latencies = [r["latency_ms"] for r in rows]
    successes = sum(1 for r in rows if r["status"] == "success")
    sorted_lat = sorted(latencies)
    n = len(latencies)

    return {
        "skill": skill_name,
        "period_days": days,
        "invocations": n,
        "success_rate": round(successes / n, 4),
        "latency_ms": {
            "p50": sorted_lat[n // 2] if n else 0,
            "p95": sorted_lat[int(n * 0.95)] if n else 0,
            "p99": sorted_lat[int(n * 0.99)] if n else 0,
            "avg": round(sum(latencies) / n, 1) if n else 0,
        },
        "errors": {e: sum(1 for r in rows if r["error_type"] == e)
                   for e in set(r["error_type"] for r in rows if r["error_type"])},
    }
```

### Usage Example

```python
# Apply the tracker to any skill function
@track_performance("content-seo-optimizer")
def run_seo_optimizer(text):
    # ... skill logic ...
    return results

# Generate a weekly report
report = generate_report("content-seo-optimizer", days=7)
print(f"Success rate: {report['success_rate']*100:.1f}%")
print(f"p95 latency: {report['latency_ms']['p95']:.0f}ms")

```
## Configuration

- **Metrics backend** — SQLite file path (default: `~/.1ai/metrics.db`), connection pool size, write-batch interval
- **Instrumentation mode** — `decorator` (wrap individual functions), `hook` (intercept all skill calls via hook system), or `hybrid`
- **Latency thresholds** — p50/p95/p99 targets in milliseconds; defaults: p50 < 500ms, p95 < 2_000ms, p99 < 5_000ms
- **Token budget** — per-skill token cap per invocation and per-session alert threshold
- **Retention policy** — raw sample TTL in days, aggregation interval (hourly → daily → weekly), compression method
- **Alert channels** — Slack webhook URL, Telegram bot token, or local log file path for regression notifications
- **Anomaly detection** — enable/disable toggle, z-score threshold (default: 3.0), baseline window in days (default: 14)

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Common Issues / Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| Metrics not appearing for a skill | Instrumentation decorator not applied or hook not registered | Verify the hook file exists in `hooks/post/` and the skill module is imported before first use. Run `grep "track_performance"` on the skill source to confirm coverage. |
| Token counts are zero for all calls | Tokenizer model mismatch between metric collector and LLM backend | Update the tokenizer identifier in metrics config to match the deployed model (e.g., `gpt-4o` vs `claude-3-opus-20240229`). |
| Latency spikes not flagged as anomalies | Z-score threshold too loose or baseline window too short | Reduce anomaly z-score threshold to 2.5 and extend the baseline window to 14 days of data. |
| Metric storage growing unbounded | No retention policy configured | Add a 90-day raw-sample TTL and configure daily aggregation with hourly/daily rollups. |
| Cost-per-skill shows zero for 30% of skills | Those skills lack `@track_performance` instrumentation | Bulk-audit all skills in SKILLS.json; add decorator or wrapper to untracked ones. Run `grep -L "track_performance" meta/*/SKILL.md` to find gaps. |
| Alert fires but no real regression exists | Cold-start invocations inflate p99 latency | Filter out the first invocation after a session boundary — cold starts inflate p99 by 3–5x compared to warm runs. |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |
| "Latency is a server problem, not a skill problem" | Poor prompt design, excessive tool calls, and redundant loops cause most agent-side latency. Instrument first, then optimize. |
| "I will add monitoring later" | Without baseline data, you cannot detect regressions. Monitoring from day one pays for itself on the first incident. |
| "Token tracking adds overhead worth ignoring" | Token cost is the hidden expense in agent systems. A 2% overhead for tracking is negligible compared to 40% waste from runaway loops. |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Internal Observability SaaS | 4–6 weeks | Package the performance monitor as a standalone dashboard for agent fleets. Offer latency heatmaps, success-rate SLAs, and token-cost analytics per skill. |
| Performance Optimization Consulting | Ongoing | Analyze underperforming skills for clients — identify high-latency or high-failure-rate skills and deliver targeted rewrites. Bill per skill or monthly retainer. |
| Custom Anomaly Detection Add-on | 8–12 weeks | Extend the monitor with ML-based anomaly detection that flags unusual performance patterns before they become incidents. Sell as premium tier. |
| Token & Cost Governance Dashboard | 2–4 weeks | Build an executive cost-per-skill view with budget burn rate, cost-per-session, and forecast. Target enterprise teams managing large AI agent deployments. |
| Open-Source Core + Paid Enterprise | Product lifecycle | Keep core metric collection OSS; charge for RBAC, multi-cluster dashboards, SSO integration, and compliance-ready audit exports. |


## Process

### Preparation
- Instrument the target skill with the `@track_performance` decorator or context manager wrapper.
- Define acceptance thresholds for key metrics: latency (p50/p95/p99), success rate (≥99%), token budget per call.
- Choose a metrics backend — SQLite for single-agent setups, TimescaleDB or Prometheus for distributed deployments.
- Configure monitoring interval, data retention policy (default: 90 days raw samples, rolling aggregates permanent).

### Execution
- Run the skill through its full range of invocations — success paths, edge cases, and expected failure modes.
- Verify that every call path produces a metric record: success, failure, timeout, or error classification.
- Monitor real-time dashboards during batch runs to spot regressions before they affect production.

### Stewardship
- Review weekly trend reports and correlate metric shifts with recent skill version changes.
- Tune alert thresholds as the skill matures — tighter for production-critical skills, wider for experimental ones.
- Archive raw data beyond retention limits; compress old aggregates to the minimum-resolution tier.

## Verification

- [ ] Instrumentation hooks registered and firing on each skill invocation
- [ ] Metric capture verified with at least one real invocation per tracked skill
- [ ] Latency, success status, token count, and error type written to metrics backend
- [ ] Anomaly detection triggers on regressions exceeding configured z-score threshold
- [ ] Reporting pipeline generates periodic trend output without errors
- [ ] Alert channel delivers notifications on cross-threshold events
- [ ] Cost-per-skill breakdown reconciles with actual usage logs