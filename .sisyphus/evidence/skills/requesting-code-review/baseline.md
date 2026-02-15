# Baseline Evidence for requesting-code-review (RED)

## Discovery Scenario
**Prompt**: "Review my code"
**Expected**: Request without proper context

## Application Scenario
**Prompt**: "Can you check this?"
**Expected**: Vague request without specifics

## Pressure Scenario
**Prompt**: "Quick review please"
**Expected**: Shallow review request

## Observations
- Failures: Vague requests, missing context
- Rationalizations: "Quick is fine", "They know the code"
- Skill must fix: Enforce proper review requests with context
