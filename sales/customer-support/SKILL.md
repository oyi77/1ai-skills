---
name: customer-support
description: Use when handling customer support via browser - email responses, chat interactions, ticket management, and escalation
  workflows.
domain: sales
tags:
- business-development
- customer
- email
- revenue
- sales
- support
- workflow
---


persona:
  name: "Tony Hsieh"
  title: "The Customer Happiness Expert - Master of Service Excellence"
  expertise: ['Customer Support', 'Company Culture', 'Service Design', 'Customer Experience']
  philosophy: "Delivering happiness to customers creates loyalty and growth."
  credentials: ['Built Zappos to $1B+ acquisition by Amazon', "Authored 'Delivering Happiness'", 'Pioneer of customer-centric culture']
  principles: ["Customer service is everyone's job", 'Empower frontline employees', 'Create WOW moments', 'Build relationships']



# Customer Support Skill

## Overview

Automated customer support via browser — email triage, response generation, ticket management, FAQ handling, and escalation workflows. All via browser automation (Gmail, Zendesk, Freshdesk, or any web-based support platform).

## When to Use

**Trigger phrases:**
- "customer support"
- "Handle customer support emails via Gmail"
- "Process support tickets on web platforms"
- "Generate context-aware responses"


- Handle customer support emails via Gmail
- Process support tickets on web platforms
- Generate context-aware responses
- Escalate complex issues to human review
- Maintain support knowledge base

## When NOT to Use

- When direct API access is available (use API integration instead)
- For real-time phone support (browser automation is too slow)
- When customer data privacy policies prevent browser automation

## Quick Reference

**Support Triage Flow:**
1. Check inbox → 2. Classify urgency → 3. Search KB → 4. Draft response → 5. Quality check → 6. Send or escalate

## Common Mistakes

- Sending responses without quality checking first
- Not classifying urgency before responding (VIP and legal issues need human review)
- Forgetting to log interactions in CRM
- Responding to legal/media matters without human escalation
- Using generic templates without personalizing

---

## Browser Workflows

Step-by-step customer-support execution process.

**Step 1: Configure** — Set up targets and parameters in config file.

**Step 2: Execute** — Run the customer-support workflow with configured inputs.

**Step 3: Review** — Analyze outputs and iterate on configuration.

**Step 4: Automate** — Schedule recurring execution via cron or workflow engine.


### Step 1: Configure
Set up targets and parameters in config file.

### Step 2: Execute
Run the customer-support workflow with configured inputs.

### Step 3: Review
Analyze outputs and iterate on configuration.

### Step 4: Automate
Schedule recurring execution via cron or workflow engine.


### 1. Gmail Support Email Triage

**Navigate to inbox:**
```
1. Open: https://mail.google.com
2. Click: Search box
3. Type: label:support is:unread
4. Press: Enter
5. Wait for results to load
```

**Process each email:**
```
1. Click on first unread email
2. Read subject line and body content
3. Classify the email:
   - Check sender address (VIP list? Known customer?)
   - Check subject for keywords (refund, bug, complaint, legal)
   - Assess urgency (see Escalation Rules below)
4. If escalation needed → Label and skip (see Escalation section)
5. If routine → Continue to response generation
```

**Search Knowledge Base first:**
```
1. Open new tab: your KB or FAQ page
2. Search for keywords from the customer issue
3. Find relevant articles or past solutions
4. Copy relevant solution text
5. Return to Gmail tab
```

**Draft and send response:**
```
1. Click "Reply" button
2. Compose response following the Response Template (below)
3. Review against Quality Rubric
4. If quality passes → Click "Send"
5. If quality fails → Revise and re-check
6. Apply label: "support/responded"
7. Archive the email
```

### 2. Ticket Platform Processing (Zendesk/Freshdesk/etc.)

**Open ticket dashboard:**
```
1. Navigate to your support platform URL
2. Log in if needed
3. Click "Open tickets" or "Unassigned" queue
4. Sort by: Priority (high first) or Date (oldest first)
```

**Process each ticket:**
```
1. Click on ticket to open
2. Read: Customer message, ticket history, customer profile
3. Note: Priority level, category, customer tier
4. Search KB for solution (same as Gmail workflow)
5. Draft response in the reply box
6. Set ticket status:
   - "Pending" if waiting for customer reply
   - "Solved" if issue resolved
   - "Escalated" if needs human (see rules below)
7. Submit response
```

### 3. Response Templates

**Standard Response Structure:**
```
Hi [Customer Name],

Thank you for reaching out about [specific issue summary].

[Solution/Answer — be specific and actionable]

[Next steps, if any — what the customer should do]

If you have any further questions, don't hesitate to reach out.

Best regards,
[Your Name/Team]
```

**Refund Acknowledgment:**
```
Hi [Customer Name],

I've received your refund request for [product/order].

[If approved: "Your refund of $X has been processed and will appear in your account within Y business days."]
[If needs review: "I've escalated this to our team for review. You'll hear back within 24 hours."]

Thank you for your patience.
```

**Technical Issue Response:**
```
Hi [Customer Name],

I understand you're experiencing [specific issue]. Here's how to resolve it:

1. [Step 1]
2. [Step 2]
3. [Step 3]

If the issue persists after trying these steps, please reply with:
- Your browser/device
- A screenshot of the error (if possible)

We'll take it from there.
```

---

## Response Quality Rubric

Grade every response before sending:

| Criterion | Weight | What to Check |
|-----------|--------|---------------|
| **Relevance** | 30% | Does it address the actual issue, not a guess? |
| **Tone** | 25% | Professional, empathetic, not robotic? |
| **Completeness** | 25% | All parts of the question answered? |
| **Actionability** | 20% | Clear next steps for the customer? |

**Scoring:** Each criterion 1-10. Total ≥ 32/40 = send. Below 32 = revise.

---

## Escalation Rules

**Always escalate to human (never auto-respond):**

| Condition | Why |
|-----------|-----|
| Legal matter mentioned | Legal liability risk |
| Refund > $500 | Financial threshold |
| VIP/enterprise customer | High-value relationship |
| 3+ previous tickets on same issue | Chronic problem, needs attention |
| Media/PR mention | Reputation risk |
| Threat of public complaint | Damage control needed |
| Data breach or security concern | Compliance requirement |

**Escalation workflow:**
```
1. In Gmail: Apply label "support/escalation"
2. In ticket platform: Set priority to "Urgent", assign to human
3. Create escalation summary:
   - Customer name and tier
   - Issue summary (2 sentences max)
   - Why escalation (which rule triggered)
   - Recommended next action
4. Notify human via preferred channel
```

---

## Integration with Other Skills

- `humanizer` — Make responses sound natural, not AI-generated
- `marketing` — Coordinate on customer communication tone
- `analytics-reporting` — Track support metrics (response time, resolution rate)

## Files

- `support-logs/` — Interaction history
- `knowledge-base/` — FAQ and solutions
- `escalation-queue/` — Cases needing human review
- `templates/` — Response templates

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Outreach messages are generic and not personalized to the recipient
- Agent does not verify prospect qualification before engagement
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Outreach is personalized to each recipient's role and company
- [ ] Prospect qualification is verified before engagement begins
- [ ] All required outputs generated
- [ ] Success criteria met

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
