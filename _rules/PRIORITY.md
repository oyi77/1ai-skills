---
name: priority
version: 1.0.0
severity: mandatory
scope: [all]
pairs-with: [registry, engineering, gate]
description: Rule conflict resolution framework — deterministic priority hierarchy when rules disagree
---

# PRIORITY.md — Rule Conflict Resolution

> **No ambiguity, no "it depends."** When two rules disagree, this file decides.
> Every rule file in `core/` has a frontmatter priority. Lower number = higher urgency.
> Conflict resolution is deterministic — same inputs always produce the same winner.

---

## §1 — Priority Bands

Every rule file in `core/*.md` is assigned to one of five priority bands in its frontmatter.
The bands define the **urgency tier** of the rule.

| Band | Range     | Category            | Examples                                       |
|------|-----------|---------------------|------------------------------------------------|
| P0   | 01 — 20   | Foundation           | RULES.md (05), ENGINEERING.md (10), VERIFICATION.md (15), GATE.md (20) |
| P1   | 21 — 40   | Safety & Security    | SECURITY.md (25), INCIDENT.md (30), ETHICS.md (35), DATA.md (40)       |
| P2   | 41 — 60   | Product & Compliance | PRD.md (45), RELEASE.md (50), COMPLIANCE.md (55), FINANCE.md (60)      |
| P3   | 61 — 80   | Quality & Docs       | QA.md (65), PERFORMANCE.md (70), DOCS.md (75), LEARN.md (80)           |
| P4   | 81 — 100  | Aspirational         | SURPASS.md (90), DOC_TEMPLATES.md (95)                                 |

> **Full catalog:** `docs/REGISTRY.md` maintains the complete list of every rule file, its priority number, version, and scope.

**Semantics:**
- **P0 (01-20):** Integrity and process — DON'T LIE, CODE MUST RUN, GATE.md checklist. Never violated. Trumps everything.
- **P1 (21-40):** Safety and security — incident response, data protection, ethical boundaries. Trumps product and quality concerns.
- **P2 (41-60):** Shipping and compliance — PRD discipline, release process, regulatory requirements. Must be satisfied before quality polish.
- **P3 (61-80):** Quality and performance — QA thoroughness, performance optimization, documentation completeness. Applied when foundation and safety are satisfied.
- **P4 (81-100):** Aspirational — competitive surpass, documentation excellence, design elegance. Applied when everything else works.

---

## §2 — Conflict Resolution Rules

When rules disagree, apply these rules **in order.** The first rule that selects a winner decides the result.

### Rule #1: Specific > General

A rule targeting a narrower scope wins over a rule with `scope: [all]` when both apply to the situation.

- `scope: [security]` beats `scope: [all]` in a security context.
- `scope: [ship, deploy]` beats `scope: [all]` during a deployment decision.
- `scope: [docs, research]` beats `scope: [all]` when evaluating documentation requirements.

**How to apply:** Check the `scope` field in each rule file's frontmatter. If one scope is a subset of the other, the narrower scope wins. If both scopes are equally specific or both are `[all]`, proceed to Rule #2.

### Rule #2: Mandatory > Recommended

Mandatory severity always beats recommended severity.

- `severity: mandatory` beats `severity: recommended` regardless of priority number.
- A recommended rule cannot override a mandatory rule — even if the recommended rule has a lower priority number.

**Exception:** See Rule #4 (version supersession) for the one case where a newer recommended rule might inform interpretation.

### Rule #3: Lower Priority Number > Higher

Within the same scope and severity tier, the lower priority number always wins.

- Priority 15 beats priority 30.
- Priority 65 beats priority 75 (both P3, both mandatory — lower number wins).

Priority numbers are **not** weighted averages — they are strict total order within a scope+severity bucket.

### Rule #4: Later Version > Earlier

If two rules have the same scope, same severity, AND the same priority number, the higher version number wins.

- Version 2.5.0 of a rule supersedes version 1.0.0 of the same-named rule.
- This handles the case where a rule has been updated to reflect new understanding.
- Version comparison follows semantic versioning: compare major first, then minor, then patch.

**Applicable only when Rules #1-#3 produce a tie.** Version is never the primary decider.

### Rule #5: AGENTS.md Classification as Tiebreaker

If Rules #1-#4 fail to resolve (e.g., same scope, same severity, same priority, same version), the session classification in AGENTS.md determines the winner.

- **SECURITY incident** → SECURITY.md rules dominate over PRODUCT.md.
- **QA session** → QA.md rules dominate over PERFORMANCE.md.
- **INCIDENT war room** → INCIDENT.md rules dominate over DOCS.md.
- **PLANNING phase** → PLAN.md and PRD.md rules dominate over SURPASS.md.

**How to find the classification:** The AGENTS.md at the repo root defines which `profile` or session type is active. The `pairs-with` field in each rule file's frontmatter hints at which rules share a domain — during a paired context, the rule whose domain matches the session type wins.

---

## §3 — Resolution Algorithm

```
function resolve(ruleA, ruleB, sessionType):
    # Rule #1: Specific > General
    if narrower_scope(ruleA, ruleB):
        return ruleA
    if narrower_scope(ruleB, ruleA):
        return ruleB

    # Rule #2: Mandatory > Recommended
    if ruleA.severity != ruleB.severity:
        return the one with severity=mandatory

    # Rule #3: Lower priority number wins
    if ruleA.priority != ruleB.priority:
        return the one with lower priority number

    # Rule #4: Later version wins
    if compare_versions(ruleA.version, ruleB.version) != 0:
        return the one with higher version

    # Rule #5: AGENTS.md classification
    return match_session_domain(ruleA, ruleB, sessionType)
```

---

## §4 — Workspace Priority (MCP Bridge)

When the 1ai framework operates within a **workspace repo** that has its own AGENTS.md, CLAUDE.md, or `.cursorrules`:

1. **Core rules** (`~/.1ai/core/*.md`) always win over workspace-specific rules for **integrity and safety violations** (P0-P1).
2. **Workspace rules** (e.g., a repo's CLAUDE.md) can override P2-P4 rules for **repo-local conventions** — but the override must be explicit (a `rules:` or `extends:` directive in the workspace config).
3. **No override of DON'T LIE** (RULES.md rule #2, priority 05) — EVER.
4. **No override of CODE MUST RUN** (RULES.md rule #5, priority 05) — EVER.

**Implicit workspace rules never win.** If a repo's AGENTS.md says "skip verification" but doesn't explicitly override GATE.md, GATE.md still applies.

### Workspace-Core MCP Routing Table

| Context | Core Wins | Workspace Wins | Conflict Resolution |
|---------|-----------|----------------|---------------------|
| Integrity violation (P0) | ✅ always | ❌ never | Core rule #2 DON'T LIE is absolute |
| Security breach (P1) | ✅ always | ❌ never | SECURITY.md dominates |
| Code style convention (P3) | ❌ can defer | ✅ when explicit | Workspace convention overrides core docs/docs |
| Lint/format config (P3) | ❌ can defer | ✅ when explicit | Workspace `.editorconfig`/`.eslintrc` wins |
| CI pipeline steps (P2-P3) | ⚠️ GATE.md applies | ✅ overrideable | Workspace can add gates, never remove |
| Naming conventions (P3) | ❌ core provides default | ✅ overrideable | Workspace conventions win if explicit |
| Feature implementation (P2-P3) | ❌ | ✅ | ENGINEERING.md §6 loop applies; workspace decides specifics |

**Bridge applies per-task, not per-session.** A task touching a workspace repo uses the bridge. A task in `~/.1ai/` itself does not.

---

## §5 — Conflict Examples

### Example A: SPEED vs QUALITY

**RULES:** PERFORMANCE.md (priority 65, mandatory, scope: [all]) says "optimize aggressively."
**RULES:** QA.md (priority 20, mandatory, scope: [qa, testing]) says "verify every layer."

**Conflict:** Run tests or skip to ship faster?

**Resolution:**
1. Rule #1: Both have scope matching the task (testing context). QA.md scope `[qa, testing]` is narrower than `[all]` when running QA. **QA wins.**
2. Rule #2: Both mandatory — tie.
3. Rule #3: QA priority 20 < PERFORMANCE priority 65. **QA wins.**

**Result:** Run tests fully. Quality before raw speed.

---

### Example B: DOCS vs INCIDENT

**RULES:** DOCS.md (priority 75, recommended, scope: [docs, research]) says "document everything before shipping."
**RULES:** INCIDENT.md (priority 30, mandatory, scope: [all]) says "contain first, document later."

**Conflict:** A production fire is happening — write docs or contain?

**Resolution:**
1. Rule #1: INCIDENT.md scope `[all]` matches the incident context, DOCS.md scope `[docs]` does not. **INCIDENT wins.**
2. (If still tied) Rule #2: mandatory > recommended. **INCIDENT wins.**
3. Rule #3: 30 < 75. **INCIDENT wins.**

**Result:** Contain the fire. Documentation can wait.

---

### Example C: ENGINEERING vs USER SHORTCUT

**SITUATION:** User says "just fix it, skip the analysis — I know what I want."
**RULES:** RULES.md rule #2 (priority 05, mandatory, scope: [all]) says DON'T LIE / verify.
**RULES:** ENGINEERING.md §6 (priority 10, mandatory, scope: [all]) says READ first, PLAN, VERIFY.

**Conflict:** User request shortcuts the engineering loop.

**Resolution:**
1. Rule #1: Both scope `[all]` — tie.
2. Rule #2: Both mandatory — tie.
3. Rule #3: RULES.md priority 05 < ENGINEERING.md priority 10. **RULES.md wins.**
4. Rule #5: If still tied, AGENTS.md profile determines whether strict analysis (ENGINEERING) or process integrity (RULES) dominates — but Rule #3 already settles it.

**Result:** User request cannot bypass RULES.md. DON'T LIE is the highest-priority rule in the system. Verify before claiming done.

---

### Example D: SECURITY vs SHIP SPEED

**RULES:** SECURITY.md (priority 25, mandatory, scope: [all]) says "no hardcoded secrets, all credentials must be vaulted."
**RULES:** RELEASE.md (priority 50, mandatory, scope: [ship, deploy]) says "ship within the deployment window."

**Conflict:** Secret needs vaulting but deployment window is closing.

**Resolution:**
1. Rule #1: SECURITY.md `[all]` is broader than RELEASE.md `[ship, deploy]` for a deployment context — but the security concern is domain-specific not scope-narrower. Narrower for the deployment: RELEASE.md targets deployment specifically. However, Rule #2 tie, Rule #3: 25 < 50. **SECURITY wins.**

**Result:** Fix the secret. No shortcut on P1 safety. The deployment window waits.

---

### Example E: Complementary Rules (no conflict)

**RULES:** VERIFICATION.md (priority 15, mandatory, scope: [all]) says "show receipts."
**RULES:** GATE.md (priority 20, mandatory, scope: [ship, commit]) says "run pre-ship checklist."

**Relationship:** These do NOT conflict — they compose. GATE.md's checklist includes verification steps. VERIFICATION.md defines the standard of evidence. Together they form a pipeline, not a disagreement.

**Signal:** Rule #5 (session type) determines which file provides the primary checklist and which provides the evidence standard. A COMMIT session runs GATE.md first; a VERIFY session runs VERIFICATION.md first.

---

## §6 — Implementation

### Tool Integration

- **`1ai rules audit`** — scans all `core/*.md` files, parses frontmatter, and flags:
  - Duplicate priority numbers across different severity/scope combinations
  - Rules with the same priority, scope, and severity (ambiguity)
  - Rules with missing or invalid `priority` field
  - Conflicts between rules that share overlapping scope
- **`1ai rules resolve --rule A --rule B --context <session-type>`** — given two rule references and a session type, prints the deterministic winner and the chain of resolution rules applied.
- **Hooks system** (`bin/1ai` hook chain) — pre-commit and pre-merge hooks can call `1ai rules resolve` to detect when conflicting rules would apply to the current change.

### Adding a New Rule

When adding a new rule file to `core/`:

1. Assign a priority number following the band table in §1.
2. Ensure no priority collision with an existing rule at the same scope + severity.
3. If a new rule overlaps scope with an existing rule, document the expected resolution in `docs/REGISTRY.md`.
4. Run `1ai rules audit` to validate the new entry.

### Versioning

- Priority numbers form a **strict total order per scope+severity tier** — no ties allowed within the same tier.
- Version bumps in individual rule files do not change priority numbers (that requires an explicit migration).
- Priority migration: `1ai rules migrate --from-priority N --to-priority M --file <path>` — updates the priority and marks the change in the audit log.

---

## §7 — Edge Cases

### Co-Equal Rules
If Rules #1-#5 all fail to resolve (same scope, severity, priority, version, and no session classification), the system consults:
1. **pairs-with** field — the rule that also pairs with the other rule's domain wins (cooperative tiebreak).
2. **Alphabetical** — if still tied, earlier name alphabetically wins. This is a last resort and should never happen in practice.

### Multi-Rule Conflicts
When 3+ rules conflict on the same decision:
- Pairwise tournament: resolve the two highest-priority (lowest number) contenders, then the winner vs the next, etc.
- The tournament result is deterministic — same input, same output.

### User Override
A human can explicitly override any resolution by stating "OVERRIDE: <rule-name>" with a reason. The override is logged in the session trace (`core/SESSION_TRACING.md`). An override without a logged reason is a GATE.md violation.

---

## §8 — Relationship to ENGINEERING.md §9

ENGINEERING.md §9 defines a 4-level conflict hierarchy for engineering decisions:

1. System Safety (don't break production)
2. Epistemic Honesty (say what's true)
3. Factual Integrity (verify before asserting)
4. User Instructions (follow but not blindly)

PRIORITY.md is the **meta-framework** that resolves conflicts between *rule files themselves.* ENGINEERING.md §9 resolves conflicts *within* engineering process decisions. The two are complementary:

| Scope | Document | Example |
|-------|----------|---------|
| Between rule files | PRIORITY.md | "SECURITY.md vs RELEASE.md — which rule applies?" |
| Within a single process | ENGINEERING.md §9 | "Speed vs honesty in a test report?" |

When both frameworks apply, PRIORITY.md always resolves first (which rule wins), then ENGINEERING.md §9 guides how to apply the winning rule.
