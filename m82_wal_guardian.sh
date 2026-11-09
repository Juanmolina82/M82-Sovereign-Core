#!/bin/bash
DB_PATH="$HOME/M82/m82_database.db"
WAL_PATH="$HOME/M82/m82_database.db-wal"

if [ -f "$WAL_PATH" ]; then
    SIZE_KB=$(du -k "$WAL_PATH" | cut -f1)
    if [ "$SIZE_KB" -gt 10240 ]; then
        sqlite3 "$DB_PATH" "PRAGMA busy_timeout=60000; PRAGMA wal_checkpoint(TRUNCATE);"
        echo "[WAL GUARDIAN] Truncated WAL file at ${SIZE_KB}KB"
    fi
fi
