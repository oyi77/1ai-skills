---
name: manim-math-animation
description: Use when producing programmatic math, science, or geometry animations with Manim — Scene structure, Mobject transforms, .animate syntax, LaTeX prerequisites, CLI render modes, and output verification. Use for explainers, proofs, and formula visualizations.
domain: content
category: content
subdomain: animation
tags:
- manim
- math
- animation
- python
- latex
- explainer
version: 1.0.0
author: oyi77
license: MIT
triggers:
- "manim animation"
- "animate a mathematical proof"
- "formula visualization"
- "geometry explainer video"
---

# Manim Math Animation

Manim renders precise programmatic animations from Python `Scene` classes. Use it when correctness of the math and the frame, not interaction, is the deliverable. Verify the CLI and LaTeX toolchain before promising a rendered result — Manim is commonly installed via `uv` and the docs require either an activated venv or a `uv run` prefix.

## Overview

A Manim project is code: one `Scene` class per video segment, `Mobject`s as visual objects, `self.play(...)` for timed transformations, `.animate` for method-based transforms. Text and formulas may require LaTeX (`Tex`, `MathTex`); plain text mobjects do not. Rendering is deterministic from source, so store the scene file with the output.

## When to Use

- Mathematical proofs, derivations, formula transformations, geometry demonstrations.
- Science explainers that need exact labels and consistent notation.
- Short looping visual explainers where Python source is the maintainable artifact.

## When NOT to Use

- Marketing sizzle, logo stings, or UI motion — use [hyperframes-motion-graphics](../hyperframes-motion-graphics/SKILL.md) or [motion-dev](../motion-dev/SKILL.md).
- Audio-reactive visuals — use [audio-reactive-animation](../audio-reactive-animation/SKILL.md).
- Live, interactive 3D — use [r3f-scene-stack](../r3f-scene-stack/SKILL.md).

## Workflow

### 1. Verify the toolchain before writing scenes

```bash
python3 -c "import manim; print(manim.__version__)"   # or: uv run python -c ...
manim --version                                        # or: uv run manim --version
```

If Manim was installed with `uv`, prefix every command with `uv run` or activate the venv. If the scene uses `Tex`/`MathTex`, verify a working LaTeX install; otherwise use `Text`/`VGroup` to avoid the dependency. Report clearly which path was verified — do not claim a render happened when the tool was absent.

### 2. Scaffold the project

Official quickstart: `manim init project my-project --default` (`uv run manim init project ...` when uv-managed). Keep one directory per project with scene source and rendered media in the project's own output tree. Track source in git; treat generated frames as artifacts.

### 3. Author the scene with verified syntax

Source-verified from Manim's official README and quickstart:

```python
from manim import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()                     # a Mobject
        circle.set_fill(PINK, opacity=0.5)    # style before animation
        self.play(Create(circle))
        self.wait(1)
```

For method-driven transforms, `.animate` wraps one method call per play (chaining multiple animate-steps in a single play is not a standard pattern — play them sequentially):

```python
from manim import *

class AnimateSquare(Scene):
    def construct(self):
        square = Square()
        self.play(Create(square))
        self.play(square.animate.shift(RIGHT * 2))
        self.play(FadeOut(square))
        self.wait()
```

Keep the math authoritative: write the derivation as comments or a companion note, then map each step to one animation. Do not let a pretty transform imply a false identity or step.

### 4. Render a low-quality preview first

Official quickstart uses `manim -p -ql example.py SquareToCircle` (preview + low quality). Equivalent with uv: `uv run manim -p -ql example.py SquareToCircle`. Confirm the specified scene class name matches the file's class exactly — a typo renders nothing and may be mistaken for a "fast render". Only after preview approval render the final quality preset.

### 5. Verify the output, not the command

- Confirm the output media file exists, opens, has non-zero duration, and shows all expected steps in the right order.
- Check formula legibility at final resolution; `Tex` output that is too small or clipped is a failed render even if the command exited 0.
- Check consistency of notation across scenes (same variables, colors, sign conventions).
- For caption/subtitle workflows, export word-level timing in a separate pipeline via [audio-reactive-animation](../audio-reactive-animation/SKILL.md) when narration is added.

## Common Pitfalls / Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "The command exited 0 so the animation is right" | Verify the file and watch it; class name typos and blank scenes also exit 0. |
| "I'll write the formula directly in the video" | Math must be authored and checked as math first; animation is presentation. |
| "LaTeX is probably installed" | Verify. `Tex`/`MathTex` fail at render time without it. |
| "I rendered at low quality, so it is basically done" | Preview is for structure; final resolution can clip formulas and labels. |
| "Manim is the right tool for a UI explainer" | It renders video, not interactive UI. Pick the engine by deliverable. |

## Verification

- [ ] Manim version verified via import/CLI; uv prefix used if needed.
- [ ] LaTeX availability verified or avoided with `Text`-only scenes.
- [ ] Preview rendered from the exact scene class name and visually checked.
- [ ] Final output file exists, opens, has non-zero duration, and all steps appear in order.
- [ ] Formula legibility, notation consistency, and resolution checked at final quality.
