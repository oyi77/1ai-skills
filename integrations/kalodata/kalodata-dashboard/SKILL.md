---
name: kalodata-dashboard
description: Use when generating CLI-based visual reports from Kalodata product research data, including ASCII trend charts,
  product cards, interactive dashboards, and markdown exports.
domain: integrations
tags:
- api
- dashboard
- integrations
- kalodata
- third-party
---

# Kalodata Dashboard Skill

## Overview

Creates CLI-based visual reports with ASCII/text-based charts, product cards, interactive reports, and markdown exports from Kalodata product research data. Works with existing `ProcessedProduct` data from the kalodata module.

## When to Use

**Trigger phrases:**
- "kalodata dashboard"
- "User asks for "dashboard", "report", "visualize", "charts", or "trends""
- "Need to display revenue trends as ASCII line/bar charts in terminal"
- "Creating product summary cards with key metrics"


- User asks for "dashboard", "report", "visualize", "charts", or "trends"
- Need to display revenue trends as ASCII line/bar charts in terminal
- Creating product summary cards with key metrics
- Generating markdown export of research findings
- Building interactive CLI-based product explorer

## The Process

1. **Identify the reporting need** – Determine what data to visualize and the report format
2. **Prepare the data** – Ensure you have `ProcessedProduct` data from kalodata research
3. **Choose visualization type** – Select from trend charts, product cards, interactive CLI or markdown export
4. **Generate the report** – Use the core patterns to create visualizations
5. **Export and share** – Save as markdown or share interactive dashboard

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Trying to create visual dashboards with real-time data (this skill works with static research data)
- Using ASCII charts for web/mobile output (use SVG/Canvas for web instead)
- Creating complex interactive web apps (use frontend-ui-ux skill instead)
- Generating reports without proper data preprocessing (ensure kalodata research completed first)

## Verification

- ASCII trend charts render correctly in terminal (no encoding issues)
- Product cards display all fields without truncation
- Markdown export preserves formatting and structure
- Interactive CLI navigation works smoothly
- Exported markdown files are readable and publishable

```typescript
function renderTrendChart(trend: number[], width = 50, height = 10): string {
  const maxVal = Math.max(...trend);
  const minVal = Math.min(...trend);
  const range = maxVal - minVal || 1;
  
  // Sample points to fit width
  const step = Math.max(1, Math.floor(trend.length / width));
  const sampled = [];
  for (let i = 0; i < trend.length; i += step) {
    sampled.push(trend[i]);
  }
  
  const chart: string[] = [];
  for (let row = height - 1; row >= 0; row--) {
    let line = '';
    const threshold = minVal + (range * row / height);
    for (const val of sampled) {
      line += val >= threshold ? '█' : ' ';
    }
    chart.push(line);
  }
  
  return chart.join('\n');
}
```

### Product Card

```typescript
function renderProductCard(product: ProcessedProduct): string {
  const trend = renderTrendChart(product.revenueTrend);
  const trendIcon = product.trendDirection === 'rising' ? '📈' 
    : product.trendDirection === 'declining' ? '📉' : '➡️';
  
  return `
┌─────────────────────────────────────────────────┐
│ ${product.title.slice(0, 50)}
├─────────────────────────────────────────────────┤
│ 💰 Revenue: ${product.revenueFormatted}
│ 📊 Sales: ${product.sales.toLocaleString()} | Creators: ${product.creators}
│ ⭐ Rating: ${product.rating} | Conversion: ${(product.conversionRate * 100).toFixed(1)}%
│ 🏷️ Commission: ${product.commissionRate} | Launch: ${product.launchDate}
│ ${trendIcon} Trend: ${product.trendDirection.toUpperCase()}
├─────────────────────────────────────────────────┤
│ ${trend}
└─────────────────────────────────────────────────┘
  `.trim();
}
```

### Interactive CLI Menu

```typescript
async function runInteractiveDashboard(products: ProcessedProduct[]): Promise<void> {
  let selected = 0;
  
  while (true) {
    console.clear();
    console.log('📊 KALODATA DASHBOARD\n');
    console.log('Use ↑↓ to navigate, Enter to select, q to quit\n');
    
    // Show product list with selection
    products.forEach((p, i) => {
      const prefix = i === selected ? '▶ ' : '  ';
      console.log(`${prefix}${i + 1}. ${p.title.slice(0, 40)} - ${p.revenueFormatted}`);
    });
    
    const key = await readKey();
    if (key === 'q') break;
    if (key === 'ArrowUp') selected = Math.max(0, selected - 1);
    if (key === 'ArrowDown') selected = Math.min(products.length - 1, selected + 1);
    if (key === 'Enter') {
      console.clear();
      console.log(renderProductCard(products[selected]));
      await readKey();
    }
  }
}
```

### Markdown Export

```typescript
function exportToMarkdown(products: ProcessedProduct[], title = 'Kalodata Report'): string {
  let md = `# ${title}\n\n`;
  md += `**Generated:** ${new Date().toISOString()}\n\n`;
  
  md += `## Summary\n\n`;
  md += `- Total Products: ${products.length}\n`;
  md += `- Total Revenue: ${formatCurrency(products.reduce((a, p) => a + p.revenue, 0))}\n`;
  md += `- Avg Conversion: ${(products.reduce((a, p) => a + p.conversionRate, 0) / products.length * 100).toFixed(1)}%\n\n`;
  
  md += `## Top Products\n\n`;
  for (const p of products.slice(0, 10)) {
    md += `### ${p.title}\n\n`;
    md += `- Revenue: ${p.revenueFormatted}\n`;
    md += `- Sales: ${p.sales.toLocaleString()}\n`;
    md += `- Rating: ${p.rating}\n`;
    md += `- Commission: ${p.commissionRate}\n`;
    md += `- Trend: ${p.trendDirection}\n\n`;
  }
  
  return md;
}
```

## Quick Reference

| Function | Purpose |
|----------|---------|
| `renderTrendChart()` | ASCII line chart from revenue trend array |
| `renderBarChart()` | Horizontal bar chart for comparisons |
| `renderProductCard()` | Single product summary with mini chart |
| `renderDashboard()` | Multi-product overview grid |
| `runInteractiveDashboard()` | CLI menu for browsing products |
| `exportToMarkdown()` | Generate markdown report file |
| `renderTable()` | Formatted data table in ASCII |

## Implementation

See `dashboard.ts` for full implementation with:
- Multiple chart types (line, bar, sparkline)
- Color support (ANSI codes)
- Interactive navigation
- Markdown export
- Summary statistics

## Common Mistakes

- **Chart too wide**: Limit width to terminal size (default 50 chars)
- **Missing trend data**: Handle empty arrays gracefully
- **No color support**: Check `isTTY` before using ANSI colors
- **Export without headers**: Always include generation timestamp

## Real-World Impact

CLI dashboards enable:
- Quick product analysis without browser
- Shareable markdown reports for stakeholders
- Interactive exploration of large product datasets
- Integration into automated workflows

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will handle auth later" | Retrofitting auth is 10x harder. Build it from day one. |
| "APIs do not change" | APIs change. Version your integrations and handle deprecations. |
| "Webhooks are optional" | Without webhooks, you miss real-time events. They are essential. |