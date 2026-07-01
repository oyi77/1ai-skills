---
name: xlsx-creator
description: Create, edit, and analyze Excel spreadsheets programmatically. Generate financial models, data tables, charts, and dashboards with formulas and formatting.
domain: content
tags:
- documents
- excel
- xlsx
- spreadsheets
- financial-models
---

# Xlsx Creator

## When to Use
**Trigger phrases:**
- "xlsx creator"
- "Create, edit, and analyze Excel spreadsheets programmatically"


- When generating Excel reports from data
- When creating financial models or budgets
- When building data tables with formulas and charts
- When converting structured data to spreadsheet format

## When NOT to Use

- For simple data storage (use CSV or JSON)
- For real-time collaborative editing (use Google Sheets API)
- For large-scale data processing (use pandas/SQL)

## Overview

Full Excel lifecycle — creation, editing, formatting, formulas, charts, and data validation. Uses openpyxl (Python) or ExcelJS (Node.js).

## Workflow

1. **Define structure** — Sheets, columns, data types
2. **Add data** — Headers, data rows, formulas
3. **Apply formatting** — Number formats, fonts, colors, borders
4. **Add charts** — Bar, line, pie, scatter charts
5. **Add validation** — Data validation rules, conditional formatting
6. **Export** — Save as .xlsx with proper naming

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "CSV is fine" | Excel supports formulas, charts, formatting, and multiple sheets |
| "I'll build it manually" | Programmatic generation handles data updates and is reproducible |
| "Spreadsheets are outdated" | Excel is still the #1 business tool for financial analysis |

## Code Example (Python)

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active
ws.title = 'Revenue'

# Headers
ws['A1'] = 'Month'
ws['B1'] = 'Revenue'
ws['C1'] = 'Expenses'

# Data
data = [('Jan', 50000, 30000), ('Feb', 55000, 32000), ('Mar', 62000, 35000)]
for i, (month, rev, exp) in enumerate(data, 2):
    ws[f'A{i}'] = month
    ws[f'B{i}'] = rev
    ws[f'C{i}'] = exp
    ws[f'D{i}'] = f'=B{i}-C{i}'  # Profit formula

# Chart
chart = BarChart()
chart.title = 'Revenue vs Expenses'
data_ref = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)
chart.add_data(data_ref, titles_from_data=True)
ws.add_chart(chart, 'F2')

wb.save('revenue.xlsx')
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run xlsx creator workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] Spreadsheet opens without errors
- [ ] Formulas calculate correctly
- [ ] Charts render with correct data
- [ ] Number formats display properly
- [ ] Conditional formatting works

