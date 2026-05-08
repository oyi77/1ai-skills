persona:
  name: "Domain Expert"
  title: "Master of Notion"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']

# Notion Workspace Skill

> 📝 Notion integration for BerkahKarya knowledge management and task tracking

## Overview

Notion is a powerful workspace for notes, knowledge bases, project management, and databases. This skill enables Vilona to interact with Notion for BerkahKarya's documentation and task management needs.

## When to Use

- **Knowledge base** — Store and retrieve company documentation
- **Task tracking** — Manage projects and to-dos
- **Database management** — Create and query Notion databases
- **Meeting notes** — Log and share meeting summaries
- **Documentation** — Create and update company docs

## Setup

### Option 1: Notion MCP (RECOMMENDED)
```bash
# Add to Claude Desktop config
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
    }
  }
}
```

### MCP Tools Available
| Tool | Purpose |
|------|---------|
| `notion_search` | Search pages/databases |
| `notion_fetch` | Get page/database details |
| `notion_create_pages` | Create new pages |
| `notion_update_page` | Update page properties |
| `notion_create_database` | Create new database |

### Option 2: API Key (Legacy)
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy API key
4. Share pages with integration

---

## Usage Examples

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

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

