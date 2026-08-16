---
name: git-workflow-mastery
description: Use when master Git workflows including branching strategies, interactive
  rebase, cherry-pick, bisect, worktrees, and advanced merge conflict resolution.
  Use when working with git workflow mastery.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- git
- version-control
- branching
- rebase
- worktrees
- merge
version: 1.0.0
category: development
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
- When cleaning up commit history before a PR
- When recovering from a broken Git state (detached HEAD, lost commits)
- When setting up CI/CD pipeline triggers per branch

## When NOT to Use

- For simple add-commit-push workflows
- When the team already has a working Git workflow
- When you only need to clone and pull — no branching or history manipulation

## Overview

Advanced Git workflows for professional development teams. Covers Git Flow, GitHub Flow, trunk-based development, interactive rebase, worktrees, and conflict resolution. This skill assumes you already know `git add`, `git commit`, `git push`, and `git pull`. It covers the next tier: history manipulation, parallel workspace management, binary-search debugging, and safe collaboration patterns.

Git is a Directed Acyclic Graph (DAG) of commits. Understanding this — that branches are just pointers, that rebase rewrites topology, that the reflog tracks every pointer movement — is the foundation of mastery. Every operation in this skill builds on that mental model.

## Branching Strategies

### Git Flow (release-oriented)

```
main        ───●──────●────────────●──────────
                \    /            /
develop         ●──●──●──●──●──●──●──●
                     \    /  \    /
feature/foo          ●──●    ●──●
                              \
release/v1.1                  ●──●
```

Best for projects with scheduled releases and long-lived feature branches.

```bash
# Initialize Git Flow (default branch names)
git flow init -d

# Start a feature
git flow feature start user-auth
# Work, commit, then finish (merges to develop)
git flow feature finish user-auth

# Start a release
git flow release start v1.1.0
# Bump version, fix last bugs, then finish (merges to main + develop)
git flow release finish v1.1.0

# Hotfix from main
git flow hotfix start 1.1.1
git flow hotfix finish 1.1.1
```

### GitHub Flow (continuous deployment)

```
main  ●──●──●──●──●──●──●──●──●
         \    /      \    /
feat     ●──●        ●──●
```

One permanent branch (`main`). Feature branches branch off, are reviewed via PR, and merge back. Deploy after every merge.

```bash
# Start from up-to-date main
git checkout main
git pull origin main
git checkout -b feat/user-auth

# Work, commit, push for review
git push -u origin feat/user-auth

# After PR merges, delete local branch
git branch -d feat/user-auth
git fetch origin --prune
```

### Trunk-Based Development (fast CI)

```
main  ●──●──●──●──●──●──●──●──●──●
         \/          \/
         └─short-lived─┘
```

Short-lived feature branches (hours, not days). No branch lives longer than one sprint. Every commit to main is deployable.

```bash
# Ultra-short feature branch
git checkout -b fix/login-crash
git commit -m "fix: handle null session in login handler"
git push -u origin fix/login-crash
# PR → merge immediately
```

**Branch naming conventions:**

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feat/` | New feature | `feat/user-auth` |
| `fix/` | Bug fix | `fix/login-crash` |
| `chore/` | Maintenance | `chore/upgrade-deps` |
| `docs/` | Documentation | `docs/api-readme` |
| `refactor/` | Code restructuring | `refactor/auth-module` |
| `test/` | Adding tests | `test/auth-flow` |
| `perf/` | Performance | `perf/query-cache` |
| `release/` | Release prep | `release/v1.1.0` |

### Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

```bash
# Standard
git commit -m "feat(auth): add OAuth2 login flow"

# Breaking change (note the !)
git commit -m "feat(api)!: change response format from XML to JSON"

# With body (multiline)
git commit -m "fix(cache): evict stale entries on write

Previously the cache only evicted on TTL expiry.
Now it evicts the stale key on every write to prevent
serving outdated data during high-throughput writes.

Closes #142"
```

## Interactive Rebase

Interactive rebase rewrites commit history by reordering, squashing, fixing up, dropping, or rewording commits. Use it before opening a PR to present a clean, logical history.

### Basic Operations

```bash
# Rebase the last 3 commits
git rebase -i HEAD~3

# This opens an editor with:
# pick a1b2c3d feat: add login form
# pick e4f5g6h fix: validate email field
# pick i7j8k9l fix: handle empty password
```

**Rebase commands:**

| Command | Short | Effect |
|---------|-------|--------|
| `pick` | `p` | Use commit as-is |
| `reword` | `r` | Edit commit message only |
| `squash` | `s` | Combine with previous commit, keep both messages |
| `fixup` | `f` | Combine with previous commit, discard message |
| `drop` | `d` | Remove commit entirely |
| `edit` | `e` | Stop to amend commit content |

### Squash Worked Commits

```bash
# Before: messy history with 6 fixup commits
# After: one clean feature commit

# Step 1: find the base commit (before your feature branch)
git merge-base HEAD main
# Returns: abc1234

# Step 2: rebase onto main (also integrates latest changes)
git rebase -i main
# In the editor, reorder so your feature commits are together,
# then mark them as 'squash' or 'fixup'

# Step 3: resolve any conflicts during rebase
git add <resolved-file>
git rebase --continue
```

### Split a Commit

```bash
# Start an edit on the commit to split
git rebase -i HEAD~3
# Mark the target commit as 'edit' (e), save, close

# Reset to the commit before it, keeping changes staged
git reset HEAD^

# Now stage files in logical groups
git add src/auth/
git commit -m "feat(auth): add login handler"
git add src/db/
git commit -m "feat(db): add users migration"
git add tests/
git commit -m "test(auth): add login flow tests"

git rebase --continue
```

### Reorder Commits

```bash
# In the rebase editor, move lines up/down.
# Safer to move dependent commits after their dependencies.

# Git will replay commits in the order listed.
# Conflicts may arise if adjacent commits touch the same files.
```

### Rebase onto a Different Branch

```bash
# Rebase feature branch onto latest main
git checkout feat/user-auth
git rebase main

# If feature is based on another feature that was merged
git rebase --onto main base-branch feat/user-auth
# Takes commits from base-branch..feat/user-auth and replays on main
```

### Edit the Root Commit

```bash
# First commit is special — --root reaches it
git rebase -i --root
```

## Cherry-Pick

Apply specific commits from one branch to another without merging the full history.

### Basic Cherry-Pick

```bash
# Apply a single commit to current branch
git checkout release/v1.0
git cherry-pick abc123

# Apply a range of commits (exclusive of first, inclusive of last)
git cherry-pick abc123..def456

# Apply from a different branch without checking it out
git cherry-pick feature/new-api -- src/api/handler.ts
```

### Cherry-Pick Options

```bash
# Don't create commits, just apply changes to working tree
git cherry-pick -n abc123

# Keep original authorship but edit message
git cherry-pick -e abc123

# Add a note in the commit message saying where it came from
git cherry-pick -x abc123
# Results in: "(cherry picked from commit abc123)" in message

# Preserve the original committer date
git cherry-pick --no-commit-date abc123
```

### Cherry-Pick with Conflicts

```bash
git cherry-pick abc123
# CONFLICT in src/app.ts

# Fix conflicts, then:
git add src/app.ts
git cherry-pick --continue

# Or abort entirely:
git cherry-pick --abort
```

### Cherry-Pick Strategy for Hotfix Backport

```bash
# 1. Fix on main
git checkout main
git commit -m "fix: resolve payment race condition"

# 2. Get the commit hash
HASH=$(git rev-parse HEAD)

# 3. Backport to release branch
git checkout release/v1.0
git cherry-pick "$HASH"
```

### Cherry-Pick a Branch onto Another

```bash
# Apply all commits on feature-branch that aren't on main
git cherry-pick main..feature-branch
```

## Bisect

Binary-search through history to find the exact commit that introduced a bug. Works in O(log n) time — 10 steps for 1000 commits.

### Manual Bisect

```bash
# Start bisect session
git bisect start

# Mark current commit as bad (has the bug)
git bisect bad                     # or: git bisect bad HEAD

# Mark a known-good commit (before bug appeared)
git bisect good v1.0               # or: git bisect good abc1234

# Git checks out a midpoint commit. Test it, then:
git bisect good   # if bug is absent
git bisect bad    # if bug is present

# Repeat until Git identifies the first bad commit
# abc1234 is the first bad commit
```

### Scripted Bisect (Fully Automated)

Write a test script that exits 0 (good) or non-zero (bad):

```bash
# Create a test script that reproduces the bug
cat > /tmp/test-bug.sh << 'EOF'
#!/bin/bash
# Build and run the test
npm run build
npm test -- --grep "login should fail with invalid token"
EOF
chmod +x /tmp/test-bug.sh

# Let bisect run it automatically
git bisect start HEAD v1.0
git bisect run /tmp/test-bug.sh
# Git outputs: "abc1234 is the first bad commit"
```

### Bisect with Skip (Flaky Tests)

```bash
# If a commit can't be tested (build breaks unrelated to your bug)
git bisect start HEAD v1.0
git bisect run /tmp/test-bug.sh
# If it hangs or fails to build, git bisect run will mark it as
# untestable (skip) and try other commits

# Manual skip:
git bisect skip
```

### Bisect with Logging

```bash
# Log each bisect step for debugging
git bisect start HEAD v1.0
git bisect run sh -c "npm run build && npm test 2>&1 | tee /tmp/bisect-log.txt"
```

### Bisect Reset

```bash
# Always reset when done, even if you cancel mid-way
git bisect reset
```

## Worktrees

Git worktrees allow checking out multiple branches simultaneously in separate directories, all sharing the same Git repository.

### Basic Worktree Operations

```bash
# Create a worktree for a new feature branch
git worktree add ../feat/user-auth -b feat/user-auth

# Create a worktree on an existing branch
git worktree add ../fix/crash fix/login-crash

# List all worktrees
git worktree list
# /repo/main           abc1234 [main]
# /repo/../feat/auth   def5678 [feat/user-auth]
# /repo/../fix/crash   987def6 [fix/crash]
```

### Worktree Lifecycle

```bash
# Create worktree with a specific commit (detached HEAD)
git worktree add ../debug/deploy-tag v1.0.0

# Create worktree and lock it (prevents pruning)
git worktree add --lock ../release/v1.1 release/v1.1

# Remove a worktree (safe — doesn't lose commits)
git worktree remove ../feat/user-auth

# Remove a locked worktree
git worktree remove --force ../release/v1.1

# Prune stale worktree references (after manually deleting the directory)
git worktree prune
```

### Worktree for Code Review

```bash
# Review a PR branch without disturbing your current work
git worktree add ../review/pr-42 feature/pr-42
cd ../review/pr-42
npm install
npm test
# Review done: remove cleanly
cd /repo/main
git worktree remove ../review/pr-42
```

### Worktree for Emergency Hotfix

```bash
# Current branch: feat/user-auth (mid-work, dirty tree)
# Emergency: fix production crash

# Create worktree on main → hotfix branch
git worktree add ../hotfix/crash main
cd ../hotfix/crash
git checkout -b hotfix/payment-null
# Fix, commit, push, PR
git add .
git commit -m "fix: handle null payment amount"
git push -u origin hotfix/payment-null

# Delete worktree after merge
cd /repo/main
git worktree remove ../hotfix/crash
```

### Worktree with .gitignore Safety

```bash
# Always add the worktree directory to .gitignore
echo ".worktrees/" >> .gitignore
git add .gitignore
git commit -m "chore: ignore worktree directory"

# Create worktree inside the project (cleaner)
git worktree add .worktrees/my-feature -b feat/new-feature
```

## Common Issues & Troubleshooting

### Detached HEAD State

**What happened:** You checked out a commit hash instead of a branch name. HEAD points directly to a commit, not a branch reference.

```text
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches...
```

**Recovery scenarios:**

```bash
# Scenario 1: You just want to go back to a branch (no new commits)
git checkout main

# Scenario 2: You made commits and want to keep them
git checkout -b new-branch-name
# Now your commits are on 'new-branch-name'
# Then merge or PR as normal

# Scenario 3: You made commits and want them on an existing branch
git checkout existing-branch
git cherry-pick detached-branch..HEAD
# Replace detached-branch with the commit hash you started at

# Scenario 4: You made commits but don't want them
git checkout main  # Git warns you, but it's fine
# The commits will eventually be garbage-collected
```

### Complex Merge Conflict Resolution

**Step-by-step for nasty conflicts:**

```bash
# When rebase hits a conflict:
git rebase main
# CONFLICT (content): Merge conflict in src/config.ts

# 1. Open the conflicted file
#    <<<<<<< HEAD       — current branch's version
#    =======            — divider
#    >>>>>>> featur     — incoming branch's version

# 2. Resolve manually, or use a merge tool
git mergetool           # Opens configured tool (vimdiff, VS Code, etc.)

# 3. Once resolved:
git add src/config.ts
git rebase --continue

# To abort the entire rebase:
git rebase --abort
```

**Conflict patterns and resolutions:**

| Conflict Pattern | Strategy |
|---|---|
| Both sides added the same function | Compare implementations, keep the correct one |
| One side deleted, other modified | `git checkout --ours/--theirs src/file.ts` to pick |
| Whitespace/formatting only | `git rebase -X theirs` to auto-resolve with incoming |
| Binary file conflict | Pick one side: `git checkout --theirs logo.png` |
| Rename/add conflict | Manually reconcile the rename with the new file |
| Multiple files, same pattern | Use a script to batch-resolve known-safe patterns |

```bash
# Accept all 'ours' or 'theirs' for a specific file
git checkout --ours src/config.ts
git add src/config.ts

# Accept all 'ours' for ALL conflicted files
git diff --name-only --diff-filter=U | xargs git checkout --ours
git add -u
```

### Reflog Recovery (Lost Commits)

**When you need it:** After a bad rebase, accidental branch delete, or `git reset --hard` that went too far.

```bash
# View every action that moved HEAD
git reflog
# abc1234 HEAD@{0}: checkout: moving from main to feat/auth
# def5678 HEAD@{1}: commit: fix: handle empty username
# 9876abc HEAD@{2}: commit: feat: add login form
# fedcba9 HEAD@{3}: rebase finished: returning to refs/heads/feat/auth

# Restore to a previous state
git reset --hard HEAD@{2}

# Or create a branch at a reflog entry (safer)
git branch recover-branch HEAD@{3}

# View reflog for a specific branch
git reflog show feat/auth

# Show reflog timeline with relative times
git reflog --date=relative
```

### Force Push Safety

```bash
# Safe force push — only succeeds if your local branch is based on
# the remote's current tip (prevents overwriting others' work)
git push --force-with-lease origin feat/auth

# Even safer: specify expected remote ref
git push --force-with-lease=feat/auth:origin/feat/auth

# Nuclear option (use ONLY on personal branches)
git push --force origin feat/auth
```

### Lost Work After Stash Drop

```bash
# List all stashes, including dropped ones
git fsck --unreachable | grep commit | cut -d' ' -f3 | xargs git log --mergeless --oneline

# Or use gitk to explore dangling commits
gitk --all $(git fsck --unreachable | grep commit | cut -d' ' -f3)

# Create a branch from the dangling commit
git branch recover-stash abc1234
```

### Undoing Things

```bash
# Undo last commit but keep changes staged
git reset --soft HEAD~1

# Undo last commit and unstage changes
git reset --mixed HEAD~1    # (default)

# Undo last commit and discard changes entirely
git reset --hard HEAD~1

# Undo a published commit (creates a new commit)
git revert HEAD
git revert abc1234          # Revert specific commit

# Amend the last commit (don't do this after push)
git add forgotten-file.ts
git commit --amend --no-edit

# Amend message only
git commit --amend -m "fix: better commit message"
```

### Cleanup and Optimization

```bash
# Remove local branches that no longer exist on remote
git fetch --prune
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -d

# Squash all fixup commits in your branch
git rebase -i --autosquash main
# (use git commit --fixup=HASH during development for auto-matching)

# Compact repository (reduces disk usage)
git gc --aggressive --prune=now

# Remove untracked files
git clean -fd          # Dry-run first with -n
git clean -fdn         # Preview what will be removed
```

## Red Flags

| Situation | Risk | Action |
|-----------|------|--------|
| Force pushing to shared branches | Destroys collaborators' history | Use `--force-with-lease` or never force push |
| Rebasing a branch others have pulled | Divergent histories, confusion | Communicate before force-push; coordinate pull timing |
| Interactive rebase on published commits | Rewriting public history | Only rebase unpublished commits |
| Cherry-pick without `-x` on hotfix branches | No traceability back to source | Use `-x` to annotate cherry-picks |
| Merge commits in a feature branch | Cluttered history before review | Squash or rebase before PR |
| Working with dirty working tree | Accidental commit of unrelated changes | Commit or stash before switching context |
| Long-lived feature branches | Merge hell, integration pain | Keep branches <1 sprint; rebase daily |
| Not running `git worktree prune` after manual delete | Stale worktree references | Prune after removing worktree directories |
| Using `git reset --hard` without checking `git status` | Losing uncommitted work | Always `git stash` or check `status` first |

## Monetization

This skill generates income through the following channels:

### 1. Git Workflow Consulting ($150-400/hr)

Companies adopting Git or migrating from centralized VCS (SVN, TFS, Perforce) need workflow setup and team training.

**Services:**
- Branch strategy design and CONTRIBUTING.md documentation
- CI/CD trigger setup per branch strategy
- Migration from SVN/TFS to Git with history preservation
- Team training workshop (half-day or full-day)
- Code review culture implementation using GitHub/GitLab flows

**Outreach:** Target startups scaling from 5→20+ engineers (the point where Git chaos sets in).

### 2. Automated Git Audit Tool ($500-2,000/project)

Build a CLI tool that scans a repo and reports:
- Branch naming convention violations
- Merge commit frequency in feature branches
- Commit message quality (Conventional Commits compliance)
- Stale branch age and count
- Large file tracking and BFG cleanup candidates

```bash
# Example output:
$ git-audit .
❌ Branch naming: 3 branches don't match convention (fix/ vs fix-)
❌ Merge commits: 12 merge commits in feature branches
⚠️  Commit quality: 40% pass Conventional Commits
ℹ️  Stale branches: 8 branches untouched >30 days
ℹ️  Large files: 2 files >10MB should use Git LFS
```

### 3. Emergency Git Recovery Service ($100-500/incident)

Developers frequently lose work through bad rebases, force pushes, or accidental branch deletion. Offer a recovery service:

```bash
# Example recovery workflow for a client
ssh client-server
cd /repo
git reflog
# Find lost state
git branch rescue-branch HEAD@{5}
git format-patch main..rescue-branch --stdout > recovery.patch
# Apply on client's fresh clone
```

Package this as an automated CLI tool + premium human-assisted recovery.

### 4. Git Automation Scripts / SaaS ($10-50/month per seat)

Build scripts that automate common complex workflows:

```bash
# Example: automated release branch creation + version bump
git-auto-release --type minor --message "release: v1.2.0"

# Example: bulk rebase all feature branches onto updated main
git-rebase-all

# Example: squash all fixup commits across all branches
git-bulk-squash
```

Sell as npm package or marketplace extension (GitHub Actions, GitLab CI templates).

### 5. Training Content ($27-297/course)

- "Git Mastery for Teams" — video course (6 modules, 3 hours)
- "Git Recovery Playbook" — PDF guide with 20 disaster-recovery scenarios
- "Git Workflow Templates" — reusable branching docs + hooks scripts

### 6. Internal Adoption for Your Team

Directly reduces integration time, CI pipeline failures, and onboarding overhead:
- **Measured impact:** Teams adopting Git Flow or trunk-based development reduce merge-conflict resolution time by 60-80%
- **Onboarding:** New engineers reach shipping velocity 2-3x faster with documented conventions
- **CI reliability:** Clean history means cleaner CI triggers — fewer false-positive failures

## Verification

- [ ] Branch strategy documented in CONTRIBUTING.md
- [ ] Commit messages follow Conventional Commits
- [ ] PRs have clean, squashed history
- [ ] No merge conflicts on main branch
- [ ] All team members understand the chosen branching model
- [ ] Reflog checked when recovering lost work
- [ ] Worktrees cleaned up after feature completion (`git worktree prune`)
- [ ] Test suite passes after every rebase operation
- [ ] CI pipeline triggers correctly per branch type
- [ ] Remote branches pruned with `git fetch --prune` on schedule

## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
2. **Choose strategy** — Select branching model based on release cadence (Git Flow, GitHub Flow, trunk-based)
3. **Branch naming** — Use convention: feat/, fix/, chore/, docs/, refactor/, test/, perf/
4. **Commit messages** — Follow Conventional Commits format with scope and body
5. **Interactive rebase** — Clean up history before merge using squash, fixup, reword
6. **Cherry-pick** — Apply specific commits to other branches for hotfix backport
7. **Bisect** — Binary search for bug-introducing commits using manual or scripted mode
8. **Worktrees** — Parallel work on multiple branches with lifecycle management
9. **Verify** — Validate output meets requirements, document results, clean up

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will clean up commits later" | You never do. Interactive rebase before every PR. |
| "Force push is fine on my branch" | Force push destroys history. Use --force-with-lease if you must. |
| "Merge commits are fine" | Squash or rebase keeps history linear and readable |
| "Git bisect is overkill" | It finds the exact bug-introducing commit in O(log n) time |
| "I can just reset --hard and redo it" | You lose uncommitted work and the reflog entry might be your only lifeline |
| "The merge conflict is too complex, I'll start over" | Conflict resolution is a skill. Use mergetool, learn the patterns, persist. |
| "Worktrees are just for large projects" | Any project with context-switching benefits from isolated workspaces |
| "Reflog is only for emergencies" | Check reflog regularly — it's the best undo button you have |
