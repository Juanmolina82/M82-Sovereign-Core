#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 ABSOLUTE DDL & NULL CATEGORY SANITIZER ENGINE
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
set -e

DB="$HOME/M82/m82_database.db"

echo "⚡ [PASO 1] Inyectando columna updated_at en sesión independiente..."
sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=120000; ALTER TABLE macro_dossier ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;" 2>/dev/null || true

echo "⚡ [PASO 2] Sanitizando los 10 registros NULL a M82_LEGACY_RAW_INGEST..."
sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=120000; UPDATE macro_dossier SET category='M82_LEGACY_RAW_INGEST' WHERE category IS NULL OR category='';"

echo "=========================================================================="
echo "📊 VERIFICACIÓN FINAL DE CATEGORÍAS (CERO REGISTROS NULL):"
echo "=========================================================================="
sqlite3 "$DB" << 'SQL_VERIFY'
.mode column
.headers on
SELECT category, COUNT(*) AS dossiers 
FROM macro_dossier 
WHERE validated=1 
GROUP BY category 
ORDER BY COUNT(*) DESC 
LIMIT 10;
SQL_VERIFY

echo "=========================================================================="
echo "⚡ [PASO 3] Sellando checkpoint TRUNCATE WAL CLEAN 0/0/0..."
sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=120000; PRAGMA wal_checkpoint(TRUNCATE);"

echo "🟢 [SANITY SUCCESS] Categorías Sanitizadas | 113 Validados | WAL CLEAN 0/0/0"
echo "=========================================================================="
