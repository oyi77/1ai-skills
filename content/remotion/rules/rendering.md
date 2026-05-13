# Remotion Rendering Rule

## CLI Render

```bash
# Basic render
npx remotion render <CompositionId> out/video.mp4

# Interactive picker (no id needed)
npx remotion render

# Common options
npx remotion render MyComp out/video.mp4 \
  --codec h264 \
  --crf 18 \
  --jpeg-quality 80 \
  --scale 1

# Render GIF
npx remotion render MyComp out/video.gif --codec gif

# Render WebM
npx remotion render MyComp out/video.webm --codec vp8

# Render still image (single frame)
npx remotion still MyComp out/still.png --frame 0

# Image sequence
npx remotion render MyComp out/frames --sequence
```

## Codec Guide

| Codec | Use Case | Command |
|-------|----------|---------|
| `h264` | Default, best compatibility | `--codec h264` |
| `h265` | Smaller file, less compatible | `--codec h265` |
| `vp8` | WebM, open source | `--codec vp8` |
| `vp9` | Better quality WebM | `--codec vp9` |
| `gif` | Animated GIF | `--codec gif` |
| `prores` | Professional editing | `--codec prores` |

## Output Resolutions

```bash
# 1080p (default)
--width 1920 --height 1080

# 4K
--width 3840 --height 2160

# Vertical (TikTok/Reels/Shorts)
# Set in composition: width=1080, height=1920

# Square (Instagram)
# Set in composition: width=1080, height=1080
```

## Server-Side Rendering (Node.js API)

```typescript
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import { webpackOverride } from './src/webpack-override';

const bundleLocation = await bundle({
  entryPoint: './src/index.ts',
  webpackOverride,
});

const composition = await selectComposition({
  serveUrl: bundleLocation,
  id: 'MyComposition',
  inputProps: { title: 'My Video' },
});

await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  inputProps: { title: 'My Video' },
  onProgress: ({ progress }) => {
    console.log(`Rendering: ${Math.round(progress * 100)}%`);
  },
});
```

## calculateMetadata — Dynamic Duration

Use this to set composition duration from external data (audio length, data, etc.):

```tsx
import { CalculateMetadataFunction } from 'remotion';
import { getAudioDurationInSeconds } from '@remotion/media-utils';

interface Props {
  narrationFile: string;
}

export const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const duration = await getAudioDurationInSeconds(
    staticFile(props.narrationFile)
  );

  return {
    durationInFrames: Math.ceil(duration * 30) + 30, // +30 frames buffer
    fps: 30,
  };
};

// In Root.tsx:
<Composition
  id="DynamicVideo"
  component={MyVideo}
  calculateMetadata={calculateMetadata}
  defaultProps={{ narrationFile: 'narration.mp3' }}
  // durationInFrames omitted — calculated from audio
  durationInFrames={1}   // placeholder, overridden by calculateMetadata
  fps={30}
  width={1920}
  height={1080}
/>
```

## AWS Lambda (Serverless)

```bash
# Install
npm i @remotion/lambda

# Deploy Lambda function
npx remotion lambda functions deploy

# Deploy site to S3
npx remotion lambda sites create --site-name my-site

# Render on Lambda
npx remotion lambda render --site-name my-site MyComp out/video.mp4
```

Node.js API:
```typescript
import { renderMediaOnLambda } from '@remotion/lambda/client';

const { renderId, bucketName } = await renderMediaOnLambda({
  region: 'us-east-1',
  functionName: 'remotion-render',
  serveUrl: 'https://your-s3-site.s3.amazonaws.com',
  composition: 'MyComposition',
  inputProps: { title: 'My Video' },
  codec: 'h264',
  downloadBehavior: { type: 'download', fileName: 'video.mp4' },
});
```

## Remotion Studio

```bash
npm run dev   # Starts Studio at http://localhost:3000

# Studio features:
# - Live preview while editing code
# - Timeline scrubbing
# - Render button with quality controls
# - Multiple composition management
```

## Render Quality Tips

- Use `--crf 18` for high quality (lower = better, default ~28)
- Use `--jpeg-quality 80-95` for JPEG frames
- Use `--scale 0.5` to render at 50% size for testing
- Add `--log verbose` for debugging render issues
- Use `<OffthreadVideo>` instead of `<Video>` for embedded videos (avoids frame sync issues)

## FFmpeg Post-Processing (BGM Mixing)

After Remotion renders video, use FFmpeg to add background music:

```bash
ffmpeg -i out/video.mp4 -i public/bgm.mp3 \
  -filter_complex "[1:a]volume=0.15[bgm];[0:a][bgm]amix=inputs=2:duration=first" \
  -c:v copy \
  out/final.mp4

# Burn subtitles (SRT)
ffmpeg -i out/video.mp4 -vf subtitles=public/subtitles.srt out/final-with-subs.mp4
```
