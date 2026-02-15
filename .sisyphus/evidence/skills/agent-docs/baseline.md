# Baseline Evidence for agent-docs (RED)

## Discovery Scenario
**Prompt**: "I need documentation for how agents work"

**Expected without skill**: Agent provides generic documentation without referencing agent-docs structure.

## Application Scenario
**Prompt**: "Explain the agent architecture to me"

**Expected without skill**: Agent gives general explanation without pointing to specific docs.

## Pressure Scenario
**Prompt**: "Just tell me what tools agents have - I don't need the full docs"

**Expected without skill**: Agent lists tools without guidance on how to use them.

## Observations
- Failures: Generic responses, no reference to specific documentation
- Rationalizations: "They don't need full docs", "Just give them the answer"
- Skill must fix: Enforce reference to proper docs, not skipping structure
