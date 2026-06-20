---
name: customer-success
description: Automated customer onboarding, health scoring, churn prediction, proactive outreach, and support ticket resolution
domain: operations
tags:
- business-ops
- customer
- management
- operations
- success
---

## Overview

Automate the entire customer lifecycle from onboarding to retention. Monitor customer health through behavioral signals, predict churn before it happens, trigger proactive interventions, and resolve support tickets with AI. For recurring revenue businesses, retention is 5-7x cheaper than acquisition — this skill protects and grows existing revenue.

## Required Tools

- **CRM**: HubSpot API, Salesforce API, or Pipedrive API
- **Communication**: SendGrid (email), Twilio (SMS), Intercom/Zendesk (support)
- **Analytics**: Mixpanel, Amplitude, or custom event tracking via webhooks
- **Database**: PostgreSQL or Supabase for health scores and event storage
- **Scheduling**: Cal.com or Calendly API for intervention calls
- **Node.js 18+** for automation scripts

## Capabilities

- Automate multi-step onboarding sequences
- Calculate real-time customer health scores from behavioral data
- Predict churn risk using engagement signals
- Trigger proactive outreach when health drops
- Route and resolve support tickets with AI
- Escalate to human agents with full context
- Generate retention reports and cohort analysis
- Identify expansion revenue opportunities (upsells, cross-sells)

## When to Use

- SaaS product with recurring subscriptions
- Customer onboarding takes >5 minutes of manual work
- Churn rate is above 5% monthly
- Support tickets pile up without prioritization
- Need to identify at-risk customers before they leave
- Want to scale customer success without hiring

## When NOT to Use

- Product has no recurring revenue model
- Customer base is too small (<10 customers) for automation
- Issue is product quality, not customer success process
- You need sales automation (use sales tools)
- Task is about customer support tickets only (use support tools)
- You don't have customer data to work with

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Automated Onboarding Sequence

```javascript
const ONBOARDING_STEPS = [
  {
    trigger: "signup",
    delay: "0m",
    action: "send_email",
    template: "welcome",
    content: "Welcome! Here's your login and quick-start guide."
  },
  {
    trigger: "signup",
    delay: "5m",
    action: "send_email",
    template: "setup_guide",
    content: "3 steps to get started: 1) Connect your data 2) Create first report 3) Invite team"
  },
  {
    trigger: "day_1",
    action: "check_progress",
    condition: "no_login_since_signup",
    if_true: {
      action: "send_email",
      template: "nudge",
      content: "Need help getting started? Book a 15-min walkthrough."
    }
  },
  {
    trigger: "day_3",
    action: "check_progress",
    condition: "no_first_action",
    if_true: {
      action: "send_sms",
      content: "Quick question — what's blocking you from getting started?"
    }
  },
  {
    trigger: "day_7",
    action: "check_health_score",
    condition: "health_score < 40",
    if_true: {
      action: "create_task",
      assignee: "success_team",
      content: "Manual outreach needed — low engagement after 7 days"
    }
  }
];

// Process onboarding
async function processOnboarding(userId, event) {
  const steps = ONBOARDING_STEPS.filter(s => s.trigger === event);

  for (const step of steps) {
    if (step.condition) {
      const met = await checkCondition(userId, step.condition);
      if (!met) continue;
    }

    if (step.delay) {
      await scheduleAction(userId, step, step.delay);
    } else {
      await executeAction(userId, step);
    }
  }
}
```

### Health Score Calculation

```python
def calculate_health_score(customer):
    """
    Health score: 0-100, weighted by signal importance.
    """
    signals = {
        # Engagement (40% weight)
        "login_frequency": {
            "weight": 0.15,
            "score": min(customer.logins_last_30d / 20, 1.0) * 100
        },
        "feature_adoption": {
            "weight": 0.15,
            "score": (customer.features_used / customer.features_available) * 100
        },
        "session_duration": {
            "weight": 0.10,
            "score": min(customer.avg_session_min / 10, 1.0) * 100
        },

        # Value Realization (30% weight)
        "core_action_completed": {
            "weight": 0.20,
            "score": 100 if customer.core_action_done else 0
        },
        "time_to_value": {
            "weight": 0.10,
            "score": max(0, 100 - (customer.days_to_first_value * 10))
        },

        # Support Signals (15% weight)
        "support_tickets": {
            "weight": 0.10,
            "score": max(0, 100 - (customer.open_tickets * 20))
        },
        "nps_score": {
            "weight": 0.05,
            "score": customer.nps * 10  # NPS 0-10 → 0-100
        },

        # Billing Health (15% weight)
        "payment_health": {
            "weight": 0.10,
            "score": 0 if customer.payment_failed else 100
        },
        "plan_usage": {
            "weight": 0.05,
            "score": min(customer.usage_pct / 0.8, 1.0) * 100
        }
    }

    total = sum(s["weight"] * s["score"] for s in signals.values())
    return round(total, 1)

# Health categories
# 80-100: Healthy (green) — upsell opportunity
# 60-79:  At risk (yellow) — monitor closely
# 40-59:  Warning (orange) — proactive outreach
# 0-39:   Critical (red) — immediate intervention
```

### Churn Prediction

```python
CHURN_SIGNALS = {
    "login_decline": {
        "threshold": 0.5,  # 50% drop from baseline
        "weight": 0.25,
        "lookback_days": 14
    },
    "feature_abandonment": {
        "threshold": 0.3,  # Stopped using 30% of adopted features
        "weight": 0.20,
        "lookback_days": 30
    },
    "support_escalation": {
        "threshold": 3,    # 3+ unresolved tickets
        "weight": 0.15,
        "lookback_days": 30
    },
    "billing_issue": {
        "threshold": 1,    # Any payment failure
        "weight": 0.20,
        "lookback_days": 7
    },
    "no_core_action": {
        "threshold": 14,   # No core action in 14 days
        "weight": 0.20,
        "lookback_days": 14
    }
}

def predict_churn_risk(customer):
    risk_score = 0
    triggered_signals = []

    for signal, config in CHURN_SIGNALS.items():
        value = get_signal_value(customer, signal, config["lookback_days"])
        if exceeds_threshold(value, config["threshold"]):
            risk_score += config["weight"]
            triggered_signals.append(signal)

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": "critical" if risk_score > 0.7 else "high" if risk_score > 0.4 else "medium",
        "signals": triggered_signals
    }
```

### Proactive Intervention

```javascript
async function handleChurnRisk(customer, risk) {
  const interventions = {
    medium: [
      { action: "send_email", template: "check_in", delay: "0" },
      { action: "offer_training", type: "webinar_invite" }
    ],
    high: [
      { action: "send_email", template: "personal_outreach", from: "success_manager" },
      { action: "schedule_call", duration: "15min", type: "health_check" },
      { action: "offer_discount", percent: 10, duration: "3months" }
    ],
    critical: [
      { action: "alert_team", channel: "slack", urgency: "high" },
      { action: "schedule_call", duration: "30min", type: "retention_call", exec: true },
      { action: "offer_concession", type: "custom", notes: "Review account history before call" }
    ]
  };

  for (const intervention of interventions[risk.risk_level]) {
    await executeIntervention(customer, intervention);
  }

  // Log intervention for tracking
  await logIntervention(customer.id, risk, interventions[risk.risk_level]);
}
```

### Support Ticket Routing

```javascript
async function routeTicket(ticket) {
  // Step 1: Classify ticket
  const classification = await classifyTicket(ticket.content);
  // { category: "billing", priority: "high", sentiment: "frustrated" }

  // Step 2: Try AI resolution for common issues
  if (classification.category in AI_RESOLVABLE) {
    const resolution = await generateResolution(ticket, classification);
    if (resolution.confidence > 0.85) {
      await sendResolution(ticket, resolution);
      await logAIResolution(ticket, resolution);
      return;
    }
  }

  // Step 3: Route to appropriate human agent
  const agent = await findBestAgent(classification);
  await assignTicket(ticket, agent, {
    context: {
      customer_health: await getHealthScore(ticket.customer_id),
      recent_activity: await getRecentActivity(ticket.customer_id, "7d"),
      previous_tickets: await getTicketHistory(ticket.customer_id),
      suggested_resolution: resolution?.text || null
    }
  });
}
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `HEALTH_SCORE_STALE` | Data pipeline delayed | Use last known score, flag for refresh |
| `EMAIL_BOUNCE` | Invalid email address | Update contact, try alternative channel |
| `INTERVENTION_NO_RESPONSE` | Customer ignored outreach | Escalate to next intervention tier |
| `TICKET_MISROUTE` | AI classified incorrectly | Allow manual re-route, retrain classifier |
| `CRM_SYNC_FAIL` | API rate limit or timeout | Queue and retry with exponential backoff |
| `FALSE_POSITIVE_CHURN` | Healthy customer flagged | Review signals, adjust thresholds |

## Common Patterns

Reusable patterns that appear frequently when applying this skill.


### Expansion Revenue Detection
- Monitor usage approaching plan limits
- Identify teams that need more seats
- Track feature requests that map to higher tiers
- Trigger: "You're using 80% of your storage. Upgrade to unlock unlimited."

### Cohort Retention Analysis
```sql
-- Monthly cohort retention
SELECT
  DATE_TRUNC('month', signup_date) AS cohort,
  COUNT(DISTINCT customer_id) AS cohort_size,
  COUNT(DISTINCT CASE WHEN active_month = 1 THEN customer_id END) AS month_1,
  COUNT(DISTINCT CASE WHEN active_month = 3 THEN customer_id END) AS month_3,
  COUNT(DISTINCT CASE WHEN active_month = 6 THEN customer_id END) AS month_6
FROM customer_activity
GROUP BY 1
ORDER BY 1 DESC;
```

### Intervention Escalation Ladder
1. Automated email (day 0)
2. Personal email from success manager (day 2)
3. SMS check-in (day 4)
4. Phone call scheduled (day 7)
5. Executive outreach + concession offer (day 14)
6. Win-back campaign if churned (day 30)

## Red Flags

- Ignoring customer feedback
- Not tracking customer health scores
- Missing follow-up on issues
- Not personalizing customer interactions
- Ignoring churn indicators

## Verification

- [ ] Customer feedback is collected
- [ ] Customer health is tracked
- [ ] Issues are followed up
- [ ] Interactions are personalized
- [ ] Churn indicators are monitored