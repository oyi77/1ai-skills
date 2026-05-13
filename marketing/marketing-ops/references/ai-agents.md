# AI Agent Orchestration Reference

Run AI as your marketing team, not just a tool. This is the architecture
for a solo founder to operate a full marketing department with AI agents.

---

## The 10-80-10 Model

```
YOU (10%)          →  AI AGENTS (80%)       →  YOU (10%)
Direction &           Research, draft,          Review, approve,
strategy              execute, optimize         publish, decide
```

You make the strategic decisions. AI handles execution. You review output quality.
Never let AI publish without human review. Never spend your time on tasks AI can do.

---

## Core Agent Architecture

### The 5 Essential Marketing Agents

**Agent 1: Content Engine**
```
Role: Research, outline, draft, optimize content
Inputs: Topic, keyword, persona, brand voice
Outputs: Blog posts, social posts, email copy, scripts
Context: brand-voice.md, persona.md, SEO keywords
Frequency: Daily
```

**Agent 2: Sales Development Rep (AI SDR)**
```
Role: Find leads, qualify, write outreach, follow up
Inputs: ICP definition, lead sources, CRM data
Outputs: Qualified lead list, personalized emails, follow-ups
Context: marketing-profile.yml, sales templates
Frequency: Daily
```

**Agent 3: Analytics Analyst**
```
Role: Pull metrics, identify trends, flag anomalies, report
Inputs: GA4 data, ad platform data, email metrics
Outputs: Weekly reports, alert summaries, optimization recs
Context: KPI targets, historical benchmarks
Frequency: Weekly + triggered alerts
```

**Agent 4: Social Manager**
```
Role: Create posts, schedule, engage, monitor mentions
Inputs: Content calendar, brand voice, trending topics
Outputs: Platform-specific posts, engagement responses
Context: brand-voice.md, platform specs, hashtag strategy
Frequency: Daily
```

**Agent 5: Campaign Orchestrator**
```
Role: Plan campaigns, coordinate other agents, track progress
Inputs: Business goals, budget, timeline
Outputs: Campaign plans, task assignments, status updates
Context: All foundation files + campaign history
Frequency: Per campaign + weekly check
```

---

## Context Engineering

### Why AI Output is Generic (And How to Fix It)

Generic AI output comes from generic context. The fix is structured context files
that every agent reads before producing anything.

**Essential context files:**
```
marketing-profile.yml    — WHO you are, WHAT you sell, WHO you sell to
brand-voice.md           — HOW you sound (personality, tone, vocabulary)
persona.md               — WHO your customer is (pains, goals, objections)
competitor-intel.md      — WHO you compete with (positioning, gaps)
performance-history.md   — WHAT has worked before (winning patterns)
```

### Context Engineering Rules
1. **Be specific, not general.** "Professional but warm" → "We use contractions.
   We never say 'leverage' or 'synergy.' We explain things like we're talking
   to a smart friend over coffee."
2. **Include examples.** On-brand vs off-brand writing samples teach better
   than rules.
3. **Update after every learning.** "Our audience responds to data-heavy posts"
   → add to brand-voice.md immediately.
4. **Every agent reads foundation files first.** No exceptions.

---

## Agent Workflow Patterns

### Pattern 1: Sequential Chain
```
Research Agent → Content Agent → Review → Publish
  (find topic)     (write draft)   (you)    (schedule)
```

### Pattern 2: Parallel Fan-Out
```
Campaign Plan → ┬→ Content Agent (blog post)
                ├→ Email Agent (sequence)
                ├→ Social Agent (posts)
                └→ Ad Agent (creative)
                   ↓
                You review all → Approve → Launch
```

### Pattern 3: Feedback Loop
```
Publish → Monitor → Analyze → Learn → Improve → Publish
         (auto)    (weekly)   (update   (better
                              context)  output)
```

---

## Human-in-the-Loop Decision Points

**Always review before:**
- Publishing any content to your audience
- Sending any email to customers/prospects
- Launching any paid ad (spending money)
- Responding to customer complaints or sensitive topics
- Making pricing or positioning changes

**Safe to automate fully:**
- Internal content drafts and outlines
- Data collection and report generation
- Social media scheduling (after approving content)
- UTM link generation
- Content calendar structure

---

## Solo Founder Weekly AI Marketing Routine

```
MONDAY (1 hour)
  □ Review last week's metrics (AI generates report)
  □ Set 3 priorities for the week
  □ Brief AI on this week's content topics

TUESDAY-THURSDAY (30 min/day)
  □ Review AI-generated content drafts
  □ Approve and schedule social posts
  □ Review any sales outreach drafts
  □ Respond to high-priority leads/customers

FRIDAY (30 min)
  □ Review AI's weekly performance summary
  □ Update context files with learnings
  □ Plan next week's themes
  □ Approve next week's content calendar

TOTAL: ~4 hours/week on marketing
(vs 20-40 hours without AI agents)
```
