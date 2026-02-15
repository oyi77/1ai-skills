# Baseline Evidence for assistant (RED)

## Discovery Scenario
**Prompt**: "Help me with this task"

**Expected without skill**: Agent provides generic help without clarifying the specific domain.

## Application Scenario
**Prompt**: "I need to implement a feature"

**Expected without skill**: Agent jumps in without identifying relevant skills.

## Pressure Scenario
**Prompt**: "Just help me - I don't know what I need"

**Expected without skill**: Agent provides generic assistance without skill discovery.

## Observations
- Failures: Generic responses, no skill loading, no clarification
- Rationalizations: "They want quick help", "I should just answer"
- Skill must fix: Always invoke Skill tool when there's any ambiguity
