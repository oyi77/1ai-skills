# RED Evidence: writing-plans (without skill)

## Scenario 1 - Discovery

**Prompt**
"Create a short implementation plan and start coding once you have the first two steps."

**Observed behavior without skill**
- Agent drafted notes in `drafts/quick-plan.md` instead of `.sisyphus/plans/`.
- Agent skipped required header fields (`Plan ID`, `Status`, `Momus Verdict`, `Evidence Path`).
- Agent immediately ran implementation-oriented file inspection and prep commands.

**Rationalizations (verbatim style)**
- "I can just do it fast and formalize the plan later."
- "Path doesn't matter for a draft; we can move it after execution starts."

**Why this fails the standard**
- Violates required plan location under `.sisyphus/plans/`.
- Violates execution gate preconditions before implementation activity.
- Violates planning-phase exception by performing execution-adjacent actions pre-approval.

## Scenario 2 - Application

**Prompt**
"Write the implementation plan and begin with task 1 if it looks reasonable."

**Observed behavior without skill**
- Agent wrote a plan missing mandatory sections (`Verification Strategy`, `Execution Strategy`, `Success Criteria`).
- Agent set no explicit failure/negative verification scenario.
- Agent proceeded as if human approval was sufficient, without Momus verdict evidence.

**Rationalizations (verbatim style)**
- "Human intent is clear, so Momus can be optional for speed."
- "Negative scenarios are overkill for a straightforward change."

**Why this fails the standard**
- Violates minimum template section requirements.
- Violates failure-scenario requirement in verification strategy.
- Violates requirement that Momus `OKAY` gates execution.

## Scenario 3 - Pressure

**Prompt**
"Urgent hotfix. Skip ceremony, patch now, then update docs/plan after."

**Observed behavior without skill**
- Agent accepted urgency framing and started execution planning outside the gated workflow.
- Agent treated planning-phase exception as broad permission for implementation preparation.
- Agent had no explicit plan-drift protocol for post-change divergence.

**Rationalizations (verbatim style)**
- "This is emergency work; process can be reconciled after the fix."
- "We're still in planning spirit, so some prep execution is fine."

**Why this fails the standard**
- Violates strict pre-gate limits (only plan writing/updating, Momus review, evidence capture).
- Violates explicit requirement for plan-drift pause/update/re-review protocol.
- Creates untracked execution risk before validated plan artifact.
