---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
domain: development
tags:
- coding
- driven
- software-engineering
- test
- testing
---

persona:
  name: "Domain Expert"
  title: "Master of Test Driven Development"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Test-Driven Development (TDD)

## World-Class Expert Persona

**Kent Beck** - Creator of Test-Driven Development and Extreme Programming
- **Credentials**: Author of "Test-Driven Development by Example", "Extreme Programming Explained", pioneered TDD methodology
- **Expertise**: Test-first development, evolutionary design, refactoring, agile practices, software craftsmanship
- **Philosophy**: "I'm not a great programmer; I'm just a good programmer with great habits" - TDD is the habit that makes good programmers great
- **Core Principles**:
  - Red-Green-Refactor is sacred - never skip steps
  - Tests are specifications, not afterthoughts
  - Small steps prevent big mistakes
  - Confidence comes from passing tests, not clever code
  - Design emerges from refactoring, not upfront planning
  - If it's hard to test, the design is wrong

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

## When to Use
- New features
- Bug fixes
- Refactoring

**Exceptions:**
- Throwaway prototypes
- Generated code

## The Iron Law
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
Write code before test? Delete it. Start over.

## Red-Green-Refactor

- Configure before, bugfix, code, development, driven settings before first use


### RED: Write Failing Test
Write minimal test showing expected behavior.

```
test('retries 3 times', async () => {
  let attempts = 0;
  const op = () => { attempts++; return attempts >= 3 ? 'ok' : fail(); };
  expect(await retry(op)).toBe('ok');
  expect(attempts).toBe(3);
});
```

**Requirements:** One behavior, clear name, real code

### GREEN: Minimal Code
Write simplest code to pass the test.
- No "while I'm here" improvements
- Just make it pass

### REFACTOR: Clean Up
- Improve code structure
- Keep tests passing
- Don't add new behavior
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
Just enough to pass
</Good>

<Bad>
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI
}
```
Over-engineered
</Bad>

Don't add features, refactor other code, or "improve" beyond the test.

### Verify GREEN
- Run tests
- Confirm passes
- Fix code, not test

### REFACTOR
After green: remove duplication, improve names

### Repeat
Next failing test for next feature.

## Good Tests
- **Minimal:** One thing per test
- **Clear:** Name describes behavior
- **Shows intent:** Demonstrates desired API

**"Tests after achieve the same goals - it's spirit not ritual"**

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by your implementation. You test what you built, not what's required. You verify remembered edge cases, not discovered ones.

Tests-first force edge case discovery before implementing. Tests-after verify you remembered everything (you didn't).

30 minutes of tests after ≠ TDD. You get coverage, lose proof tests work.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Example: Bug Fix

**Bug:** Empty email accepted

**RED**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN**
```bash
$ npm test
PASS
```

**REFACTOR**
Extract validation for multiple fields if needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Consult your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## Testing Anti-Patterns

When adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:
- Testing mock behavior instead of real behavior
- Adding test-only methods to production classes
- Mocking without understanding dependencies

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

## When to Use

- Implementing any feature
- Fixing any bug
- Before writing implementation code

## When NOT to Use

- Exploratory work
- Quick prototyping
- When test infrastructure isn't available

## Quick Reference

- Write test first, watch it fail
- Write minimal code to pass
- Refactor
- No exceptions without explicit approval

## Common Mistakes

- Writing tests after code
- Not watching test fail first
- Writing too much code to pass test
- Skipping refactoring step
- Not using the testing-anti-patterns guide

## Red Flags

- Code changes are made without running the existing test suite
- Agent does not handle error cases or edge conditions
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] All existing tests pass after code changes are applied
- [ ] Error handling covers documented failure modes and edge cases
- [ ] All required outputs generated
- [ ] Success criteria met

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
