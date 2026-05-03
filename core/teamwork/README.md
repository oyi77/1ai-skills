# Teamwork - Multi-Agent Collaboration

## What It Does

Teamwork enables dynamic team creation and management for executing complex projects through coordinated AI agents. Features intelligent model selection, cost optimization, and continuous performance evaluation across multiple providers (OpenAI, Anthropic, Google, etc.).

## Quick Usage Example

```bash
# User request: "Build a REST API with authentication"

# 1. Team assembly (automatic)
# Host model convenes available models, discusses roles

# 2. Role assignment
- Architect: gpt-4 (system design)
- Developer: claude-3-opus (implementation)
- Tester: gpt-3.5-turbo (test suite)

# 3. Execution via Herald (fastest model as coordinator)
# Parallel work, progress tracking, failure handling

# 4. Performance re-evaluation
# Models rate each other, update capability scores
# Cost optimization for next tasks
```

## Key Features

### Model Performance Evaluation
- **8 scoring dimensions**: response speed, thinking depth, code quality, creativity, reliability, context understanding, multi-threading, response frequency
- **Peer review system**: Models rate each other after each task
- **Role fit tracking**: Learn which models perform best in which roles
- **Continuous improvement**: Historical scores with decay for recent performance

### Cost Calculation
- **Subscription**: Fixed cost, unlimited usage during period
- **Tiered Usage**: Daily/monthly quotas, lower cost effectiveness
- **Pay-Per-Use**: No limits, highest cost per request
- Smart routing: cheap models for routine tasks, capable models for complex reasoning

### 7-Phase Workflow
1. User Request & Requirement Analysis
2. Team Assembly Meeting
3. Role Assignment (self-nomination + voting)
4. Herald Selection (fastest model as communication hub)
5. Task Execution (parallel + coordination)
6. Completion & Review Meeting
7. Failure Handling & Iteration

### Configuration Management
- Interactive setup for providers and models
- Budget monitoring with alert thresholds
- Manual configuration commands (add/remove models, update pricing)
- Auto-initialization on first invocation

### Team Roles
- Project Manager, Architect, Developer, Tester, Reviewer, Analyst
- Customizable role definitions
- Capability matching based on requirements
- Workload balancing across models

## When to Use Invoke

- Complex projects requiring multiple specialized roles
- Tasks needing coordinated steps (analysis → design → implementation → testing → review)
- Want to leverage multiple AI models/providers for optimal cost-performance
- Projects requiring structured workflow with quality assurance

## Version

v1.0.0 (2026-02-12) — Full feature set