---
name: hyperframes-oversized-cursor
description: "House-style oversized macOS cursor technique for HyperFrames videos. Use when a scene involves cursors, pointer-led action, kicking off a UI scene, igniting a morph/transition/typing with a click, or when a scene reads as static/dead/stale and needs motion to carry the eye. Covers cursor size/look, off-screen entry law, tip-targeting, click-ignition, and cross-scene handoff."
domain: "content-creation"
tags:
  - hyperframes
  - cursor
  - motion
  - click-ignition
  - eye-carrier
  - ui-animation
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
license: Apache-2.0
---
## Overview

This skill creates the oversized animated cursor effect popular in product demo and walkthrough videos, as a HyperFrames composition. Use it to draw attention to exact click points and drag gestures in a UI demo. It renders the annotated MP4 from the HTML timeline.


# HyperFrames — Oversized Cursor

A deliberately oversized macOS-style pointer that travels the frame as a visible protagonist: enters from off-screen, walks the eye to the next point of interest, clicks to cause the next thing that happens, and leaves.

## When to Use

- User wants a **cursor** in the video (demo, tutorial, UI walkthrough)
- User wants to **kick off a UI scene** with a cursor click
- User wants to **ignite a morph/transition/typing** with a click
- User wants to **add motion to a static scene** (the cursor carries the eye)
- User wants a **cross-scene handoff** via cursor

## When NOT to Use

- User wants a full video workflow (use `hyperframes-product-launch-video`)
- User wants transitions without a cursor (use `hyperframes-cut-the-curve`)
- User wants a real hand/finger (not stylized cursor)

## Why It Exists

Big cursor movement is one of the cheapest high-yield motion sources: one element, transform-only tweens, and it (1) brings the eye across the screen, (2) gives causal ignition to morphs/transitions, (3) segments the eye out of a stale state. Bigger is better — an actual-size cursor disappears at video scale.

## Size & Look

- **Full-frame scenes: `7cqw`** (≈134px at 1920). In-mock / small-frame: `4.6-5.5cqw`. Never smaller.
## Workflow

### 1 · Size and style the cursor

```css
#root .cursor {
  position: absolute;
  left: 48%;
  top: 115%;
  width: 7cqw;
  height: 7cqw;
  z-index: 20;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
  pointer-events: none;
  will-change: transform;
}
```

### 2 · Animate entry from off-screen

```javascript
tl.fromTo(
  cursor,
  { left: "48.6%", top: "115%" },
  { left: "48.6%", top: "55%", duration: 0.85, ease: "power3.out", immediateRender: false },
  0.25,
);
```

### 3 · Add click ignition

```javascript
tl.to(cursor, { scale: 0.84, duration: 0.1, ease: "power2.in", transformOrigin: "21% 14%" }, t);
tl.to(cursor, { scale: 1, duration: 0.22, ease: "power2.out", transformOrigin: "21% 14%" }, t + 0.1);
```

### 4 · Exit physically

Either leave the frame or hand off via cut-the-curve to the next scene.

## Anti-Rationalization Table

```css
#root .cursor {
  position: absolute;
  left: 48%;
  top: 115%; /* off-screen below — the resting pose IS off-screen */
  width: 7cqw;
  height: 7cqw;
  z-index: 20;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
  pointer-events: none;
  will-change: transform;
}
```

## Entry Law — Physical, Never Revealed

The cursor **always enters from off-screen** (canonical: from below, `top:115-120%`) and travels to its first target in one decelerating glide. It must feel like it entered the room. Never opacity-fade it in at a resting position, never mask-reveal it.

- Default path: straight up the y-axis to the target
- `duration: 0.4-0.92s`, `ease: power3.out`, `immediateRender: false` on the fromTo

```javascript
tl.fromTo(
  cursor,
  { left: "48.6%", top: "115%" },
  { left: "48.6%", top: "55%", duration: 0.85, ease: "power3.out", immediateRender: false },
  0.25,
);
```

## Tip-Targeting & the Click Tap

The hot-spot is the arrow TIP, not the box center. Land the tip on the target's center, pivot all press scaling on the tip: `transformOrigin: '21% 14%'`.

Click = asymmetric compress/expand (1:2 ratio reads as a real tap):

```javascript
tl.to(cursor, { scale: 0.84, duration: 0.1, ease: "power2.in", transformOrigin: "21% 14%" }, t);
tl.to(cursor, { scale: 1, duration: 0.22, ease: "power2.out", transformOrigin: "21% 14%" }, t + 0.1);
```

## The Click Ignites the Next Beat

Never let a morph, typing run, window transform, or scene-defining animation simply start. Park the cursor on the trigger and let the click cause it, same-frame:

- click → menu/submenu cascade, toggle flip
- click → typing kickoff into an input
- click → composer morph-down / window shrink
- click → logo ignition / flight launch

During long beats it doesn't own (typing, narration), the cursor drifts aside (0.5-0.9s, `power2.out`) — never sits frozen, never wobbles idly.

## Exit Law & Cross-Scene Handoff

Two sanctioned exits — both physical, never an opacity fade in place:

1. **Leave the frame:** accelerate off the nearest edge with `power2.in` (`left:'118%'`, `left:'-12%'`, or `top:'116%'`), 0.5-0.7s.
2. **Cut-the-curve handoff:** in the final ~0.3s before a hard cut, the cursor starts accelerating toward the NEXT scene's first click point, covering the first ~1/3 of that path; the next composition sets the cursor at the handoff pose and continues at matched velocity.

```javascript
// Scene A, last 0.3s — start the journey:
tl.to(cursor, { left: "40.7%", top: "63.7%", duration: 0.3, ease: "power2.in" }, CUT - 0.3);
// Scene B, t=0 — finish it at matched velocity:
gsap.set(cursorB, { left: "40.7%", top: "63.7%" });
tl.to(cursorB, { left: "22%", top: "45%", duration: 0.6, ease: "power2.out" }, 0);
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll fade the cursor in at its first position" | Physical off-screen entry — never opacity reveal |
| "I'll use a normal-sized cursor" | 7cqw minimum — actual-size disappears at video scale |
| "I'll let the animation just start" | Click ignites the beat — same-frame causation |
| "I'll leave the cursor frozen during typing" | Drift aside — never frozen, never idle wobble |
| "I'll fade the cursor out at the end" | Physical exit (off-frame or cut-the-curve handoff) |
| "I'll center the cursor box on the target" | Tip-targeting — the hot-spot is the arrow tip |

## Verification

- [ ] ≥ 7cqw full-frame (4.6-5.5cqw inside a mock) — when unsure, bigger
- [ ] Enters from off-screen on one continuous vector (no fade/mask reveal)
- [ ] Tip lands on the target center; press pivots on `transformOrigin: '21% 14%'`
- [ ] Every click causes something, same-frame
- [ ] Drifts aside during beats it doesn't own; zero idle wobble
- [ ] Exits physically (off-frame or cut-the-curve handoff) — no fade-in-place
