---
name: slack-mcp
description: MCP server for Slack integration
---
## Slack Mcp

MCP server for Slack integration

### Usage

```
/slack-mcp <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create a Slack app with bot token scopes (chat:write, channels:read)
2. Install the app and get the SLACK_BOT_TOKEN
3. Configure the MCP server with the token

## Available Tools

| Tool | Description |
|------|-------------|
| `send_message` | Post a message to a channel or user |
| `list_channels` | List available channels |
| `get_channel_history` | Retrieve recent messages from a channel |
| `add_reaction` | Add an emoji reaction to a message |
| `create_channel` | Create a new channel |

## Common Patterns

- Use Block Kit JSON for rich message formatting
- Post to channels by name (with #) or ID
- Use threads to keep conversations organized
- Mention users with user_id format in messages

## When NOT to Use

- When Slack messages contain regulated communications requiring archival
- When the bot operates in channels used for security incident coordination
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- MCP server does not verify channel permissions before posting
- Agent does not handle Slack message size limits
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Channel permissions are verified before posting
- [ ] Message size limits are respected
- [ ] All required outputs generated
- [ ] Success criteria met

