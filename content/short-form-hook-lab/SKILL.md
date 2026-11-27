---
name: short-form-hook-lab
description: Use when checking or ranking short-form opening lines (Reels, Shorts, TikToks) before shooting — five text-only heuristics with explicit limits for length and speakability, concrete markers, stakes, front-loading, and audience address. Use for hook drafts, hooks.txt batches, and pre-shoot triage. This is not a view predictor.
domain: content
category: content
subdomain: social-media
tags:
- hooks
- short-form
- reels
- shorts
- copywriting
- triage
version: 1.0.0
author: oyi77
license: MIT
triggers:
- "score this hook"
- "hook feedback"
- "rank these hooks"
- "first line of my reel"
---

# Short-Form Hook Lab

Text-only triage for opening lines: score one hook or a ranked batch in seconds, offline. Five heuristics — length/speakability, concrete markers, stakes, front-loading, audience address — each 0–100, plus an overall and a verdict. The tool kills greetings, preambles, and vague openers well and makes no claim about predicting reach.

Uses `hook_lab.py` (runnable, no deps beyond stdlib). For pacing and edits after the hook, use [video-editor](../video/editor/SKILL.md).

## Overview

Opening lines decide whether anyone hears the rest. This playbook runs five cheap, local checks before recording, then hands the verdict back to you. It deliberately does not claim to predict reach: real retention data from your own account is the only judge between two decent hooks.

## When to Use

- Reviewing a first line before recording, or ranking a batch of candidates.
- Killing a greeting, preamble, or content-free opener on evidence, not taste.
- Checking that a hook says something concrete within its first few words.

## When NOT to Use

- Predicting which hook will travel — no text model does that; retention graph wins.
- Judging full scripts, pacing, or edit — use [video-editor](../video/editor/SKILL.md).
- Platform policy, posting, or engagement automation — out of scope entirely.

## Workflow

### 1. Run it (repeatable, local)

```bash
python3 hook_lab.py hooks.txt          # one hook per line, ranked
python3 hook_lab.py --hook "I lost $18,000 because one missing contract."
python3 hook_lab.py hooks.txt --json   # machine-readable
```

stdin works (`pbpaste | python3 hook_lab.py -`). All scoring is local, text-only.

### 2. Read the verdict, then the weakest check

- STRONG ≥ 70 overall, no dealbreaker. OK 45–69. WEAK < 45, or any greeting/preamble/attention-demand (`hey`, `today`, `in this video`, `stop scrolling`). ABSTAIN = over-long or zero concrete markers — not an insult, a "can't judge from text".
- Check scores before overall: a 72 with CONCRETE 20 is a different problem than a 72 with FRONTLOAD 20.

### 3. Hand-edit, then re-run

The five checks name properties, not rewrites. A low number says "here is what to look at", not "delete this word". Re-run after edits; two rounds is normal, five says rewrite from a different idea, not iterate the same draft.

## Checks and score bands

| Check | Measures | Lower looks like |
|---|---|---|
| LENGTH | speakability window (≤ ~12 words ideal, −8/word past) | off-the-cuff rambling past 20 words |
| CONCRETE | numbers, money, proper nouns, spoken counts ("twenty grand") | abstract nouns only; "zero dollars" counted |
| STAKES | risk/loss/gain vocabulary | no reason to care beyond scrolling past |
| FRONTLOAD | payload early; greetings/preambles/attention-demands penalized | "Hey guys, today I wanted to talk about…" |
| AUDIENCE | explicit viewer ("you", "your") | unaddressed generality |

Scores are heuristics on a 0–100 band, not measurements of your actual retention. The scorer was **not** validated against your niche, your face, or your audience — do not pick between two decent hooks on 1–2 points.

## Common Pitfalls / Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "80 vs 79, shoot the 80" | Deltas under ~5 points are scoring noise; retention decides between decent hooks. |
| "Greeting scored high, so it works" | Dealbreaker logic floors FRONTLOAD and forces WEAK regardless of other checks. |
| "The tool predicts virality" | Text heuristics never saw your face, edit, audio, or distribution. Kill weak, trust the graph. |
| "ABSTAIN means the hook is bad" | Abstain means text can't evidence it (too long / no concrete marker) — judge by ear. |

## Verification

- [ ] Ran on a real batch or single hook; scores and verdict are consistent with the check table.
- [ ] Dealbreaker handling confirmed (greeting/preamble → WEAK, FRONTLOAD 0).
- [ ] Spoken numbers counted ("twenty grand", "zero dollars"); digits counted; "one"/"first" not counted.
- [ ] ABSTAIN path exercised on an over-long or marker-free hook.
- [ ] Output framed as triage; no reach/virality claim made to the user.
