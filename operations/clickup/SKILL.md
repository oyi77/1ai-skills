---
name: clickup
description: 'Skill: clickup. See SKILL.md body for details. Use when this domain
  is relevant.'
domain: operations
---
*Use ClickUp for flexible task management. Tasks, docs, time - all in one.*

## When NOT to Use

- When the operational process requires change advisory board approval
- When the process involves legally mandated human review or sign-off
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Operational changes are made without stakeholder communication
- Agent does not track compliance with established processes
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Changes are communicated to stakeholders before implementation
- [ ] Compliance with established processes is tracked and reported
- [ ] All required outputs generated
- [ ] Success criteria met

## How to Use

1. Identify the task lifecycle: create tasks in ClickUp with clear assignees, priorities, and due dates.
2. Use ClickUp's hierarchy: Spaces > Folders > Lists > Tasks. Match the hierarchy to team structure.
3. Leverage custom fields for domain-specific metadata (e.g., sprint points, client name, ticket type).
4. Automate repetitive workflows using ClickUp Automations (triggers: status change, due date, assignee).
5. Use ClickUp Docs for meeting notes and specs linked to relevant tasks.
6. Track time per task for workload visibility and billing accuracy.

### ClickUp API Integration

- Use the ClickUp REST API v2 for programmatic task creation, updates, and reporting.
- Authenticate via personal API token or OAuth2 app.
- Key endpoints: `/team`, `/space`, `/folder`, `/list`, `/task`, `/time_entries`.
- Webhooks enable real-time event-driven workflows on task changes.

### Best Practices

- Keep task descriptions actionable with clear acceptance criteria.
- Use tags and custom fields consistently across the workspace to avoid data silos.
- Archive completed Lists quarterly to keep workspace navigable.
- Review the verification checklist after applying this skill.
- Document automation patterns you discover for future use.

### Troubleshooting

- If tasks are not syncing, verify API token scope covers the target Space.
- If automations fail silently, check the ClickUp Automations log in the task view.
- For rate limit errors (HTTP 429), implement exponential backoff on API calls.
- If output quality is low, provide more context about the workspace structure.
- For SSO issues, verify the ClickUp plan supports the SAML/SSO integration tier.
- If dashboards show stale data, force-refresh the widget or check the data source filter date range.