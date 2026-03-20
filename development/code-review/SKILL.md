---
name: code-review
description: Systematic code review patterns covering security, performance, maintainability, correctness, and testing — with severity levels, structured feedback guidance, and anti-patterns to avoid. Use when reviewing PRs or establishing review standards.
source: https://github.com/LeoYeAI/openclaw-master-skills
---

# Code Review Checklist

Thorough, structured approach to reviewing code. Work through each dimension systematically rather than scanning randomly.

## Review Dimensions

| Dimension | Focus | Priority |
|-----------|-------|----------|
| Security | Vulnerabilities, auth, data exposure | Critical |
| Performance | Speed, memory, scalability bottlenecks | High |
| Correctness | Logic errors, edge cases, data integrity | High |
| Maintainability | Readability, structure, future-proofing | Medium |
| Testing | Coverage, quality, reliability of tests | Medium |
| Accessibility | WCAG compliance, keyboard nav, screen readers | Medium |
| Documentation | Comments, API docs, changelog entries | Low |

## Security Checklist

- [ ] SQL Injection — parameterized statements, no string concatenation with user input
- [ ] XSS — user content escaped/sanitized before rendering
- [ ] CSRF Protection — state-changing requests require valid CSRF tokens
- [ ] Authentication — every protected endpoint verifies auth
- [ ] Authorization — resource access scoped to user's permissions; no IDOR
- [ ] Input Validation — all external input validated server-side
- [ ] Secrets Management — no credentials in source code
- [ ] Dependency Safety — new deps from trusted sources, no known CVEs
- [ ] Sensitive Data — PII/tokens never logged or in error messages
- [ ] Rate Limiting — public/auth endpoints have rate limits
- [ ] File Upload Safety — validated type/size, stored outside webroot
- [ ] HTTP Security Headers — CSP, X-Content-Type-Options, HSTS set

## Performance Checklist

- [ ] N+1 Queries — batched or joined; no loops issuing individual queries
- [ ] Unnecessary Re-renders — memoization applied where measurable
- [ ] Memory Leaks — listeners/subscriptions/timers cleaned up
- [ ] Bundle Size — tree-shakeable deps; no full-library imports for one function
- [ ] Lazy Loading — heavy components use code splitting
- [ ] Caching Strategy — appropriate caching for expensive operations
- [ ] Database Indexing — queries checked with EXPLAIN
- [ ] Pagination — no unbounded SELECT *
- [ ] Async Operations — long tasks offloaded to background jobs

## Correctness Checklist

- [ ] Edge Cases — empty arrays, zero values, negative numbers handled
- [ ] Null/Undefined Handling — nullable values checked before access
- [ ] Off-by-One Errors — loop bounds, pagination offsets verified
- [ ] Race Conditions — shared state uses locks/transactions/atomics
- [ ] Timezone Handling — stored UTC, converted at presentation layer
- [ ] Error Propagation — async errors caught; promises never silently swallowed
- [ ] State Consistency — multi-step mutations are transactional

## Maintainability Checklist

- [ ] Naming Clarity — descriptive names that reveal intent
- [ ] Single Responsibility — each function/class does one thing
- [ ] DRY — duplicated logic extracted into shared utilities
- [ ] Dead Code Removal — commented-out code and unused imports removed
- [ ] Consistent Patterns — follows existing codebase conventions
- [ ] Function Length — short enough to understand at a glance

## Testing Checklist

- [ ] Test Coverage — new logic paths have corresponding tests
- [ ] Edge Case Tests — boundary values, empty inputs, error conditions
- [ ] No Flaky Tests — deterministic; no timing/external service reliance
- [ ] Test Independence — each test manages own state
- [ ] Meaningful Assertions — assert on behavior, not implementation details
- [ ] Regression Tests — bug fixes include test reproducing original bug

## Review Process

| Pass | Focus | Time | What to Look For |
|------|-------|------|------------------|
| First | High-level structure | 2-5 min | Architecture fit, file organization, overall approach |
| Second | Line-by-line detail | Bulk | Logic errors, security, performance, edge cases |
| Third | Edge cases & hardening | 5 min | Failure modes, concurrency, missing tests |

## Severity Levels

| Level | Label | Blocks Merge? |
|-------|-------|---------------|
| Critical | `[CRITICAL]` | Yes — security vuln, data loss, crash |
| Major | `[MAJOR]` | Yes — bug, logic error, perf regression |
| Minor | `[MINOR]` | No — maintenance improvement |
| Nitpick | `[NIT]` | No — style preference |

## Giving Feedback

- Be specific — point to the exact line, explain the issue
- Explain why — state the risk or consequence
- Suggest a fix — offer concrete alternative or code snippet
- Ask, don't demand — use questions for subjective points
- Acknowledge good work — call out clean solutions
- Use severity labels — so author knows what blocks merge

## Review Anti-Patterns

| Anti-Pattern | Description |
|--------------|-------------|
| Rubber-Stamping | Approving without reading |
| Bikeshedding | Debating names while ignoring race conditions |
| Blocking on Style | Refusing to approve over formatting (use a linter) |
| Gatekeeping | Requiring your preferred approach when submitted one is correct |
| Drive-by Reviews | One vague comment then disappearing |
| Scope Creep | Requesting unrelated refactors |
| Stale Reviews | Letting PRs sit for days |
| Emotional Language | Critique the code, not the person |

## NEVER Do

1. NEVER approve without reading every changed line
2. NEVER block a PR solely for style preferences
3. NEVER leave feedback without a severity level
4. NEVER request changes without explaining why
5. NEVER review more than 400 lines in one sitting
6. NEVER skip the security checklist
7. NEVER make it personal
