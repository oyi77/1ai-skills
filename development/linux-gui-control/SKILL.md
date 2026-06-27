---
name: linux-gui-control
description: Automate Linux desktop GUI interactions using xdotool, wmctrl, and dogtail for window management, mouse/keyboard
  simulation, and accessibility inspection.
domain: development
tags:
- coding
- control
- gui
- linux
- software-engineering
- testing
persona: "name: Linus Torvalds\n  title: The Linux Creator - Master of System Control\n  expertise:\n  - Linux\n  - System\
  \ Programming\n  - Git\n  - Operating Systems\n  philosophy: Talk is cheap. Show me the code.\n  credentials:\n  - Created\
  \ Linux kernel\n  - Created Git\n  - Maintains largest open source project\n  principles:\n  - Control the system\n  - Script\
  \ everything\n  - Prefer command line\n  - Automate workflows\n"
---
# Linux Gui Control

## When to Use

**Trigger phrases:**
- "linux gui control"
- "Help me with linux gui control"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


This skill provides tools and procedures for automating interactions with the Linux desktop environment.


## When NOT to Use

- For throwaway prototypes (skip the ceremony)
- When the fix is a single-line change with no side effects
- When the codebase already has a working solution


## Overview

Linux Gui Control supports coding practices with best practices and proven patterns.

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

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings