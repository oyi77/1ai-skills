---
name: telegram-bot
description: Telegram bot patterns for message handling and webhook integrations
---
## Telegram Bot

Build Telegram bots

### Usage

```
/telegram-bot <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## When NOT to Use

- When the bot interacts with users in regulated industries requiring compliance review
- When Telegram API rate limits would make the automation impractical
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Bot sends messages without rate limiting causing API throttling
- Agent does not handle Telegram webhook failures or retries
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Rate limiting is implemented respecting Telegram API limits
- [ ] Webhook failures trigger retry logic with exponential backoff
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