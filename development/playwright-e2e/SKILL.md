---
name: playwright-e2e
description: End-to-end test automation with Playwright — cross-browser testing, page objects, and CI integration
domain: development
tags:
- coding
- e2e
- playwright
- software-engineering
- testing
---


## Overview

Playwright-based E2E testing for reliable, fast, cross-browser test automation. Covers test design, page object patterns, fixtures, parallel execution, and CI integration.

## Capabilities

- Write cross-browser E2E tests (Chromium, Firefox, WebKit)
- Implement page object pattern for maintainable tests
- Use fixtures for test setup and teardown
- Run tests in parallel for faster feedback
- Generate test reports and trace files for debugging

## When to Use

- Need reliable E2E tests for critical user flows
- Existing Selenium tests are slow and flaky
- Testing across multiple browsers is required
- CI pipeline needs fast, parallel test execution

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The playwright-e2e workflow follows a standard pipeline pattern.

Core flow:
```
# playwright-e2e primary flow
input = prepare(raw_data)
result = process(input, config={automation, browser, cross, e2e, integration})
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


### Page Object Pattern
```typescript
// pages/LoginPage.ts
class LoginPage {
  constructor(private page: Page) {}
  
  async goto() { await this.page.goto('/login') }
  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email)
    await this.page.fill('[data-testid="password"]', password)
    await this.page.click('[data-testid="submit"]')
  }
}

// tests/login.spec.ts
test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto()
  await loginPage.login('user@test.com', 'password')
  await expect(page).toHaveURL('/dashboard')
})
```

### Fixture Pattern
```typescript
// fixtures.ts
const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login')
    await page.fill('[data-testid="email"]', 'user@test.com')
    await page.fill('[data-testid="password"]', 'pass')
    await page.click('[data-testid="submit"]')
    await use(page)
  }
})
```

## Common Patterns

- **data-testid**: Use `data-testid` attributes for stable selectors
- **Page objects**: Encapsulate page interactions in classes
- **Auto-wait**: Playwright auto-waits — avoid manual `waitFor` when possible
- **Trace on failure**: Enable trace recording for debugging CI failures

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

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |