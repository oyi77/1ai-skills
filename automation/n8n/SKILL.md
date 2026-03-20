# n8n Workflow Automation Skill

> 🔥 n8n-based workflow automation for BerkahKarya operations

## Overview

n8n is a powerful workflow automation tool that can connect all your apps and services. This skill enables Vilona to create, manage, and monitor n8n workflows for BerkahKarya operations.

## When to Use

- **Automate repetitive tasks** — Reduce manual work
- **Connect apps** — Link different services together
- **Create workflows** — Build automated pipelines
- **Monitor executions** — Track workflow health
- **Trigger events** — Start workflows on schedules or webhooks

## Key Features

### Workflow Creation
- Create workflows from natural language descriptions
- Template-based workflow generation
- Connect to 400+ integrations

### Monitoring
- Track workflow execution status
- View error logs
- Monitor success rates

### Integration Points
- **Scheduled triggers** — Time-based automation
- **Webhook triggers** — Event-based automation
- **Custom integrations** — Connect to internal systems

## Setup

### n8n-mcp (MCP Server - RECOMMENDED)
```bash
# Install MCP server
npm install -g n8n-mcp-server

# Add to Claude Desktop config
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "https://your-n8n.com/api/v1",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

### MCP Tools Available
| Tool | Purpose |
|------|---------|
| `n8n_list_workflows` | List all workflows |
| `n8n_get_workflow` | Get workflow details |
| `n8n_create_workflow` | Create new workflow |
| `n8n_update_partial_workflow` | Update workflow |
| `n8n_validate_workflow` | Validate config |
| `n8n_execute_workflow` | Trigger execution |

### Node Discovery (500+ nodes)
- `n8n_search_nodes` - Find nodes
- `n8n_get_node` - Get node details

## References
- **GitHub**: [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills)
- **n8n-mcp**: [n8n-mcp.com](https://www.n8n-mcp.com)

---

## Setup (Legacy)

### Local n8n
```bash
# Install n8n
npm install n8n -g

# Start n8n
n8n start

# Access at http://localhost:5678
```

### n8n Cloud
```bash
# Or use n8n.cloud for managed service
# Sign up at https://n8n.io
```

## Common Workflows for BerkahKarya

### 1. Task Reminder Workflow
```
Trigger: Schedule (daily 9 AM)
→ Get tasks from Notion/ClickUp/Jira
→ Check deadlines
→ Send reminder via Slack/Telegram/WhatsApp
```

### 2. Lead Follow-up Automation
```
Trigger: New row in Google Sheets
→ Parse lead info
→ Create task in CRM
→ Send welcome message
→ Schedule follow-up
```

### 3. Social Media Scheduler
```
Trigger: Scheduled
→ Fetch content from Notion
→ Format for platform
→ Post to Twitter/Instagram/TikTok
→ Log results
```

### 4. Revenue Alert Workflow
```
Trigger: Scheduled (hourly)
→ Check payment gateway status
→ Alert on new payments
→ Update dashboard
```

## Usage Examples

### Create Simple Workflow
```
User: "Buatkan workflow untuk reminder tugas harian"
Vilona: [Creates n8n workflow with Notion + Slack integration]
```

### Monitor Workflow Health
```
User: "cek status workflow yesterday"
Vilona: [Shows execution stats, errors, success rate]
```

### Connect New Service
```
User: "connect shopee ke slack"
Vilona: [Creates webhook-based workflow]
```

## Auto-Activation Triggers

| Trigger Phrases | Action |
|----------------|--------|
| "automation", "workflow", "n8n" | Activate n8n skill |
| "connect app", "integrate" | Create integration workflow |
| "schedule", "reminder" | Create reminder workflow |
| "monitor", "cek status" | Show workflow stats |

## Integration with Other Skills

| Connected Skill | Use Case |
|-----------------|----------|
| `notion` | Store workflow configs, log executions |
| `communication-mcp` | Send notifications (Slack, Discord, Telegram) |
| `database-mcp` | Store execution history |
| `ai-lead-generation` | Automate lead follow-ups |

## Python CLI Client

A standalone REST API client is available for direct n8n interaction from scripts and agents.
Use n8n for complex API integrations -- agent calls n8n webhook, n8n handles credentials, auth, retries.
Agent never touches external API keys.

```bash
# Set API key
export N8N_API_KEY="your-key"
export N8N_BASE_URL="http://localhost:5678"  # default

# List workflows
python scripts/n8n_client.py --action list

# Trigger a workflow
python scripts/n8n_client.py --action trigger --workflow-id 123 --data '{"key": "value"}'

# View recent executions
python scripts/n8n_client.py --action executions --workflow-id 123

# Create a webhook workflow
python scripts/n8n_client.py --action create-webhook --name "My Hook" --path "/my-hook"

# Activate/deactivate
python scripts/n8n_client.py --action activate --workflow-id 123
python scripts/n8n_client.py --action deactivate --workflow-id 123
```

## Files in This Skill

- `SKILL.md` - This file
- `templates/` - Pre-built workflow templates
- `../../scripts/n8n_client.py` - REST API client (list, trigger, create, manage workflows)

---

*Use n8n to automate operations. Reduce manual work, increase efficiency.*
