---
name: humanizer
description: Use when transforming AI-generated text into natural, human-sounding prose — rewriting out robotic patterns, filler transitions, and symmetrical sentence structures while preserving meaning and facts.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- writing
- editing
- humanizer
- tone
- style
- ai-detection
version: 1.0.0
category: content
---

# Humanizer

Rewrite AI-generated text so it reads like a person wrote it. Preserves meaning and facts; changes only voice, rhythm, and word choice.

## When to Use

**Trigger phrases:**
- "humanize this" · "make this sound human" · "less robotic"
- "rewrite in my voice" · "natural-sounding"
- "pass AI detection" · "de-AI this"

**Use cases:**
- Blog posts and newsletters drafted by an LLM that need an editorial pass
- Marketing copy that reads too polished and symmetrical
- Email and social copy that needs conversational rhythm

## When NOT to Use

- Legal, medical, financial, or safety-critical text — precision beats voice
- Fact-heavy technical docs where hedging language ("furthermore", "it should be noted") carries meaning
- Translation — use `humanizer-zh` for Chinese
- Anything where you must not change the wording (contracts, citations)

## The Robot Patterns

AI text has recognizable tells. Hunt them:

| Tell | Example | Fix |
|---|---|---|
| Filler transitions | "Furthermore," "Moreover," "In addition," | Cut, or use "Also," / "Plus," / nothing |
| Hedge phrases | "It's important to note that", "It should be noted" | Delete; just state the thing |
| Symmetrical sentences | Three sentences, all ~20 words | Vary: 8 words. Then 30. Then 4. |
| Passive constructions | "The decision was made to…" | "We decided to…" |
| Empty intensifiers | "Very unique", "incredibly important" | Delete the intensifier or use a concrete detail |
| Perfect parallel triads | "fast, reliable, and scalable" | Break one out; make it concrete ("fast, reliable, and it fits on a laptop") |
| Rule-of-three openers | "In today's fast-paced world…" | Delete the whole sentence |
| Generic wrap-ups | "In conclusion, X is a powerful tool…" | End on a specific point or a call to action |

## Workflow

### 1. Read the draft and mark the tells

Skim once. Highlight every filler transition, hedge phrase, and symmetrical run. Don't rewrite yet — just see the shape.

### 2. Rewrite paragraph by paragraph

For each paragraph:

- **Vary sentence length.** Mix short (≤8 words), medium (15–20), and one long (25–30). No three-in-a-row of the same length.
- **Use contractions.** "It is" → "it's", "do not" → "don't" — unless the register is formal.
- **Prefer active voice.** Subject, verb, object.
- **Cut 20–30% of words.** First pass always over-writes.
- **Add one concrete detail** per paragraph (a number, a name, a specific verb) where the AI was vague.

### 3. Check the openings

AI loves to open with "In today's…", "In the world of…", or a definition. Replace with a specific image, a claim, or a question. First line should earn the second.

### 4. Read it aloud

If you stumble, the sentence is too long or the rhythm is wrong. Break it.

### 5. Spot-check the meaning

Diff the humanized version against the original for:
- Facts, numbers, names, dates — unchanged
- No new claims added
- No claims dropped that the reader needs

## Example

**Before (AI):**
> Furthermore, it is important to note that in today's fast-paced digital landscape, businesses must adapt their content strategies in order to remain competitive. Moreover, artificial intelligence tools can significantly enhance productivity and efficiency across various content workflows. In addition, teams that embrace these technologies will be better positioned for future success.

**After (human):**
> Content teams that don't adapt will lose. AI tools make them faster — a 3-hour newsletter draft becomes 40 minutes — but only if people keep editing. The tool writes the first draft; you write the version people read.

**What changed:** 63 words → 42. Cut all three filler transitions. Broke the symmetrical triad. Added a concrete number (3 hours → 40 minutes). Active voice. Ends on a point, not a summary.

## Optional: persona overlay

When a target voice is specified (e.g. the `persona:` field in frontmatter), apply the persona's principles on top: sentence rhythm, favorite constructions, what they'd cut. Don't impersonate a real named person unless that's authorized — use the persona as a *style lens*, not a claim of authorship.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "AI detection scores are the goal" | Optimizing for a detector makes prose worse. Optimize for the reader; detection follows. |
| "More edits = more human" | Over-editing makes it choppy. Aim for natural, not fragmented. |
| "I can keep the filler, it's harmless" | "Furthermore" is a signal to the reader that a machine wrote this. Cut it. |
| "Facts can shift slightly" | No. Meaning and facts are frozen; only voice changes. |

## Verification

- [ ] All facts, numbers, names, dates unchanged from source
- [ ] No new claims introduced
- [ ] Sentence lengths vary (no 3-in-a-row of same length)
- [ ] Filler transitions and hedge phrases removed
- [ ] Read aloud without stumbling
- [ ] Register matches the brief (formal / conversational / marketing)
