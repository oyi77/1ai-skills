---
name: google-flow
description: Use when navigating and operating Google Flow (labs.google/fx/tools/flow) - an AI video generation tool. Helps with project management, scenebuilder interface, prompt entry, preset selection, model configuration, and video generation workflow.
---

# Google Flow Skill

## Overview

Google Flow is an AI video generation tool that creates videos from text prompts using Google's Veo model. This skill guides automation of the Flow interface.

## When to Use

- When generating AI videos from text prompts
- When automating Google Flow project management
- When configuring video generation settings
- When building video scenes programmatically

## When NOT to Use

- When you need image generation (use gemini-image-generator)
- When you don't have Google Flow access
- When credits are low/empty

## Quick Reference

**Access:** https://labs.google/fx/tools/flow

**Workflow:**
1. Access Flow
2. Create/select project
3. Enter prompt
4. Configure settings
5. Generate video

## Common Mistakes

- Not checking credit balance before generating
- Using wrong aspect ratio for intended use
- Not saving intermediate results
- Skipping prompt refinement iterations

## Prerequisites

- Active Google account with Google Flow access at https://labs.google/fx/tools/flow
- Chrome browser with OpenClaw extension attached
- Credits available (each generation uses credits)

## Core Workflow

### 1. Access Flow

```
Navigate to: https://labs.google/fx/tools/flow
```

### 2. Project Management

**List existing projects:**

```browser
action: open
targetUrl: https://labs.google/fx/tools/flow
```

Shows project cards with:
- Date created (e.g., "Feb 14 - 09:22")
- Edit project button (pencil icon)
- Delete project button (trash icon)

**Create new project:**

```browser
action: open
targetUrl: https://labs.google/fx/tools/flow/project/new
```

Steps:
1. Click "New project" button (add_2 icon)
2. Click "Edit project" button in breadcrumb
3. Enter project name in textbox
4. Click "Save to Project" button

**Navigate to Scenebuilder:**

Click "Scenebuilder" button in breadcrumb navigation.

### 3. Scenebuilder Interface Elements

**Navigation Breadcrumb:**
- Flow (link to home)
- Project name (with edit button)
- Scenebuilder button

**Media Type Tabs:**
- "Videos" (default, selected)
- "Images" (alternative mode)

**Generation Controls (Left Panel):**

| Element | Ref | Purpose |
|---------|-----|---------|
| Mode dropdown | combobox | "Text to Video" |
| Model selector | button | "Veo 3.1 - Fast" |
| Aspect ratio | icon | "crop_9_16" = Portrait (9:16) |
| Output count | text | "x2" = 2 outputs per prompt |
| Settings button | button | tune/Settings |
| Prompt textbox | textbox | "Generate a video with text…" |
| Clear prompt | button | restart_alt/Clear prompt |
| Expand button | button | pen_spark/Expand |
| Create button | button | arrow_forward/Create |

**Asset Panel (Right Side):**
- Search clips textbox
- View toggles: cozy, grid_on, favorite
- Placeholder: "Type in the prompt box to start"

### 4. Generating Videos

**Basic Text-to-Video:**

```
1. Click prompt textbox ref
2. Type descriptive prompt
3. Click "Create" button
```

**Prompt Tips:**
- Be specific about subjects, actions, environments
- Include camera movements ("slow pan", "tracking shot")
- Describe lighting and mood
- Mention style ("cinematic", "documentary", "animated")

**Configuration via Settings:**

Click Settings (tune icon) to configure:
- **Aspect Ratio**: Portrait (9:16), Landscape (16:9), Square (1:1)
- **Outputs per prompt**: 1-4 videos (default: 2)
- **Model**: Veo 3.1 - Fast (default)
- **Credits**: Shows cost per generation

**💡 Credit-Saving Tip:**
For testing or single video needs, change **"Outputs per prompt" from 2 to 1** in Settings before generating. This halves the credit cost (5 credits vs 10 credits).

**Using Presets (via Expand):**

Click "Expand" button (pen_spark) to access style presets:
- Cinematic Preset
- Film Noir Preset
- Action Figure Preset
- Create New Expander (custom)

Each preset applies consistent visual style to prompts.

### 5. Managing Generated Videos

**View Videos Tab:**
- Select "Videos" radio button
- Clips appear in asset panel
- Search clips: use textbox + search button

**View Modes:**
- Cozy view (list with details)
- Grid view (thumbnails)
- Favorites view (starred clips)

**Actions per clip:**
- Preview
- Download
- Favorite
- Delete

## Advanced Workflows

### Batch Generation

1. Open project in Scenebuilder
2. Enter first prompt
3. Configure settings
4. Generate (uses credits)
5. Modify prompt for variation
6. Generate again

### Project Organization

1. Create named projects for different video series
2. Use consistent naming: "Client-Campaign-Date"
3. Delete old tests to clean up

### Credit Management

- Check "10 credits" link in Settings (shows current cost)
- Each generation costs credits based on settings
- Default: Portrait 9:16 x2 outputs = 10 credits
- **Save credits**: Reduce to x1 output = 5 credits (recommended for testing)
- Higher resolution/more outputs = more credits

## Common UI Interactions

**Click Elements:**
```
action: act
request:
  kind: click
  ref: {element_reference}
```

**Type Text:**
```
action: act
request:
  kind: type
  ref: {textbox_reference}
  text: "prompt text here"
```

**Press Key:**
```
action: act
request:
  kind: press
  key: Escape  # close dialogs
```

## Troubleshooting

**"There doesn't seem to be a project here…"**
- Project needs to be named and saved first
- Click "Edit project" → enter name → "Save to Project"

**Create button disabled**
- Prompt textbox is empty
- Type a description first

**Settings not opening**
- Check if another dialog is open
- Press Escape and try again

**Videos not appearing**
- Generation takes time
- Check Notifications (alt+T region)
- Verify credits available

## URL Patterns

| Action | URL |
|--------|-----|
| Home | /fx/tools/flow |
| New Project | /fx/tools/flow/project/new |
| Existing Project | /fx/tools/flow/project/{uuid} |
| Help | https://support.google.com/googleone?p=g1_ai_credit_menu |

## Reference Screenshots

See `assets/flow-screenshot-main.png` for complete UI layout.
See `assets/flow-screenshot-expanded.png` for preset panel view.
