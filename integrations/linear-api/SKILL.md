---
name: linear-api
description: Linear API integration — issue tracking, project management, cycle planning,
  team workflows via GraphQL API
domain: integrations
---

## Overview

Integrate with Linear for modern project management — create/update issues, manage cycles and projects, automate team workflows via GraphQL API.

## Capabilities

- GraphQL API for all Linear operations
- Issue, project, and cycle management
- Team and user management
- Custom views and filters
- Webhook subscriptions for real-time events
- Automation with Linear workflows

## When to Use

- Building custom project management tools
- Syncing Linear with external systems (GitHub, Slack, Jira)
- Automating issue triage and assignment
- Generating custom reports and dashboards
- Building CLI tools for Linear

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


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


### GraphQL Query — List Issues

```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "{ issues(first: 50, filter: { state: { name: { eq: \"In Progress\" } } }) { nodes { id title identifier state { name } assignee { name } priority } } }"
  }'
```

### Create Issue

```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation { issueCreate(input: { title: \"Fix auth bug\", teamId: \"team-id\", priority: 1, description: \"Login fails on Safari\" }) { success issue { id identifier } } }"
  }'
```

### Update Issue State

```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation { issueUpdate(id: \"issue-id\", input: { stateId: \"state-id\" }) { success issue { state { name } } } }"
  }'
```

### Python Client

```python
import requests

API_KEY = "lin_api_xxx"
headers = {"Authorization": API_KEY, "Content-Type": "application/json"}

# List issues
query = """
{
  issues(first: 50, filter: { state: { name: { eq: "Todo" } } }) {
    nodes { id title identifier priority assignee { name } }
  }
}
"""
resp = requests.post("https://api.linear.app/graphql", json={"query": query}, headers=headers)
issues = resp.json()["data"]["issues"]["nodes"]

# Create issue
mutation = """
mutation {
  issueCreate(input: {
    title: "New feature",
    teamId: "team-id",
    priority: 2,
    projectId: "project-id"
  }) {
    success
    issue { id identifier url }
  }
}
"""
```

### Cycle Management

```bash
# Get active cycle
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query": "{ team(id: \"team-id\") { activeCycle { id name startsAt endsAt issues { nodes { title } } } } }"}'
```

### Webhook Setup

```bash
# Create webhook subscription
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{
    "query": "mutation { webhookCreate(input: { url: \"https://your-server.com/webhook\", teamId: \"team-id\", resourceTypes: [\"Issue\", \"Project\", \"Cycle\"] }) { success webhook { id } } }"
  }'
```

## Common Patterns

- **Auto-triage**: Assign new issues based on labels/components
- **Cycle Reports**: Generate weekly cycle summaries
- **GitHub Sync**: Link PRs to Linear issues via branch names
- **Slack Notifications**: Post issue updates to Slack channels
- **Custom Dashboards**: Build project health dashboards from Linear data

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
