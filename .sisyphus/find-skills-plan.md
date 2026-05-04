# Plan: Create meta/find-skills Meta-Skill

## Objective
Create an intelligent skill discovery system that automatically finds, evaluates, and activates community skills when local skills don't cover user needs.

## Requirements

### Functional Requirements
1. **User Request Analysis** - Extract intent and keywords from user queries
2. **Local Skill Check** - Search existing skills before external lookup
3. **Community Search** - Query skills.sh and awesome-openclaw-skills APIs
4. **Credibility Scoring** - Rank skills by downloads, ratings, recency, author reputation
5. **Safety Validation** - Malware scan, secret detection, dependency analysis
6. **Installation** - Download and activate skills automatically
7. **Integration** - Work with meta/performance-monitor and meta/auto-learner

### Non-Functional Requirements
- **Performance**: Response time < 2 seconds for skill discovery
- **Reliability**: 99% success rate for skill installation
- **Security**: All skills validated before activation
- **Compatibility**: Works with existing 1ai-skills structure

## Architecture

```
meta/find-skills/
├── SKILL.md          # Main skill definition
├── config.json       # Configuration (API endpoints, thresholds)
├── cache/            # Cached skill metadata
└── logs/             # Discovery and installation logs
```

## Implementation Steps

### Step 1: Create Skill Structure
```bash
mkdir -p meta/find-skills
```

### Step 2: Write SKILL.md
- Persona: Sergey Brin (search expert)
- Overview: Explain skill discovery system
- When to Use: Automatic activation triggers
- How It Works: 5-step process with code examples
- Integration: Connect with other meta-skills
- Safety: Credibility scoring and validation
- Examples: Marketing, trading, DevOps use cases

### Step 3: Create Configuration
```json
{
  "apiEndpoints": [
    "https://api.skills.sh/v1/skills",
    "https://raw.githubusercontent.com/openclaw-community/awesome-openclaw-skills/main/index.json"
  ],
  "minCredibilityScore": 70,
  "maxCacheAgeHours": 24,
  "autoActivate": true
}
```

### Step 4: Implement Core Functions

#### checkLocalSkills(userRequest)
```javascript
function checkLocalSkills(userRequest) {
  const localSkills = loadActivationRules();
  const matches = findMatchingSkills(userRequest, localSkills);
  return matches.length > 0 ? matches : null;
}
```

#### searchCommunitySkills(query)
```javascript
async function searchCommunitySkills(query) {
  const results = [];
  for (const endpoint of config.apiEndpoints) {
    const response = await fetch(endpoint + '?q=' + encodeURIComponent(query));
    results.push(...(await response.json()).results);
  }
  return results;
}
```

#### scoreSkill(skill)
```javascript
function scoreSkill(skill) {
  let score = 0;
  score += Math.min(skill.downloads / 1000, 10);
  score += skill.rating * 2;
  const ageDays = (Date.now() - new Date(skill.updatedAt)) / (1000 * 60 * 60 * 24);
  score += Math.max(0, 10 - ageDays / 30);
  if (skill.author.verified) score += 5;
  if (skill.author.skillsCount > 10) score += 3;
  return score;
}
```

#### checkSafety(skill)
```javascript
function checkSafety(skill) {
  return runMalwareScan(skill) && 
         runSecretDetection(skill) &&
         checkDependencies(skill);
}
```

#### installSkill(skillId)
```javascript
async function installSkill(skillId) {
  const response = await fetch(`https://api.skills.sh/v1/skills/${skillId}/download`);
  const content = await response.text();
  await fs.writeFile(`./skills/${skillId}/SKILL.md`, content);
  updateActivationRules(skillId);
}
```

### Step 5: Integration Points

#### With meta/performance-monitor
```javascript
// Track skill discovery metrics
performanceMonitor.track('skill_discovery', {
  query: userRequest,
  skillsFound: results.length,
  skillInstalled: skillId,
  responseTime: Date.now() - startTime
});
```

#### With meta/auto-learner
```javascript
// Learn from discovery patterns
autoLearner.recordPattern({
  userIntent: extractedIntent,
  skillsActivated: [skillId],
  success: installationSuccess
});
```

### Step 6: Testing

#### Unit Tests
- `testLocalSkillCheck()` - Verify local skill matching
- `testCommunitySearch()` - Mock API responses
- `testScoringAlgorithm()` - Verify credibility scoring
- `testSafetyChecks()` - Validate security functions

#### Integration Tests
- `testFullDiscoveryFlow()` - End-to-end skill discovery
- `testInstallation()` - Skill download and activation
- `testMetaIntegration()` - Performance monitoring and learning

#### User Acceptance Tests
- "Find me a viral marketing skill" → Should discover and install
- "Can you do crypto trading analysis?" → Should find trading skills
- "I need Kubernetes help" → Should locate DevOps skills

## Success Criteria

✅ Local skills checked before external search
✅ Community skills discovered and ranked
✅ Credibility scoring working (0-100 scale)
✅ Safety validation passing
✅ Skills installed and activated automatically
✅ Integration with meta-skills functional
✅ Response time < 2 seconds
✅ 99% installation success rate

## Risk Mitigation

### Risk: API Unavailable
**Mitigation**: Cache results, fallback to local skills, notify user

### Risk: Malicious Skills
**Mitigation**: Comprehensive safety checks, sandboxed execution, user review

### Risk: Performance Issues
**Mitigation**: Rate limiting, caching, async operations

### Risk: Compatibility Problems
**Mitigation**: Version checking, dependency validation, rollback capability

## Deployment Plan

1. **Create directories**: `mkdir -p meta/find-skills`
2. **Write SKILL.md**: Based on template above
3. **Create config.json**: API endpoints and thresholds
4. **Implement functions**: Core discovery logic
5. **Add integration**: Connect with meta-skills
6. **Write tests**: Unit, integration, UAT
7. **Document**: Update README with new capability
8. **Deploy**: Commit and push to repository

## Rollback Plan

If issues occur:
1. Disable auto-activation: `config.autoActivate = false`
2. Revert to local skills only
3. Notify users of temporary limitation
4. Fix and redeploy

## Metrics for Success

- **Discovery Rate**: % of user requests that trigger skill search
- **Installation Rate**: % of searches that result in installation
- **User Satisfaction**: Feedback ratings on discovered skills
- **Performance**: Average response time for discovery
- **Coverage**: % of user needs covered by discovered skills

## Next Steps

After implementing find-skills:
1. Create meta/create-skills for skill generation
2. Create meta/auto-evolve for continuous improvement
3. Update README to showcase self-evolving capabilities
4. Test complete system end-to-end

---

**Plan Status**: Ready for execution
**Executor**: Sisyphus-Junior (quick category)
**Estimated Time**: 30 minutes
