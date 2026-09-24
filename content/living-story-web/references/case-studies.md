# Case studies

Worked examples of the thesis → asset pipeline → technique set → verification chain. These are archetypes, not templates: derive the thesis from the current project, never copy a prior brand, palette, or URL.

## 1. Manufacturing — material becoming product

- **Thesis:** make the production line feel like a single journey from raw material to finished product, leading to a "request a sample" CTA.
- **Asset pipeline:** flat illustration of the machine in layers (raw input, press, conveyor, finished product), separated with clean pivots for the press and belt.
- **Technique set:** scale journey (macro shot of material → full line reveal) plus unfolding (machine covers open as scroll deepens). One focal action at a time; the product panel is the readable hold.
- **Verification:** forward/reverse recording of the press stroke with no sliding parts; mobile recompose crops the belt, not the product; reduced motion collapses to a three-panel document flow.

## 2. Archive — nested histories

- **Thesis:** make the archive feel like opening a succession of nested drawers, each revealing an earlier layer of the record.
- **Asset pipeline:** layered archival documents with correct occlusion; panel borders authored as actual edges so a subject can cross them.
- **Technique set:** panel crossing (a document slips over a border into the next panel) plus match cut (the closing shape of one drawer matches the opening of the next).
- **Verification:** same progress always opens the same drawer — no flicker on reverse or anchor jump; keyboard users can reach every panel without the scrub.

## 3. Music — rhythm as changing space

- **Thesis:** make the track feel like a room that changes shape in time with the rhythm, leading to a listen action.
- **Asset pipeline:** single environment illustration plus secondary elements (light, dust, fixtures) that animate with smaller amplitude and different timing than the primary action.
- **Technique set:** convergence (several explanatory panels combine into one resolved room) with time-based damping so camera and environment stay synchronized.
- **Verification:** stop holds the primary action; secondary motion continues on a separate transform layer; pointer influence resets on leave.

## 4. Product app — one-camera explainer

- **Thesis:** make the workflow feel like a single continuous camera move from recognition to demonstration to resolution, leading to sign-up.
- **Asset pipeline:** existing product screens plus a lightweight rigged mascot or object; no full character art required.
- **Technique set:** match cut between screens (shared shapes carry the eye) plus a scale journey from detail to overview. Navigation and sign-up stay reachable without completing the story.
- **Verification:** critical flows (auth, forms, routes) still pass after the story layer is added; links resolve from one config source; no invented capabilities.

## Common failure signature

When a living-story build goes wrong, the symptom is usually one of:

- **Sliding cutout** — the character translates as one piece instead of articulating → no rig/sequence, or pose sheet used as smooth motion.
- **Foot skating** — feet slide on the ground while walking → no foot contact / weight transfer in the pose keys.
- **State drift** — a different frame at the same scroll position → state derived from accumulated events instead of normalized progress.
- **Frozen half-state** — reduced-motion user stuck on an intermediate scene → reduced path not authored, or treated as "pause at frame zero".

Each maps directly to a row in the [Anti-Rationalization Table](../SKILL.md) and a check in [Validation](validation.md).
