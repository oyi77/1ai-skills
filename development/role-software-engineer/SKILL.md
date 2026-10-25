---
name: role-software-engineer
description: Use when orchestrating end-to-end software engineering workflows covering
  bug triage, test-driven development, concurrency audits, API contracts, code reviews,
  and safe refactoring.
domain: development
author: oyi77
version: 1.0.0
category: development
tags:
- development
- software-engineering
- tdd
- code-review
- debugging
- architecture
license: MIT
subdomain: software-engineering
---

## Overview

The `role-software-engineer` skill serves as the principal operational router and composite orchestrator for production software engineering tasks. Instead of accumulating generic implementation boilerplate into a monolithic document, this role enforces a strict 5-phase engineering state machine and deterministically dispatches specialized execution to verified child skills in the repository.

```
[Phase 1: Triage & Root Cause] ──► [Phase 2: Invariants & Plan] ──► [Phase 3: TDD Execution]
                                                                            │
      [Phase 5: Delivery & Review] ◄── [Phase 4: Empirical Gates] ◄─────────┘
```

The role guarantees that every code modification is backed by a reproducing test failure before touching production code, preserves architectural layer boundaries, verifies API contract parity, and eliminates unverified claims through empirical execution receipts.

## When to Use

- When assigned complex software engineering tasks requiring multi-step coordination across debugging, implementation, and review.
- When fixing regressions or production incidents where the root cause must be isolated before editing code.
- When refactoring legacy components, decomposing god-files, or cleaning up dead code paths.
- When implementing new endpoints or database schemas requiring API contract and zero-downtime guarantees.
- When performing pre-merge code review and concurrency race audits on critical paths.

## When NOT to Use

- When performing isolated exploratory bug bounty scans without code access (use `cybersecurity/role-penetration-tester`).
- When conducting pure cloud infrastructure provisioning with no application code (use `devops/role-devops-sre-engineer`).
- When designing high-level product requirements or user stories from scratch (use `operations/role-product-manager`).
- When performing visual-only design token audits or CSS typography tuning (use `content/role-ui-ux-designer`).

## Deterministic Dispatch Matrix

| Problem Condition / Operational Phase | Delegated Child Skill | Primary Artifact / Output |
|---|---|---|
| Unknown root cause, silent failure, or runtime error | `development/systematic-debugging` | Isolated trace, single concrete cause, and proof |
| Reproducing bug, regression, or defect fix | `development/tdd-bug-reproduction` | Failing regression test (Red) before fix (Green) |
| Shared mutable state, async workers, connection pools | `development/concurrency-race-audit` | Mutex synchronization, race-free transaction proof |
| Client-server drift, OpenAPI diff, payload mismatch | `development/api-contract-drift-audit` | Schema parity report and contract test suite |
| Unsafe types, `any` abuse, blind casting | `development/type-narrowing-audit` | Discriminated unions, Zod/Pydantic runtime guards |
| Dead endpoints, unmounted routers, unused functions | `development/dead-code-graveyard` | Quarantine audit and zero-regression deletion proof |
| Final pull request audit and security sweep | `development/code-reviewer` | Line-by-line diff review and empirical test receipt |

## Workflow

### Phase 1: Problem Triage & Root Cause Isolation

1. Enforce anti-speculation rules: Never guess or output bulleted possibilities.
2. Formulate minimal reproduction command isolating input state, environment, and error output.
3. If root cause is obscure, dispatch immediately to `development/systematic-debugging`.

### Phase 2: Invariant Specification & Implementation Plan

1. Map trust boundaries, affected interfaces, and database constraints.
2. Check for sibling routes or handlers sharing the defect pattern to prevent single-instance fixes.
3. Formulate minimal surgical diff plan adhering to YAGNI (Level 1: Delete; Level 2: Stdlib; Level 3: Installed deps).

### Phase 3: Red-Green-Refactor Execution

1. Write the isolated reproducing test first via `development/tdd-bug-reproduction`.
2. Execute the test suite to observe explicit failure (Red confirmation).
3. Apply the minimal implementation diff to make the test pass (Green confirmation).
4. If modifying shared types or async handlers, dispatch to `development/type-narrowing-audit` or `development/concurrency-race-audit`.

### Phase 4: Empirical Quality Gates

1. Run full type checking (`tsc --noEmit` or `mypy --strict`).
2. Run full test suite with coverage assertions (`pytest` or `npm test`).
3. Audit sibling callers to verify zero downstream regressions.

### Phase 5: Code Review & Delivery

1. Perform self-review of unified diff using `development/code-reviewer`.
2. Confirm zero dead code or debug comments remain in source files.
3. Emit execution receipt with command exit codes, test counts, and verified status.

## Anti-Rationalization

| Shortcut / Excuse | Flawed Rationalization | Required Engineering Behavior |
|---|---|---|
| "The bug is obvious, no test needed" | "Writing a test takes longer than the one-line fix." | Write failing test first. Every fix without a test will regress within 6 months. |
| "It works on my machine" | "Local curl succeeded, so CI will be fine." | Execute automated hermetic test suite with clean state and record exact receipt. |
| "I'll clean up the types later" | "Using `any` gets the feature out the door faster." | Apply runtime type narrowing and schema validation immediately. |
| "Only this function is affected" | "No need to check sibling handlers." | Audit every caller and sibling route sharing the pattern across the repository. |
| "Delete the old route silently" | "Nobody is using that v1 endpoint anymore." | Dispatch to `development/dead-code-graveyard` for access verification and safe deprecation. |

## Implementation Examples

### Automated Engineering Dispatcher (Python)

```python
import sys
from typing import Dict, List, Optional

class SoftwareEngineerRouter:
    """Deterministic skill dispatcher for Software Engineering tasks."""
    
    DISPATCH_TABLE: Dict[str, str] = {
        "bug_fix": "development/tdd-bug-reproduction",
        "root_cause_unknown": "development/systematic-debugging",
        "concurrency_issue": "development/concurrency-race-audit",
        "contract_mismatch": "development/api-contract-drift-audit",
        "unsafe_types": "development/type-narrowing-audit",
        "dead_code": "development/dead-code-graveyard",
        "pre_merge_review": "development/code-reviewer",
    }
    
    def dispatch(self, issue_type: str, context: Dict[str, str]) -> str:
        skill = self.DISPATCH_TABLE.get(issue_type)
        if not skill:
            raise ValueError(f"Unknown issue type: {issue_type}")
        
        print(f"[ENGINEER ROLE] Dispatching task '{context.get('title')}' -> {skill}")
        return skill

if __name__ == "__main__":
    router = SoftwareEngineerRouter()
    target_skill = router.dispatch(
        issue_type="bug_fix",
        context={"title": "Fix payment idempotency token race condition"}
    )
    assert target_skill == "development/tdd-bug-reproduction"
    print("Software Engineer dispatcher routing verified.")
```

### Red-Green-Refactor Verification Script (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

TEST_FILE="tests/test_regression.py"
echo "=== Step 1: Running Regression Test (Expect Red) ==="
if pytest "$TEST_FILE" -q; then
    echo "ERROR: Test passed before fix! Reproduction invalid."
    exit 1
else
    echo "SUCCESS: Test reproduced failure cleanly."
fi

echo "=== Step 2: Applying Minimal Fix ==="
# Fix applied here...

echo "=== Step 3: Re-running Regression Test (Expect Green) ==="
pytest "$TEST_FILE" -q --tb=short
echo "SUCCESS: Fix verified. 100% tests passing."
```

## Verification Checklist

- [ ] Problem definition isolated with concrete reproduction trace before code modification.
- [ ] Reproducing test created and verified failing (Red state confirmed).
- [ ] Minimal surgical diff applied to resolve root cause without unrequested abstractions.
- [ ] Sibling files audited to eliminate similar vulnerabilities across the codebase.
- [ ] Full automated test suite passes with zero regressions.
- [ ] Code review completed with empirical execution receipt documented.
