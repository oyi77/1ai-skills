---
name: cron-designer
description: Design complex cron schedules
domain: automation
---
## Cron Designer

Design complex cron schedules

### Usage

```
/cron-designer <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## When NOT to Use

- When the scheduled task affects production data and requires manual approval
- When the cron job must coordinate across multiple distributed systems
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Cron jobs run without health checks confirming successful completion
- Agent schedules jobs during peak load periods degrading performance
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Each job has a health check confirming successful completion
- [ ] Scheduling avoids peak load windows
- [ ] All required outputs generated
- [ ] Success criteria met

## Additional Notes

Additional context and best practices for this skill.

### Best Practices
- Combine with related skills for comprehensive coverage
- Review the verification checklist after applying this skill
- Document patterns you discover for future use

### Troubleshooting
- If output quality is low, provide more context in your input
- If the skill does not cover your use case, check related skills
- For integration issues, verify prerequisites and dependencies are met

## Additional Notes

Additional context and best practices for this skill.

### Best Practices
- Combine with related skills for comprehensive coverage
- Review the verification checklist after applying this skill
- Document patterns you discover for future use

### Troubleshooting
- If output quality is low, provide more context in your input
- If the skill does not cover your use case, check related skills
- For integration issues, verify prerequisites and dependencies are met