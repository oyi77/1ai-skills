# Remotion Parameters & Zod Schema Rule

## Why Parameters?

Parametrize compositions so you can render the same video template with different data — useful for SaaS video generation, personalized videos, A/B testing.

## Basic Props

```tsx
// Define props interface
interface MyVideoProps {
  title: string;
  subtitle: string;
  backgroundColor: string;
  durationSecs: number;
}

// Use in component
export const MyVideo: React.FC<MyVideoProps> = ({
  title,
  subtitle,
  backgroundColor,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor }}>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </AbsoluteFill>
  );
};

// Register with defaultProps
<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{
    title: 'Hello World',
    subtitle: 'A programmatic video',
    backgroundColor: '#1a1a2e',
    durationSecs: 5,
  }}
/>
```

## Zod Schema (Recommended — enables Studio UI editing)

```bash
npm install zod
```

```tsx
import { z } from 'zod';
import { zColor } from '@remotion/zod-types';

// Define schema
export const MyVideoSchema = z.object({
  title: z.string().describe('Main headline text'),
  subtitle: z.string().default(''),
  primaryColor: zColor().default('#4f46e5'),
  backgroundColor: zColor().default('#1a1a2e'),
  durationSecs: z.number().min(1).max(120).default(10),
  logoUrl: z.string().url().optional(),
  items: z.array(z.object({
    label: z.string(),
    value: z.number(),
  })).default([]),
});

// Infer TypeScript type
type MyVideoProps = z.infer<typeof MyVideoSchema>;

// Component
export const MyVideo: React.FC<MyVideoProps> = ({
  title, primaryColor, items,
}) => { /* ... */ };

// Register with schema
<Composition
  id="MyVideo"
  component={MyVideo}
  schema={MyVideoSchema}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={MyVideoSchema.parse({})}
/>
```

## Dynamic Duration from Props

```tsx
export const MyVideoSchema = z.object({
  narrationFile: z.string().default('narration.mp3'),
  title: z.string(),
});

// calculateMetadata runs before rendering to set duration
export const calculateMetadata: CalculateMetadataFunction<
  z.infer<typeof MyVideoSchema>
> = async ({ props }) => {
  const audioDuration = await getAudioDurationInSeconds(
    staticFile(props.narrationFile)
  );

  return {
    durationInFrames: Math.ceil(audioDuration * 30) + 30, // +1s buffer
    props: {
      ...props,
      // Can also transform/augment props here
    },
  };
};

<Composition
  id="NarratedVideo"
  component={NarratedVideo}
  schema={MyVideoSchema}
  calculateMetadata={calculateMetadata}
  durationInFrames={1}   // placeholder — overridden
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ narrationFile: 'narration.mp3', title: 'My Video' }}
/>
```

## Passing Props at Render Time (CLI)

```bash
# Pass JSON props via CLI
npx remotion render MyVideo out/video.mp4 \
  --props='{"title":"My Custom Title","primaryColor":"#ff6b6b"}'

# From a JSON file
npx remotion render MyVideo out/video.mp4 \
  --props=./my-props.json
```

## Passing Props via Server-Side API

```typescript
await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation: 'out/video.mp4',
  inputProps: {
    title: 'Generated Video',
    subtitle: 'For customer #12345',
    primaryColor: '#22c55e',
    items: [
      { label: 'Revenue', value: 15000000 },
      { label: 'Users', value: 5432 },
    ],
  },
});
```

## Environment Variables in Remotion

```tsx
// Access env vars (must be prefixed with REMOTION_ or set via Vite)
const apiUrl = process.env.REMOTION_API_URL;

// Or use import.meta.env in Vite-based setups
const key = import.meta.env.VITE_API_KEY;
```

## Template Pattern for SaaS Video Generation

```tsx
// Template registry
const TEMPLATES = {
  'product-showcase': ProductShowcaseVideo,
  'data-report': DataReportVideo,
  'testimonial': TestimonialVideo,
  'promo': PromoVideo,
} as const;

// Root registers all templates
export const RemotionRoot = () => (
  <>
    {Object.entries(TEMPLATES).map(([id, Component]) => (
      <Composition
        key={id}
        id={id}
        component={Component}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    ))}
  </>
);

// Render specific template with data
await renderMedia({
  composition: await selectComposition({
    serveUrl: bundleLocation,
    id: 'product-showcase',
    inputProps: productData,
  }),
  // ...
});
```
