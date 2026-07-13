---
name: anti-patterns
version: 3.1.0
severity: mandatory
scope: [all]
pairs-with: [engineering, verification, learn]
description: Growing catalog of AI agent failure modes — discovered from real incidents
---

# ANTI-PATTERNS.md — AI Agent Failure Catalog

> Every failure mode here was discovered from a real incident. This is a living document.
> When you discover a new anti-pattern, add it: incident → symptom → root cause → rule.

---

## How to Add a New Anti-Pattern

```
### AP-NNN: [Short Name]
**Discovered:** [date, incident]
**Symptom:** [what the AI did wrong]
**Root cause:** [why — the underlying bias or gap]
**Rule:** [what rule/protocol prevents this]
**Enforcement:** [hook, gate, CI, review]
```

---

## Catalog

### AP-001: Code-Written = Feature-Done
**Symptom:** Agent says "I implemented auth" after writing code, without running it. Code is text; behavior is runtime.
**Rule:** VERIFICATION.md §1 — Receipt Requirement. **Enforcement:** GATE.md Gate 6 (tests pass), Gate 7 (use like real user).

### AP-002: Test-Exists = Test-Passes
**Symptom:** "I added tests" without running them. Or runs them but doesn't paste output.
**Rule:** VERIFICATION.md §2 — Self-Skeptic Protocol. **Enforcement:** VERIFICATION.md §6 — Mandatory Completion Block.

### AP-003: No-Error = Working
**Symptom:** "Build completed without errors" as proof of correctness. Compiling ≠ working.
**Rule:** VERIFICATION.md §3 — Verification Levels (Level 0 ≠ Level 1). **Enforcement:** GATE.md Gates 4+6+7.

### AP-004: Happy Path Only
**Symptom:** Tests only successful case, not: declined, timeout, duplicate, zero, negative.
**Rule:** VERIFICATION.md §4 — Break It First Mandate. **Enforcement:** GATE.md Gate 8 (business logic).

### AP-005: Summary Instead of Receipt
**Symptom:** "API returns correct data" instead of pasting actual curl response. Summaries hide failures.
**Rule:** VERIFICATION.md §1 — Receipt = literal output. **Enforcement:** REVIEWER.md §2.4 — Receipt Validation.

### AP-006: Business Capability Conflation
**Symptom:** "Yes, we can email institutions" because code has email-sending capability. Tech ≠ business.
**Rule:** ENGINEERING.md §3 — Business Capability Honesty. **Enforcement:** Mandatory principle, caught in review.

### AP-007: Overclaim "Production Grade"
**Symptom:** "Production grade" because code compiles and tests pass. But no deployment, no load testing, no real users.
**Rule:** ENGINEERING.md §3 — Honest Assessment + Business Capability Honesty. **Enforcement:** GATE.md Gate 11 (monitoring), §6.5.

### AP-008: Skip Decomposition
**Symptom:** Given "Add payment integration", immediately starts coding. No restatement, no scoping. One giant PR.
**Rule:** PLAN.md §2 — Decomposition Protocol. **Enforcement:** PLAN.md mandatory for COMPLEX.

### AP-009: Silent Scope Creep
**Symptom:** While fixing a bug, also refactors adjacent code, renames variables, changes imports. 3x more changes.
**Rule:** ENGINEERING.md §7 — Drive-by edits prohibition. **Enforcement:** REVIEWER.md §2.1 — Diff Integrity Check.

### AP-010: Hallucinated Dependencies
**Symptom:** Suggests package that doesn't exist, is abandoned, or published yesterday by random user.
**Rule:** ENGINEERING.md §5 — Verify package is real and not freshly published. **Enforcement:** Pre-commit check.

### AP-011: Self-Verification
**Symptom:** Agent writes code AND reviews it themselves. "Diff looks good." Confirmation bias.
**Rule:** ENGINEERING.md §3 — No Self-Verification. **Enforcement:** REVIEWER.md §1 — Context Isolation.

### AP-012: Anti-Thrash Failure
**Symptom:** Same fix approach 4+ times with minor variations, never questioning root hypothesis.
**Rule:** ENGINEERING.md §3 — Anti-Thrash (2 failures = stop and rethink). **Enforcement:** 3rd failure → escalate.

### AP-013: Skip PR Lifecycle (Complexity Minimization)
**Symptom:** Agent classifies COMPLEX change as SIMPLE to avoid issue/PR/review overhead. One giant PR ships bugs.
**Rule:** ENGINEERING.md §4 + §4.1 — Complexity check + PR Lifecycle mandatory for COMPLEX.
**Enforcement:** GATE.md Gate 14 — fresh-context review required for COMPLEX.
**Red flags:** "it's basically one thing" (but 6 files) · "one PR to keep it clean" (3 concerns) · "review not needed" (self-assessing complexity) · PR diff >300 lines with no issue reference.

### AP-014: Literal Execution Without Understanding Intent
**Symptom:** "Add cron job every hour" → immediately writes cron. Never asks: is cron right? is real-time better?
**Rule:** RULES.md §Understand Intent. PLAN.md Step 1 — Intent Clarification.
**Enforcement:** GATE.md Gate 0 — Intent must be documented before any code.
**Red flags:** Literal restatement without identifying goal · Risky/irreversible solution without asking · Sees better alternative but stays silent · Adds scope without telling user · Asks "are you sure?" for trivially clear requests.

### AP-015: Blind Trust in User Claims
**Symptom:** User says "API is working" or "tests pass" — agent believes without checking. Builds on broken foundation.
**Rule:** RULES.md §Don't Trust — Verify. ENGINEERING.md §3 — Anti-Sycophancy (expanded).
**Enforcement:** GATE.md Gate 0 (verify claims before proceeding). RULES.md §2 (receipts apply to user claims too).
**Red flags:** Accepts "it's working" without curl/running tests/checking logs · Skips verification because "user confirmed" · Builds on user's assumption without checking it · Ignores contradictions in user prompt · Backs down from correct observation just because user disagrees.


### AP-016: Stub Ships as Feature
**Symptom:** "Payment system done" — has placeholder UI, TODO handlers, no integration. Code compiles, nothing works.
**Rule:** RULES.md §11 (Zero Stubs). ENGINEERING.md §11.2 (MVP Must Be Demoable). §2 Zero-hygiene.
**Enforcement:** grep for TODO/FIXME/stub before commit. User-test each feature flow end-to-end.
**Red flags:** Feature is "done" but has no real API calls · UI shows buttons that don't work · Code says "TODO: implement" · Function has docstring but empty body · "Will add later" in commit message.

### AP-017: Over-Engineering Before Revenue
**Symptom:** Builds event-driven microservice architecture for a blog. Spends 2 weeks on abstractions before any content renders.
**Rule:** RULES.md §REVENUE FIRST. DESIGN PRINCIPLES KISS+YAGNI. ENGINEERING.md §11.3.
**Enforcement:** KISS check in code review. Revenue-first prioritization: does this abstraction ship revenue faster?
**Red flags:** Abstract interfaces for every dependency on day 1 · Schema before any API · Kubernetes before cron · Event bus before REST · "But we'll need it later" justification · More config than logic.

### AP-018: Perfect But Unshipped
**Symptom:** "I can't ship until I refactor/fix X/add Y." Perfect code never ships. Revenue never arrives.
**Rule:** RULES.md §SHIP FAST. DESIGN PRINCIPLES §MVP-FIRST. ENGINEERING.md §11.1.
**Enforcement:** docs/track/ must exist before feature can be marked "done but deferred". Ship working version, track improvements.
**Red flags:** "One more refactor before release" · "When X is done, then we launch" · Feature complete for 2 weeks but not deployed · Chasing 100% test coverage before ship.

### AP-019: Aesthetic Before Business Flow
**Symptom:** Spends 3 days on button animations, color palette, font system BEFORE core checkout works. Revenue flow incomplete.
**Rule:** RULES.md §REVENUE FIRST. ENGINEERING.md §11.3 hierarchy.
**Enforcement:** Code review: does this PR touch revenue-relevant flow? If not, does it ship before revenue flow is complete?
**Red flags:** CSS animations before API integration · Design system before business logic · Theme switching before payment works · "It doesn't look good enough" as ship blocker · More UI polish than backend work in early stages.
---

## Meta: How Anti-Patterns Become Rules

```
1. INCIDENT  → Something goes wrong
2. ANALYSIS  → Root cause (not symptom)
3. PATTERN   → Generalize failure class
4. RULE      → Create/update rule that prevents it
5. ENFORCEMENT → Hook, gate, CI, or review checklist
6. VERIFY    → Rule actually catches the pattern
```

When you discover a new anti-pattern:
1. Add it here with the template
2. If it needs a new rule → update relevant rule file
3. If it needs enforcement → add to GATE.md or a hook
4. Commit: `learn: add AP-NNN [short name]`
