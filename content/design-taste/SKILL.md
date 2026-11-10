---
name: design-taste
description: Use when building a UI and need to ground taste in real products — query Kage MCP for screenshots and layout prompts of comparable apps, then synthesize a design brief before writing code. Use when "design a site like X", "UI in the spirit of Y", or "what should this look like" — a taste-first research layer for agents, not a template gallery.
domain: content
author: oyi77
license: MIT
subdomain: design
category: content
tags:
  - design
  - ui
  - taste
  - inspiration
  - research
  - mcp
  - screenshots
  - prompts
version: 1.0.0
triggers:
  - "design a site like"
  - "ui in the spirit of"
  - "design taste"
  - "ui inspiration"
  - "like linear for"
  - "what should this look like"
  - "find design references"
  - "competitor ui"
  - "design brief from references"
argument-hint: "[product_or_style] for [audience]"
---

## Overview

Design-taste is a research layer that grounds UI decisions in real products before an agent writes code. It uses Kage MCP (free, keyless at `https://kage.design/mcp`) to find screenshots and stored layout prompts for comparable apps, extracts concrete decisions (layout, typography, spacing, colour), then synthesizes a brief for the build. Research is mandatory — an agent that skips it defaults to the same generic Tailwind layout every time.

Refero (paid MCP, MIT skill) teaches the same workflow with 150k+ app screens and flows; Kage covers the same shape of research with 600+ web products and no auth. Use whichever endpoint you can reach.

## When to Use

- User says "design X like Y" — a named reference product
- User says "in the spirit of" or "similar to" without naming a product
- User asks "what should this look like" or "how should this feel"
- New surface, no existing design language in the repo
- Competitor teardown: "what do Linear, Notion, Arc do here?"
- Before delegating a build to `hallmark`, `impeccable`, or `anti-slop-frontend`

## When NOT to Use

- DESIGN.md already exists and tokens are locked — go straight to `impeccable document` + build
- User has a Figma frame or a screenshot of the target — use `image-to-code` directly
- Task is pure component work in an existing system — use `shadcn-ui` or `21st-dev`
- User wants accessibility fixes only — use `accessibility-audit`
- User wants a rendered audit of existing code — use `ui-critique`

## Workflow

### 1. Frame the brief (no tools yet)

Write three lines before calling anything:
- **What** — the surface (landing, pricing, onboarding, dashboard)
- **Who** — the audience and the job they hire the product for
- **Constraint** — stack, brand colour, platform, deadline

Ambiguous brief? Ask one question. Do not guess product positioning.

### 2. Query Kage MCP

Endpoint: `https://kage.design/mcp` (Streamable HTTP, no auth). Add to `.cursor/mcp.json` or `claude mcp add --transport http kage https://kage.design/mcp`.

Tools:
- `design_brief` — closest matches to a text brief; returns stored prompts + screenshots
- `search_designs` — search the 600+ library by product/style/industry
- `get_design` — one product's full prompt, taxonomy, extracted components with prompts, and the screenshot
- `get_component` — one extracted component (hero, pricing, footer) with its prompt and crop
- `list_taxonomy` — vocabulary of page types, styles, industries, stacks, colours

```json
{
  "mcpServers": {
    "kage": { "url": "https://kage.design/mcp" }
  }
}
```

Example call: `"Design a landing page like Linear for a dental clinic"` → `design_brief` returns Linear's stored prompt (layout, type, spacing, colour only — no brand or copy) plus 2–3 comparable screenshots.

### 3. Synthesize, do not average

Pick **one** primary reference. Borrow at most one narrow detail (a hero rhythm, a nav treatment) from a secondary. Do not blend three products into a beige average.

For each borrowed decision, write one line:
```
Layout: hero left-aligned + dense feature bento  ← from Linear
Type: Public Sans, 72/16/12 scale                ← from Stripe
Colour: #0A0A0A surface, single accent            ← from Vercel
Motion: 200ms ease-out, no parallax               ← justified restraint
```

If no MCP is available (Kage down, restricted environment), fall back to the methodology alone: name 2–3 comparable products from memory, extract layout/type/colour from what you know of them, and state clearly in the brief that no live research was run.

### 4. Lock the direction, then build

Save the synthesis as a `design-brief.md` beside the surface (or in `PRODUCT.md` per `impeccable`). Then delegate the actual build:
- Full page → `hallmark` (Floor enforcement) or `impeccable` (24 commands)
- Craft constraints only → `anti-slop-frontend`
- Component assembly → `21st-dev` + `shadcn-ui`

Verification of the built page is owned by the downstream skill, not this one.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I already know what Linear looks like" | Memory of a product is a vibe, not a spec. Query MCP; you'll find spacing and type values you'd have gotten wrong. |
| "MCP is down, I'll skip research" | Do the synthesis from memory and say so in the brief. Silent skip = default Tailwind layout. |
| "Three references make it richer" | Three references average into generic. Pick one primary, borrow narrowly from others. |
| "The screenshots are the design" | Prompts describe layout/type/colour, not brand or copy. Building a clone is a ToS and craft violation. |
| "Research is overhead for a small component" | For a single button, fine. For any surface with a hero, pricing, or onboarding flow — research first. |

## Verification

- [ ] Brief names one primary reference and at most one secondary detail-borrow
- [ ] Layout, typography, spacing, and colour each traced to a source (live MCP or named-from-memory)
- [ ] No product copy, logo, or brand asset reproduced
- [ ] Build delegated to the correct downstream skill (`hallmark` / `impeccable` / `anti-slop-frontend` / `21st-dev`)
- [ ] If research was skipped or MCP failed, the brief says so explicitly

## References

- Kage library and taxonomy: <https://kage.design>
- Kage MCP setup: <https://kage.design/mcp-setup>
- Kage terms (prompts free for commercial use, no attribution; no bulk scraping): <https://kage.design/terms>
- Refero skill (MIT, same methodology, paid MCP): <https://github.com/referodesign/refero_skill>
- Google DESIGN.md spec (format the brief can target): <https://github.com/google-labs-code/design.md>