#!/data/data/com.termux/files/usr/bin/bash
set -e

DB_PATH="$HOME/M82/m82_database.db"

echo "⚡ [M82 DDL FIX] Agregando columna alpha_score a macro_dossier..."

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 1. Agregar columna si no existe (idempotente)
ALTER TABLE macro_dossier ADD COLUMN alpha_score REAL DEFAULT 0.0;
SQL 2>/dev/null || echo "Info: Columna alpha_score ya activa en macro_dossier."

sqlite3 "$DB_PATH" << 'SQL'
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=60000;

-- 2. Re-inyección atómica del registro en macro_dossier
INSERT OR REPLACE INTO macro_dossier (source, category, headline, risk_score, m82_tag, alpha_score)
VALUES (
  'REFINITIV_LSEG_CLOSE_23OCT',
  'EQUITIES_AI_ENERGY_CORRELATION',
  'META Q3 CapEx $34.9B FCF -$2.12B + TSLA CapEx cut $20B -> Nasdaq -2.6% | Brent $112 Hormuz Strikes -> Off-Hormuz Merey 16 $93.92 ITM Quad-SPVs',
  1.68,
  'META_TSLA_DROP_HORMUZ_LINK',
  0.92
);

PRAGMA wal_checkpoint(TRUNCATE);
SELECT '🟢 MACRO_DOSSIER REPARADO Y CHECKPOINTED 0/0/0' AS status;
SQL
