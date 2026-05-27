---
name: nocode-orchestrator
description: Build and manage automations across Make.com, n8n, Zapier, and Pipedream — onboarding, support tickets, content approval, invoice processing
---

## Overview

Design, build, and manage business process automations using no-code/low-code platforms. Maps manual processes to automated workflows, selects the right platform for each use case, and deploys production-grade automations that businesses pay $2K-$10K per workflow for. A sellable service with low build effort and high leverage across all domains.

## Required Tools

- Make.com account (best for complex multi-step workflows)
- n8n instance (self-hosted, best for cost-sensitive clients)
- Zapier account (best for simple integrations, largest app ecosystem)
- Pipedream account (best for code-in-the-middle workflows)
- Node.js/Python for custom API connectors
- `curl` for API testing and webhook debugging

## Capabilities

- Map manual business processes to automated workflows
- Select optimal platform based on complexity, cost, and integration needs
- Build multi-step workflows with branching, error handling, and retries
- Deploy and monitor workflows in production
- Optimize costs by routing simple tasks to cheaper platforms
- Create reusable workflow templates for common business patterns
- Debug failing workflows with structured logging

## When to Use

- "Automate our customer onboarding process"
- "When a support ticket comes in, triage it and assign to the right person"
- "Process invoices automatically when they arrive by email"
- "Sync data between our CRM, email tool, and project management"
- "Build a content approval workflow for our team"
- Client says: "We do this manually every day, it takes 2 hours"

## Pseudo Code

### Process Mapping

```markdown
## Process: Customer Onboarding
Trigger: New customer signs up (Stripe webhook)

Steps:
1. Create customer record in CRM (HubSpot)
2. Send welcome email with setup guide
3. Create onboarding project in PM tool (Linear/Asana)
4. Add to customer Slack channel
5. Schedule Day 3 check-in email
6. Schedule Day 7 follow-up task
7. If enterprise: assign account manager

Error handling:
- CRM API down → retry 3x, then queue for manual
- Email fails → retry, fallback to SMS
- Slack channel exists → skip creation, just add member
```

### Platform Selection

```python
def select_platform(process):
    """Choose optimal platform based on process characteristics."""
    criteria = {
        'step_count': len(process['steps']),
        'has_custom_logic': any(s.get('type') == 'code' for s in process['steps']),
        'integration_count': len(set(s['app'] for s in process['steps'])),
        'runs_per_month': process['frequency'] * 30,
        'budget': process.get('budget', 'medium'),
    }

    # Decision matrix
    if criteria['has_custom_logic'] and criteria['step_count'] > 10:
        return 'pipedream'  # Code flexibility for complex workflows
    elif criteria['budget'] == 'low' and criteria['runs_per_month'] > 10000:
        return 'n8n'  # Self-hosted, no per-run cost
    elif criteria['step_count'] <= 5 and criteria['integration_count'] <= 3:
        return 'zapier'  # Simple, fast to build
    else:
        return 'make'  # Best balance for complex multi-step
```

### Make.com Workflow Build

```json
{
  "name": "Customer Onboarding",
  "modules": [
    {
      "id": 1,
      "app": "webhook",
      "action": "custom-webhook",
      "trigger": true,
      "config": {
        "url": "https://hook.make.com/abc123",
        "method": "POST"
      }
    },
    {
      "id": 2,
      "app": "hubspot",
      "action": "create-contact",
      "config": {
        "email": "{{1.body.email}}",
        "firstname": "{{1.body.name}}",
        "lifecyclestage": "customer"
      }
    },
    {
      "id": 3,
      "app": "gmail",
      "action": "send-email",
      "config": {
        "to": "{{1.body.email}}",
        "subject": "Welcome aboard!",
        "body": "{{templates.welcome_email}}"
      }
    },
    {
      "id": 4,
      "app": "slack",
      "action": "add-to-channel",
      "config": {
        "channel": "#customers",
        "email": "{{1.body.email}}"
      },
      "error_handler": {
        "type": "continue",
        "condition": "already_in_channel"
      }
    },
    {
      "id": 5,
      "app": "router",
      "condition": "{{1.body.plan}} == 'enterprise'",
      "routes": [
        {"target": 6, "label": "Enterprise path"},
        {"target": 7, "label": "Standard path"}
      ]
    },
    {
      "id": 6,
      "app": "asana",
      "action": "create-task",
      "config": {
        "name": "Enterprise onboarding: {{1.body.company}}",
        "assignee": "account_manager",
        "due_date": "+7d"
      }
    }
  ]
}
```

### n8n Self-Hosted Setup

```bash
# Deploy n8n with Docker
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=secure_password \
  n8nio/n8n

# Import workflow via API
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

### Pipedream Code Step

```javascript
// Pipedream Node.js step — custom logic in the middle of a workflow
export default defineComponent({
  async run({ steps, $ }) {
    const customer = steps.trigger.event.body;

    // Custom business logic
    const tier = customer.mrr > 1000 ? 'enterprise' :
                 customer.mrr > 100 ? 'growth' : 'starter';

    // Enrich with external data
    const companyInfo = await fetch(
      `https://api.clearbit.com/v2/companies/find?domain=${customer.domain}`,
      { headers: { Authorization: `Bearer ${process.env.CLEARBIT_KEY}` } }
    ).then(r => r.json());

    return {
      ...customer,
      tier,
      company_size: companyInfo.metrics.employees,
      industry: companyInfo.category.industry,
    };
  },
});
```

### Cost Optimization

```python
def optimize_costs(workflows):
    """Route workflows to cheapest viable platform."""
    costs = {
        'zapier': {'per_run': 0.025, 'included': 750},
        'make': {'per_run': 0.004, 'included': 10000},
        'n8n': {'per_run': 0, 'monthly_hosting': 20},
        'pipedream': {'per_run': 0.002, 'included': 100000},
    }

    for wf in workflows:
        monthly_runs = wf['frequency'] * 30
        best = min(costs.items(), key=lambda x:
            max(0, monthly_runs - x[1].get('included', 0)) * x[1].get('per_run', 0)
            + x[1].get('monthly_hosting', 0)
        )
        wf['recommended_platform'] = best[0]
    return workflows
```

### Monitoring Dashboard

```python
def check_workflow_health(platform, workflow_id):
    """Monitor workflow execution status."""
    if platform == 'make':
        resp = httpx.get(
            f"https://api.make.com/v2/scenarios/{workflow_id}/executions",
            headers={"Authorization": f"Token {MAKE_API_KEY}"},
            params={"limit": 100}
        )
        executions = resp.json()['executions']
        failed = [e for e in executions if e['status'] == 'error']
        return {
            'total': len(executions),
            'failed': len(failed),
            'success_rate': (len(executions) - len(failed)) / len(executions) * 100,
            'last_error': failed[0] if failed else None,
        }
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| Webhook timeout | Upstream service slow | Increase timeout, add retry with backoff |
| API rate limit | Too many calls | Batch requests, add delays between steps |
| Auth token expired | OAuth refresh failed | Re-authenticate, alert user |
| Step timeout | Complex logic too slow | Split into sub-workflows, optimize code steps |
| Duplicate execution | Webhook fired twice | Add idempotency key, deduplicate in first step |
| Platform outage | Make/Zapier down | Queue triggers, replay on recovery |

## Common Patterns

- **Fan-out/fan-in**: Trigger N parallel steps, wait for all to complete, merge results
- **Error boundary**: Wrap risky steps in error handlers, continue on failure
- **Idempotency**: Use unique IDs to prevent duplicate processing on webhook retries
- **Rate limiting**: Add deliberate delays between API calls to respect limits
- **Dead letter queue**: Failed executions go to a review queue instead of dropping
- **Template library**: Build reusable workflow templates for common patterns (onboarding, support triage, invoice processing)
