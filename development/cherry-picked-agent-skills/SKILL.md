---
name: cherry-picked-agent-skills
description: 6 unique agent skills cherry-picked from Addy Osmani's agent-skills — interview extraction, idea refinement, adversarial review, source-driven development, context engineering, and deprecation workflows. Use when requirements gathering, idea refinement, adversarial review, documentation-driven dev, context optimization, code deprecation.
domain: development
tags: [agent-skills, methodology, interview, context-engineering, deprecation, adversarial-review]
---


## Overview

Six unique agent workflow skills cherry-picked from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) that do not overlap with existing 1ai-skills. Each skill defines a structured methodology for AI agents to follow during specific development workflows.

## Skill 1: interview-me

**Description**: One-question-at-a-time interview that extracts what the user actually wants, not what they initially say they want.

**When to use**: Starting any non-trivial feature or project. When requirements are vague. When the user says "just build X" without clear specifications.

**Key Principles**:
- Ask one question at a time — never batch questions
- Mirror back what you heard before asking the next question
- Dig into the "why" behind each request
- Surface implicit constraints the user hasn't mentioned
- Stop interviewing when you can state the requirement back and the user confirms

**Process**:
1. Restate the user's initial request in your own words
2. Ask: "What problem does this solve for you?"
3. Ask about constraints: timeline, tech stack, existing code, audience
4. Ask about success criteria: how will you know this is done?
5. Summarize the extracted requirements and ask for confirmation
6. Only then begin planning or implementation

## Skill 2: idea-refine

**Description**: Divergent then convergent thinking to turn vague ideas into concrete, actionable proposals.

**When to use**: Brainstorming sessions. When the user has a rough concept but no clear path. When multiple approaches are possible.

**Key Principles**:
- Divergent phase: generate many options without judgment
- Convergent phase: evaluate, filter, and combine into a single proposal
- Never skip divergent thinking — jumping to solutions misses better alternatives
- Score options on feasibility, impact, and effort

**Process**:
1. **Divergent**: Generate 5-10 possible interpretations of the idea
2. **Expand**: For each interpretation, list pros, cons, and dependencies
3. **Cluster**: Group related interpretations together
4. **Score**: Rate each cluster on feasibility (1-5), impact (1-5), effort (1-5)
5. **Convergent**: Select top 1-3 candidates, combine best elements
6. **Propose**: Present a concrete proposal with clear next steps

## Skill 3: doubt-driven-development

**Description**: Adversarial fresh-context review of in-flight decisions. Actively tries to find flaws in the current approach.

**When to use**: After making a significant architectural decision. Before committing to an implementation path. When things feel "too easy."

**Key Principles**:
- Assume the current approach has a flaw — find it
- Fresh context: pretend you just joined the project and know nothing
- Steel-man the alternatives, don't straw-man them
- If you can't find a flaw after honest effort, the decision is probably sound
- Document what you checked and why it passed

**Process**:
1. State the decision or approach under review
2. List the assumptions it depends on
3. For each assumption: what if this is wrong?
4. Research alternative approaches with fresh eyes
5. Write the strongest case against the current approach
6. If the case is strong: pivot or hedge. If weak: document and proceed.

## Skill 4: source-driven-development

**Description**: Ground every decision in official documentation and cite sources. No vibes-based coding.

**When to use**: Working with any SDK, framework, or API. When behavior is unclear. When you're about to write code that depends on library internals.

**Key Principles**:
- Official docs > blog posts > Stack Overflow > assumptions
- Always cite the source URL when referencing behavior
- If you can't find a source, explicitly flag the assumption
- Docs go stale — prefer latest version-specific documentation
- When docs conflict with observed behavior, note the discrepancy

**Process**:
1. Before implementing, search official documentation for the relevant API/feature
2. Copy the key snippets and cite the URL
3. If docs are ambiguous, check GitHub issues for clarification
4. Implement based on documented behavior, not assumptions
5. Add inline comments citing sources for non-obvious decisions
6. If you discover docs are wrong, document the discrepancy

## Skill 5: context-engineering

**Description**: Feed agents the right information at the right time. Context is not about having more — it's about having the right pieces.

**When to use**: Setting up agent workflows. When agents produce generic output. When context windows are a bottleneck. When building CLAUDE.md, AGENTS.md, or system prompts.

**Key Principles**:
- More context is not always better — irrelevant context degrades output
- Structure context in layers: critical (always loaded), important (loaded on demand), reference (available but not loaded)
- Context includes: codebase patterns, conventions, constraints, examples, anti-patterns
- Update context as the project evolves — stale context is worse than no context

**Process**:
1. **Audit**: What does the agent currently know? What is it missing?
2. **Classify**: Critical (must know) vs important (should know) vs reference (nice to know)
3. **Structure**: Place critical context in always-loaded files (CLAUDE.md), important in category files (AGENTS.md), reference in browsable locations
4. **Test**: Does the agent produce better output with the new context?
5. **Iterate**: Remove context that doesn't improve output, add what's missing
6. **Maintain**: Review and update context files regularly

## Skill 6: deprecation-and-migration

**Description**: Code-as-liability mindset. Systematically identify zombie code, deprecated dependencies, and dead features for removal.

**When to use**: Pre-release cleanup. When technical debt is accumulating. When dependencies have known vulnerabilities or deprecations. When code coverage reports show unused paths.

**Key Principles**:
- Every line of code is a liability — it must be maintained, tested, and understood
- Dead code creates confusion about what's actually used
- Deprecation without a migration path is just abandonment
- Remove before you add — cleanup creates capacity for new work

**Process**:
1. **Audit**: Scan for unused imports, dead functions, unreachable code paths
2. **Dependencies**: Check for deprecated packages, outdated versions, known vulnerabilities
3. **Features**: Identify features with zero usage or zero tests
4. **Prioritize**: Risk (high/medium/low) x effort (high/medium/low)
5. **Plan**: Create migration plan with rollback capability
6. **Execute**: Remove or migrate one category at a time, test after each
7. **Document**: Record what was removed and why, in case it's needed later

## When to Use

- Requirements gathering: **interview-me**
- Turning vague ideas into specs: **idea-refine**
- Validating architectural decisions: **doubt-driven-development**
- Working with SDKs and APIs: **source-driven-development**
- Optimizing agent context files: **context-engineering**
- Technical debt cleanup: **deprecation-and-migration**

## How to Use

1. Understand the requirement and existing codebase patterns
2. Design the solution with error handling and testability in mind
3. Implement incrementally with tests for each change
4. Verify against expected outcomes (manual and automated)
5. Document usage, edge cases, and integration points
6. Review with team before merging to shared branches

## Red Flags

- **Skipping tests to ship faster**: Untested code breaks in production when you least expect it
- **No error handling in production code**: Unhandled errors crash services and lose user data
- **Hardcoded configuration values**: Hardcoded values prevent environment switching and leak secrets
- **Ignoring security implications**: Missing input validation, auth bypasses, and injection vulnerabilities
- **Over-engineering simple solutions**: Premature abstraction adds complexity without proportional benefit
