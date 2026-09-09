---
name: hyperframes-seam-craft
description: "Render-correctness doctrine for scene-to-scene seams in HyperFrames videos. Use when assembling the master timeline, when a white flash appears at a cut, when reasoning about transition opacity dips, or when verifying render-side mechanics of overlapping scene wrappers. Covers the opaque stage-ground white-flash guard, injector overlap mechanics, template placeholders, and the ping-pong track reassignment."
domain: "content-creation"
tags:
  - hyperframes
  - seams
  - transitions
  - render-correctness
  - white-flash
  - stage-ground
  - injector
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
---

# HyperFrames — Seam Craft

Render-correctness doctrine for scene-to-scene seams: the prerequisites and master-timeline mechanics that make any transition composite correctly, independent of which specific transition is chosen.

## When to Use

- User wants to **assemble the master timeline** / index.html
- User sees a **white flash at a cut** (especially on dark films)
- User wants to understand **transition opacity dips**
- User wants to verify **render-side mechanics** of overlapping scene wrappers
- User is working with **Tier-B-ready** transitions (transform/opacity/filter on clip wrappers)

## When NOT to Use
## Workflow

### 1 · Paint the stage ground

```css
#root { background: var(--canvas-deep, var(--canvas, #000)); }
```

### 2 · Verify no same-track overlap

At each break boundary, the injector reassigns clip `data-track-index` as a 0/1 ping-pong. Verify no two overlapping wrappers share a track.

### 3 · Apply template placeholders

Substitute `__OLD__`, `__NEW__`, `__T__`, `__DUR__`, `__DX__`, `__DY__` in each transition template.

### 4 · Verify with seam-gate

```bash
node scripts/seam-gate.mjs verify --ledger ledger.json --project .
```

## Anti-Rationalization Table
- User wants the motion law (use `hyperframes-motion-doctrine`)
- User wants a full video workflow (use `hyperframes-product-launch-video`)

## Stage Ground Prerequisite (White-Flash Guard)

Several templates open a window where the two wrappers' summed opacity < 1 (the cut-the-curve mid-window cut, zoom-through's 0.15 floor, plain crossfade's power-curve dip). Whatever is BEHIND the wrappers shows through during that window. If `#root` has no opaque background, the renderer composites the dip over its default **white** page → a white flash at every seam.

**The assembler must paint the stage:**

```css
#root { background: var(--canvas-deep, var(--canvas, #000)); }
```

## How the Injector Applies a Transition

At a `break` boundary between scene i (from) and scene i+1 (to), the injector:

1. Extends `#el-<from>` wrapper `data-duration` by `duration_s` (holds its final frame)
2. Pulls `#el-<to>` wrapper `data-start` earlier by `duration_s` (creates the overlap window)
3. Reassigns **all** clip `data-track-index` as a 0/1 ping-pong so the two overlapping wrappers never share a track
4. Stamps the `gsap_template` into `window.__timelines["main"]` at `T = overlap-start`

## Template Placeholders

| Token | Meaning |
|-------|---------|
| `__OLD__` | `"#el-<from>"` — outgoing clip wrapper selector |
| `__NEW__` | `"#el-<to>"` — incoming clip wrapper selector |
| `__T__` | overlap-start time in seconds |
| `__DUR__` | `duration_s` for this boundary |
| `__DX__` | horizontal travel: `-1920` (LEFT) / `1920` (RIGHT) |
| `__DY__` | vertical travel: `-1080` (UP) / `1080` (DOWN) |

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll leave #root transparent" | White flash at every seam — paint the stage |
| "I'll let both wrappers share a track" | Same-track overlap is illegal — ping-pong reassignment |
| "I'll start the transition at the break" | Transition starts at overlap-start, not the break |
| "I'll use a unique transition per scene" | Budget is 2-3 per film — repetition creates cohesion |

## Verification

- [ ] `#root` has opaque background
- [ ] No same-track overlap between wrappers
- [ ] Template placeholders substituted correctly
- [ ] `seam-gate.mjs verify` passes with 0 fail
- [ ] No white flashes on 3+ sampled frames at cuts
