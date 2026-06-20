---
name: oh-my-opencode-agents
description: Deep dive into each oh-my-opencode agent - Sisyphus, Hephaestus, Oracle, Librarian, Explore - their characteristics,
  use cases, and when to use each
domain: integrations
tags:
- agents
- ai-agent
- api
- integrations
- opencode
- third-party
---

# Oh My OpenCode Agents

## Overview

Oh My OpenCode provides a curated suite of specialized agents, each optimized for specific tasks. This skill provides detailed guidance on when and how to use each agent effectively.

## When to Use

- **Sisyphus**: When you have complex multi-step tasks that need agent autonomy to figure out the approach
- **Hephaestus**: When you need autonomous problem-solving with thorough research, especially for complex refactoring or feature implementation
- **Oracle**: After 2+ failed approaches, when you need architectural guidance, debugging strategy, or multi-system tradeoffs analysis
- **Librarian**: When you need to consult official documentation, open-source implementations, or best practices for unfamiliar libraries
- **Explore**: When you need rapid codebase exploration, pattern discovery across modules, or quick file/symbol location

## The Agent Team
- Primary agent handles core task execution
- Validator agent checks output quality
- Reporter agent formats and delivers results
- Each agent operates with clear input/output contracts


### Sisyphus — Main Orchestrator Agent

**Model**: Opus 4.6 (primary), with Prometheus (Planner) and Metis (Plan Consultant)

**Characteristics**:
- Goal-oriented execution without step-by-step instructions
- Fires 2-5 parallel explore/librarian agents before writing code
- Follows TODO lists strictly — forces continuation if quitting halfway
- Leverages LSP for refactoring — deterministic and surgical
- Comment checker — prevents AI from adding excessive comments

**Best For**:
- Complex multi-step tasks requiring coordination
- Tasks where you want the agent to figure out the approach
- Long-running autonomous work with minimal intervention

**When NOT to Use**:
- Simple, single-file changes (use quick category instead)
- When you need to closely control every step

**Key Patterns**:
- "Sisyphus doesn't waste time hunting for files himself; he keeps the main agent's context lean. Instead, he fires off background tasks to faster, cheaper models in parallel to map the territory for him."
- Uses hash-anchored edit tool (`LINE#ID` format) to validate content before changes
- Multi-model orchestration — delegates to specialists based on task type

### Hephaestus — Autonomous Deep Worker

**Model**: GPT 5.3 Codex Medium

**Characteristics**:
- Goal-oriented: Give objective, not recipe — determines steps itself
- Explores before acting: 2-5 parallel explore/librarian agents first
- End-to-end completion: Doesn't stop until 100% done with verification
- Pattern matching: Searches existing codebase for style consistency
- "Legitimate" precision — surgical, minimal code

**Best For**:
- Autonomous problem-solving with thorough research
- Complex refactoring requiring deep codebase understanding
- Feature implementation from scratch
- Tasks that need careful planning before execution

**When NOT to Use**:
- Quick fixes or trivial changes
- When you need to approve each step
- Tasks outside of software development

**Key Principles**:
- Explores existing patterns before writing
- Verifies all changes with lsp_diagnostics, build, tests
- Matches project's coding style

### Oracle — Architecture & Debugging Consultant

**Model**: GPT 5.2

**Characteristics**:
- High-IQ strategic consultation
- Complex debugging after 2+ failed fix attempts
- Architecture design decisions
- Multi-system tradeoffs analysis

**Best For**:
- Complex architecture design
- After completing significant work (self-review)
- 2+ failed fix attempts
- Unfamiliar code patterns
- Security/performance concerns
- Multi-system tradeoffs

**When NOT to Use**:
- Simple file operations (use direct tools)
- First attempt at any fix (try yourself first)
- Questions answerable from code already read
- Trivial decisions

**Consultation Pattern**:
1. Implement first attempt yourself
2. If 2+ attempts fail → Consult Oracle
3. Oracle provides architectural guidance
4. Implement Oracle's recommendations
5. Verify thoroughly

### Librarian — Documentation & Search Agent

**Model**: GLM-4.7

**Characteristics**:
- Official documentation search
- Open source implementation patterns
- Real-time source code digestion
- External library best practices

**Best For**:
- Working with unfamiliar libraries/APIs
- Finding how others solved similar problems
- Official API documentation lookup
- OSS implementation examples

**When NOT to Use**:
- Questions answerable from codebase already read
- Simple codebase questions (use Explore)
- Things inferable from existing patterns

**Trigger Phrases**:
- "How do I use [library]?"
- "Best practice for [framework feature]?"
- "Find examples of [library] usage"
- "Working with unfamiliar [package]"

### Explore — Fast Codebase Explorer

**Model**: Grok Code Fast 1

**Characteristics**:
- Blazing fast contextual grep
- Pattern discovery across modules
- Quick file and symbol location
- Multiple search angles in parallel

**Best For**:
- Finding specific patterns in codebase
- Locating files/functions/classes
- Cross-layer pattern discovery
- Quick codebase mapping

**When NOT to Use**:
- You know exactly what to search (use direct grep)
- Single keyword search (use grep)
- Known file location (use read)

**Usage Pattern**:
- Fire liberally for any non-trivial codebase question
- Use direct tools when you know the pattern
- Use Explore when multiple angles needed

## Agent Selection Matrix

| Task Type | Primary Agent | Secondary Agent |
|-----------|---------------|-----------------|
| Complex multi-step | Sisyphus | Hephaestus |
| Autonomous deep work | Hephaestus | Sisyphus |
| Architecture design | Oracle | Sisyphus |
| Complex debugging | Oracle | Hephaestus |
| Library integration | Librarian | Explore |
| Codebase exploration | Explore | Librarian |
| Quick fixes | Direct tools | Sisyphus |
| Unknown scope | Hephaestus | Oracle |

## Agent-Model Matching

For optimal performance, match agents to models:

| Agent | Recommended Model | Fallback |
|-------|------------------|----------|
| Sisyphus | Opus 4.6 | GPT-4.5, Claude 3.7 |
| Hephaestus | GPT 5.3 Codex Medium | GPT-4.5, Claude 3.7 |
| Oracle | GPT 5.2 | GPT-4.5, Claude 3.7 |
| Librarian | GLM-4.7 | GPT-4.5, Claude 3.7 |
| Explore | Grok Code Fast 1 | Any fast model |

## Parallel Execution Patterns
This section covers parallel execution patterns for the oh-my-opencode-agents skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Pattern 1: Multi-Agent Discovery
```
// Fire 2-5 agents in parallel for comprehensive understanding
- Hephaestus: Deep research on the problem domain
- Librarian: External documentation and examples
- Explore: Internal codebase patterns
- Oracle: Architecture considerations (if complex)
```

### Pattern 2: Sequential with Parallel Discovery
```
// Hephaestus fires parallel agents first, then synthesizes
1. Hephaestus launches parallel exploration
2. Waits for results
3. Synthesizes information
4. Implements solution
5. Verifies end-to-end
```

### Pattern 3: Emergency Consultation
```
// Hephaestus tries 2-3 approaches, then consults Oracle
1. First approach attempt
2. If fails → Alternative approach
3. If fails → Oracle consultation
4. Implement Oracle's recommendations
5. Verify
```

## Skill Integration
- Connects with existing toolchain via standard interfaces
- Supports webhook-based event notifications
- Compatible with CI/CD pipelines for automated workflows
- Provides structured output for downstream consumption


### Required Workflow Skills
- **superpowers:using-git-worktrees** — REQUIRED: Isolated workspace
- **superpowers:writing-plans** — Creates plans Sisyphus executes
- **superpowers:requesting-code-review** — Code review template
- **superpowers:finishing-a-development-branch** — Complete development

### Subagents Should Use
- **superpowers:test-driven-development** — Subagents follow TDD
- **superpowers:systematic-debugging** — Debug failures properly

## Quality Gates

All agents must follow:

1. **Before Implementation**: Explore existing patterns
2. **After Implementation**: 
   - lsp_diagnostics on all modified files
   - Run related tests
   - Run build/typecheck
3. **Before Completion**: Verify 100% of requirements met

## Common Mistakes
This section covers common mistakes for the oh-my-opencode-agents skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Sisyphus
- Providing step-by-step instructions ( defeats autonomy)
- Skipping parallel agent launches
- Not following TODO list

### Hephaestus
- Not exploring before acting
- Not matching codebase patterns
- Skipping verification

### Oracle
- Consulting too early (before trying yourself)
- Consulting for simple questions
- Not following Oracle's recommendations

### Librarian
- Using for simple questions answerable from code
- Not being specific enough in queries
- Ignoring results

### Explore
- Using when direct tools suffice
- Not providing enough context
- Limiting search scope

## Red Flags

**Never**:
- Use Sisyphus for trivial tasks
- Skip Hephaestus's parallel exploration
- Consult Oracle before trying 2+ approaches
- Use Explore when you know the answer
- Skip verification after any agent work

## The Process

1. **Identify task type** – Determine if task is complex (Sisyphus), autonomous (Hephaestus), strategic (Oracle), documentation (Librarian), or exploration (Explore)
2. **Choose agent** – Select agent based on task requirements, skill level of existing codebase, and collaboration needs
3. **Configure agent** – Set model, temperature, and any agent-specific options in configuration
4. **Load skill** – Ensure oh-my-opencode-agents skill is available to agent environment
5. **Initiate work** – Invoke agent with clear objectives, task context, and success criteria
6. **Monitor progress** – Track agent output, verify tool usage, adjust parameters if needed
7. **Verify completion** – Run lsp_diagnostics, build, and tests for agent-generated code

## Red Flags

- **Assigning trivial work to complex agents** – Using Sisyphus for single-file edits or Hephaestus for quick fixes wastes resources
- **Consulting Oracle too early** – Oracle should be invoked after 2+ failed attempts, not as first resort
- **Using Explore for documentation** – Explore is for codebase exploration, not reading official docs (use Librarian)
- **Ignoring agent characteristics** – Not leveraging parallel exploration (Hephaestus), not using TODO lists (Sisyphus)
- **Skipping verification steps** – Agent work should be verified with lsp_diagnostics, build, and tests before commit
- **Config mismatch** – Using wrong models, temperatures, or permissions for agent capabilities

## Verification

- **Skill loaded**: Invoke skill tool and verify all agents have correct model assignments and characteristics
- **Agent selection**: `/agent sisyphus`, `/agent hephaestus`, `/agent oracle` should all switch without error
- **Agent behavior**: Agent follows own characteristics (Sisyphus uses TODO, Hephaestus explores first)
- **Output quality**: Agent responses match expected domain expertise (Oracle gives architectural insights, Librarian gives docs)
- **Verification hooks**: Agent completes with lsp_diagnostics, build, and tests executed
- **Parallel execution**: Hephaestus fires 2-5 explore/librarian agents before acting, Sisyphus fires parallel tasks
- **No redundancy**: Each agent used for purpose it's designed for, not confused with others

## References

- Agent System: https://github.com/code-yeongyu/oh-my-opencode#for-those-who-want-to-read-meet-sisyphus
- Agent-Model Matching: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/guide/agent-model-matching.md
- Quality Standards: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/features.md

## Related Skills

- oh-my-opencode: Overall integration overview
- oh-my-opencode-installation: Setup guide
- oh-my-opencode-configuration: Configuration options
- oh-my-opencode-features: Complete features list

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
