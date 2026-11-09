#!/usr/bin/env bash
set -e

M82_DIR="$HOME/M82"
GALLERY_DIR="$HOME/storage/shared/Pictures/M82_Cards"

mkdir -p "$M82_DIR" "$HOME/M82_Backups" "$M82_DIR/desks" "$M82_DIR/scripts"
if [ -d "$HOME/storage/shared" ]; then
    mkdir -p "$GALLERY_DIR"
else
    mkdir -p "/sdcard/Pictures/M82_Cards"
fi

termux-wake-lock 2>/dev/null || true

sqlite3 "$M82_DIR/m82_database.db" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_source TEXT,
    headline TEXT UNIQUE,
    status TEXT DEFAULT 'PENDING',
    alpha_score REAL DEFAULT 0.0,
    asset_impact TEXT DEFAULT 'MACRO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS m82_daemons_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_name TEXT UNIQUE,
    desk_category TEXT,
    vector_type TEXT,
    status TEXT,
    last_heartbeat DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS price_ticks (
    asset TEXT PRIMARY KEY,
    bid REAL,
    ask REAL,
    last_price REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF_SQL

echo "✅ Base de datos SQLite3 WAL inicializada correctamente."
