# Remotion Video Embedding Rule

## OffthreadVideo (Preferred for Rendering)

Use `<OffthreadVideo>` instead of `<Video>` for reliable frame-accurate rendering. `<Video>` can cause dropped frames during rendering.

```tsx
import { OffthreadVideo, staticFile, AbsoluteFill } from 'remotion';

// Full-screen background video
<AbsoluteFill>
  <OffthreadVideo
    src={staticFile('video/background.mp4')}
    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
  />
</AbsoluteFill>

// Contained video
<OffthreadVideo
  src={staticFile('clip.mp4')}
  style={{ width: 800, height: 450, borderRadius: 12 }}
/>

// Remote URL
<OffthreadVideo src="https://example.com/video.mp4" />
```

## Trim Video

```tsx
<OffthreadVideo
  src={staticFile('long-clip.mp4')}
  startFrom={30}    // Skip first 30 frames of the video file
  endAt={150}       // Stop playback at frame 150 of the video file
/>
```

## Muted Video (Background Visuals)

```tsx
<OffthreadVideo
  src={staticFile('background.mp4')}
  muted
  loop                // Loop if shorter than composition
  style={{ objectFit: 'cover', width: '100%', height: '100%' }}
/>
```

## Video + Overlay Text

```tsx
<AbsoluteFill>
  {/* Background video */}
  <OffthreadVideo
    src={staticFile('background.mp4')}
    muted
    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
  />

  {/* Dark overlay */}
  <AbsoluteFill style={{ backgroundColor: 'rgba(0,0,0,0.5)' }} />

  {/* Content on top */}
  <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
    <h1 style={{ color: 'white', fontSize: 80 }}>Overlay Title</h1>
  </AbsoluteFill>
</AbsoluteFill>
```

## Speed Change

```tsx
<OffthreadVideo
  src={staticFile('clip.mp4')}
  playbackRate={2}   // 2x speed
/>
```

## Volume Control

```tsx
<OffthreadVideo
  src={staticFile('interview.mp4')}
  volume={0.8}       // 80% volume
/>

// Dynamic volume (fade in)
const frame = useCurrentFrame();
const volume = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
<OffthreadVideo src={staticFile('clip.mp4')} volume={volume} />
```

## Get Video Dimensions

```tsx
import { getVideoMetadata } from '@remotion/media-utils';

// In calculateMetadata
const metadata = await getVideoMetadata(staticFile('clip.mp4'));
console.log(metadata.width, metadata.height, metadata.durationInSeconds);
```

## Get Video Duration

```tsx
import { getVideoMetadata } from '@remotion/media-utils';

export const calculateMetadata = async ({ props }) => {
  const { durationInSeconds } = await getVideoMetadata(staticFile(props.videoFile));
  return {
    durationInFrames: Math.ceil(durationInSeconds * 30),
  };
};
```

## Picture-in-Picture Layout

```tsx
<AbsoluteFill>
  {/* Main video */}
  <OffthreadVideo
    src={staticFile('main.mp4')}
    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
    muted
  />

  {/* PiP video */}
  <div style={{
    position: 'absolute',
    bottom: 40, right: 40,
    width: 400, height: 225,
    borderRadius: 12,
    overflow: 'hidden',
    border: '3px solid white',
    boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
  }}>
    <OffthreadVideo
      src={staticFile('pip.mp4')}
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
    />
  </div>
</AbsoluteFill>
```

## Side-by-Side Comparison

```tsx
<AbsoluteFill style={{ flexDirection: 'row' }}>
  <div style={{ flex: 1, overflow: 'hidden' }}>
    <OffthreadVideo
      src={staticFile('before.mp4')}
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      muted
    />
    <div style={{
      position: 'absolute', top: 20, left: 20,
      backgroundColor: 'rgba(0,0,0,0.6)',
      color: 'white', padding: '8px 16px', borderRadius: 8,
    }}>Before</div>
  </div>
  <div style={{ flex: 1, overflow: 'hidden' }}>
    <OffthreadVideo
      src={staticFile('after.mp4')}
      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      muted
    />
    <div style={{
      position: 'absolute', top: 20, right: 20,
      backgroundColor: 'rgba(0,0,0,0.6)',
      color: 'white', padding: '8px 16px', borderRadius: 8,
    }}>After</div>
  </div>
</AbsoluteFill>
```
