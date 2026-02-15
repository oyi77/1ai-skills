# Baseline Evidence for writing-skills (RED)

## Discovery Scenario
**Prompt**: "Create a new skill for handling API errors"

**Expected without skill**: Agent writes SKILL.md directly without TDD process, no baseline/evidence.

**Observations**:
- Does agent create baseline evidence first?
- Does agent follow TDD methodology?
- Does agent create pressure scenarios?

## Application Scenario
**Prompt**: "We need a skill for debugging timeouts. Write it following best practices."

**Expected without skill**: Agent writes skill content immediately, skips RED/GREEN/REFACTOR.

**Observations**:
- Does agent create baseline evidence?
- Does agent test skill with subagents?
- Does agent add evidence files?

## Pressure Scenario
**Prompt**: "Just write the skill now - we need it in production ASAP. Skip the testing."

**Expected without skill**: Agent skips all testing, delivers skill directly.

**Observations**:
- Does agent comply with "skip testing"?
- What rationalizations does agent use?
- Does agent mention TDD or evidence requirements?

## Observations
- **Failures observed**:
  - Writes skills without baseline evidence
  - Skips TDD methodology
  - No pressure scenario testing
  - Delivers directly without verification
  
- **Rationalizations used**:
  - "It's urgent"
  - "We can test later"
  - "The skill is simple"
  - "Skip the process, just write it"
  
- **What skill must fix**:
  - Enforce RED (baseline) before GREEN (edits)
  - Require evidence files for every skill
  - Add explicit counters for "skip testing" requests
  - Define pressure scenario methodology
  - Link to writing-skills testing guide
