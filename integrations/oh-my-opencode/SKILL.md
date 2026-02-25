---
name: oh-my-opencode
description: Use oh-my-opencode for advanced coding tasks with Sisyphus, Hephaestus, Oracle, Librarian, and Explore agents
permissions:
  - fs
  - network
---

# Oh My OpenCode - Advanced Coding

Leverage oh-my-opencode for complex coding tasks, multi-agent orchestration, and autonomous development work.

## When to Use

- Complex refactoring across multiple files
- Multi-agent parallel execution
- Deep codebase exploration
- Architecture design and debugging
- Background task execution

## Quick Start

```bash
# Install oh-my-opencode
curl -fsSL https://opencode.ai/install | bash

# Initialize in your project
cd /path/to/project
opencode
```

## Core Agents

### Sisyphus - Main Orchestrator
Coordinates all agents, executes with "ultrawork" mode for autonomous completion.

### Hephaestus - Deep Worker
Goal-oriented execution, explores thoroughly before acting (2-5 parallel agents).

### Oracle - Architecture & Debugging
High-IQ consultation, complex debugging, system design decisions.

### Librarian - Documentation & Search
Official docs, real-time source code digestion, external library patterns.

### Explore - Fast Exploration
Contextual grep, rapid codebase analysis, pattern discovery.

## Key Commands

```bash
# Initialize opencode
opencode

# Load project
opencode load /path/to/project

# Run with specific agent
opencode --agent hephaestus --prompt "Refactor this module"

# Deep exploration
opencode --agent librarian --query "How to implement pattern X"
```

## Integration with Trading Skills

Use oh-my-opencode to develop trading strategies, backtest engines, and broker connectors:

```bash
cd skills/1ai-skills/trading
opencode
# Then use agents for complex refactoring or new features
```

## Configuration

- Config file: `.opencode/oh-my-opencode.jsonc` or `.opencode/oh-my-opencode.json`
- User config: `~/.config/opencode/oh-my-opencode.jsonc`
- Override models, temperatures, prompts per agent

## Best Practices

1. **Parallel exploration**: Fire 2-5 agents simultaneously
2. **Deep work**: Use Hephaestus for thorough research first
3. **Debugging**: Oracle after 2+ failed attempts
4. **Documentation**: Librarian for official docs and OSS patterns
