---
name: video-strategy-orchestrator
description: "Decides WHEN to use Remotion, HyperFrames, AI video generation, or a hybrid of all three. Use when building video production pipelines, choosing a video tool for a task, or when the user asks 'which video tool should I use?'. Evaluates input type, complexity, determinism needs, and output format to pick the right engine — or combine them. Read BEFORE starting any video production task in the 1ai ecosystem."
domain: "content-creation"
tags:
  - video
  - strategy
  - orchestrator
  - remotion
  - hyperframes
  - ai-video
  - hybrid
  - pipeline
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
---

# Video Strategy Orchestrator

Decides **when** to use Remotion, HyperFrames, AI video generation, or a hybrid. Evaluates input, complexity, determinism needs, and output format to pick the right engine.

## When to Use

- User asks **"which video tool should I use?"**
- User wants to **build a video pipeline** and needs to choose the engine
- User has a **video task** and the tool is unspecified
- User wants to **combine multiple video tools** in one pipeline
- You're starting a video task in 1ai-content and need to decide the approach

## When NOT to Use

- User explicitly names a tool (e.g., "use Remotion")
- User wants a specific HyperFrames workflow (use `video-production-orchestrator`)
- Task is clearly FFmpeg-only (format conversion, compression)

## Workflow

### 1 · Identify input type

What is the source material?
- Existing React component → lean Remotion
- Product URL or brief → lean HyperFrames
- Text/article/topic → lean HyperFrames
- Text/image prompt → lean AI Video
- Existing footage → lean HyperFrames (talking-head-recut)

### 2 · Assess determinism need

- **High** (pixel-exact, branded, template-based) → Remotion or HyperFrames
- **Low** (creative, varied, experimental) → AI Video

### 3 · Evaluate complexity

- **Complex logic/conditionals** → Remotion
- **Medium (DOM + CSS)** → HyperFrames
- **Simple (prompt only)** → AI Video

### 4 · Check for hybrid opportunity

Can combining engines produce a better result?
- AI generates content + HyperFrames adds timing → HYBRID
- Remotion template + HyperFrames overlays → HYBRID

### 5 · Route and justify

State the chosen engine(s) and why (one sentence).

## The Three Engines

### 1. Remotion (React-Based Rendering)

**What:** React components → video via headless Chrome + FFmpeg

**Strengths:**
- Component reusability (React ecosystem)
- Complex logic (hooks, state, conditional rendering)
- Type safety (TypeScript)
- Existing template library (`ProductAd.tsx`, `ProductAd-Hook`)
- Deterministic output

**Weaknesses:**
- React learning curve for agents
- Verbose for simple animations
- Harder to generate from scratch via LLM
- Bundle size (React + Remotion runtime)

**Best for:**
- Template-based product ads (existing compositions)
- Videos requiring complex logic/conditionals
- When you have a React component library
- When TypeScript safety matters

### 2. HyperFrames (HTML→MP4)

**What:** HTML + CSS + seekable animations → deterministic MP4

**Strengths:**
- Agent-native (LLMs write HTML best)
- Simpler than React for most video tasks
- Built-in transition catalog (cut-the-curve, zoom-through, etc.)
- Design system support (frame.md)
- Lower-level control (direct DOM manipulation)

**Weaknesses:**
- No component model (plain HTML files)
- Manual state management
- Less suited for complex interactivity
- Newer ecosystem (fewer templates)

**Best for:**
- Product launch videos from URLs
- Motion graphics and kinetic type
- Talking-head recut with overlays
- Faceless explainers
- Changelog/digest videos
- When the agent generates the composition

### 3. AI Video Generation (Prompt-Based)

**What:** Text/image prompt → AI-generated video

**Strengths:**
- Creative output (invented visuals)
- No manual animation work
- Fast iteration (prompt → video)
- Good for abstract/conceptual content

**Weaknesses:**
- Stochastic (different output each time)
- Limited control over exact timing
- No deterministic output (can't pixel-match)
- Provider-dependent quality
- Cost per generation

**Best for:**
- Creative/experimental content
- Abstract explainers
- Social media content (variety over precision)
- When exact timing doesn't matter

## Decision Matrix

| Factor | Remotion | HyperFrames | AI Video |
|--------|----------|-------------|----------|
| **Input type** | React component | HTML/template | Text/image prompt |
| **Determinism** | High | High | Low |
| **Complexity** | High (hooks, state) | Medium (DOM + CSS) | Low (prompt only) |
| **Agent-friendliness** | Medium | High | High |
| **Reusability** | High (components) | Medium (templates) | Low (prompts) |
| **Timing control** | Frame-exact | Frame-exact | Approximate |
| **Existing templates** | Yes (ProductAd) | Yes (frame presets) | N/A |
| **Best for** | Template-based ads | Agent-generated videos | Creative/experimental |

## When to Use Each

### Use Remotion When:
- You have an existing React composition (e.g., `ProductAd.tsx`)
- The video requires complex logic (conditional rendering, data fetching)
- You need TypeScript safety
- You're extending an existing Remotion project
- The user explicitly asks for Remotion

### Use HyperFrames When:
- The agent generates the composition from scratch
- You need a product launch video from a URL
- You want motion graphics, kinetic type, or logo stings
- You need a talking-head recut with overlays
- You want a faceless explainer
- You need a changelog/digest video
- The user wants HTML-based video

### Use AI Video Generation When:
- The content is abstract or conceptual
- Exact timing doesn't matter
- You want creative variety (multiple versions)
- The user provides a prompt, not a script
- You're generating social media content (TikTok/Reels)
- The user says "generate a video from this idea"

## When to Combine (Hybrid Pipelines)

### Pattern 1: AI → HyperFrames (Enhance AI output)

**Use when:** Generate base content with AI, then add precise timing/overlays with HyperFrames.

```
1. AI video generation → base footage
2. HyperFrames → add kinetic captions, lower-thirds, brand overlays
3. FFmpeg → final assembly
```

**Example:** Generate an explainer with AI, then add synced captions and a branded intro/outro with HyperFrames.

### Pattern 2: Remotion → HyperFrames (Template + Overlay)

**Use when:** Render a Remotion composition, then overlay with HyperFrames.

```
1. Remotion → render product ad (deterministic, branded)
2. HyperFrames → add talking-head overlay, captions, or data callouts
3. FFmpeg → composite layers
```

**Example:** Render a `ProductAd` with Remotion, then add a talking-head narrator and captions with HyperFrames.

### Pattern 3: HyperFrames → AI (Fill gaps)

**Use when:** Build the structure with HyperFrames, then fill gaps with AI-generated content.

```
1. HyperFrames → build intro, outro, and transition structure
2. AI video → generate middle scenes (abstract/experimental)
3. HyperFrames → stitch everything together with precise timing
```

**Example:** Create a branded intro/outro with HyperFrames, generate the middle explainer content with AI, then assemble with HyperFrames transitions.

### Pattern 4: AI → Remotion (Data-driven templates)

**Use when:** Generate data/content with AI, then render with Remotion templates.

```
1. AI → generate product descriptions, pricing, reviews
2. Remotion → render ProductAd template with AI-generated data
3. Output → deterministic, branded video
```

**Example:** Scrape product reviews with AI, then render a Remotion product ad with the data.

## Routing Logic

```
START: What's the input?
├── Existing React component → REMOTION
├── Product URL + "launch video" → HYPERFRAMES (product-launch-video)
├── Existing footage + "add graphics" → HYPERFRAMES (talking-head-recut)
├── Text/article + "explainer" → HYPERFRAMES (faceless-explainer)
├── "motion graphics" / "logo sting" → HYPERFRAMES (motion-graphics)
├── "changelog" / "digest" → HYPERFRAMES (changelog-video)
├── "captions" / "subtitles" → HYPERFRAMES (embedded-captions)
├── Text prompt + "creative" → AI VIDEO GENERATION
├── "social media" + "variety" → AI VIDEO GENERATION
├── Need precise timing + creative content → HYBRID (AI + HyperFrames)
├── Have template + need overlays → HYBRID (Remotion + HyperFrames)
└── Unclear → Ask: "Do you need precise timing or creative variety?"
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll always use HyperFrames, it's agent-native" | Remotion is better for existing React templates |
| "I'll always use AI, it's faster" | AI is stochastic — bad for precise timing |
| "I'll always use Remotion, it's more powerful" | HyperFrames is simpler for agent-generated content |
| "I'll use all three for every video" | Over-engineering — pick the minimum viable engine |
| "I'll skip the orchestrator and just pick one" | Wrong tool = wasted effort. Evaluate deliberately. |
| "Hybrid is always better" | Hybrid adds complexity — only combine when necessary |

## Verification

- [ ] Input type identified (component, URL, text, prompt)
- [ ] Determinism requirement assessed (high/low)
- [ ] Complexity evaluated (simple/medium/complex)
- [ ] Engine chosen with justification
- [ ] If hybrid, combination pattern documented
- [ ] User didn't have to pick the tool (orchestrator decided)
