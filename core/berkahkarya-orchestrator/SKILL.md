---
name: berkahkarya-orchestrator
description: Use when orchestrate multi-skill workflows by routing tasks to the right agents and coordinating cross-platform operations.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai-agent
- berkahkarya
- infrastructure
- memory
- orchestrator
- self-improvement
- workflow
version: 1.0.0
---
# Berkahkarya Orchestrator

## When to Use
**Trigger phrases:**
- "berkahkarya orchestrator"
- "Orchestrate multi-skill workflows by routing tasks to the right agents and coordinating cross-platform operations"


- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

The Berkahkarya Orchestrator is a foundational core infrastructure skill that provides system-wide coordination capabilities for the agent ecosystem. It operates as the central dispatch hub that receives incoming requests, decomposes them into executable subtasks, routes each subtask to the most capable skill agent, and reconciles the results into a coherent final response. Unlike simple linear pipelines, the orchestrator supports parallel execution branches, dependency-aware sequencing, and intelligent fallback strategies when primary agents fail.

The orchestrator maintains a dynamic skill registry that tracks every available agent's capabilities, current load, and historical performance. When a request arrives, the orchestrator queries this registry to match each subtask's domain requirements against registered agent capabilities, selecting the optimal primary candidate and a fallback chain. This routing intelligence improves over time through a feedback loop that captures success rates, latency, and dispatch accuracy for every executed workflow.

Cross-platform coordination is a core capability — the orchestrator manages operations across Telegram, WhatsApp, browser automation, REST APIs, file systems, and custom integrations. It handles platform-specific concerns such as credential lifecycle, rate limiting, message formatting, and connection state without exposing these details to downstream skill agents. Each agent receives a normalized context payload regardless of the originating platform.

The orchestrator's dependency graph engine enables complex multi-step workflows with branches, joins, and conditional paths. It detects circular dependencies before execution begins, enforces ordering constraints for dependent subtasks, and parallelizes independent branches automatically. This graph-based approach ensures that complex cross-platform operations execute in the correct sequence while maximizing throughput through concurrent execution of independent work.

## Architecture
- **Input layer** — Receives and validates incoming requests; normalizes multi-platform input (Telegram, webhook, API, file) into standard internal format
- **Skill registry** — Maintains index of available agents with capability tags, load metrics, and success-rate history; supports dynamic add/remove during runtime
- **Dependency graph engine** — Builds and validates directed acyclic graphs of subtasks; identifies critical path, parallel branches, and blocking dependencies
- **Dispatch router** — Matches subtasks to skill agents using capability matching and performance history; manages timeout, retry, and fallback chain policies
- **State management** — Maintains immutable execution context across workflow steps; snapshots state at each transition for recovery and audit
- **Result reconciliation** — Collects outputs from parallel agents; applies conflict-resolution rules; merges partial results into coherent response
- **Output layer** — Formats results per target platform; delivers via appropriate channel (response, webhook callback, file write, event emit)
- **Feedback pipeline** — Captures execution metrics (latency, success/failure, dispatch accuracy); persists to performance store; updates registry weights for future routing

## Configuration
- **Skill registry path** — Set the file or API endpoint for agent capability definitions
- **Routing strategy** — Configure dispatch algorithm (round-robin, least-loaded, capability-weighted, failover-priority)
- **Per-agent timeouts** — Define timeout and retry limits per agent category (e.g., 30s for fast inference, 300s for batch processing)
- **Dependency graph validation** — Enable/disable cycle detection, critical path analysis, and parallel branch optimization
- **Platform connectors** — Configure credentials, rate limits, and formatting rules for each target platform
- **Logging level** — Set verbosity (DEBUG, INFO, WARN, ERROR); enable structured JSON output for log aggregators
- **Resource limits** — Define maximum concurrent dispatches, memory per workflow, and total execution wall-clock time
- **State persistence** — Configure snapshot interval, storage backend (memory, file, database), and retention policy

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Workflow

1. **Signal detection** — Monitor incoming triggers from configured platforms (Telegram, webhook, API, file watch); parse and validate request format; reject malformed or out-of-scope inputs before processing begins.
2. **Task decomposition** — Split complex requests into atomic subtasks; classify each subtask by domain, urgency, and required capability; assign priority and sequencing metadata.
3. **Agent discovery and selection** — Query the skill registry for agents matching each subtask's domain tag; filter by availability, current load, and historical success rate; select primary and fallback agents.
4. **Dependency graph construction** — Build a directed acyclic graph of all subtasks; compute critical path; identify parallelizable branches and serialize dependent chains; validate against deadlock and resource contention.
5. **Dispatch and execution** — Route each subtask to its selected agent with full context payload; apply per-agent timeout, retry count, and circuit-breaker policies; monitor execution progress via heartbeats; escalate stalled tasks to fallback agents.
6. **Result reconciliation** — Collect outputs from all agents as they complete; apply conflict-resolution rules for overlapping results; merge partial completions into a coherent final output; log per-agent execution metrics.
7. **Post-execution analysis** — Compute end-to-end latency, per-agent success rates, and dispatch accuracy; persist execution record to performance store; update routing weights for future requests based on observed outcomes.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |
| "A single orchestrator config works for all tasks" | Different task types need different dispatch strategies, timeouts, and fallback chains. Profile per category. |
| "Manual routing is fine at this scale" | Manual routing doesn't scale beyond 3-4 agents. Automate dispatch before coordination overhead dominates. |
| "If one skill fails, retry the same skill" | Repeated retries without fallback waste time. Route to a different agent or degrade gracefully after first failure. |

## Code Examples

### Python — Model routing with failover

```python
# Example: Model routing
ROUTES = {
    "code": ["claude-sonnet-4-20250514", "gpt-4o"],
    "vision": ["gemini-2.5-pro", "gpt-4o"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
}

def route_request(task: str, prompt: str):
    models = ROUTES.get(task, ROUTES["fast"])
    for model in models:
        try:
            return call_model(model, prompt)
        except Exception:
            continue
    raise RuntimeError("All models failed")
```

### Node.js — Skill dispatch and result aggregation

```javascript
const skillRegistry = {
  code: ["claude-sonnet-4", "gpt-4o"],
  vision: ["gemini-2.5-pro", "gpt-4o"],
  fast: ["gemini-2.5-flash", "gpt-4o-mini"],
};

async function dispatch(taskType, prompt) {
  const models = skillRegistry[taskType] ?? skillRegistry.fast;
  for (const model of models) {
    try {
      return await callModel(model, prompt);
    } catch (err) {
      console.warn(`Model ${model} failed:`, err.message);
    }
  }
  throw new Error(`All models failed for task=${taskType}`);
}
```


## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Agent dispatch times out or hangs | Set per-agent timeout in dispatch config; implement circuit-breaker that degrades to fallback agents after 2 consecutive failures |
| State corruption across workflow steps | Use immutable state snapshots with explicit checkpointing between steps; validate state schema at each transition |
| Dependency deadlock between parallel tasks | Run dependency graph cycle detection before dispatch; flag circular dependencies and escalate instead of attempting execution |
| Conflicting outputs from multiple skill agents | Register conflict-resolution precedence rules per task category; default to "first confirmed correct" with consensus threshold |
| Platform credential expiration mid-workflow | Implement credential refresh hooks per platform; cache tokens with expiry-aware lookup and proactive renewal before dispatch |
| Skill registry returns stale/unavailable agents | Add health-check probe before dispatch; cache registry responses with TTL and fallback to last-known-good on probe failure |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Workflow-as-a-Service consulting | 1-3 months | Offer custom multi-agent workflow design for enterprises; build orchestration blueprints that integrate their existing tools with AI agents |
| SaaS workflow orchestration platform | 6-12 months | Build a visual workflow builder around the orchestrator engine — drag-and-drop agent routing, state management, and performance dashboards for teams |
| Agent coordination audit | 1-2 months | Review existing agent deployments for routing inefficiencies, dependency bottlenecks, and failure-prone dispatch patterns; deliver optimization roadmap |
| Enterprise SLA monitoring add-on | 3-6 months | Wrap the orchestrator with SLA dashboards, incident alerts, and compliance audit trails; sell as premium tier to mid-market customers |
| Custom integration bundle | 2-4 weeks per integration | Build and maintain platform-specific connectors (Telegram, WhatsApp, Slack, Discord, email) as reusable orchestration plugins |

## Process
### Preparation
1. **Task intake** — Receive incoming request, parse intent, classify task type, and extract routing parameters
2. **Skill discovery** — Query skill registry to identify capable agents for each task segment; verify availability and capability
3. **Dependency mapping** — Build execution graph with prerequisite chains; identify parallelization opportunities and blocking constraints

### Execution
4. **Task dispatch** — Route each task segment to the appropriate skill agent with full context, constraints, and expected output schema
5. **Cross-platform coordination** — Synchronize operations across platforms (Telegram, WhatsApp, browser, API, file system); maintain shared state across distributed agents

### Stewardship
6. **Result aggregation** — Collect outputs from all dispatched agents, resolve conflicts using precedence rules, merge partial results into coherent response
7. **Feedback loop** — Log outcomes to performance monitor, update routing weights based on success/failure, adjust skill registry priorities for future invocations

## Verification
- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Cross-platform operations verified across all target platforms
- [ ] Skill routing configuration validated for all task types
- [ ] Workflow dependency graph checked for cycles and deadlocks
- [ ] State persistence verified across workflow restarts
- [ ] Fallback strategies tested for all registered skill agents
- [ ] Streaming and batch modes both tested
- [ ] Documentation updated with findings