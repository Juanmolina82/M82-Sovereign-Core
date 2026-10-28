#!/usr/bin/env bash
# ==============================================================================
# M82 BACKUP GUARD — COPIA INMUTABLE
# Node: Caracas HQ Node
# ==============================================================================

DB_PATH="$HOME/M82/m82_database.db"
BACKUP_DIR="$HOME/M82/backups"

mkdir -p "$BACKUP_DIR"

if [ -f "$DB_PATH" ]; then
    sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; VACUUM INTO '$BACKUP_DIR/m82_database_backup.db';" 2>/dev/null || \
    cp "$DB_PATH" "$BACKUP_DIR/m82_database_backup.db"
fi
