---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
domain: content
tags:
- content-creation
- digital-content
- media
- skills
- writing
persona: "name: \"Ernest Hemingway\"\n  title: \"Master of Concise Prose\"\n  expertise: [\"economy of language\", \"iceberg\
  \ theory\", \"dialogue precision\", \"emotional restraint\"]\n  philosophy: \"All you have to do is write one true sentence.\
  \ Write the truest sentence that you know.\"\n  credentials:\n    - \"Nobel Prize in Literature (1954)\"\n    - \"Pulitzer\
  \ Prize for Fiction for The Old Man and the Sea\"\n    - \"Author of The Sun Also Rises, A Farewell to Arms, For Whom the\
  \ Bell Tolls\"\n    - \"Pioneered minimalist prose style that revolutionized 20th century writing\"\n  principles:\n   \
  \ - \"Use short sentences and short first paragraphs\"\n    - \"Use vigorous English - be positive, not negative\"\n   \
  \ - \"Eliminate every word that serves no purpose\"\n    - \"Show the tip of the iceberg - let depth remain beneath surface\"\
  \n    - \"Write drunk, edit sober - separate creation from refinement\"\n    - \"Never use a long word where a short one\
  \ will do\"\n    - \"One true sentence - start with what you know is absolutely true\"\n"
---


# Writing Skills

## Overview
Writing skills IS Test-Driven Development applied to process documentation.

## When to Use
- Creating new skills
- Editing existing skills
- Verifying skills work before deployment

## When NOT to Use
- Just documenting what you did (that's narrative, not skill)
- Technique isn't proven/reproducible
- Haven't pressure-tested with subagents

## Quick Reference

**TDD Cycle:** RED → GREEN → REFACTOR

## Common Mistakes
- Writing skill before running baseline test
- Not documenting exact agent failures
- Making skills too generic
- Skipping refactor/loophole-closing phase
- Not using lint harness

## What is a Skill?
A skill is a reference guide for proven techniques, patterns, or tools.

**Skills are:** Reusable techniques, patterns, tools
**Skills are NOT:** Narratives about one-off solutions

## TDD Mapping
| TDD | Skills |
|-----|--------|
| Test case | Pressure scenario |
| RED | Agent violates without skill |
| GREEN | Agent complies with skill |
| Refactor | Close loopholes |

## SKILL.md Structure

**Frontmatter:**
- `name`: letters, numbers, hyphens only
- `description`: Start with "Use when..." (trigger, not workflow)

```markdown
---
name: skill-name
description: Use when [specific triggering conditions]
---
```

**Required sections:**
- ## Overview
- ## When to Use
- ## When NOT to Use
- ## Quick Reference
- ## Common Mistakes

## Common Mistakes
What goes wrong + fixes

## Real-World Impact (optional)
Concrete results
```


## Claude Search Optimization (CSO)

**Critical for discovery:** Future Claude needs to FIND your skill

### 1. Rich Description Field

**Purpose:** Claude reads description to decide which skills to load for a given task. Make it answer: "Should I read this skill right now?"

**Format:** Start with "Use when..." - trigger only, NOT workflow

**CRITICAL:** Description = When to Use, NOT What It Does

```yaml
# ❌ BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent with code review

# ✅ GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks
```

**Content:**
- Use concrete triggers and situations
- Describe the problem, not language-specific symptoms
- Keep triggers technology-agnostic unless skill is tech-specific
- Write in third person (injected into system prompt)

**Name by what you DO:**
- ✅ `condition-based-waiting` > `async-test-helpers`
- ✅ `root-cause-tracing` > `debugging-techniques`

**Cross-reference skills explicitly:**
- ✅ `REQUIRED: Use superpowers:test-driven-development`
- ❌ Avoid @ links (force-loads, burns context)
```

**Use flowcharts ONLY for:**
- Non-obvious decision points
- Process loops where you might stop too early
- "When to use A vs B" decisions

## Flowcharts & Examples
- Flowcharts: only for non-obvious decisions
- Examples: one excellent example, not multi-language
- Code: complete, runnable, from real scenario

## File Organization
- **Inline:** All content fits in SKILL.md
- **With tool:** SKILL.md + reusable code file
- **Heavy reference:** SKILL.md + separate reference files

## The Iron Law
```
NO SKILL WITHOUT A FAILING TEST FIRST
```
Write skill before testing? Delete it. Start over.

## Testing Skill Types

**Discipline skills (TDD, verification):**
- Test: pressure scenarios, rationalization counters
- Success: agent follows rule under pressure

**Technique skills (how-to):**
- Test: application scenarios, edge cases
- Success: agent applies technique correctly

**Pattern skills (mental models):**
- Test: recognition, application
- Success: agent identifies when to apply

**Reference skills (APIs):**
- Test: retrieval, application
- Gap testing: Are common use cases covered?

**Success criteria:** Agent finds and correctly applies reference information

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Obviously clear" | Clear to you ≠ clear to agents. Test it. |
| "Testing is overkill" | Untested skills have issues. Always. |
| "No time to test" | Untested wastes more time later. |

## Bulletproofing Skills

**Close every loophole explicitly:**
- State the rule AND forbid specific workarounds
- Add "Violating the letter = violating the spirit"

This cuts off entire class of "I'm following the spirit" rationalizations.

### Build Rationalization Table
Capture rationalizations from baseline testing:
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks |
| "I'll test after" | Tests passing proves nothing |

### Red Flags List
```
## Red Flags - STOP
- Code before test
- "I already manually tested"
- "This is different because..."
```

## RED-GREEN-REFACTOR for Skills

- Configure before, creating, deployment, editing, existing settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### RED: Baseline
Run scenario WITHOUT skill. Document:
- What choices did they make?
- What rationalizations?
- Which pressures triggered violations?

This is "watch the test fail" - you must see what agents naturally do before writing the skill.

### GREEN: Write Minimal Skill
Write skill addressing those rationalizations. Run with skill - agent should comply.

### REFACTOR: Close Loopholes
Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

## Anti-Patterns
- ❌ Narrative: "In session X, we found..."
- ❌ Multi-language: 3 implementations = mediocre
- ❌ Code in flowcharts: Can't copy-paste
- ❌ Generic labels: helper1, step3

**Don't:**
- Create multiple skills without testing each
- Skip testing because "batching is more efficient"

## Skill Creation Checklist

**RED Phase:**
- Create pressure scenarios
- Run WITHOUT skill - document baseline
- Identify rationalization patterns

**GREEN Phase:**
- Name: letters, numbers, hyphens only
- Frontmatter: name + description
- Description: starts with "Use when...", third person
- Run WITH skill - verify compliance

**REFACTOR Phase:**
- Find new rationalizations
- Add explicit counters
- Re-test until bulletproof

## Red Flags

- Content quality is not reviewed before publication or distribution
- Agent does not adapt tone and style for the target audience
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Content quality passes review before publication or distribution
- [ ] Tone and style are appropriate for the target audience
- [ ] All required outputs generated
- [ ] Success criteria met

