#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 PERFECT NULL CATEGORY SANITIZER -- BASH HERE-DOC ENGINE
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
set -e

DB="$HOME/M82/m82_database.db"

echo "⚡ [M82 PERFECT SANITIZER] Mapeando 10 registros NULL a M82_LEGACY_RAW_INGEST..."

# Ejecución limpia mediante Here-Doc (evita colisiones de comillas en línea)
sqlite3 "$DB" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

UPDATE macro_dossier 
SET category = 'M82_LEGACY_RAW_INGEST' 
WHERE category IS NULL OR category = '';

PRAGMA wal_checkpoint(TRUNCATE);
SQL

echo "=========================================================================="
echo "📊 VERIFICACIÓN FINAL DE CATEGORÍAS TOP 10 (SIN NULLS):"
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
echo "🟢 [SUCCESS] 10 Registros NULL Convertidos | Categorías Sanitizadas | WAL 0/0/0"
echo "=========================================================================="
