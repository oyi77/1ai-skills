---
name: emil-design-skills
description: Collection of 8 design engineering skills by Emil Kowalski (Vercel, Linear) — animation standards, UI craft, Apple
  design principles, library selection, and prototyping. Based on years of production experience. Use when the user asks about
  UI polish, animation decisions, or wants to audit/improve interface motion.
domain: content
author: mahipal
license: MIT
subdomain: ui-design
tags:
- design
- animation
- ui
- motion
- css
- frontend
- prototyping
- apple-design
- craft
version: 1.0.0
depends_on:
- emil-design-eng
- review-animations
- improve-animations
- find-animation-opportunities
- animation-vocabulary
- apple-design
- pick-ui-library
- prototype
---
persona:
  name: "Emil Kowalski"
  title: "The Design Engineer — UI Craft Authority"
  expertise: ['Animation Design', 'UI Components', 'Design Systems', 'Motion Engineering', 'Frontend Architecture']
  philosophy: "Taste is trained, not innate. Unseen details compound into something stunning."
  credentials: ['Design Engineer at Vercel', 'Design Engineer at Linear', 'Creator of Sonner, cmdk, vaul', 'Author of animations.dev']
  principles: ['Default to flagging; approval is earned', 'Right easing for the right moment', 'Sub-300ms for UI motion', 'Motion must be justified, not decorative']

# Emil Kowalski — Skills for Design Engineers

**Upstream:** [github.com/emilkowalski/skills](https://github.com/emilkowalski/skills)  
**Stars:** 23K+ · **License:** MIT  
**Author:** Emil Kowalski — [@emilkowalski](https://github.com/emilkowalski) · [animations.dev](https://animations.dev/) · [emilkowal.ski](https://emilkowal.ski/ui/agents-with-taste)

---

## Why These Skills Exist

> "Agents don't have great taste."

Emil built these skills because AI agents consistently pick wrong animation ingredients — `ease-in` for enter animations (should be `ease-out`), solid borders instead of semi-transparent shadows, wrong timing curves. These skills encode his years of experience at Vercel and Linear into actionable rules any agent can follow.

This is **domain expertise as code**. AI doesn't replace taste — it amplifies it when the taste is encoded.

---

## When to Use

**Trigger phrases:**
- "improve the animations in this project"
- "audit the UI motion"
- "what library should I use for X?"
- "design this UI with Apple-level polish"
- "review these animation changes"
- "help me pick between animation approaches"
- "prototype this UI component in multiple ways"

**Use when:**
- Building UI that needs to feel polished, not just functional
- Reviewing animation/motion PRs
- Choosing frontend libraries for a new project
- Designing gesture-driven or spring-based interactions
- Looking for where motion adds value (and where it doesn't)
- You want your agent to build interfaces that stand out from AI slop

**Don't use for:**
- General code review (non-motion changes)
- Brand/graphic design (logos, illustrations)
- Backend or infrastructure decisions

---

## How to Use

1. **Identify the task** — Match the trigger phrases above (motion review, UI polish, library selection, prototyping)
2. **Pick the relevant skill** — Load the individual SKILL.md from `skills/` for the specific concern (animation review, design philosophy, or prototyping)
3. **Load dependencies** — Install the `depends_on` skills for the selected skill (see Installation)
4. **Apply the rules** — Let the encoded rules drive the review or build; do not skip critique steps
5. **Verify** — Run the skill's Verification Checklist before declaring done

---

## The 8 Skills

### 1. emil-design-eng — Core Design Philosophy
**File:** `skills/emil-design-eng/SKILL.md`

The foundational skill. Encodes Emil's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great.

**Covers:**
- Core philosophy (taste is trained, unseen details compound)
- Building UI that users don't think about
- When and why to animate
- Component-level design decisions

**Invoke:** `emil-design-eng` in conversation when discussing UI decisions.

---

### 2. review-animations — Strict Animation Review
**File:** `skills/review-animations/SKILL.md`

A specialized reviewer that evaluates animation and motion code against a high craft bar. Reference: `STANDARDS.md` (loaded on demand for precise values).

**Covers:**
- 10 non-negotiable standards (justified motion, frequency-appropriate, responsive easing, sub-300ms, etc.)
- Easing curves, duration tables, spring config
- Gesture, clip-path, performance, accessibility rules
- Default to flagging — approval is earned

**Invoke:** `review-animations` or "review these animations".

---

### 3. improve-animations — Codebase Motion Audit
**File:** `skills/improve-animations/SKILL.md`

Advisor skill: surveys the codebase's animation and motion code, then produces a prioritized audit with self-contained implementation plans. Read-only — plans improvements but doesn't apply them.

**Covers:**
- Codebase-wide motion survey
- Prioritized finding hierarchy (blockers, high-impact, polish)
- Implementation plans precise enough for cheaper models to execute
- Red flags: transforms on non-composited properties, unnecessary JS animation, timing inconsistencies

**Invoke:** "improve the animations in this project" or "audit the motion in this codebase".

---

### 4. find-animation-opportunities — Motion Discovery
**File:** `skills/find-animation-opportunities/SKILL.md`

Sweeps an interface for moments that would genuinely benefit from motion — while rejecting everything that shouldn't animate. The defining trait is **restraint**.

**Covers:**
- Page transitions, skeleton loading, micro-interactions
- Hover → press → release animation chains
- What NOT to animate (reject most candidates)
- Precise recipes with exact timing and easing

**Invoke:** "what could be animated here?" or "make this feel more alive".

---

### 5. animation-vocabulary — Precise Motion Language
**File:** `skills/animation-vocabulary/SKILL.md`

Teaches agents the right vocabulary to describe animations precisely — so you get better results without trial-and-error prompting.

**Covers:**
- Complete easing vocabulary (ease-out, ease-in-out, overshoot, bounce, spring, etc.)
- Duration naming conventions (instant, fast, normal, slow, deliberate)
- Animation types (enter, exit, layout, hover, press, focus, drag, scroll, stagger)
- How to compose descriptions for LLM prompts

**Invoke:** `animation-vocabulary` or "help me describe this animation correctly".

---

### 6. apple-design — Apple's Design Principles for the Web
**File:** `skills/apple-design/SKILL.md`

Distills Apple's WWDC design talks — chiefly *Designing Fluid Interfaces* (WWDC 2018) — and translates them into web platform primitives.

**Covers:**
- Response: kill latency (respond on pointer-down, not release)
- Continuity: motion starts from current state, inherits velocity
- Physicality: springs, momentum, inertia, resistance
- Depth: translucent materials, layers, z-space
- Typography: optical sizing, tracking, leading
- Reduced-motion: respect system preferences

**Invoke:** `apple-design` when designing gesture-driven UI, spring animations, or sheet/drag interactions.

---

### 7. pick-ui-library — Curated Library Selection
**File:** `skills/pick-ui-library/SKILL.md`

Opinionated, taste-driven library recommendations for frontend tasks. No menu of options — one clear answer per task.

**Covers:** UI primitives (base-ui), command menus (cmdk), toasts (Sonner), OTP inputs (input-otp), charts, virtualization, drag-drop, state management, styling, animations (Motion), forms, tables, date pickers, and more.

**Invoke:** "what should I use for X?" or `pick-ui-library` with your task.

---

### 8. prototype — UI Variant Prototyping
**File:** `skills/prototype/SKILL.md`

Builds multiple genuinely different versions of a described UI piece, rendered behind a visual picker so you can flip through them live and choose a winner.

**Covers:**
- True divergence (not three tints of the same idea)
- Each variant meets the full craft bar
- Visual picker with live switching
- Export/promote the winning variant

**Invoke:** `prototype` or "show me multiple ways to build this UI".

---

## Installation

```bash
# Install a single skill via npm (example: pick-ui-library)
npx skills@latest add emilkowalski/skills pick-ui-library

# Install all skills
npx skills@latest add emilkowalski/skills

# Install to a specific agent root
npx skills@latest add emilkowalski/skills --root ~/.claude/skills
npx skills@latest add emilkowalski/skills --root ~/.copilot/skills
```

After install, each skill is loadable by name in conversation:

```
emil-design-eng
review-animations
improve-animations
find-animation-opportunities
animation-vocabulary
apple-design
pick-ui-library
prototype
```

---

## Skill Architecture

Each skill in this collection follows a strict pattern:

| Property | Description |
|----------|-------------|
| `disable-model-invocation: true` | Most skills only activate when explicitly named — they don't trigger on general conversation |
| Focus | Every skill does ONE thing and declines anything outside its scope |
| Operating Posture | Clear persona and bias statement at the top |
| Standards | Referenced via `STANDARDS.md` or inline — all values are concrete (e.g., "sub-300ms", "cubic-bezier(0.16, 1, 0.3, 1)") |
| Anti-patterns | Explicitly listed |

---

## Quality Comparison

| Dimension | Emil's Skills | Typical AI-generated Skills |
|-----------|-------------|---------------------------|
| Specificity | Exact CSS values, curves, durations | Vague principles |
| Scope | Single responsibility per skill | Kitchen-sink catch-alls |
| Authority | Production experience (Vercel, Linear) | Generic best-practice regurgitation |
| Taste | "Approve only what earns it" | "Here are your options" |
| Restraint | "Don't animate most things" | "Add animations everywhere" |

---

## References

- [Emil Kowalski — Agents With Taste](https://emilkowal.ski/ui/agents-with-taste)
- [Emil Kowalski — 7 Practical Animation Tips](https://emilkowal.ski/ui/7-practical-animation-tips)
- [Emil Kowalski — You Don't Need Animations](https://emilkowal.ski/ui/you-dont-need-animations)
- [Animations.dev](https://animations.dev/) — Emil's animation course
- [skills.sh](https://skills.sh/emilkowalski/skills) — skills.sh dashboard
- [Upstream repo](https://github.com/emilkowalski/skills)

---

## Verification Checklist

- [ ] User's problem is UI/design/animation related
- [ ] Specific skill matched to task (review vs improve vs find vs prototype)
- [ ] If using review-animations, STANDARDS.md loaded for precise values
- [ ] Installation via `npx skills@latest add emilkowalski/skills <name>` if skill not yet available
- [ ] Output follows the skill's operating posture (read-only where applicable)
- [ ] Animation recommendations include exact CSS values (easing, duration)
- [ ] Library recommendations are from the curated list, not generic
