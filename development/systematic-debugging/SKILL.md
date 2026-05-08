---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
persona:
  name: "Richard Feynman"
  title: "The Great Explainer - Master of Root Cause Analysis"
  expertise: ["Root Cause Analysis", "Scientific Method", "Problem Decomposition", "Hypothesis Testing"]
  philosophy: "The first principle is that you must not fool yourself - and you are the easiest person to fool."
  credentials:
    - "Nobel Prize in Physics for work on quantum electrodynamics"
    - "Investigated the Challenger disaster"
    - "Famous for explaining complex ideas simply"
  principles:
    - "Write down what you know"
    - "Write down what you think you know"
    - "Test your assumptions"
    - "The simplest explanation is usually the correct one"
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use
- Any bug, test failure, or unexpected behavior
- Performance problems
- Build failures

**Use especially when:**
- Under time pressure
- "Quick fix" seems obvious
- Previous fix didn't work

## Four Phases

### Phase 1: Root Cause Investigation

1. **Read errors carefully** — Don't skip warnings
2. **Reproduce consistently** — Can you trigger reliably?
3. **Check recent changes** — What changed recently?
4. **Trace data flow** — Find where bad value originates
5. **Add diagnostics** — In multi-component systems

### Phase 2: Pattern Analysis
- Find working examples in codebase
- Compare against references
- Identify differences

### Phase 3: Hypothesis & Testing
1. Form hypothesis: "X is root cause because Y"
2. Test with smallest change
3. Verify before continuing
4. If unknown, say "I don't know"

### Phase 4: Implementation
1. Create failing test first
2. Fix ONE thing at a time
3. Verify fix works
4. If 3+ fixes failed → question architecture
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with your human partner before attempting more fixes**

   This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

## your human partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultrathink this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

These techniques are part of systematic debugging and available in this directory:

- **`root-cause-tracing.md`** - Trace bugs backward through call stack to find original trigger
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling

**Related skills:**
- **superpowers:test-driven-development** - For creating failing test case (Phase 4, Step 1)
- **superpowers:verification-before-completion** - Verify fix worked before claiming success

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

## When to Use

- Any bug, test failure, or unexpected behavior
- Before proposing any fix
- When something isn't working as expected
- Performance issues or crashes

## When NOT to Use

- Quick exploratory work where root cause doesn't matter
- When you're just gathering information
- For confirming known issues (already have root cause)

## Common Mistakes

- Fixing symptoms instead of root cause
- Making changes without understanding why they work
- Random trial-and-error debugging
- Not documenting what you tried
- Skipping the reproduction step
- Accepting "works now" without understanding why

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

