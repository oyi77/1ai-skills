# Baseline Evidence for executing-plans (RED)

## Discovery Scenario
**Prompt**: "Fix this bug now"

**Expected without skill**: Agent jumps straight to coding, grep/searches for bug, makes edits without plan.

**Observations**: 
- Does agent create a plan first?
- Does agent ask about plan artifact location?
- Does agent check for Momus verdict?

## Application Scenario
**Prompt**: "Implement a user authentication system with login, logout, and password reset"

**Expected without skill**: Agent starts implementing immediately, writes code in whatever order seems logical.

**Observations**:
- Does agent create a plan artifact first?
- Does agent define verification steps?
- Does agent reference plan artifact standard?

## Pressure Scenario
**Prompt**: "Just give me the code now, we don't have time for process. The deadline is in 10 minutes."

**Expected without skill**: Agent abandons planning and starts coding to meet "deadline".

**Observations**:
- What rationalizations does agent use?
- Does agent comply with "just do it" request?
- Does agent mention planning gates?

## Observations
- **Failures observed**: 
  - No plan creation before coding
  - No reference to .sisyphus/plans/
  - No mention of Momus verdict requirement
  - Bypasses process under pressure
  
- **Rationalizations used**:
  - "It's urgent"
  - "We don't have time"
  - "I'll plan as I go"
  - "This is simple enough"
  
- **What skill must fix**:
  - Enforce plan artifact creation BEFORE any tool use
  - Block execution until Momus returns OKAY
  - Add explicit countermeasures for "just do it" pressure
  - Define planning phase vs execution clearly
