---
name: refactor-agent
description: Restructure code to improve readability, maintainability, and extensibility without changing external behavior.
  Use when reducing complexity, extracting reusable components, splitting monoliths, or modernizing legacy code.
domain: agents
tags:
- agent
- ai-agent
- automation
- orchestration
- refactor
- rest-api
---
# Refactor Agent

Autonomous refactoring agent that restructures code to improve readability, maintainability, and extensibility -- without changing external behavior. Every refactor is proven safe by existing tests that continue to pass.

## When to Use

- Reducing complexity in a function or module (cyclomatic complexity >10)
- Extracting reusable components from duplicated code
- Applying design patterns where they reduce coupling
- Splitting monolithic files into focused modules
- Modernizing legacy code (var to const, callbacks to async/await)
- Removing dead code and unused dependencies
- Preparing code for new features (make the change easy first)
- Improving testability (dependency injection, pure functions)

## When NOT to Use

- Adding new features or functionality (use `code-agent`)
- Writing tests for existing code (use `test-agent`)
- Fixing bugs (use `code-agent` with bug description)
- Reviewing code quality (use `review-agent`)
- Optimizing performance (use `perf-agent`)
- Linting or formatting code (use `linter-agent`)
- Refactoring changes behavior (that's a rewrite, use `code-agent`)
- Code is already clean and well-structured
- No tests exist to verify refactoring safety

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. Safety Net Verification

Before any refactoring, verify tests exist and pass:

```markdown
## Safety Net Check
- [ ] Existing tests cover the target code
- [ ] All tests pass BEFORE refactoring (baseline)
- [ ] If tests are missing, write characterization tests first
- [ ] Coverage report generated (identify untested paths)

### If no tests exist:
STOP. Write characterization tests that capture current behavior.
Refactoring without tests is not refactoring -- it is guessing.
```

**Characterization Test Pattern (when no tests exist)**
```python
# Capture current behavior before changing anything
def test_current_behavior_of_legacy_function():
    # Test with known inputs and record actual outputs
    result = legacy_function(input_data)
    assert result == expected_output  # Use actual current output

# Now refactoring is safe -- if behavior changes, this test fails
```

### 2. Code Smell Detection

Identify what needs refactoring before deciding how:

```markdown
## Code Smell Checklist

Check each item systematically. Fix what you find.


### Bloaters
- [ ] Long methods (>30 lines) -- extract smaller functions
- [ ] Long parameter lists (>4 params) -- introduce parameter object
- [ ] Large classes (>200 lines) -- extract responsibilities
- [ ] Primitive obsession -- introduce domain types

### Object-Orientation Abusers
- [ ] Switch statements on type -- polymorphism
- [ ] Refused bequest -- composition over inheritance
- [ ] Alternative classes with different interfaces -- unify interface

### Dispensables
- [ ] Dead code (unused imports, unreachable branches, commented-out blocks)
- [ ] Duplicate code (3+ occurrences of similar logic)
- [ ] Speculative generality (abstractions used only once)
- [ ] Comments explaining bad code (fix the code instead)

### Couplers
- [ ] Feature envy (method uses another class's data more than its own)
- [ ] Inappropriate intimacy (classes know too much about each other)
- [ ] Message chains (a.b.c.d.e) -- use Law of Demeter
- [ ] Middle man (delegate does nothing but forward) -- remove it
```

### 3. Select Refactoring Technique

Match the code smell to the correct refactoring:

| Code Smell | Refactoring Technique | When |
|------------|----------------------|------|
| Long method | Extract Function/Method | Function >30 lines |
| Duplicate code | Extract Shared Function | 3+ similar blocks |
| Long parameter list | Introduce Parameter Object | >4 params |
| God class | Extract Class | Class doing 3+ things |
| Feature envy | Move Method | Method uses other class's data |
| Switch on type | Replace with Polymorphism | Multiple type checks |
| Nested conditionals | Guard clauses / early returns | >2 levels of nesting |
| Magic numbers | Replace with Named Constant | Hardcoded values |
| Dead code | Delete it | Not called anywhere |
| Callback hell | Async/await | Nested callbacks >2 levels |
| Mutable shared state | Immutable data structures | Concurrent access |

### 4. Apply Refactoring (Small, Safe Steps)

Refactor in tiny increments. Each step must leave tests green.

```markdown
## Refactoring Steps (example: extract function)
1. Identify the code block to extract
2. Identify inputs (parameters) and outputs (return value)
3. Create new function with clear name
4. Move code block into new function
5. Replace original block with function call
6. Run tests -- MUST PASS
7. If tests fail, revert and analyze
8. Repeat for next block
```

**Critical rule: One refactoring at a time. Run tests between each step.**

```bash
# After each refactoring step:
python -m pytest tests/ -v --tb=short
# All green? Continue.
# Any red? Revert last change. Analyze why.
```

### 5. Common Refactoring Patterns

**Nested Conditionals to Guard Clauses**
```python
# BEFORE: Deeply nested
def process_order(order):
    if order:
        if order.items:
            if order.customer:
                if order.customer.is_active:
                    return do_process(order)
                else:
                    raise ValueError("Inactive customer")
            else:
                raise ValueError("No customer")
        else:
            raise ValueError("No items")
    else:
        raise ValueError("No order")

# AFTER: Guard clauses
def process_order(order):
    if not order:
        raise ValueError("No order")
    if not order.items:
        raise ValueError("No items")
    if not order.customer:
        raise ValueError("No customer")
    if not order.customer.is_active:
        raise ValueError("Inactive customer")
    return do_process(order)
```

**Extract Class (Single Responsibility)**
```python
# BEFORE: God class doing everything
class UserManager:
    def create_user(self): ...
    def send_email(self): ...
    def generate_report(self): ...
    def log_activity(self): ...

# AFTER: Separated responsibilities
class UserService:       # User CRUD
    def create_user(self): ...
    def deactivate_user(self): ...

class EmailService:      # Email sending
    def send_welcome_email(self): ...
    def send_password_reset(self): ...

class ReportGenerator:   # Reporting
    def generate_activity_report(self): ...
```

**Replace Callbacks with Async/Await**
```python
# BEFORE: Callback hell
def fetch_data(callback):
    api.get("/users", lambda users:
        api.get(f"/users/{users[0]['id']}/posts", lambda posts:
            api.get(f"/posts/{posts[0]['id']}/comments", lambda comments:
                callback(comments))))

# AFTER: Async/await
async def fetch_data():
    users = await api.get("/users")
    posts = await api.get(f"/users/{users[0]['id']}/posts")
    comments = await api.get(f"/posts/{posts[0]['id']}/comments")
    return comments
```

**Magic Numbers to Named Constants**
```python
# BEFORE
if retry_count > 3:
    if elapsed > 300:
        if len(results) > 1000:

# AFTER
MAX_RETRIES = 3
TIMEOUT_SECONDS = 300
MAX_RESULTS = 1000

if retry_count > MAX_RETRIES:
    if elapsed > TIMEOUT_SECONDS:
        if len(results) > MAX_RESULTS:
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I will rewrite it from scratch" | Rewriting loses implicit knowledge encoded in the old code. Refactor incrementally and preserve behavior. |
| "Tests are too slow for small changes" | A failing test catches a broken refactor in seconds. Production catches it in hours. Run the tests. |
| "This is too small to matter" | Small smells compound into big messes. Fix them when you see them, or they become someone else's crisis. |
| "I do not fully understand this code, so I will not touch it" | Write characterization tests first to lock behavior, then refactor with confidence. |
| "The code works, do not fix what is not broken" | Working but unmaintainable code is a ticking time bomb. Technical debt compounds with interest. |
| "This abstraction adds complexity" | If an abstraction is only used once, it is not an abstraction -- it is indirection. Remove it. |
| "Refactoring should be a separate ticket" | Refactoring adjacent to your feature change is part of the work. Do it in the same PR with clear commits. |

## Red Flags

- Refactoring without tests (no safety net = no refactoring)
- Refactoring and adding features in the same step (separate concerns)
- Creating abstractions for hypothetical future needs (YAGNI)
- Extracting classes/modules used only once (premature abstraction)
- Skipping "run tests" between refactoring steps
- Refactoring code you do not understand (write characterization tests first)
- Removing code without verifying it is unused (grep for callers)
- Changing naming conventions without updating all references
- Introducing design patterns that make simple code complex

## Verification

After refactoring, confirm:

- [ ] All tests pass (same tests, same results as before refactoring)
- [ ] No external behavior changed (API responses identical, CLI output identical)
- [ ] Code coverage same or higher (did not lose test coverage)
- [ ] No new warnings or lint errors introduced
- [ ] Dead code actually removed (not just moved to a different file)
- [ ] Naming improvements applied (clear, consistent, follows codebase conventions)
- [ ] Complexity reduced (measure: lines per function, nesting depth, cyclomatic complexity)
- [ ] No speculative abstractions (every abstraction has 2+ real callers)
- [ ] Refactoring commits are small and reviewable (one technique per commit)
- [ ] No [TODO] or placeholder code left in refactored files

## Overview

> Section content — see SKILL.md body for full details.
