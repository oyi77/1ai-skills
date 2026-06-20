---
name: oh-my-opencode-features
description: Complete reference of all oh-my-opencode features including agents, tools, MCPs, hooks, workflow automation,
  and productivity enhancements
domain: integrations
tags:
- ai-agent
- api
- features
- integrations
- opencode
- third-party
- workflow
---

# Oh My OpenCode Features

## Overview

This skill provides a comprehensive reference of all features available in oh-my-opencode, including curated agents, powerful tools, MCP integrations, hook systems, and productivity enhancements.

## When to Use

- **Agent orchestration** – When you need specialized agents for complex tasks, deep work, architecture decisions, documentation, or codebase exploration
- **MultiModel workflows** – When leveraging multiple LLM providers, fallback chains, or per-agent model optimization
- **Background execution** – When running parallel agents, async task completion, or autonomous deep work
- **LSP/AST tools** – When refactoring, renaming, searching code with AST awareness, or running diagnostics
- **Hooks integration** – When automating workflows via PreToolUse, PostToolUse, UserPromptSubmit, Stop triggers
- **Session management** – When managing session history, session continuity, or session-based task continuation
- **Workflow automation** – When using Ultrawork, Ralph Loop, TDD, debugging patterns
- **Quality verification** – When enforcing comment checks, TODO enforcement, and verification before completion

## Core Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### 1. Curated Agent System

#### Sisyphus — Main Orchestrator
- **Purpose**: Primary autonomous agent for complex tasks
- **Key Features**:
  - Goal-oriented execution without step-by-step instructions
  - Multi-model orchestration
  - Parallel agent launches (2-5 agents simultaneously)
  - Strict TODO list enforcement
  - Hash-anchored edit tool (LINE#ID format)
  - Comment checker for clean code
  - Claude Code compatibility layer

#### Hephaestus — Autonomous Deep Worker
- **Purpose**: Goal-oriented autonomous problem-solving
- **Key Features**:
  - Explores before acting (2-5 parallel explore/librarian agents)
  - End-to-end completion with verification
  - Pattern matching for codebase consistency
  - Surgical, minimal code generation
  - Thorough research before action

#### Oracle — Architecture & Debugging
- **Purpose**: High-IQ strategic consultation
- **Key Features**:
  - Complex debugging after 2+ failed attempts
  - Architecture design decisions
  - Multi-system tradeoffs analysis
  - Security/performance concerns review
  - Read-only consultation model

#### Librarian — Documentation & Search
- **Purpose**: External knowledge retrieval
- **Key Features**:
  - Official documentation search
  - Open source implementation patterns
  - Real-time source code digestion
  - Best practices for unfamiliar libraries
  - Multi-source search (docs, GitHub, Stack Overflow)

#### Explore — Fast Codebase Exploration
- **Purpose**: Rapid codebase analysis
- **Key Features**:
  - Blazing fast contextual grep
  - Pattern discovery across modules
  - Multiple search angles simultaneously
  - Quick file and symbol location

### 2. Multi-Model Orchestration

#### Model Selection
- Support for multiple LLM providers:
  - OpenAI (GPT-4o, GPT-4 Turbo, etc.)
  - Anthropic (Claude 3.5, Claude 3, etc.)
  - Google (Gemini Pro, etc.)
  - OpenCode Zen (curated models)

#### Fallback Chains
- Automatic fallback on model failure
- Configurable fallback order
- Per-agent model selection

#### Model Optimization
- Temperature tuning per agent
- Context window optimization
- Token usage tracking

### 3. Background Task Execution

#### Parallel Execution
- Run multiple agents simultaneously
- Async task completion
- Concurrent tool execution
- Background task persistence

#### Task Management
- Task queue with prioritization
- Progress tracking and reporting
- Task cancellation and restart
- Background/foreground switching

### 4. LSP & AST Tools

#### Built-in LSP Tools
- **lsp_diagnostics**: Get errors, warnings, hints
- **lsp_goto_definition**: Jump to symbol definition
- **lsp_find_references**: Find all usages of symbol
- **lsp_rename**: Rename symbol across workspace
- **lsp_symbols**: Get symbols from file/workspace
- **lsp_prepare_rename**: Check if rename is valid

#### AST-Grep Tools
- **ast_grep_search**: AST-aware code search
- **ast_grep_replace**: AST-aware code replacement
- Multi-language support (25+ languages)

#### Refactoring Capabilities
- Deterministic, surgical refactoring
- Safe multi-file changes
- Pattern-based code transformation

### 5. Hash-Anchored Edit Tool

#### How It Works
- Uses `LINE#ID` format for edits
- Validates content hash before applying changes
- Prevents stale-line edit errors
- Atomic, verifiable modifications

#### Usage Pattern
```typescript
// Before: Line 42 contains specific content
// Edit is anchored to content hash, not line number
// Ensures edit applies to intended location
```

### 6. MCP (Model Context Protocol) Integration

#### Built-in MCPs

| MCP | Provider | Purpose |
|-----|----------|---------|
| websearch | Exa | Web search for current information |
| context7 | Context7 | Official documentation lookup |
| grep_app | Grep.app | GitHub code search |
| playwright | Browser | Browser automation |
| git-master | Git | Git operations |

#### Custom MCPs
- Add custom MCP servers
- Configure MCP groups
- Per-project MCP settings
- MCP server authentication

### 7. Hook System

#### Available Hooks

| Hook | Purpose | Usage |
|------|---------|-------|
| PreToolUse | Validate before tool execution | Security, logging |
| PostToolUse | Process after tool execution | Verification, cleanup |
| UserPromptSubmit | Process user prompts | Context injection |
| Stop | Cleanup on session end | Resource cleanup |
| PreAgentRun | Before agent execution | Setup, validation |
| PostAgentRun | After agent completion | Review, logging |

#### Hook Configuration
- Enable/disable specific hooks
- Chain multiple handlers
- Custom hook scripts
- Per-agent hook settings

### 8. Claude Code Compatibility

#### Supported Features
- **Commands**: `/` commands for common actions
- **Agents**: Full agent system compatibility
- **Skills**: Skill tool integration
- **MCP**: MCP server integration
- **Hooks**: PreToolUse, PostToolUse, UserPromptSubmit, Stop

#### Compatibility Mode
- Seamless migration from Claude Code
- Identical command interface
- Shared configuration patterns

### 9. Session Management

#### Session Features
- **Session List**: View all sessions
- **Session Read**: Review previous sessions
- **Session Search**: Find by content
- **Session Export**: Share or backup

#### Session Persistence
- Configurable storage location
- Automatic session saving
- Session continuity across restarts
- Max session count management

### 10. Todo System

#### Features
- **TODO List**: Track all tasks
- **TODO Write**: Create/manage todos
- **Status Tracking**: Pending, in_progress, completed
- **Auto-Continuation**: Forces agent to finish

#### Enforcement
- Strict TODO following
- Auto-reminder for incomplete tasks
- Task completion verification
- Progress reporting

## Productivity Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### 1. Ralph Loop

**Purpose**: Self-referential development loop

**Features**:
- Automatic plan execution and validation
- Iterative improvement
- Goal tracking
- Progress monitoring

### 2. Ultrawork Mode

**Activation**: Include "ultrawork" or "ulw" in prompt

**Effects**:
- Parallel agents activate
- Background tasks enabled
- Deep exploration mode
- Relentless execution

### 3. Comment Checker

**Purpose**: Maintain code quality

**Rules**:
- Prevents excessive comments
- Justifies necessary comments
- Enforces code readability
- Follows project style

### 4. Context Injection

**Features**:
- Auto-inject AGENTS.md
- Conditional rules injection
- Project context awareness
- User preferences preservation

### 5. Auto-Completion

**Features**:
- End-to-end task completion
- Verification before finishing
- Evidence-based reporting
- Quality gate enforcement

## Workflow Enhancements
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


### 1. Parallel Agent Dispatching

```typescript
// Fire multiple agents for independent tasks
- Explore: Map codebase structure
- Librarian: Find relevant documentation
- Hephaestus: Research best practices
- Oracle: Review architecture
```

### 2. Subagent-Driven Development

```typescript
// Dispatch fresh subagent per task
- Two-stage review (spec, quality)
- No context pollution
- Parallel-safe execution
- Review checkpoints
```

### 3. Git Worktree Integration

```typescript
// Isolated workspace per task
- Create worktree for feature
- Commit to feature branch
- Merge when complete
- Clean up when done
```

### 4. Test-Driven Development

```typescript
// Subagents follow TDD
- Write test first
- Implement feature
- Verify tests pass
- Refactor as needed
```

### 5. Systematic Debugging

```typescript
// Structured debugging approach
- Reproduce issue
- Identify root cause
- Implement fix
- Verify solution
- Document learnings
```

## Tool Categories
| Tool | Purpose | Required |
|------|---------|----------|
| CLI | Primary execution | Yes |
| API client | External service calls | Conditional |
| Validator | Output checking | Recommended |


### File Operations
- **read**: Read file contents
- **write**: Write/overwrite files
- **edit**: Modify file contents
- **glob**: Find files by pattern
- **grep**: Search file contents

### Code Analysis
- **lsp_diagnostics**: Get diagnostics
- **lsp_goto_definition**: Jump to definition
- **lsp_find_references**: Find references
- **lsp_rename**: Rename symbol
- **ast_grep_search**: AST search
- **ast_grep_replace**: AST replace

### System Operations
- **bash**: Execute shell commands
- **interactive_bash**: Interactive terminal
- **session_***: Session management
- **Notion_***: Notion integration

### Browser Operations
- **skill_mcp**: MCP server tools
- **playwright**: Browser automation
- **dev-browser**: Persistent browser state
- **agent-browser**: CLI browser automation
- **browser-use**: Web automation

### Web Operations
- **websearch_web_search_exa**: Web search
- **google_search**: Google search + analysis
- **webfetch**: Fetch URL content
- **look_at**: Analyze media files

## Configuration Categories
```json
{
  "enabled": true,
  "autoRun": false,
  "timeout": 30000,
  "retries": 3
}
```

Set environment variables as needed for authentication and endpoints.


### Agent Configuration
- Model selection per agent
- Temperature tuning
- Permission settings
- Custom prompts

### Feature Configuration
- Parallel execution limits
- Background task settings
- Hook enable/disable
- Quality gate settings

### Integration Configuration
- MCP server setup
- Hook script configuration
- Plugin integration
- External tool connection

### UI Configuration
- Theme selection
- Keybind customization
- Layout preferences
- Display options

## Security Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### Permission System
- File system access control
- Network access restrictions
- Shell command allowlisting
- API key management

### Validation
- Input validation before execution
- Content hash verification
- Safe mode options
- Audit logging

### Compliance
- ToS-aware configuration
- Security best practices
- Audit trail maintenance
- Secret management

## Performance Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### Optimization
- Intelligent context truncation
- Token usage tracking
- Parallel execution efficiency
- Cache management

### Scalability
- Concurrent agent limits
- Resource usage monitoring
- Memory optimization
- Background task queuing

## Extensibility
This section covers extensibility for the oh-my-opencode-features skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Custom Tools
- Create custom tools
- Define tool schemas
- Implement execution logic
- Register with system

### Custom Hooks
- Write custom hooks
- Script integration
- Event-driven automation
- Workflow customization

### Plugin System
- Extend functionality
- Add new agents
- Integrate external services
- Customize behavior

## Comparison with Other Harnesses

| Feature | Oh My OpenCode | Standard OpenCode | Claude Code |
|---------|---------------|-------------------|-------------|
| Agents | 5 curated | Basic | 1 |
| Parallel Tasks | Yes | Limited | No |
| Background Exec | Yes | No | No |
| Hook System | 25+ | Basic | 4 |
| MCP Built-ins | 5+ | 0 | 0 |
| Claude Compat | Full | Full | Native |
| Hash Anchoring | Yes | No | No |
| TODO Enforcement | Yes | No | No |

## Feature Quick Reference

| Category | Key Features |
|----------|-------------|
| Agents | Sisyphus, Hephaestus, Oracle, Librarian, Explore |
| Models | OpenAI, Anthropic, Google, OpenCode Zen |
| Tools | LSP, AST-Grep, File Ops, Bash, Session |
| MCPs | websearch, context7, grep_app, playwright, git-master |
| Hooks | 25+ hooks, custom scripts, per-agent settings |
| Sessions | List, Read, Search, Export, Persistence |
| Workflow | Ultrawork, Ralph Loop, TDD, Debugging |
| Quality | Comment Checker, TODO Enforcement, Verification |

## The Process

1. **Identify feature needs** – Determine which oh-my-opencode features address your task (agents, MCPs, hooks, sessions, workflows)
2. **Verify feature availability** – Check feature is enabled in configuration and compatible with your OpenCode version
3. **Configure feature** – Set up MCP servers, hooks, categories as needed in config
4. **Load feature in session** – Ensure feature is accessible (agents via /agent, MCPs via /mcp, etc.)
5. **Use feature** – Execute feature-specific workflows (parallel agents, hooks, ultrawork, etc.)
6. **Monitor execution** – Watch feature behavior, adjust configs, debug issues
7. **Verify output** – Run lsp_diagnostics, build, tests to confirm feature completed correctly

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Feature conflicts** – Enabling multiple conflicting features (e.g., multiple LSP tools fighting over same file)
- **Version mismatch** – Using features from different oh-my-opencode versions causing incompatibilities
- **Missing dependencies** – Enabling MCPs without required tools or permissions
- **Hook loops** – Hooks triggering themselves infinitely due to improper conditions
- **Over-enforcement** – Enabling all quality checks when only specific ones needed causes slowdowns
- **Ignoring workflows** – Not following Ultrawork, Ralph Loop, or TDD when they should apply
- **Session corruption** – Attempting to use features on stale or corrupted sessions

## Verification

- **Feature loads**: Feature commands work (e.g., `/mcp list`, `/agent sisyphus`)
- **MCPs respond**: MCP servers execute tool calls and return expected results
- **Hooks fire**: Hook conditions trigger expected actions at right times
- **Sessions valid**: Session commands return valid data without errors
- **Workflows execute**: Ultrawork completes autonomously, TDD creates tests, Ralph Loop iterates to completion
- **Quality checks pass**: Comment checker, TODO enforcement, verification run as configured
- **Integration clean**: All features work together without conflicts or race conditions

## References

- Features Overview: https://github.com/code-yeongyu/oh-my-opencode#features
- Configuration: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/configurations.md
- Agent System: https://github.com/code-yeongyu/oh-my-opencode#for-those-who-want-to-read-meet-sisyphus
- OpenCode Docs: https://opencode.ai/docs/

## Related Skills

- oh-my-opencode: Overall integration
- oh-my-opencode-installation: Setup guide
- oh-my-opencode-agents: Agent deep dive
- oh-my-opencode-usage: Daily usage
- oh-my-opencode-configuration: Advanced setup
