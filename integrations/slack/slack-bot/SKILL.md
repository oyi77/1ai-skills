---
name: slack-bot
description: Skill for Build Slack bots. Provides automation and best practices.
domain: integrations
---
## Slack Bot

Build Slack bots

### Usage

```
/slack-bot <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create a Slack app at api.slack.com/apps
2. Configure bot scopes (chat:write, channels:read, reactions:write)
3. Install the app to your workspace and get the bot token
4. Implement event listeners for messages, reactions, and slash commands
5. Deploy to a persistent host with Socket Mode or HTTP Events API

## Bot Implementation

```python
from slack_bolt import App

app = App(token="xoxb-...", signing_secret="...")

@app.message("hello")
def handle_hello(message, say):
    say(f"Hey <@{message['user']}>! How can I help?")

@app.command("/deploy")
def handle_deploy(ack, command, say):
    ack(f"Deploying {command['text']}...")
    say("Deployment complete!")
```

## Common Patterns

- Use Block Kit for rich interactive messages
- Implement slash commands for quick actions
- Use Socket Mode for firewall-friendly connections
- Store conversation state per channel for multi-turn workflows

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

