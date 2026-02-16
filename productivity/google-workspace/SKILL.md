---
name: google-workspace
description: Integrate with Google Workspace (Docs, Sheets, Drive, Calendar) using MCP servers
category: productivity
tags: [google, workspace, productivity, mcp, automation]
---

# Google Workspace Integration

Comprehensive Google Workspace integration using MCP servers for seamless automation and productivity.

## Overview

This skill enables deep integration with Google Workspace services including Google Docs, Sheets, Drive, and Calendar through Model Context Protocol (MCP) servers.

## Capabilities

### Document Management
- Create, read, update Google Docs
- Format and style documents
- Collaborate on shared documents
- Export to various formats

### Spreadsheet Operations
- Create and manipulate Google Sheets
- Perform data analysis
- Generate charts and visualizations
- Import/export data

### File Management
- Upload/download files to Google Drive
- Organize folders and permissions
- Share files and folders
- Search across Drive

### Calendar Integration
- Create and manage events
- Schedule meetings
- Set reminders and notifications
- Sync with other calendars

## MCP Integration

### Google Cloud MCP
Interact with Google Cloud services and manage cloud resources.

**Installation**: Contact Google Cloud team for MCP server details

**Configuration**:
```json
{
  "mcpServers": {
    "google-cloud": {
      "command": "npx",
      "args": ["@google-cloud/mcp-server"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

## Usage Examples

### Create a Document
```
Create a new Google Doc titled "Q1 Report" with the following content:
- Executive Summary
- Financial Overview
- Key Metrics
```

### Analyze Spreadsheet Data
```
Open the "Sales Data" spreadsheet and:
1. Calculate total revenue by region
2. Create a pie chart showing distribution
3. Export summary to PDF
```

### Schedule Meeting
```
Schedule a team meeting for next Tuesday at 2 PM:
- Duration: 1 hour
- Attendees: team@company.com
- Add Google Meet link
- Send calendar invites
```

## Best Practices

1. **Authentication**: Use service accounts for automated access
2. **Permissions**: Follow principle of least privilege
3. **Rate Limiting**: Respect API quotas and limits
4. **Error Handling**: Implement retry logic for transient failures
5. **Data Privacy**: Handle sensitive data according to company policies

## Requirements

- Google Workspace account
- API credentials (OAuth 2.0 or Service Account)
- MCP server installed and configured
- Appropriate permissions for target resources

## Related Skills

- `productivity/email-automation` - Email automation with Gmail
- `productivity/calendar-management` - Advanced calendar features
- `operations/project-management` - Project tracking integration
