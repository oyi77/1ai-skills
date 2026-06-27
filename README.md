# 1ai-skills

**Your AI agent is lazy. These 1337 skills fix that.**

AI agents skip tests, ignore security, write placeholder code, and cut corners whenever they can. 1ai-skills forces them to follow real workflows with anti-rationalization tables, code examples, and verification checklists — across every domain.

[![Skills](https://img.shields.io/badge/Skills-1337-blue?style=flat-square)](https://github.com/oyi77/1ai-skills)
[![Tested](https://img.shields.io/badge/Tests-100%25%20Pass-brightgreen?style=flat-square)](https://github.com/oyi77/1ai-skills/blob/main/scripts/test-skills.py)
[![Warnings](https://img.shields.io/badge/Warnings-0-brightgreen?style=flat-square)](https://github.com/oyi77/1ai-skills/blob/main/scripts/test-skills.py)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/oyi77/1ai-skills/blob/main/LICENSE)
[![Categories](https://img.shields.io/badge/Categories-19-purple?style=flat-square)](https://oyi77.is-a.dev/1ai-skills/)

---

## The Problem

Your AI agent says:

> "I'll add tests later." "Security is a nice-to-have." "This placeholder works fine."

It doesn't. It won't. It never does.

## The Solution

Every skill in this library includes an **Anti-Rationalization Table** — a structured argument that prevents your agent from cutting corners:

```markdown
| Rationalization | Reality |
|---|---|
| "Tests slow me down" | Bugs slow you down 10x more. Tests are speed, not overhead. |
| "I will refactor later" | Technical debt compounds. Refactor as you go. |
| "It works on my machine" | If it is not in CI, it does not work. Ship proof, not claims. |
```

---

## Quick Start

### Claude Code (Recommended)

```bash
/plugin marketplace add oyi77/1ai-skills
/plugin install 1ai-skills@1ai-skills
```

### Cursor

```bash
git clone https://github.com/oyi77/1ai-skills.git
cp -r 1ai-skills/cybersecurity/* .cursor/rules/
```

### Gemini CLI

```bash
gemini skills install https://github.com/oyi77/1ai-skills.git --path skills
```

### Any Agent

```bash
git clone https://github.com/oyi77/1ai-skills.git
# Point your agent to the skills/ directory
```

---

## 1337 Skills Across 19 Categories

| Category | Skills | What It Covers |
|---|---:|---|
| Cybersecurity | 786 | Threat hunting, forensics, pen testing, SOC ops, incident response |
| Development | 92 | TDD, debugging, code review, PRD, engineering workflows |
| Content | 64 | Video, audio, design, writing, document generation |
| Mindset | 55 | Negotiation, leadership, critical thinking, productivity |
| Marketing | 45 | SEO, viral content, email, ads, growth |
| Core | 44 | AI infrastructure, memory, self-improvement, model routing |
| Integrations | 36 | GitHub, Discord, Notion, Slack, Stripe, Firebase, Supabase |
| DevOps | 33 | Docker, Kubernetes, CI/CD, cloud ops, GitOps |
| Automation | 28 | Bots, workflows, scrapers, process automation |
| Research | 23 | Deep research, market analysis, competitive intelligence |
| Trading | 20 | Crypto, DeFi, Polymarket, trading strategies |
| Operations | 19 | Business ops, governance, HR, legal, project management |
| Agents | 16 | AI agent orchestration, coding, research, autonomous execution |
| MCP | 14 | Model Context Protocol servers and tool integrations |
| Meta | 13 | Self-evolving meta-skills, performance monitoring |
| Financial | 15 | Finance analysis, valuation, tax, portfolio management |
| Sales | 14 | Lead generation, CRM, outreach, sales automation |
| Data | 10 | Data pipelines, analysis, visualization, ETL |
| Productivity | 10 | Calendars, email, meetings, workspace management |

---

## What Makes This Different

| | Other repos | 1ai-skills |
|---|---|---|
| **Skills** | 24-100 curated | **1337 tested** |
| **Anti-rationalization** | Some | **Every skill** |
| **Code examples** | Some | **Every skill** |
| **Test suite** | None | **8-dimension, 100% pass** |
| **Cybersecurity** | None | **786 skills** |
| **Verification checklists** | Some | **Every skill** |
| **Dynamic website** | Static | **Auto-generated from data** |
| **Self-evolving** | No | **Meta-skills that improve** |

---

## Every Skill Has

- **YAML frontmatter** — Machine-readable metadata (name, description, domain, tags)
- **Anti-Rationalization Table** — Prevents agents from cutting corners
- **Code Examples** — Concrete, runnable code (Python, JS, Bash, SQL)
- **Workflow** — Step-by-step instructions with bold labels
- **When to Use** — 3+ trigger conditions
- **When NOT to Use** — 2+ contraindications
- **Verification Checklist** — Success criteria you can check

---

## Test Suite

```bash
python3 scripts/test-skills.py           # Full test
python3 scripts/test-skills.py --quick   # Skip SDK checks
python3 scripts/test-skills.py --json    # JSON output
python3 scripts/test-skills.py --skill NAME  # Single skill
```

**8 test dimensions:**
1. Structure (YAML frontmatter, required fields)
2. Content (sections, depth, no placeholders)
3. Code syntax (Python `ast.parse`, JS/TS, Bash)
4. Internal links (all `/skills/` links resolve)
5. Description quality (50-200 chars, action-oriented)
6. Quality markers (anti-rationalization, code, verification)
7. SDK availability (referenced imports are installable)
8. Workflow completeness (has workflow section)

**Result: 1337/1337 PASS · 0 warnings · 0 failures**

---

## New Skills (Just Added)

| Skill | Category | What It Does |
|---|---|---|
| docx-creator | content | Generate Word documents programmatically |
| pdf-creator | content | Create, edit, extract PDFs |
| pptx-creator | content | Build PowerPoint presentations |
| xlsx-creator | content | Create Excel spreadsheets with formulas |
| canvas-design | content | Generative art, SVG, data visualizations |
| frontend-ui-design | content | React/Vue UI components, design systems |
| theme-factory | content | Design tokens, color systems, typography |
| gemini-api-dev | core | Google Gemini API integration |
| replicate-runner | core | Run AI models on Replicate cloud |
| model-router | core | Multi-provider LLM routing |
| stripe-integration | integrations | Stripe payments and subscriptions |
| supabase-integration | integrations | Supabase auth, DB, real-time |
| firebase-integration | integrations | Firebase auth, Firestore, functions |
| bigquery-integration | integrations | BigQuery analytics and SQL |
| spec-driven-development | development | PRD-first workflow |
| context-engineering | development | Agent context window design |
| browser-testing-devtools | development | Playwright E2E testing |
| git-workflow-mastery | development | Advanced Git workflows |

---

## Self-Evolving System

1ai-skills includes 13 meta-skills that make the library improve itself:

- **skill-tracker** — Logs every skill invocation with metrics
- **skill-evolver** — Analyzes usage patterns and suggests improvements
- **skill-feedback-capture** — Captures user feedback on skill quality
- **auto-learner** — Learns from corrections and updates skills
- **performance-monitor** — Tracks skill success rates and response quality
- **skill-banner** — Shows activation banner with skill summary

---

## Slash Commands

| Command | What It Does |
|---|---|
| `/find` | Search and activate the right skill |
| `/audit` | Run comprehensive skill library audit |
| `/lint` | Lint and fix skill content quality |
| `/new-skill` | Create a new skill from template |

---

## For Contributors

```bash
# Create a new skill
python3 scripts/generate-site.py          # Regenerate website
bash scripts/audit-skills.sh --write      # Update SKILLS.json
python3 scripts/validate-skills.py        # Validate structure
python3 scripts/test-skills.py            # Run all tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Compatible With

- Claude Code
- Cursor
- Gemini CLI / Antigravity
- Windsurf
- OpenCode
- GitHub Copilot
- Kiro
- Any agent that reads SKILL.md files

---

## License

MIT — use freely, contribute back.

---

**Star this repo if it saves your agent from being lazy.**
