#!/usr/bin/env node
'use strict';

/**
 * 1ai-skills Dependency Installer
 * Installs all required packages for 301 skills with external dependencies
 * 
 * Usage: node scripts/install-skill-deps.js [--category <cat>] [--dry-run]
 * Also runs automatically via npm postinstall.
 */

const { execSync } = require('child_process');
const os = require('os');
const fs = require('fs');

const PLATFORM = os.platform();
const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const CATEGORY = args.find(a => !a.startsWith('--'));

// Colors
const c = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  dim: '\x1b[2m'
};

function log(msg, color = 'reset') {
  console.log(`${c[color]}${msg}${c.reset}`);
}

function run(cmd, silent = true) {
  if (DRY_RUN) {
    log(`  [DRY RUN] ${cmd}`, 'dim');
    return true;
  }
  try {
    execSync(cmd, { 
      encoding: 'utf8', 
      stdio: silent ? 'pipe' : 'inherit',
      timeout: 300000 
    });
    return true;
  } catch (err) {
    return false;
  }
}

function check(cmd) {
  try {
    execSync(`which ${cmd}`, { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

function has(pkg, manager) {
  try {
    if (manager === 'npm') {
      execSync(`npm list -g ${pkg}`, { stdio: 'pipe' });
      return true;
    } else if (manager === 'pip') {
      execSync(`python3 -c "import ${pkg.replace('-', '_').split('[')[0]}"`, { stdio: 'pipe' });
      return true;
    } else if (manager === 'brew') {
      execSync(`brew list ${pkg}`, { stdio: 'pipe' });
      return true;
    }
  } catch {}
  return false;
}

// ─────────────────────────────────────────────────────────────────────────────
// REQUIREMENTS BY CATEGORY
// ─────────────────────────────────────────────────────────────────────────────

const REQUIREMENTS = {
  mcp: {
    name: 'MCP Servers (codebase-memory + agent-reach)',
    packages: [
      { name: 'cbm', check: () => check('cbm'), install: () => run('node scripts/install-mcp-tools.js') }
    ]
  },
  
  npm: {
    name: 'NPM Packages',
    packages: [
      { name: 'wscat', check: () => has('wscat', 'npm'), install: () => run('npm install -g wscat') },
      { name: 'newman', check: () => has('newman', 'npm'), install: () => run('npm install -g newman') },
      { name: 'flowise', check: () => has('flowise', 'npm'), install: () => run('npm install -g flowise') },
      // Content UI frameworks (dev deps, skip for global)
      // { name: 'antd', check: () => false, install: () => run('npm install antd @ant-design/icons') },
    ]
  },
  
  python: {
    name: 'Python Packages',
    packages: [
      // Cybersecurity essentials
      { name: 'requests', check: () => has('requests', 'pip'), install: () => run('pip3 install requests') },
      { name: 'scapy', check: () => has('scapy', 'pip'), install: () => run('pip3 install scapy') },
      { name: 'impacket', check: () => has('impacket', 'pip'), install: () => run('pip3 install impacket') },
      { name: 'pwntools', check: () => has('pwn', 'pip'), install: () => run('pip3 install pwntools') },
      { name: 'frida-tools', check: () => has('frida', 'pip'), install: () => run('pip3 install frida-tools') },
      { name: 'volatility3', check: () => has('volatility3', 'pip'), install: () => run('pip3 install volatility3') },
      { name: 'semgrep', check: () => check('semgrep'), install: () => run('pip3 install semgrep') },
      { name: 'trufflehog', check: () => check('trufflehog'), install: () => run('pip3 install trufflehog') },
      { name: 'sqlmap', check: () => check('sqlmap'), install: () => run('pip3 install sqlmap') },
      { name: 'sherlock-project', check: () => check('sherlock'), install: () => run('pip3 install sherlock-project') },
      { name: 'shodan', check: () => has('shodan', 'pip'), install: () => run('pip3 install shodan') },
      { name: 'dnstwist', check: () => check('dnstwist'), install: () => run('pip3 install dnstwist') },
      { name: 'oletools', check: () => has('oletools', 'pip'), install: () => run('pip3 install oletools') },
      { name: 'yara-python', check: () => has('yara', 'pip'), install: () => run('pip3 install yara-python') },
      { name: 'pefile', check: () => has('pefile', 'pip'), install: () => run('pip3 install pefile') },
      { name: 'sslyze', check: () => check('sslyze'), install: () => run('pip3 install sslyze') },
      { name: 'boto3', check: () => has('boto3', 'pip'), install: () => run('pip3 install boto3') },
      { name: 'checkov', check: () => check('checkov'), install: () => run('pip3 install checkov') },
      { name: 'prowler', check: () => check('prowler'), install: () => run('pip3 install prowler') },
      // Content/media
      { name: 'moviepy', check: () => has('moviepy', 'pip'), install: () => run('pip3 install moviepy') },
      { name: 'edge-tts', check: () => has('edge_tts', 'pip'), install: () => run('pip3 install edge-tts') },
      { name: 'faster-whisper', check: () => has('faster_whisper', 'pip'), install: () => run('pip3 install faster-whisper') },
      // Utilities
      { name: 'pyjwt', check: () => has('jwt', 'pip'), install: () => run('pip3 install pyjwt') },
      { name: 'jinja2', check: () => has('jinja2', 'pip'), install: () => run('pip3 install jinja2') },
      { name: 'watchdog', check: () => has('watchdog', 'pip'), install: () => run('pip3 install watchdog') },
      { name: 'websockets', check: () => has('websockets', 'pip'), install: () => run('pip3 install websockets') },
      { name: 'telethon', check: () => has('telethon', 'pip'), install: () => run('pip3 install telethon') },
    ]
  },
  
  brew: {
    name: 'Homebrew Packages',
    packages: [
      { name: 'ffmpeg', check: () => check('ffmpeg'), install: () => run('brew install ffmpeg') },
      { name: 'yara', check: () => check('yara'), install: () => run('brew install yara') },
      { name: 'trivy', check: () => check('trivy'), install: () => run('brew install trivy') },
      { name: 'semgrep', check: () => check('semgrep'), install: () => run('brew install semgrep') },
      { name: 'trufflehog', check: () => check('trufflehog'), install: () => run('brew install trufflehog') },
      { name: 'git-secrets', check: () => check('git-secrets'), install: () => run('brew install git-secrets') },
      { name: 'cosign', check: () => check('cosign'), install: () => run('brew install cosign') },
      { name: 'tfsec', check: () => check('tfsec'), install: () => run('brew install tfsec') },
      { name: 'terrascan', check: () => check('terrascan'), install: () => run('brew install terrascan') },
      { name: 'kubeaudit', check: () => check('kubeaudit'), install: () => run('brew install kubeaudit') },
    ]
  }
};

// ─────────────────────────────────────────────────────────────────────────────
// INSTALLER
// ─────────────────────────────────────────────────────────────────────────────

function installCategory(cat) {
  const data = REQUIREMENTS[cat];
  if (!data) {
    log(`❌ Unknown category: ${cat}`, 'red');
    return;
  }
  
  log(`\n${'─'.repeat(60)}`, 'dim');
  log(`📦 ${data.name}`, 'blue');
  log(`${'─'.repeat(60)}`, 'dim');
  
  let installed = 0;
  let skipped = 0;
  let failed = 0;
  
  for (const pkg of data.packages) {
    if (pkg.check()) {
      log(`  ✅ ${pkg.name} (already installed)`, 'dim');
      skipped++;
      continue;
    }
    
    log(`  📥 Installing ${pkg.name}...`, 'yellow');
    if (pkg.install()) {
      log(`  ✅ ${pkg.name}`, 'green');
      installed++;
    } else {
      log(`  ⚠️  ${pkg.name} (failed, may need manual install)`, 'yellow');
      failed++;
    }
  }
  
  log(`  Result: ${installed} installed, ${skipped} skipped, ${failed} failed`, 'dim');
}

function main() {
  log('\n🚀 1ai-skills Dependency Installer', 'blue');
  log('=' .repeat(60), 'blue');
  
  if (DRY_RUN) {
    log('  ⚠️  DRY RUN MODE — no changes will be made', 'yellow');
  }
  
  // Check prerequisites
  log('\n🔍 Checking prerequisites...', 'dim');
  
  if (!check('node')) {
    log('❌ Node.js not found. Please install Node.js 18+', 'red');
    process.exit(1);
  }
  
  if (!check('python3')) {
    log('❌ Python 3 not found. Please install Python 3.9+', 'red');
    process.exit(1);
  }
  
  if (PLATFORM === 'darwin' && !check('brew')) {
    log('⚠️  Homebrew not found. Installing...', 'yellow');
    run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"');
  }
  
  // Install categories
  const cats = CATEGORY ? [CATEGORY] : Object.keys(REQUIREMENTS);
  
  for (const cat of cats) {
    installCategory(cat);
  }
  
  // Summary
  log(`\n${'═'.repeat(60)}`, 'blue');
  log('✅ Installation complete!', 'green');
  log(`${'═'.repeat(60)}`, 'blue');
  
  log('\n📝 Notes:', 'dim');
  log('  • Some cybersecurity tools may need sudo for full functionality', 'dim');
  log('  • API keys should be configured in ~/.omp/mcp.json or environment', 'dim');
  log('  • Run with --dry-run to preview without installing', 'dim');
  log('  • Run with --category <npm|python|brew|mcp> to install specific category', 'dim');
  
  log('\n🔑 API Keys (configure in ~/.omp/mcp.json or .env):', 'dim');
  log('  • OPENAI_API_KEY — for AI-powered features', 'dim');
  log('  • ANTHROPIC_API_KEY — for Claude integration', 'dim');
  log('  • GOOGLE_API_KEY — for Gemini integration', 'dim');
  log('  • GITHUB_TOKEN — for GitHub API access', 'dim');
  
  log('');
}

main();
