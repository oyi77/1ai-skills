# google-canvas Skill

> **Framework Agnostic** - This skill works with ANY AI agent (OpenCode, OpenClaw, Claude Desktop, custom agents, etc.)
> 
> **How to Use**: Read this file and follow the instructions. No special loading required.

## What It Does

Google Canvas workspace automation - create documents, spreadsheets, presentations, and automate document workflows through browser.

## When to Use

- Create Google Docs, Sheets, Slides
- Automate document workflows
- Extract data from existing Canvas documents
- Real-time collaboration
- Generate reports and dashboards

## Key Capabilities

- **Document Creation**: Docs, Sheets, Slides via browser
- **Data Extraction**: Pull data from existing documents
- **Workflow Automation**: Multi-step document processes
- **Template Management**: Reusable document templates
- **Collaboration**: Share and manage permissions

## Browser Workflow

### Create Document via Google Canvas

1. Navigate: https://canvas.google.com
2. Click: "New" button
3. Select: document type (doc/sheet/slide)
4. Fill: content via prompts
5. Save: with proper naming
6. Share: set permissions

### Extract Data from Spreadsheet

1. Navigate: https://canvas.google.com
2. Open: target spreadsheet
3. Select: data range
4. Copy: to clipboard
5. Parse: into structured format
6. Save: to local storage

## Usage Examples

### Create Q1 Report
```
User: "Create a Q1 report in Google Sheets"
Skill: Opens Canvas → creates new sheet → populates template → saves
```

### Generate Meeting Notes Doc
```
User: "Create meeting notes document for today's standup"
Skill: Creates Google Doc → adds agenda template → shares with team
```

### Build Dashboard
```
User: "Create a sales dashboard in Google Sheets"
Skill: Creates sheet → adds charts → links to data sources → shares
```

## Skills It Coordinates

- `agent-browser` - Browser automation
- `google-workspace` MCP (when available) - Direct API integration

## Files Created

- `canvas-templates/` - Reusable document templates
- `canvas-output/` - Generated documents
