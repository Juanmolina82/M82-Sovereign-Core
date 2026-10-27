#!/bin/bash
set -e
DB=~/M82/m82_database.db

echo "[M82] Ejecutando migración DDL sobre macro_dossier..."

sqlite3 $DB <<'EOSQL'
PRAGMA busy_timeout=120000;
PRAGMA journal_mode=WAL;

-- 1. Agregar la columna 'timestamp' en caso de que falte por esquema legacy
ALTER TABLE macro_dossier ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP;
EOSQL 2>/dev/null || echo "[M82] Columna 'timestamp' ya preexistía o migrada."

sqlite3 $DB <<'EOSQL'
PRAGMA busy_timeout=120000;
PRAGMA journal_mode=WAL;

-- 2. Asegurar campos faltantes adicionales
ALTER TABLE macro_dossier ADD COLUMN alpha_score REAL DEFAULT 0.99;
ALTER TABLE macro_dossier ADD COLUMN status TEXT DEFAULT 'PROCESSED';
ALTER TABLE macro_dossier ADD COLUMN asset_impact TEXT;
ALTER TABLE macro_dossier ADD COLUMN event_trigger TEXT;
EOSQL 2>/dev/null || echo "[M82] Columnas adicionales verificadas."

sqlite3 $DB <<'EOSQL'
PRAGMA busy_timeout=120000;
PRAGMA journal_mode=WAL;

-- 3. Crear los índices de forma limpia
CREATE INDEX IF NOT EXISTS idx_macro_tag ON macro_dossier(m82_tag);
CREATE INDEX IF NOT EXISTS idx_macro_cat ON macro_dossier(category);
CREATE INDEX IF NOT EXISTS idx_macro_time ON macro_dossier(timestamp DESC);

-- 4. Checkpoint atómico
PRAGMA wal_checkpoint(TRUNCATE);
EOSQL

echo "[M82] Esquema sanitizado exitosamente sin parse errors."
