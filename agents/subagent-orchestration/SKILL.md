---
name: subagent-orchestration
description: Subagent Context Package. Use when relevant to this domain.
domain: agents
---
## Overview

Subagent orchestration solves the fundamental challenge of multi-agent systems: agents lose critical context when spawned as subagents, leading to duplicated work, incorrect assumptions, and wasted tokens. This skill provides battle-tested patterns for managing context flow, parallelizing work across isolated instances, scaling with cascade methods, and evaluating agent output with formal grading systems.

## When to Use

- Spawning subagents that need codebase context they cannot predict upfront
- Building multi-agent workflows where context is progressively refined
- Encountering "context too large" or "missing context" failures in agent tasks
- Parallelizing independent tasks across git worktrees
- Scaling from 1 agent to N agents for large refactors or migrations
- Running checkpoint or continuous evaluations on agent output
- Coordinating multi-service workflows with PM2

## When NOT to Use

- Task can be done by a single agent without context issues
- Task is trivially simple (single file, obvious fix)
- You don't have git worktrees set up for parallelization
- Task requires real-time coordination (use message queues)
- You're building a custom agent framework (use development tools)
- Task is about agent training, not orchestration
- You don't need context management (task is self-contained)

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. The Context Problem

Subagents are spawned with limited context. They do not know:
- Which files contain relevant code
- What patterns exist in the codebase
- What terminology the project uses
- What decisions were already made upstream

**Standard approaches that fail:**

| Approach | Problem |
|----------|---------|
| Send everything | Exceeds context limits, wastes tokens on irrelevant code |
| Send nothing | Agent lacks critical information, makes incorrect assumptions |
| Guess what is needed | Often wrong, leads to iterative spawning failures |
| Send full AGENTS.md | Too broad, agent cannot find the needle in the haystack |

### 2. Iterative Retrieval Pattern

A 4-phase loop that progressively refines context for subagents:

```
Phase 1: DISPATCH   -- broad query to gather candidate files
Phase 2: EVALUATE   -- score candidates for relevance (0.0 - 1.0)
Phase 3: REFINE     -- update search criteria based on evaluation
Phase 4: LOOP       -- repeat (max 3 cycles), then proceed
```

**Phase 1: DISPATCH**
```markdown
Initial broad query:
- Patterns: src/**/*.ts, lib/**/*.ts
- Keywords: [task-specific terms from parent agent]
- Excludes: *.test.ts, *.spec.ts, node_modules/

Dispatch to retrieval subagent with: task description + search patterns
```

**Phase 2: EVALUATE**
```markdown
Score each retrieved file:
- High (0.8-1.0): Directly implements target functionality
- Medium (0.5-0.7): Contains related patterns or types
- Low (0.2-0.4): Tangentially related
- None (0-0.2): Not relevant, exclude from next cycle
```

**Phase 3: REFINE**
```markdown
Update search criteria:
- Add new patterns discovered in high-relevance files
- Add terminology found in codebase
- Exclude confirmed irrelevant paths
- Target specific gaps identified in evaluation
```

**Phase 4: LOOP**
```markdown
Repeat with refined criteria (max 3 cycles):
- Cycle 1: Broad discovery (expect 60% relevant)
- Cycle 2: Focused retrieval (expect 85% relevant)
- Cycle 3: Gap-filling (expect 95% relevant)
- After 3 cycles: proceed with available context
```

**Delivering Context to Subagent**
```markdown
# Subagent Context Package
## Task: [specific, bounded task description]

Replace this template with the actual task description for the subagent.

## Files: [top 5-10 most relevant files with line ranges]

Replace with actual file paths and line ranges relevant to the task.

## Patterns: [project conventions discovered during retrieval]

Replace with discovered naming, import, and error-handling patterns.

## Constraints: [what NOT to do, boundaries of the task]

Replace with explicit boundaries to prevent scope creep.

## Previous Decisions: [relevant upstream choices]
```

### 3. Parallelization with Git Worktrees

Use git worktrees to run multiple agents in isolated working directories:

```bash
# Create isolated worktrees for parallel work
git worktree add .worktrees/auth-feature -b feature/auth
git worktree add .worktrees/api-refactor -b refactor/api
git worktree add .worktrees/test-coverage -b test/coverage
```

**When to Parallelize**

| Parallelizable | Sequential |
|----------------|-----------|
| Independent feature branches | Dependent changes across modules |
| Separate file modifications | Shared file modifications |
| Independent test suites | Integration tests |
| Documentation updates | Database migrations |
| Linting/formatting | Architecture decisions |

**Worktree Orchestration Pattern**
```markdown
1. Decompose task into independent subtasks
2. Create one worktree per subtask
3. Spawn one agent per worktree with bounded context
4. Each agent works independently
5. Merge results: rebase onto main, resolve conflicts
6. Run integration tests on merged result
```

**Token Savings**
- Each agent operates with only its relevant context (not the full codebase)
- No cross-contamination between parallel tasks
- Typical savings: 40-70% tokens vs single-agent sequential approach

### 4. Cascade Method for Scaling Instances

Scale from 1 agent to N agents using a hierarchical cascade:

```
                    Lead Agent
                   /    |     \
            Worker 1  Worker 2  Worker 3
           /    \        |        \
      W1a   W1b      W2a        W3a
```

**Cascade Rules**
- Lead Agent: decomposes task, assigns subtasks, merges results
- Worker Agents: execute bounded subtasks, report back
- Leaf Workers: file-level changes, no further delegation
- Maximum depth: 3 levels (lead -> worker -> leaf)

**When to Use Cascade vs Flat**

| Cascade (hierarchical) | Flat (all peers) |
|------------------------|------------------|
| Task needs decomposition reasoning | Tasks are fully independent |
| Subtasks have dependencies | No cross-task coordination needed |
| Quality gate needed between phases | Speed is priority |
| Large refactors (100+ files) | Small parallel tasks (5-10 files each) |

### 5. Evaluation: Checkpoint vs Continuous

**Checkpoint Evals**
Run at defined milestones (end of phase, before merge, before deploy):
```markdown
[CHECKPOINT EVAL: phase-name]
Tests:
  - [ ] All unit tests pass
  - [ ] Integration tests pass
  - [ ] No lint errors
  - [ ] Type checking passes
  - [ ] Build succeeds
Result: X/Y passed -> proceed or block
```

**Continuous Evals**
Run after every significant change (every edit, every commit):
```markdown
[CONTINUOUS EVAL: after-each-edit]
Trigger: PostToolUse (Edit/Write)
Tests:
  - [ ] File still passes type check
  - [ ] Related tests still pass
  - [ ] No new lint warnings
Result: Real-time pass/fail feedback
```

**When to Use Each**

| Checkpoint | Continuous |
|------------|-----------|
| Large tasks with clear phases | Small incremental changes |
| Expensive evals (full test suite) | Cheap evals (single file lint) |
| Team workflows with review gates | Solo agent workflows |
| CI/CD pipeline integration | Local development |

### 6. Grader Types and pass@k Metrics

**Grader Types**

**Code-Based (deterministic)**
```bash
grep -q "expected_pattern" src/file.ts && echo "PASS" || echo "FAIL"
npm test -- --testPathPattern="feature" && echo "PASS" || echo "FAIL"
```

**Model-Based (LLM evaluation)**
```markdown
Evaluate: Does this code change solve the stated problem?
Score 1-5. Pass threshold: >= 4.
```

**Human (flag for review)**
```markdown
[HUMAN REVIEW] Change: description. Risk: HIGH. Requires manual sign-off.
```

**pass@k Metrics**
- pass@1: First attempt success rate (target: >70%)
- pass@3: Success within 3 attempts (target: >90%)
- pass^k: All k trials succeed (use for critical paths)
- Track regressions: if pass@k drops after a change, investigate immediately

### 7. PM2 and Multi-Agent Orchestration

Use PM2 to manage long-running agent processes:

```bash
# Start multi-agent workflow
pm2 start ecosystem.config.js

# Monitor all agents
pm2 monit

# View agent logs
pm2 logs agent-backend
pm2 logs agent-frontend

# Restart failed agent
pm2 restart agent-backend
```

**Ecosystem Config Pattern**
```javascript
module.exports = {
  apps: [
    { name: 'agent-backend',  script: 'agent.js', args: '--role backend',  instances: 2 },
    { name: 'agent-frontend', script: 'agent.js', args: '--role frontend', instances: 1 },
    { name: 'agent-test',     script: 'agent.js', args: '--role test',     instances: 1 },
  ]
};
```

**PM2 Orchestration Rules**
- One PM2 process per agent role (not per file)
- Use `--max-restarts 3` to prevent infinite restart loops
- Log to files, not stdout, for post-mortem analysis
- Monitor memory: agents with context bloat need compaction

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I will just send all context to the subagent" | Context bloat causes the agent to miss what matters; targeted context outperforms everything dumps |
| "Parallelization is always faster" | Coordination overhead can exceed parallelism gains for tasks under 5 minutes |
| "Continuous evals are too expensive" | A single broken change caught early costs 10x less than debugging after a full task completes |
| "The parent agent knows what context the subagent needs" | Parents optimize for their own understanding; iterative retrieval discovers what the subagent actually needs |
| "PM2 is overkill for agent orchestration" | When running 3+ agents with restart logic and logging, PM2 saves hours of manual management |

## Red Flags

- Subagent asking for files the parent already read (context not passed)
- Same subagent spawned repeatedly for the same task (context failure loop)
- Parallel agents modifying the same file (worktree isolation not used)
- Evaluation running only at the very end (defeats the purpose of eval-driven development)
- pass@1 below 50% (agent reliability issue, needs better prompts or context)
- Cascade depth exceeding 3 levels (over-delegation, decompose differently)
- PM2 processes crashing and restarting in a loop (check memory and context size)
- Token spend per subagent exceeding the parent agent (context packaging problem)

## Verification

- [ ] Context problem addressed: subagents receive targeted, relevant context via iterative retrieval
- [ ] Parallelization used correctly: independent tasks in separate worktrees, no shared-file conflicts
- [ ] Cascade depth under 3: no excessive delegation chains
- [ ] Evaluation strategy chosen: checkpoint for large phased tasks, continuous for incremental work
- [ ] Grader type appropriate: code-based for deterministic checks, model-based for quality assessment
- [ ] pass@k metrics tracked: pass@1 > 70%, pass@3 > 90%
- [ ] PM2 configured for long-running workflows: restart limits, log files, memory monitoring
- [ ] Token cost per subagent is lower than equivalent single-agent approach
