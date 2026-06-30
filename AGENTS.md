# AGENTS.md — 1ai-skills

## This repo
Production-ready AI agent skill library — 1337 skills across 19 categories with anti-rationalization tables, code examples, and verification checklists.
Stack: Node.js / Python / YAML skills
Domain: Agent skill library — NOT a product repo. Do not add features here unless adding new skills.

## Rules — thin loader, no submodule
Engineering rules are enforced by machine-level loaders when `setup-dev.sh` has been run:
- Claude Code: SessionStart hook injects `~/.1ai/core/RULES.md`
- OpenCode: plugin injects `~/.1ai/core/RULES.md`
- OMP: wrapper appends `~/.1ai/core/RULES.md` to launch sessions

Primary rules file:
```bash
cat ~/.1ai/core/RULES.md
```

Pre-ship gate:
```bash
cat ~/.1ai/core/GATE.md
```

## What this repo is

1ai-skills provides domain-specific playbooks for AI agents. Each skill has:
- YAML frontmatter (name, description, domain, tags)
- Anti-Rationalization Table (prevents cutting corners)
- Workflow (step-by-step)
- Code examples (Python/JS/Bash)
- Verification checklist

**1ai-rules = HOW to code. 1ai-skills = WHAT to do.**

## Finding and using skills

```bash
# Find by category
ls ~/projects/1ai-skills/development/    # TDD, debugging, code review, PRD
ls ~/projects/1ai-skills/devops/         # Docker, K8s, CI/CD
ls ~/projects/1ai-skills/integrations/   # Stripe, Firebase, Supabase, GitHub
ls ~/projects/1ai-skills/cybersecurity/  # 786 security skills
ls ~/projects/1ai-skills/trading/        # Crypto, DeFi, Polymarket

# Search via brain MCP (if 1ai-hub is running)
# gbrain_search or vilona_brain_search: "stripe integration skill"

# Search SKILLS.json directly
python3 -c "
import json
s = json.load(open('SKILLS.json'))
hits = [sk for sk in s.get('skills', []) if 'stripe' in sk.get('name','').lower()]
for h in hits: print(h['name'], '-', h.get('description','')[:80])
"

# Read a skill
cat ~/projects/1ai-skills/integrations/stripe-integration/SKILL.md
```

## 19 Categories

| Category | Count | What it covers |
|----------|------:|----------------|
| cybersecurity | 786 | Threat hunting, forensics, pen testing, SOC, incident response |
| development | 92 | TDD, debugging, code review, PRD, engineering workflows |
| content | 64 | Video, audio, design, writing, docs |
| mindset | 55 | Negotiation, leadership, critical thinking |
| marketing | 45 | SEO, viral content, email, ads, growth |
| core | 44 | AI infrastructure, memory, self-improvement, model routing |
| integrations | 36 | GitHub, Discord, Notion, Slack, Stripe, Firebase, Supabase |
| devops | 33 | Docker, Kubernetes, CI/CD, cloud ops, GitOps |
| automation | 28 | Bots, workflows, scrapers, process automation |
| research | 23 | Deep research, market analysis, competitive intelligence |
| trading | 20 | Crypto, DeFi, Polymarket, trading strategies |
| operations | 19 | Business ops, governance, HR, legal, project management |
| agents | 16 | AI agent orchestration, coding, research, autonomous execution |
| mcp | 14 | Model Context Protocol servers and tool integrations |
| financial | 15 | Finance analysis, valuation, tax, portfolio management |
| sales | 14 | Lead gen, CRM, outreach, sales automation |
| data | 10 | Data pipelines, analysis, visualization, ETL |
| productivity | 10 | Calendars, email, meetings, workspace management |
| meta | 13 | Self-evolving meta-skills, performance monitoring |

## Hard rules
1. Read code before writing code.
2. No completion claim without literal receipt.
3. Compile/test/use like a real user before claiming work is ready.
4. Task must match this repo domain (adding/improving skills).
5. Run GATE.md before commit/PR.

## Commands
- Test: `python3 scripts/test-skills.py`
- Lint: `python3 scripts/lint-skills.py`
- Audit: `bash scripts/audit-skills.sh`
- Sync to brain: `bash ~/.1ai/scripts/sync-to-brain.sh`
