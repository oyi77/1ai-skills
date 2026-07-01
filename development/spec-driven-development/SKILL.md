---
name: spec-driven-development
description: Write a PRD covering objectives, commands, structure, code style, testing, and boundaries before any code. Spec before code, always.
domain: development
tags:
- engineering
- spec
- prd
- planning
- requirements
- design-doc
---

# Spec Driven Development

## When to Use
**Trigger phrases:**
- "spec driven development"
- "Write a PRD covering objectives, commands, structure, code style, testing, and b"


- When starting a new project, feature, or significant change
- When the requirements are unclear or underspecified
- When multiple people will work on the same feature
- When you need to prevent scope creep during implementation

## When NOT to Use

- For trivial one-line fixes
- For exploratory prototyping (but document findings after)

## Overview

Spec-Driven Development (SDD) forces clarity before code. A spec is a living document that defines WHAT to build, WHY, and the acceptance criteria. It prevents the most common engineering failure: building the wrong thing fast.

## Workflow

1. **Interview** - Ask clarifying questions until 95% confident
2. **Define objectives** - What problem does this solve? For whom?
3. **Specify commands** - CLI commands, API endpoints, UI flows
4. **Define structure** - File layout, module boundaries, data model
5. **Set code style** - Naming, patterns, error handling conventions
6. **Define testing** - What tests prove it works? Edge cases?
7. **Set boundaries** - What is NOT in scope? What are the constraints?
8. **Review** - Get sign-off before writing any code

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I know what to build" | You know what you THINK the user wants. A spec forces validation. |
| "Specs slow me down" | Rework from unclear requirements costs 5-10x more than writing a spec |
| "I will document after" | You never do. Document before or accept technical debt. |
| "Agile means no specs" | Agile means iterating on specs, not skipping them. |

## Spec Template

```markdown
# Feature: [Name]

## Objective
What problem does this solve?

## User Stories
As a [role], I want [action] so that [benefit].

## Commands / API
- `command arg1 arg2` - Does X
- `POST /api/endpoint` - Creates Y

## Structure
- `src/module/file.ts` - Purpose

## Testing
- [ ] Unit: tests X
- [ ] Integration: tests Y

## Boundaries
- NOT doing: [explicit exclusions]
- Constraints: [performance, security]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## Verification

- [ ] Spec reviewed by at least one other person
- [ ] All acceptance criteria are testable
- [ ] Boundaries explicitly state what is NOT in scope
- [ ] No implementation details in the spec (WHAT, not HOW)

