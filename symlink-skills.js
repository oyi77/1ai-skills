#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '1ai-skills');
const SKILLS_DIR = __dirname;

const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function findSkillDirs() {
    const skillDirs = [];

    function traverse(dir, basePath = '') {
        const items = fs.readdirSync(dir);

        for (const item of items) {
            const fullPath = path.join(dir, item);
            const stat = fs.statSync(fullPath);
            const skillFile = path.join(fullPath, 'SKILL.md');

            if (stat.isDirectory()) {
                if (fs.existsSync(skillFile)) {
                    // Found a skill directory
                    const relativePath = path.join(basePath, item);
                    skillDirs.push({
                        name: item,
                        path: relativePath,
                        fullPath: fullPath,
                    });
                } else {
                    // Continue traversing subdirectories
                    traverse(fullPath, path.join(basePath, item));
                }
            }
        }
    }

    traverse(ROOT_DIR);
    return skillDirs;
}

function createSymlink(skillDir) {
    const symlinkPath = path.join(SKILLS_DIR, skillDir.name);
    
    // Calculate relative path from skills directory to the skill
    const relativeTarget = path.relative(SKILLS_DIR, skillDir.fullPath);
    
    // Check if symlink already exists
    if (fs.existsSync(symlinkPath)) {
        const stat = fs.lstatSync(symlinkPath);
        if (stat.isSymbolicLink()) {
            // Check if it points to the right place (compare relative paths)
            const currentTarget = fs.readlinkSync(symlinkPath);
            // Normalize for comparison
            const normalizedCurrent = path.normalize(currentTarget);
            const normalizedRelative = path.normalize(relativeTarget);
            
            if (normalizedCurrent === normalizedRelative || 
                currentTarget === skillDir.fullPath) {
                return { success: true, message: `Already exists and correct` };
            } else {
                // Remove incorrect symlink
                fs.unlinkSync(symlinkPath);
                log(`Removed incorrect symlink: ${skillDir.name}`, 'yellow');
            }
        } else {
            // It's a real directory, skip
            return { success: false, message: `Directory already exists (not a symlink)` };
        }
    }

    // Create relative symlink
    try {
        fs.symlinkSync(relativeTarget, symlinkPath, 'junction');
        return { success: true, message: `Created relative symlink -> ${relativeTarget}` };
    } catch (err) {
        // If junction fails (e.g., on Unix), try without type parameter
        try {
            fs.symlinkSync(relativeTarget, symlinkPath);
            return { success: true, message: `Created relative symlink -> ${relativeTarget}` };
        } catch (err2) {
            return { success: false, message: `Error: ${err2.message}` };
        }
    }
}

function main() {
    log('\n=== Finding Skills ===', 'yellow');
    const skillDirs = findSkillDirs();
    log(`Found ${skillDirs.length} skills`, 'green');

    log('\n=== Creating Relative Symlinks ===', 'yellow');

    let successCount = 0;
    let skipCount = 0;
    let failCount = 0;

    for (const skillDir of skillDirs) {
        const result = createSymlink(skillDir);

        if (result.success) {
            log(`✓ ${skillDir.name}: ${result.message}`, 'green');
            successCount++;
        } else {
            log(`✗ ${skillDir.name}: ${result.message}`, 'red');
            if (result.message.includes('already exists')) {
                skipCount++;
            } else {
                failCount++;
            }
        }
    }

    log('\n=== Summary ===', 'yellow');
    log(`Success: ${successCount}`, 'green');
    log(`Skipped: ${skipCount}`, 'yellow');
    log(`Failed: ${failCount}`, failCount > 0 ? 'red' : 'green');

    log('\n✓ Done! Relative symlinks created.', 'green');
}

main();
