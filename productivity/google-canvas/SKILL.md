---
name: google-canvas
description: Use when creating, opening, reading, editing, or collaborating on Google Canvas documents and Gemini Canvas shared
  applications through browser automation.
domain: productivity
tags:
- canvas
- google
- productivity
- time-management
- tools
---
persona:
  name: "Domain Expert"
  title: "Master of Google Canvas"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Google Canvas Skill

## Overview

Full lifecycle Google Canvas and Gemini Canvas automation — create new documents, open shared canvases by URL, interact with embedded applications, read content, edit existing documents, manage collaboration, and handle permissions. Supports both traditional Canvas documents and Gemini-powered interactive applications.

**Access**: 
- Google Canvas: `canvas.google.com`
- Gemini Canvas: `gemini.google.com/share/{id}`

## When to Use

- Create new Google Canvas documents (doc, sheet, code, data)
- Open and interact with Gemini Canvas shared applications
- Read content from Canvas documents or embedded apps
- Edit existing Canvas content (append, replace, modify)
- Collaborate on shared canvases (comment, suggest)
- Extract data from Canvas documents
- Interact with AI-powered applications in Gemini Canvas
- Manage sharing permissions

## When NOT to Use

- Traditional Google Docs/Sheets/Slides at `docs.google.com` (use `productivity/google-workspace`)
- When you need direct API access (use Google Workspace MCP)
- Simple text editing (use local files instead)

---

## Gemini Canvas Shared Applications
This section covers gemini canvas shared applications for the google-canvas skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Overview

Gemini Canvas can host interactive AI-powered applications accessible via share links. These apps run in iframes and provide specialized functionality beyond traditional documents.

### Accessing Shared Applications

**URL Pattern**: `https://gemini.google.com/share/{share-id}`

**Login Workflow**:
```javascript
// 1. Navigate to shared URL
window.location.href = 'https://gemini.google.com/share/e5bf9afa6676';

// 2. Wait for page load
await new Promise(r => setTimeout(r, 3000));

// 3. Focus iframe (app runs in cross-origin iframe)
const centerX = window.innerWidth / 2;
const centerY = window.innerHeight / 2;
// Click center to focus iframe

// 4. Tab to input field
// Press Tab key

// 5. Enter email
// Type email address

// 6. Submit
// Press Enter
```

**Common Login Elements**:
- Email input field (usually centered)
- Submit button or Enter key submission
- Verification/loading screen
- Dashboard after successful login

### Example: Affiliate GO Foto Studio

**Tested Application**: AI-powered photo studio for affiliate marketing content generation.

**Interface Structure**:

#### Sidebar Navigation
- **Beranda (Home)**: Dashboard with AI Assistant
- **Membuat Model**: AI model generation from photos
- **Mockup Studio**: Product visualization templates
- **POV Tangan**: Hand-holding product shots
- **Foto Touring**: Travel/car-themed staging
- **POV Mirror Selfie**: Mirror-style product shots
- **Foto Produk Affiliate**: Professional product staging
- **Affiliate Islami**: Ramadan/Lebaran themed content

#### Header Elements
- **Cici Button**: AI Assistant chatbot toggle
- **Logout Button**: End session
- **Collapse Sidebar**: Expand workspace

### Interaction Patterns for Embedded Apps

#### Navigation
```javascript
// Click sidebar items (approximate coordinates)
// Sidebar is ~15% of viewport width (~250px on 1710px screen)

// Example: Click "Mockup Studio"
const sidebarX = 100; // Left sidebar area
const mockupY = 500; // Approximate Y position
// Click at (sidebarX, mockupY)
```

#### Content Generation Workflow
```
1. Select Module
   - Click sidebar item (e.g., "Mockup Studio")
   
2. Upload Content
   - Find upload zone (dashed rectangle)
   - Click or drag-and-drop file
   - Supported: PNG, JPG, HEIC (max 10MB)
   
3. Configure Settings
   - Model/Template selection
   - Aspect ratio: 1:1, 16:9, 3:4, 9:16
   - Theme selection
   
4. Generate
   - Click primary action button
   - Example: "Generate 7 Mockup"
   
5. View Results
   - Results appear in "Hasil" (Result) panel
   - Download or save generated content
```

#### AI Assistant (Cici)
```javascript
// Toggle AI assistant
// Click "Cici" button in header (top-right area)
// Approximate coordinates: X=905, Y=115

// Use for:
// - Creative suggestions
// - Prompt refinement
// - Troubleshooting
// - Feature guidance
```

### Technical Considerations

**Cross-Origin Iframes**:
- Apps run in `shim.html` iframes
- Direct DOM access limited
- Use pixel-based clicking or keyboard navigation
- Focus iframe before interactions

**Element Selectors**:
```javascript
// Since iframe is cross-origin, use coordinate-based clicking
// or keyboard navigation

// Focus iframe
click(centerX, centerY);

// Tab navigation
pressKey('Tab');

// Type in focused field
type('text content');

// Submit
pressKey('Enter');
```

**File Uploads**:
- Handle via browser file picker
- Drag-and-drop simulation
- Upload zones are large dashed rectangles

---

## Google Canvas Documents
This section covers google canvas documents for the google-canvas skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


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

## Complete Automation Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Example 1: Access Gemini Canvas App

```javascript
// Complete workflow: Open shared app and navigate
async function accessGeminiCanvasApp(shareUrl, loginEmail) {
  // 1. Navigate to shared URL
  window.location.href = shareUrl;
  await new Promise(r => setTimeout(r, 5000));
  
  // 2. Focus iframe
  const centerX = window.innerWidth / 2;
  const centerY = window.innerHeight / 2;
  // Click center to focus
  
  // 3. Tab to email input
  // Press Tab
  
  // 4. Enter email
  // Type loginEmail
  
  // 5. Submit
  // Press Enter
  
  // 6. Wait for dashboard load
  await new Promise(r => setTimeout(r, 5000));
  
  return 'App loaded successfully';
}

// Usage
await accessGeminiCanvasApp(
  'https://gemini.google.com/share/e5bf9afa6676',
  'user@gmail.com'
);
```

### Example 2: Generate Content in Embedded App

```javascript
// Workflow: Upload and generate in Affiliate GO
async function generateMockup(productImagePath) {
  // 1. Click Mockup Studio in sidebar
  // Click at (100, 500)
  
  // 2. Wait for module to load
  await new Promise(r => setTimeout(r, 2000));
  
  // 3. Upload product image
  // Click upload zone or use file picker
  // Upload productImagePath
  
  // 4. Select template (e.g., "Manekin")
  // Click template button
  
  // 5. Choose aspect ratio (e.g., 1:1)
  // Click aspect ratio button
  
  // 6. Generate
  // Click "Generate 7 Mockup" button
  
  // 7. Wait for generation
  await new Promise(r => setTimeout(r, 30000));
  
  // 8. Download results
  // Right-click generated images and save
  
  return 'Mockups generated successfully';
}
```

---

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |


### Common Issues

**Issue**: Cannot access iframe content
- **Cause**: Cross-origin restrictions
- **Solution**: Use pixel-based clicking or keyboard navigation

**Issue**: Login not working
- **Cause**: Input field not focused
- **Solution**: Click center of page first, then Tab to input

**Issue**: Sidebar navigation not responding
- **Cause**: Page not fully loaded
- **Solution**: Wait 5-10 seconds after page load

**Issue**: Upload not working
- **Cause**: File picker requires user interaction
- **Solution**: Use browser automation file upload methods

**Issue**: Generated content not appearing
- **Cause**: Generation takes time
- **Solution**: Wait 30-60 seconds for AI processing

**Issue**: "You need access" message
- **Cause**: Not logged in or no permissions
- **Solution**: Login with authorized email address

---

## URL Patterns

| Action | URL |
|--------|-----|
| Google Canvas Home | `https://canvas.google.com` |
| Canvas Document | `https://canvas.google.com/doc/{id}` |
| Gemini Canvas Shared App | `https://gemini.google.com/share/{id}` |
| New Canvas Document | Create via UI from home page |

---

## Integration with Other Skills

- `productivity/google-flow` — For video generation workflows
- `content/gemini-image-generator` — For image generation
- `marketing/content-creator` — Canvas as content drafting tool
- `marketing/ads-manager` — Canvas for campaign planning docs
- `research/mckinsey-research` — Canvas for strategy deliverables

---

## Best Practices
This section covers best practices for the google-canvas skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### For Gemini Canvas Apps

1. **Always wait for iframe load**: 5-10 seconds after navigation
2. **Focus iframe first**: Click center before interactions
3. **Use keyboard navigation**: Tab, Enter for cross-origin iframes
4. **Handle file uploads carefully**: May require automation-specific methods
5. **Wait for AI generation**: 30-60 seconds for content generation
6. **Download immediately**: Results may be session-based

### For Google Canvas Documents

1. **Wait for content load**: Canvas loads asynchronously
2. **Check permissions**: Verify editor access before attempting edits
3. **Use keyboard shortcuts**: Faster than clicking for common actions
4. **Auto-save is automatic**: No manual save needed
5. **Test with small edits first**: Verify access and functionality

---

**Last Updated**: 2026-02-16  
**Tested**: ✅ Gemini Canvas shared app (Affiliate GO Foto Studio)  
**Features**: Login workflow, sidebar navigation, content generation, AI assistant

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Automation creates duplicate entries across connected platforms
- Agent does not handle timezone differences correctly
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] No duplicate entries are created across connected platforms
- [ ] Timezone handling is correct for all scheduling operations
- [ ] All required outputs generated
- [ ] Success criteria met

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
