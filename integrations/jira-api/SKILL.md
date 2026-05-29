---
name: jira-api
description: Jira API integration — issue management, sprint planning, workflow automation, custom fields, JQL queries
---

## Overview

Integrate with Atlassian Jira for project management automation — create/update issues, manage sprints, run JQL queries, automate workflow transitions, and sync with external systems.

## Capabilities

- Create, update, and transition issues via REST API
- Manage sprints and boards (Scrum/Kanban)
- Query issues with JQL (Jira Query Language)
- Handle custom fields and issue types
- Automate workflow transitions
- Manage users, groups, and permissions
- Webhook event handling for real-time sync

## When to Use

- Automating bug/issue creation from monitoring alerts
- Syncing tasks between Jira and other project tools
- Building custom dashboards or reports from Jira data
- Automating sprint ceremonies (standup reports, burndown)
- Bulk operations on issues (migration, cleanup)

## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Authenticate with Jira REST API

```bash
# Cloud (API token)
curl -s -u "email@company.com:API_TOKEN" \
  "https://your-domain.atlassian.net/rest/api/3/myself"

# Server/Data Center (Personal Access Token)
curl -s -H "Authorization: Bearer $JIRA_TOKEN" \
  "https://jira.company.com/rest/api/2/myself"
```

### Create an Issue

```bash
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -u "email:API_TOKEN" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "issuetype": {"name": "Task"},
      "summary": "Fix login bug",
      "description": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Login fails on mobile"}]}]},
      "priority": {"name": "High"},
      "assignee": {"accountId": "user-id"}
    }
  }'
```

### Query with JQL

```bash
# Search issues
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/search" \
  -H "Content-Type: application/json" \
  -u "email:API_TOKEN" \
  -d '{
    "jql": "project = PROJ AND status = \"In Progress\" AND assignee = currentUser() ORDER BY priority DESC",
    "maxResults": 50,
    "fields": ["summary", "status", "priority", "assignee"]
  }'
```

### Transition Issue

```bash
# Get available transitions
curl -s "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/transitions" \
  -u "email:API_TOKEN"

# Transition to "Done"
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/transitions" \
  -H "Content-Type: application/json" \
  -u "email:API_TOKEN" \
  -d '{"transition": {"id": "31"}}'
```

### Sprint Management

```bash
# Get active sprint for board
curl -s "https://your-domain.atlassian.net/rest/agile/1.0/board/1/sprint?state=active" \
  -u "email:API_TOKEN"

# Move issue to sprint
curl -s -X POST "https://your-domain.atlassian.net/rest/agile/1.0/sprint/42/issue" \
  -H "Content-Type: application/json" \
  -u "email:API_TOKEN" \
  -d '{"issues": ["PROJ-123"]}'
```

### Python Client

```python
from jira import JIRA

jira = JIRA(server="https://your-domain.atlassian.net", basic_auth=("email", "API_TOKEN"))

# Create issue
issue = jira.create_issue(
    project="PROJ",
    summary="Automated bug report",
    issuetype={"name": "Bug"},
    priority={"name": "High"}
)

# Search with JQL
issues = jira.search_issues("project = PROJ AND status = 'To Do'", maxResults=50)

# Transition
jira.transition_issue(issue, "In Progress")
```

## Common Patterns

- **Alert → Issue**: Auto-create Jira issues from monitoring alerts (PagerDuty, Datadog)
- **PR → Issue Link**: Link GitHub PRs to Jira issues via commit messages
- **Sprint Reports**: Generate standup/burndown reports via JQL queries
- **Bulk Migration**: Script bulk issue updates using pagination (`startAt`)
- **Webhook Sync**: Listen to Jira webhooks for real-time issue state changes

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
