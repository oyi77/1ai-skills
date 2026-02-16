---
name: google-canvas
description: Use when creating, opening, reading, editing, or collaborating on Google Canvas documents through browser automation.
---

# Google Canvas Skill

## Overview

Full lifecycle Google Canvas automation — create new documents, open shared canvases by URL, read content, edit existing documents, manage collaboration, and handle permissions. All via browser at `canvas.google.com`.

## When to Use

- Create new Google Canvas documents (doc, sheet, code, data)
- Open and read shared Canvas documents by URL
- Edit existing Canvas content (append, replace, modify)
- Collaborate on shared canvases (comment, suggest)
- Extract data from Canvas documents
- Manage sharing permissions

## When NOT to Use

- Traditional Google Docs/Sheets/Slides at `docs.google.com` (use google-workspace)
- When you need direct API access (use Google Workspace MCP)
- Simple text editing (use local files instead)

## Quick Reference

| Action | URL Pattern |
|--------|-------------|
| Home | `canvas.google.com` |
| New doc | Click "+ New" → select type |
| Open shared | `canvas.google.com/doc/{document-id}` |
| Open by link | Paste shared URL in browser |

## Common Mistakes

- Confusing Google Canvas (`canvas.google.com`) with Google Docs (`docs.google.com`) — they are different products
- Not waiting for content to fully load before reading
- Trying to edit without proper permissions (viewer vs editor)
- Not handling auth prompts when opening shared documents
- Forgetting to save/sync before navigating away

---

## Core Workflows

### 1. Create New Canvas Document

```
1. Navigate: https://canvas.google.com
2. Click: "+ New" or "Create new" button
3. Select canvas type:
   - Document (rich text)
   - Spreadsheet (data/tables)
   - Code (programming)
4. Wait for editor to load
5. Enter content via the prompt/input area
6. Title: Click the untitled document name → type title
7. Verify: Content renders correctly
```

**Canvas Types:**
| Type | Best For |
|------|----------|
| Document | Reports, notes, articles, plans |
| Spreadsheet | Data analysis, tables, dashboards |
| Code | Programming, scripts, technical docs |

### 2. Open Shared Canvas by URL

```
1. Navigate to the shared URL:
   - Format: https://canvas.google.com/doc/{document-id}
   - Or: Use the full sharing link from the owner
2. Handle auth if prompted:
   - If login required → Sign in with Google account
   - If permission denied → Request access (click "Request access" button)
3. Wait for document to fully load (check for content area)
4. Identify your access level:
   - Viewer: Can read, cannot edit
   - Commenter: Can read and add comments
   - Editor: Full read/write access
```

**Troubleshooting access:**
- "You need access" → Click "Request access" → owner must approve
- "Sign in required" → Authenticate with correct Google account
- "Document not found" → URL may be incorrect or document deleted
- Blank page → Wait longer, Canvas content loads asynchronously

### 3. Read Content from Canvas

```
1. Open the Canvas document (new or shared)
2. Wait for content to fully render
3. Select all content:
   - Keyboard: Cmd+A (Mac) / Ctrl+A (Windows)
   - Or: Manually select specific sections
4. Copy content:
   - Keyboard: Cmd+C / Ctrl+C
   - Parse clipboard content
5. For structured data (spreadsheets):
   - Identify cell ranges
   - Read row by row
   - Extract headers separately
```

**Reading specific sections:**
- Scroll to target section
- Use search (Cmd+F) to find specific text
- Screenshot for visual content (charts, images)

### 4. Edit Existing Canvas

**Prerequisites:** Must have Editor access.

#### Append Content
```
1. Open the Canvas document
2. Click at the end of existing content
3. Type or paste new content
4. Verify content appears correctly
5. Changes auto-save
```

#### Replace/Modify Content
```
1. Open the Canvas document
2. Find target text:
   - Cmd+F → search for text to modify
   - Or: Scroll to target section
3. Select the text to replace:
   - Click and drag to select
   - Or: Double-click for word, triple-click for paragraph
4. Type replacement content
5. Verify modification
6. Changes auto-save
```

#### Insert at Specific Position
```
1. Open the Canvas document
2. Click at the desired insertion point
3. Type or paste content
4. Verify positioning is correct
```

### 5. AI-Assisted Editing (Canvas AI Features)

Google Canvas has built-in AI capabilities:

```
1. Open Canvas document
2. Select text you want AI to work with
3. Look for AI action buttons:
   - "Help me write" / "Suggest" / AI sparkle icon
4. Enter your instruction (e.g., "Make this more concise")
5. Review AI suggestion
6. Accept or reject the suggestion
7. Verify final content
```

### 6. Collaboration & Sharing

#### Share a Document
```
1. Open the Canvas document
2. Click "Share" button (top-right area)
3. Enter email addresses or generate link
4. Set permission level:
   - Viewer: Can only read
   - Commenter: Can read and comment
   - Editor: Full access
5. Click "Send" or "Copy link"
```

#### Add Comments
```
1. Open shared Canvas document (need Commenter+ access)
2. Select the text you want to comment on
3. Click comment icon (or Cmd+Option+M)
4. Type your comment
5. Click "Comment" to post
```

#### Resolve Comments
```
1. Click on the comment thread
2. Read the discussion
3. Click "Resolve" to close the thread
4. Or reply with additional context
```

### 7. Export & Download

```
1. Open the Canvas document
2. Look for menu/settings (three dots or File menu)
3. Select export format:
   - PDF
   - Plain text
   - HTML
4. Download to local storage
```

---

## URL Patterns

| Action | URL |
|--------|-----|
| Home/Dashboard | `https://canvas.google.com` |
| Specific document | `https://canvas.google.com/doc/{id}` |
| New document | Create via UI from home page |

## Integration with Other Skills

- `google-flow` — For video generation workflows
- `content-creator` — Canvas as content drafting tool
- `marketing` — Canvas for campaign planning docs
- `mckinsey-research` — Canvas for strategy deliverables

## Files

- `canvas-templates/` — Reusable document templates
- `canvas-output/` — Downloaded/exported documents
