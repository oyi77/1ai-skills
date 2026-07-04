# 1ai Company OS — Core Rules
> BerkahKarya / 1ai — Single source of truth for all agents and humans.
> Version: 4.0.0 | Updated: 2026-07-04
> **Do not edit copies.** All changes here → auto-synced to 1ai-skills and 1ai-playbook.

---

## Company OS Files

### Identity & Direction

| File | Purpose | Severity |
|------|---------|----------|
| `MISSION.md` | Vision, mission, values, north star metric, non-negotiables | mandatory |
| `OKR.md` | Quarterly objectives, KRs, KPIs, task-to-goal alignment | mandatory |

### People & Authority

| File | Purpose | Severity |
|------|---------|----------|
| `ROLES.md` | Every role (human+agent), L1-L5 authority levels, RACI matrix, domain ownership | mandatory |
| `HIRING.md` | Adding, managing, retiring agents and human collaborators | mandatory |
| `ONBOARDING.md` | First-session checklist for any new agent or human, verification questions | mandatory |

### Operations

| File | Purpose | Severity |
|------|---------|----------|
| `DECISION.md` | Who decides what, approval thresholds, decision log, forbidden decisions | mandatory |
| `COMMS.md` | Communication channels, cadence, escalation path, human notification triggers | mandatory |
| `FINANCE.md` | Budget approval, spending limits per authority level, revenue tracking, invoicing | mandatory |

### Safety & Governance

| File | Purpose | Severity |
|------|---------|----------|
| `ETHICS.md` | Absolute prohibitions, escalation triggers, autonomy boundaries, override conditions | mandatory |
| `INCIDENT.md` | Severity levels (SEV1-4), response protocol, war room, postmortem template | mandatory |
| `SECURITY.md` | Data classification, secrets management, access control, audit trail | mandatory |

---

## Engineering Rules

| File | Purpose | Severity |
|------|---------|----------|
| `RULES.md` | Universal compact rules — one file for ALL models | mandatory |
| `ENGINEERING.md` | Full engineering protocol: ownership, core loop, principles | mandatory |
| `PLAN.md` | Task decomposition: 7 steps before any code | mandatory |
| `PRD.md` | PRD template, atomic issue format, PR description standard | mandatory |
| `GATE.md` | Pre-ship checklist: 15 gates before every commit | mandatory |
| `REVIEWER.md` | Adversarial fresh-context PR review protocol | mandatory |
| `QA.md` | QA scenarios, happy+sad paths, testing protocol | mandatory |
| `VERIFICATION.md` | Receipt and proof enforcement | mandatory |
| `RELEASE.md` | Versioning, changelog, deployment checklist, rollback | mandatory |
| `DOCS.md` | Documentation standards and generation templates | recommended |
| `ANTI-PATTERNS.md` | Growing failure catalog from real incidents | mandatory |
| `SURPASS.md` | Competitive research and surpass framework | recommended |
| `LEARN.md` | Retrospective and rule update protocol | recommended |
| `PROCESS.md` | Core loop: READ→THINK→DECIDE→PLAN→BUILD→VERIFY | mandatory |

---

## Enforcement Chain

```
New agent/human
    └── ONBOARDING.md (9-step checklist + verification questions)

Every task
    ├── RULES.md            (universal laws)
    ├── PLAN.md             (7 steps: understand→research→PRD+issues→
    │                        brainstorm→scope→decompose→risks→confirm)
    ├── OKR.md §5           (which KR does this task advance?)
    └── ETHICS.md           (within autonomy boundaries?)

Building
    ├── ENGINEERING.md      (SOLID, clean code, error handling)
    └── SECURITY.md         (secrets, access control)

Before every commit
    └── GATE.md             (15 gates: intent→codebase→domain→check→
                             tests→real-user→logic→QA→review→lint→
                             security→rollback→diff→docs→agent-review)

Every PR
    ├── PRD.md §4           (PR description template)
    └── REVIEWER.md         (§2.0 prerequisites → §2.1-2.6 full review)

Production deploy
    └── RELEASE.md          (10-gate release checklist + rollback plan)

Incident
    ├── INCIDENT.md         (severity → response → war room → postmortem)
    └── COMMS.md §5         (human notification for SEV1/SEV2)

Decisions
    └── DECISION.md         (authority thresholds + decision log)

Spending
    └── FINANCE.md          (L1-L5 limits + approval process)

Quarterly
    └── OKR.md              (review, score, reset)
```

---

## Sync Architecture

```
~/.1ai/core/           ← SINGLE SOURCE OF TRUTH
    │
    ├── scripts/sync-foundation.sh
    │       │
    │       ├── /projects/1ai-skills/_rules/    (copy — never edit here)
    │       └── /projects/1ai-playbook/rules/   (copy + human-readable INDEX.md)
    │
    └── .git/hooks/post-commit → runs sync-foundation.sh on every commit
```

**To change a rule:** edit in `~/.1ai/core/` → commit → hook auto-syncs both repos.
**Never edit** `1ai-skills/_rules/` or `1ai-playbook/rules/` directly.

---

## Rule Lifecycle

```
1. Identify gap (LEARN.md retrospective, incident postmortem, user feedback)
2. Write/update rule file in core/
3. Bump version in frontmatter
4. Reference from BOOTSTRAP.md if session-type specific
5. Commit → post-commit hook syncs to 1ai-skills + 1ai-playbook
6. Update CHANGELOG.md
```

---

> *Rules are contracts. Agents are employees. Proof is currency.*
