---
name: qa-review-fix-loop
description: Comprehensive QA→Review→Fix loop protocol for any codebase. Layer-based testing with evidence requirements. Use when performing full QA cycles, codebase audits, pre-release testing, or.
domain: development
tags: 
- [qa
- testing
- quality-assurance
- review-loop
- defect-tracking
- regression-testing
- evidence-based]
---

# QA → Review → Fix Loop Protocol

Comprehensive, evidence-based QA protocol. Layer-based testing with mandatory re-verification. Works on any project — web app, mobile app, trading engine, bot, API, CLI tool, monorepo. Every layer reaches a state that is **independently verified**, not claimed, to function correctly.

**Source:** QA_REVIEW_FIX_LOOP_PROTOCOL.md — universal QA protocol

## Overview

**QA Review-Fix Loop** implements an iterative quality cycle: review code → identify issues → fix → re-review → verify. Maintains a fix queue and tracks resolution progress until all issues are resolved.


## When to Use

**Trigger phrases:**
- "Run QA on this codebase"
- "Full QA cycle"
- "Test everything end-to-end"
- "Pre-release testing"
- "Codebase audit"
- "Find and fix all bugs"
- "Verify this works"

**Use cases:**
- Pre-release QA cycles
- Post-refactor regression testing
- New codebase onboarding (understand + verify)
- Defect-driven development
- Cross-layer integration verification

**When NOT to use:**
- Single bug fix (use `skill://systematic-debugging` instead)
- Code review only (use `skill://code-reviewer`)
- Unit test writing (use `skill://test-driven-development`)


## When NOT to Use

- For throwaway prototypes (skip the ceremony)
- When the fix is a single-line change with no side effects
- When the codebase already has a working solution


## Process

### Step 0 — Discover the Codebase

Do not assume the stack. Inspect the repository first:

1. Read `README.md`, `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` to identify languages, frameworks, entry points
2. Map actual layers present — only test what exists:
   - Frontend (web, mobile, desktop UI)
   - Backend services / servers
   - REST / GraphQL / RPC APIs
   - Databases & migrations
   - MCP servers / tool integrations
   - Bots (chat, trading, Discord/Telegram/Slack)
   - Engines (trading, simulation, rules, scoring)
   - Background jobs / workers / cron tasks
   - CLI tools
   - Infra/config (Docker, CI/CD, env handling)
   - Third-party integrations (payment, auth, data providers)
3. For each layer, identify how it's tested (existing suite? `npm test`? `pytest`? manual? none?)
4. Produce a Layer Inventory before testing begins

### Step 1 — The Loop (per layer)

For **each layer** in the Layer Inventory, repeat:

```
[1] QA PASS       → run tests, click through, call endpoints, log every defect
[2] REVIEW PASS   → root-cause each defect, confirm reproducibility,
                     reject fixes that only mask symptoms
[3] FIX PASS      → implement one fix at a time per defect
[4] RE-QA         → re-run the EXACT test that caught the defect,
                     PLUS regression check on adjacent code
[5] EXIT CHECK
     ├─ New or surviving defects? → back to [2] REVIEW
     ├─ Zero defects this pass?   → layer CLEARED → next layer
     └─ Same defect survives 3 attempts? → STOP, escalate with root-cause writeup
```

**Rules:**
- No layer is "done" off a single pass. Done = zero new defects + regression check
- No batching unrelated fixes — fix and re-verify as separate changes
- A fix that only suppresses a symptom is rejected at Review
- After all layers CLEARED, run one full cross-layer end-to-end pass

### Step 2 — Coverage Requirements (per layer)

**Frontend / UI:**
- Every page/screen, route (including 404, redirects)
- Every button, menu, dropdown, modal, tab, tooltip, toast
- Every form: valid/invalid/empty input, boundary values, required fields
- Every interactive state: loading, empty, error, success, disabled, offline
- Navigation flows end-to-end
- Responsive breakpoints if applicable

**Backend / Services:**
- Every endpoint × every HTTP method
- Auth & permission boundaries (authenticated vs not, role A vs role B, expired tokens)
- Input validation: valid, invalid, missing, boundary, malicious
- Error handling: correct status codes, no stack traces to clients
- Idempotency where it matters (payments, order creation)
- Concurrency/race conditions (double-submits, parallel writes)

**APIs:**
- Response shape matches declared schema exactly
- Status codes correct for every branch (2xx/4xx/5xx)
- Rate limiting behavior if implemented
- Backward compatibility if breaking-change-sensitive

**MCP Servers / Tool Integrations:**
- Every tool called with: valid args, invalid args, missing args, wrong types
- Returned data matches declared output schema
- Failures surfaced as informative errors, never silent no-ops
- Tool descriptions match actual behavior

**Bots (chat, trading, messaging):**
- Every command/trigger phrase, including near-misses and typos
- Conversation state transitions (multi-step flows, cancel, timeout)
- Failure recovery: malformed input, network drop, upstream failure

**Engines (trading, simulation, rules):**
- Core calculations verified against known expected values
- Edge cases: zero, negative, null, extreme values, empty datasets
- **A wrong number that doesn't crash is worse than a crash** — silent miscalculation must be tested
- Determinism check where expected, or documented non-determinism where intentional

**Background Jobs / Workers / Cron:**
- Job runs on schedule/trigger as configured
- Failure and retry behavior
- Idempotency on re-run
- Resource cleanup (no orphaned processes, locks, temp files)

**Infra / Config / CI-CD:**
- Environment variable handling (missing var fails loudly)
- Build succeeds from clean clone
- CI pipeline actually runs the test suite it claims

**Cross-cutting (always check):**
- Logging: real errors visible, not swallowed
- Secrets: none hardcoded in code
- Dependency drift: `npm install` / `pip install` from clean environment works

### Step 3 — End-to-End Cross-Layer Pass

After every layer is CLEARED, run at least one full journey crossing layers:

```
User action → API call → backend logic → engine/bot processing →
database write → response back → UI reflects new state correctly
```

Pick 2-4 most important real-world journeys and run them fully after the last fix.

### Step 4 — Definition of Done

Done when, and only when:

1. Every layer in the Layer Inventory is CLEARED (zero open defects, confirmed by re-test)
2. Cross-layer end-to-end pass run after the last fix, and is itself defect-free
3. Final Evidence Report complete, including explicit list of anything not tested and why

If any of these three are missing, the work is **not done**.

## Verification

### Evidence Requirements (replaces "100% working" claims)

For **every layer**, report:

```
LAYER: <name>
Method:        [ ] Automated (suite/command name)
                [ ] Manual (what was clicked/called/observed)
Test cases run: <N>
Passed:         <N>
Failed → fixed → re-verified: <N>
Open defects:   <N>   (must be 0 to mark CLEARED)
Not tested:     <list skipped items + exact reason>
```

An honest "not verified — here's why" is strictly better than a false "100% confirmed."

### Anti-Patterns to Reject

- Claiming "100% tested" without evidence table
- Marking a layer done after single QA pass with no re-test
- Fixing a bug by catching/silencing an error instead of addressing root cause
- Batch-fixing unrelated defects in one change
- Skipping harder layers while testing easy ones
- Reporting "no defects found" without stating what was actually run

### Tracking Template

Use this for each layer:

| Pass | Method | Defects Found | Fixed | Re-verified | Open |
|------|--------|---------------|-------|-------------|------|
| 1 | Automated/Manual | N | N | N | N |
| 2 | Automated/Manual | N | N | N | 0 |

Status progression: `Not started` → `In QA` → `Fixing` → `Re-QA` → `CLEARED`

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |

## Related Skills

- `skill://verification-before-completion` — Pre-completion verification
- `skill://code-reviewer` — Code review process
- `skill://systematic-debugging` — Individual bug investigation
- `skill://test-driven-development` — TDD workflow
- `skill://engineering-hard-rules` — Engineering enforcement protocol
- `skill://requesting-code-review` — Request external review
