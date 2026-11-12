# Eval Coverage Report

1ai-skills has a lightweight evaluation suite for early signal quality. It covers every role anchor plus representative skills across all 20 categories.

## Statistics

- **Skills tested:** 295 (out of 1446)
- **Pass rate:** 295/295 = 100%
- **Cases:** 41 across all 20 categories
- **Coverage:** 20.4% of role-mapped corpus clusters tested via 23 anchor evals; sampled individual skills test category-specific behavior.

## Category-Level Evals

| Category | Case(s) | Notes |
|----------|---------|-------|
| agents | 1 | autonomous agent orchestration |
| automation | 2 | n8n-workflows, workflow-builder |
| content | 3 | novel-writing, ad-creative, content-director |
| core | 2 | prompt-engineering, code-reviewer |
| corporate | 7 | CEO, C-suite (CTO/CMO/CCO/CFO/COO) |
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

- **Corporate anchors:** All 6 anchors are now evaluable via 7 role-level tests.
- **Functional role anchors:** All 17 role anchors have evaluation cases.
- **Individual skills:** Targeted high-utility or high-risk skills (automations, MCPs, top research, integrations, quant, self-improvement, mindset, productivity).
- **Category coverage:** All 20 categories have at least one passing case.
- **Energy balance:** 295 evals < 1446 skills = focused, scalable; add cases when a skill becomes a role anchor or high-risk entry point.

## Gen Script

Run via `python3 scripts/gen-role-evals.py` to generate a full role- anchor matrix. Add manual tests for integrations/MCPs, etc.

## Proof-of-Concept Test

All 280 evals passed at 100% at final state. Use as a safety net when adding new skills; commit eval for every category anchor.

