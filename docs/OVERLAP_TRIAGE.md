# Tier-2 Semantic-Overlap Triage

Source: `python3 scripts/lint-skills.py --overlap`. **51 pairs** flagged (≥2 of {description-token Jaccard, activation-phrase Jaccard, tag ratio} cross threshold). Signals: desc, trig, tags.

**Method:** auto-classified by body signature, then **every verdict verified by reading the pair's frontmatter + Overview by hand**. The auto-classifier was wrong in both directions (MCP servers with real docs called stubs; generic-template infra skills called substantive), so the table below reflects manual reading only.

**Verdict key:** `duplicate` (merge) · `adjacent` (keep both, cross-link) · `distinct` (keep both, no link) · `noise` (false positive — shared template, not shared function).

---

## GENUINE — both substantive (22)

| A | B | signal | verdict |
|---|---|---|---|
| tauri-apps | wails-apps | 1.81 | adjacent — Rust vs Go desktop frameworks; both already name the other in When-NOT-to-Use |
| stripe-mcp | supabase-mcp | 1.70 | distinct — payments API vs database API |
| notion-mcp | supabase-mcp | 1.67 | distinct — notes API vs database API |
| github-mcp | supabase-mcp | 1.62 | distinct — repos API vs database API |
| github-mcp | stripe-mcp | 1.59 | distinct — code vs payments |
| notion-mcp | stripe-mcp | 1.56 | distinct — notes vs payments |
| github-mcp | notion-mcp | 1.55 | distinct — repos vs notes |
| **grok-browser** | **super-browser** | 1.55 | **duplicate candidate** — super-browser explicitly bundles 8 browser skills; confirm grok-browser is in that set, then deprecate grok-browser with a redirect |
| social-media-engagement | social-media-upload | 1.55 | adjacent — engage vs publish; cross-link |
| clickup | jira | 1.53 | distinct — different vendors, different APIs |
| resend-mcp | stripe-mcp | 1.50 | distinct — email vs payments |
| github-mcp | resend-mcp | 1.49 | distinct — repos vs email |
| resend-mcp | supabase-mcp | 1.48 | distinct — email vs database |
| linear-mcp | resend-mcp | 1.47 | distinct — issues vs email |
| polymarket-fast-loop | polymarket-weather-trader | 1.47 | adjacent — same platform, different strategies; cross-link |
| clickup | multi-channel-reminder | 1.39 | adjacent — task tracking vs reminders; cross-link |
| jira | multi-channel-reminder | 1.39 | adjacent — same; cross-link |
| notion-mcp | resend-mcp | 1.37 | distinct — notes vs email |
| conducting-social-engineering-penetration-test | conducting-social-engineering-pretext-call | 1.33 | adjacent — umbrella engagement vs single pretext call; cross-link |
| content-scheduler | lynk | 1.25 | adjacent — scheduling vs affiliate link mgmt; cross-link if scheduling overlaps |
| data | performance-monitor | 1.21 | adjacent — pipeline vs monitoring; cross-link |
| analytics-dashboard | lynk | 1.18 | distinct — analytics vs affiliate links |

---

## ADJACENT (18)

| A | B | signal | verdict |
|---|---|---|---|
| polymarket | polymarket-fast-loop | 1.72 | parent/child — platform skill vs specific bot; cross-link |
| polymarket | polymarket-weather-trader | 1.70 | parent/child — weather-specific strategy; cross-link |
| vault-pki | vault-secrets | 1.65 | sibling engines on one Vault server (PKI vs KV); cross-link |
| ios-swiftui | swiftui-patterns | 1.60 | **decide**: ios-swiftui body is thin/generic, swiftui-patterns is substantive — rewrite ios-swiftui as iOS-specific or deprecate into swiftui-patterns; do not blind-merge |
| ai-research-agent | sherlock-research | 1.48 | general research vs Sherlock-style OSINT; cross-link |
| business-development | talent-crm | 1.45 | BD outreach vs talent pipeline; cross-link |
| jira | revenue-team | 1.20 | task tracker vs revenue ops; distinct function, shared "team ops" vocabulary |
| auto-git-commiter | vilona | 1.18 | distinct — git versioning vs memory persistence; shared core-infra template only |
| auto-learner | data | 1.30 | meta learning loop vs data pipeline; cross-link |
| data | self-assessment | 1.29 | pipeline vs meta self-check; cross-link |
| lynk | market-research | 1.25 | affiliate links vs market research; cross-link |
| lynk | social-growth | 1.23 | affiliate links vs social growth; cross-link |
| lynk | viral-marketing | 1.23 | affiliate links vs viral marketing; cross-link |
| governance-team | operations-team | 1.74 | governance (policy/access/compliance) vs ops (SOP/SLA/on-call); cross-link |
| revenue-team | operations-team | 1.70 | distinct — pipeline/forecasting vs SOP/incident; shared "team" boilerplate |
| marketing-strategy | viral-marketing | 1.43 | adjacent — full framework (personas, AIDA, calendar, scripts) vs narrow amplification; cross-link |
| kalodata-product-research | kalodata-research-automation | 1.41 | parent/child — automation composes product-research + video-analysis + storyboard-extract |
| sales-strategy | talent-crm | 1.29 | sales pipeline vs recruiting pipeline; shared pipeline vocabulary |

---

## DISTINCT (4)

| A | B | signal | verdict |
|---|---|---|---|
| lynk | marketing-strategy | 1.30 | affiliate link platform vs content/campaign framework |
| jira | operations-team | 1.19 | issue-tracker API vs SOP execution |
| teamwork | vilona | 1.31 | teamwork body is generic core-infra template; vilona has real entity/memory code |
| hive-mind | vilona | 1.23 | TiDB config-sync vs entity/memory layer; tag-level overlap only |

---

## TEMPLATE NOISE (7)

Shared boilerplate, not shared function. Both sides are stub-template bodies or share one generated section.

| A | B | signal | note |
|---|---|---|---|
| hardening-linux-endpoint-with-cis-benchmark | hardening-windows-endpoint-with-cis-benchmark | 1.85 | OS-specific siblings; both bodies are stub template — real fix is rewriting both, not merging |
| hunting-for-persistence-mechanisms-in-windows | hunting-for-registry-persistence-mechanisms | 1.77 | general vs registry-specific; both stub template |
| polymarket | tushare-finance | 1.27 | prediction markets vs stock data; shared trading template |
| crypto-trading-bot | polymarket | 1.25 | generic bot vs platform-specific; shared template |
| maybe-hft | sherlock-research | 1.24 | HFT vs OSINT research; shared research template |
| governance-team | jira | 1.20 | governance team vs issue tracker; shared ops template |
| adcp-advertising | lynk | 1.19 | advertising protocol vs affiliate links; shared marketing template |

---

## Notes

- **Path drift resolved:** `operations-team` → `operations/team`, `marketing-strategy` → `marketing/strategy`, `sales-strategy` → `sales/strategy`, kalodata skills → `integrations/kalodata/*`. The linter keys on frontmatter `name`, so directory names differ from the flagged names.
- **One duplicate candidate** worth acting on: `grok-browser` vs `super-browser`. Every other substantive pair is adjacent (cross-link) or distinct (leave alone).
- **No merges performed.** Every verdict above is a recommendation; merging is a human/author decision.
- **The dominant quality problem is not duplication — it is stub bodies.** CIS hardening, persistence hunting, Vault, corporate team roles, and several marketing/research skills still carry generic template Overviews. Rewrite those before re-running triage.
- Re-run: `python3 scripts/lint-skills.py --overlap`.
