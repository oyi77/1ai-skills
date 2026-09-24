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

## Tooling by approach

Pick the tool that produces a runtime-ready artifact; generation tools that output only static concept art do not qualify.

| Approach | Representative tools | Runtime artifact | Watch for |
| --- | --- | --- | --- |
| 2D skeleton rig | Rive, Spine, DragonBones, Adobe Character Animator | Exported rig + keyframes (JSON/binary) with a runtime | Export size, joint limits, mesh-deformation artifacts at extremes |
| Frame sequence | After Effects / Blender render → ffmpeg | Ordered image strip (WebP/AVIF/PNG) or sprite sheet | Frame count × resolution memory, progressive decode |
| 3D with illustrated shading | Blender → glTF/glb → three.js | Skinned mesh + clip + toon/cel material | Skinning weight count, draw calls, DRACO/meshopt size |
| SVG/CSS illustration | Inline SVG, CSS transforms | DOM or `<use>`-driven bones | Pivot placement, no true mesh deformation |

For most living-story sites the decision is: **a rig with a runtime** (small file, smooth, needs authored joints) versus **a frame sequence** (large file, works with any pre-rendered action, needs progressive loading). A sparse pose sheet only ever yields a stepped comic — acceptable when stepped is the intent, never a substitute for smooth motion.

## Frame sequence production

Pre-render an action to an ordered strip, then normalize it for scroll indexing.

```bash
# Extract a rendered clip to a numbered WebP strip, 2x retina, ~72% quality.
ffmpeg -i render.mov -vf "scale=-2:1080" -q:v 72 frame-%04d.webp
```

Production checklist for the strip:

- **Identity consistency** — same proportions, baseline, lighting, framing, and alpha edges across all frames.
- **Frame density** — enough intermediates for the action speed; a 1s walk at 24 fps is 24 frames, not 8.
- **Format** — WebP (lossy + alpha, good browser support) or AVIF (smaller, newer) over PNG for photographic/illustrated frames; PNG only when lossless edges are mandatory.
- **Memory** — decoded cost is `width × height × 4 × residentFrames` bytes plus renderer overhead. A 1920×1080 RGBA frame is ~8.3 MB decoded; hold a small window around the current index, never the whole strip.
- **Progressive decode** — preload frames near the current index; keep a known valid frame visible while the next decodes. Do not fetch every frame before the first useful render.

## 2D rig requirements

Separate head, neck, hair sections, torso, pelvis, limbs, hands, accessories, and relevant clothing sections. Draw hidden overlap areas needed during rotation. Define pivots at anatomical or mechanical joints, parenting order, and masking/occlusion rules. Use alternate authored views for large turns; do not stretch a front view into a back view.

For object-led stories, define real hinges, constraints, assembly order, contact points, and material behavior. Avoid applying human motion heuristics blindly.

## 3D rig requirements

For a rigged 3D model with an illustrated treatment, confirm the pipeline end to end before committing:

- **Skinning budget** — 4 bone weights per vertex is the common real-time cap; more joints raise shader and upload cost.
- **Clip size** — bake only the clips the story uses; strip unused keyframes and channels.
- **Shading** — a toon/cel material keeps the illustrated look; a full PBR material costs more and drifts toward photoreal.
- **Compression** — ship glTF with meshopt (glb) or DRACO compression; verify the decoder is wired before counting on the smaller size.
- **Fallback** — the reduced-motion path still needs a static composition of the same content.

## Feasibility checkpoint

Record for each primary action:

- Actual source file and provenance/license.
- Required views, layers, or clips.
- Available production method and runtime.
- Missing work and concrete fallback.
- Proof clip or observed behavior.

Prototype the hardest visible action before authoring the entire world. If smooth motion cannot be produced, say so promptly. A reduced static accessibility path is required but is not a substitute for completing the requested animated path.
