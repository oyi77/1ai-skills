---
name: incremental-implementation
description: Delivers changes incrementally. Use when implementing any feature or change that touches more than one file.
domain: development
tags:
- coding
- implementation
- incremental
- software-engineering
- testing
---


# Incremental Implementation Skill

## Overview

Delivers working changes in small, verifiable slices using a vertical slice approach. Each slice implements functionality across all layers (frontend, backend, database, tests) to deliver complete, testable features. This prevents large, risky changes and ensures the system remains in a working state throughout development.

## When to Use

- **Multi-file changes**: When implementing features that touch multiple files or modules
- **Feature building**: When adding new functionality with multiple components
- **Refactoring**: When restructuring code that affects multiple layers
- **Complex implementations**: When the task is too large to complete in a single mental context
- **High-risk changes**: When changes could break existing functionality

## The Process

1. **Plan the vertical slice**
   - Identify the smallest end-to-end change that delivers value
   - Map all files that need modification across layers (database, backend, frontend)
   - Define acceptance criteria for this slice

2. **Implement the slice**
   - Modify database schema if needed
   - Update backend logic and API endpoints
   - Implement frontend components that consume new data
   - Write tests for the new behavior

3. **Verify and test**
   - Run the full test suite to ensure no regressions
   - Manually verify the new functionality works end-to-end
   - Check that all related functionality still works

4. **Commit the slice**
   - Create a descriptive commit with scope and purpose
   - Ensure commit message follows project conventions
   - Verify the commit passes CI checks

5. **Move to next slice**
   - Update the plan with remaining slices
   - Repeat from step 1 until complete

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Red Flags

- **Building everything at once** – Implementing all changes before testing any increases risk exponentially
- **No tests between slices** – Skipping tests turns incremental work into one risky batch
- **Slices that don't deliver value** – Each slice should be functionally complete
- **Cross-slice dependencies** – If slices depend on each other, they're not properly isolated
- **Testing only at the end** – If testing happens only after all implementation, it's not incremental

## Verification

- **Each slice leaves the system in a working state** – All tests pass, no broken functionality
- **Acceptance criteria met** – The slice implements and tests the defined functionality
- **No regressions introduced** – Existing tests continue to pass
- **CI/checks pass** – All automated checks pass before committing
## Notes

- This skill integrates with the broader 1ai-skills ecosystem for development workflows
- Combine with related skills for maximum impact across your pipeline
- Monitor output quality and iterate on configuration based on results
- Keep dependencies up to date for security and performance
- Document custom workflows and configurations for team knowledge sharing

## Process

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

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |