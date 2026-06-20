---
name: notion
description: Automate Notion workflows including database CRUD, page creation, content publishing, and workspace management
  via API.
domain: productivity
tags:
- api
- notion
- productivity
- time-management
- tools
- workflow
---
## Usage Examples
```
# Basic usage
## When to Use

**Trigger phrases:**
- "notion"
- "Help me with notion"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Query via MCP
```
User: "Apa saja task yang overdue?"
Vilona: Uses notion_search to find tasks, notion_fetch for details
```

### Create Page
```
User: "Buat meeting notes untuk meeting yesterday"
Vilona: Uses notion_create_pages
```

## References
- **Notion MCP**: [developers.notion.com/guides/mcp](https://developers.notion.com/guides/mcp)
- **Skill**: [notion-tasks](https://skillmd.ai/skills/notion-tasks-1/)

---

## Usage Examples (Legacy)
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### API Key Setup
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy API key
4. Share relevant pages with the integration

### Environment Variables
```bash
NOTION_API_KEY=your_api_key_here
NOTION_DATABASE_ID=your_database_id  # For specific databases
```

## Usage Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Query Database
```
User: "Apa saja task yang overdue?"
Vilona: [Queries Notion for overdue tasks]
→ Returns: List of overdue items with owners and due dates
```

### Create Page
```
User: "Buat meeting notes untuk meeting yesterday"
Vilona: [Creates new page in Meeting Notes database]
→ Content: Attendees, agenda, decisions, action items
```

### Update Task Status
```
User: "Update task 'launch campaign' jadi done"
Vilona: [Updates Notion database entry]
→ Status changed to "Done"
→ Last updated timestamp added
```

### Search Knowledge Base
```
User: "Cari info tentang pricing strategy"
Vilona: [Searches Notion pages]
→ Returns relevant pages with snippets
```

## Common Databases for BerkahKarya
This section covers common databases for berkahkarya for the notion skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### 1. Task Tracker
```
Database: Tasks
Properties:
- Name (title)
- Status (select: Todo, In Progress, Done)
- Assignee (person)
- Due Date (date)
- Priority (select: High, Medium, Low)
- Project (relation)
```

### 2. Project Roadmap
```
Database: Projects
Properties:
- Project Name (title)
- Status (select: Planning, Active, Completed, On Hold)
- Start Date (date)
- End Date (date)
- Owner (person)
- Team Members (multi-person)
- Budget (number)
```

### 3. Meeting Notes
```
Database: Meetings
Properties:
- Title (title)
- Date (date)
- Attendees (multi-person)
- Agenda (rich text)
- Decisions (rich text)
- Action Items (relation to Tasks)
```

### 4. Knowledge Base
```
Database: Documents
Properties:
- Title (title)
- Category (select: Strategy, Process, Product, Marketing, etc.)
- Tags (multi-select)
- Last Updated (date)
- Content (rich text)
```

## Auto-Activation Triggers

| Trigger Phrases | Action |
|----------------|--------|
| "notion", "docs", "documentation" | Activate Notion skill |
| "task", "todo", "to-do" | Query/create tasks |
| "meeting notes", "meeting" | Create/access meeting notes |
| "search", "cari" | Search knowledge base |
| "update status", "mark done" | Update database entries |

## Integration with Other Skills

| Connected Skill | Use Case |
|-----------------|----------|
| `n8n` | Workflow automation triggers |
| `communication-mcp` | Share Notion pages to Slack/Discord |
| `jira` | Sync tasks between systems |
| `clickup` | Bi-directional task sync |
| `calendar-management` | Link meetings to calendar events |

## Notion API Endpoints Used

- `GET /v1/databases/{id}` — Query database
- `GET /v1/pages/{id}` — Get page
- `POST /v1/pages` — Create page
- `PATCH /v1/pages/{id}` — Update page
- `GET /v1/search` — Search all content

## Commands

```bash
# Query tasks
notion query --database tasks --filter "status=TODO"

# Create task
notion create task --title "New campaign" --assignee paijo

# Update status
notion update --page-id xxx --property status --value "Done"

# Search
notion search --query "pricing strategy"
```

---

*Use Notion as BerkahKarya's central knowledge hub. Everything searchable, everything connected.*

## When NOT to Use

- When the productivity tool handles legally privileged communications
- When the automation affects compliance-archived records or legal holds
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

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

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
