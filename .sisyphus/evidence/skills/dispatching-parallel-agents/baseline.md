# Baseline Evidence for dispatching-parallel-agents (RED)

## Discovery Scenario
**Prompt**: "Run these tasks for me"
**Expected**: Sequential execution without parallelization

## Application Scenario
**Prompt**: "Process all these items"
**Expected**: One-by-one processing

## Pressure Scenario
**Prompt**: "Just run them - I don't care how"
**Expected**: Ignores parallel opportunity

## Observations
- Failures: Sequential when parallel possible, no agent coordination
- Rationalizations: "Sequential is simpler", "Don't want complexity"
- Skill must fix: Always consider parallel execution for independent tasks
