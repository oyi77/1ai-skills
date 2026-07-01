---
name: cypress-e2e
description: Cypress E2E testing — component testing, API testing, fixtures, custom commands, CI integration. Use when working with cypress e2e.
domain: development
tags:
- api
- coding
- cypress
- e2e
- software-engineering
- testing
---


## Overview

Cypress is a JavaScript end-to-end testing framework that runs in the browser. It provides real-time reloading, automatic waiting, time travel debugging, and built-in assertions. This skill covers E2E testing, component testing, API testing, and CI integration patterns.

## Capabilities

- End-to-end browser testing with real DOM interaction
- Component testing for React, Vue, Angular, Svelte
- API testing and intercepting network requests
- Automatic waiting and retry logic
- Time travel debugging with screenshots/video
- Custom commands for reusable test utilities
- Fixtures for test data management
- Parallel test execution in CI
- Visual regression testing with plugins
- Accessibility testing integration

## When to Use
**Trigger phrases:**
- "cypress e2e"
- "Cypress E2E testing — component testing, API testing, fixtures, custom commands,"


- Testing critical user flows (login, checkout, forms)
- Need visual debugging of test failures
- Testing SPAs with complex async behavior
- Component testing in isolation
- API endpoint testing
- CI/CD pipeline with automated testing

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The cypress-e2e workflow follows a standard pipeline pattern.

Core flow:
```
# cypress-e2e primary flow
input = prepare(raw_data)
result = process(input, config={commands, component, custom, cypress, e2e})
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


### Setup
```bash
npm install cypress --save-dev
npx cypress open  # Opens test runner
npx cypress run   # Headless run
```

### Configuration
```javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    supportFile: 'cypress/support/e2e.js',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    retries: { runMode: 2, openMode: 0 },
    env: {
      apiUrl: 'http://localhost:8080/api',
    },
  },
  component: {
    devServer: { framework: 'react', bundler: 'vite' },
    specPattern: 'cypress/component/**/*.cy.{js,ts}',
  },
});
```

### Basic E2E Tests
```typescript
// cypress/e2e/login.cy.ts
describe('Login', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login with valid credentials', () => {
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="user-menu"]').should('contain', 'user@example.com');
  });

  it('should show error for invalid credentials', () => {
    cy.get('[data-testid="email"]').type('wrong@example.com');
    cy.get('[data-testid="password"]').type('wrongpassword');
    cy.get('[data-testid="submit"]').click();
    cy.get('[data-testid="error"]').should('be.visible').and('contain', 'Invalid credentials');
  });

  it('should validate required fields', () => {
    cy.get('[data-testid="submit"]').click();
    cy.get('[data-testid="email-error"]').should('contain', 'Email is required');
    cy.get('[data-testid="password-error"]').should('contain', 'Password is required');
  });
});
```

### API Interception
```typescript
// Intercept and mock API responses
describe('Dashboard', () => {
  it('should display user data', () => {
    cy.intercept('GET', '/api/user', { fixture: 'user.json' }).as('getUser');
    cy.intercept('GET', '/api/dashboard', { fixture: 'dashboard.json' }).as('getDashboard');
    
    cy.visit('/dashboard');
    cy.wait(['@getUser', '@getDashboard']);
    
    cy.get('[data-testid="user-name"]').should('contain', 'John Doe');
    cy.get('[data-testid="stats"]').should('be.visible');
  });

  it('should handle API errors gracefully', () => {
    cy.intercept('GET', '/api/dashboard', { statusCode: 500, body: { error: 'Server error' } });
    cy.visit('/dashboard');
    cy.get('[data-testid="error-message"]').should('contain', 'Something went wrong');
  });
});
```

### Custom Commands
```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.request({
      method: 'POST',
      url: `${Cypress.env('apiUrl')}/auth/login`,
      body: { email, password },
    }).then((resp) => {
      window.localStorage.setItem('token', resp.body.token);
    });
  });
});

Cypress.Commands.add('getByTestId', (testId: string) => {
  return cy.get(`[data-testid="${testId}"]`);
});

// Usage
cy.login('user@example.com', 'password123');
cy.visit('/dashboard');
cy.getByTestId('user-menu').should('be.visible');
```

### Fixtures
```json
// cypress/fixtures/user.json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin"
}
```

```typescript
cy.fixture('user.json').then((user) => {
  expect(user.name).to.equal('John Doe');
});
```

### Component Testing
```typescript
// cypress/component/Button.cy.tsx
import { Button } from '../../src/components/Button';

describe('Button', () => {
  it('renders correctly', () => {
    cy.mount(<Button variant="primary">Click Me</Button>);
    cy.get('button').should('contain', 'Click Me').and('have.class', 'btn-primary');
  });

  it('calls onClick when clicked', () => {
    const onClick = cy.stub().as('onClick');
    cy.mount(<Button onClick={onClick}>Click</Button>);
    cy.get('button').click();
    cy.get('@onClick').should('have.been.calledOnce');
  });

  it('is disabled when disabled prop is true', () => {
    cy.mount(<Button disabled>Disabled</Button>);
    cy.get('button').should('be.disabled');
  });
});
```

### Page Objects Pattern
```typescript
// cypress/pages/LoginPage.ts
class LoginPage {
  visit() { cy.visit('/login'); }
  fillEmail(email: string) { cy.getByTestId('email').type(email); }
  fillPassword(password: string) { cy.getByTestId('password').type(password); }
  submit() { cy.getByTestId('submit').click(); }
  getError() { return cy.getByTestId('error'); }
  
  login(email: string, password: string) {
    this.visit();
    this.fillEmail(email);
    this.fillPassword(password);
    this.submit();
  }
}

export const loginPage = new LoginPage();

// Usage in test
loginPage.login('user@example.com', 'password123');
cy.url().should('include', '/dashboard');
```

### CI Integration
```yaml
# .github/workflows/cypress.yml
name: Cypress Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run build
      - uses: cypress-io/github-action@v6
        with:
          start: npm run preview
          wait-on: 'http://localhost:3000'
          record: true
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `cy.visit failed` | App not running | Ensure dev server is running on baseUrl |
| `Element not found` | Wrong selector or timing | Use `data-testid` or add `cy.wait` |
| `CORS error` | API CORS misconfig | Configure proxy in cypress.config or server |
| `Test flaky` | Race condition | Use `cy.intercept` + `cy.wait` for API calls |
| `Video recording failed` | Missing ffmpeg | Install ffmpeg or disable video |

## Common Patterns

Proven patterns for cypress-e2e usage.

- **Batch processing**: Process multiple items in parallel for throughput
- **Retry with backoff**: Handle transient failures gracefully
- **Rate limiting**: Respect API limits with configurable delays
- **Logging**: Structured logging for debugging and audit trails


### Testing Forms
```typescript
cy.get('form').within(() => {
  cy.get('input[name="name"]').type('John');
  cy.get('input[name="email"]').type('john@example.com');
  cy.get('select[name="role"]').select('admin');
  cy.get('input[type="file"]').selectFile('fixture.pdf');
  cy.get('button[type="submit"]').click();
});
```

### Testing File Upload
```typescript
cy.get('input[type="file"]').selectFile('cypress/fixtures/test.pdf');
cy.get('[data-testid="upload-status"]').should('contain', 'Upload complete');
```

### Testing with Database
```typescript
// cypress/support/commands.ts
Cypress.Commands.add('seedDatabase', () => {
  cy.task('db:seed');
});

// cypress.config.ts
module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on) {
      on('task', {
        'db:seed'() { /* seed database */ return null; },
      });
    },
  },
});
```

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