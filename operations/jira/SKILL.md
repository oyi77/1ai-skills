---
name: jira
description: >
  Skill: jira. See SKILL.md body for details. Use when this domain is relevant.
---
*Use Jira for structured project tracking. Every task has a home.*

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

1. Define the project type: Scrum (sprint-based) or Kanban (flow-based) in Jira project settings.
2. Create issues with proper issue types: Epic > Story > Task > Sub-task hierarchy.
3. Assign story points, priority, and sprint at creation time for backlog grooming efficiency.
4. Use JQL (Jira Query Language) for advanced filtering: `project = X AND status != Done ORDER BY priority`.
5. Configure board columns to match the team's actual workflow (not default states).
6. Link related issues (blocks, is blocked by, duplicates) to surface dependency risks early.

### Jira REST API Integration

- Authenticate via API token (basic auth) or OAuth2 for Jira Cloud.
- Key endpoints: `/rest/api/3/issue`, `/rest/api/3/search`, `/rest/api/3/board`.
- Use webhooks for event-driven automation on issue transitions and comments.
- Batch operations via JQL-based bulk edit for large-scale changes.

### Best Practices

- Keep issue descriptions concise but include acceptance criteria in the description or linked Confluence page.
- Use components and labels consistently; avoid overlapping taxonomies.
- Close sprints by moving unfinished items to the next sprint with a comment explaining the delay.
- Review the verification checklist after applying this skill.
- Document JQL patterns and automation rules for team reuse.

### Troubleshooting

- If API calls return 403, verify the token has project-level permissions for the target board.
- If transitions are missing, check the workflow scheme assigned to the issue type.
- For JQL syntax errors, use the Jira issue navigator's "Advanced" mode to validate queries.
- If output quality is low, provide more context about the project configuration.
- For bulk import issues, use the CSV importer with column mapping validation before committing.
- If dashboards show stale data, verify the board filter JQL and refresh the gadget configuration.