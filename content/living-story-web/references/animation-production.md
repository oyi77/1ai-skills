# Animation production and feasibility

## Choose based on evidence

| Source available | Suitable approach | Limitation to resolve |
| --- | --- | --- |
| Layered character artwork | 2D skeleton plus mesh deformation | Joint overlap, pivots, alternate views |
| Rigged model and clips | 3D animation with illustrated treatment | Runtime licensing, skinning, shading and device budget |
| Dense aligned frames | Scroll-indexed image sequence | Memory, decoding, frame alignment and progressive loading |
| Single flat illustration | Limited depth and secondary motion | Cannot establish articulated turns or walking by itself |
| Sparse pose sheet | Storyboard or intentionally stepped comic | Insufficient intermediate movement for smooth animation |

Inspect actual tools and assets before choosing. Generation tools may produce concept art without producing a usable rig or coherent animation. Do not equate an alpha channel with clean separation: inspect compositing on both light and dark backgrounds.

## 2D rig requirements

Separate head, neck, hair sections, torso, pelvis, limbs, hands, accessories, and relevant clothing sections. Draw hidden overlap areas needed during rotation. Define pivots at anatomical or mechanical joints, parenting order, and masking/occlusion rules. Use alternate authored views for large turns; do not stretch a front view into a back view.

For object-led stories, define real hinges, constraints, assembly order, contact points, and material behavior. Avoid applying human motion heuristics blindly.

## Sequence requirements

Inspect identity consistency, proportions, baseline, lighting, framing, alpha edges, and action progression. Use enough authored intermediate frames for the intended motion; determine density from action speed and visible quality, not an arbitrary frame count. Avoid blending incompatible silhouettes into ghosts. Align camera changes separately from subject action where possible.

Estimate decoded memory as width × height × 4 × resident frame count, plus renderer overhead. Cap resident frames, decode upcoming content progressively, and keep a known valid frame while loading. Do not fetch every frame before the first useful render.

## Feasibility checkpoint

Record for each primary action:
- Actual source file and provenance/license.
- Required views, layers, or clips.
- Available production method and runtime.
- Missing work and concrete fallback.
- Proof clip or observed behavior.

Prototype the hardest visible action before authoring the entire world. If smooth motion cannot be produced, say so promptly. A reduced static accessibility path is required but is not a substitute for completing the requested animated path.
