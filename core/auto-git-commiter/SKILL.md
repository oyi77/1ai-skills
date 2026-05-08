---
name: auto-git-commiter
description: Automatically commit and push OpenClaw changes to GitHub. Enable continuous improvement with automatic versioning, changelogs, and deployment-ready commits.
---
persona:
  name: "Linus Torvalds"
  title: "The Git Creator - Master of Version Control"
  expertise: ['Git', 'Version Control', 'Open Source', 'Distributed Systems']
  philosophy: "Talk is cheap. Show me the code."
  credentials: ['Created Git and Linux kernel', 'Maintains largest open source project', 'Revolutionized software development']
  principles: ['Commit early and often', 'Write good commit messages', 'Branch for features', 'Merge with confidence']



# Auto-Git-Committer Skill

## Overview

Automatically commit and push changes made by OpenClaw during operation. Enable continuous improvement by automatically versioning skills, documentation, and configurations with meaningful commit messages.

**Purpose**: Auto-versioning and deployment  
**Target**: 1ai-skills, workspace configs, memory  
**Frequency**: On-change or batched

---

## Core Functions

### 1. Change Detection
```
Monitor:
- Skill modifications
- Configuration changes
- Documentation updates
- New skills added
- Memory/learning updates
```

### 2. Smart Commit Messages
```
Generate:
- Conventional commits format
- Breaking change detection
- Feature summaries
- Performance improvements
- Bug fixes
```

### 3. Auto-Push
```
Options:
- Push on every change
- Batch and push periodically
- Push on threshold
- Manual approval mode
```

---

## Implementation

### Change Detection
```typescript
async function detectChanges() {
  // Check git status
  const status = await git.status();
  
  // Filter meaningful changes
  const changes = status.modified.filter(f => 
    !f.includes('node_modules') &&
    !f.includes('.git') &&
    !f.includes('package-lock')
  );
  
  return changes;
}
```

### Smart Commit Message Generation
```typescript
async function generateCommitMessage(changes) {
  const types = {
    'SKILL.md': 'skill',
    '.md': 'docs',
    'package.json': 'deps',
    'config': 'config',
    'memory/': 'memory'
  };
  
  // Analyze change patterns
  const patterns = {
    'feat': changes.some(c => c.includes('new')),
    'fix': changes.some(c => c.includes('fix')),
    'improvement': changes.some(c => c.includes('improve')),
    'docs': changes.some(c => c.endsWith('.md'))
  };
  
  // Generate message
  const type = Object.entries(patterns)
    .filter(([_, v]) => v)[0]?.[0] || 'chore';
    
  return `${type}(${Object.keys(patterns).filter(k => patterns[k]).join(',')}): ${changes.length} files updated`;
}
```

### Batch Commit
```typescript
async function batchCommit(options = {}) {
  const {
    maxChanges = 10,
    maxAge = 3600000, // 1 hour
    push = true
  } = options;
  
  // Wait for threshold
  const changes = await waitForChanges(maxChanges);
  
  if (changes.length === 0) return;
  
  // Generate commit message
  const message = await generateCommitMessage(changes);
  
  // Stage and commit
  await git.add('.');
  await git.commit(message);
  
  // Push if enabled
  if (push) {
    await git.push();
    console.log(`✅ Committed and pushed: ${message}`);
  }
}
```

---

## Commit Types

### Conventional Commits
```
feat:     New skill or feature
fix:      Bug fix or improvement
docs:     Documentation changes
style:    Formatting, no code change
refactor: Code refactoring
test:     Adding tests
chore:    Maintenance
perf:     Performance improvement
memory:   Learning/memory update
skill:    Skill enhancement
```

### Auto-Detection
```typescript
const patterns = {
  'feat': [
    'new skill',
    'add skill',
    'create skill'
  ],
  'fix': [
    'fix',
    'bug',
    'error',
    'improve'
  ],
  'skill': [
    'SKILL.md',
    'skill.json',
    'keywords'
  ],
  'memory': [
    'memory/',
    'MEMORY.md',
    'learn'
  ]
};
```

---

## Safety Features

### Approval Modes
```typescript
const approvalModes = {
  // Auto-commit everything
  auto: {},
  
  // Wait for confirmation
  manual: {
    requireApproval: true
  },
  
  // Only certain files
  selective: {
    include: ['skills/', 'docs/'],
    exclude: ['memory/', 'private/']
  },
  
  // Batch only
  batch: {
    maxAge: 3600000,
    push: true
  }
};
```

### Protected Files
```typescript
const protectedFiles = [
  'SOUL.md',      // Identity
  'USER.md',       // User context
  'AGENTS.md',     // Core rules
  '.env',          // Secrets
  'credentials*',  // Credentials
  '*.key'          // Keys
];

// Never auto-commit these
function isProtected(file) {
  return protectedFiles.some(p => 
    file === p || file.match(p.replace('*', '.*'))
  );
}
```

---

## Workflow Integration

### With Runtime-Self-Improvement
```
After skill improvement:
1. Apply change
2. Create backup
3. Generate commit message
4. Auto-commit
5. Push to remote
```

### With Heartbeat
```
During heartbeat:
1. Check for pending changes
2. If > 5 changes or > 1 hour:
3. Batch commit and push
4. Log commit to memory
```

### With Skill-Performance-Monitor
```
On performance improvement:
1. Update skill documentation
2. Commit with performance tag
3. Push for version tracking
```

---

## Usage

### Basic Auto-Commit
```typescript
// Enable auto-commit
const autoCommit = new AutoGitCommit({
  push: true,
  mode: 'batch',
  maxAge: 3600000
});

// Start monitoring
autoCommit.start();
```

### Manual Commit
```typescript
// Force commit now
await autoCommit.commitNow('feat(skills): Added new AI consulting skill');
```

---

## Metrics

| Metric | Target |
|--------|--------|
| Commits/day | 5-20 |
| Push success | 100% |
| Conflicts | <1% |
| Backup created | 100% |

---

## Best Practices

### Do's
✅ Always backup before changes  
✅ Use conventional commits  
✅ Test changes locally first  
✅ Review logs regularly  
✅ Handle conflicts gracefully  

### Don'ts
❌ Never commit secrets  
❌ Don't commit broken changes  
❌ Don't ignore conflicts  
❌ Don't overload commits  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation

---


## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- [runtime-self-improvement](/skills/runtime-self-improvement) - Apply improvements
- [skill-performance-monitor](/skills/skill-performance-monitor) - Track improvements
- [self-improving-agent](/skills/self-improving-agent) - Learn and improve
