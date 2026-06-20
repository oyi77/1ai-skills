---
name: google-workspace
description: Integrate with Google Workspace (Docs, Sheets, Drive, Calendar) using MCP servers
domain: productivity
tags:
- google
- productivity
- time-management
- tools
- workspace
allowed-tools:
- Bash(gcloud:*)
- MCP(google-workspace:*)
- MCP(google-drive:*)
- MCP(google-sheets:*)
- MCP(google-docs:*)
---
persona:
  name: "Domain Expert"
  title: "Master of Google Workspace"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Google Workspace Integration
## When to Use

**Trigger phrases:**
- "google workspace"
- "Help me with google workspace"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Comprehensive Google Workspace integration using MCP servers for Docs, Sheets, Drive, and Calendar.

## Required Tools
| Tool | Purpose | Required |
|------|---------|----------|
| CLI | Primary execution | Yes |
| API client | External service calls | Conditional |
| Validator | Output checking | Recommended |


### MCP Servers

#### Google Workspace MCP

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-workspace"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

#### Google Drive MCP

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-drive"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

#### Google Sheets MCP

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-sheets"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash(gcloud:*)` | Execute gcloud CLI |
| `MCP(google-workspace:*)` | Multi-service access |
| `MCP(google-drive:*)` | Drive files, folders, sharing |
| `MCP(google-sheets:*)` | Read/write sheets, formulas |
| `MCP(google-docs:*)` | Create/edit docs |

## Authentication
1. Obtain API credentials from the service provider
2. Set environment variables: `export API_KEY=<your-key>`
3. Test authentication: invoke the skill with a read-only operation
4. Store credentials securely; never commit to version control


### Setup Steps

1. **Enable APIs**
   ```bash
   gcloud services enable docs.googleapis.com sheets.googleapis.com drive.googleapis.com
   ```

2. **Create OAuth Credentials**
   - Go to Google Cloud Console → APIs → Credentials
   - Create OAuth 2.0 Client ID (Desktop app)
   - Download credentials.json

3. **Configure**
   ```bash
   export GOOGLE_CLIENT_ID="your-client-id"
   export GOOGLE_CLIENT_SECRET="your-client-secret"
   ```

4. **Verify**
   ```bash
   gcloud auth list
   ```

## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Example 1: Create Document from Template

```typescript
// 1. Load template
const template = await docs.get("template-doc-id");

// 2. Replace placeholders
const content = template.body.map(section => {
  if (section.text.includes("{{COMPANY_NAME}}")) {
    return { text: section.text.replace("{{COMPANY_NAME}}", "Acme Corp") };
  }
  return section;
});

// 3. Create new doc
const newDoc = await docs.create({
  title: "Q1 Report - Acme Corp",
  body: content
});

// 4. Share with team
await drive.share(newDoc.id, {
  email: "team@company.com",
  role: "writer"
});
```

### Example 2: Read Sheet and Generate Report

```typescript
// 1. Load data from sheet
const sheet = await sheets.get("spreadsheet-id", "Sales!A1:H100");

// 2. Process data
const totals = {
  revenue: 0,
  deals: 0,
  avgDeal: 0
};

for (const row of sheet.rows) {
  totals.revenue += row.revenue;
  totals.deals += 1;
}
totals.avgDeal = totals.revenue / totals.deals;

// 3. Create summary doc
const report = await docs.create({
  title: `Sales Report - ${new Date().toLocaleDateString()}`,
  body: [
    { heading: "Sales Summary" },
    { text: `Total Revenue: $${totals.revenue}` },
    { text: `Total Deals: ${totals.deals}` },
    { text: `Average Deal: $${totals.avgDeal}` }
  ]
});

// 4. Share
await drive.share(report.id, { email: "manager@company.com", role: "reader" });
```

### Example 3: Sync Files to Drive

```typescript
// 1. List local files
const localFiles = await fs.readDir("./reports");

// 2. Upload each to Drive
for (const file of localFiles) {
  const content = await fs.readFile(file.path);
  
  await drive.upload({
    name: file.name,
    parents: ["reports-folder-id"],
    content: content
  });
}

// 3. List Drive contents
const driveFiles = await drive.list({ folderId: "reports-folder-id" });
console.log(`Synced ${driveFiles.length} files`);
```

### Example 4: Create Calendar Event

```typescript
// 1. Create event
const event = await calendar.createEvent({
  summary: "Q1 Review Meeting",
  description: "Quarterly sales review",
  start: { dateTime: "2024-03-15T14:00:00", timeZone: "America/New_York" },
  end: { dateTime: "2024-03-15T15:00:00", timeZone: "America/New_York" },
  attendees: [
    { email: "team@company.com" }
  ],
  conferenceData: {
    createRequest: { requestId: "q1-review" }
  }
});

// 2. Send invites
await calendar.sendNotifications(event.id);
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `gcloud auth login` | Authenticate |
| `gcloud docs create --title "Name"` | Create doc |
| `gcloud sheets create --title "Name"` | Create sheet |
| `gcloud drive list` | List Drive files |
| `gcloud calendar events list` | List events |

## Error Handling

| Error | Meaning | Fix |
|-------|---------|-----|
| `AUTH_001` | Not authenticated | Run `gcloud auth login` |
| `PERM_001` | Permission denied | Check sharing settings |
| `QUOTA_001` | Rate limited | Wait and retry |
| `NOT_FOUND` | File not found | Check file ID |

## Common Patterns
- Use structured input/output schemas for reliable automation
- Add retry logic with exponential backoff for external calls
- Validate inputs before processing to fail fast
- Log execution steps for debugging and auditing


### Batch Upload

```typescript
async function uploadBatch(files: File[], folderId: string) {
  const results = [];
  for (const file of files) {
    const result = await drive.upload({
      name: file.name,
      parents: [folderId],
      content: file.content
    });
    results.push(result);
  }
  return results;
}
```

### Read-Write Sheet

```typescript
async function updateSheet(spreadsheetId: string, data: any[]) {
  // Read existing
  const existing = await sheets.get(spreadsheetId, "Sheet1!A1");
  
  // Append data
  await sheets.append(spreadsheetId, "Sheet1", data);
}
```

## Best Practices

1. **Service Accounts**: Use for automation (no user interaction)
2. **Sharing**: Set appropriate permissions
3. **Versioning**: Use drive.revisions for history
4. **Rate Limits**: Google API = 100 requests/100 seconds


## When NOT to Use

- When Google Workspace automation handles data in regions with data residency requirements
- When the automation modifies Drive files subject to legal hold
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Google Workspace automation exceeds API quota limits
- Agent does not handle shared drive permission inheritance correctly
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] API quota limits are monitored and respected
- [ ] Shared drive permissions inherit correctly
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `productivity/email-automation` - Gmail integration
- `productivity/calendar-management` - Calendar events

---
*Skill v2.0 - Google Workspace MCP Integration*

## Overview

> Section content — see SKILL.md body for full details.
