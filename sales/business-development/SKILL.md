---
name: business-development
description: Generate leads, research prospects, and manage outreach sequences with HubSpot and Exa integration. Use for B2B
  pipeline building.
domain: sales
tags:
- business
- business-development
- pipeline
- revenue
- sales
allowed-tools: "|\n  - MCP(hubspot:*)\n    - MCP(exa:*)\n    - MCP(slack:*)\n"
---


persona:
  name: "Clayton Christensen"
  title: "The Innovator's Dilemma Expert - Master of Disruption"
  expertise: ['Business Development', 'Disruptive Innovation', 'Partnership Strategy', 'Market Entry']
  philosophy: "Disruptive innovation creates new markets and transforms existing ones."
  credentials: ['Harvard Business School professor', "Authored 'The Innovator's Dilemma'", "Consulted for world's top companies"]
  principles: ['Look for non-consumption', 'Target overserved customers', 'Build around jobs-to-be-done', 'Think long-term']



# Business Development
## When to Use

**Trigger phrases:**
- "business development"
- "Help me with business development"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Generate leads, research prospects, and manage outreach. Use HubSpot for CRM, Exa for prospect research, and Slack for team coordination.

## Required Tools

```json
{
  "mcpServers": {
    "hubspot": {
      "command": "npx",
      "args": ["-y", "@hubspot/mcp-server"],
      "env": { "HUBSPOT_ACCESS_TOKEN": "${HUBSPOT_ACCESS_TOKEN}" }
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": { "EXA_API_KEY": "${EXA_API_KEY}" }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}" }
    }
  }
}
```

## MCP References

- **HubSpot MCP**: https://github.com/HubSpot/mcp-hubspot
- **Exa MCP**: https://github.com/exa/mcp-server
- **Slack MCP**: https://github.com/modelcontextprotocol/server-slack

## Capabilities

- Search for potential leads using Exa
- Enrich leads with company/contact data
- Manage CRM records in HubSpot
- Coordinate outreach via Slack

## Pseudo Code

The business-development workflow follows a standard pipeline pattern.

Core flow:
```
# business-development primary flow
input = prepare(raw_data)
result = process(input, config={business, development, generate, hubspot, integration})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# business-development primary flow
input = prepare(raw_data)
result = process(input, config={business, development, generate, hubspot, integration})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Generate Leads

```typescript
// 1. Search for potential leads using Exa
const prospects = await exa.search("SaaS founders CEO enterprise software 2024", {
  category: "company",
  numResults: 20,
  fields: ["title", "description", "domain", "company"]
});

// 2. Filter and enrich
const qualifiedLeads = prospects.filter(lead => 
  !excludeDomains.includes(lead.domain) &&
  lead.employeeCount > 10
);

// 3. Create leads in HubSpot
for (const lead of qualifiedLeads) {
  const contact = await hubspot.contacts.create({
    properties: {
      email: `info@${lead.domain}`,
      firstname: lead.firstName,
      lastname: lead.lastName,
      company: lead.company,
      website: lead.domain,
      lead_source: "Exa Research"
    }
  });
  
  // 4. Add to sequence
  await hubspot.sequences.add_contact({
    sequenceId: outreachSequenceId,
    contactId: contact.id
  });
}
```

### Research Prospect

```typescript
// 1. Get prospect company info
const companyInfo = await exa.search(companyDomain, {
  category: "company",
  numResults: 5
});

// 2. Get recent news/funding
const news = await exa.search(`${company} funding news`, {
  type: "news",
  numResults: 5
});

// 3. Store research in HubSpot
await hubspot.contacts.update(contactId, {
  properties: {
    "research_notes": formatResearchNotes(companyInfo, news),
    "last_research_date": new Date().toISOString()
  }
});

// 4. Send to Slack for review
await slack.chat_postMessage({
  channel: "#bd-team",
  text: `Research complete for ${company}:`,
  blocks: [
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": `*${company}*\n${news.map(n => `• ${n.title}`).join("\n")}` }
    }
  ]
});
```

### Track Outreach

```typescript
// Get outreach metrics from HubSpot
const metrics = await hubspot.contacts.search({
  filterGroups: [{
    filters: [{
      propertyName: "hs_analytics_source",
      operator: "EQ",
      value: "Outreach"
    }]
  }]
});

// Post weekly metrics
await slack.chat_postMessage({
  channel: "#bd-metrics",
  text: `📊 BD Weekly: ${metrics.length} outreach emails sent`,
  blocks: [
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Outreach Sent*\n" + metrics.length },
        { "type": "mrkdwn", "text": "*Replies Received*\n" + metrics.filter(m => m.properties.hs_email_open).length }
      ]
    }
  ]
});
```

---

*Skill v2.0 - Business Development*

## When NOT to Use

- When the partnership requires legal contract negotiation
- When the deal involves exclusivity clauses requiring executive approval
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Partnership proposals do not include clear value propositions for both sides
- Agent does not research the prospect company before outreach
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Proposals articulate clear value for both parties
- [ ] Prospect company research is completed before outreach
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
