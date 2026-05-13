# Product Showcase & Commercial Video in Remotion

## Visual Identity

Product videos = clean minimalism, dramatic reveals, floating product mockups, feature callouts, before/after splits, pricing sections, and a strong CTA. Think Apple-style or Shopify ad aesthetics.

## Dramatic Product Reveal

```tsx
const ProductReveal: React.FC<{
  productImage: string;
  productName: string;
  tagline?: string;
}> = ({ productImage, productName, tagline }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spotlight from above
  const spotlightY = interpolate(frame, [0, 40], [-200, 0], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Product scale-up
  const productScale = spring({ frame: frame - 20, fps, config: { damping: 60, stiffness: 150 } });

  // Name reveal
  const nameOpacity = interpolate(frame, [45, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0a', justifyContent: 'center', alignItems: 'center' }}>
      {/* Spotlight gradient */}
      <div style={{
        position: 'absolute',
        width: 600, height: 600,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%)',
        top: '50%', left: '50%',
        transform: `translate(-50%, calc(-50% + ${spotlightY}px))`,
      }} />

      {/* Product */}
      <div style={{
        transform: `scale(${productScale})`,
        marginBottom: 40,
        filter: 'drop-shadow(0 40px 60px rgba(0,0,0,0.8))',
      }}>
        <Img src={staticFile(productImage)} style={{ width: 480, height: 480, objectFit: 'contain' }} />
      </div>

      {/* Product name */}
      <div style={{ opacity: nameOpacity, textAlign: 'center' }}>
        <h1 style={{ color: 'white', fontSize: 72, fontWeight: 300, margin: 0, letterSpacing: 8 }}>
          {productName}
        </h1>
        {tagline && (
          <p style={{ color: '#888', fontSize: 28, margin: '12px 0 0', fontWeight: 300 }}>
            {tagline}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

## Floating Product (3D-Style Rotation)

```tsx
const FloatingProduct: React.FC<{ imageSrc: string }> = ({ imageSrc }) => {
  const frame = useCurrentFrame();

  // Gentle rotation + float
  const rotateY = Math.sin(frame * 0.03) * 15;  // -15° to +15°
  const floatY = Math.sin(frame * 0.05) * 12;   // gentle bob

  // Perspective shadow
  const shadowBlur = 40 + Math.sin(frame * 0.05) * 10;
  const shadowOpacity = 0.4 - Math.sin(frame * 0.05) * 0.1;

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      {/* Shadow */}
      <div style={{
        position: 'absolute',
        bottom: -20, left: '10%',
        width: '80%', height: 30,
        backgroundColor: 'rgba(0,0,0,0.3)',
        borderRadius: '50%',
        filter: `blur(${shadowBlur}px)`,
        opacity: shadowOpacity,
        transform: `scaleX(${1 + Math.sin(frame * 0.05) * 0.1})`,
      }} />

      {/* Product */}
      <div style={{
        transform: `translateY(${floatY}px) perspective(800px) rotateY(${rotateY}deg)`,
      }}>
        <Img src={staticFile(imageSrc)} style={{ width: 500, height: 500, objectFit: 'contain' }} />
      </div>
    </div>
  );
};
```

## Feature Callout List

```tsx
interface Feature {
  icon: string;   // emoji or SVG path
  title: string;
  desc: string;
}

const FeatureCallouts: React.FC<{ features: Feature[] }> = ({ features }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 32 }}>
      {features.map((f, i) => {
        const delay = i * 12;
        const slideX = spring({ frame: frame - delay, fps, config: { damping: 80 } });
        const x = interpolate(slideX, [0, 1], [-80, 0]);
        const opacity = interpolate(frame - delay, [0, 15], [0, 1], {
          extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
        });

        return (
          <div key={i} style={{
            display: 'flex',
            alignItems: 'center',
            gap: 20,
            transform: `translateX(${x}px)`,
            opacity,
          }}>
            <div style={{
              width: 56, height: 56,
              backgroundColor: 'rgba(79,70,229,0.15)',
              borderRadius: 16,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 28,
              border: '1px solid rgba(79,70,229,0.3)',
            }}>
              {f.icon}
            </div>
            <div>
              <div style={{ color: 'white', fontSize: 28, fontWeight: 700 }}>{f.title}</div>
              <div style={{ color: '#94a3b8', fontSize: 22 }}>{f.desc}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
```

## Before / After Split Reveal

```tsx
const BeforeAfterReveal: React.FC<{
  beforeSrc: string;
  afterSrc: string;
  revealStartFrame?: number;
}> = ({ beforeSrc, afterSrc, revealStartFrame = 30 }) => {
  const frame = useCurrentFrame();

  const revealProgress = interpolate(frame, [revealStartFrame, revealStartFrame + 60], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  return (
    <AbsoluteFill>
      {/* Before (full width) */}
      <OffthreadVideo src={staticFile(beforeSrc)} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />

      {/* After (clip reveal from left) */}
      <AbsoluteFill style={{ clipPath: `inset(0 ${100 - revealProgress}% 0 0)` }}>
        <OffthreadVideo src={staticFile(afterSrc)} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </AbsoluteFill>

      {/* Divider line */}
      <div style={{
        position: 'absolute',
        top: 0, bottom: 0,
        left: `${revealProgress}%`,
        width: 3,
        backgroundColor: 'white',
        boxShadow: '0 0 12px rgba(255,255,255,0.8)',
      }} />

      {/* Labels */}
      <div style={{ position: 'absolute', top: 40, left: 40, color: 'white', fontSize: 28, fontWeight: 700, backgroundColor: 'rgba(0,0,0,0.6)', padding: '8px 20px', borderRadius: 999 }}>BEFORE</div>
      <div style={{ position: 'absolute', top: 40, right: 40, color: 'white', fontSize: 28, fontWeight: 700, backgroundColor: 'rgba(79,70,229,0.8)', padding: '8px 20px', borderRadius: 999 }}>AFTER</div>
    </AbsoluteFill>
  );
};
```

## Pricing Card

```tsx
const PricingCard: React.FC<{
  price: string;
  currency?: string;
  period?: string;
  features: string[];
  ctaText?: string;
  triggerFrame?: number;
}> = ({ price, currency = 'Rp', period = '/bulan', features, ctaText = 'Mulai Sekarang', triggerFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const appear = spring({ frame: frame - triggerFrame, fps, config: { damping: 70 } });
  const scale = interpolate(appear, [0, 1], [0.8, 1]);
  const opacity = interpolate(appear, [0, 0.3], [0, 1]);

  return (
    <div style={{
      backgroundColor: '#1e1b4b',
      border: '2px solid #6366f1',
      borderRadius: 24,
      padding: 48,
      width: 480,
      transform: `scale(${scale})`,
      opacity,
      boxShadow: '0 0 80px rgba(99,102,241,0.3)',
    }}>
      {/* Price */}
      <div style={{ marginBottom: 32 }}>
        <span style={{ color: '#94a3b8', fontSize: 28 }}>{currency} </span>
        <span style={{ color: 'white', fontSize: 96, fontWeight: 900 }}>{price}</span>
        <span style={{ color: '#94a3b8', fontSize: 28 }}>{period}</span>
      </div>

      {/* Features */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 40 }}>
        {features.map((f, i) => {
          const delay = triggerFrame + 20 + i * 8;
          const fOpacity = interpolate(frame - delay, [0, 12], [0, 1], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
          });
          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 12, opacity: fOpacity }}>
              <span style={{ color: '#22c55e', fontSize: 24 }}>✓</span>
              <span style={{ color: '#e2e8f0', fontSize: 24 }}>{f}</span>
            </div>
          );
        })}
      </div>

      {/* CTA */}
      <div style={{
        backgroundColor: '#6366f1',
        color: 'white',
        fontSize: 28,
        fontWeight: 700,
        padding: '18px 0',
        borderRadius: 12,
        textAlign: 'center',
      }}>
        {ctaText}
      </div>
    </div>
  );
};
```

## CTA (Call to Action) Screen

```tsx
const CTAScreen: React.FC<{ headline: string; url: string; buttonText: string }> = ({
  headline, url, buttonText,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headlineScale = spring({ frame, fps, config: { damping: 60 } });
  const urlOpacity = interpolate(frame, [20, 35], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const btnScale = spring({ frame: frame - 25, fps, config: { damping: 8, stiffness: 300 } });

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)',
      justifyContent: 'center',
      alignItems: 'center',
      flexDirection: 'column',
      gap: 32,
    }}>
      <h1 style={{
        color: 'white',
        fontSize: 80,
        fontWeight: 900,
        textAlign: 'center',
        margin: 0,
        transform: `scale(${headlineScale})`,
      }}>
        {headline}
      </h1>

      <div style={{
        backgroundColor: '#6366f1',
        color: 'white',
        fontSize: 40,
        fontWeight: 700,
        padding: '20px 60px',
        borderRadius: 16,
        transform: `scale(${btnScale})`,
        boxShadow: '0 0 40px rgba(99,102,241,0.6)',
      }}>
        {buttonText}
      </div>

      <div style={{ color: '#94a3b8', fontSize: 32, opacity: urlOpacity }}>
        {url}
      </div>
    </AbsoluteFill>
  );
};
```

## Apple-Style Product Video Structure

```tsx
// 60-second product hero video
<>
  {/* 0-3s: Black screen, product name fade in */}
  <Sequence from={0} durationInFrames={90}><BrandIntro /></Sequence>

  {/* 3-8s: Product reveal */}
  <Sequence from={90} durationInFrames={150}><ProductReveal productImage="product.png" productName="ProMax" /></Sequence>

  {/* 8-18s: Feature 1 callout */}
  <Sequence from={240} durationInFrames={300}><FeatureScene featureIndex={0} /></Sequence>

  {/* 18-28s: Feature 2 */}
  <Sequence from={540} durationInFrames={300}><FeatureScene featureIndex={1} /></Sequence>

  {/* 28-38s: Before/After */}
  <Sequence from={840} durationInFrames={300}><BeforeAfterReveal beforeSrc="before.mp4" afterSrc="after.mp4" /></Sequence>

  {/* 38-50s: Pricing */}
  <Sequence from={1140} durationInFrames={360}><PricingSection /></Sequence>

  {/* 50-60s: CTA */}
  <Sequence from={1500} durationInFrames={300}><CTAScreen headline="Coba Gratis 14 Hari" url="berkahkarya.org" buttonText="Mulai Sekarang →" /></Sequence>
</>
```

## Cross-References
- For Lottie animated icons (features): load `rules/ecosystem.md` → @remotion/lottie
- For Rive interactive animations: load `rules/ecosystem.md` → @remotion/rive
- For product reveal with motion blur: load `rules/effects.md` → @remotion/motion-blur
- For draw-on SVG underline/checkmark: load `rules/effects.md` → @remotion/paths
- For 3D product spin: load `rules/3d.md`
- For copy-paste scene templates: load `rules/ecosystem.md` → Clippkit / remocn
