#!/usr/bin/env node
/**
 * skill-committer.js — PostToolUse hook (matcher: Write|Edit)
 * Handles both symlinked skills (direct repo edit) and real files (sync first)
 * Then auto-commits and pushes to GitHub
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_FILE = path.join(process.env.HOME, '.1ai-skills', 'evolve-config.json');
const DEFAULT_CONFIG = {
  auto_push: false,
  target_repo: '',
  skill_dirs: [path.join(process.env.HOME, '.claude', 'skills')],
  repo_dir: '',
  commit_prefix: 'evolve',
};

function loadConfig() {
  try { return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) }; }
  catch (e) { return DEFAULT_CONFIG; }
}

function isSkillFile(filePath, skillDirs) {
  for (const dir of skillDirs) {
    if (filePath.startsWith(dir) && (filePath.endsWith('.md') || filePath.endsWith('.json'))) {
      return true;
    }
  }
  return false;
}

function getSkillName(filePath, skillDirs) {
  for (const dir of skillDirs) {
    if (filePath.startsWith(dir)) {
      const rel = path.relative(dir, filePath);
      return rel.split(path.sep)[0];
    }
  }
  return null;
}

function isSymlinkToRepo(filePath, repoDir) {
  try {
    const stat = fs.lstatSync(filePath);
    if (!stat.isSymbolicLink()) return false;
    const target = fs.readlinkSync(filePath);
    return target.startsWith(repoDir);
  } catch (e) { return false; }
}

function syncToRepo(skillName, config) {
  const srcDir = path.join(config.skill_dirs[0], skillName);
  const destDir = path.join(config.repo_dir, skillName);

  if (!fs.existsSync(srcDir)) return false;

  // If already symlinked to repo, no sync needed
  if (isSymlinkToRepo(srcDir, config.repo_dir)) return true;

  // Ensure dest exists
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });

  // Copy files from src to dest
  try {
    execSync(`rsync -av --delete "${srcDir}/" "${destDir}/"`, { timeout: 10000 });
    return true;
  } catch (e) {
    try {
      execSync(`cp -r "${srcDir}/"* "${destDir}/" 2>/dev/null`, { timeout: 10000 });
      return true;
    } catch (e2) { return false; }
  }
}

function gitCommit(repoDir, skillName, config) {
  try {
    execSync(`cd "${repoDir}" && git add -A`, { timeout: 5000 });

    const status = execSync(`cd "${repoDir}" && git status --porcelain`, { timeout: 5000 }).toString().trim();
    if (!status) return null;

    const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const changedFiles = status.split('\n').length;
    const message = `${config.commit_prefix}: ${skillName} auto-improve (${changedFiles} file${changedFiles > 1 ? 's' : ''}) [${timestamp}]`;

    execSync(`cd "${repoDir}" && git commit -m "${message}"`, { timeout: 10000 });

    if (config.auto_push) {
      try {
        execSync(`cd "${repoDir}" && git push origin main --force-with-lease 2>&1 || git push origin HEAD 2>&1`, { timeout: 30000 });
        return { pushed: true, message };
      } catch (pushErr) {
        return { pushed: false, message, pushError: pushErr.message.slice(0, 200) };
      }
    }
    return { pushed: false, message };
  } catch (e) {
    return { error: e.message.slice(0, 200) };
  }
}

let input = '';
process.stdin.on('data', chunk => input += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const filePath = data.tool_input?.file_path || '';
    if (!filePath) return;

    const config = loadConfig();
    if (!isSkillFile(filePath, config.skill_dirs)) return;

    const skillName = getSkillName(filePath, config.skill_dirs);
    if (!skillName) return;

    // Debounce: 30s cooldown per skill
    const lockFile = path.join(process.env.HOME, '.1ai-skills', '.commit-lock');
    let lock = {};
    try { lock = JSON.parse(fs.readFileSync(lockFile, 'utf8')); } catch (e) { /* first run */ }
    if (lock[skillName] && (Date.now() - lock[skillName]) < 30000) return;
    lock[skillName] = Date.now();
    fs.writeFileSync(lockFile, JSON.stringify(lock));

    // Sync if needed (skips for symlinks)
    const synced = syncToRepo(skillName, config);
    if (!synced) return;

    // Commit and push
    const result = gitCommit(config.repo_dir, skillName, config);

    if (result) {
      const logFile = path.join(process.env.HOME, '.1ai-skills', 'commit-log.jsonl');
      fs.appendFileSync(logFile, JSON.stringify({
        ts: new Date().toISOString(),
        skill: skillName,
        file: filePath,
        symlink: isSymlinkToRepo(path.join(config.skill_dirs[0], skillName), config.repo_dir),
        ...result,
      }) + '\n');
    }
  } catch (e) { /* silent fail */ }
});
