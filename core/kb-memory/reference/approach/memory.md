---
name: memory-system
description: Store, retrieve, and organize knowledge across sessions using structured memory files and entity tracking. Use when working with memory system.
domain: core
author: mahipal
license: Apache-2.0
subdomain: core-platform
tags:
- infrastructure
- memory
- self-improvement
- system
version: 1.0.0
---
# Memory System

## When to Use
**Trigger phrases:**
- "memory system"
- "Store, retrieve, and organize knowledge across sessions using structured memory "


- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

Memory System provides persistent knowledge management for AI agents, enabling them to store, retrieve, and organize information across session boundaries. Without structured memory, each conversation starts from scratch — the agent has no recollection of past decisions, user preferences, or project context. This skill implements a file-based memory architecture inspired by Tiago Forte's PARA method, organizing knowledge into Projects, Areas, Resources, and Archives with atomic entity tracking and relationship mapping.

The system operates across three complementary memory layers. First, a **knowledge graph** stores structured facts as entities with typed relations and observations — enabling the agent to answer questions like "which PRs touched the auth module?" or "what was the deployment configuration decision?" without re-reading files. Second, **working memory** provides a short-term buffer for the current session's active context, automatically decaying stale items. Third, **daily notes** capture raw chronological activity as a fallback for unstructured recall.

**Session persistence** is the core differentiator. The memory system writes structured YAML files to disk after every significant action, ensuring that a session interrupted mid-task can resume with full context. File paths follow a predictable convention under `~/.1ai/memory/`, organized by category and date. Cross-session retrieval uses keyword search against entity names and observation text, with configurable importance scoring to surface the most relevant memories first.

**Entity tracking** powers the knowledge graph. Each entity (concept, person, file, decision) is stored as a named node with typed observations and explicit relations to other entities. For example, a "deployment-config" entity might relate to "v3.35.0-release" via a "USED_IN" relation, with observations describing the actual values chosen. This graph structure supports spreading activation — querying "deployment config" can surface related decisions about environment variables, CI pipelines, and rollback procedures without explicit mention.

**Recall optimization** balances depth against context window constraints. Shallow recall returns 5-10 highest-importance observations from recent sessions. Deep recall expands to entity neighborhoods, following relations 1-2 hops from matching nodes. The system supports time-windowed queries ("what happened last session?"), category filters (projects only), and minimum importance thresholds. Weekly synthesis compresses fragmented observations into consolidated summaries, preventing memory bloat while preserving signal.
## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Workflow

1. **Detect Session Start** — On initialization, read the session context file at `~/.1ai/.session-context.md`. If stale (>30 min), verify all claims against disk state. Load memory index from `~/.1ai/memory/index.yaml` to identify previously tracked entities.

2. **Load Active Entities** — From the memory index, select entities tagged `active: true`. Expand each entity's observations and 1-hop relations into working memory. Prune entities that haven't been referenced in the last 7 days by demoting them to `inactive`.

3. **Process Incoming Facts** — As the agent executes tasks, extract structured facts: decisions made, files created, configurations set, errors encountered. For each fact, determine if it creates a new entity, adds an observation to an existing entity, or establishes a relation between entities.

4. **Write to Disk** — Persist all changes atomically: write to a temporary file, verify integrity, then rename into place. The `entities/` directory stores one YAML file per entity. The `relations/` directory stores relation pairs. The `daily/` directory stores chronological session logs. Flush write buffer after every action or at most 60 seconds of idle.

5. **Index Update** — After each write, rebuild the in-memory index. The index maps entity names to file paths, relation types to entity pairs, and timestamps to memory entries. This enables O(1) lookup for known entities and O(log n) range queries on timestamps.

6. **Periodic Consolidation** — Every 7 sessions or 24 hours (whichever comes first), run the 4-tier consolidation pipeline: Working → Episodic → Semantic → Procedural. Working memories with 3+ references promote to Episodic. Patterns observed across 5+ episodes extract as Semantic rules. Verified Semantic patterns promoted to Procedural (actionable skills). Consolidation runs as a background task and writes results to `~/.1ai/memory/consolidated/`.

7. **Recall on Request** — When the agent receives a query or starts a new task, search the memory system using the following cascade: (a) exact entity name match, (b) keyword search on observations, (c) fuzzy match on entity names (Levenshtein distance ≤2), (d) spreading activation from the closest matching entity. Return top results ranked by importance × recency with a token budget of 4K characters.

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

## Code Examples

```python
import yaml
from pathlib import Path
from datetime import datetime, timedelta

# === Entity tracking ===
MEMORY_DIR = Path("~/.1ai/memory").expanduser()

def save_entity(name: str, entity_type: str, observations: list[str], relations: list[dict] = None):
    """Store or update a knowledge graph entity."""
    entity_path = MEMORY_DIR / "entities" / f"{name.lower().replace(' ', '-')}.yaml"
    entity_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "name": name,
        "type": entity_type,
        "observations": observations,
        "relations": relations or [],
        "updated": datetime.now().isoformat(),
        "access_count": 0,
    }
    if entity_path.exists():
        existing = yaml.safe_load(entity_path.read_text())
        data["access_count"] = existing.get("access_count", 0) + 1
        existing_obs = set(existing.get("observations", []))
        data["observations"] = list(existing_obs | set(observations))

    # Atomic write
    tmp = entity_path.with_suffix(".yaml.tmp")
    tmp.write_text(yaml.dump(data, default_flow_style=False))
    tmp.rename(entity_path)
    return entity_path

def query_entities(keyword: str, max_results: int = 10, min_importance: float = 0.0):
    """Search entities by keyword in name and observations."""
    results = []
    for path in (MEMORY_DIR / "entities").glob("*.yaml"):
        entity = yaml.safe_load(path.read_text())
        importance = entity.get("importance", 0.5)
        if importance < min_importance:
            continue
        text = f"{entity['name']} {' '.join(entity.get('observations', []))}"
        if keyword.lower() in text.lower():
            results.append((importance, entity))
    results.sort(key=lambda x: -x[0])
    return [e for _, e in results[:max_results]]

# === Session persistence ===
def save_session_snapshot(session_id: str, context: dict):
    """Persist full session context for recovery after interruption."""
    daily_path = MEMORY_DIR / "daily" / datetime.now().strftime("%Y-%m-%d") / f"{session_id}.yaml"
    daily_path.parent.mkdir(parents=True, exist_ok=True)
    daily_path.write_text(yaml.dump({
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "context": context,
    }, default_flow_style=False))

# === Weekly consolidation ===
def consolidate_weekly():
    """Compress fragmented daily observations into consolidated summaries."""
    consolidated = {"decisions": [], "patterns": [], "artifacts": []}
    cutoff = datetime.now() - timedelta(days=7)
    daily_dir = MEMORY_DIR / "daily"
    for day_dir in sorted(daily_dir.iterdir()):
        if not day_dir.is_dir():
            continue
        day_date = datetime.strptime(day_dir.name, "%Y-%m-%d")
        if day_date < cutoff:
            continue
        for session_file in day_dir.glob("*.yaml"):
            session = yaml.safe_load(session_file.read_text())
            ctx = session.get("context", {})
            if "decision" in ctx:
                consolidated["decisions"].append(ctx["decision"])
            if "pattern" in ctx:
                consolidated["patterns"].append(ctx["pattern"])

    out_path = MEMORY_DIR / "consolidated" / f"week-{datetime.now().strftime('%Y-W%W')}.yaml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.dump(consolidated, default_flow_style=False))
    return out_path
```

## Common Issues / Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| Memory file not found on session resume | Index file stale or corruption | Run `rebuild_index()` which rescans the entities/ directory and regenerates `~/.1ai/memory/index.yaml` |
| Entity observations truncated after save | YAML write buffer not flushed before rename | Use atomic write pattern: write to `.tmp` file, call `flush()`, then `rename()` — never write directly to the target path |
| Cross-session recall returns empty results | Memory directory path mismatch between sessions | Verify `MEMORY_DIR` is an absolute path in both sessions; check `~/.1ai/memory/` exists and is readable |
| Knowledge graph query too slow (>5s) | Too many uncategorized entities (>500) without indexing | Run consolidation to categorize entities; enable weekly pruning of entities with `importance < 0.2` and no access in 30 days |
| YAML parse error on memory load | Corrupted write from process kill mid-write | Use journaling: keep the last-known-good backup at `~/.1ai/memory/index.yaml.bak` and fall back on parse failure |
| Duplicate entities for same concept | Case variations or typo-different names | Normalize entity names to lowercase with hyphenated words; before creating, search by Levenshtein distance ≤2 |
| Memory growing unbounded (>50MB) | No consolidation or pruning configured | Set `MAX_ENTITIES=200` in config; run weekly consolidation; archive entities not accessed in 60 days to `.archive/` |

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll remember what I did last session without writing it down" | Context window compaction WILL lose state. Without persistent memory files, every session starts blank. Write every decision. |
| "One big JSON file is simpler than a structured directory" | A single file creates write contention, makes partial reads wasteful, and breaks entirely on corruption. Structured directories let you recover individual entities. |
| "I don't need entity tracking — I'll just grep the session logs" | grep is linear-scan over unstructured text. Entity tracking gives O(1) lookup by name, typed relations for graph traversal, and importance scoring for relevance ranking. |
| "Consolidation can wait until memory gets slow" | By the time it's slow, you have thousands of fragmented observations. Prevention: consolidate after every 7 sessions or 24 hours, whichever comes first. |
| "Recalling everything is better than recalling selectively" | LLM context windows are finite and expensive. Selective recall with importance × recency ranking maximizes relevant signal per token. |
| "Memory persistence is just file I/O — no design needed" | Without schema design, entity naming conventions, and relation types, the knowledge graph becomes a write-only archive. Plan the schema before the first write. |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Consulting: Agent Memory Architecture | 2-4 weeks | Design and implement memory systems for companies building AI agents. Deliverable: persistent memory layer with entity tracking, session persistence, and recall optimization. $5K-15K per engagement. |
| Plugin: Memory Backend Adapter | 1-2 weeks | Build a drop-in memory backend adapter for popular agent frameworks (LangChain, CrewAI, AutoGen). Package as pip-installable plugin. $49-99/license for commercial use. |
| Template: PARA Memory Starter Kit | 3-5 days | Pre-configured memory directory structure with YAML schemas, indexing scripts, and consolidation pipeline. Publish on GitHub Marketplace / Gumroad. $29-49 one-time. |
| Training: Agent Memory Course | 4-6 weeks | Video course teaching PARA method for AI agents, entity tracking, recall optimization, and memory consolidation. Hosted on Udemy / Teachable. $199-399 per student. |
| SaaS: Hosted Memory Backend | Ongoing | Cloud-hosted memory service with API, dashboard, and auto-scaling. Free tier up to 100 entities, paid plans from $19/mo for 10K entities with GraphQL query API. |
| Integration: Memory Bridge Plugin | 1-3 weeks | Custom integration that bridges this memory system into a client's existing agent architecture. Includes knowledge graph migration, bulk import, and custom recall endpoints. $3K-8K fixed price. |
## Process

### Preparation
1. Initialize the memory directory structure: `~/.1ai/memory/entities/`, `~/.1ai/memory/relations/`, `~/.1ai/memory/daily/`, `~/.1ai/memory/consolidated/`, `~/.1ai/memory/.archive/`.
2. Create the index file `~/.1ai/memory/index.yaml` with empty entity and relation lists if it does not exist.
3. Set environment variables: `MEMORY_DIR` (default `~/.1ai/memory`), `MAX_ENTITIES` (default 500), `CONSOLIDATION_INTERVAL` (default 24h).
4. Verify read/write access to all directories. If permission errors occur, adjust ownership or fall back to a user-writable location.

### Execution
1. Load the memory index on session start. For each active entity, preload its observations into working memory.
2. Intercept significant actions (file edits, decisions, errors, API calls) and extract structured facts.
3. Write facts to the appropriate entity files atomically. Update relations when a fact connects two entities.
4. Flush the write buffer after every action. If the session is interrupted mid-write, the `.tmp` file is cleaned on next start.
5. Run consolidation every 7 sessions or 24 hours. The 4-tier pipeline promotes frequent patterns to procedural memory.
6. On user query or task context request, execute the recall cascade: exact name → keyword → fuzzy → spreading activation.

### Stewardship
1. Audit memory health weekly: check for orphaned entities (no relations, no observations), broken YAML, and excessive entity count.
2. Prune entities with `importance < 0.2` and no access in 30 days. Move to `.archive/` rather than deleting permanently.
3. Update `index.yaml` after any structural change. Document schema changes in `~/.1ai/memory/SCHEMA.md`.
4. Monitor memory size. If exceeding `MAX_ENTITIES`, force consolidation and archive low-access entities.
5. Back up the entire `~/.1ai/memory/` directory weekly. Use `tar czf` with date-stamped filename to a backup location.
## Verification

- [ ] Memory directory structure exists with all required subdirectories (entities, relations, daily, consolidated)
- [ ] `index.yaml` parses without error and contains expected entity names
- [ ] Atomic write pattern works: concurrent reads see only completed files (no `.tmp` remnants)
- [ ] Entity creation preserves existing observations (merge, not overwrite)
- [ ] Cross-session recall returns entities from prior sessions within configurable time window
- [ ] Weekly consolidation produces a valid YAML summary file
- [ ] Recall cascade finds entities by exact name, keyword, fuzzy match, and spreading activation
- [ ] Memory size stays under MAX_ENTITIES after 7 days of simulated use
- [ ] Backup script runs successfully and produces a readable archive
- [ ] All error paths handled: missing directory, corrupt YAML, disk full, permission denied