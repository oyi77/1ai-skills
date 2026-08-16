---
name: document-creator
description: Use when creating, editing, and generating Office documents programmatically
  — Word, PowerPoint, Excel, and PDF. One interface for all document formats with
  shared methodology.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- documents
- office
- docx
- pptx
- xlsx
- pdf
- automation
- reports
version: 2.0.0
category: content
---




# Document Creator

Generate professional Office documents programmatically across all major formats. Each format has dedicated reference files with library-specific code, but the workflow is shared:

## Overview

| Format | Library (Python) | Library (Node.js) | Reference |
|--------|-----------------|-------------------|-----------|
| **Word** (.docx) | python-docx | docx | [reference/format/docx.md](./reference/format/docx.md) |
| **PowerPoint** (.pptx) | python-pptx | pptxgenjs | [reference/format/pptx.md](./reference/format/pptx.md) |
| **Excel** (.xlsx) | openpyxl / xlsxwriter | exceljs / xlsx | [reference/format/xlsx.md](./reference/format/xlsx.md) |
| **PDF** (.pdf) | fpdf2 / reportlab | pdfkit / jspdf | [reference/format/pdf.md](./reference/format/pdf.md) |

## Workflow

1. **Define structure** — Plan document sections, sheets, slides, or pages
2. **Choose format** — Select the right format for the audience (Word for contracts, PPTX for presentations, XLSX for data, PDF for distribution)
3. **Load data** — From JSON, CSV, database, or API
4. **Generate** — Use the format-specific reference for exact API calls
5. **Validate** — Check output opens cleanly in the target application
6. **Deliver** — Save or stream to client

## When to Use

| Need | Format |
|------|--------|
| Contracts, proposals, reports | **Word** (.docx) |
| Meeting decks, pitches | **PowerPoint** (.pptx) |
| Financial models, data tables | **Excel** (.xlsx) |
| Distribution, printing, archiving | **PDF** |
| Bulk personalized documents | **Word** + mail merge |
| Charts with live data | **Excel** or **PowerPoint** |
| Invoice generation | **PDF** or **Word** |



## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll just use one library for everything" | Each format has different semantics — one library can't do it all | Use the right library per format (python-docx, python-pptx, openpyxl, fpdf2) |
| "Manual document creation is fine" | Manual creation doesn't scale and introduces errors | Programmatic generation ensures consistency and version control |
| "PDF generation is too complex" | fpdf2 and reportlab handle complex layouts well | Invest in learning the library; it pays off on every document |


| Need | Format |
|------|--------|
| Contracts, proposals, reports | **Word** (.docx) |
| Meeting decks, pitches | **PowerPoint** (.pptx) |
| Financial models, data tables | **Excel** (.xlsx) |
| Distribution, printing, archiving | **PDF** |
| Bulk personalized documents | **Word** + mail merge |
| Charts with live data | **Excel** or **PowerPoint** |
| Invoice generation | **PDF** or **Word** |

## Provider Reference

Load format-specific reference files for exact API usage, code examples, and troubleshooting.
## Process

1. **Define structure** — Plan document sections, sheets, slides, or pages
2. **Choose format** — Select the right format for the audience (Word for contracts, PPTX for presentations, XLSX for data, PDF for distribution)
3. **Load data** — From JSON, CSV, database, or API
4. **Generate** — Use the format-specific reference for exact API calls
5. **Validate** — Check output opens cleanly in the target application
6. **Deliver** — Save or stream to client

## Verification Checklist

- [ ] Output opens correctly in target application (Word, PowerPoint, Excel, PDF viewer)
- [ ] All data populated correctly without truncation
- [ ] Formatting matches specifications (fonts, colors, layout)
- [ ] File size is reasonable for distribution
- [ ] Cross-platform compatibility verified
