# Tier-2 Semantic-Overlap Triage

Source: `python3 scripts/lint-skills.py --overlap`. **51 pairs** flagged (≥2 of {description-token Jaccard, activation-phrase Jaccard, tag ratio} cross threshold). Signals: desc, trig, tags.

**Method:** First pass auto-classified by body (Overview count, template markers, line count). Auto-classifier produced false categories (MCP servers with real docs flagged as GENUINE pairs needing review; OS-specific sibling skills with stub bodies flagged as TEMPLATE NOISE). Corrected by manual verification of the flagging pair's description + Overview sections.

**Verdict key:** `duplicate` (merge into one) · `adjacent` (keep both, cross-link via Related Skills) · `distinct` (keep both, no cross-link — shared tags only) · `noise` (false positive: boilerplate stub or shared generic template).

---

## GENUINE — requires human review (24)

Both skills are substantive (real Overview content, non-boilerplate body). Judge duplicate / adjacent / distinct:

| A | B | signal | verdict |
|---|---|---|---|
| tauri-apps | wails-apps | 1.81 | adjacent — Rust vs Go desktop frameworks; cross-link both |
| stripe-mcp | supabase-mcp | 1.70 | distinct — different APIs (payments vs database) |
| notion-mcp | supabase-mcp | 1.67 | distinct — different APIs (notes vs database) |
| github-mcp | supabase-mcp | 1.62 | distinct — different APIs (repos vs database) |
| github-mcp | stripe-mcp | 1.59 | distinct — different APIs (code vs payments) |
| notion-mcp | stripe-mcp | 1.56 | distinct — different APIs |
| github-mcp | notion-mcp | 1.55 | distinct — different APIs (repos vs notes) |
| grok-browser | super-browser | 1.55 | adjacent — super-browser bundles 8 browser skills incl. grok-class; decide if grok-browser should be merged into super-browser's bundle |
| social-media-engagement | social-media-upload | 1.55 | adjacent — engagement vs upload; cross-link |
| clickup | jira | 1.53 | distinct — different task-management tools (ClickUp vs Jira) |
| resend-mcp | stripe-mcp | 1.50 | distinct — different APIs (email vs payments) |
| github-mcp | resend-mcp | 1.49 | distinct — different APIs |
| resend-mcp | supabase-mcp | 1.48 | distinct — different APIs |
| linear-mcp | resend-mcp | 1.47 | distinct — different APIs (issues vs email) |
| polymarket-fast-loop | polymarket-weather-trader | 1.47 | adjacent — same platform, different strategies; cross-link |
| clickup | multi-channel-reminder | 1.39 | adjacent — reminder tooling vs task tooling; cross-link |
| jira | multi-channel-reminder | 1.39 | adjacent — same; cross-link |
| notion-mcp | resend-mcp | 1.37 | distinct — different APIs |
| conducting-social-engineering-penetration-test | conducting-social-engineering-pretext-call | 1.33 | adjacent — pen-test umbrella vs pretext-call specific; cross-link |
| content-scheduler | lynk | 1.25 | adjacent — content scheduling vs affiliate link mgmt; cross-link if overlap is scheduling |
| data | performance-monitor | 1.21 | adjacent — data pipeline vs monitoring; cross-link |
| jira | revenue-team | 1.20 | distinct — task tracker vs revenue ops |
| auto-git-commiter | vilona | 1.18 | distinct — git automation vs orchestration |
| analytics-dashboard | lynk | 1.18 | distinct — analytics vs affiliate links |

---

## ADJACENT (15)

| A | B | signal | verdict |
|---|---|---|---|
| polymarket | polymarket-fast-loop | 1.72 | parent/child — fast-loop is Polymarket-specific bot; keep both, cross-link |
| polymarket | polymarket-weather-trader | 1.70 | parent/child — weather-specific; keep both, cross-link |
| vault-pki | vault-secrets | 1.65 | sibling engines (PKI vs key/value secrets) on same Vault server; keep both, cross-link |
| ios-swiftui | swiftui-patterns | 1.60 | adjacent — iOS SwiftUI guides; consider merge if genuinely duplicated |
| ai-research-agent | sherlock-research | 1.48 | adjacent — general research vs Sherlock-specific; cross-link |
| business-development | talent-crm | 1.45 | adjacent — BD outreach vs talent pipeline; cross-link |
| teamwork | vilona | 1.31 | adjacent — collaboration vs orchestration; cross-link |
| auto-learner | data | 1.30 | adjacent — meta learning vs data; cross-link |
| data | self-assessment | 1.29 | adjacent — data pipeline vs meta self-assessment; cross-link |
| lynk | market-research | 1.25 | adjacent — affiliate links vs market research; cross-link |
| hive-mind | vilona | 1.23 | adjacent — multi-agent vs orchestration; cross-link |
| lynk | social-growth | 1.23 | adjacent — affiliate links vs social growth; cross-link |
| lynk | viral-marketing | 1.23 | adjacent — affiliate links vs viral marketing; cross-link |
| governance-team | jira | 1.20 | adjacent — team governance vs task tracker; cross-link |
| adcp-advertising | lynk | 1.19 | adjacent — advertising vs affiliate links; cross-link |

---

## TEMPLATE NOISE (5)

| A | B | signal | verdict |
|---|---|---|---|
| hardening-linux-endpoint-with-cis-benchmark | hardening-windows-endpoint-with-cis-benchmark | 1.85 | OS-specific siblings sharing CIS-benchmark boilerplate; not duplicates — keep both, no merge |
| hunting-for-persistence-mechanisms-in-windows | hunting-for-registry-persistence-mechanisms | 1.77 | general vs registry-specific; both share stub boilerplate; keep both |
| polymarket | tushare-finance | 1.27 | different platforms (Polymarket prediction vs Tushare stock data); shared trading boilerplate |
| crypto-trading-bot | polymarket | 1.25 | generic bot vs Polymarket-specific; shared trading boilerplate |
| maybe-hft | sherlock-research | 1.24 | unrelated domains (HFT research vs Sherlock OSINT); shared research boilerplate |

---

## UNRESOLVED (7)

| A | B | signal | verdict |
|---|---|---|---|
| governance-team | operations-team | 1.74 | operations-team not found at expected path — check if renamed/moved |
| revenue-team | operations-team | 1.70 | same — operations-team missing |
| marketing-strategy | viral-marketing | 1.43 | marketing-strategy not found — check path |
| kalodata-product-research | kalodata-research-automation | 1.41 | kalodata paths missing — likely moved under integrations/ or renamed |
| lynk | marketing-strategy | 1.30 | marketing-strategy missing |
| sales-strategy | talent-crm | 1.29 | sales-strategy missing — check path |
| jira | operations-team | 1.19 | operations-team missing |

**Action:** Resolve missing paths before re-running. If they exist under different paths, re-run `lint-skills.py --overlap` and re-triage.

---

## Notes

- Auto-classifier's first pass was wrong on MCP-server bodies (they contain real docs, not boilerplate stubs) — MCP pair verdicts corrected to `distinct` after reading Overview sections directly.
- No merges performed. All 51 verdicts above are recommendations; merging is a human decision.
- Re-run `python3 scripts/lint-skills.py --overlap` after addressing any verdict.
