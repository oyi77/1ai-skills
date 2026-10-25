---
name: role-qa-automation-engineer
description: Use when orchestrating end-to-end quality assurance, test automation
  suites, API integration testing, browser E2E flows, coverage auditing, and chaos
  resilience.
domain: development
author: oyi77
version: 1.0.0
category: development
tags:
- qa
- testing
- automation
- playwright
- cypress
- coverage
- quality-engineering
- e2e
license: MIT
subdomain: qa-automation
---

## Overview

The `role-qa-automation-engineer` skill directs comprehensive software verification, test harness construction, and automated regression testing. Rather than treating QA as an afterthought or relying on fragile manual spot-checks, this role orchestrates a multi-tier test pyramid spanning hermetic unit tests, API contract validations, cross-browser E2E journeys, test coverage gap audits, and chaos resilience sweeps.

```
[Phase 1: Test Strategy & Risk Matrix] ──► [Phase 2: Harness & Fixtures] ──► [Phase 3: Multi-Layer Execution]
                                                                                              │
                [Phase 5: Release Certification] ◄── [Phase 4: Flakiness & Chaos Audit] ◄────┘
```

The QA automation engineer enforces zero-unverified-claims, deterministically eliminates flaky tests, and certifies release readiness through machine-verifiable execution reports.

## When to Use

- When building or refactoring automated test suites across unit, integration, and E2E layers.
- When generating comprehensive test fixtures and edge-case test matrices for complex business logic.
- When validating REST/GraphQL APIs against schema specifications, error envelopes, and rate limits.
- When automating web user journeys using Playwright or Cypress with resilient locator strategies.
- When measuring true branch/condition test coverage and isolating untested execution paths.
- When diagnosing flaky tests, timing races, and non-deterministic test failures in CI.

## When NOT to Use

- When fixing internal code implementation bugs or refactoring production code (use `development/role-software-engineer`).
- When conducting penetration testing or hunting for security vulnerabilities (use `cybersecurity/role-security-engineer`).
- When managing CI runner infrastructure or container build pipelines (use `devops/role-devops-sre-engineer`).
- When designing UI design tokens or styling mockups (use `content/role-ui-ux-designer`).

## Deterministic Dispatch Matrix

| Verification Scope / Defect Challenge | Delegated Child Skill | Primary Testing Artifact |
|---|---|---|
| Auto-generating test cases from contracts, schemas, or specs | `development/automated-test-generator` | Parameterized test suite covering edge and boundary cases |
| Validating REST/GraphQL API contracts, envelopes, and status codes | `development/api-testing` | Automated API test suite with hermetic mock fixtures |
| Cross-browser UI testing, headless runs, and visual locators | `development/playwright-e2e` | Headless Playwright specs with resilient auto-waiting |
| Component testing, legacy frontend suites, and DOM interaction | `development/cypress-e2e` | Cypress integration specs and custom command fixtures |
| Live DevTools inspection, network interception, and console audits | `development/browser-testing-devtools` | CDP network traces, console error audits, DOM captures |
| Identifying untested branches, lines, and dead test paths | `development/test-coverage-analyzer` | Coverage delta report and missing-branch test targets |
| Systematic QA audit loops, pre-release certification, bug remediation | `development/qa-review-fix-loop` | Audit ledger, defect fix loop, and release sign-off |
| Flaky test stabilization, mutation testing, and chaos verification | `development/agentic-quality-engineering` | Mutation survival scores and deterministic retry harness |

## Workflow

### Phase 1: Test Strategy & Risk Profiling

1. Identify critical business paths (e.g. checkout, auth, data export, state mutations).
2. Establish the test pyramid allocation (70% Unit, 20% API/Integration, 10% E2E).
3. Dispatch to `development/automated-test-generator` to scaffold edge and boundary case matrices.

### Phase 2: Hermetic Harness & Fixture Setup

1. Isolate test execution from shared external environments (use ephemeral SQLite/PostgreSQL, mock third-party APIs).
2. Wire API contract and integration test suites using `development/api-testing`.
3. Ensure fixtures are immutable and auto-clearing between test runs.

### Phase 3: Browser & End-to-End Automation

1. For modern web applications, scaffold E2E specifications via `development/playwright-e2e`.
2. For legacy or existing Cypress suites, implement flows via `development/cypress-e2e`.
3. Eliminate arbitrary `sleep()` calls; enforce deterministic condition polling and accessibility role selectors (`getByRole`, `getByTestId`).
4. Inspect live browser execution, network traffic, and DOM health using `development/browser-testing-devtools`.

### Phase 4: Coverage Analysis & Flakiness Elimination

1. Measure branch and statement coverage using `development/test-coverage-analyzer`.
2. Target all untested error branches and exception handlers.
3. Apply chaos testing, mutation testing, and race stabilization via `development/agentic-quality-engineering`.
4. Ensure tests pass deterministically 10/10 consecutive runs under parallel contention.

### Phase 5: QA Loop & Release Certification

1. Execute the full end-to-end audit battery using `development/qa-review-fix-loop`.
2. Compile pass/fail telemetry, execution durations, and coverage metrics.
3. Issue formal QA certification receipt before staging or production rollout.

## Anti-Rationalization

| Testing Excuse | Flawed Rationalization | Required QA Discipline |
|---|---|---|
| "E2E tests are too slow, unit tests are enough" | "Unit tests prove each function works in isolation." | Unit tests cannot catch integration drift, broken routes, or hydration mismatches. Maintain a lean, high-value E2E suite. |
| "The test only fails intermittently, it's just CI noise" | "Rerunning the job makes it pass, so it's fine." | Flaky tests hide real concurrency bugs and destroy team trust. Quarantine and fix root cause immediately. |
| "Add `sleep(5000)` to fix the timing issue" | "A 5-second pause ensures the element is loaded." | Arbitrary sleeps slow suites and still fail on slow CI runners. Use explicit condition waits (`waitForSelector`, `expect().toBeVisible()`). |
| "100% line coverage means zero bugs" | "Every line was touched during the test run." | Line coverage without assertion depth is meaningless. Test boundary values, error branches, and edge conditions. |
| "Manual testing is faster for this sprint" | "We will automate the test suite after release." | Unautomated manual tests never get written post-release. Automate regression checks before declaring work done. |

## Implementation Examples

### Automated Test Runner & Flakiness Detector (Python)

```python
import subprocess
import sys
from typing import List

def run_flakiness_check(test_target: str, iterations: int = 5) -> bool:
    """Runs a test target repeatedly to detect non-deterministic flakiness."""
    print(f"=== Starting Flakiness Detection: {test_target} ({iterations} runs) ===")
    
    for i in range(1, iterations + 1):
        print(f"Run {i}/{iterations}...", end=" ", flush=True)
        res = subprocess.run(
            [sys.executable, "-m", "pytest", test_target, "-q"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode != 0:
            print(f"FAILED on run {i}!")
            print(f"Error output:\n{res.stdout}\n{res.stderr}")
            return False
        print("PASSED")
        
    print(f"SUCCESS: {test_target} passed {iterations}/{iterations} runs deterministically.")
    return True

if __name__ == "__main__":
    test_target = "tests/test_api_contract.py"
    # Example invocation: run_flakiness_check(test_target)
    print("Flakiness detection framework initialized.")
```

### Headless Playwright Test Script (Bash/Node)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Executing Playwright E2E Suite ==="
npx playwright test --project=chromium --reporter=list

echo "=== Auditing Test Coverage ==="
npm run test:coverage -- --coverageReporters="text-summary"
```

## Verification Checklist

- [ ] Critical business user flows mapped to automated test scenarios.
- [ ] API integration tests validate response payloads, status codes, and error envelopes.
- [ ] Browser E2E specs use resilient accessibility selectors without arbitrary time sleeps.
- [ ] Test coverage measured with zero uncovered critical error branches.
- [ ] Flaky test detection executed with 100% deterministic passes across consecutive runs.
- [ ] Formal QA execution report compiled with pass counts and timing receipts.
