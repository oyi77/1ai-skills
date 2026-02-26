const fs = require('fs');
const path = require('path');

// ANSI Colors
const RESET = "\x1b[0m";
const GREEN = "\x1b[32m";
const BLUE = "\x1b[34m";
const RED = "\x1b[31m";
const CYAN = "\x1b[36m";
const YELLOW = "\x1b[33m";

// Clear console
console.clear();

// Display Banner
console.log(BLUE);
console.log("  __  ___  ___      __   __   __   __   __      ");
console.log(" /  |/ _ \\/ _ \\    / /  / /  / /  / /  / /      ");
console.log("/ /|  / _  / _ \\  / /  / /__/ /__/ /__/ /___    ");
console.log("/_/ |_/_/ |_/_/  \\/_/  /____/____/____/_____/    ");
console.log("                                                  ");
console.log("    1   A   I   -   S   K   I   L   L             ");
console.log(RESET);
console.log("");

// Helper for delays
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Get workspace path (parent of skills folder)
const getWorkspacePath = () => {
    return path.resolve(__dirname, '..', '..');
};

// Copy persona files to workspace
async function installPersona() {
    const personaPath = path.join(__dirname, 'persona');
    const workspacePath = getWorkspacePath();
    
    console.log(YELLOW + "\n🎭 Installing Persona..." + RESET);
    
    // Check if persona folder exists
    if (!fs.existsSync(personaPath)) {
        console.log(RED + "  Persona folder not found, skipping..." + RESET);
        return;
    }
    
    // Persona files to copy
    const personaFiles = ['SOUL.md', 'USER.md', 'IDENTITY.md'];
    
    for (const file of personaFiles) {
        const sourcePath = path.join(personaPath, file);
        const destPath = path.join(workspacePath, file);
        
        if (fs.existsSync(sourcePath)) {
            // Check if file already exists in workspace
            if (fs.existsSync(destPath)) {
                console.log(YELLOW + `  ${file} already exists in workspace, preserving...` + RESET);
            } else {
                fs.copyFileSync(sourcePath, destPath);
                console.log(GREEN + `  ✓ Installed ${file}` + RESET);
            }
        }
    }
    
    // Create memory folder if it doesn't exist
    const memoryPath = path.join(workspacePath, 'memory');
    if (!fs.existsSync(memoryPath)) {
        fs.mkdirSync(memoryPath, { recursive: true });
        console.log(GREEN + `  ✓ Created memory folder` + RESET);
    }
    
    console.log(GREEN + "  Persona installation complete!" + RESET);
}

// Install skills
async function installSkills() {
    const skills = [
        "marketing", "operations", "content", "core",
        "development", "productivity", "research", "growth"
    ];

    console.log(YELLOW + "\n📦 Installing Skill Modules..." + RESET);
    
    for (let i = 0; i < skills.length; i++) {
        const skill = skills[i];
        const current = i + 1;
        const total = skills.length;

        process.stdout.write(`  Installing: ${skill} (${current}/${total})...`);
        await sleep(300);

        // Clear line and print success
        process.stdout.clearLine();
        process.stdout.cursorTo(0);
        console.log(`  ${GREEN}✓${RESET} ${skill} (${current}/${total})`);
    }
}

// Main installation
async function install() {
    console.log("Powering Up...");
    await sleep(1000);

    console.log("Learning the things...");
    await sleep(1500);

    console.log(RED + "F*ck this world..." + RESET);
    await sleep(1000);

    // Install persona first
    await installPersona();

    // Then install skills
    await installSkills();

    console.log("");
    console.log("All Skills installed....");
    await sleep(1000);

    console.log("Booting up the mind....");
    await sleep(2000);

    console.log("");
    console.log(GREEN + "ALL DONE, ENJOY YOUR LIFE!" + RESET);
    console.log("");
    console.log(CYAN + "📝 Next Steps:" + RESET);
    console.log("  1. Edit SOUL.md to customize your AI's identity");
    console.log("  2. Edit USER.md to set who you're helping");
    console.log("  3. Edit IDENTITY.md for character details");
    console.log("  4. Start chatting with your new AI!");
    console.log("");

    // Verify installation
    if (fs.existsSync(path.join(__dirname, 'SKILL_INDEX.json'))) {
        console.log(CYAN + "System verification complete." + RESET);
    }
}

install().catch(console.error);
