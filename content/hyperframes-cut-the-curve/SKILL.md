---
name: hyperframes-cut-the-curve
description: "The transition technique catalog for HyperFrames videos — five velocity-matched SEAMS (zoom-through, inverse zoom-through, cut-the-curve, waterfall cut, rack-focus blur-cut) plus in-scene techniques (waterfall entry, nudge curve). Covers partial-travel velocity matching, Z scale-sign rule, size-scaled blur, the 10/65/25 slide ratio, and the 2-3 transition budget. Read before authoring any transition, text-beat handoff, or kinetic text entry."
domain: "content-creation"
tags:
  - hyperframes
  - transitions
  - animation
  - cut-the-curve
  - zoom-through
  - waterfall
  - rack-focus
  - velocity-matching
  - easing
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill creates a dynamic "cut the curve" animation — a curve being sliced along a moving line — as a HyperFrames composition. Use it for explainer moments where a literal cutting action makes a concept click. It renders a crisp, deterministic MP4 from the HTML composition.


# HyperFrames — Cut the Curve (Transition Catalog)

Five SEAM techniques, one principle: **cut at peak velocity, match direction and speed on both sides of the cut** — plus two in-scene techniques (arrivals, slides). This is the implementation reference; the motion law lives in `hyperframes-motion-doctrine`.

## When to Use

- User wants to add **transitions** between scenes
- User wants **text-beat handoffs** or **kinetic text entry**
- User wants **group repositioning** (nudge curve)
- User is authoring any multi-scene HyperFrames composition
- User wants to understand velocity-matched cuts

## When NOT to Use

- User wants a full video workflow (use `hyperframes-product-launch-video`)
- User wants motion doctrine/gateway rules (use `hyperframes-motion-doctrine`)
- User wants cursor-led action (use `hyperframes-oversized-cursor`)
- User wants seam render mechanics (use `hyperframes-seam-craft`)

## Catalog

| # | Technique | Scope | Axis | Use for |
|---|-----------|-------|------|---------|
| 1 | Zoom-Through | Within-scene text swap | Z, toward | progressing deeper into same thought |
| 2 | Inverse Zoom-Through | Arrival/payoff beat | Z, away | something bigger lands |
| 3 | Cut the Curve | Between scenes | X/Y | the default boundary |
## Workflow

### 1 · Pick the transition

Match the transition to the scope:
- Between scenes → Cut the Curve (default)
- Within-scene text swap → Zoom-Through
- Arrival/payoff → Inverse Zoom
- Text-to-text seam → Waterfall Cut
- Title cards → Waterfall Entry
- Group reposition → Nudge Curve

### 2 · Verify Z sign

On Z-axis transitions, the scale-velocity sign must match:
- Push (forward): growing exit → growing entry
- Pull (back): shrinking exit → shrinking entry

### 3 · Set blur values

- Text-scale subjects: **10px** peak blur
- Full-frame surfaces: **18-20px** peak blur

### 4 · Apply mirrored eases

- Exit: `power4.in`
- Entry: `power4.out`
- Same distance and duration on both sides

### 5 · Verify with seam-gate

```bash
node scripts/seam-gate.mjs verify --ledger ledger.json --project .
```

## Anti-Rationalization Table
| 6 | Waterfall Entry | In-scene ARRIVAL | Y, from below | title cards, segment openers |
| 7 | Nudge Curve | In-scene group slide | X/Y | repositioning a composed group |

## Z Direction is a Sign

| Z vector | Exit scale | Entry scale |
|----------|-----------|-------------|
| Push (forward) | growing 1 → 1.2 | growing 0.75 → 1 |
| Pull (back) | shrinking 1 → 0.8 | shrinking 1.25 → 1 |

**Banned mirrors:** receding exit → grow-from-small entry (the common violation), push exit → oversized retraction.

## Blur Logic

| Subject | Peak blur |
|---------|-----------|
| Text-scale (headline, word group) | **10px** |
| Full-frame surface | **18-20px** |

Same peak blur on both sides at the swap frame. Blur the WRAPPER, never children.

## 1. Zoom-Through (forward)

| Phase | Scale | Blur | Opacity | Ease | Duration |
|-------|-------|------|---------|------|----------|
| Exit | 1 → 1.2 | 0 → 10px | 1 → 0.15 | power3.in | 0.2s |
| Cut | in: 0.75 | 10px | out: 0 / in: 0.15 | — | — |
| Entry | 0.75 → 1 | 10 → 0px | 0.15 → 1 | expo.out | 0.5s |

## 3. Cut the Curve (default scene boundary)

**Partial travel:** ~12% of frame (≈230px at 1920) — never full off-screen moves.

| Direction | Exit | Entry start → end |
|-----------|------|-------------------|
| Leftward | x: 0 → −230 | x: +230 → 0 |
| Rightward | x: 0 → +230 | x: −230 → 0 |
| Upward | y: 0 → −230 | y: +230 → 0 |
| Downward | y: 0 → +230 | y: −230 → 0 |

Mechanics:
- **Mirrored eases:** exit `power4.in` + entry `power4.out`, same distance and duration
- **Fade trick:** exit opacity completes at ~25-30% of travel; entry ignites at ~0.35 opacity mid-path
- Exit 0.2-0.4s; entry ≥ exit

## 6. Waterfall Entry (in-scene arrival)

Staggered ARRIVAL cascade: elements whip in from below, each starting before the previous settles.

| Parameter | Anchor/heavy | Normal word | Light/punctuation |
|-----------|--------------|-------------|-------------------|
| Y offset | 60-80px | 40-50px | 30-48px |
| Duration | 0.16-0.20s | 0.13-0.16s | 0.10-0.13s |
| Overlap | 0-2f gap | 1f overlap | 1-2f overlap |

## 7. Nudge Curve (in-scene group slide)

Slow-fast-slow repositioning via three chained tweens:

| Phase | Ease | Distance | Time |
|-------|------|----------|------|
| 1 ramp-in | power3.in | ~10% | ~20% |
| 2 burst | none (linear) | ~65% | ~18% |
| 3 tail | power4.out | ~25% | ~62% |

The tail is ≥3× the ramp-in in TIME.

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll use full off-screen moves" | Partial travel (~12%) + early fade creates velocity |
| "I'll fade in place for arrivals" | Binary 0→1 via tl.set — fading fights the snap |
| "I'll use power4.inOut on both sides" | Mirrored power4.in / power4.out for velocity match |
| "I'll add 20px blur to text" | 10px text; 18-20px only full-frame |
| "I'll use one ease for the nudge" | Three-phase chain (ramp-in, burst, tail) required |

## Verification

- [ ] Only 2-3 transition types per film
- [ ] Z sign matched on both sides of cut
- [ ] Blur values correct for subject type
- [ ] Mirrored eases (power4.in / power4.out)
- [ ] Partial travel, not full off-screen
- [ ] Waterfall gaps shrink (×0.84 decay)
- [ ] Nudge tail ≥ 3× ramp-in time
