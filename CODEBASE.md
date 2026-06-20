# CODEBASE.md — 1ai-skills
> Auto-generated codebase memory for AI agents. Last updated: 2026-06-19.

## Purpose
The world's largest open-source AI agent skill ecosystem — 1286 production-ready skills across 18 categories with self-evolving meta-skills that auto-find, auto-create, and auto-evolve capabilities.

## Tech Stack
- **Languages**: JavaScript, Python, Bash, Markdown
- **Frameworks**: None (skill definitions, not an application)
- **Key Libraries**: Node.js scripts for hooks installation and skill management

## Entry Points
- **Main**: `scripts/install-hooks.js` (install hooks into AI agents)
- **CLI**: `scripts/hooks-cli.js` (skill hooks management)
- **Validation**: `scripts/validate-skills.py` (skill quality checks)
- **Manifest**: `SKILLS.json` (skill registry)

## Directory Structure
| Directory | Description |
|-----------|-------------|
| `agents/` | Autonomous agent skills (research, coding, computer-use, browser-use) |
| `automation/` | Workflow automation & bots (n8n, Telegram, WhatsApp, job-hunter) |
| `content/` | Content creation & media (Remotion video, AI podcast, faceless YouTube, image gen) |
| `core/` | Infrastructure & memory systems (self-improving, hive-mind, session-brain, model-router) |
| `cybersecurity/` | 785 security skills across 26 domains (threat hunting, forensics, pen testing, cloud security) |
| `data/` | Data analysis, pipelines (Airflow, Dagster, DBT, Spark) |
| `development/` | Coding, debugging, TDD, code review, subagent orchestration |
| `devops/` | Docker, K8s, CI/CD, Terraform, GitOps, service mesh |
| `financial/` | Finance skills (all-in-one-finance, wolf-finance, model-builder, earnings-viewer) |
| `integrations/` | Slack, Discord, Notion, GitHub, Linear, MCP servers |
| `marketing/` | SEO, growth, ads, email marketing, content analytics |
| `mcp/` | MCP server/client skills (Slack, GitHub, Notion, Stripe, Supabase) |
| `meta/` | Self-evolving system (find-skills, create-skills, auto-evolve, skill-evolution, auto-learner) |
| `mindset/` | Personal development (leadership, time-management, critical-thinking, negotiation) |
| `operations/` | Business operations (finance-ops, governance, KYC, legal, HR) |
| `productivity/` | Google Workspace, calendar, email automation, meeting management |
| `research/` | Analysis & investigation (McKinsey, Polymarket, Sherlock, deep research) |
| `sales/` | Closing, outreach, CRM, lead generation, business development |
| `trading/` | Markets, algorithms (Polymarket, crypto bots, DeFi, risk management) |
| `references/` | Shared checklists (SEO, marketing, code-review, trading) |
| `hooks/` | Session lifecycle hooks (session-start, pre-commit, post-task) |
| `scripts/` | Install hooks, validate skills, quality tests |
| `docs/` | Setup guides (OpenCode, Claude, Cursor, HuggingFace) |
| `manifests/` | HuggingFace space manifest, agents manifest |

## Key Files
| File | Purpose |
|------|---------|
| `SKILLS.json` | Skill registry and metadata |
| `AGENTS.md` | AI agent configuration and behavior rules |
| `llms.txt` | LLM-readable skill catalog |
| `CONTRIBUTING.md` | Contribution guide with SKILL.md anatomy requirements |
| `QUICK_START.md` | Quick start guide for installation |
| `scripts/install-hooks.js` | Auto-detect agents and install hooks |
| `scripts/hooks-cli.js` | CLI for managing skill hooks |
| `scripts/validate-skills.py` | Validate SKILL.md structure and quality |

## Architecture
Each skill is a directory containing a `SKILL.md` file with structured sections: persona, frameworks, usage patterns, quality metrics, verification checklists. Meta-skills in `meta/` form a self-evolving loop: Execute → Monitor → Collect → Recognize → Assess → Find → Create → Generate → Learn → Evolve. Hooks system auto-detects installed AI agents (Claude Code, OpenClaw, Cursor, Windsurf, etc.) and wires lifecycle hooks.

## Run Commands
```bash
npx skills add oyi77/1ai-skills    # Install all skills
node scripts/install-hooks.js --yes  # Install hooks into detected agents
node scripts/hooks-cli.js status     # Check hook installation status
python3 scripts/test_quality.py      # Run skill quality tests
python3 scripts/validate-skills.py   # Validate all SKILL.md files
```

## Environment Variables
`~/.1ai-skills/evolve-config.json` — auto-evolution configuration (created by hooks installer).
