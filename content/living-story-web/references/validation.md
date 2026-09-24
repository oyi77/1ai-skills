# Validation and evidence

Set explicit budgets appropriate to the actual project and devices. Distinguish measured results from targets. Reuse existing checks; add tests only for meaningful animation logic or regression risks.

## Device matrix

Verify on a matrix that covers real usage, not just the author's desktop.

| Profile | Representative | What to check |
| --- | --- | --- |
| Desktop, large viewport | 1440p+ | Composition, texture memory, camera |
| Laptop, small viewport | 1280×720 | Crop, panel legibility |
| Tablet portrait | 768×1024 | Touch nav, no hover-only content |
| Mobile, mid-range | 390×844 | Cropped hands/faces, horizontal overflow, frame budget |
| Mobile, low-end | older Android, 4 GB | Degraded path, memory cap, 30 fps acceptability |
| Reduced motion | any, OS preference | Document-flow narrative, live toggle |

Do not claim mobile correctness from a desktop emulation that resizes the window; inspect the actual viewport layout and touch behavior where the toolchain permits.

## Required observations

| Check | Evidence | Failure examples |
| --- | --- | --- |
| Project fit | Opening view and primary flow | Industry/brand copied from an unrelated project |
| Primary action | Short real playback or frame progression | Sliding cutout, disconnected limbs, foot skating |
| Timeline | Forward, reverse, stop and large jump | Different state at the same progress, flicker |
| Pointer/touch | Pointer move/leave and touch navigation | Pointer fights scroll, hover-only content |
| Mobile | Actual target viewport inspection | Cropped hands, covered face, horizontal overflow |
| Reduced motion | Initial preference and live toggle | Frozen intermediate scene, hidden copy, excessive empty space |
| Failure fallback | Renderer/assets unavailable where practical | Blank screen or inaccessible CTA |
| Existing functionality | Relevant critical flows | Broken forms, routes, auth, or integrations |
| Links | Config and rendered destinations | Duplicated mismatching URLs, fake placeholder links |
| Performance | Actual tooling on named device/profile | Unbounded frame memory, background work, loading gaps |

Use short recordings for forward/reverse behavior where supported. If recording is unavailable, inspect successive states and timing through available authorized tools; label recordings as unavailable rather than fabricating them. Screenshots alone demonstrate composition, not smoothness.

## Performance measurement

Report the device/profile, method, observations, and remaining uncertainty. Do not claim universal 60 FPS from one desktop run.

- **Frame timing** — Chrome DevTools Performance panel or the browser's frame inspector; a long task or >16 ms frames on target device is the signal.
- **Layout shift** — Lighthouse or the field CLS metric; pinned sections must not shift surrounding content.
- **LCP** — measure with and without the story layer to prove the experience does not delay the largest contentful paint.
- **Memory** — Chrome Task Manager or `performance.memory` (Chromium-only, coarse); watch for texture growth during long scrolls.
- **Idle cost** — confirm rAF and network go quiet when the tab is hidden or the section is offscreen.

For a reproducible check, add an animation-logic test only where there is meaningful logic: e.g. `progress → scene interval` mapping, `progress → frame index` clamping, or pose interpolation at boundaries. Do not test the browser's compositor.

## Completion report

Briefly state what changed and how it serves the project. Link the authorized result and evidence when available. Identify unfinished primary animation, asset licensing questions, and unverified devices explicitly. Include editing locations for links, scene timing, copy and assets. Do not call the result production-ready until the required actions and critical functionality are complete and sufficiently verified.
