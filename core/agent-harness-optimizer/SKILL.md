---
name: agent-harness-optimizer
description: Agent harness optimization patterns for token efficiency, memory persistence, session management, and cross-harness parity. Use when optimizing agent performance, reducing token costs, configuring hook profiles, managing session lifecycles, or running agents across Claude Code, Cursor, OpenCode, Codex, and Gemini.
domain: core
tags: [token-optimization, memory-persistence, session-management, hooks, cross-harness, performance]
persona:
  name: "NanoClaw"
  title: "Harness Performance Architect"
  expertise: ["Token Optimization", "Hook Systems", "Memory Persistence", "Cross-Harness Engineering", "Session Lifecycle Management"]
  philosophy: "Every token spent must earn its place. Optimize the harness, not just the model."
---

## Overview

Agent harness optimization is the practice of tuning the runtime environment that surrounds an AI agent -- model selection, prompt structure, hook configuration, memory persistence, and session management -- to maximize output quality while minimizing token cost and latency. Derived from real-world patterns across 10+ months of daily agentic work, these techniques apply to any harness: Claude Code, Cursor, OpenCode, Codex, Gemini, and beyond.

## When to Use

- Token costs are rising faster than output quality
- Agents lose context between sessions or after compaction
- Hook scripts are slow, brittle, or produce noisy output
- You need the same agent behavior across multiple AI coding harnesses
- Session history grows unwieldy and needs structured management
- Background processes are eating into the main context window
- You want to set up continuous learning from session patterns

## Process / Steps
1. Gather requirements and constraints from the user
2. Validate prerequisites (tools, permissions, data)
3. Execute the core operation with error handling
4. Verify output meets quality standards
5. Report results and log for future reference


### 1. Token Optimization Audit

Assess current token spend across three vectors:

**Model Selection Routing**
- Use fast/cheap models (Haiku-class) for: lint checks, simple file reads, status queries, hook callbacks
- Use standard models (Sonnet-class) for: code generation, refactoring, test writing, standard tasks
- Use premium models (Opus-class) for: architecture decisions, security review, complex debugging, multi-system changes
- Route dynamically: `if task.complexity < 3 then fast_model elif task.complexity < 7 then standard_model else premium_model`

**System Prompt Slimming**
- Audit CLAUDE.md and AGENTS.md for redundant instructions -- most projects have 30-50% duplication
- Move rarely-used instructions to category-specific files loaded on demand
- Use compact formats: bullet lists over paragraphs, code over prose
- Target: system prompt under 4K tokens for standard workflows, under 8K for complex projects
- Strip instructions that duplicate harness defaults (e.g., "use Read tool" when the harness already enforces this)

**Background Process Isolation**
- Never run builds, tests, or long-running commands in the main context window
- Use `run_in_background: true` for all operations over 5 seconds
- Offload analysis to cheaper models via subagent delegation
- Use `Grep`/`Glob` for discovery instead of `Bash find`/`grep` to reduce output tokens

### 2. Memory Persistence via Hooks

Implement session-persistent memory using hook-based save/load:

**SessionStart Hook (Load)**
```bash
# On session start, load prior context
# Read project memory, notepad, and recent session summary
cat .omc/project-memory.json 2>/dev/null
cat .omc/notepad.md 2>/dev/null
```

**PreToolUse Hook (Capture)**
```bash
# Capture tool calls and prompts for pattern extraction
echo "$(date +%s)|$TOOL_NAME|$INPUT_PREVIEW" >> .omc/session-trace.log
```

**PostToolUse/Stop Hook (Save)**
```bash
# On session end, persist learnings
# Save key decisions, patterns learned, errors encountered
# Keep under 2000 chars to avoid context bloat on next load
```

**Memory File Structure**
```
.omc/
  project-memory.json    # Persistent project context (conventions, stack, decisions)
  notepad.md             # Working memory (auto-pruned after 7 days)
  session-trace.log      # Tool call log for pattern extraction
  state/                 # Mode-specific state (autopilot, ralph, etc.)
```

### 3. Session Management

Manage agent sessions with structured lifecycle commands:

**Branch** -- Create isolated work contexts per task
- Each task gets a git worktree or branch for isolation
- Prevents context bleed between unrelated tasks

**Search** -- Query prior session history
- Search session transcripts for patterns, decisions, and solutions
- Avoid re-solving problems already solved

**Export** -- Extract session artifacts
- Export decisions, code changes, and learnings as structured documents
- Share across team or feed into continuous learning

**Compact** -- Reduce active context size
- Summarize conversation history into dense notes
- Remove resolved tool outputs, keep only decisions and blockers
- Target: compact to 30% of original size

**Metrics** -- Track session efficiency
- Tokens spent per task, per tool, per decision
- Time-to-completion for common task types
- Error rate and retry count

### 4. Hook Runtime Controls

Configure hook behavior at runtime without editing files:

```bash
# Set strictness profile
export ECC_HOOK_PROFILE=minimal    # Only critical hooks (security, error)
export ECC_HOOK_PROFILE=standard   # Default -- lint, typecheck, memory
export ECC_HOOK_PROFILE=strict     # All hooks including style, docs

# Disable specific hooks temporarily
export ECC_DISABLED_HOOKS="pre:bash:tmux-reminder,post:edit:typecheck"

# Cap SessionStart context size
export ECC_SESSION_START_MAX_CHARS=4000

# Disable SessionStart context for low-context setups
export ECC_SESSION_START_CONTEXT=off

# Suppress cost warnings but keep other context/scope warnings
export ECC_CONTEXT_MONITOR_COST_WARNINGS=off
```

**Hook Profile Design Principles**
- `minimal`: For fast iteration, debugging, and exploration. Only blocks security violations.
- `standard`: For daily development. Includes type checking, lint, and memory hooks.
- `strict`: For production code, PRs, and releases. Enforces style, docs, and full verification.

### 5. Cross-Harness Parity

Ensure agent behavior is consistent across harnesses:

| Concern | Claude Code | Cursor | OpenCode | Codex | Gemini |
|---------|-------------|--------|----------|-------|--------|
| Rules location | `~/.claude/rules/` | `.cursorrules` | `opencode.json` | `AGENTS.md` | System prompt |
| Hooks | Native hook system | File watchers | Plugin events | None | None |
| Skills/Commands | Plugin + slash commands | Custom instructions | Plugins + commands | Markdown only | Prompt-only |
| Memory | `.claude/` directory | `.cursor/` | `.opencode/` | Project root | External store |
| MCP | Native support | Limited | Plugin-based | None | None |

**Parity Checklist**
- [ ] Core instructions translated to each harness's native format
- [ ] Hooks replicated as file watchers or plugin events where native hooks unavailable
- [ ] Skills portable as markdown with harness-agnostic trigger detection
- [ ] Memory files in project root (harness-agnostic) with harness-specific symlinks
- [ ] Test each harness independently: same input should produce same output quality

### 6. Continuous Learning from Sessions

Feed session patterns back into the system:

**Observation Capture** (automatic via hooks)
- Record: tool calls, user corrections, error resolutions, repeated workflows
- Scope: project-specific patterns stay project-scoped, universal patterns become global

**Pattern Detection** (background analysis)
- User corrections become instinct candidates (confidence: 0.3-0.5 initially)
- Repeated successful patterns increase confidence (up to 0.9)
- Failed patterns decrease confidence or get removed

**Evolution Path**
```
Observation -> Instinct (0.3) -> Validated Instinct (0.7) -> Skill (0.9)
```

- Instincts below 0.5 confidence are suggestions only
- Instincts above 0.7 are auto-applied with logging
- Instincts at 0.9+ are candidates for promotion to reusable skills

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The model is expensive so the harness does not matter" | Harness optimization typically reduces tokens 40-60% with no quality loss |
| "Hooks slow down my workflow" | A well-tuned hook profile adds under 2 seconds and catches errors that cost minutes to debug later |
| "Cross-harness support is not needed -- I only use Claude Code" | Team members and CI pipelines may use different harnesses; parity prevents drift |
| "Memory persistence is overkill for small projects" | Even small projects benefit from remembering past decisions to avoid re-debating settled questions |
| "System prompt length does not matter with 200K context" | Longer system prompts increase latency, cost, and the chance the model ignores key instructions |

## Red Flags

- Token spend increasing without corresponding quality improvement
- Hooks producing errors or warnings that get ignored repeatedly
- Session context hitting limits mid-task (needs compaction strategy)
- Same bugs reappearing across sessions (memory/learning not working)
- Agent behavior differs significantly across harnesses for the same project
- Background processes leaking into main context window
- Hook scripts exceeding 3 seconds execution time
- System prompt over 8K tokens with no measurable quality benefit

## Verification

- [ ] System prompt audit complete: under 4K tokens for standard, under 8K for complex projects
- [ ] Model routing configured: fast/standard/premium tiers mapped to task complexity
- [ ] Memory persistence working: session start loads prior context, session end saves learnings
- [ ] Hook profile set to appropriate strictness for the current work mode
- [ ] Background isolation confirmed: no long-running commands in main context
- [ ] Cross-harness test passed: core workflow works on at least 2 harnesses
- [ ] Session metrics tracked: token cost per task measured and within budget
- [ ] Continuous learning active: observations being captured and instincts accumulating
