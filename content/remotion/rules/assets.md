# Remotion Assets Rule

## Static Assets Location

All static assets must go in the `/public` folder and be referenced with `staticFile()`.

```bash
public/
├── images/
│   ├── logo.png
│   └── background.jpg
├── audio/
│   ├── narration.mp3
│   └── bgm.mp3
├── video/
│   └── clip.mp4
└── fonts/
    └── CustomFont.ttf
```

## Images

Always use `<Img>` (not `<img>`) — it waits for the image to load before rendering:

```tsx
import { Img, staticFile } from 'remotion';

// Local image
<Img src={staticFile('images/logo.png')} style={{ width: 200 }} />

// URL image
<Img src="https://picsum.photos/800/600" style={{ width: '100%' }} />
```

## Background Image

```tsx
<AbsoluteFill>
  <Img
    src={staticFile('background.jpg')}
    style={{
      width: '100%',
      height: '100%',
      objectFit: 'cover',
    }}
  />
  {/* Content on top */}
  <div style={{ position: 'absolute', inset: 0 }}>
    <h1>Overlay Text</h1>
  </div>
</AbsoluteFill>
```

## Videos

Use `<OffthreadVideo>` for reliable frame-accurate rendering (preferred over `<Video>`):

```tsx
import { OffthreadVideo, staticFile } from 'remotion';

// Background video
<OffthreadVideo
  src={staticFile('video/background.mp4')}
  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
/>

// Trim video
<OffthreadVideo
  src={staticFile('clip.mp4')}
  startFrom={30}    // skip first 30 frames
  endAt={150}       // stop at frame 150
/>

// Muted video
<OffthreadVideo src={staticFile('clip.mp4')} muted />
```

## GIF

```tsx
import { Gif } from '@remotion/gif';

<Gif
  src={staticFile('animation.gif')}
  width={300}
  height={300}
  fit="contain"
/>
```

## Lottie Animations

```bash
npm install @remotion/lottie
```

```tsx
import { Lottie } from '@remotion/lottie';
import animationData from './animation.json';

<Lottie
  animationData={animationData}
  style={{ width: 400, height: 400 }}
/>
```

## Custom Fonts (Local)

```tsx
import { loadFont } from '@remotion/fonts';

const font = loadFont({
  family: 'MyFont',
  url: staticFile('fonts/MyFont.woff2'),
  weight: '400',
  style: 'normal',
});

// Wait for font to load using delayRender
const { fontFamily } = font;
<h1 style={{ fontFamily }}>Custom Font Text</h1>
```

## Preloading Assets

For reliable rendering, preload critical assets:

```tsx
import { prefetch } from 'remotion';

// Preload at component mount
useEffect(() => {
  const { free } = prefetch(staticFile('large-video.mp4'));
  return free; // cleanup
}, []);
```

## delayRender / continueRender (Async Data)

Use when you need to fetch data before rendering:

```tsx
import { delayRender, continueRender, cancelRender } from 'remotion';
import { useState, useEffect } from 'react';

const handle = delayRender('Loading data');

const MyComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('https://api.example.com/data')
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        continueRender(handle);
      })
      .catch((err) => cancelRender(err));
  }, []);

  if (!data) return null;
  return <div>{data.title}</div>;
};
```
