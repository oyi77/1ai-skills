---
name: xlsx-creator
description: Create, edit, and analyze Excel spreadsheets programmatically. Generate financial models, data tables, charts, and dashboards with formulas and formatting.
domain: content
author: mahipal
license: Apache-2.0
subdomain: content-creation
tags:
- documents
- excel
- xlsx
- spreadsheets
- financial-models
version: 1.0.0
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
Full Excel lifecycle support — creation, editing, formatting, formulas, charts, data validation, and analysis. Covers both generation (building workbooks from data) and manipulation (modifying existing spreadsheets, extracting data).

**Python stack:** openpyxl for full spreadsheet creation and formatting (styles, charts, conditional formatting, data validation), pandas for bulk data import/export, xlsxwriter for high-performance write-only workloads with rich formatting (charts, conditional formats, data bars).
**Node.js stack:** exceljs for streaming read/write with rich formatting (fonts, fills, borders, alignment, merged cells, conditional formatting, data validation, charts, pivot tables), xlsx (SheetJS) for zero-dependency parsing and basic creation, fast-csv for CSV conversion.

Key capabilities: multi-sheet workbooks, named ranges (define names for formula clarity), conditional formatting (color scales, data bars, icon sets), data validation (lists, ranges, custom formulas), pivot tables, sparklines (inline mini-charts), cell comments, merged cells, print settings (page layout, headers/footers, margins), and streaming API for large datasets.

## Workflow

1. **Define structure** — Determine sheets needed (summary, data, charts). Plan column widths, data types (text, number, date, currency), and named ranges. Choose the right library: openpyxl/xlsxwriter for Python server-side, exceljs for Node.js with large datasets (streaming).
2. **Add data** — Write headers on row 1. Populate data rows from arrays, dicts, or database queries. Add formulas (SUM, IF, VLOOKUP, XLOOKUP) as cell formulas or computed values. Use named ranges for formula clarity (e.g., `=SUM(Revenue_2026)` instead of `=SUM(B2:B100)`).
3. **Apply formatting** — Set number formats (#,##0 for integers, #,##0.00 for decimals, $#,##0.00 for currency, YYYY-MM-DD for dates). Apply fonts, fill colors, borders, alignment (wrap text, merge cells). Style header rows with bold text and background fills.
4. **Add charts** — Create bar, line, pie, scatter charts. Position them at specific cell anchors (e.g., `F2`). Configure chart title, axis labels, legend, and data labels. For sparklines, use openpyxl's `SparklineGroup` or exceljs's `sparklines` property.
5. **Add validation and conditional formatting** — Data validation: dropdown lists, numeric ranges, custom formulas. Conditional formatting: color scales (heat maps), data bars (in-cell bar charts), icon sets (traffic lights), highlight rules (cells > threshold).
6. **Export** — Save as `.xlsx` with proper naming (include date/timestamp for reports). For large workbooks, use streaming write (xlsxwriter's `Workbook()` or exceljs's `worksheet.write()`). Set document properties (title, author, company).

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "CSV is fine" | Excel supports formulas, charts, formatting, and multiple sheets |
| "I'll build it manually" | Programmatic generation handles data updates and is reproducible |
| "Spreadsheets are outdated" | Excel is still the #1 business tool for financial analysis |
| "openpyxl is all I need" | xlsxwriter is faster for write-only workloads with larger datasets; exceljs supports streaming for files over 100MB |
| "I can just use pandas to_excel()" | pandas output lacks rich formatting (charts, conditional formatting, merged cells, proper number formats) — use openpyxl/xlsxwriter for production reports |
| "Formulas will auto-calculate on open" | Excel prompts users to recalculate if formulas reference external files; use `data_only=True` or pre-compute values alongside formulas

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

## Code Example (Node.js)

```javascript
import ExcelJS from 'exceljs';

const workbook = new ExcelJS.Workbook();
workbook.creator = 'Report Bot';
workbook.created = new Date();

const sheet = workbook.addWorksheet('Revenue');

// Headers with styling
sheet.getCell('A1').value = 'Month';
sheet.getCell('B1').value = 'Revenue';
sheet.getCell('C1').value = 'Expenses';
sheet.getCell('D1').value = 'Profit';

const headerRow = sheet.getRow(1);
headerRow.font = { bold: true, color: { argb: 'FFFFFFFF' } };
headerRow.fill = {
  type: 'pattern',
  pattern: 'solid',
  fgColor: { argb: 'FF4472C4' },
};
headerRow.alignment = { horizontal: 'center' };

// Data rows with formulas
const data = [
  { month: 'Jan', revenue: 50000, expenses: 30000 },
  { month: 'Feb', revenue: 55000, expenses: 32000 },
  { month: 'Mar', revenue: 62000, expenses: 35000 },
];
data.forEach((row, i) => {
  const r = i + 2;
  sheet.getCell(`A${r}`).value = row.month;
  sheet.getCell(`B${r}`).value = row.revenue;
  sheet.getCell(`C${r}`).value = row.expenses;
  sheet.getCell(`D${r}`).value = { formula: `B${r}-C${r}`, result: row.revenue - row.expenses };
  sheet.getCell(`D${r}`).numFmt = '$#,##0';
});

// Number formats
sheet.getColumn(2).numFmt = '$#,##0';
sheet.getColumn(3).numFmt = '$#,##0';
sheet.getColumn(4).numFmt = '$#,##0';

// Column widths
sheet.columns = [
  { key: 'month', width: 12 },
  { key: 'revenue', width: 16 },
  { key: 'expenses', width: 16 },
  { key: 'profit', width: 16 },
];

await workbook.xlsx.writeFile('revenue.xlsx');
console.log('Workbook saved');
```

## Setup & Configuration

**Python environment:**
```bash
pip install openpyxl xlsxwriter pandas
```

**Node.js environment:**
```bash
npm install exceljs xlsx
```

**Performance tuning for large datasets:**
- **Python:** Use `xlsxwriter` instead of `openpyxl` for write-only workloads (5-10x faster, lower memory). For >100K rows, stream data in chunks.
- **Node.js:** Use `exceljs` streaming writer for files over 50MB: `const workbook = new ExcelJS.stream.xlsx.WorkbookWriter({ stream })`.
- **Memory:** For 1M+ row exports, generate CSV (faster) and offer a conversion tool, or use database-level export (e.g., SQL Server Export to Excel).

**Additional features (openpyxl):**
```python
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.formatting.rule import CellIsRule, DataBarRule, ColorScaleRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.chart.label import DataLabelList
```

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| File corrupt when opening in Excel | Check for XML-invalid characters in cell values (Tab, Ctrl-Z, non-BMP Unicode). Sanitize strings: `str(value).replace('\t', ' ').replace('\x1a', '')` |
| Formulas display as text instead of calculating | Excel cached values; openpyxl formulas need Excel to recalculate. Set `ws.calculation = Calculation(alculationMode='auto')` or use `data_only` when reading |
| openpyxl crashes with large files (>1GB) | Switch to xlsxwriter (write-only, low memory). For reads, use `read_only=True` mode in openpyxl to iterate without loading entire file |
| Chart data not updating when source changes | Charts reference cells by address, not named ranges. Use defined names: `wb.defined_names['Revenue_Data'] = ...` and set chart data to named range |
| Date formats show as serial numbers | Apply number format explicitly: `cell.number_format = 'YYYY-MM-DD'`. Excel auto-detects dates only within a certain range |
| Unicode characters (Chinese, emoji) display as ??? | Ensure the font supports the characters (Calibri supports most). For emoji, use `cell.value = str(value)` — Excel handles rendering |
| Merged cells break sorting and filtering | Avoid merged cells in data tables. Use `center_across_selection` alignment instead or merge only in header rows — never in data rows |
| Conditional formatting won't apply to entire column | Use `DataBarRule` with `extend=True` (openpyxl) or apply conditional formatting rules to column ranges: `sheet.conditionalFormatting.add('A:A', rule)` |

## Monetization

- **Financial reporting service** — Build branded monthly/quarterly reports for SMBs. Combine SQL data sources with styled Excel output. Charged $100-500/setup + $50/month per report.
- **Data export add-on** — Add "Export to Excel" feature to existing SaaS products. Charge as a premium tier feature. Common for CRM, analytics, and inventory platforms.
- **Invoice/billing generator** — Automated invoice generation with Excel templates. Fill customer data, line items, tax calculations, and totals. Sell as standalone tool ($50-200 one-time).
- **Excel template marketplace** — Create and sell premium financial model templates: budgeting, forecasting, P&L, cash flow, DCF analysis. Sell on Etsy, Gumroad, or dedicated sites ($5-50/template).
- **Conversion API** — JSON/CSV/API → formatted Excel micro-SaaS. Charge per file ($0.10-1.00) or monthly subscription for bulk conversion. Use streaming for large datasets.
- **Data cleaning service** — Process messy Excel/CSV files: normalize formats, deduplicate, apply validation, generate clean structured output. $0.50-2.00 per file via API.


## Process

1. **Environment setup** — Install libraries: `pip install openpyxl xlsxwriter pandas` (Python) or `npm install exceljs xlsx` (Node.js). For streaming large files (>100MB), prefer xlsxwriter (Python) or exceljs streaming (Node.js). Test basic workbook creation.
2. **Template design** — Sketch the workbook structure (sheet names, column layout, header row styling, chart positions). For data-driven reports, map incoming data fields to cell positions and decide which values are formulas vs literals.
3. **Data assembly** — Load data from source (JSON, CSV, SQL query, API). Write headers, populate data rows, insert formulas. Apply number formats (currency, date, percentage). Add named ranges for formula readability.
4. **Formatting and polish** — Apply conditional formatting rules (color scales, data bars, highlight rules). Add charts with proper data ranges. Set print settings (page orientation, margins, header/footer, print area). Add data validation for input cells.
5. **Quality check** — Open the output in Excel (not just Google Sheets — formatting differences exist). Verify formulas recalculate correctly, charts render, number formats display properly, conditional formatting triggers correctly, and page breaks are correct.
6. **Delivery** — Save with clear naming (include date/timestamp for periodic reports). Set document properties (Title, Author, Company, Keywords). For APIs, return the .xlsx buffer for download rather than saving to disk.

## Verification

- [ ] Workbook opens without errors in Excel (desktop) and Google Sheets
- [ ] All formulas calculate correctly (no #REF!, #VALUE!, #DIV/0! errors)
- [ ] Charts render with correct data ranges and formatting
- [ ] Number/date/currency formats display as expected in target locale
- [ ] Conditional formatting rules trigger on correct cells
- [ ] Data validation dropdowns and constraints work
- [ ] Named ranges resolve correctly in formulas
- [ ] Column widths and row heights fit content
- [ ] Print layout (page orientation, margins, headers/footers) is correct
- [ ] File size is reasonable — use streaming for datasets over 100K rows
