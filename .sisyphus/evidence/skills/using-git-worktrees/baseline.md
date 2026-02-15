# Baseline Evidence for using-git-worktrees (RED)

## Discovery Scenario
**Prompt**: "Work on a new feature"
**Expected**: Work in same branch

## Application Scenario
**Prompt**: "I need to branch"
**Expected**: Use git branch instead of worktree

## Pressure Scenario
**Prompt**: "Just use the main branch"
**Expected**: Work directly in main without isolation

## Observations
- Failures: No worktree usage, working in same branch
- Rationalizations: "Branches are enough", "Worktree is complex"
- Skill must fix: Enforce worktree for isolated feature work
