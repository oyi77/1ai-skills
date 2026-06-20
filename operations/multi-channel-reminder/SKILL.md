---
name: multi-channel-reminder
description: 'Skill: multi-channel-reminder. See SKILL.md body for details. Use when this domain is relevant.'
domain: operations
tags:
- business-ops
- channel
- management
- multi
- operations
- reminder
---
## When to Use

**Trigger phrases:**
- "multi channel reminder"
- "Help me with multi channel reminder"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

*Never miss a task. Always notified. Multiple channels, one system.*

## When NOT to Use

- When the operational process requires change advisory board approval
- When the process involves legally mandated human review or sign-off
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Operational changes are made without stakeholder communication
- Agent does not track compliance with established processes
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Changes are communicated to stakeholders before implementation
- [ ] Compliance with established processes is tracked and reported
- [ ] All required outputs generated
- [ ] Success criteria met

## How to Use

1. Define the reminder schedule: one-time, recurring (daily/weekly/monthly), or event-triggered.
2. Select delivery channels: email, SMS, WhatsApp, Telegram, Slack, Discord, or push notification.
3. Configure escalation rules: if the primary channel fails or the reminder is unacknowledged, escalate to the next channel.
4. Use timezone-aware scheduling to respect recipient local time (never send at 3 AM).
5. Track acknowledgment: mark a reminder as "done" to stop follow-up escalation.
6. Aggregate reminders into daily digests for low-priority items to avoid notification fatigue.

### Multi-Channel Delivery

- WhatsApp: use WAHA API or WhatsApp Business API for session-based messaging.
- Telegram: use Bot API with inline keyboard buttons for acknowledgment actions.
- Email: use transactional email providers (Resend, SendGrid) with tracking pixels for open rates.
- SMS: use Twilio or Vonage for reliable delivery with delivery receipt callbacks.
- Slack/Discord: use webhook URLs for channel-targeted notifications.

### Best Practices

- Respect user notification preferences and quiet hours; never override opt-outs.
- Use idempotent reminder creation to prevent duplicate sends on retry.
- Log all sent reminders with channel, status, and timestamp for audit trails.
- Review the verification checklist after applying this skill.
- Document channel-specific formatting quirks (e.g., MarkdownV2 escaping for Telegram).

### Troubleshooting

- If reminders are not delivered, verify the channel API credentials are not expired.
- If duplicates are sent, check for missing idempotency keys in the reminder creation logic.
- For timezone mismatches, confirm the recipient's timezone is stored as IANA format (e.g., `Asia/Jakarta`).
- If output quality is low, provide more context about the target audience and channels.
- For rate-limited channels (e.g., WhatsApp Business), batch sends with configurable delays between messages.

## Overview

> Section content — see SKILL.md body for full details.
