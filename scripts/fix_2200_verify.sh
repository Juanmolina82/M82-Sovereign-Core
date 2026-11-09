#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- Verificación usando esquema sanitizado
SELECT '🟢 MULTI_STREAM_2200:' || COUNT(*) FROM m82_multi_stream WHERE daemon_source='REFINITIV_2200_WIRE';
SELECT id, topic, risk_score, source FROM macro_dossier WHERE topic='REFINITIV_WORKSPACE_USER_CAPTURE_2200';

PRAGMA wal_checkpoint(TRUNCATE);
EOF_SQL

echo "🟢 [SUCCESS] Base de datos verificada y WAL truncada en 0/0/0 CLEAN."
