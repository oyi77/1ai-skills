---
name: finance-ops
description: Run AI-powered CFO analysis for cost detection, financial modeling, scenario planning, and operational efficiency
  optimization.
domain: operations
tags:
- business-ops
- finance
- management
- operations
- ops
---
## Skill Definition

**Name:** `finance-ops`

**Pattern:** operations/finance/finance-ops

**Description:** AI-powered CFO capabilities for cost analysis, financial modeling, scenario planning, and operational efficiency. Identifies hidden costs and optimization opportunities in 30 minutes.

---

## Implementation

How to set up and configure this skill.


### Phase 1: CFO Briefing Generation

**Financial Health Dashboard**
```python
def generate_cfo_briefing(company_data):
    return {
        "cash_runway": calculate_runway(
            cash_balance, 
            monthly_burn,
            growth_trajectory
        ),
        "unit_economics": analyze_unit_economics(
            cac, ltv, gross_margin, payback_period
        ),
        "efficiency_metrics": calculate_efficiency_scores(
            revenue_per_employee,
            opex_ratio,
            gross_margin_trend
        ),
        "risk_indicators": identify_financial_risks(
            concentration_risk,
            covenant_compliance,
            working_capital
        )
    }
```

**Key Metrics Matrix**
```
GROWTH METRICS          | EFFICIENCY METRICS      | RISK METRICS
------------------------|-------------------------|----------------
MRR/ARR Growth          | CAC Payback Period      | Cash Runway
Net Revenue Retention   | LTV/CAC Ratio          | Burn Multiple
Expansion Revenue       | Gross Margin            | Debt/Equity
New Customer ARR        | OpEx as % Revenue       | Quick Ratio
```

### Phase 2: Cost Intelligence

**Hidden Cost Detection**
```python
cost_categories = {
    "software_spend": {
        "red_flags": [
            "duplicate_tools",
            "unused_licenses", 
            "auto_renewal_without_review",
            "per-seat_pricing_inefficiency"
        ],
        "optimization_opportunities": [
            "annual_prepay_discounts",
            "volume_negotiation",
            "tier_downgrades",
            "consolidation"
        ]
    },
    "cloud_infrastructure": {
        "red_flags": [
            "orphaned_resources",
            "oversized_instances",
            "unused_reserved_capacity",
            "data_transfer_inefficiency"
        ],
        "optimization_opportunities": [
            "spot_instances",
            "reserved_instance_planning",
            "right_sizing",
            "auto_scaling"
        ]
    },
    "vendor_agreements": {
        "red_flags": [
            "evergreen_contracts",
            "auto_escalation_clauses",
            "no_competitive_bidding",
            "payment_term_inefficiency"
        ]
    }
}
```

**Cost Benchmarking**
```python
def benchmark_costs(company_spending, peer_data):
    """
    Compare against industry benchmarks
    """
    benchmarks = {
        "software_spend": {
            "percent_of_revenue": 0.08,  # 8% benchmark
            "percent_of_headcount": 1200  # $1,200/employee
        },
        "cloud_spend": {
            "percent_of_revenue": 0.12,  # 12% for SaaS
            "cost_per_customer": 25  # varies by ACV
        },
        "facilities": {
            "cost_per_employee": 8000,  # annual
            "square_feet_per_employee": 150
        }
    }
    
    return calculate_variance(company_spending, benchmarks)
```

### Phase 3: Scenario Modeling

**Three-Statement Model**
```python
class FinancialModel:
    def __init__(self, assumptions):
        self.revenue_model = assumptions['revenue']
        self.cost_model = assumptions['costs']
        self.working_capital = assumptions['wc']
        
    def project(self, years=3):
        income_statement = self.build_income_statement()
        balance_sheet = self.build_balance_sheet()
        cash_flow = self.build_cash_flow()
        
        return {
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow
        }
    
    def scenario_analysis(self, scenarios):
        """
        Run multiple scenarios:
        - Base case
        - Upside case  
        - Downside case
        - Stress test
        """
        results = {}
        for name, assumptions in scenarios.items():
            results[name] = self.project_with_assumptions(assumptions)
        return results
```

**Scenario Variables**
```python
scenario_variables = {
    "revenue": {
        "growth_rate": [0.50, 0.75, 1.00, 1.25],  # Base to upside
        "churn_rate": [0.05, 0.03, 0.02, 0.01],
        "expansion_rate": [0.10, 0.15, 0.20, 0.30]
    },
    "costs": {
        "headcount_growth": [0.30, 0.40, 0.50, 0.60],
        "salary_inflation": [0.03, 0.04, 0.05, 0.06],
        "software_inflation": [0.05, 0.07, 0.10, 0.12]
    },
    "funding": {
        "next_round_timing": [12, 9, 6, 18],  # months
        "valuation_multiple": [8, 10, 12, 6]  # ARR multiple
    }
}
```

### Phase 4: Operational Efficiency

**Working Capital Optimization**
```python
def optimize_working_capital(ap, ar, inventory):
    """
    Identify WC optimization opportunities
    """
    opportunities = []
    
    # Accounts Payable
    if ap.days_payable_outstanding < 45:
        opportunities.append({
            "area": "AP",
            "opportunity": "Extend payment terms",
            "potential_cash": calculate_cash_release(ap, target_dpo=60)
        })
    
    # Accounts Receivable
    if ar.days_sales_outstanding > 30:
        opportunities.append({
            "area": "AR",
            "opportunity": "Improve collections",
            "potential_cash": calculate_cash_release(ar, target_dso=25)
        })
    
    return opportunities
```

**Headcount Efficiency Analysis**
```python
def analyze_headcount_efficiency(org_data):
    metrics = {
        "revenue_per_employee": total_revenue / headcount,
        "managers_to_ic_ratio": n_managers / n_individual_contributors,
        "span_of_control": direct_reports_per_manager,
        "layers": org_hierarchy_depth
    }
    
    benchmarks = get_industry_benchmarks(sector, stage)
    return compare_and_identify_gaps(metrics, benchmarks)
```

---

## Usage Examples

Practical examples showing real-world usage.


### Example 1: Monthly CFO Briefing

```python
# Generate comprehensive CFO briefing
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

## Integration Points

**Cross-Skill Dependencies**
- `trading/black-edge` - For market intelligence
- `research/mckinsey-research` - For strategic frameworks
- `marketing/growth-engine` - For CAC/LTV analysis
- `operations/operations-team` - For SOP integration

**Data Source Requirements**
- Accounting: QuickBooks, NetSuite, Xero
- Analytics: Mixpanel, Amplitude, Segment
- HRIS: BambooHR, Gusto, Workday
- Cloud: AWS Cost Explorer, GCP Billing

---

## Output Format

```yaml
finance_ops_report:
  reporting_period: "2025-04"
  generated_at: "2025-05-04T10:00:00Z"
  
  executive_summary:
    cash_position: "$2.3M"
    runway_months: 14
    burn_rate: "$165K/month"
    key_insight: "Optimize cloud spend to extend runway 3 months"
    
  unit_economics:
    cac: "$1,200"
    ltv: "$8,400"
    ltv_cac_ratio: 7.0
    gross_margin: 0.76
    payback_months: 8
    magic_number: 1.2
    
  cost_analysis:
    total_annual_spend: "$4.2M"
    optimization_opportunities:
      - category: "Software"
        annual_spend: "$480K"
        opportunity: "$72K"
        quick_win: True
      - category: "Cloud Infrastructure"
        annual_spend: "$580K"
        opportunity: "$87K"
        quick_win: False
      - category: "Vendor Contracts"
        annual_spend: "$320K"
        opportunity: "$48K"
        quick_win: True
    total_opportunity: "$207K"
    
  scenario_analysis:
    base_case:
      year_1_arr: "$7.8M"
      year_3_arr: "$21M"
      cash_needed: "$3M"
    upside_case:
      year_1_arr: "$9.5M"
      year_3_arr: "$32M"
      cash_needed: "$5M"
    downside_case:
      year_1_arr: "$6.2M"
      year_3_arr: "$14M"
      cash_needed: "$1M"
      
  operational_metrics:
    revenue_per_employee: "$180K"
    benchmark: "$220K"
    gap: "-18%"
    recommendation: "Review G&A headcount"
    
  action_items:
    - priority: "HIGH"
      action: "Renegotiate AWS reserved instances"
      owner: "VP Engineering"
      timeline: "2 weeks"
      savings: "$87K/year"
    - priority: "HIGH"
      action: "Cancel unused software licenses"
      owner: "IT Manager"
      timeline: "1 week"
      savings: "$35K/year"
    - priority: "MEDIUM"
      action: "Extend vendor payment terms"
      owner: "Finance Manager"
      timeline: "1 month"
      savings: "$48K/year"
```

---

## Triggers

- `/finance cfo-briefing` - Generate monthly CFO report
- `/finance cost-audit` - Run 30-minute cost optimization
- `/finance scenario-plan` - Build multi-year financial model
- `/finance runway` - Calculate and optimize cash runway

---

**Prerequisites:** Requires access to company financial data. Can work with exported CSVs if direct integrations unavailable.

**Donation:** Support development → https://www.tip.md/oyi77

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


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).
## Verification

After completing this skill, confirm:

- [ ] Changes are communicated to stakeholders before implementation
- [ ] Compliance with established processes is tracked and reported
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
