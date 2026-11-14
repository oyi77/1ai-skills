---
name: minimalist-design
description: Use when applying Dieter Rams' "less but better" approach to product and UI design — stripping a design down to its essentials using the 10 Principles of Good Design, with a concrete audit checklist.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- design
- minimalism
- dieter-rams
- product-design
- ui
- functional-aesthetics
- sustainability
version: 1.0.0
category: content
---

# Minimalist Design

Apply Dieter Rams' approach to timeless product design: **less, but better**.

## When to Use

**Trigger phrases:**
- "minimalist design" · "clean UI" · "reduce visual noise"
- "Dieter Rams" · "less is more" · "stripped down"
- "declutter this interface" · "make it calmer"

**Use cases:**
- Auditing a cluttered product UI against Rams' principles
- Designing a new product where restraint is the differentiator
- Deciding what to cut when a design feels busy

## When NOT to Use

- Dense data displays (trading terminals, dashboards) — use `dataviz` for density done well
- Marketing landing pages where visual energy is the goal
- Children's products and playful brands where maximalism is intentional
- Anything where you'd remove an accessibility aid (labels, contrast) to look "clean"

## The 10 Principles of Good Design

Rams' own list. Use as the audit axis.

1. **Is innovative** — does not look new for its own sake
2. **Makes a product useful** — emphasizes usefulness, ignores everything that detracts
3. **Is aesthetic** — the quality of execution affects how we perceive usefulness
4. **Makes a product understandable** — self-explanatory; clarifies structure
5. **Is unobtrusive** — neutral, restrained; leaves room for the user's self-expression
6. **Is honest** — does not make a product appear more valuable than it is
7. **Is long-lasting** — avoids fashion; remains relevant for years
8. **Is thorough down to the last detail** — nothing arbitrary; care shows respect for the user
9. **Is environmentally friendly** — conserves resources, minimizes visual and physical pollution
10. **Is as little design as possible** — less, but better; concentrates on the essential

## Workflow

### 1. Inventory every element

List every visible element on the screen/product: buttons, labels, dividers, colors, icons, motion, sounds, states. No judgement yet — just the census.

### 2. Score each element against three questions

For each element, answer:

- **Does removing it break a task?** If no, it's a candidate.
- **Does it earn its attention cost?** Every element competes for the same finite attention.
- **Is it honest?** Does it represent real function, or is it decoration pretending to be function?

### 3. Remove in passes, not all at once

Cut the obvious candidates first, then re-render and look again. Removal is iterative — you can't see what else is noise until the loudest noise is gone.

### 4. Apply the reduction hierarchy

When two elements compete, remove the lower-priority one:

1. Motion and decoration first
2. Redundant labels and dividers
3. Secondary actions and states
4. Color variation that carries no meaning
5. Finally: elements required for the core task (rarely removable)

### 5. Verify nothing essential was lost

Run the core task end-to-end. If any step became harder, you cut too deep — restore the specific element, not the whole pass.

## Concrete Audit Checklist

Work through these on any design:

- [ ] **One primary action** per screen (everything else is secondary or tertiary)
- [ ] **Color count ≤ 3** functional colors (+ neutrals); every color earns its place
- [ ] **No decorative elements** that don't carry function (gradients, drop shadows, borders, icons)
- [ ] **Every icon has a label**, or is a universally-recognized glyph (X, ←, →)
- [ ] **Type scale ≤ 4 sizes** (e.g., 32/22/16/13)
- [ ] **No filler copy** — every sentence conveys information the user needs
- [ ] **Empty states** are informative, not just "Nothing here"
- [ ] **Contrast ratios** meet WCAG AA (4.5:1 body, 3:1 large)
- [ ] **Motion** ≤ 200 ms, only for state change — no decorative animation
- [ ] **Would this survive 5 years?** No trend-chasing (glassmorphism, neumorphism, etc.)

## Example: Reduction in practice

**Before (typical SaaS card):**
Header + subtitle + 3-line description + icon + "Learn more →" + "Get started" button + "Or see pricing" link + divider + tag chip + date.

**After (Rams pass):**
Title + one-line description + "Get started" button.

Cut: subtitle (redundant with title), description (move to detail view), icon (decorative), "Learn more" (low-value), pricing link (in nav), divider (whitespace does the job), tag chip (metadata, not primary), date (metadata).

The card now has one job and one action. Nothing to parse.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "But users might want that feature" | They might — in a detail view. Default to showing the one thing that matters most. |
| "Whitespace wastes space" | Whitespace is the cheapest way to create hierarchy. It's not waste. |
| "Removing X will confuse users" | Test it. Most "confusion" fears are wrong; measure task completion, not opinions. |
| "It's not minimal if it has color" | Rams used color sparingly and deliberately. Restraint ≠ grayscale. |
| "Clean means fewer features" | Minimalism is about what you *show*, not what the product *does*. |

## Verification

- [ ] One primary action per screen
- [ ] ≤3 functional colors, ≤4 type sizes
- [ ] No decorative elements that don't carry function
- [ ] Every icon labeled or universally recognized
- [ ] WCAG AA contrast maintained
- [ ] Core task completable end-to-end after every cut
- [ ] Survives the "5-year test" — no trend-chasing
