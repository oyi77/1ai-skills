# Learning Lifecycle — Knowledge Without Memory Pollution

## Problem Statement

AI agents in the 1ai-skills ecosystem operate across sessions. Each session discovers
patterns, conventions, and fixes. If every observation persisted indefinitely, the
knowledge store would accumulate noise, contradictory facts, and stale context —
**memory pollution**.

This document defines a lifecycle for durable knowledge that balances retention with
relevance.

## Learning Mechanisms

The ecosystem supports four learning mechanisms, each with a distinct scope and decay:

| Mechanism | Scope | Persistence | Decay | Use Case |
|-----------|-------|-------------|-------|----------|
| **`learn` tool** | Session → durable lesson | ~permanent | None; manual retirement only | Non-obvious fixes, project conventions, workflows |
| **Session context** (`.session-context.md`) | Active session | ~minutes to hours | File age check (>30 min = stale) | Work-in-progress state across compactions |
| **Auto-learner** (skill) | Cross-session pattern extraction | Long-term | Implicit (new patterns override old) | Repeated execution patterns from skill usage |
| **Brain save** (`vilona_brain_remember`/`learn`) | Project-level memory | ~permanent | Importance-weighted priority | Commit summaries, architectural decisions |

## The Learning Lifecycle

```
Session event
    │
    ▼
┌──────────────┐
│  Observe     │ ← Context: fix a bug, discover a pattern, learn a convention
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Filter      │ ← Is it durable? Non-obvious? Reusable? → YES → persist
└──────┬───────┘                                      │
       │ NO                                            │
       ▼                                              ▼
  (discard)                                    ┌──────────────┐
                                               │  Learn       │ ← Write via learn tool or brain save
                                               └──────┬───────┘
                                                      │
                                                      ▼
                                          ┌──────────────────────┐
                                          │  Memory Store        │ ← gbrain, mempalace, managed skills
                                          │  (importance-weighted)│
                                          └──────┬───────────────┘
                                                 │
                                                 ▼
                                          ┌──────────────────────┐
                                          │  Review & Consolidate│ ← After N sessions: merge, deduplicate,
                                          │                       │   deprecate stale facts
                                          └──────┬───────────────┘
                                                 │
                                          ┌──────┴───────┐
                                          │              │
                                          ▼              ▼
                                   ┌──────────┐  ┌──────────┐
                                   │ Retain   │  │ Retire   │ ← Manual removal, or
                                   └──────────┘  └──────────┘   fact no longer referenced
```

## Filter Criteria — What to Learn

Only persist an observation if it passes ALL criteria:

1. **Non-obvious** — Could not be inferred from existing documentation or code
2. **Reusable** — Will apply to future work, not a one-off context
3. **Durable** — Not expected to change with the next code change
4. **Self-contained** — Stands alone without heavy surrounding context

### Examples

| Observation | Pass? | Reason |
|------------|-------|--------|
| "OMP loads CJS hook files as extensions when named .js" | ✅ PASS | Non-obvious, reusable, durable, self-contained |
| "User prefers tabs over spaces" | ✅ PASS | Non-obvious convention, applies across sessions |
| "This specific line had a typo (fixed now)" | ❌ FAIL | Fixed — no reuse value |
| "The weather was hot during debugging" | ❌ FAIL | Irrelevant to future work |
| "We tried approach A then B then C" | ❌ FAIL | Outcome matters, not the discarded attempts |

## Anti-Patterns — Memory Pollution

| ❌ Anti-Pattern | Why It's Pollution | ✅ Alternative |
|----------------|-------------------|---------------|
| Learning every commit message | Floods the store with transient metadata | Learn only architectural decisions and non-obvious bugs |
| Re-learning the same fact every session | Redundant; indicates missing consolidation | Consolidate related facts into one durable entry |
| Learning raw logs or error output | Noise with no actionable signal | Learn the root cause and fix pattern, not the error text |
| Learning "how to use X tool" for standard tools | Covered by tool docs and existing skills | Reference the skill:// URL instead |
| Learning transient config values | Will change next deploy | Learn the config location and format, not the value |
| Learning session timestamps/iterations | Metadata with no reuse | Learn only the outcome and key decision |

## Retention Policy

| Fact Type | Suggested Retention | Review Cadence |
|-----------|-------------------|----------------|
| Bug fix pattern | 6 months | Re-verify when related code changes |
| Project convention | Permanent | Annual audit |
| Architecture decision | Permanent | Reference in ADR |
| Tool quirk/workaround | 3 months | May be fixed in tool update |
| User preference | Until user changes it | Ask periodically |

## Implementation

### In Agent Sessions

```python
# Good: non-obvious, reusable fact
learn("export const is allowed; module.exports = fn causes factory error in OMP extensions")

# Bad: transient state
learn("Fixed line 42's typo in validate.py")
```

### In Skill Content

Skills should reference this lifecycle in their "Learning" or "Cross-Session"
sections to guide agents on what to persist:

```yaml
# In SKILL.md
learning_guidance:
  persist_when: "discovering a new bypass or workaround not documented anywhere"
  ignore_when: "routine execution with no surprises"
```

### In CI

The `auto-learner` meta-skill enforces:
- Deduplication checks before persisting
- Importance weighting (0.0–1.0)
- Age-based decay for facts below 0.5 importance

## Privacy

- Learning must never capture PII, credentials, or user-identifying data
- The `learn` tool stores lessons in the agent's local memory, not in shared stores
- Before persisting, filter any sensitive content from the lesson
- See `SECURITY.md` for reporting accidental exposure

## Historical Context

This document was created as Phase 13 of the 1ai-skills quality upgrade plan (v3.30.0).
Before this phase, the learning lifecycle was implicit — agents relied on the `learn` tool
and brain saves without systematic retention guidance.
