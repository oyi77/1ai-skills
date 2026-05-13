# Remotion Text Animations Rule

## Basic Fade-In Text

```tsx
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' });
<h1 style={{ opacity, color: 'white', fontSize: 80 }}>Hello World</h1>
```

## Word-by-Word Reveal

```tsx
const words = "This is animated text".split(' ');
const framesPerWord = 8;

{words.map((word, i) => {
  const startFrame = i * framesPerWord;
  const opacity = interpolate(frame - startFrame, [0, 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <span key={i} style={{ opacity, marginRight: '0.25em' }}>
      {word}
    </span>
  );
})}
```

## Character-by-Character Reveal (Typewriter)

```tsx
const text = "Type this text.";
const charsPerFrame = 0.5; // one char every 2 frames
const charsToShow = Math.floor(frame * charsPerFrame);
const visibleText = text.slice(0, charsToShow);

<p style={{ fontFamily: 'monospace', fontSize: 48, color: 'white' }}>
  {visibleText}<span style={{ opacity: frame % 20 < 10 ? 1 : 0 }}>|</span>
</p>
```

## Spring-Based Text Entrance (Recommended)

```tsx
const { fps } = useVideoConfig();
const scale = spring({ frame, fps, config: { damping: 12, stiffness: 200 } });
const translateY = interpolate(scale, [0, 1], [40, 0]);

<h1 style={{
  transform: `translateY(${translateY}px) scale(${scale})`,
  opacity: scale,
  color: 'white',
  fontSize: 72,
}}>
  Title Text
</h1>
```

## Slide In From Direction

```tsx
// Slide from left
const x = interpolate(frame, [0, 30], [-400, 0], {
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.cubic),
});
<div style={{ transform: `translateX(${x}px)` }}>Text</div>

// Slide from bottom
const y = interpolate(frame, [0, 30], [100, 0], {
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.quart),
});
<div style={{ transform: `translateY(${y}px)` }}>Text</div>
```

## Subtitle / Caption Display

```tsx
interface Caption {
  text: string;
  startFrame: number;
  endFrame: number;
}

const captions: Caption[] = [
  { text: "Hello world", startFrame: 0, endFrame: 60 },
  { text: "This is a caption", startFrame: 60, endFrame: 120 },
];

const currentCaption = captions.find(
  (c) => frame >= c.startFrame && frame < c.endFrame
);

{currentCaption && (
  <div style={{
    position: 'absolute',
    bottom: 80,
    left: 0,
    right: 0,
    textAlign: 'center',
    fontSize: 48,
    color: 'white',
    textShadow: '2px 2px 4px black',
    padding: '0 40px',
  }}>
    {currentCaption.text}
  </div>
)}
```

## Loading Google Fonts

```tsx
import { loadFont } from '@remotion/google-fonts/Inter';

const { fontFamily } = loadFont();

// In your component:
<h1 style={{ fontFamily }}>Text with Google Font</h1>
```

Or use `@remotion/google-fonts` package with specific font:
```bash
npm install @remotion/google-fonts
```

```tsx
import { loadFont } from '@remotion/google-fonts/Montserrat';
const { fontFamily } = loadFont('normal'); // 'normal' | 'italic'
```

## Text Gradient

```tsx
<h1 style={{
  fontSize: 80,
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
}}>
  Gradient Text
</h1>
```

## Highlighted Word Emphasis

```tsx
// Highlight specific word in sync with audio
const highlightedWord = captions.find(
  (c) => frame >= c.startFrame && frame < c.endFrame
)?.word;

{words.map((word, i) => (
  <span
    key={i}
    style={{
      color: word === highlightedWord ? '#fbbf24' : 'white',
      fontWeight: word === highlightedWord ? 'bold' : 'normal',
      transition: 'none', // No CSS transitions! Use frame-based logic
    }}
  >
    {word}{' '}
  </span>
))}
```
