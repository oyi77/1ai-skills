---
name: docs-governance
description: Use when governing repository documentation lifecycle — classifying docs by artifact role (README, ADR, CHANGELOG, SPEC, RUNBOOK), routing new docs to canonical locations, auditing staleness and orphan pages, enforcing doc-code parity on releases, or resolving duplicate/conflicting documentation across a monorepo.
domain: development
subdomain: documentation
category: development
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- documentation
- governance
- adr
- changelog
- monorepo
- staleness
triggers:
- docs governance
- documentation audit
- adr process
- changelog policy
- orphan docs
- doc code parity
argument-hint: "[audit | classify | route]"
---

# Docs Governance

## Overview

Documentation is infrastructure, not decoration. Ungoverned docs rot silently, contradict code, mislead agents, and multiply into duplicates across monorepos. This skill establishes artifact-role classification, canonical routing, staleness audits, and doc-code parity gates.

## When to Use

**Trigger phrases:**
- "docs governance", "documentation audit", "doc code parity"
- "adr process", "changelog policy", "orphan docs"

Use directly when:
- Auditing a repo's documentation surface for staleness, duplication, or contradiction.
- Routing a new document to its canonical location and role.
- Enforcing docs updates as part of release gates.
- Resolving conflicting versions of the same guidance (e.g., three READMEs saying different things).
- Onboarding agents to a monorepo with unclear doc ownership.

## When NOT to Use

- Writing the actual content of a doc → use `agent-docs` or `writing` skills.
- Generating API reference from code comments → language-native tools (Sphinx, TypeDoc, JSDoc).
- Single-file typo fixes.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Docs don't affect runtime, low priority." | Stale docs actively harm: agents follow wrong instructions, humans waste hours, onboarding doubles in cost. |
| "We'll clean up docs later." | Later never arrives. Attach doc updates to the same PR as the code change they describe. |
| "More docs is better." | Duplicate docs are worse than none—they disagree. One canonical source per topic, links everywhere else. |
| "The wiki is our docs home." | Wikis drift outside git review. Durable decisions belong in-repo where diffs and blame work. |

## Workflow

### 1. Artifact-Role Classification

Every document serves exactly ONE role. Classify before placing:

| Role | Canonical Location | Purpose | Update Trigger |
|---|---|---|---|
| **README** | `<component>/README.md` | What it is, how to run, entry points | Structure/setup change |
| **ADR** | `docs/adr/NNNN-title.md` | Hard-to-reverse decision + rationale | Architecture decision |
| **CHANGELOG** | `CHANGELOG.md` | User-visible changes, dated entries | Every release |
| **SPEC / PLAN** | `docs/specs/` or issue-linked | Required behavior before implementation | Feature kickoff |
| **RUNBOOK** | `docs/runbooks/<service>.md` | Operational procedures, incident steps | Infra/process change |
| **CONTRACT** | `docs/contracts/` or OpenAPI/proto | Interface guarantees between systems | API/schema change |
| **REFERENCE** | Generated from code (docstrings) | Symbol-level API details | Code change (auto) |
| **GUIDE / TUTORIAL** | `docs/guides/` | Task-oriented walkthroughs | User-facing workflow change |

Rule: if a doc fits no role, it is either a duplicate (merge it) or misplaced (reclassify it).

### 2. Monorepo Routing Table

For multi-package repos, establish ownership:

```text
repo/
├── README.md              # root: what the repo is, index of packages
├── AGENTS.md              # agent-facing conventions (already enforced here)
├── CHANGELOG.md           # root: cross-package releases only
├── docs/
│   ├── adr/               # repo-wide architecture decisions
│   ├── contracts/         # cross-service interfaces
│   └── guides/            # cross-cutting tutorials
└── packages/
    ├── foo/
    │   ├── README.md      # package-local: setup, usage
    │   └── CHANGELOG.md   # package-local releases
    └── bar/
        └── ...
```

Package docs stay with the package. Root docs cover only what spans packages. Never duplicate content across levels—link instead.

### 3. Staleness Audit

Detect decay signals:

```bash
# docs older than code they describe
find docs/ -name '*.md' -mtime +180 | while read d; do
  echo "STALE? $d ($(stat -c %y "$d" | cut -d' ' -f1))"
done

# docs referencing deleted files/symbols
grep -roh '\b[a-z_][a-z0-9_/]*\.\(py\|ts\|js\|go\)\b' docs/ | sort -u | \
  while read ref; do [ -e "$ref" ] || echo "ORPHAN REF: $ref"; done

# TODO/FIXME markers left in shipped docs
grep -rn 'TODO\|FIXME\|WIP\|placeholder' docs/ */README.md
```

Output a triage table: path, age, signal, owner, action (update/archive/delete/rewrite).

### 4. Doc-Code Parity Gate

Attach to release workflow:

1. Diff touched source files against referenced docs.
2. Any changed public symbol, endpoint, config key, or CLI flag MUST have a corresponding doc update in the same commit range.
3. Blocking check:

```bash
# changed endpoints without openapi/doc update
changed_routes=$(git diff HEAD~1 --name-only -- 'src/**/routes*' 'src/**/api*')
for r in $changed_routes; do
  git diff HEAD~1 --name-only -- 'docs/' 'openapi.json' | grep -q . || \
    { echo "PARITY FAIL: $r changed but no doc update"; exit 1; }
done
```

### 5. Deduplication Sweep

When multiple docs cover one topic:

1. Pick the canonical owner by role table (§1).
2. Merge unique content INTO canonical.
3. Replace losers with one-line pointer: `See [docs/adr/0007](../adr/0007-hmac-v2.md)`.
4. Record the merge in CHANGELOG under `docs:` entries.

## Verification

- [ ] Every doc classified to exactly one artifact role
- [ ] Zero duplicate topics across roles/levels (pointers replace copies)
- [ ] Staleness audit run; aged/orphan docs triaged with owners
- [ ] Release gate blocks doc-code drift
- [ ] ADR numbering contiguous, statuses accurate (accepted/superseded)
- [ ] CHANGELOG covers all user-visible changes since last release
- [ ] Root vs package doc boundaries respected in monorepo layout