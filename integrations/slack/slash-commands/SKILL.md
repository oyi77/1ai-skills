---
name: slash-commands
description: Create Slack slash commands
domain: integrations
---
## Slash Commands

Create Slack slash commands

### Usage

```
/slash-commands <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Register slash commands in your Slack app configuration
2. Set the request URL to your server endpoint
3. Acknowledge the command within 3 seconds (respond immediately)
4. Process long-running tasks asynchronously and send results via response_url

## Command Implementation

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/slack/commands", methods=["POST"])
def handle_command():
    command = request.form.get("command")
    text = request.form.get("text", "")

    if command == "/status":
        status = get_system_status()
        return jsonify({"response_type": "ephemeral", "text": status})

    elif command == "/deploy":
        process_deploy.delay(text, request.form["response_url"])
        return jsonify({"response_type": "ephemeral", "text": f"Deploying {text}..."})

    return jsonify({"text": "Unknown command"})
```

## Common Patterns

- Respond within 3 seconds to avoid timeout errors
- Use response_url for delayed responses to long-running tasks
- Set response_type to ephemeral for private responses
- Use conversation builders for multi-step command flows

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

