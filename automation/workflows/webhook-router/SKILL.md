---
name: webhook-router
description: Route webhooks intelligently
domain: automation
---
## Webhook Router

Route webhooks intelligently

### Usage

```
/webhook-router <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## When NOT to Use

- When webhook payloads contain unencrypted sensitive data
- When the routing logic requires complex business rules beyond pattern matching
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Router does not validate webhook signatures allowing spoofed requests
- Agent does not implement idempotency for duplicate deliveries
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Webhook signatures are validated before processing
- [ ] Idempotency prevents duplicate processing of re-delivered webhooks
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