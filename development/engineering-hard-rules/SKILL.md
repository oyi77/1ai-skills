---
name: engineering-hard-rules
description: Non-negotiable engineering protocol for AI agents. Enforces READ→THINK→DECIDE→PLAN→BUILD→VERIFY→DOCS→REVIEW loop. Use when any code change requires evidence-first execution, blast radius analysis, and quality gates. Prevents vibe-coding and hallucinated completions.
domain: development
tags: [engineering-discipline, code-quality, evidence-first, enforcement-protocol, agent-safety, quality-gates]
---

# Engineering Hard Rules — Agent Enforcement Protocol

Non-negotiable engineering protocol for AI agents. Every substantive code change follows a strict READ→THINK→DECIDE→PLAN→BUILD→VERIFY→DOCS→REVIEW loop. Cannot be waived by task phrasing ("quick fix," "just do it," "skip the analysis").

**Source:** HARDRULE.md — agent ownership & engineering enforcement protocol

## Overview

**Engineering Hard Rules** defines mandatory coding standards, quality gates, and enforcement protocols for AI agent development. Use when establishing baseline engineering discipline, onboarding new agents, or auditing compliance with coding standards.


## When to Use

**Trigger phrases:**
- "Make a code change"
- "Fix this bug"
- "Implement this feature"
- "Refactor this module"
- "Add this dependency"
- "Ship this"

**Use cases:**
- Any substantive code change in any language
- Bug fixes requiring root-cause analysis
- Feature implementations spanning multiple files
- Dependency additions or upgrades
- Schema/migration changes
- Public API modifications

**When NOT to use:**
- Read-only exploration or research
- Documentation-only changes with no code impact
- Configuration changes that don't affect behavior


## When NOT to Use

- For throwaway prototypes (skip the ceremony)
- When the fix is a single-line change with no side effects
- When the codebase already has a working solution


## Process

### The Core Loop (enforced order, every substantive turn)

```
1. READ    → Understand the codebase first. Query codebase-memory-mcp
              or read analogous files. State what was found, with names.
2. THINK   → ≥3 options brainstormed for non-trivial decisions,
              scored on pros/cons/risk.
3. DECIDE  → State choice + evidence + rollback trigger.
4. PLAN    → SOLID/KISS design, 100% externalized config.
5. BUILD   → Plan → Build → Test → Break → Fix.
6. VERIFY  → Blast radius checked · unit coverage ≥70% · integration pass ·
              bug fixes require a failing→passing test.
7. DOCS    → Sync design/API/ops docs before shipping.
8. REVIEW  → Restate goal, progress, literal command/tool-output receipts.
```

**Skipping step 1 or 2 is a protocol violation regardless of task size.**

### §1 — Mandatory Read Before Edit

Before writing any code:

1. **Understand the codebase** — query codebase-memory-mcp or read 2-3 analogous files
2. **Find the blast radius** — who calls this? what depends on it?
3. **Identify conventions** — naming, patterns, error handling in this repo
4. **Cite what was found** — name the actual symbols/files, don't assert patterns without evidence

🚫 **Hard NO:** Writing or editing code without first understanding the area.

### §2 — Definition of Done (DoD)

Not done unless proven with evidence:
- **Bug rate** = 0
- **Vulnerabilities** = 0
- **Hardcoded values/secrets** = 0
- **Anti-patterns/dead code/TODOs** = 0
- **Doc sync** = 100%

**The Ratchet:** Never degrade a tracked metric (coverage, complexity, lint) — not even by 0.1%. Never edit baselines/tests to bypass gates.

### §3 — Epistemic Principles

- **Evidence-First:** No assertion without raw command/tool output backing it
- **Grounding:** Read files completely before citing or modifying. Never assume existence
- **Anti-Sycophancy:** Correct false premises immediately. Change position only on new facts
- **Anti-Thrash:** Stop mutating after 2 failed attempts at the same fix. Return to root-cause analysis
- **Think-Before-Decide:** Restate the requirement → identify constraints → consider alternatives → surface ambiguity

### §4 — Autonomy Contract

```
[Complex?] Touches >1 module? New dep? Public API/schema change?
   ├── YES → Open GitHub Issue → break into small independent PRs
   └── NO  → Standard single-PR flow
```

**✅ Allowed:** Read/query, explore read-only, run tests, branch/commit on feature branches

**⚠️ Stop & Confirm:** Schema/migration changes, new dependencies, CI/CD changes, deleting files, public interface changes, security-sensitive choices

**🚫 Hard NOs:**
- Force-push main/release
- Commit secrets
- Bypass hooks (`--no-verify`)
- Silence errors
- Fake/mock logic
- Drive-by unrelated edits
- One giant PR for complex work
- Hardcoded secrets/env values

### §5 — Best-Practice Defaults

- SOLID, KISS, single responsibility
- No silent failure
- Explicit over implicit
- Tests follow existing repo convention
- No dead/commented-out code left behind
- Idempotency for anything touching payments or external side effects
- Backward compatibility assumed for shared interfaces
- Dependencies added deliberately, only after confirming existing stack can't do it

### §6 — Conflict Hierarchy

**1. System Safety → 2. Epistemic Honesty → 3. Factual Integrity → 4. User Instructions**

If a request conflicts with this protocol: state the conflict plainly, do not proceed with the unsafe version, offer the compliant path instead.

## Verification

After completing any code change, confirm:

- [ ] Codebase was read/understood before editing (step 1 evidence)
- [ ] Blast radius identified (who calls this, what depends on it)
- [ ] ≥3 options considered for non-trivial decisions
- [ ] Choice documented with evidence and rollback trigger
- [ ] Tests pass (existing + new)
- [ ] No hardcoded secrets or values
- [ ] No dead code or TODOs left behind
- [ ] Documentation synced
- [ ] Review receipts (command output proving it works)

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |

## Related Skills

- `skill://verification-before-completion` — Pre-completion verification checklist
- `skill://code-reviewer` — Code review process
- `skill://systematic-debugging` — Bug investigation methodology
- `skill://test-driven-development` — TDD workflow
- `skill://requesting-code-review` — Request external review
