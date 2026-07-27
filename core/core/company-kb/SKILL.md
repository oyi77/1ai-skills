---
name: company-kb
description: company-kb — Company Knowledge Base Skill. Use when relevant to this domain.
domain: core
author: mahipal
license: Apache-2.0
subdomain: core-platform
tags:
- company
- infrastructure
- memory
- self-improvement
- collaboration
- privacy
- brain-integration
version: 2.0.0
---

# Company KB — Quick Reference

**Role:** The Company Knowledge Base (company-kb) stores organization-specific memory — products, services, team members, clients, procedures, and operational history. While the parent `kb` skill manages the PARA structure and general knowledge retrieval, company-kb specializes in entity tracking, company-wide procedures, agent accountability records, and cross-referencing decisions to organizational context. Both agents and humans use this to maintain a single source of truth.

## Organization Structure

Maintain a consistent directory layout so every agent and human can navigate without guessing:

```
~/kb/company/
├── products/              # Products and services (one dir per product)
│   └── agent-platform/entity.yaml
├── clients/               # Client accounts, contacts, contracts
├── team/                  # Team members, roles, skills
├── decisions/             # ADRs and policy decisions with rationale
├── operations/            # Session logs, runbooks, monitoring configs
├── vendors/               # Third-party tools, services, contracts
├── procedures/            # Step-by-step SOPs for recurring tasks
├── projects/              # Active and completed project records
└── index.yaml             # Cross-entity references and tag index
```

This layout is **not mandatory** — adapt to your org. What matters is predictability: every agent should be able to infer where a new entity lives without asking.

### Entity File Convention

Each `entity.yaml` follows a minimal schema:

```yaml
name: Agent Management Platform
type: product
status: active
version: 2.1.0
team: Platform
tags: [orchestration, mcp, agents]
links:                # Cross-references to other entities
  - type: client
    name: Acme Corp
    relation: deployed_at
  - type: decision
    name: pricing-tier-structure
    relation: informed_by
created: 2026-01-10
updated: 2026-03-22
```

Use the `links` field to build an entity graph. An agent reading about Acme Corp can immediately discover which products are deployed there and what pricing decisions affected them.

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
    entry = {"title": title, "context": context, "decision": decision,
             "alternatives": alternatives, "date": str(date or dt.today())}
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
    logs.append({"agent": agent_id, "task": task, "outcome": outcome,
                 "facts": facts_added, "ts": datetime.datetime.now().isoformat()})
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

## Multi-Agent Collaboration Patterns

When multiple agents share the company KB, low-level races are rare (writes are additive), but **read-before-write** violations happen. Use a simple lock convention for destructive operations:

```python
import fcntl, os

LOCK_FILE = KB_COMPANY / ".entity.lock"

def update_entity(entity_type, name, transform_fn):
    """Apply a transformation to an entity under file lock."""
    file_path = KB_COMPANY / entity_type / name / "entity.yaml"
    with open(LOCK_FILE, "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            data = yaml.safe_load(file_path.read_text()) if file_path.exists() else {}
            new_data = transform_fn(data)
            file_path.write_text(yaml.dump(new_data, default_flow_style=False, sort_keys=False))
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)

def add_link(source_type, source_name, target_type, target_name, relation):
    """Atomically add a cross-entity link."""
    def _add(data):
        links = data.get("links", [])
        links.append({"type": target_type, "name": target_name, "relation": relation})
        data["links"] = links
        data["updated"] = str(datetime.date.today())
        return data
    update_entity(source_type, source_name, _add)
```

**Naming convention for agent IDs** in session logs — use `<role>/<session-hash>` so humans can trace which agent type performed what:

```bash
# Example session log entries
{"agent": "deploy-platform/20260322-a1b2", "task": "release v2.2.0", ...}
{"agent": "support-oncall/20260322-c3d4", "task": "investigate client timeout", ...}
```

## Cross-Project Memory Sharing via Entity Linking

The `links` field in every entity.yaml creates a **navigable entity graph** across projects. An agent working on project Alpha can discover related entities in project Beta through shared references. Build automated link inference:

```python
def auto_link_entities(entity_type, name):
    """Scan entity attributes and auto-create links to matching entities."""
    file_path = KB_COMPANY / entity_type / name / "entity.yaml"
    if not file_path.exists():
        return
    data = yaml.safe_load(file_path.read_text())
    text = yaml.dump(data).lower()
    existing_links = {(l["type"], l["name"]) for l in data.get("links", [])}

    # Scan all entity dirs for name matches in attribute text
    for etype_dir in KB_COMPANY.iterdir():
        if not etype_dir.is_dir() or etype_dir.name == entity_type:
            continue
        for ent_dir in etype_dir.iterdir():
            ef = ent_dir / "entity.yaml"
            if not ef.exists():
                continue
            ent_name = ent_dir.name
            if (etype_dir.name, ent_name) in existing_links:
                continue
            # Check if this entity's name appears in the source entity's text
            if ent_name.lower() in text:
                add_link(entity_type, name, etype_dir.name, ent_name, "references")
```

Run this after bulk imports or periodic index rebuilds. The resulting graph lets agents answer queries like "which clients are affected by the pricing change?" by traversing link chains.

### Graph Traversal Example

```python
def traverse_links(start_type, start_name, max_depth=3):
    """BFS traversal of the entity link graph."""
    visited = set()
    queue = [(start_type, start_name, 0)]
    while queue:
        etype, ename, depth = queue.pop(0)
        key = (etype, ename)
        if key in visited or depth > max_depth:
            continue
        visited.add(key)
        yield (etype, ename, depth)
        file_path = KB_COMPANY / etype / ename / "entity.yaml"
        if not file_path.exists():
            continue
        data = yaml.safe_load(file_path.read_text())
        for link in data.get("links", []):
            queue.append((link["type"], link["name"], depth + 1))
```

## Privacy Considerations and Access Boundaries

Not every entity belongs in a shared KB. Define clear boundaries:

| Data Class | Store in company-kb? | Example |
|---|---|---|
| Public/product info | Yes | Features, pricing, team roles |
| Client metadata | Yes | Tier, stack, account manager |
| Client PII | **No** — use encrypted vault | SSN, credit cards, personal addresses |
| Credentials/secrets | **Never** — use Vault or env | API keys, passwords, tokens |
| Internal procedures | Yes | Release checklists, escalation paths |
| HR records | **No** | Salary, performance reviews |
| Session logs (agents) | Yes, sanitized | Task + outcome, no raw data dumps |

**Access boundary enforcement:**

```python
PRIVACY_TYPES = {"team", "vendors"}

def can_access(entity_type, viewer_role):
    """Check if a viewer role can access an entity type."""
    if entity_type in PRIVACY_TYPES:
        return viewer_role in {"admin", "manager"}
    return True

def register_entity_safe(entity_type, name, attributes, viewer_role="agent"):
    if not can_access(entity_type, viewer_role):
        raise PermissionError(f"{viewer_role} cannot write {entity_type} entities")
    return register_entity(entity_type, name, attributes)
```

When writing session logs, **strip sensitive fields** before persisting:

```python
def sanitize_log(entry):
    """Remove sensitive keys from a log entry before writing."""
    SENSITIVE_KEYS = {"api_key", "password", "token", "secret", "session_cookie"}
    if isinstance(entry, dict):
        return {k: sanitize_log(v) for k, v in entry.items()
                if k.lower() not in SENSITIVE_KEYS}
    if isinstance(entry, list):
        return [sanitize_log(item) for item in entry]
    return entry
```

## Integration with 1ai-Hub Brain

For agents operating in the 1ai-hub ecosystem, push critical entity changes to the brain for cross-session recall:

```python
def remember_entity_change(entity_type, name, change_summary, importance=0.6):
    """Push entity changes to 1ai-hub brain for cross-session awareness."""
    import subprocess, json
    payload = {
        "content": f"Company KB update: {entity_type}/{name} — {change_summary}",
        "category": "company-kb",
        "importance": importance
    }
    # Via hub brain_remember MCP tool
    subprocess.run([
        "bash", "-c",
        f'echo \'{json.dumps(payload)}\' | xargs -I{{}} '
        f'claude mcp brain_remember {{}}'
    ], capture_output=True)
```

**Search the brain for stale entity references before creating new ones:**

```bash
# Search brain for existing entity context
xd://mcp__ai_hub_brain_brain_search \
  query="Acme Corp deployment status" \
  service="gbrain"
```

This prevents duplicate entities and catches cross-project references that local YAML files would miss.

## Team Scenario — Real-World Workflow

**Scenario:** Support agent "Alice" encounters a client timeout. She needs to know the client's tier, what products they use, and whether there's a known incident.

```python
def triage_client(client_name, symptom):
    """Gather context for client support triage."""
    # 1. Load client entity
    client_path = KB_COMPANY / "clients" / client_name / "entity.yaml"
    if not client_path.exists():
        print(f"Unknown client: {client_name}")
        return

    client = yaml.safe_load(client_path.read_text())
    print(f"Client: {client['name']} ({client.get('tier', 'unknown')})")

    # 2. Traverse links to find products and decisions
    for link in client.get("links", []):
        linked_path = KB_COMPANY / link["type"] / link["name"] / "entity.yaml"
        if linked_path.exists():
            linked = yaml.safe_load(linked_path.read_text())
            print(f"  {link['relation']}: {link['name']} (v{linked.get('version', '?')})")

    # 3. Check operations log for recent incidents mentioning this client
    log_path = KB_COMPANY / "operations" / "session-log.json"
    if log_path.exists():
        import json
        logs = json.loads(log_path.read_text())
        recent = [e for e in logs[-50:] if client_name.lower() in e.get("task", "").lower()]
        for entry in recent:
            print(f"  Recent: {entry['task']} → {entry['outcome']}")
```

Run this during intake — 3 seconds of structured lookup replaces 15 minutes of hunting through chat transcripts.

## Checklist

- [ ] All product/service entities registered with name, status, version, and owning team
- [ ] Client entities include tier, MRR, onboarding date, and primary contact
- [ ] Decisions recorded with context, alternatives considered, and timestamp
- [ ] Session log tracks agent activity for accountability and audit trails
- [ ] Entity index cross-references related entities (e.g., a client linked to their active products)
- [ ] File lock convention used for concurrent agent writes to the same entity
- [ ] Sensitive data never written to YAML entities (use vault/encrypted store instead)
- [ ] Privacy boundaries enforced for team/vendor/procedure entity types
- [ ] Cross-project links maintained via `links` field; auto-linker run after batch imports
- [ ] Critical entity changes pushed to 1ai-hub brain for cross-session recall

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Entity tracking is just busywork" | When a client asks about a feature they discussed 3 months ago, a structured entity registry lets you answer in seconds instead of re-reading entire session transcripts. |
| "Decisions are obvious, no need to write them down" | Three months later, the team has no idea why a $99/mo price was chosen over $79. Record context + alternatives or accept re-litigating every decision. |
| "Only engineers need company KB" | Sales needs client history, support needs procedures, operations needs vendor records. A company-wide KB serves every function. Store it where agents AND humans can read it. |
| "My agents all run in sequence, no lock needed" | Even sequential agents race on stale read-before-write. A file lock costs microseconds and prevents corrupted entity files that take hours to untangle. |
| "I'll just keep this in my head / chat logs" | Human memory fades after 48 hours. Chat logs are unstructured and buried. A YAML entity is searchable, parseable, and survives session restarts. |
| "Privacy is someone else's problem" | PII in a shared YAML file is a data breach waiting to happen. Classify every field before writing and never assume the consumer has authorized access. |

## When to Use
Use this skill when working with company kb.

## Workflow
See the parent skill for authoritative workflow documentation.
