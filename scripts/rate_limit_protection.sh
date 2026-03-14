#!/bin/bash
# JENDRALBOT Rate Limit Protection Script
# Automatically detects and handles Post Bridge rate limits

WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/rate_limit_log.txt"

# Check HTTP 500 errors
check_rate_limit() {
    local error_count=$(grep -c "HTTP 500" "$LOG_FILE" 2>/dev/null || echo "0")
    
    if [ "$error_count" -ge 3 ]; then
        return 0  # Rate limit detected
    fi
    return 1  # No rate limit
}

# Calculate dynamic delay
calculate_delay() {
    local post_number=$1
    local attempts=$2
    
    # Base delay: 2 minutes
    local base_delay=120
    
    # Add post progression component (exponential)
    local delay_multiplier=$(echo "scale=1; 1.1 ^ $post_number" | bc)
    delay_multiplier=$(echo "$delay_multiplier < 10 ? $delay_multiplier : 10" | bc)
    
    # Add attempt multiplier (exponential backoff)
    local attempt_multiplier=$((2 ** $attempts))
    attempt_multiplier=$(echo "$attempt_multiplier < 16 ? $attempt_multiplier : 16" | bc)
    
    # Calculate final delay
    local delay_seconds=$((base_delay * delay_multiplier * attempt_multiplier / 10))
    
    # Cap at 10 minutes
    delay_seconds=$(echo "$delay_seconds < 600 ? $delay_seconds : 600" | bc)
    
    echo "$delay_seconds"
}

# Main execution
main() {
    echo "Rate Limit Protection Active"
    echo "Monitoring HTTP 500 errors..."
    
    if check_rate_limit; then
        echo "⚠️  Rate limit detected!"
        echo "⏸️  Pausing for 15 minutes..."
        sleep 900
    fi
}

main "$@"