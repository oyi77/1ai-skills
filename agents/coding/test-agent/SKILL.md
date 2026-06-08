---
name: test-agent
description: Test Agent. Use when relevant to this domain.
domain: agents
---
# Test Agent

Autonomous test writing agent that creates comprehensive test suites covering happy paths, error paths, edge cases, and integration points. This agent writes tests that catch real bugs, not tests that merely exercise code.

## When to Use

- Writing tests for new features before or after implementation
- Adding missing test coverage for existing code
- Writing regression tests for reported bugs
- Creating integration tests for API endpoints
- Building end-to-end tests for critical user flows
- Improving test coverage metrics (meaningfully, not just line counting)
- Setting up test infrastructure for a new project

## When NOT to Use

- Implementing the code being tested (use `code-agent`)
- Refactoring existing code (use `refactor-agent`)
- Reviewing test quality (use `review-agent`)
- Optimizing test execution speed (use `perf-agent`)
- Linting test files (use `linter-agent`)
- Tests require complex infrastructure setup (use DevOps)
- Code is trivially simple (no test value)
- No clear expected behavior to test against

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. Analyze the Code Under Test

Read the implementation before writing any test:

```markdown
## Code Analysis

Analyze the code under test before writing any tests.

### Public Interface
- [Function/method name] -- [inputs] -> [output] -- [side effects]
- [Function/method name] -- [inputs] -> [output] -- [side effects]

### Error Conditions
- [What happens on null/undefined input]
- [What happens on empty collection]
- [What happens on network failure]
- [What happens on permission denied]

### Dependencies to Mock
- [External service] -- [how it is called]
- [Database] -- [what queries are made]
- [File system] -- [what files are read/written]
```

### 2. Test Strategy

Choose the right test type for each concern:

| Concern | Test Type | Why |
|---------|-----------|-----|
| Pure logic, calculations | Unit test | Fast, isolated, easy to maintain |
| API endpoints, database queries | Integration test | Tests real interactions |
| User workflows, multi-step flows | End-to-end test | Tests the whole system |
| Edge cases, boundary values | Unit test | Targeted, fast to run |
| Error handling, recovery | Unit + Integration | Tests both isolation and real failure modes |
| Performance, load | Performance test | Separate from functional tests |

**Test Pyramid:**
```
        /  E2E  \         Few (5-10 critical flows)
       / -------- \
      / Integration\      Moderate (test boundaries)
     / ------------ \
    /   Unit Tests    \    Many (test every function)
   /__________________ \
```

### 3. Write Unit Tests

Test individual functions with varied inputs:

```python
import pytest
from myapp.calculator import calculate_total

class TestCalculateTotal:
    """Tests for calculate_total function."""

    # Happy path
    def test_simple_addition(self):
        assert calculate_total([10, 20, 30]) == 60

    def test_single_item(self):
        assert calculate_total([42]) == 42

    # Edge cases
    def test_empty_list(self):
        assert calculate_total([]) == 0

    def test_negative_numbers(self):
        assert calculate_total([-10, 20, -5]) == 5

    def test_decimal_precision(self):
        assert calculate_total([0.1, 0.2]) == pytest.approx(0.3)

    def test_large_numbers(self):
        assert calculate_total([10**15, 10**15]) == 2 * 10**15

    def test_zero_values(self):
        assert calculate_total([0, 0, 0]) == 0

    # Error cases
    def test_none_input_raises(self):
        with pytest.raises(TypeError):
            calculate_total(None)

    def test_non_numeric_values_raise(self):
        with pytest.raises(TypeError):
            calculate_total([1, "two", 3])
```

### 4. Write Integration Tests

Test interactions between components:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from myapp.main import app
from myapp.database import get_db

@pytest.fixture
async def client(test_db):
    """Create test client with test database."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
async def test_db():
    """Set up and tear down test database."""
    await create_tables()
    yield
    await drop_tables()

class TestUserAPI:
    async def test_create_user(self, client):
        resp = await client.post("/users", json={
            "name": "Alice",
            "email": "alice@example.com"
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Alice"
        assert "id" in data

    async def test_create_user_duplicate_email(self, client):
        await client.post("/users", json={"name": "Alice", "email": "a@b.com"})
        resp = await client.post("/users", json={"name": "Bob", "email": "a@b.com"})
        assert resp.status_code == 409

    async def test_get_user_not_found(self, client):
        resp = await client.get("/users/nonexistent")
        assert resp.status_code == 404

    async def test_list_users_pagination(self, client):
        for i in range(15):
            await client.post("/users", json={"name": f"User{i}", "email": f"u{i}@test.com"})
        resp = await client.get("/users?limit=10&offset=0")
        assert resp.status_code == 200
        assert len(resp.json()) == 10
```

### 5. Edge Cases Checklist

Every function should be tested against these categories:

```markdown
## Edge Case Categories
- [ ] **Empty input**: null, undefined, empty string, empty array, empty object
- [ ] **Boundary values**: 0, 1, -1, max int, min int, NaN, Infinity
- [ ] **Type mismatches**: string where number expected, array where object expected
- [ ] **Concurrency**: race conditions, simultaneous writes, deadlocks
- [ ] **Large inputs**: 10K items, 1MB strings, deeply nested objects
- [ ] **Special characters**: unicode, emojis, SQL injection strings, HTML tags
- [ ] **Missing dependencies**: service down, file not found, permission denied
- [ ] **Timeout conditions**: slow response, hanging connection, partial data
```

### 6. Test Quality Rules

```markdown
## Test Quality Checklist
- [ ] Each test tests ONE thing (not a god test with 10 assertions)
- [ ] Test names describe the scenario: test_create_user_with_duplicate_email_raises_409
- [ ] Assertions are specific (assertEqual, not assertTrue)
- [ ] Test data is meaningful (not just "test1", "foo", "bar")
- [ ] Tests are independent (no test relies on another test's state)
- [ ] Tests are deterministic (same result every run, no flaky tests)
- [ ] Mocks are used at the boundary (mock external services, not internal logic)
- [ ] Cleanup happens in fixtures/teardown (no leftover state)
```

### 7. Regression Test Pattern

When fixing a bug, write a test that fails before the fix and passes after:

```python
def test_regression_issue_423_duplicate_order_processing():
    """
    Regression test for GitHub issue #423.
    Bug: Orders were processed twice when submitted during high latency.
    Fix: Added idempotency key check before processing.
    """
    order = create_order(items=[{"id": 1, "qty": 2}])

    # Simulate duplicate submission
    result1 = process_order(order.id, idempotency_key="key-123")
    result2 = process_order(order.id, idempotency_key="key-123")

    assert result1.status == "processed"
    assert result2.status == "already_processed"
    assert get_order_count(order.id) == 1  # Not 2
```

## Test Naming Conventions

| Language | Convention | Example |
|----------|-----------|---------|
| Python | `test_<what>_<scenario>_<expected>` | `test_create_user_duplicate_email_returns_409` |
| JavaScript | `it('<expected> when <scenario>')` | `it('returns 409 when email already exists')` |
| Go | `Test_<What>_<Scenario>` | `TestCreateUser_DuplicateEmail` |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know this works, I tested it manually" | Manual testing does not repeat. Automated tests catch regressions every time code changes. |
| "100% coverage means bug-free code" | Coverage measures lines executed, not scenarios tested. A function with one test can have 100% coverage but miss edge cases. |
| "Tests are too slow" | Slow tests are a design problem. Unit tests should be fast. If they are not, your code has too many dependencies. |
| "This code is too simple to test" | Simple code breaks too. And simple tests are fast to write. No excuse. |
| "Testing error paths is not worth it" | Error paths are where production fails. They need more testing than happy paths, not less. |
| "Mocking is too complex" | Complex mocking means complex code. Simplify the code, then the tests become simple. |
| "The test framework is too hard to set up" | Every major language has a 5-minute test setup. pytest, Jest, Go testing -- all trivial. |

## Red Flags

- Tests that pass regardless of implementation (testing the mock, not the code)
- Tests with `sleep()` or timing dependencies (flaky by nature)
- Test functions longer than the code they test (over-complicated test setup)
- Tests that depend on execution order (test interdependence)
- Catching exceptions in tests without asserting the specific exception type
- Tests that test framework behavior instead of application logic
- No tests for error paths (only happy path tested)
- Test data that does not represent realistic inputs

## Verification

After writing tests, confirm:

- [ ] All tests pass (`pytest -v`, `npm test`, `go test ./...`)
- [ ] Happy path covered (normal inputs produce expected outputs)
- [ ] Error paths covered (invalid inputs raise/handle errors correctly)
- [ ] Edge cases covered (empty, null, boundary values, large inputs)
- [ ] Tests are independent (each test passes when run alone)
- [ ] Test names describe the scenario (not just `test_function_1`)
- [ ] No flaky tests (run suite 3 times, all pass every time)
- [ ] Coverage is meaningful (not just hitting lines, but testing scenarios)
- [ ] Regression tests added for any bugs fixed in this session
- [ ] No [TODO] or placeholder assertions in test code
