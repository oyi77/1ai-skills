---
name: berkahkarya-orchestrator
description: "Orchestrate BerkahKarya multi-skill workflows by routing tasks to the right agents and coordinating cross-platform operations."
domain: core
---
# BerkahKarya Orchestrator

Master task router and workflow coordinator for the BerkahKarya AI workforce.

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Skill Directory (150+ skills across 13 divisions)
This section covers skill directory (150+ skills across 13 divisions) for the berkahkarya-orchestrator skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### 🤖 AUTOMATION (`automation/`)
| Skill | When to Use |
|-------|-------------|
| `telegram-userbot` | DM, voice note, ring call, monitor groups, outreach |
| `postbridge-social-manager` | Schedule posts to TikTok/IG/YouTube via PostBridge |
| `n8n` | Build automated workflows, webhooks, integrations |
| `workflow-builder` | Design multi-step automation flows |
| `job-hunter` | Autonomous job search and application |
| `voice-ai-agent` | Voice-based AI interactions |
| `content-publisher` | Publish to Substack, Medium |
| `joko-moltbook` | Moltbook post queue |
| `moltbook-interact` | Moltbook engagement |
| `clawild-moltbook` | Moltbook crypto intel |

### 🎬 CONTENT (`content/`)
| Skill | When to Use |
|-------|-------------|
| `content-generator` | TikTok 9:16 video, AI-generated content |
| `larry-playbook` | Viral TikTok slideshow (Larry's formula) |
| `content-kingdom` | Multi-platform content system |
| `content-planner-auto` | Content calendar, scheduling |
| `viral-research-engine` | Trending topics, viral hooks research |
| `seedance` | Seedance AI video generation |
| `grok-video-generation` | Grok/Aurora AI video |
| `gemini-image-generator` | Product images, posed photos |
| `humanizer` | Make AI text sound human (EN) |
| `humanizer-zh` | Make AI text sound human (ZH/ID) |
| `faceless-youtube` | Faceless YouTube channel automation |
| `ai-newsletter` | Newsletter creation |
| `ai-podcast` | Podcast production |
| `comment-reply-manager` | Auto-reply comments, DM funnel |
| `video-editor` | FFmpeg video editing |
| `writing-skills` | Writing best practices |

### ⚙️ CORE (`core/`)
| Skill | When to Use |
|-------|-------------|
| `berkahkarya-orchestrator` | THIS skill — master routing |
| `joko-orchestrator` | Multi-skill coordination |
| `joko-proactive-agent` | Proactive monitoring, heartbeat |
| `memory-system` | Persistent memory, semantic search |
| `self-improving-agent` | Learn from feedback, improve |
| `runtime-self-improvement` | Real-time skill improvement |
| `find-skills` | Discover new skills from ClawHub |
| `agent-docs` | Write AI-optimized documentation |
| _(rag-system removed)_ | Retrieval-augmented generation |
| `vilona` | Vilona persona activation |

### 💻 DEVELOPMENT (`development/`)
| Skill | When to Use |
|-------|-------------|
| `brainstorming` | Before building anything — explore first |
| `writing-plans` | Create implementation plans |
| `executing-plans` | Execute approved plans |
| `code-reviewer` | Review code quality |
| `requesting-code-review` | Request review before merging |
| `test-driven-development` | TDD workflow |
| `systematic-debugging` | Debug complex issues |
| `prd-generator` | Product requirement documents |
| `subagent-driven-development` | Multi-agent coding |

### 🔗 INTEGRATIONS (`integrations/`)
| Skill | When to Use |
|-------|-------------|
| `oh-my-opencode` | Advanced coding with specialized agents |
| `cloud-mcp` | Cloud service MCP servers |
| `database-mcp` | Database MCP servers |
| `communication-mcp` | Slack, email MCP |

### 📣 MARKETING (`marketing/`)
| Skill | When to Use |
|-------|-------------|
| `ads-manager` | Research ads, clone competitor ads |
| `affiliate-marketing` | Affiliate program management |
| `ai-digital-products` | Digital product strategy |
| `buzzer-engagement-army` | Engagement automation army |
| `content-analytics-engine` | Analytics, A/B testing, ROI |
| `social-media-engagement` | Auto-like, comment, follow |
| `social-media-upload` | Upload to social platforms |
| `twitter-automation` | X/Twitter automation |
| `seo-optimizer` | SEO strategy and optimization |
| `email-marketing` | Email campaigns, drip sequences |
| `stripe-revenue-bot` | Stripe payment automation |
| `market-research` | Market intelligence |
| `analytics-dashboard` | Performance tracking |
| `build-in-public` | Build in public strategy |

### 🏢 OPERATIONS (`operations/`)
| Skill | When to Use |
|-------|-------------|
| `project-management` | Sprint planning, task tracking |
| `product-team` | PRDs, roadmap, release |
| `operations-team` | SOPs, on-call, SLA |
| `revenue-team` | Sales pipeline, forecasting |
| `payment-invoicing` | TriPay, LYNK, Midtrans |
| `multi-channel-reminder` | Task reminders via DM/call |
| `clickup` | ClickUp integration |
| `jira` | Jira integration |

### 📋 PRODUCTIVITY (`productivity/`)
| Skill | When to Use |
|-------|-------------|
| `calendar-management` | Google Calendar, scheduling |
| `email-automation` | Gmail automation |
| `google-workspace` | Docs, Sheets, Drive |
| `notion` | Notion database |
| `google-canvas` | Google Canvas documents |

### 🔬 RESEARCH (`research/`)
| Skill | When to Use |
|-------|-------------|
| `mckinsey-research` | Market analysis, TAM, strategy |
| `ai-research-agent` | Deep research automation |
| `polymarket-analyst` | Prediction markets, EV |
| `trendradar` | Trend monitoring |
| `kalodata/*` | TikTok analytics (7 sub-skills) |
| `dispatching-parallel-agents` | Parallel multi-agent research |

### 💼 SALES (`sales/`)
| Skill | When to Use |
|-------|-------------|
| `business-development` | Lead gen, prospect research |
| `sales-strategy` | CRM, pipeline, outreach |
| `customer-support` | Support automation |
| `ai-lead-generation` | AI-powered lead finding |
| `ai-marketplace` | Digital marketplace strategy |

### 📈 TRADING (`trading/`)
| Skill | When to Use |
|-------|-------------|
| `strategy/xauusd_asia_7c_breakout` | XAUUSD 7-candle Asia session |
| `EA/` | Expert Advisor automation |
| orchestrator | Trading team coordination |
| researcher | Market research for trading |
| strategist | Strategy development |
| executor | Trade execution |
| `team/risk_manager` | Risk management |

---

## Orchestration Patterns
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


### Pattern 1: Single Task → Direct Skill
```
"Generate TikTok video" → content/content-generator
"Ring Veris" → automation/telegram-userbot
"Research XAUUSD" → trading/team/researcher
```

### Pattern 2: Multi-Step Workflow
```
"Launch product campaign":
1. research/market-research → competitor analysis
2. marketing/content-creator → content plan
3. content/content-generator → create videos
4. marketing/social-media-upload → schedule posts
5. marketing/analytics-dashboard → monitor results
```

### Pattern 3: Parallel Execution (3+ independent tasks)
```
"Build full marketing funnel":
Spawn in parallel:
  - Agent A: content/viral-research-engine
  - Agent B: marketing/ads-manager  
  - Agent C: sales/business-development
  - Agent D: marketing/email-marketing
Merge results → core/joko-orchestrator
```

### Pattern 4: Alert Escalation
```
Task overdue →
  1. automation/telegram-userbot DM
  2. automation/telegram-userbot voice note (female/Vilona)
  3. automation/telegram-userbot ring (5x until answered)
```

---

## Management Alert System

```python
# When to escalate:
OVERDUE_30MIN → DM ke PIC
OVERDUE_1H    → DM + VN (Vilona female voice)
OVERDUE_2H    → Ring sampai diangkat (5 attempts)
CRITICAL      → Ring semua management sekaligus

# Management team:
Veris  → @alwayscuanbos (Ads Master)
Sony   → id=7963750650  (Ops Manager)  
Nuno   → @oens77        (Trading Master)
Paijo  → @codergaboets  (CEO)
```

## Decision Tree

```
User Request
    ↓
1. Is it a SINGLE skill task?
   YES → Use that skill directly
   NO  → Continue
    ↓
2. Does it span 2-3 skills?
   YES → Run sequentially, pass outputs forward
   NO  → Continue
    ↓
3. Does it span 3+ independent tasks?
   YES → Dispatch parallel agents (max 5 concurrent)
   NO  → Continue
    ↓
4. Is it a complex business workflow?
   YES → Break into phases, use core/joko-orchestrator
```

## Business Lines → Skill Clusters

| Business Line | Primary Skills |
|--------------|----------------|
| Talent Agency | sales/*, operations/project-management |
| Entertainment/Media | content/*, marketing/*, automation/telegram-userbot |
| Quant Fund | trading/*, research/polymarket-analyst |
| Software House | development/*, integrations/* |
| Affiliate Marketing | marketing/affiliate-marketing, automation/post-bridge, content/* |

## When to Use

- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
