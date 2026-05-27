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

## Pseudo Code

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
