---
name: career-ops
description: AI-powered job search system — CV optimization, ATS scanning, interview prep, application tracking. Use when job searching, writing CVs, preparing for interviews, tracking applications,.
domain: productivity
tags: 
- [career
- job-search
- cv
- resume
- interview
- ats
- hiring
- job-tracker]
---

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Overview

Career Ops: a local AI-powered job search system for AI coding CLIs. 15 commands covering the full job search pipeline from evaluation through offer negotiation. Generates ATS-optimized CVs, scans job portals, tracks applications, and prepares interview responses.

Source: [santifer/career-ops](https://github.com/santifer/career-ops)

## Capabilities

- Evaluate job fit across 6 dimensions
- Generate ATS-optimized CVs tailored to specific roles
- Scan job portals for new opportunities
- Track applications through pipeline stages
- Prepare STAR+R interview responses
- Run full application pipelines end-to-end

## When to Use

**Trigger phrases:**
- "career ops"
- "Starting a job search and need strategy"
- "Optimizing CV for ATS systems"
- "Preparing for behavioral or technical interviews"


- Starting a job search and need strategy
- Optimizing CV for ATS systems
- Preparing for behavioral or technical interviews
- Tracking multiple job applications
- Researching compensation for a role
- Scanning for new job postings

## Commands

| Command | Purpose |
|---------|---------|
| `evaluate` | Assess fit for a specific role across 6 dimensions |
| `scan` | Scan job portals for new opportunities |
| `pdf` | Generate ATS-optimized CV as PDF |
| `batch` | Process multiple job applications |
| `tracker` | Manage application pipeline tracker |
| `apply` | Submit tailored application for a role |
| `pipeline` | Run full search pipeline end-to-end |
| `contacto` | Find and manage recruiter contacts |
| `deep` | Deep research on a company or role |
| `training` | Practice interview questions and scenarios |
| `project` | Build portfolio project for target role |
| `dashboard` | View job search analytics and status |

## 6 Evaluation Dimensions

| Dimension | What It Assesses |
|-----------|-----------------|
| Role Summary | Key responsibilities, team structure, growth path |
| CV Match | Skills alignment, experience gaps, keyword coverage |
| Level Strategy | Seniority positioning, title negotiation |
| Comp Research | Salary range, equity, benefits benchmarking |
| Personalization | Company-specific tailoring for cover letter/CV |
| Interview Prep | STAR+R responses for likely questions |

## Interview Prep: STAR+R Method

**S**ituation → **T**ask → **A**ction → **R**esult → **R**eflection

Generates structured responses for behavioral questions with:
- Concrete metrics and outcomes
- Lessons learned (Reflection)
- Role-specific question bank

## Usage

```
User: "Evaluate this job posting for me"
Agent: Runs evaluate command, returns 6-dimension analysis with score

User: "Optimize my CV for this SWE role"
Agent: Runs pdf command with role-specific keyword injection for ATS pass

User: "Where am I in my job search?"
Agent: Runs dashboard, shows application pipeline status and next actions
```

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

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I am too busy to organize" | Disorganization costs more time than organizing. Invest upfront. |
| "Multitasking is productive" | Context switching costs 25 minutes per switch. Focus on one thing. |
| "I will remember this" | You will not. Write it down. Externalize your memory. |