# analytics-reporting Skill

## What It Does

Data analytics and reporting - collect data from various sources, analyze metrics, generate dashboards, and create actionable reports.

## When to Use

- Track business metrics
- Generate performance reports
- Create dashboards
- Analyze trends
- Support data-driven decisions

## Key Capabilities

- **Data Collection**: Gather data from multiple sources
- **Metric Analysis**: Calculate and interpret KPIs
- **Dashboard Creation**: Visual data representation
- **Report Generation**: Structured insights and recommendations
- **Trend Analysis**: Identify patterns over time

## Browser Workflows

### Collect Analytics Data

1. Navigate: analytics platform (GA4, Mixpanel, etc.)
2. Select: date range and metrics
 data to CSV/She3. Export:ets
4. Process: clean and structure data
5. Store: in data warehouse

### Generate Report

1. Gather: data from all sources
2. Analyze: calculate metrics and trends
3. Visualize: create charts and graphs
4. Write: insights and recommendations
5. Export: to PDF/Docs/Sheets

## Usage Examples

### Weekly Business Review
```
User: "Generate our weekly metrics report"
Skill: Collects data → calculates KPIs → creates visualizations → generates report
```

### Marketing Campaign Analysis
```
User: "How did our Q1 campaign perform?"
Skill: Analyzes campaign data → compares to goals → identifies wins/issues → reports
```

### Dashboard Update
```
User: "Update the sales dashboard with latest data"
Skill: Pulls latest numbers → updates charts → refreshes display → notifies team
```

## Skills It Coordinates

- `agent-browser` - Browser automation
- `analytics-tracking` (skills.sh) - Analytics implementation
- `google-workspace` MCP - Sheets/Docs integration
- `supabase` MCP - Data storage (when available)

## Key Metrics Tracked

| Category | Metrics |
|----------|---------|
| Revenue | MRR, ARR, Growth Rate, Churn |
| Marketing | Traffic, Leads, CAC, Conversion Rate |
| Product | DAU, MAU, Retention, NPS |
| Support | Ticket Volume, Resolution Time, CSAT |

## Report Quality Rubric

| Criterion | Weight | Threshold |
|-----------|--------|-----------|
| Accuracy | 35% | Data verified |
| Clarity | 25% | Easy to understand |
| Actionability | 25% | Clear recommendations |
| Completeness | 15% | All relevant data |

## Files Created

- `analytics-data/` - Raw data exports
- `dashboards/` - Dashboard definitions
- `reports/` - Generated reports
- `insights/` - Key insights and learnings
