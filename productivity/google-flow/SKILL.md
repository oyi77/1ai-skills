---
name: google-flow
description: Use when navigating and operating Google Flow (labs.google/fx/tools/flow) - an AI video generation tool. Helps with project management, scenebuilder interface, prompt entry, preset selection, model configuration, and video generation workflow.
---

# Google Flow Skill

## Overview

Google Flow is an AI video generation tool that creates videos from text prompts using Google's Veo 3.1 model. This skill provides detailed automation guidance for the Flow interface.

**Access**: https://labs.google/fx/tools/flow  
**Model**: Veo 3.1 - Fast  
**Credit Cost**: 20 credits per generation (with 1 output)

## When to Use

- When generating AI videos from text prompts
- When automating Google Flow project management
- When configuring video generation settings
- When building video scenes programmatically

## When NOT to Use

- When you need image generation (use `content/gemini-image-generator`)
- When you don't have Google Flow access
- When credits are low/empty

---

## Complete Video Generation Workflow

### Step 1: Navigate to Google Flow

```
URL: https://labs.google/fx/tools/flow
```

**Expected State**: Flow home page with existing projects or "New project" button

### Step 2: Create New Project

**Method 1: Click Button**
```javascript
// Find and click "New project" button
const buttons = Array.from(document.querySelectorAll('button'));
const newProjectButton = buttons.find(b => b.innerText.includes('New project'));
if (newProjectButton) {
  newProjectButton.click();
}
```

**Method 2: Direct Navigation**
```
URL: https://labs.google/fx/tools/flow/project/new
```

**Result**: Redirects to Scenebuilder view with default project name (e.g., "Feb 16 - 23:39")

### Step 3: Rename Project (Optional but Recommended)

**Click Edit Project Button**:
```javascript
// Click the pencil (edit) icon next to project name
const editButton = document.querySelector('button[aria-label="Edit project"]') || 
                   Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('edit'));
if (editButton) {
  editButton.click();
}
```

**Type New Name**:
```javascript
// Type project name (input field appears after clicking edit)
// Example: "Ocean Waves Video"
```

**Save Project Name**:
- Click checkmark icon to save
- Or press Enter to confirm

### Step 4: Configure Settings (Optimize Credits)

**Open Settings Dialog**:
```javascript
// Click Settings (tune) icon
const tuneButton = Array.from(document.querySelectorAll('i, span, button'))
  .find(el => el.innerText === 'tune');
if (tuneButton) {
  tuneButton.click();
}
```

**Settings Panel Options**:
- **Aspect Ratio**: Portrait (9:16), Landscape (16:9), Square (1:1)
- **Outputs per prompt**: 1, 2, 3, or 4 videos
  - **Default**: 2 outputs = 40 credits
  - **Recommended**: 1 output = 20 credits (saves 50% credits)
- **Model**: Veo 3.1 - Fast (default)

**Change Outputs to 1** (Credit Saving):
```javascript
// Find and click the "1" option for outputs
// This reduces cost from 40 to 20 credits per generation
```

**Close Settings**:
- Click outside the dialog
- Or press Escape key

### Step 5: Enter Video Prompt

**Click Prompt Textarea**:
```javascript
// Focus the main prompt input
const promptTextarea = document.getElementById('PINHOLE_TEXT_AREA_ELEMENT_ID');
if (promptTextarea) {
  promptTextarea.focus();
  promptTextarea.click();
}
```

**Alternative Selector**:
```javascript
// Find by placeholder text
const textarea = document.querySelector('textarea[placeholder*="Generate a video"]');
```

**Type Your Prompt**:
```javascript
// Example prompt
const prompt = "A peaceful ocean wave rolling onto a sandy beach at golden hour";
promptTextarea.value = prompt;

// Or use browser_press_key to type naturally
```

**Prompt Writing Tips**:
- Be specific about subjects, actions, environments
- Include camera movements: "slow pan", "tracking shot", "aerial view"
- Describe lighting and mood: "golden hour", "dramatic lighting", "soft shadows"
- Mention style: "cinematic", "documentary", "animated", "photorealistic"
- Specify duration hints: "slow motion", "time-lapse"

**Example Prompts**:
```
"A serene mountain landscape at sunset with clouds moving slowly across the sky"
"A close-up of a coffee cup with steam rising, cinematic lighting"
"An aerial view of a winding river through a forest, slow pan"
"A time-lapse of a flower blooming, macro photography style"
```

### Step 6: Generate Video

**Click Create Button**:
```javascript
// Find and click the Create button (arrow_forward icon)
const createButton = Array.from(document.querySelectorAll('button'))
  .find(b => b.innerText.includes('Create') || b.querySelector('i')?.innerText === 'arrow_forward');
if (createButton) {
  createButton.click();
}
```

**Alternative Method**:
```javascript
// Direct selector for Create button
const createBtn = document.querySelector('button:has(i:contains("arrow_forward"))');
```

**Expected Behavior**:
1. Button becomes disabled
2. Progress indicator appears
3. Percentage counter shows progress: "1%... 23%... 62%... 100%"
4. Generation typically takes 60-90 seconds

### Step 7: Monitor Generation Progress

**Progress Indicators**:
- Percentage counter in UI
- Progress bar animation
- Notification area updates

**Wait for Completion**:
```javascript
// Wait for generation to complete (60-90 seconds typical)
// Progress will show: 1% → 100%
```

**Check for Notifications**:
- Credit usage notification appears
- Example: "30 credits left" (if started with 50)

### Step 8: View Generated Video

**Video Appears in Asset Panel**:
- Right side panel shows generated video(s)
- Thumbnail preview available
- Click to play full video

**Video Actions**:
- **Preview**: Click thumbnail to play
- **Download**: Click download icon
- **Favorite**: Click star icon
- **Delete**: Click trash icon

---

## Key Element Selectors

### Critical Elements

| Element | Selector | Alternative |
|---------|----------|-------------|
| Prompt Textarea | `#PINHOLE_TEXT_AREA_ELEMENT_ID` | `textarea[placeholder*="Generate a video"]` |
| Create Button | `button:has(i:contains("arrow_forward"))` | Button with text "Create" |
| Settings Button | `button:has(i:contains("tune"))` | Button with "Settings" text |
| New Project Button | Button with text "New project" | - |
| Edit Project Button | `button[aria-label="Edit project"]` | Button with `edit` icon |

### JavaScript Helper Functions

```javascript
// Click element by text content
function clickByText(text) {
  const buttons = Array.from(document.querySelectorAll('button'));
  const button = buttons.find(b => b.innerText.includes(text));
  if (button) button.click();
  return button;
}

// Click element by icon name
function clickByIcon(iconName) {
  const elements = Array.from(document.querySelectorAll('i, span, button'));
  const element = elements.find(el => el.innerText === iconName);
  if (element) element.click();
  return element;
}

// Type in prompt textarea
function enterPrompt(promptText) {
  const textarea = document.getElementById('PINHOLE_TEXT_AREA_ELEMENT_ID');
  if (textarea) {
    textarea.focus();
    textarea.value = promptText;
    return true;
  }
  return false;
}

// Generate video (complete workflow)
async function generateVideo(promptText) {
  // 1. Enter prompt
  enterPrompt(promptText);
  
  // 2. Wait a moment
  await new Promise(r => setTimeout(r, 500));
  
  // 3. Click Create
  clickByText('Create');
  
  return 'Video generation started';
}
```

---

## Credit Management

### Credit Costs (as of Feb 2026)

| Configuration | Credits per Generation |
|---------------|------------------------|
| 1 output, Portrait 9:16 | 20 credits |
| 2 outputs, Portrait 9:16 | 40 credits |
| 3 outputs, Portrait 9:16 | 60 credits |
| 4 outputs, Portrait 9:16 | 80 credits |

**Recommendation**: Use 1 output for testing and iteration to save credits.

### Check Credit Balance

**View in Settings**:
- Open Settings (tune icon)
- Credit cost shown at bottom
- Example: "20 credits" per generation

**After Generation**:
- Notification shows remaining credits
- Example: "30 credits left"

### Credit Optimization Tips

1. **Start with 1 output**: Test prompts with single output first
2. **Iterate prompts**: Refine prompt before generating multiple outputs
3. **Use presets**: Leverage style presets for consistency
4. **Delete failed attempts**: Clean up to avoid confusion

---

## Advanced Features

### Using Style Presets

**Access Presets**:
```javascript
// Click Expand button (pen_spark icon)
clickByIcon('pen_spark');
```

**Available Presets**:
- **Cinematic Preset**: Film-like quality with depth of field
- **Film Noir Preset**: Black and white, high contrast
- **Action Figure Preset**: Toy-like aesthetic
- **Create New Expander**: Custom style preset

**Apply Preset**:
1. Click "Expand" button
2. Select preset from list
3. Preset applies to current and future prompts

### Aspect Ratio Selection

**Available Ratios**:
- **Portrait (9:16)**: Vertical video, ideal for mobile/social
- **Landscape (16:9)**: Horizontal video, standard widescreen
- **Square (1:1)**: Equal dimensions, social media friendly

**Change Aspect Ratio**:
```javascript
// Click aspect ratio icon in settings
// Icon shows current ratio: crop_9_16, crop_16_9, crop_square
```

### Model Selection

**Current Model**: Veo 3.1 - Fast (default and only option)

**Future Models**: May include quality vs. speed tradeoffs

---

## Troubleshooting

### Common Issues

**Issue**: Create button is disabled
- **Cause**: Prompt textarea is empty
- **Solution**: Enter a text prompt first

**Issue**: "There doesn't seem to be a project here…"
- **Cause**: Project not saved
- **Solution**: Click "Edit project" → enter name → save

**Issue**: Settings dialog won't open
- **Cause**: Another dialog is already open
- **Solution**: Press Escape to close dialogs, then try again

**Issue**: Video generation stuck at low percentage
- **Cause**: Network issue or server load
- **Solution**: Wait 2-3 minutes, refresh page if needed

**Issue**: "Not enough credits"
- **Cause**: Credit balance too low
- **Solution**: Purchase more credits or reduce outputs per prompt

**Issue**: Video quality is poor
- **Cause**: Vague or unclear prompt
- **Solution**: Add more specific details about scene, lighting, camera movement

---

## Complete Automation Example

### Generate Video from Scratch

```javascript
// Complete workflow: Create project and generate video
async function createVideoProject(projectName, videoPrompt) {
  // 1. Navigate to new project
  window.location.href = 'https://labs.google/fx/tools/flow/project/new';
  await new Promise(r => setTimeout(r, 3000)); // Wait for page load
  
  // 2. Rename project
  const editBtn = document.querySelector('button[aria-label="Edit project"]');
  if (editBtn) {
    editBtn.click();
    await new Promise(r => setTimeout(r, 500));
    // Type project name here
  }
  
  // 3. Configure settings (1 output to save credits)
  const tuneBtn = Array.from(document.querySelectorAll('i, span, button'))
    .find(el => el.innerText === 'tune');
  if (tuneBtn) {
    tuneBtn.click();
    await new Promise(r => setTimeout(r, 1000));
    // Select 1 output option
    // Close settings
  }
  
  // 4. Enter prompt
  const textarea = document.getElementById('PINHOLE_TEXT_AREA_ELEMENT_ID');
  if (textarea) {
    textarea.focus();
    textarea.value = videoPrompt;
  }
  
  // 5. Generate
  const createBtn = Array.from(document.querySelectorAll('button'))
    .find(b => b.innerText.includes('Create'));
  if (createBtn) {
    createBtn.click();
  }
  
  return 'Video generation started';
}

// Usage
createVideoProject(
  "Ocean Sunset",
  "A peaceful ocean wave rolling onto a sandy beach at golden hour, cinematic slow motion"
);
```

---

## Best Practices

### Prompt Engineering

1. **Start specific**: "A red sports car" → "A red Ferrari 458 driving on a coastal highway"
2. **Add camera work**: "slow pan left", "tracking shot", "aerial view"
3. **Describe lighting**: "golden hour", "soft morning light", "dramatic sunset"
4. **Include motion**: "waves crashing", "leaves falling", "clouds drifting"
5. **Specify style**: "cinematic", "documentary", "animated", "photorealistic"

### Project Organization

1. **Name projects clearly**: "Client-Campaign-Date" format
2. **One project per concept**: Keep related videos together
3. **Delete test projects**: Clean up failed attempts
4. **Use favorites**: Star best outputs for easy access

### Credit Efficiency

1. **Test with 1 output**: Iterate prompts before bulk generation
2. **Refine prompts**: Get it right before generating multiple versions
3. **Use presets**: Maintain consistency without re-prompting
4. **Monitor balance**: Check credits before large batches

---

## URL Patterns

| Action | URL |
|--------|-----|
| Home | https://labs.google/fx/tools/flow |
| New Project | https://labs.google/fx/tools/flow/project/new |
| Existing Project | https://labs.google/fx/tools/flow/project/{uuid} |
| Help/Support | https://support.google.com/googleone?p=g1_ai_credit_menu |

---

## Reference Screenshots

See `assets/flow-screenshot-main.png` for complete UI layout.  
See `assets/flow-screenshot-expanded.png` for preset panel view.

---

## Related Skills

- `content/gemini-image-generator` - For static image generation
- `marketing/content-creator` - For video content strategy
- `productivity/google-canvas` - For collaborative brainstorming

---

**Last Updated**: 2026-02-16  
**Tested**: ✅ Video generation successful (20 credits, 60s generation time)  
**Model**: Veo 3.1 - Fast
