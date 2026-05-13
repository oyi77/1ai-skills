# Remotion Transitions Rule

## Using @remotion/transitions

```bash
npm install @remotion/transitions
```

```tsx
import { TransitionSeries } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { wipe } from '@remotion/transitions/wipe';
import { flip } from '@remotion/transitions/flip';
import { clockWipe } from '@remotion/transitions/clock-wipe';

export const MyVideo = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={90}>
      <Scene1 />
    </TransitionSeries.Sequence>

    <TransitionSeries.Transition
      presentation={fade()}
      timing={{ type: 'linear', durationInFrames: 20 }}
    />

    <TransitionSeries.Sequence durationInFrames={90}>
      <Scene2 />
    </TransitionSeries.Sequence>

    <TransitionSeries.Transition
      presentation={slide({ direction: 'from-right' })}
      timing={{ type: 'spring', config: { damping: 200 } }}
    />

    <TransitionSeries.Sequence durationInFrames={90}>
      <Scene3 />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
```

## Available Transition Presentations

```tsx
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';        // direction: from-left/right/top/bottom
import { wipe } from '@remotion/transitions/wipe';          // direction: from-left/right/top/bottom
import { flip } from '@remotion/transitions/flip';          // direction: from-left/right/top/bottom
import { clockWipe } from '@remotion/transitions/clock-wipe'; // rotates like a clock
import { iris } from '@remotion/transitions/iris';          // circle wipe
import { none } from '@remotion/transitions/none';          // no visual transition, just timing
```

## Transition Timing Options

```tsx
// Linear
{ type: 'linear', durationInFrames: 20 }

// Spring (natural/bouncy)
{ type: 'spring', config: { damping: 200, stiffness: 80 } }

// Custom easing
{
  type: 'custom',
  durationInFrames: 30,
  easingFunction: Easing.out(Easing.cubic),
}
```

## Manual Cross-Fade (No Package)

If you prefer not using `@remotion/transitions`:

```tsx
const TRANSITION_DURATION = 20;
const SCENE1_DURATION = 90;
const SCENE2_DURATION = 90;

export const ManualTransition = () => {
  const frame = useCurrentFrame();

  // Scene 1 fades out starting at frame 70
  const scene1Opacity = interpolate(
    frame,
    [SCENE1_DURATION - TRANSITION_DURATION, SCENE1_DURATION],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  // Scene 2 fades in starting at frame 70
  const scene2Opacity = interpolate(
    frame,
    [SCENE1_DURATION - TRANSITION_DURATION, SCENE1_DURATION],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: scene1Opacity }}>
        <Scene1 />
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: scene2Opacity }}>
        <Scene2 />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

## Slide Transition (Manual)

```tsx
const SLIDE_FRAMES = 30;

// Slide out to left
const scene1X = interpolate(frame, [60, 60 + SLIDE_FRAMES], [0, -1920], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
  easing: Easing.in(Easing.cubic),
});

// Slide in from right
const scene2X = interpolate(frame, [60, 60 + SLIDE_FRAMES], [1920, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.cubic),
});

<AbsoluteFill style={{ transform: `translateX(${scene1X}px)` }}><Scene1 /></AbsoluteFill>
<AbsoluteFill style={{ transform: `translateX(${scene2X}px)` }}><Scene2 /></AbsoluteFill>
```

## Zoom Transition

```tsx
// Scene zooms in / next scene reveals underneath
const scale = interpolate(frame, [50, 80], [1, 1.2], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
const opacity = interpolate(frame, [60, 80], [1, 0], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

<AbsoluteFill style={{
  transform: `scale(${scale})`,
  opacity,
}}>
  <Scene1 />
</AbsoluteFill>
```

## Wipe Transition (Clip-Path)

```tsx
const wipeProgress = interpolate(frame, [60, 90], [0, 100], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});

<AbsoluteFill>
  <Scene1 />
  <AbsoluteFill style={{
    clipPath: `inset(0 ${100 - wipeProgress}% 0 0)`,
  }}>
    <Scene2 />
  </AbsoluteFill>
</AbsoluteFill>
```
