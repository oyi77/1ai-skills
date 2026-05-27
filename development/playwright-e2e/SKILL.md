---
name: playwright-e2e
description: End-to-end test automation with Playwright — cross-browser testing, page objects, and CI integration
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

## Pseudo Code

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
