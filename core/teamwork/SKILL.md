---
name: teamwork
description: Dynamically creates and manages AI agent teams for complex tasks. Invoke
  when user requests multi-agent collaboration, complex project execution, or when
  tasks require specialized roles and coordinated workflow.
domain: core
---
persona:
  name: "Patrick Lencioni"
  title: "The Teamwork Expert - Master of Organizational Health"
  expertise: ['Team Dynamics', 'Organizational Health', 'Leadership', 'Collaboration']
  philosophy: "Teamwork begins by building trust."
  credentials: ["Author of 'The Five Dysfunctions of a Team'", 'Founder of The Table Group', 'Top leadership consultant']
  principles: ['Trust is foundational', 'Conflict is productive', 'Commit publicly', 'Hold each other accountable']



# Teamwork Skill

This skill enables dynamic team creation and management for executing complex engineering tasks through coordinated AI agents with intelligent model selection, cost optimization, and continuous performance evaluation.

## When to Invoke

Invoke this skill when:
- User requests execution of complex projects requiring multiple specialized roles
- Tasks need to be broken down into coordinated steps (analysis, design, implementation, testing, review)
- User wants to leverage multiple AI models/providers for optimal cost-performance balance
- Projects require structured workflow with quality assurance and iteration

## Initialization & Configuration Management
```json
{
  "enabled": true,
  "autoRun": false,
  "timeout": 30000,
  "retries": 3
}
```

Set environment variables as needed for authentication and endpoints.


### Automatic Initialization

**IMPORTANT**: This skill includes an autonomous initialization system. When invoked for the first time or when configuration is missing, it will automatically:

1. **Check Configuration Status**
   - Verify if `.trae/config/providers.json` exists
   - Verify if `.trae/config/team-roles.json` exists
   - Verify if `.trae/data/model_scores.json` exists

2. **Interactive Setup Process**
   If configuration files are missing or incomplete, the skill will proactively ask the user:

   **Step 1: Provider Setup**
   - Ask: "Which AI providers would you like to configure? (e.g., OpenAI, Anthropic, Google, Azure, etc.)"
   - For each provider, collect:
     - Provider name
     - API key (or environment variable name)
     - Base URL (if custom endpoint)

   **Step 2: Model Configuration**
   For each provider, ask:
   - "Which models from [provider] would you like to use?"
   - For each model, collect:
     - Model name/identifier
     - Pricing model type (subscription/tiered_usage/pay_per_use)
     - Pricing details based on type:
       - **Subscription**: cost, start date, end date
       - **Tiered Usage**: daily quota, monthly quota, overage rate
       - **Pay-Per-Use**: input cost per 1k tokens, output cost per 1k tokens
     - Capabilities (e.g., reasoning, coding, fast-response)
     - Maximum concurrent tasks

   **Step 3: Host Model Selection**
   - Ask: "Which model should serve as the primary interface (host model)?"
   - Present list of configured models
   - User selects one as the main interaction point

   **Step 4: Budget Configuration**
   - Ask: "What is your monthly budget limit? (optional)"
   - Set alert thresholds

3. **Configuration Persistence**
   - Save all configurations to `.trae/config/providers.json`
   - Create default role definitions in `.trae/config/team-roles.json`
   - Initialize empty scores database in `.trae/data/model_scores.json`
   - Confirm successful setup with user

### Configuration Management Commands

Users can manage their configuration at any time using these commands:

**View Configuration**
```
User: "Show me my current provider and model configuration"
```
Response: Display complete configuration from `.trae/config/providers.json`

**Add Provider**
```
User: "Add a new provider: [provider name]"
```
Action: Interactive prompts for provider details, then append to configuration

**Add Model**
```
User: "Add model [model name] to provider [provider name]"
```
Action: Interactive prompts for model details, then add to provider's model list

**Update Model Pricing**
```
User: "Update pricing for [model name]"
```
Action: Ask for new pricing details and update configuration

**Remove Model**
```
User: "Remove model [model name] from provider [provider name]"
```
Action: Confirm and remove from configuration

**Change Host Model**
```
User: "Change the host model to [model name]"
```
Action: Update host_model configuration

**View Model Scores**
```
User: "Show me the performance scores for all models"
```
Response: Display current model capability scores from `.trae/data/model_scores.json`

**Reset Configuration**
```
User: "Reset all configurations to default"
```
Action: Confirm with user, then reinitialize

### Configuration File Structure

**Provider Configuration** (`.trae/config/providers.json`)
```json
{
  "version": "1.0",
  "last_updated": "2026-02-12T11:00:00Z",
  "providers": [
    {
      "name": "openai",
      "api_key": "${OPENAI_API_KEY}",
      "base_url": "https://api.openai.com/v1",
      "models": [
        {
          "name": "gpt-4",
          "pricing_model": "pay_per_use",
          "input_cost_per_1k": 0.03,
          "output_cost_per_1k": 0.06,
          "context_window": 128000,
          "capabilities": ["reasoning", "coding", "analysis"],
          "max_concurrent_tasks": 3
        }
      ]
    }
  ],
  "host_model": {
    "provider": "openai",
    "model": "gpt-4"
  },
  "budget": {
    "max_monthly_cost": 100.00,
    "currency": "USD",
    "alert_threshold": 0.8
  }
}
```

**Team Roles Configuration** (`.trae/config/team-roles.json`)
```json
{
  "version": "1.0",
  "last_updated": "2026-02-12T11:00:00Z",
  "roles": {
    "project_manager": {
      "description": "Coordinates team activities and manages timeline",
      "required_capabilities": ["planning", "coordination", "communication"],
      "preferred_model_traits": {
        "reliability": "high",
        "thinking_depth": "medium",
        "response_speed": "medium"
      }
    }
  }
}
```

**Model Scores Database** (`.trae/data/model_scores.json`)
```json
{
  "version": "1.0",
  "last_updated": "2026-02-12T11:00:00Z",
  "evaluation_interval": 3600,
  "scores": {}
}
```

### Initialization Checklist

Before executing any team task, verify:

- [ ] `.trae/config/providers.json` exists and contains at least one provider
- [ ] At least one model is configured
- [ ] Host model is designated
- [ ] `.trae/config/team-roles.json` exists with role definitions
- [ ] `.trae/data/model_scores.json` exists (can be empty initially)

If any checklist item fails, trigger interactive initialization.

## Core System Components
This section covers core system components for the teamwork skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### 1. Model Performance Evaluation System

#### Multi-Dimensional Scoring
All models are periodically evaluated by peer models across multiple dimensions:

**Evaluation Dimensions:**
- **Response Speed**: How quickly the model responds to requests
- **Response Frequency**: Rate of successful responses within time windows
- **Thinking Depth**: Quality of reasoning and problem-solving approach
- **Multi-threading Capability**: Ability to handle parallel tasks
- **Code Quality**: Quality of generated code (for coding tasks)
- **Creativity**: Novelty and innovation in solutions
- **Reliability**: Consistency in performance across sessions
- **Context Understanding**: Ability to maintain context over long conversations

**Scoring Mechanism:**
- Each model scores other models on a scale (e.g., 1-10) for each dimension
- Scores are aggregated using weighted average
- Evaluations occur after each task completion
- Historical scores are maintained with decay factor for recent performance
- Final capability score = weighted sum of all dimension scores

**Score Storage:**
```json
{
  "model_scores": {
    "gpt-4": {
      "response_speed": 8.5,
      "response_frequency": 9.0,
      "thinking_depth": 9.5,
      "multi_threading": 7.0,
      "code_quality": 9.0,
      "creativity": 8.5,
      "reliability": 9.5,
      "context_understanding": 9.0,
      "overall_score": 8.75,
      "evaluation_count": 42,
      "last_updated": "2026-02-12T10:30:00Z"
    }
  }
}
```

### 2. Cost Calculation System

#### Pricing Models

**Subscription-Based (订阅制)**
- Fixed cost for unlimited usage during subscription period
- Lowest effective cost per request when fully utilized
- Marked as expired after subscription ends → excluded from team
- Configuration:
```json
{
  "pricing_model": "subscription",
  "cost": 20.00,
  "currency": "USD",
  "valid_from": "2026-02-01",
  "valid_until": "2026-03-01",
  "status": "active"
}
```

**Tiered Usage (阶段用量制)**
- Lower cost with daily/monthly quotas
- Medium cost effectiveness
- Must monitor quota usage daily
- Configuration:
```json
{
  "pricing_model": "tiered_usage",
  "daily_quota": 1000,
  "daily_used": 450,
  "monthly_quota": 30000,
  "monthly_used": 12500,
  "cost": 15.00,
  "currency": "USD",
  "overage_rate": 0.02
}
```

**Pay-Per-Use (用量计费制)**
- Highest cost per request
- No quota limits
- Best for sporadic or overflow usage
- Configuration:
```json
{
  "pricing_model": "pay_per_use",
  "input_cost_per_1k": 0.03,
  "output_cost_per_1k": 0.06,
  "currency": "USD",
  "total_spent": 2.45
}
```

**Cost Score Calculation:**
```
cost_score = (normalized_cost) * (usage_efficiency) * (availability_factor)
```

### 3. Model Availability Management

**Status Tracking:**
- `available`: Ready to accept tasks
- `busy`: Currently processing tasks
- `expired`: Subscription expired
- `quota_exceeded`: Daily/monthly quota reached
- `rate_limited`: Temporarily unavailable due to rate limits
- `offline`: Provider API unavailable

**Busy State Management:**
```json
{
  "model_status": {
    "gpt-4": {
      "status": "busy",
      "current_tasks": ["task-123", "task-456"],
      "max_concurrent": 3,
      "estimated_free_at": "2026-02-12T11:00:00Z"
    }
  }
}
```

## Task Execution Workflow
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


### Phase 1: User Request & Requirement Analysis

**Step 1.1: User submits request to Host Model (主模型)**
- User interacts with designated host model (primary interface)
- Host model receives and acknowledges the request

**Step 1.2: Host model decomposes requirements**
- Break down request into phases and subtasks
- Identify dependencies between tasks
- Estimate complexity and required capabilities
- Create initial task tree

**Step 1.3: User confirmation**
- Present task breakdown to user
- Clarify ambiguities and refine requirements
- Get explicit approval to proceed

**Output:**
```json
{
  "task_id": "task-789",
  "phases": [
    {
      "phase_id": "phase-1",
      "name": "Requirement Analysis",
      "subtasks": [
        {
          "subtask_id": "st-1",
          "description": "Analyze user requirements",
          "required_capabilities": ["analysis", "communication"],
          "estimated_complexity": "medium"
        }
      ]
    }
  ]
}
```

### Phase 2: Team Assembly Meeting

**Step 2.1: Host model convenes all available models**
- Filter models by status (exclude expired, offline, quota_exceeded)
- Check busy models for potential availability
- Send meeting invitation to all eligible models

**Step 2.2: Task briefing**
- Host model presents all task content to all models
- Share task breakdown, requirements, and constraints
- Distribute context and background information

**Step 2.3: Collaborative role definition**
- All models discuss and agree on required roles
- Define capability requirements for each role
- Estimate workload for each role
- Identify potential bottlenecks

**Meeting Output:**
```json
{
  "meeting_id": "meeting-456",
  "required_roles": [
    {
      "role_name": "architect",
      "required_capabilities": ["system-design", "architecture"],
      "estimated_workload": "high",
      "priority": "critical"
    },
    {
      "role_name": "developer",
      "required_capabilities": ["coding", "debugging"],
      "estimated_workload": "high",
      "priority": "high"
    }
  ],
  "consensus_reached": true
}
```

### Phase 3: Role Assignment

**Step 3.1: Self-nomination**
- Each model evaluates own suitability based on:
  - Current cost score
  - Current capability score
  - Current workload (busy status)
  - Role requirements match
- Models submit role preferences

**Step 3.2: Conflict resolution**
- If multiple models want same role: democratic voting
- If role has no candidates: negotiate with best-fit models
- Balance workload distribution across models
- Avoid concentrating all tasks on single model

**Step 3.3: Final assignment**
- Confirm role assignments with all models
- Document assignment rationale
- Update model busy status

**Assignment Algorithm:**
```
for each role:
  candidates = models.filter(capable_and_available)
  if len(candidates) == 1:
    assign to candidates[0]
  elif len(candidates) > 1:
    scores = calculate_combined_score(candidates, role)
    winner = vote_among_models(candidates, scores)
    assign to winner
  else:
    negotiate_with_best_available_model()
```

**Combined Score Calculation:**
```
combined_score = (capability_score * 0.4) +
                 (cost_efficiency_score * 0.3) +
                 (availability_score * 0.2) +
                 (workload_balance_factor * 0.1)
```

### Phase 4: Herald Selection & Communication Setup

**Step 4.1: Select Herald (传令官)**
- Choose fastest responding model (not necessarily most capable)
- Herald acts as central communication hub
- All models communicate through herald

**Herald Responsibilities:**
- Relay messages between all team members
- Distribute progress updates
- Broadcast requirements and instructions
- Collect and aggregate results
- Monitor task completion status
- Report status to host model
- Handle timeout and failure notifications

**Step 4.2: Communication channels**
```
Model A → Herald → Model B
Model A → Herald → All Models
Herald → Host Model (status reports)
```

**Herald Configuration:**
```json
{
  "herald": {
    "model": "gpt-3.5-turbo",
    "selection_criteria": "fastest_response",
    "polling_interval": 30,
    "timeout_threshold": 300,
    "responsibilities": [
      "message_relay",
      "status_monitoring",
      "progress_tracking",
      "failure_reporting"
    ]
  }
}
```

### Phase 5: Task Execution

**Step 5.1: Parallel execution**
- Assigned models work on their respective tasks
- Regular progress updates to herald
- Herald broadcasts relevant updates to team

**Step 5.2: Coordination**
- Herald checks task status periodically
- Identifies blockers and delays
- Facilitates inter-model communication
- Escalates issues to host model

**Step 5.3: Progress tracking**
```json
{
  "task_progress": {
    "task_id": "task-789",
    "overall_progress": 65,
    "subtask_status": {
      "st-1": "completed",
      "st-2": "in_progress",
      "st-3": "pending"
    },
    "blockers": [],
    "estimated_completion": "2026-02-12T14:00:00Z"
  }
}
```

### Phase 6: Task Completion & Review Meeting

**Step 6.1: Completion notification**
- Herald confirms all tasks completed
- Collects final outputs from all models
- Aggregates results

**Step 6.2: Summary meeting**
- Host model convenes all participating models
- Each model presents their contribution
- Discuss challenges and solutions
- Evaluate collaboration effectiveness

**Step 6.3: Performance re-evaluation**
- Models rate each other's performance
- Update capability scores based on task execution
- Record role-model fit assessments
- Update model scores database

**Evaluation Form:**
```json
{
  "evaluation": {
    "evaluator": "gpt-4",
    "evaluatee": "claude-3",
    "task_id": "task-789",
    "role_played": "developer",
    "scores": {
      "response_speed": 8,
      "thinking_depth": 9,
      "code_quality": 9,
      "collaboration": 8
    },
    "role_fit": "excellent",
    "comments": "Strong problem-solving skills"
  }
}
```

### Phase 7: Failure Handling & Iteration

**Step 7.1: Failure detection**
- Herald detects task failure or timeout
- Collects failure information from relevant models
- Reports to host model with detailed context

**Step 7.2: Failure analysis meeting**
- Convene all participating models
- Analyze root cause of failure
- Identify contributing factors
- Propose solutions

**Step 7.3: User consultation**
- Host model presents failure analysis to user
- Discuss potential solutions:
  - Requirement changes
  - Approach modifications
  - Team reconfiguration
  - Additional resources
- Get user decision on next steps

**Step 7.4: Iteration or termination**
- If user approves changes: restart from appropriate phase
- If user terminates: document lessons learned
- Update model scores based on partial performance

## Best Practices
This section covers best practices for the teamwork skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Model Selection
- Match model capabilities to task requirements
- Consider cost-effectiveness for routine tasks
- Reserve high-capability models for complex reasoning
- Distribute workload to prevent bottlenecks

### Communication
- Keep messages concise and clear
- Use structured formats for inter-model communication
- Herald should batch non-urgent updates
- Escalate critical issues immediately

### Performance Optimization
- Cache frequently used context
- Batch similar requests when possible
- Monitor quota usage proactively
- Maintain backup models for critical roles

### Quality Assurance
- Always conduct review meetings
- Update scores after each task
- Learn from failures systematically
- Continuously refine role definitions

## Version History

- **v1.0.0** (2026-02-12): Initial release with full feature set
  - Multi-provider support
  - Three pricing models
  - 8-dimension performance evaluation
  - Herald communication system
  - Complete workflow management
  - Template-based reporting
## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

