---
name: karpathy-coding-principles
description: Andrej Karpathy's 4 coding principles — think before coding, simplicity first, surgical changes, goal-driven execution. Use when coding, reviewing code quality, reducing overengineering, improving LLM output, writing clean code.
domain: core
tags: [coding-principles, code-quality, best-practices, karpathy, simplicity, clean-code]
---

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Overview

Andrej Karpathy's 4 coding principles distilled into actionable rules for AI agents and developers. Focuses on reducing overengineering, maintaining simplicity, making minimal changes, and verifying outcomes. Originally from [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills).

## Capabilities

- Enforce explicit reasoning before writing code
- Prevent speculative features and unnecessary abstractions
- Restrict changes to only what the task requires
- Convert imperative tasks into declarative goals with verification

## When to Use

- Writing or reviewing code for quality
- Reducing overengineering in implementations
- Coaching LLMs to produce cleaner output
- Code review to catch scope creep
- Refactoring sessions to simplify architecture
- Any coding task where discipline matters

## Principle 1: Think Before Coding

**Before writing any code, reason explicitly about the problem.**

- Surface assumptions — state what you believe about the requirements
- Ask clarifying questions — do not guess when ambiguity exists
- Outline your approach in plain language before implementation
- Consider edge cases and failure modes upfront

```
# BAD: Jump straight to code
def process(data):
    # immediately writing implementation

# GOOD: Think first
# Assumption: data is a list of dicts with 'id' and 'value' keys
# Edge cases: empty list, missing keys, negative values
# Approach: validate -> transform -> aggregate
def process(data):
    ...
```

## Principle 2: Simplicity First

**Write the minimum code that solves the problem. No speculative features.**

- No abstractions for single-use logic — just write it inline
- No "just in case" parameters, configs, or extension points
- Prefer boring, readable code over clever solutions
- If a function is only called once, it probably does not need to exist

```python
# BAD: Over-engineered for current needs
class DataProcessor:
    def __init__(self, config: ProcessingConfig):
        self.strategy = config.get_strategy()
        self.pipeline = Pipeline(config.steps)
    
    def process(self, data): ...

# GOOD: Simple, direct, matches actual requirement
def process_data(data: list[dict]) -> list[dict]:
    return [transform(item) for item in data if item["active"]]
```

## Principle 3: Surgical Changes

**Edit only what the task requires. No drive-by refactoring.**

- Touch only the files and lines necessary for the change
- Do not rename variables, reorder imports, or fix style unless asked
- If you notice an unrelated issue, note it — do not fix it in the same change
- Keep diffs small and reviewable

```python
# BAD: Task says "add timeout parameter"
# Also renames function, fixes whitespace, adds type hints to unrelated code

# GOOD: Task says "add timeout parameter"
# Adds the parameter with a default, threads it through to the call site. Done.
```

## Principle 4: Goal-Driven Execution

**Define what "done" looks like before starting. Verify it when finished.**

- Convert imperative requests into declarative goals with checkable criteria
- Every change should have a verification step (test, command output, visual check)
- Stop when the goal is met — do not polish beyond requirements
- If verification fails, fix the root cause, not the test

```python
# Goal: "The API returns paginated results"
# Verification criteria:
# 1. GET /items?page=2&limit=10 returns items 11-20
# 2. Response includes total_count and has_next fields
# 3. Edge case: page beyond total returns empty list, not error
```

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |