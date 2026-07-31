---
name: project-management
description: Coordinate sprints, track deadlines, manage tasks, and maintain project documentation with Notion and Slack. Use when working with project management.
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- business-ops
- management
- notion
- operations
- project
- slack
version: 1.1.0
---
# Project Management

## When to Use

**Trigger phrases:**
- "project management"
- "Help me with project management"
- "sprint planning"
- "deadline tracking"
- "task management"

**Use cases:**
- Running sprint-based or Kanban-style development cycles
- Tracking cross-functional deliverables with hard deadlines
- Building and maintaining project documentation (SOPs, runbooks, meeting notes)
- Coordinating async teams across time zones
- Onboarding new team members with structured task lists and process docs

**When NOT to use:**
- For processes that change daily (too much overhead)
- When the team is too small to benefit from SOPs
- For one-time events that will not repeat
- When ad-hoc communication replaces all formal tracking


## Overview

Project Management is the discipline of initiating, planning, executing, monitoring, and closing work to achieve specific goals within defined constraints (scope, time, budget). This skill covers the operational backbone — sprint cadence, task tracking, documentation hygiene, stakeholder communication, and continuous improvement — using lightweight tools (Notion, Slack) rather than heavyweight enterprise suites.

The core philosophy: **process serves the team, not the other way around.** Every artifact (backlog, sprint board, SOP, retrospective notes) exists to reduce cognitive load and increase predictability, not to generate busywork.

Key concepts:
- **Sprint-based cadence** — fixed timeboxes (1-2 weeks) with a definition of done
- **Kanban pull** — continuous flow with WIP limits for support/operations work
- **Scrum ceremonies** — planning, daily sync, review, retrospective (tailored to team size)
- **Documentation as a habit** — SOPs, decision logs, and meeting notes kept current as part of the workflow, not an afterthought


## Workflow — Sprint Cadence

This workflow describes a standard 2-week sprint cycle for a small-to-mid-size team (3-12 people). Adjust timeboxes to fit your context.

### Phase 1: Sprint Planning (Day 1, 60-90 min)

1. **Load the backlog** — Pull highest-priority items from the prioritized backlog. Each item should have a clear description, acceptance criteria, and a complexity estimate (t-shirt sizes: S/M/L/XL).
2. **Set sprint goal** — One sentence that captures what the team commits to delivering. The goal should survive scope-tradeoff decisions during the sprint.
3. **Break down work** — Split large items (XL) into smaller deliverables that can finish within the sprint. Assign owners where possible.
4. **Capacity check** — Account for planned PTO, meetings, and support rotation. A sustainable velocity is 60-80% of theoretical capacity.
5. **Commit** — The team agrees on the sprint scope. Items added mid-sprint replace something of equal size (tradeoff, not stretch).

**Output:** Sprint board (To Do / In Progress / Review / Done) with a sprint-goal tag, assigned owners, and due dates.

### Phase 2: Daily Sync (15 min)

Each person answers three questions:
1. What did I complete yesterday?
2. What will I work on today?
3. Are there any blockers?

**Rules:**
- Blocker discussion is kept to awareness-only during the sync; deep-dives happen as a follow-up with the relevant parties
- The board is updated during or immediately after the sync
- Async teams may use a Slack thread or a shared doc instead of a live meeting

### Phase 3: Mid-Sprint Check (Day 5-6, 15-30 min)

1. **Burndown review** — Compare completed vs planned scope. Is the team on track?
2. **Scope adjustment** — If the team is significantly ahead or behind, adjust scope with stakeholder awareness
3. **Blocker sweep** — Proactively unblock items that are stalled

### Phase 4: Sprint Review (Day 10, 30-60 min)

1. **Demo completed work** — Show what shipped, not just status updates. Stakeholders attend.
2. **Collect feedback** — Capture input that affects the next sprint's backlog
3. **Update backlog priority** — Reorder based on new information from the demo

### Phase 5: Retrospective (Day 10, 45-60 min, immediately after Review)

1. **Gather data** — Each person writes 2-3 items in three columns: What Went Well / What Could Be Better / Ideas
2. **Cluster and vote** — Group related items; team votes on the top 1-2 areas to improve
3. **Action items** — Define one concrete change to try next sprint, with an owner
4. **Follow-up** — The action item is checked at the next retro; repeat or replace if it didn't stick

**Output:** A single retrospective document (Notion or shared doc) with the date, clustered feedback, and agreed action items.

### Continuous Practices (every day)

- **Backlog grooming** — Spend 15-30 min/week keeping the backlog prioritized and refined
- **Decision log** — Record non-obvious decisions with context, options considered, and rationale
- **Weekly digest** — A 3-bullet summary for stakeholders: what shipped, what's next, what's blocked


## Common Pitfalls

| Pitfall | Symptom | Prevention |
|---|---|---|
| Sprint goal too vague | Team finishes items but nothing coherent ships | Write the goal before picking items; every item must contribute to it |
| Overcommitment | Burndown flatlines at 50% by mid-sprint | Track historical velocity for 3-4 sprints before trusting any estimate |
| Retro without follow-through | Same complaints every sprint; action items never executed | Assign one owner and one deadline per action item; check at the next retro before adding new ones |
| Board drift | Board status does not match reality (items marked Done but not deployed) | Enforce a definition of done (coded, reviewed, tested, deployed, documented) before closing |
| Meeting bloat | Planning/review/retro each run 2x longer than planned | Use a timer; hard stop at the scheduled end even if not everything was covered |
| Zombie backlog | Hundreds of untouched items nobody will ever do | Archive items older than 3 months; split the active backlog (current sprint + next 2 sprints) from the icebox |
| Async time-zone friction | Decisions stall waiting for a reply that comes 12h later | Use written decision records with a "default consent" rule: if no objection within 24h, the proposal is accepted |
| Stakeholder surprise | Stakeholders learn about delays at the review instead of mid-sprint | Send a one-line status update when an item's risk crosses a threshold (not just at fixed checkpoints) |


## SOP Template

- **Purpose** — Why this process exists (trigger, expected outcome)
- **Scope** — Who and what it covers
- **Procedure** — Step-by-step instructions with decision points
- **Escalation** — When and how to escalate (criteria, contact, SLA)
- **Review** — Schedule for periodic updates (quarterly by default)


## Key Metrics

- **Sprint completion rate** — % of committed items delivered (target: 70-90%; >90% may mean undercommitting)
- **Cycle time** — Average days from "In Progress" to "Done" per item size
- **Error/rework rate** — Items re-opened or significantly reworked after closing
- **Stakeholder satisfaction** — Survey after each release or major milestone
- **Process overhead ratio** — Time spent in ceremonies vs. time spent on delivery


## Process

The project management process applies at three levels:

### Level 1: Daily Execution
1. **Start of day** — Review personal task list, update board, check for blockers
2. **During day** — Track time or effort per item (optional, useful for estimation calibration)
3. **End of day** — Close completed items, add notes, update next-day priorities

### Level 2: Sprint Cycle (detailed above in Workflow)
1. **Prepare** — Groom backlog, confirm stakeholder availability for review
2. **Execute** — Run the 5-phase sprint cycle (Planning → Daily Sync → Mid-Sprint → Review → Retro)
3. **Verify** — Compare actual velocity to plan, audit documentation completeness

### Level 3: Quarterly / Program Level
1. **Align** — Set quarterly objectives (OKRs or equivalent) that break into sprint-sized chunks
2. **Roadmap** — Maintain a 2-3 quarter forward-looking roadmap; update based on retrospective themes
3. **Review** — Assess whether the project management process itself needs adjustment


## Verification

Before closing a sprint or project, run through this checklist:

- [ ] All committed items are in Done with a definition of done met
- [ ] The board reflects the current reality (no stale In Progress items)
- [ ] Decision log is up to date with this sprint's key decisions
- [ ] Retrospective was held and at least one action item is assigned
- [ ] Documentation (SOPs, runbooks) was updated for any process changes this sprint
- [ ] Stakeholder digest was sent (at least a brief written summary)
- [ ] Backlog is groomed for the next sprint

For ongoing operations:
- [ ] Weekly status digest sent on schedule
- [ ] Board WIP limits are respected (no >3 items per person in In Progress)
- [ ] At least one backlog item has been groomed (refined or removed) this week
- [ ] Action items from the last retro are visible and being tracked


## Monetization

Project management skills generate revenue through delivery, not by being the deliverable. The pathways below assume you are either a solo operator, a fractional PM, or run a small agency.

### 1. Fractional / Contract Project Management
- Offer retainer-based PM services to 3-5 early-stage startups that cannot afford a full-time PM
- Scope: sprint setup (Notion + Slack), weekly sync facilitation, backlog grooming, stakeholder reporting
- Typical rate: $1,500-4,000/month per client for 5-10 hours/week

### 2. SOP & Process Documentation
- Many small businesses have no documented workflows; they operate on tribal knowledge
- Deliverable: a Notion or Google Doc SOP library covering their 10-20 most critical processes
- Rate: $2,000-6,000 per engagement (flat fee)

### 3. PM Tool Migration & Setup
- Companies migrating from spreadsheets to Notion, Linear, or Asana need someone to set up the templates, permissions, and integration (Slack, calendar, GitHub)
- Deliverable: configured workspace + team training session
- Rate: $500-2,500 per workspace

### 4. Retainer + Kickback Model (scalable)
- Set up a project management template marketplace (Notion templates, Linear starter kits)
- Offer a free tier to build an audience; sell premium templates ($19-97 each)
- Combine with a low-touch coaching call add-on ($200-500/month for monthly process audit)

### 5. Outcome-Backed Pricing (advanced)
- For clients where improved PM directly impacts revenue (e.g., agency delivery teams): price as a percentage of throughput improvement
- Example: if your PM process increases monthly deliverables from 8 to 12, take 10-20% of the incremental revenue for 6 months
- Requires baseline metrics and quarterly measurement


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "We do not need SOPs" | Without SOPs, quality depends on memory. Document everything. |
| "Manual processes work fine" | Manual processes do not scale and are error-prone. Automate. |
| "Compliance is optional" | Compliance protects you legally. Build it in from the start. |
| "Standups are a waste of time" | A 15-min standup saves hours of misalignment per week when done right. The failure mode is bad facilitation, not the ceremony itself. |
| "We will fix it in the next sprint" | Without a retro action item and an owner, "next sprint" never arrives. Make it concrete and assigned. |
| "Estimates are always wrong so why estimate" | Estimates are not predictions; they force conversation about scope, dependencies, and risk. The value is in the discussion, not the number. |


## When NOT to Use (expanded)

- For processes that change daily (too much overhead for formal sprint tracking)
- When the team is too small to benefit from SOPs (1-2 people may use lightweight checklists instead)
- For one-time events that will not repeat (a single event is a project, not a process)
- When ad-hoc communication already achieves reliable outcomes (do not add ceremony where none is needed)