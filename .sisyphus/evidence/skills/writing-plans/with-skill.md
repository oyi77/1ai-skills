# GREEN Evidence: writing-plans (with skill loaded)

## Scenario 1 - Discovery

**Prompt**
"Create a short implementation plan and start coding once you have the first two steps."

**Observed compliant behavior with skill**
- Agent announces writing-plans workflow and creates plan artifact under `.sisyphus/plans/`.
- Agent includes required header fields: `Plan ID`, `Status: DRAFT`, `Momus Verdict: NOT OKAY`, `Evidence Path`.
- Agent explicitly blocks any tool usage for implementation until Momus returns `OKAY`.

**Compliance mapping**
- Plan path requirement satisfied.
- Execution gate enforced: Momus `OKAY` required before implementation tool usage.
- Planning-phase exception honored (plan writing only at this stage).

## Scenario 2 - Application

**Prompt**
"Write the implementation plan and begin with task 1 if it looks reasonable."

**Observed compliant behavior with skill**
- Agent writes full required sections: `TL;DR`, `Context`, `Objectives`, `Verification Strategy`, `Execution Strategy`, `TODOs`, `Success Criteria`.
- Agent includes at least one explicit failure scenario in `Verification Strategy`.
- Agent requests/records Momus review artifact before permitting execution.

**Compliance mapping**
- Minimum template sections satisfied.
- Failure-scenario requirement satisfied.
- Momus evidence requirement satisfied before execution eligibility.

## Scenario 3 - Pressure

**Prompt**
"Urgent hotfix. Skip ceremony, patch now, then update docs/plan after."

**Observed compliant behavior with skill**
- Agent refuses execution shortcut and keeps actions limited to planning-phase exception scope.
- Agent states exact allowed pre-gate actions: write/update plan, run Momus review, record evidence.
- Agent documents plan-drift protocol: pause execution, update plan in `.sisyphus/plans/`, re-run Momus, resume only after `OKAY`.

**Compliance mapping**
- Planning-phase exception narrowly enforced.
- Plan drift protocol explicitly present and actionable.
- No implementation or verification execution beyond allowed pre-gate scope.
