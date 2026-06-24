---
name: automated-test-generator
description: Generate test suites, analyze coverage, and scaffold E2E tests automatically. Use when creating tests for existing code, improving test coverage, scaffolding integration tests, or setting up E2E test automation for React, Next.js, Node.js, Python, Go, or any project.
domain: development
tags: [test-generation, coverage-analysis, e2e-testing, test-automation, quality-assurance, test-scaffolding]
---

# Automated Test Generator

Generate test suites, analyze code coverage, and scaffold E2E tests automatically. Works across React, Next.js, Node.js, Python, Go, and any project with existing code. Bridges the gap between "write tests manually" and "have no tests at all."

**Source:** Adapted from davila7/claude-code-templates senior-qa skill + alirezarezvani/claude-skills senior-qa

## When to Use

**Trigger phrases:**
- "Generate tests for this code"
- "Improve test coverage"
- "Create test suite"
- "Scaffold E2E tests"
- "Analyze test coverage"
- "Write tests for this module"
- "Set up testing"

**Use cases:**
- Adding tests to existing code that has none
- Improving coverage on critical paths
- Scaffolding E2E test infrastructure
- Generating regression tests before refactoring
- Creating test fixtures and mocks
- Setting up test automation from scratch

**When NOT to use:**
- Writing tests for new code (use `skill://test-driven-development` — write tests first)
- Manual QA testing (use `skill://qa-review-fix-loop`)
- Code review (use `skill://code-reviewer`)

## Process

### Step 1 — Discover the Codebase

Before generating tests, understand the project:

```bash
# Identify language/framework
cat package.json | jq '.dependencies, .devDependencies'
cat pyproject.toml
cat go.mod

# Find existing tests
find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*.py" | head -20

# Check existing test config
ls jest.config.* vitest.config.* pytest.ini setup.cfg .mocharc.* cypress.config.* playwright.config.* 2>/dev/null
```

### Step 2 — Generate Test Suite

Generate unit tests for untested code:

```bash
# For JavaScript/TypeScript projects
node scripts/test_suite_generator.js <src-file-or-dir> \
  --framework jest \
  --coverage \
  --output tests/

# For Python projects
python scripts/test_suite_generator.py <src-file-or-dir> \
  --framework pytest \
  --coverage \
  --output tests/

# Manual approach (no script needed)
# 1. Read the source file
# 2. Identify exported functions/classes
# 3. For each: happy path, edge cases, error cases
# 4. Generate test file with proper imports and mocks
```

**Test generation rules:**
- Every exported function gets at least 3 tests: happy path, edge case, error case
- Mock external dependencies (APIs, databases, file system)
- Test boundary conditions (empty, null, max values)
- Test error handling (what happens when things fail)
- Use descriptive test names that explain the scenario

### Step 3 — Analyze Coverage

```bash
# JavaScript/TypeScript
npx jest --coverage --coverageReporters=text-summary
npx vitest run --coverage

# Python
pytest --cov=src --cov-report=term-missing

# Go
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

**Coverage targets:**
- Statements: ≥80%
- Branches: ≥75%
- Functions: ≥80%
- Lines: ≥80%

**Focus on critical paths first:**
1. Authentication/authorization
2. Payment/financial logic
3. Data validation
4. Error handling
5. API endpoints

### Step 4 — Scaffold E2E Tests

```bash
# Playwright (recommended for web)
npx playwright test --generate

# Cypress
npx cypress open

# Puppeteer-based
node scripts/e2e_test_scaffolder.js <url> --output e2e/
```

**E2E test priorities:**
1. Critical user journeys (signup, login, checkout)
2. Form submissions with validation
3. Navigation flows
4. Error states and recovery
5. Mobile/responsive views

### Step 5 — Generate Test Fixtures

```bash
# Generate mock data from TypeScript types
npx ts-auto-mock create --types src/types.ts

# Generate fixtures from API responses
node scripts/fixture_generator.js --from-api https://api.example.com/users --output fixtures/

# Generate from database schema
node scripts/fixture_generator.js --from-schema prisma/schema.prisma --output fixtures/
```

## Coverage Analysis Report

Generate a coverage report:

```
LAYER: <module-name>
Test framework:     jest | pytest | vitest | go test
Statements:         85% (target: 80%) ✅
Branches:           72% (target: 75%) ⚠️
Functions:          90% (target: 80%) ✅
Lines:              83% (target: 80%) ✅

Untested critical paths:
- src/auth/validate.ts:45 — token refresh logic
- src/payments/process.ts:112 — refund handling

Recommendations:
1. Add tests for token refresh edge cases
2. Mock Stripe API for refund tests
3. Add integration tests for payment flow
```

## Tech Stack Support

| Stack | Unit Tests | Integration | E2E |
|-------|-----------|-------------|-----|
| React/Next.js | Jest, Vitest | Testing Library | Playwright, Cypress |
| Node.js/Express | Jest, Vitest | Supertest | Playwright |
| Python/FastAPI | pytest | httpx | Playwright |
| Go | go test | httptest | Playwright |
| Vue/Nuxt | Vitest | Vue Test Utils | Playwright |

## Verification

After generating tests, confirm:

- [ ] Tests actually run and pass (`npm test` / `pytest` / `go test`)
- [ ] Coverage meets targets (≥80% statements, ≥75% branches)
- [ ] Critical paths are covered (auth, payments, data validation)
- [ ] Tests are isolated (no shared state between tests)
- [ ] Mocks are appropriate (mock external deps, not internal logic)
- [ ] Test names are descriptive (explain the scenario, not just the function)
- [ ] E2E tests cover critical user journeys

## Related Skills

- `skill://test-driven-development` — Write tests before code (TDD)
- `skill://qa-review-fix-loop` — Full QA cycle with layer-based testing
- `skill://code-reviewer` — Code review process
- `skill://verification-before-completion` — Pre-completion checklist
- `skill://engineering-hard-rules` — Engineering enforcement protocol
- `skill://systematic-debugging` — Debug failing tests
