# Remotion Animations Rule

## interpolate()

Maps an input value (usually `frame`) to an output range.

```tsx
import { interpolate, useCurrentFrame } from 'remotion';

const frame = useCurrentFrame();

// Fade in over 30 frames
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

// Slide in from left
const translateX = interpolate(frame, [0, 45], [-200, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.cubic),
});
```

## spring()

Physics-based animation, great for natural motion. Animates 0→1 by default.

```tsx
import { spring, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Basic spring (bounce in)
const scale = spring({ frame, fps });

// Custom spring — less bounce
const scaleSmooth = spring({
  frame,
  fps,
  config: { damping: 200, stiffness: 100 },
});

// Spring with fixed duration (no overshoot)
const progress = spring({
  frame,
  fps,
  durationInFrames: 60,
  config: { damping: 100 },
});

// Delayed spring
const delayed = spring({ frame: frame - 30, fps }); // starts at frame 30

// Map spring (0→1) to another range
const width = interpolate(progress, [0, 1], [0, 800]);
```

## Easing Curves

```tsx
import { Easing, interpolate } from 'remotion';

const eased = interpolate(frame, [0, 60], [0, 1], {
  easing: Easing.out(Easing.cubic),      // ease-out cubic
  // Easing.in(Easing.cubic)             // ease-in cubic
  // Easing.inOut(Easing.cubic)          // ease-in-out cubic
  // Easing.bezier(0.25, 0.1, 0.25, 1)  // custom bezier
  // Easing.bounce                       // bouncy
  // Easing.elastic(2)                   // elastic
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

## Common Animation Patterns

### Fade in
```tsx
const opacity = interpolate(frame, [0, 20], [0, 1], {
  extrapolateRight: 'clamp',
});
```

### Fade out (at end of composition)
```tsx
const { durationInFrames } = useVideoConfig();
const opacity = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {
  extrapolateLeft: 'clamp',
});
```

### Scale entrance
```tsx
const scale = spring({ frame, fps, config: { damping: 10 } });
<div style={{ transform: `scale(${scale})` }}>Content</div>
```

### Slide up
```tsx
const y = interpolate(frame, [0, 30], [50, 0], {
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.quad),
});
<div style={{ transform: `translateY(${y}px)` }}>Content</div>
```

### Counter animation
```tsx
const { fps } = useVideoConfig();
const progress = spring({ frame, fps, durationInFrames: 60, config: { damping: 100 } });
const count = Math.floor(interpolate(progress, [0, 1], [0, targetNumber]));
```

### Staggered children (trail effect)
```tsx
{items.map((item, i) => {
  const delay = i * 5; // 5 frame delay per item
  const opacity = interpolate(frame - delay, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return <div key={i} style={{ opacity }}>{item}</div>;
})}
```

### Color interpolation
```tsx
import { interpolateColors } from 'remotion';

const color = interpolateColors(
  frame,
  [0, 60],
  ['#ff0000', '#0000ff']
);
```

## Sequencing with `<Sequence>`

`useCurrentFrame()` resets to 0 inside a `<Sequence>`. This is the key feature for modular scene components.

```tsx
// Scene component doesn't need to know its start time
const Scene1 = () => {
  const frame = useCurrentFrame(); // always starts at 0
  const opacity = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' });
  return <AbsoluteFill style={{ opacity }}>Scene 1</AbsoluteFill>;
};

// Root composition sequences them
<>
  <Sequence from={0} durationInFrames={90}><Scene1 /></Sequence>
  <Sequence from={90} durationInFrames={90}><Scene2 /></Sequence>
</>
```

## fps-aware timing (ALWAYS do this)

```tsx
const { fps } = useVideoConfig();

// Good — works at any fps
const fadeIn = interpolate(frame, [0, 0.5 * fps], [0, 1]);
const duration = 3 * fps; // 3 seconds

// Bad — breaks if fps changes
const fadeIn = interpolate(frame, [0, 15], [0, 1]);
```
