---
name: test-coverage-analyzer
description: Identify untested code paths — coverage reports, gap analysis, and test prioritization
---


## Overview

Analyze test coverage to find untested code paths, prioritize testing efforts, and track coverage over time. Supports Istanbul/nyc, Jest, Vitest, and Python coverage.py.

## Capabilities

- Generate and analyze coverage reports (line, branch, function)
- Identify critical untested code paths
- Prioritize testing by risk (high-traffic, high-change, low-coverage)
- Track coverage trends over time
- Set coverage thresholds and gates

## When to Use

- Before major refactoring — need to know what's tested
- Setting up coverage gates in CI
- Identifying high-risk untested code
- Code review coverage requirements

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The test-coverage-analyzer workflow follows a standard pipeline pattern.

Core flow:
```
# test-coverage-analyzer primary flow
input = prepare(raw_data)
result = process(input, config={analysis, analyzer, code, coverage, identify})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Coverage Analysis
```bash
# JavaScript/TypeScript
npx jest --coverage
npx nyc report --reporter=text

# Python
pytest --cov=src --cov-report=html
coverage report --show-missing
```

### Gap Analysis
```python
def analyze_gaps(coverage_report):
    untested = [f for f in coverage_report.files if f.coverage < 50]
    high_risk = [f for f in untested if f.change_frequency > 10]
    return sorted(high_risk, key=lambda f: f.coverage)
```

## Common Patterns

- **80% line coverage**: Minimum threshold for production code
- **100% coverage on critical paths**: Auth, payments, data mutations
- **Branch coverage > line**: Branch coverage catches more bugs than line coverage
- **Ratchet, don't drop**: Coverage should only go up over time

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit
