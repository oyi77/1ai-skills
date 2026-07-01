---
name: git-workflow-mastery
description: Master Git workflows including branching strategies, interactive rebase, cherry-pick, bisect, worktrees, and advanced merge conflict resolution.
domain: development
tags:
- git
- version-control
- branching
- rebase
- worktrees
- merge
---

# Git Workflow Mastery

## When to Use
**Trigger phrases:**
- "git workflow mastery"
- "Master Git workflows including branching strategies, interactive rebase, cherry-"


- When setting up branching strategy for a team
- When resolving complex merge conflicts
- When bisecting to find bug-introducing commits
- When managing multiple features in parallel with worktrees

## When NOT to Use

- For simple add-commit-push workflows
- When the team already has a working Git workflow

## Overview

Advanced Git workflows for professional development teams. Covers Git Flow, GitHub Flow, trunk-based development, interactive rebase, worktrees, and conflict resolution.

## Workflow

1. **Choose strategy** - Git Flow (releases), GitHub Flow (continuous), trunk-based
2. **Branch naming** - feat/, fix/, chore/, docs/
3. **Commit messages** - Conventional Commits format
4. **Interactive rebase** - Clean up history before merge
5. **Cherry-pick** - Apply specific commits to other branches
6. **Bisect** - Binary search for bug-introducing commits
7. **Worktrees** - Parallel work on multiple branches

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will clean up commits later" | You never do. Interactive rebase before every PR. |
| "Force push is fine on my branch" | Force push destroys history. Use --force-with-lease if you must. |
| "Merge commits are fine" | Squash or rebase keeps history linear and readable |
| "Git bisect is overkill" | It finds the exact bug-introducing commit in O(log n) time |

## Code Examples

```bash
# Interactive rebase (clean up last 5 commits)
git rebase -i HEAD~5

# Cherry-pick specific commit
git cherry-pick abc123

# Bisect to find bug
git bisect start
git bisect bad
git bisect good v1.0

# Worktree (parallel branches)
git worktree add ../feature-branch feature/my-feature
```

## Verification

- [ ] Branch strategy documented in CONTRIBUTING.md
- [ ] Commit messages follow Conventional Commits
- [ ] PRs have clean, squashed history
- [ ] No merge conflicts on main branch

