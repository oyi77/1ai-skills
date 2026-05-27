---
name: n8n
description: Install n8n. Use when relevant to this domain.
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

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This workflow is simple, skip error handling" | Workflows without error handling fail silently - data gets lost |
| "I'll add monitoring later" | Without monitoring, you won't know when workflows break |
| "Manual testing is enough" | Manual testing isn't repeatable - automated tests catch regressions |
| "n8n Cloud handles reliability" | Cloud doesn't fix bad workflow logic - still need error handling |
| "This is just internal, doesn't need QA" | Internal workflows break too - people depend on them |
| "Webhooks are fire-and-forget" | Webhooks need acknowledgment + retry logic |

## Red Flags

- No error handling on HTTP requests (will fail silently)
- No retry logic for transient failures
- Credentials hardcoded in workflow (security risk)
- No logging/output tracking
- Infinite loops possible (trigger → action → trigger again)
- No rate limiting on webhook endpoints
- Workflow does more than one thing (violates single responsibility)

## Verification

After creating/modifying an n8n workflow, confirm:

- [ ] Workflow has error handling on every HTTP node
- [ ] Retry logic configured (3+ attempts with backoff)
- [ ] Credentials stored in n8n credentials, not in workflow JSON
- [ ] Test execution completed successfully (all nodes green)
- [ ] Webhook endpoints have rate limiting configured
- [ ] Execution log shows expected data flow
- [ ] Error workflow configured for failure notifications

---

*Use n8n to automate BerkahKarya operations. Reduce manual work, increase efficiency.*

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

