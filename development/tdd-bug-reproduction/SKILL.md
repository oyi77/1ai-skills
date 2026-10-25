---
name: tdd-bug-reproduction
description: Isolating bugs, writing failing minimal reproduction test cases, and verifying fixes with Test-Driven Development discipline. Use when diagnosing regressions, resolving customer-reported defects, fixing flakiness, or verifying edge case boundaries.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - tdd
  - testing
  - debugging
  - bug-fix
  - regression-test
  - vitest
  - pytest
---

## Overview

Applying fixes directly to production code without first reproducing the failure in an automated test guarantees recurring regressions and incomplete root cause isolation. The TDD Bug Reproduction playbook establishes a disciplined Red-Green-Refactor protocol for defect remediation: isolating the minimal failing state, codifying it into an automated failing regression test, implementing the minimal surgical fix, and proving the fix permanently prevents recurrence.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "The bug is so obvious that writing a test first is a waste of time." | Obvious fixes frequently patch visible symptoms while leaving the fundamental root cause unaddressed, allowing the defect to recur. | Never write a fix before committing or running a failing test that reproduces the defect with an assertion error. |
| "Writing a reproduction test takes too long; we need this in production immediately." | Untested emergency hotfixes often introduce secondary regressions, escalating a minor bug into a critical outage. | A minimal reproduction takes minutes. Isolate the input payload, feed it into a unit test, assert the failure, then fix it. |
| "I manually tested it in my browser/terminal and verified it works." | Manual tests are ephemeral and disappear once your terminal closes. They provide zero protection against future commits breaking the code again. | Codify the manual reproduction into the test suite as a permanent regression test executed by CI on every pull request. |
| "The bug only occurs in production, so it cannot be tested in unit tests." | Any software defect is a deterministic product of state, inputs, and environment. Production conditions can be captured and mocked. | Extract the exact production payload, mock external dependencies, and replicate the failure locally in an automated test. |
| "The existing test suite already passed, so the fix must be solid." | If existing tests passed while the bug existed in production, the test suite had a coverage blind spot that must now be filled. | Add explicit assertion coverage for the exact failing edge condition before declaring the ticket resolved. |
| "We will write the test after deploying the fix." | Post-hoc tests written after the fix is already implemented inevitably suffer from confirmation bias and rarely test edge failure modes. | Red-first is non-negotiable. Watch the test fail with the expected error, apply the code change, and watch it turn green. |

## When to Use

- Triaging and fixing customer-reported bug tickets or production exception alerts (e.g. Sentry, Datadog).
- Fixing unexpected regressions discovered during code review, staging QA, or release testing.
- Debugging edge cases: off-by-one errors, timezone conversions, floating-point arithmetic, or null pointer exceptions.
- Hardening flaky or intermittent test cases against race conditions and non-deterministic behavior.

## When NOT to Use

- External third-party infrastructure outages (e.g. AWS S3 down, Stripe API offline) where application code is functioning correctly.
- Purely cosmetic static text copy updates or documentation spelling adjustments that involve zero executable logic.
- Greenfield exploratory prototyping where no functional specifications or interfaces have stabilized.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│            TDD Bug Reproduction Workflow               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Symptom Isolation & Minimal Case Extraction         │
│    - Extract minimal input vector that triggers bug    │
│    - Strip away unrelated parameters and side-effects  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Failing Regression Test Authoring (RED)             │
│    - Write focused test asserting expected behavior    │
│    - Execute test and verify it FAILS with exact error │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Minimal Surgical Fix Implementation (GREEN)         │
│    - Implement the smallest diff that solves the root  │
│    - Re-run test and verify it PASSES cleanly          │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Boundary & Sibling Pattern Audit (REFACTOR)         │
│    - Fuzz adjacent boundaries (empty, max, null, type) │
│    - Audit sibling routes or functions sharing pattern │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. Full Suite Regression Verification                  │
│    - Run complete project test suite to prevent breaks │
│    - Commit reproduction test and fix atomically       │
└───────────────────────────┘
```

### Step 1: Symptom Isolation & Minimal Case Extraction
Strip away noise from the bug report:
- Extract the smallest possible set of inputs that triggers the bug.
- Eliminate unrelated configuration, extraneous parameters, and database state.
- Create a pure, deterministic input-output pair.

### Step 2: Failing Regression Test Authoring (RED)
Write the test before touching a single line of production code:
- Create or locate the appropriate test file.
- Add a test named explicitly after the scenario (e.g., `test_handles_empty_token_array_without_throwing`).
- Execute the test and confirm:
  1. The test executes.
  2. The test fails (exit code non-zero).
  3. The failure message matches the exact reported bug, not a syntax or import error.

### Step 3: Minimal Surgical Fix Implementation (GREEN)
Implement the fix:
- Modify only the lines necessary to resolve the root cause.
- Avoid unrequested refactoring, premature optimization, or unrelated cleanup.
- Re-run the reproduction test and confirm it passes with 100% certainty.

### Step 4: Boundary & Sibling Pattern Audit (REFACTOR)
Harden the fix and clean up:
- Parameterize the test with adjacent boundary conditions: empty string, `null`, negative numbers, max integer, special characters.
- Audit sibling modules, controllers, or helper functions that implement the same pattern to eradicate the bug class repo-wide.

### Step 5: Full Suite Regression Verification
Verify safety across the entire repository:
- Run the full test suite (`npm test`, `pytest`, `cargo test`).
- Confirm zero collateral regressions in existing tests.
- Commit the failing test and the surgical fix together in a single atomic commit.

## Code Examples

### TypeScript / Vitest Reproduction Cycle

```typescript
// STEP 1 & 2: Author the failing test in tests/date-utils.test.ts (RED)
import { describe, it, expect } from 'vitest';
import { calculateBillingCycleEnd } from '../src/utils/date-utils';

describe('Bug Reproduction: calculateBillingCycleEnd leap year handling', () => {
  it('should correctly handle February 29 in leap years without shifting to March', () => {
    // Input date: Feb 29, 2024 (Leap year)
    const startDate = new Date('2024-02-29T00:00:00Z');
    
    // Expected next billing month: March 29, 2024
    const nextCycle = calculateBillingCycleEnd(startDate, 1);

    expect(nextCycle.toISOString()).toBe('2024-03-29T00:00:00.000Z');
  });

  // Boundary check: Non-leap year subsequent month
  it('should clamp to February 28 when starting on January 31 in a non-leap year', () => {
    const startDate = new Date('2023-01-31T00:00:00Z');
    const nextCycle = calculateBillingCycleEnd(startDate, 1);

    expect(nextCycle.toISOString()).toBe('2023-02-28T00:00:00.000Z');
  });
});
```

### Python / Pytest Parameterized Bug Reproduction

```python
import pytest
from datetime import date
from myapp.billing import add_billing_months

# STEP 1 & 2: Failing reproduction test (RED)
# Bug report: Adding 1 month to Jan 31 returns March 3 due to naive day addition
@pytest.mark.parametrize("start_date, months_to_add, expected_date", [
    (date(2024, 1, 31), 1, date(2024, 2, 29)),  # Leap year clamp
    (date(2023, 1, 31), 1, date(2023, 2, 28)),  # Non-leap year clamp
    (date(2024, 2, 29), 1, date(2024, 3, 29)),  # Exact day match
    (date(2024, 3, 31), 1, date(2024, 4, 30)),  # 30-day month clamp
])
def test_add_billing_months_end_of_month_boundaries(start_date, months_to_add, expected_date):
    result = add_billing_months(start_date, months_to_add)
    assert result == expected_date
```

### Verification Script Protocol (Terminal Execution Proof)

```bash
# 1. Run the new reproduction test and verify FAILURE (Red)
npm test tests/date-utils.test.ts
# Output: FAIL tests/date-utils.test.ts > calculateBillingCycleEnd leap year handling
# Expected: "2024-03-29T00:00:00.000Z", Received: "2024-03-01T00:00:00.000Z"
# Exit code: 1 (CONFIRMED RED)

# 2. Apply surgical fix to src/utils/date-utils.ts

# 3. Re-run reproduction test and verify SUCCESS (Green)
npm test tests/date-utils.test.ts
# Output: PASS tests/date-utils.test.ts (2 tests passed)
# Exit code: 0 (CONFIRMED GREEN)

# 4. Run entire project test suite to verify ZERO collateral damage
npm test
# Output: All 142 tests passed! (CONFIRMED NO REGRESSIONS)
```

## Verification Checklist

- [ ] Minimal reproduction case isolated from customer report or log trace.
- [ ] Automated test authored and committed or staged before changing production code.
- [ ] Test proven to FAIL against unmodified code with the exact expected error symptom (Red verified).
- [ ] Minimal surgical fix applied to address the concrete root cause (Green verified).
- [ ] Adjacent boundary values and edge cases added to the test suite (Refactor verified).
- [ ] Sibling files and handlers audited for identical bug patterns.
- [ ] Full repository test suite passes with zero regressions.
