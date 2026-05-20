# 1ai-Skills — 220 Open-Source AI Agent Skills (Self-Evolving)

> The world's largest open-source AI skill ecosystem with **self-evolving meta-skills** — agents that auto-find, auto-create, auto-evolve. Single install, then evolving forever.

[![Skills: 220](https://img.shields.io/badge/skills-220-blue)](https://github.com/oyi77/1ai-skills)
[![Categories: 16](https://img.shields.io/badge/categories-16-green)](https://github.com/oyi77/1ai-skills)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](https://github.com/oyi77/1ai-skills/blob/main/LICENSE)
[![Auto-Release](https://img.shields.io/badge/auto--release-enabled-brightgreen)](https://github.com/oyi77/1ai-skills/releases)

**Star** this repo if you find it useful. Support development: https://www.tip.md/oyi77

---

## What Is This?

1ai-Skills is a collection of **220 production-ready AI agent skills** organized across **16 categories**. Each skill embeds expertise from world-class practitioners — Warren Buffett on investing, Elon Musk on first-principles thinking, Gary Vaynerchuk on viral marketing — translated into actionable frameworks AI agents can execute.

**New in v3.0:** 12 **meta-skills** that form a **self-evolving agent operating system** — the system can find missing skills from the community, create new skills when none exist, and continuously evolve to improve itself. **Single install, then evolving forever.**

---

## Quick Start

```bash
# Install all skills
npx skills add oyi77/1ai-skills

# Clone directly
git clone https://github.com/oyi77/1ai-skills.git

# Add as submodule
git submodule add https://github.com/oyi77/1ai-skills.git skills
```

---

## Self-Evolving Agent System (v3.0)

12 meta-skills that create a **self-evolving agent operating system** — finds what's missing, creates what doesn't exist, and evolves forever:

| Meta-Skill | What It Does |
|---|---|
| `meta/performance-monitor` | Track latency, success rates, cost, satisfaction scores |
| `meta/feedback-collector` | Aggregate feedback from explicit, implicit, and automated sources |
| `meta/self-assessment` | Skills evaluate their own accuracy, completeness, and efficiency |
| `meta/improvement-generator` | Create prioritized improvement plans from insights |
| `meta/skill-evolution` | Version control skills with safe rollback capability |
| `meta/auto-learner` | Autonomous learning from execution patterns |
| `meta/pattern-recognition` | Identify success and failure patterns across all skills |
| `meta/meta-orchestrator` | Coordinate the entire self-improvement loop |
| `meta/data` | Centralized SQLite storage for metrics, feedback, and versions |
| `meta/find-skills` | **Discover** community skills when local skills don't cover a need (Ada Lovelace persona) |
| `meta/create-skills` | **Generate** new skills when no existing solution exists (Grace Hopper persona) |
| `meta/auto-evolve` | **Orchestrate** the full evolution loop: find → create → improve (Charles Darwin persona) |

**System Flow:** Execute → Monitor → Collect → Recognize → Assess → **Find → Create** → Generate → Learn → Evolve → Repeat

---

## What's New in v3.1 — Anatomy & Structure Improvements

Based on analysis of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), we've standardized all 220 skills with **complete anatomy**:

### 📚 New `references/` Directory
Shared checklists to reduce token usage (replaces duplicated content in skills):
- `references/seo-checklist.md` — SEO audits (technical, on-page, Core Web Vitals, GEO)
- `references/marketing-checklist.md` — Marketing campaigns (content, social, email, paid ads)
- `references/code-review-checklist.md` — Code reviews (functionality, security, performance, accessibility)
- `references/trading-checklist.md` — Trading (strategy, risk management, portfolio)

### 📋 New `CONTRIBUTING.md`
Complete contribution guide with:
- SKILL.md anatomy requirements (frontmatter, sections, naming conventions)
- Persona guidelines (expertise, credentials, philosophy, principles)
- Pull request process with quality gates

### 🔧 New `docs/` Setup Guides
Platform-specific setup instructions:
- `docs/opencode-setup.md` — OpenCode integration via AGENTS.md and skill tool
- `docs/claude-setup.md` — Claude Code slash commands and plugin setup
- `docs/cursor-setup.md` — Cursor rules and @references setup

### 🪝 New `hooks/` System
Session lifecycle hooks for automation:
- `hooks/session-start.sh` — Auto-detect project type, suggest relevant skills
- `hooks/pre-commit.sh` — Validate SKILL.md structure before commit
- `hooks/post-task.sh` — Log skill performance after execution
- `hooks/hooks.json` — Hook configuration

### 📐 New `LIFECYCLE_INDEX.md`
Maps all 216 skills to the software development lifecycle:
- **DEFINE** → research skills (McKinsey, Feynman, Musk)
- **PLAN** → planning skills (writing-plans, find-skills, create-skills)
- **BUILD** → development skills (TDD, systematic-debugging, subagent-driven-development)
- **VERIFY** → verification skills (analytics, performance-monitor)
- **REVIEW** → review skills (code-reviewer, self-assessment)
- **SHIP** → shipping skills (SEO optimizer, viral marketing, growth engine)

### 🔧 Standardized Anatomy (ALL 220 Skills)
Every SKILL.md now has complete sections:
- ✅ **When NOT to Use** — Exclusion cases (prevents misuse)
- ✅ **Common Rationalizations** — Excuse/reality tables (prevents skipping steps)
- ✅ **Red Flags** — Behavioral signs of violations
- ✅ **Verification** — Evidence-based checklists (proves completion)

### 🔗 Cross-Skill References
Skills now reference each other (not duplicate content):
- "For SEO audits, also see `marketing/seo-optimizer`"
- "After debugging, use `development/systematic-debugging`"
- "Before creating skills, run `meta/find-skills`"

---

## Quick Start

## All 220 Skills by Category

| Category | Count | Highlights |
|---|---|---|
| **research/** | 25 | McKinsey analysis, deep research, Polymarket analyst, continuous learning |
| **core/** | 24 | Self-improvement, memory systems, AI orchestration, session brain |
| **content/** | 23 | Remotion video engine, video generation, AI podcast, faceless YouTube, humanizer, Seedance |
| **marketing/** | 22 | Marketing Ops OS, SEO optimizer, viral marketing, growth engine, Twitter automation |
| **automation/** | 21 | n8n workflows, WhatsApp/Telegram/Twitter bots, job hunter, scrapers |
| **development/** | 17 | TDD, systematic debugging, code review, PRD generator, git worktrees |
| **financial/** | 14 | All-in-One Finance (16 modules), Wolf Finance (22 modules), model builder, earnings viewer, pitch deck |
| **agents/** | 14 | Research, review, planning, code, deploy, refactor, linter, security |
| **integrations/** | 11 | Slack, Discord, Notion, GitHub — bots, webhooks, APIs |
| **operations/** | 10 | Finance ops, revenue team, project management, payment invoicing |
| **mcp/** | 10 | MCP servers for Slack, GitHub, Notion, Stripe, Supabase, Linear |
| **meta/** | 12 | find-skills, create-skills, auto-evolve, performance monitor, auto-learner |
| **sales/** | 6 | High-ticket closing, lead generation, business development |
| **devops/** | 6 | Docker, Kubernetes, GitHub Actions, ArgoCD, GitLab CI |
| **trading/** | 7 | Black Edge, AlphaEar, Polymarket, Tushare, crypto trading bot |
| **productivity/** | 6 | Google Workspace, calendar, email automation, Notion |
| **data/** | 4 | Data cleaning, anomaly detection, report generation, visualization |

---

## Featured Skills

### Self-Improving AI
- **Meta Orchestrator** — Coordinates the auto-improvement loop across all skills
- **Auto Learner** — Agents learn from execution data autonomously
- **Skill Evolution** — Version control for AI skills with safe rollback

### Trading and Finance
- **All-in-One Finance** — 16-module institutional suite: equities, crypto, forex, commodities, fixed income, derivatives with evidence tiers and risk gates
- **Wolf Finance** — 22-module multi-asset intelligence: all above plus corporate finance, wealth management, quant strategies, compliance/KYC
- **Black Edge** — Hidden market intelligence from satellite imagery, dark pools, options flow
- **AlphaEar Strategy** — Multi-signal trading: news + sentiment + options
- **Value Investing** — Warren Buffett's capital allocation framework
- **Rothschild Dynasty** — 250-year wealth preservation methodology

### Marketing and Growth
- **Marketing Ops** — Complete AI CMO for solo founders: research, content, SEO/GEO/SMO, ads, email, sales, CRO, pricing, retention, stage playbooks ($0→$100K MRR)
- **SEO Optimizer** — Full-stack SEO with content attack briefs and GSC optimization
- **Viral Marketing** — Gary Vaynerchuk's high-volume content machine
- **Growth Engine** — Automated A/B testing with Bayesian statistical validation
- **Twitter Automation** — AI-powered posting, engagement, and audience growth

### Content & Media
- **Remotion** — Programmatic video engine: React-based rendering, 16+ genres, TTS pipeline, post-processing (anime, cinematic, influencer, podcast, promo, docs)
- **AI Podcast** — Joe Rogan/Malcolm Gladwell style podcast creation
- **Faceless YouTube** — MrBeast-style automated YouTube content
- **Seedance** — Cinematic AI video production

### Engineering
- **Systematic Debugging** — Evidence-driven root cause analysis
- **TDD** — Test-driven development with red-green-refactor loop
- **Code Reviewer** — Production-quality review with severity ratings

### Innovation Thinking
- **Musk First Principles** — Breakthrough problem-solving
- **Steve Jobs Product Design** — Technology meets liberal arts
- **Feynman Scientific Method** — Explain complex things simply

---

## How Skills Work

Each skill contains:

1. **Expert Persona** — Credentials, expertise, and philosophy from world-class practitioners
2. **Actionable Frameworks** — Step-by-step methodologies ready for AI execution
3. **Usage Patterns** — Triggers, inputs, outputs, and integration points
4. **Quality Metrics** — Self-assessment criteria and improvement triggers

---

## Architecture

```
1ai-skills/
├── agents/        # Autonomous agent skills (14)
├── automation/    # Workflow automation & bots (21)
├── content/       # Content creation & media (22)
├── core/          # Infrastructure & memory (24)
├── data/          # Data analysis & visualization (4)
├── development/   # Coding, debugging, TDD (17)
├── devops/        # Docker, CI/CD, K8s (6)
├── integrations/  # Slack, Discord, Notion, GitHub (11)
├── marketing/     # SEO, growth, advertising (21)
├── mcp/           # MCP server skills (10)
├── meta/          # Self-improving agent system (9) ← NEW
├── operations/    # Business operations (10)
├── productivity/  # Google, calendar, email (6)
├── research/      # Analysis, investigation (25)
├── sales/         # Closing, outreach, CRM (6)
└── trading/       # Markets, algorithms (7)
```

---

## Use Cases

- **AI Agent Developers** — Add expert-level capabilities to any LLM agent
- **Automation Engineers** — Pre-built workflows for n8n, Slack, Discord, WhatsApp
- **SEO Professionals** — Technical SEO, content optimization, GEO for AI Overviews
- **Traders** — Black Edge intelligence, Polymarket analysis, crypto bots
- **Startups** — Revenue playbook, growth engine, high-ticket closing
- **DevOps Teams** — Docker, Kubernetes, CI/CD pipeline skills
- **Content Creators** — AI podcast, faceless YouTube, video generation

---

## Contributing

1. Fork the repository
2. Create a skill: `category/skill-name/SKILL.md`
3. Follow the existing SKILL.md format (persona, frameworks, usage)
4. Submit a pull request

---

## Support Development

- Star this repository
- Donate: https://www.tip.md/oyi77
- Report issues
- Contribute new skills

## License

MIT License

---

**Built by [1ai](https://github.com/oyi77) — Standing on the shoulders of giants.**
trigger CI

