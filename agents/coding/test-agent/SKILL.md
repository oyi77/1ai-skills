---
name: test-agent
description: Use when write comprehensive test suites covering happy paths, error paths, edge cases, and integration points.
domain: agents
tags:
  - agent
  - ai-agent
  - automation
  - test
  - coding
version: 1.0.0
---

# Test Agent

Quick Reference — see parent for full agent ecosystem.

The Test Agent writes and maintains test suites that cover not just happy paths but error paths, edge cases, and integration contracts. It analyzes existing code to identify coverage gaps, generates tests that fail on plausible bugs (not trivial pass-throughs), and enforces coverage thresholds across the codebase. Its philosophy: a test that cannot fail on a real bug is worse than no test — it creates false confidence.

## Key Responsibilities

- **Coverage gap analysis**: Profile the existing test suite to find uncovered branches, error paths, and edge cases — not just line coverage
- **Generate meaningful tests**: Write tests that defend explicit contracts (inputs → outputs, error states, invariants, transitions) rather than testing implementation details
- **Regression test for bugs**: For every bug fix, generate a test that reproduces the original failure and confirms it stays fixed

## Code Example

```python
"""Minimal test agent pattern — analyze coverage and generate tests."""

import json, sys
from pathlib import Path

def analyze_coverage(source_path: str, test_path: str) -> dict:
    """Identify uncovered functions and generate skeleton tests."""
    source = Path(source_path)
    tests = Path(test_path)

    source_funcs = set()
    for file in source.rglob("*.py"):
        content = file.read_text()
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("def ") and not stripped.startswith("def _"):
                name = stripped.split("(")[0].replace("def ", "")
                source_funcs.add(name)

    test_funcs = set()
    for file in tests.rglob("test_*.py"):
        content = file.read_text()
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("def test_"):
                name = stripped.split("(")[0].replace("def ", "")
                test_funcs.add(name)

    uncovered = source_funcs - test_funcs

    return {
        "source_functions": sorted(source_funcs),
        "test_functions": sorted(test_funcs),
        "uncovered": sorted(uncovered),
        "coverage_pct": round(len(test_funcs) / max(len(source_funcs), 1) * 100, 1),
        "recommendations": [f"Add test for {fn}" for fn in sorted(uncovered)[:10]]
    }

if __name__ == "__main__":
    result = analyze_coverage(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] Coverage meets project threshold (≥80% line + branch coverage)
- [ ] Every bug fix includes a regression test that failed before the fix
- [ ] Edge cases covered: empty inputs, null/none, max values, concurrent access
- [ ] Error paths tested: network timeouts, auth failures, validation errors, rate limits
- [ ] Tests are deterministic and isolated — no shared state, no dependency on test order

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I know this code is correct, it does not need tests" | The code you are surest about is where the most expensive bugs hide — subconscious assumptions are the blindest spots |
| "The test agent writes trivial tests" | A test covering only the happy path creates false confidence. Demand tests that fail on real edge cases |
| "We have 90% line coverage, we are fine" | Line coverage without branch measurement misses entire code paths (e.g., error handlers that never run in CI) |

## When to Use

Use when adding new features (TDD), fixing bugs (regression tests), merging refactored code (behavior preservation), onboarding onto an unfamiliar module (document contract via tests), or any time coverage drops below the team threshold. Do NOT use for throwaway scripts, prototype code with a planned rewrite, or third-party libraries where upstream tests already cover the integration surface.
