---
name: browser-testing-devtools
description: Test web applications using browser DevTools, Playwright, or Puppeteer. Automate E2E testing, visual regression, performance auditing, and accessibility checking.
domain: development
tags:
- testing
- browser
- devtools
- playwright
- e2e
- accessibility
---

# Browser Testing Devtools

## When to Use
**Trigger phrases:**
- "browser testing devtools"
- "Test web applications using browser DevTools, Playwright, or Puppeteer"


- When testing web application user flows
- When debugging frontend issues with DevTools
- When automating visual regression testing
- When auditing web performance (Core Web Vitals)

## When NOT to Use

- For unit testing (use Jest/Vitest)
- For API testing (use Postman/httpie skills)

## Overview

Browser-based testing using Playwright for E2E automation, DevTools for debugging, and Lighthouse for performance/accessibility auditing.

## Workflow

1. **Choose tool** - Playwright (E2E), Puppeteer (scraping), DevTools (debug)
2. **Write test** - User flow as code (navigate, click, assert)
3. **Add assertions** - Element visibility, text content, network requests
4. **Visual regression** - Screenshot comparison
5. **Performance audit** - Core Web Vitals, bundle size
6. **Accessibility audit** - WCAG violations, color contrast

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual testing is enough" | Humans miss regressions. Automated tests catch them every time. |
| "E2E tests are too slow" | Modern Playwright runs parallel tests in seconds |
| "I will test in production" | Production testing means production bugs. Test before deploy. |

## Code Example (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('user can login and see dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name=email]', 'user@example.com');
  await page.fill('input[name=password]', 'password123');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toHaveText('Welcome back');
});
```

## Verification

- [ ] Tests run in CI pipeline
- [ ] Visual regression baselines updated
- [ ] Performance budget enforced (LCP < 2.5s)
- [ ] Accessibility audit passes (0 violations)

