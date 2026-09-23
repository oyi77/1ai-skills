# Validation and evidence

Set explicit budgets appropriate to the actual project and devices. Distinguish measured results from targets. Reuse existing checks; add tests only for meaningful animation logic or regression risks.

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

Report tests not run as unverified, never passed. For performance, state the device/profile, method, observations and remaining uncertainty; do not claim universal 60 FPS from one desktop run.

## Completion report

Briefly state what changed and how it serves the project. Link the authorized result and evidence when available. Identify unfinished primary animation, asset licensing questions, and unverified devices explicitly. Include editing locations for links, scene timing, copy and assets. Do not call the result production-ready until the required actions and critical functionality are complete and sufficiently verified.
