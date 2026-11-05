# Provenance And Sourcing Notes

## Source
Upstream repo reviewed: `togg53192-cmd/jailbreaks` at `https://github.com/togg53192-cmd/jailbreaks` on 2026-11-05.

## License Status
The upstream repository publishes no `LICENSE` file (README only). Per this repo's convention for companion references, nothing was copied, and the source is credited by name and URL rather than by extracted text.

## Adoption Statement
Only the *technique taxonomy* was adopted — the structural family names and the description of the moves. No payload text, quoted sentences, headings, ordering, or code blocks were taken from the upstream corpus. This documents a technique class, not a jailbreak payload.

## Rejection Of The 40-File Payload Library
The source repo ships a model-versioned set of forty files (Opus v1/v2, Grok-4.7, Qwen-3.8, DeepSeek-4.1, and others). These payloads were deliberately not vendored. Model-specific payloads decay within weeks: a skill library that vendors them ships stale attacks within a quarter. The technique families survive because they target instruction hierarchy, which is architectural, not a model quirk. Stability comes from ignoring the text and documenting the moves.

## Family Names Taken From The Taxonomy
Two families were adopted:

1. **policy-layer impersonation** — an attack that targets the model's own alignment policy rather than the application's system prompt.
2. **anti-detector framing** — an attack that targets the metadata and reminder channel rather than the policy or content.

## How To Extend (Checklist)
Adding a new family requires all four items below, each written as full prose, not fragments:
1. A structural description of the attack with the distinguishing property stated explicitly.
2. One sanitized skeleton using `[PLACEHOLDER]` slots in a fenced code block. The skeleton must be visibly a skeleton.
3. A one-line detection hint telling a defender what to look for.
4. A one-line severity note on why the family is high-impact.

## Attribution & Origin Note
Upstream source: `togg53192-cmd/jailbreaks`, no license. Adopted on 2026-11-05 by ai-hacker. This document is a provenance record, not a copy; alternative phrasing such as "adapted from" is not permitted when no license is present.