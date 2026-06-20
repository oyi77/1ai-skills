---
name: github-actions
description: Github Actions. Use when working with github actions in integrations domain.
domain: integrations
tags:
- actions
- api
- github
- integrations
- third-party
---
## When to Use

**Trigger phrases:**
- "github actions"
- "Help me with github actions"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Github Actions

Automate GitHub Actions

### Usage

```
/github-actions <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create `.github/workflows/` directory in your repository
2. Define workflow YAML files with trigger conditions (push, PR, schedule)
3. Configure jobs with steps, using marketplace actions or custom scripts
4. Set repository secrets for credentials and API keys
5. Monitor workflow runs in the Actions tab

## Workflow Template

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

## Common Patterns

- Cache dependencies to speed up builds (actions/cache action)
- Use matrix builds for multi-platform testing
- Pin action versions to SHA for reproducibility
- Use `concurrency` to cancel redundant workflow runs
- Set `permissions` explicitly for security hardening

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
