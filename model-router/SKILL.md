---
name: model-router
description: Intelligent model routing via subagents - automatically spawn the right model for each task complexity
dependencies:
  - sessions_spawn
  - subagents
---

# Model Router Skill

Intelligent task routing that spawns subagents with optimal models based on task complexity.

## Philosophy

- **Main session**: Always fast (llama-3.2-1b) for instant responses
- **Subagents**: Spawned with task-appropriate models
- **Parallel execution**: Multiple complex tasks can run simultaneously

## Model Tiers

| Tier | Model | Alias | Best For |
|------|-------|-------|----------|
| **Fast** | nvidia/meta/llama-3.2-1b-instruct | `fast` | Chat, simple QA, summaries |
| **Balanced** | nvidia/minimaxai/minimax-m2.1 | `balanced` | General tasks, analysis |
| **Advanced** | nvidia/moonshotai/kimi-k2.5 | `advanced` | Complex reasoning, long context |
| **Reasoning** | nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b | `reasoning` | Math, logic, deep analysis |
| **Code** | nvidia/qwen/qwen2.5-coder-32b-instruct | `code` | Programming, debugging |

## Commands

### Route Task

```
route [task] with [model]
route analyze XAUUSD strategy with advanced
route debug this Python error with code
route deep research on quantum computing with reasoning
```

### Auto-Route (Smart Detection)

```
auto-route [task]
```

Automatically detects complexity and spawns appropriate subagent.

### Spawn with Model

```
spawn [task] --model [alias] [--timeout N]
```

## Task Complexity Detection

The router auto-detects task type:

**Fast (no spawn)**:
- Simple greetings
- Quick questions
- Status checks
- Acknowledgments

**Balanced**:
- Market summaries
- Strategy explanations
- General analysis

**Advanced**:
- Multi-step analysis
- Trading strategy development
- Complex calculations

**Reasoning**:
- Mathematical proofs
- Logical puzzles
- Deep analysis requiring step-by-step thinking

**Code**:
- Programming tasks
- Debugging
- Code review
- Technical implementation

## Usage Examples

### Trading Analysis
```
You: Analyze XAUUSD breakout strategy
Router: [spawns subagent with advanced model]
Subagent: [performs deep technical analysis]
Router: [presents summarized results]
```

### Coding Task
```
You: Fix this Python script for data processing
Router: [spawns subagent with code model]
Subagent: [debugs and refactors code]
Router: [presents solution]
```

### Simple Chat (No Spawn)
```
You: What's the weather?
Router: [handles directly with fast model]
```

## Workflow

1. User sends request
2. Router analyzes task complexity
3. If complex → spawn subagent with optimal model
4. Subagent performs work in background
5. Router presents results when complete

## Configuration

Override model mapping in config:

```json
{
  "modelRouter": {
    "tiers": {
      "fast": "nvidia/meta/llama-3.2-1b-instruct",
      "balanced": "nvidia/minimaxai/minimax-m2.1",
      "advanced": "nvidia/moonshotai/kimi-k2.5",
      "reasoning": "nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b",
      "code": "nvidia/qwen/qwen2.5-coder-32b-instruct"
    },
    "defaultTimeout": 120,
    "maxConcurrent": 4
  }
}
```
