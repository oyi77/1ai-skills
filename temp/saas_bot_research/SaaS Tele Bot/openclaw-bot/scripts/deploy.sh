#!/bin/bash
# =============================================================================
# OPENCLAW BOT - DEPLOYMENT SCRIPT
# =============================================================================
# This script handles deployment to various environments
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# =============================================================================
# CONFIGURATION
# =============================================================================

ENVIRONMENT=""
VERSION=""
SKIP_TESTS=false
SKIP_BUILD=false
FORCE=false

# =============================================================================
# FUNCTIONS
# =============================================================================

print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --environment    Target environment (development|staging|production)"
    echo "  -v, --version        Version to deploy (default: from package.json)"
    echo "  --skip-tests         Skip running tests"
    echo "  --skip-build         Skip build step"
    echo "  -f, --force          Force deployment without confirmation"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -e staging"
    echo "  $0 -e production -v 3.0.1"
    echo "  $0 -e production --skip-tests -f"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -e|--environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            -v|--version)
                VERSION="$2"
                shift 2
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --skip-build)
                SKIP_BUILD=true
                shift
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            -h|--help)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
}

validate_environment() {
    if [ -z "$ENVIRONMENT" ]; then
        log_error "Environment is required"
        print_usage
        exit 1
    fi
    
    case $ENVIRONMENT in
        development|staging|production)
            ;;
        *)
            log_error "Invalid environment: $ENVIRONMENT"
            log_info "Valid environments: development, staging, production"
            exit 1
            ;;
    esac
}

get_version() {
    if [ -z "$VERSION" ]; then
        VERSION=$(node -p "require('./package.json').version")
    fi
    log_info "Deploying version: $VERSION"
}

confirm_deployment() {
    if [ "$FORCE" = true ]; then
        return 0
    fi
    
    echo ""
    log_warning "You are about to deploy to ${YELLOW}$ENVIRONMENT${NC}"
    log_warning "Version: ${YELLOW}$VERSION${NC}"
    echo ""
    read -p "Are you sure? (yes/no): " CONFIRM
    
    if [ "$CONFIRM" != "yes" ]; then
        log_info "Deployment cancelled"
        exit 0
    fi
}

run_tests() {
    if [ "$SKIP_TESTS" = true ]; then
        log_warning "Skipping tests"
        return 0
    fi
    
    log_info "Running tests..."
    
    if npm test; then
        log_success "All tests passed"
    else
        log_error "Tests failed"
        exit 1
    fi
}

run_build() {
    if [ "$SKIP_BUILD" = true ]; then
        log_warning "Skipping build"
        return 0
    fi
    
    log_info "Building project..."
    
    if npm run build; then
        log_success "Build completed"
    else
        log_error "Build failed"
        exit 1
    fi
}

deploy_docker() {
    log_info "Building Docker image..."
    
    IMAGE_NAME="openclaw-bot"
    IMAGE_TAG="$VERSION"
    
    docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
    docker tag "$IMAGE_NAME:$IMAGE_TAG" "$IMAGE_NAME:latest"
    
    log_success "Docker image built: $IMAGE_NAME:$IMAGE_TAG"
    
    # Push to registry if configured
    if [ -n "$DOCKER_REGISTRY" ]; then
        log_info "Pushing to registry..."
        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
        docker push "$DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
        log_success "Image pushed to registry"
    fi
}

deploy_kubernetes() {
    log_info "Deploying to Kubernetes..."
    
    NAMESPACE="openclaw-$ENVIRONMENT"
    
    # Update image in deployment
    kubectl set image deployment/openclaw-bot \
        openclaw-bot="$DOCKER_REGISTRY/openclaw-bot:$VERSION" \
        -n "$NAMESPACE"
    
    # Wait for rollout
    kubectl rollout status deployment/openclaw-bot -n "$NAMESPACE" --timeout=300s
    
    log_success "Kubernetes deployment completed"
}

deploy_staging() {
    log_info "Deploying to STAGING..."
    
    run_tests
    run_build
    deploy_docker
    
    if command -v kubectl &> /dev/null; then
        deploy_kubernetes
    else
        log_warning "kubectl not found, skipping Kubernetes deployment"
    fi
    
    log_success "Staging deployment completed"
}

deploy_production() {
    log_info "Deploying to PRODUCTION..."
    
    # Additional checks for production
    log_info "Running production checks..."
    
    # Check if on main branch
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "main" ]; then
        log_error "Not on main branch. Current: $CURRENT_BRANCH"
        exit 1
    fi
    
    # Check if working directory is clean
    if [ -n "$(git status --porcelain)" ]; then
        log_error "Working directory is not clean"
        exit 1
    fi
    
    run_tests
    run_build
    
    # Create git tag
    log_info "Creating git tag v$VERSION..."
    git tag -a "v$VERSION" -m "Release v$VERSION"
    git push origin "v$VERSION"
    
    deploy_docker
    deploy_kubernetes
    
    log_success "Production deployment completed"
    log_info "Version v$VERSION is now live!"
}

# =============================================================================
# MAIN
# =============================================================================

parse_args "$@"
validate_environment
get_version
confirm_deployment

case $ENVIRONMENT in
    development)
        run_tests
        run_build
        log_success "Development deployment ready"
        log_info "Start with: npm run dev"
        ;;
    staging)
        deploy_staging
        ;;
    production)
        deploy_production
        ;;
esac

echo ""
log_success "Deployment process completed!"
