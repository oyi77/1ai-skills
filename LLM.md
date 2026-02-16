# 1ai-skills - AI Workforce for One-Person Company

## What is This?
AI workforce for one-person company - you're the owner, AI agents do all the work. This repo contains 73 skills (42 local + 31 external) that can be loaded into your AI agent to help run your business.

## Installation

### For Humans
Paste this into your LLM agent session:
```
Install and configure 1ai-skills by following the instructions here:
https://raw.githubusercontent.com/paijo/1ai-skills/refs/heads/main/LLM.md
```

Or install manually (non-interactive by default):
```bash
# Install ALL skills from 1ai-skills (non-interactive, default)
npx skills add paijo/1ai-skills --skill brainstorming
npx skills add paijo/1ai-skills --skill writing-plans
npx skills add paijo/1ai-skills --skill executing-plans
npx skills add paijo/1ai-skills --skill test-driven-development
npx skills add paijo/1ai-skills --skill systematic-debugging
npx skills add paijo/1ai-skills --skill marketing
npx skills add paijo/1ai-skills --skill sales
npx skills add paijo/1ai-skills --skill business-development
# ... add more as needed
```

For interactive mode (ask questions), use:
```bash
npx skills add paijo/1ai-skills --skill [name] --interactive
```

### For LLM Agents
If you're an LLM Agent helping set up 1ai-skills, welcome! Follow these steps:

**DEFAULT (Non-Interactive)**: Install all skills automatically without asking questions.

#### Step 1: Install all skills (non-interactive)
```bash
# Install all skills at once - NO QUESTIONS ASKED
npx skills add paijo/1ai-skills --skill brainstorming
npx skills add paijo/1ai-skills --skill writing-plans
npx skills add paijo/1ai-skills --skill executing-plans
# ... continue with all skills
```

#### Step 2: Verify setup
```bash
# List installed skills
npx skills list
```

#### Step 3: Congratulate user
Say congratulations! 🎉

**Only ask user if they explicitly want interactive mode.**

## How to Use
1. **Load all skills**: "Load all 1ai-skills"
2. **Load category**: "Load marketing skills"
3. **Load specific**: "Load brainstorming skill"

## Skill Categories

| Category | Skills |
|----------|--------|
| **Planning** | brainstorming, writing-plans, executing-plans |
| **Development** | test-driven-development, systematic-debugging, subagent-driven-development, finishing-a-development-branch, using-git-worktrees |
| **Marketing & Sales** | marketing, sales, business-development |
| **Content** | humanizer, humanizer-zh, writing-skills, gemini-image-generator, content-creator |
| **Research** | mckinsey-research, polymarket-analyst, market-research |
| **Operations** | customer-support, project-management, analytics-reporting |
| **Productivity** | google-canvas, google-workspace, email-automation, calendar-management, dispatching-parallel-agents, using-superpowers |
| **Intelligence** | self-improving-agent |
| **Quality** | receiving-code-review, requesting-code-review, verification-before-completion |
| **Tools** | agent-docs |
| **Jobs** | jobhunter-master, joko-proactive-agent |
| **Platforms** | clawild-moltbook, joko-moltbook, moltbook-interact, google-flow |
| **Orchestration** | joko-orchestrator |
| **Team Orchestrators** | revenue-team, operations-team, product-team, governance-team |

## Auto-Activation

Skills can auto-activate based on keywords in user directives. See SKILL_INDEX.json for full keyword mappings.

## Team Orchestration

Skills are organized into 4 teams:
- **Revenue Team**: marketing, sales, business-development, content-creator
- **Operations Team**: project-management, customer-support, market-research
- **Product Team**: subagent-driven-development, verification-before-completion
- **Governance Team**: receiving-code-review, agent-docs, systematic-debugging

## Self-Improvement

The self-improving-agent skill enables continuous learning from feedback. When quality issues are identified, the agent can:
1. Receive feedback and parse it
2. Self-grade against rubric
3. Generate improvements
4. Commit learnings to knowledge base
