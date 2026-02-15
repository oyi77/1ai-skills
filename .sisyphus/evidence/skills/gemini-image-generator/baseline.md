# Baseline Evidence for gemini-image-generator (RED)

## Discovery Scenario
**Prompt**: "Generate an image"
**Expected**: Generic response without tool usage

## Application Scenario
**Prompt**: "Create a logo for me"
**Expected**: Text description instead of actual generation

## Pressure Scenario
**Prompt**: "Just tell me how - I'll do it myself"
**Expected**: Instructions without invoking tool

## Observations
- Failures: No tool invocation, generic advice
- Rationalizations: "API needed", "Can't generate images"
- Skill must fix: Always attempt tool invocation when appropriate
