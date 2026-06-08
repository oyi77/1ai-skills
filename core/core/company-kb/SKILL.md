---
name: company-kb
description: company-kb — Company Knowledge Base Skill. Use when relevant to this
  domain.
persona:
  name: Domain Expert
  title: Master of Company Kb
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
domain: core
---
# company-kb — Company Knowledge Base Skill

## Description
Read, search, and write BerkahKarya company knowledge files. Uses ChromaDB semantic search (748 chunks indexed by BER-50) and direct file access to `company-knowledge/`.

## When to Use
- User asks about company info, procedures, history, products, team
- Agent needs to look up internal documentation
- Storing new company knowledge for future recall
- Paijo asks about anything related to BerkahKarya operations

## Commands
| Command | Description |
|---------|-------------|
| `status` | Check current state and health |
| `run` | Execute the primary operation |
| `list` | Show available items or resources |
| `help` | Display usage information |


### Search (semantic)
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/company-kb/scripts/kb.py search "<query>"
```
Queries ChromaDB `company-knowledge` collection (748 chunks). Returns top 5 results with scores and source references.

### Read a file
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/company-kb/scripts/kb.py read <relative-path>
```
Reads a file from `company-knowledge/` directory.

### List all files
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/company-kb/scripts/kb.py list
```

### Write / Update a file
```bash
python3 ~/.openclaw/workspace/skills/1ai-skills/core/company-kb/scripts/kb.py write <relative-path> "<content>"
```
Creates or updates a file in `company-knowledge/`. Use PARA structure: `projects/`, `areas/`, `resources/`, `archives/`.

## Configuration
- **ChromaDB path**: `~/.openclaw/chroma_db/`
- **Collection**: `company-knowledge` (748 chunks)
- **KB files**: `~/.openclaw/workspace/company-knowledge/`
- **Dependency**: `chromadb` Python package (v1.5.1 installed)

## PARA Structure for New Files
```
company-knowledge/
├── projects/    ← Active projects (JENDRALBOT, trading, etc.)
├── areas/       ← Ongoing responsibilities (marketing, trading, ops)
├── resources/   ← Reference material (products, team, procedures)
└── archives/    ← Completed/inactive items
```

## Examples

```bash
# Search for product info
python3 .../kb.py search "JENDRALBOT affiliate products"

# Search for team info
python3 .../kb.py search "Nuno trading strategy XAUUSD"

# Read a specific file
python3 .../kb.py read resources/products.md

# List all files
python3 .../kb.py list

# Write new knowledge
python3 .../kb.py write resources/team.md "# Team\n\n- Paijo: CEO/Engineer\n- Nuno: Trading\n- Sony: Ops\n- Veris: Marketing"
```

## Notes
- Local OpenClaw accesses files directly via this skill
- Cloud OpenClaw will use Knowledge API (separate task, BER-52+)
- ChromaDB re-indexing: Run BER-50 indexer after writing new files

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

