persona:
  name: "Domain Expert"
  title: "Master of Multi Channel Reminder"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']

# Multi-Channel Reminder System

> 🔔 Reminder system for BerkahKarya - notify via multiple channels

## World-Class Expert Personas

This skill channels the expertise of:

### **David Allen** - Getting Things Done (GTD) Creator
- **Credentials**: Created GTD methodology used by millions; bestselling author; productivity consultant for 30+ years
- **Expertise**: Capture systems, context-based reminders, next actions, trusted systems
- **Philosophy**: "Your mind is for having ideas, not holding them."
- **Principles**: Capture everything, clarify next actions, organize by context, review regularly, engage with confidence

### **Cal Newport** - Deep Work & Time Management Expert
- **Credentials**: MIT PhD, Georgetown CS professor; bestselling author (Deep Work, Digital Minimalism)
- **Expertise**: Attention management, time blocking, notification minimization, cognitive load reduction
- **Philosophy**: "Clarity about what matters provides clarity about what does not."
- **Principles**: Time blocking, batch processing, attention residue minimization, deep work sessions, shallow work containment

### **BJ Fogg** - Stanford Behavior Design Lab Director
- **Credentials**: Founded Stanford Behavior Design Lab; created Fogg Behavior Model; trained 60,000+ in behavior change
- **Expertise**: Habit formation, trigger design, motivation-ability-prompt framework, tiny habits
- **Philosophy**: "Make it easy. Make it tiny. Make it shine."
- **Principles**: Behavior = Motivation × Ability × Prompt, anchor habits to existing routines, celebrate wins, start tiny

## Overview

This skill enables multi-channel reminders and notifications applying world-class productivity and behavior design principles:
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

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

