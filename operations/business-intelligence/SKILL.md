---
name: business-intelligence
description: Define and track KPIs across revenue, marketing, and content performance with weekly business reviews and data-driven
  decisions. Use when working with business intelligence.
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- business
- business-ops
- intelligence
- management
- operations
version: 1.0.0
---
# Business Intelligence

## When to Use
**Trigger phrases:**
- "business intelligence"
- "Define and track KPIs across revenue, marketing, and content performance with we"


- Generating business reports and dashboards
- Analyzing business metrics and KPIs
- Tracking business performance over time
- Creating data visualizations
- Automating reporting workflows


## When NOT to Use

- For processes that change daily (too much overhead)
- When the team is too small to benefit from SOPs
- For one-time events that will not repeat


Business Intelligence (BI) is the practice of transforming raw operational, financial, and engagement data into actionable insights that drive strategic decisions. For solo founders and small teams, BI provides the visibility needed to identify growth levers, optimize spending, and surface problems before they compound. Effective BI combines disciplined KPI definition, automated data collection, regular review cadences, and visual dashboards that make performance patterns immediately obvious.

The BI lifecycle spans five stages: **Define** which metrics matter (leading indicators for future outcomes, lagging indicators for past results), **Collect** data from disparate sources (payment processors, ad platforms, analytics tools, CRM), **Analyze** for trends, anomalies, and correlations, **Report** through dashboards and scheduled summaries, and **Act** by translating insights into concrete business decisions. Skipping any stage — especially the last — turns BI into a reporting exercise with no ROI.

A key principle is distinguishing **vanity metrics** from **actionable metrics**. Page views and social followers feel good but do not drive decisions. Conversion rates, customer acquisition cost (CAC), lifetime value (LTV), unit economics, and churn rate directly inform where to invest time and money. Every KPI in your dashboard should have a clear "if this number moves, I will do X" response.

For small teams, the goal is not enterprise-grade data lakes but a reliable, low-maintenance stack: a spreadsheet or lightweight BI tool connected to 3-5 source systems, refreshed daily or weekly, reviewed on a fixed cadence. Overbuilding data infrastructure before establishing decision-making discipline is the most common failure mode.

## Workflow

```python
# Example: SOP execution tracker
def execute_sop(sop_name: str, steps: list[str]) -> dict:
    results = []
    for i, step in enumerate(steps, 1):
        try:
            result = execute_step(step)
            results.append({"step": i, "status": "ok", "result": result})
        except Exception as e:
            results.append({"step": i, "status": "error", "error": str(e)})
            break
    return {"sop": sop_name, "steps": results}
```

1. **Assess** — Evaluate current state and identify gaps
2. **Design** — Plan improved processes and workflows
3. **Implement** — Roll out changes with team alignment
4. **Measure** — Track operational KPIs
5. **Iterate** — Continuous improvement based on data

## SOP Template

- **Purpose** — Why this process exists
- **Scope** — Who and what it covers
- **Procedure** — Step-by-step instructions
- **Escalation** — When and how to escalate
- **Review** — Schedule for periodic updates

## Key Metrics

- Process completion time
- Error/rework rate
- Team satisfaction scores
- Cost per operation
- SLA compliance rate

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings

## Common Pitfalls

- **Tracking every metric instead of the few that matter.** A dashboard with 30+ KPIs dilutes focus and leads to analysis paralysis. Limit to 5-7 leading indicators and 3-5 lagging indicators per business area. Every KPI passes the test: "If this moves, I take a specific action."
- **Building dashboards nobody uses.** Beautiful charts that are never reviewed at decision time are sunk cost. Design each dashboard around a weekly review meeting agenda, not around data availability. If a chart doesn't change a decision, remove it.
- **Relying on single data sources without cross-validation.** Ad platform reporting overattributes conversions, payment processor data misses refunds, analytics tools sample traffic. Reconcile at least two independent sources for revenue and acquisition KPIs before reporting them as truth.
- **Treating BI as a one-time setup rather than a cadence.** Building a dashboard is useless without a recurring review ritual. The insight comes from watching trends week-over-week, not from staring at a static snapshot. Schedule the review before building the report.
- **Confusing data collection with decision-making.** Data without a decision framework is noise. Before collecting any metric, document: "If this number drops below X, we will do Y." Without that commitment, BI generates reports that feel productive but change nothing.

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| BI Dashboard as a Service | 1-4 weeks | Build and maintain custom dashboards for 3-5 local businesses using Google Sheets + Looker Studio or Metabase. Charge a monthly retainer for data integration, refresh, and a monthly review call. Recurring revenue with high stickiness once dashboards are embedded in client operations. |
| Paid BI Audit & Setup | 2-5 days per client | Offer a structured BI audit: map existing data sources, define 10 core KPIs, set up automated reporting (Stripe + Google Analytics + social platforms into a weekly email). One-off fee plus optional monthly maintenance. Appeal to funded startups that outgrew spreadsheets but cannot afford a data analyst. |
| Data-Driven Consulting Retainer | Monthly | Position as a fractional BI lead: review KPIs weekly, produce a monthly executive summary deck, recommend operational changes based on data trends. Clients pay for the decision framework, not the dashboard. Best paired with a specific vertical (e-commerce, SaaS, content creators). |
| Analytics Template Products | 1-2 weeks to build | Create sellable template packs: e-commerce KPI tracker (Stripe + Shopify), content creator analytics dashboard, SaaS unit economics model. Sell on Gumroad or as Notion/Google Sheets templates. Low-touch, scaleable. Update quarterly as platforms change APIs. |
| Automated Weekly Report Subscription | 1-3 days per client | Use Python scripts or Zapier/n8n to pull data from 3-5 sources and email a formatted weekly report with key KPI changes, trend arrows, and anomaly flags. Price as a monthly subscription. Low effort once automated, high retention. Ideal for agencies managing client reporting manually. |