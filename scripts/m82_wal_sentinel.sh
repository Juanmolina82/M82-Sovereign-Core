#!/usr/bin/env bash
# ==============================================================================
# M82 WAL SENTINEL — CHECKPOINTING Y MANTENIMIENTO WAL (60s)
# Node: Caracas HQ Node
# ==============================================================================

DB_PATH="$HOME/M82/m82_database.db"

while true; do
    if [ -f "$DB_PATH" ]; then
        sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(PASSIVE);" >/dev/null 2>&1
    fi
    sleep 60
done
