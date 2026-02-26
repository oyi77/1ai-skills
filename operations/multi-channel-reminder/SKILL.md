#PM|# Multi-Channel Reminder System
KM|
VX|> 🔔 Reminder system for BerkahKarya - notify via multiple channels
RW|
MS|## Overview
SY|
BN|This skill enables Vilona to send reminders and notifications to multiple channels:
KY|- **Text**: WhatsApp, SMS, Signal
HB|- **Call**: Voice calls (Twilio)
ZH|- **Chat**: Slack, Discord, Telegram
NN|- **Email**: Gmail, Outlook
TX|
XN|## Architecture
BY|
ST|```
YR|Vilona (AI)
HV|    │
QN|    ├── Task Sources (Notion, ClickUp, Jira, etc.)
ZQ|    │
PJ|    ├── n8n Workflow (automation)
PM|    │
QP|    └── Multi-Channel Output
ZN|            ├── WhatsApp (Twilio/ultramsg)
NJ|            ├── Signal (Signal MCP)
RW|            ├── Slack
XM|            ├── Discord
WQ|            ├── Telegram
HQ|            ├── Voice Call (Twilio)
JZ|            └── Email
```
ZM|

> 🔔 Reminder system for BerkahKarya - notify via multiple channels

## Overview

This skill enables Vilona to send reminders and notifications to multiple channels:
- **Text**: WhatsApp, SMS
- **Call**: Voice calls (Twilio)
- **Chat**: Slack, Discord, Telegram
- **Email**: Gmail, Outlook

## Architecture

```
Vilona (AI)
    │
    ├── Task Sources (Notion, ClickUp, Jira, etc.)
    │
    ├── n8n Workflow (automation)
    │
    └── Multi-Channel Output
            ├── WhatsApp (Twilio/ultramsg)
            ├── Slack
            ├── Discord
            ├── Telegram
            ├── Voice Call (Twilio)
            └── Email
```

## MCP Servers Required
RJ|
PP|### 1. Communication MCP
BV|```bash
YB|# Slack, Discord, Telegram, Signal integration
SW|{
TS|  "mcpServers": {
QT|    "slack": { ... },
KJ|    "discord": { ... },
NQ|    "telegram": { ... },
JV|    "signal": { ... }
BK|}
NN|```

TB|### 2. Twilio (Voice + SMS + WhatsApp)
BV|```bash
KZ|# For calls, SMS, WhatsApp
BW|TWILIO_ACCOUNT_SID=your_sid
QB|TWILIO_AUTH_TOKEN=your_token
YV|TWILIO_PHONE_NUMBER=+1234567890
SX|```

NJ|### 3. Signal CLI (for Signal messages)
BV|```bash
# Using signal-cli or API service
SIGNAL_API_KEY=your_signal_key
# Or use services like: signal-cli, messagebird, etc.
```

RR|### 4. Email MCP
BV|```bash
JN|# For email notifications
MM|GMAIL_API_KEY=your_key
WV|```

KZ|## Usage Examples

### 1. Communication MCP
```bash
# Slack, Discord, Telegram integration
{
  "mcpServers": {
    "slack": { ... },
    "discord": { ... },
    "telegram": { ... }
  }
}
```

### 2. Twilio (Voice + SMS)
```bash
# For calls and SMS
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```

### 3. Email MCP
```bash
# For email notifications
GMAIL_API_KEY=your_key
```

## Usage Examples

### Create Reminder
```
User: "Remind Veris tentang campaign launch tomorrow 9 AM via WhatsApp"
Vilona: 
1. Checks task in ClickUp/Notion
2. Creates n8n workflow for scheduled reminder
3. WhatsApp notification triggered at 9 AM
```

### Multi-Channel Alert
```
User: "Notify all team members about urgent deadline via Slack and WhatsApp"
Vilona:
1. Creates workflow with multiple notification nodes
2. All channels get the message
```

### Voice Call Reminder
```
User: "Call me if there's an urgent task"
Vilona:
1. Sets up trigger workflow
2. Voice call made via Twilio
```

## Workflow Template (n8n)

### Daily Task Reminder
```
Trigger: Schedule (Daily 9:00 AM)
│
├─► Notion: Get today's tasks
│
├─► Filter: Overdue + Due Today
│
├─► Slack: Send to #tasks
├─► WhatsApp: Send to team
└─► Email: Summary to manager
```

### Urgent Alert
```
Trigger: Webhook (from ClickUp/Jira)
│
├─► Filter: Priority = High
│
├─► Slack: @mention owner
├─► WhatsApp: Urgent message
├─► Discord: Alert channel
└─► Voice Call: If critical
```

## Channel Comparison
BT|
YR|| Channel | Speed | Best For |
XJ||---------|-------|----------|
TY|| WhatsApp | Fast | Personal, urgent |
TS|| Signal | Fast | Privacy-sensitive, secure |
VS|| Slack | Fast | Team, async |
XQ|| Discord | Fast | Community, alerts |
JT|| Telegram | Fast | Bot integrations |
KP|| Voice Call | Instant | Critical emergencies |
VX|| Email | Slow | Non-urgent, summaries |

HX|## Auto-Activation Triggers

ST|| Trigger Phrases | Action |
BY||----------------|--------|
ZJ|| "remind", "reminder" | Create reminder |
TY|| "notify", "alert" | Send notification |
PJ|| "call me", "voice" | Trigger voice call |
TR|| "whatsapp", "signal", "slack", "discord" | Select channel |
HX|| "urgent", "critical" | Multi-channel alert |

| Channel | Speed | Best For |
|---------|-------|----------|
| WhatsApp | Fast | Personal, urgent |
| Slack | Fast | Team, async |
| Discord | Fast | Community, alerts |
| Telegram | Fast | Bot integrations |
| Voice Call | Instant | Critical emergencies |
| Email | Slow | Non-urgent, summaries |

## Auto-Activation Triggers

| Trigger Phrases | Action |
|----------------|--------|
| "remind", "reminder" | Create reminder |
| "notify", "alert" | Send notification |
| "call me", "voice" | Trigger voice call |
| "whatsapp", "slack", "discord" | Select channel |
| "urgent", "critical" | Multi-channel alert |

## Integration with Task Managers

### ClickUp Integration
```javascript
// When task created/updated in ClickUp
clickup_task_created → n8n webhook → 
  Check priority → 
  If urgent → Multi-channel notification
```

### Jira Integration
```javascript
// Sprint start/end
jira_sprint_started → n8n → 
  Get sprint tasks → 
  Post to Slack #sprint
```

### Notion Integration
```javascript
// Task due date reached
notion_task_due → n8n → 
  Get task details → 
  Send reminder via channel
```

## Configuration

### Team Notification Groups
```json
{
  "teams": {
    "engineering": {
      "slack": "#engineering",
      "whatsapp": "group-link"
    },
    "marketing": {
      "slack": "#marketing", 
      "whatsapp": "group-link"
    }
  }
}
```

### Reminder Rules
```json
{
  "reminder_rules": {
    "overdue": {
      "channels": ["slack", "whatsapp"],
      "immediate": true
    },
    "due_today": {
      "channels": ["slack"],
      "time": "09:00"
    },
    "due_tomorrow": {
      "channels": ["slack"],
      "time": "17:00"
    },
    "critical": {
      "channels": ["slack", "whatsapp", "voice"],
      "immediate": true
    }
  }
}
```

---

*Never miss a task. Always notified. Multiple channels, one system.*
