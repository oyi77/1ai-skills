#!/bin/bash
# =============================================================================
# OPENCLAW BOT - SETUP SCRIPT
# =============================================================================
# This script sets up the development environment for OpenClaw Bot
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# FUNCTIONS
# =============================================================================

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                    OPENCLAW BOT SETUP                         ║"
    echo "║              AI Video Marketing SaaS Platform                 ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

# =============================================================================
# MAIN SCRIPT
# =============================================================================

print_header

# Check if running in correct directory
if [ ! -f "package.json" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_info "Starting setup process..."
echo ""

# =============================================================================
# CHECK PREREQUISITES
# =============================================================================

print_info "Checking prerequisites..."

MISSING_DEPS=0

check_command "node" || MISSING_DEPS=1
check_command "npm" || MISSING_DEPS=1
check_command "git" || MISSING_DEPS=1

if [ $MISSING_DEPS -eq 1 ]; then
    print_error "Please install missing dependencies and try again"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 20 ]; then
    print_error "Node.js 20+ is required. Current version: $(node -v)"
    exit 1
fi

print_success "Node.js version: $(node -v)"
print_success "npm version: $(npm -v)"

# =============================================================================
# INSTALL DEPENDENCIES
# =============================================================================

echo ""
print_info "Installing dependencies..."

if npm install; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# =============================================================================
# SETUP ENVIRONMENT
# =============================================================================

echo ""
print_info "Setting up environment..."

if [ -f ".env" ]; then
    print_warning ".env file already exists"
    read -p "Do you want to overwrite it? (y/N): " OVERWRITE
    if [[ $OVERWRITE =~ ^[Yy]$ ]]; then
        cp .env.example .env
        print_success ".env file created from template"
    fi
else
    cp .env.example .env
    print_success ".env file created from template"
fi

print_warning "Please edit .env file with your actual configuration values"

# =============================================================================
# SETUP DATABASE
# =============================================================================

echo ""
print_info "Setting up database..."

# Check if PostgreSQL is running
if pg_isready -q 2>/dev/null; then
    print_success "PostgreSQL is running"
    
    read -p "Do you want to run database migrations? (y/N): " RUN_MIGRATIONS
    if [[ $RUN_MIGRATIONS =~ ^[Yy]$ ]]; then
        if npm run migrate:dev; then
            print_success "Database migrations completed"
        else
            print_error "Failed to run migrations"
            print_info "You can run migrations later with: npm run migrate:dev"
        fi
    fi
else
    print_warning "PostgreSQL is not running"
    print_info "Please start PostgreSQL and run migrations manually:"
    print_info "  npm run migrate:dev"
fi

# Check if Redis is running
if redis-cli ping > /dev/null 2>&1; then
    print_success "Redis is running"
else
    print_warning "Redis is not running"
    print_info "Please start Redis for full functionality"
fi

# =============================================================================
# SETUP GIT HOOKS
# =============================================================================

echo ""
print_info "Setting up Git hooks..."

if [ -d ".git" ]; then
    # Setup pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook for OpenClaw Bot

echo "Running pre-commit checks..."

# Run linter
if ! npm run lint; then
    echo "Linting failed. Please fix errors before committing."
    exit 1
fi

# Run type check
if ! npm run typecheck; then
    echo "Type checking failed. Please fix errors before committing."
    exit 1
fi

echo "Pre-commit checks passed!"
EOF
    chmod +x .git/hooks/pre-commit
    print_success "Pre-commit hook installed"
else
    print_warning "Not a Git repository. Skipping Git hooks setup."
fi

# =============================================================================
# BUILD PROJECT
# =============================================================================

echo ""
print_info "Building project..."

if npm run build; then
    print_success "Build completed successfully"
else
    print_warning "Build had issues, but setup can continue"
fi

# =============================================================================
# FINAL INSTRUCTIONS
# =============================================================================

echo ""
print_success "Setup completed!"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo ""
echo "1. Edit ${YELLOW}.env${NC} file with your configuration:"
echo "   - Telegram Bot Token"
echo "   - Database credentials"
echo "   - API keys"
echo ""
echo "2. Start the development server:"
echo "   ${YELLOW}npm run dev${NC}"
echo ""
echo "3. Run tests:"
echo "   ${YELLOW}npm test${NC}"
echo ""
echo "4. View documentation:"
echo "   ${YELLOW}docs/MASTER_PROMPT.md${NC}"
echo ""
echo -e "${BLUE}Happy coding! 🚀${NC}"
echo ""
