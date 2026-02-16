# content-creator Skill

> **Framework Agnostic** - This skill works with ANY AI agent (OpenCode, OpenClaw, Claude Desktop, custom agents, etc.)
> 
> **How to Use**: Read this file and follow the instructions. No special loading required.

## What It Does

Multi-platform content generation using browser automation (ChatGPT, Gemini, Grok, Google Flow, Canva). No APIs required - all interactions happen through browser.

## When to Use

- Create social media content (TikTok, Instagram, LinkedIn, Twitter)
- Generate blog posts and articles
- Create video scripts
- Design images
- Write marketing copy
- Any content creation task

## Key Capabilities

- **Text Generation**: Via ChatGPT/Gemini/Grok browser interfaces
- **Video Creation**: Via Google Flow
- **Image Generation**: Via Canva + DALL-E through ChatGPT
- **Multi-Platform**: Optimized output for each platform
- **Quality Check**: Self-grading against content rubric
- **Iteration**: Refine and improve based on feedback

## How It Works

```
Input: "Create [TYPE] content about [TOPIC] for [PLATFORM]"
   ↓
Analyze: Determine content type, platform preferences
   ↓
Select Tools:
   - Text → copywriting skill → generate via browser
   - Image → agent-browser → DALL-E via ChatGPT
   - Video → google-flow skill
   ↓
Generate: Via browser automation
   ↓
Quality Check: Against content rubric
   ↓
Iterate: If fail, refine prompt → retry
   ↓
Output: Complete content package
```

## Platform Workflows

| Platform | Workflow |
|----------|----------|
| TikTok | Google Flow → video → download → upload → caption → schedule |
| YouTube | ChatGPT → script → Google Flow → video → upload |
| Instagram | Canva → design → DALL-E → image → upload |
| LinkedIn | ChatGPT → post → edit → publish |
| Twitter | Grok → tweet/thread → publish |

## Browser Automation Patterns

### Generate LinkedIn Post via ChatGPT

1. Navigate: https://chatgpt.com
2. Click: button[aria-label="New chat"]
3. Fill: textarea[placeholder="Send a message"] with prompt
4. Wait: for response (selector: .result-message)
5. Extract: text from .result-message
6. Quality check: against criteria
7. If fail: refine prompt → retry
8. If pass: save to content-library/

### Generate Image via ChatGPT + DALL-E

1. Navigate: https://chatgpt.com
2. Click: "New chat"
3. Fill: "Generate an image of [description] using DALL-E 3"
4. Wait: for image generation
5. Extract: image URL
6. Download: image to local storage
7. Save: to content-library/images/

### Create Video via Google Flow

1. Navigate: https://flow.google.com
2. Click: "New video project"
3. Fill: script or topic
4. Select: video style
5. Generate: video
6. Download: to content-library/videos/
7. Save: metadata to content-library/manifest.json

## Content Quality Rubric

| Criterion | Weight | Threshold |
|-----------|--------|-----------|
| Relevance | 30% | Matches topic |
| Platform fit | 25% | Appropriate format |
| Engagement | 25% | Has hooks, CTAs |
| Brand voice | 20% | Consistent tone |

## Usage Examples

### Create LinkedIn Post
```
User: "Create a LinkedIn post about AI automation for my tech startup"
Skill: Uses ChatGPT browser → generates post → checks quality → outputs content
```

### Generate Instagram Image
```
User: "Create an Instagram image for our product launch"
Skill: Uses DALL-E via ChatGPT → generates image → downloads → saves
```

### Create YouTube Script
```
User: "Write a YouTube script about machine learning basics"
Skill: ChatGPT → generates outline → expands to full script → saves
```

## Skills It Coordinates

- `agent-browser` - Browser automation
- `copywriting` - Content writing (from skills.sh)
- `content-strategy` - Content planning (from skills.sh)
- `social-content` - Social media optimization (from skills.sh)

## Self-Improvement

The skill self-grades after each content generation:
1. Check against rubric criteria
2. If score < 7/10, refine prompt
3. Retry generation
4. Log improvements for future reference

## Troubleshooting

- **Browser not responding**: Restart browser automation session
- **Content quality low**: Refine prompt with more context
- **Platform not loading**: Check internet connection, try alternative platform
- **Rate limiting**: Wait 30s, retry with exponential backoff

## Files Created

- `content-library/` - Generated content storage
  - `posts/` - Text posts
  - `images/` - Generated images
  - `videos/` - Generated videos
  - `scripts/` - Video scripts
  - `manifest.json` - Content metadata
