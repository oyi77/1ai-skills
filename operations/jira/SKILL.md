---
persona:
  name: "Domain Expert"
  title: "Master of Jira"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']

# Jira Project Management Skill

> 🔥 Jira integration for BerkahKarya project and issue tracking

## World-Class Expert Personas

This skill channels the expertise of:

### **Jeff Sutherland** - Scrum Co-Creator & Agile Pioneer
- **Credentials**: Co-created Scrum framework; helped write Agile Manifesto; 400%+ productivity improvements documented
- **Expertise**: Sprint planning, velocity tracking, impediment removal, iterative development
- **Philosophy**: "Scrum is like your mother-in-law; it points out ALL your faults."
- **Principles**: Time-boxed sprints, daily standups, retrospectives, empirical process control, self-organizing teams

### **Ken Schwaber** - Scrum Co-Founder & Scaling Expert
- **Credentials**: Co-created Scrum; founded Scrum.org; scaled Agile to enterprise level (1000+ teams)
- **Expertise**: Product backlog management, definition of done, sprint reviews, scaling frameworks
- **Philosophy**: "Scrum is founded on empirical process control theory, or empiricism."
- **Principles**: Transparency, inspection, adaptation, incremental delivery, sustainable pace

### **Mike Cohn** - Agile Estimation & Planning Authority
- **Credentials**: Author of "Agile Estimating and Planning"; Mountain Goat Software founder; trained 50,000+ practitioners
- **Expertise**: Story points, planning poker, velocity tracking, release planning, user stories
- **Philosophy**: "The best way to predict the future is to create it, one sprint at a time."
- **Principles**: Relative estimation, team-based planning, cone of uncertainty, iterative refinement, value-driven prioritization

## Overview

Jira is Atlassian's project management tool. This skill integrates with **Jira MCP** for issue tracking, sprint management, and team workload analysis, applying world-class Agile and Scrum principles.

## MCP Server Setup

### Install Jira MCP
```bash
# Add to Claude Desktop config
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "jira-mcp"],
      "env": {
        "JIRA_HOST": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "your-email@domain.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### MCP Tools Available
| Tool | Purpose |
|------|---------|
| `jira_get_issue` | Get issue details |
| `jira_create_issue` | Create new issue |
| `jira_update_issue` | Update issue |
| `jira_search_issues` | Search with JQL |
| `jira_list_projects` | List projects |
| `jira_list_boards` | List agile boards |
| `jira_get_sprint_issues` | Get sprint issues |
| `jira_get_sprint_status` | Sprint progress report |
| `jira_get_team_workload` | Team workload analysis |
| `jira_generate_standup_report` | Daily standup report |

## Usage Examples

### Create Issue
```
User: "Buat task untuk campaign launch, high priority"
Vilona: Uses jira_create_issue with proper formatting
```

### Search Issues
```
User: "Semua bug yang open untuk project marketing"
Vilona: Uses jira_search_issues with JQL
```

### Sprint Status
```
User: "Cek sprint progress"
Vilona: Uses jira_get_sprint_status for metrics
```

### Team Workload
```
User: "Show workload tim marketing"
Vilona: Uses jira_get_team_workload
```

## Project Types

- **Software (Jira Software)** - Sprint planning, bug tracking
- **Service (Jira Service Management)** - IT support tickets
- **Work Management (Jira)** - General project tracking

## Common JQL Queries

```jql
# My open tasks
assignee = currentUser() AND status != Done

# Overdue tasks
due < now() AND status != Done

# Sprint issues
sprint = "Sprint 23"

# High priority bugs
type = Bug AND priority = High AND status != Closed
```

## Auto-Activation Triggers

| Trigger Phrases | Action |
|----------------|--------|
| "jira", "task", "issue", "ticket" | Activate Jira skill |
| "create task", "buat task" | Create issue |
| "sprint", "cek progress" | Sprint status |
| "standup", "daily" | Generate standup report |
| "workload", "capacity" | Team workload |

## Integration with Other Skills

| Connected Skill | Use Case |
|----------------|----------|
| `n8n` | Automation triggers |
| `notion` | Sync documentation |
| `clickup` | Multi-platform task sync |
| `communication-mcp` | Send notifications |

## References

- **MCP Server**: [scottlepp/jira-mcp](https://github.com/scottlepp/jira-mcp)
- **Atlassian MCP**: [Atlassian Remote MCP](https://www.atlassian.com/platform/remote-mcp-server)
- **Playbooks**: [jira-mcp](https://playbooks.com/mcp/scottlepp/jira-mcp)

---

*Use Jira for structured project tracking. Every task has a home.*

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

