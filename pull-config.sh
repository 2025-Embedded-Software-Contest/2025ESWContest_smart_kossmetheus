#!/bin/bash

# CareDian Home Assistant Config Pull Script
# This script pulls the latest configuration from GitHub repository

CONFIG_DIR="/config"
LOG_FILE="/config/pull-config.log"

echo "$(date): Starting config pull from GitHub..." | tee -a "$LOG_FILE"

# Change to config directory
cd "$CONFIG_DIR" || {
    echo "$(date): ERROR - Cannot change to config directory" | tee -a "$LOG_FILE"
    exit 1
}

# Check if git repository exists
if [ ! -d ".git" ]; then
    echo "$(date): ERROR - Not a git repository" | tee -a "$LOG_FILE"
    exit 1
fi

# Stash any local changes to prevent conflicts
echo "$(date): Stashing local changes..." | tee -a "$LOG_FILE"
git stash

# Pull latest changes from origin (updated to use main branch)
echo "$(date): Pulling latest changes..." | tee -a "$LOG_FILE"
if git pull origin main; then
    echo "$(date): Successfully pulled latest configuration" | tee -a "$LOG_FILE"
    
    # Restart Home Assistant to apply changes
    echo "$(date): Restarting Home Assistant..." | tee -a "$LOG_FILE"
    if command -v ha &> /dev/null; then
        ha core restart
        echo "$(date): Home Assistant restart initiated" | tee -a "$LOG_FILE"
    else
        echo "$(date): WARNING - 'ha' command not available, manual restart required" | tee -a "$LOG_FILE"
    fi
else
    echo "$(date): ERROR - Failed to pull changes" | tee -a "$LOG_FILE"
    exit 1
fi

echo "$(date): Config pull completed successfully" | tee -a "$LOG_FILE"