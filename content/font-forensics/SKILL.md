---
name: font-forensics
description: Use when identifying a typeface from a logo or screenshot and choosing a license-safe replacement — evidence tiers, visual comparison, webfont licensing checks, and fallback stacks. Use for font matching, logo typography audits, and accessible typography specs.
domain: content
category: content
subdomain: design
tags:
- typography
- fonts
- logo
- licensing
- accessibility
- web-design
version: 1.0.0
author: oyi77
license: MIT
triggers:
- "what font is this"
- "identify logo font"
- "match this typeface"
- "font licensing"
---

# Font Forensics

Identify typefaces with graded evidence, then specify a legally usable, accessible replacement. Reference databases such as fontinlogo.com can supply a candidate; they are not proof of licensing or of an exact match.

## Overview

Font identification is an evidence problem, not a guessing game. Strongest evidence is the target's own published asset (brand guideline, CSS `@font-face`, design token file). Next comes a verified database entry with the glyph-level comparison. Weakest is visual similarity. Never ship a font because a lookup site said so — confirm the license for the actual usage (print, logo, web embedding, app bundling) before it enters a design system. Pair this with [better-typography](../better-typography/SKILL.md) for scale and [design-system](../design-system/SKILL.md) for tokens.

## When to Use

- Reverse-engineering a logo or screenshot's typeface for a redesign or style audit.
- Selecting an open-licensed substitute for a proprietary brand font.
- Reviewing a font choice for web embedding, desktop app bundling, or client handoff.

## When NOT to Use

- Authoring a font from scratch — no skill here covers font design.
- Pure type scale, line-height, or hierarchy decisions without identification — use `better-typography`.
- Validating a trademark or brand identity claim; this skill covers typography only.

## Workflow

### 1. Collect primary evidence first

Check, in order: official brand guidelines or press kit; the live site's CSS (`font-family`, `@font-face`, font file URLs); the design system repo; the image's metadata. Record the URL and retrieval date for each. If the target is a paid/closed resource, note that and do not bypass access controls.

### 2. Cross-check candidates against a database

Lookup services can narrow candidates; fontinlogo.com, for example, indexes brand → font with a "verified" tier. Treat "verified" as a claim requiring a source link. Compare at least three discriminating glyphs — e.g. lowercase `a/g`, numeral `1`, and the `R` leg — at similar weight and size. A match on one letterform is not a match.

### 3. Assign an evidence tier

| Tier | Basis | Allowed action |
|---|---|---|
| A — primary | Official guideline, CSS, or font file from the target | Specify directly, subject to license |
| B — corroborated | Verified database entry + glyph comparison | Use as candidate; confirm before shipping |
| C — visual only | Similar-looking font | Prototype only; never present as the original |

Write the tier next to the candidate in the design note. Do not launder tier C into tier A by repeating the guess.

### 4. Check the license for the intended use

Read the actual license text from the foundry or repository. Confirm: commercial use, logo use, webfont embedding, modification, redistribution, and any seat/domain limits. OFL permits embedding and modification with conditions; Apache-2.0 and SIL OFL are not interchangeable; "free for personal use" is not commercial clearance. When the license cannot be verified, choose a documented open-licensed substitute.

### 5. Specify a robust stack

```css
/* Tier B candidate plus license-safe fallbacks; order matters. */
:root {
  --font-display: "Candidate Display", "Inter", "Helvetica Neue", Arial, sans-serif;
}
.hero-title {
  font-family: var(--font-display);
  font-weight: 650;
  font-synthesis: none;
}
```

Include at least one locally available or system fallback. If a webfont is used, self-host only when the license allows it, include the license file, and set `font-display: swap` with metrics that limit layout shift. Check contrast and text rendering at the real display size.

### 6. Audit before handoff

Run a local audit of declared font families when a codebase is available. Resolve single-level `var()` indirection first, since stacks are commonly declared once on `:root`; flag unresolved references instead of guessing:

```python
import re
from pathlib import Path

css = Path("styles.css").read_text(encoding="utf-8")
aliases = {
    "--" + m.group(1): m.group(2).strip()
    for m in re.finditer(r"--([\w-]+)\s*:\s*([^;}\n]+)", css)
}
families = re.findall(r"font-family\s*:\s*([^;]+);", css)
assert families, "no font-family declarations found"
for declaration in families:
    stack = declaration.strip()
    alias = re.fullmatch(r"var\(--([\w-]+)\)", stack)
    if alias:
        stack = aliases.get("--" + alias.group(1), stack)  # one level only
    names = [n.strip().strip("'\"") for n in stack.split(",")]
    assert len(names) >= 2, f"no fallback in: {declaration}"
    assert names[-1].lower() in {"serif", "sans-serif", "monospace", "system-ui", "cursive"}, \
        f"no generic fallback in: {declaration}"
print(f"{len(families)} declarations with fallbacks")
```

## Common Pitfalls / Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The logo site says verified, so the license is fine" | Identification and licensing are separate questions. |
| "It looks identical at 100px" | Compare discriminating glyphs at target size and weight; many superfamilies converge. |
| "Free font means free for client work" | Check the license clause for commercial and embedding rights. |
| "I'll skip fallbacks, the webfont will always load" | Network, blocked domains, and FOIT happen; fallback is required. |
| "It's only a logo, accessibility doesn't apply" | Logo lockups often contain wordmarks and adjacent text; contrast and legibility still matter. |

## Verification

- [ ] Candidate has a recorded evidence tier and source URL with retrieval date.
- [ ] At least three discriminating glyphs compared; tier marked in design note.
- [ ] License text checked for the exact intended uses; open substitute chosen if unverified.
- [ ] Font stack contains a generic fallback; local audit ran without assertion errors.
- [ ] Contrast, real-size rendering, and reduced-motion preview verified where relevant.
