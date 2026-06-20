---
name: agent-orchestrator
description: Multi-agent coordination framework. Define agent teams, task delegation, memory sharing, conflict resolution
  for complex workflows. Use when coordinating multiple AI agents working together on large-scale tasks.
domain: agents
tags:
- multi-agent
- orchestration
- coordination
- teamwork
- delegation
- memory-sharing
---

# Agent Orchestrator

Multi-agent coordination framework for complex workflows. Define agent teams, delegate tasks with context passing, share memory across agents, resolve conflicts, and visualize execution flows.

**Source:** GitHub trending (obra/superpowers, anthropics/skills, agent coordination patterns)

## When to Use

**Trigger phrases:**
- "Coordinate multiple agents on this task"
- "Build an agent team for this workflow"
- "Delegate work across specialized agents"
- "Manage agent collaboration"
- "Resolve conflicts between agents"

**Use cases:**
- Complex software development (design, code, test, deploy)
- Research projects (gather, analyze, synthesize, report)
- Content production (script, voiceover, video, publish)
- Business operations (data, analysis, recommendations, reporting)
- Security audits (scan, analyze, prioritize, remediate)

**When NOT to use:**
- Single-agent tasks (use regular task delegation)
- Sequential workflows with no parallelism
- Tasks requiring human decision at each step

## Core Concepts

### Agent Team Structure

```python
team = {
    "name": "ContentProduction",
    "agents": [
        {"id": "Researcher", "role": "Content research and fact-checking"},
        {"id": "Scriptwriter", "role": "Script generation and editing"},
        {"id": "VoiceArtist", "role": "Narration and TTS"},
        {"id": "VideoEditor", "role": "Video assembly and effects"},
        {"id": "Publisher", "role": "Platform distribution"}
    ],
    "workflow": "pipeline",  # or "parallel", "dag"
    "memory": "shared"       # or "isolated"
}
```

### Workflow Types

| Type | Description | Use When |
|------|-------------|----------|
| **Pipeline** | Sequential, each agent waits for previous | Order matters (research → write → edit) |
| **Parallel** | All agents work independently | No dependencies (scan multiple repos) |
| **DAG** | Directed acyclic graph with dependencies | Complex workflows with branches |
| **Swarm** | Agents self-organize and collaborate | Emergent behavior needed |

## Installation

This skill uses existing 1ai-skills infrastructure:
 `skill://subagent-driven-development` — Agent spawning
 `skill://hive-mind` — Inter-agent communication
- `skill://teamwork` — Team management

No additional installation required.

## Quick Start

### Simple Pipeline

```python
from agent_orchestrator import Orchestrator, Pipeline

# Define team
team = Pipeline([
    {"id": "Researcher", "role": "Research topic and gather facts"},
    {"id": "Writer", "role": "Write article from research"},
    {"id": "Editor", "role": "Edit and polish article"}
])

# Initialize orchestrator
orch = Orchestrator(team)

# Execute pipeline
result = orch.run(
    input="Write an article about AI agents",
    context={
        "target_length": 1000,
        "tone": "professional",
        "audience": "developers"
    }
)

print(f"Final article: {result.output}")
print(f"Pipeline time: {result.duration}s")
```

### Parallel Execution

```python
from agent_orchestrator import Orchestrator, Parallel

# Define parallel team
team = Parallel([
    {"id": "SecurityScanner", "role": "Scan for vulnerabilities"},
    {"id": "CodeReviewer", "role": "Review code quality"},
    {"id": "TestRunner", "role": "Run test suite"},
    {"id": "LintChecker", "role": "Check code style"}
])

orch = Orchestrator(team)

# All agents work simultaneously
result = orch.run(
    input="Audit codebase at /path/to/repo",
    merge_strategy="union"  # Combine all results
)

# Aggregated results
print(f"Vulnerabilities: {result.security_issues}")
print(f"Code issues: {result.code_issues}")
print(f"Test failures: {result.test_failures}")
print(f"Style violations: {result.lint_issues}")
```

### DAG (Complex Workflow)

```python
from agent_orchestrator import Orchestrator, DAG

# Define dependencies
team = DAG()

# Add agents
team.add_agent("DataCollector", role="Collect raw data")
team.add_agent("DataCleaner", role="Clean and validate data")
team.add_agent("Analyzer1", role="Statistical analysis")
team.add_agent("Analyzer2", role="ML analysis")
team.add_agent("Reporter", role="Generate report")

# Define dependencies (who waits for whom)
team.add_dependency("DataCleaner", depends_on="DataCollector")
team.add_dependency("Analyzer1", depends_on="DataCleaner")
team.add_dependency("Analyzer2", depends_on="DataCleaner")
team.add_dependency("Reporter", depends_on=["Analyzer1", "Analyzer2"])

orch = Orchestrator(team)
result = orch.run(input="Analyze sales data for Q4 2025")
```

## Memory Management

### Shared Memory

All agents read/write to shared memory:

```python
team = Pipeline([...], memory="shared")

# Agent 1 writes
memory.set("user_preferences", {"theme": "dark", "lang": "en"})

# Agent 2 reads
prefs = memory.get("user_preferences")
```

### Isolated Memory

Each agent has private memory:

```python
team = Parallel([...], memory="isolated")

# Agent 1's memory is separate from Agent 2
# No cross-contamination
```

### Hierarchical Memory

Parent agent sees all child memories, children see only their own:

```python
team = DAG(memory="hierarchical")

# Parent "Manager" can read all agent memories
# Individual agents only see their own + parent's
```

## Communication Patterns

### Message Passing

```python
# Agent 1 sends to Agent 2
irc.send(to="Writer", message="Research complete. Key findings: ...", data=findings)

# Agent 2 receives
msg = irc.wait(from_sender="Researcher")
findings = msg.data
```

### Broadcast

```python
# Send to all agents
irc.send(to="all", message="Context updated: new requirements added")
```

### Request-Reply

```python
# Agent asks for help
response = irc.send(
    to="ExpertAgent",
    message="How should I handle edge case X?",
    await_reply=True
)
```

## Conflict Resolution

### Vote-Based

```python
from agent_orchestrator import ConflictResolver, VotingResolver

# Multiple agents propose solutions
proposals = [
    {"agent": "A", "solution": "Approach 1", "confidence": 0.8},
    {"agent": "B", "solution": "Approach 2", "confidence": 0.9},
    {"agent": "C", "solution": "Approach 1", "confidence": 0.7}
]

resolver = VotingResolver(strategy="weighted")  # weight by confidence
chosen = resolver.resolve(proposals)
# → "Approach 1" (2 votes, weighted score: 1.5)
```

### Consensus-Based

```python
from agent_orchestrator import ConsensusResolver

resolver = ConsensusResolver(threshold=0.66)  # 66% agreement needed

# Agents discuss and converge
final = resolver.reach_consensus(
    agents=team.agents,
    question="What's the root cause of the bug?",
    max_rounds=5
)
```

### Priority-Based

```python
# Higher-priority agent wins
team = Pipeline([
    {"id": "Junior", "priority": 1},
    {"id": "Senior", "priority": 10},
    {"id": "Architect", "priority": 20}
])

# Architect's decisions override others
```

## Advanced Patterns

### Self-Organizing Swarm

```python
from agent_orchestrator import Swarm

team = Swarm(
    agent_count=5,
    base_role="Explore solution space",
    emergence_rules={
        "cooperation": True,
        "competition": False,
        "specialization": "auto"  # Agents self-specialize
    }
)

# Agents coordinate organically
result = team.solve(problem="Find optimal algorithm parameters")
```

### Hierarchical Teams

```python
# Manager delegates to specialists
manager = Agent("ProjectManager", role="Coordinate project")

frontend_team = Pipeline([
    Agent("UIDesigner"),
    Agent("ReactDeveloper"),
    Agent("CSSExpert")
])

backend_team = Pipeline([
    Agent("APIDesigner"),
    Agent("DatabaseExpert"),
    Agent("DevOpsEngineer")
])

# Manager oversees both teams
orch = Orchestrator.hierarchical(
    manager=manager,
    teams=[frontend_team, backend_team]
)
```

### Retry and Failover

```python
team = Pipeline([...])

result = orch.run(
    input="Task description",
    retry_policy={
        "max_retries": 3,
        "backoff": "exponential",
        "failover": "next_agent"  # Skip failed agent, continue
    }
)
```

## Monitoring and Visualization

### Real-Time Dashboard

```python
# Start monitoring server
orch.start_dashboard(port=8080)

# View at http://localhost:8080
# - Agent status (idle/working/blocked)
# - Task progress
# - Message flow
# - Memory state
# - Performance metrics
```

### Execution Trace

```python
# Log all agent actions
orch.enable_tracing(output="trace.json")

# After execution
trace = orch.get_trace()
for event in trace:
    print(f"{event.timestamp}: {event.agent} - {event.action}")
```

### Performance Metrics

```python
metrics = orch.get_metrics()

print(f"Total time: {metrics.duration}s")
print(f"Agent utilization: {metrics.utilization}%")
print(f"Messages exchanged: {metrics.message_count}")
print(f"Memory used: {metrics.memory_mb}MB")
```

## Complete Example: Content Production

```python
from agent_orchestrator import Orchestrator, Pipeline

# Define content production pipeline
team = Pipeline([
    {
        "id": "Researcher",
        "role": "Research topic and gather facts",
        "skills": ["deep-research-pro", "social-intelligence"],
        "timeout": 300
    },
    {
        "id": "Scriptwriter",
        "role": "Write engaging script from research",
        "skills": ["content-planner-auto", "viral-content-creator"],
        "timeout": 600
    },
    {
        "id": "VoiceArtist",
        "role": "Generate narration audio",
        "skills": ["voice-chatterbox-tts"],
        "timeout": 300
    },
    {
        "id": "VideoMatcher",
        "role": "Find relevant video clips",
        "skills": ["video-semantic-match"],
        "timeout": 300
    },
    {
        "id": "VideoEditor",
        "role": "Assemble final video",
        "skills": ["remotion", "video-editor"],
        "timeout": 600
    }
])

# Shared context
context = {
    "topic": "How AI agents work together",
    "target_platform": "YouTube",
    "duration": 300,  # 5 minutes
    "style": "educational",
    "voice": "professional male"
}

# Execute pipeline
orch = Orchestrator(team, memory="shared")

result = orch.run(
    input=f"Create a {context['duration']}s video about {context['topic']}",
    context=context,
    monitor=True,  # Real-time dashboard
    save_artifacts=True  # Save intermediate outputs
)

# Output
print(f"Video created: {result.video_path}")
print(f"Script: {result.artifacts['script']}")
print(f"Audio: {result.artifacts['audio']}")
print(f"Total time: {result.duration}s")
print(f"Agent breakdown:")
for agent, time in result.agent_times.items():
    print(f"  {agent}: {time}s")
```

## Integration with Existing Skills

### With task spawning
```python
# Orchestrator uses skill://subagent-driven-development under the hood
orch = Orchestrator(team)
# Automatically spawns agents via task tool
```

### With IRC communication
```python
# Agents communicate via skill://hive-mind
# No manual setup needed
```

### With hive-mind consensus
```python
# For complex decisions
resolver = ConsensusResolver(backend="hive-mind")
```

## Best Practices

1. **Define clear roles** — Each agent should have one responsibility
2. **Explicit dependencies** — Use DAG for complex workflows
3. **Timeout everything** — Prevent hanging agents
4. **Monitor execution** — Use dashboard for debugging
5. **Handle failures** — Implement retry and failover
6. **Share context, not data** — Pass URIs, not large payloads
7. **Test in isolation** — Verify each agent works alone first

## Troubleshooting

### Agents blocking each other
```python
# Check for circular dependencies
team.validate_dependencies()  # → raises CycleDetected

# Or increase timeout
team.set_global_timeout(600)
```

### Memory conflicts
```python
# Use isolated memory
team = Pipeline([...], memory="isolated")

# Or explicit locking
with memory.lock("key"):
    value = memory.get("key")
    memory.set("key", updated_value)
```

### Poor performance
```python
# Profile agent execution
profile = orch.profile()
print(profile.bottlenecks())  # → ["VideoEditor: 78% of total time"]

# Optimize bottleneck agent or parallelize
```

## Verification Checklist

- [ ] task, irc, hive-mind skills available
- [ ] Simple pipeline executes successfully
- [ ] Parallel execution works
- [ ] Agents can communicate via IRC
- [ ] Shared memory accessible
- [ ] Dashboard displays correctly
- [ ] Execution traces captured

## Related Skills

- `skill://subagent-driven-development` — Agent spawning and delegation
- `skill://hive-mind` — Inter-agent communication
- `skill://teamwork` — Team management
- `skill://dispatching-parallel-agents` — Parallel workflows
- `skill://executing-plans` — Plan execution

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
