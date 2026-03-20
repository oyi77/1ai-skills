# AGENTS.md - Skills Library

Specialized skills for AI agent execution across domains.

## OVERVIEW

34+ skill directories covering content generation, trading, automation, marketing, and development.

## CATEGORIES

| Category | Skills |
|----------|--------|
| **Content** | content-generator, humanizer, video-editor, ai-podcast, faceless-youtube |
| **Trading** | crypto-trading-bot, polymarket-analyst, maybe-hft (MT5) |
| **Marketing** | marketing, twitter-automation, social-media-engagement, email-marketing |
| **Automation** | workflow-builder, jobhunter, content-publisher |
| **Development** | code-reviewer, test-driven-development, systematic-debugging |
| **Operations** | project-management, operations-team, revenue-team |

## KEY SKILLS

- `paperclip` - Control plane API interactions
- `release` - Full release coordination
- `content-generator` - Multi-provider video generation (NVIDIA NIM, BytePlus Seedance)
- `faceless-youtube` - Automated faceless YouTube channel

## ANTI-PATTERNS

- **NEVER** create new skill without checking existing
- **NEVER** skip skill discovery before implementing

## PRE-TASK CHECK

```bash
find skills/ -name "*keyword*"
grep -r "keyword" skills/ --include="*.md" | head -20
```

## REFERENCES

- Parent: `workspace/AGENTS.md`
- Root: `AGENTS.md`
