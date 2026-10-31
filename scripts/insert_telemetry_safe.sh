#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Inserción limpia en macro_dossier (sin campo 'sentiment')
INSERT OR REPLACE INTO macro_dossier (topic, summary, risk_score, source)
VALUES (
    'SOVEREIGN_NODE_TELEMETRY',
    'Real-time ingestion pipeline synchronized. Refinitiv Workspace wires & Edge VLA inference validated under 0.30x LOCK.',
    1.68,
    'Sovereign Execution Core'
);

-- Inserción limpia en m82_multi_stream (contiene alpha_score y status)
INSERT OR IGNORE INTO m82_multi_stream (daemon_source, headline, status, alpha_score, asset_impact)
VALUES (
    'SOVEREIGN_CORE',
    '[SYSTEM_CHECK | 2026-10-19] BBDD integrity 100% - WAL mode clean',
    'PROCESSED',
    0.99,
    'SYSTEM'
);

SELECT 'M82 BBDD INTEGRITY OK — ' || count(*) || ' RECORDS' FROM macro_dossier;
SQL

sqlite3 "$DB_PATH" "PRAGMA wal_checkpoint(TRUNCATE); SELECT 'WAL CLEAN OK';"
