---
name: github-pr
description: Use when gitHub PR — Create, review, and merge pull requests via CLI and API, branch protection, auto-merge. See parent skill for all GitHub automation capabilities.
domain: integrations
tags:
- api
- github
- integrations
- pr
version: 1.0.0
---

# GitHub PR

## Quick Reference

The GitHub PR sub-skill covers pull request lifecycle automation — creation, review, merge via `gh` CLI and REST/GraphQL APIs, branch protection policies, required status checks, auto-merge trains, and merge queue configuration. This layers on the parent [GitHub Automation Hub](../SKILL.md) which covers the full Actions+Issues+PR ecosystem and money-making protocols.

**Use this when** you need to automate PR workflows, enforce merge policies, or build review pipelines beyond manual clicking.

## Overview

Pull requests are the gate between code and production. Automation here directly impacts code quality, deployment velocity, and compliance. Key patterns:
- **Auto-merge trains** — merge approved PRs automatically once CI passes
- **Branch protection rules** — enforce required reviews, status checks, linear history
- **Cross-repo dependencies** — update downstream PRs when upstream changes
- **PR templates** — standardize descriptions, link issues, add checklists
- **Merge queue** — group PRs into merge batches with atomic CI (GitHub Merge Queue)

The parent skill's `auto-merge-prs.sh` and `release.sh` scripts, plus the CI pipeline flow, are the canonical templates.

## Quick Start

### 1. Create and Review a PR
```bash
# Create
gh pr create --repo owner/repo \
  --base main --head feature-branch \
  --title "Add login validation" \
  --body "Closes #42" \
  --reviewer @teammate --label enhancement

# Review
gh pr review PR_NUM --approve --repo owner/repo
gh pr review PR_NUM --request-changes --body "Please fix the error handling"
```

### 2. Set Up Branch Protection
```bash
# Requires: gh >= 2.30, write access to repo
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["CI / test (20)", "lint"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "required_linear_history": true,
  "allow_force_pushes": false
}
EOF
```

### 3. Auto-Merge Approved PRs
```bash
# Merge all open PRs that have at least one APPROVED review
gh pr list --repo owner/repo --state open --json number,reviews \
  | jq -c '.[] | select(.reviews | any(.state == "APPROVED")) | .number' \
  | xargs -I {} gh pr merge {} --repo owner/repo --squash --delete-branch
```

## Code Snippet: Validate PR Title Convention

```python
#!/usr/bin/env python3
"""Validate PR titles match conventional commit format."""
import os, requests, sys

TOKEN = os.environ["GITHUB_TOKEN"]
PR_URL = os.environ.get("PR_URL", "")
# Usage: run as a GitHub Actions step with ${{ github.event.pull_request.title }}

title = sys.argv[1] if len(sys.argv) > 1 else "no title"
import re
pattern = r'^(feat|fix|refactor|docs|test|chore|perf|ci)(\(.+\))?: .{5,}$'
if not re.match(pattern, title):
    print(f"::error::PR title does not match conventional commit format")
    print(f"Expected: feat|fix|refactor|docs|test|chore|perf|ci(scope): description")
    print(f"Got: {title}")
    sys.exit(1)
print(f"Title '{title}' is valid")
```

## Verification Checklist

- [ ] PR creation works via both `gh` CLI and REST API
- [ ] Branch protection rules enforce required reviews and status checks
- [ ] Auto-merge only triggers on PRs with passing CI and APPROVED review
- [ ] PR templates render correctly with YAML frontmatter
- [ ] Merge queue batches PRs and validates atomically (if enabled)

## When to Use

Use when gitHub PR — Create, review, and merge pull requests via CLI and API, branch protection, auto-merge. See parent skill for all GitHub automation capabilities.

## Workflow

Execute these steps sequentially:

### 1. Create and Review a PR
```bash
# Create
gh pr create --repo owner/repo \
  --base main --head feature-branch \
  --title "Add login validation" \
  --body "Closes #42" \
  --reviewer @teammate --label enhancement

# Review
gh pr review PR_NUM --approve --repo owner/repo
gh pr review PR_NUM --request-changes --body "Please fix the error handling"
```

### 2. Set Up Branch Protection
```bash
# Requires: gh >= 2.30, write access to repo
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["CI / test (20)", "lint"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "required_linear_history": true,
  "allow_force_pushes": false
}
EOF
```

### 3. Auto-Merge Approved PRs
```bash
# Merge all open PRs that have at least one APPROVED review
gh pr list --repo owner/repo --state open --json number,reviews \
  | jq -c '.[] | select(.reviews | any(.state == "APPROVED")) | .number' \
  | xargs -I {} gh pr merge {} --repo owner/repo --squash --delete-branch
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll just click the green merge button" | Automated merge trains prevent stale PRs, enforce linear history, and ensure CI passes on merge commit — not just the branch head. |
| "Branch protection slows down development" | Protection rules prevent force-pushes to main, require passing CI, and enforce reviews. The time saved debugging production issues far exceeds the setup cost. |
| "PR templates are a nice-to-have" | Standardized PR descriptions link code changes to issues automatically, produce better changelogs, and make code reviews faster. Worth 10 minutes of setup. |
