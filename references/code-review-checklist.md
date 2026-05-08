# Code Review Checklist

Shared reference for code review skills. Load this when reviewing code.

## Functionality
- [ ] Code does what it's supposed to do (matches spec/requirements)
- [ ] Edge cases handled (null, empty, max values, boundary conditions)
- [ ] Error handling: graceful degradation, user-friendly messages
- [ ] No silent failures (errors logged, exceptions propagated correctly)
- [ ] Business logic is correct and complete

## Code Quality
- [ ] Readable: variable names are descriptive (no a, b, temp, data)
- [ ] Functions are small (< 30 lines, single responsibility)
- [ ] No deep nesting (> 3 levels of indentation)
- [ ] DRY: no duplicated logic (extract reusable functions)
- [ ] No magic numbers (use named constants)
- [ ] Comments explain "why", not "what" (code should be self-documenting)

## Architecture & Design
- [ ] Follows project patterns and conventions
- [ ] Single Responsibility Principle: class/function does one thing
- [ ] Loose coupling: dependencies injected, not hard-coded
- [ ] High cohesion: related code is grouped together
- [ ] No god objects/functions (break up large components)
- [ ] Design patterns used appropriately (not over-engineered)

## Security
- [ ] No hardcoded secrets (API keys, passwords, tokens in code)
- [ ] Input validation: all user input sanitized
- [ ] SQL injection prevention (parameterized queries, ORM)
- [ ] XSS prevention (output encoding, CSP headers)
- [ ] CSRF protection (tokens, SameSite cookies)
- [ ] Authentication/authorization checks present
- [ ] No sensitive data in logs or error messages
- [ ] Dependency check: no known vulnerabilities (npm audit, pip-audit)

## Performance
- [ ] No N+1 queries (batch database calls)
- [ ] No unnecessary re-renders (React: memo, useMemo, useCallback)
- [ ] Large datasets: pagination or infinite scroll
- [ ] Images optimized (WebP format, lazy loading, proper sizing)
- [ ] No blocking operations in main thread
- [ ] Caching implemented where appropriate (Redis, CDN, browser cache)

## Testing
- [ ] New code has corresponding tests (target: 80%+ coverage)
- [ ] Tests are meaningful (test behavior, not implementation)
- [ ] Edge cases covered in tests
- [ ] Mocks/stubs used appropriately (not over-mocked)
- [ ] Tests are fast (< 1s for unit, < 10s for integration)
- [ ] Test names describe what they verify

## Type Safety & Linting
- [ ] No `any` type in TypeScript (use specific types)
- [ ] No `@ts-ignore` or `@ts-expect-error` without justification
- [ ] Linter passes with no errors or warnings
- [ ] Types are explicit (avoid implicit `any`)
- [ ] Interfaces/types defined for complex objects

## Git & Commit Hygiene
- [ ] Commit messages follow convention (Conventional Commits)
- [ ] Commits are atomic (one logical change per commit)
- [ ] No commented-out code (use version control instead)
- [ ] No debug statements left in (console.log, print, debugger)
- [ ] Diff is reasonable (< 300 lines for reviews)

## Accessibility (if UI)
- [ ] Semantic HTML elements used (nav, button, heading hierarchy)
- [ ] ARIA labels where native HTML insufficient
- [ ] Keyboard navigation works (tab order, focus indicators)
- [ ] Color contrast ratio ≥ 4.5:1 (WCAG AA)
- [ ] Alt text on all images
- [ ] Form inputs have associated labels

## Documentation
- [ ] Public APIs have JSDoc/TSDoc comments
- [ ] Complex logic has explanatory comments
- [ ] README updated if setup/usage changed
- [ ] Breaking changes documented in CHANGELOG

## Severity Labels (Use These in Review Comments)

| Label | Meaning | Action Required? |
|-------|---------|-------------------|
| 🔴 **Critical** | Breaks functionality, security hole, data loss risk | MUST fix before merge |
| 🟠 **Major** | Bug, performance issue, missing error handling | SHOULD fix before merge |
| 🟡 **Minor** | Code smell, readability issue, missing test | Fix soon, can merge with acknowledgement |
| 🔵 **Nit** | Style preference, naming suggestion | Optional, author decides |
| 💡 **FYI** | Alternative approach, interesting pattern, learning | No action required |

## Review Speed Norms
- PRs < 100 lines: review within 4 hours
- PRs 100-300 lines: review within 1 business day
- PRs 300+ lines: request split, or allow 2 business days
- Emergency hotfixes: review within 1 hour
