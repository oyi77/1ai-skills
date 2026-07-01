---
name: pdf-creator
description: Create, edit, and extract text from PDF documents. Generate reports, invoices, and forms. Parse existing PDFs for data extraction.
domain: content
tags:
- documents
- pdf
- reports
- invoices
- extraction
---

# Pdf Creator

## When to Use
**Trigger phrases:**
- "pdf creator"
- "Create, edit, and extract text from PDF documents"


- When generating PDF reports, invoices, or certificates
- When extracting text or data from existing PDFs
- When converting other document formats to PDF
- When filling PDF forms programmatically

## When NOT to Use

- For editable documents (use `docx-creator`)
- For simple text output (use markdown)
- For scanned image PDFs without OCR (add OCR step first)

## Overview

Full PDF lifecycle support — creation, editing, extraction, and form filling. Uses ReportLab (Python) or pdf-lib (Node.js) for generation, PyPDF2/pdf-parse for extraction.

## Workflow

1. **Define layout** — Page size, margins, orientation
2. **Add elements** — Text, images, tables, shapes, charts
3. **Apply styling** — Fonts, colors, borders, backgrounds
4. **Add metadata** — Title, author, keywords, encryption
5. **Export/Extract** — Save PDF or parse existing one

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Screenshots work for reports" | PDFs are searchable, accessible, and professional |
| "I'll just print to PDF" | Programmatic PDFs are reproducible and data-driven |
| "PDFs are hard to generate" | Modern libraries (ReportLab, pdf-lib) make it straightforward |

## Code Example (Python)

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas('invoice.pdf', pagesize=A4)
c.setFont('Helvetica-Bold', 24)
c.drawString(100, 750, 'Invoice #2026-001')

c.setFont('Helvetica', 12)
c.drawString(100, 700, 'Client: Acme Corp')
c.drawString(100, 680, 'Amount: $15,000.00')
c.drawString(100, 660, 'Due: 2026-07-15')

c.save()
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run pdf creator workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] PDF opens without errors in all readers
- [ ] Text is selectable (not rasterized)
- [ ] Fonts render correctly
- [ ] Page breaks in correct positions
- [ ] Metadata (title, author) is set

