---
name: prompt-library-curator
description: Use when collecting website and UI prompts from curated galleries into a reusable, rights-checked local library — intake criteria, metadata schema, prompt normalization, deduplication, and safe use of paid sources. Use for design prompt packs and inspiration research.
domain: content
category: content
subdomain: design
tags:
- prompts
- curation
- web-design
- licensing
- inspiration
- research
version: 1.0.0
author: oyi77
license: MIT
triggers:
- "curate design prompts"
- "build prompt library"
- "website prompt gallery"
- "reuse UI prompts"
---

# Prompt Library Curator

Convert scattered gallery prompts into a small, verifiable local library with provenance and rights metadata. Galleries such as jiro.build (1,500+ website prompts), header.design (animated header prompt + code), scrolltide.co (scroll-driven templates, shaders, sections), landdding.com, and recent.design are useful references; most are paid or access-gated. Respect those boundaries.

## Overview

A prompt copied from a gallery with no source, license, or date is unusable later: you cannot tell whether it is safe to reuse, whether it still matches the product, or whether you wrote it. This skill defines an intake gate and a compact metadata record. It curates references and locally authored adaptations — it does not scrape paywalls, bypass logins, or redistribute gated prompt text. Pair with [design-taste](../design-taste/SKILL.md) for reference research and [awwwards-quality-sites](../awwwards-quality-sites/SKILL.md) for build quality.

## When to Use

- Building a team prompt pack from public or purchased gallery material.
- Turning a one-off prompt into a reusable, attributed pattern.
- Auditing an existing prompt collection for provenance and duplicate entries.

## When NOT to Use

- Generating a one-off website from a single prompt — use the frontend design skills.
- Extracting prompts from a service you do not have rights to access.
- Storing secrets, customer data, or credentials in prompt metadata.

## Workflow

### 1. Intake gate

Record for each candidate: source URL, access date, access basis (public / purchased / licensed by employer), rights statement found, and whether the prompt text itself is copyrightable or licensed. If any field is missing, the candidate enters `quarantine`, not the active library.

Never copy content behind a paywall or login you do not hold. When a service offers an MCP or API, use the sanctioned interface with the account that owns the access. A purchased prompt pack may permit client work but forbid redistribution — read the terms, do not assume.

### 2. Normalize into one record per prompt

```yaml
id: scroll-hero-reveal-01
title: Scroll-linked hero reveal
source_url: https://example.com/library/item
access: purchased            # public | purchased | licensed
access_date: 2026-11-27
rights: "personal + client use; no redistribution of prompt text"
original_author: "gallery author or unknown"
adaptation: "rewritten for React/CSS; removed vendor-specific class names"
tier: A                      # A verified rights | B rights unclear | C quarantine
tags: [scroll, hero, motion, landing]
body: |
  Build a hero section where …
```

Keep the original text separate from your adaptation. Never overwrite `source_url` or `rights` during edits.

### 3. Deduplicate by intent, not wording

Two prompts with different prose but the same activation (hero reveal, header animation, pricing grid) are one pattern with variants. Keep the stronger record and link the others as variants. Descriptions that differ only in adjectives are duplicates.

### 4. Reduce dependency on any single gallery

Gallery catalogs are volatile and often gated. Store a summary of the *pattern* (layout intent, motion behavior, accessibility constraints) rather than a verbatim transcript you cannot legally share. When a prompt depends on a paid asset, record the dependency explicitly so a future agent can substitute an equivalent.

### 5. Validate the library locally

```python
import json

records = json.load(open("prompts.json", encoding="utf-8"))
required = {"id", "source_url", "access", "access_date", "rights", "tier", "body"}
for record in records:
    missing = required - record.keys()
    assert not missing, f"{record.get('id', '<no id>')}: missing {sorted(missing)}"
    assert record["tier"] in {"A", "B", "C"}, f"bad tier: {record['tier']}"
    assert record["source_url"].startswith("https://"), f"bad source: {record['id']}"
assert len({r["id"] for r in records}) == len(records), "duplicate ids"
print(f"{len(records)} records valid")
```

Run this before merging a batch; fix failures at the record level, not by weakening the validator.

### 6. Apply with taste and verification

Select a prompt by tags and tier; prefer tier A. Adapt it to the actual brand, content, and framework rather than pasting verbatim. Confirm the result against [awwwards-quality-sites](../awwwards-quality-sites/SKILL.md) checks: accessibility, responsiveness, no fabricated content. Record the outcome back into the record so the next agent knows what worked.

## Common Pitfalls / Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "It's public on the internet, so I can reuse it" | Public access is not a license; check terms and attribution. |
| "I bought it, so I can share it with the team" | Per-seat and client-work terms differ; read the grant. |
| "I'll add provenance later" | Provenance is the record; without it the prompt has no trustworthy future use. |
| "More prompts means a better library" | Duplicate intents create routing noise; curate, do not accumulate. |
| "The gallery prompt is validated, so the output is good" | Galleries sell starting points; accessibility and content still need verification. |

## Verification

- [ ] Every active record has source URL, access basis, date, rights statement, tier, and body.
- [ ] No record comes from an access the agent does not hold; no paywall bypass used.
- [ ] Local validator ran with zero assertion errors and unique ids.
- [ ] Duplicate intents consolidated; at least one pattern has a documented adaptation.
- [ ] Output built from a prompt checked against accessibility and responsiveness criteria.
