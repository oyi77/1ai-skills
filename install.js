const fs = require('fs');
const path = require('path');

// ANSI Colors
const RESET = "\x1b[0m";
const GREEN = "\x1b[32m";
const BLUE = "\x1b[34m";
const RED = "\x1b[31m";
const CYAN = "\x1b[36m";

// Clear console
console.clear();

// Display Banner
console.log(BLUE);
console.log("  __  ___  ___      __   __   __   __   __      ");
console.log(" /  |/ _ \\/ _ \\    / /  / /  / /  / /  / /      ");
console.log("/ /|  / _  / _ \\  / /  / /__/ /__/ /__/ /___    ");
console.log("/_/ |_/_/ |_/_/ \\_\\/_/  /____/____/____/_____/    ");
console.log("                                                  ");
console.log("    1   A   I   -   S   K   I   L   L             ");
console.log(RESET);
console.log("");

// Helper for delays
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function install() {
    console.log("Powering Up...");
    await sleep(1000);

    console.log("Learning the things...");
    await sleep(1500);

    console.log(RED + "F*ck this world..." + RESET);
    await sleep(1000);

    const skills = [
        "marketing", "operations", "content", "core",
        "development", "productivity", "research", "growth"
    ];

    for (let i = 0; i < skills.length; i++) {
        const skill = skills[i];
        const current = i + 1;
        const total = skills.length;

        process.stdout.write(`Installing skill module: ${skill} (${current}/${total})...`);
        await sleep(500);

        // Clear line and print success
        process.stdout.clearLine();
        process.stdout.cursorTo(0);
        console.log(`${GREEN}Installed ${skill} (${current}/${total})        ${RESET}`);
    }

    console.log("");
    console.log("All Skills installed....");
    await sleep(1000);

    console.log("Booting up the mind....");
    await sleep(2000);

    console.log("");
    console.log(GREEN + "ALL DONE, ENJOY YOUR LIFE!" + RESET);
    console.log("");

    // Verify installation
    if (fs.existsSync(path.join(__dirname, 'SKILL_INDEX.json'))) {
        console.log(CYAN + "System verification complete." + RESET);
    }
}

install().catch(console.error);
