---
name: kb-memory
description: Knowledge base and memory system for AI agents. Covers company KB, persistent memory, session recall, and brain architecture for context preservation.
domain: core
author: oyi77
license: Apache-2.0
subdomain: ai-infrastructure
tags:
- knowledge-base
- memory
- context
- persistence
- recall
- brain
version: 2.0.0
---

# KB-Memory: Knowledge Base & Memory System

Unified skill for agent knowledge persistence and recall. Covers four approaches to maintaining context across sessions.

## Approaches

| Approach | Purpose | Reference |
|----------|---------|-----------|
| **KB** — Static knowledge base | Reference docs, policies, permanent facts | [reference/approach/kb.md](./reference/approach/kb.md) |
| **Company KB** — Organization wiki | Team docs, product info, internal guides | [reference/approach/company-kb.md](./reference/approach/company-kb.md) |
| **Memory System** — Persistent agent memory | Cross-session recall, user preferences | [reference/approach/memory.md](./reference/approach/memory.md) |
| **Session Brain** — Session context | Current conversation state, working memory | [reference/approach/session-brain.md](./reference/approach/session-brain.md) |

## How They Fit Together

```
Permanent ←──────────────────────────────────→ Ephemeral
    │                                              │
  Company KB          Memory System          Session Brain
  (team wiki)      (cross-session facts)    (current conv)
    │                                              │
    └── Both backed by KB (base reference docs) ───┘
```

- **KB** — Foundation. Static reference material that doesn't change.
- **Company KB** — Organization-specific information.
- **Memory System** — Learned facts about user, projects, and preferences.
- **Session Brain** — Working memory for the current task.
