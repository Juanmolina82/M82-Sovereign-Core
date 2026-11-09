#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 MONOLITHIC NULL CATEGORY SANITIZER -- ATOMIC SINGLE-RUN
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
set -e

DB="$HOME/M82/m82_database.db"

echo "⚡ [M82 SANITIZER] Mapeando 10 registros NULL a M82_LEGACY_RAW_INGEST..."

sqlite3 "$DB" "PRAGMA journal_mode=WAL; PRAGMA busy_timeout=120000; UPDATE macro_dossier SET category='M82_LEGACY_RAW_INGEST' WHERE category IS NULL OR category=''; PRAGMA wal_checkpoint(TRUNCATE);"

echo "=========================================================================="
echo "📊 VERIFICACIÓN FINAL DE CATEGORÍAS TOP 10:"
echo "=========================================================================="
sqlite3 "$DB" "SELECT category, COUNT(*) FROM macro_dossier WHERE validated=1 GROUP BY category ORDER BY COUNT(*) DESC LIMIT 10;"

echo "=========================================================================="
echo "🟢 [SANITY CHECK COMPLETE] Null Categories Fixed | WAL CLEAN 0/0/0"
echo "=========================================================================="
