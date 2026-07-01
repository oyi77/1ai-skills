---
name: docx-creator
description: Create, edit, and analyze Word documents programmatically using python-docx or docx.js. Generate reports, proposals, and templates with formatting, tables, images, and styles.
domain: content
tags:
- documents
- word
- docx
- office
- reports
- templates
---

# Docx Creator

## When to Use
**Trigger phrases:**
- "docx creator"
- "Create, edit, and analyze Word documents programmatically using python-docx or d"


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

1. **Define structure** — Outline document sections, headings, and content blocks
2. **Set up styles** — Configure fonts, colors, spacing, and page layout
3. **Add content** — Insert text, tables, images, and lists with proper formatting
4. **Apply formatting** — Set headers/footers, page numbers, table of contents
5. **Export** — Save as .docx with proper file naming

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Plain text is fine for reports" | Professional documents need formatting — headers, tables, styles matter for credibility |
| "I'll just use copy-paste" | Programmatic generation is reproducible, version-controlled, and scalable |
| "Word is outdated" | .docx is still the business standard for contracts, proposals, and formal documents |

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

## Verification

- [ ] Document opens without errors in Word/LibreOffice
- [ ] All styles applied correctly
- [ ] Tables render with proper formatting
- [ ] Images display at correct size
- [ ] Headers/footers show on all pages

