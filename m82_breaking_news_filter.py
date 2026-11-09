#!/usr/bin/env bash
set -euo pipefail

DB_PATH="$HOME/M82/m82_database.db"

sqlite3 "$DB_PATH" << 'EOF_SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Marcar como PROCESSED todos los avisos de sistema/timestamps para ignorarlos en tarjetas
UPDATE m82_multi_stream 
SET status = 'SYSTEM_IGNORE' 
WHERE headline LIKE '%timestamp%' 
   OR headline LIKE '%LSEG_SECRET%' 
   OR headline LIKE '%Esperando validación%';

-- 2. Limpiar duplicados manteniendo solo la última entrada por titular
DELETE FROM m82_multi_stream 
WHERE id NOT IN (
    SELECT MAX(id) 
    FROM m82_multi_stream 
    GROUP BY headline
);

SELECT '🟢 FILTRO APLICADO — Registros listos para Breaking News:' || COUNT(*) 
FROM m82_multi_stream 
WHERE status='PENDING';
EOF_SQL

echo "✅ [M82 AGI] Base de datos depurada. Solo Breaking Wires activos en cola."
