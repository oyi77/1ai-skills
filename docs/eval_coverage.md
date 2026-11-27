# Eval Coverage Report

1ai-skills has a lightweight evaluation suite for early signal quality. It covers every role anchor plus representative skills across all 20 categories.

## Statistics

- **Cases:** 53 across all 20 categories
- **Checks:** 399 total; 399 passed, 0 failed, 0 skipped (100%)
- **Corpus:** 1462 active skills in 20 categories (`SKILLS.json`)
- **Coverage:** 17 `role-*` anchor cases + 14 corporate cases (6 C-suite + 8 exception handlers); the remaining 22 cases sample individual skills for category-specific behavior.

Regenerate the numbers with `python3 scripts/run-evals.py --all --json` (`total_cases`, `total_checks`, `total_passed`).

## Category-Level Evals

| Category | Case(s) | Notes |
|----------|---------|-------|
| agents | 1 | autonomous agent orchestration |
| automation | 2 | n8n-workflows, workflow-builder |
| content | 3 | novel-writing, ad-creative, content-director |
| core | 2 | prompt-engineering, code-reviewer |
| corporate | 14 | CEO, C-suite (CTO/CMO/CCO/CFO/COO) + 8 exception handlers (owner-idea-intake, multi-department-brainstorm, owner-decision-log, incident-commander, crisis-communications, legal-counsel, people-operations, vendor-and-partnerships) |
| cybersecurity | 3 | request.bin, ssh-audit, dnsenum |
| data | 1 | airbyte-connector |
| development | 5 | test-driven-development, code-reviewer, api-contract, concurrency, system-architect |
| devops | 2 | dockerfile-optimize, terraform-infra |
| financial | 1 | compound-interest-model |
| integrations | 1 | stripe-integration |
| marketing | 2 | seo-optimizer, ad-creative |
| mcp | 2 | github-mcp, mcp-server-builder |
| meta | 1 | auto-evolve |
| mindset | 1 | first-principles-thinking |
| operations | 1 | shared-checklists-sop |
| productivity | 1 | meeting-management |
| research | 2 | market-analysis, competitor-intelligence |
| sales | 2 | lead-scoring, email-workflow |
| trading | 1 | polyswap-arb |

## Notes on Coverage

- **Corporate anchors:** All 6 C-suite anchors plus 8 exception handlers are covered (14 cases).
- **Functional role anchors:** All 17 role anchors have evaluation cases.
- **Individual skills:** Targeted high-utility or high-risk skills (automations, MCPs, top research, integrations, quant, self-improvement, mindset, productivity).
- **Category coverage:** All 20 categories have at least one passing case.
- **Energy balance:** 399 checks across 53 cases < 1462 skills = focused, scalable; add cases when a skill becomes a role anchor or high-risk entry point.

## Gen Script

Run via `python3 scripts/gen-role-evals.py` to generate a full role- anchor matrix. Add manual tests for integrations/MCPs, etc.

## Proof-of-Concept Test

All 399 checks passed at 100% at final state. Use as a safety net when adding new skills; commit eval for every category anchor.

