---
name: finance-ops
description: Run AI-powered CFO analysis for cost detection, financial modeling, scenario planning, and operational efficiency
  optimization. Use when working with finance ops.
domain: operations
tags:
- business-ops
- finance
- management
- operations
- ops
---
# Finance Ops

## When to Use

**Trigger phrases:**
- "finance ops"
- "Help me with finance ops"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

briefing = generate_cfo_briefing(
    company_data=load_company_financials(),
    period="2025-04"
)

# Key sections:
# 1. Executive Summary
# 2. Cash Position & Runway
# 3. Unit Economics Update
# 4. Cost Analysis & Optimization
# 5. Risk Assessment
# 6. Board Metrics

print(f"Cash Runway: {briefing.cash_runway.months} months")
print(f"LTV/CAC: {briefing.unit_economics.ltv_cac_ratio}")
print(f"Optimization Opportunities: ${briefing.cost_opportunities.total_annual_value}")
```

### Example 2: Scenario Planning

```python
# Build 3-year financial model
model = FinancialModel(
    assumptions={
        "revenue": {
            "starting_arr": 5000000,
            "growth_rate": 0.75,
            "net_retention": 1.15
        },
        "costs": {
            "gross_margin": 0.75,
            "sales_marketing": 0.40,  # % of revenue
            "r_and_d": 0.25,
            "g_and_a": 0.15
        }
    }
)

# Run scenarios
scenarios = model.scenario_analysis({
    "base_case": base_assumptions,
    "upside_case": {**base_assumptions, "growth_rate": 1.00},
    "downside_case": {**base_assumptions, "growth_rate": 0.50, "churn": 0.05},
    "stress_test": {**base_assumptions, "growth_rate": 0.25, "churn": 0.08}
})

# Compare scenarios
for name, result in scenarios.items():
    print(f"{name}: {result.year_3.arr} ARR, {result.cash_position} cash")
```

### Example 3: Cost Audit

```python
# 30-minute cost audit
def run_cost_audit(spending_data):
    findings = []
    
    # Software spend analysis
    software_findings = analyze_software_spend(spending_data.software)
    findings.extend(software_findings)
    
    # Cloud infrastructure analysis
    cloud_findings = analyze_cloud_spend(spending_data.cloud)
    findings.extend(cloud_findings)
    
    # Vendor agreement review
    vendor_findings = analyze_vendor_contracts(spending_data.vendors)
    findings.extend(vendor_findings)
    
    # Calculate total savings opportunity
    total_opportunity = sum(f["annual_savings"] for f in findings)
    
    return {
        "findings": findings,
        "total_annual_opportunity": total_opportunity,
        "quick_wins": [f for f in findings if f["implementation"] == "immediate"]
    }

# Run the audit
audit_results = run_cost_audit(load_spending_data())
print(f"Total Savings Opportunity: ${audit_results.total_annual_opportunity:,}")
print(f"Quick Wins: {len(audit_results.quick_wins)}")
```

---


## When NOT to Use

- For processes that change daily (too much overhead)
- When the team is too small to benefit from SOPs
- For one-time events that will not repeat


## Overview

Finance Ops streamlines operational efficiency for operational excellence.

## Workflow

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

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run finance ops workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings