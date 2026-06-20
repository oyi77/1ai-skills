#!/usr/bin/env node
'use strict';

/**
 * 1ai-skills MCP Tools Installer
 * Installs codebase-memory-mcp (cbm) and agent-reach for AI agents
 * 
 * Usage: node scripts/install-mcp-tools.js
 * Also runs automatically via npm postinstall.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const HOME = process.env.HOME || process.env.USERPROFILE;
const PLATFORM = os.platform();
const ARCH = os.arch();

// Colors for output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m'
};

function log(msg, color = 'reset') {
  console.log(`${colors[color]}${msg}${colors.reset}`);
}

function run(cmd, silent = false) {
  try {
    return execSync(cmd, { 
      encoding: 'utf8', 
      stdio: silent ? 'pipe' : 'inherit',
      timeout: 120000
    });
  } catch (err) {
    return null;
  }
}

function checkCommand(cmd) {
  return run(`which ${cmd}`, true) !== null;
}

// --- Install codebase-memory-mcp (cbm) ---

function installCodebaseMemory() {
  log('\n📦 Installing codebase-memory-mcp (cbm)...', 'blue');
  
  // Check if already installed
  if (checkCommand('cbm')) {
    const version = run('cbm --version', true);
    log(`✅ cbm already installed: ${version.trim()}`, 'green');
    return true;
  }

  // Determine binary URL
  let binaryUrl;
  if (PLATFORM === 'darwin') {
    if (ARCH === 'arm64') {
      binaryUrl = 'https://github.com/DeusData/codebase-memory-mcp/releases/download/v0.8.1/codebase-memory-mcp-darwin-arm64.tar.gz';
    } else {
      binaryUrl = 'https://github.com/DeusData/codebase-memory-mcp/releases/download/v0.8.1/codebase-memory-mcp-darwin-amd64.tar.gz';
    }
  } else if (PLATFORM === 'linux') {
    if (ARCH === 'arm64') {
      binaryUrl = 'https://github.com/DeusData/codebase-memory-mcp/releases/download/v0.8.1/codebase-memory-mcp-linux-arm64.tar.gz';
    } else {
      binaryUrl = 'https://github.com/DeusData/codebase-memory-mcp/releases/download/v0.8.1/codebase-memory-mcp-linux-amd64.tar.gz';
    }
  } else {
    log(`⚠️  Unsupported platform: ${PLATFORM}`, 'yellow');
    log('   Please install manually: https://github.com/DeusData/codebase-memory-mcp', 'yellow');
    return false;
  }

  log(`   Downloading from: ${binaryUrl}`, 'blue');
  
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cbm-'));
  const tarPath = path.join(tmpDir, 'cbm.tar.gz');
  
  // Download
  run(`curl -L -o ${tarPath} ${binaryUrl}`);
  
  // Extract
  run(`tar -xzf ${tarPath} -C ${tmpDir}`);
  
  // Find binary (named codebase-memory-mcp in tarball)
  const binaryPath = path.join(tmpDir, 'codebase-memory-mcp');
  
  if (!fs.existsSync(binaryPath)) {
    log('❌ Binary not found after extraction', 'red');
    return false;
  }

  // Install to /usr/local/bin (try with sudo if needed)
  const installPath = '/usr/local/bin/cbm';
  
  fs.chmodSync(binaryPath, 0o755);
  
  // Try without sudo first
  try {
    fs.copyFileSync(binaryPath, installPath);
    log('✅ cbm installed to /usr/local/bin/cbm', 'green');
  } catch (err) {
    // Need sudo
    log('   Requires sudo for /usr/local/bin...', 'yellow');
    const result = run(`sudo mv ${binaryPath} ${installPath}`);
    if (result === null) {
      log('❌ Failed to install cbm (sudo required)', 'red');
      log(`   Manual install: mv ${binaryPath} /usr/local/bin/cbm`, 'yellow');
      return false;
    }
    log('✅ cbm installed to /usr/local/bin/cbm', 'green');
  }
  
  // Cleanup
  fs.rmSync(tmpDir, { recursive: true, force: true });
  
  // Verify
  const version = run('cbm --version', true);
  if (version) {
    log(`   Version: ${version.trim()}`, 'green');
    return true;
  }
  
  return false;
}

// --- Install agent-reach ---

function installAgentReach() {
  log('\n📦 Installing agent-reach...', 'blue');
  
  // Check if already installed
  if (checkCommand('agent-reach')) {
    const version = run('agent-reach --version', true);
    log(`✅ agent-reach already installed: ${version ? version.trim() : 'unknown'}`, 'green');
    return true;
  }

  // Check for pipx
  if (!checkCommand('pipx')) {
    log('⚠️  pipx not found. Installing pipx first...', 'yellow');
    
    // Try brew first (macOS/Linux with Homebrew)
    if (checkCommand('brew')) {
      run('brew install pipx');
    } else if (checkCommand('apt-get')) {
      // Debian/Ubuntu
      run('sudo apt-get update && sudo apt-get install -y pipx');
    } else if (checkCommand('dnf')) {
      // Fedora
      run('sudo dnf install -y pipx');
    } else if (checkCommand('pacman')) {
      // Arch
      run('sudo pacman -S --noconfirm python-pipx');
    } else {
      log('❌ Cannot auto-install pipx. Please install manually:', 'red');
      log('   https://pipx.pypa.io/stable/installation/', 'yellow');
      return false;
    }
    
    // Ensure pipx path
    run('pipx ensurepath', true);
  }

  // Install agent-reach from GitHub
  log('   Installing from GitHub (this may take 1-2 minutes)...', 'blue');
  
  const result = run('pipx install git+https://github.com/Panniantong/Agent-Reach.git');
  
  if (result === null) {
    log('❌ Failed to install agent-reach', 'red');
    log('   Manual install: pipx install git+https://github.com/Panniantong/Agent-Reach.git', 'yellow');
    return false;
  }
  
  log('✅ agent-reach installed', 'green');
  
  // Setup
  log('   Running agent-reach setup...', 'blue');
  run('agent-reach setup --safe', true);
  
  return true;
}

// --- Configure MCP ---

function configureMCP() {
  log('\n⚙️  Configuring MCP servers...', 'blue');
  
  const ompConfigPath = path.join(HOME, '.omp', 'mcp.json');
  
  let config = {};
  if (fs.existsSync(ompConfigPath)) {
    try {
      config = JSON.parse(fs.readFileSync(ompConfigPath, 'utf8'));
    } catch (err) {
      log('⚠️  Could not parse existing mcp.json', 'yellow');
    }
  }
  
  if (!config.mcpServers) {
    config.mcpServers = {};
  }
  
  // Add codebase-memory
  if (!config.mcpServers['codebase-memory']) {
    config.mcpServers['codebase-memory'] = {
      command: 'cbm',
      args: ['serve', '--stdio']
    };
    log('   Added codebase-memory MCP server', 'green');
  }
  
  // Add agent-reach
  if (!config.mcpServers['agent-reach']) {
    config.mcpServers['agent-reach'] = {
      command: 'agent-reach',
      args: ['mcp', '--stdio']
    };
    log('   Added agent-reach MCP server', 'green');
  }
  
  // Write config
  const ompDir = path.dirname(ompConfigPath);
  if (!fs.existsSync(ompDir)) {
    fs.mkdirSync(ompDir, { recursive: true });
  }
  
  fs.writeFileSync(ompConfigPath, JSON.stringify(config, null, 2));
  log(`✅ MCP config written: ${ompConfigPath}`, 'green');
}

// --- Main ---

function main() {
  log('\n🚀 1ai-skills MCP Tools Installer', 'blue');
  log('=' .repeat(50), 'blue');
  
  const cbmInstalled = installCodebaseMemory();
  const agentReachInstalled = installAgentReach();
  
  if (cbmInstalled || agentReachInstalled) {
    configureMCP();
  }
  
  log('\n' + '='.repeat(50), 'blue');
  
  if (cbmInstalled && agentReachInstalled) {
    log('✅ All MCP tools installed successfully!', 'green');
    log('\nNext steps:', 'blue');
    log('  1. Restart your AI agent session', 'blue');
    log('  2. Test cbm: cbm --version', 'blue');
    log('  3. Test agent-reach: agent-reach --version', 'blue');
    log('  4. Index a project: cbm cli index_repository \'{"repo_path": "."}\'', 'blue');
    log('  5. Search Twitter: agent-reach twitter search "AI agents" --limit 10', 'blue');
  } else {
    log('⚠️  Some tools failed to install', 'yellow');
    log('   See manual installation instructions in:', 'yellow');
    log('   - skill://codebase-memory-mcp', 'yellow');
    log('   - skill://agent-reach', 'yellow');
  }
  
  log('');
}

main();
