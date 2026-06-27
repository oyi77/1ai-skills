---
name: agentic-quality-engineering
description: AI-powered quality engineering with flaky test detection, mutation testing, chaos engineering, risk-based test prioritization, and cross-project pattern learning. Use when building quality.
domain: development
tags: 
- [quality-engineering
- flaky-tests
- mutation-testing
- chaos-engineering
- risk-based-testing
- pattern-learning
- test-automation]
---

# Agentic Quality Engineering

AI-powered quality engineering beyond traditional testing. Covers flaky test detection, mutation testing, chaos engineering, risk-based prioritization, contract testing, and cross-project pattern learning. Coordinates specialized QA agents for comprehensive quality coverage.

**Source:** Adapted from proffesor-for-testing/agentic-qe — 60 QE agents, 75 skills, MCP server

## Overview

**Agentic Quality Engineering** applies software quality practices to AI agent systems — test strategies for LLM outputs, evaluation harnesses, regression detection, and quality metrics specific to autonomous agents.


## When to Use

**Trigger phrases:**
- "Detect flaky tests"
- "Run mutation testing"
- "Chaos engineering"
- "Risk-based test prioritization"
- "Quality engineering pipeline"
- "Test effectiveness validation"
- "Contract testing"
- "Coordinate QA agents"
- "Pattern learning for tests"

**Use cases:**
- Detecting and stabilizing flaky tests in CI/CD
- Validating test suite effectiveness with mutation testing
- Building resilience through chaos engineering
- Prioritizing tests by risk and impact
- Learning test patterns across projects
- Coordinating multiple QA specialists
- Quality gate enforcement with anti-sycophancy checks

**When NOT to use:**
- Writing initial tests (use `skill://test-driven-development`)
- Manual QA cycles (use `skill://qa-review-fix-loop`)
- Simple test generation (use `skill://automated-test-generator`)
- Code review (use `skill://code-reviewer`)


## When NOT to Use

- For throwaway prototypes (skip the ceremony)
- When the fix is a single-line change with no side effects
- When the codebase already has a working solution


## Process

### 1. Flaky Test Detection & Stabilization

Identify tests that pass/fail intermittently:

```bash
# Run tests multiple times to detect flakiness
for i in {1..10}; do npm test 2>&1 | tee run-$i.log; done

# Analyze results for inconsistent passes/failures
grep -l "FAIL" run-*.log | wc -l  # how many runs failed?
grep -l "PASS" run-*.log | wc -l  # how many runs passed?
```

**Root cause categories:**

| Cause | Detection | Fix |
|-------|-----------|-----|
| Race conditions | Tests pass in isolation, fail in parallel | Add proper waits, use locks |
| Shared state | Tests fail when run in specific order | Reset state in beforeEach/afterEach |
| Time-dependent | Tests fail at certain times | Mock time, use fixed dates |
| External dependency | Tests fail when API is down | Mock external services |
| Resource exhaustion | Tests fail under load | Clean up resources, add timeouts |

**Stabilization approach:**
1. Reproduce the flake (run in isolation, then in parallel)
2. Identify the root cause category
3. Apply targeted fix (not retry — retry masks the problem)
4. Verify fix across 100 runs
5. Add to flaky test dashboard

### 2. Mutation Testing

Validate that tests actually catch bugs:

```bash
# JavaScript/TypeScript
npx stryker run

# Python
mutmut run

# Java
pitest
```

**Mutation operators:**
- Replace arithmetic operators (+ → -, * → /)
- Negate conditionals (if x → if !x)
- Remove statements (delete lines)
- Change return values
- Modify boundary conditions

**Interpreting results:**

```
Mutation Score: 78%
- Killed mutants: 156 (tests caught these)
- Survived mutants: 44 (tests MISSED these — gaps!)
- No coverage: 12 (untested code)

Survived mutants = test weaknesses. Each survived mutant
represents a bug your tests would NOT catch.
```

**Target:** Mutation score ≥80%. Below that, tests are providing false confidence.

### 3. Chaos Engineering for Testing

Inject faults to test system resilience:

```bash
# Network chaos
tc netem delay 100ms 50ms  # add latency
tc netem loss 5%            # packet loss

# Process chaos
kill -9 $(pgrep service)    # random kill
stress --cpu 4 --timeout 30 # resource exhaustion

# Application chaos
# Inject via middleware/interceptor
```

**Chaos test scenarios:**

| Scenario | Injection | Expected Behavior |
|----------|-----------|-------------------|
| Network latency | Add 200ms delay | Graceful timeout, retry |
| Service unavailable | Return 503 | Circuit breaker activates |
| Database slow | Add 2s query delay | Connection pool handles it |
| Memory pressure | Limit to 512MB | Graceful degradation |
| Random kills | SIGKILL worker | Supervisor restarts it |

**Chaos test checklist:**
- [ ] Each service survives individual failure
- [ ] Cascading failures are contained
- [ ] Monitoring detects anomalies
- [ ] Recovery is automatic
- [ ] Data integrity maintained during chaos

### 4. Risk-Based Test Prioritization

Not all tests are equal. Prioritize by risk:

```
Risk Score = Impact × Likelihood × Detection Gap

Impact:          1-5 (data loss = 5, UI glitch = 1)
Likelihood:      1-5 (frequently used = 5, rarely used = 1)
Detection Gap:   1-5 (no monitoring = 5, full monitoring = 1)
```

**Priority matrix:**

| Risk Score | Priority | Test Frequency |
|------------|----------|----------------|
| 80-125 | Critical | Every commit, E2E |
| 50-79 | High | Every PR |
| 25-49 | Medium | Nightly |
| 1-24 | Low | Weekly |

**Apply to test selection:**
```bash
# Run critical tests first (fastest feedback)
npm test -- --testPathPattern="auth|payment|data"

# Run high-priority on PR
npm test -- --testPathPattern="api|validation|security"

# Run full suite nightly
npm test --coverage
```

### 5. Contract Testing

Validate API contracts between services:

```bash
# Pact (consumer-driven contracts)
npx pact-broker publish ./pacts --consumer-app-version=1.0.0

# OpenAPI validation
npx @stoplight/prism mock openapi.yaml

# GraphQL schema testing
npx graphql-inspector diff old-schema.graphql new-schema.graphql
```

**Contract test strategy:**
1. Consumer defines expected contract
2. Provider verifies it fulfills the contract
3. CI verifies contracts on every change
4. Breaking changes detected before deployment

### 6. Pattern Learning

Learn from test successes and failures across projects:

```
Pattern Storage:
- Successful test patterns → reuse in similar code
- Failed test patterns → avoid in future
- Defect patterns → proactive test generation
- Coverage patterns → gap prediction
```

**Pattern categories:**
- **Test structure patterns**: How to test similar modules
- **Mock patterns**: Effective mocking strategies for common dependencies
- **Assertion patterns**: What to assert for different scenarios
- **Fixture patterns**: Reusable test data setups

### 7. Quality Gate with Anti-Sycophancy

Reject hollow tests that provide false confidence:

```python
# Anti-sycophancy checks
def validate_test_quality(test_file):
    issues = []
    
    # Check for tautological assertions
    if "expect(true).toBe(true)" in test_file:
        issues.append("Tautological assertion — tests nothing")
    
    # Check for empty test bodies
    if re.search(r'it\(.+\)\s*\{\s*\}', test_file):
        issues.append("Empty test body — tests nothing")
    
    # Check for assertion count
    assertion_count = test_file.count("expect(")
    if assertion_count == 0:
        issues.append("No assertions — test cannot fail meaningfully")
    
    # Check for meaningful assertions (not just truthy)
    if "expect(result).toBeTruthy()" in test_file and assertion_count == 1:
        issues.append("Only truthy check — add specific assertions")
    
    return issues
```

**Quality gate criteria:**
- [ ] Mutation score ≥80%
- [ ] No tautological assertions
- [ ] No empty test bodies
- [ ] Coverage ≥80% statements, ≥75% branches
- [ ] No tests that always pass regardless of implementation
- [ ] Critical paths have dedicated test suites

## Agent Coordination

For complex quality engineering, coordinate specialized agents:

```
qe-queen-coordinator
├── qe-test-architect      — test strategy & generation
├── qe-coverage-specialist — gap analysis & prioritization
├── qe-flaky-hunter        — flaky test detection & fix
├── qe-chaos-engineer      — fault injection & resilience
├── qe-security-scanner    — SAST/DAST integration
├── qe-quality-gate        — go/no-go decisions
└── qe-tdd-specialist      — RED-GREEN-REFACTOR cycles
```

**Coordination protocol:**
1. Queen decomposes quality task
2. Spawns domain-specific agents in parallel
3. Agents share findings via memory namespaces
4. Queen synthesizes final recommendation
5. Quality gate enforces thresholds

## Verification

After implementing quality engineering, confirm:

- [ ] Flaky tests detected and stabilized (0 intermittent failures in CI)
- [ ] Mutation score ≥80% (tests actually catch bugs)
- [ ] Chaos tests pass (system survives fault injection)
- [ ] Risk-based prioritization implemented (critical tests run first)
- [ ] Contract tests validate API boundaries
- [ ] Anti-sycophancy checks reject hollow tests
- [ ] Pattern learning captures reusable test strategies

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |

## Related Skills

- `skill://test-driven-development` — TDD workflow
- `skill://automated-test-generator` — Generate tests automatically
- `skill://qa-review-fix-loop` — Full QA cycle
- `skill://test-coverage-analyzer` — Coverage analysis
- `skill://code-reviewer` — Code review
- `skill://engineering-hard-rules` — Engineering enforcement
- `skill://verification-before-completion` — Pre-completion checklist
