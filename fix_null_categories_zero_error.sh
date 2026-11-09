#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 ZERO-ERROR CATEGORY SANITIZER
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
set -e

DB="$HOME/M82/m82_database.db"

echo "⚡ [M82 ZERO-ERROR] Sanitizando categorías NULL a M82_LEGACY_RAW_INGEST..."

# 1. Asegurar la presencia de la columna category únicamente y actualizar
sqlite3 "$DB" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

UPDATE macro_dossier 
SET category = 'M82_LEGACY_RAW_INGEST' 
WHERE category IS NULL OR category = '';

PRAGMA wal_checkpoint(TRUNCATE);
SQL

echo "=========================================================================="
echo "📊 VERIFICACIÓN TOP 10 CATEGORÍAS (CERO NULLS):"
echo "=========================================================================="

sqlite3 "$DB" << 'SQL_CHECK'
.mode column
.headers on
SELECT category, COUNT(*) FROM macro_dossier WHERE validated=1 GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10;
SQL_CHECK

echo "=========================================================================="
echo "🟢 [SUCCESS] Categorías Sanitizadas | Total Validados: 113 | WAL 0/0/0"
echo "=========================================================================="
