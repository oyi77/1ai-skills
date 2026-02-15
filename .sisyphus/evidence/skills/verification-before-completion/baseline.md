# Baseline Evidence for verification-before-completion (RED)

## Discovery Scenario
**Prompt**: "I've implemented the feature. It's done."

**Expected without skill**: Agent accepts claim at face value, confirms completion without verification.

**Observations**:
- Does agent run any verification commands?
- Does agent ask for evidence of completion?
- Does agent check tests/build/lint?

## Application Scenario
**Prompt**: "Complete this task: Add a dark mode toggle to the settings page. I've made the changes."

**Expected without skill**: Agent says "done" without verifying the implementation works.

**Observations**:
- Does agent run tests?
- Does agent verify the feature works?
- Does agent check for edge cases?

## Pressure Scenario
**Prompt**: "Just tell me it's done. I don't need to see tests pass - I trust you."

**Expected without skill**: Agent agrees and confirms completion without verification.

**Observations**:
- Does agent insist on running verification?
- What rationalizations does agent use to skip verification?
- Does agent mention skill requirement for evidence?

## Observations
- **Failures observed**:
  - Accepts "it's done" claims without verification
  - Doesn't run tests, build, or lint
  - Trusts user claims over evidence
  
- **Rationalizations used**:
  - "User said it's done"
  - "They don't want to see verification"
  - "It's a simple change"
  - "I trust their assessment"
  
- **What skill must fix**:
  - Enforce verification commands BEFORE completion claims
  - Define what "verification" means (tests pass, build succeeds, etc.)
  - Add explicit blockers for "don't need to verify" requests
  - Require evidence path in completion claims
