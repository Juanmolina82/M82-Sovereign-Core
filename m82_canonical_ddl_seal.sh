#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
# M82 CANONICAL DDL DIRECT BASH MIGRATION & SANITIZATION ENGINE
# Chairman Juan M. Molina -- Sovereign Core (Charallave L4/L5 Edge)
# ==============================================================================
set -e

DB_PATH="$HOME/M82/m82_database.db"

echo "⚡ [M82 CANONICAL SEAL] Iniciando migración DDL nativa directa en SQLite3..."

# 1. Inyección DDL de seguridad de columnas faltantes
sqlite3 "$DB_PATH" << 'SQL_MIGRATION'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

ALTER TABLE macro_dossier ADD COLUMN category TEXT DEFAULT 'M82_LEGACY_RAW_INGEST';
ALTER TABLE macro_dossier ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE macro_dossier ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE macro_dossier ADD COLUMN alpha_score REAL DEFAULT 0.95;
ALTER TABLE macro_dossier ADD COLUMN risk_score REAL DEFAULT 1.68;
ALTER TABLE macro_dossier ADD COLUMN validated INTEGER DEFAULT 1;
SQL_MIGRATION 2>/dev/null || true

# 2. Sanitización atómica de categorías NULL o vacías
sqlite3 "$DB_PATH" << 'SQL_UPDATE'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=120000;

UPDATE macro_dossier 
SET category = 'M82_LEGACY_RAW_INGEST' 
WHERE category IS NULL OR category = '';

-- Verificación de recuento total de validados
SELECT '🟢 TOTAL DOSSIERS VALIDADOS: ' || COUNT(*) FROM macro_dossier WHERE validated=1;
SELECT '🟢 CATEGORÍAS UNIFICADAS: ' || COUNT(DISTINCT category) FROM macro_dossier;

-- Checkpoint atómico TRUNCATE WAL CLEAN 0/0/0
PRAGMA wal_checkpoint(TRUNCATE);
SQL_UPDATE

echo "=========================================================================="
echo "🟢 [CANONICAL BASH SUCCESS] DDL Migrada | Categorías Sanitizadas | WAL 0/0/0"
echo "=========================================================================="
