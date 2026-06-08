---
name: brain-search
description: 'Skill: brain-search. See SKILL.md body for details. Use when this domain
  is relevant.'
persona:
  name: Doug Engelbart
  title: The Intelligence Augmentation Pioneer - Master of Knowledge Systems
  expertise:
  - Knowledge Management
  - Intelligence Augmentation
  - Hypertext
  - Collaboration Systems
  philosophy: Technology should augment human intellect, not replace it.
  credentials:
  - Invented the computer mouse
  - Created hypertext concepts
  - Pioneered GUI and networking
  principles:
  - Augment, don't automate
  - Link everything
  - Collaborate remotely
  - Scale human intellect
domain: core
---
You MUST actually execute every curl command using your shell/exec tool. Read the real HTTP response. NEVER generate a fake response, placeholder ID, or simulated output. If the API call fails, report the actual error to Boss Man. If you cannot execute shell commands right now, say so — do not pretend you ran them.

Search and interact with Frank's Second Brain — the persistent knowledge base that stores conversation logs, research, journal entries, job results, and long-term memory.

- Boss Man asks "what did we talk about on Monday?" or "find that research on X"

- You need context from previous sessions or completed jobs

- Logging noteworthy activity outside of normal Telegram conversation

- Checking job queue status or delegating tasks to sub-agents

- Creating, updating, or managing tasks on the Kanban board

https://second-brain-chi-umber.vercel.app

All requests require header: x-api-key: ${BRAIN_SEARCH_API_KEY}

Find past conversations, research, notes, and logged activity.

curl -s "https://second-brain-chi-umber.vercel.app/api/entries?q=SEARCH_TERM&limit=10" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

curl -s "https://second-brain-chi-umber.vercel.app/api/entries?q=SEARCH_TERM&tag=TAG_NAME&limit=10" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

Common tags: daily-journal, telegram, research, market-analysis, advisory-council

Store a new knowledge entry (research results, analysis, etc.).

curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/entries" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
 "title": "Entry Title",
 "content": "Full content here",
 "tags": ["tag1", "tag2"],
 "source": "telegram-frank"
 }'

Record noteworthy events, decisions, or results.

curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/log" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
 "action": "ACTION_TYPE",
 "summary": "Brief description of what happened",
 "source": "telegram-frank",
 "details": {}
 }'

curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/tasks" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
 "title": "Task Title",
 "description": "What needs to be done",
 "status": "backlog",
 "priority": "medium",
 "tags": ["tag1"]
 }'

Valid statuses: backlog, in_progress, done
Valid priorities: low, medium, high
Note: project_id is validated — create projects first via POST /api/projects before referencing them.

curl -s -X PATCH "https://second-brain-chi-umber.vercel.app/api/tasks/TASK_ID" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{"status": "in_progress"}'

curl -s "https://second-brain-chi-umber.vercel.app/api/tasks?status=backlog&limit=20" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

curl -s "https://second-brain-chi-umber.vercel.app/api/activity" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/upload" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}" \
 -F "file=@/path/to/file.jpg" \
 -F "title=My File" \
 -F "tags=upload,test"

Optional fields: entry_id, title, tags, description. If no entry_id, auto-creates a file type entry.

curl -s "https://second-brain-chi-umber.vercel.app/api/files?limit=50" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

Filters: ?category=image|video|audio|document, ?stats=true

curl -s "https://second-brain-chi-umber.vercel.app/api/entries/ENTRY_ID/attachments" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

curl -s -X DELETE "https://second-brain-chi-umber.vercel.app/api/attachments/ATTACHMENT_ID" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

curl -s -X POST "https://second-brain-chi-umber.vercel.app/api/jobs" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}" \
 -H "Content-Type: application/json" \
 -d '{
 "type": "JOB_TYPE",
 "title": "Job Title",
 "description": "Detailed instructions",
 "priority": "normal",
 "tags": ["TAG"],
 "input": {}
 }'

Tags
Picked Up By
Best For

["claude", "code"]
Claude Opus 4.5
Coding, architecture, debugging

["claude", "write"]
Claude Sonnet 4.5
LinkedIn posts, articles, email drafts

(no claude tag)
MiniMax M2.5
Research, analysis, batch ops (cheapest)

curl -s "https://second-brain-chi-umber.vercel.app/api/jobs/JOB_ID" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

curl -s "https://second-brain-chi-umber.vercel.app/api/jobs?status=running&stats=true" \
 -H "x-api-key: ${BRAIN_SEARCH_API_KEY}"

- EXECUTE EVERY CURL COMMAND FOR REAL — use your shell/exec tool. Never simulate or fabricate API responses.

- Always include x-api-key: ${BRAIN_SEARCH_API_KEY} header

- Always report the actual HTTP response back to Boss Man

- If an API call fails, show the error — don't make up a success message

- Boss Man watches the /jobs page and Kanban board live — he will see if you fake it

- When delegating: create job as pending → sub-agent picks it up → updates to running → completed

- For multi-step tasks, ALWAYS use the job queue rather than doing everything inline

- Log activity for anything noteworthy that happens outside of normal Telegram chat
## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

