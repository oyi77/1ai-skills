---
name: docx-creator
description: Create, edit, and analyze Word documents programmatically using python-docx or docx.js. Generate reports, proposals, and templates with formatting, tables, images, and styles.
domain: content
author: mahipal
license: Apache-2.0
subdomain: content-creation
tags:
- documents
- word
- docx
- office
- reports
- templates
version: 1.0.0
---

# Docx Creator

## When to Use
- When generating Word documents from data or templates
- When creating reports, proposals, or contracts programmatically
- When converting structured data to formatted .docx files
- When batch-generating documents with variable content

## When NOT to Use

- For simple text output (use plain text or markdown)
- When the user needs a PDF instead (use `pdf-creator`)
- For real-time collaborative editing (use Google Docs API)

## Overview

Create professional Word documents with full formatting support. Handles headers, footers, tables, images, styles, and page layout. Works with python-docx (Python) or docx (Node.js).

## Workflow

1. **Define structure** — Outline document sections, headings, and content blocks. Map data sources to document sections.
2. **Set up styles** — Configure fonts, colors, spacing, heading hierarchy, and page layout. Create reusable style definitions.
3. **Build reusable templates** — Design template .docx files with placeholders, pre-styled sections, and content controls for variable substitution.
4. **Add content** — Insert text with runs, tables with merged cells, images with sizing, lists with nesting, and hyperlinks with proper formatting.
5. **Apply formatting** — Set headers/footers with page numbers, section breaks for orientation changes, table-of-contents fields, and watermarks.
6. **Assemble and merge** — Combine template sections, inject dynamic data, merge multiple docx fragments into one coherent document.
7. **Export and validate** — Save as .docx with proper file naming, validate output opens cleanly, check rendering fidelity across Word and LibreOffice.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|
| "Plain text is fine for reports" | Professional documents need formatting — headers, tables, styles matter for credibility and readability |
| "I'll just use copy-paste" | Programmatic generation is reproducible, version-controlled, scalable, and eliminates manual errors |
| "Word is outdated" | .docx is still the business standard for contracts, proposals, formal reports, and regulatory filings |
| "Templates are too much overhead" | A well-designed template cuts document generation time by 80% and enforces brand consistency |
| "python-docx can't do that" | Most limitations can be worked around using XML manipulation via lxml on the underlying docx XML |
| "Batch generation is overkill" | When you need 50+ personalized documents, manual creation costs 10x more in time and errors |

## Code Example (Python)

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
doc.add_heading('Quarterly Report', 0)

# Styled paragraph
p = doc.add_paragraph()
run = p.add_run('Revenue increased by 23%')
run.bold = True
run.font.size = Pt(14)

# Table
table = doc.add_table(rows=1, cols=3)
table.style = 'Light Shading Accent 1'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Metric'
hdr_cells[1].text = 'Q1'
hdr_cells[2].text = 'Q2'

doc.save('report.docx')
```

### Template Assembly with Placeholders

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
import re, json

def fill_template(template_path: str, data: dict, output_path: str):
    """Replace {{placeholder}} tags in a .docx template with data values."""
    doc = Document(template_path)
    for para in doc.paragraphs:
        for key, value in data.items():
            if f'{{{{{key}}}}}' in para.text:
                for run in para.runs:
                    if f'{{{{{key}}}}}' in run.text:
                        run.text = run.text.replace(f'{{{{{key}}}}}', str(value))
                        run.bold = True
    # Process tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in data.items():
                        if f'{{{{{key}}}}}' in para.text:
                            para.text = para.text.replace(f'{{{{{key}}}}}', str(value))
    doc.save(output_path)
    print(f"Generated: {output_path}")

# Usage
data = {"client_name": "Acme Corp", "date": "2026-07-27", "amount": "$12,500"}
fill_template("proposal_template.docx", data, "proposal_acme.docx")
```

### Batch Document Generation

```python
from docx import Document
from docx.shared import Pt
import csv

def batch_generate(csv_path: str, template_path: str, output_dir: str):
    """Generate one personalized document per CSV row using a template."""
    doc_template = Document(template_path)
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            doc = Document(template_path)
            for para in doc.paragraphs:
                for key, val in row.items():
                    tag = f"{{{{{key}}}}}"
                    if tag in para.text:
                        para.text = para.text.replace(tag, val)
            out_path = f"{output_dir}/document_{i+1}.docx"
            doc.save(out_path)
            print(f"Created: {out_path}")

# CSV columns: name, company, amount
batch_generate("clients.csv", "invoice_template.docx", "./output")
```

### Tables with Merged Cells and Formatting

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

doc = Document()
table = doc.add_table(rows=4, cols=4)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# Merge top row across all columns for a title
title_cell = table.cell(0, 0)
title_cell_end = table.cell(0, 3)
title_cell.merge(title_cell_end)
title_cell.text = "Annual Summary"

# Set column widths
for row in table.rows:
    for idx, cell in enumerate(row.cells):
        cell.width = Cm(3.5)
        # Shade header cells
        if row == table.rows[0]:
            shading = cell._element.get_or_add_tcPr()
            shd = shading.makeelement(qn('w:shd'), {
                qn('w:fill'): '2E75B6',
                qn('w:val'): 'clear'
            })
            shading.append(shd)

doc.save('styled_table.docx')
```

### Adding Images and Page Layout

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, Emu
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn

doc = Document()

# Landscape section for wide tables
section = doc.sections[0]
new_section = doc.add_section()
new_section.orientation = WD_ORIENT.LANDSCAPE
new_section.page_width = Cm(29.7)
new_section.page_height = Cm(21.0)

# Add image with precise sizing
doc.add_paragraph().add_run("Chart Analysis:").bold = True
doc.add_picture("chart.png", width=Inches(5.5))

# Faded draft-stamp text in header (simple alternative to complex watermark XML)
for section in doc.sections:
    header = section.header
    p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    run = p.add_run("CONFIDENTIAL — DRAFT")
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(192, 192, 192)
    run.italic = True

doc.save('report_with_chart.docx')
```

## Setup / Configuration

### Python Environment

```bash
pip install python-docx
```

python-docx is the primary library for .docx generation in Python. No external services or API keys required.

### Node.js Environment

```bash
npm install docx
```

### Project Structure

```
docx-generator/
├── templates/          # Template .docx files with {{placeholder}} tags
├── output/             # Generated documents
├── scripts/
│   ├── generate.py     # Main generation script
│   └── helpers.py      # Shared formatting utilities
└── data/
    └── source.csv      # Input data for batch generation
```

## Common Issues / Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| "KeyError: 'no such image'" | Image file path is invalid or format unsupported | Use absolute paths; ensure PNG/JPEG format; check file exists before calling add_picture |
| Table cells don't merge visually | merge() only works on rectangular areas; merged region must span contiguous cells | Always merge from top-left to bottom-right cell in the rectangle; verify cell range |
| Styles not applying | Style names are case-sensitive; custom styles must be registered | Use exact built-in names like 'Light Shading Accent 1'; register custom styles via doc.styles |
| Placeholders not replaced | Text is split across multiple runs (common in templated docx) | Iterate all runs per paragraph; use paragraph-level text replacement instead of per-run |
| Document corrupt in Word | OPC package structure broken; invalid XML in custom elements | Validate with python-docx's built-in validation; avoid raw lxml that creates invalid OPC relationships |
| Images stretched or cropped | Aspect ratio not preserved; page margins clip the image | Always specify at most one dimension (width OR height); use Inches for predictable sizing |
| Batch generation slows down | Loading template fresh for each file is I/O-bound | Cache Document objects; use multiprocessing for independent files |
| Font not rendering on other machines | Font is not embedded or not installed on target system | Use web-safe fonts (Calibri, Arial, Times New Roman); embed fonts via XML for critical branding |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Document Automation Service | 2-4 weeks | Build custom docx generators for law firms, real estate agencies, and HR departments. Charge $500-2,000 per automation pipeline. |
| Template Marketplace | 4-8 weeks | Create and sell premium .docx template collections (proposals, invoices, reports) on platforms like Creative Market or Gumroad. $10-50 per template. |
| SaaS Document Platform | 3-6 months | Web app where users upload data and get formatted documents. Monthly subscription ($29-99/mo) with usage tiers. |
| Batch Processing API | 1-2 months | REST API that accepts JSON data and returns formatted .docx. Charge per-document ($0.50-2.00) or monthly retainer. |
| Consulting + Integration | 2-8 weeks | Enterprise integration projects connecting docx generation to CRM/ERP systems. $5,000-15,000 per engagement. |
| Educational Content | Ongoing | Tutorials, video courses, and ebooks on programmatic document generation. $20-100 per course. |

## Process

### Stewardship

- Version-control both templates and generation scripts — a broken template produces broken documents
- Test generated documents on both Word and LibreOffice before client delivery
- Maintain a style guide document that defines font choices, color palette, spacing, and logo usage
- Log all generated documents with metadata (timestamp, input data hash, template version) for audit trails
- Archive old document versions for at least 90 days for compliance purposes

## Verification

- [ ] Document opens without errors in Word/LibreOffice
- [ ] All styles applied correctly (headings, body text, lists)
- [ ] Tables render with proper formatting, merged cells, and alignment
- [ ] Images display at correct size and position
- [ ] Headers/footers show on all pages with correct page numbers
- [ ] Placeholder values replaced correctly (no {{}} tags left visible)
- [ ] Section breaks produce correct page orientation (portrait/landscape)
- [ ] File size is reasonable for the content (no embedded bloat)
- [ ] Metadata fields (author, title, subject) populated correctly
