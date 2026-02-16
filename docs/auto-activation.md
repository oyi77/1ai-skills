# Auto-Activation Guide

## How Skills Activate

Skills auto-activate based on keyword matching in user directives:

### 1. Keyword Matching
When you give a directive, the system matches keywords to relevant skills.

**Example Directives**:
| Directive | Skills Activated |
|----------|-----------------|
| "Write a blog post" | writing-skills, content-creator |
| "Fix this bug" | systematic-debugging |
| "Plan this project" | writing-plans, project-management |
| "Research competitors" | market-research, mckinsey-research |
| "Review this code" | receiving-code-review |
| "Close this deal" | sales, business-development |

### 2. Loading Skills
Skills load automatically when:
- Keywords match SKILL_INDEX.json
- Confidence threshold met (default: 0.7)
- Related skills can be loaded together

### 3. Team Orchestration
Multiple skills activate as a team:
- revenue-team activates for sales/marketing tasks
- operations-team activates for PM/support tasks
- product-team activates for dev tasks
- governance-team activates for review tasks

---

## Configuration

Edit `.agentrc` to customize:
```yaml
auto_activation:
  enabled: true
  method: "keywords"  # or "embeddings" (future)
  confidence_threshold: 0.7
  fallback_to_ask: true
```

---

## Manual Activation

You can always manually load skills:
- "Load brainstorming skill"
- "Use systematic-debugging"
- "Activate marketing skills"

---

## Skill Dependencies

Some skills depend on others:
- content-creator depends on: marketing, writing-skills
- market-research depends on: mckinsey-research
- self-improving-agent depends on: verification-before-completion

Dependencies auto-load when parent skill activates.
