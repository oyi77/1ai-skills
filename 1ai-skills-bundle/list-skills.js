const fs = require('fs');
const path = require('path');

const BLUE = "\x1b[34m";
const GREEN = "\x1b[32m";
const CYAN = "\x1b[36m";
const RESET = "\x1b[0m";

const SKILL_INDEX_PATH = path.join(__dirname, 'skill-index.json');

function loadSkillIndex() {
    try {
        if (fs.existsSync(SKILL_INDEX_PATH)) {
            return JSON.parse(fs.readFileSync(SKILL_INDEX_PATH, 'utf8'));
        }
    } catch (e) {
        console.error("Could not load skill index:", e.message);
    }
    return { skills: [], teams: [] };
}

function listSkills() {
    const skillIndex = loadSkillIndex();
    const skills = skillIndex.skills || [];
    const teams = skillIndex.teams || [];

    console.log(BLUE);
    console.log("  __  ___  ___      __   __   __   __   __      ");
    console.log(" /  |/ _ \\/ _ \\    / /  / /  / /  / /  / /      ");
    console.log("/ /|  / _  / _ \\  / /  / /__/ /__/ /__/ /___    ");
    console.log("/_/ |_/_/ |_/_/  \\_\\/_/  /____/____/____/_____/    ");
    console.log("                                                  ");
    console.log("    1   A   I   -   S   K   I   L   L   S         ");
    console.log(RESET);
    console.log("");

    const localSkills = skills.filter(s => s.source === 'local');
    const externalSkills = skills.filter(s => s.source === 'external');

    console.log(`${CYAN}Total Skills: ${skills.length}${RESET}`);
    console.log(`  Local: ${GREEN}${localSkills.length}${RESET}`);
    console.log(`  External: ${GREEN}${externalSkills.length}${RESET}`);
    console.log("");

    const categories = {};
    skills.forEach(skill => {
        if (skill.domains && skill.domains.length > 0) {
            const domain = skill.domains[0];
            if (!categories[domain]) {
                categories[domain] = [];
            }
            categories[domain].push(skill);
        } else if (!categories['other']) {
            categories['other'] = [];
            categories['other'].push(skill);
        } else {
            categories['other'].push(skill);
        }
    });

    console.log(CYAN + "Skills by Category:" + RESET);
    console.log("");

    Object.keys(categories).sort().forEach(category => {
        console.log(BLUE + `  ${category.toUpperCase()}` + RESET);
        categories[category].forEach(skill => {
            const source = skill.source === 'local' ? GREEN + '(local)' + RESET : YELLOW + '(external)' + RESET;
            console.log(`    - ${skill.name} ${source}`);
            if (skill.description) {
                console.log(`      ${skill.description.substring(0, 60)}...`);
            }
        });
        console.log("");
    });

    if (teams.length > 0) {
        console.log(CYAN + "Team Orchestrators:" + RESET);
        console.log("");
        teams.forEach(team => {
            console.log(BLUE + `  ${team.name}` + RESET);
            console.log(`    Skills: ${team.skills.join(', ')}`);
            console.log("");
        });
    }

    console.log(GREEN + "Use a skill by referencing its name in your AI agent." + RESET);
    console.log("");
}

const YELLOW = "\x1b[33m";

listSkills();
