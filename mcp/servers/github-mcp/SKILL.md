---
name: github-mcp
description: MCP server for GitHub automation
domain: mcp
---
## Github Mcp

MCP server for GitHub automation

### Usage

```
/github-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Set the GITHUB_PERSONAL_ACCESS_TOKEN environment variable
2. Configure the MCP server in your client settings
3. Use tools for repository, issue, PR, and workflow management

## Available Tools

| Tool | Description |
|------|-------------|
| `search_repositories` | Search GitHub repos by query |
| `create_issue` | Create a new issue with labels and assignees |
| `create_pull_request` | Open a PR with title, body, and base branch |
| `list_issues` | List issues with filters (state, labels, assignee) |
| `get_file_contents` | Read file content from a repository |
| `create_or_update_file` | Commit a file change directly |

## Common Patterns

- Use search_repositories before get_file_contents to resolve repo IDs
- Create issues with structured templates for consistency
- Link PRs to issues using keywords for automatic closing

## When NOT to Use

- When the MCP server requires organization admin permissions
- When the repository contains classified or export-controlled code
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not validate webhook payload signatures
- Agent does not handle GitHub API deprecation notices
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Webhook payload signatures are validated before processing
- [ ] API deprecation notices are monitored and addressed
- [ ] All required outputs generated
- [ ] Success criteria met

