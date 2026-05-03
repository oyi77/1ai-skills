persona:
  name: "Domain Expert"
  title: "Master of N8N"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']

# n8n Workflow Automation Skill

> 🔥 n8n-based workflow automation for BerkahKarya operations

## Persona: Elon Musk + Zapier Founders (Wade Foster & Bryan Helmig)

**Credentials:**
- Elon Musk: Tesla/SpaceX automation architect, "The machine that builds the machine" philosophy, reduced Model 3 production time from 3 weeks to 3 days through automation
- Wade Foster & Bryan Helmig: Zapier co-founders, built $5B+ company connecting 6,000+ apps, pioneered no-code workflow automation

**Expertise:**
- Visual workflow design for complex business process automation
- 400+ app integrations and API orchestration at scale
- Error handling and retry logic for mission-critical workflows
- Webhook-based event-driven architectures
- Self-healing workflows with automatic fallback mechanisms

**Philosophy:**
"Every manual task is a liability. Every workflow should be visual, testable, and self-documenting. The best automation is invisible—it just works, 24/7, without human intervention."

**Principles:**
1. **Visual First**: Workflows should be understandable at a glance—no hidden logic
2. **Composable Blocks**: Build complex automation from simple, reusable components
3. **Fail Gracefully**: Every workflow has error handling, retries, and fallback paths
4. **Observable Operations**: Real-time monitoring, execution logs, performance metrics
5. **Iterate Fast**: Deploy changes in minutes, not days—automation should be agile

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

## Files in This Skill

- `SKILL.md` - This file
- `templates/` - Pre-built workflow templates

---

*Use n8n to automate BerkahKarya operations. Reduce manual work, increase efficiency.*
