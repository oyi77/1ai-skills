# The Viral Formula — What Makes Videos Sell & Go Viral

## Load This File First For Any Video Intended To Sell Or Go Viral

This is the **meta-layer** above all genre files. Every video that needs to perform — get shares, drive purchases, build audiences — must be built on these principles regardless of genre.

---

## The Algorithm Is The Audience

MrBeast's leaked production guide states it directly: *"Anytime you say the word 'algorithm,' replace it with 'audience.'"* The algorithm amplifies what humans respond to. Build for humans, the algorithm follows.

The three metrics that determine if a video succeeds:
1. **CTR** (Click-Through Rate) — does the thumbnail + title make people click?
2. **AVD** (Average View Duration) — how long do people watch?
3. **AVP** (Average View Percentage) — what % of the video do they finish?

Design every frame and every second to maximize all three.

---

## The Universal Viral Structure

Every format that reliably goes viral follows this shape:

```
HOOK (0–3s)     → Stop the scroll. State or show the payoff immediately.
TEASE (3–15s)   → Why should they keep watching? Plant the open loop.
ESCALATION      → Stakes rise continuously. Never stay flat.
RE-HOOK (3 min) → A second hook for people who almost left.
PAYOFF          → Deliver on every promise made in the hook.
CTA             → What do you want them to do next?
```

The **open loop** is the most important structural device: *"I'll show you the result at the end."* Once the brain opens a loop, it is neurologically compelled to close it.

---

## The 5-Second Hook Rule

Research across viral videos: the average time before a viral video delivers on its thumbnail promise is **7.2 seconds**. Your target is **5 seconds**.

```tsx
// Implement as: massive text + visual in first 5 seconds
const HOOK_RULES = {
  show:     'The most surprising/dramatic moment FIRST, then explain how',
  text:     'Bold, large, high-contrast text overlay visible within 2 frames',
  audio:    'No silence in the first 5 seconds — music or speech immediately',
  format:   '9:16 vertical fills the entire phone screen — no wasted space',
  question: 'Open a loop: "You won\'t believe what happened when..."',
};
```

### Hook Formulas That Work

```tsx
// The Curiosity Gap
"I tried X for 30 days. The results were shocking."
"What happens when you [unexpected premise]?"

// The Stakes Reveal
"Last person to [action] wins [prize]."
"$1 vs $1,000,000 [thing] — can you spot the difference?"

// The Transformation Promise
"I went from [bad state] to [good state] in [time]."
"Watch how [ordinary thing] becomes [extraordinary result]."

// The Counter-Intuitive Claim
"Why [common belief] is completely wrong."
"The [profession] thing nobody tells you about [topic]."

// The Relatability Hook
"POV: You [universal situation everyone recognises]."
"Tell me you're [type of person] without telling me you're [type]."
```

---

## The Retention Curve — Never Let It Drop

Platform algorithms measure retention at specific checkpoints. Design video events to fire BEFORE each drop-off point:

```tsx
const RETENTION_CHECKPOINTS = [
  { time: '0:00–0:05', danger: 'highest drop-off — hook must fire here' },
  { time: '0:30',      danger: 'first wave — re-establish stakes or reveal new info' },
  { time: '1:00',      danger: 'second wave — pattern interrupt needed' },
  { time: '3:00',      danger: 'mid-video crisis — the "re-hook" must fire HERE' },
  { time: '50%',       danger: 'algorithm checkpoint — must feel rewarding to reach' },
  { time: '80%',       danger: 'completion stretch — tease final payoff explicitly' },
];

// Pattern interrupts — fire every 60–90 seconds:
// - Cut to different camera angle / scene
// - Text overlay with a bold claim
// - Sound effect on a reveal
// - Change of music energy
// - Zoom in/out on key moment
// - Counter/progress graphic update
```

---

## Emotion → Action Map

Different emotions drive different viewer actions. Match your emotional target to your goal:

```tsx
const EMOTION_TO_ACTION = {
  // Drives SHARES
  awe:         'Show impossible scale, beauty, or skill',
  laughter:    'Unexpected subversions, relatable mishaps, absurd premises',
  anger:       'Injustice, hypocrisy, things that "should not be this way"',
  inspiration: 'Transformation, overcoming, proving doubters wrong',

  // Drives PURCHASES
  desire:      'Show the product making life better, more beautiful, more fun',
  fomo:        'Limited time, exclusive access, "everyone is doing this"',
  trust:       'Real person, real results, before/after, testimonial',
  relief:      'This solves the exact pain I have right now',

  // Drives FOLLOWS/SUBSCRIBERS
  curiosity:   'Recurring series, cliffhangers, "part 2 coming..."',
  belonging:   'Community identity, "people like us do things like this"',
  surprise:    'Subvert expectations at the moment they feel safe',
};
```

---

## Platform-Specific Optimisation

### Short-Form (TikTok / Reels / Shorts) — Completion King
```tsx
const SHORT_FORM = {
  duration:   '15–60 seconds optimal; under 30s for maximum completion rate',
  aspect:     '9:16 vertical, 1080×1920',
  hook:       '2-second hook — no intros, no logos, straight to content',
  captions:   'Always — 85% watched with sound off',
  loop:       'Design the video to loop — last frame → first frame seamlessly',
  trending:   'Use trending audio within 48 hours of it trending',
  text:       'Large, bold, center-bottom text for accessibility',
  cta:        '"Follow for part 2" or "Comment [word] and I\'ll send you..."',
};
```

### Long-Form YouTube — Retention Architecture
```tsx
const LONG_FORM = {
  duration:    '8–15 minutes sweet spot for ad revenue + watch time',
  thumbnail:   'High contrast, face with strong emotion, 3 words max',
  title:       'Curiosity gap + number: "I Did X For Y Days (Results Shocked Me)"',
  chapters:    'Add YouTube chapters — signal value at each timestamp',
  reHook:      'At 2:30–3:00, explicitly say what\'s coming: "In a moment I\'ll show you..."',
  endscreen:   'Last 20 seconds: recommend next video to watch',
  description: 'Put key info + links in first 3 lines (visible without "show more")',
};
```

### Live Shopping / TikTok Shop — Direct Conversion
```tsx
const LIVE_COMMERCE = {
  structure:  'Demo → Testimonial → Scarcity → Price Reveal → CTA',
  urgency:    'Real countdown timers, limited stock counters',
  social:     'Read comments live, address objections in real time',
  offer:      'Exclusive live-only discount or bundle',
  repetition: 'Repeat the CTA every 60–90 seconds for new viewers joining',
};
```

---

## The Virality Stack — Build These Into Every Video

Priority order — implement from top down:

```tsx
const VIRALITY_STACK = [
  // TIER 1 — Non-negotiable
  'Hook in first 3 seconds — no exceptions',
  'Open loop that resolves at the end',
  'Captions/subtitles always',
  'Pattern interrupt every 60–90 seconds',
  'Payoff that delivers on the hook promise',

  // TIER 2 — High impact
  'Escalating stakes throughout (never plateau)',
  'Sound design: music lifts, hits on cuts, silence for emphasis',
  'Text overlays on key moments — reinforce the spoken word',
  'Progress indicator (timer, counter, bar) — visual commitment device',
  'Emotional arc: tension → release → tension → release → BIG release',

  // TIER 3 — Viral multipliers
  'The "wow factor" — something NO other creator could do at your level',
  'Shareability trigger — end with something people will text to a friend',
  'Community bait — ask a question viewers argue about in comments',
  'Cliffhanger / Part 2 tease — give them a reason to follow',
  'Authenticity signal — one unpolished moment to break the "ad" feeling',
];
```

---

## Video Length By Goal

| Goal | Length | Format |
|------|--------|--------|
| Viral share bait | 15–30s | Short-form, loop-able |
| Product awareness | 30–60s | Short-form with hook |
| Product conversion | 60–90s | Demo + testimonial + CTA |
| Trust building | 3–8 min | Story-driven, documentary |
| Deep education | 8–20 min | YouTube, chapter-marked |
| Community building | 10–30 min | Long-form YouTube/podcast |
| Live commerce | 30–120 min | Live stream |

---

## The Sales Video Formula (AIDA → PASM)

Classic AIDA is not enough for video. The modern sales video follows **PASM**:

```
P — PAIN:       Show the problem viscerally. Make them feel it.
A — AGITATE:    Make it worse. Show consequences of NOT solving it.
S — SOLUTION:   Reveal the product/service as the inevitable answer.
M — MOMENTUM:   Urgency + social proof + risk reversal → CTA.
```

```tsx
// Time allocation for a 90-second sales video
const PASM_TIMING = {
  pain:       { start: 0,  end: 15,  pct: '17%' },  // hook IS the pain
  agitate:    { start: 15, end: 35,  pct: '22%' },  // make it worse
  solution:   { start: 35, end: 70,  pct: '39%' },  // demo the product
  momentum:   { start: 70, end: 90,  pct: '22%' },  // proof + urgency + CTA
};
```

---

## Remotion Implementation: The Viral Framework Component

```tsx
// Universal viral video wrapper — apply to any genre
export const ViralVideoWrapper: React.FC<{
  children: React.ReactNode;
  showProgressBar?: boolean;
  showCaptions?: boolean;
  hookText?: string;
  targetPlatform?: 'tiktok' | 'youtube' | 'instagram' | 'universal';
}> = ({
  children,
  showProgressBar = true,
  hookText,
  targetPlatform = 'universal',
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  const progress = frame / durationInFrames;

  // Hook text appears in first 3 seconds
  const hookOpacity = interpolate(
    frame,
    [0, 6, fps * 3, fps * 3 + 10],
    [0, 1, 1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  return (
    <AbsoluteFill>
      {children}

      {/* Progress bar — visual commitment device */}
      {showProgressBar && (
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0,
          height: 3, backgroundColor: 'rgba(255,255,255,0.2)', zIndex: 200,
        }}>
          <div style={{
            height: '100%',
            width: `${progress * 100}%`,
            backgroundColor: '#ff4500',
            transition: 'none',
          }} />
        </div>
      )}

      {/* Hook text overlay */}
      {hookText && (
        <div style={{
          position: 'absolute',
          top: '12%', left: 0, right: 0,
          textAlign: 'center',
          padding: '0 40px',
          opacity: hookOpacity,
          zIndex: 190,
        }}>
          <div style={{
            display: 'inline-block',
            backgroundColor: 'rgba(0,0,0,0.75)',
            color: 'white',
            fontSize: targetPlatform === 'tiktok' ? 72 : 56,
            fontWeight: 900,
            padding: '12px 28px',
            borderRadius: 12,
            lineHeight: 1.2,
          }}>
            {hookText}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
```

---

## Which Genre To Load Next

Once you've read this file and understand the viral principles, load the genre-specific file:

| Goal | Primary Genre | Combine With |
|---|---|---|
| Go viral on TikTok/Reels | `genres/influencer.md` | `genres/ugc.md` |
| Sell a product | `genres/product.md` | `genres/ugc.md` |
| Build brand trust | `genres/documentary.md` | `genres/promo.md` |
| Entertain + go viral | `genres/challenge.md` | `genres/influencer.md` |
| Educate + build authority | `genres/education.md` | `genres/talk.md` |
| News / explainer | `genres/news.md` | `genres/promo.md` |
| Sensory / calming viral | `genres/asmr.md` | `genres/mv.md` |
| Gaming / esports content | `genres/gaming.md` | `genres/influencer.md` |
| Comedy / sketch | `genres/comedy.md` | `genres/influencer.md` |
