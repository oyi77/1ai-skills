---
name: oh-my-opencode
description: Use when working with OpenCode AI coding agent and oh-my-opencode harness to install, configure, and leverage
  its advanced features including Sisyphus, Hephaestus, Oracle, Librarian, and Explore agents
domain: integrations
tags:
- ai-agent
- api
- integrations
- opencode
- third-party
---

# Oh My OpenCode Integration

## Overview

Oh My OpenCode is the ultimate harness for OpenCode, providing advanced multi-model orchestration, curated agents, background task execution, and comprehensive tooling. This skill enables OpenClaw to leverage OpenCode's full potential with all the power of oh-my-opencode's agent ecosystem.

## When to Use

**Trigger phrases:**
- "oh my opencode"
- "Installing or configuring OpenCode with oh-my-opencode"
- "Operating OpenCode from OpenClaw environment"
- "Leveraging advanced agents (Sisyphus, Hephaestus, Oracle, Librarian, Explore)"


- Installing or configuring OpenCode with oh-my-opencode
- Operating OpenCode from OpenClaw environment
- Leveraging advanced agents (Sisyphus, Hephaestus, Oracle, Librarian, Explore)
- Running background agents and parallel tasks
- Using LSP/AST tools, MCP servers, and Claude Code compatibility
- Implementing autonomous deep work with goal-oriented execution

## Quick Start

1. **Install OpenCode and oh-my-opencode**:
   - Use the oh-my-opencode-installation skill for detailed setup
   - Or paste this to your LLM agent:
   ```
   Install and configure oh-my-opencode:
   https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.md
   ```

2. **Initialize for your project**:
   ```
   cd /path/to/project
   opencode
   /init
   ```

3. **Load this skill in OpenClaw**:
   - Load the oh-my-opencode skill
   - Configure according to your needs

## Core Agents
- Primary agent handles core task execution
- Validator agent checks output quality
- Reporter agent formats and delivers results
- Each agent operates with clear input/output contracts


### Sisyphus — Main Orchestrator
- The primary agent that coordinates all others
- Uses Prometheus (planner) and Metis (plan consultant)
- Executes with "ultrawork" mode for autonomous completion
- Delegates to specialized agents based on task requirements

### Hephaestus — Autonomous Deep Worker
- Goal-oriented execution (GPT 5.3 Codex Medium)
- Explores thoroughly before acting (2-5 parallel agents)
- End-to-end completion with verification
- Pattern matching for codebase consistency

### Oracle — Architecture & Debugging
- High-IQ strategic consultation (GPT 5.2)
- Complex debugging after 2+ failed attempts
- Architecture design decisions
- Multi-system tradeoffs analysis

### Librarian — Documentation & Search
- Official docs and open source implementations (GLM-4.7)
- Real-time source code digestion
- External library patterns and best practices

### Explore — Fast Codebase Exploration
- Contextual grep for rapid codebase analysis
- Pattern discovery across multiple modules
- Quick file and symbol location

## Installation Methods
This section covers installation methods for the oh-my-opencode skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### For Humans
```
Install and configure oh-my-opencode:
https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.md
```

### For LLM Agents
```bash
curl -s https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/docs/guide/installation.md
```

### Manual Installation
```bash
# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Install oh-my-opencode
npm install -g oh-my-opencode

# Or use npm directly
npm install -g @opencode-ai/plugin
```

## Configuration
```json
{
  "enabled": true,
  "autoRun": false,
  "timeout": 30000,
  "retries": 3
}
```

Set environment variables as needed for authentication and endpoints.


### Config Locations
- Project: `.opencode/oh-my-opencode.jsonc` or `.opencode/oh-my-opencode.json`
- User: `~/.config/opencode/oh-my-opencode.jsonc` or `~/.config/opencode/oh-my-opencode.json`

### Key Configuration Options
- **Agents**: Override models, temperatures, prompts for each agent
- **Built-in Skills**: playwright, git-master, and more
- **Background Tasks**: Concurrency limits per provider/model
- **Categories**: Domain-specific task delegation
- **Hooks**: 25+ configurable hooks
- **MCPs**: Built-in websearch (Exa), context7, grep_app
- **LSP**: Full LSP support with refactoring tools

## Features
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


### Agent Orchestration
- Multi-model support with intelligent routing
- Domain-specific task categories (visual, business-logic, etc.)
- Fallback chains and model recommendations

### Background Execution
- Run multiple agents in parallel like a real dev team
- Async task completion
- Todo continuation enforcement

### Tools & Refactoring
- Full LSP / AST Tools (refactoring, rename, diagnostics)
- Hash-anchored edit tool (LINE#ID format)
- AST-aware code search and replacement

### Claude Code Compatibility
- Commands, Agents, Skills, MCP, Hooks
- PreToolUse, PostToolUse, UserPromptSubmit, Stop hooks
- Full compatibility layer

### Session Management
- List, read, search, analyze session history
- Session continuity across agents
- Session-based task continuation

## Workflow Integration
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


### With OpenClaw
1. Load oh-my-opencode skill in OpenClaw
2. Ensure OpenCode is installed and configured
3. Use agents as needed for tasks
4. Leverage background execution for parallel work

### Best Practices
- Start with Sisyphus for complex tasks
- Use Hephaestus for autonomous deep work
- Consult Oracle for architecture decisions
- Use Librarian for unfamiliar libraries
- Employ Explore for rapid codebase analysis

### Common Patterns
- **Parallel exploration**: Fire 2-5 agents simultaneously
- **Deep work**: Use Hephaestus for thorough research first
- **Debugging**: Oracle after 2+ failed attempts
- **Documentation**: Librarian for official docs and OSS patterns

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |


### Plugin Not Loading
1. Verify config file location and format
2. Check permissions and dependencies
3. Review error logs: `opencode logs`

### Agent Issues
1. Check model availability and API keys
2. Review agent-specific configuration
3. Validate permissions settings

### Performance Issues
- Reduce concurrency limits
- Disable unused hooks
- Optimize model selections

## Safety & Considerations
This section covers safety & considerations for the oh-my-opencode skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Terms of Service
- OpenCode works with Claude, ChatGPT, and Gemini subscriptions
- Some plugins may have ToS implications
- Review official documentation for latest guidance

### Security
- Use official installation sources only
- Verify plugin origins before installing
- Review permissions before loading skills

## The Process

1. **Verify prerequisites** – Check Node.js 18+, OpenCode and oh-my-opencode are installed
2. **Install or verify installation** – Use oh-my-opencode-installation skill for guided setup
3. **Configure agents** – Set models, temperatures, and permissions in config location
4. **Choose the right agent** – Sisyphus for coordination, Hephaestus for deep work, Oracle for architecture, Librarian for docs, Explore for exploration
5. **Load skill in OpenClaw** – Ensure the skill is accessible to your agent environment
6. **Execute tasks** – Use agents with appropriate task categories for domain-specific work
7. **Monitor and iterate** – Watch agent output, adjust configuration as needed

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **Trying to use without OpenCode** – Oh My OpenCode is a harness on top of OpenCode, not a standalone tool
- **Using agents incorrectly** – Assigning simple tasks to Sisyphus (overkill) or complex tasks to quick category (under-scope)
- **Ignoring fallback chains** – Relying on single model when fallbacks configured for reliability
- **Skipping verification** – Not running lsp_diagnostics, build, or tests after agent completes
- **Confusing agent capabilities** – Using Librarian for code writing (use Hephaestus) or Explore for deep analysis (use Librarian)
- **Overriding built-in skills** – Removing playwright, git-master, which are critical for OpenCode workflows

## Verification

- **Installation verified**: Run `opencode --version` and `oh-my-opencode --help` - both should execute without error
- **Agent configuration**: Check `opencode config get agents` shows configured agents with models
- **Skill loaded**: Invoke skill tool and verify content loads without errors
- **Agent selection**: `/agent sisyphus` or `/agent hephaestus` should switch without error
- **Feature working**: `/help` shows expected commands, `/status` shows valid session state
- **Agent output**: Agent responds with domain-appropriate guidance, not generic responses
- **Background tasks**: Parallel agent launches complete within timeout, results accessible

## References

- Official Documentation: https://opencode.ai/docs/
- Oh My OpenCode: https://github.com/code-yeongyu/oh-my-opencode
- Installation Guide: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/guide/installation.md
- Features: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/features.md
- Configuration: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/configurations.md
- Agent-Model Matching: https://github.com/code-yeongyu/oh-my-opencode/blob/master/docs/guide/agent-model-matching.md

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |

## Related Skills

- oh-my-opencode-installation: Detailed installation guide
- oh-my-opencode-agents: Deep dive into each agent
- oh-my-opencode-configuration: Configuration options
- oh-my-opencode-features: Complete features list
- opencode-cli: OpenCode CLI usage

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
