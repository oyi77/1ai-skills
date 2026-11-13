# Corporate Cases — Dispatch Coverage Registry

**Version:** 1.0.0  
**Last updated:** 2026-11-13  
**Total corporate skills:** 14

This document registers all corporate dispatch paths, triggers, personas, workflows, and verification requirements. Every corporate skill MUST have:

1. **Triggers** — explicit phrases in frontmatter
2. **Dispatch matrix** — valid delegated targets that resolve to actual skills
3. **Workflow** — documented steps
4. **Verification checklist** — pre-execution gates
5. **Integration** — 1ai-rules references (DECISION.md, INCIDENT.md, etc.)
6. **Anti-rationalization table** — corner-cutting defenses
7. **Persona** — named expert with philosophy/principles
8. **Frontmatter** — version, license, subdomain, tags, description, argument-hint

---

## Coverage Table

| Skill | Triggers | Dispatch Matrix | Workflow | Verification | Integration | Anti-Rat | Persona |
|---|---|---|---|---|---|---|---|
| role-ceo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-cto | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-cfo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-cmo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-coo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-cco | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-owner-idea-intake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-multi-department-brainstorm | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-owner-decision-log | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-incident-commander | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-crisis-communications | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-legal-counsel | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-people-operations | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| role-vendor-and-partnerships | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Status:** 14/14 corporate skills have complete dispatch documentation.

---

## Skill Registry

### C-Suite Anchors (6)

| Role | Skill Path | Persona | Subdomain | Triggers |
|---|---|---|---|---|
| CEO | `corporate/ceo/SKILL.md` | Satya Nadella | corporate-leadership | ceo role, corporate strategy, executive coordination, resource allocation, cross-team alignment |
| CTO | `corporate/cto/SKILL.md` | Larry Page | core-technology-leadership | cto role, tech strategy, engineering leadership, r&d roadmap, infrastructure overhaul |
| CFO | `corporate/cfo/SKILL.md` | Ruth Porat | financial-leadership | cfo role, financial strategy, budget allocation, investment analysis, revenue optimization |
| CMO | `corporate/cmo/SKILL.md` | Seth Godin | marketing-leadership | cmo role, marketing strategy, growth plan, customer acquisition, sales pipeline oversight |
| COO | `corporate/coo/SKILL.md` | Sheryl Sandberg | operational-leadership | coo role, operations strategy, process optimization, cross-team coordination, hr & legal oversight |
| CCO | `corporate/cco/SKILL.md` | Ana Andjelic | creative-leadership | cco role, content strategy, creative direction, brand voice, multi-format content |

### Corporate Exception Handlers (8)

| Role | Skill Path | Persona | Subdomain | Triggers |
|---|---|---|---|---|
| Owner Idea Intake | `corporate/owner-idea-intake/SKILL.md` | Vilona | corporate-idea-management | owner idea, new product idea, what if we build, like tradoor, competitor reference, should we build this, idea evaluation, strategic fit, vilona triage, owner proposal |
| Multi-Department Brainstorm | `corporate/multi-department-brainstorm/SKILL.md` | Ruth Porat | corporate-decision-making | multi-department review, cross-functional debate, stakeholder discussion, brainstorm across teams, who should weigh in, department perspectives |
| Owner Decision Log | `corporate/owner-decision-log/SKILL.md` | Aswath Damodaran | corporate-decision-making | log the decision, decision log, record the idea outcome, owner decision, audit trail, write up the verdict |
| Incident Commander | `corporate/incident-commander/SKILL.md` | Charity Majors | corporate-exception-management | production down, outage, data loss, security breach, incident commander, sev1, sev2, war room, sev1 incident, production outage, service down, blast radius, postmortem |
| Crisis Communications | `corporate/crisis-communications/SKILL.md` | Ana Andjelic | corporate-exception-management | pr crisis, reputational, viral complaint, public apology, holding statement, brand crisis, media response |
| Legal Counsel | `corporate/legal-counsel/SKILL.md` | Christine Lagarde | corporate-exception-management | legal review, contract terms, gdpr, privacy policy, nda, ip assignment, regulatory compliance, legal dispute, outside counsel |
| People Operations | `corporate/people-operations/SKILL.md` | Sheryl Sandberg | corporate-people-operations | hire, onboarding, offboarding, performance review, compensation, role change, team restructure |
| Vendor & Partnerships | `corporate/vendor-and-partnerships/SKILL.md` | Aswath Damodaran | corporate-strategy | vendor evaluation, procurement, partnership, strategic partnership, m&a, acquisition target, due diligence, contract review |

---

## Dispatch Path Registry

### CEO Dispatch

| Objective | Target | Artifact |
|---|---|---|
| Technology Strategy | `corporate/cto` | Architecture doc, R&D backlog |
| Growth Strategy | `corporate/cmo` | Growth plan, acquisition funnel |
| Content Vision | `corporate/cco` | Content strategy, brand guidelines |
| Financial Strategy | `corporate/cfo` | Financial model, investment thesis |
| Operations | `corporate/coo` | Operational playbook, OKR tracking |
| Incident Response | `corporate/incident-commander` | SEV declaration, war room |
| Owner Idea | `corporate/owner-idea-intake` → `corporate/multi-department-brainstorm` | Build/research/archive verdict |
| M&A / Partnership | `corporate/vendor-and-partnerships` → `corporate/cfo` | Diligence, valuation, deal memo |
| PR Crisis | `corporate/crisis-communications` → `corporate/cco` + `corporate/cmo` | Crisis playbook |
| Legal Dispute | `corporate/legal-counsel` | Compliance review, counsel brief |
| Hiring | `corporate/people-operations` | Hire packet, onboarding |
| Customer Escalation | `corporate/crisis-communications` → `sales/role-customer-support` | Executive response |

### CTO Dispatch

| Objective | Target | Artifact |
|---|---|---|
| Engineering | `development/role-software-engineer` | Code, tests, PRs |
| Architecture | `development/role-system-architect` | ADRs, system design |
| Security | `cybersecurity/role-security-engineer` | Threat model, findings |
| Offensive Security | `cybersecurity/role-penetration-tester` | Exploit chain, PoC |
| Data | `data/role-data-engineer` | Pipelines, ETL |
| AI/ML | `core/role-ai-ml-engineer` | Model routing, evals |

### CFO Dispatch

| Objective | Target | Artifact |
|---|---|---|
| Financial Analysis | `financial/role-financial-analyst` | DCF, sensitivity analysis |
| Trading | `trading/role-quantitative-trader` | Backtest, risk model, P&L |

### CMO Dispatch

| Objective | Target | Artifact |
|---|---|---|
| Growth Marketing | `marketing/role-growth-marketer` | Funnel metrics, experiments |
| Sales | `sales/role-sales-engineer` | Pipeline, close rate |

### COO Dispatch

| Objective | Target | Artifact |
|---|---|---|
| Product Management | `operations/role-product-manager` | Roadmap, PRD |
| Customer Support | `sales/role-customer-support` | SLA, churn analysis |
| HR Onboarding | `operations/hr-onboarding` | 90-day plan |
| Legal Compliance | `operations/legal-compliance` | Control set, audit evidence |
| Contract Management | `operations/contract-manager` | Redlines, terms |
| Governance | `operations/governance-team` | Policy, compliance |

### CCO Dispatch

| Objective | Target | Artifact |
|---|---|---|
| UI/UX Design | `content/role-ui-ux-designer` | Figma, CSS tokens |
| Content Production | `content/role-content-creator` | Video, copy, images |

---

## Hook Registry

| Hook | Type | Script | Triggers |
|---|---|---|---|
| role-router | UserPromptSubmit | `hooks/skill-router-prompt.js` | Any prompt with score >= 30.0 matching role-* anchor |
| owner-intake | UserPromptSubmit | `hooks/owner-idea-intake.js` | "I have an idea", "what if we build", competitor reference |

---

## Verification Registry

Every corporate skill MUST pass:

1. **Frontmatter validation** — `python3 scripts/validate-skills.py`
2. **Schema validation** — `python3 scripts/validate-skill-schema.py`
3. **Lint** — `python3 scripts/lint-skills.py`
4. **Test** — `python3 scripts/test-skills.py`
5. **Eval** — `python3 scripts/run-evals.py --category corporate`
6. **Dispatch refs** — `python3 scripts/check-dispatch-refs.py`
7. **Role map** — `python3 scripts/role_map.py`
8. **Router regression** — `python3 scripts/test_skill_router_regression.py`

---

## Integration Registry

| Corporate Skill | 1ai-rules Integration |
|---|---|
| All | DECISION.md §4 (decision logging), COMMS.md (undocumented = unapproved) |
| CEO, C-Suite | ROLES.md §1 (role registry), §2 (authority thresholds) |
| Incident Commander | INCIDENT.md (SEV declaration, war room, postmortem) |
| Crisis Communications | COMMS.md, INCIDENT.md, LEGAL.md |
| Legal Counsel | LEGAL.md, INCIDENT.md |
| Multi-Department Brainstorm | MULTI_AGENT.md (Advocate/Skeptic/Synthesizer protocol) |
| Owner Idea Intake | SURPASS.md (research protocol), DECISION.md §2 (authority gates) |
| Vendor & Partnerships | DECISION.md §2 (Type 2 approval), §4 (logging) |
| People Operations | DECISION.md §2 (Type 2 hiring), §4 (logging) |

---

## Anti-Rationalization Registry

Every corporate skill includes an anti-rationalization table. Common patterns:

| Rationalization | Reality |
|---|---|
| "We'll fix it later" | Later becomes never; technical debt compounds |
| "It's just a small change" | Small changes have cascading effects |
| "The demo looked good" | Demos omit failure modes and edge cases |
| "We can skip the checklist" | Checklists prevent known failure modes |
| "AI can decide this" | AI prepares briefs; humans decide Type 2 |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-11-13 | Initial registry; 14/14 corporate skills documented |

---

## License

MIT — same as 1ai-skills repo.
