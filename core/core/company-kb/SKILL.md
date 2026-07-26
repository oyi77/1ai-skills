---
name: company-kb
description: company-kb — Company Knowledge Base Skill. Use when relevant to this domain.
domain: core
tags:
- company
- infrastructure
- memory
- self-improvement
version: 1.0.0
---

# Company KB — Quick Reference

**Role:** The Company Knowledge Base (company-kb) stores organization-specific memory — products, services, team members, clients, procedures, and operational history. While the parent `kb` skill manages the PARA structure and general knowledge retrieval, company-kb specializes in entity tracking, company-wide procedures, agent accountability records, and cross-referencing decisions to organizational context. Both agents and humans use this to maintain a single source of truth.

## Quick Start

### 1. Define Company Entities
Register core entities — products, clients, team members, procedures:

```python
import yaml
from pathlib import Path

KB_COMPANY = Path("~/kb/company").expanduser()

def register_entity(entity_type, name, attributes):
    """Register or update a company entity."""
    dir_path = KB_COMPANY / entity_type / name
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / "entity.yaml"
    data = {"name": name, "type": entity_type, **attributes}
    file_path.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))

register_entity("products", "Agent Management Platform", {
    "status": "active", "version": "2.1.0", "team": "Platform",
    "description": "Multi-agent orchestration with MCP support",
})
register_entity("clients", "Acme Corp", {
    "tier": "enterprise", "mrr": 49900, "onboarding_date": "2026-01-15",
    "account_manager": "Alice", "stack": ["notion", "slack", "custom-api"],
})
```

### 2. Record Decisions and Procedures
Capture why decisions were made and how procedures work:

```python
def record_decision(title, context, decision, alternatives, date=None):
    from datetime import date as dt
    entry = {"title": title, "context": context, "decision": decision, "alternatives": alternatives, "date": str(date or dt.today())}
    Path(KB_COMPANY / "decisions" / f"{title.replace(' ', '-').lower()}.yaml").write_text(yaml.dump(entry))

record_decision("Pricing Tier Structure",
    "Needed to differentiate free vs pro features for launch",
    "Pro at $99/mo with unlimited agents, Standard at $49/mo with 5-agent limit",
    ["Single tier at $79/mo", "Usage-based pricing"])
```

### 3. Agent Accountability Log
Track what each agent session accomplished:

```python
import datetime, json

def log_session(agent_id, task, outcome, facts_added=0):
    log = KB_COMPANY / "operations" / "session-log.json"
    logs = json.loads(log.read_text()) if log.exists() else []
    logs.append({"agent": agent_id, "task": task, "outcome": outcome, "facts": facts_added, "ts": datetime.datetime.now().isoformat()})
    log.write_text(json.dumps(logs, indent=2))
```

## One Focused Code Snippet — Quick Entity Lookup

```python
def find_company_info(query, entity_type=None):
    """Search all company entities by name or attribute."""
    results = []
    search_dir = KB_COMPANY / (entity_type or "")
    for f in search_dir.rglob("*.yaml"):
        text = f.read_text().lower()
        if query.lower() in text:
            results.append(f.relative_to(KB_COMPANY))
    return results[:10]
```

## Checklist

- [ ] All product/service entities registered with name, status, version, and owning team
- [ ] Client entities include tier, MRR, onboarding date, and primary contact
- [ ] Decisions recorded with context, alternatives considered, and timestamp
- [ ] Session log tracks agent activity for accountability and audit trails
- [ ] Entity index cross-references related entities (e.g., a client linked to their active products)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Entity tracking is just busywork" | When a client asks about a feature they discussed 3 months ago, a structured entity registry lets you answer in seconds instead of re-reading entire session transcripts. |
| "Decisions are obvious, no need to write them down" | Three months later, the team has no idea why a $99/mo price was chosen over $79. Record context + alternatives or accept re-litigating every decision. |
| "Only engineers need company KB" | Sales needs client history, support needs procedures, operations needs vendor records. A company-wide KB serves every function. Store it where agents AND humans can read it. |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
Use this skill when working with company kb.


## Workflow
See the parent skill for authoritative workflow documentation.
