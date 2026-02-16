---
name: content-scheduler
description: Schedule social media posts across multiple platforms. Queue content, optimize posting times, manage content calendar, and automate distribution for consistent social media presence.
---

# Content Scheduler Skill

## Overview

Automate content scheduling across X, Instagram, TikTok, and LinkedIn. Queue posts in advance, optimize posting times, manage content calendar, and maintain consistent social media presence without manual posting.

## When to Use

- Schedule posts in advance
- Batch content creation
- Maintain posting consistency
- Optimize posting times
- Plan content calendar
- Automate recurring posts
- Cross-platform scheduling

## Core Features

### 1. Queue Management
```javascript
const contentQueue = {
  platform: 'x',  // x, instagram, tiktok, linkedin
  content: {
    text: 'Check out our latest AI video!',
    media: '/path/to/video.mp4',
    hashtags: ['#AI', '#Video']
  },
  scheduledTime: '2026-02-20T10:00:00+07:00',
  status: 'queued'  // queued, posted, failed
};
```

### 2. Optimal Time Suggestions
```javascript
const optimalTimes = {
  x: ['12:00', '15:00', '17:00'],
  instagram: ['11:00', '13:00', '19:00'],
  tiktok: ['07:00', '12:00', '20:00'],
  linkedin: ['08:00', '12:00', '17:00']
};
```

### 3. Recurring Posts
```javascript
const recurringPost = {
  content: 'Weekly tip: ...',
  schedule: 'every Monday at 10:00',
  platforms: ['x', 'linkedin']
};
```

### 4. Content Calendar View
```
Week of Feb 17-23, 2026
Mon: 3 posts (X, Instagram, LinkedIn)
Tue: 2 posts (TikTok, X)
Wed: 4 posts (All platforms)
...
```

## Integration with social-media-upload
```javascript
async function scheduleAndPost(queuedPost) {
  const now = new Date();
  const scheduledTime = new Date(queuedPost.scheduledTime);
  
  if (now >= scheduledTime) {
    // Time to post
    await uploadToPlatform(
      queuedPost.platform,
      queuedPost.content
    );
    queuedPost.status = 'posted';
  }
}
```

## Best Practices
- Schedule 1-2 weeks in advance
- Post 1-3 times per day per platform
- Use analytics to optimize times
- Batch create content weekly
- Mix content types (video, image, text)

---

**Related Skills**: `marketing/social-media-upload`, `marketing/analytics-dashboard`
