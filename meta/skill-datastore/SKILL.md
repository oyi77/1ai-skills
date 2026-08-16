---
name: meta-skill-datastore
description: Use when centralized database for meta-skill operations. Stores performance
  metrics, feedback, patterns, and skill evolution history. Use when working with
  meta skill datastore.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- datastore
- meta
- meta-learning
- self-improvement
- skill
- skill-evolution
version: 1.0.0
category: meta
---

# Meta Skill Datastore

## When to Use

**Trigger phrases:**
- "meta skill datastore"
- "Help me with meta skill datastore"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/meta-datastore record-execution --skill seo-optimizer --success true --latency 245

# Query performance
/meta-datastore query "SELECT AVG(latency_ms) FROM skill_executions WHERE skill_name='seo-optimizer'"

# Get improvement candidates
/meta-datastore get-improvements --min-impact 0.7 --status proposed
```

### Integration

Connects to:
- performance-monitor (writes metrics)
- feedback-collector (stores feedback)
- pattern-recognition (queries patterns)
- skill-evolution (tracks versions)


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Meta Skill Datastore is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for skill management
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |
| "SQLite is too simple for metrics" | SQLite handles millions of rows for single-agent deployments; operational overhead of a full DBMS is wasted. |
| "Just log to a file" | Structured queryability enables cross-skill pattern discovery that flat file grep cannot provide. |
| "Feedback is subjective noise" | Aggregated feedback across 100+ invocations reveals statistically significant improvement signals. |

## Process

### Preparation
- Define the metrics schema: latency, success rate, token usage, error category.
- Configure retention policies: daily aggregation, monthly archival, yearly purge.
- Validate the SQLite database file path and ensure write permissions.

### Execution
- Record every skill invocation with name, timestamp, duration, success/failure, and error type.
- Store feedback as structured JSON with rating, free-text comments, and invocation reference.
- Run weekly aggregation queries to compute quartile performance bounds per skill.

### Stewardship
- Monitor database file size; compact with `VACUUM` quarterly.
- Archive data older than 90 days to compressed JSONL for long-term trend analysis.
- Update schema via migration scripts rather than destructive recreations.

## Workflow

1. **Instrument** — Add a `record_execution()` call at the end of every skill's main function to capture latency, success, and tokens.
2. **Collect** — Batch-write execution records into the datastore; use WAL mode for concurrent access.
3. **Analyze** — Run weekly SQL queries identifying skills with degrading performance or rising error rates.
4. **Feedback ingest** — Accept structured feedback records tied to specific invocation IDs for full traceability.
5. **Pattern detect** — Join execution data with feedback to surface skills performing well technically but poorly in user ratings.
6. **Version track** — Store skill SKILL.md content hashes alongside executions to correlate version changes with performance shifts.
7. **Report** — Generate a weekly meta-datastore digest showing top-5 improvement candidates with supporting evidence.

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
- [ ] SQLite database file created and writable
- [ ] record_execution inserts rows without error
- [ ] Query by skill_name returns correct aggregation
- [ ] Feedback records link to valid invocation IDs
- [ ] VACUUM runs without locking concurrent readers
- [ ] Schema migration applies without data loss

## Code Examples

```python
import sqlite3
import json
from datetime import datetime, timezone

DB_PATH = "~/.1ai/meta-datastore.db"

def record_execution(skill_name: str, success: bool, latency_ms: int,
                     tokens_used: int = 0, error_type: str = "") -> int:
    """Record a skill execution and return the invocation ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS skill_executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        success INTEGER NOT NULL,
        latency_ms INTEGER NOT NULL,
        tokens_used INTEGER DEFAULT 0,
        error_type TEXT DEFAULT ''
    )""")
    cur = conn.execute(
        "INSERT INTO skill_executions(skill_name, timestamp, success, latency_ms, tokens_used, error_type) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (skill_name, datetime.now(timezone.utc).isoformat(), int(success), latency_ms, tokens_used, error_type)
    )
    conn.commit()
    conn.close()
    return cur.lastrowid

def get_avg_latency(skill_name: str) -> float:
    """Return average latency for a skill over the last 100 runs."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT AVG(latency_ms) FROM skill_executions "
        "WHERE skill_name = ? ORDER BY id DESC LIMIT 100",
        (skill_name,)
    ).fetchone()
    conn.close()
    return row[0] if row[0] else 0.0

def store_feedback(invocation_id: int, rating: int, comment: str) -> None:
    """Attach feedback to a specific skill execution."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invocation_id INTEGER NOT NULL,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        comment TEXT,
        created TEXT NOT NULL,
        FOREIGN KEY (invocation_id) REFERENCES skill_executions(id)
    )""")
    conn.execute(
        "INSERT INTO feedback(invocation_id, rating, comment, created) VALUES (?, ?, ?, ?)",
        (invocation_id, rating, comment, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def get_improvement_candidates(min_invocations: int = 10) -> list[dict]:
    """Return skills with high latency or low success rate needing improvement."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT skill_name, COUNT(*) as runs,
               AVG(latency_ms) as avg_lat,
               AVG(success) as success_rate
        FROM skill_executions
        GROUP BY skill_name
        HAVING runs >= ?
        ORDER BY success_rate ASC, avg_lat DESC
    """, (min_invocations,)).fetchall()
    conn.close()
    return [
        {"skill": r[0], "runs": r[1], "avg_latency_ms": round(r[2], 1), "success_rate": round(r[3], 2)}
        for r in rows
    ]
```

## Common Issues

| Error | Root Cause | Fix |
|---|---|---|
| `database is locked` | Concurrent writes from parallel skill invocations | Enable WAL mode: `PRAGMA journal_mode=WAL;` |
| `no such table` | First run without schema initialization | Call `record_execution` once to auto-create tables |
| `disk full` | Unbounded metric growth exceeding disk quota | Add retention: `DELETE FROM skill_executions WHERE id NOT IN (SELECT id FROM skill_executions ORDER BY id DESC LIMIT 10000)` |
| `FOREIGN KEY constraint failed` | Orphaned feedback referencing deleted invocation | Cascade delete: add `ON DELETE CASCADE` to feedback FK |
| `inconsistent results` | Concurrent read during write without transaction isolation | Wrap writes in `BEGIN IMMEDIATE` / `END` blocks |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Meta-skill analytics SaaS | 3-6 months | Hosted dashboard showing cross-skill performance trends, regression alerts, and improvement recommendations for agent teams |
| Custom integration consulting | 1-3 months | Deploy the datastore schema and reporting pipeline into existing agent orchestration platforms (LangChain, CrewAI, AutoGen) |
| Performance benchmarking service | 2-4 months | Run standardized skill workloads, publish comparative benchmarks, charge for detailed per-skill diagnostic reports |
| Managed datastore plugin | 1-2 months | Bundle as a ready-to-install plugin for OMP / 1ai-hub with automated setup, migration management, and backup scheduling |
| Open-core enterprise license | 3-9 months | Free single-agent SQLite version; paid multi-agent PostgreSQL backend with sharding and real-time dashboards |