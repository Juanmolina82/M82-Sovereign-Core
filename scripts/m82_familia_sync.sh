#!/usr/bin/env bash
set -euo pipefail

FAM_DB="$HOME/M82/sqlite/m82_familia.db"
LOG_FILE="$HOME/M82/logs/familia/kronos_sync.log"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Running Kronos T8 Sunday Council Audit..." >> "$LOG_FILE"

sqlite3 "$FAM_DB" << 'SQL' >> "$LOG_FILE"
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

UPDATE rituales SET ultimo_ejecutado = CURRENT_TIMESTAMP WHERE codigo = 'T8_KRONOS_COUNCIL';

SELECT '=== ESTADO INTEGRAL DINASTÍA M82 ===';
SELECT id, nombre, rol_m82, estado FROM familia_miembros;
SELECT '=== RITUALES Y KANBAN ===';
SELECT codigo, frecuencia, ultimo_ejecutado FROM rituales;
SQL

PRAGMA_CHECK=$(sqlite3 "$FAM_DB" "PRAGMA wal_checkpoint(PASSIVE);")
echo "WAL Passive Checkpoint: $PRAGMA_CHECK" >> "$LOG_FILE"
