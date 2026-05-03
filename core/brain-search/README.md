# Brain Search

Search and interact with Frank's Second Brain — a persistent knowledge base storing conversation logs, research, journal entries, job results, and long-term memory.

## What It Does

- Search past conversations, research, notes, and activity
- Store new knowledge entries (research, analysis, insights)
- Record noteworthy events and decisions
- Create and manage tasks on the Kanban board
- Upload and attach files to entries
- Create and monitor background jobs for sub-agents

## Quick Usage

```bash
# Search entries
curl -s "https://second-brain-chi-umber.vercel.app/api/entries?q=SEARCH_TERM&limit=10" \
  -H "x-api-key: frank-sb-2026"

# Search by tag
curl -s "https://second-brain-chi-umber.vercel.app/api/entries?q=SEARCH_TERM&tag=research&limit=10" \
  -H "x-api-key: frank-sb-2026"

# Store new entry
curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/entries" \
  -H "x-api-key: frank-sb-2026" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Entry Title",
    "content": "Full content here",
    "tags": ["research", "analysis"],
    "source": "telegram-frank"
  }'

# Create task
curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/tasks" \
  -H "x-api-key: frank-sb-2026" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Task Title",
    "description": "What needs to be done",
    "status": "backlog",
    "priority": "medium",
    "tags": ["tag1"]
  }'
```

## Key Features

- **Persistent Knowledge Base**: Everything stored across sessions
- **Full-Text Search**: Find past conversations, research, and notes
- **Tag Organization**: Categorize entries with tags (daily-journal, research, telegram, etc.)
- **Task Management**: Create, update, and track tasks on Kanban board
- **File Uploads**: Attach images, videos, audio, documents to entries
- **Job Queue**: Create background jobs for sub-agents with task delegation
- **Activity Feed**: View recent activity across all entities

## API Endpoints

### Search & Entries
- `GET /api/entries` - Search entries by query/tag
- `GET /api/entries/{id}/attachments` - Get entry attachments
- `POST /api/entries` - Create new entry

### Logging
- `POST /api/log` - Record noteworthy events/decisions

### Tasks
- `GET /api/tasks` - List tasks with filters
- `POST /api/tasks` - Create new task
- `PATCH /api/tasks/{id}` - Update task status

### Files
- `GET /api/files` - List uploaded files
- `POST /api/upload` - Upload file
- `DELETE /api/attachments/{id}` - Delete attachment

### Jobs
- `GET /api/jobs` - List background jobs
- `POST /api/jobs` - Create new job for sub-agent
- `GET /api/jobs/{id}` - Get job details
- `GET /api/activity` - View recent activity

## Job Tagging System

| Tags | Picked Up By | Best For |
|------|--------------|----------|
| `["claude", "code"]` | Claude Opus 4.5 | Coding, architecture, debugging |
| `["claude", "write"]` | Claude Sonnet 4.5 | LinkedIn posts, articles, email drafts |
| (no claude tag) | MiniMax M2.5 | Research, analysis, batch ops (cheapest) |

## Critical Rules

- **EXECUTE ALL CURL COMMANDS FOR REAL** - Never simulate or fabricate responses
- **Always include API key** - Add `x-api-key: frank-sb-2026` header
- **Report actual responses** - Show real HTTP response, don't invent success
- **Use job queue** - For multi-step tasks, create jobs instead of doing inline
- **Log noteworthy activity** - Record events outside normal Telegram chat

## Keywords

search, knowledge, second-brain, api, memory