#!/bin/bash
mkdir -p ~/M82/logs /sdcard/Pictures/M82_Cards

sqlite3 ~/M82/m82_database.db << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

CREATE TABLE IF NOT EXISTS m82_multi_stream (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    daemon_source TEXT NOT NULL,
    headline TEXT NOT NULL,
    status TEXT CHECK(status IN ('PENDING', 'VERIFIED', 'DISPATCHED')) DEFAULT 'PENDING',
    alpha_score REAL DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
SQL

echo "[M82 DB] Initialized in WAL mode (busy_timeout=60000)."
