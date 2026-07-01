---
name: content-validation-workflow
description: Validate AI-generated content quality through sample generation, human review gates, and controlled batch production
  workflows. Use when working with content validation workflow.
domain: development
tags:
- coding
- content
- software-engineering
- testing
- validation
- workflow
---
# Content Validation Workflow

## When to Use

**Trigger phrases:**
- "content validation workflow"
- "Help me with content validation workflow"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- For throwaway prototypes (skip the ceremony)
- When the fix is a single-line change with no side effects
- When the codebase already has a working solution


## Overview

Content Validation Workflow supports coding practices with best practices and proven patterns.

## Workflow

```python
# Example: TDD workflow
def test_user_creation():
    user = create_user(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None

def test_user_creation_invalid_email():
    with pytest.raises(ValidationError):
        create_user(name="Alice", email="invalid")
```

1. **Understand requirements** — Clarify acceptance criteria and constraints
2. **Design solution** — Plan architecture and identify patterns
3. **Implement** — Write code following project conventions
4. **Test** — Unit tests, integration tests, edge cases
5. **Review** — Code review for quality, security, and performance
6. **Document** — Update relevant docs and changelogs

## Quality Gates

- [ ] All tests passing
- [ ] No lint errors or warnings
- [ ] Code coverage meets threshold (≥70%)
- [ ] No security vulnerabilities detected
- [ ] Documentation updated

## Best Practices

- Follow SOLID principles and KISS
- Write self-documenting code with clear naming
- Handle errors explicitly — no silent failures
- Keep functions small and focused (<50 lines)
- Use immutable data patterns where possible

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |


## Process

1. **Research** — Analyze target audience, competitors, and trending topics
1. **Create** — Generate content following brand guidelines and best practices
1. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings