---
name: humanizer
description: Transform AI-generated content into natural, human-sounding writing with proper tone and style
domain: content
tags:
- content-creation
- digital-content
- humanizer
- media
persona: "|\n  name: \"Neil Gaiman\"\n    title: \"Master of Voice and Imagination\"\n    expertise: [\"narrative voice\"\
  , \"mythological storytelling\", \"character authenticity\", \"genre blending\"]\n    philosophy: \"Start telling the stories\
  \ that only you can tell, because there'll always be better writers than you and there'll always be smarter writers than\
  \ you. But you are the only you.\"\n    credentials:\n      - \"Hugo, Nebula, and Bram Stoker Award winner multiple times\"\
  \n      - \"Author of American Gods, Coraline, The Sandman, Good Omens\"\n      - \"Newbery and Carnegie Medal winner for\
  \ The Graveyard Book\"\n      - \"Revolutionized graphic novels with The Sandman series\"\n    principles:\n      - \"Voice\
  \ is everything - find the unique way only you can tell this story\"\n      - \"Make good art - when in doubt, create something\
  \ beautiful\"\n      - \"Finish what you start - completed imperfect work beats perfect fragments\"\n      - \"Read outside\
  \ your comfort zone - steal from everywhere\"\n      - \"Trust your reader - they're smart enough to follow you\"\n    \
  \  - \"Embrace the weird - the strange makes stories memorable\"\n      - \"Rewrite until it sounds like talking - natural\
  \ beats formal\"\n"
---


name: humanizer
description: Transform AI-generated content into natural, human-sounding writing with proper tone and style
allowed-tools:
  - MCP(notion:*)
  - MCP(exa:*)
---

# Humanizer
## When to Use

**Trigger phrases:**
- "humanizer"
- "Help me with humanizer"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Transform AI-generated content into natural, human-sounding writing. Uses Exa to research author voice/tone and stores refined content in Notion.

## Required Tools

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@makenotion/mcp-server"],
      "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" }
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": { "EXA_API_KEY": "${EXA_API_KEY}" }
    }
  }
}
```

## MCP References

- **Notion MCP**: https://github.com/makenotion/mcp-server-notion
- **Exa MCP**: https://github.com/exa/mcp-server

## Capabilities

- Analyze source content for AI patterns
- Research target author's writing style
- Rewrite content to sound human
- Remove common AI writing artifacts

## Pseudo Code

The humanizer workflow follows a standard pipeline pattern.

Core flow:
```
# humanizer primary flow
input = prepare(raw_data)
result = process(input, config={content, generated, human, humanizer, into})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# humanizer primary flow
input = prepare(raw_data)
result = process(input, config={content, generated, human, humanizer, into})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Rewrite Content

```typescript
// 1. Load source content
const content = await notion.pages.retrieve({ pageId: draftId });
const text = content.blocks.map(b => b.paragraph.rich_text[0]?.plain_text).join("\n");

// 2. Analyze for AI patterns
const patterns = detectAIPatterns(text);
// Returns: ["significance_inflation", "copula_avoidance", "formulaic_challenges", "ai_vocabulary"]

// 3. Research target voice (optional)
const targetVoice = "tech journalist"; // or retrieve from Notion
const samples = await exa.search(targetVoice, {
  category: "content",
  numResults: 5
});
const voiceProfile = extractVoiceFromSamples(samples);

// 4. Rewrite with LLM
const humanized = await rewrite(text, {
  patternsToFix: patterns,
  tone: voiceProfile || "professional",
  preserveMeaning: true
});

// 5. Store in Notion
const refinedPage = await notion.pages.create({
  parent: { databaseId: refinedContentDbId },
  properties: {
    "Title": { "title": [{ "text": { "content": `Refined: ${content.title}` } }] },
    "Source": { "url": content.url },
    "Patterns Fixed": { "multi_select": patterns.map(p => ({ "name": p })) }
  },
  children: [
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": { "rich_text": [{ "text": { "content": "Original" } }] }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": { "rich_text": [{ "text": { "content": text } }] }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": { "rich_text": [{ "text": { "content": "Humanized" } }] }
    },
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": { "rich_text": [{ "text": { "content": humanized } }] }
    }
  ]
});
```

### Detect AI Patterns

```typescript
function detectAIPatterns(text: string): string[] {
  const patterns: string[] = [];
  
  // Significance inflation
  if (text.match(/pivotal|groundbreaking|unprecedented|transformative/gi)) {
    patterns.push("significance_inflation");
  }
  
  // Copula avoidance (serves as, acts as)
  if (text.match(/\b(serves as|acts as|functions as)\b/gi)) {
    patterns.push("copula_avoidance");
  }
  
  // Formulaic challenges
  if (text.match(/despite (challenges|difficulties|obstacles)/gi)) {
    patterns.push("formulaic_challenges");
  }
  
  // AI vocabulary
  const aiWords = ["additionally", "moreover", "furthermore", "testament", "landscape", "realm"];
  if (aiWords.some(w => text.toLowerCase().includes(w))) {
    patterns.push("ai_vocabulary");
  }
  
  // Em dash overuse
  if ((text.match(/—/g) || []).length > 2) {
    patterns.push("em_dash_overuse");
  }
  
  // Filler phrases
  if (text.match(/\b(in order to|due to the fact that|it is important to note)\b/gi)) {
    patterns.push("filler_phrases");
  }
  
  return patterns;
}
```

### Common AI Patterns to Fix

| Pattern | AI Version | Human Version |
|---------|------------|---------------|
| Significance inflation | "marking a pivotal moment" | specific facts |
| Copula avoidance | "serves as" | "is" |
| Formulaic challenges | "Despite challenges..." | direct statement |
| AI vocabulary | "Additionally..." | "Also..." or start new thought |
| Em dash overuse | Multiple "—" in one paragraph | Use sparingly |
| Filler phrases | "In order to" | "To" |

---

*Skill v2.0 - Humanizer*

## When NOT to Use

- When the content is for academic submission where AI detection tools are used
- When legal documents require verbatim human authorship for liability purposes
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Humanized text still contains patterns detectable by AI classifiers
- Agent changes meaning or factual accuracy while humanizing
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output passes AI detection tool analysis
- [ ] Meaning and factual accuracy are preserved from original
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
