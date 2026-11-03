---
name: build-design
description: "Use when building UI from a Figma file or design image to match the design using the project's existing tokens and components."
domain: content
author: jakubkrehel
license: MIT
subdomain: design
tags:
- figma
- design-to-code
- implementation
- ui-build
version: 1.0.0
category: content
triggers:
- "build-design"
- "figma to code"
- "build from design"
- "implement design"
---
# Build design

## Overview

Builds UI from a Figma file or design image so it matches the design, using the project's existing tokens and components. Reads the design at its source, builds with what the project already has, then compares.
## When to Use

You have a Figma file or design image and need UI that matches it, built with the project's existing tokens and components.


This skill turns a design into code that matches it. It reads the design at its source, builds with what the project already has, then compares the result against the design before calling it done.

The design decides. Values come from the design file, never from your taste or a pattern you liked elsewhere. A change the design does not show is a deviation, and a deviation is the user's call.

It owns no domain rules. Where the design breaks one, build it as designed and report the conflict with its owner. Contrast is a requirement in `better-accessibility` and a measurement in `better-colors`. Focus and semantics are `better-accessibility`, type is `better-typography` and spacing and structure are `better-layout`. Palette is `better-colors`, copy is `better-writing` and surfaces, icons and motion are `better-ui`. Reviewing finished work is `interface-review`, exploring alternatives is `variant` and stress testing a component is `break`.
The design decides; the floor does not. Before calling the build done, enforce `hallmark`'s non-waivable Floor (tokenized primitives, accessible contrast, viewport boundaries) and `impeccable`'s Craft Floor — a faithful build that violates the floor is still a defect.

## Workflow

1. Read the skill principles and references for the current task scope.
2. Apply the rules to the actual interface, code, or design under review.
3. Document findings or changes with evidence (file:line, measured values).
4. Verify against the project's existing conventions and constraints.
5. Report or implement the fix, never silently changing stack or taste.

## 1. Read the design at its source

A Figma link means the Figma MCP. Search the available and deferred tools for `figma` before saying it is unavailable, since the server often sits under a name you did not expect. A server that lists only an authenticate tool is connected but signed out, so ask the user to authenticate. With no Figma tool at all, ask the user to connect one, and do not build from memory or guesswork meanwhile. [figma.md](figma.md) holds which tools to call and what each returns.

A screenshot or exported image has no values to read. Sizes are ratios to the capture, so state the scale you assumed and treat every measurement as an estimate. Ask for the Figma link when one exists, since it replaces the whole estimate.

Scope the run to the frames named. Frames that show the same thing at different widths are one piece at several breakpoints, not separate pieces.

This step is done when you hold a screenshot of every frame in scope and its values for spacing, size, radius, color, type and the components used. From a Figma file they are exact. From an image they are estimates at the scale you stated.

## 2. Map the design onto the project

Read the project's tokens and component library before writing anything. Then map every design value to what exists:

| In the design | In code |
| --- | --- |
| A bound variable or style | The token with the same name or the same value |
| A raw value that equals a token | That token |
| A raw value with no token | The nearest existing token, listed in the report as rounded |
| A component instance | The project's component of that name, with the variant the design shows |
| A component instance with no project equivalent | Plain markup in place, listed as a deviation, and ask whether a component should exist |
| A one-off group of layers | Plain markup in place, not a new component |

Never add a token, a component variant or an arbitrary value to hit a number. Stop and ask which way to go when rounding would visibly change the design. That means more than 2px on spacing or size, or a color landing on a different step.

Check what data the design needs and wire it to what exists. Where the backend for part of it does not exist yet, build that part as UI fed by props and name it in the report as unwired.

## 3. Build only what the design shows

Implement the frames, the breakpoints the frames define and the states the file draws, such as hover, empty or error. A state the file does not draw is not yours to design. Leave it to the existing component's default and list it as missing.

Leave everything around the piece as it was. No neighbouring copy edits, no icon swaps, no "while I was here" cleanups. A diff wider than the design is the most common way this goes wrong.

## 4. Compare against the design

Render the build at each frame's width beside the design screenshot and walk it element by element. Compare the properties **Read the design at its source** collected. "Gap is 12px, design is 16px" is a finding. "Feels a bit tight" is not.

With a browser at hand, screenshot each width and compare. Without one, hand over the local URL with the widths to check and say the comparison is unverified. Do not report a match you did not look at.

Fix every mismatch you caused, then compare again. This step is done when every remaining difference is a rounding or a question.

## 5. Report and stop

| Element | Design | Built | Status |
| --- | --- | --- | --- |
| Card padding | 20px | `p-5` | Matches |
| Title size | 15px | `text-sm`, 14px | Rounded to token |
| Badge | Filled pill | Text label | Deviates, asked: no badge component exists |

Then list, one line each, and omit a list with nothing in it:

- **Unwired.** What renders from props until the backend exists.
- **Missing states.** What the design does not draw.
- **Domain conflicts.** Where the design breaks a rule, with the owning skill.

Close by saying where the build is running and at which widths you compared.

## Before you finish

| You notice | Fix |
| --- | --- |
| "Figma isn't connected" written before any tool search | Search the tools for `figma` first |
| Values in code that appear in no Figma response, only in the screenshot | Read them from the design context |
| An arbitrary utility such as `w-[343px]` or a raw hex in the diff | Map it to a token, or ask if rounding shows |
| A new file under the components directory for a frame that is not a component | Inline it as plain markup |
| A loading or error branch the design never drew | Remove it, keep the default and list it as missing |
| Files in the diff that no frame touches | Revert them |
| A contrast or focus change the design does not show | Restore the design and report the conflict with its owner |
| A comparison claimed with no screenshot of the build | Render each frame width, or say it is unverified |
| Hard-coded sample data with no mention in the report | List it under **Unwired** |

## When NOT to Use

- Pure backend logic with no UI/design considerations
- Tasks outside the scope of interface design and evaluation
- When a more specific skill already covers the exact need

## Verification

- [ ] Applied the skill's principles to the actual interface/code
- [ ] Verified changes against project conventions and constraints
- [ ] Checked for accessibility and usability issues where relevant
- [ ] Documented findings or changes clearly

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough for now" | Polish matters - small details compound into quality |
| "I'll fix it later" | Fix it now while context is fresh |
| "This is subjective" | Follow the principles and measurable criteria in this skill |
