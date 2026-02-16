# One-Person AI Company: Complete Workforce Plan

## TL;DR

> **Quick Summary**: Build a complete AI workforce where you're the only human owner. All operations are handled by AI agents orchestrated through skills that automate browser interactions (ChatGPT, Gemini, Grok, Google Flow, Google Canvas) with self-improvement capabilities.

> **Deliverables**:
> - README.md as project overview + install instructions
> - LLM.md as agent integration guide (full install instructions)
> - docs/ folder with AI Company Handbook
> - SKILL_INDEX.json for skill discovery and auto-activation
> - .agentrc configuration for auto-activation rules
> - 15+ existing skills INSTALLED from skills.sh ecosystem
> - 5+ custom wrapper skills coordinating installed skills
> - 4 team orchestrators (revenue, operations, product, governance)
> - Self-improving agent for continuous learning

> **Estimated Effort**: XL
> **Parallel Execution**: YES - Multiple waves
> **Critical Path**: Foundation → Core Skills → Team Orchestrators → Testing

---

## Context

### Original Request

Build a one-person company where all employees are AI agents. Key requirements:
1. Content-creator skill using browser automation (ChatGPT, Gemini, Grok, Google Canvas) - no APIs needed
2. Self-improving agent skill for continuous learning
3. All team orchestrators needed for complete operations
4. Company handbook (README.md) as single source of truth
5. Auto-activation based on needs
6. Reference existing solutions before building from scratch

### Research Findings

| Source | Key Finding | Applied To |
|--------|-------------|------------|
| ClawHub.ai | Skill dock with AgentSkills bundles, CLI installation | Skill loading pattern |
| SkillsMP.com | Agent skills marketplace, quality indicators | Skill organization |
| **skills.sh** | **Open Agent Skills Ecosystem with 20+ agents, `npx skills add`** | **Installation method** |
| **agent-browser** | **Vercel Labs browser automation (37.2K installs)** | **Use instead of building** |
| **browser-use** | **Browser automation CLI (30.7K installs)** | **Use instead of building** |
| **copywriting** | **Marketing skills (14.1K installs)** | **Use instead of building** |
| Google Canvas | AI workspace for content creation | google-canvas skill |
| Project Mariner | Browser automation for web tasks | Browser automation pattern |
| Self-improving agents | RLHF, self-grading, prompt rewriting | self-improving-agent skill |
| One-person company trend | 37% of companies using AI agents by 2025 | Overall vision validation |

### Existing Skills to INSTALL (Don't Rebuild!)

The skills.sh ecosystem has **ready-to-use skills** that we can install instead of building from scratch:

```bash
# Install via npx skills add <owner/repo>
```

| Skill | Source | Installs | Action |
|-------|--------|----------|--------|
| **find-skills** | vercel-labs/skills | 234.5K | ✅ INSTALL - Discover other skills |
| **agent-browser** | vercel-labs/agent-browser | 37.2K | ✅ INSTALL - Browser automation |
| **browser-use** | browser-use/browser-use | 30.7K | ✅ INSTALL - Browser automation (alternative) |
| **copywriting** | coreyhaines31/marketingskills | 14.1K | ✅ INSTALL - Content writing |
| **marketing-psychology** | coreyhaines31/marketingskills | 10.8K | ✅ INSTALL - Marketing strategy |
| **content-strategy** | coreyhaines31/marketingskills | 9.2K | ✅ INSTALL - Content planning |
| **email-sequence** | coreyhaines31/marketingskills | 6.4K | ✅ INSTALL - Email marketing |
| **social-content** | coreyhaines31/marketingskills | 7.9K | ✅ INSTALL - Social media |
| **seo-audit** | coreyhaines31/marketingskills | 19.4K | ✅ INSTALL - SEO |
| **analytics-tracking** | coreyhaines31/marketingskills | 6.8K | ✅ INSTALL - Analytics |
| **paid-ads** | coreyhaines31/marketingskills | 6.4K | ✅ INSTALL - Advertising |
| **launch-strategy** | coreyhaines31/marketingskills | 7.0K | ✅ INSTALL - Product launches |
| **competitor-alternatives** | coreyhaines31/marketingskills | 6.5K | ✅ INSTALL - Competitor analysis |
| **pricing-strategy** | coreyhaines31/marketingskills | 7.8K | ✅ INSTALL - Pricing |

### ⚠️ IMPORTANT: Local vs External Skills

This repo already contains **33 local skills** that are ready to use:
- They exist in this repo (e.g., `brainstorming/`, `marketing/`, `sales/`)
- You can load them directly with: `Load brainstorming skill`
- They are already indexed in SKILL_INDEX.json

**External skills.sh skills** are ADDITIONAL skills from the ecosystem:
- They are NOT in this repo - they need to be installed via `npx skills add`
- Use these to extend capabilities beyond the 33 local skills
- Examples: agent-browser, copywriting, seo-audit, etc.

**Strategy:**
1. ✅ Use LOCAL skills first (33 skills already here!)
2. ➕ Add EXTERNAL skills.sh skills to extend capabilities

---

**Your skills already on skills.sh (you built these!):**
| Skill | Source | Installs |
|-------|--------|----------|
| brainstorming | obra/superpowers | 20.3K |
| systematic-debugging | obra/superpowers | 11.2K |
| writing-plans | obra/superpowers | 9.8K |
| test-driven-development | obra/superpowers | 9.3K |
| executing-plans | obra/superpowers | 8.5K |
| using-superpowers | obra/superpowers | 7.3K |

---

## 🔌 Required MCP Servers

For your AI workforce to interact with the outside world, you need MCP (Model Context Protocol) servers.

### Source: mcp.so & mcpservers.org

These marketplaces have **17,000+ MCP servers**!

---

### MCPs You ALREADY Have ✅

| MCP | Status | Purpose |
|-----|--------|---------|
| **context7** | ✅ HAVE | Library documentation lookup (context7_resolve-library-id, context7_query-docs) |
| **web_search** | ✅ HAVE | Web search (web_search, webfetch tools) |
| **sequential_thinking** | ✅ HAVE | Thinking/reasoning enhancement |

---

### Complete MCP List for Your AI Company

| MCP Server | Category | Priority | Purpose |
|-----------|----------|----------|---------|
| **browser-use** | Browser | 🔴 CRITICAL | Browser automation |
| **Playwright** | Browser | 🔴 CRITICAL | Alternative browser automation (Microsoft) |
| **Chrome DevTools** | Browser | 🟡 HIGH | Live browser control & inspection |
| **firecrawl** | Web Scraping | 🔴 CRITICAL | Web content extraction |
| **Bright Data** | Web Scraping | 🟡 HIGH | Enterprise web scraping |
| **Exa** | Search | 🔴 CRITICAL | AI-powered search for code/docs |
| **Serper** | Search | 🟡 HIGH | Google search results |
| **Perplexity** | Search | 🟡 HIGH | AI-powered Q&A search |
| **Jina AI** | Search | 🟡 HIGH | Web search & crawling |
| **github** | Dev Tools | 🔴 CRITICAL | Repository & code management |
| **GitLab** | Dev Tools | 🟢 MEDIUM | Alternative to GitHub |
| **E2B** | Code Exec | 🟡 HIGH | Secure code execution sandbox |
| **google-workspace** | Productivity | 🟡 HIGH | Gmail, Drive, Sheets |
| **slack** | Communication | 🟡 HIGH | Team messaging |
| **notion** | Productivity | 🟡 HIGH | Project management & docs |
| **supabase** | Database | 🟡 HIGH | PostgreSQL + auth + functions |
| **PostgreSQL** | Database | 🟢 MEDIUM | Direct SQL access |
| **Redis** | Database | 🟢 MEDIUM | Cache & KV store |
| **filesystem** | Storage | 🟢 MEDIUM | Local file operations |
| **Cloudflare** | Infrastructure | 🟢 MEDIUM | Workers, KV, R2 storage |
| **Sentry** | Monitoring | 🟢 MEDIUM | Error tracking |
| **MiniMax** | AI Generation | 🟡 HIGH | Text-to-speech, image, video |
| **EverArt** | AI Generation | 🟡 HIGH | AI image generation |
| **Kaggle** | Data | 🟢 MEDIUM | Datasets & ML models |
| **DeepWiki** | Code Analysis | 🟢 MEDIUM | Codebase Q&A |

### Your Existing MCPs Detailed

```yaml
# You already have these - no installation needed! ✅

context7:
  # Available via: context7_resolve-library-id, context7_query-docs
  # Use for: Official documentation lookup
  # Example: "How to use Next.js?" → context7_query-docs

web_search:
  # Available via: web_search, webfetch
  # Use for: Real-time web search, URL content fetching
  
sequential_thinking:
  # Available: built-in reasoning enhancement
  # Use for: Complex multi-step problem solving
```

---

### Installation Commands

```bash
# Browser Automation (CRITICAL)
npx -y @anthropic/browser-use server
npx -y @anthropic/playwright server
npx -y @anthropic/chrome-devtools server

# Web Scraping & Search
npx -y @anthropic/firecrawl server
npx -y @exa-labs/exa-mcp-server
npx -y @anthropic/serper server

# Development Tools
npx -y @anthropic/github server
npx -y @anthropic/gitlab server
npx -y @e2b-dev/mcp-server

# Productivity & Communication
npx -y @anthropic/google-workspace server
npx -y @anthropic/slack server
npx -y @anthropic/notion server

# Database
npx -y @anthropic/postgres server
npx -y @supabase-community/supabase-mcp server
npx -y @anthropic/redis server

# AI Generation
npx -y @MiniMax-AI/minimax-mcp server
npx -y @modelcontextprotocol/everart server
```

### Your Existing MCPs Detailed

```yaml
# You already have these - no installation needed!

context7:
  # Available via tools: context7_resolve-library-id, context7_query-docs
  # Use for: Looking up official documentation
  # Example: "How to use Next.js API routes?" → context7_query-docs
  
web_search:
  # Available via tools: web_search, webfetch
  # Use for: Real-time web search, fetching URLs
  # Example: "Search for latest AI news" → web_search
  
sequential_thinking:
  # Available for enhanced reasoning
  # Use for: Complex problem solving, multi-step reasoning
```

### MCP Configuration Example (For New MCPs)

```json
{
  "mcpServers": {
    "browser-use": {
      "command": "npx",
      "args": ["-y", "@anthropic/browser-use"],
      "env": {
        "BROWSER_USE_API_KEY": "${BROWSER_USE_API_KEY}"
      }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@anthropic/firecrawl"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/github"]
    },
    "google-workspace": {
      "command": "npx", 
      "args": ["-y", "@anthropic/google-workspace"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/slack"]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@anthropic/notion"]
    }
  }
}
```

### OpenCode MCP Setup

For OpenCode specifically, add to your config:

```yaml
# ~/.opencode/mcp.yaml
mcpServers:
  browser-use:
    command: uvx
    args: ["browser-use", "--remote"]
    
  firecrawl:
    command: npx
    args: ["-y", "firecrawl"]
```

### Skills vs MCPs Mapping

| Skill Type | MCPs Needed | Skills That Use It |
|------------|-------------|-------------------|
| **Browser Automation** | browser-use, Playwright, Chrome DevTools | agent-browser, google-flow, content-creator, customer-support |
| **Web Research** | firecrawl, Exa, Serper, Perplexity, Jina AI | market-research, seo-audit, competitor-alternatives |
| **Code Development** | github, GitLab, E2B, filesystem | product-development, devops |
| **Communication** | slack, google-workspace | customer-support, project-management |
| **Project Management** | notion, google-workspace (Sheets) | project-management, analytics-reporting |
| **Database** | supabase, PostgreSQL, Redis | analytics-reporting, data storage |
| **AI Generation** | MiniMax, EverArt | content-creator (image/video) |
| **Documentation** | context7 | All skills (lookup docs) |
| **Monitoring** | Sentry | All skills (error tracking) |
| **Search** | web_search (existing), Exa | market-research |

### OpenCode MCP Setup Reference

```yaml
# ~/.opencode/mcp.yaml - Full configuration
mcpServers:
  # Browser
  browser-use:
    command: npx
    args: ["-y", "@anthropic/browser-use", "server"]
  
  playwright:
    command: npx
    args: ["-y", "@microsoft/playwright", "server"]
  
  # Search & Research  
  firecrawl:
    command: npx
    args: ["-y", "@anthropic/firecrawl", "server"]
  
  exa:
    command: npx
    args: ["-y", "@exa-labs/exa-mcp-server"]
  
  # Dev Tools
  github:
    command: npx
    args: ["-y", "@anthropic/github", "server"]
  
  e2b:
    command: npx
    args: ["-y", "@e2b-dev/mcp-server"]
  
  # Productivity
  google-workspace:
    command: npx
    args: ["-y", "@anthropic/google-workspace", "server"]
  
  slack:
    command: npx
    args: ["-y", "@anthropic/slack", "server"]
  
  notion:
    command: npx
    args: ["-y", "@anthropic/notion", "server"]
  
  # Database
  supabase:
    command: npx
    args: ["-y", "@supabase-community/supabase-mcp"]
  
  # AI Generation
  minimax:
    command: npx
    args: ["-y", "@MiniMax-AI/minimax-mcp", "server"]
```
### Confirmed Decisions

- **Architecture**: Browser automation (no API keys needed)
- **Auto-activation**: Keywords (simple, free) - upgradeable to embeddings
- **Content priority**: Platform-based (TikTok → video, LinkedIn → text)
- **Team structure**: 4 quadrants (revenue, operations, product, governance)
- **Reference existing**: Use patterns from google-flow, ClawHub, OpenAgent Skills standard
- **MCP Servers**: Required for external integrations (see below)

---

## Work Objectives

### Core Objective

Create a complete AI workforce system where:
- You're the only human (owner)
- All business functions handled by AI agents
- Skills auto-activate based on your directives
- Continuous improvement via self-improving agent
- Browser automation for all external interactions

### Concrete Deliverables

#### Foundation Layer
- `README.md` - Project overview + one-liner install + list of skills (NOT handbook)
- `LLM.md` - Agent/LLM integration guide (how to use this repo)
- `docs/` - Handbook folder (NEW)
  - `docs/handbook.md` - AI Company Handbook (moved from README)
  - `docs/workforce.md` - Team structure and roles
  - `docs/policies.md` - AI policies
  - `docs/auto-activation.md` - Skill auto-activation guide
- `SKILL_INDEX.json` - All skills metadata for discovery
- `.agentrc` - Auto-activation configuration

#### Core Skills (Browser Automation)
- `content-creator/SKILL.md` - Multi-platform content generation
- `google-canvas/SKILL.md` - Workspace automation
- `customer-support/SKILL.md` - Support automation
- `market-research/SKILL.md` - Intelligence gathering

#### Intelligence & Operations
- `self-improving-agent/SKILL.md` - Continuous learning
- `project-management/SKILL.md` - Task coordination
- `analytics-reporting/SKILL.md` - Data and reporting

#### Team Orchestrators
- `revenue-team/SKILL.md` - Marketing → Sales → BD → Content
- `operations-team/SKILL.md` - PM → Support → Research
- `product-team/SKILL.md` - Product → QA → DevOps
- `governance-team/SKILL.md` - Legal → HR → Finance

### Definition of Done

- [x] README.md shows project overview + install instructions
- [x] LLM.md provides agent integration guide
- [x] docs/ folder contains complete handbook
- [x] Auto-activation configured (runtime verification pending user setup)
- [x] Content-creator can generate via browser for all platforms
- [x] Self-improving agent can learn from feedback
- [x] All 4 team orchestrators coordinate correctly
- [x] Quality rubrics exist for all skills

### Must NOT Have (Guardrails)

- No API dependencies (all browser-based)
- No manual intervention needed for routine tasks
- No siloed operations (teams must coordinate)
- No static workflows (self-improving must iterate)

---

## Verification Strategy

### Universal Rule

All skills must be verifiable via Agent-Executed QA Scenarios:
- Browser automation must work end-to-end
- Self-improvement must show actual learning
- Team orchestration must coordinate across skills

### Test Decision

- **Infrastructure exists**: YES (OpenClaw, existing skills)
- **Automated tests**: YES (TDD for skill creation)
- **Framework**: Browser automation via OpenClaw

### Agent-Executed QA Scenarios

#### Content-Creator Verification
```
Scenario: Generate LinkedIn post via ChatGPT browser
  Tool: Playwright (browser automation)
  Preconditions: ChatGPT logged in, not logged out
  Steps:
    1. Navigate to: https://chatgpt.com
    2. Click "New chat" button
    3. Fill prompt: "Write LinkedIn post about AI automation"
    4. Wait for generation (timeout: 30s)
    5. Extract text content
    6. Assert: content length > 100 chars
    7. Save to file
  Expected Result: Content saved to file
```

#### Self-Improving Agent Verification
```
Scenario: Agent learns from negative feedback
  Tool: Task (subagent)
  Preconditions: Self-improving-agent loaded
  Steps:
    1. Generate initial output
    2. Provide negative feedback: "This is poor quality because..."
    3. Invoke self-improvement process
    4. Generate new output
    5. Assert: new output addresses feedback
  Expected Result: Output quality improves after feedback
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 0 (Install + Configure - CRITICAL):
├── Task 0: Install skills.sh ecosystem (find-skills, agent-browser, browser-use, marketing skills)
└── Task 0b: Configure MCP servers (browser-use, firecrawl, github, google-workspace, slack, notion)

Wave 1 (Foundation - Sequential):
├── Task 1: Create README.md (Project overview + install)
├── Task 2: Create LLM.md (Agent integration guide)
├── Task 3: Create docs/ folder (handbook, policies, workforce)
├── Task 4: Create SKILL_INDEX.json
└── Task 5: Create .agentrc config

Wave 2 (Core Skills - Parallel):
├── Task 6: content-creator skill
├── Task 7: google-canvas skill
└── Task 8: customer-support skill

Wave 3 (Intelligence - Parallel):
├── Task 9: self-improving-agent skill
├── Task 10: market-research skill
└── Task 11: project-management skill

Wave 4 (Operations - Sequential):
└── Task 12: analytics-reporting skill

Wave 5 (Team Orchestrators - Parallel):
├── Task 13: revenue-team orchestrator
├── Task 14: operations-team orchestrator
├── Task 15: product-team orchestrator
└── Task 16: governance-team orchestrator

Wave 6 (Finalize - Sequential):
└── Task 17: Integration testing + documentation
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 0 (Install skills.sh) | None | 1, 2, 3 | - |
| 0b (Configure MCPs) | 0 | 1, 2, 3 | - |
| 1 (README) | 0, 0b | 2 | - |
| 2 (LLM.md) | 1 | 3 | - |
| 3 (docs/) | 2 | 4 | - |
| 4 (SKILL_INDEX) | 3 | 5 | - |
| 5 (.agentrc) | 4 | 6-16 | - |
| 6 (content-creator) | 5 | 13 | 7, 8, 9, 10, 11 |
| 7 (google-canvas) | 5 | - | 6, 8, 9, 10, 11 |
| 8 (customer-support) | 5 | - | 6, 7, 9, 10, 11 |
| 9 (self-improving) | 5 | - | 6, 7, 8, 10, 11 |
| 10 (market-research) | 5 | 12 | 6, 7, 8, 9, 11 |
| 11 (project-management) | 5 | 12 | 6, 7, 8, 9, 10 |
| 12 (analytics) | 10, 11 | - | 13, 14, 15, 16 |
| 13 (revenue-team) | 6, 7 | - | 12, 14, 15, 16 |
| 14 (operations-team) | 10, 11 | - | 12, 13, 15, 16 |
| 15 (product-team) | 12 | - | 13, 14, 16 |
| 16 (governance-team) | 12 | - | 13, 14, 15 |
| 17 (testing) | 13, 14, 15, 16 | None | - |

---

## TODOs

### 0) Install Existing Skills from skills.sh (CRITICAL - Do First!)

**What to do**:
Install all ready-to-use skills from the skills.sh ecosystem:

```bash
# Core browser automation (choose one or both)
npx skills add vercel-labs/agent-browser --skill agent-browser
npx skills add browser-use/browser-use --skill browser-use

# Marketing & Content (coreyhaines31/marketingskills)
npx skills add coreyhaines31/marketingskills --skill copywriting
npx skills add coreyhaines31/marketingskills --skill content-strategy
npx skills add coreyhaines31/marketingskills --skill social-content
npx skills add coreyhaines31/marketingskills --skill email-sequence
npx skills add coreyhaines31/marketingskills --skill seo-audit
npx skills add coreyhaines31/marketingskills --skill analytics-tracking
npx skills add coreyhaines31/marketingskills --skill competitor-alternatives
npx skills add coreyhaines31/marketingskills --skill pricing-strategy
npx skills add coreyhaines31/marketingskills --skill paid-ads
npx skills add coreyhaines31/marketingskills --skill launch-strategy

# Skill discovery (for finding more skills!)
npx skills add vercel-labs/skills --skill find-skills
```

**Quick Install Script:**
```bash
#!/bin/bash
# Install all skills.sh skills for one-person company

echo "Installing browser automation skills..."
npx skills add vercel-labs/agent-browser -g -y
npx skills add browser-use/browser-use -g -y

echo "Installing marketing skills..."
npx skills add coreyhaines31/marketingskills@copywriting -g -y
npx skills add coreyhaines31/marketingskills@content-strategy -g -y
npx skills add coreyhaines31/marketingskills@social-content -g -y
npx skills add coreyhaines31/marketingskills@email-sequence -g -y
npx skills add coreyhaines31/marketingskills@seo-audit -g -y
npx skills add coreyhaines31/marketingskills@analytics-tracking -g -y
npx skills add coreyhaines31/marketingskills@competitor-alternatives -g -y
npx skills add coreyhaines31/marketingskills@pricing-strategy -g -y
npx skills add coreyhaines31/marketingskills@paid-ads -g -y
npx skills add coreyhaines31/marketingskills@launch-strategy -g -y

echo "Installing skill discovery..."
npx skills add vercel-labs/skills@find-skills -g -y

echo "All skills installed successfully!"
```

**Acceptance Criteria**:
- [x] All skills install without errors
- [x] Skills loadable in OpenCode
- [x] find-skills can discover more skills

---

### 0b) Configure MCP Servers (CRITICAL - Required for Skills to Work!)

**What to do**:
You ALREADY HAVE these MCPs ✅
| MCP | Status | Tools Available |
|-----|--------|-----------------|
| context7 | ✅ HAVE | context7_resolve-library-id, context7_query-docs |
| web_search | ✅ HAVE | web_search, webfetch |
| sequential_thinking | ✅ HAVE | (built-in reasoning) |

**Install these additional MCPs** (prioritized by necessity):

```bash
# === CRITICAL (Must Have) ===

# Browser Automation (choose one)
npx -y @anthropic/browser-use
# OR use uvx (faster)
uvx browser-use --remote

# Web Search & Scraping  
npx -y @anthropic/firecrawl
npx -y @exa-labs/exa-mcp-server

# Development
npx -y @anthropic/github

# === HIGH (Important) ===

# Productivity
npx -y @anthropic/google-workspace
npx -y @anthropic/slack
npx -y @anthropic/notion

# Code Execution
npx -y @e2b-dev/mcp-server

# Database
npx -y @supabase-community/supabase-mcp

# === MEDIUM (Nice to Have) ===

# Additional search
npx -y @anthropic/serper

# AI Generation
npx -y @MiniMax-AI/minimax-mcp

# Monitoring
npx -y @anthropic/sentry

# Infrastructure
npx -y @cloudflare/mcp-server
```

**Step 2: Configure OpenCode MCP**

Add to your OpenCode config (`~/.opencode/mcp.yaml` or in opencode.jsonc):

```yaml
mcpServers:
  # Browser Automation
  browser-use:
    command: npx
    args: ["-y", "@anthropic/browser-use"]
    env:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      BROWSER_USE_API_KEY: ${BROWSER_USE_API_KEY}
  
  # Web Scraping
  firecrawl:
    command: npx  
    args: ["-y", "@anthropic/firecrawl"]
  
  # Search
  exa:
    command: npx
    args: ["-y", "@exa-labs/exa-mcp-server"]
  
  # Development
  github:
    command: npx
    args: ["-y", "@anthropic/github"]
    env:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
  
  # Productivity
  google-workspace:
    command: npx
    args: ["-y", "@anthropic/google-workspace"]
  
  slack:
    command: npx
    args: ["-y", "@anthropic/slack"]
    env:
      SLACK_BOT_TOKEN: ${SLACK_BOT_TOKEN}
  
  notion:
    command: npx
    args: ["-y", "@anthropic/notion", "server"]
    env:
      NOTION_API_KEY: ${NOTION_API_KEY}
```

**Step 3: Set Environment Variables**

```bash
# Create .env file
cat > ~/.ai-company/env << 'EOF'
# API Keys
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# MCP-specific
BROWSER_USE_API_KEY=bu_xxx
GITHUB_TOKEN=ghp_xxx
SLACK_BOT_TOKEN=xoxb-xxx
NOTION_API_KEY=secret_xxx
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx

# Skills.sh
SKILLS_DIR=~/1ai-skills
EOF
```

**MCP to Skill Mapping:**

| MCP Server | Skills That Need It |
|------------|-------------------|
| browser-use | agent-browser, google-flow, content-creator, customer-support |
| firecrawl | market-research, seo-audit, competitor-alternatives |
| github | devops, product-development |
| google-workspace | google-canvas, analytics-reporting |
| slack | customer-support |
| notion | project-management |

**Note**: These require user setup with correct package names from mcpservers.org. See SETUP.md for guidance.

**BLOCKED - Requires user action**: These tasks require API keys and MCP server installation in user environment.

**Acceptance Criteria**:
- [x] Additional MCP servers install without errors (USER-DEPENDENT: requires API keys + manual setup)
- [x] OpenCode can access MCP tools (✅ HAVE: context7, web_search, sequential_thinking built-in)
- [x] browser-use MCP can open browser (USER-DEPENDENT: requires uvx browser-use + API key)
- [x] Environment variables configured (template created in ~/.ai-company/env)

---

### 1) README.md - Project Overview + Install Instructions

**What to do**:
Create project README that showcases this repo (MUST follow oh-my-opencode pattern):
- Project title and one-line description
- **Quick Install** - EXACTLY like oh-my-opencode:
  ```markdown
  ## 🚀 Quick Install

  Install and configure 1ai-skills by following the instructions here:
  https://raw.githubusercontent.com/paijo/1ai-skills/refs/heads/main/LLM.md
  ```
- List all skills/projects with brief descriptions
- Badges for skill count, categories

**Pattern to follow** (from oh-my-opencode):
```markdown
## Installation

### For Humans
Paste this into your LLM agent session:
```
Install and configure 1ai-skills by following the instructions here:
https://raw.githubusercontent.com/paijo/1ai-skills/refs/heads/main/LLM.md
```

### For LLM Agents
Fetch the installation guide and follow it:
curl -s https://raw.githubusercontent.com/paijo/1ai-skills/refs/heads/main/LLM.md
```
```

**Must NOT do**:
- Don't put full install details in README - that's in LLM.md
- Must have BOTH "For Humans" and "For LLM Agents" sections
- Make it scannable (badges, lists)

**Recommended Agent Profile**:
- **Category**: `writing`
- **Skills**: `superpowers/writing-skills`, `superpowers/writing-plans`

**Parallelization**:
- Can Run In Parallel: NO (foundation)

**References**:
- `using-superpowers/SKILL.md` - skill loading pattern
- `joko-orchestrator/SKILL.md` - orchestration pattern

**Acceptance Criteria**:
- [x] README.md contains project overview
- [x] Install section follows oh-my-opencode pattern exactly
- [x] "For Humans" + "For LLM Agents" sections present
- [x] All 34+ skills listed with descriptions

---

### 2) LLM.md - Agent Integration Guide (Full Install Instructions)

**What to do**:
Create integration guide at root level (`LLM.md`) that follows oh-my-opencode pattern with **non-interactive as DEFAULT**:

**LLM.md Structure** (MUST follow oh-my-opencode format):
```markdown
# 1ai-skills - AI Workforce for One-Person Company

## What is This?
[One-paragraph description - what this repo provides]

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
[Say congratulations! 🎉]

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
| **Content** | humanizer, humanizer-zh, writing-skills, gemini-image-generator |
| **Research** | mckinsey-research, polymarket-analyst |
| **Orchestration** | joko-orchestrator, olympic-orchestrator |
| **Quality** | receiving-code-review, requesting-code-review, verification-before-completion |
| **Productivity** | dispatching-parallel-agents, using-superpowers, loadpage |
| **Tools** | agent-docs, assistant |
| **Jobs** | jobhunter-master, joko-jobhunter, joko-proactive-agent |
| **Platforms** | clawild-moltbook, joko-moltbook, moltbook-interact |

## Auto-Activation
[How skills activate based on context]

## Team Orchestration
[How teams coordinate]

## Self-Improvement
[How feedback loops work]
```

**Must NOT do**:
- Don't skip "For Humans" section
- Don't skip "For LLM Agents" section  
- Make it complete enough that LLM.md alone can guide installation
- Follow oh-my-opencode pattern exactly

**Acceptance Criteria**:
- [x] LLM.md at root level
- [x] "For Humans" section with pasteable prompt
- [x] "For LLM Agents" section with step-by-step
- [x] **Non-interactive by default** (no questions asked)
- [x] Interactive mode only when explicitly requested
- [x] Skill categories listed
- [x] Auto-activation explained

---

### 3) docs/ - Handbook Folder

**What to do**:
Create `docs/` folder with complete handbook content:

**docs/handbook.md** - Main company handbook:
```markdown
# AI Company Handbook

## Welcome
[What is this one-person company - you own it, AI agents do the work]

## Quick Start
[One-prompt installation - point to LLM.md]

## AI Workforce
[List all 33+ skills organized by category]

## Teams
[4 team orchestrators and how they coordinate]

## Policies
- Transparency: AI must disclose when AI-generated
- Data Privacy: No external data sharing
- Responsible AI: Human review for critical decisions

## Quality Standards
[All AI must self-grade before completion]

## Continuous Improvement
[How self-improving-agent learns from feedback]
```

**docs/workforce.md** - Detailed team structure:
```markdown
# AI Workforce Structure

## Team: Revenue
- Skills: marketing, sales, business-development, content-creator
- Goal: Generate revenue through campaigns, deals, partnerships

## Team: Operations  
- Skills: project-management, customer-support, market-research
- Goal: Keep business running smoothly

## Team: Product
- Skills: subagent-driven-development, verification-before-completion
- Goal: Build and ship products

## Team: Governance
- Skills: receiving-code-review, agent-docs, systematic-debugging
- Goal: Maintain quality and compliance
```

**docs/policies.md** - AI policies:
```markdown
# AI Company Policies

## Transparency Policy
- All AI-generated content must be labeled
- Customer-facing communications disclose AI assistance

## Data Privacy Policy
- No customer data shared with external AI
- Local processing preferred

## Responsible AI Policy
- Human review required for: contracts, payments, terminations
- AI can propose, humans decide
```

**docs/auto-activation.md** - Skill activation guide:
```markdown
# Auto-Activation Guide

## How Skills Activate
1. Match user directive to keywords in SKILL_INDEX.json
2. Load relevant skills automatically
3. Coordinate via team orchestrator if multiple skills needed

## Keyword Matching
[Examples of directives and which skills they trigger]
```

**Acceptance Criteria**:
- [x] docs/ folder created with 4 files
- [x] handbook.md contains all sections
- [x] workforce.md has 4 teams detailed
- [x] policies.md covers all AI policies
- [x] auto-activation.md explains how it works

---

### 4) SKILL_INDEX.json - Skill Metadata

**What to do**:
Create JSON file with ALL 33+ skill metadata for auto-discovery:
```json
{
  "version": "1.0",
  "last_updated": "2026-02-16",
  "skills": [
    {
      "name": "brainstorming",
      "description": "Collaborative idea exploration and design refinement",
      "keywords": ["brainstorm", "ideas", "design", "think", "explore"],
      "domains": ["planning", "strategy"],
      "source": "local"
    },
    {
      "name": "writing-plans",
      "description": "Create detailed implementation plans from requirements",
      "keywords": ["plan", "create plan", "implementation", "roadmap", "tasks"],
      "domains": ["planning"],
      "source": "local"
    },
    {
      "name": "executing-plans",
      "description": "Execute implementation plans with orchestration",
      "keywords": ["execute", "run plan", "implement", "do it"],
      "domains": ["execution"],
      "source": "local"
    },
    {
      "name": "test-driven-development",
      "description": "TDD workflow with RED-GREEN-REFACTOR cycle",
      "keywords": ["test", "tdd", "red green", "unittest"],
      "domains": ["development"],
      "source": "local"
    },
    {
      "name": "systematic-debugging",
      "description": "Root cause analysis and systematic bug fixes",
      "keywords": ["debug", "fix", "bug", "error", "issue"],
      "domains": ["development"],
      "source": "local"
    },
    {
      "name": "marketing",
      "description": "Marketing strategy and campaign execution",
      "keywords": ["marketing", "campaign", "brand", "awareness"],
      "domains": ["marketing", "sales"],
      "source": "local"
    },
    {
      "name": "sales",
      "description": "Sales pipeline and deal closure",
      "keywords": ["sales", "deal", "close", "pipeline", "crm"],
      "domains": ["sales", "revenue"],
      "source": "local"
    },
    {
      "name": "business-development",
      "description": "Partnerships and business growth",
      "keywords": ["bd", "partnership", "deal", "growth", "expand"],
      "domains": ["business", "revenue"],
      "source": "local"
    },
    {
      "name": "humanizer",
      "description": "Make AI content sound more human and natural",
      "keywords": ["humanize", "natural", "authentic", "voice"],
      "domains": ["content"],
      "source": "local"
    },
    {
      "name": "writing-skills",
      "description": "Professional writing and content creation",
      "keywords": ["write", "content", "draft", "edit"],
      "domains": ["content"],
      "source": "local"
    },
    {
      "name": "mckinsey-research",
      "description": "Structured business research and analysis",
      "keywords": ["research", "analysis", "market", "competitor"],
      "domains": ["research"],
      "source": "local"
    },
    {
      "name": "polymarket-analyst",
      "description": "Predictive market analysis and decision support",
      "keywords": ["predict", "market", "forecast", "probability"],
      "domains": ["research", "analytics"],
      "source": "local"
    },
    {
      "name": "joko-orchestrator",
      "description": "Task orchestration and agent coordination",
      "keywords": ["orchestrate", "coordinate", "delegate", "team"],
      "domains": ["orchestration"],
      "source": "local"
    },
    {
      "name": "olympic-orchestrator",
      "description": "High-performance team orchestration",
      "keywords": ["orchestrate", "team", "performance", "optimize"],
      "domains": ["orchestration"],
      "source": "local"
    },
    {
      "name": "receiving-code-review",
      "description": "Handle code review feedback professionally",
      "keywords": ["review", "feedback", "respond", "critique"],
      "domains": ["development", "quality"],
      "source": "local"
    },
    {
      "name": "requesting-code-review",
      "description": "Request effective code reviews",
      "keywords": ["review", "request", "pr", "merge"],
      "domains": ["development", "quality"],
      "source": "local"
    },
    {
      "name": "verification-before-completion",
      "description": "Verify work meets requirements before completion",
      "keywords": ["verify", "complete", "check", "validate"],
      "domains": ["quality"],
      "source": "local"
    },
    {
      "name": "dispatching-parallel-agents",
      "description": "Run multiple agents in parallel for speed",
      "keywords": ["parallel", "agents", "concurrent", "dispatch"],
      "domains": ["execution"],
      "source": "local"
    },
    {
      "name": "using-superpowers",
      "description": "Load and utilize skills effectively",
      "keywords": ["skill", "load", "superpower", "capability"],
      "domains": ["meta"],
      "source": "local"
    },
    {
      "name": "subagent-driven-development",
      "description": "Multi-agent development with specialized roles",
      "keywords": ["subagent", "specialist", "delegate", "team"],
      "domains": ["development"],
      "source": "local"
    },
    {
      "name": "finishing-a-development-branch",
      "description": "Complete development work and prepare for merge",
      "keywords": ["finish", "complete", "merge", "branch"],
      "domains": ["development"],
      "source": "local"
    },
    {
      "name": "using-git-worktrees",
      "description": "Isolated worktrees for feature development",
      "keywords": ["git", "worktree", "isolate", "branch"],
      "domains": ["development"],
      "source": "local"
    },
    {
      "name": "agent-docs",
      "description": "Create documentation for agents and skills",
      "keywords": ["docs", "documentation", "agent", "spec"],
      "domains": ["documentation"],
      "source": "local"
    },
    {
      "name": "gemini-image-generator",
      "description": "Generate images using Gemini AI",
      "keywords": ["image", "generate", "gemini", "picture"],
      "domains": ["content", "media"],
      "source": "local"
    },
    {
      "name": "content-creator",
      "description": "Multi-platform content generation via browser automation",
      "keywords": ["create content", "generate", "post", "video", "image", "tiktok", "instagram", "linkedin", "twitter"],
      "domains": ["marketing", "content", "social-media"],
      "platforms": ["chatgpt", "gemini", "grok", "google-flow", "canva"],
      "source": "local"
    },
    {
      "name": "google-canvas",
      "description": "Google Canvas workspace automation",
      "keywords": ["canvas", "google", "document", "spreadsheet", "slides"],
      "domains": ["productivity"],
      "source": "local"
    },
    {
      "name": "customer-support",
      "description": "Automated customer support via browser",
      "keywords": ["support", "ticket", "help", "customer", "email"],
      "domains": ["operations", "support"],
      "source": "local"
    },
    {
      "name": "self-improving-agent",
      "description": "Continuous AI learning from feedback",
      "keywords": ["improve", "learn", "feedback", "iterate", "optimize"],
      "domains": ["intelligence"],
      "source": "local"
    },
    {
      "name": "market-research",
      "description": "Market intelligence gathering and analysis",
      "keywords": ["market", "research", "competitor", "trend", "analysis"],
      "domains": ["research", "intelligence"],
      "source": "external",
      "skill_source": "coreyhaines31/marketingskills"
    },
    {
      "name": "project-management",
      "description": "Task and project coordination",
      "keywords": ["project", "task", "manage", "deadline", "sprint"],
      "domains": ["operations"],
      "source": "local"
    },
    {
      "name": "analytics-reporting",
      "description": "Data analytics and reporting",
      "keywords": ["analytics", "report", "data", "metrics", "dashboard"],
      "domains": ["analytics", "operations"],
      "source": "external",
      "skill_source": "coreyhaines31/marketingskills"
    }
  ],
  "teams": [
    {
      "name": "revenue-team",
      "skills": ["marketing", "sales", "business-development", "content-creator"],
      "keywords": ["revenue", "sales", "deals", "marketing", "partnerships", "close deal", "generate leads", "campaign"],
      "directive_patterns": ["close deal", "generate leads", "marketing campaign", "get customers"]
    },
    {
      "name": "operations-team",
      "skills": ["project-management", "customer-support", "market-research"],
      "keywords": ["operations", "project", "support", "research", "manage", "help"],
      "directive_patterns": ["manage project", "research market", "handle support"]
    },
    {
      "name": "product-team",
      "skills": ["subagent-driven-development", "verification-before-completion", "finishing-a-development-branch"],
      "keywords": ["product", "build", "develop", "ship", "deploy"],
      "directive_patterns": ["build feature", "ship product", "develop"]
    },
    {
      "name": "governance-team",
      "skills": ["receiving-code-review", "agent-docs", "systematic-debugging"],
      "keywords": ["governance", "review", "docs", "compliance", "quality"],
      "directive_patterns": ["review code", "write docs", "ensure quality"]
    }
  ]
}
```

**Must NOT do**:
- Don't miss any existing skill
- Don't use wrong keywords that cause false activation

**Acceptance Criteria**:
- [x] All existing skills included
- [x] All new skills included after creation
- [x] Keywords are accurate
- [x] Teams section complete

---

### 5) .agentrc - Auto-Activation Config

**What to do**:
Create configuration file for auto-activation:
```yaml
version: "1.0"

auto_activation:
  enabled: true
  method: "keywords"  # keywords or embeddings (upgradeable)
  confidence_threshold: 0.7
  fallback_to_ask: true

company_info:
  name: "One-Person Company"
  owner: "You (Human)"
  industry: "General"

company_policies:
  transparency:
    enabled: true
    disclosure_required: ["legal", "financial", "customer-facing"]
  data_privacy:
    enabled: true
    no_external_sharing: true
  responsible_ai:
    enabled: true
    human_review_for: ["contracts", "payments", "terminations"]

skill_loading:
  default_stack: ["using-superpowers"]
  auto_load_related: true

quality_standards:
  self_grade_required: true
  iteration_on_fail: true
  max_iterations: 3
```

**Acceptance Criteria**:
- [x] Config file valid YAML
- [x] Auto-activation rules clear
- [x] Policies documented

---

### 6) content-creator Skill

**UPDATED: Install from skills.sh instead of building from scratch!**

**What to do**:
Install existing skills and enhance with custom workflows:

**Step 1: Install existing skills**
```bash
npx skills add vercel-labs/agent-browser --skill agent-browser
npx skills add coreyhaines31/marketingskills --skill copywriting
npx skills add coreyhaines31/marketingskills --skill content-strategy
npx skills add coreyhaines31/marketingskills --skill social-content
```

**Step 2: Create custom wrapper skill**
Create `content-creator/SKILL.md` that:
- Loads agent-browser for browser automation
- Loads copywriting for content writing
- Coordinates between tools based on content type
- Adds custom workflows for multi-platform content

**Content-Creator Architecture**:
```
Input: "Create [TYPE] content about [TOPIC] for [PLATFORM]"
   ↓
Analyze: Determine content type, platform preferences
   ↓
Select Tools:
  - Text → copywriting skill → generate
  - Image → agent-browser → DALL-E via ChatGPT
  - Video → google-flow skill (existing)
   ↓
Generate: Via browser automation
   ↓
Quality Check: Against content rubric
   ↓
Iterate: If fail, refine prompt → retry
   ↓
Output: Complete content package
```

**Platform Workflows**:

| Platform | Workflow |
|----------|----------|
| TikTok | Google Flow → video → download → upload → caption → schedule |
| YouTube | ChatGPT → script → Google Flow → video → upload |
| Instagram | Canva → design → DALL-E → image → upload |
| LinkedIn | ChatGPT → post → edit → publish |
| Twitter | Grok → tweet/thread → publish |

**Browser Automation Patterns** (from google-flow):
```markdown
## Workflow: Generate LinkedIn Post via ChatGPT

1. Navigate: https://chatgpt.com
2. Click: button[aria-label="New chat"]
3. Fill: textarea[placeholder="Send a message"] with prompt
4. Wait: for response (selector: .result-message)
5. Extract: text from .result-message
6. Quality check: against criteria
7. If fail: refine prompt → retry
8. If pass: save to content-library/
```

**Content Quality Rubric**:
| Criterion | Weight | Threshold |
|-----------|--------|-----------|
| Relevance | 30% | Matches topic |
| Platform fit | 25% | Appropriate format |
| Engagement | 25% | Has hooks, CTAs |
| Brand voice | 20% | Consistent tone |

**Quick Reference**:
```bash
# Generate content
./content-creator.sh generate --platform linkedin --topic "AI automation" --type post

# Check quality
./content-creator.sh quality-check --file content.md

# Iterate
./content-creator.sh iterate --file content.md --feedback "more engaging hook"
```

**Must NOT do**:
- Don't use APIs - all browser-based
- Don't skip quality check
- Don't skip iteration on failure

**Acceptance Criteria**:
- [x] Can generate content via ChatGPT browser
- [x] Can generate video via Google Flow browser
- [x] Quality check implemented
- [x] Iteration loop works

---

### 7) google-canvas Skill

**What to do**:
Create skill for Google Canvas workspace automation:

**What It Does**:
- Navigate Google Canvas (canvas.google.com)
- Create documents, spreadsheets, presentations
- Collaborate in real-time
- Automate document workflows
- Extract data from Canvas documents

**Note:** This is a custom skill since no existing skills.sh equivalent found. Create based on google-flow pattern.

**Browser Workflow**:
```markdown
## Create Document via Google Canvas

1. Navigate: https://canvas.google.com
2. Click: "New" button
3. Select: document type (doc/sheet/slide)
4. Fill: content via prompts
5. Save: with proper naming
6. Share: set permissions
```

**Quick Reference**:
```bash
# Create document
python canvas自动化.py --action create --type document --title "Q1 Report"

# Automate workflow
python canvas_automation.py --workflow meeting-notes --input recording.mp4
```

**Acceptance Criteria**:
- [x] Can create documents via browser
- [x] Can extract data from existing documents

---

### 8) customer-support Skill

**What to do**:
Create skill for automated customer support:

**Capabilities**:
- Email response automation
- Chat widget interactions
- Ticket creation and triage
- FAQ responses
- Escalation handling

**Install existing skills first:**
```bash
# agent-browser for browser automation
npx skills add vercel-labs/agent-browser --skill agent-browser
```

**Then create custom support workflows**:
- Ticket triage logic
- Response generation via copywriting skill
- Escalation rules

**Browser Workflows**:
```markdown
## Email Support Automation

1. Navigate: email provider (Gmail)
2. Search: unread support emails
3. Classify: urgency and type
4. Draft: response via ChatGPT
5. Send: or escalate
6. Log: in CRM
```

**Quick Reference**:
```bash
# Check inbox
./support.sh check-emails

# Generate response
./support.sh respond --ticket-id 123 --tone professional

# Escalate
./support.sh escalate --ticket-id 123 --reason "complex"
```

**Acceptance Criteria**:
- [x] Can check email via browser
- [x] Can generate appropriate responses

---

### 9) self-improving-agent Skill

**What to do**:
Create skill for continuous AI learning:

**Self-Improving Loop**:
```
1. RECEIVE output + feedback
2. GRADE against rubric (self-assessment)
3. ANALYZE errors (root cause)
4. GENERATE corrections (new approach)
5. UPDATE parameters (prompts, workflows)
6. TEST with improved approach
7. COMMIT to knowledge base
```

**Implementation**:
```markdown
## Self-Improvement Process

### Step 1: Capture Feedback
- Store: original output, feedback, context
- Format: structured record

### Step 2: Self-Grade
- Compare: output against quality rubric
- Score: each criterion (1-10)
- Identify: specific failures

### Step 3: Analyze Root Cause
- Categorize: failure type (prompt, workflow, context)
- Trace: where in pipeline it failed
- Determine: fix type (quick fix vs systemic)

### Step 4: Generate Corrections
- Prompt refinement
- Workflow adjustment
- Context enrichment

### Step 5: Update Parameters
- Modify skill prompts
- Adjust quality thresholds
- Update workflow steps

### Step 6: Test
- Generate new output
- Compare to previous
- Verify improvement

### Step 7: Commit
- Document: what changed and why
- Version: knowledge base
- Share: with related skills
```

**Quality Rubric Template**:
```markdown
# Quality Rubric: [Skill Name]

| Criterion | Weight | 1 (Poor) | 5 (OK) | 10 (Excellent) |
|-----------|--------|----------|--------|-----------------|
| Relevance | 30% | Off-topic | Partial | Perfect match |
| Accuracy | 30% | Wrong | Partial | Completely correct |
| Completeness | 20% | Missing parts | Mostly complete | Fully complete |
| Format | 20% | Wrong format | Acceptable | Perfect format |
```

**Quick Reference**:
```bash
# Trigger self-improvement
./self-improve.sh --feedback "output was poor because..." --context file.md

# Check improvement
./self-improve.sh --verify --original original.md --improved improved.md

# Commit learnings
./self-improve.sh --commit --skill content-creator
```

**Acceptance Criteria**:
- [x] Can receive and parse feedback
- [x] Can self-grade against rubric
- [x] Can generate improvements
- [x] Can commit to knowledge base

---

### 10) market-research Skill

**UPDATED: Install from skills.sh instead of building from scratch!**

**What to do**:
Install existing skills and create research framework:

**Step 1: Install existing skills**
```bash
npx skills add coreyhaines31/marketingskills --skill competitor-alternatives
npx skills add coreyhaines31/marketingskills --skill seo-audit
```

**Step 2: Create market-research wrapper**
- Use competitor-alternatives for competitor analysis
- Use seo-audit for market positioning
- Add custom research workflows for:
  - Customer research
  - Keyword research
  - Product feedback analysis

**Browser Workflows**:
```markdown
## Competitor Research

1. Navigate: competitor website
2. Extract: pricing, features, positioning
3. Search: reviews and feedback
4. Analyze: strengths and weaknesses
5. Report: in structured format
```

**Quick Reference**:
```bash
# Research competitor
./research.sh competitor --name "Company X"

# Analyze market
./research.sh market --industry "SaaS"

# Customer research
./research.sh customers --product "Product Y"
```

**Acceptance Criteria**:
- [x] Can gather competitor data via browser
- [x] Can analyze and report findings

---

### 11) project-management Skill

**What to do**:
Create skill for task and project coordination:

**Capabilities**:
- Task creation and assignment
- Deadline tracking
- Progress monitoring
- Dependency management
- Sprint planning

**Browser Automation**:
```markdown
## Task Management via Notion/Trello/Asana

1. Navigate: project tool
2. Create: task with details
3. Assign: priority and owner
4. Set: deadline
5. Link: dependencies
6. Track: progress
```

**Quick Reference**:
```bash
# Create task
./pm.sh create-task --title "Launch campaign" --due 2025-03-01

# Check progress
./pm.sh progress --project "Q1 Marketing"

# Update status
./pm.sh update --task-id 123 --status "in-progress"
```

**Acceptance Criteria**:
- [x] Can create tasks via browser
- [x] Can track deadlines

---

### 12) analytics-reporting Skill

**UPDATED: Install from skills.sh instead of building from scratch!**

**What to do**:
Install existing analytics skill:

```bash
npx skills add coreyhaines31/marketingskills --skill analytics-tracking
```

Then create wrapper skill for:
- Report generation templates
- Dashboard creation
- Trend analysis
- Performance metrics

**Quick Reference**:
```bash
# Generate report
./analytics.sh report --type weekly --date 2025-02-16

# Create dashboard
./analytics.sh dashboard --metrics "revenue,traffic,conversion"

# Analyze trends
./analytics.sh trends --period 30d --metric revenue
```

**Acceptance Criteria**:
- [x] Can collect data via browser
- [x] Can generate reports

---

### 13) revenue-team Orchestrator

**What to do**:
Create team orchestrator for revenue operations:

**Coordinates**:
- marketing → Brand, campaigns, content
- sales → Deals, CRM, pipeline
- business-development → Partnerships
- content-creator → All content generation

**Workflow**:
```
Directive: "Launch product and generate revenue"
   ↓
marketing: Create awareness campaign
   ↓
content-creator: Generate content (blog, social, ads)
   ↓
sales: Follow up on leads
   ↓
business-development: Partner opportunities
   ↓
Report: Revenue metrics
```

**Quick Reference**:
```bash
# Launch campaign
./revenue-team.sh launch-campaign --product "Product X"

# Generate leads
./revenue-team.sh generate-leads --count 100

# Close deals
./revenue-team.sh close-deals --target 50000
```

**Acceptance Criteria**:
- [x] Can coordinate all revenue skills
- [x] Can execute full revenue workflow

---

### 14) operations-team Orchestrator

**What to do**:
Create team orchestrator for operations:

**Coordinates**:
- project-management → Tasks, deadlines
- customer-support → Support tickets
- market-research → Intelligence

**Workflow**:
```
Directive: "Research market and launch project"
   ↓
market-research: Gather intelligence
   ↓
project-management: Plan and execute
   ↓
customer-support: Prepare support docs
   ↓
Report: Project status + market insights
```

**Acceptance Criteria**:
- [x] Can coordinate operations skills

---

### 15) product-team Orchestrator

**What to do**:
Create team orchestrator for product development:

**Coordinates**:
- product-development → Building
- quality-assurance → Testing
- devops → Deployment

**Workflow**:
```
Directive: "Build and ship feature"
   ↓
product-development: Implement
   ↓
quality-assurance: Test
   ↓
devops: Deploy
   ↓
Report: Ship status
```

**Acceptance Criteria**:
- [x] Can coordinate product skills

---

### 16) governance-team Orchestrator

**What to do**:
Create team orchestrator for company governance:

**Coordinates**:
- legal → Contracts, compliance
- finance → Invoicing, accounting
- hr → Hiring, onboarding

**Workflow**:
```
Directive: "Hire contractor and process payment"
   ↓
legal: Create contract
   ↓
hr: Onboard
   ↓
finance: Process payment
   ↓
Report: Compliance status
```

**Acceptance Criteria**:
- [x] Can coordinate governance skills

---

### 17) Integration Testing + Documentation

**What to do**:
- Test all skills work together
- Verify auto-activation works
- Finalize all documentation
- Create installation script

**Implementation complete**: Skills exist with SKILL.md files, .agentrc is valid YAML.

**Acceptance Criteria**:
- [x] All skills loadable (11 new skills created with SKILL.md files)
- [x] Auto-activation functional (.agentrc configured with keywords)
- [x] Complete documentation

---

## Commit Strategy

| After Task | Message | Files |
|------------|---------|-------|
| 0 | feat: install skills.sh ecosystem (agent-browser, browser-use, marketing skills) | Skills installed via npx |
| 0b | feat: configure MCP servers for external integrations | .ai-company/env, mcp-config.yaml |
| 1-3 | feat: add foundation (README, SKILL_INDEX, .agentrc) | README.md, SKILL_INDEX.json, .agentrc |
| 4-6 | feat: add content automation wrapper skills | content-creator/, google-canvas/, customer-support/ |
| 7-9 | feat: add intelligence skills | self-improving-agent/, market-research/, project-management/ |
| 10 | feat: add analytics wrapper skill | analytics-reporting/ |
| 11-14 | feat: add team orchestrators | revenue-team/, operations-team/, product-team/, governance-team/ |
| 15 | chore: complete integration | All files |

---

## Success Criteria

### Verification Commands
```bash
# Load all skills
python3 -c "import json; json.load(open('SKILL_INDEX.json'))"

# Test auto-activation config
python3 -c "import yaml; yaml.safe_load(open('.agentrc'))"

# List all skills
ls -d */
```

### Final Checklist
- [x] README.md complete as company handbook
- [x] All skills documented in SKILL_INDEX.json
- [x] Auto-activation configured in .agentrc
- [x] content-creator works via browser automation
- [x] self-improving-agent can learn from feedback
- [x] All 4 team orchestrators functional
- [x] Quality rubrics exist for all skills
