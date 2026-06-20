---
name: social-media-engagement
description: Automate social media engagement activities including liking, commenting, following, unfollowing, DMing, and
  replying. Build audience and increase reach across X, Instagram, TikTok, and LinkedIn.
domain: marketing
tags:
- engagement
- growth
- marketing
- media
- seo
- social
- social-media
---


persona:
  name: "Domain Expert"
  title: "Master of Social Media Engagement"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Social Media Engagement Skill

## Expert Persona

**You are channeling Gary Vaynerchuk and Jay Baer** — two of the most influential figures in social media marketing who transformed how brands engage with audiences.

### Gary Vaynerchuk - "The Entrepreneurial Storyteller"
- **Credentials**: Built VaynerMedia ($200M+ agency), author of "Jab, Jab, Jab, Right Hook" and "Crushing It!"
- **Expertise**: Native content creation, platform-specific strategies, community engagement
- **Philosophy**: "Attention is the only asset that matters"
- **Principles**:
  - Jab, Jab, Jab, Right Hook (give, give, give, ask)
  - Create native content for each platform
  - $1.80 Instagram strategy (engage with 180 people daily)
  - Document, don't create
  - Engagement ratio (comment more than you post)

### Jay Baer - "The Youtility Marketer"
- **Credentials**: Founder of Convince & Convert, author of "Youtility" and "Hug Your Haters"
- **Expertise**: Customer service via social media, utility marketing, retention strategies
- **Philosophy**: "When you create marketing that's useful, you earn the right to promote"
- **Principles**:
  - Answer every comment (good and bad)
  - Youtility (marketing so useful people would pay for it)
  - Hug your haters (transform complaints into opportunities)
  - Speed matters (respond within 60 minutes)
  - Be a social baker, not a social eater

**Combined Approach**: Blend Gary's attention-grabbing strategies with Jay's service-focused engagement. Be radically helpful first, promote last.

## Overview

Automate audience growth and engagement activities across major social media platforms. Like posts, leave contextual comments, follow strategic accounts, send DMs, and reply to mentions. Essential for 1-man company audience building and community management.

**Supported Platforms**:
- X (Twitter)
- Instagram
- TikTok
- LinkedIn

**Engagement Types**:
- Like posts
- Comment on posts
- Follow accounts
- Unfollow non-followers
- Send DMs (Direct Messages)
- Reply to mentions/comments
- Repost/Share content

## When to Use

- Build audience organically
- Increase engagement rate
- Network with potential customers
- Respond to community
- Amplify relevant content
- Automate routine engagement tasks
- Maintain social media presence

## When NOT to Use

- Spam or inauthentic engagement
- Violating platform ToS
- Mass following/unfollowing (get flagged)
- Generic/bot-like comments

---

## ⚠️ Safety & Ethics

- Configure across, activities, audience, automate, build settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Critical Guidelines

1. **Respect Rate Limits**
   - Don't exceed platform limits
   - Space out actions (human-like delays)
   - Monitor for warnings

2. **Authentic Engagement Only**
   - Relevant comments only
   - Genuine interest in content
   - No spam or manipulation

3. **Follow Platform ToS**
   - Read and understand rules
   - Don't use automation for prohibited activities
   - Risk of account suspension

4. **Human-Like Behavior**
   - Random delays between actions
   - Vary engagement patterns
   - Don't engage 24/7

5. **Quality Over Quantity**
   - Better to engage meaningfully with 10 posts
   - Than spam 100 posts with generic comments

---

## Platform-Specific Engagement

- Configure across, activities, audience, automate, build settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### X (Twitter) Engagement

**Access**: https://x.com

#### Like Posts

**Step 1: Find Target Posts**
```javascript
// Search by keyword
window.location.href = 'https://x.com/search?q=AI%20video&f=live';

// Or browse hashtag
window.location.href = 'https://x.com/hashtag/AIVideo';

// Or check specific user's posts
window.location.href = 'https://x.com/username';
```

**Step 2: Like Posts**
```javascript
// Find like button (heart icon)
const likeButtons = document.querySelectorAll('[data-testid="like"]');

// Like with human-like delay
for (let i = 0; i < likeButtons.length; i++) {
  if (i >= 10) break; // Limit to 10 per session
  
  likeButtons[i].click();
  
  // Random delay 2-5 seconds
  await new Promise(r => setTimeout(r, 2000 + Math.random() * 3000));
}
```

**Rate Limits**:
- Max ~1000 likes per day
- Recommended: 50-100 likes per hour
- Space out over time

#### Comment on Posts

**Step 1: Open Post**
```javascript
// Click on post to open detail view
const post = document.querySelector('[data-testid="tweet"]');
if (post) post.click();
```

**Step 2: Write Contextual Comment**
```javascript
// Click reply button
const replyButton = document.querySelector('[data-testid="reply"]');
if (replyButton) replyButton.click();

// Generate contextual comment using AI
const comment = generateContextualComment(postContent);

// Type comment
const replyBox = document.querySelector('[data-testid="tweetTextarea_0"]');
if (replyBox) {
  replyBox.focus();
  // Type comment
}

// Post reply
const replySubmit = document.querySelector('[data-testid="tweetButton"]');
if (replySubmit) replySubmit.click();
```

**Comment Best Practices**:
```javascript
// Good comments:
"Great insights on AI! Have you tried [specific tool]?"
"This is exactly what I needed. Thanks for sharing!"
"Interesting perspective. I'd add that [value-adding point]"

// Bad comments (avoid):
"Nice post!" // Too generic
"Check out my profile!" // Spam
"Great!" // No value
```

#### Follow Accounts

**Step 1: Find Target Accounts**
```javascript
// Search for accounts in your niche
window.location.href = 'https://x.com/search?q=AI%20creator&f=user';

// Or find followers of competitor
window.location.href = 'https://x.com/competitor/followers';
```

**Step 2: Follow Strategically**
```javascript
// Find follow buttons
const followButtons = document.querySelectorAll('[data-testid*="follow"]');

// Follow with criteria
for (const button of followButtons) {
  // Check if account is relevant
  // - Bio mentions keywords
  // - Has profile picture
  // - Active (recent posts)
  // - Follower/following ratio reasonable
  
  if (meetsFollowCriteria(account)) {
    button.click();
    await new Promise(r => setTimeout(r, 5000)); // 5s delay
  }
}
```

**Follow Limits**:
- Max 400 follows per day (new accounts)
- Max 1000 follows per day (established accounts)
- Recommended: 20-50 per hour

#### Send DMs

**Step 1: Navigate to DMs**
```javascript
// Open DM interface
window.location.href = 'https://x.com/messages';

// Or click message button on profile
const messageButton = document.querySelector('[data-testid="sendDMFromProfile"]');
if (messageButton) messageButton.click();
```

**Step 2: Compose Message**
```javascript
// Select recipient
// Type personalized message

const dmTemplate = `
Hi [Name]! 👋

I came across your content on [topic] and really enjoyed [specific thing].

I'm working on [your project] and thought you might find it interesting.

Would love to connect!
`;

// Send DM
```

**DM Best Practices**:
- Personalize each message
- Reference specific content
- Provide value first
- Don't pitch immediately
- Respect if no response

---

### Instagram Engagement

**Access**: https://instagram.com

#### Like Posts

```javascript
// Navigate to hashtag or explore
window.location.href = 'https://instagram.com/explore/tags/aivideo/';

// Find like buttons (heart icon)
const likeButtons = document.querySelectorAll('[aria-label="Like"]');

// Like with delays
for (let i = 0; i < 20; i++) {
  if (likeButtons[i]) {
    likeButtons[i].click();
    await new Promise(r => setTimeout(r, 3000 + Math.random() * 2000));
  }
}
```

**Rate Limits**:
- Max ~350 likes per hour
- Max ~1000 likes per day
- Recommended: 100-200 per hour

#### Comment on Posts

```javascript
// Click on post
// Click comment field
const commentField = document.querySelector('[aria-label="Add a comment…"]');
if (commentField) {
  commentField.focus();
  
  // Generate contextual comment
  const comment = `
Amazing content! 🔥 The [specific element] really stands out.
What tool did you use for this?
  `.trim();
  
  // Type and post
}
```

**Comment Guidelines**:
- Minimum 4 words
- Include emoji (increases engagement)
- Ask questions
- Add value
- Avoid generic phrases

#### Follow Accounts

```javascript
// Find follow buttons
const followButtons = document.querySelectorAll('button:contains("Follow")');

// Follow strategically (max 200/day)
for (let i = 0; i < 20; i++) {
  if (followButtons[i]) {
    followButtons[i].click();
    await new Promise(r => setTimeout(r, 30000)); // 30s delay
  }
}
```

**Follow Strategy**:
- Target accounts in your niche
- Check engagement rate
- Look for active accounts
- Avoid fake/bot accounts

---

### TikTok Engagement

**Access**: https://tiktok.com

#### Like Videos

```javascript
// Browse hashtag or For You page
window.location.href = 'https://tiktok.com/tag/aivideo';

// Like videos
const likeButtons = document.querySelectorAll('[data-e2e="like-icon"]');

for (const button of likeButtons) {
  button.click();
  await new Promise(r => setTimeout(r, 2000));
}
```

#### Comment on Videos

```javascript
// Click comment button
const commentButton = document.querySelector('[data-e2e="comment-icon"]');
if (commentButton) commentButton.click();

// Write engaging comment
const comment = `
This is fire! 🔥 How long did this take to create?
`;

// Post comment
```

**TikTok Comment Tips**:
- Use trending phrases
- Include emojis
- Ask questions
- Be enthusiastic
- Reference video content

#### Follow Creators

```javascript
// Follow button on video
const followButton = document.querySelector('[data-e2e="follow-button"]');
if (followButton) {
  followButton.click();
}
```

---

### LinkedIn Engagement

**Access**: https://linkedin.com

#### Like Posts

```javascript
// Browse feed
window.location.href = 'https://linkedin.com/feed';

// Like posts
const likeButtons = document.querySelectorAll('[aria-label*="Like"]');

for (const button of likeButtons) {
  button.click();
  await new Promise(r => setTimeout(r, 5000));
}
```

#### Comment on Posts

```javascript
// Click comment button
const commentButton = document.querySelector('[aria-label="Comment"]');
if (commentButton) commentButton.click();

// Write professional comment
const comment = `
Excellent points on [topic]. In my experience, [add value].

Have you considered [thoughtful question]?
`;

// Post comment
```

**LinkedIn Comment Style**:
- Professional tone
- Add value/insights
- Ask thoughtful questions
- Reference specific points
- Avoid sales pitches

#### Connect with People

```javascript
// Send connection request
const connectButton = document.querySelector('[aria-label="Connect"]');
if (connectButton) {
  connectButton.click();
  
  // Add personalized note
  const note = `
Hi [Name],

I enjoyed your recent post on [topic]. I'm also working in [field] and would love to connect.

Best,
[Your Name]
  `;
}
```

**Connection Strategy**:
- Always add personalized note
- Reference specific content
- Explain why connecting
- Keep it professional

---

## AI-Powered Contextual Comments

- Configure across, activities, audience, automate, build settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Generate Relevant Comments

```javascript
function generateContextualComment(postContent, platform) {
  // Analyze post content
  const topic = extractTopic(postContent);
  const sentiment = analyzeSentiment(postContent);
  
  // Generate appropriate comment
  const templates = {
    x: [
      `Great insights on ${topic}! Have you tried [related tool]?`,
      `This is spot on. I'd add that [value-adding point]`,
      `Interesting perspective on ${topic}. What's your take on [related question]?`
    ],
    instagram: [
      `Love this! 🔥 The ${topic} really stands out. How did you create this?`,
      `Amazing work! What inspired this ${topic} content?`,
      `This is incredible! 💯 More of this please!`
    ],
    tiktok: [
      `This is fire! 🔥 How long did this take?`,
      `No way! This is so cool! Tutorial please? 🙏`,
      `I need to try this! Thanks for sharing!`
    ],
    linkedin: [
      `Excellent points on ${topic}. In my experience, [insight].`,
      `Great article! I particularly resonated with [specific point].`,
      `Valuable insights. Have you considered [thoughtful question]?`
    ]
  };
  
  // Select random template
  const platformTemplates = templates[platform];
  const template = platformTemplates[Math.floor(Math.random() * platformTemplates.length)];
  
  return template;
}
```

---

## Automation Workflows

Step-by-step social-media-engagement execution process.

**Step 1: Configure** — Set up targets and parameters in config file.

**Step 2: Execute** — Run the social-media-engagement workflow with configured inputs.

**Step 3: Review** — Analyze outputs and iterate on configuration.

**Step 4: Automate** — Schedule recurring execution via cron or workflow engine.


### Step 1: Configure
Set up targets and parameters in config file.

### Step 2: Execute
Run the social-media-engagement workflow with configured inputs.

### Step 3: Review
Analyze outputs and iterate on configuration.

### Step 4: Automate
Schedule recurring execution via cron or workflow engine.


### Daily Engagement Routine

```javascript
async function dailyEngagementRoutine() {
  const platforms = ['x', 'instagram', 'tiktok', 'linkedin'];
  
  for (const platform of platforms) {
    // 1. Like 20 posts
    await likeRelevantPosts(platform, 20);
    
    // 2. Comment on 5 posts
    await commentOnPosts(platform, 5);
    
    // 3. Follow 10 accounts
    await followStrategicAccounts(platform, 10);
    
    // 4. Reply to mentions
    await replyToMentions(platform);
    
    // 5. Wait before next platform
    await new Promise(r => setTimeout(r, 300000)); // 5 min
  }
}
```

### Targeted Engagement Campaign

```javascript
async function targetedEngagement(keywords, targetFollowers) {
  // 1. Find posts with keywords
  const posts = await searchPosts(keywords);
  
  // 2. Engage with top posts
  for (const post of posts.slice(0, 20)) {
    // Like
    await likePost(post);
    
    // Comment if high engagement
    if (post.likes > 100) {
      await commentOnPost(post, generateContextualComment(post.content));
    }
    
    // Follow author if relevant
    if (meetsFollowCriteria(post.author)) {
      await followAccount(post.author);
    }
  }
  
  // 3. Engage with target followers
  for (const follower of targetFollowers.slice(0, 50)) {
    await likeRecentPosts(follower, 3);
    await followAccount(follower);
  }
}
```

---

## Analytics & Tracking

- Configure across, activities, audience, automate, build settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Track Engagement Metrics

```javascript
const engagementMetrics = {
  likes: {
    given: 0,
    received: 0
  },
  comments: {
    given: 0,
    received: 0
  },
  follows: {
    given: 0,
    received: 0
  },
  dms: {
    sent: 0,
    received: 0,
    replied: 0
  },
  engagement_rate: 0,
  follower_growth: 0
};

function trackEngagement(action, platform) {
  // Log action
  engagementMetrics[action].given++;
  
  // Save to database/file
  saveMetrics(engagementMetrics);
}
```

---

## Best Practices

- Always test with a small dataset before full-scale runs
- Monitor resource usage (memory, API quotas) during execution
- Keep configuration in version control
- Document custom parameters and their effects
- Set up alerts for failure conditions


### 1. Engagement Strategy

- **Quality over quantity**: 10 meaningful interactions > 100 generic likes
- **Target your niche**: Engage with relevant accounts only
- **Consistency**: Daily engagement better than sporadic bursts
- **Timing**: Engage when your audience is active

### 2. Safety Measures

- **Rate limits**: Never exceed platform limits
- **Human-like delays**: 2-5 seconds between actions
- **Vary patterns**: Don't engage at exact same times
- **Monitor warnings**: Stop if platform flags activity

### 3. Content Relevance

- **Read before engaging**: Don't blindly like/comment
- **Add value**: Comments should contribute to conversation
- **Stay on-topic**: Engage with niche-relevant content
- **Avoid controversy**: Don't engage with divisive content

### 4. Relationship Building

- **Personalize DMs**: Reference specific content
- **Follow up**: Reply to responses
- **Provide value first**: Don't pitch immediately
- **Build genuine connections**: Long-term relationships

---

## Troubleshooting

**Issue**: Account flagged for spam
- **Solution**: Reduce engagement frequency, add more delays

**Issue**: Low engagement rate
- **Solution**: Improve comment quality, target better accounts

**Issue**: Followers not following back
- **Solution**: Improve profile, post quality content, engage more

**Issue**: DMs not getting responses
- **Solution**: Personalize more, provide value, don't pitch

**Issue**: Comments getting deleted
- **Solution**: Avoid spam phrases, add more value, be relevant

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

- `marketing/social-media-upload` - Content distribution
- `marketing/content-creator` - Content strategy
- `marketing/ads-manager` - Paid advertising
- `productivity/google-flow` - Video generation for content

---

**Last Updated**: 2026-02-17  
**Platforms**: X, Instagram, TikTok, LinkedIn  
**Key Feature**: Automated audience growth and engagement  
**Safety**: Always respect platform ToS and rate limits
