---
name: claude-office-skills
description: Use when you need practical office/business skills for Claude - contracts, HR, finance, PDF, documents, presentations, workflows, CRM, marketing, e-commerce, project management, data engineering. 137 ready-to-use skills across 20+ categories. Zero setup - copy SKILL.md into any Claude conversation.
category: integrations
domain: integrations
tags:
  - office-automation
  - document-processing
  - contract-review
  - hr-automation
  - finance-automation
  - pdf-tools
  - presentation-generation
  - workflow-automation
  - claude-skills
version: 1.0.0
---

# Claude Office Skills: 137 Practical Business Skills for Claude

A curated collection of practical Claude Skills for real-world office tasks. Zero setup required - just copy a skill's SKILL.md into your Claude conversation.

---

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll just prompt Claude directly" | Generic prompts miss domain-specific workflows and edge cases | Skills embed professional knowledge: risk patterns, completeness checklists, jurisdiction rules |
| "Writing prompts is faster" | Reusable skills save hours on repeated tasks; one skill = infinite uses | Invest 5 min to install, save hours every time |
| "My documents are too unique" | Skills are templates - you provide the document, skill provides the methodology | Skills work on YOUR documents, not toy examples |
| "I don't need legal/finance expertise in AI" | AI hallucinates on legal/finance; skills embed guardrails (risk patterns, checklists) | Use skills for high-stakes docs; generic prompts for low-stakes |
| "Official Anthropic skills are enough" | Official skills cover DOCX/XLSX/PPTX/PDF basics only; this adds 130+ business workflows | Use official for format ops, these for business logic |

---

## When to Use

**Use when you need Claude to:**

- **Legal/Contracts**: Review contracts for risks, generate NDAs, check completeness against 19-item checklist, apply jurisdiction-specific rules (US, China, EU, California)
- **HR/Careers**: Tailor resumes, write cover letters, create job descriptions, generate offer letters, screen applicants
- **Finance/Business**: Create invoices, organize expenses, build DCF valuations, financial models, investment memos, SaaS metrics
- **PDF Power Tools**: Chat with PDFs, convert formats, OCR scanned docs, merge/split, fill forms, compress, watermark
- **Document Processing**: Create/edit Word, Excel, PowerPoint via python-docx, python-pptx, openpyxl, xlwings, pdfplumber
- **Presentations**: Generate HTML slides (reveal.js), dev slides (slidev), MD slides (marp), AI-powered slides
- **Templates**: Build CVs (rendercv), forms (docassemble), contracts (accord-project), invoices (docxtpl)
- **Workflows**: n8n (172k★, 7800 templates), MCP servers, batch processing, document pipelines
- **CRM/Sales**: HubSpot/Salesforce/Pipedrive automation, lead routing, customer success
- **Marketing**: Google/Meta/TikTok/LinkedIn/Twitter ads, Mailchimp, SEO, social publishing
- **E-commerce**: Shopify, WooCommerce, Amazon seller automation
- **Communication**: Slack/Teams/Discord/Telegram/WhatsApp/Twilio automation
- **Project Management**: Jira/Asana/Monday/Linear/Trello/ClickUp/Notion/Airtable automation
- **Data Engineering**: ETL, database sync, Google Sheets/Gmail/Calendar automation
- **Research**: Deep research, web search, academic search, competitive analysis, news monitoring

---

## Quick Start

### Option 1: Install All 137 Skills (Moltbot/ClawdBot)
```bash
# Install ALL skills
curl -fsSL https://raw.githubusercontent.com/claude-office-skills/skillz/main/install.sh | bash

# Install by category
curl -fsSL https://raw.githubusercontent.com/claude-office-skills/skillz/main/install.sh | bash -s -- --category legal
curl -fsSL https://raw.githubusercontent.com/claude-office-skills/skillz/main/install.sh | bash -s -- --category pdf
curl -fsSL https://raw.githubusercontent.com/claude-office-skills/skillz/main/install.sh | bash -s -- --category workflow

# Available categories: legal, hr, finance, pdf, workflow, template, doc, conversion, parsing, slide, productivity, marketing
```

### Option 2: Single Skill via Direct Link
```
Use this skill: https://raw.githubusercontent.com/claude-office-skills/skillz/main/contract-review/SKILL.md

Then review my contract: [upload file]
```

### Option 3: Copy-Paste into Any Claude Conversation
1. Click any skill link on the [GitHub repo](https://github.com/claude-office-skills/skills)
2. Copy the SKILL.md content
2. Paste into Claude.ai, Claude Code, or API system prompt
3. Upload your document and ask for help

### Option 4: API Integration
```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")
skill_content = open("contract-review/SKILL.md").read()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=skill_content,
    messages=[{"role": "user", "content": "Review this contract..."}]
)
```

---

## Skill Categories (137 Skills)

### Legal & Contracts
| Skill | Description |
|-------|-------------|
| `contract-review` | Analyze contracts for risks, check completeness, get recommendations |
| `nda-generator` | Create professional NDAs for different scenarios |

### HR & Careers
| Skill | Description |
|-------|-------------|
| `resume-tailor` | Optimize resume for specific job applications |
| `cover-letter` | Write compelling, personalized cover letters |
| `job-description` | Create clear, inclusive job postings |
| `offer-letter` | Generate professional employment offers |
| `applicant-screening` | Screen candidates against job requirements |

### Finance & Business
| Skill | Description |
|-------|-------------|
| `invoice-generator` | Create professional invoices with proper formatting |
| `expense-report` | Organize and summarize business expenses |
| `invoice-organizer` | Organize, categorize, and track invoices |
| `proposal-writer` | Write winning business proposals |
| `stock-analysis` | Stock research & analysis |
| `dcf-valuation` | Discounted cash flow models |
| `financial-modeling` | Build financial models |
| `company-research` | Company deep research |
| `investment-memo` | Write investment memos |
| `crypto-report` | Cryptocurrency analysis |
| `saas-metrics` | MRR, ARR, churn analysis |

### Communication & Writing
| Skill | Description |
|-------|-------------|
| `internal-comms` | Status reports, newsletters, FAQs |
| `doc-coauthoring` | Structured workflow for writing documentation |
| `email-drafter` | Professional email templates and responses |
| `email-classifier` | Auto-categorize emails by type and priority |
| `suspicious-email` | Analyze emails for phishing and scam indicators |

### Productivity
| Skill | Description |
|-------|-------------|
| `meeting-notes` | Transform raw notes into structured summaries |
| `weekly-report` | Create consistent status updates |
| `file-organizer` | Organize and rename files based on content |
| `changelog-generator` | Generate release notes from commits/updates |
| `data-analysis` | Analyze spreadsheet data and generate insights |

### PDF Power Tools (73k+ stars inspiration)
| Skill | Description |
|-------|-------------|
| `chat-with-pdf` | Answer questions, summarize, extract from PDFs |
| `pdf-converter` | Convert PDF to/from Word, Excel, Image formats |
| `pdf-ocr` | Extract text from scanned PDFs using OCR |
| `pdf-merge-split` | Combine or split PDF documents |
| `pdf-form-filler` | Fill out PDF forms programmatically |
| `pdf-compress` | Reduce PDF file size while maintaining quality |
| `pdf-watermark` | Add watermarks, page numbers, headers/footers |

### Document Processing (Official + Community)
| Category | Libraries |
|----------|-----------|
| **Official (Anthropic)** | DOCX, XLSX, PPTX, PDF - source-available |
| **Core** | python-docx (5.4k★), python-pptx (3.2k★), openpyxl (3.8k★), xlwings (3.3k★), pdfplumber (9.6k★) |
| **Conversion** | pandoc (42k★), markitdown (86k★), pdf2docx (3.3k★), marp-cli (3.1k★) |
| **Parsing/OCR** | PaddleOCR (69k★), docling (51.5k★), surya (19k★), unstructured (14k★), camelot (4.2k★) |

### Presentation Skills
| Skill | Library |
|-------|---------|
| `html-slides` | reveal.js (70.5k★) |
| `dev-slides` | slidev (44k★) |
| `md-slides` | marp (3.1k★) |
| `ai-slides` | sli-ai |

### Template Skills
| Skill | Library |
|-------|---------|
| `cv-builder` | rendercv (15.4k★) |
| `form-builder` | docassemble (919★) |
| `contract-template` | accord-project (322★) |
| `invoice-template` | easy-invoice (476★) |
| `template-engine` | docxtpl (2.1k★) |

### Workflow & Automation
| Skill | Description |
|-------|-------------|
| `n8n-workflow` | 7800+ templates, 172k★ |
| `mcp-hub` | 1200+ AI Agent tools, 40k★ |
| `office-mcp` | 39 tools: PDF, Spreadsheet, Document, Conversion, Presentation |
| `batch-processor` | Bulk document processing |
| `doc-pipeline` | Document workflow pipeline |
| `browser-automation` | Puppeteer for scraping & testing |

### CRM & Sales Automation
| Skill | Platform |
|-------|----------|
| `crm-automation` | HubSpot, Salesforce |
| `pipedrive-automation` | Pipedrive |
| `lead-routing` | Multi-platform |
| `customer-success` | Onboarding, health scoring, retention |

### Marketing & Advertising
| Skill | Platform |
|-------|----------|
| `google-ads-manager` | Google |
| `facebook-meta-ads` | FB & Instagram |
| `tiktok-marketing` | TikTok |
| `linkedin-automation` | LinkedIn |
| `twitter-x-automation` | Twitter/X |
| `mailchimp-automation` | Mailchimp |
| `email-marketing` | Multi-platform |
| `seo-optimizer` | SEO strategy |
| `ads-copywriter` | Multi-platform |
| `social-publisher` | Cross-platform |

### E-commerce
| Skill | Platform |
|-------|----------|
| `shopify-automation` | Shopify |
| `woocommerce-automation` | WooCommerce |
| `amazon-seller` | Amazon |

### Communication & Messaging
| Skill | Platform |
|-------|----------|
| `slack-workflows` | Slack |
| `microsoft-teams` | Teams |
| `discord-bot` | Discord |
| `telegram-bot` | Telegram |
| `whatsapp-automation` | WhatsApp |
| `twilio-sms` | Twilio |

### Project Management
| Skill | Platform |
|-------|----------|
| `jira-automation` | Jira |
| `asana-automation` | Asana |
| `monday-automation` | Monday.com |
| `linear-automation` | Linear |
| `trello-automation` | Trello |
| `clickup-automation` | ClickUp |
| `notion-automation` | Notion |
| `airtable-automation` | Airtable |

### Customer Support
| Skill | Platform |
|-------|----------|
| `zendesk-automation` | Zendesk |
| `intercom-automation` | Intercom |

### Data Engineering
| Skill | Use Case |
|-------|----------|
| `etl-pipeline` | Extract, Transform, Load |
| `database-sync` | Cross-database sync |
| `sheets-automation` | Google Sheets |
| `gmail-workflows` | Email automation |
| `calendar-automation` | Scheduling |

### Research & Intelligence
| Skill | Use Case |
|-------|----------|
| `deep-research` | Multi-source deep research |
| `web-search` | Intelligent web search |
| `academic-search` | Scholarly paper research |
| `competitive-analysis` | Competitor research |
| `news-monitor` | News tracking & alerts |

### Visual & Creative
| Skill | Use Case |
|-------|----------|
| `image-generation` | AI image creation |
| `diagram-creator` | Technical diagrams |
| `chart-designer` | Data visualization |
| `infographic` | Infographic design |
| `ppt-visual` | Presentation visuals |

### Media & Content
| Skill | Platform |
|-------|----------|
| `youtube-automation` | YouTube |
| `podcast-automation` | Multi-platform |
| `transcription` | Audio/video transcription |

### Smart Home & IoT
| Skill | Platform |
|-------|----------|
| `home-assistant` | Home Assistant |
| `spotify-automation` | Spotify |
| `weather-automation` | Multi-platform |
| `apple-shortcuts` | iOS/macOS |

### DevOps & Security
| Skill | Use Case |
|-------|----------|
| `devops-automation` | CI/CD & infrastructure |
| `security-monitoring` | Threat detection |

### HR & Operations
| Skill | Department |
|-------|------------|
| `hr-automation` | Recruiting & onboarding |
| `docusign-automation` | E-signature workflows |

### AI & Agents
| Skill | Use Case |
|-------|----------|
| `ai-agent-builder` | Design multi-step AI agents |
| `obsidian-automation` | Knowledge management (PKM) |

---

## Advanced: Office MCP Server (39 Tools)

```bash
cd mcp-servers/office-mcp && npm install && npm run build
```

| Module | Tools | Capabilities |
|--------|-------|--------------|
| PDF | 10 | Extract, merge, split, compress, watermark, forms, OCR |
| Spreadsheet | 7 | Read/write Excel, analyze, formulas, pivot tables |
| Document | 6 | Create/edit Word, templates, merge documents |
| Conversion | 9 | xlsx⇔csv, docx⇔md, json→xlsx, batch convert |
| Presentation | 7 | Create PPT, extract, Markdown→slides, HTML export |

### Extensible Knowledge Base
- **Base**: Universal risk patterns, completeness checklists
- **Jurisdictions**: US Federal, California, China, EU (community-contributed)
- **Domain**: Healthcare, Finance, Government (community-contributed)
- **Custom**: Your company rules, private knowledge (you control)

### Pre-built Agents (5 personas)
| Agent | Role | Key Skills |
|-------|------|------------|
| ⚖️ Legal Specialist | Contract Review | contract-review, nda-generator |
| 📊 Data Analyst | Excel & Finance | data-analysis, dcf-valuation |
| 📋 Admin Assistant | Email & Calendar | email-drafter, meeting-notes |
| 🔬 Research Analyst | Deep Research | deep-research, company-research |
| ✍️ Content Creator | Writing & Marketing | content-writer, seo-optimizer |

---

## Verification Checklist

- [ ] Identify the correct category for your task
- [ ] Install skill via preferred method (all / category / single)
- [ ] Paste SKILL.md into Claude conversation or load via API
- [ ] Upload your document / provide context
- [ ] Verify output against skill's embedded checklists (legal: 19-item completeness, risk patterns)
- [ ] For high-stakes docs: run through multiple relevant skills (contract-review + jurisdiction + risk patterns)

---

## References

- **GitHub Repository**: https://github.com/claude-office-skills/skills
- **Install Script**: https://raw.githubusercontent.com/claude-office-skills/skillz/main/install.sh
- **MCP Server**: https://github.com/claude-office-skills/skillz/tree/main/mcp-servers/office-mcp
- **Knowledge Base**: https://github.com/claude-office-skills/skillz/tree/main/mcp-servers/office-mcp/knowledge
- **Agents**: https://github.com/claude-office-skills/skillz/tree/main/agents
- **License**: MIT
- **Official Docs**: [Claude Skills Overview](https://www.anthropic.com/news/claude-skills), [Creating Custom Skills](https://github.com/claude-office-skills/skillz/blob/main/CONTRIBUTING.md)

---

## Related 1ai-skills

- `document-creator` — Programmatic Office doc generation (Word/PPT/Excel/PDF)
- `pdf-extraction` — Extract text/tables from PDFs (if available in this repo)
- `invoice-automation` — Multi-platform invoicing (if available in this repo)
- `meeting-notes` — Structured meeting summaries (if available in this repo)
- `data-analysis` — Spreadsheet insights (if available in this repo)