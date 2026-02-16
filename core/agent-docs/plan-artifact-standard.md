# Plan Artifact Standard and Momus Contract

## Purpose

Define the canonical artifact contract for plans that gate execution workflows. This standard is mandatory for planning, execution, and completion workflow skills.

## Scope

- Applies to any plan intended for execution by workflow skills.
- Applies to planning and execution activity under `.sisyphus/plans/`.
- Applies to Momus validation before execution.

## Required Plan Location

- The plan artifact MUST be saved under `.sisyphus/plans/`.
- Execution MAY NOT begin from plans outside `.sisyphus/plans/`.

## Required Header Fields

Each plan file MUST include these header fields near the top:

- `Plan ID`: stable identifier for the plan instance.
- `Status`: one of `DRAFT`, `READY`, `IN_PROGRESS`, `BLOCKED`, `DONE`.
- `Momus Verdict`: one of `OKAY` or `NOT OKAY`.
- `Evidence Path`: path to Momus review evidence (for example, `.sisyphus/evidence/<plan-id>/momus-review.md`).

## Momus Output Schema

Momus review output MUST follow this schema:

- `verdict`: `OKAY` or `NOT OKAY`.
- `reasons`: required non-empty list of explicit reasons that justify the verdict.
- `required_fixes`: required list of concrete fixes.
  - For `NOT OKAY`, this list MUST be non-empty.
  - For `OKAY`, this list MAY be empty.

Minimal representation:

```yaml
verdict: OKAY|NOT OKAY
reasons:
  - <required reason 1>
required_fixes:
  - <required fix 1>
```

## Phase Definitions

- `Planning Phase`: creating or updating the plan artifact and obtaining Momus review.
  - Allowed actions: write plan, update plan, run Momus review, capture evidence.
  - No implementation execution.
- `Execution Phase`: implementation work driven by an approved plan.
  - Preconditions: plan exists under `.sisyphus/plans/` and Momus verdict is `OKAY`.

## Execution Gate

Before any implementation execution:

1. Confirm plan file exists in `.sisyphus/plans/`.
2. Confirm latest Momus verdict is `OKAY`.
3. Confirm evidence path exists and points to the latest review.

If any check fails, execution is blocked.

## Planning-Phase Exception

The only allowed pre-gate actions are:

- Writing or updating the plan artifact.
- Running Momus review.
- Recording Momus evidence.

Any implementation or verification execution beyond plan authoring/review is blocked until Momus verdict is `OKAY`.

## Plan Drift Protocol

Plan drift means implementation reality no longer matches the approved plan.

When drift is detected, follow this exact protocol:

1. Pause execution immediately.
2. Update the plan artifact in `.sisyphus/plans/` to reflect new reality.
3. Re-run Momus review on the updated plan.
4. Resume execution only after Momus returns `OKAY` and evidence is updated.

## Minimum Plan Template Sections

Every plan MUST include at least these sections:

- `TL;DR`
- `Context`
- `Objectives`
- `Verification Strategy`
- `Execution Strategy`
- `TODOs`
- `Success Criteria`

## Failure Scenario Requirement

Every plan MUST include at least one explicit negative/failure scenario in its verification strategy (for example, expected failure path, guardrail behavior, or rollback condition).

## Compliance Summary

Execution workflow skills MUST enforce all of the following:

- Plan path under `.sisyphus/plans/`.
- Momus verdict `OKAY` before execution.
- Planning-phase exception only for plan writing and Momus review.
- Plan drift protocol: pause, update plan, re-run Momus, then resume.
