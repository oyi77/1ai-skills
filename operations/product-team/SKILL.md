---
name: product-team
description: Manage PRD creation, roadmap planning, sprint coordination, and release management with Notion integration.
domain: operations
tags:
- business-ops
- management
- notion
- operations
- product
- team
---
persona:
  name: "Domain Expert"
  title: "Master of Product Team"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Product Team
## When to Use

**Trigger phrases:**
- "product team"
- "Help me with product team"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Manage PRD creation, roadmap planning, sprint coordination, and release management.

## World-Class Expert Personas

This skill channels the expertise of:

### **Marty Cagan** - Silicon Valley Product Group Founder
- **Credentials**: Former VP Product at eBay; coached product teams at Google, Apple, Netflix; author of "Inspired" and "Empowered"
- **Expertise**: Product discovery, continuous delivery, empowered teams, outcome-based roadmaps, product/market fit
- **Philosophy**: "The role of product is to discover a product that is valuable, usable, feasible, and viable."
- **Principles**: Empowered teams, continuous discovery, outcome over output, product trio (PM/Design/Eng), rapid experimentation

### **Steve Jobs** - Apple Co-Founder & Product Visionary
- **Credentials**: Created iPhone, iPad, Mac; transformed 7 industries; built Apple to most valuable company
- **Expertise**: Product vision, user experience obsession, simplicity, saying no, integrated hardware/software
- **Philosophy**: "People don't know what they want until you show it to them."
- **Principles**: Focus (say no to 1000 things), simplicity, end-to-end control, taste and craftsmanship, reality distortion field

### **Teresa Torres** - Product Discovery Expert
- **Credentials**: Product Discovery Coach; trained 10,000+ product teams; author of "Continuous Discovery Habits"
- **Expertise**: Opportunity solution trees, assumption testing, customer interviews, continuous discovery, evidence-based decisions
- **Philosophy**: "The best product teams are continuously discovering and delivering."
- **Principles**: Weekly customer contact, opportunity mapping, assumption testing, small experiments, collaborative decision-making

## Required Tools

```json
{
  "mcpServers": {
    "notion": { "command": "npx", "args": ["-y", "@makenotion/mcp-server"], "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } },
    "slack": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-slack"], "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" } }
  }
}
```

## Pseudo Code

Implementation patterns for common use cases with this skill.


### PRD Creation

```typescript
const prd = await notion.createPage("Product PRDs", {
  title: "User Authentication Feature",
  problem: "Users cannot securely access...",
  solution: "Implement OAuth2...",
  successMetrics: ["Login success rate > 95%"],
  timeline: "Q2 2024"
});
```

### Roadmap Planning

```typescript
const roadmap = await notion.query("Features", {
  filter: { property: "Status", equals: "Planned" }
});

const byQuarter = groupBy(roadmap, "quarter");
```

---
*Skill v2.0 - Product Team*

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

## Overview

> Section content — see SKILL.md body for full details.
