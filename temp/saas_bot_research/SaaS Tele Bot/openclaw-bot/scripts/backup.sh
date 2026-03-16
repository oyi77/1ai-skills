#!/bin/bash
# =============================================================================
# OPENCLAW BOT - BACKUP SCRIPT
# =============================================================================
# This script performs database and file backups
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

# Default values (override with environment variables)
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-openclaw}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-}"

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"
REDIS_PASSWORD="${REDIS_PASSWORD:-}"

BACKUP_DIR="${BACKUP_DIR:-./backups}"
S3_BUCKET="${S3_BUCKET:-openclaw-backups}"
S3_REGION="${S3_REGION:-ap-southeast-1}"

RETENTION_DAYS="${RETENTION_DAYS:-30}"

# =============================================================================
# FUNCTIONS
# =============================================================================

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

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                   OPENCLAW BOT BACKUP                         ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo "Time: $(date)"
    echo "Backup Directory: $BACKUP_DIR"
    echo ""
}

# =============================================================================
# BACKUP FUNCTIONS
# =============================================================================

backup_postgresql() {
    log_info "Starting PostgreSQL backup..."
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/postgresql_${DB_NAME}_${TIMESTAMP}.sql.gz"
    
    # Create backup directory if not exists
    mkdir -p "$BACKUP_DIR"
    
    # Set PGPASSWORD for non-interactive authentication
    export PGPASSWORD="$DB_PASSWORD"
    
    # Perform backup
    if pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" --verbose 2>/dev/null | gzip > "$BACKUP_FILE"; then
        log_success "PostgreSQL backup completed: $BACKUP_FILE"
        
        # Get file size
        FILESIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        log_info "Backup size: $FILESIZE"
        
        return 0
    else
        log_error "PostgreSQL backup failed"
        return 1
    fi
}

backup_redis() {
    log_info "Starting Redis backup..."
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/redis_${TIMESTAMP}.rdb"
    
    # Create backup directory if not exists
    mkdir -p "$BACKUP_DIR"
    
    # Trigger Redis BGSAVE
    if [ -n "$REDIS_PASSWORD" ]; then
        redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" BGSAVE
    else
        redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" BGSAVE
    fi
    
    # Wait for BGSAVE to complete
    log_info "Waiting for Redis BGSAVE to complete..."
    sleep 5
    
    # Copy RDB file
    REDIS_DIR=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" CONFIG GET dir | tail -1)
    REDIS_RDB=$(redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" CONFIG GET dbfilename | tail -1)
    
    if cp "$REDIS_DIR/$REDIS_RDB" "$BACKUP_FILE"; then
        log_success "Redis backup completed: $BACKUP_FILE"
        return 0
    else
        log_error "Redis backup failed"
        return 1
    fi
}

upload_to_s3() {
    log_info "Uploading backups to S3..."
    
    if ! command -v aws &> /dev/null; then
        log_warning "AWS CLI not found, skipping S3 upload"
        return 1
    fi
    
    S3_PATH="s3://$S3_BUCKET/backups/$(date +%Y/%m/%d)"
    
    if aws s3 sync "$BACKUP_DIR" "$S3_PATH" --region "$S3_REGION"; then
        log_success "Backups uploaded to S3: $S3_PATH"
        return 0
    else
        log_error "S3 upload failed"
        return 1
    fi
}

cleanup_old_backups() {
    log_info "Cleaning up old backups (retention: $RETENTION_DAYS days)..."
    
    # Local cleanup
    find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete
    log_success "Local cleanup completed"
    
    # S3 cleanup (if configured)
    if command -v aws &> /dev/null && [ -n "$S3_BUCKET" ]; then
        log_info "Cleaning up S3 backups..."
        
        CUTOFF_DATE=$(date -d "$RETENTION_DAYS days ago" +%Y-%m-%d 2>/dev/null || date -v-${RETENTION_DAYS}d +%Y-%m-%d)
        
        aws s3 ls "s3://$S3_BUCKET/backups/" --recursive | \
        while read -r line; do
            FILE_DATE=$(echo "$line" | awk '{print $1}')
            FILE_PATH=$(echo "$line" | awk '{$1=$2=$3=""; print $0}' | sed 's/^ *//')
            
            if [[ "$FILE_DATE" < "$CUTOFF_DATE" ]]; then
                aws s3 rm "s3://$S3_BUCKET/$FILE_PATH"
            fi
        done
        
        log_success "S3 cleanup completed"
    fi
}

verify_backup() {
    local backup_file=$1
    
    log_info "Verifying backup: $backup_file"
    
    if [ -f "$backup_file" ]; then
        # Check if file is not empty
        if [ -s "$backup_file" ]; then
            log_success "Backup file exists and is not empty"
            
            # Try to gunzip if it's a .gz file
            if [[ "$backup_file" == *.gz ]]; then
                if gunzip -t "$backup_file" 2>/dev/null; then
                    log_success "Backup file is valid gzip"
                    return 0
                else
                    log_error "Backup file is corrupted (invalid gzip)"
                    return 1
                fi
            fi
            
            return 0
        else
            log_error "Backup file is empty"
            return 1
        fi
    else
        log_error "Backup file not found"
        return 1
    fi
}

# =============================================================================
# MAIN
# =============================================================================

print_header

# Parse arguments
BACKUP_TYPE="${1:-all}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Perform backups based on type
case $BACKUP_TYPE in
    postgres|postgresql|db)
        backup_postgresql
        ;;
    redis|cache)
        backup_redis
        ;;
    all|full)
        backup_postgresql
        backup_redis
        upload_to_s3
        cleanup_old_backups
        ;;
    cleanup)
        cleanup_old_backups
        ;;
    *)
        echo "Usage: $0 [postgres|redis|all|cleanup]"
        echo ""
        echo "Options:"
        echo "  postgres  - Backup PostgreSQL only"
        echo "  redis     - Backup Redis only"
        echo "  all       - Full backup (default)"
        echo "  cleanup   - Clean up old backups only"
        exit 1
        ;;
esac

echo ""
log_success "Backup process completed!"
echo ""
