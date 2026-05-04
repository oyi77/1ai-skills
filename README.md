# 1ai-Skills — 216 Open-Source AI Agent Skills (Self-Evolving)

> The world's largest open-source AI skill ecosystem with **self-evolving meta-skills** — agents that auto-find, auto-create, auto-evolve. Single install, then evolving forever.

[![Skills: 213](https://img.shields.io/badge/skills-216-blue)](https://github.com/oyi77/1ai-skills)
[![Categories: 16](https://img.shields.io/badge/categories-16-green)](https://github.com/oyi77/1ai-skills)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](https://github.com/oyi77/1ai-skills/blob/main/LICENSE)
[![Auto-Release](https://img.shields.io/badge/auto--release-enabled-brightgreen)](https://github.com/oyi77/1ai-skills/releases)

**Star** this repo if you find it useful. Support development: https://www.tip.md/oyi77

---

## What Is This?

1ai-Skills is a collection of **216 production-ready AI agent skills** organized across **16 categories**. Each skill embeds expertise from world-class practitioners — Warren Buffett on investing, Elon Musk on first-principles thinking, Gary Vaynerchuk on viral marketing — translated into actionable frameworks AI agents can execute.

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

## All 213 Skills by Category

| Category | Count | Highlights |
|---|---|---|
| **research/** | 25 | McKinsey analysis, deep research, Polymarket analyst, continuous learning |
| **core/** | 24 | Self-improvement, memory systems, AI orchestration, session brain |
| **content/** | 22 | Video generation, AI podcast, faceless YouTube, humanizer, Seedance |
| **marketing/** | 21 | SEO optimizer, viral marketing, growth engine, Twitter automation |
| **automation/** | 21 | n8n workflows, WhatsApp/Telegram/Twitter bots, job hunter, scrapers |
| **development/** | 17 | TDD, systematic debugging, code review, PRD generator, git worktrees |
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
- **Black Edge** — Hidden market intelligence from satellite imagery, dark pools, options flow
- **AlphaEar Strategy** — Multi-signal trading: news + sentiment + options
- **Value Investing** — Warren Buffett's capital allocation framework
- **Rothschild Dynasty** — 250-year wealth preservation methodology

### Marketing and Growth
- **SEO Optimizer** — Full-stack SEO with content attack briefs and GSC optimization
- **Viral Marketing** — Gary Vaynerchuk's high-volume content machine
- **Growth Engine** — Automated A/B testing with Bayesian statistical validation
- **Twitter Automation** — AI-powered posting, engagement, and audience growth

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
