const fs = require('fs');
const path = require('path');
const os = require('os');

const GREEN = "\x1b[32m";
const RED = "\x1b[31m";
const YELLOW = "\x1b[33m";
const CYAN = "\x1b[36m";
const BLUE = "\x1b[34m";
const RESET = "\x1b[0m";

const SKILL_INDEX_PATH = path.join(__dirname, 'skill-index.json');

function verifyInstallation() {
    console.log(BLUE);
    console.log("  __  ___  ___      __   __   __   __   __      ");
    console.log(" /  |/ _ \\/ _ \\    / /  / /  / /  / /  / /      ");
    console.log("/ /|  / _  / _ \\  / /  / /__/ /__/ /__/ /___    ");
    console.log("/_/ |_/_/ |_/_/  \\_\\/_/  /____/____/____/_____/    ");
    console.log("                                                  ");
    console.log("    V   E   R   I   F   I   C   A   T   I   O   N");
    console.log(RESET);
    console.log("");

    let allPassed = true;

    console.log("Checking installation components...\n");

    console.log(`${CYAN}1. Skill Index:${RESET}`);
    if (fs.existsSync(SKILL_INDEX_PATH)) {
        try {
            const index = JSON.parse(fs.readFileSync(SKILL_INDEX_PATH, 'utf8'));
            console.log(`   ${GREEN}[PASS]${RESET} skill-index.json found`);
            console.log(`   Skills: ${index.skills ? index.skills.length : 0}`);
            console.log(`   Teams: ${index.teams ? index.teams.length : 0}`);
        } catch (e) {
            console.log(`   ${RED}[FAIL]${RESET} skill-index.json is invalid JSON`);
            allPassed = false;
        }
    } else {
        console.log(`   ${RED}[FAIL]${RESET} skill-index.json not found`);
        allPassed = false;
    }
    console.log("");

    console.log(`${CYAN}2. Installation Scripts:${RESET}`);
    const scripts = ['install-skills.js', 'list-skills.js', 'verify-install.js'];
    scripts.forEach(script => {
        const scriptPath = path.join(__dirname, script);
        if (fs.existsSync(scriptPath)) {
            console.log(`   ${GREEN}[PASS]${RESET} ${script}`);
        } else {
            console.log(`   ${RED}[FAIL]${RESET} ${script} not found`);
            allPassed = false;
        }
    });
    console.log("");

    console.log(`${CYAN}3. Package Configuration:${RESET}`);
    const configs = ['package.json', 'setup.py', 'MANIFEST.in', 'README.md', 'requirements.txt'];
    configs.forEach(config => {
        const configPath = path.join(__dirname, config);
        if (fs.existsSync(configPath)) {
            console.log(`   ${GREEN}[PASS]${RESET} ${config}`);
        } else {
            console.log(`   ${YELLOW}[WARN]${RESET} ${config} not found`);
        }
    });
    console.log("");

    console.log(`${CYAN}4. Skill Directories:${RESET}`);
    const rootDir = path.resolve(path.join(__dirname, '..'));
    const categories = ['core', 'development', 'marketing', 'sales', 'content', 'research', 'operations', 'productivity', 'automation', 'trading', 'growth'];
    let totalSkills = 0;

    categories.forEach(cat => {
        const catPath = path.join(rootDir, cat);
        if (fs.existsSync(catPath)) {
            try {
                const entries = fs.readdirSync(catPath, { withFileTypes: true });
                const skillCount = entries.filter(e => e.isDirectory()).length;
                if (skillCount > 0) {
                    console.log(`   ${GREEN}[OK]${RESET} ${cat}: ${skillCount} skills`);
                    totalSkills += skillCount;
                }
            } catch (e) {
                console.log(`   ${YELLOW}[WARN]${RESET} ${cat}: Could not read directory`);
            }
        }
    });
    console.log(`   Total local skills found: ${totalSkills}`);
    console.log("");

    console.log(`${CYAN}5. Target Directories:${RESET}`);
    const homedir = os.homedir();
    const targetDirs = [
        path.join(homedir, '.opencode', 'skills'),
        path.join(homedir, '.claude', 'skills'),
        path.join(homedir, '.openclaw', 'workspace', 'skills')
    ];

    targetDirs.forEach(dir => {
        if (fs.existsSync(dir)) {
            try {
                const entries = fs.readdirSync(dir, { withFileTypes: true });
                const skillCount = entries.filter(e => e.isDirectory()).length;
                console.log(`   ${GREEN}[EXISTS]${RESET} ${dir} (${skillCount} categories)`);
            } catch (e) {
                console.log(`   ${GREEN}[EXISTS]${RESET} ${dir}`);
            }
        } else {
            console.log(`   ${YELLOW}[NOT FOUND]${RESET} ${dir}`);
        }
    });
    console.log("");

    console.log("------------------------------------------------");
    if (allPassed) {
        console.log(`${GREEN}VERIFICATION PASSED${RESET}`);
        console.log("");
        console.log("1ai-skills-bundle is properly installed!");
        console.log("Skills are available to your AI agents.");
    } else {
        console.log(`${RED}VERIFICATION FAILED${RESET}`);
        console.log("");
        console.log("Some components are missing. Try reinstalling:");
        console.log("  npm install @1ai/1ai-skills-bundle");
    }
    console.log("");
}

verifyInstallation();
