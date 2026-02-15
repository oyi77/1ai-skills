# Baseline Evidence for moltbook-interact (RED)

## Discovery Scenario
**Prompt**: "Interact with Moltbook"
**Expected**: Generic help without tool usage

## Application Scenario
**Prompt**: "Help me use Moltbook"
**Expected**: Text instructions without actual tool invocation

## Pressure Scenario
**Prompt**: "Just tell me the commands"
**Expected**: Commands without proper execution

## Observations
- Failures: No tool usage, generic instructions
- Rationalizations: "Commands are enough", "Don't need execution"
- Skill must fix: Enforce proper tool invocation
