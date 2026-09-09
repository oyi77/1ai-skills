---
name: hyperframes-pr-to-video
description: "Turn a GitHub pull request into a changelog, feature-reveal, fix, or refactor explainer video using HyperFrames. Use when the user provides a PR URL, owner/repo#N ref, or says 'this PR'. Reads diff via gh CLI, visualizes code changes as animated diffs with narration. Teaches diff parsing, change visualization, and technical storytelling."
domain: "content-creation"
tags:
  - hyperframes
  - pr-to-video
  - changelog
  - github
  - code-diff
  - feature-reveal
  - developer-content
version: "1.0.0"
author: "oyi77"
subdomain: "video-production"
type: "content"
---

# HyperFrames — PR to Video

A GitHub pull request → changelog / feature-reveal / fix / refactor explainer. Read via `gh` CLI, visualized as animated code diffs with narration.

## When to Use

- User provides a **PR URL** (`github.com/owner/repo/pull/123`)
- User provides a **`owner/repo#N` ref**
- User says **"this PR"** (current branch's PR)
- User wants a **feature-reveal** video for a merged PR
- User wants a **changelog** video for a release

## When NOT to Use

- User wants a product launch from a website (use `hyperframes-product-launch-video`)
- User wants a weekly digest (use `hyperframes-changelog-video`)
- No PR involved (use `hyperframes-faceless-explainer`)

## Workflow

### 1 · Fetch the PR

```bash
gh pr view 123 --json title,body,files,additions,deletions,author
gh pr diff 123 > pr-123.diff
```

Extract: title, description, files changed, lines added/removed, author.

### 2 · Classify the change

- **Feature:** new files, new functions → feature-reveal arc
- **Fix:** bug reference, test changes → before/after arc
- **Refactor:** moved code, no behavior change → simplification arc
- **Chore:** deps, config → brief mention or skip

### 3 · Plan the story

- **Hook (0-3s):** What changed in one sentence
- **Context (3-8s):** Why it mattered (the problem)
- **Diff walkthrough (8-20s):** Animated code diff, key hunks highlighted
- **Result (20-25s):** Before/after, metrics if available
- **CTA (25-30s):** Link to PR, try it out

### 4 · Visualize the diff

Render code hunks as styled blocks with line-level highlighting:

```html
<div class="clip diff-scene" data-start="8" data-duration="12" data-track-index="1">
  <div class="diff-header">src/auth.ts — +42 / -18</div>
  <pre class="diff-added">+ function verifyToken(token) {</pre>
  <pre class="diff-removed">- function checkAuth(req) {</pre>
</div>
```

### 5 · Render

```bash
npx hyperframes render --output pr-123-reveal.mp4
```

## Anti-Rationalization Table

| Rationalization | Reality |
|----------------|---------|
| "I'll show the entire diff" | Pick 2-3 key hunks — full diffs are unreadable on video |
| "I'll skip the context" | Viewers need the WHY before the WHAT |
| "I'll use tiny monospace" | 24px+ for code, highlight don't wallpaper |
| "I'll skip the author credit" | Credit the author — it's their work |

## Verification

- [ ] PR fetched via `gh` CLI (title, files, diff)
- [ ] Change classified (feature/fix/refactor/chore)
- [ ] Story arc matches classification
- [ ] Only 2-3 key hunks visualized
- [ ] Code readable at video resolution (24px+)
- [ ] Author credited
