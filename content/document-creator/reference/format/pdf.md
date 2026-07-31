---
name: pdf-creator
description: Create, edit, and extract text from PDF documents. Generate reports, invoices, and forms. Parse existing PDFs for data extraction.
domain: content
author: mahipal
license: Apache-2.0
subdomain: content-creation
tags:
- documents
- pdf
- reports
- invoices
- extraction
version: 1.0.0
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

Full PDF lifecycle support — creation, editing, extraction, and form filling. Covers both generation (building PDFs from scratch) and manipulation (merging, splitting, annotating existing files).

**Python stack:** ReportLab for generation (full layout control, vector graphics), PyPDF2/pdfplumber for extraction, pdfrw for form filling.
**Node.js stack:** pdf-lib for generation and manipulation (zero dependencies), pdf-parse for text extraction, jspdf for browser-side generation.

Key capabilities: multi-page documents with headers/footers, tables with dynamic data, embedded images and barcodes, digital signatures, password encryption, and programmatic form filling.

## Workflow

1. **Choose the right library** — ReportLab (Python) for complex layouts, pdf-lib (Node.js) for serverless, PyPDF2/pdfplumber for extraction. Match the library to your deployment environment.
2. **Define layout** — Set page size (A4, Letter, custom), margins, orientation. Sketch header/footer regions and content areas. For multi-page documents, plan where page breaks occur.
3. **Build content structure** — Add pages, set up coordinate system (bottom-left origin in ReportLab, top-left in pdf-lib). Define reusable styles for headings, body text, tables.
4. **Add elements** — Draw text at specific coordinates, embed images (PNG for diagrams, JPEG for photos), construct tables from data arrays, include vector shapes and barcodes.
5. **Apply styling** — Set fonts (embed custom `.ttf` if needed), apply colors (RGB/CMYK), add borders and backgrounds to elements. Ensure consistent spacing.
6. **Add metadata & security** — Set title, author, subject, keywords. Apply 128-bit AES encryption for password-protected documents. Add digital signatures if required.
7. **Export or extract** — Save to file or buffer. For extraction: open the PDF, iterate pages, extract text by region or as full page text. Handle tables with pdfplumber for structured data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Screenshots work for reports" | PDFs are searchable, accessible, and professional |
| "I'll just print to PDF" | Programmatic PDFs are reproducible and data-driven |
| "PDFs are hard to generate" | Modern libraries (ReportLab, pdf-lib) make it straightforward |
| "A CSV file is enough for data" | PDF reports convey structure, hierarchy, and branding |
| "I only need the Python library" | Node.js (pdf-lib) works server-side and in-browser, expanding deployment options |
| "Extraction doesn't need testing" | PDF layouts vary wildly; always validate extraction output against ground truth |

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

## Code Example (Node.js)

```javascript
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

const doc = await PDFDocument.create();
const page = doc.addPage([595.28, 841.89]); // A4 in points
const font = await doc.embedFont(StandardFonts.HelveticaBold);

page.drawText('Invoice #2026-001', {
  x: 100, y: 750, size: 24, font,
});
page.drawText('Client: Acme Corp', { x: 100, y: 700, size: 12 });
page.drawText('Amount: $15,000.00',   { x: 100, y: 680, size: 12 });
page.drawText('Due: 2026-07-15',      { x: 100, y: 660, size: 12 });

const pdfBytes = await doc.save();
```

## Setup & Configuration

**Python environment:**
```bash
pip install reportlab pypdf2 pdfplumber pdfrw
```

**Node.js environment:**
```bash
npm install pdf-lib pdf-parse
```

For custom fonts, download `.ttf` files and register them:
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('CustomFont', 'path/to/font.ttf'))
```

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Text is not selectable / rasterized | The PDF contains images, not text. Use a text-based library (ReportLab, pdf-lib) rather than screenshot-to-PDF converters |
| Fonts render incorrectly on another system | Embed fonts using `pdfmetrics.registerFont` (ReportLab) or embed font data in pdf-lib |
| Large file size | Compress images before embedding; use JPEG for photos (compression=0.5-0.8) and PNG for diagrams |
| Unwanted page breaks | Calculate content height before drawing; use `Frame` objects in ReportLab for automatic flow |
| Extraction returns garbled text | Try `pdfplumber` instead of PyPDF2 — it handles more complex layouts |
| Form fields not fillable after merge | Use `pdfrw` for form preservation; not all merge tools retain AcroForm fields |

## Monetization

- **Invoice automation service** — Generate branded invoices for small businesses ($50-200/setup + monthly)
- **Certificate/credential generator** — Bulk PDF certificate creation for course platforms and event organizers
- **PDF data extraction API** — Offer as a micro-SaaS: upload PDF → structured JSON ($0.10-0.50/page)
- **Report builder add-on** — Integrate PDF generation into existing SaaS products as a premium feature
- **Form filler service** — Automate government/banking form filling with data extraction and validation

## Process

1. **Environment setup** — Install libraries: `pip install reportlab pypdf2 pdfplumber pdfrw` (Python) or `npm install pdf-lib pdf-parse` (Node.js). Set up font files if using custom typefaces.
2. **Template design** — Sketch the document layout (page size, margins, header/footer regions, table positions). For data-driven documents, map data fields to coordinates.
3. **Content assembly** — Build the document programmatically: add static elements (logo, letterhead), populate dynamic data (tables, fields), apply styling.
4. **Quality check** — Open in multiple PDF readers (Acrobat, browser, mobile). Verify text is selectable, fonts render, links work, page breaks are correct.
5. **Delivery** — Save with appropriate metadata and encryption. If extracting: verify extracted text matches expected content.

## Verification

- [ ] PDF opens without errors in all readers (Acrobat, Chrome, mobile)
- [ ] Text is selectable and copyable (not rasterized)
- [ ] Fonts render correctly (all embedded if custom)
- [ ] Page breaks fall in correct positions
- [ ] Metadata (title, author, subject, keywords) is set
- [ ] Encryption password protects sensitive content where required
- [ ] Table of contents / internal links work correctly
- [ ] File size is reasonable for the content
