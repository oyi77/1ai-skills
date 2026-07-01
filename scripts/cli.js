#!/usr/bin/env node
/**
 * 1ai-skills CLI
 * Usage:
 *   1ai-skills update    — Check for updates and apply
 *   1ai-skills version   — Show current version
 *   1ai-skills status    — Show installed skill count + version
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");
const https = require("https");

const PKG_PATH = path.join(__dirname, "..", "package.json");
const pkg = JSON.parse(fs.readFileSync(PKG_PATH, "utf8"));
const CURRENT_VERSION = pkg.version;
const PKG_NAME = pkg.name;

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { "User-Agent": `${PKG_NAME}/${CURRENT_VERSION}` } }, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        return fetch(res.headers.location).then(resolve).catch(reject);
      }
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => resolve(data));
      res.on("error", reject);
    }).on("error", reject);
  });
}

function compareVersions(a, b) {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    if (pa[i] > pb[i]) return 1;
    if (pa[i] < pb[i]) return -1;
  }
  return 0;
}

function countSkills(dir) {
  let count = 0;
  try {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory() && !entry.name.startsWith(".")) {
        const skillPath = path.join(dir, entry.name, "SKILL.md");
        if (fs.existsSync(skillPath)) count++;
        // Check nested (e.g., content/video/remotion/)
        const subDir = path.join(dir, entry.name);
        for (const sub of fs.readdirSync(subDir, { withFileTypes: true })) {
          if (sub.isDirectory() && !sub.name.startsWith(".")) {
            if (fs.existsSync(path.join(subDir, sub.name, "SKILL.md"))) count++;
          }
        }
      }
    }
  } catch {}
  return count;
}

async function checkUpdate() {
  try {
    const data = await fetch(`https://registry.npmjs.org/${PKG_NAME}/latest`);
    const latest = JSON.parse(data);
    const latestVersion = latest.version;
    return { latest: latestVersion, current: CURRENT_VERSION, hasUpdate: compareVersions(latestVersion, CURRENT_VERSION) > 0 };
  } catch {
    return null;
  }
}

async function cmdUpdate() {
  console.log(`\n  1ai-skills v${CURRENT_VERSION}\n`);
  console.log("  Checking for updates...");

  const info = await checkUpdate();
  if (!info) {
    console.log("  ⚠ Could not check for updates (offline or registry error)");
    return;
  }

  if (!info.hasUpdate) {
    console.log("  ✅ Already up to date!");
    return;
  }

  console.log(`\n  📦 New version available: v${info.latest} (current: v${info.current})`);
  console.log(`\n  To update, run:`);
  console.log(`    npm install -g ${PKG_NAME}@latest`);
  console.log(`\n  Or for npx users:`);
  console.log(`    npx ${PKG_NAME}@latest\n`);
}

function cmdVersion() {
  console.log(CURRENT_VERSION);
}

function cmdStatus() {
  const pkgDir = path.join(__dirname, "..");
  const categories = [
    "content", "core", "development", "integrations", "marketing",
    "meta", "mindset", "operations", "productivity", "research",
    "sales", "trading", "data", "devops", "cybersecurity",
    "automation", "financial", "mcp",
  ];
  let total = 0;
  for (const cat of categories) {
    total += countSkills(path.join(pkgDir, cat));
  }
  console.log(`\n  1ai-skills v${CURRENT_VERSION}`);
  console.log(`  ${total} skills across ${categories.length} categories`);
  console.log(`  Repo: https://github.com/oyi77/1ai-skills\n`);
}

// Main
const args = process.argv.slice(2);
const cmd = args[0];

switch (cmd) {
  case "update":
    cmdUpdate();
    break;
  case "version":
    cmdVersion();
    break;
  case "status":
    cmdStatus();
    break;
  default:
    console.log(`
  1ai-skills v${CURRENT_VERSION}

  Usage:
    1ai-skills update    Check for updates
    1ai-skills version   Show version
    1ai-skills status    Show installed skills
`);
}
