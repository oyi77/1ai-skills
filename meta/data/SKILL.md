---
name: data
description: Centralized database for meta-skill operations. Stores performance metrics, feedback, patterns, and skill evolution
  history.
persona:
  name: Database Architect
  expertise: SQLite, data modeling, query optimization
  philosophy: Data is the foundation of intelligence
---
## Meta Skill Datastore

Storage layer for self-improving agent system.

### Database Schema

```sql
-- Performance metrics
CREATE TABLE skill_executions (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN,
    latency_ms INTEGER,
    tokens_used INTEGER,
    cost_usd REAL,
    user_satisfaction REAL,
    output_quality REAL,
    error_type TEXT,
    input_hash TEXT
);

-- Feedback collection
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER, -- 1-5
    comment TEXT,
    sentiment_score REAL,
    source TEXT, -- 'explicit', 'implicit', 'automated'
    processed BOOLEAN DEFAULT FALSE
);

-- Pattern recognition
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    pattern_type TEXT, -- 'success', 'failure', 'input', 'execution'
    pattern_hash TEXT,
    frequency INTEGER,
    first_seen DATETIME,
    last_seen DATETIME,
    success_rate REAL
);

-- Skill versions
CREATE TABLE skill_versions (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    version TEXT,
    previous_version TEXT,
    changes TEXT,
    breaking_change BOOLEAN,
    deployed_at DATETIME,
    rolled_back BOOLEAN DEFAULT FALSE
);

-- Improvements
CREATE TABLE improvements (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    improvement_type TEXT,
    description TEXT,
    impact_score REAL,
    effort_score REAL,
    status TEXT, -- 'proposed', 'approved', 'implemented', 'rejected'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Learning cycles
CREATE TABLE learning_cycles (
    id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL,
    cycle_number INTEGER,
    started_at DATETIME,
    completed_at DATETIME,
    samples_analyzed INTEGER,
    improvements_generated INTEGER,
    status TEXT
);
```

### Usage

```python
# Record execution
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

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

