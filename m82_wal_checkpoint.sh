#!/usr/bin/env bash
# M82 WAL AUTO-CHECKPOINT & TRUNCATE
DB="$HOME/M82/m82_database.db"
sqlite3 "$DB" "PRAGMA busy_timeout=15000; PRAGMA wal_checkpoint(TRUNCATE);"
echo "🧹 [$(date '+%Y-%m-%d %H:%M:%S')] WAL Checkpoint ejecutado con éxito." >> ~/M82/wal_maint.log
