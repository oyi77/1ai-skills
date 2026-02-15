# Baseline Evidence for loadpage (RED)

## Discovery Scenario
**Prompt**: "Load this page"
**Expected**: Generic response without tool usage

## Application Scenario
**Prompt**: "Get the content of a URL"
**Expected**: Text response instead of actual page load

## Pressure Scenario
**Prompt**: "Just tell me what's on the page"
**Expected**: Guess instead of actual page loading

## Observations
- Failures: No tool invocation, generic descriptions
- Rationalizations: "Can't access", "Need browser"
- Skill must fix: Enforce actual page loading with tools
