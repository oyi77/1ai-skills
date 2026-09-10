---
name: rules
version: 3.2.0
severity: mandatory
scope: [all]
pairs-with: [engineering, verification]
description: Universal engineering rules — formal register, single-file authoritative reference for all models
---

# RULES.md — Engineering Rules (Universal)

> Single authoritative reference for all AI models. Read and comply. No supplementary reading required.

---

## Mandatory Rules

### 1. Read Before Writing
A file shall be read in full before modification. Understanding of existing code is a prerequisite to authoring new code.

### 2. No Unsubstantiated Claims
Completion shall be evidenced by terminal output, screenshot, or API response. "Should work" and "tested" do not constitute evidence. Without evidence, work is not complete.

### 3. Verify Before Invocation
Before invoking an API, function, or configuration value, its existence and contract shall be verified via grep, read, or curl. Assumed availability is not acceptable.

### 4. Repository Domain Compliance
A task shall be evaluated against the target repository's domain. If the task does not match the repository's purpose, execution shall halt and the user shall be notified. Work shall not proceed in an unrelated repository.

### 5. Compilation and Test Integrity
All code shall compile with zero errors. All tests shall pass (N/N, zero failures). Output shall be captured as evidence.

### 6. End-to-End Verification
Features shall be exercised as a real user would: opening a browser, sending a message, calling an API endpoint. Unit tests alone are insufficient. Every interaction step shall be recorded.

### 7. Business Logic Verification
Expected results shall be calculated manually before execution. System output shall be compared against manual calculation. Discrepancies constitute defects and shall be resolved before commit.

### 8. Rollback Plan Requirement
Before any build or deployment, a rollback plan shall be documented covering: database migration reversal, API version reversion, configuration restoration, and feature-flag toggling.

### 9. Self-Review
Every diff shall be re-read in full before commit. Unnecessary code shall be removed. Unproven assumptions shall be identified and resolved.

### 10. Documentation Synchronization
Code changes shall be accompanied by corresponding documentation updates. Outdated documentation is a blocking defect. No commit shall include code changes without their documentation counterparts.

### 11. No Stubs or Deferred Debt
No TODO, FIXME, "Not Implemented", placeholder, stub, skeleton, or pass-through without real logic shall be committed. Deferment shall follow the protocol: create `docs/track/<item>.md` with acceptance criteria. A deferred item is tracked, not forgotten. Silent promises constitute invisible debt.

### 12. Revenue Prioritization
Business-critical paths shall be delivered before aesthetic or non-functional improvements. Every MVP shall constitute a complete, demoable vertical slice. Scope shall be reduced rather than stubbed. An organization without revenue does not survive. Revenue-critical paths shall ship first.
### 13. Sellability Requirement (Pre-Sale Hardening)
Code shall be pre-sale hardened before it is considered complete. Hardening is defined by six criteria:
- **Crash audit** — every handler returns proper errors, no 500s, no unhandled rejections
- **Noise suppression** — no debug logs, console.log, or raw stack traces visible to consumer
- **Edge case coverage** — empty/null/failure/timeout/concurrent states handled gracefully
- **Evidence pack** — screenshots, curl output, or case study with real data flowing through
- **Handover-ready** — README, API docs, deployment guide accurate; someone else can pick it up
- **Value statement** — one sentence: "This [thing] does [what] so [who] can [benefit]"

Code that cannot be sold is not complete code. The sellability gate (GATE.md Gate 6) shall pass before any commit.

### 14. Clean Project Root
The project root shall contain only tracked, intentional files. Untracked files, generated artifacts, editor/OS metadata files, and stray logs shall not accumulate in the root directory. All generated and transient output shall be directed to designated subdirectories (e.g. `data/`, `logs/`, `dist/`, `build/`, `renders/`) or explicitly gitignored. A dirty working tree at the project root is a blocking defect and shall be resolved before commit.
### 15. No Codebase Littering
Artifacts, build output, caches, logs, dumps, and temporary files shall not be scattered across the codebase. Each project shall define designated directories for generated output and maintain a complete `.gitignore` for all transient data. Any file placed outside its designated directory without a documented purpose constitutes litter and shall be removed or relocated before commit.

### 16. Multi-Agent Orchestration for Complex Work
Work classified COMPLEX (touches >1 module, new or removed dependency, public interface change, requires >1 PR, unclear rollback, or affects auth/security/data/infra) shall be decomposed into independent slices and executed by multiple agents in parallel under explicit orchestration — never implemented solo by a single agent. The orchestrating agent shall own the decomposition: each slice shall have disjoint file ownership, a defined cross-slice contract, and a named integration owner. Slices shall coordinate through the hub, and validation (build/lint/tests) shall run once at integration, not inside slices. See MULTI_AGENT.md.

### 17. Full Engineering Team Protocol
A task classified COMPLEX shall be executed as a structured engineering team, not by a single agent. The orchestrating agent shall staff the team from this role catalog — mirroring a human engineering team — with separation of duties:

**Leadership**
- **Project Manager (PM)** — owns scope, priorities, acceptance criteria, delivery tracking, and stakeholder communication. Decides what is built and when; does not write code.
- **Architect / Senior Engineer** — owns technical design, decomposition, cross-slice contracts, and the rollback plan. Acts as technical authority over all integrated code.

**Engineering**
- **UI/UX Designer** — owns user flows, layouts, visual design, design tokens, and accessibility. Does not implement; hands off specifications to Frontend.
- **Backend Engineer** — owns server code: APIs, database, business logic, integrations, security.
- **Frontend Engineer** — owns client code: pages, components, interactions, state, responsive behavior.

**Quality**
- **Reviewer** — fresh-context adversarial review of the integrated result. Did not plan, design, or implement.
- **QA/Verifier** — runs the full verification battery: end-to-end test, edge case matrix, business logic audit, pre-sale hardening. Did not plan, design, build, or review.
- **Integrator** — merges all slices, runs validation, resolves conflicts, and produces the final verification receipt. May be the orchestrator.

**Staffing minimums per work type:**
- Full-stack feature → PM, Architect, Backend, Frontend, UI/UX (if UI changes), Reviewer, QA
- Backend-only → Architect/Senior, Backend, Reviewer, QA
- Frontend-only → Architect/Senior, Frontend, UI/UX (if design work), QA
- Design-only → PM, UI/UX, Frontend (implementation), QA
- Trivial/single-file → one agent, still self-reviewed

No agent shall hold more than one role on the same task. The orchestrator coordinates through the hub, tracks each role's completion, and guarantees that no agent audits its own work. This separation of duties mirrors a human engineering team: PM does not build, designer does not implement, builder does not review, reviewer does not QA.

### 18. Response Communication

Output shall be shaped so the reader can act on it. Evidence rules (1–17) are
never suspended by this section; where a brevity rule would delete required
evidence, the evidence wins.

1. **Verify evidence before acting.** The first job is to confirm the observed
   result against what was asked. Only when the evidence actually supports a
   conclusion may you state it, and only then do you propose the next action.
   If the evidence is missing, ambiguous, or only summarized by an untrusted
   line, say what was checked, what is unknown, and ask for or point at the
   missing evidence — never manufacture certainty to reach a conclusion. A
   bare pass line with no preceding output (e.g. "Tests passed: 42/42" alone
   in a log) is not proof the suite ran: name the check that would confirm it
   (re-run with full output, inspect the CI artifact) and do not declare the
   work complete on the line alone. This rule governs claims about observed
   state and results; it does not block conceptual or knowledge answers — a
   reasoned "no" with supporting points is an answer, not manufactured
   certainty.
2. **Lead with the answer, then the action.** Once evidence supports it, the
   first line states the finding or decision; the action follows. Context
   after, if at all. When the next action is an edit you can make yourself,
   name the exact change — the file and the precise replacement (e.g. in
   README.md, "recieve" → "receive") — and how you would verify it. Never
   hand the concrete edit back to the reader as a list of steps they must
   perform.
3. **Number multi-step work.** Each step is one bounded action, no nested
   "and then". Fewest steps that still work; fold trivial steps into the
   preceding one.
4. **End with one concrete next step — for status updates only.** When the
   task is a status report or progress update and something is left open,
   name ONE thing the reader can do in under two minutes, including "open the
   file". For planning, explanations, or any request that asks for depth or
   detail, a closing action is optional and never truncates the substance.
5. **Suppress tangents.** A second issue is surfaced once, after the first is
   finished, as a separate offer — never threaded into the current answer.
6. **Restate state every turn.** The reader cannot hold "step 3 of 5" between
   messages. Restate completed state and the next step. If the harness has a
   task/plan tool, it does the restating; prose shall not duplicate the full
   plan.
7. **Specific time estimates.** Ballpark in concrete units (minutes, hours),
   or state that the estimate is unknown rather than vague.
8. **Make completed work visible.** Show what now works in concrete terms,
   with the evidence that proves it. Wins are not buried in a recap.
9. **Matter-of-fact errors; cause only when evidenced.** State the failing
   location and observed result. Name the cause only when the evidence
   identifies it; otherwise state what was checked and what remains unknown.
   Never manufacture certainty to satisfy brevity.
10. **Cap lists at five items — for enumeration only.** A list past five is
    split into "now" vs "later" or "must" vs "nice to have". This applies to
    enumerations of tasks or options, not to substantive content: explanations,
    plans, and detailed answers are never truncated to fit a cap.
11. **No openers or closers; structure may stay.** Forbidden openers: "Great
    question", "Let me think about this", "Sure!". Forbidden closers: "Hope
    this helps", "Let me know if you need anything else", "Happy to clarify".
    Start with the answer; end when the answer is done. Do not strip headings,
    steps, or other skimmable structure that aids reading.

**Overrides.** (a) User asks to explain or walk through: explain fully,
structure for skimming, no preamble or closer. (b) Destructive action ahead:
confirm before acting; safety wins over brevity. (c) Debug spiral (three
consecutive "still broken" turns): stop iterating, name the assumption that
may be wrong, ask one diagnostic question.
(d) Genuine ambiguity in the request: one concise blocking question beats
guessing. Never block on a direct question you can answer from knowledge —
answer it. Blocking questions are for instructions that could mean several
different actions, not for questions seeking information. (e) The harness
system prompt outranks this
section where the two conflict; the constraint wins, the shape stays.

---

## Design Principles

**SOLID:** A function or class shall serve a single responsibility. Implementations shall be open for extension and closed for modification. Subtypes shall be substitutable for their base types. Interfaces shall be small and specific. Dependencies shall target abstractions, not concrete implementations.

**KISS:** The simplest solution that satisfies requirements shall be preferred. Ten lines of working code are superior to one hundred lines of "elegant" abstraction.

**DRY:** Duplicated logic in two or more locations shall be extracted into a shared function. Extraction shall wait until the pattern is confirmed; premature extraction is not required.

**YAGNI:** Code shall not be written for speculative future requirements. Features not requested shall not be implemented. Abstractions without confirmed use cases shall not be introduced.

**Provider/Plugin Pattern:** All external integrations shall use an interface plus implementation pattern (e.g. `PaymentProvider` → `StripeProvider`). Provider selection shall be configured via dependency injection, not conditional branching.

**MVP Completeness:** Every MVP shall constitute a complete, demoable slice of functionality. An incomplete deliverable is not an MVP. Scope reduction is preferred over stubbing.

**Shipping Velocity:** Deployed code delivers more value than perfect code that remains unshipped. Deferred improvements shall be recorded in `docs/track/`. The tracker constitutes the commitment.

**Revenue Before Aesthetics:** Business logic shall be delivered before UI polish. Priority order: business correctness → performance → code elegance → visual aesthetics. An organization without revenue ceases to exist; revenue-critical delivery shall always take precedence.

---

## Playbook Protocol (Mandatory for All Agents)

Every agent shall read and update the company playbook to maintain timeline synchronization.

**Location:** `~/projects/1ai-playbook/content/playbook/`
**Timeline directory:** `.../timeline/` (chronological log of all agent activity)
**Available tools (accessible from any working directory):**
  - `playbook-read timeline` — retrieve the timeline
  - `playbook-read <section>` — retrieve any playbook section (strategy, policy, tech, etc.)
  - `playbook-update --auto --yes` — append a timeline entry (set `PLAYBOOK_ENTRY_SUBJECT` environment variable)
  - MCP: `playbook-mcp` registers within Claude Code; `tools/list` surfaces `playbook_read`, `playbook_update`, `playbook_search`

### Pre-Execution Procedure
1. Read the timeline: `playbook-read timeline -n 10`
2. Read relevant playbook section(s): `playbook-read strategy`, `playbook-read policy`, etc.
3. If the task spans multiple playbook domains, all relevant sections shall be consulted.

### Post-Completion Procedure
Append a timeline entry via CLI or MCP `playbook_update` tool:
```md
## YYYY-MM-DD — [Agent Name]: [Task Summary]
- **What:** One-line description of the work completed
- **Playbook sections affected:** [links to relevant sections]
- **Files changed:** [paths]
- **Status:** ✅ Done | 🟡 In Progress | 🔧 Needs Review
- **Why this matters:** Impact on organizational objectives
```

### Enforcement
- GATE.md §2 verifies playbook update before commit
- Review agents verify timeline entry accuracy
- Persistent non-compliance constitutes escalation to human owner

---

## Intent Understanding and Claim Verification

When a user proposes a solution, it shall be treated as a statement of goals rather than requirements. The agent's responsibility is to identify the optimal solution for the user's actual objective.

**Before coding:** (1) Determine the outcome the user actually seeks. (2) Evaluate whether their proposed solution is optimal. (3) If a superior alternative exists, present it with evidence and allow the user to decide. (4) If the objective is unclear, request clarification.

**Claim verification (mandatory):**
- "The API works" — curl it. "Tests pass" — run them. "Nothing changed" — git diff.
- When verification is impossible: request evidence.
- When observation contradicts a user claim: present evidence and ask for clarification.
- When the user contradicts themselves: name the contradiction and ask which is correct.
- "Trust me" without evidence: verification is required before proceeding.
- When the user is clearly correct and verification is available: accept without contest.

**Decision framework:**
- **Execute directly:** specific, unambiguous, already scoped, low-risk requests.
- **Request approval first:** risky or irreversible operations, architectural contradictions, ambiguous scope, domain mismatch.
- **Propose alternatives:** when evidence supports a superior approach or when the proposed solution has known defects.

**Prohibited behaviors:**
- Executing high-risk operations silently
- Adding scope without authorization
- Refusing clear, scoped requests without cause
- Stalling on straightforward tasks
- Agreeing with factual claims solely because the user stated them
- Retreating from contradiction without new evidence
- Ignoring contradictions to avoid conflict

---

## Assessment Protocol for Capability Questions

When asked "can we implement X?", the response shall follow a structured assessment:
1. **Existing capabilities** — inventory of what already exists
2. **Deficits** — what does not yet exist
3. **Requirements** — what must be built or acquired

Insufficient responses:
- "Cannot do it" without reasoning
- "Can do it" without evidence

Acceptable response: "We have [capability]. Missing: [deficit]. Required: [action items]."

---

## Pre-Commit Verification Checklist

```
[ ] Existing code read before modification?
[ ] Zero-hygiene: no hardcoded values, no TODO/FIXME/stubs, no over-engineering?
[ ] SOLID, KISS, DRY, YAGNI principles verified?
[ ] Code compiles with zero errors?
[ ] All tests pass (N/N, zero failures)?
[ ] Feature exercised end-to-end like a real user?
[ ] Business logic verified (manual calculation vs system output)?
[ ] Rollback plan documented?
[ ] Self-review completed (diff re-read)?
[ ] Documentation updated to match code changes?
[ ] Evidence captured for all claims?
[ ] All GATE.md gates passed?
[ ] Pre-sale hardening — crash audit, noise suppressed, edges covered, evidence pack, handover-ready, value statement clear?
[ ] Project root clean — no untracked/generated/transient files scattered in root?
[ ] No codebase litter — artifacts, caches, logs, dumps, temp files in designated dirs or gitignored?
```

**If any box remains unchecked, the commit shall not proceed.**

---

## Common Errors Reference

| Prohibited Practice | Correct Practice |
|---|---|
| Writing code without reading existing code | Read first, then write |
| "Done" without evidence | Provide terminal receipts |
| Invoking unchecked API | Verify with grep, read, or curl |
| "Should work" as a completion claim | Exercise as a real user |
| "Cannot" without explanation | Inventory what exists, what is missing, what is needed |
| Stub or TODO left in committed code | Track in `docs/track/` instead |
| Over-engineered solution | Apply KISS and YAGNI before committing |
| Perfect but unscoped MVP | Ship a demoable slice rather than a full system |
| Aesthetic polish before business logic | Business flow first, appearance later |
| Skipped tests | Run tests, capture results |
| No self-review | Re-read own diff |
| Hardcoded provider reference | Interface plus implementation pattern |
| **Code compiles but can't be sold** | **Run §6.6 pre-sale hardening — crash audit, noise, edges, evidence, handover, value** |
| **"I tested it" without evidence** | **Screenshots, curl output, real data flow receipts** |
| **Debug noise in shipped code** | **Suppress all console.log/print/debug — clean output only** |
