# Code patterns

Copy-pasteable, dependency-light patterns for the contracts in [Implementation](implementation.md). All snippets are framework-agnostic unless noted; adapt names to the project.

## Normalized scroll progress and scene intervals

Map native scroll position to a `0..1` progress value, then derive scene state from progress — never from accumulated scroll events.

```javascript
// scenes: ordered intervals covering [0, 1]. Last scene may be open-ended.
const scenes = [
  { id: "intro", start: 0, end: 0.25 },
  { id: "transform", start: 0.25, end: 0.72 },
  { id: "resolve", start: 0.72, end: 1 },
];

function scrollProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  if (max <= 0) return 1;
  return Math.min(1, Math.max(0, window.scrollY / max));
}

function activeScene(p) {
  return scenes.find((s) => p >= s.start && p < s.end) ?? scenes[scenes.length - 1];
}

// Local progress within a scene, clamped — used to index frames or poses.
function localProgress(p, scene) {
  const span = scene.end - scene.start || 1;
  return Math.min(1, Math.max(0, (p - scene.start) / span));
}
```

## Time-based damping

Smoothing must survive reverse scroll, anchor jumps, and tab switches. Use elapsed-time decay, not per-event easing.

```javascript
let smoothed = 0;
let last = performance.now();

function tick(now) {
  const dt = Math.min(0.05, (now - last) / 1000); // clamp gaps (hidden tab resume)
  last = now;
  const lambda = 12; // higher = snappier; lower = softer
  smoothed += (scrollProgress() - smoothed) * (1 - Math.exp(-lambda * dt));
  applyState(smoothed);
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
```

`applyState(p)` reads `smoothed`, resolves the active scene, and writes one set of transforms. Keep a single smoothed value so camera, panel, and protagonist stay synchronized.

## React scroll-progress hook

```tsx
import { useEffect, useRef } from "react";

export function useScrollProgress(lambda = 12) {
  const progress = useRef(0);
  const target = useRef(0);

  useEffect(() => {
    let raf = 0;
    let last = performance.now();

    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      target.current = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 1;
    };
    const tick = (now: number) => {
      const dt = Math.min(0.05, (now - last) / 1000);
      last = now;
      progress.current += (target.current - progress.current) * (1 - Math.exp(-lambda * dt));
      raf = requestAnimationFrame(tick);
    };

    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    raf = requestAnimationFrame(tick);
    return () => {
      window.removeEventListener("scroll", onScroll);
      cancelAnimationFrame(raf);
    };
  }, [lambda]);

  return progress; // read .current in a rAF-driven consumer, not in render
}
```

Prefer a rendering engine or `ref` + `requestAnimationFrame` for hot paths; avoid `setState` per frame.

## Native CSS scroll-driven animation

Modern browsers support `animation-timeline: scroll()` / `view()` with no JavaScript. Use it for simple scrub-reveals; fall back to the JS timeline above for state machines.

```css
@keyframes reveal {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.panel {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}
```

## Web Animations API + ScrollTimeline

```javascript
const panel = document.getElementById("panel");
const timeline = new ScrollTimeline({
  source: document.scrollingElement,
  axis: "block",
});

panel.animate(
  [
    { opacity: 0, transform: "translateY(24px)" },
    { opacity: 1, transform: "translateY(0)" },
  ],
  { duration: 1, fill: "both", timeline },
);
```

## Scroll-indexed frame sequence

For dense aligned frames (rendered character passes, product turntables). Decode progressively; never hold every frame decoded at once.

```javascript
const FRAMES = ["walk-001.webp", "walk-002.webp", /* ... */ "walk-120.webp"];
const STAGE_START = 0.25;
const STAGE_END = 0.6;

const images = FRAMES.map((src) => {
  const img = new Image();
  img.src = src;
  return img;
});

let current = -1;

function applyFrames(p) {
  const local = (p - STAGE_START) / (STAGE_END - STAGE_START);
  const index = Math.min(
    FRAMES.length - 1,
    Math.max(0, Math.round(local * (FRAMES.length - 1))),
  );
  if (index !== current) {
    current = index;
    stage.style.backgroundImage = `url(${images[index].src})`;
  }
}
```

Memory budget: `width × height × 4 × residentFrames` bytes plus renderer overhead. If a frame is a 1920×1080 RGBA texture it costs ~8.3 MB decoded — a 120-frame sequence is ~1 GB if held fully decoded. Preload a small window around the current index, not the whole strip, and keep a known valid frame while loading.

## Reduced-motion handling

```javascript
const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
let reduced = mq.matches;

function applyReducedMotion() {
  // Swap the pinned canvas for a document-flow version of the full narrative.
  story.classList.toggle("reduced", reduced);
  if (reduced) showDocumentFlow();
  else hideDocumentFlow();
}

mq.addEventListener("change", (e) => {
  reduced = e.matches;
  applyReducedMotion();
});
applyReducedMotion();
```

Reduced motion is not "stop everything at frame zero" — it is the full narrative in readable flow with scrubbed camera and articulated animation disabled.

## 2D rig via CSS transform hierarchy

A layered character rig: separate elements per body part, pivots at joints, parented via nested DOM. Drive bone rotation/translation from timeline progress.

```html
<div id="character">
  <div class="torso">
    <div class="arm upper"><div class="arm lower"></div></div>
    <div class="leg upper"><div class="leg lower"></div></div>
  </div>
</div>
```

```css
.arm, .leg { transform-origin: top center; } /* pivot at the joint */
.torso  { transform-origin: 50% 90%; }
```

```javascript
// One pose per key progress. Bones interpolated between adjacent keys.
const keys = [
  { t: 0.0, arm: -20, leg: 10 },
  { t: 0.5, arm: 15, leg: -12 },
  { t: 1.0, arm: -20, leg: 10 },
];

function poseAt(t) {
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t >= a.t && t <= b.t) {
      const k = (t - a.t) / (b.t - a.t || 1);
      return {
        arm: a.arm + (b.arm - a.arm) * k,
        leg: a.leg + (b.leg - a.leg) * k,
      };
    }
  }
  return keys[keys.length - 1];
}

function applyPose(p) {
  const pose = poseAt(p);
  armUpper.style.transform = `rotate(${pose.arm}deg)`;
  legUpper.style.transform = `rotate(${pose.leg}deg)`;
}
```

For large turns, switch to an alternate authored view rather than stretching a front view into a back view. Use separate transform layers for primary motion, pointer response, and idle animation so they never overwrite each other.

## Resource lifecycle

```javascript
let rafId = 0;
const resizeObserver = new ResizeObserver(recalculateGeometry);
const intersectionObserver = new IntersectionObserver(pauseWhenOffscreen);

function dispose() {
  cancelAnimationFrame(rafId);
  resizeObserver.disconnect();
  intersectionObserver.disconnect();
  renderer?.dispose?.();
  window.removeEventListener("scroll", onScroll);
}
```

Pause the rAF loop when the tab is hidden or the section is offscreen; resume without a time-step jump (the `dt` clamp in the damping loop handles this).
