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

## Pseudo Code

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
