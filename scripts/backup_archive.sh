#!/usr/bin/env bash
# Backup archive folder to remote storage (example using rsync)
set -e
ARCHIVE_DIR="$BASE/archive"
DESTINATION="/mnt/backup/berkahkarya-archive"
mkdir -p "$DESTINATION"
rsync -av --delete "$ARCHIVE_DIR/" "$DESTINATION/"
 echo "Archive backup completed at $(date)"
