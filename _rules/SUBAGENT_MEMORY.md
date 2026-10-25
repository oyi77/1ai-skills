---
name: subagent-memory
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [memory, multi-agent]
description: Subagent Memory Frontmatter Protocol — structured frontmatter handoff so subagents start with full context (GAP-017)
---
# Subagent Memory Frontmatter Protocol (GAP-017)

**Status:** Active · **Version:** 1.0 · **Last updated:** 2026-07-13

## Problem Statement

Subagents spawn blind — they have zero context about the task's entities, prior decisions, or session state. This forces every subagent to re-discover state from scratch, wasting tokens and producing inconsistent output. The Subagent Memory Protocol provides a structured frontmatter handoff so subagents start with full context.

## Design

Each subagent task assignment gets a **YAML frontmatter block** passed via a `memory-context.md` file (referenced via `local://` URI). The subagent reads this file on start, works, writes its own `memory-output.md` with discoveries, and the orchestrator merges results back into entity files.

## Frontmatter Format

```
---
entities:
  - name: project-1ai-rules
    type: project
    last_seen: 2026-07-13
    facts:
      - "Core rules live in ~/.1ai/core/"
    decisions:
      - "PROCESS.md deleted: content merged into ENGINEERING.md §6"
  - name: user-openclaw
    type: person
    last_seen: 2026-07-12
    facts:
      - "Prefers terse responses, no filler"
      - "Working on 1ai-framework ecosystem"
    decisions: []
session:
  session_id: d92f380b
  date: 2026-07-13
  open_tasks:
    - "GAP-017: Create subagent memory frontmatter protocol"
decisions:
  - "Subagent frontmatter uses entity:// URIs for cross-reference"
---
```

### Fields

| Field | Type | Description |
|---|---|---|
| `entities` | array | List of entity references with facts and decisions |
| `entities[].name` | string | Entity canonical name |
| `entities[].type` | string | Entity type (project, person, concept, tool, domain) |
| `entities[].last_seen` | date | Last modification date |
| `entities[].facts` | string[] | Known facts (newest first, max 50) |
| `entities[].decisions` | string[] | Architectural decisions |
| `session.session_id` | string | Current session identifier |
| `session.date` | date | Session date |
| `session.open_tasks` | string[] | Unresolved tasks from session file |
| `decisions` | string[] | Cross-cutting decisions relevant to all entities |

## Lifecycle

```
     Orchestrator                          Subagent
          │                                    │
          ├─ memory-context.sh ───────────────►│
          │   (entities + session →            │
          │    frontmatter YAML)               │
          │                                    ├─ read memory-context.md
          │                                    ├─ work
          │                                    ├─ write memory-output.md
          │                                    │   (YAML frontmatter:
          │                                    │    new_facts, new_decisions)
          │◄───────────────────────────────────┤
          │
          ├─ memory-merge.sh
          │   (memory-output.md →
          │    entity file updates)
          │
          ▼
     Next task
```

### Step-by-step

1. **Spawn:** Orchestrator runs `memory-context.sh <entity-names...> --session <id> --output local://memory-context.md`
2. **Context file** contains YAML frontmatter with entity facts, session state, and open tasks
3. **Subagent reads** the context file at start — typically via `read("local://memory-context.md")` in its eval cell
4. **Subagent works** on the assignment with full context
5. **Subagent writes output** as another frontmatter file (e.g. `local://memory-output.md`) with:
   - `new_facts` — discoveries made during the task
   - `new_decisions` — decisions taken
   - `entities_touched` — which entities were modified
6. **Orchestrator runs** `memory-merge.sh <output-dir>` which:
   - Parses each output file's YAML frontmatter
   - Calls `memory.sh remember` for each new fact/decision
   - Validates YAML structure before merging

## Output Format (subagent writes)

```
---
new_facts:
  - entity: project-1ai-rules
    fact: "SUBAGENT_MEMORY.md added to core/ with lifecycle protocol"
  - entity: user-openclaw
    fact: "Assigned GAP-017, completed subagent memory protocol"
new_decisions:
  - entity: project-1ai-rules
    decision: "GAP-017: Subagent frontmatter uses YAML, referenced via local:// URIs"
entities_touched:
  - project-1ai-rules
  - user-openclaw
session_id: d92f380b
---
```

## Integration with GAP-002

GAP-002 defines the base memory protocol (entity files, session traces, `1ai memory` CLI). GAP-017 builds on top:

| GAP-002 | GAP-017 |
|---|---|
| Entity files (`memory/entities/*.md`) | Multi-entity context aggregation for subagent handoff |
| `1ai memory remember` | `memory-context.sh` batches entity facts |
| `1ai memory recall` | `memory-merge.sh` pipes back entity writes |
| Session traces (`.md` files) | Session frontmatter in context + output files |

## CLI Interface

```
1ai memory context <entity>... [--session <id>] [--output <path>]
    Generate context frontmatter for specified entities
    Default output: local://memory-context.md in cwd

1ai memory merge <output-dir>
    Merge output context files from subagents into entity store
    Scans <output-dir>/*-output.md, parses frontmatter, calls remember
```

## Cross-Reference

- GAP-002: `core/MEMORY.md` — Base memory protocol (entity format, directory layout)
- `core/SUBAGENT_MEMORY.md` — This document
- Entity URIs: `entity://<entity-name>` references an entity file
