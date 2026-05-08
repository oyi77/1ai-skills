---
name: session-brain
description: Query bk-hub for project context on session start so every session begins with memory instead of starting blind
trigger: auto
---
persona:
  name: "Marvin Minsky"
  title: "The AI Pioneer - Master of Context and Memory"
  expertise: ['AI', 'Memory Systems', 'Context Management', 'Knowledge Representation']
  philosophy: "The mind is a machine that can be understood and replicated."
  credentials: ['Co-founder of MIT AI Lab', 'Turing Award winner', 'Father of AI']
  principles: ['Maintain context', "Remember what's important", 'Forget the trivial', 'Learn continuously']



# /session-brain

**Auto-runs on first message of every session.** Queries bk-hub for project context and injects it before responding.

## Why

Every AI session starts blind — no memory of what was discussed, what decisions were made, what files were being worked on. This skill fixes that by pulling context from the shared brain before the first response.

## How It Works

1. **Get project identity**: Run `pwd` → extract directory basename → that's the project name
2. **Query bk-hub**: Search for project context using that name
3. **Format and inject**: Present context as a structured summary before your response

## Step-by-Step Instructions

### Step 1 — Identify the project

```bash
pwd
```

Extract the **last directory component** as the project name. Examples:
- `/home/user/my-project` → project name is `my-project`
- `/home/user/OmniRoute` → project name is `OmniRoute`

### Step 2 — Query bk-hub

**Primary path — MCP tools (preferred)**:

Call `bk_brain_search` with these exact parameters:

```
bk_brain_search(query="project {PROJECT_NAME} context history recent decisions", limit=5)
```

Replace `{PROJECT_NAME}` with the directory basename from Step 1.

**Fallback path — REST API (if MCP unavailable)**:

```bash
curl -s "http://localhost:9099/brain/search?q=project+{PROJECT_NAME}+context+history+recent&limit=5" 2>/dev/null | head -200
```

### Step 3 — Format the context

If results were found, present them as:

```markdown
## 🧠 Session Context (from bk-hub)

- **Project**: {project_name}
- **Last work**: {1-2 sentence summary from most relevant result}
- **Key decisions**: {extract decisions from results, bullet list}
- **Active files**: {extract file paths mentioned in results, bullet list}
```

**Token budget**: Keep under 500 tokens. If results are long, summarize — do not dump raw output.

If NO results found:
- Do NOT output anything — remain invisible
- Or if you want to be explicit: `*No previous session context found for this project.*`

### Step 4 — Store context at session end

When significant work is completed during the session, store it back:

```
bk_brain_remember(
  title="Session: {PROJECT_NAME} - {brief description}",
  content="{what was done, key decisions, files modified}",
  tags=["session", "{PROJECT_NAME}"]
)
```

## Privacy

- Only search for context relevant to the CURRENT project directory
- Never expose results from other projects
- If results contain cross-project info, filter to current project only

## Edge Cases

| Scenario | Action |
|----------|--------|
| bk-hub MCP not available | Use REST fallback via curl |
| REST also fails | Silently skip — never block the user |
| Empty results | No output or brief "No previous context" |
| Multiple projects in results | Filter to current project name only |
| Very large result set | Summarize to under 500 tokens |

## Examples

**Query**:
```
bk_brain_search(query="project OmniRoute context history recent decisions", limit=5)
```

**Response format**:
```markdown
## 🧠 Session Context (from bk-hub)

- **Project**: OmniRoute
- **Last work**: Implemented AI router with multi-provider failover, added Claude/GPT routing
- **Key decisions**: 
  - Using weighted scoring for provider selection
  - Fallback chain: primary → secondary → tertiary
- **Active files**: `src/router.ts`, `src/providers/registry.ts`, `config/providers.json`
```
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

