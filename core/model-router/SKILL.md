---
name: model-router
description: Intelligent model routing via subagents - automatically spawn the right model for each task complexity. Use when executing complex tasks that benefit from specialized models, when you want to maintain fast session response times, when distributing workload across multiple models, when running parallel subagents with different capabilities, or when implementing adaptive model selection based on task requirements.
dependencies:
  - sessions_spawn
  - subagents
---

# Model Router Skill

Intelligent task routing that spawns subagents with optimal models based on task complexity.

## Overview

Model Router is an orchestration skill that intelligently selects the appropriate AI model for each task based on its complexity and requirements. It maintains fast response times in the main session while offloading complex work to specialized subagents. This skill enables parallel execution of multiple complex tasks with different model needs, optimizing both speed and capability.

## When to Use

- **Complex task handling**: Tasks requiring reasoning, long context, or deep analysis
- **Performance optimization**: When main session speed is critical but sub-tasks need power
- **Workload distribution**: When multiple complex tasks can run in parallel
- **Resource efficiency**: When you want to use the right model for each job
- **Task isolation**: When subagents need different capabilities or configurations
- **Scalable automation**: When building agent workflows with automatic model selection

## The Process
1. Validate input and check prerequisites
2. Initialize required connections and contexts
3. Execute core operation with monitoring
4. Validate output against expected format
5. Deliver results and log execution summary


### Step 1: Task Complexity Assessment

The router analyzes incoming requests to determine complexity level:

| Criteria | Fast | Balanced | Advanced | Reasoning | Code |
|----------|------|----------|----------|-----------|------|
| Simple interaction | ✅ | | | | |
| General analysis | | ✅ | | | |
| Strategy development | | | ✅ | | |
| Mathematical proofs | | | | ✅ | |
| Programming tasks | | | | | ✅ |
| Multi-step reasoning | | | ✅ | ✅ | ✅ |
| code review | | | | | ✅ |
| Complex synthesis | | | | | ✅ |

### Step 2: Route Selection

**Option A: Direct Response (Fast Model)**
```typescript
// For simple requests - handled directly
if (isSimpleRequest(request)) {
  return await fastModel.generate(request);
}
```

**Option B: Spawn Subagent (Complex Requests)**
```typescript
// For complex requests - spawn subagent
if (isComplexRequest(request)) {
  const subagent = spawnSubagent({
    model: determineOptimalModel(request),
    task: request,
    timeout: 120 // seconds
  });
  return await subagent.complete();
}
```

### Step 3: Subagent Configuration

```typescript
interface SubagentConfig {
  model: string;           // Model identifier
  task: string;           // Task description
  timeout: number;        // Execution timeout in seconds
  maxRetries: number;     // Retry attempts on failure
  parentSession?: string; // Session to continue
}
```

### Step 4: Execute and Collect Results

```typescript
async function executeWithRouter(task: string) {
  const complexity = analyzeComplexity(task);
  
  switch (complexity) {
    case 'simple':
      return await fastModel.generate(task);
    
    case 'balanced':
      const balancedAgent = spawnSubagent({
        model: 'balanced',
        task,
        timeout: 120
      });
      return await balancedAgent.complete();
    
    case 'complex':
      const complexAgent = spawnSubagent({
        model: 'advanced',
        task,
        timeout: 300
      });
      return await complexAgent.complete();
  }
}
```

### Step 5: Result Aggregation

Router collects subagent results and formats for consumption:

```typescript
// Subagent output format
interface SubagentResult {
  success: boolean;
  output: string;
  timing: {
    spawnTime: number;
    executionTime: number;
    totalTime: number
  };
  model: string;
  errors?: string[];
}
```

## Commands
| Command | Description |
|---------|-------------|
| `status` | Check current state and health |
| `run` | Execute the primary operation |
| `list` | Show available items or resources |
| `help` | Display usage information |


### Route Task with Explicit Model

```
route [task] with [model]
```

**Examples:**
```bash
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

## Model Tiers

| Tier | Model | Alias | Best For |
|------|-------|-------|----------|
| **Fast** | nvidia/meta/llama-3.2-1b-instruct | `fast` | Chat, simple QA, summaries |
| **Balanced** | nvidia/minimaxai/minimax-m2.1 | `balanced` | General tasks, analysis |
| **Advanced** | nvidia/moonshotai/kimi-k2.5 | `advanced` | Complex reasoning, long context |
| **Reasoning** | nvidia/deepseek-ai/deepseek-r1-distill-qwen-32b | `reasoning` | Math, logic, deep analysis |
| **Code** | nvidia/qwen/qwen2.5-coder-32b-instruct | `code` | Programming, debugging |

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
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


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

### Parallel Execution

```
You: Research three competitors and analyze their strategies
Router: [spawns 3 parallel subagents]
Subagent 1: [Researches competitor A]
Subagent 2: [Researches competitor B]
Subagent 3: [Researches competitor C]
Router: [aggregates all results]
```

## Workflow

1. User sends request
2. Router analyzes task complexity
3. If complex → spawn subagent with optimal model
4. Subagent performs work in background
5. Router presents results when complete

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- **❌ All tasks routed to fast model**: Complexity detection not working - check task descriptions
- **❌ Subagents not spawning**: Session spawn feature not configured or unavailable
- **❌ Timeout errors on all spawns**: Default timeout too short for complex tasks
- **❌ Wrong model selected**: Task description lack key indicators of complexity
- **❌ Concurrent task limit reached**: Max concurrent setting too low for workload
- **❌ Subagent hangs indefinitely**: Network issue or model unavailable
- **❌ Results not aggregating**: Router failure to collect subagent outputs

## Verification

**Connection Tests:**
```bash
# Verify subagent spawn capability
session info --spawn-enabled

# Check model availability
models list | grep -E "fast|balanced|advanced|reasoning|code"
```

**Functional Tests:**

1. **Simple Task Test:**
   ```bash
   route "What is 2+2?" with fast
   # Should return immediately without spawning
   ```

2. **Complex Task Test:**
   ```bash
   route "Write Python sorting algorithm" with code
   # Should spawn subagent and return working code
   ```

3. **Auto-Detection Test:**
   ```bash
   auto-route "Explain quantum computing"
   # Should auto-select appropriate model
   ```

**Configuration Verification:**
```bash
# Verify model mapping
cat config.json | jq '.modelRouter.tiers'

# Test each model alias
for tier in fast balanced advanced reasoning code; do
  echo "Testing $tier..."
  route "Test" with $tier 2>/dev/null && echo "✓ $tier OK" || echo "✗ $tier failed"
done
```

**Output Verification:**
```typescript
// Expected output format verification
interface RouterOutput {
  taskId: string;
  modelUsed: string;
  executionTime: number;
  success: boolean;
  result?: any;
  error?: string;
}
```

**Quick Health Check:**
```bash
echo "Model Router Check"
echo "=================="
echo "Spawn capability: $(session info --spawn-enabled 2>/dev/null && echo '✓' || echo '✗')"
echo "Model count: $(models list | wc -l)"
echo "Config valid: $(cat config.json | jq '.modelRouter.tiers' > /dev/null && echo '✓' || echo '✗')"
echo "Max concurrent: $(cat config.json | jq '.modelRouter.maxConcurrent' || echo '4 (default)')"
```
