---
name: kb
description: Query and maintain the knowledge base for project context, decisions, and architecture documentation. Use on
  session start.
domain: core
tags:
- infrastructure
- memory
- self-improvement
persona:
  name: Domain Expert
  title: Master of Kb
  expertise:
  - Core Excellence
  - Best Practices
  - Professional Standards
  philosophy: Excellence is not a skill, it's an attitude.
  credentials:
  - Industry leader
  - Practiced professional
  - Thought leader
  principles:
  - Quality first
  - Continuous improvement
  - Evidence-based
  - Customer focused
---
# KB — BerkahKarya Knowledge Base Skill

**Purpose:** Read, search, and write files in `company-knowledge/` with ChromaDB semantic search.

## When to Use

Use this skill when:
- Searching company knowledge (strategies, playbooks, finance, trading, marketing)
- Reading specific knowledge files (e.g. `areas/finance/cashflow-tracker.md`)
- Writing new or updated knowledge entries to the KB with PARA structure
- Any agent (Vilona, Paijo via Telegram) needs to query or update company context

## Commands
| Command | Description |
|---------|-------------|
| `status` | Check current state and health |
| `run` | Execute the primary operation |
| `list` | Show available items or resources |
| `help` | Display usage information |


### Search (Semantic)
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py search "<query>"
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py search "<query>" --limit 10
```
Queries the ChromaDB `company-knowledge` collection (748 chunks indexed by BER-50).

### Read
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py read "areas/finance/cashflow-tracker.md"
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py read "resources/founder-context.md"
```
Reads file from `company-knowledge/` on disk. Falls back to ChromaDB chunks if file not found locally.

### Write
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py write "areas/marketing/new-strategy.md" "# Strategy\n\ncontent here"
# Or from stdin:
cat content.md | python3 .../kb.py write "areas/finance/status.md" -
```
Writes/updates a file in `company-knowledge/`. Warns if path doesn't follow PARA structure.
After writing, re-run the ChromaDB indexer to make the file searchable.

### List
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py list
python3 ~/.openclaw/workspace/skills/1ai-skills/core/kb/scripts/kb.py list "areas/finance"
```
Lists files on disk. Falls back to ChromaDB indexed paths if directory is empty.

## PARA Structure

All knowledge files should be placed under:
```
company-knowledge/
├── projects/     ← Active time-bound projects
├── areas/        ← Ongoing areas of responsibility
│   ├── content/
│   ├── finance/
│   ├── marketing/
│   ├── operations/
│   └── trading/
├── resources/    ← Reference material, playbooks, guides
│   ├── playbooks/
│   ├── tool-guides/
│   └── vilona-operating-principles.md
└── archives/     ← Completed or inactive material
```

## ChromaDB Details

- **Collection:** `company-knowledge`
- **Path:** `~/.openclaw/chroma_db/`
- **Chunks indexed:** 748 (as of BER-50)
- **Dep:** ChromaDB indexer (BER-50) must be running to re-index new files

## Indexed Files (as of BER-50)

Key files available for search:
- `areas/finance/cashflow-tracker.md`, `crisis-status-latest.md`, `emergency-protocol.md`
- `areas/marketing/jendralbot-strategy.md`, `competitor-analysis.md`
- `areas/trading/quant-backtest-report.md`, `quant-final-report.md`
- `resources/founder-context.md`, `company-lessons-learned.md`
- `resources/playbooks/` — execution plans, cron schedules, strategies

## Usage Pattern in Agent Context

```python
# In SKILL.md or agent context — search and read pattern:

# 1. Search for relevant context
# kb search "cashflow crisis protocol"
# → returns top chunks with file paths and snippets

# 2. Read the specific file for full content
# kb read "areas/finance/emergency-protocol.md"
# → returns full markdown content

# 3. Write updates after decisions
# kb write "areas/finance/crisis-status-latest.md" "<updated content>"
```

## Notes

- Local OpenClaw accesses files directly via this skill
- Cloud OpenClaw uses the Knowledge API (separate BER task)
- Re-index after writes: run the ChromaDB indexer script (BER-50)

## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
