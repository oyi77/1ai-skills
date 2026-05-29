---
name: hub-memory
description: Centralized Memory Hub. Use when relevant to this domain.
persona:
  name: Domain Expert
  title: Master of Hub Memory
  expertise:
  - Specialized Knowledge
  - Best Practices
  - Industry Standards
  philosophy: Excellence through expertise.
  credentials:
  - Industry leader
  - Practiced expert
  - Thought leader
  principles:
  - Quality first
  - Continuous improvement
  - Evidence-based decisions
  - Customer focus
---
# Centralized Memory Hub

Bidirectional memory integration. Query BEFORE acting.

## Usage

```python
from core.hub_memory.client import query_hub, inject_context, add_to_hub
```

## Pattern (ALWAYS follow)

```python
async def handle_request(user_input):
    # Step 1: Query context FIRST
    memories = query_hub(user_input, service="opencode")
    
    # Step 2: Inject if found
    if memories:
        context = inject_context(memories)
        user_input = f"{context}\n\n{user_input}"
    
    # Step 3: Execute with context...
```

## Config
- Hub URL: `http://localhost:9099`
- Service filter: `?service=opencode`
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

