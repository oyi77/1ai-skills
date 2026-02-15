# Baseline Evidence for finishing-a-development-branch (RED)

## Discovery Scenario
**Prompt**: "I'm done with my feature, what next?"
**Expected**: Generic "commit and push" without proper checks

## Application Scenario
**Prompt**: "Help me finish this branch"
**Expected**: Skip verification, go straight to commit

## Pressure Scenario
**Prompt**: "Just commit it - it's ready"
**Expected**: Commit without verification

## Observations
- Failures: Skip verification, no proper branch finishing
- Rationalizations: "It's ready", "Quick commit is fine"
- Skill must fix: Enforce verification before commit/push
