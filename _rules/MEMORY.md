---
name: memory
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [session-tracing, subagent-memory]
description: Agent Memory Protocol — filesystem-based read/write contract so sessions accumulate context (GAP-002)
---
# Agent Memory Protocol (GAP-002)

**Status:** Active · **Version:** 1.0 · **Last updated:** 2026-07-13

## Purpose

Every new agent session starts blind — re-reading files, re-discovering state, re-making decisions. The Memory Protocol provides a filesystem-based read/write contract so sessions accumulate context.

**Write side exists** (`skills/auto-brain-save/` → Vilona brain API).  
**Read side defined here** — local filesystem protocol for session-start loading.

---

## Directory Layout

```
~/.1ai/memory/
├── entities/           # Long-term entity knowledge
│   ├── project-1ai-rules.md
│   └── user-openclaw.md
├── sessions/           # Short-term session traces (auto-rotated)
│   └── 2026-07-13-session-abc123.md
├── index.json          # Metadata index (entity → file, last_seen)
└── config.yaml         # Tiers, TTL, compaction rules
```

---

## Entity Files (`memory/entities/<entity-name>.md`)

YAML frontmatter + markdown body. One file per logical entity (project, person, concept, tool).

```yaml
---
name: project-1ai-rules
type: project
last_seen: 2026-07-13
aliases:
  - 1ai-rules
facts:
  - "Core rules live in ~/.1ai/core/"
  - "Latest commit: 983b0ea"
decisions:
  - "PROCESS.md deleted: content merged into ENGINEERING.md §6"
  - "Memory protocol: filesystem-based, no external DB"
---
```

**Fields:**
- `name` — primary entity identifier (alphanumeric + hyphens)
- `type` — entity type: `project`, `person`, `concept`, `tool`, `domain`
- `last_seen` — last modified date (`YYYY-MM-DD`)
- `aliases` — alternative names for cross-reference resolution
- `facts` — known-true statements about the entity (sorted newest-first)
- `decisions` — architectural/rationale decisions involving this entity

**Body:** Freeform markdown notes, log of interactions, or any unstructured context.
**TTL:** Infinite. Entities persist until explicitly archived or removed.

---

## Session Trace Files (`memory/sessions/<date>-session-<id>.md`)

Auto-generated on session end. Single file per session.

```yaml
---
date: 2026-07-13
session_id: abc123
tasks_completed: 12
entities: ["project-1ai-rules", "user-openclaw"]
files_touched:
  - "core/MEMORY.md"
  - "bin/1ai"
outcome: "Memory protocol implemented"
decisions:
  - "Memory protocol passes through hooks and CLI"
---
```

**TTL:** 30 days. Older sessions are auto-compacted (summaries merged into entity files).

---

## Index (`memory/index.json`)

Rebuildable from filesystem scan. Not required for correct operation — purely for fast lookups.

```json
{
  "entities": {
    "project-1ai-rules": {
      "path": "entities/project-1ai-rules.md",
      "type": "project",
      "last_seen": "2026-07-13"
    }
  },
  "last_updated": "2026-07-13T04:00:00Z"
}
```

---

## Config (`memory/config.yaml`)

```yaml
tiers:
  entity:
    ttl_days: 0          # 0 = infinite
    max_items: 1000      # max entity files
  session:
    ttl_days: 30
    max_items: 100       # max session trace files before rotation
context:
  max_facts_per_entity: 50
  max_entities_per_load: 10
  max_recent_sessions: 5
```

---

## CLI Interface (`1ai memory <subcommand>`)

| Subcommand | Args | Effect |
|---|---|---|
| `remember` | `<entity> <fact>` | Add a fact to an entity (creates if new) |
| `recall` | `[entity]` | Print facts for entity (or all entities) |
| `session-start` | — | Initialize/register current session |
| `session-end` | `[summary]` | Finalize session trace + auto-save facts |
| `status` | — | Show memory stats (entity count, session count, config) |
| `compact` | — | Rotate stale sessions, compact entity files |
| `forget` | `<entity>` | Archive entity file (preserves data, marks inactive) |

---

## Entity-File Format Specification

### File Location

Each entity is stored at `~/.1ai/memory/entities/<sanitized-name>.md`.

**Name sanitization rules:**
1. Convert to lowercase
2. Replace non-alphanumeric characters (except `.` and `-`) with `-`
3. Collapse consecutive hyphens
4. Strip leading/trailing hyphens

### Frontmatter Rules

- Frontmatter is **YAML** delimited by `---` on its own line
- The `name` field in frontmatter is the canonical entity name (may differ from filename)
- `facts` — array of strings. Each fact is a complete statement.
- `decisions` — array of strings. Each decision = a choice + rationale.
- Writers **prepend** new facts/decisions to maintain reverse-chronological order
- Maximum 50 facts per entity (oldest trimmed on write). Rationale: context window discipline.

### Entity Reference

An entity reference is the string `entity://<entity-name>`.  
Tools and hooks MAY embed `entity://` URIs in prompts to trigger entity file loading.

---

## Integration Points

### Session-Start Hook

The session-start hook (`~/.claude/hooks/1ai-rules-session-start`) injects at session initialization:

1. Read the config
2. Load last N session trace summaries
3. Load top-K entities by recency
4. Append as context block

### Session-End Hook

The session-end hook (concept) runs `1ai memory session-end` to finalize the trace.

### Auto-Brain-Save Skill

The existing `skills/auto-brain-save/` calls `vilona_brain_remember()` — this is the WRITE side to external Vilona storage. The local memory protocol is a COMPLEMENTARY READ/WRITE layer that works offline and doesn't depend on Vilona availability.

---

## Lifecycle

```
Session Start
  │
  ├─ 1ai memory session-start
  │     └─ registers session in memory/sessions/
  │
  ├─ 1ai memory recall —agent
  │     └─ injects entity facts + recent sessions into context
  │
  ├─ 1ai memory remember <entity> <fact>
  │     └─ persists a new fact during the session
  │
  ├─ 1ai memory session-end [summary]
  │     └─ finalizes session trace, compacts entities
  │
Session End
```

---

## GAP Coverage

| Gap | Coverage |
|---|---|
| GAP-002 | Core protocol — directory layout, entity/session format, read/write |
| GAP-015 | Vector memory — embedding + semantic search (future, adds `index.json` vectors) |
| GAP-017 | Subagent frontmatter — entity references in subagent task assignments |
