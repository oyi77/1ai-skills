---
name: google-flow
description: Use when navigating and operating Google Flow (labs.google/fx/tools/flow) - an AI video generation tool. Helps
  with project management, scenebuilder interface, prompt entry, preset selection, model configuration, and video generation
  workflow.
domain: productivity
tags:
- flow
- google
- productivity
- time-management
- tools
- video
- workflow
---
persona:
  name: "Domain Expert"
  title: "Master of Google Flow"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Google Flow Skill

## Overview

Google Flow is an AI video generation tool that creates videos from text prompts using Google's Veo 3.1 model. This skill provides detailed automation guidance for the Flow interface.

**Access**: https://labs.google/fx/tools/flow  
**Model**: Veo 3.1 - Fast  
**Credit Cost**: 20 credits per generation (with 1 output)

## When to Use

**Trigger phrases:**
- "google flow"
- "When generating AI videos from text prompts"
- "When automating Google Flow project management"
- "When configuring video generation settings"


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
1. Receive input and validate format
2. Route to appropriate handler based on input type
3. Execute core operation with monitoring
4. Transform output to expected format
5. Return results or trigger follow-up actions


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
This section covers key element selectors for the google-flow skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


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
This section covers credit management for the google-flow skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


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
- Core operation execution with comprehensive error handling
- Input validation and output quality assurance
- Integration with existing workflows and toolchains
- Detailed logging for debugging and audit trails


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

## Downloading Videos for Local Use
This section covers downloading videos for local use for the google-flow skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Overview

Download generated videos to use with other skills/agents (e.g., sending via Telegram, editing, uploading to social media).

### Step 1: Locate Generated Video

**In Asset Panel**:
```javascript
// Find video elements in the asset panel
const videos = document.querySelectorAll('video, [role="img"]');
// Videos appear after generation completes
```

**Video Card Elements**:
- Thumbnail preview
- Download button (download icon)
- Video metadata (duration, timestamp)

### Step 2: Download Video via UI

**Click Download Button**:
```javascript
// Find and click download button for specific video
const downloadButtons = Array.from(document.querySelectorAll('button'))
  .filter(b => {
    const icon = b.querySelector('i');
    return icon && (icon.innerText === 'download' || icon.innerText === 'file_download');
  });

// Click the first download button
if (downloadButtons[0]) {
  downloadButtons[0].click();
}
```

**Expected Behavior**:
- Browser download dialog appears
- Video downloads to default Downloads folder
- Filename format: `flow-video-{timestamp}.mp4`

### Step 3: Download Video Programmatically

**Extract Video URL**:
```javascript
// Get video source URL from video element
async function getVideoUrl() {
  const videoElement = document.querySelector('video');
  if (videoElement) {
    return videoElement.src || videoElement.querySelector('source')?.src;
  }
  return null;
}
```

**Download with Custom Filename**:
```javascript
// Download video with specific filename
async function downloadVideo(filename = 'google-flow-video.mp4') {
  const videoUrl = await getVideoUrl();
  if (!videoUrl) {
    return 'No video found';
  }
  
  // Fetch video blob
  const response = await fetch(videoUrl);
  const blob = await response.blob();
  
  // Create download link
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  
  // Cleanup
  URL.revokeObjectURL(url);
  
  return `Downloaded: ${filename}`;
}

// Usage
await downloadVideo('ocean-waves-sunset.mp4');
```

### Step 4: Save to Specific Directory

**Using Browser Automation**:
```javascript
// Download and save to specific path
// Note: This requires browser automation with file system access
async function downloadToPath(videoUrl, savePath) {
  const response = await fetch(videoUrl);
  const arrayBuffer = await response.arrayBuffer();
  const buffer = Buffer.from(arrayBuffer);
  
  // Save using Node.js fs (in automation context)
  // fs.writeFileSync(savePath, buffer);
  
  return `Saved to: ${savePath}`;
}
```

**Recommended Save Location**:
```
/Users/paijo/Downloads/google-flow-videos/
  ├── ocean-waves-2026-02-16.mp4
  ├── mountain-sunset-2026-02-16.mp4
  └── coffee-steam-2026-02-16.mp4
```

### Step 5: Integration with Other Skills

**Example: Send via Telegram**:
```javascript
// Complete workflow: Generate → Download → Send
async function generateAndSendVideo(prompt, telegramChatId) {
  // 1. Generate video
  await generateVideo(prompt);
  
  // 2. Wait for completion (60-90s)
  await new Promise(r => setTimeout(r, 90000));
  
  // 3. Download video
  const videoPath = `/Users/paijo/Downloads/google-flow-videos/${Date.now()}.mp4`;
  await downloadToPath(await getVideoUrl(), videoPath);
  
  // 4. Use with telegram skill
  // await sendTelegramVideo(telegramChatId, videoPath);
  
  return videoPath;
}
```

**Example: Batch Download Multiple Videos**:
```javascript
// Download all videos in current project
async function downloadAllVideos() {
  const videos = document.querySelectorAll('video');
  const downloads = [];
  
  for (let i = 0; i < videos.length; i++) {
    const videoUrl = videos[i].src;
    const filename = `flow-video-${i + 1}-${Date.now()}.mp4`;
    await downloadVideo(filename);
    downloads.push(filename);
    
    // Wait between downloads
    await new Promise(r => setTimeout(r, 1000));
  }
  
  return downloads;
}
```

---

## Creating Longer Videos
This section covers creating longer videos for the google-flow skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Overview

Google Flow generates short videos (~5-10 seconds). Create longer videos through:
1. **Video Stitching** - Combine multiple clips sequentially
2. **Frame-to-Video** - Extend duration using image sequences

### Method 1: Video Stitching (Recommended)

**Concept**: Generate multiple related clips and stitch them together.

**Step 1: Plan Video Sequence**:
```javascript
// Define scenes for a longer narrative
const scenes = [
  "Opening shot: Aerial view of a coastal highway at sunrise",
  "Medium shot: Red sports car driving along the coast",
  "Close-up: Car wheels on wet pavement",
  "Wide shot: Car approaching a cliff overlook",
  "Final shot: Car parked at overlook, ocean in background"
];
```

**Step 2: Generate Each Clip**:
```javascript
// Generate all clips sequentially
async function generateVideoSequence(scenes) {
  const videoFiles = [];
  
  for (let i = 0; i < scenes.length; i++) {
    // Generate clip
    await generateVideo(scenes[i]);
    
    // Wait for completion
    await new Promise(r => setTimeout(r, 90000));
    
    // Download clip
    const filename = `scene-${i + 1}.mp4`;
    await downloadVideo(filename);
    videoFiles.push(filename);
    
    // Small delay before next generation
    await new Promise(r => setTimeout(r, 5000));
  }
  
  return videoFiles;
}
```

**Step 3: Stitch Videos Using FFmpeg**:
```bash
# Create file list
cat > filelist.txt << EOF
file 'scene-1.mp4'
file 'scene-2.mp4'
file 'scene-3.mp4'
file 'scene-4.mp4'
file 'scene-5.mp4'
EOF

# Concatenate videos
ffmpeg -f concat -safe 0 -i filelist.txt -c copy final-video.mp4

# Result: ~25-50 second video (5 clips × 5-10s each)
```

**Step 4: Automated Stitching Function**:
```javascript
// Complete workflow: Generate sequence and stitch
async function createLongVideo(scenes, outputFilename) {
  // 1. Generate all clips
  const clips = await generateVideoSequence(scenes);
  
  // 2. Create ffmpeg command
  const fileList = clips.map(f => `file '${f}'`).join('\n');
  
  // 3. Execute stitching (requires shell access)
  // const command = `echo "${fileList}" > filelist.txt && ffmpeg -f concat -safe 0 -i filelist.txt -c copy ${outputFilename}`;
  // await executeShellCommand(command);
  
  return {
    clips: clips,
    output: outputFilename,
    totalClips: clips.length,
    estimatedDuration: `${clips.length * 7}s (approx)`
  };
}

// Usage
await createLongVideo(scenes, 'coastal-drive-full.mp4');
```

### Method 2: Frame-to-Video Extension

**Concept**: Use Google Flow's image-to-video mode to extend existing clips.

**Step 1: Extract Key Frames**:
```bash
# Extract last frame from video
ffmpeg -sseof -1 -i scene-1.mp4 -update 1 -q:v 1 last-frame.jpg

# Extract first frame from video
ffmpeg -i scene-1.mp4 -vframes 1 first-frame.jpg
```

**Step 2: Generate Extension Clips**:
```javascript
// Switch to Image-to-Video mode in Google Flow
async function generateFromFrame(frameImagePath, prompt) {
  // 1. Switch to "Images" tab
  const imagesTab = Array.from(document.querySelectorAll('button'))
    .find(b => b.innerText === 'Images');
  if (imagesTab) imagesTab.click();
  
  // 2. Upload frame image
  // (Upload functionality varies by UI)
  
  // 3. Enter continuation prompt
  await enterPrompt(prompt);
  
  // 4. Generate
  clickByText('Create');
}

// Usage
await generateFromFrame(
  'last-frame.jpg',
  'Continue the ocean wave motion, slow and peaceful'
);
```

**Step 3: Stitch Original + Extension**:
```bash
# Combine original clip with extension
ffmpeg -f concat -safe 0 -i <(echo "file 'original.mp4'"; echo "file 'extension.mp4'") -c copy extended.mp4
```

### Method 3: Looping for Duration

**Create Seamless Loops**:
```javascript
// Generate loop-friendly video
const loopPrompt = "Seamless loop: Ocean waves gently rolling, perfect loop, continuous motion";
await generateVideo(loopPrompt);
```

**Repeat Video N Times**:
```bash
# Loop video 5 times for longer duration
ffmpeg -stream_loop 4 -i ocean-loop.mp4 -c copy ocean-extended.mp4

# Result: 5× original duration
```

### Video Stitching Best Practices

1. **Maintain Consistency**:
   - Use same aspect ratio for all clips
   - Keep similar lighting/color grading
   - Use same style preset

2. **Smooth Transitions**:
   - Plan scene flow logically
   - Use transition prompts: "fade to...", "cut to..."
   - Consider overlap frames

3. **Credit Efficiency**:
   - Generate all clips in one session
   - Use 1 output per scene
   - Total cost: 20 credits × number of scenes

4. **Quality Control**:
   - Review each clip before stitching
   - Re-generate poor quality clips
   - Test stitched video for continuity

### Example: 60-Second Video Production

```javascript
// Complete workflow for 1-minute video
async function create60SecondVideo(topic) {
  // 1. Define 8 scenes (8 × 7s ≈ 56s)
  const scenes = [
    `Opening: ${topic} establishing shot, cinematic`,
    `Scene 2: ${topic} detail shot, slow motion`,
    `Scene 3: ${topic} wide angle, dramatic lighting`,
    `Scene 4: ${topic} close-up, shallow depth of field`,
    `Scene 5: ${topic} medium shot, natural movement`,
    `Scene 6: ${topic} aerial view, sweeping motion`,
    `Scene 7: ${topic} artistic angle, golden hour`,
    `Closing: ${topic} final shot, fade to black`
  ];
  
  // 2. Generate all scenes
  console.log('Generating 8 scenes...');
  const clips = await generateVideoSequence(scenes);
  
  // 3. Stitch together
  console.log('Stitching clips...');
  await createLongVideo(clips, `${topic}-60s.mp4`);
  
  // 4. Return result
  return {
    topic: topic,
    scenes: 8,
    totalCredits: 160, // 8 × 20
    outputFile: `${topic}-60s.mp4`,
    duration: '~56 seconds'
  };
}

// Usage
await create60SecondVideo('ocean-sunset');
```

---

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |


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
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


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
This section covers best practices for the google-flow skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


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


## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Automation creates duplicate entries across connected platforms
- Agent does not handle timezone differences correctly
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] No duplicate entries are created across connected platforms
- [ ] Timezone handling is correct for all scheduling operations
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `content/gemini-image-generator` - For static image generation
- `marketing/content-creator` - For video content strategy
- `productivity/google-canvas` - For collaborative brainstorming
- **Video Editing**: Use FFmpeg for stitching downloaded clips
- **Telegram Integration**: Send generated videos via messaging apps
- **Social Media**: Upload to platforms using automation skills

---

**Last Updated**: 2026-02-16  
**Tested**: ✅ Video generation successful (20 credits, 60s generation time)  
**Model**: Veo 3.1 - Fast

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
