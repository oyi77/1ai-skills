---
name: social-media-upload
description: Distribute content across multiple social media platforms (X, Instagram, TikTok, LinkedIn, Facebook, YouTube).
  Upload images, videos, and text with platform-specific optimization.
domain: marketing
tags:
- growth
- marketing
- media
- seo
- social
- social-media
- upload
- video
---


persona:
  name: "Domain Expert"
  title: "Master of Social Media Upload"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Social Media Upload Skill

## Expert Persona

**You are channeling the Buffer and Hootsuite teams** — pioneers of social media management and cross-platform publishing automation.

### Buffer Team - "The Social Media Scheduling Experts"
- **Credentials**: $200M+ company, 140K+ customers, transparent culture
- **Expertise**: Multi-platform publishing, optimal timing algorithms, social analytics
- **Philosophy**: "Publish great content consistently"
- **Principles**:
  - 4-1-1 rule (4 valuable shares, 1 self-promo, 1 soft ask)
  - Platform-specific optimization (different formats per channel)
  - Queue-based automation (evergreen content recycling)
  - Data-driven scheduling (best times for each platform)
  - Visual-first approach

### Hootsuite Team - "The Social Media Command Center"
- **Credentials**: $100M+ in funding, enterprise social media management leader
- **Expertise**: Social listening, team collaboration, cross-platform security
- **Philosophy**: "Organize, manage, and secure your social presence"
- **Principles**:
  - Centralized content calendar
  - Approval workflows for teams
  - Team collaboration tools
  - Social listening streams
  - Security and compliance first

**Combined Approach**: Blend Buffer's publishing efficiency with Hootsuite's enterprise-grade management. Optimize each post for its platform while maintaining brand consistency. Test multiple variations to maximize engagement.

## Overview

Automate content distribution across major social media platforms from a single workflow. Upload videos, images, and text with platform-specific formatting, hashtags, and captions. Essential for 1-man company content distribution.

**Supported Platforms**:
- X (Twitter)
- Instagram
- TikTok
- LinkedIn
- Facebook
- YouTube

## When to Use
**Trigger phrases:**
- "social media upload"
- "Distribute content across multiple social media platforms (X, Instagram, TikTok,"


- Distribute video content generated from `google-flow` or `grok-video-generation`
- Post same content to multiple platforms simultaneously
- Schedule social media posts
- Upload marketing materials
- Share blog posts/articles
- Cross-post content efficiently
- Maintain consistent social media presence

## When NOT to Use

- Engagement activities (use `marketing/social-media-engagement`)
- Analytics and reporting (use platform analytics)
- Direct messaging (use engagement skill)

---

## Platform-Specific Workflows

Step-by-step social-media-upload execution process.

**Step 1: Configure** — Set up targets and parameters in config file.

**Step 2: Execute** — Run the social-media-upload workflow with configured inputs.

**Step 3: Review** — Analyze outputs and iterate on configuration.

**Step 4: Automate** — Schedule recurring execution via cron or workflow engine.


### Step 1: Configure
Set up targets and parameters in config file.

### Step 2: Execute
Run the social-media-upload workflow with configured inputs.

### Step 3: Review
Analyze outputs and iterate on configuration.

### Step 4: Automate
Schedule recurring execution via cron or workflow engine.


### X (Twitter) Upload

**Access**: https://x.com or https://twitter.com

**Step 1: Navigate and Login**
```javascript
// Navigate to X
window.location.href = 'https://x.com';

// Login if needed
// Handle authentication
```

**Step 2: Create Post**
```javascript
// Click "Post" or "What's happening" button
// Usually in top-right or center of feed

// Find and click post button
const postButton = document.querySelector('[data-testid="SideNav_NewTweet_Button"]');
if (postButton) postButton.click();
```

**Step 3: Add Content**
```javascript
// Type text content
const tweetBox = document.querySelector('[data-testid="tweetTextarea_0"]');
if (tweetBox) {
  tweetBox.focus();
  // Type your content
}

// Add media (image/video)
const mediaButton = document.querySelector('[data-testid="fileInput"]');
// Upload file
```

**Step 4: Optimize for X**
```javascript
// Add hashtags (2-3 recommended)
const hashtags = '#AI #VideoMarketing #ContentCreation';

// Mention relevant accounts
const mentions = '@username';

// Keep under 280 characters for text
```

**Step 5: Post**
```javascript
// Click "Post" button
const submitButton = document.querySelector('[data-testid="tweetButton"]');
if (submitButton) submitButton.click();
```

**Thread Creation**:
```javascript
// For longer content, create thread
// 1. Post first tweet
// 2. Click "Add another tweet" or reply to yourself
// 3. Continue thread
// 4. Post all at once
```

---

### Instagram Upload

**Access**: https://instagram.com

**Step 1: Navigate to Upload**
```javascript
// Navigate to Instagram
window.location.href = 'https://instagram.com';

// Click "Create" or "+" button
const createButton = document.querySelector('[aria-label="New post"]');
if (createButton) createButton.click();
```

**Step 2: Select Content Type**
```
- Post (single image/video)
- Carousel (multiple images)
- Reel (short video)
- Story (24-hour content)
```

**Step 3: Upload Media**
```javascript
// Select file from computer
// Instagram supports:
// - Images: JPG, PNG (max 1080x1080 for feed)
// - Videos: MP4 (max 60s for feed, 90s for Reels)
// - Aspect ratios: 1:1 (square), 4:5 (portrait), 16:9 (landscape)
```

**Step 4: Edit and Filter**
```
1. Apply filters (optional)
2. Adjust brightness, contrast, saturation
3. Crop/resize if needed
4. Add music (for Reels)
```

**Step 5: Write Caption**
```javascript
// Caption best practices:
// - First line is crucial (before "...more")
// - Use 3-5 relevant hashtags
// - Include call-to-action
// - Tag relevant accounts
// - Add location (increases discoverability)

const caption = `
Check out this amazing AI-generated video! 🎥✨

Created using cutting-edge AI technology. What do you think?

#AIVideo #ContentCreation #DigitalMarketing

📍 Location: Your City
`;
```

**Step 6: Advanced Settings**
```
- Alt text (accessibility)
- Turn off commenting (optional)
- Hide like count (optional)
- Tag people
```

**Step 7: Share**
```javascript
// Click "Share" button
// Post goes live immediately
```

---

### TikTok Upload

**Access**: https://tiktok.com

**Step 1: Navigate to Upload**
```javascript
// Navigate to TikTok
window.location.href = 'https://tiktok.com';

// Click "Upload" button (desktop)
// Or use TikTok mobile app for better experience
```

**Step 2: Upload Video**
```
Requirements:
- Format: MP4, MOV
- Length: 3 seconds to 10 minutes
- Resolution: 1080x1920 (9:16 vertical)
- File size: Up to 4GB
```

**Step 3: Edit Video**
```
- Trim/cut clips
- Add text overlays
- Select cover image
- Add effects/filters
```

**Step 4: Add Details**
```javascript
// Caption (max 2200 characters)
const caption = 'AI-generated video magic! 🪄 #AIVideo #TechTrends #FYP';

// Hashtags (use trending + niche)
const hashtags = [
  '#FYP',           // For You Page
  '#ForYou',        // Discovery
  '#AIVideo',       // Niche
  '#TechTrends',    // Category
  '#Viral'          // Aspirational
];

// Add sound/music
// - Use trending sounds for better reach
// - Or upload original audio
```

**Step 5: Settings**
```
- Who can view: Public/Friends/Private
- Allow comments: Yes/No
- Allow Duet: Yes/No
- Allow Stitch: Yes/No
- Disclose AI-generated content: Yes (if applicable)
```

**Step 6: Post**
```javascript
// Click "Post" button
// Video processes and goes live
```

---

### LinkedIn Upload

**Access**: https://linkedin.com

**Step 1: Create Post**
```javascript
// Navigate to LinkedIn
window.location.href = 'https://linkedin.com';

// Click "Start a post" box
const postBox = document.querySelector('[data-control-name="share_box"]');
if (postBox) postBox.click();
```

**Step 2: Add Content**
```javascript
// Type professional content
const content = `
🎥 Excited to share our latest AI-generated video showcasing innovative marketing strategies!

Key takeaways:
✅ AI is transforming content creation
✅ Video marketing drives 80% more engagement
✅ Automation enables 1-person companies to scale

What's your experience with AI in marketing? Let's discuss in the comments!

#AIMarketing #VideoContent #DigitalTransformation #Innovation
`;
```

**Step 3: Upload Media**
```javascript
// Click media button
const mediaButton = document.querySelector('[data-control-name="media"]');

// Upload image or video
// LinkedIn supports:
// - Images: JPG, PNG (max 5MB)
// - Videos: MP4 (max 10 minutes, 5GB)
```

**Step 4: Add Article/Link (Optional)**
```
- Paste URL for link preview
- LinkedIn auto-generates preview
- Edit title/description if needed
```

**Step 5: Tag People/Companies**
```
- @ mention connections
- Tag companies (increases visibility)
```

**Step 6: Post Settings**
```
- Post as: Personal profile or Company page
- Notify connections: Yes/No
```

**Step 7: Publish**
```javascript
// Click "Post" button
// Content goes live immediately
```

---

## Multi-Platform Distribution

- Configure across, content, distribute, facebook, images settings before first use


### Workflow: Post to All Platforms

```javascript
async function distributeContent(videoPath, caption) {
  const platforms = ['x', 'instagram', 'tiktok', 'linkedin'];
  const results = [];
  
  for (const platform of platforms) {
    // 1. Navigate to platform
    await navigateToPlatform(platform);
    
    // 2. Upload content
    await uploadMedia(platform, videoPath);
    
    // 3. Add platform-specific caption
    const optimizedCaption = optimizeCaption(caption, platform);
    await addCaption(optimizedCaption);
    
    // 4. Post
    await publishPost(platform);
    
    results.push({ platform, status: 'success' });
    
    // 5. Wait between platforms
    await new Promise(r => setTimeout(r, 5000));
  }
  
  return results;
}
```

### Platform-Specific Optimization

```javascript
function optimizeCaption(baseCaption, platform) {
  const optimizations = {
    x: {
      maxLength: 280,
      hashtagCount: 2-3,
      style: 'concise, punchy'
    },
    instagram: {
      maxLength: 2200,
      hashtagCount: 3-5,
      style: 'engaging, visual-focused'
    },
    tiktok: {
      maxLength: 2200,
      hashtagCount: 4-6,
      style: 'trendy, casual'
    },
    linkedin: {
      maxLength: 3000,
      hashtagCount: 3-5,
      style: 'professional, value-driven'
    }
  };
  
  const config = optimizations[platform];
  
  // Truncate if needed
  let optimized = baseCaption.substring(0, config.maxLength);
  
  // Add platform-specific hashtags
  optimized += '\n\n' + getPlatformHashtags(platform, config.hashtagCount);
  
  return optimized;
}
```

---

## Integration with Video Generation Skills

- Configure across, content, distribute, facebook, images settings before first use


### From Google Flow to Social Media

```javascript
async function flowToSocial(videoPrompt, platforms) {
  // 1. Generate video with Google Flow
  await generateVideo(videoPrompt);
  await new Promise(r => setTimeout(r, 90000)); // Wait for generation
  
  // 2. Download video
  const videoPath = await downloadVideo('flow-video.mp4');
  
  // 3. Create platform-specific captions
  const baseCaption = 'Check out this AI-generated video!';
  
  // 4. Distribute to platforms
  for (const platform of platforms) {
    await uploadToPlatform(platform, videoPath, baseCaption);
  }
  
  return 'Distribution complete';
}

// Usage
await flowToSocial(
  'A peaceful ocean wave at sunset',
  ['x', 'instagram', 'tiktok', 'linkedin']
);
```

### From Grok Imagine to Social Media

```javascript
async function grokToSocial(grokVideoPath, platforms) {
  // 1. Video already generated in Grok app
  // 2. Downloaded to device
  // 3. Transferred to computer
  
  // 4. Distribute
  const caption = 'AI-powered video created with Grok Imagine! 🤖';
  
  for (const platform of platforms) {
    await uploadToPlatform(platform, grokVideoPath, caption);
  }
}
```

---

## Best Practices

- Always test with a small dataset before full-scale runs
- Monitor resource usage (memory, API quotas) during execution
- Keep configuration in version control
- Document custom parameters and their effects
- Set up alerts for failure conditions


### Content Optimization

1. **Video Specs by Platform**:
   - **X**: 1920x1080 (16:9) or 1080x1080 (1:1), max 2:20
   - **Instagram Feed**: 1080x1080 (1:1), max 60s
   - **Instagram Reels**: 1080x1920 (9:16), max 90s
   - **TikTok**: 1080x1920 (9:16), 3s-10min
   - **LinkedIn**: 1920x1080 (16:9), max 10min

2. **Hashtag Strategy**:
   - Research trending hashtags
   - Mix popular + niche hashtags
   - Platform-specific hashtag counts
   - Create branded hashtags

3. **Posting Times**:
   - **X**: 12-3pm, 5-6pm
   - **Instagram**: 11am-1pm, 7-9pm
   - **TikTok**: 6-9am, 12-3pm, 7-11pm
   - **LinkedIn**: 7-9am, 12pm, 5-6pm

4. **Caption Writing**:
   - Hook in first line
   - Clear value proposition
   - Call-to-action
   - Relevant hashtags
   - Emojis for engagement

### Automation Safety

1. **Rate Limits**:
   - Don't post too frequently
   - Space out posts (15-30 min between platforms)
   - Respect platform limits

2. **Content Variety**:
   - Don't post identical content
   - Customize for each platform
   - Vary posting times

3. **Authenticity**:
   - Disclose AI-generated content
   - Maintain brand voice
   - Engage with audience

---

## Troubleshooting

**Issue**: Upload fails
- **Solution**: Check file format, size, resolution

**Issue**: Caption truncated
- **Solution**: Respect platform character limits

**Issue**: Video processing stuck
- **Solution**: Wait longer, refresh page, try re-upload

**Issue**: Post not appearing
- **Solution**: Check privacy settings, verify account status

**Issue**: Hashtags not working
- **Solution**: Avoid banned hashtags, use relevant tags

---


## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Marketing changes are deployed without measuring impact
- Agent does not comply with platform-specific content guidelines
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Marketing changes have measurable impact metrics before and after
- [ ] Platform content guidelines are followed for each target
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `productivity/google-flow` - Video generation
- `content/grok-video-generation` - Alternative video generation
- `marketing/social-media-engagement` - Audience engagement
- `marketing/content-creator` - Content strategy
- `marketing/ads-manager` - Paid advertising

---

**Last Updated**: 2026-02-17  
**Platforms**: X, Instagram, TikTok, LinkedIn, Facebook, YouTube  
**Key Feature**: Multi-platform distribution automation

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
