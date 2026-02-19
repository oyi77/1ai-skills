const fs = require('fs');
const path = require('path');
const os = require('os');

const RESET = "\x1b[0m";
const GREEN = "\x1b[32m";
const BLUE = "\x1b[34m";
const CYAN = "\x1b[36m";
const YELLOW = "\x1b[33m";

console.log(BLUE);
console.log("  __  ___  ___      __   __   __   __   __      ");
console.log(" /  |/ _ \\/ _ \\    / /  / /  / /  / /  / /      ");
console.log("/ /|  / _  / _ \\  / /  / /__/ /__/ /__/ /___    ");
console.log("/_/ |_/_/ |_/_/  \\_\\/_/  /____/____/____/_____/    ");
console.log("                                                  ");
console.log("    1   A   I   -   S   K   I   L   L   S         ");
console.log(RESET);
console.log("");

const SKILL_INDEX_PATH = path.join(__dirname, 'skill-index.json');

function getSkillIndex() {
    try {
        if (fs.existsSync(SKILL_INDEX_PATH)) {
            return JSON.parse(fs.readFileSync(SKILL_INDEX_PATH, 'utf8'));
        }
    } catch (e) {
        console.error("Could not load skill index:", e.message);
    }
    return { skills: [], teams: [] };
}

function getSkillDirs() {
    const rootDir = path.resolve(path.join(__dirname, '..'));
    const categories = ['core', 'development', 'marketing', 'sales', 'content', 'research', 'operations', 'productivity', 'automation', 'trading', 'growth'];
    const skillDirs = [];

    categories.forEach(cat => {
        const catPath = path.join(rootDir, cat);
        if (fs.existsSync(catPath)) {
            const entries = fs.readdirSync(catPath, { withFileTypes: true });
            entries.forEach(entry => {
                if (entry.isDirectory()) {
                    const skillPath = path.join(catPath, entry.name);
                    const skillMdPath = path.join(skillPath, 'SKILL.md');
                    if (fs.existsSync(skillMdPath)) {
                        skillDirs.push({
                            name: entry.name,
                            path: skillPath,
                            category: cat,
                            source: 'local'
                        });
                    }
                }
            });
        }
    });

    return skillDirs;
}

function getTargetDir() {
    const homedir = os.homedir();
    const candidates = [
        path.join(homedir, '.opencode', 'skills'),
        path.join(homedir, '.claude', 'skills'),
        path.join(homedir, '.openclaw', 'workspace', 'skills'),
        path.join(process.cwd(), 'skills')
    ];

    for (const dir of candidates) {
        const parent = path.dirname(dir);
        if (fs.existsSync(parent) || dir === candidates[candidates.length - 1]) {
            return dir;
        }
    }

    return candidates[0];
}

function installSkills() {
    console.log("Loading skill index...");
    const skillIndex = getSkillIndex();
    const localSkills = skillIndex.skills.filter(s => s.source === 'local');
    const externalSkills = skillIndex.skills.filter(s => s.source === 'external');

    console.log(`Found ${localSkills.length} local skills and ${externalSkills.length} external skills`);
    console.log("");

    const targetDir = getTargetDir();
    console.log(`Target directory: ${CYAN}${targetDir}${RESET}`);
    console.log("");

    if (!fs.existsSync(targetDir)) {
        console.log("Creating skills directory...");
        fs.mkdirSync(targetDir, { recursive: true });
    }

    const skillDirs = getSkillDirs();
    console.log(`Installing ${skillDirs.length} local skills...\n`);

    let installed = 0;
    let skipped = 0;

    skillDirs.forEach((skill, index) => {
        const destPath = path.join(targetDir, skill.category, skill.name);
        
        try {
            if (!fs.existsSync(path.join(targetDir, skill.category))) {
                fs.mkdirSync(path.join(targetDir, skill.category), { recursive: true });
            }

            if (!fs.existsSync(destPath)) {
                copyDirRecursive(skill.path, destPath);
                console.log(`${GREEN}[+]${RESET} ${skill.category}/${skill.name}`);
                installed++;
            } else {
                console.log(`${YELLOW}[=]${RESET} ${skill.category}/${skill.name} (already exists)`);
                skipped++;
            }
        } catch (err) {
            console.error(`${RED}[-]${RESET} ${skill.category}/${skill.name} - ${err.message}`);
        }
    });

    console.log("");
    console.log(GREEN + "Installation complete!" + RESET);
    console.log(`Installed: ${installed} skills`);
    console.log(`Skipped: ${skipped} skills (already installed)`);
    console.log("");
    console.log(`${CYAN}Skills installed to: ${targetDir}${RESET}`);
    console.log("");
    console.log("Usage: Reference skills by name in your AI agent");
    console.log("Example: 'Use the brainstorming skill to plan this project'");
    console.log("");
}

function copyDirRecursive(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }

    const entries = fs.readdirSync(src, { withFileTypes: true });

    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isDirectory()) {
            copyDirRecursive(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

installSkills();
