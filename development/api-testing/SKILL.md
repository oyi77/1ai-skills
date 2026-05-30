---
name: api-testing
description: REST and GraphQL API testing — contract testing, schema validation, and integration test automation
---


## Overview

API testing for REST and GraphQL endpoints. Covers contract testing, schema validation, authentication testing, error handling, and performance assertions.

## Capabilities

- Write API contract tests for REST and GraphQL
- Validate response schemas and status codes
- Test authentication and authorization flows
- Check rate limiting and error handling
- Automate API regression testing in CI

## When to Use

- Building or consuming REST/GraphQL APIs
- Need to verify API contracts between services
- API breaking changes need detection before deploy
- Testing auth flows and permission boundaries

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Pseudo Code

The api-testing workflow follows a standard pipeline pattern.

Core flow:
```
# api-testing primary flow
input = prepare(raw_data)
result = process(input, config={api, automation, contract, graphql, integration})
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


### REST Contract Test
```python
def test_user_api_contract(response):
    assert response.status_code == 200
    assert response.json() == {
        "id": int,
        "email": str,
        "name": str,
        "created_at": str  # ISO 8601
    }
```

### GraphQL Test
```python
def test_graphql_query():
    query = """
    query GetUser($id: ID!) {
        user(id: $id) { id name email }
    }
    """
    result = graphql_execute(query, variables={"id": "1"})
    assert result["data"]["user"]["id"] == "1"
```

## Common Patterns

- **Contract first**: Define API schema before implementation
- **Status code coverage**: Test 200, 201, 400, 401, 403, 404, 500
- **Auth boundary tests**: Verify protected endpoints reject unauthenticated requests
- **Idempotency tests**: POST requests should be safe to retry

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
