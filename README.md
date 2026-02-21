# 1ai-skills

## What is This?
AI workforce for one-person company - you're the owner, AI agents do the work.

## Installation

This toolkit is designed to be **cross-platform** (Windows, macOS, Linux).

**Requirement**: Node.js 18+

### Quick Install (All Agents)
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/oyi77/1ai-skills.git
cd 1ai-skills
npm install
```

---

## Agent-Specific Installation

### For Claude Code (claude.ai)
```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or use direct install
claude install oyi77/1ai-skills
```

### For OpenCode
```bash
# Install to OpenCode skills directory
cd ~/.opencode/skills
git clone https://github.com/oyi77/1ai-skills.git

# Or use OpenCode's skill management
opencode skills install oyi77/1ai-skills
```

### For OpenCraw
```bash
# OpenCraw uses the skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/oyi77/1ai-skills.git
cd 1ai-skills
npm install
```

---

### For Humans
Paste this into your LLM agent session:
```
Install and configure 1ai-skills by following the instructions here:
https://raw.githubusercontent.com/oyi77/1ai-skills/refs/heads/main/LLM.md
```

### For LLM Agents
Fetch the installation guide and follow it:
curl -s https://raw.githubusercontent.com/oyi77/1ai-skills/refs/heads/main/LLM.md

## Skills (80 skills - 49 local + 31 external)

| Category | Skills |
|----------|--------|
| Planning | brainstorming, writing-plans, executing-plans |
| Development | test-driven-development, systematic-debugging, subagent-driven-development, finishing-a-development-branch, using-git-worktrees, vercel-composition-patterns, vercel-react-best-practices, vercel-react-native-skills, web-design-guidelines |
| Marketing & Sales | marketing, sales, business-development, copywriting, content-strategy, email-sequence, social-content, seo-audit, analytics-tracking, paid-ads, launch-strategy, competitor-alternatives, pricing-strategy, ab-test-setup |
| CRO | page-cro, form-cro, popup-cro, signup-flow-cro, onboarding-cro, paywall-upgrade-cro |
| Content | humanizer, humanizer-zh, writing-skills, gemini-image-generator, content-creator, copy-editing |
| Research | mckinsey-research, polymarket-analyst, market-research, competitor-alternatives |
| Operations | customer-support, project-management, analytics-reporting |
| Productivity | google-canvas, google-workspace, email-automation, calendar-management, dispatching-parallel-agents, using-superpowers |
| **Trading** | **trading, trading-researcher, trading-strategist, trading-risk-manager, trading-executor, trading-team, xauusd-asia-7c-breakout** |
| Intelligence | self-improving-agent |
| Quality | receiving-code-review, requesting-code-review, verification-before-completion |
| Tools | agent-docs |
| Jobs | job-hunter, joko-proactive-agent |
| Platforms | clawild-moltbook, joko-moltbook, moltbook-interact, google-flow |
| Browser Automation | agent-browser, browser-use |
| Growth | free-tool-strategy, referral-program, programmatic-seo, schema-markup, product-marketing-context, marketing-ideas, marketing-psychology |
| Orchestration | joko-orchestrator |
| Team Orchestrators | revenue-team, operations-team, product-team, governance-team |

---

## 🚀 Trading Skills

Looking for trading automation? We have a comprehensive **Trading Skills System** with:

- **Multi-Broker Support**: MetaTrader 5, MetaTrader 4, CCXT (crypto)
- **Trading Modes**: Backtest, Paper Trade, Real Trade
- **XAUUSD Strategy**: Asia 7-Candle Breakout strategy included
- **Autonomous Trading**: Full trading team (Researcher, Strategist, Risk Manager, Executor)

### Try it:
> "I want to do trading" or "How do I use trading skills?"

**Learn more**: See `trading/SKILL.md` for complete documentation.

## Quick Links
- Full Guide: LLM.md
- Handbook: docs/
- Skills Index: SKILL_INDEX.json
