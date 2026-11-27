---
name: r3f-scene-stack
description: Use when building interactive React Three Fiber scenes that need rigid-body physics, cinematic postprocessing, GPU particles, or live parameter tuning — library boundaries, Suspense setup, collider choices, effect budgets, and runtime knobs. Use for 3D product demos and interactive scenes.
domain: content
category: content
subdomain: 3d-web
tags:
- threejs
- react-three-fiber
- rapier
- postprocessing
- particles
- tweakpane
- webgl
version: 1.0.0
author: oyi77
license: MIT
triggers:
- "r3f physics"
- "react three scene with physics"
- "3d product demo"
- "bloom depth of field three"
- "particle effects three.js"
---

# R3F Scene Stack

Compose four libraries around one React Three Fiber canvas without turning the scene into a dependency soup: `@react-three/rapier` for physics, `@react-three/postprocessing` for cinematic effects, `three.quarks` (or `quarks.r3f`) for particles, and Tweakpane for live tuning. Library APIs move fast — verify against the installed version before writing code.

## Overview

Each library owns one concern and one boundary. Physics owns transforms of rigid bodies; never animate a physics-controlled object directly with React props. Postprocessing owns the full-frame pass chain; it goes inside the canvas after the scene. Particles own their own buffer and renderer; do not manually mutate their geometry in a React render loop. Tweakpane is a development aid: keep it out of production bundles behind an explicit flag.

For video output or frame-driven animation, this is the wrong tool — use [remotion](../video/remotion/SKILL.md) or [audio-reactive-animation](../audio-reactive-animation/SKILL.md). For UI-level motion, use [motion-dev](../motion-dev/SKILL.md).

## When to Use

- Interactive 3D product views where objects fall, collide, or respond to drag.
- Cinematic WebGL scenes with bloom, depth of field, or vignette.
- GPU particle effects that need a declarative React wrapper.
- Tuning scene constants at runtime before freezing them into code.

## When NOT to Use

- Static 3D model display with no simulation — plain `@react-three/fiber` + drei is enough.
- Deterministic offscreen video rendering — use a frame-driven engine.
- Low-end targets where postprocessing or WASM physics blows the performance budget; verify with profiling before committing to the stack.

## Workflow

### 1. Check versions and package contracts

Verify what is actually installed (`npm ls @react-three/fiber @react-three/rapier @react-three/postprocessing three.quarks tweakpane`) and read that version's README/types. Do not assume examples from a newer major apply to the installed version. Install only the packages the scene needs:

```bash
npm install three @react-three/fiber @react-three/drei @react-three/rapier @react-three/postprocessing
```

`@react-three/rapier` initializes WASM lazily: `<Physics>` must be inside `<Suspense>`. Missing that wrapper is the most common "blank scene" failure.

### 2. Build physics first

```tsx
import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { Physics, RigidBody, CuboidCollider } from "@react-three/rapier";

function Scene() {
  return (
    <Canvas>
      <Suspense fallback={null}>
        <Physics gravity={[0, -9.81, 0]} timeStep={1 / 60}>
          <RigidBody colliders="hull" restitution={0.2}>
            <mesh><boxGeometry args={[1, 1, 1]} /></mesh>
          </RigidBody>
          <RigidBody type="fixed">
            <CuboidCollider args={[5, 0.1, 5]} position={[0, -2, 0]} />
          </RigidBody>
        </Physics>
      </Suspense>
    </Canvas>
  );
}
```

Choose collider strategy deliberately: auto colliders from meshes are convenient for simple shapes, `colliders="hull"` for convex complexity, and explicit `CuboidCollider`/`BallCollider` for stable, predictable bodies. Set `debug` on `<Physics>` while developing to see collider geometry; remove it before shipping. Keep the fixed `timeStep` unless you have a measured reason to vary it.

### 3. Add postprocessing inside the canvas

```tsx
import { EffectComposer, Bloom, DepthOfField } from "@react-three/postprocessing";

<EffectComposer>
  <Bloom luminanceThreshold={0.9} luminanceSmoothing={0.2} mipmapBlur />
  <DepthOfField focusDistance={0.02} focalLength={0.05} bokehScale={2} />
</EffectComposer>
```

Effects are a budget, not a checklist. Add one, measure frame time, then add the next. Bloom on every surface destroys contrast; a depth-of-field pass on a scene with no depth separation just blurs everything. Keep the composer a sibling of scene content inside `<Canvas>`, never outside it.

### 4. Add particles at the right abstraction level

`three.quarks` is a three.js particle/VFX engine (`BatchedRenderer`, emitter shapes, size/color over life). For React-native composition use its declarative wrapper from `quarks.r3f`:

```bash
npm install quarks.r3f three.quarks
```

```tsx
import { QuarksProvider, ParticleSystem } from "quarks.r3f";
import { ConeEmitter, SizeOverLife, PiecewiseBezier, Bezier } from "three.quarks";

// Follow the installed version's example for emitter props; shapes and enums
// (e.g. RenderMode) are version-sensitive — verify before shipping.
```

Emitters are not physics bodies. If particles must collide, that is a different design: use instanced rigid bodies or bake the effect.

### 5. Tune live, then freeze constants

Tweakpane creates a draggable control panel bound to a plain params object. Use it in development only:

```ts
import { Pane } from "tweakpane";

const params = { gravity: -9.81, bloom: 0.9, particles: 600 };
const pane = new Pane({ title: "Scene tuning" });
pane.addBinding(params, "gravity", { min: -20, max: 0 });
pane.addBinding(params, "bloom", { min: 0, max: 2 });
pane.on("change", () => {
  // Apply values to your scene state; do not mutate Three objects directly here.
});
```

Once values are chosen, copy them into code and strip the pane from the production bundle. Confirm `panel` state never reaches production telemetry or URLs.

### 6. Verify in a real browser

- Render at target viewport sizes; check no horizontal overflow and usable controls on touch.
- Toggle each effect independently and confirm frame rate stays within budget.
- Drag a rigid body: it must not snap back to a React-set transform.
- With `prefers-reduced-motion`, reduce or stop nonessential particle and camera motion.
- Check WebGL context loss/failure fallback: a static poster or message, not a blank screen.

## Common Pitfalls / Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Physics is deterministic, I can skip the fixed timestep" | Rapier's default 60Hz step is deliberate; variable steps make replays diverge. |
| "I'll set mesh position from React state each frame" | That fights the physics solver. Apply impulses/forces; let Rapier own transforms. |
| "One more effect won't hurt" | Every pass costs a full-frame render. Measure before adding the next. |
| "The README example will work on whatever version is installed" | These APIs change majors frequently. Check installed package types first. |
| "Tweakpane is just a dev tool, it can stay" | It adds UI and bundle weight; keep it behind a dev-only flag. |

## Verification

- [ ] Installed versions checked against the code examples; no assumed APIs.
- [ ] `<Physics>` is wrapped in `<Suspense>`; collider strategy and timeStep are explicit.
- [ ] Each postprocessing effect added one at a time with frame-time measurement.
- [ ] Particles live in their own renderer/wrapper, not React-mutated geometry.
- [ ] Debug colliders and Tweakpane removed from production build.
- [ ] Browser check done at target viewports, with reduced-motion and WebGL-failure behavior verified.
