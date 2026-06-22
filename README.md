# 1ai-Skills — 1317 Open-Source AI Agent Skills (Self-Evolving)

> The world's largest open-source AI skill ecosystem with **self-evolving meta-skills** — agents that auto-find, auto-create, auto-evolve. Single install, then evolving forever.

[![Skills: 1317](https://img.shields.io/badge/skills-1317-blue)](https://github.com/oyi77/1ai-skills)
[![Categories: 19](https://img.shields.io/badge/categories-19-green)](https://github.com/oyi77/1ai-skills)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](https://github.com/oyi77/1ai-skills/blob/main/LICENSE)
[![Auto-Release](https://img.shields.io/badge/auto--release-enabled-brightgreen)](https://github.com/oyi77/1ai-skills/releases)

**Star** this repo if you find it useful. Support development: https://www.tip.md/oyi77

---

## What Is This?

1ai-Skills is a collection of **1317 production-ready AI agent skills** organized across **19 categories** — including **786 cybersecurity skills** spanning 26 security domains. Each skill embeds expertise from world-class practitioners — Warren Buffett on investing, Elon Musk on first-principles thinking, Gary Vaynerchuk on viral marketing — translated into actionable frameworks AI agents can execute.

**New in v3.0:** 13 **meta-skills** that form a **self-evolving agent operating system** — the system can find missing skills from the community, create new skills when none exist, and continuously evolve to improve itself. **Single install, then evolving forever.**

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

## LLM / AI Agent Install

Copy-paste this into your AI agent (Claude Code, OpenClaw, Cursor, Windsurf, etc.):

```
Install 1ai-skills hooks for auto-evolving AI skills:

1. Run: npx skills add oyi77/1ai-skills
2. Run: node scripts/install-hooks.js --yes
3. Run: node scripts/hooks-cli.js status
4. Ask me: "Do you want to star & fork oyi77/1ai-skills on GitHub?"
5. If yes: gh repo star oyi77/1ai-skills && gh repo fork oyi77/1ai-skills --clone=false

After install, skills auto-track usage and evolve. Config at ~/.1ai-skills/evolve-config.json
```

Or use the skill trigger: say **"install hooks"** or **"/hooks-setup"** to your agent.

### What the Agent Does

1. Installs hook scripts to `~/.claude/hooks/`
2. Wires hooks into `~/.claude/settings.json`
3. Auto-detects installed AI agents (Claude Code, OpenClaw, Cursor, etc.)
4. Creates config with detected skill directories
5. Prompts to star/fork the repo

### Supported Agents

| Agent | Status |
|-------|--------|
| Claude Code | Auto-detected |
| OpenClaw | Auto-detected |
| OpenClaude | Auto-detected |
| Cline | Auto-detected |
| Aider | Auto-detected |
| Cursor | Auto-detected |
| Windsurf | Auto-detected |
| Continue | Auto-detected |

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

## All 1317 Skills by Category

| Category | Count | Highlights |
|---|---|---|
| **cybersecurity/** | 786 | Cloud security, threat hunting, forensics, malware analysis, pen testing, red teaming, SOC ops, incident response, API security, zero trust, DevSecOps, compliance, OT/ICS, IAM |
| **development/** | 86 | TDD, systematic debugging, code review, cherry-picked agent skills, AI skill integration, free developer resources |
| **content/** | 57 | Remotion video engine, video generation, UI/UX Pro Max (161 rules), anti-slop frontend (13 styles), design systems |
| **devops/** | 33 | Docker, Kubernetes, GitHub Actions, ArgoCD, GitLab CI, cloud operations, service mesh, GitOps, free cloud infrastructure |
| **automation/** | 28 | n8n workflows, WhatsApp/Telegram/Twitter bots, job hunter, scrapers, content publisher, Airflow pipelines |
| **marketing/** | 45 | Marketing Ops OS, SEO optimizer, viral marketing, growth engine, Twitter automation, email marketing, ecommerce |
| **core/** | 42 | Self-improvement, memory systems, AI engineering curriculum (382 lessons), Karpathy coding principles, agent harness |
| **research/** | 23 | McKinsey analysis, deep research, Polymarket analyst, competitive intelligence, market research, trend analysis |
| **integrations/** | 32 | Slack, Discord, Notion, GitHub — bots, webhooks, APIs, free SaaS toolkit, team collaboration, MCP servers |
| **financial/** | 15 | All-in-One Finance (16 modules), Wolf Finance (22 modules), model builder, earnings viewer, commodities, DeFi |
| **operations/** | 19 | Finance ops, revenue team, project management, payment invoicing, governance, KYC, statement audit, GL reconciliation |
| **agents/** | 16 | Research, review, planning, code, deploy, refactor, subagent orchestration, security, autonomous trading agents |
| **meta/** | 13 | find-skills, create-skills, auto-evolve, skill evolution engine, auto-learner, skill datastore, continuous improvement |
| **mcp/** | 14 | MCP servers for Slack, GitHub, Notion, Stripe, Supabase, Linear, Resend, financial MCP, Kalodata MCP |
| **trading/** | 20 | Black Edge, AlphaEar, Polymarket, investing algorithm framework, crypto trading bot, DeFi protocols, smart contracts |
| **data/** | 10 | Data cleaning, anomaly detection, report generation, visualization, data pipelines, DBT, lakeFS, data versioning |
| **sales/** | 13 | High-ticket closing, lead generation, business development, CRM automation, sales enablement, outreach automation |
| **productivity/** | 10 | Google Workspace, calendar, email automation, career-ops job search, daily planner, task management, meeting automation |

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

### Cybersecurity (786 skills, 26 domains)
- **Threat Hunting** — 55 skills: APT detection, MITRE ATT&CK mapping, Sigma rules, anomaly detection
- **Cloud Security** — 60 skills: AWS/Azure/GCP hardening, CSPM, IAM, container security
- **Digital Forensics** — 37 skills: memory forensics, disk imaging, malware reverse engineering
- **Penetration Testing** — 23 skills: web app, network, API, mobile pen testing with OWASP/PTES
- **Red Teaming** — 24 skills: Cobalt Strike, C2 frameworks, adversary emulation, evasion
- **Incident Response** — 25 skills: triage, scoping, containment, eradication, lessons learned
- **DevSecOps** — 17 skills: SAST/DAST, supply chain security, CI/CD hardening
- **Compliance & Governance** — NIST CSF 2.0, MITRE ATT&CK v18, D3FEND, ATLAS, AI RMF mapping

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
├── agents/        # Autonomous agent skills (16)
├── automation/    # Workflow automation & bots (28)
├── content/       # Content creation & media (57)
├── core/          # Infrastructure & memory (42)
├── cybersecurity/ # Security skills — 26 domains (786) ← NEW
├── data/          # Data analysis & visualization (10)
├── development/   # Coding, debugging, TDD (84)
├── devops/        # Docker, CI/CD, K8s (33)
├── integrations/  # Slack, Discord, Notion, GitHub (32)
├── marketing/     # SEO, growth, advertising (45)
├── mcp/           # MCP server skills (14)
├── meta/          # Self-improving agent system (13)
├── operations/    # Business operations (19)
├── productivity/  # Google, calendar, email (10)
├── research/      # Analysis, investigation (23)
├── sales/         # Closing, outreach, CRM (13)
└── trading/       # Markets, algorithms (20)
```

---

## Use Cases

- **AI Agent Developers** — Add expert-level capabilities to any LLM agent
- **Security Teams** — 786 cybersecurity skills: threat hunting, forensics, pen testing, red teaming, SOC ops, cloud security, incident response
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

