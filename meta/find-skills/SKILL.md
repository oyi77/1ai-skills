---
name: find-skills
description: Automatically discover evaluate and activate community skills when local skills dont cover user needs Includes credibility scoring and safety checks for complete self-sufficiency
---
persona:
  name: "Ada Lovelace"
  title: "The First Programmer - Master of Algorithmic Discovery"
  expertise: ['Search', 'Pattern Matching', 'Credibility Analysis', 'Safety Validation']
  philosophy: "The analytical engine can do whatever we know how to order it to perform. My mission - ensure no capability gap goes unfilled."
  credentials: ['First computer programmer', 'Mathematical visionary', 'Pioneer of algorithmic thinking']
  principles: ['Search locally first', 'Validate before trusting', 'Score by merit not popularity', 'Safety is non-negotiable']

# Find Skills - Intelligent Skill Discovery System

## Overview

Automatically discover and integrate community skills when your local skills dont cover a need. Works as the **discovery layer** of the self-evolving system - before creating new skills always check if they already exist.

**Makes your AI agent complete and self-sufficient** - never say "I cant do that" again!

## When to Use

**Automatic Activation** when:
- User asks "how do I do X" where X isnt covered by local skills
- User says "find a skill for X" or "is there a skill for X"
- User asks "can you do X" where X is specialized
- The auto-evolve system detects a capability gap
- meta/create-skills checks before generating a new skill

## When NOT to Use

- Local skills already cover the need perfectly
- The request is trivial and doesnt need a dedicated skill
- Youre in an air-gapped environment with no internet

## Skill Discovery Process

### Step 1: Check Local Skills First

Before searching externally always check whats already installed:

1. Scan all skill activation rules in .opencode/skills/
2. Match user intent against skill descriptions
3. If match found - Use existing skill skip discovery
4. If no match - Proceed to Step 2

### Step 2: Extract Search Intent

Parse the users request into actionable search terms:

- Extract domain keywords (marketing trading devops design)
- Extract action words (create analyze automate optimize)
- Extract platform/context (twitter kubernetes react shopify)
- Form 2-3 search queries combining these terms

### Step 3: Search Community Sources

Query multiple skill registries in parallel:

1. **skills.sh API** - https://api.skills.sh/v1/skills?q={query}
2. **GitHub awesome-openclaw-skills** - Community curated list
3. **npm registry** - Published OpenClaw skill packages
4. **GitHub search** - Public repositories with openclaw-skill topic

### Step 4: Score and Rank Results

Apply credibility scoring algorithm (0-100 scale):

| Factor | Weight | Max Points |
|--------|--------|------------|
| Downloads/Installs | 20% | 20 |
| User Ratings | 20% | 20 |
| Recency (updated within 30 days) | 15% | 15 |
| Author Verification | 15% | 15 |
| Code Quality (lint pass) | 15% | 15 |
| Documentation Quality | 10% | 10 |
| Community Endorsements | 5% | 5 |

**Minimum score to recommend: 70/100**

### Step 5: Safety Validation

Before any skill installation run these checks:

1. **Malware Scan** - Check for obfuscated code eval() exec() patterns
2. **Secret Detection** - Scan for hardcoded API keys tokens passwords
3. **Dependency Analysis** - Verify all dependencies are legitimate packages
4. **Permission Check** - Ensure skill doesnt request excessive permissions
5. **Sandboxed Test** - Run skill in isolated environment before activation

### Step 6: Install and Activate

If skill passes all checks:

1. Download skill files to appropriate category directory
2. Update .skill-activation.json with new rules
3. Verify skill loads correctly in test mode
4. Activate for production use
5. Log installation for meta/performance-monitor tracking

## Integration with Meta-Skills

### With meta/create-skills

find-skills searches existing first
- Found? Install existing skill
- Not found? Delegate to create-skills to generate new one

### With meta/auto-evolve

auto-evolve detects capability gap
- find-skills searches for existing solutions
  - Found? Install and activate
  - Not found? create-skills generates new one

### With meta/performance-monitor

performance-monitor tracks discovery metrics
- Query response time
- Installation success rate
- Skill utilization after install
- User satisfaction with discovered skills

### With meta/auto-learner

auto-learner records discovery patterns
- Which queries lead to installs
- Which sources are most reliable
- Which skill types are most needed

## Examples

### Example 1: Marketing Skill Discovery

User: "I need to automate my Instagram posting"

find-skills process:
1. Local check: No instagram skill found
2. Search intent: "instagram" "social media" "automate posting"
3. Community search: Found 3 skills
   - social-media-upload (score: 87/100)
   - instagram-automation (score: 72/100)
   - auto-poster (score: 45/100) below threshold
4. Safety check: social-media-upload pass instagram-automation pass
5. Recommend: social-media-upload (highest score)
6. Install and activate

### Example 2: Trading Skill Discovery

User: "Can you help with crypto trading signals?"

find-skills process:
1. Local check: crypto-trading-bot exists but doesnt cover signals
2. Search intent: "crypto" "trading signals" "technical analysis"
3. Community search: Found 2 skills
   - trading-signal-analyzer (score: 82/100)
   - crypto-signals-free (score: 35/100) below threshold suspicious
4. Safety check: trading-signal-analyzer passes
5. Install: trading-signal-analyzer

### Example 3: Gap Detection via Auto-Evolve

auto-evolve: Performance data shows 12 failed requests for "podcast creation"

find-skills process:
1. Local check: No podcast skill
2. Search intent: "podcast" "audio creation" "ai podcast"
3. Community search: No results with score above 70
4. Delegate to create-skills to Generate ai-podcast skill
5. New skill installed and activated

## Configuration

Default configuration can be overridden in config.json:

```json
{
  "apiEndpoints": [
    "https://api.skills.sh/v1/skills",
    "https://raw.githubusercontent.com/openclaw-community/awesome-openclaw-skills/main/index.json"
  ],
  "minCredibilityScore": 70,
  "maxCacheAgeHours": 24,
  "autoActivate": true,
  "safetyChecks": {
    "malwareScan": true,
    "secretDetection": true,
    "dependencyAnalysis": true,
    "sandboxedTest": true
  }
}
```

## Troubleshooting

### No skills found
- Broaden search terms
- Try synonyms and related domains
- If still nothing delegate to create-skills

### Skills fail safety check
- Do NOT install - safety is non-negotiable
- Report the skill to community registry
- Generate alternative via create-skills

### Installation fails
- Check network connectivity
- Verify directory permissions
- Try manual installation as fallback

### Found skill doesnt work as expected
- Check version compatibility
- Review skill documentation for requirements
- Report issue to skill author
- Consider create-skills to generate a better alternative
