---
name: session-brain
description: Query bk-hub for project context on session start so every session begins with memory instead of starting blind. Use when working with session brain.
domain: core
author: mahipal
license: Apache-2.0
subdomain: core-platform
tags:
- brain
- infrastructure
- memory
- self-improvement
- session
trigger: auto
version: 1.0.0
---
# Session Brain

## When to Use

**Trigger phrases:**
- "session brain"
- "Help me with session brain"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


**Auto-runs on first message of every session.** Queries bk-hub for project context and injects it before responding.


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

Session Brain is the memory bridge that survives agent compaction. Every AI agent session starts with an empty context window — all prior work, decisions, and project state from previous sessions are gone. Session Brain solves this by querying bk-hub (or the brain knowledge graph) at session start, retrieving the most recent project context, and injecting it into the agent's working memory before any user message is processed.

The lifecycle begins when the agent harness fires the first-message hook. Session Brain reads a persistent scratchpad file (`~/.1ai/.session-context.md`) that holds the current step, affected files, architectural decisions, and verification state from the last active session. If the file is fresh (updated within the last 30 minutes), its contents are trusted as ground truth. If stale or missing, Session Brain probes the brain's memory systems — GBrain, MemPalace, and the knowledge graph — to reconstruct context from stored facts, entity relationships, and session embeddings.

After loading context, Session Brain performs a reconciliation check: it compares the loaded project state against the current filesystem and git state. Branch changes, uncommitted edits, and modified lockfiles are surfaced so the agent does not act on stale assumptions. The reconciled context is then formatted as a structured preamble that prepends every agent response for the duration of the session.

Session Brain also handles mid-session compaction events. When the LLM context window is compressed (a compaction event), the preamble and key observations are re-injected automatically. During active work, transition checkpoints write state back to the scratchpad after every significant edit block or todo advancement, ensuring partial progress is not lost if the session terminates unexpectedly.

At session end, Session Brain triggers a brain-save operation that persists the full session summary — what was built, commit hash, key files changed, architectural decisions, test state, and current blockers — into long-term memory (GBrain) with high importance. This ensures the next session can resume from exactly where the last one left off, even across days or weeks of inactivity.
## Architecture

Session Brain operates in four coordinated layers:

- **Hook Layer** — A first-message hook registered with the agent harness (`.claude/hooks/`) fires before any user message is processed. It intercepts session initialization, checks for a live scratchpad, and decides whether to load from disk or query the brain. Runs with a strict timeout so it never delays the first user response by more than a few seconds.
- **Context Loader** — Reads `~/.1ai/.session-context.md` if it exists and is recent (30-minute freshness window). Falls back to querying GBrain/MemPalace via the brain recall/search APIs when the scratchpad is stale or missing. Returns structured context: current step, affected files, pending decisions, and verification state.
- **Reconciliation Engine** — Compares loaded context against live git state (`git branch --show-current`, `git status --porcelain`, `git log -1 --oneline`). Detects branch switches, uncommitted changes, and merge conflicts. Generates delta warnings when disk reality diverges from loaded memory.
- **Persistence Manager** — Writes checkpoint updates to the scratchpad after todo transitions, edit blocks, or explicit save signals. On session end (or brain-save signal), commits the full session summary to GBrain with importance=0.8 for long-term recall.
## Configuration

Session Brain is configured through environment variables and the scratchpad file path:

- `SESSION_CONTEXT_PATH` — Path to the persistent scratchpad file (default: `~/.1ai/.session-context.md`)
- `SCRATCHPAD_FRESHNESS_MINUTES` — Max age of scratchpad before fallback to brain query (default: `30`)
- `BRAIN_IMPORTANCE_LEVEL` — Importance level for end-of-session brain saves (default: `0.8`)
- `BRAIN_TIMEOUT_SECONDS` — Timeout for brain API calls during context recovery (default: `10`)
- `AUTO_SAVE_ON_TODO` — Whether to checkpoint scratchpad on every todo transition (default: `true`)
- `RECONCILE_GIT` — Whether to perform git-state reconciliation on load (default: `true`)
- `COMPACTION_REINJECT` — Whether to re-inject context after a compaction event (default: `true`)
## Integration

Session Brain integrates with the following systems:

- **Agent harness hook system** — Registered as a first-message hook that auto-runs before any user message. Compatible with OMP, Claude Code, and custom agent runners that support lifecycle hooks.
- **bk-hub / GBrain / MemPalace** — Primary sources for long-term memory retrieval. Queries via the brain MCP tools (`xd://mcp__ai_hub_brain_search`, `xd://mcp__ai_hub_brain_recall`, `xd://mcp__ai_hub_brain_remember`). Falls back across backends when one is unavailable.
- **Knowledge graph** — Reads entity relationships and architectural decisions via `xd://mcp__memory_search_nodes` and `xd://mcp__memory_read_graph` for structural project context.
- **Git CLI** — Performs reconciliation via `git branch`, `git status`, `git log` to detect state divergence between memory and reality.
- **Performance monitor** — Exports checkpoint timing and context-load latency metrics for the skill performance monitoring system.
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will remember what I was working on next session" | Agent context is wiped on compaction. Without explicit persistence, every session starts blind. You WILL lose progress. |
| "The scratchpad is just overhead I do not need" | A 30-line scratchpad is the difference between resuming in 2 seconds vs spending 10 minutes reconstructing context from scratch. |
| "I can just read the git log to figure out where I was" | Git log tells you what was committed, not what you were about to do next, what decisions were pending, or what verification half-failed. |
| "Memory compaction does not happen often enough to worry about" | Compaction can happen mid-stream on long conversations. Without re-injection, the agent loses all project context in the middle of a task. |
| "Brain save at session end is optional" | Without an end-of-session brain save, the next agent session has zero memory of this session. You break the chain of continuity permanently. |

## Code Examples

```python
# Example: Session context loader with scratchpad fallback
import os, json, time
from pathlib import Path

SCRATCHPAD_PATH = Path(os.getenv("SESSION_CONTEXT_PATH", "~/.1ai/.session-context.md")).expanduser()
FRESHNESS = int(os.getenv("SCRATCHPAD_FRESHNESS_MINUTES", "30"))

class SessionContext:
    def __init__(self):
        self.step = None
        self.files = []
        self.decisions = {}
        self.verification_state = {}
        self.last_updated = 0

    def load(self) -> dict:
        """Load session context from scratchpad or return empty."""
        if not SCRATCHPAD_PATH.exists():
            return {"status": "no_context", "context": self.__dict__}
        age_minutes = (time.time() - SCRATCHPAD_PATH.stat().st_mtime) / 60
        if age_minutes > FRESHNESS:
            return {"status": "stale", "age_minutes": age_minutes, "context": self.__dict__}
        text = SCRATCHPAD_PATH.read_text()
        return {"status": "fresh", "age_minutes": age_minutes, "preamble": text[:2000]}

    def save_checkpoint(self, step: str, files: list, decisions: dict):
        """Write a checkpoint to the scratchpad file."""
        SCRATCHPAD_PATH.parent.mkdir(parents=True, exist_ok=True)
        content = f"""## Active
- Step: {step}
- Files: {', '.join(files)}
- Decisions: {json.dumps(decisions)}
- Last updated: {time.ctime()}
"""
        SCRATCHPAD_PATH.write_text(content)
        self.last_updated = time.time()
```
## Process

### Preparation
- Verify brain backends are reachable (GBrain, MemPalace, knowledge graph)
- Ensure scratchpad directory exists (`~/.1ai/` writable)
- Set `SESSION_CONTEXT_PATH` to the desired location
- Configure freshness window based on expected session length
- Register the first-message hook with the agent harness

### Execution
- On session start, read scratchpad and check freshness
- If stale or missing, query bk-hub brain search for project context
- Reconcile loaded context against live git state
- Inject reconciled preamble into agent working memory
- On each todo transition or edit block, write checkpoint to scratchpad
- On compaction signal, re-inject preamble
- On session end, save full summary to GBrain with high importance

### Stewardship
- Monitor scratchpad age as a health metric (stale = risk of context loss)
- Periodically verify brain saves are actually persistent (query next session)
- Rotate stale context files when projects change
- Tune freshness window to balance recency vs brain API overhead
## Verification

- [ ] Scratchpad file exists at `SESSION_CONTEXT_PATH` after first checkpoint
- [ ] Context loads fresh scratchpad (under freshness window) with correct step and files
- [ ] Context correctly identifies stale scratchpad (over freshness window) and falls back to brain
- [ ] Git reconciliation detects branch switch and warns about divergence
- [ ] Compaction re-injection actually restores preamble after artificial compaction
- [ ] End-of-session brain save is queryable in next session
- [ ] Multiple concurrent checkpoints do not overwrite each other
- [ ] Brain API timeout does not block session start (graceful degradation)

## Workflow

1. **Session Start Trigger** — Agent harness fires first-message hook. Session Brain intercepts before any user message is processed.
2. **Scratchpad Probe** — Read `~/.1ai/.session-context.md`. Check mtime vs current time. If under freshness window, parse preamble and proceed to step 5.
3. **Brain Fallback** — If scratchpad is stale or missing, call `brain_search()` and `brain_recall()` to retrieve project context from persistent memory. Use broad queries first (project name, recent work topics), then narrow with specific entity names.
4. **State Reconciliation** — Run `git branch --show-current` and `git status --porcelain`. Compare git state against loaded context. Log warnings for branch switches, dirty working tree, or merge conflicts.
5. **Preamble Injection** — Format the loaded context as a structured preamble: current milestone, affected files, key decisions, verification status. Prepend this to the agent's working context.
6. **Active Checkpointing** — After each todo transition, edit block, or explicit save signal, rewrite the scratchpad with updated step, files, and decisions. Keep the file under 50 lines.
7. **Session Termination** — On session end, compose a comprehensive summary (what was built, commit hash, key files, architectural decisions, test state, blockers) and persist to GBrain with importance=0.8. The scratchpad remains on disk for fast resume.

## Common Issues

| Issue | Root Cause | Solution |
|---|---|---|
| Scratchpad shows stale context | Freshness window too long or brain fallback failed | Reduce `SCRATCHPAD_FRESHNESS_MINUTES`; verify brain API reachability |
| Brain save not found next session | Importance level too low or API timeout | Set `BRAIN_IMPORTANCE_LEVEL >= 0.7`; increase `BRAIN_TIMEOUT_SECONDS` |
| Compaction loses preamble | `COMPACTION_REINJECT` disabled or hook not registered | Enable compaction re-injection; verify hook is in `.claude/hooks/` |
| Git reconciliation false positives | Working tree has intentional uncommitted changes (e.g., secrets, build artifacts) | Add patterns to gitignore; set `RECONCILE_GIT=false` if noisy |
| Scratchpad grows too large | Checkpoints accumulate without truncation | Enforce 50-line limit; clean old entries during save |
| Multiple concurrent sessions collide | All sessions share same scratchpad file | Use per-project scratchpad paths: `SESSION_CONTEXT_PATH=~/.1ai/.context-{project}.md` |
| Hook fires but context not injected | Hook timeout shorter than brain query latency | Ensure hook timeout > `BRAIN_TIMEOUT_SECONDS` + 2s buffer |
| Brain API error blocks session start | Missing fallback in hook logic | Ensure all brain calls are wrapped in try/except with empty-context fallback |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Persistent agent workspace as SaaS | 3-6 months | Offer session persistence as a service for enterprise AI agent deployments — agents that remember context across sessions, survive restarts, and bridge team handoffs |
| Custom hook integration consulting | 1-3 months | Integrate Session Brain into existing CI/CD agent pipelines for organizations running Claude Code, OMP, or custom agent harnesses |
| Premium scratchpad analytics | 3-6 months | Track agent session health metrics: context hit rate, checkpoint frequency, compaction recovery rate, and productivity impact reports |
| Managed brain persistence add-on | 2-4 months | Bundle with existing AI agent platforms: agents pay per GBrain save for guaranteed cross-session memory retention with SLA |
| Training & playbooks | 1-2 months | Sell documented patterns for context persistence, compaction survival, and cross-session bridging for teams adopting AI coding agents |
| Knowledge graph enrichment pipeline | 4-8 months | Automatically extract entity relationships from session checkpoints into a shared knowledge graph for team-wide agent context sharing |