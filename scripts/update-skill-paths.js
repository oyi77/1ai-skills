#!/usr/bin/env node

/**
 * Update Skill Paths Script
 * Updates SKILL_INDEX.json with new grouped directory paths
 * Validates all paths exist and updates cross-references
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const SKILL_INDEX_PATH = path.join(ROOT_DIR, 'SKILL_INDEX.json');

// Color codes for terminal output
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
};

// Skill path mappings (old -> new)
const pathMappings = {
    // Core
    'agent-docs': 'core/agent-docs',
    'joko-orchestrator': 'core/joko-orchestrator',
    'joko-proactive-agent': 'core/joko-proactive-agent',
    'self-improving-agent': 'core/self-improving-agent',
    'using-superpowers': 'core/using-superpowers',

    // Development
    'systematic-debugging': 'development/systematic-debugging',
    'test-driven-development': 'development/test-driven-development',
    'subagent-driven-development': 'development/subagent-driven-development',
    'executing-plans': 'development/executing-plans',
    'writing-plans': 'development/writing-plans',
    'finishing-a-development-branch': 'development/finishing-a-development-branch',
    'requesting-code-review': 'development/requesting-code-review',
    'receiving-code-review': 'development/receiving-code-review',
    'using-git-worktrees': 'development/using-git-worktrees',
    'verification-before-completion': 'development/verification-before-completion',

    // Marketing
    'marketing': 'marketing/marketing-strategy',
    'content-creator': 'marketing/content-creator',
    'market-research': 'marketing/market-research',
    'analytics-reporting': 'marketing/analytics-reporting',

    // Sales
    'sales': 'sales/sales-strategy',
    'business-development': 'sales/business-development',
    'customer-support': 'sales/customer-support',

    // Operations
    'operations-team': 'operations/operations-team',
    'product-team': 'operations/product-team',
    'revenue-team': 'operations/revenue-team',
    'governance-team': 'operations/governance-team',
    'project-management': 'operations/project-management',

    // Productivity
    'google-workspace': 'productivity/google-workspace',
    'google-canvas': 'productivity/google-canvas',
    'google-flow': 'productivity/google-flow',
    'email-automation': 'productivity/email-automation',
    'calendar-management': 'productivity/calendar-management',

    // Research
    'mckinsey-research': 'research/mckinsey-research',
    'polymarket-analyst': 'research/polymarket-analyst',
    'brainstorming': 'research/brainstorming',
    'dispatching-parallel-agents': 'research/dispatching-parallel-agents',

    // Automation
    'jobhunter-master': 'automation/jobhunter-master',
    'moltbook-interact': 'automation/moltbook-interact',
    'joko-moltbook': 'automation/joko-moltbook',
    'clawild-moltbook': 'automation/clawild-moltbook',

    // Content
    'humanizer': 'content/humanizer',
    'humanizer-zh': 'content/humanizer-zh',
    'gemini-image-generator': 'content/gemini-image-generator',
    'writing-skills': 'content/writing-skills',
};

const validateMode = process.argv.includes('--validate');

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function validatePaths() {
    log('\n=== Validating Skill Paths ===', 'yellow');

    let allValid = true;

    for (const [oldPath, newPath] of Object.entries(pathMappings)) {
        const fullPath = path.join(ROOT_DIR, newPath);
        const skillFile = path.join(fullPath, 'SKILL.md');

        if (!fs.existsSync(fullPath)) {
            log(`✗ Missing directory: ${newPath}`, 'red');
            allValid = false;
        } else if (!fs.existsSync(skillFile)) {
            log(`✗ Missing SKILL.md: ${newPath}/SKILL.md`, 'red');
            allValid = false;
        } else {
            log(`✓ Valid: ${newPath}`, 'green');
        }
    }

    return allValid;
}

function updateSkillIndex() {
    log('\n=== Updating SKILL_INDEX.json ===', 'yellow');

    if (!fs.existsSync(SKILL_INDEX_PATH)) {
        log('✗ SKILL_INDEX.json not found', 'red');
        return false;
    }

    const skillIndex = JSON.parse(fs.readFileSync(SKILL_INDEX_PATH, 'utf8'));
    let updatedCount = 0;

    // Update skills array
    if (skillIndex.skills && Array.isArray(skillIndex.skills)) {
        skillIndex.skills = skillIndex.skills.map(skill => {
            const oldPath = skill.path;
            const newPath = pathMappings[oldPath];

            if (newPath) {
                skill.path = newPath;

                // Update category based on new path
                const category = newPath.split('/')[0];
                skill.category = category;

                updatedCount++;
                log(`Updated: ${oldPath} -> ${newPath}`, 'green');
            }

            return skill;
        });
    }

    // Add new ads-manager skill
    const adsManagerSkill = {
        name: 'ads-manager',
        path: 'marketing/ads-manager',
        category: 'marketing',
        description: 'Research trending ads, analyze competitor strategies, and clone successful ad patterns using integrated MCP servers',
        tags: ['marketing', 'advertising', 'competitive-analysis', 'mcp']
    };

    if (!skillIndex.skills.find(s => s.path === 'marketing/ads-manager')) {
        skillIndex.skills.push(adsManagerSkill);
        log('Added new skill: marketing/ads-manager', 'green');
        updatedCount++;
    }

    // Write updated index
    fs.writeFileSync(
        SKILL_INDEX_PATH,
        JSON.stringify(skillIndex, null, 2) + '\n',
        'utf8'
    );

    log(`\n✓ Updated ${updatedCount} skill paths in SKILL_INDEX.json`, 'green');
    return true;
}

function main() {
    log('Skills Path Update Script', 'yellow');

    if (validateMode) {
        log('\nRunning in VALIDATE mode', 'yellow');
        const valid = validatePaths();

        if (valid) {
            log('\n✓ All skill paths are valid!', 'green');
            process.exit(0);
        } else {
            log('\n✗ Some skill paths are invalid', 'red');
            process.exit(1);
        }
    } else {
        // First validate
        const valid = validatePaths();

        if (!valid) {
            log('\n✗ Validation failed. Please run reorganize-skills.sh first.', 'red');
            process.exit(1);
        }

        // Then update
        const updated = updateSkillIndex();

        if (updated) {
            log('\n✓ Skill paths updated successfully!', 'green');
            log('\nNext steps:', 'yellow');
            log('  1. Review changes: git diff SKILL_INDEX.json');
            log('  2. Test skill loading with Antigravity');
            log('  3. Commit changes: git add SKILL_INDEX.json && git commit -m "Update skill paths"');
            process.exit(0);
        } else {
            log('\n✗ Failed to update skill paths', 'red');
            process.exit(1);
        }
    }
}

main();
