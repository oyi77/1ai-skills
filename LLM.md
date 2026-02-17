# 1ai-skills - AI Workforce for One-Person Company

## What is This?
AI workforce for one-person company - you're the owner, AI agents do all the work. This repo contains **80 skills** (49 local + 31 external) that can be loaded into your AI agent to help run your business.

## Quick Installation

```bash
# Clone to your agent's skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/oyi77/1ai-skills.git
cd 1ai-skills
npm install
```

For detailed installation by agent (OpenCode, Claude Code, etc.), see INSTALL.md

## Skill Categories

| Category | Skills |
|----------|--------|
| **Trading** | trading, trading-researcher, trading-strategist, trading-risk-manager, trading-executor, trading-team, xauusd-asia-7c-breakout |
| **Planning** | brainstorming, writing-plans, executing-plans |
| **Development** | test-driven-development, systematic-debugging, subagent-driven-development, finishing-a-development-branch, using-git-worktrees |
| **Marketing & Sales** | marketing, sales, business-development, copywriting, content-strategy, seo-audit, competitor-alternatives |
| **Content** | humanizer, humanizer-zh, writing-skills, content-creator |
| **Research** | mckinsey-research, polymarket-analyst, market-research |
| **Operations** | customer-support, project-management, analytics-reporting |
| **Productivity** | google-workspace, email-automation, calendar-management, using-superpowers |
| **Intelligence** | self-improving-agent |
| **Quality** | receiving-code-review, requesting-code-review, verification-before-completion |
| **Orchestration** | joko-orchestrator, revenue-team, operations-team, product-team, governance-team |

## Auto-Activation

Skills can auto-activate based on keywords. See SKILL_INDEX.json for full keyword mappings.

## Team Orchestration

Skills are organized into teams:
- **Trading Team**: trading, trading-researcher, trading-strategist, trading-risk-manager, trading-executor
- **Revenue Team**: marketing, sales, content-creator
- **Operations Team**: project-management, customer-support, market-research
- **Product Team**: subagent-driven-development, verification-before-completion
- **Governance Team**: receiving-code-review, systematic-debugging
