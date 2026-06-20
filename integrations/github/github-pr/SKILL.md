---
name: github-pr
description: Create PR via CLI. Use when performing github pr tasks in integrations workflows.
domain: integrations
tags:
- api
- github
- integrations
- third-party
- workflow
---
## Github Pr

Handle pull requests

### Usage

```
/github-pr <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create pull requests via API or CLI with descriptive titles and bodies
2. Request reviews from appropriate team members
3. Link related issues using keywords (closes #45, fixes #67)
4. Ensure CI checks pass before merging

## PR Workflow

```bash
# Create PR via CLI
## When to Use

**Trigger phrases:**
- "github pr"
- "Help me with github pr"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

gh pr create --title "feat: add user auth" --body "## Summary
- Added JWT-based auth
- Protected /api routes"

# Review and merge
gh pr review 123 --approve
gh pr merge 123 --squash
```

## Common Patterns

- Use PR templates for consistent description format
- Require at least 2 approvals for production branches
- Squash merge for clean commit history on main
- Use draft PRs for work-in-progress visibility
- Set branch protection rules to enforce checks

## When NOT to Use

- When the integration requires admin-level permissions on the target platform
- When the data exchange involves regulated information requiring encryption
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Integration does not handle API errors or service unavailability
- Agent does not verify data consistency across connected systems
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] API errors and service outages are handled with appropriate retry logic
- [ ] Data consistency is verified across all connected systems
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
