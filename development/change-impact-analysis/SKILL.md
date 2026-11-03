---
name: change-impact-analysis
description: Use when performing evidence-backed impact analysis before changing code, data, interfaces, or governance documents, then comparing the planned impact with the actual diff after implementation. Covers call paths, data and schema, API contracts, tests, documentation, ADRs, deployment, migration, and rollback. Use for cross-module or high-risk changes, database migrations, authentication, public interfaces, blast-radius questions, pre-change checks, and post-implementation alignment.
domain: development
subdomain: devsecops
category: development
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- impact-analysis
- risk-assessment
- planning
- change-management
- blast-radius
triggers:
- change impact
- impact analysis
- blast radius
- affected callers
- migration risk
- pre change check
argument-hint: "file_path OR component_name"
---

# Change Impact Analysis

## Overview

Change Impact Analysis is the evidence-first discipline of mapping who and what a code, data, interface, or governance change will affect BEFORE executing it, then reconciling the actual diff against the plan. It prevents production outages, silent contract violations, and irreversible migrations by enforcing read-only dependency discovery (`git grep`, AST queries, import mappings) over intuition, and by attaching rollback steps and verification commands to every change.

Read-only by default. Use git grep, ast_grep, find, and read to map dependencies—never assume directory structures or model intuitions.

## When to Use

**Trigger phrases:**
- "change impact"
- "impact analysis"
- "blast radius"
- "affected callers"
- "migration risk"

Use directly when:
- Planning cross-module, public-interface, or data-migration changes.
- Pre-change: want to know who/what will be affected by a proposed diff.
- Post-change: verify the actual diff matches the planned impact.
- Auditing authentication, API, or schema modifications.
- Assessing rollback feasibility and recovery steps.

## When NOT to Use

- Single-file, low-risk refactors without cross-module dependencies.
- When a targeted linter/formatter check suffices (e.g., unused imports).
- For debugging test failures—use `test-agent` instead.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just make the change and see what breaks." | Unverified changes cause production outages without recovery paths. Plan first, execute second. |
| "The caller will figure it out if their code breaks." | Silent contract violations cascade into data corruption, security gaps, or billing discrepancies. |
| "I can grep the directory name for dependencies." | Directory names are not call signatures. Use `git grep` on function names, AST queries, or import mappings. |
| "This is just a rename, no big deal." | Renames affect imports, routes, API contracts, tests, docs, and ADRs. Map all before renaming. |

## Workflow

### 1. Establish Evidence Sources (Read-Only)

Query authoritative sources for dependency mapping:

```bash
# Callers / imports
git grep -n "import.*from.*${COMPONENT}" -- '*.{py,ts,js}'
ast-grep --pattern "from '$COMPONENT'"  # or JS import/export patterns

# API routes
grep -r "get|post|put|delete.*'/$COMPONENT" -- '*.py'  # FastAPI/Express
grep -r "$COMPONENT:"                 # Diesel/Rust or Rust routers

# Tests
git ls-files | xargs grep -l "test.*$COMPONENT"
```

### 2. Map Impacted Surfaces

| Surface | Evidence Method |
|---|---|
| **Code** | `git grep` for callers, AST for call graphs, import statements |
| **Data** | Schema files, migrations, type definitions, ORM models |
| **Interfaces** | OpenAPI specs, GraphQL schemas, REST route tables |
| **Tests** | `TEST_IDS.md`, pytest markers, Jest test files |
| **Documentation** | ADRs, CHANGELOG, README, internal wiki links |
| **Deployment** | systemd units, Dockerfiles, k8s manifests, CI/CD configs |
| **Rollback** | Migration scripts, backup procedures, revert commands |

### 3. Route to Specialized Skills (Deterministic Dispatch)

| Impact Type | Delegated Skill |
|---|---|
| API contract changes | `api-contract-drift-audit` |
| Database migration | `prisma-migration-ledger-reconcile`, `zero-downtime-migration-audit` |
| Authentication/auth changes | `auth-patterns`, `jwt-token-security` |
| Front-end component change | `frontend-design`, `impeccable` |
| DevOps / deployment | `devops/`, `systemd-deploy-parity-verify` |
| Documentation / ADR | `docs-governance`, `contract-manager` |
| Test strategy | `agent-reach`, `test-agent`, `test-coverage-analyzer` |

### 4. Plan Mitigation Steps

For each impacted surface, identify:
- Owner / reviewer
- Verification command or checklist
- Rollback procedure
- Communication timeline

### 5. Execute & Compare Diff

After changes:

```bash
git diff --stat
git diff HEAD~1 --name-only              # only changed files
git diff HEAD~1 -- '*.{py,ts,js}'          # code only
```

Reconcile planned impacts with actual diff and report:
- Scope drift (missing/added files)
- Unverified consumers
- Unfixed breakages
- Remaining risk

## Verification Checklist

- [ ] Dependency mapping completed via `git grep` or AST queries
- [ ] No inferred dependencies (verified by import paths, not directory names)
- [ ] All impacted test files identified and linked
- [ ] ADR and documentation updates planned/scheduled
- [ ] Rollback procedure documented with exact recovery commands
- [ ] Post-implementation diff matches planned impact (no scope drift)
- [ ] Zero unverified callers/consumers