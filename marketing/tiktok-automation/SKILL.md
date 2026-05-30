---
name: tiktok-automation
description: TikTok content posting automation with session persistence, dynamic element detection, and selector learning. Use when automatically uploading TikTok videos with captions and hashtags, setting up persistent browser sessions for login-free posting, learning TikTok's UI to handle changing selectors, implementing fallback mechanisms for reliable uploads, tracking upload progress with real-time updates, or scheduling TikTok content posting.
dependencies: - playwright
---


# TikTok Automation Skill 🎵

**Production-ready** automation untuk TikTok content posting & management.

## Overview

TikTok Automation Skill provides production-ready automation for TikTok content posting and management. It features automatic login with session persistence, dynamic element detection that adapts to TikTok's changing UI, selector learning that saves successful selectors for future use, robust fallback mechanisms that retry with alternative selectors when primary ones fail, real-time progress tracking for upload status, and comprehensive logging for debugging and auditing. This skill enables reliable automated content posting without manual intervention.

## When to Use

- **Auto-login with session persistence**: Maintain login sessions across sessions to avoid re-login
- **Content upload**: Post videos with captions, hashtags, and settings
- **Dynamic element detection**: Adapt to TikTok's changing class names and selectors
- **Selector learning**: Learn and save successful selectors to `selectors.json`
- **Fallback mechanism**: Retry with alternative selectors when primary ones fail
- **Progress tracking**: Real-time upload status updates during the process
- **Cross-platform posting**: Schedule posts for optimal timing
- **Bulk uploads**: Process multiple videos from a folder

## The Process

- Configure automatically, automation, browser, captions, changing settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Step 1: Session and Login

**Load Existing Session**:
```javascript
// Check for existing session
const sessionFile = 'tiktok-session.json';
const sessionData = fs.readFileSync(sessionFile, 'utf8');
const session = JSON.parse(sessionData);

// If session valid, skip login
if (session.isValid()) {
  await page.goto('https://www.tiktok.com/upload');
} else {
  await performLogin();
}
```

**Login Flow**:
1. Navigate to login page
2. Enter credentials
3. Handle 2FA if enabled
4. Save session to file
5. Store cookies for reuse

### Step 2: Navigate to Upload Page

```javascript
await page.goto('https://www.tiktok.com/upload');
await page.waitForSelector('#upload-area', { timeout: 30000 });
```

**Expected State**:
- Upload area visible
-Drag and drop zone present
- File input visible or hidden (depending on TikTok's current UI)

### Step 3: Dynamic Element Detection

**Multi-Strategy Selector Detection**:
```javascript
async function findElement(strategy, { timeout = 30000 } = {}) {
  switch (strategy) {
    case 'learned':
      return await findWithLearnedSelectors();
    case 'text':
      return await findWithTextContent();
    case 'structure':
      return await findWithDOMStructure();
    case 'role':
      return await findWithAccessibilityRole();
    default:
      return await findWithAllStrategies();
  }
}
```

### Step 4: Upload Video File

**File Upload Methods**:

**Method 1: Drag and Drop**
```javascript
await page.dragAndDrop(filePath, '#upload-area');
await page.waitForSelector('#upload-preview');
```

**Method 2: File Input**
```javascript
const fileInput = await findFileInput();
await fileInput.setInputFiles(filePath);
```

**Method 3: Form Submission**
```javascript
const form = await findUploadForm();
await form.append('video', filePath);
await form.submit();
```

### Step 5: Add Metadata

**Caption Input**:
```javascript
const captionInput = await findCaptionInput();
await captionInput.fill('Your caption Here 🎵 #viral #fyp');
```

**Hashtags**:
```javascript
// Add hashtags to caption or separate input
await page.type('#hashtag-input', '#viral #fyp #tiktok');
```

**Privacy Settings**:
```javascript
// Comment permissions
await findElement({ selector: '#allow-comments' }).click();

// Duet/ Stitch settings
await findElement({ selector: '#allow-duet' }).click();
```

### Step 6: Finalize and Publish

**Visibility Settings**:
```javascript
await page.select('#privacy', 'public'); // public, friends, private
await page.select('#duet-setting', 'everyone'); // everyone, friends, off
await page.select('#stitch-setting', 'everyone'); // everyone, friends, off
```

**Upload Process**:
```javascript
// Click publish button
await findElement({ text: 'Publish', selector: '[type="submit"]' }).click();

// Wait for upload confirmation
await page.waitForSelector('#upload-success', { timeout: 60000 });
```

### Step 7: Save Success and Update Selectors

**Learn Successful Selectors**:
```javascript
async function saveSuccessfulSelector(element, context) {
  const selectorData = {
    selector: element._selector,
    method: 'css' | 'xpath' | 'text',
    confidence: 0.95,
    lastUsed: new Date().toISOString(),
    fallbacks: []
  };
  
  fs.writeFileSync('selectors.json', JSON.stringify(selectorData, null, 2));
}
```

**Update Selector Database**:
```json
{
  "uploadButton": {
    "selector": "button[data-e2e='upload-button']",
    "method": "css",
    "confidence": 0.98,
    "lastUsed": "2026-02-18T22:00:00Z",
    "fallbacks": [
      {"selector": "button[type='file']", "method": "css"},
      {"text": "Upload", "method": "text"}
    ]
  }
}
```

## Common Patterns

**Scheduled Upload**:
```bash
# Upload with scheduling
./script.sh --video video.mp4 --caption "My video" --schedule "2026-02-20 10:00"
```

**Batch Upload**:
```bash
# Process all videos in folder
./script.sh --folder ./videos --caption-template "Check out {filename}"
```

**Quick Upload with Fallback**:
```bash
# Try learned selectors first, fallback to text detection
./script.sh --video video.mp4 --fallback text
```

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **❌ Session expired but re-login fails**: Credentials invalid or TikTok blocked account
- **❌ Selector learning stuck**: Upload never succeed to save new selectors
- **❌ Upload stuck at 0%**: File format issue or internet connectivity problem
- **❌ Caption input not found**: TikTok changed UI - run `--update-selectors`
- **❌ 2FA prompt appears**: Session file invalid or TikTok changed 2FA handling
- **❌ Video processing stuck**: TikTok servers busy - retry after queue
- **❌ Rate limit exceeded**: TikTok flagged automation - reduce frequency or change approach

## Verification

**Connection Tests**:
```bash
# Verify Playwright installation
node -e "require('playwright'); console.log('Playwright OK')"

# Check config validity
jq . config.json
```

**Functional Verification**:

1. **Session Persistence Test**:
   ```bash
   # First run - should login and create session
   ./script.sh --video video1.mp4 --caption "Test"
   
   # Second run - should use session, skip login
   ./script.sh --video video2.mp4 --caption "Test"
   # Verify: No login prompts, faster upload start
   ```

2. **Dynamic Detection Test**:
   ```bash
   ./script.sh --video video.mp4 --fallback dynamic
   
   # Verify: Multiple selector strategies tried in order
   # Check log for: "Trying learned selector...", "Fallback to text detection..."
   ```

3. **Selector Learning Test**:
   ```bash
   # After successful upload, check selector saved
   ./script.sh --video video.mp4 --caption "Test"
   
   # Verify selectors.json updated with new selectors
   cat selectors.json | jq '.uploadButton'
   ```

**Debug Options Test**:
```bash
# Verbose logging
./script.sh --video video.mp4 --verbose

# Headless mode (for CI/CD)
./script.sh --video video.mp4 --headless

# Slow motion (for debugging)
./script.sh --video video.mp4 --slow
```

**Output Verification**:

**Console Output**:
```
✓ Session loaded successfully
✓ Navigated to upload page
✓ Upload button found: [learned]
✓ Video uploaded successfully
✓ Metadata added: 150 characters
✓ Published at 2026-02-18 22:00:00
✓ Selector saved to selectors.json
```

**Log File Check**:
```bash
# Check persistent logs
tail -f tiktok-automation.log

# Verify log entries
grep -E "(✓|✗|ERROR|WARN)" tiktok-automation.log
```

**Quick Health Check**:
```bash
echo "TikTok Automation Status"
echo "========================="
echo "Session Valid: $(jq -e .isValid tiktok-session.json 2>/dev/null && echo '✓' || echo '✗')"
echo "Selectors Learned: $(jq 'keys' selectors.json | wc -l)"
echo "Last Upload: $(jq -r '.lastUsed' selectors.json 2>/dev/null || echo 'Never')"
echo "Config Valid: $(jq . config.json > /dev/null 2>&1 && echo '✓' || echo '✗')"
```
