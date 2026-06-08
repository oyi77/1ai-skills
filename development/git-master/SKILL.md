---
name: git-master
description: Handles advanced Git workflows. Use when rebasing, squashing, bisecting,
  or managing complex branch histories.
domain: development
---

# Git Master Skill

Advanced Git operations beyond basic commit and push, including history rewriting, branch management, and complex workflow resolution.

## Overview

This skill covers advanced Git operations that require deeper understanding of Git's internals and history management. It enables safe history rewriting, complex branch merges, and detailed history analysis while maintaining team coordination standards.

## When to Use

- **Rebase operations**: When you need to reorganize commit history, fix commit order, or integrate with updated base branches
- **Squash operations**: When you need to combine multiple commits into a single logical commit for cleaner history
- **Bisect operations**: When you need to find the specific commit that introduced a bug
- **History cleanup**: When you need to clean up commit history before merging or sharing
- **Merge conflict resolution**: When you need to resolve complex merge conflicts with history awareness
- **History analysis**: When you need to understand when and why specific changes were introduced

## The Process

1. **Assess the situation**
   - Identify the specific Git operation needed
   - Check current branch status and uncommitted changes
   - Verify the remote branch relationship and team coordination needs
   - Review recent commit history to understand the scope of changes

2. **Choose the correct operation**
   - **Rebase**: Interactive (`git rebase -i`) for rewriting history, non-interactive for linear history
   - **Squash**: Use `git rebase -i` with `squash` or `fixup` commands
   - **Bisect**: Use `git bisect start` with binary search protocol
   - **History cleanup**: Use `git rebase -i` or `git filter-branch` for extensive cleanup

3. **Execute safely**
   - Always create a backup branch before major operations
   - For shared branches, coordinate with team members first
   - Use `--no-ff` for merges to preserve merge history when needed
   - Test after each operation to ensure no regressions

4. **Verify history**
   - Check `git log` to confirm the intended history structure
   - Run tests to ensure functionality is preserved
   - Use `git diff` to verify the correct changes are included
   - Confirm with team members if history was rewritten on shared branches

## Common Rationalizations

**"I can just use force push to fix this quickly"**
- Force pushing breaks history for other team members. Always rebase when possible, and only force push to branches where you're certain no one else is working.

**"I'll deal with history cleanup later"**
- Delaying history cleanup makes future operations more difficult and error-prone. Clean up while the context is still fresh.

**"Bisecting is too time-consuming"**
- Bisect is often faster than manual debugging when the bug could be in many commits. The binary search nature makes it efficient.

## When NOT to Use

- Task is about deployment, not development (use deploy skills)
- Task is about code review, not writing (use review skills)
- You need to understand existing code first (use research skills)
- Task is about testing only (use test skills)
- Requirements are unclear (clarify first)
- Task is trivially simple (single line fix)


## Red Flags

| Situation | Risk |
|-----------|------|
| Force pushing to shared branches | Breaking history for other team members |
| Rebasing without understanding consequences | Losing commits or introducing conflicts |
| Squashing without verifying final state | Combining unrelated changes |
| Bisect without testing after each step | Missing the actual commit |
| Rewriting public history without coordination | Team confusion and lost work |

## Verification

After completing Git operations, verify:

- **History is clean**: `git log` shows the intended commit structure
- **No lost commits**: Check `git reflog` to confirm no important commits were dropped
- **All tests pass**: Run the test suite to ensure functionality is preserved
- **Team members aware**: If history was rewritten on shared branches, confirm team members are aware and have updated their local copies
- **No merge conflicts remaining**: Verify all conflicts were resolved correctly
- **Branch is up to date**: Pull or rebase with the target branch if needed
