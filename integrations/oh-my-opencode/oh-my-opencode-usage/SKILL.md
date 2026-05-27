---
name: oh-my-opencode-usage
description: Daily usage patterns for oh-my-opencode including workflow commands, session management, agent invocation, and productivity tips
---

# Oh My OpenCode Usage

## Overview

This skill provides practical guidance for daily use of oh-my-opencode, covering common workflows, commands, session management, and productivity patterns.

## When to Use

- **Starting new project** – When initializing OpenCode and oh-my-opencode for a new project
- **Daily development** – When using OpenCode for regular coding tasks, debugging, or code review
- **Multi-step workflows** – When following Plan First/Build Later or Direct Implementation patterns
- **Agent delegation** – When switching between Sisyphus, Hephaestus, Oracle, Librarian, Explore agents
- **Session management** – When saving, restoring, or sharing OpenCode sessions
- **Configuration validation** – When verifying oh-my-opencode configuration is working correctly
- **Troubleshooting** – When diagnosing OpenCode issues or agent behavior

## Getting Started

### Starting a Session

```bash
# Navigate to your project
cd /path/to/project

# Start OpenCode
opencode

# Or start with specific configuration
opencode --config /path/to/config.json
```

### Initializing a Project

```bash
# Inside OpenCode
/init
```

This creates an `AGENTS.md` file in your project root, helping OpenCode understand your project structure and coding patterns.

## Core Commands

### Session Commands

| Command | Description |
|---------|-------------|
| `/init` | Analyze project and create AGENTS.md |
| `/help` | Show available commands |
| `/status` | Show current session status |
| `/config` | Manage configuration |
| `/undo` | Undo last changes |
| `/redo` | Redo undone changes |
| `/share` | Share current conversation |
| `/quit` | Exit OpenCode |

### Agent Commands

| Command | Description |
|---------|-------------|
| `/agent` | Switch agent type |
| `/model` | Change model |
| `/temperature` | Adjust temperature |
| `/context` | Manage context window |

### Tool Commands

| Command | Description |
|---------|-------------|
| `/lsp` | LSP operations |
| `/mcp` | Manage MCP servers |
| `/grep` | Search codebase |
| `/read` | Read file |
| `/edit` | Edit file |
| `/write` | Write file |

## Workflow Patterns

### Pattern 1: Plan First, Build Later

**Use when**: Adding new features or making significant changes

1. **Switch to Plan mode**:
   ```
   <TAB>
   ```

2. **Describe what you want**:
   ```
   I want to add user authentication with OAuth.
   Consider using the existing auth patterns in auth/
   directory. Include login, logout, and session management.
   ```

3. **Review and iterate**:
   ```
   That plan looks good, but add password reset functionality.
   ```

4. **Switch to Build mode**:
   ```
   <TAB>
   Sounds good! Go ahead and make the changes.
   ```

### Pattern 2: Direct Implementation

**Use when**: Making straightforward changes

```
Take a look at @src/utils/helper.ts and add error handling
to the parse function following the pattern in @src/utils/validator.ts
```

### Pattern 3: Exploration First

**Use when**: Working with unfamiliar code

```
How is authentication handled in @packages/functions/src/api/index.ts?
Explain the key components and flow.
```

### Pattern 4: Parallel Agents

**Use when**: Complex tasks benefit from multiple perspectives

```bash
# Fire multiple agents in parallel
Hephaestus: Research the best approach for this feature
Librarian: Find official documentation for the library
Explore: Map out the existing codebase structure
Oracle: Review the architecture decision
```

### Pattern 5: Background Execution

**Use when**: Long-running tasks

1. **Start background task**:
   ```
   Run a comprehensive test suite and report results
   ```

2. **Continue working** while it runs:
   ```
   Meanwhile, review the PR comments
   ```

3. **Check results**:
   ```
   Check background task status
   ```

## Agent Invocation

### Sisyphus Usage

**When to use**: Complex multi-step tasks requiring orchestration

```
Sisyphus, implement a new feature for user notifications:
- Include email and push notifications
- Follow the existing notification patterns
- Write tests for all new code
- Update documentation
```

### Hephaestus Usage

**When to use**: Autonomous deep work requiring research

```
Hephaestus, research and implement a new caching layer:
1. Analyze current performance bottlenecks
2. Research best practices for Redis caching
3. Implement the solution
4. Test thoroughly
```

### Oracle Usage

**When to use**: After 2+ failed attempts or architecture decisions

```
Oracle, I've tried three approaches to fix this bug but
the issue persists. Can you review the code and suggest
a different approach?
```

### Librarian Usage

**When to use**: Working with unfamiliar libraries

```
Librarian, how do I implement rate limiting with this
library? Find the official documentation and examples.
```

### Explore Usage

**When to use**: Quick codebase exploration

```
Explore, find all uses of the `parseConfig` function
and show me how it's called across the codebase.
```

## Session Management

### Session Continuity

OpenCode maintains session history that can be useful:

```bash
# List sessions
/sessions list

# Read previous session
/sessions read <session-id>

# Search sessions
/sessions search "authentication"
```

### Session Files

Sessions are stored in:
- **Global**: `~/.config/opencode/sessions/`
- **Project**: `.opencode/sessions/`

### Exporting Sessions

```bash
# Share current session
/share

# Export to file
/sessions export <session-id> --output session.json
```

## File References

### Using @ for File References

```bash
# Reference a specific file
@src/auth/login.ts

# Reference with line numbers
@src/utils/helper.ts:42

# Reference with symbol
@src/utils/helper.ts#parseFunction
```

### Quick File Actions

```bash
# Read and explain
@src/api/controller.ts Explain the main flow

# Read and summarize
@src/docs/architecture.md Summarize key points

# Find and display
@src/**/*test*.py Show me the test patterns
```

## Productivity Tips

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Toggle Plan/Build mode |
| `Ctrl+P` | Command palette |
| `Ctrl+F` | Find in conversation |
| `Ctrl+R` | Redo |
| `Ctrl+Z` | Undo |

### Efficient Prompting

**Good**:
```
Add error handling to @src/services/payment.ts following
the pattern in @src/services/validation.ts. Include
specific error codes and logging.
```

**Bad**:
```
Fix the payment service
```

### Managing Context

- Use `@` to reference files instead of pasting code
- Break complex tasks into smaller steps
- Use Plan mode for complex changes
- Review context before making decisions

### Multi-Model Workflow

```bash
# Use cheaper model for exploration
/model cheap

# Explore codebase
Find all API endpoints

# Switch to capable model for implementation
/model gpt-4o

# Implement the feature
```

## Common Use Cases

### Code Review

```bash
# Start a review session
Review @src/api/user.ts for:
- Error handling completeness
- Security vulnerabilities
- Performance issues
- Code style consistency
```

### Debugging

```bash
# Start debugging session
The function at @src/utils/parser.ts:123 is failing
with "undefined is not a function". Help me debug.
```

### Documentation

```bash
# Generate documentation
Generate API documentation for @src/api/ based on
the existing docstring patterns. Include examples.
```

### Refactoring

```bash
# Plan refactoring
Refactor @src/core/ to use the factory pattern
shown in @src patterns/factory/. Plan first.
```

### Testing

```bash
# Generate tests
Add unit tests for @src/services/notification.ts
following the existing test patterns in @src tests/.
Aim for 80% coverage.
```

## Configuration Profiles

### Create Profile

```jsonc
// ~/.config/opencode/profiles/development.json
{
  "name": "development",
  "model": "openai/gpt-4o",
  "temperature": 0.7,
  "mcp": ["websearch", "context7"],
  "features": {
    "agent": true,
    "background": true
  }
}
```

### Switch Profile

```bash
/profile development
/profile production
```

## Integration with OpenClaw

### Using Both Tools

1. **Load oh-my-opencode in OpenClaw**:
   ```
   Load the oh-my-opencode skill
   ```

2. **Use OpenCode commands**:
   ```
   Run /init on the current project
   ```

3. **Leverage agents**:
   ```
   Sisyphus, help me with this refactoring task
   ```

### Coordination Patterns

```
# In OpenClaw
Use oh-my-opencode to initialize the project
Then switch to Sisyphus for the implementation
Consult Oracle if architecture questions arise
Use Explore for quick codebase queries
```

## Best Practices

### 1. Start with /init
Always initialize new projects to let OpenCode understand your codebase.

### 2. Use Plan Mode for Complex Changes
Toggle to Plan mode (`<TAB>`) for significant modifications.

### 3. Reference Files Directly
Use `@` for file references instead of pasting code.

### 4. Leverage Parallel Agents
For complex tasks, fire multiple agents in parallel.

### 5. Review Before Building
Use Plan mode to review and iterate before implementing.

### 6. Use Sessions Effectively
Save and reference sessions for context continuity.

### 7. Leverage MCPs
Use built-in MCPs for web search, documentation, and code search.

## Troubleshooting

### Slow Response
- Reduce context size
- Switch to faster model
- Disable unused features

### Context Overflow
- Break into smaller tasks
- Use file references instead of pasting
- Clear conversation history

### Unexpected Behavior
- Check current agent/model
- Review configuration
- Restart session if needed

## Quick Reference

| Task | Command/Pattern |
|------|-----------------|
| Add feature | Plan mode → Review → Build mode |
| Debug issue | Direct mode → Oracle if stuck |
| Explore code | `@file` or Explore agent |
| Find patterns | `grep` or Explore agent |
| Write tests | Direct mode with pattern reference |
| Code review | Direct mode with specific criteria |
| Documentation | Librarian + Direct mode |

## The Process

1. **Start session** – Navigate to project and run `opencode`, or use specific config with `opencode --config`
2. **Initialize project** – Run `/init` to create AGENTS.md and analyze codebase
3. **Choose workflow pattern** – Select from: Plan First/Build Later, Direct Implementation, Task-based delegation
4. **Load appropriate skill** – Ensure relevant oh-my-opencode skills are accessible to agent
5. **Execute commands** – Run session commands (`/help`, `/status`, `/undo`, `/redo`, etc.)
6. **Delegate tasks** – Use agents explicitly (`/agent sisyphus`, `/agent hephaestus`, etc.) or implicitly via commands
7. **Monitor execution** – Watch agent output, tool usage, and progress indicators
8. **Verify output** – Run lsp_diagnostics, build, and tests on agent-generated code
9. **Continue or exit** – Save session with `/share` or exit with `/quit`

## Red Flags

- **Not initializing project** – Skipping `/init` for new projects causes AGENTS.md absence, poor agent behavior
- **Confusing modes** – Using Direct mode for complex planning, or Plan mode for quick edits
- **Wrong agent selection** – Using Sisyphus for trivial edits, or direct mode for complex refactoring
| **Ignoring tool commands** – Not using `/lsp`, `/mcp`, `/read`, `/edit`, `/write` when needed
- **Skipping verification** – Assuming agent work is correct without running tests
- **Session drift** – Running multiple unrelated tasks without session structure causing context pollution
- **Pattern mismatch** – Using Plan First pattern for straightforward changes, wasting time

## Verification

- **Session starts**: `opencode` enters TUI or CLI without errors
- **Init succeeds**: `/init` creates AGENTS.md in project root
- **Commands work**: All session commands execute without errors (`/help`, `/status`, `/agent`, `/undo`, etc.)
- **Agents responding**: `/agent <name>` switches agent successfully, agents respond to commands
- **Tool commands functional**: `/read`, `/edit`, `/write`, `/mcp` execute as expected
- **Workflow patterns complete**: Plan First or Direct mode execute successfully end-to-end
- **Output verified**: Agent-generated code passes lsp_diagnostics, build, and tests
- **Clean exit**: `/quit` exits cleanly, `/share` produces expected output

## References

- OpenCode CLI: https://opencode.ai/docs/cli/
- OpenCode TUI: https://opencode.ai/docs/tui/
- Agent System: https://github.com/code-yeongyu/oh-my-opencode#for-those-who-want-to-read-meet-sisyphus
- Configuration: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/configurations.md

## Related Skills

- oh-my-opencode: Overall integration
- oh-my-opencode-agents: Agent deep dive
- oh-my-opencode-installation: Setup guide
- oh-my-opencode-configuration: Advanced setup
