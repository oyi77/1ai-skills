---
name: meeting-management
description: AI-powered meeting management — agenda creation, note-taking, action item extraction, follow-up tracking. Use when planning meetings, capturing decisions, or tracking meeting outcomes.
domain: productivity
tags: [meetings, notes, action-items, agenda, follow-up, collaboration]
---

## Overview

Structured meeting management system that helps plan agendas, capture notes in real-time, extract action items, and track follow-ups. Turns meetings from time sinks into productive decision-making sessions.

## When to Use

- Planning a meeting and need a structured agenda
- Capturing notes and decisions during a meeting
- Extracting action items from meeting transcripts
- Tracking follow-ups and accountability after meetings
- Preparing meeting summaries for absent team members

## Process
1. Validate input and check prerequisites
2. Initialize required connections and contexts
3. Execute core operation with monitoring
4. Validate output against expected format
5. Deliver results and log execution summary


### 1. Pre-Meeting: Agenda Creation

```
Meeting: [title]
Date: [date]
Duration: [time]
Attendees: [list]

Agenda:
1. [Topic] — [owner] — [time allocation]
2. [Topic] — [owner] — [time allocation]
3. [Topic] — [owner] — [time allocation]

Pre-read materials: [links]
Goal: [specific outcome]
```

### 2. During Meeting: Note-Taking Framework

Use the **ALIVE** framework:
- **A**ctions — Who does what by when
- **L**earnings — New information discovered
- **I**ssues — Problems raised (not yet resolved)
- **V**otes — Decisions made
- **E**scalations — Items needing higher approval

### 3. Post-Meeting: Action Item Extraction

```
Action Items from [meeting name] — [date]

| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | [task] | [name] | [date] | Pending |
| 2 | [task] | [name] | [date] | Pending |

Decisions Made:
- [decision 1] — rationale: [why]
- [decision 2] — rationale: [why]

Open Items (next meeting):
- [item 1]
- [item 2]
```

### 4. Follow-Up Tracking

- Send summary within 24 hours
- Track action items in project management tool
- Follow up on overdue items before next meeting
- Review open items at start of next meeting

## Meeting Types

| Type | Duration | Focus | Template |
|------|----------|-------|----------|
| Standup | 15 min | Blockers, progress | Yesterday/Today/Blockers |
| Planning | 60 min | Scope, priorities | Backlog refinement |
| Retrospective | 45 min | Improvements | Start/Stop/Continue |
| 1:1 | 30 min | Growth, feedback | Wins/Challenges/Goals |
| Brainstorm | 60 min | Ideas, solutions | How Might We + dot voting |

## Anti-Patterns

- No agenda = no meeting (decline or request agenda)
- Action items without owners = wishful thinking
- Meeting notes never sent = meeting never happened
- Recurring meetings without periodic review = calendar cancer

## Verification

- [ ] Every meeting has a written agenda
- [ ] Every meeting produces action items with owners and deadlines
- [ ] Summary sent within 24 hours
- [ ] Action items tracked to completion
- [ ] Recurring meetings reviewed quarterly for necessity

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows
