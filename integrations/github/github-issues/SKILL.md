---
name: github-issues
description: Create an issue. Use when performing github issues tasks in integrations workflows.
domain: integrations
tags:
- api
- github
- integrations
- issues
- third-party
- workflow
---
## Github Issues

Manage GitHub issues

### Usage

```
/github-issues <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Use GitHub Issues API to programmatically create, update, and manage issues
2. Apply labels and milestones for organization and prioritization
3. Link issues to pull requests using keywords (fixes #123)
4. Use issue templates for consistent bug reports and feature requests

## Issue Management API

```bash
# Create an issue
## When to Use

**Trigger phrases:**
- "github issues"
- "Help me with github issues"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

curl -X POST "https://api.github.com/repos/OWNER/REPO/issues" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"title": "Bug: login fails", "labels": ["bug"]}'

# Add a comment
curl -X POST "https://api.github.com/repos/OWNER/REPO/issues/123/comments" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"body": "Investigating this now."}'
```

## Common Patterns

- Use issue templates to standardize bug reports
- Apply labels automatically based on file paths changed in PRs
- Close issues automatically via PR merge keywords
- Use GitHub Projects for kanban-style tracking

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
