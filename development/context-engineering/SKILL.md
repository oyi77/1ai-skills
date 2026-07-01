---
name: context-engineering
description: Design and manage the context window for AI coding agents. Structure prompts, manage file loading, and optimize token usage for maximum agent effectiveness. Use when designing and manage the context window for ai coding agents.
domain: development
tags:
- engineering
- context
- prompts
- ai-agents
- token-optimization
---

# Context Engineering

## When to Use
**Trigger phrases:**
- "context engineering"
- "Design and manage the context window for AI coding agents"


- When setting up AI agent instructions for a project
- When optimizing agent performance on large codebases
- When managing context window limits for complex tasks
- When designing multi-agent systems with shared context

## When NOT to Use

- For simple one-off prompts
- When the codebase fits entirely in context

## Overview

Context Engineering is the practice of designing what information an AI agent sees and in what order. The right context produces correct output; the wrong context produces hallucinations.

## Workflow

1. **Map information needs** - What does the agent need to know?
2. **Prioritize** - Critical context first, nice-to-have last
3. **Structure** - AGENTS.md, .cursor/rules/, system prompts
4. **Manage loading** - Progressive disclosure, lazy loading
5. **Optimize tokens** - Compress, deduplicate, summarize
6. **Test** - Does the agent produce correct output with this context?

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "More context is always better" | Context window has limits. Noise degrades signal. Prioritize ruthlessly. |
| "The agent will figure it out" | Without explicit context, agents hallucinate patterns and APIs |
| "README is enough" | Agents need different context than humans - code structure, conventions, gotchas |

## Context Architecture

```markdown
# AGENTS.md (loaded first, always)
- Project overview (2-3 sentences)
- Key commands (test, build, lint)
- File structure map
- Coding conventions
- Known gotchas

# System prompt (agent-specific)
- Role definition
- Quality gates
- Anti-rationalization rules
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run context engineering workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] AGENTS.md is under 500 lines
- [ ] Key commands are copy-pasteable
- [ ] File structure map is accurate
- [ ] No redundant information across context files
- [ ] Agent produces correct output with this context

