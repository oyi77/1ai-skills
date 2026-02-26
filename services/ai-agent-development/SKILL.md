---
name: ai-agent-development
description: Build and sell custom AI agents as services or products. Create vertical-specific AI solutions for clients and generate $2K-$8K/month recurring revenue.
---

# AI Agent Development Skill

## Overview

Build custom AI agents for businesses and sell them as services or products. Create specialized agents for industries like legal, healthcare, real estate, finance, and more. This is one of the highest-margin AI services you can offer.

**Market**: $11.78B by 2026  
**Pricing**: $199-799/month per agent  
**Revenue Potential**: $2K-8K/month

---

## When to Use

- Client needs custom automation
- Repetitive tasks that AI can handle
- Industry-specific workflows
- Build once, sell multiple times
- Create recurring revenue

---

## When NOT to Use

- One-time projects (use fixed-price)
- Very small budgets (<$1K)
- Highly regulated without expertise
- Complex custom integrations

---

## Business Models

### 1. Agent-as-a-Service (Recurring)
```
Price: $199-799/month per client
Duration: Multi-month contracts
Upsell: Additional agents, features
Example: $500/mo × 10 clients = $5K MRR
```

### 2. Custom Development (One-time)
```
Price: $2,000-10,000 per agent
Scope: Full customization
Support: 30-90 days included
Upsell: Monthly maintenance
```

### 3. Vertical SaaS (Product)
```
Price: $49-199/month per user
Build: Industry-specific agent
Example: Legal agent, HR agent, etc.
```

---

## High-Demand Agent Types

### By Industry

| Industry | Agent Type | Price/mo |
|----------|------------|----------|
| Legal | Contract review, case research | $300-800 |
| Healthcare | Patient intake, scheduling | $400-1000 |
| Real Estate | Lead qualification, scheduling | $200-500 |
| Finance | Invoice processing, reporting | $300-700 |
| HR | Resume screening, onboarding | $200-400 |
| Sales | Outreach, follow-up | $300-600 |
| Support | FAQ, ticket routing | $200-500 |

### By Function

| Function | Agent Type | Price/mo |
|----------|------------|----------|
| Operations | Data entry, scheduling | $150-300 |
| Marketing | Content, social, SEO | $200-400 |
| Finance | Bookkeeping, invoicing | $250-500 |
| Sales | SDR, follow-up | $300-600 |
| Admin | Scheduling, email | $150-300 |

---

## Development Stack

### Core Tools
| Tool | Use | Price |
|------|-----|-------|
| Claude Code | Agent reasoning | $20/mo |
| OpenAI API | Language model | Usage |
| LangGraph | Agent workflows | Free |
| MCP | Tool integration | Free |
| n8n | Automation | Free/$50 |
| Railway | Deployment | $5-50/mo |

### Example Stack Cost: ~$100/month for 10 agents

---

## Development Process

### Phase 1: Discovery (1-2 days)
```
1. Understand client workflow
2. Identify automation opportunities
3. Define success metrics
4. Estimate development time
```

### Phase 2: Build (3-7 days)
```
1. Set up agent architecture
2. Implement tools/APIs
3. Add knowledge base
4. Test extensively
```

### Phase 3: Deploy (1-2 days)
```
1. Deploy to production
2. Integrate with client systems
3. Train client team
4. Document usage
```

### Phase 4: Support (Ongoing)
```
1. Monitor performance
2. Fix bugs
3. Add features
4. Upsell opportunities
```

---

## Code Example: Basic Agent

```python
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

# Define agent state
class AgentState(TypedDict):
    user_input: str
    context: dict
    action: str
    result: str

# Build agent graph
graph = StateGraph(AgentState)

graph.add_node("understand", understand_user)
graph.add_node("plan", plan_action)
graph.add_node("execute", execute_action)
graph.add_node("respond", respond_to_user)

graph.set_entry_point("understand")
graph.add_edge("understand", "plan")
graph.add_edge("plan", "execute")
graph.add_edge("execute", "respond")
graph.add_edge("respond", END)

# Compile and use
agent = graph.compile()

result = agent.invoke({
    "user_input": "Schedule meeting with John tomorrow at 2pm",
    "context": {"calendar": calendar}
})
```

---

## Tools & Integrations

### Knowledge Base
| Tool | Use | Price |
|------|-----|-------|
| Notion | Documentation | $10/mo |
| Confluence | Team wiki | Free |
| Pinecone | Vector DB | $60/mo |
| Chroma | Local vector | Free |

### APIs to Integrate
| API | Use | Price |
|-----|-----|-------|
| Google Calendar | Scheduling | Free |
| Slack | Notifications | Free |
| CRM (HubSpot) | Customer data | Free/$50 |
| Email (SendGrid) | Outbound | Free tier |

---

## Integration with 1ai-skills

### Revenue Model

```
Build Agent → Deploy → Monthly Retainer → Upsell Features
```

### Skill Synergies

| Skill | Use Case |
|-------|----------|
| voice-ai-agent | Build voice agents |
| ai-consulting | Find clients |
| automation | Connect tools |
| marketing | Showcase work |

---

## Pricing Guide

### Starter Agent ($199/mo)
- Single task automation
- Basic knowledge base
- Email support
- 100 API calls/day

### Professional Agent ($499/mo)
- Multi-task automation
- Advanced knowledge base
- Priority support
- Unlimited API calls
- Custom integrations

### Enterprise Agent ($999/mo)
- Full workflow automation
- Dedicated support
- SLA guarantee
- Custom development
- Training sessions

---

## Best Practices

### Do's
✅ Start with simple agents  
✅ Over-deliver on first project  
✅ Document everything  
✅ Build reusable components  
✅ Create case studies  
✅ Ask for referrals  

### Don'ts
❌ Don't underprice  
❌ Don't overpromise  
❌ Don't skip contracts  
❌ Don't ignore security  
❌ Don't forget backups  

---

## Scaling Tips

1. **Template agents** - Build once, customize for each client
2. **Self-service** - Let clients update knowledge base
3. **Monitoring** - Automate issue detection
4. **Upsell** - Offer additional agents/features

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Business models
  - Development process
  - Pricing strategies

---

## Related Skills

- [voice-ai-agent](/skills/voice-ai-agent) - Voice agent building
- [ai-consulting](/skills/ai-consulting) - Client acquisition
- [automation](/skills/automation) - Workflow building
