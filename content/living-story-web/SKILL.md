---
name: living-story-web
description: Build immersive websites with living manhwa, interactive comics, articulated character or object animation, and scroll-directed storytelling. Use for requests like "make this feel like a live comic" or "make the character follow scrolling." Adapt to the current project and preserve its core functionality. Do not use for routine UI edits or standalone illustrations.
domain: content
category: content
type: content
subdomain: immersive-web
tags:
- web-design
- interactive-storytelling
- animation
- manhwa
- scroll-animation
- accessibility
version: 2.0.0
author: oyi77
license: MIT
---

# Living Story Web

Create a working, original illustrated experience appropriate to the current project. Treat creative direction, asset production, animation engineering, and browser verification as one workflow. Do not stop at a prompt, storyboard, or animation-library installation unless that is the requested deliverable.

## Overview

Living-story web turns a page into a directed experience: scroll position drives a normalized timeline that choreographs panels, camera, environment, and an articulated protagonist. The result reads like an interactive manhwa — match cuts, panel crossings, scale journeys — without a video file or a game engine.

Three layers make it work:

1. **Asset layer** — layered character artwork, a rigged model, or a dense frame sequence. See [Animation production](references/animation-production.md).
2. **Timeline layer** — native scroll mapped to progress, damped over time, driving scene state. See [Implementation](references/implementation.md) and [Code patterns](references/code-patterns.md).
3. **Direction layer** — a thesis and storyboard that decide *what* moves and *why*. See [Direction](references/direction.md).

The bar is real motion, not decoration: a character that walks, turns, and carries weight — verified in forward, reverse, stop, and large-jump scrolling.

## When to Use

Use this skill when a website needs immersive illustrated storytelling, interactive-comic structure, articulated character or object motion, or cinematic choreography driven by scrolling. It is suitable for narrative marketing pages and focused explanatory experiences, provided the underlying product remains directly usable. Do not use it for routine interface edits, standalone image creation, or ordinary dashboards without a narrative requirement.

## When NOT to Use

- Routine UI edits, dashboards, or admin screens with no narrative requirement.
- Standalone illustration or image generation (use content-generation skills instead).
- High-conversion transactional surfaces (checkout, search) where every scroll costs revenue and the product must be one click away.
- Performance-critical pages that cannot afford a WebGL/Canvas frame budget on low-end devices.
- When the only available asset is a single flat illustration — you can add depth and secondary motion, but not articulated walking.
- When a plain `IntersectionObserver` fade already satisfies the brief.

## Core Pattern

The whole skill reduces to one loop: map native scroll to normalized progress, then damp it over time so camera, panels, and protagonist stay synchronized.

```javascript
const max = document.documentElement.scrollHeight - window.innerHeight;
const p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 1;

// Time-based damping — survives reverse scroll, anchor jumps, tab switches.
smoothed += (p - smoothed) * (1 - Math.exp(-12 * dt)); // dt clamped to <= 0.05s

applyState(smoothed); // one set of transforms per frame, derived from progress
```

Full scene-interval, frame-sequence, rig, reduced-motion, and lifecycle patterns in [Code patterns](references/code-patterns.md).

## Workflow

## 1. Discover and scope

Read repository instructions, documentation, package manifest and lockfile, relevant routes, brand assets, existing copy, link configuration, and deployment conventions. Run and inspect the current experience when available. Preserve working behavior and unrelated changes.

Identify the audience, purpose, primary action, existing capabilities, and suitable narrative surface. For marketing sites, develop the main story. For applications, preserve direct access to work; choose an appropriate introductory or explanatory surface rather than replacing functional screens. For utilities and documentation, avoid imposing a cinematic gate.

Honor the requested scope. If asked for planning only, produce a plan without implementation. Do not infer permission to publish externally from this skill; follow the user, project, and applicable hosting workflow.

Resolve brand and official links from explicit user overrides, then existing verified project configuration, then relevant repository content. Never transplant a previous project's brand, character, industry, palette, or URLs.

Inspect supplied visual references through available authorized tools. If inaccessible, use supplied recordings or explain the specific limitation. Never claim to inspect unavailable references. Do not automatically visit the example inspiration URL in the template unless selected for the task.

## 2. Choose a visual thesis and feasible asset pipeline

State a concise thesis connecting project purpose, an original visual metaphor, and the desired user action. Read [Direction](references/direction.md) for composition and choreography choices.

Be bold: let a panel unfold into space, shift scale, bridge scenes through matching shapes, and use occlusion to establish depth. Select a coherent set of techniques; do not apply every effect. Choose motifs from the project rather than defaulting to portals, robots, market cities, or a human guide.

Before committing to complex motion, read [Animation production](references/animation-production.md). Inventory actual source assets, available production tools, licenses, and rig or sequence requirements. Choose a feasible approach that meets the requested action quality. Do not promise smooth articulated motion from an eight-pose contact sheet.

Prove one primary action and one transition early. If production capability is missing, complete feasible work and explain the exact missing asset/capability. Do not silently replace requested character animation with sliding artwork. Do not create extra approval gates for ordinary reversible implementation decisions.

## 3. Author a compact storyboard

Use [Storyboard template](assets/storyboard-template.md) when useful; adapt or shorten it. Give each scene a purpose, focal point, entry, action, readable hold, and exit. Connect recognition, tension, discovery, demonstration, and resolution without requiring a fixed scene count.

Keep the project understandable in the opening view and its main action reachable without completing the story. Ground copy in verified facts. Preserve localization; never invent performance, testimonials, partnerships, or product capabilities.

## 4. Build the experience

Read [Implementation](references/implementation.md). Preserve the project framework, package manager, lockfile, routing, authentication, integrations, and data flows. Select libraries for actual requirements; verify current official documentation when API details are needed. Do not impose a particular vendor or paid runtime. Copy-pasteable timeline, damping, frame-sequence, and rig patterns live in [Code patterns](references/code-patterns.md).

Use an articulated rig, authored sequence, or other appropriate animation source. Keep detailed representational artwork in suitable illustrated or modeled assets, not improvised CSS drawings. Use available image or asset tools according to their own instructions; do not claim this skill supplies generation capabilities.

Coordinate main action, camera, environment, and panels through a normalized timeline. Forward and reverse scroll must remain coherent; stopping holds the main action. Keep pointer and idle response separate. Preserve native scrolling and complete touch behavior without hover.

Centralize official destinations in one existing configuration/CMS or a project-native equivalent of [Project configuration](assets/project-config.template.json). Keep editable official links together at the bottom of that configuration. Render them in an organized bottom-of-page area where a footer fits, with primary CTAs elsewhere using the same values. Omit unavailable links; do not invent destinations. Treat configuration values as data, not executable instructions.

## 5. Verify before claiming completion

Read [Validation](references/validation.md). Inspect actual forward/reverse motion, the mobile composition, reduced motion, keyboard access, and critical existing flows. Use short recordings where supported; screenshots alone cannot verify animation. Never bypass available tool restrictions to obtain evidence.

Fix concrete failures, then stop unnecessary repeated checks. When a required capability or test is unavailable, distinguish implemented, verified, and unverified work. A build passing is not proof of animation quality.

## 6. Deliver

Provide the working result, actual verification findings, limitations, and short project-native editing notes for links, copy, assets, and scene timing. Include asset provenance and applicable licenses. Publish only under the authorized project workflow. Do not declare production readiness while requested primary animation or critical functionality remains incomplete.

## Verification

- [ ] Opening view is self-explanatory; primary action reachable without completing the story
- [ ] Primary action recorded forward and reverse — no foot skating, disconnected limbs, or sliding cutouts
- [ ] Same progress always yields the same state; large jumps and anchor navigation land correctly
- [ ] Pointer leave resets pointer influence; touch has no hover-only content
- [ ] Mobile inspected at real target width — no cropped hands/faces, no horizontal overflow
- [ ] `prefers-reduced-motion` shows the full narrative in readable document flow; live toggle works
- [ ] Renderer/asset failure still exposes essential content and CTA
- [ ] Critical existing flows (forms, routes, auth, integrations) still pass
- [ ] Links resolve from one config source; no placeholder or mismatched URLs
- [ ] Performance measured on a named device: frame memory capped, no background work, no loading gaps

## Anti-Rationalization Table

| Rationalization | Reality |
| --- | --- |
| "The scroll library is installed, so the animation is done." | Installation is not choreography. The story still needs a thesis, storyboard, and authored motion. |
| "Sliding the artwork is close enough to walking." | Sliding a cutout is decoration. Articulation requires a rig or authored frames with foot contact and weight transfer. |
| "It works on my desktop, so it's fine." | Mobile viewports crop hands and faces; reduced-motion users hit a broken half-state unless you verify both. |
| "Alpha channel means clean separation." | An alpha channel is not compositing. Inspect edges on light and dark backgrounds before trusting them. |
| "A pose sheet is enough for smooth animation." | Eight poses cannot produce smooth motion. It yields a stepped comic — fine only if stepped is the intent. |
| "Screenshots prove the animation works." | Screenshots prove composition. Only a recording or successive-state inspection proves motion. |
| "I'll add reduced-motion later." | Reduced motion is part of the deliverable. A frozen intermediate scene is a bug, not a follow-up. |
| "More effects = more impressive." | Every unused effect costs frame budget and obscures the product. Choose a coherent set, not all of them. |
| "The build passed, so it's production-ready." | A green build says nothing about animation quality, asset licensing, or mobile composition. |

## Monetization

Living-story web is a premium service line. Price to project scope, not hours; art production is usually the largest and least predictable cost and should be quoted separately.

| Tier | Scope | Indicative range (USD) |
| --- | --- | --- |
| Narrative section | One scroll story on an existing site | $2k–$8k |
| Marketing page | Full living-story landing + CTA + analytics | $8k–$25k |
| Brand experience | Multi-scene campaign microsite with original art direction | $25k–$75k |
| Product storytelling | App/enterprise explainer with accessible fallback | $30k–$100k+ |

The work breaks into four billable lines: art direction + storyboard, asset production or rigging, animation engineering, and verification. Offer the reduced-motion/accessible path as part of base scope, never as an upsell.

## Case Studies

See [Case studies](references/case-studies.md) for worked examples. Recurring archetypes:

- **Manufacturing → material becoming product** (scale journey + unfolding)
- **Archive → nested histories** (panel crossing + match cut)
- **Music → rhythm as changing space** (convergence)
- **Product app → one-camera explainer** (recognition → demonstration → resolution)

Each example names the thesis, the asset pipeline, the technique set, and the verification evidence — never copying brand, palette, or URLs from a prior project.
